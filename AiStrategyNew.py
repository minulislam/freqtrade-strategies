from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
import logging
from pandas import DataFrame
from freqtrade.resolvers import StrategyResolver
from itertools import combinations
from functools import reduce

logger = logging.getLogger(__name__)
'''
2021-07-05 17:31:15,019 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy AiStrategyNew from '/freqtrade/user_data/strategies/AiStrategyNew.py'...
2021-07-05 17:31:15,020 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2021-07-05 17:31:15,021 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_mean_threshold = 0.01
2021-07-05 17:31:15,021 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_strategies = 12
2021-07-05 17:31:15,022 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_mean_threshold = 0.566
2021-07-05 17:31:15,022 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_strategies = 52
2021-07-05 17:31:15,023 - AiStrategyNew - INFO - Buy stratrategies: ('CombinedBinHClucAndMADV5', 'CombinedBinHClucAndMADV6', 'SMAOffsetProtectOpt', 'NostalgiaForInfinityV4')
2021-07-05 17:31:15,023 - AiStrategyNew - INFO - Sell stratrategies: ('CombinedBinHAndClucV8', 'SMAOffsetProtectOpt')
'''

# DO NOT MODIFY THE STRATEGY LIST
# You'll need to run hyperopt to find the best strategy combination for buy/sell.
# Also, make sure you have all strategies listed here in user_data/strategies
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

MAX_COMBINATIONS = len(STRAT_COMBINATIONS) - 1


class AiStrategyNew(IStrategy):
    loaded_strategies = {}
    timeframe = '5m'
    informative_timeframe = '1h'
    # Run "populate_indicators()" only for new candle.
    # process_only_new_candles = True

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 200
    
    buy_mean_threshold = DecimalParameter(0.0, 1, default=0.5, load=True)
    sell_mean_threshold = DecimalParameter(0.0, 1, default=0.5, load=True)
    buy_strategies = IntParameter(0, MAX_COMBINATIONS, default=0, load=True)
    sell_strategies = IntParameter(0, MAX_COMBINATIONS, default=0, load=True)

    # print(len(MAX_COMBINATIONS))
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
            dataframe[f"strat_sell_signal_{strategy_name}"] = strategy.advise_sell(
                strategy_indicators, metadata
            )["sell"]
            # values = dataframe[f"strat_sell_signal_{strategy_name}"].tolist()
            # logger.info(f"sell_signals_{strategy_name}: {values}")

        dataframe['sell'] = (
            dataframe.filter(like='strat_sell_signal_').mean(axis=1) > self.sell_mean_threshold.value
        ).astype(int)
        return dataframe
#  AiStrategyNew |    918 |           1.27 |        1164.22 |          7862.251 |         786.23 |        2:36:00 |   572   267    79  62.3 | 2077.558 USDT  156.31%