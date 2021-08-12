import pytest
import pandas as pd

from src.backtest.backtest import Backtest
from src.setups.cross_mm import CrossMMSetupWIN
from src.servers.server_mt5 import MetaTraderConnection

df = pd.read_csv('src/database/ohlc/WIN$N_M1.csv', sep=',')

server = MetaTraderConnection()

setup = CrossMMSetupWIN(connection=server, symbol='WINQ21')
backtest = Backtest(setup=setup, dataframe=df)

class MessageException(Exception):
    def __init__(self, message: str):
        self.msg = message
        super().__init__(self.msg)

class TestBackTest():
    def test_is_stack_empty(self):
        try:
            assert backtest.is_stack_empty([]) == True
        except AssertionError as e:
            raise MessageException(f"{e}")

    def test_is_dataframe_empty(self):
        try:
            assert backtest.is_dataframe_empty(pd.DataFrame()) == True
        except AssertionError as e:
            raise MessageException(f"{e}")

    def test_setup_pre_processing_infos(self):
        try:
            assert type(backtest.setup_pre_processing_infos(("15/05", 215412, 1.0, "BUY"))) == dict
        except AssertionError as e:
            raise MessageException(f"{e}")

    def test_send_setup_stack_info(self):
        try:
            assert backtest.send_setup_stack_info() == None
        except AssertionError as e:
            raise MessageException(f"{e}")