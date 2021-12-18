import threading
import subprocess
import time
import random
import datetime
import pandas as pd
from datetime import datetime

from src.api.api import server_run
from src.servers.server_mt5 import MetaTraderConnection

from src.setups.cross_mm import CrossMMSetupWIN
from src.setups.mfi import MFISetup
from src.backtest.backtest import Backtest

server_run()

start = time.perf_counter()

df = pd.read_csv('src/database/ohlc/WIN$N_M1.csv', sep=',')

server = MetaTraderConnection()
setup = CrossMMSetupWIN(connection=server, symbol='WINQ21')

backtest = Backtest(setup=setup, dataframe=df)
backtest.run_backtest()

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')
