from src.setups.setup import Setup

class CrossMMSetupWIN(Setup):
    def __init__(self, period_ma_short=8, applied_price_ma_short='Close', type_ma_short='SMA', period_ma_long=20, applied_price_ma_long='Close', type_ma_long='SMA'):
        super().__init__()
        self.__dataframe = None

        self.__indicator_params = {
            'short_ma': {
                'period': period_ma_short, 
                'type': type_ma_short, 
                'applied_price': applied_price_ma_short
            },
            'long_ma': {
                'period': period_ma_long, 
                'type': type_ma_long, 
                'applied_price': applied_price_ma_long
            },
        }

        self.__setup_params = {
            'volume': None,
            'tp': None,
            'sl': None,
            'position_modify': None,
            'position_close': None,
            'breakeven': None,
            'trailing_stop': None
        }

    def __del__(self):
        super().__del__()
        del self.__dataframe
        del self.__indicator_params
        del self.__setup_params
        

    def set_take_profit(self, tp: float) -> None:
        self.__setup_params['tp'] = tp

    def set_stop_loss(self, sl: float) -> None:
        self.__setup_params['sl'] = sl

    def set_volume(self, volume: float) -> None:
        self.__setup_params['volume'] = volume

    def set_breakeven(self, qtd: int, **kwargs) -> None:
        
        if qtd == 0:
            self.__setup_params['breakeven'] = None
            return

        self.__setup_params['breakeven'] = []

        for i in range(qtd):
            self.__setup_params['breakeven'].append((be, to))

    def set_trailing_stop(self):
        pass

    def set_position_modify(self, value: float):
        if value == None:
            self.__setup_params['position_modify'] = None
            return

        self.__setup_params['position_modify'] = value
        
    def set_position_close(self, value: float):
        if value == None:
            self.__setup_params['position_close'] = None
            return

        self.__setup_params['position_close'] = value

    def get_setup_dataframe(self):
        return self.__dataframe


    def create_strategy(self, dataframe):

        if self.__indicator_params['short_ma']['type'] == 'SMA':
            dataframe['MMS'] = dataframe[self.__indicator_params['short_ma']['applied_price']].rolling(window=self.__indicator_params['short_ma']['period']).mean().fillna(0)

        if self.__indicator_params['long_ma']['type'] == 'SMA':
            dataframe['MML'] = dataframe[self.__indicator_params['long_ma']['applied_price']].rolling(window=self.__indicator_params['long_ma']['period']).mean().fillna(0)

        if self.__indicator_params['short_ma']['type'] == 'EMA':
            dataframe['MMS'] = dataframe[self.__indicator_params['short_ma']['applied_price']].ewm(min_periods=self.__indicator_params['short_ma']['period'], span=self.__indicator_params['short_ma']['period'], adjust=False).mean().fillna(0)

        if self.__indicator_params['long_ma']['type'] == 'EMA':
            dataframe['MML'] = dataframe[self.__indicator_params['long_ma']['applied_price']].ewm(min_periods=self.__indicator_params['long_ma']['period'], span=self.__indicator_params['long_ma']['period'], adjust=False).mean().fillna(0)

        signal = []
        signal.append(None)

        for i in range(1, len(dataframe['Close'])):
            if self.signal_buy(dataframe['MML'][i - 1], dataframe['MMS'][i - 1], dataframe['MML'][i], dataframe['MMS'][i]):
                signal.append(True)
            elif self.signal_sell(dataframe['MML'][i - 1], dataframe['MMS'][i - 1], dataframe['MML'][i], dataframe['MMS'][i]):
                signal.append(False)
            else:
                signal.append(None)

        dataframe['Signal'] = signal

        dataframe['Signal_Type'] = dataframe['Signal'].replace({False: 'SELL', True: 'BUY', None: 'HOLD'})

        self.__dataframe = dataframe

        print(dataframe)

    '''>>> Override'''
    def get_setup_params(self):
        return self.__setup_params

    def get_indicators_params():
        return self.__indicators_params

    def signal_buy(self, mml_last: float, mms_last: float, mml_previous: float, mms_previous: float) -> bool:
        return True if (mml_last < mms_last and mml_previous > mms_previous) else False
    
    def signal_sell(self, mml_last: float, mms_last: float, mml_previous: float, mms_previous: float) -> bool:
        return True if mml_last > mms_last and mml_previous < mms_previous else False

    def get_stack_info_from_pre_setup_processing(self, datetime, price, results, **kwargs):
        return
    
    def export_backtesting_info(self):
        return