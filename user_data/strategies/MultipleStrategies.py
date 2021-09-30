# Strategy specific imports, files must reside in same folder as strategy
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from BinClucMadSMACore import BinClucMadSMACore as CoreStrategy


class BinClucMadv1(CoreStrategy):
    INTERFACE_VERSION = 2

    stoploss = -0.99

    # Custom stoploss
    use_custom_stoploss = False
    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True
    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 200

    buy_params = {
        "buy_minimum_conditions": 1,
        "smaoffset_buy_condition_0_enable": False,
        "smaoffset_buy_condition_1_enable": False,
        "v6_buy_condition_0_enable": False, # avg 0.47 dd 27%
        "v6_buy_condition_1_enable": True, # no trade
        "v6_buy_condition_2_enable": True,  # avg 2.32
        "v6_buy_condition_3_enable": True, # avg 1.12 dd 6%
        "v8_buy_condition_0_enable": True, # avg 0.74
        "v8_buy_condition_1_enable": False,  # avg 0.41 dd 37%
        "v8_buy_condition_2_enable": True,   # avg 1.37
        "v8_buy_condition_3_enable": False,  # avg 0.41
        "v8_buy_condition_4_enable": True,   # avg 1.29
        "v9_buy_condition_0_enable": False,
        "v9_buy_condition_1_enable": True,
        "v9_buy_condition_2_enable": True,
        "v9_buy_condition_3_enable": True,
        "v9_buy_condition_4_enable": False,
        "v9_buy_condition_5_enable": True,
        "v9_buy_condition_6_enable": True,
        "v9_buy_condition_7_enable": True,
        "v9_buy_condition_8_enable": False,
        "v9_buy_condition_9_enable": False,
        "v9_buy_condition_10_enable": False,

    }

 
class BinClucMadv2(CoreStrategy):
    INTERFACE_VERSION = 2

    stoploss = -0.99

    # Custom stoploss
    use_custom_stoploss = False
    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True
    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 200

    buy_params = {
        "buy_minimum_conditions": 1,
        "smaoffset_buy_condition_0_enable": False,
        "smaoffset_buy_condition_1_enable": False,
        "v6_buy_condition_0_enable": False, # avg 0.47 dd 27%
        "v6_buy_condition_1_enable": True, # no trade
        "v6_buy_condition_2_enable": True,  # avg 2.32
        "v6_buy_condition_3_enable": True, # avg 1.12 dd 6%
        "v8_buy_condition_0_enable": True, # avg 0.74
        "v8_buy_condition_1_enable": False,  # avg 0.41 dd 37%
        "v8_buy_condition_2_enable": True,   # avg 1.37
        "v8_buy_condition_3_enable": False,  # avg 0.41
        "v8_buy_condition_4_enable": True,   # avg 1.29
        "v9_buy_condition_0_enable": False,
        "v9_buy_condition_1_enable": False,
        "v9_buy_condition_2_enable": False,
        "v9_buy_condition_3_enable": False,
        "v9_buy_condition_4_enable": False,
        "v9_buy_condition_5_enable": False,
        "v9_buy_condition_6_enable": False,
        "v9_buy_condition_7_enable": False,
        "v9_buy_condition_8_enable": False,
        "v9_buy_condition_9_enable": False,
        "v9_buy_condition_10_enable": False,

    }



class BinClucMadSMAv1(CoreStrategy):

    INTERFACE_VERSION = 2


    stoploss = -0.228  # effectively disabled.
    # Custom stoploss
    use_custom_stoploss = False
    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True
    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 200

    buy_params = {
        "buy_minimum_conditions": 1,
        "smaoffset_buy_condition_0_enable": True,
        "smaoffset_buy_condition_1_enable": True,
        "v6_buy_condition_0_enable": False, # avg 0.47 dd 27%
        "v6_buy_condition_1_enable": True, # no trade
        "v6_buy_condition_2_enable": True,  # avg 2.32
        "v6_buy_condition_3_enable": True, # avg 1.12 dd 6%
        "v8_buy_condition_0_enable": True, # avg 0.74
        "v8_buy_condition_1_enable": False,  # avg 0.41 dd 37%
        "v8_buy_condition_2_enable": True,   # avg 1.37
        "v8_buy_condition_3_enable": False,  # avg 0.41
        "v8_buy_condition_4_enable": True,   # avg 1.29
        "v9_buy_condition_0_enable": False,
        "v9_buy_condition_1_enable": False,
        "v9_buy_condition_2_enable": False,
        "v9_buy_condition_3_enable": False,
        "v9_buy_condition_4_enable": False,
        "v9_buy_condition_5_enable": False,
        "v9_buy_condition_6_enable": False,
        "v9_buy_condition_7_enable": False,
        "v9_buy_condition_8_enable": False,
        "v9_buy_condition_9_enable": False,
        "v9_buy_condition_10_enable": False,


    }




class BinClucMadSMAv2(CoreStrategy):

    INTERFACE_VERSION = 2

    stoploss = -0.228  # effectively disabled.
    # Custom stoploss
    use_custom_stoploss = False
    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True
    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 200

    buy_params = {
        "buy_minimum_conditions": 1,

        "smaoffset_buy_condition_0_enable": True,
        "smaoffset_buy_condition_1_enable": True,
        "v6_buy_condition_0_enable": False, # avg 0.47 dd 27%
        "v6_buy_condition_1_enable": True, # no trade
        "v6_buy_condition_2_enable": True,  # avg 2.32
        "v6_buy_condition_3_enable": True, # avg 1.12 dd 6%
        "v8_buy_condition_0_enable": True, # avg 0.74
        "v8_buy_condition_1_enable": False,  # avg 0.41 dd 37%
        "v8_buy_condition_2_enable": True,   # avg 1.37
        "v8_buy_condition_3_enable": False,  # avg 0.41
        "v8_buy_condition_4_enable": True,   # avg 1.29
        "v9_buy_condition_0_enable": False,
        "v9_buy_condition_1_enable": True,
        "v9_buy_condition_2_enable": True,
        "v9_buy_condition_3_enable": True,
        "v9_buy_condition_4_enable": False,
        "v9_buy_condition_5_enable": True,
        "v9_buy_condition_6_enable": True,
        "v9_buy_condition_7_enable": True,
        "v9_buy_condition_8_enable": False,
        "v9_buy_condition_9_enable": False,
        "v9_buy_condition_10_enable": False,

    }



