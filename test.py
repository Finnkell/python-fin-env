from src.servers.server_mt5 import MetaTraderConnection

import requests
import pandas as pd
from time import sleep

from src.models.svm import SVCModel
from src.models.decision_tree import DecisionTreeClassifierModel


model = DecisionTreeClassifierModel()

model.example_indicators_win()

model.save_model()

server = MetaTraderConnection()

ATIVO = 'WINQ21'

timeframe = server.get_timeframe('TIMEFRAME_M5')


def SMA(data, period=30, column='close'):
    return data[column].rolling(window=period).mean()

def EMA(data, period=21, column='close'):
    return data[column].ewm(span=period, adjust=False).mean()

def MACD(data, period_long=26, period_short=12, period_signal=9, column='close'):
    short_ema = EMA(data, period=period_short)
    long_ema = EMA(data, period=period_long)

    data['MACD'] = short_ema - long_ema

    data['Signal_Line'] = EMA(data, period=period_signal, column='MACD')

    return data

def RSI(data, period=7, column='close'):
    delta = data[column].diff(1)
    delta = delta.dropna()

    up = delta.copy()
    down = delta.copy()

    up[up < 0] = 0
    down[down > 0] = 0

    data['UP'] = up
    data['DOWN'] = down

    avg_gain = SMA(data, period, column='UP')
    avg_loss = abs(SMA(data, period, column='DOWN'))

    RS = avg_gain/avg_loss

    RSI = 100.0 - (100.0/(1.0 + RS))

    data['RSI'] = RSI

    return data

while True:

    ohlc = server.get_symbol_ohlc(symbol=ATIVO, timeframe=timeframe, date=0, count=5)

    ohlc = pd.DataFrame(ohlc)

    ohlc = MACD(ohlc)
    ohlc = RSI(ohlc)
    ohlc['EMA'] = EMA(ohlc)
    ohlc['SMA'] = EMA(ohlc)


    result = requests.get(f'http://10.0.0.148:5000/decision_tree_predict?close_price={ohlc["close"].index[-1]}&macd={ohlc["MACD"].index[-1]}&signal_line={ohlc["Signal_Line"].index[-1]}&rsi={ohlc["RSI"].index[-1]}&ema={ohlc["EMA"].index[-1]}&sma={ohlc["SMA"].index[-1]}', auth=('user', 'pass'))

    label = result.json()['label']

    print(label)

    if server.get_positions(symbol=ATIVO) == () and label == 'SELL':
        order_request = server.sell(volume=1.0, symbol=ATIVO, price=server.get_symbol_last_bid(symbol=ATIVO), tp=100, sl=100)
 
    if server.get_positions(symbol=ATIVO) == () and label == 'BUY':
        order_request = server.buy(volume=1.0, symbol=ATIVO, price=server.get_symbol_last_bid(symbol=ATIVO), tp=100, sl=100)


    sleep(0.5)