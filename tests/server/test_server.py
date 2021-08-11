import pytest

from datetime import date, datetime, timezone
from time import time
import pytz

from src.servers.server_mt5 import MetaTraderConnection
import unittest

server = MetaTraderConnection()
server.set_magic_number()

tickets = []
results = []

# global results
symbol = 'WINQ21'
group = None
tickets = tickets
results = results

class MessageException(Exception):
    def __init__(self, message: str):
        self.msg = message
        super().__init__(self.msg)

class TestServer():

    # @pytest.mark.parametrize('symbol', ['WIN121', 'AAAAAA', 12312, 'WIN$N'])
    def test_select_symbol(self):
        global symbol

        try:
            assert server.get_symbol_info(symbol) != None
        except:
            raise MessageException(message=f"Symbol {symbol} doesn\'t exist")

    def test_get_symbol_ohlc(self):
        global symbol

        try:
            assert server.get_symbol_ohlc(symbol=symbol, timeframe='TIMEFRAME_M1', count=10) != None
        except:
            raise MessageException(message=f"Couldn\'t get OHLC data from {symbol}")

    def test_get_symbol_info(self):
        global symbol
        
        try:
            assert server.get_symbol_info(symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} info")

    def test_get_symbol_info_last(self):
        global symbol

        try:
            assert server.get_symbol_info_last(symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} last price")

    def test_get_symbol_bid(self):
        global symbol

        try:
            assert server.get_symbol_info_bid(symbol=symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} bid")

    def test_get_symbol_bid_high(self):
        global symbol

        try:
            assert server.get_symbol_info_bid_high(symbol=symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} bid high")

    def test_get_symbol_bid_low(self):
        global symbol
        try:
            assert server.get_symbol_info_bid_low(symbol=symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} bid low")

    def test_get_symbol_ask(self):
        global symbol
        try:
            assert server.get_symbol_info_ask(symbol=symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} ask")

    def test_get_symbol_ask_high(self):
        global symbol
        try:
            assert server.get_symbol_info_ask_high(symbol=symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} ask_high")

    def test_get_symbol_ask_low(self):
        global symbol
        try:
            assert server.get_symbol_info_ask_low(symbol=symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} ask_low")

    def test_get_symbol_volume(self):
        global symbol
        try:
            assert server.get_symbol_info_volume(symbol=symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} volume")

    def test_get_symbol_info_trade_tick_size(self):
        global symbol
        try:
            assert server.get_symbol_info_trade_tick_size(symbol=symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} trade tick size")

    def test_get_symbol_info_trade_tick_value(self):
        global symbol
        try:
            assert server.get_symbol_info_trade_tick_value(symbol=symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} trade tick value")

    def test_get_symbol_info_trade_tick_profit(self):
        global symbol
        try:
            assert server.get_symbol_info_trade_tick_profit(symbol=symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} trade tick profit")

    def test_get_symbol_info_trade_tick_loss(self):
        global symbol
        try:
            assert server.get_symbol_info_trade_tick_loss(symbol=symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} trade tick loss")

    def test_get_symbol_info_last_high(self):
        global symbol
        try:
            assert server.get_symbol_info_last_high(symbol=symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} info last high")
            
    def test_get_symbol_info_last_low(self):
        global symbol
        try:
            assert server.get_symbol_info_last_low(symbol=symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} info last low")

    def test_buy(self):
        global symbol
        global tickets
        global results

        price = server.get_symbol_info_last(symbol=symbol)

        result = server.buy(volume=1, symbol=symbol, price=price, comment="Buy Test")

        results.append(result)
        tickets.append(result.order)

        try:
            assert result != None
        except:
            raise MessageException(message=f"Couldn\'t put an buy order at {symbol}")

        if result != None:
            tickets.append( result.order )

    def test_sell(self):
        global symbol
        global tickets
        global results

        price = server.get_symbol_info_last(symbol=symbol)

        result = server.sell(volume=1, symbol=symbol, price=price, comment="Sell Test")

        results.append(result)
        tickets.append(result.order)

        try:
            assert result != None
        except:
            raise MessageException(message=f"Couldn\'t put an sell order at {symbol}")

        if result != None:
            tickets.append( result.order )

    """" LIMIT ORDERS NEED TO BE IMPLEMENTED YET

    def test_buy_limit(self):
        global symbol
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
        global symbol
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

    def test_get_orders_history(self):
        global symbol
        pass

    def test_get_deals_history(self):
        global symbol
        pass

    def test_get_last_trade(self):
        global symbol
        try:
            assert server.get_last_trade() != None
        except:
            raise MessageException(message=f"Coudn\'t get last trade")

    # Group Orders Test need to be implemented 
    def test_get_orders(self):
        global symbol
        global tickets

        result = server.get_orders(symbol=symbol)
        print(f'result: {result}')

        try:
            assert result != None
        except:
            raise MessageException(message=f"Coudn\'t get order from {symbol} symbol")

        print(f"Result tickets: {results[-1]}")

        try:
            assert server.get_orders(ticket=results[-1].order) != None
        except:
            raise MessageException(message=f"Coudn\'t get order from {results[-1].order} ticket")

    # Group Positions Test need to be implemented 
    def test_get_positions(self):
        global symbol
        global tickets

        try:
            assert server.get_positions(symbol=symbol) != None
        except:
            raise MessageException(message=f"Couldn\'t get {symbol} ticks")

        try:
            assert server.get_positions(ticket=tickets[0]) != None
        except:
            raise MessageException(message=f"Couldn\'t get {self.tickets[0]} ticket")

    # POSITION
    def test_position_close(self):
        global symbol
        result = server.buy(volume=1, symbol=symbol, price=server.get_symbol_info_last(symbol=symbol), comment="Buy Test")

        try:
            assert server.position_close(result) != None
        except:
            raise MessageException(message=f"Couldn\'t get close {result} position")

    def test_position_close_by(self):
        global symbol
        global tickets
        global results

        try:
            assert server.position_close_by(results[0], results[-1]) != None
        except:
            raise MessageException(message=f"Couldn\'t close {results[0].order} ticket with {results[1].order} ticket")