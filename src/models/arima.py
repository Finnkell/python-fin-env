from statsmodel.tsa.arima.model import SARIMAX, ARIMA
from sklearn.metrics import mean_squared_error

class ARIMAModel:

    def __init__(self):
        self.model = None
        self.model_fit = None
        self.predict = None

        self.X_train = None
        self.y_train = None
        self.X_train = None
        self.y_test = None

        self.order = (1, 0, 0)

    def get_data(self, X, y, test_size=0.2):
        train_size = int(len(X)*(1-test_size))
        self.X_train, self.X_test = X[0: train_size], X[train_size:len(X)]
        self.y_train, self.y_test = y[0: train_size], y[train_size:len(X)]

    def create_mode(self):
        self.model = SARIMAX(endog=self.X_train, exog=self.y_train, order=self.order)

    def fit_model(self):
        self.model_fit = self.model.fit()

    def predict_model(self):
        self.predict = self.model_fit.predict(start=(len(X_train) - 1), end=(len(X) - 1), exog=self.X_test)

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

    def create_mode(self):
        pass

    def train_model(self):
        pass

    def predict_model(self):
        pass

    def evaluate_model(self):
        pass
