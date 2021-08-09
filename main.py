import threading
import concurrent.futures
import subprocess
import time
import random
import datetime
import pandas as pd
from datetime import datetime
from src.api.api import server_run
from src.servers.server_mt5 import MetaTraderConnection

from src.setups.cross_mm import CrossMMSetupWIN
from src.models.decision_tree import DecisionTreeClassifierModel
from src.backtest.backtest import Backtest

import requests

dataframe = pd.read_csv('src/database/ohlc/WIN$N_M1.csv', sep=',')

start = time.perf_counter()

setup = CrossMMSetupWIN('WIN$N')
backtest = Backtest(setup, dataframe)

t1 = threading.Thread(target=backtest.run_backtest())

t1.start()

t1.join()

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')
