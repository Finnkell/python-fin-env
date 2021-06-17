import pandas as pd
import numpy as np
import os 

path = 'src/database/ticks'

df = pd.DataFrame()

for entry in os.scandir(path):
    df_aux = pd.read_csv(entry.path, parse_dates=(['time'])).drop(columns='Unnamed: 0')
    df = pd.concat([df, df_aux])

class Renko:

    def __init__(self, symbol):
        # server.set_symbol_info_tick(symbol)
        # self.dataset = pd.DataFrame(server.get_symbol_info_tick())

        self.renko_chart = None

    def create_chart(self):
        
        dataframe = df

        prices = list(dataframe.price)
        renko = []

        renko.append(0)

        top = prices[0]

        for _i in range(1, len(prices)):
            
            if prices[_i - 1] == prices[_i] or (prices[_i - 2] < prices[_i - 1] and abs(prices[_i] - prices[_i - 1]) == 5 and prices[_i - 1] > prices[_i]):
                renko.append(0)

            elif prices[_i - 1] == prices[_i] or (prices[_i - 2] > prices[_i - 1] and abs(prices[_i] - prices[_i - 1]) == 5 and prices[_i - 1] < prices[_i]):
                renko.append(0)

            elif top > prices[_i] and abs(top - prices[_i]) == 10:
                renko.append(-2)

            elif top < prices[_i] and abs(top - prices[_i]) == 10:
                top = prices[_i]
                renko.append(2)

            elif prices[_i - 1] < prices[_i] and abs(prices[_i - 1] - prices[_i]) == 5:
                top = prices[_i]
                renko.append(1)

            elif prices[_i - 1] > prices[_i] and abs(prices[_i - 1] - prices[_i]) == 5:
                renko.append(-1)

            else:
                renko.append(0)

        dataframe['renko'] = renko
        print(dataframe.head(30))


    def export_chart(self):
        return self.renko_chart


    def update_chart(self):
        self.create_chart()