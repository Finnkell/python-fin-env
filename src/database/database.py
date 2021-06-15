from datetime import datetime

import pandas as pd

class Candles:
    def __init__(self):
        self.dataframe = None
        self.time = []
        self.price = []
        self.volume = []

    def create_table(self):
        self.dataframe = pd.DataFrame({'time': self.time, 'price': self.price, 'volume': self.volume})
        self.dataframe['time'] = pd.to_datetime(self.dataframe['time'], unit='s')

    def create_candles(self, period):
        pass
        # if datetime.now().sec == 0:
        #     pass

    def set_ticks(self, time, price, volume):
        self.time.append(time)
        self.price.append(price)
        self.volume.append(volume)

    def to_string_dataframe(self):
        print(f'{self.dataframe}')

    def save_dataframe(self):
        self.dataframe.to_csv(f'src/database/tick_data_{str(datetime.now().day)}_{str(datetime.now().month)}_{str(datetime.now().year)}-{str(datetime.now().hour)}-{str(datetime.now().minute)}.csv')
