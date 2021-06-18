#Imports para execução da DLL
import time
import gc
from ctypes import *
from ctypes.wintypes import UINT
import struct

#Caminho para a DLL, python tem que ser 32bits
profit_dll = WinDLL('./ProfitDLL.dll')
profit_dll.argtypes  = None

# Error Codes
NL_ERR_INIT = 80
NL_OK = 0
NL_ERR_INVALID_ARGS = 90
NL_ERR_INTERNAL_ERROR = 100


class ProfitConnection:

    def __init__(self):
        pass

    def __del__(self):
        pass

    def buy_order(self):
        pass

    def sell_order(self, volume, ticket, price):
        price = float(price)
        volume = int(volume)

        result = profit_dll.SendSellOrder(c_wchar_p(), c_wchar_p(), c_wchar_p(), c_wchar_p(ticket), c_wchar_p(), c_double(price), c_int(volume))

        print(f'SendOrder = {str(result)}')
        