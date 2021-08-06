from abc import abstractmethod, ABCMeta

class Setup(metaclass=ABCMeta):
    def __init__(self):
        pass

    def __del__(self):
        pass

    @abstractmethod
    def get_indicators_params(self, position: Position()) -> dict:
        pass

    @abstractmethod
    def get_setup_params(self) -> dict:
        pass

    @abstractmethod
    def signal_buy(self, **kwargs) -> bool:
        pass
    
    @abstractmethod
    def signal_sell(self, **kwargs) -> bool:
        pass

    @abstractmethod
    def get_stack_info_from_pre_setup_processing(self, datetime, price, restults: dict, **kwargs):
        pass

    @abstractmethod
    def export_backtesting_info(self):
        pass

    @abstractmethod
    def get_orders(self):
        pass

    @abstractmethod
    def get_any_position(self):
        pass