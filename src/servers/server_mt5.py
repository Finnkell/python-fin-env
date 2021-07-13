import MetaTrader5 as mt5

class MetaTraderConnection:
    
    def __init__(self):
#%%
        if not mt5.initialize():
            mt5.shutdown()
        else:
            print(f'Connect Sucessfully {mt5.version()}')
#%%     
        self.symbol_ohlc = None
        self.symbol_tick = None
        self.symbol_info = {}
        self.symbol_info_tick = {}
        self.last_order = {}
        self.position = None
        self.order = None

        self.by_request = None
        self.by_result = None

        self.magic_number = None

        self.orders_history = {}

#%%
    def __del__(self):
        version = mt5.version()
        mt5.shutdown()
        print(f'Disconnected from {version}')
#%% 
    def set_symbol_ohlc(self, symbol, timeframe, date, count):
        self.verify_symbol(symbol)
        self.symbol_ohlc = mt5.copy_rates_from_pos(symbol, timeframe, date, count)

    def get_symbol_ohlc(self):
        return self.symbol_ohlc if self.symbol_ohlc != None else None

    def set_symbol_info_tick(self, symbol='WINQ21'):
        self.verify_symbol(symbol)
        
        symbol_info_tick_dict = mt5.symbol_info_tick(symbol)._asdict()
        for key in symbol_info_tick_dict.keys():
            self.symbol_info_tick[key] = symbol_info_tick_dict[key]

    def get_symbol_info_tick(self, ticker):
        self.set_symbol_info_tick(symbol=ticker)

    def set_symbol_info(self, symbol):
        self.verify_symbol(symbol)

        symbol_info_dict = mt5.symbol_info(symbol)._asdict()

        for key in symbol_info_dict.keys():
            self.symbol_info[key] = symbol_info_dict[key]

    def set_symbol_ticks(self, symbol, date, count):
        self.symbol_ticks = mt5.copy_ticks_from(symbol, date, count, mt5.COPY_TICKS_ALL)

    def get_symbol_ticks(self):
        return self.symbol_ticks[0][1] if self.symbol_ticks[0][1] != None else None

    def get_orders(self, symbol=None, ticket=None, group=None):
        if symbol != None:
            self.order = mt5.orders_get(symbol=symbol)
        elif ticket != None:
            self.order = mt5.orders_get(ticket=ticket)
        elif group != None:
            self.order = mt5.orders_get(group=group)
        else:
            return None

    def get_positons(self, symbol=None, ticket=None, group=None):
        if symbol != None:
            self.position = mt5.positions_get(symbol=symbol)
        elif ticket != None:
            self.position = mt5.positions_get(ticket=ticket)
        elif group != None:
            self.position = mt5.positions_get(group=group)
        else:
            return None

    def get_symbol_bid(self):
        return self.symbol_info_tickself['bid']

    def get_symbol_ask(self):
        return self.symbol_info_tick['ask']

    def get_symbol_volume(self):
        return self.symbol_info_tick['volume']

    def get_symbol_last(self):
        return self.symbol_info_tick['last']

    def get_symbol_point(self):
        return self.symbol_info['point']

    def get_order_ticket(self):
        return self.last_order.ticket
    
    def get_order_volume(self):
        return self.last_order.volume

    def get_order_ticket(self):
        return self.last_order.order

    def get_position_type(self):
        return self.position.type

    def get_position_symbol(self):
        return self.position.symbol

    def get_position_volume(self):
        return self.position.volume

    def get_position_magic(self):
        return self.position.magic

    # Assets - Need to be reallocated

    def get_order_from_history(self, ticket):
        if not self.orders_history[ticket]:
            print(f'{ticket} not listed on orders history')
        else:
            return self.orders_history[ticket]

    def to_string_orders(self):
        print(f'Orders = {self.last_order}')

    def to_string_positions(self):
        print(f'Positions = {self.position}')


    def set_magic_number(self, number_magic=1234):
        self.magic_number = number_magic

        

    def get_symbol(self, symbol):
        selected = mt5.symbol_select(symbol)

        if not selected:
            print(f'Failed to select symbol {symbol}')
        else:
            pass
    
    def buy(self, volume, symbol, price, sl, tp, deviation, comment=''):

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": sl,
            "tp": tp,
            "magic": self.magic_number,
            "deviation": deviation,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        if mt5.order_check(request) == None:
            return None

        result = mt5.order_send(request)

        self.by_request = request
        self.by_result = result

        self.orders_history[result.order] = (request, result)

        return result

    def buy_limit(self, volume, symbol, price, sl, tp, deviation, comment=''):
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY_LIMIT,
            "price": price,
            "sl": sl,
            "tp": tp,
            "magic": self.magic_number,
            "deviation": deviation,
            "comment": comment,
            "expiration": 0,
            "type_time": mt5.ORDER_TIME_DAY,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        if mt5.order_check(request) == None:
            return None

        result = mt5.order_send(request)

        self.by_request = request
        self.by_result = result

        self.orders_history[result.order] = (request, result)

        return result

    def sell(self, volume, symbol, price, sl, tp, deviation, comment=''):
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": sl,
            "tp": tp,
            "magic": self.magic_number,
            "deviation": deviation,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_DAY,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        if mt5.order_check(request) == None:
            return None

        result = mt5.order_send(request)

        self.by_request = request
        self.by_result = result

        self.orders_history[result.order] = (request, result)

        return result

    def sell_limit(self, volume, symbol, price, sl, tp, comment=''):

        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "magic": self.magic_number,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL_LIMIT,
            "stoplimit": 0.0,
            "price": price,
            "sl": sl,
            "tp": tp,
            "type_time": mt5.ORDER_TIME_GTC,
            "expiration": 0,
            "deviation": 0,
            "comment": comment,
        }

        if mt5.order_check(request) == None:
            return None

        result = mt5.order_send(request)

        self.by_request = request
        self.by_result = result

        self.orders_history[result.order] = (request, result)

        return result
    
    def order_modify(self, volume, symbol, price, sl, tp, deviation, comment=''):
        
        request = {
            "action": mt5.TRADE_ACTION_MODIFY,
            "symbol": symbol,
            "volume": volume,
            "price": price,
            "sl": sl,
            "tp": tp,
            "magic": self.magic_number,
            "deviation": deviation,
            "comment": comment,
            "expiration": 0,
            "type_time": mt5.ORDER_TIME_DAY,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        result = mt5.order_check(request)

        if result == None:
            return None

        self.by_request = request
        self.by_result = result

        self.orders_history[result.order] = (request, result)

        return result

    def position_close(self, ticket):

        if self.get_positons(ticket) == None:
            return None

        volume = self.by_request['volume']

        if self.by_request['type'] == mt5.ORDER_TYPE_SELL:
            m_type = mt5.ORDER_TYPE_BUY
            m_price = self.get_symbol_ask()
            m_position_id = ticket
            symbol = self.by_request['symbol']
            magic = self.by_request['magic']

        elif self.by_request['type'] == mt5.ORDER_TYPE_BUY:
            m_type = mt5.ORDER_TYPE_SELL
            m_price = self.get_symbol_bid()
            m_position_id = ticket
            symbol = self.by_request['symbol']
            magic = self.by_request['magic']

        print(f'Position_id = {m_position_id}')

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": m_type,
            "price": m_price,
            "position": m_position_id,
            # "sl": sl,
            # "tp": tp,
            "magic": magic,
            "deviation": 0,
            "comment": f"Position {self.by_request['type']} closed by {m_type}",
            "type_time": mt5.ORDER_TIME_DAY,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        result = mt5.order_send(request)
        
        return result
    
    def position_close_by(self, ticket_in, ticket_out):
        if self.get_positons(ticket_in) == None:
            return None
        elif self.get_positons(ticket_in) == None:
            return None

        request = {
            "action": mt5.TRADE_ACTION_CLOSE_BY,
            "position": ticket_in,
            "position_by": ticket_out,
            # "sl": sl,
            # "tp": tp,
            "magic": self.magic_number,
            "comment": f"Position {ticket_in} closed by {ticket_out}",
        }

        result = mt5.order_send(request)
        
        return result

    def verify_symbol(self, symbol):

        if symbol == None:
            raise ValueError

        if not mt5.symbol_select(symbol):
            raise NameError