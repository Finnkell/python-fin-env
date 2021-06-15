from src.server import MetaTraderConnection
from time import sleep
from datetime import datetime

import MetaTrader5 as mt5

import pandas as pd

SYMBOL = 'WINM21'

server = MetaTraderConnection()

server.set_magic_number(123456789)

last_bar = 0

def is_new_bar(current_time):
    global last_bar

    print("lastbar: ", last_bar)
    if last_bar == 0:
        last_bar = current_time;
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

while server:

    candles = get_ohlc(SYMBOL)

    print(candles)

    server.get_symbol(SYMBOL)

    server.get_symbol_info_tick(SYMBOL)
    server.get_symbol_info(SYMBOL)

    price = server.get_symbol_ask()
    point = server.get_symbol_point()

    if not is_new_bar(datetime.now()):
        if candles['close'].iloc[-3] > candles['close'].iloc[-2]:
            server.buy(10.0, SYMBOL, price, price - 100*point, price + 100*point, 0, "Buy")
            print(f'{server.by_result.order} - \n{server.get_order_from_history(server.by_result.order)}')


        if candles['close'].iloc[-3] < candles['close'].iloc[-2]:
            if mt5.positions_get(symbol=SYMBOL) != ():
                server.position_close()

    sleep(0.5)