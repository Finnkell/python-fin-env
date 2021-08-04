from src.setups.setup import Setup
import random

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
            'volume': 1.0,
            'tp': 100.0,
            'sl': 100.0,
            'position_modify': None,
            'position_close': None,
            'breakeven': None,
            'trailing_stop': None,
        }

        self.__backtest_info = {
            'order': [],
            'positions': [],
            'position_closed': [],
        }

    def __del__(self):
        super().__del__()
        del self.__dataframe
        del self.__indicator_params
        del self.__setup_params

    def get_setup_dataframe(self):
        return self.__dataframe

    def get_position_side(self, ticket: int) -> str or None:
        for position in self.__backtest_info['order']:
            if position['ticket'] == ticket:
                return position['side']

        return None
    
    def get_position_price(self, ticket: int) -> None:
        for position in self.__backtest_info['order']:
            if position['ticket'] == ticket:
                return position['price']

        return None

    def get_position_take_profit(self, ticket: int) -> None:
        for position in self.__backtest_info['order']:
            if position['ticket'] == ticket:
                return position['tp']

        return None

    def get_position_stop_loss(self, ticket: int) -> None:
        for position in self.__backtest_info['order']:
            if position['ticket'] == ticket:
                return position['sl']

        return None

    def get_take_profit(self) -> float or None:
        return self.__setup_params['tp'] if self.__setup_params['tp'] != None else None

    def get_stop_loss(self) -> float or None:
        return self.__setup_params['sl'] if self.__setup_params['sl'] != None else None

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
            if self.signal_buy(dataframe['Close'], dataframe['MML'][i - 1], dataframe['MMS'][i - 1], dataframe['MML'][i], dataframe['MMS'][i]):
                signal.append(True)
            elif self.signal_sell(dataframe['Close'], dataframe['MML'][i - 1], dataframe['MMS'][i - 1], dataframe['MML'][i], dataframe['MMS'][i]):
                signal.append(False)
            else:
                signal.append(None)

        dataframe['Signal'] = signal

        dataframe['Signal_Type'] = dataframe['Signal'].replace({False: 'SELL', True: 'BUY', None: 'HOLD'})

        self.__dataframe = dataframe


    '''>>> Override'''
    def get_setup_params(self):
        return self.__setup_params

    def get_indicators_params(self):
        return self.__indicators_params

    def get_any_position(self) -> bool:
        return True if self.__backtest_info['order'] != [] else False
    
    def get_orders(self) -> list:
        return self.__backtest_info['order'] if self.__backtest_info['order'] != [] else []

    def signal_buy(self, price: float, mml_last: float, mms_last: float, mml_previous: float, mms_previous: float) -> bool:
        return True if (mml_last < mms_last and mml_previous > mms_previous) else False
    
    def signal_sell(self, price: float, mml_last: float, mms_last: float, mml_previous: float, mms_previous: float) -> bool:
        return True if mml_last > mms_last and mml_previous < mms_previous else False

    '''>>> Backtest functions'''
    def set_order_entry(self, date, side, price, comment):
        if side == 'BUY':
            tp = price + self.get_take_profit()
            sl = price - self.get_stop_loss()
        elif side == 'SELL':
            tp = price - self.get_take_profit()
            sl = price + self.get_stop_loss()
        
        self.__backtest_info['order'].append(
            {
                'ticket': random.randint(1, 100000) + round(random.randint(1, 5)*random.random()) + price,
                'date': date,
                'price': price,
                'side': side,
                'tp': tp,
                'sl': sl,
                'comment': comment,
            }
        )

    def set_position_close(self, ticket=None, start_date=None, end_date=None, price=None, position=None, comment=''):
        
        if comment == 'Close by take profit':
            result = self.get_position_take_profit(ticket) - price
        else: 
            result = self.get_position_stop_loss(ticket) - price

        if position != None:
            self.__backtest_info['position_closed'].append({
                'ticket': ticket,
                'start_date': start_date,
                'end_date': end_date,
                'price': price,
                'tp': self.get_position_take_profit(ticket),
                'sl': self.get_position_stop_loss(ticket),
                'comment': comment,
                'result': result
            })

        self.__backtest_info['order'] = list(filter(lambda order: order['ticket'] != ticket, self.__backtest_info['order']))

    def set_backtest_take_profit(self, value):
        if self.get_backtest_order():
            self.__backtest_info['take_profit'] = self.__backtest_info['take_profit']
        else:
            self.__backtest_info['take_profit'] = value

    def set_backtest_stop_loss(self, value):
        if self.get_backtest_order():
            self.__backtest_info['stop_loss'] = self.__backtest_info['stop_loss']
        else:
            self.__backtest_info['stop_loss'] = value

    def __get_backtesting_info(self):
        return self.__backtest_info

    def get_stack_info_from_pre_setup_processing(self, stack_info, results):
        datetime, price, _ = stack_info

        for i in [results]:
            if i['order_entry'] == True:
                if i['side'] == 'BUY':
                    self.set_order_entry(date=datetime, side='BUY', price=price, comment='BUY order entry')
                    
                elif i['side'] == 'SELL':
                    self.set_order_entry(date=datetime, side='SELL', price=price, comment='SELL order entry')

            for position in i['positions_to_close']:
                if position['comment'] == 'Close by take profit':
                    self.set_position_close(ticket=position['ticket'], start_date=position['start_time'], end_date=datetime, price=position['price'], position=i['positions_to_close'], comment=position['comment'])
                
                elif position['comment'] == 'Close by stop loss':
                    self.set_position_close(ticket=position['ticket'], start_date=position['start_time'], end_date=datetime, price=position['price'], position=i['positions_to_close'], comment=position['comment'])


    def get_signal_buy_from_setup(self, price: float, **kwargs):
        mml_last = kwargs['kwargs'][0]
        mms_last = kwargs['kwargs'][1]
        mml_previous = kwargs['kwargs'][2]
        mms_previous = kwargs['kwargs'][3]

        return self.signal_buy(price=price, mml_last=mml_last, mms_last=mms_last, mml_previous=mml_previous, mms_previous=mms_previous)

    def get_signal_sell_from_setup(self, price: float, **kwargs):

        mml_last = kwargs['kwargs'][0]
        mms_last = kwargs['kwargs'][1]
        mml_previous = kwargs['kwargs'][2]
        mms_previous = kwargs['kwargs'][3]

        return self.signal_sell(price=price, mml_last=mml_last, mms_last=mms_last, mml_previous=mml_previous, mms_previous=mms_previous)

    def export_backtesting_info(self):
        print(self.__backtest_info)
        return self.__get_backtesting_info()