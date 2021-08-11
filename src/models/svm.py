from src.models.model import Model

from sklearn.svm import SVR, NuSVR, LinearSVR, SVC, NuSVC, LinearSVC
from sklearn import datasets
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import *

import joblib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


'''
>>> Regression Models: SVR, NuSVR, LinearSVR
'''
class SVRModel(Model):
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

    def __str__(self):
        print(f'Support Vector Machine Regressor model: {self.__model}')


    def create_model(self, C: float=1.0, kernel: str='rbf', degree: int=3, gamma: str='scale', coef0: float=0.0, tol: float=1e-3, epsilon: float=0.1, shrinking: bool=True, cache_size: float=200.0, verbose: bool=False, max_iter: int=-1) -> None:

        if type(C) != float or type(kernel) != str or type(degree) != int or type(gamma) != str or type(coef0) != float or type(tol) != float or type(epsilon) != float or type(shrinking) != bool or type(cache_size) != float or type(verbose) != bool or type(max_iter) != int: 
            raise TypeError

        self.__model = make_pipeline(StandardScaler(), SVR(C=C, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0, tol=tol, epsilon=epsilon, shrinking=shrinking, cache_size=cache_size, verbose=verbose, max_iter=max_iter))


    def get_data(self, dataframe: pd.DataFrame()=None) -> None:
        if type(dataframe) != type(pd.DataFrame()) and dataframe == None:
            raise ValueError
        return None

    def example(self):
        return None

    def fit_model(self, X_train, y_train):
        self.__model.fit(X_train, y_train)

    def predict(self, X_pred):
        self.__y_pred = self.__model.predict(X_pred)
        return self.__y_pred

    def evaluate_model(self):
        raise NotImplementedError

    def model_summary(self):
        SVR_ACCURACY = accuracy_score(y_pred, y_test)
        SVR_R2SCORE = r2_score(y_pred, y_test)
        return {}

    def save_model(self):
        model_filename = 'src/api/models/SVR.pkl'
        print(f'Saving model to {model_filename}...')
        joblib.dump(self.__model, model_filename)


class NuSVRModel(Model):
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

    def __str__(self):
        print(f'Nu Support Vector Machine Regressor model: {self.__model}')

    def create_model(self, C: float=1.0, kernel: str='rbf', degree: int=3, gamma: str='scale', coef0: float=0.0, tol: float=1e-3, epsilon: float=0.1, shrinking: bool=True, cache_size: float=200.0, verbose: bool=False, max_iter: int=-1) -> None:

        if type(C) != float or type(kernel) != str or type(degree) != int or type(gamma) != str or type(coef0) != float or type(tol) != float or type(epsilon) != float or type(shrinking) != bool or type(cache_size) != float or type(verbose) != bool or type(max_iter) != int: 
            raise TypeError

        self.__model = make_pipeline(StandardScaler(), SVR(C=C, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0, tol=tol, epsilon=epsilon, shrinking=shrinking, cache_size=cache_size, verbose=verbose, max_iter=max_iter))

    def get_data(self, dataframe=None):
        if type(dataframe) != type(pd.DataFrame()) and dataframe == None:
            raise ValueError
        return None

    def example(self):
        return None

    def fit_model(self, X_train, y_train):
        self.__model.fit(X_train, y_train)

    def predict(self, X_pred):
        self.__y_pred = self.__model.predict(X_pred)
        return self.__y_pred

    def evaluate_model(self):
        raise NotImplementedError
    
    def model_summary(self):
        summary = {}
        return summary

    def save_model(self):
        model_filename = 'src/api/models/NuSVR.pkl'
        print(f'Saving model to {model_filename}...')
        joblib.dump(self.__model, model_filename)


