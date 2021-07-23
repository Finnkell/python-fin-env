from sklearn.svm import SVR, NuSVR, LinearSVR, SVC, NuSVC, LinearSVC
from sklearn import datasets
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score, mean_squared_log_error, accuracy_score
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


### Regression Models
class SVRModel:
    def __init__(self):
        self.model = None

    def __del__(self):
        pass

    def example_model_ohlc_win(self, validation_size=0.2):
        dataframe = pd.read_csv('src/database/ohlc/WIN$N_M15.csv', sep=',')
        
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

        regression = make_pipeline(StandardScaler(with_mean=True, with_std=True), SVC(C=100, tol=10e-6))

        self.model = regression
        regression.fit(X_train, y_train)
        predicted = regression.predict(X_test)

        print(f'MSLE: {mean_squared_log_error(predicted, y_test)} WIN$N D1 Dataset')


    def example_model_boston(self, validation_size=0.2):
        X, y = datasets.load_boston(return_X_y=True)

        train_size = int(len(X) * (1 - validation_size))

        X_train, X_test = X[:train_size], X[train_size:len(X)]
        y_train, y_test = y[:train_size], y[train_size:len(y)]

        regression = make_pipeline(StandardScaler(), SVR())

        self.model = regression
        regression.fit(X_train, y_train)
        predicted = regression.predict(X_test)

        print(f'MSLE: {mean_squared_log_error(predicted, y_test)} Boston Dataset')


    def example_model_diabetes(self, validation_size=0.2):
        X, y = datasets.load_diabetes(return_X_y=True)

        train_size = int(len(X) * (1 - validation_size))

        X_train, X_test = X[:train_size], X[train_size:len(X)]
        y_train, y_test = y[:train_size], y[train_size:len(y)]

        regression = make_pipeline(StandardScaler(), SVR())

        regression.fit(X_train, y_train)
        predicted = regression.predict(X_test)

        print(f'MSLE: {mean_squared_log_error(predicted, y_test)} Diabetes Dataset')


    def model_summary(self):
        pass

    def save_model(self):
        model_filename = 'src/api/models/SVR.pkl'
        print(f'Saving model to {model_filename}...')
        joblib.dump(self.model, model_filename)


class NuSVRModel:
    def __init__(self):
        pass

    def __del__(self):
        pass

    def example_model_boston(self, validation_size=0.2):
        X, y = datasets.load_boston(return_X_y=True)

        train_size = int(len(X) * (1 - validation_size))

        X_train, X_test = X[:train_size], X[train_size:len(X)]
        y_train, y_test = y[:train_size], y[train_size:len(y)]

        regression = make_pipeline(StandardScaler(), NuSVR())

        regression.fit(X_train, y_train)
        predicted = regression.predict(X_test)

        print(f'MSLE: {mean_squared_log_error(predicted, y_test)} Boston Dataset')


    def example_model_diabetes(self, validation_size=0.2):
        X, y = datasets.load_diabetes(return_X_y=True)

        train_size = int(len(X) * (1 - validation_size))

        X_train, X_test = X[:train_size], X[train_size:len(X)]
        y_train, y_test = y[:train_size], y[train_size:len(y)]

        regression = make_pipeline(StandardScaler(), NuSVR())

        regression.fit(X_train, y_train)
        predicted = regression.predict(X_test)

        print(f'MSLE: {mean_squared_log_error(predicted, y_test)} Diabetes Dataset')


    def model_summary(self):
        pass


class LinearSVRModel:
    def __init__(self):
        pass

    def __del__(self):
        pass

    def example_model_boston(self, validation_size=0.2):
        X, y = datasets.load_boston(return_X_y=True)

        train_size = int(len(X) * (1 - validation_size))

        X_train, X_test = X[:train_size], X[train_size:len(X)]
        y_train, y_test = y[:train_size], y[train_size:len(y)]

        regression = make_pipeline(StandardScaler(), LinearSVR())

        regression.fit(X_train, y_train)
        predicted = regression.predict(X_test)

        print(f'MSLE: {mean_squared_log_error(predicted, y_test)} Boston Dataset')


    def example_model_diabetes(self, validation_size=0.2):
        X, y = datasets.load_diabetes(return_X_y=True)

        train_size = int(len(X) * (1 - validation_size))

        X_train, X_test = X[:train_size], X[train_size:len(X)]
        y_train, y_test = y[:train_size], y[train_size:len(y)]

        regression = make_pipeline(StandardScaler(), LinearSVR())

        regression.fit(X_train, y_train)
        predicted = regression.predict(X_test)

        print(f'MSLE: {mean_squared_log_error(predicted, y_test)} Diabetes Dataset')


    def model_summary(self):
        pass


### Classification Models

