from datetime import date, datetime, timezone
from time import time
import pytz

from src.servers.server_mt5 import MetaTraderConnection
import unittest

server = MetaTraderConnection()

tickets = []
results = []
server.set_magic_number()

print('##########################################################')

class ServerTest(unittest.TestCase):
    def setUp(self):
        global tickets
        global results

        self.symbol = 'WINQ21'
        self.group = None
        self.tickets = tickets
        self.results = results

    def test_select_symbol(self):
        self.assertIsNotNone(server.get_symbol_info(self.symbol), "You don\'t have {self.symbol} on your MetTrader Market Observer")

    def test_get_symbol_ohlc(self):
        self.assertIsNotNone(server.get_symbol_ohlc(symbol=self.symbol, timeframe=server.get_timeframe(timeframe='TIMEFRAME_M1'), count=10), "Couldn\'t get OHLC data from {self.symbol}")

    def test_get_symbol_info_tick(self):
        self.assertIsNotNone(server.get_symbol_last_info_tick(self.symbol), "Couldn\'t get {self.symbol} info tick")

    def test_get_symbol_info(self):
        self.assertIsNotNone(server.get_symbol_info(self.symbol), "Couldn\'t get {self.symbol} info")

    def test_get_symbol_bid(self):
        self.assertIsNotNone(server.get_symbol_last_bid(symbol=self.symbol), "Couldn\'t get {self.symbol} bid")

    def test_get_symbol_ask(self):
        self.assertIsNotNone(server.get_symbol_last_ask(symbol=self.symbol), "Couldn\'t get {self.symbol} ask")

    def test_get_symbol_volume(self):
        self.assertIsNotNone(server.get_symbol_last_volume(symbol=self.symbol), "Couldn\'t get {self.symbol} volume")

    def test_get_symbol_last(self):
        self.assertIsNotNone(server.get_symbol_last_price(symbol=self.symbol), "Couldn\'t get {self.symbol} last price")

    def test_get_symbol_point(self):
        self.assertIsNotNone(server.get_symbol_point(symbol=self.symbol), "Couldn\'t get {self.symbol} point")

    def test_buy(self):
        price = server.get_symbol_last_price(symbol=self.symbol)
        point = server.get_symbol_point(symbol=self.symbol)

        # sl = float(price - 10*point)
        # tp = float(price + 5*point)

        result = server.buy(volume=1, symbol=self.symbol, price=price, comment="Buy Test")

        self.results.append(result)
        self.tickets.append(result.order)

        self.assertIsNotNone(result, "Couldn\'t put an buy order at {self.symbol}")

        if result != None:
            self.tickets.append( result.order )

    def test_sell(self):
        price = server.get_symbol_last_price(symbol=self.symbol)
        point = server.get_symbol_point(symbol=self.symbol)
        
        # sl = float(price + 10*point)
        # tp = float(price - 5*point)

        result = server.sell(volume=1, symbol=self.symbol, price=price, comment="Sell Test")

        self.results.append(result)
        self.tickets.append(result.order)

        self.assertIsNotNone(result, "Couldn\'t put an sell order at {self.symbol}")

        if result != None:
            self.tickets.append( result.order )

    """" LIMIT ORDERS NEED TO BE IMPLEMENTED YET

    def test_buy_limit(self):
        price = server.get_symbol_ask()
        point = server.get_symbol_point()

        sl = price - 10*point
        tp = price + 5*point
        self.assertIsNotNone(server.buy_limit(1.0, self.symbol, sl, tp, 0, "Buy-Limit Test"), "Couldn\'t put an buy limit order at {self.symbol}")

        if server.last_order != None:
            self.ticket.append( server.last_order )

    def test_sell_limit(self):
        price = server.get_symbol_bid()
        point = server.get_symbol_point()
        
        sl = price + 10*point
        tp = price - 5*point
        self.assertIsNotNone(server.sell_limit(1.0, self.symbol, sl, tp, 0, "Sell-Limit Test"), "Couldn\'t put an sell limit order at {self.symbol}")

        if server.last_order != None:
            self.ticket.append( server.last_order )

    """

    # Group Orders Test need to be implemented 
    def test_get_orders(self):
        result = server.get_orders(symbol=self.symbol)

        self.assertIsNotNone(result, "Coudn\'t get order from {self.symbol} symbol")
        self.assertIsNotNone(server.get_orders(ticket=result[-1].ticket), "Coudn\'t get order from {self.tickets[-1]} ticket")

    # Group Positions Test need to be implemented 
    def test_get_positions(self):
        self.assertIsNotNone(server.get_positions(symbol=self.symbol), "Couldn\'t get {self.symbol} ticks")
        self.assertIsNotNone(server.get_positions(ticket=self.tickets[0]), "Couldn\'t get {self.tickets[0]} ticket")
        # self.assertIsNotNone(server.get_orders(group=self.group), "Couldn\'t get {self.group} ticks")

    # POSITION
    def test_position_close(self):
        result = server.buy(volume=1, symbol=self.symbol, price=server.get_symbol_last_price(symbol=self.symbol), comment="Buy Test")
        self.assertIsNotNone(server.position_close(result), "Couldn\'t close {result} position")

    def test_position_close_by(self):
        self.assertIsNotNone(server.position_close_by(self.results[0], self.results[-1]), "Couldn\'t close {self.results[0].order} ticket with {self.results[1].order} ticket")