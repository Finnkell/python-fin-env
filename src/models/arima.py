from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

import numpy as np
import pandas as pd

class ARIMAModel:
    def __init__(self):
        self.model = None
        self.model_fit = None
        self.predict = None
        self.predict_out_of_sample = None

        self.X_train = None
        self.y_train = None
        self.X_train = None
        self.y_test = None

        self.dataset = None
        self.X = None
        self.y = None

        self.order = (1, 0, 0)

    def set_data(self, sample, test_size=0.2, return_period=10):
        X = self.data_analysis(np.array(sample).reshape(-1, 1))

        self.X = X

        y = X.loc[:, 'Close'].shift(-1).dropna()

        train_size = int(len(X)*(1-test_size))
        
        self.X_train, self.X_test = X[0: train_size], X[train_size:len(X)]
        self.y_train, self.y_test = y[0: train_size], y[train_size:len(X)]

    def data_analysis(self, sample):
        dataframe = pd.DataFrame(sample)
        scaler = StandardScaler()

        scaler.fit(dataframe)
        transformed_dataframe = scaler.transform(sample)

        return pd.DataFrame(transformed_dataframe, columns=['Close'])
        

    def create_model(self):
        self.model = ARIMA(endog=self.X_train, exog=self.y_train, order=self.order)

    def fit_model(self):
        self.model_fit = self.model.fit()

    def predict_model(self):
        self.predict = self.model_fit.predict(start=int(len(self.X_train) - 1), end=int(len(self.X) - 1), exog=self.X_test)[2:]

    def real_time_predict(self, out_of_sample):
        self.len_out_of_sample = int(len(out_of_sample))

        self.predict_out_of_sample = self.model_fit.predict(start=int(len(self.X_train) - 1), end=int(len(self.X) - 1), exog=out_of_sample)[2:]

        return self.predict_out_of_sample

    def calculate_mean_squared_error_out_of_sample(self):
        return mean_squared_error(self.y_test[(len(self.y_test) - self.len_out_of_sample)-1:], self.predict_out_of_sample)


    def calculate_mean_squared_error(self):
        return mean_squared_error(self.y_test, self.predict)

    def evaluate_model(self):
        pass

    def save_model(self):
        pass

    def model_summary(self):
        print(self.model_fit.summary()) if self.model_fit != None else print(f'The model ins\'t fitted!')
    
class SARIMAXModel:

    def __init__(self):
        self.model = None

        self.X_train = None
        self.y_train = None
        self.X_train = None
        self.y_test = None

        self.order = ()

    def create_model(self):
        pass

    def fit_model(self):
        pass

    def predict(self):
        pass

    def evaluate_model(self):
        pass

    def save_model(self):
        pass

    def model_summary(self):
        print(self.model_fit.summary()) if self.model_fit != None else print(f'The model ins\'t fitted!')