class LinearSVRModel(Model):
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

    def __str__(self):
        print(f'Linear Support Vector Machine Regressor model: {self.__model}')

    def create_model(self, C: float=1.0, kernel: str='rbf', degree: int=3, gamma: str='scale', coef0: float=0.0, tol: float=1e-3, epsilon: float=0.1, shrinking: bool=True, cache_size: float=200.0, verbose: bool=False, max_iter: int=-1) -> None:

        if type(C) != float or type(kernel) != str or type(degree) != int or type(gamma) != str or type(coef0) != float or type(tol) != float or type(epsilon) != float or type(shrinking) != bool or type(cache_size) != float or type(verbose) != bool or type(max_iter) != int: 
            raise TypeError

        self.__model = make_pipeline(StandardScaler(), SVR(C=C, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0, tol=tol, epsilon=epsilon, shrinking=shrinking, cache_size=cache_size, verbose=verbose, max_iter=max_iter))

    def get_data(self, dataframe=None):
        if type(dataframe) != type(pd.DataFrame()) and dataframe == None:
            raise ValueError
        return None

    def example(self):
        return None

    def fit_model(self, X_train, y_train):
        self.__model.fit(X_train, y_train)

    def predict(self, X_pred):
        self.__y_pred = self.__model.predict(X_pred)
        return self.__y_pred

    def evaluate_model(self):
        raise NotImplementedError
    
    def model_summary(self):
        summary = {}
        return summary

    def save_model(self):
        model_filename = 'src/api/models/LinearSVR.pkl'
        print(f'Saving model to {model_filename}...')
        joblib.dump(self.__model, model_filename)


'''
>>> Classification Models: SVC, NuSVC, LinearSVC
'''
class SVCModel(Model):
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

    def __str__(self):
        print(f'Support Vector Machine Classifier model: {self.__model}')


    def example_model_ohlc_win(self, validation_size=0.2):
        database = 'WIN$N_M15'

        dataframe = pd.read_csv(f'src/database/ohlc/{database}.csv', sep=',')
        
        dataframe = dataframe.drop(['Ticks', 'Volume', 'Spread', 'Date', 'Time'], axis=1)

        X = dataframe

        value = dataframe['Close'][dataframe.index[-1]]
        temp = pd.DataFrame(X['Close'].shift(-1).fillna(value))

        y = pd.DataFrame()

        y['Diff'] = dataframe['Open']/temp['Close']
        y['Signal'] = np.where(y['Diff'] > 1, 1, 0)
        y = y.drop(['Diff'], axis=1)

        train_size = int(len(X) * (1 - validation_size))

        X_train, X_test = X[:train_size], X[train_size:len(X)]
        y_train, y_test = y[:train_size], y[train_size:len(y)]

        self.__X_train, self.__X_test, self.__y_train, self.__y_test = X_train, X_test, y_train, y_test

        regression = make_pipeline(StandardScaler(with_mean=True, with_std=True), SVC(C=100, tol=10e-6))

        regression.fit(X_train, y_train)
        self.__model = regression

        predicted = regression.predict(X_test)
        self.__y_pred = predicted

        self.__model_sum = self.__model_summary()

    def create_model(self, C: float=1.0, kernel: str='rbf', degree: int=3, gamma: str='scale', coef0: float=0.0, tol: float=1e-3, epsilon: float=0.1, shrinking: bool=True, cache_size: float=200.0, verbose: bool=False, max_iter: int=-1) -> None:

        if type(C) != float or type(kernel) != str or type(degree) != int or type(gamma) != str or type(coef0) != float or type(tol) != float or type(epsilon) != float or type(shrinking) != bool or type(cache_size) != float or type(verbose) != bool or type(max_iter) != int: 
            raise TypeError

        self.__model = make_pipeline(StandardScaler(), SVR(C=C, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0, tol=tol, epsilon=epsilon, shrinking=shrinking, cache_size=cache_size, verbose=verbose, max_iter=max_iter))


    def get_data(self, dataframe):
        if type(dataframe) != type(pd.DataFrame()) and dataframe == None:
            raise ValueError
        return None

    def example(self):
        return None

    def fit_model(self, X_train, y_train):
        self.__model.fit(X_train, y_train)

    def predict(self, X_pred):
        self.__y_pred = self.__model.predict(X_pred)
        return self.__y_pred

    def evaluate_model(self):
        raise NotImplementedError

    def model_summary(self):
        SVC_ACCURACY_SCORE = accuracy_score(y_pred=self.__y_pred, y_true=self.__y_test)
        SVC_BALANCED_ACCURACY_SCORE = accuracy_score(y_pred=self.__y_pred, y_true=self.__y_test)
        SVC_AVERAGE_PRECISION_SCORE = average_precision_score(y_score=self.__y_pred, y_true=self.__y_test)
        SVC_BRIER_SCORE_LOSS = brier_score_loss(y_prob=self.__y_pred, y_true=self.__y_test)
        SVC_F1_SCORE = f1_score(y_pred=self.__y_pred, y_true=self.__y_test)
        SVC_LOG_LOSS = log_loss(y_pred=self.__y_pred, y_true=self.__y_test)
        SVC_PRECISION = precision_score(y_pred=self.__y_pred, y_true=self.__y_test)

        summary = {
            'accuracy_score': SVC_ACCURACY_SCORE,
            'balanced_accuracy_score': SVC_BALANCED_ACCURACY_SCORE,
            'average_precision_score': SVC_AVERAGE_PRECISION_SCORE,
            'brier_score_loss': SVC_BRIER_SCORE_LOSS,
            'f1_score': SVC_F1_SCORE,
            'log_score': SVC_LOG_LOSS,
            'precision_score': SVC_PRECISION
        }

        return summary

    def save_model(self):
        model_filename = 'src/api/models/SVC.pkl'
        model_summary_filename = 'src/api/models/SVC_SUMMARY.pkl'
        
        print(f'Saving model to {model_filename}...')
        print(f'Saving model summary to {model_summary_filename}...')

        joblib.dump(self.__model, model_filename)
        joblib.dump(self.__model_sum, model_summary_filename)


