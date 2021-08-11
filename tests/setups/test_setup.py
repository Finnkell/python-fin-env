import pytest
import pandas as pd

from src.servers.server_mt5 import MetaTraderConnection
from src.setups.cross_mm import CrossMMSetupWIN

server = MetaTraderConnection(server="XPMT5-Demo", login=64946322, password="30052000josePablo")
setup = CrossMMSetupWIN(connection=server, symbol='WINQ21')

class MessageException(Exception):
    def __init__(self, message: str):
        self.msg = message
        super().__init__(self.msg)

df = pd.read_csv("src/database/ohlc/WIN$N_M1.csv", nrows=25)

class TestSetup():
    def test_create_strategy(self):
        global df
        global setup

        try:
            dataframe = df.rename(columns={"Date": "DIA"}).copy()
            with pytest.raises(ValueError):
                setup.create_strategy(dataframe=dataframe)
        except AssertionError as e:
            raise MessageException(f"{e}")

        try:
            assert type(setup.create_strategy(dataframe=df)) == type(pd.DataFrame())
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_get_indicators_params(self):
        global setup

        try:
            assert type(setup.get_indicators_params()) == dict
        except AssertionError as e:
            raise MessageException(f"{e}")

    def test_get_setup_dataframe(self):
        global setup

        try:
            assert setup.get_setup_dataframe != None
        except AssertionError as e:
            raise MessageException(f"{e}")

    def test_get_volume(self):
        global setup

        try:
            assert type(setup.get_volume) != float
        except AssertionError as e:
            raise MessageException(f"{e}")

    def test_get_position_volume(self):
        global setup

        # Setting an wrong ticket to None
        try:
            with pytest.raises(TypeError):
                setup.get_position_volume(ticket="12312312")
        except AssertionError as e:
            raise MessageException(f"{e}")

        try:
            assert setup.get_position_volume(ticket=12312312) != None
        except AssertionError as e:
            raise MessageException(f"{e}")

    def test_get_position_volume(self):
        global setup

        # Setting an wrong ticket to None
        try:
            with pytest.raises(TypeError):
                setup.get_position_side(ticket="12312312")
        except AssertionError as e:
            raise MessageException(f"{e}")

        #Ticket Ficticio
        try:
            assert setup.get_position_side(ticket=12312312) == None
        except AssertionError as e:
            raise MessageException(f"{e}")

    def test_get_position_price(self):
        global setup

        # Setting an wrong ticket to None
        try:
            with pytest.raises(TypeError):
                setup.get_position_price(ticket="12312312")
        except AssertionError as e:
            raise MessageException(f"{e}")

        #Ticket Ficticio
        try:
            assert setup.get_position_price(ticket=12312312) == None
        except AssertionError as e:
            raise MessageException(f"{e}")


    def test_get_position_take_profit(self):
        global setup

        # Setting an wrong ticket to None
        try:
            with pytest.raises(TypeError):
                setup.get_position_take_profit(ticket="12312312")
        except AssertionError as e:
            raise MessageException(f"{e}")

        #Ticket Ficticio
        try:
            assert setup.get_position_take_profit(ticket=12312312) == None
        except AssertionError as e:
            raise MessageException(f"{e}")

    def test_get_position_stop_loss(self):
        global setup

        # Setting an wrong ticket to None
        try:
            with pytest.raises(TypeError):
                setup.get_position_stop_loss(ticket="12312312")
        except AssertionError as e:
            raise MessageException(f"{e}")

        #Ticket Ficticio
        try:
            assert setup.get_position_stop_loss(ticket=12312312) == None
        except AssertionError as e:
            raise MessageException(f"{e}")

    def test_get_take_profit(self):
        global setup

        try:
            assert setup.get_take_profit() != None
        except AssertionError as e:
            raise MessageException(f"{e}")

    def test_get_stop_loss(self):
        global setup

        try:
            assert setup.get_stop_loss() != None
        except AssertionError as e:
            raise MessageException(f"{e}")

    def test_get_any_position(self):
        global setup

        try:
            assert type(setup.get_any_position()) == bool
        except AssertionError as e:
            raise MessageException(f"{e}")

    def test_get_orders(self):
        global setup

        try:
            assert type(setup.get_orders()) == list
        except AssertionError as e:
            raise MessageException(f"{e}")

    def test_set_order_entry(self):
        try:
            with pytest.raises(TypeError):
                setup.set_order_entry(1105, "BUY", 0.0, 1.0, "BOUGHT")
                setup.set_order_entry("11/05", 0, 0.0, 1.0, "BOUGHT")
                setup.set_order_entry("11/05", "BUY", "0.0", 1.0, "BOUGHT")
                setup.set_order_entry("11/05", "BUY", 0.0, "1.0", "BOUGHT")
                setup.set_order_entry("11/05", "BUY", 0.0, 1.0, 0.0)
        except AssertionError as e:
            raise MessageException(f"{e}")


        try:
            assert setup.set_order_entry("11/05", "BUY", 0.0, 1.0, "BOUGHT") == None
            assert setup.set_order_entry("11/05", "BUY", 0.0, 1.0, "BOUGHT") == None
            assert setup.set_order_entry("11/05", "BUY", 0.0, 1.0, "BOUGHT") == None
            assert setup.set_order_entry("11/05", "BUY", 0.0, 1.0, "BOUGHT") == None
            assert setup.set_order_entry("11/05", "BUY", 0.0, 1.0, "BOUGHT") == None
        except AssertionError as e:
            raise MessageException(f"{e}")
        

    def test_set_position_close(self):
        try:
            with pytest.raises(TypeError):
                setup.set_position_close("123", "11/05", "12/05", "BUY", 0.0, {}, "BOUGHT")
                setup.set_position_close(123, 1105, "12/05", "BUY", 0.0, {}, "BOUGHT")
                setup.set_position_close(123, "11/05", 1205, "BUY", 0.0, {}, "BOUGHT")
                setup.set_position_close(123, "11/05", "12/05", 0, 0.0, {}, "BOUGHT")
                setup.set_position_close(123, "11/05", "12/05", "BUY", "0.0", {}, "BOUGHT")
                setup.set_position_close(123, "11/05", "12/05", "BUY", "0.0", "{}", "BOUGHT")
                setup.set_position_close(123, "11/05", "12/05", "BUY", "0.0", {}, 0)
        except AssertionError as e:
            raise MessageException(f"{e}")


        try:
            assert setup.set_position_close(123, "11/05", "12/05", "BUY", 0.0, {}, "BOUGHT") == None
            assert setup.set_position_close(123, "11/05", "12/05", "BUY", 0.0, {}, "BOUGHT") == None
            assert setup.set_position_close(123, "11/05", "12/05", "BUY", 0.0, {}, "BOUGHT") == None
            assert setup.set_position_close(123, "11/05", "12/05", "BUY", 0.0, {}, "BOUGHT") == None
            assert setup.set_position_close(123, "11/05", "12/05", "BUY", 0.0, {}, "BOUGHT") == None
            assert setup.set_position_close(123, "11/05", "12/05", "BUY", 0.0, {}, "BOUGHT") == None
            assert setup.set_position_close(123, "11/05", "12/05", "BUY", 0.0, {}, "BOUGHT") == None
        except AssertionError as e:
            raise MessageException(f"{e}")