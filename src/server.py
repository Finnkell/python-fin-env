import MetaTrader5 as mt5

class MetaTraderConnection:
    
    def __init__(self):
        if not mt5.initialize():
            mt5.shutdown()
        else:
            print(f'Connect Sucessfully {mt5.version()}')
        
        self.symbol_ohlc = None
        self.symbol_tick = None
        self.symbol_info = None
        self.symbol_info_tick = None
        self.last_order = None
        self.position = None

        self.by_request = None
        self.by_result = None

    def __del__(self):
        version = mt5.version()
        mt5.shutdown()
        print(f'Disconnected from {version}')
    
    def get_symbol_ohlc(self, symbol, timeframe, date, count):
        self.symbol_ohlc = mt5.copy_rates_from_pos(symbol, timeframe, date, count)

    def get_symbol_info_tick(self, symbol):
        self.symbol_info_tick = mt5.symbol_info_tick(symbol)

    def get_symbol_info(self, symbol):
        self.symbol_info = mt5.symbol_info(symbol)

    def get_symbol_ticks(self, symbol, date, count):
        self.symbol_ticks = mt5.copy_ticks_from(symbol, date, count, mt5.COPY_TICKS_ALL)

    def get_orders(self, symbol):
        self.last_order = mt5.orders_get(symbol=symbol)

    def get_positons(self, symbol):
        self.position = mt5.positions_get(symbol)

    def get_symbol_bid(self):
        return self.symbol_info_tick.bid

    def get_symbol_ask(self):
        return self.symbol_info_tick.ask

    def get_symbol_volume(self):
        return self.symbol_info_tick.volume

    def get_symbol_last(self):
        return self.symbol_info_tick.last

    def get_symbol_point(self):
        return self.symbol_info.point

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



    def to_string_orders(self):
        print(f'Orders = {self.last_order}')

    def to_string_positions(self):
        print(f'Positions = {self.position}')



    def get_symbol(self, symbol):
        selected = mt5.symbol_select(symbol)

        if not selected:
            print(f'Failed to select symbol {symbol}')
        else:
            pass
    
    def buy(self, volume, symbol, price, sl, tp, deviation, comment):

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": sl,
            "tp": tp,
            "magic": 234897,
            "deviation": deviation,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        result = mt5.order_send(request)
        self.by_request = request
        self.by_result = result

        return result
    
    def sell(self, volume, symbol, price, sl, tp, deviation, comment):
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": sl,
            "tp": tp,
            "magic": 234897,
            "deviation": deviation,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        result = mt5.order_send(request)

        self.by_request = request

        return result

    def position_close(self): 

        volume = self.by_request['volume']

        if self.by_request['type'] == mt5.ORDER_TYPE_SELL:
            m_type = mt5.ORDER_TYPE_BUY
            m_price = self.get_symbol_ask()
            m_position_id = self.by_result.order
            symbol = self.by_request['symbol']
            magic = self.by_request['magic']

        elif self.by_request['type'] == mt5.ORDER_TYPE_BUY:
            m_type = mt5.ORDER_TYPE_SELL
            m_price = self.get_symbol_bid()
            m_position_id = self.by_result.order
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
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        result = mt5.order_send(request)
        
        return result