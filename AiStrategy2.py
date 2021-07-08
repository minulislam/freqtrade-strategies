from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
import logging
from pandas import DataFrame
from freqtrade.resolvers import StrategyResolver
from itertools import combinations
from functools import reduce

logger = logging.getLogger(__name__)
'''
2021-07-05 17:31:15,086 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy AiStrategy2 from '/freqtrade/user_data/strategies/AiStrategy2.py'...
2021-07-05 17:31:15,088 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2021-07-05 17:31:15,088 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_mean_threshold = 0.01
2021-07-05 17:31:15,089 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_strategies = 61
2021-07-05 17:31:15,089 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_mean_threshold = 0.566
2021-07-05 17:31:15,090 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_strategies = 35
2021-07-05 17:31:15,090 - AiStrategy2 - INFO - Buy stratrategies: ('SMAOffsetProtectOpt',)
2021-07-05 17:31:15,091 - AiStrategy2 - INFO - Sell stratrategies: ('CombinedBinHClucAndMADV6', 'CombinedBinHClucAndMADV9', 'SMAOffsetProtectOpt')

'''


STRATEGIES = [
    "CombinedBinHClucAndMADV5",
    "CombinedBinHClucAndMADV6",
    "CombinedBinHAndClucV8",
    "CombinedBinHClucAndMADV9",
    "SMAOffsetProtectOpt",
    "NostalgiaForInfinityV4",
]
STRAT_COMBINATIONS = reduce(
    lambda x, y: list(combinations(STRATEGIES, y)) + x, range(len(STRATEGIES)+1), []
)


class AiStrategy2(IStrategy):
    loaded_strategies = {}

    buy_mean_threshold = DecimalParameter(0.0, 1, default=0.5, load=True)
    sell_mean_threshold = DecimalParameter(0.0, 1, default=0.5, load=True)
    buy_strategies = IntParameter(0, len(STRAT_COMBINATIONS), default=0, load=True)
    sell_strategies = IntParameter(0, len(STRAT_COMBINATIONS), default=0, load=True)
    # print(len(STRAT_COMBINATIONS))

      
    
    buy_params = {
         "buy_mean_threshold": 0.01,
         "buy_strategies": 61,
    }

    # # Sell hyperspace params:
    sell_params = {
         "sell_mean_threshold": 0.566,
         "sell_strategies": 35,
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
    timeframe = '5m'
    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.041
    trailing_only_offset_is_reached = True
    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True
    # Number of candles the strategy requires before producing valid signals
    # startup_candle_count: int = 200
    informative_timeframe = '1h'

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
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        strategies = STRAT_COMBINATIONS[self.buy_strategies.value]
        for strategy_name in strategies:
            strategy = self.get_strategy(strategy_name)
            strategy_indicators = strategy.advise_indicators(dataframe, metadata)
            dataframe[f"strat_buy_signal_{strategy_name}"] = strategy.advise_buy(
                strategy_indicators, metadata
            )["buy"]

        dataframe['buy'] = (
            dataframe.filter(like='strat_buy_signal_').mean(axis=1) > self.buy_mean_threshold.value
        ).astype(int)
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        strategies = STRAT_COMBINATIONS[self.sell_strategies.value]
        # strategies = STRATEGIES
        for strategy_name in strategies:
            strategy = self.get_strategy(strategy_name)
            strategy_indicators = strategy.advise_indicators(dataframe, metadata)
            dataframe[f"strat_sell_signal_{strategy_name}"] = strategy.advise_sell(
                strategy_indicators, metadata
            )["sell"]

        dataframe['sell'] = (
            dataframe.filter(like='strat_sell_signal_').mean(axis=1) > self.sell_mean_threshold.value
        ).astype(int)
        return dataframe
