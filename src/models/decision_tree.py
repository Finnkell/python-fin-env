from src.models.model import Model

from sklearn import datasets
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import *
from sklearn.model_selection import train_test_split

import numpy as np
import pandas as pd
import joblib


class DecisionTreeClassifierModel(Model):
    def __init__(self):
        super().__init__()
        self.__model = None
        self.__model_sum = None

        self.__X_train = None
        self.__X_test = None
        self.__y_train = None
        self.__y_test = None
        self.__y_pred = None

    def __del__(self):
        super().__del__()
        del self.__model
        del self.__model_sum
        del self.__X_train
        del self.__X_test
        del self.__y_train
        del self.__y_test
        del self.__y_pred

    def create_model(self, **kwargs):
        self.__model = make_pipeline(StandardScaler(), DecisionTreeClassifier())

    def get_data(self, dataframe):
        dataframe = dataframe.drop(['Ticks', 'Volume', 'Spread', 'Date', 'Time'], axis=1)

        X = dataframe

        X = MACD(X)
        X = RSI(X)
        X['EMA'] = EMA(X)
        X['SMA'] = SMA(X)

        X['Target'] = np.where(X['Close'].shift(-1) > X['Close'], 0, 1)

        X = X.dropna(inplace=False)

        columns = ['Close', 'MACD', 'RSI', 'Signal_Line', 'EMA', 'SMA']

        X, y = X[columns].values, X['Target'].values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=41)

        self.__X_train, self.__X_test, self.__y_train, __self.y_test = X_train, X_test, y_train, y_test


    def example(self, dataframe):

        self.get_data(dataframe)
        self.create_model()
        self.fit_model(self.__X_train, self.__y_train)
        self.__y_pred = self.predict(self.__X_test)
        self.__model_sum = self.model_summary()

        print(self.model_sum)

    def fit_model(self, X_train, y_train):
        return self.__model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.__model.predict(X_test)
    
    def evaluate_model(self):
        return

    def model_summary(self):
        DECISION_TREE_CLASSIFIER_ACCURACY_SCORE = accuracy_score(y_pred=self.__y_pred, y_true=self.__y_test)
        DECISION_TREE_CLASSIFIER_BALANCED_ACCURACY_SCORE = accuracy_score(y_pred=self.__y_pred, y_true=self.__y_test)
        DECISION_TREE_CLASSIFIER_AVERAGE_PRECISION_SCORE = average_precision_score(y_score=self.__y_pred, y_true=self.__y_test)
        DECISION_TREE_CLASSIFIER_BRIER_SCORE_LOSS = brier_score_loss(y_prob=self.__y_pred, y_true=self.__y_test)
        DECISION_TREE_CLASSIFIER_F1_SCORE = f1_score(y_pred=self.__y_pred, y_true=self.__y_test)
        DECISION_TREE_CLASSIFIER_LOG_LOSS = log_loss(y_pred=self.__y_pred, y_true=self.__y_test)
        DECISION_TREE_CLASSIFIER_PRECISION = precision_score(y_pred=self.__y_pred, y_true=self.__y_test)

        summary = {
            'accuracy_score': DECISION_TREE_CLASSIFIER_ACCURACY_SCORE,
            'balanced_accuracy_score': DECISION_TREE_CLASSIFIER_BALANCED_ACCURACY_SCORE,
            'average_precision_score': DECISION_TREE_CLASSIFIER_AVERAGE_PRECISION_SCORE,
            'brier_score_loss': DECISION_TREE_CLASSIFIER_BRIER_SCORE_LOSS,
            'f1_score': DECISION_TREE_CLASSIFIER_F1_SCORE,
            'log_score': DECISION_TREE_CLASSIFIER_LOG_LOSS,
            'precision_score': DECISION_TREE_CLASSIFIER_PRECISION
        }

        return summary

    def save_model(self, flag='PROD'):

        if flag == 'PROD':
            model_filename = 'src/api/models/DecisionTreeClassifier.pkl'
            print(f'Saving model to {model_filename}...')
            joblib.dump(self.__model, model_filename)

        if flag == 'TEST':
            model_filename = 'src/api/models/test/DecisionTreeClassifier.pkl'
            print(f'Saving model to {model_filename}...')
            joblib.dump(self.__model, model_filename)

class DecisionTreeRegressor(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    def example_model_boston(self):
        pass


class ID3Model():
    def __init__(self):
        pass

    def __del__(self):
        pass

    def example_model_boston(self):
        pass


def SMA(data, period=30, column='Close'):
    return data[column].rolling(window=period).mean()

def EMA(data, period=21, column='Close'):
    return data[column].ewm(span=period, adjust=False).mean()

def MACD(data, period_long=26, period_short=12, period_signal=9, column='Close'):
    short_ema = EMA(data, period=period_short)
    long_ema = EMA(data, period=period_long)

    data['MACD'] = short_ema - long_ema

    data['Signal_Line'] = EMA(data, period=period_signal, column='MACD')

    return data

def RSI(data, period=7, column='Close'):
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