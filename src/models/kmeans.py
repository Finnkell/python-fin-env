from src.models.model import Model

from sklearn.cluster import KMeans
from sklearn import datasets
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_log_error

import numpy as np
import pandas as pd
import joblib

class KMeansModel(Model):
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
        pass


    def create_model(self, **kwargs):
        self.__model = make_pipeline(StandardScaler(), KMeans())

    def get_data(self, dataframe):
        pass

    def example(self):
        pass

    def fit_model(self, X_train, y_train):
        pass

    def predict(self, X_test):
        pass

    def evaluate_model(self):
        pass

    def save_model(self):
        pass

    def model_summary(self):
        pass

    def example_model_iris(self, validation_size=0.2):
        X, y = datasets.load_iris(return_X_y=True)

        train_size = int(len(X) * (1 - validation_size))

        X_train, X_test = X[:train_size], X[train_size:len(X)]
        y_train, y_test = y[:train_size], y[train_size:len(y)]

        clustering = make_pipeline(StandardScaler(), KMeans())

        clustering.fit(X_train, y_train)
        predicted = clustering.predict(X_test)

        print(f'MSLE: {mean_squared_log_error(predicted, y_test)} Boston Dataset')


class MiniBatchKMeansModel():
    def __init__(self):
        pass

    def __del__(self):
        pass

    def example_model_boston(self):
        pass
