from src.server import MetaTraderConnection
from src.database.database import Candles

from src.models.arima import ARIMAModel

from time import sleep
from datetime import datetime

import MetaTrader5 as mt5

import pandas as pd
import numpy as np

# Globals
last_bar = 0

# Symbol
SYMBOL = 'WINQ21'

server = MetaTraderConnection()
dataframe = Candles()
arima_model = ARIMAModel()

server.set_magic_number(123456789)

win_data = pd.read_csv('src/database/WIN$N_M1.csv', sep=',')

arima_model.set_data(win_data['Close'])

arima_model.create_model()
arima_model.fit_model()
arima_model.predict_model()
arima_model.model_summary()


def is_new_bar(current_time):
    global last_bar

    if last_bar == 0:
        last_bar = current_time
        return False

    if last_bar > current_time:
        return False

    if last_bar < current_time:
        last_bar = current_time
        return True

    return False 


def get_ohlc(symbol):
    server.get_symbol_ohlc(symbol, mt5.TIMEFRAME_M1, 0, 10)
    candles = server.symbol_ohlc
    candles = pd.DataFrame(candles)

    return candles

candles = []

arima_pct = 0

while server:
    
    server.get_symbol_info(SYMBOL)
    server.get_symbol_info_tick(SYMBOL)

    ohlc = get_ohlc(SYMBOL)

    # if not is_new_bar(datetime.now()):

    arima_model.set_data(ohlc['close'])
    
    candles.append(ohlc.iloc[4, -1])
    
    if len(candles) == 1000:

        predict = arima_model.real_time_predict(candles)
        arima_pct = arima_model.calculate_mean_squared_error_out_of_sample()

        candles = []

        if mt5.positions_get(symbol=SYMBOL) == ():
            print(arima_pct)

            if arima_pct > 0 and arima_pct < 0.2:
                if ohlc.iloc[4, -3] > ohlc.iloc[4, -2]:
                    price = server.get_symbol_bid()
                    point = server.get_symbol_point()
                    
                    sl = price + 10*point
                    tp = price - 5*point

                    server.sell(1.0, SYMBOL, price, sl, tp, 0, "Venda")

            if arima_pct > 1.5 and arima_pct < 1.7:
                if ohlc.iloc[4, -3] < ohlc.iloc[4, -2]:
                    price = server.get_symbol_ask()
                    point = server.get_symbol_point()

                    sl = price - 10*point
                    tp = price + 5*point

                    server.buy(1.0, SYMBOL, price, sl, tp, 0, "Compra")
    