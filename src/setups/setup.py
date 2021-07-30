from abc import abstractmethod, ABCMeta
from enum import Enum

class OrderType(Enum):
    BUY = 0
    SELL = 1
    BUY_LIMIT = 2
    SELL_LIMIT = 3
    BUY_STOP = 4
    SELL_STOP = 5
    BUY_STOP_LIMIT = 6
    SELL_STOP_LIMIT = 7

class OrderState(Enum):
    PENDING = 0
    FILLED = 1
    CANCELED = 2

def modify_order():
    pass

class Order():
    def __init__(self):
        self.id = None
        self.price: float = None
        self.sl: float = None
        self.tp: float = None
        self.side: OrderType = None
        self.state: OrderState = None
        self.start_date: str = None
        self.end_date: str = None

    def __del__(self):
        pass

    def get_order_id(self):
        return self.id

    def modify_order(self, id):
        pass
    
    def cancel_order(self):
        pass

class Position():
    def __init__(self):
        self.id = None
        self.price = None
        self.sl = None
        self.tp = None
        self.start_date = None
        self.side = None

    def __del__(self):
        pass

    def send_position(self, price: float, sl: float, tp: float, start_date: str) -> None:
        self.price = price
        self.sl = sl
        self.tp = tp
        self.start_date = start_date
        self.side = Side

    def cancel_position(self):
        pass

    def zero_position(self):
        pass


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
