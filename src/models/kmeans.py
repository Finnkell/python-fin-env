from sklearn.cluster import KMeans
from sklearn import datasets
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_log_error
import numpy as np


class KMeansModel():
    def __init__(self):
        pass

    def __del__(self):
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
