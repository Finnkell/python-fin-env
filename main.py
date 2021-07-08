from src.servers.server_profit import ProfitConnection
from time import sleep
from datetime import datetime

ativo = 'WINQ21'
bolsa = 'F'
t_flag = 'TICK'

flag = True

connection = ProfitConnection(key=1127858027317301205)
connection.subscribe_ticker(ticker=ativo, bolsa=bolsa, flag=t_flag)

while True:
    connection.set_theoretical_price()
    continue