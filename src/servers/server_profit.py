#Imports para execução da DLL
import time
import gc
from ctypes import *
from ctypes.wintypes import UINT
import struct
from utils.utils_profit import *

#Caminho para a DLL, python tem que ser 32bits
profit_dll = WinDLL('./ProfitDLL.dll')
profit_dll.argtypes  = None


class ProfitConnection:
#%%
    def __init__(self, password):
        try: 
            global profit_dll
            key = input("Chave de acesso: ")
            bRoteamento = True
            
            if bRoteamento:
                result = profit_dll.DLLInitialize(c_wchar_p(key), stateCallback, historyCallBack, accountCallback, newTradeCallback, newDailyCallback, priceBookCallback, offerBookCallback, newHistoryCallback, progressCallBack, newTinyBookCallBack)
            else:
                result = profit_dll.InitializeMarket(c_wchar_p(key), stateCallback, newTradeCallback, newDailyCallback, priceBookCallback, offerBookCallback, newHistoryCallback, progressCallBack, newTinyBookCallBack)

            profit_dll.SendSellOrder.restype = c_longlong
            profit_dll.SendBuyOrder.restype = c_longlong
            profit_dll.SendStopBuyOrder.restype = c_longlong
            profit_dll.SendStopSellOrder.restype = c_longlong
            profit_dll.SendZeroPosition.restype = c_longlong

            print('DLLInitialize: ' + str(result))
            wait_login()
        
        except Exception as e:
            print(str(e))
        
        self.api = profit_dll

        self.bolsa = None
        self.asset = None
        
        self.conta = None
        self.broker = None
        self.password = password

        self.order_id = None

#%%
    def __del__(self):
        result = self.api.DLLFinalize()
        self.api = None

        print('DLLFinalize: ' + str(result))

#%%
    @WINFUNCTYPE(None, c_int, c_wchar_p, c_double, c_double, c_double)
    def buy_limit_order(self, volume, ticket, price, sl, tp):
        price = float(price)
        volume = int(volume)

        if self.api == None: return None

        result = self.api.SendBuyOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticket), c_wchar_p(self.bolsa), c_double(price), c_int(volume))

        # if sl > price or tp < price:
        #     return None
            
        # sl = float(price - sl)
        # tp = float(price + tp)

        # take_profit = profit_dll.SendSellOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticket), c_wchar_p(self.bolsa), c_double(tp), c_int(volume))
        # stop_loss = profit_dll.SendStopSellOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticket), c_wchar_p(self.bolsa), c_double(sl), c_int(volume))

        print(f'SendOrder = {str(result)}')
        
#%%
    @WINFUNCTYPE(None, c_int, c_wchar_p, c_double, c_double, c_double)
    def sell_limit_order(self, volume, ticket, price, sl, tp):
        price = float(price)
        volume = int(volume)

        if self.api == None: return None

        result = self.api.SendSellOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticket), c_wchar_p(self.bolsa), c_double(price), c_int(volume))

        # if sl < price or tp > price:
        #     return None+

        # sl = float(price + sl)
        # tp = float(price - tp)

        # take_profit = profit_dll.SendBuyOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticket), c_wchar_p(self.bolsa), c_double(tp), c_int(volume))
        # stop_loss = profit_dll.SendStopBuyOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticket), c_wchar_p(self.bolsa), c_double(sl), c_int(volume))

        print(f'SendOrder = {str(result)}')

#%%
    @WINFUNCTYPE(None, c_int, c_wchar_p, c_double)
    def buy_stop_order(self, volume, ticket, price):

        price = float(price)
        volume = int(volume)

        if self.api == None: return None

        result = self.api.SendStopBuyOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticket), c_wchar_p(self.bolsa), c_double(price), c_int(volume))

        print(f'SendOrder = {str(result)}')
        
#%%
    @WINFUNCTYPE(None, c_int, c_wchar_p, c_double)
    def sell_stop_order(self, volume, ticket, price):

        price = float(price)
        volume = int(volume)

        if self.api == None: return None

        result = self.api.SendStopSellOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticket), c_wchar_p(self.bolsa), c_double(price), c_int(volume))

        print(f'SendOrder = {str(result)}')

    
#%% 
    def subscribe_ticket(self):
        if self.api == None: return None

        asset = input('Asset: ')
        bolsa = input('Bolsa: ')

        self.bolsa = bolsa
        self.asset = asset
        
        result = self.api.SubscribeTicker(c_wchar_p(asset), c_wchar_p(bolsa))
        print ("Ticker Subscribed: " + str(result))

#%%
    def unsubscribe_ticker(self):
        if self.api == None: return None

        self.bolsa = bolsa
        self.asset = asset
        
        result = self.api.UnsubscribeTicker(c_wchar_p(asset), c_wchar_p(bolsa))
        print ("Ticker Unsubscribed: " + str(result))

#%%
    def subscribe_book_offer(self):
        if self.api == None: return None

        asset = input('Asset: ')
        bolsa = input('Bolsa: ')

        self.bolsa = bolsa
        self.asset = asset

        result = self.api.SubscribeOfferBook(c_wchar_p(asset), c_wchar_p(bolsa))
        print ("Book Offer Subscribed: " + str(result))

#%%
    def unsubscribe_book_offer(self):
        if self.api == None: return None

        self.bolsa = bolsa
        self.asset = asset

        result = self.api.UnsubscribeOfferBook(c_wchar_p(asset), c_wchar_p(bolsa))
        print ("Book Offer Unsubscribed: " + str(result))

#%%
    def order_change(self):
        if self.api == None: return None

        result = self.api.SendChangeOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(self.order_id))

        print ("Book Offer Unsubscribed: " + str(result))


#%%
    @WINFUNCTYPE(None, c_wchar_p, c_wchar_p)
    def get_orders_total(self, datetime_start, datetime_end):
        if self.api == None: return None

        return self.api.GetOrders(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(datetime_start), c_wchar_p(datetime_end))
                                                                 
#%%
    def get_position(self, ticker):
        if self.api == None: return None

        return self.api.GetPosition(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(ticker), c_wchar_p(self.bolsa))
#%%
    @WINFUNCTYPE(None, TChangeCotation)
    def last_tick(self, cotation):
        return cotation.last_price

#%%
    def ohlc_by_timeframe(self, timeframe):
        pass