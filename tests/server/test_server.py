from src.servers.server_mt5 import MetaTraderConnection
import unittest

server = MetaTraderConnection()

print('##########################################################')

class ServerTest(unittest.TestCase):
    def setUp(self):
        self.symbol = None
        self.group = None
        self.ticket = []

    def test_buy(self):
        server.set_symbol_info_tick(symbol='WINQ21')
        server.set_symbol_info(symbol='WINQ21')
        price = server.get_symbol_ask()
        point = server.get_symbol_point()

        sl = price - 10*point
        tp = price + 5*point
        self.assertIsNotNone(server.buy(1.0, self.symbol, sl, tp, 0, "Buy Test"), "Couldn\'t put an buy order at {self.symbol}")

        if server.last_order != None:
            self.ticket.append( server.last_order )

    def test_sell(self):
        price = server.get_symbol_bid()
        point = server.get_symbol_point()
        
        sl = price + 10*point
        tp = price - 5*point
        self.assertIsNotNone(server.buy(1.0, self.symbol, sl, tp, 0, "Sell Test"), "Couldn\'t put an sell order at {self.symbol}")

        if server.last_order != None:
            self.ticket.append( server.last_order )

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

    def test_select_symbol(self, ativo):
        if server.get_symbol_info(ativo) != None:
            self.symbol = ativo

        self.assertIsNotNone(server.get_symbol_info(ativo), "You don\'t have {ativo} on your MetTrader Market Observer")

    def test_get_symbol_ohlc(self):
        self.assertIsNotNone(server.get_symbol_ohlc(self.symbol), "Couldn\'t get OHLC data from {self.symbol}")

    def test_get_symbol_info_tick(self):
        self.assertIsNotNone(server.get_symbol_info_tick(self.symbol), "Couldn\'t get {self.symbol} info tick")

    def test_get_symbol_info(self):
        self.assertIsNotNone(server.get_symbol_info(self.symbol), "Couldn\'t get {self.symbol} info")

    def test_get_symbol_ticks(self):
        self.assertIsNotNone(server.get_symbol_ticks(self.symbol), "Couldn\'t get {self.symbol} ticks")

    # Group Orders Test need to be implemented 
    def test_get_orders(self):
        self.assertIsNotNone(server.get_orders(symbol=self.symbol), "Couldn\'t get {self.symbol} ticks")
        self.assertIsNotNone(server.get_orders(ticket=server.last_order), "Couldn\'t get {server.last_order} ticks")
        # self.assertIsNotNone(server.get_orders(group=self.group), "Couldn\'t get {self.group} ticks")

    # Group Positions Test need to be implemented 
    def test_get_positions(self):
        self.assertIsNotNone(server.get_positons(symbol=self.symbol), "Couldn\'t get {self.symbol} ticks")
        self.assertIsNotNone(server.get_positons(ticket=server.last_order), "Couldn\'t get {server.last_order} ticks")
        # self.assertIsNotNone(server.get_orders(group=self.group), "Couldn\'t get {self.group} ticks")

    def test_get_symbol_bid(self):
        self.assertIsNotNone(server.get_symbol_bid(), "Couldn\'t get {self.symbol} bid")

    def test_get_symbol_ask(self):
        self.assertIsNotNone(server.get_symbol_ask(), "Couldn\'t get {self.symbol} ask")

    def test_get_symbol_volume(self):
        self.assertIsNotNone(server.get_symbol_volume(), "Couldn\'t get {self.symbol} volume")

    def test_get_symbol_last(self):
        self.assertIsNotNone(server.get_symbol_last(), "Couldn\'t get {self.symbol} last price")

    def test_get_symbol_point(self):
        self.assertIsNotNone(server.get_symbol_point(), "Couldn\'t get {self.symbol} point")

    # ORDERS
    def test_get_order_type(self):
        self.assertIsNotNone(server.get_order_type(), "Couldn\'t order type")

    def test_get_last_order_symbol(self):
        self.assertIsNotNone(server.get_order_ticket(), "Couldn\'t get order symbol")

    def test_get_order_volume(self):
        self.assertIsNotNone(server.get_order_volume(), "Couldn\'t get order volume")

    def test_get_order_last_ticket(self):
        self.assertIsNotNone(server.get_order_last_ticket(), "Couldn\'t get last ticket")

    def test_get_order_magic(self):
        self.assertIsNotNone(server.get_order_magic, "Couldn\'t get order magic")

    # POSITION    
    def test_get_position_type(self):
        self.assertIsNotNone(server.get_position_type(), "Couldn\'t position type")

    def test_get_last_position_symbol(self):
        self.assertIsNotNone(server.get_position_symbol(), "Couldn\'t get position symbol")

    def test_get_position_volume(self):
        self.assertIsNotNone(server.get_position_volume(), "Couldn\'t get position volume")

    def test_get_position_last_ticket(self):
        self.assertIsNotNone(server.get_position_last_ticket(), "Couldn\'t get last ticket")

    def test_get_position_magic(self):
        self.assertIsNotNone(server.get_position_magic, "Couldn\'t get position magic")

    def test_get_orders_from_history(self):
        self.assertIsNotNone(server.get_orders_from_history(server.last_order), "Couldn\'t get {server.last_order} from history of orders")
