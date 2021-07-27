class CrossMMSetupWIN():
    def __init__(self, period_ma_short= 8, applied_price_ma_short='Close', type_ma_short='SMA', period_ma_long=20, applied_price_ma_long='Close', type_ma_long='SMA'):
        self.dataframe = None

        self.params = {
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


    def __del__(self):
        pass

    def example(self):
        pass

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

        return dataframe


    def signal_buy(self):
        pass

    def signal_sell(self):
        pass
