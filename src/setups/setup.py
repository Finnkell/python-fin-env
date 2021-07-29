from abc import abstractmethod, ABCMeta

class Setup(metaclass=ABCMeta):
    def __init__(self):
        pass

    def __del__(self):
        pass

    @abstractmethod
    def signal_buy(self) -> bool:
        pass
    
    @abstractmethod
    def signal_sell(self) -> bool:
        pass

    @abstractmethod
    def get_stack_info_from_pre_setup_processing(self, datetime, price, restults: dict, **kwargs):
        pass

    @abstractmethod
    def export_backtesting_info(self):
        pass