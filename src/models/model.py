from abc import ABCMeta, abstractmethod

class Model(metaclass=ABCMeta):
    def __init__(self):
        return

    def __del__(self):
        return

    @abstractmethod
    def example(self):
        pass

    @abstractmethod
    def create_model(self, **kwargs):
        pass

    @abstractmethod
    def fit_model(self, X_train: 'DataFrame', y_train: 'DataFrame'):
        pass

    @abstractmethod
    def predict(self, x_test: list or 'DataFrame' or 'np.array'):
        pass

    @abstractmethod
    def evaluate_model(self):
        pass

    @abstractmethod
    def model_summary(self):
        pass

    @abstractmethod
    def save_model(self):
        pass
