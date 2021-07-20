import MetaTrader5 as mt5

class MetaTraderConnection:
    
    def __init__(self):
        if not mt5.initialize():
            mt5.shutdown()
        else:
            print(f'Connect Sucessfully {mt5.version()}')
   
        self.position = None     
        self.order = None

        self.by_request = None
        self.by_result = None

        self.magic_number = 0

        self.trade_history = {}

    def __del__(self):
        version = mt5.version()
        mt5.shutdown()
        print(f'Disconnected from {version}')

    # GETTERS
    def get_timeframe(self, timeframe='M1'):
        try:
             timeframe = mt5.TIMEFRAME_M1 if timeframe == 'M1' else mt5.TIMEFRAME_D1 
        except:
            return None
        
        return timeframe

    """
        NEED TO FIND, WHAT KINDA OF DATETIME NEED TO BE PASSSED TO 'DATE' PARAMETER
    """
    def get_symbol_ohlc(self, symbol, timeframe, date, count):
        self.verify_symbol(symbol)
        return mt5.copy_rates_from_pos(symbol, timeframe, date, count)

    def get_orders(self, symbol=None, ticket=None, group=None):
        if symbol != None:
            return mt5.orders_get(symbol=symbol)
        elif ticket != None:
            return mt5.orders_get(ticket=ticket)
        elif group != None:
            return mt5.orders_get(group=group)
        else:
            return None

    def get_orders_total(self):
        return mt5.orders_total()

    def get_positions(self, symbol=None, ticket=None, group=None):
        if symbol != None:
            return mt5.positions_get(symbol=symbol)
        elif ticket != None:
            return mt5.positions_get(ticket=ticket)
        elif group != None:
            return mt5.positions_get(group=group)
        else:
            return None

    def get_positions_total(self):
        return mt5.positions_total()

    def get_symbol_last_info_tick(self, symbol='WINQ21'):
        self.verify_symbol(symbol)

        return mt5.symbol_info_tick(symbol)

    def get_symbol_last_bid(self, symbol=None):
        self.verify_symbol(symbol)

        return mt5.symbol_info_tick(symbol).bid

    def get_symbol_last_ask(self, symbol=None):
        self.verify_symbol(symbol)

        return mt5.symbol_info_tick(symbol).ask

    def get_symbol_last_volume(self, symbol=None):
        self.verify_symbol(symbol)

        return mt5.symbol_info_tick(symbol).volume

    def get_symbol_last_price(self, symbol=None):
        self.verify_symbol(symbol)

        return mt5.symbol_info_tick(symbol).last

    def get_symbol_info(self, symbol=None):
        self.verify_symbol(symbol)

        return mt5.symbol_info(symbol)

    def get_symbol_point(self, symbol=None):
        self.verify_symbol(symbol)

        return mt5.symbol_info(symbol).point

    def get_symbol_last_high(self, symbol=None):
        self.verify_symbol(symbol)

        return mt5.symbol_info(symbol).lasthigh

    def get_symbol_last_low(self, symbol=None):
        self.verify_symbol(symbol)

        return mt5.symbol_info(symbol).lastlow

    def get_trade_from_history(self, ticket=None):
        if ticket == None:
            return self.trade_history
        elif not self.trade_history[ticket]:
            print(f'{ticket} not listed on orders history')
            return None
        
        return self.trade_history[ticket]

    def get_orders_history(self, datetime_start, datetime_end, symbol=None):
        if symbol == None:
            mt5.history_orders_get(datetime_end, datetime_start)

        return mt5.history_orders_get(datetime_end, datetime_start, symbol=symbol)

    def get_deals_history(self, datetime_start, datetime_end, symbol=None):
        if symbol == None:
            mt5.history_deals_get(datetime_end, datetime_start)
            
        return mt5.history_deals_get(datetime_end, datetime_start, symbol=symbol)

    def get_last_trade(self):
        if self.by_result == None:
            print('Don\'t have any trade')
            return None
        
        return self.by_result

    def to_string_orders(self):
        print(f'Orders = {self.last_order}')

    def to_string_positions(self):
        print(f'Positions = {self.position}')

    def set_magic_number(self, number_magic=1234):
        self.magic_number = number_magic   

    def get_symbol(self, symbol):
        selected = mt5.symbol_select(symbol)

        if selected == None:
            return None
    
    def buy(self, volume, symbol, price, sl=0.0, tp=0.0, deviation=0, comment=''):
        self.verify_symbol(symbol)

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(volume),
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": price - sl*self.get_symbol_point(symbol=symbol),
            "tp": price + tp*self.get_symbol_point(symbol=symbol),
            "magic": self.magic_number,
            "deviation": deviation,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        if mt5.order_check(request) == None:
            print('Order check gone wrong')
            return None

        result = mt5.order_send(request)

        self.by_request = request
        self.by_result = result

        self.trade_history[result.order] = (request, result)

        return result

    def buy_limit(self, volume, symbol, price, sl=0.0, tp=0.0, deviation=0, comment=''):
        self.verify_symbol(symbol)
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(volume),
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

        self.trade_history[result.order] = (request, result)

        return result

    def sell(self, volume, symbol, price, sl=0.0, tp=0.0, deviation=0, comment=''):
        self.verify_symbol(symbol)
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(volume),
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": price + sl*self.get_symbol_point(symbol=symbol),
            "tp": price - tp*self.get_symbol_point(symbol=symbol),
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

        self.trade_history[result.order] = (request, result)

        return result

    def sell_limit(self, volume, symbol, price, sl=0.0, tp=0.0, comment='=0'):
        self.verify_symbol(symbol)

        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "magic": self.magic_number,
            "volume": float(volume),
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

        self.trade_history[result.order] = (request, result)

        return result
    
    def order_modify(self, volume, symbol, price, sl=0.0, tp=0.0, deviation=0, comment=''):
        self.verify_symbol(symbol)
        
        request = {
            "action": mt5.TRADE_ACTION_MODIFY,
            "symbol": symbol,
            "volume": float(volume),
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

        self.trade_history[result.order] = (request, result)

        return result

    def position_close(self, order_request):
        if self.get_positions(ticket=order_request.order) == None:
            return None

        volume = float(order_request.volume)

        if order_request.request.type == mt5.ORDER_TYPE_SELL:
            m_type = mt5.ORDER_TYPE_BUY
            m_price = self.get_symbol_last_ask(symbol=order_request.request.symbol)
            m_position_id = order_request.order
            symbol = order_request.request.symbol
            magic = order_request.request.magic

        elif order_request.request.type == mt5.ORDER_TYPE_BUY:
            m_type = mt5.ORDER_TYPE_SELL
            m_price = self.get_symbol_last_bid(symbol=order_request.request.symbol)
            m_position_id = order_request.order
            symbol = order_request.request.symbol
            magic = order_request.request.magic

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": m_type,
            "price": m_price,
            "position": m_position_id,
            "magic": magic,
            "deviation": 0,
            "comment": f"Position {order_request.request.type} closed by {m_type}",
            "type_time": mt5.ORDER_TIME_DAY,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        result = mt5.order_check(request)

        if result == None:
            return None

        result = mt5.order_send(request)
        
        return result
    
    def position_close_by(self, order_request, order_request_by):
        if self.get_positions(ticket=order_request.order) == None:
            print('gone wrong 1')
            return None
        elif self.get_positions(ticket=order_request_by.order) == None:
            print('gone wrong 2')
            return None

        request = {
            "action": mt5.TRADE_ACTION_CLOSE_BY,
            "position": order_request.order,
            "position_by": order_request_by.order,
            "magic": order_request.request.magic
        }

        result = mt5.order_check(request)

        if result == None:
            print('gone wrong')
            return None

        result = mt5.order_send(request)
        
        return result

    def verify_symbol(self, symbol):
        if symbol == None:
            raise ValueError

        if not mt5.symbol_select(symbol):
            raise NameError