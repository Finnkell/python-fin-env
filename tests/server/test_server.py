import pytest

from datetime import date, datetime, timezone
from time import time
import pytz

from src.servers.server_mt5 import MetaTraderConnection
import unittest

server = MetaTraderConnection()

tickets = []
results = []
server.set_magic_number()

# global results
symbol = 'VALE3'
group = None
tickets = tickets
results = results

class MessageException(Exception):
    def __init__(self, message: str):
        self.msg = message
        super().__init__(self.msg)

class TestServer():

    @pytest.mark.parametrize('symbol', ['WIN121', 'AAAAAA', 12312, 'WIN$N'])
    def test_select_symbol(self, symbol):
        try:
            assert server.get_symbol_info(symbol) != None
        except:
            raise MessageException(message=f"Symbol {symbol} doesn\'t exist")

    def test_get_symbol_ohlc(self):
        try:
            assert server.get_symbol_ohlc(symbol=symbol, timeframe=server.get_timeframe(timeframe='TIMEFRAME_M1'), count=10) != None
        except:
            raise MessageException(message=f"Couldn\'t get OHLC data from {symbol}")

    def test_get_symbol_info(self):
        try:
            assert server.get_symbol_info(symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} info")

    def test_get_symbol_bid(self):
        try:
            assert server.get_symbol_info_bid(symbol=symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} bid")

    def test_get_symbol_ask(self):
        try:
            assert server.get_symbol_info_ask(symbol=symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} bid")

    def test_get_symbol_volume(self):
        try:
            assert server.get_symbol_info_volume(symbol=symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} volume")

    def test_get_symbol_info_trade_tick_size(self):
        try:
            assert server.get_symbol_info_trade_tick_size(symbol=symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} trade tick size")

    def test_buy(self):
        price = server.get_symbol_last_price(symbol=symbol)
        point = server.get_symbol_point(symbol=symbol)

        # sl = float(price - 10*point)
        # tp = float(price + 5*point)

        result = server.buy(volume=1, symbol=symbol, price=price, comment="Buy Test")

        self.results.append(result)
        self.tickets.append(result.order)

        try:
            assert result != None
        except:
            raise MessageException(message=f"Couldn\'t put an buy order at {symbol}")

        if result != None:
            self.tickets.append( result.order )

    def test_sell(self):
        price = server.get_symbol_last_price(symbol=symbol)
        point = server.get_symbol_point(symbol=symbol)
        
        # sl = float(price + 10*point)
        # tp = float(price - 5*point)

        result = server.sell(volume=1, symbol=symbol, price=price, comment="Sell Test")

        self.results.append(result)
        self.tickets.append(result.order)

        try:
            assert result != None
        except:
            raise MessageException(message=f"Couldn\'t put an sell order at {symbol}")

        if result != None:
            self.tickets.append( result.order )

    """" LIMIT ORDERS NEED TO BE IMPLEMENTED YET

    def test_buy_limit(self):
        price = server.get_symbol_ask()
        point = server.get_symbol_point()

        sl = price - 10*point
        tp = price + 5*point
        try:
            assert server.buy_limit(1.0, symbol, sl, tp, 0, "Buy-Limit Test"), "Couldn\'t put an buy limit order at {symbol}")
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} bid")

        if server.last_order != None:
            self.ticket.append( server.last_order )

    def test_sell_limit(self):
        price = server.get_symbol_bid()
        point = server.get_symbol_point()
        
        sl = price + 10*point
        tp = price - 5*point
        try:
            assert server.sell_limit(1.0, symbol, sl, tp, 0, "Sell-Limit Test"), "Couldn\'t put an sell limit order at {symbol}")
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} bid")

        if server.last_order != None:
            self.ticket.append( server.last_order )

    """

    # Group Orders Test need to be implemented 
    def test_get_orders(self):
        result = server.get_orders(symbol=symbol)

        try:
            assert result != None
        except:
            raise MessageException(message=f"Coudn\'t get order from {symbol} symbol")

        try:
            assert server.get_orders(ticket=result[-1].ticket) != None
        except:
            raise MessageException(message=f"Coudn\'t get order from {self.tickets[-1]} ticket")

    # Group Positions Test need to be implemented 
    def test_get_positions(self):
        try:
            assert server.get_positions(symbol=symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} ticks")

        try:
            assert server.get_positions(ticket=self.tickets[0]) != None
        except:
            raise MessageException(message=f"Couldn\'t get {self.tickets[0]} ticket")
            
        try:
            assert server.get_orders(group=self.group) != None
        except:
            raise MessageException(message=f"Couldn\'t get {self.group} ticks")

    # POSITION
    def test_position_close(self):
        result = server.buy(volume=1, symbol=symbol, price=server.get_symbol_last_price(symbol=symbol), comment="Buy Test")

        try:
            assert server.position_close(result) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} bid")

    def test_position_close_by(self):
        try:
            assert server.position_close_by(self.results[0], self.results[-1]) != None
        except:
            raise MessageException(message=f"Couldn\'t close {self.results[0].order} ticket with {self.results[1].order} ticket")