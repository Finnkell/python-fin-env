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

server = MetaTraderConnection()

# print(server.get_orders(symbol='WINQ21'))

# # while True:
#     # print(f"Last: {server.get_symbol_info_last(symbol='WINQ21')}")
#     print(f"OHLC: {server.get_symbol_info(symbol='WINQ21').trade_tick_value}")
#     print(f"OHLC: {server.get_symbol_info(symbol='WINQ21').trade_tick_size}")

# import requests

# dataframe = pd.read_csv('src/database/ohlc/WIN$N_M1.csv', sep=',')

start = time.perf_counter()

setup = CrossMMSetupWIN(symbol='WIN$N', period_ma_short=2, period_ma_long=3)

last_time = 0

def new_bar():
    global last_time

    time_now = datetime.now()


    if last_time == 0:
        last_time = time_now

        return False
    
    if time_now.minute != last_time.minute:
        last_time = time_now

        return True

    return False



while True:
    if new_bar():
        rates = server.get_symbol_ohlc(symbol='WINQ21', timeframe='TIMEFRAME_M1', count=50)
        rates_frame = pd.DataFrame(rates)
        rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')

        rates_frame = rates_frame.rename(columns = {'time': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close'})

        setup_dataframe = setup.create_strategy(dataframe=rates_frame)
        # print(f"\nSetup: \n{setup_dataframe}")

        # print(f"Signal Type: {setup_dataframe['Signal_Type'].iloc[-1]}")
        # print(f"Position: {server.get_positions(symbol='WINQ21')}")

        if server.get_positions(symbol='WINQ21') == ():
            if setup_dataframe['Signal_Type'].iloc[-1] == 'BUY':
                print(f"MM 2 PREV: {setup_dataframe['MMS'].iloc[-2]} | MM 3 PREV: {setup_dataframe['MML'].iloc[-2]}")
                print(f"MM 2 AGORA: {setup_dataframe['MMS'].iloc[-1]} | MM 3 AGORA: {setup_dataframe['MML'].iloc[-1]}")

                result = server.buy(volume=1.0, symbol='WINQ21', price=server.get_symbol_info_last(symbol='WINQ21'), sl=200, tp=200)
                print(f"\nResult: {result}")
            elif setup_dataframe['Signal_Type'].iloc[-1] == 'SELL':
                print(f"MM 2 PREV: {setup_dataframe['MMS'].iloc[-2]} | MM 3 PREV: {setup_dataframe['MML'].iloc[-2]}")
                print(f"MM 2 AGORA: {setup_dataframe['MMS'].iloc[-1]} | MM 3 AGORA: {setup_dataframe['MML'].iloc[-1]}")

                result = server.sell(volume=1.0, symbol='WINQ21', price=server.get_symbol_info_last(symbol='WINQ21'), sl=200, tp=200)
                print(f"\nResult: {result}")
            else:
                print('Hold')


# backtest = Backtest(setup, dataframe)

# t1 = threading.Thread(target=backtest.run_backtest())

# t1.start()

# t1.join()

# finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')
