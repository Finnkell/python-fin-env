from abc import ABCMeta, abstractmethod
from enum import Enum

class EnumIndicators(Enum):
    pass

class Indicator(metaclass=ABCMeta):
    def __init__(self):
        pass
    
    @abstractmethod
    def create(self):
        pass