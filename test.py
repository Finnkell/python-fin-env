from src.models.svm import SVRModel
from src.servers.server_mt5 import MetaTraderConnection
import requests
import pandas as pd
from time import sleep

model = SVRModel()

model.example_model_ohlc_win()

model.save_model()

server = MetaTraderConnection()

ATIVO = 'WINQ21'

timeframe = server.get_timeframe('M1')

while True:

    ohlc = server.get_symbol_ohlc(symbol=ATIVO, timeframe=timeframe, date=0, count=5)


    result = requests.get(f'http://10.0.0.148:5000/predict_svm?open_price={ohlc["open"][-1]}&high_price={ohlc["high"][-1]}&low_price={ohlc["low"][-1]}&close_price={ohlc["close"][-1]}', auth=('user', 'pass'))

    label = result.json()['label']

    print(label)

    if server.get_positions(symbol=ATIVO) == () and label == 'SELL':
        order_request = server.sell(volume=1.0, symbol=ATIVO, price=server.get_symbol_last_bid(symbol=ATIVO), tp=50, sl=100)
 
    if server.get_positions(symbol=ATIVO) == () and label == 'BUY':
        order_request = server.buy(volume=1.0, symbol=ATIVO, price=server.get_symbol_last_bid(symbol=ATIVO), tp=50, sl=100)


    sleep(0.5)