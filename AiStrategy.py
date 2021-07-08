from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
import logging
from pandas import DataFrame
from freqtrade.resolvers import StrategyResolver
from itertools import combinations
from functools import reduce
import talib.abstract as ta

logger = logging.getLogger(__name__)
'''
2021-07-05 17:31:14,913 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy AiStrategy from '/freqtrade/user_data/strategies/AiStrategy.py'...
2021-07-05 17:31:14,914 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2021-07-05 17:31:14,916 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_mean_threshold = 0.01
2021-07-05 17:31:14,917 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_strategies = 12
2021-07-05 17:31:14,918 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_mean_threshold = 0.566
2021-07-05 17:31:14,919 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_strategies = 52
2021-07-05 17:31:14,920 - AiStrategy - INFO - Buy stratrategies: ('CombinedBinHClucAndMADV5', 'CombinedBinHClucAndMADV6', 'NostalgiaForInfinityV4', 'SMAOffsetProtectOpt')
2021-07-05 17:31:14,920 - AiStrategy - INFO - Sell stratrategies: ('CombinedBinHAndClucV8', 'NostalgiaForInfinityV4')
'''

# DO NOT MODIFY THE STRATEGY LIST
# You'll need to run hyperopt to find the best strategy combination for buy/sell.
# Also, make sure you have all strategies listed here in user_data/strategies
STRATEGIES = [
    "CombinedBinHClucAndMADV5",
    "CombinedBinHClucAndMADV6",
    "CombinedBinHAndClucV8",
    "CombinedBinHClucAndMADV9",
    "NostalgiaForInfinityV4",
    "SMAOffsetProtectOpt",
    
]

STRAT_COMBINATIONS = reduce(
    lambda x, y: list(combinations(STRATEGIES, y)) + x, range(len(STRATEGIES)+1), []
)


class AiStrategy(IStrategy):
    loaded_strategies = {}
    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True
    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 400
    informative_timeframe = '1h'

    
    buy_mean_threshold = DecimalParameter(0.0, 1, default=0.5, load=True)
    sell_mean_threshold = DecimalParameter(0.0, 1, default=0.5, load=True)
    buy_strategies = IntParameter(0, len(STRAT_COMBINATIONS), default=0, load=True)
    sell_strategies = IntParameter(0, len(STRAT_COMBINATIONS), default=0, load=True)
    # print(len(STRAT_COMBINATIONS))

    # Buy hyperspace params:
      
    
    buy_params = {
         "buy_mean_threshold": 0.01,
         "buy_strategies": 12,
    }

    # # Sell hyperspace params:
    sell_params = {
         "sell_mean_threshold": 0.566,
         "sell_strategies": 52,
     }

    # ROI table:
    # minimal_roi = {
    #     "0": 0.056,
    #     "22": 0.042,
    #     "72": 0.021,
    #     "126": 0
    # }
    # ROI table:
    minimal_roi = {
        "0": 0.242,
        "28": 0.046,
        "68": 0.035,
        "137": 0
    }

    # Stoploss:
    stoploss = -0.203

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.041
    trailing_only_offset_is_reached = True

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        logger.info(f"Buy stratrategies: {STRAT_COMBINATIONS[self.buy_strategies.value]}")
        logger.info(f"Sell stratrategies: {STRAT_COMBINATIONS[self.sell_strategies.value]}")

    def informative_pairs(self):
        pairs = self.dp.current_whitelist()
        informative_pairs = [(pair, self.informative_timeframe) for pair in pairs]
        return informative_pairs

    def get_strategy(self, strategy_name):
        strategy = self.loaded_strategies.get(strategy_name)
        if not strategy:
            config = self.config
            config["strategy"] = strategy_name
            strategy = StrategyResolver.load_strategy(config)

        strategy.dp = self.dp
        strategy.wallets = self.wallets
        self.loaded_strategies[strategy_name] = strategy
        return strategy

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # dataframe['ai_ema_100'] = ta.EMA(dataframe, timeperiod=100)
        # dataframe['ai_ema_200'] = ta.EMA(dataframe, timeperiod=200)
        # dataframe['ai_sma_200'] = ta.SMA(dataframe, timeperiod=200)
        # dataframe['ai_sma_200_dec'] = dataframe['ai_sma_200'] < dataframe['ai_sma_200'].shift(20)
        

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        strategies = STRAT_COMBINATIONS[self.buy_strategies.value]
        for strategy_name in strategies:
            strategy = self.get_strategy(strategy_name)
            strategy_indicators = strategy.advise_indicators(dataframe, metadata)
            dataframe[f"strat_buy_signal_{strategy_name}"] = strategy.advise_buy(
                strategy_indicators, metadata
            )["buy"]
            # values = dataframe[f"strat_buy_signal_{strategy_name}"].tolist()
            # logger.info(f"buy_signals_{strategy_name}: {values}")

        dataframe['buy'] = (
            dataframe.filter(like='strat_buy_signal_').mean(axis=1) > self.buy_mean_threshold.value
        ).astype(int)
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        strategies = STRAT_COMBINATIONS[self.sell_strategies.value]
        for strategy_name in strategies:
            strategy = self.get_strategy(strategy_name)
            strategy_indicators = strategy.advise_indicators(dataframe, metadata)
            # print(strategy_indicators)
            dataframe[f"strat_sell_signal_{strategy_name}"] = strategy.advise_sell(
                strategy_indicators, metadata
            )["sell"]
            # values = dataframe[f"strat_sell_signal_{strategy_name}"].tolist()
            # logger.info(f"sell_signals_{strategy_name}: {values}")

        dataframe['sell'] = (
            dataframe.filter(like='strat_sell_signal_').mean(axis=1) > self.sell_mean_threshold.value
        ).astype(int)
        return dataframe
