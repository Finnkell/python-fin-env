from sklearn.svm import SVR, NuSVR, LinearSVR, SVC, NuSVC, LinearSVC
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score, mean_squared_log_error, accuracy_score


### Regression Models
class SVRModel:
    def __init__(self):
        pass

    def __del__(self):
        pass

    def example_model_boston(self, validation_size=0.2):
        X, y = datasets.load_boston(return_X_y=True)

        train_size = int(len(X) * (1 - validation_size))

        X_train, X_test = X[:train_size], X[train_size:len(X)]
        y_train, y_test = y[:train_size], y[train_size:len(y)]

        regression = make_pipeline(StandardScaler(), SVR())

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

        train_size = int(len(X) * (1 - validation_size))

        X_train, X_test = X[:train_size], X[train_size:len(X)]
        y_train, y_test = y[:train_size], y[train_size:len(y)]

        regression = make_pipeline(StandardScaler(), SVC())

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

        train_size = int(len(X) * (1 - validation_size))

        X_train, X_test = X[:train_size], X[train_size:len(X)]
        y_train, y_test = y[:train_size], y[train_size:len(y)]

        regression = make_pipeline(StandardScaler(), NuSVC())

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
        X, y = datasets.fetch_rcv1(return_X_y=True)

        train_size = int(len(X) * (1 - validation_size))

        X_train, X_test = X[:train_size], X[train_size:len(X)]
        y_train, y_test = y[:train_size], y[train_size:len(y)]

        regression = make_pipeline(StandardScaler(), LinearSVC())

        regression.fit(X_train, y_train)
        predicted = regression.predict(X_test)

        print(f'Accuracy: {accuracy_score(predicted, y_test)} RCV1 Dataset')


    def model_summary(self):
        pass