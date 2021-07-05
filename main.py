from src.servers.server_profit import ProfitConnection
from time import sleep
from datetime import datetime

connection = ProfitConnection(key=1127858027317301205)

ativo = 'WINQ21'
bolsa = 'F'
t_flag = 'OHLC'

while True:
    print('-------------------------------------')
    connection.get_account()

    connection.subscribe_offer_book(ticker=ativo, bolsa=bolsa)

    connection.buy_limit_order(volume='10', ticker=ativo, price='127455.0', sl=0, tp=0)

    sleep(5)


    connection.sell_limit_order(volume='10', ticker=ativo, price='127455.0', sl=0, tp=0)

    print(f'Position: {connection.get_position(ativo)}')

    connection.send_zero_position(ticker=ativo, price='127500.0')

    sleep(5)

    print(f'Ticker Info: {connection.get_ticker_info(ticker=ativo, bolsa=bolsa)}')


# datetime('2021', '07', '05'), datetime.now()