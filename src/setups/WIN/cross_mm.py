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
            # 'position_modify': None,
            # 'position_close': None,
            # 'breakeven': None,
            # 'trailing_stop': None
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



    def create_strategy(self, dataframe, tp=200, sl=200, volume=1.0):
        self.dataframe = dataframe

        if self.params['short_ma']['type'] == 'SMA':
            dataframe['MMS'] = dataframe[self.params['short_ma']['applied_price']].rolling(window=self.params['short_ma']['period']).mean().fillna(0)

        if self.params['long_ma']['type'] == 'SMA':
            dataframe['MML'] = dataframe[self.params['long_ma']['applied_price']].rolling(window=self.params['long_ma']['period']).mean().fillna(0)

        if self.params['short_ma']['type'] == 'EMA':
            dataframe['MMS'] = dataframe[self.params['short_ma']['applied_price']].ewm(min_periods=self.params['short_ma']['period'], span=self.params['short_ma']['period'], adjust=False).mean().fillna(0)

        if self.params['long_ma']['type'] == 'EMA':
            dataframe['MML'] = dataframe[self.params['long_ma']['applied_price']].ewm(min_periods=self.params['long_ma']['period'], span=self.params['long_ma']['period'], adjust=False).mean().fillna(0)

        # Strategy Logic
        
        # dataframe['Signal'] = dataframe['MML'] < dataframe['MMS']

        signal = []
        price_tp = []
        price_sl = []

        signal.append(None)
        price_tp.append(None)
        price_sl.append(None)

        aux_tp = 0
        aux_sl = 0

        for i in range(1, len(dataframe['Close'])):
            if dataframe['MML'][i - 1] > dataframe['MMS'][i - 1] and dataframe['MML'][i] < dataframe['MMS'][i]:
                signal.append(True)

                aux_tp = dataframe['Close'][i] + tp
                aux_sl = dataframe['Close'][i] - sl

                price_tp.append(aux_tp)
                price_sl.append(aux_sl)

            elif dataframe['MML'][i - 1] < dataframe['MMS'][i - 1] and dataframe['MML'][i] > dataframe['MMS'][i]:
                signal.append(False)

                aux_tp = dataframe['Close'][i] - tp
                aux_sl = dataframe['Close'][i] + sl

                price_tp.append(aux_tp)
                price_sl.append(aux_sl)
            else:
                signal.append(None)
                price_tp.append(aux_tp)
                price_sl.append(aux_sl)
                

        dataframe['Signal'] = signal
        dataframe['TP'] = price_tp
        dataframe['SL'] = price_sl

        dataframe['Signal_Type'] = dataframe['Signal'].replace({False: 'SELL', True: 'BUY', None: 'HOLD'})

        for i in range(len(dataframe['Signal_Type'])):
            if dataframe['Signal_Type'][i] == 'BUY':
                dataframe['TP'][i] = dataframe['Open'][i] + tp
                dataframe['SL'][i] = dataframe['Open'][i] - sl
            elif dataframe['Signal_Type'][i] == 'SELL':
                dataframe['TP'][i] = dataframe['Open'][i] - tp
                dataframe['SL'][i] = dataframe['Open'][i] + sl
            else:
                dataframe['TP'][i] = 0
                dataframe['SL'][i] = 0

        return dataframe


    @override
    def get_setup_params(self):
        return self.__setup_params

    @override
    def get_indicators_params():
        return self.__indicators_params

    @override
    def signal_buy(self, mml_last: float, mms_last: float, mml_previous: float, mms_previous: float) -> bool:
        return True if mml_last < mms_last and mml_previous > mms_previous else False
    
    @override
    def signal_sell(self, mml_last: float, mms_last: float, mml_previous: float, mms_previous: float) -> bool:
        return True if mml_last > mms_last and mml_previous < mms_previous else False

    @override
    def get_stack_info_from_backtest(self, dt, price, **kwargs):
        return
    
    @override
    def export_backtest_log_report(self):
        return

    def override(self):
        def wrapper(f=None):
            return 
        return