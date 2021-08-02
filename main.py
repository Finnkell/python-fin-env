import threading
import concurrent.futures
import subprocess
import time
import random
import pandas as pd
from datetime import datetime
from src.api.api import server_run
from src.servers.server_mt5 import MetaTraderConnection

from src.setups.cross_mm import CrossMMSetupWIN
from src.models.decision_tree import DecisionTreeClassifierModel

import requests

dataframe = pd.read_csv('src/database/ohlc/WIN$N_M15.csv', sep=',')

start = time.perf_counter()

setup = CrossMMSetupWIN()
model = DecisionTreeClassifierModel()
server = MetaTraderConnection()

server.get_symbol_info('PETR4F')

t1 = threading.Thread(target=setup.create_strategy(dataframe))
t2 = threading.Thread(target=model.example(dataframe))

t1.start()
t2.start()

t1.join()
t2.join()

while True:
    print(server.get_symbol_ohlc(symbol='PETR4F', timeframe='TIMEFRAME_M15'))

    time.sleep(1)

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')
