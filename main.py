from src.servers.server_profit import ProfitConnection
# from src.servers.server_mt5 import MetaTraderConnection
from time import sleep
from datetime import datetime

from multiprocessing import Queue, Pool, Process


ativo = 'WINQ21'
bolsa = 'F'
t_flag = 'TICK'

flag = True

profit_connection = ProfitConnection(key=1127858027317301205)
# mt_connection = MetaTraderConnection()

profit_connection.subscribe_ticker(ticker=ativo, bolsa=bolsa, flag=t_flag)

# t1 = Process(target=profit_connection.)
# t2 = Process(target=mt_connection.)

while True:
    print(f'LasPrice: {profit_connection.get_last_price()}')