class NuSVCModel(Model):
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

    def __str__(self):
        print(f'Nu Support Vector Machine Classifier model: {self.__model}')

    def create_model(self, C: float=1.0, kernel: str='rbf', degree: int=3, gamma: str='scale', coef0: float=0.0, tol: float=1e-3, epsilon: float=0.1, shrinking: bool=True, cache_size: float=200.0, verbose: bool=False, max_iter: int=-1) -> None:

        if type(C) != float or type(kernel) != str or type(degree) != int or type(gamma) != str or type(coef0) != float or type(tol) != float or type(epsilon) != float or type(shrinking) != bool or type(cache_size) != float or type(verbose) != bool or type(max_iter) != int: 
            raise TypeError

        self.__model = make_pipeline(StandardScaler(), SVR(C=C, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0, tol=tol, epsilon=epsilon, shrinking=shrinking, cache_size=cache_size, verbose=verbose, max_iter=max_iter))

    def get_data(self, dataframe):
        if type(dataframe) != type(pd.DataFrame()) and dataframe == None:
            raise ValueError
        return None

    def example(self):
        return None

    def fit_model(self, X_train, y_train):
        self.__model.fit(X_train, y_train)

    def predict(self, X_pred):
        self.__y_pred = self.__model.predict(X_pred)
        return self.__y_pred

    def evaluate_model(self):
        raise NotImplementedError
    
    def model_summary(self):
        summary = {}
        return summary

    def save_model(self):
        model_filename = 'src/api/models/NuSVC.pkl'
        print(f'Saving model to {model_filename}...')
        joblib.dump(self.__model, model_filename)


class LinearSVCModel(Model):
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

    def __str__(self):
        print(f'Linear Support Vector Machine Classifier model: {self.__model}')


    def create_model(self, C: float=1.0, kernel: str='rbf', degree: int=3, gamma: str='scale', coef0: float=0.0, tol: float=1e-3, epsilon: float=0.1, shrinking: bool=True, cache_size: float=200.0, verbose: bool=False, max_iter: int=-1) -> None:

        if type(C) != float or type(kernel) != str or type(degree) != int or type(gamma) != str or type(coef0) != float or type(tol) != float or type(epsilon) != float or type(shrinking) != bool or type(cache_size) != float or type(verbose) != bool or type(max_iter) != int: 
            raise TypeError

        self.__model = make_pipeline(StandardScaler(), SVR(C=C, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0, tol=tol, epsilon=epsilon, shrinking=shrinking, cache_size=cache_size, verbose=verbose, max_iter=max_iter))

    def get_data(self, dataframe):
        if type(dataframe) != type(pd.DataFrame()) and dataframe == None:
            raise ValueError
        return None

    def example(self):
        return None

    def fit_model(self, X_train, y_train):
        self.__model.fit(X_train, y_train)

    def predict(self, X_pred):
        self.__y_pred = self.__model.predict(X_pred)
        return self.__y_pred

    def evaluate_model(self):
        raise NotImplementedError
    
    def model_summary(self):
        summary = {}
        return summary

    def save_model(self):
        model_filename = 'src/api/models/linearSVC.pkl'
        print(f'Saving model to {model_filename}...')
        joblib.dump(self.__model, model_filename)