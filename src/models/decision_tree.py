from sklearn import datasets
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import *
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import joblib
from src.models.model import Model


class DecisionTreeClassifierModel(Model):
    def __init__(self):
        super().__init__()
        self.model = None
        self.model_sum = None

        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_pred = None

    def __del__(self):
        del self.model
        del self.model_sum
        del self.X_train
        del self.X_test
        del self.y_train
        del self.y_test
        del self.y_pred

    def example_indicators_win(self):

        database = 'WIN$N_M15'

        dataframe = pd.read_csv(f'src/database/ohlc/{database}.csv', sep=',')

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

        self.X_train, self.X_test, self.y_train, self.y_test = X_train, X_test, y_train, y_test

        classifier = make_pipeline(StandardScaler(), DecisionTreeClassifier())

        classifier.fit(X_train, y_train)
        self.model = classifier

        predicted = classifier.predict(X_test)
        self.y_pred = predicted

        self.model_sum = self.model_summary()


    def model_summary(self):
        DECISION_TREE_CLASSIFIER_ACCURACY_SCORE = accuracy_score(y_pred=self.y_pred, y_true=self.y_test)
        DECISION_TREE_CLASSIFIER_BALANCED_ACCURACY_SCORE = accuracy_score(y_pred=self.y_pred, y_true=self.y_test)
        DECISION_TREE_CLASSIFIER_AVERAGE_PRECISION_SCORE = average_precision_score(y_score=self.y_pred, y_true=self.y_test)
        DECISION_TREE_CLASSIFIER_BRIER_SCORE_LOSS = brier_score_loss(y_prob=self.y_pred, y_true=self.y_test)
        DECISION_TREE_CLASSIFIER_F1_SCORE = f1_score(y_pred=self.y_pred, y_true=self.y_test)
        DECISION_TREE_CLASSIFIER_LOG_LOSS = log_loss(y_pred=self.y_pred, y_true=self.y_test)
        DECISION_TREE_CLASSIFIER_PRECISION = precision_score(y_pred=self.y_pred, y_true=self.y_test)

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

    def save_model(self):
        model_filename = 'src/api/models/DecisionTreeClassifier.pkl'
        print(f'Saving model to {model_filename}...')
        joblib.dump(self.model, model_filename)

        return

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