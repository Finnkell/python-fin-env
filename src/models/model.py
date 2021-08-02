from abc import ABCMeta, abstractmethod

class Model(metaclass=ABCMeta):
    def __init__(self):
        return

    def __del__(self):
        return

    @abstractmethod
    def get_data(self) -> None:
        pass

    @abstractmethod
    def example(self) -> None:
        pass

    @abstractmethod
    def create_model(self, **kwargs) -> None:
        pass

    @abstractmethod
    def fit_model(self, X_train: 'DataFrame', y_train: 'DataFrame') -> None:
        pass

    @abstractmethod
    def predict(self, x_test: list or 'DataFrame' or 'np.array') -> list:
        pass

    @abstractmethod
    def evaluate_model(self) -> None:
        pass

    @abstractmethod
    def model_summary(self) -> dict:
        pass

    @abstractmethod
    def save_model(self) -> None:
        pass
