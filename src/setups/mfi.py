'''
TODO: Refatoração de código
'''

import warnings
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')
plt.style.use('fivethirtyeight')


class MFISetup():

    def __init__(self):
        self.dataframe = None


    def example(self):
        dataframe = pd.read_csv('src/database/WIN$N_M15.csv', sep=',')
        dataframe = dataframe.set_index(pd.DatetimeIndex(dataframe['Date'].values))

        self.dataframe = dataframe


    def calculations(self):
        typical_price = (self.dataframe['Close'] + self.dataframe['High'] + self.dataframe['Low'])/3
        period = 14

        money_flow = typical_price*self.dataframe['Volume']

        positive_flow = []
        negative_flow = []

        for i in range(1, len(typical_price)):
            if typical_price[i] > typical_price[i - 1]:
                positive_flow.append(money_flow[i - 1])
                negative_flow.append(0)
            elif typical_price[i] < typical_price[i - 1]:
                positive_flow.append(0)
                negative_flow.append(money_flow[i - 1])
            else:
                positive_flow.append(0)
                negative_flow.append(0)

        positive_mf = [sum(positive_flow[i + 1 - period : i + 1]) for i in range(period - 1, len(positive_flow))]
        negative_mf = [sum(negative_flow[i + 1 - period : i + 1]) for i in range(period - 1, len(negative_flow))]

        mfi = 100 * (np.array(positive_mf) / (np.array(positive_mf) + np.array(negative_mf)))

        dataframe_mfi = pd.DataFrame()
        dataframe_mfi['MFI'] = mfi

    
        new_dataframe = pd.DataFrame()
        new_dataframe = self.dataframe[period:]
        new_dataframe['MFI'] = mfi

        new_dataframe['Buy'], new_dataframe['Sell'] = self.get_signal(new_dataframe, 80, 20)

        fig, ax = plt.subplots(2, figsize=(15, 5))
        ax[1].plot(new_dataframe['MFI'], label='Money Flow Index')
        ax[1].axhline(20, linestyle='--', color='blue')
        ax[1].axhline(80, linestyle='--', color='blue')
        ax[1].set_xlim(left=pd.to_datetime('2021.03.01'), right=pd.to_datetime('2021.04.01'))
        ax[0].plot(new_dataframe['Close'], label='Money Flow Index Setup', alpha=0.5)
        ax[0].set_xlim(left=pd.to_datetime('2021.03.01'), right=pd.to_datetime('2021.04.01'))
        ax[0].scatter(new_dataframe.index, new_dataframe['Buy'], color='green', label='Buy signal', marker='^', alpha=1)
        ax[0].scatter(new_dataframe.index, new_dataframe['Sell'], color='red', label='Sell signal', marker='v', alpha=1)
        ax[0].set_title('Money Flow Index Setup')
        ax[0].set_xlabel('Candles')
        ax[0].set_ylabel('Close price')


    def get_signal(self, data, high, low):
        buy_signal = []
        sell_signal = []

        for i in range(len(data['MFI'])):
            if data['MFI'][i] > high:
                buy_signal.append(np.nan)
                sell_signal.append(data['Close'][i])
            elif data['MFI'][i] < low:
                sell_signal.append(np.nan)
                buy_signal.append(data['Close'][i])
            else:
                buy_signal.append(np.nan)
                sell_signal.append(np.nan)

        return buy_signal, sell_signal