from src.server import MetaTraderConnection
from src.database.database import Candles

from time import sleep
from datetime import datetime

import MetaTrader5 as mt5

import pandas as pd

SYMBOL = 'WINM21'

server = MetaTraderConnection()
dataframe = Candles()

server.set_magic_number(123456789)

last_bar = 0

def is_new_bar(current_time):
    global last_bar

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
    server.get_symbol_info_tick(SYMBOL)

    ticks = server.symbol_info_tick

    dataframe.set_ticks(ticks.time, ticks.last, ticks.volume)
    dataframe.create_table()

    dataframe.to_string_dataframe()

    if datetime.now().minute % 10 == 0:
        dataframe.save_dataframe()

    print(f'last tick {ticks.last}|{datetime.now().second}')

    candles = get_ohlc(SYMBOL)

    # print(candles)

    server.get_symbol(SYMBOL)

    server.get_symbol_info_tick(SYMBOL)
    server.get_symbol_info(SYMBOL)

    price = server.get_symbol_ask()
    point = server.get_symbol_point()

    order_result = []

    if not is_new_bar(datetime.now()):
        # order_result.append( server.sell_limit(10.0, SYMBOL, price + 25*point, 0, 0, "SellLimit") )

        print(f'orders_result: {order_result}')

        if candles['close'].iloc[-3] > candles['close'].iloc[-2]:
            # order_result.append( server.sell_limit(10.0, SYMBOL, price + 25*point, 0, 0, "SellLimit") )
            order_result.append( server.buy(10.0, SYMBOL, price, price - 100*point, price + 100*point, 0, "Buy") )


        if candles['close'].iloc[-3] < candles['close'].iloc[-2]:
            order_result.append( server.sell(10.0, SYMBOL, price, price + 100*point, price - 100*point, 0, "Sell") )

        print(f'{server.by_result.order} - \n{server.get_order_from_history(server.by_result.order)}')
        # print(f'{server.by_result.order} - \n{server.get_order_from_history(server.by_result.order)}')
        
    sleep(0.5)