class SVCModel:
    def __init__(self):
        pass

    def __del__(self):
        pass

    def example_model_ohlc_win(self, validation_size=0.2):
        dataframe = pd.read_csv('src/database/ohlc/PETR4_M1.csv', sep=',')

        dataframe = dataframe.drop(['Ticks', 'Volume', 'Spread', 'Date', 'Time'], axis=1)

        X = dataframe

        value = dataframe['Close'][dataframe.index[-1]]
        temp = pd.DataFrame(X['Close'].shift(-1).fillna(value))

        y = pd.DataFrame()

        y['Signal'] = np.where(dataframe['Close'] < temp['Close'], 1, 0)

        train_size = int(len(X) * (1 - validation_size))

        X_train, X_test = X[:train_size], X[train_size:len(X)]
        y_train, y_test = y[:train_size], y[train_size:len(y)]

        regression = make_pipeline(MinMaxScaler(), SVC())

        self.model = regression
        regression.fit(X_train, y_train)
        predicted = regression.predict(X_test)

        print(f'MSLE: {mean_squared_log_error(predicted, y_test)} WIN$N D1 Dataset')

    def example_model_breast_cancer(self, validation_size=0.2):
        X, y = datasets.load_breast_cancer(return_X_y=True)

        train_size = int(len(X) * (1 - validation_size))

        X_train, X_test = X[:train_size], X[train_size:len(X)]
        y_train, y_test = y[:train_size], y[train_size:len(y)]

        regression = make_pipeline(StandardScaler(), SVC())

        regression.fit(X_train, y_train)
        predicted = regression.predict(X_test)

        print(f'Accuracy: {accuracy_score(predicted, y_test)} Breast Cancer Dataset')


    def example_model_rcv1(self, validation_size=0.2):
        X, y = datasets.fetch_rcv1(return_X_y=True)

        train_size = int(X.shape[0] * (1 - validation_size))

        X_train, X_test = X[:train_size], X[train_size:X.shape[0]]
        y_train, y_test = y[:train_size], y[train_size:y.shape[0]]

        regression = make_pipeline(StandardScaler(with_mean=False), SVC())

        regression.fit(X_train, y_train)
        predicted = regression.predict(X_test)

        print(f'Accuracy: {accuracy_score(predicted, y_test)} RCV1 Dataset')


    def model_summary(self):
        pass


class NuSVCModel:
    def __init__(self):
        pass

    def __del__(self):
        pass

    def example_model_breast_cancer(self, validation_size=0.2):
        X, y = datasets.load_breast_cancer(return_X_y=True)

        train_size = int(len(X) * (1 - validation_size))

        X_train, X_test = X[:train_size], X[train_size:len(X)]
        y_train, y_test = y[:train_size], y[train_size:len(y)]

        regression = make_pipeline(StandardScaler(), NuSVC())

        regression.fit(X_train, y_train)
        predicted = regression.predict(X_test)

        print(f'Accuracy: {accuracy_score(predicted, y_test)} Breast Cancer Dataset')


    def example_model_rcv1(self, validation_size=0.2):
        X, y = datasets.fetch_rcv1(return_X_y=True)

        train_size = int(X.shape[0] * (1 - validation_size))

        X_train, X_test = X[:train_size], X[train_size:X.shape[0]]
        y_train, y_test = y[:train_size], y[train_size:y.shape[0]]

        regression = make_pipeline(StandardScaler(with_mean=False), NuSVC())

        regression.fit(X_train, y_train)
        predicted = regression.predict(X_test)

        print(f'Accuracy: {accuracy_score(predicted, y_test)} RCV1 Dataset')


    def model_summary(self):
        pass


class LinearSVCModel:
    def __init__(self):
        pass

    def __del__(self):
        pass

    def example_model_breast_cancer(self, validation_size=0.2):
        X, y = datasets.load_breast_cancer(return_X_y=True)

        train_size = int(len(X) * (1 - validation_size))

        X_train, X_test = X[:train_size], X[train_size:len(X)]
        y_train, y_test = y[:train_size], y[train_size:len(y)]

        regression = make_pipeline(StandardScaler(), LinearSVC())

        regression.fit(X_train, y_train)
        predicted = regression.predict(X_test)

        print(f'Accuracy: {accuracy_score(predicted, y_test)} Breast Cancer Dataset')


    def example_model_rcv1(self, validation_size=0.2):
        # X, y = datasets.fetch_rcv1(return_X_y=True).todense()

        # train_size = int(X.shape[0] * (1 - validation_size))

        # X_train, X_test = X[:train_size], X[train_size:X.shape[0]]
        # y_train, y_test = y[:train_size], y[train_size:y.shape[0]]

        # regression = make_pipeline(StandardScaler(with_mean=False), LinearSVC())

        # regression.fit(X_train, y_train)
        # predicted = regression.predict(X_test)

        # print(f'Accuracy: {accuracy_score(predicted, y_test)} RCV1 Dataset')
        pass

    def model_summary(self):
        pass