#Imports para execução da DLL
import time
import gc
from ctypes import *
from ctypes.wintypes import UINT
import struct
from src.servers.utils.utils_profit import *
from time import sleep

#Caminho para a DLL, python tem que ser 32bits
profit_dll = WinDLL('./ProfitDLL.dll')
profit_dll.argtypes  = None

# Globals
b_ativo = False
b_market_connected = False 
b_connected = False
b_broker_connected = False
n_count = 0

price_array_sell = []
price_array_buy = []

ticker_flag = None

class ProfitConnection:
#%%
    def __init__(self, key, password=1234):
        global profit_dll
        
        self.key = str(key)
        self.api = profit_dll
        self.result = None

        try: 
            b_roteamento = True

            if b_roteamento:
                try:
                    self.result = self.api.DLLInitialize(c_wchar_p(self.key), state_callback, history_callback, order_change_callback, account_callback, new_trade_callback, new_daily_callback, price_book_callback, offer_book_callback, new_history_callback, progress_callback, new_tinybook_callback, change_cotation_callback, new_daily_callback)
                except Exception as e:
                    print(f'ERROR: {e}')
                    
            else:
                try:
                    self.result = self.api.InitializeMarket(c_wchar_p(self.key), state_callback, new_trade_callback, new_daily_callback, price_book_callback, offer_book_callback, new_history_callback, progress_callback, new_tinybook_callback)
                except Exception as e:
                    print(f'MARKET ERROR: {e}')
                
            self.api.SendSellOrder.restype = c_longlong
            self.api.SendBuyOrder.restype = c_longlong
            self.api.SendStopBuyOrder.restype = c_longlong
            self.api.SendStopSellOrder.restype = c_longlong
            self.api.SendZeroPosition.restype = c_longlong

            print('DLLInitialize: ' + str(self.result))

            self.wait_login()
        
        except Exception as e:
            print(f'{str(e)}')
        
        self.bolsa = 'B'
        self.asset = None
        
        self.conta = '70275403'
        self.broker = '33001'
        self.password = 'BCBnWv4lJ1'

        self.order_id = None

#%%
    def __del__(self):
        sleep(5)
        result = self.api.DLLFinalize()
        del self.api
        
        print('DLLFinalize: ' + str(result))
#%%
    def wait_login(self):    
        bWaiting = True
        global b_market_connected

        while bWaiting:
            if b_market_connected:
                self.api.SetAssetListCallback(asset_list_callback)
                print("DLL Conected")
                
                bWaiting = False

#%%
    def get_account(self):
        return self.api.GetAccount()

#%%
    def buy_limit_order(self, volume, ticker, price, sl=0, tp=0):
        price = float(price)
        volume = int(volume)

        if self.api == None: return None

        result = self.api.SendBuyOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticker), c_wchar_p(self.bolsa), c_double(price), c_int(volume))

        # if sl > price or tp < price:
        #     return None
            
        # sl = float(price - sl)
        # tp = float(price + tp)

        # take_profit = profit_dll.SendSellOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticket), c_wchar_p(self.bolsa), c_double(tp), c_int(volume))
        # stop_loss = profit_dll.SendStopSellOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticket), c_wchar_p(self.bolsa), c_double(sl), c_int(volume))

        print(f'SendBuyOrder = {str(result)}')
        
#%%
    def sell_limit_order(self, volume, ticker, price, sl, tp):
        price = float(price)
        volume = int(volume)

        if self.api == None: return None

        result = self.api.SendSellOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticker), c_wchar_p(self.bolsa), c_double(price), c_int(volume))

        # if sl < price or tp > price:
        #     return None+

        # sl = float(price + sl)
        # tp = float(price - tp)

        # take_profit = profit_dll.SendBuyOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticket), c_wchar_p(self.bolsa), c_double(tp), c_int(volume))
        # stop_loss = profit_dll.SendStopBuyOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticket), c_wchar_p(self.bolsa), c_double(sl), c_int(volume))

        print(f'SendSellOrder = {str(result)}')

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
    def subscribe_ticker(self, ticker, bolsa, flag='OHLC'):
        if self.api == None: return None

        global ticker_flag

        ticker_flag = flag

        asset = ticker
        bolsa = bolsa

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
    def subscribe_offer_book(self, ticker, bolsa):
        if self.api == None: return None

        asset = ticker
        bolsa = bolsa

        result = self.api.SubscribeOfferBook(c_wchar_p(asset), c_wchar_p(bolsa))
        print ("Book Offer Subscribed: " + str(result))

#%%
    def unsubscribe_offer_book(self):
        if self.api == None: return None

        self.bolsa = bolsa
        self.asset = asset

        result = self.api.UnsubscribeOfferBook(c_wchar_p(asset), c_wchar_p(bolsa))
        print ("Book Offer Unsubscribed: " + str(result))

#%%
    def subscribe_price_book(self, ticker, bolsa, flag='TRADE'):
        if self.api == None: return None

        asset = ticker
        bolsa = bolsa

        global ticker_flag

        ticker_flag = flag

        result = self.api.SubscribePriceBook(c_wchar_p(asset), c_wchar_p(bolsa))

        print(f'Price Book Subscribe: {str(result)}')


#%%
    def get_ticker_info(self, ticker, bolsa):
        if self.api == None: return None

        asset = ticker
        bolsa = bolsa

        result = self.api.RequestTickerInfo(c_wchar_p(asset), c_wchar_p(bolsa))

        print(f'Ticker Info Request: {str(result)}')

#%%
    def order_change(self):
        if self.api == None: return None

        result = self.api.SendChangeOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(self.order_id))

        print ("Book Offer Unsubscribed: " + str(result))

#%%
    def send_zero_position(self, ticker, price):
        result = self.api.SendZeroPosition(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(ticker), c_wchar_p(self.bolsa), c_wchar_p(self.password), c_wchar_p(price))

        print(f'Zero Position: {result}')
#%%
    def get_orders_total(self, datetime_start, datetime_end):
        if self.api == None: return None

        return self.api.GetOrders(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(datetime_start), c_wchar_p(datetime_end))
                                                                 
#%%
    def get_position(self, ticker):
        if self.api == None: return None

        return self.api.GetPosition(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(ticker), c_wchar_p(self.bolsa))

#%%
    def ohlc_by_timeframe(self, timeframe):
        pass
    
#%% CALLBACKS
@WINFUNCTYPE(None, c_int32, c_int32)
def state_callback(n_type, n_result):

    global b_ativo
    global b_market_connected
    global b_connected
    
    n_connection_state_type = n_type
    result = n_result
        
    if n_connection_state_type == 0: # notificacoes de login
        if result == 0:
            b_connected = True
            print("Login: conectado")
        else:
            b_connected = False
            print('Login: ' + str(result))
    elif n_connection_state_type == 1:
        if result == 5:
            # bBrokerConnected = True
            print("Broker: Conectado.")            
        elif result > 2:
            bBrokerConnected = False
            # print("Broker: Sem conexão com corretora.")
        else:
            bBrokerConnected = False
            print("Broker: Sem conexão com servidores (" + str(result) + ")")
            
    elif n_connection_state_type == 2:  # notificacoes de login no Market
        if result == 4:
            print("Market: Conectado" )
            b_market_connected = True
        else:
            # print("Market: " + str(result))
            b_market_connected = False
        
        # print(f'MarketConnected: {b_market_connected}')

    elif n_connection_state_type == 3: # notificacoes de login
        if result == 0:
            print("Ativação: OK")
            b_ativo = True
        else:
            # print("Ativação: " + str(result))
            b_ativo = False    
        
    if b_market_connected and b_ativo and b_connected:
        print("Serviços Conectados")


@WINFUNCTYPE(None, TAssetID, c_wchar_p, c_uint, c_double, c_double, c_int, c_int, c_int, c_int)
def new_history_callback(asset_id, date, trade_number, price, vol, qtd, buy_agent, sell_agent, trade_type):    
    print(asset_id.ticker + ' | Trade History | ' + date + ' (' + str(trade_number) + ') ' + str(price))
    return

@WINFUNCTYPE(None, TAssetID, c_int)
def progress_callback(asset_id, n_progress):
    print(asset_id.ticker + ' | Progress | ' + str(n_progress))
    return
    
@WINFUNCTYPE(None, TAssetID, c_int, c_int, c_int, c_int, c_int, c_double, c_double, c_double, c_long, c_wchar_p, c_wchar_p , c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p)
def history_callback(r_asset_id, n_corretora, n_qtd, n_trade_qtd, n_leaves_qtd, side, s_price, s_stop_price, s_avg_price, n_profit_id, tipo_ordem, conta, titular, cl_ord_id, status, date):
    print(f'Corretora: {n_corretora} | Conta: {conta} | Quantidade: {n_qtd} | Quantidade executada: {n_trade_qtd} | Side: {side} | Price: {s_price} | Avg Price: {s_avg_price} |Tipo de Ordem: {tipo_ordem} | Status: {status} | Date: {date}')
    return

@WINFUNCTYPE(None, TAssetID, c_int, c_int, c_int, c_int, c_int, c_double, c_double, c_double, c_long, c_wchar_p, c_wchar_p , c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p)
def order_change_callback(r_asset_id, n_corretora, n_qtd, n_trade_qtd, n_leaves_qtd, side, s_price, s_stop_price, s_avg_price, n_profit_id, tipo_ordem, conta, titular, cl_ord_id, status, date, text_message):
    print("todo - orderChangeCallBack Conta=" + str(conta))
    return

@WINFUNCTYPE(None, c_int, c_wchar_p, c_wchar_p, c_wchar_p)
def account_callback(n_corretora, corretora_nome_completo, account_id, nome_titular):
    print("Conta | " + account_id + ' - ' + nome_titular + ' | Corretora ' + str(n_corretora) + ' - ' + corretora_nome_completo)
    return

@WINFUNCTYPE(None, TAssetID, c_int, c_int, c_int, c_int, c_int, c_double, POINTER(c_int), POINTER(c_int))
def price_book_callback(asset_id, n_action, n_position, side, n_qtd, n_count, s_price, p_array_sell, p_array_buy):
    # if p_array_sell is not None:
    print(f'price: {s_price} |')
    sleep(2)
        # print("todo - priceBookCallBack")
    return

@WINFUNCTYPE(None, TAssetID, c_wchar_p, c_uint, c_double, c_double, c_int, c_int, c_int, c_int, c_wchar)
def new_trade_callback(asset_id, date, trade_number, price, vol, qtd, buy_agent, sell_agent, trade_type, b_is_edit):
    global ticker_flag

    if ticker_flag == 'OHLC':
        print(asset_id.ticker + ' | Trade | ' + str(date) + '(' + str(trade_number) + ') ' + str(price))
    return

@WINFUNCTYPE(None, TAssetID, c_double, c_int, c_int)
def new_tinybook_callback(asset_id, price, qtd, side):
    global ticker_flag
    
    if ticker_flag == 'OHLC':
        if side == 0 :
            print(asset_id.ticker + ' | TinyBook | Buy: ' + str(price) + ' ' + str(qtd))
        else :
            print(asset_id.ticker + ' | TinyBook | Sell: ' + str(price) + ' ' + str(qtd))
            
    return

@WINFUNCTYPE(None, TAssetID, c_wchar_p, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_int, c_int, c_int, c_int, c_int, c_int, c_int)
def new_daily_callback(asset_id, date, s_open, s_high, s_low, s_close, s_vol, s_ajuste, s_max_limit, s_min_limit, s_vol_buyer, s_vol_seller, n_qtd, n_negocios, n_contratos_open, n_qtd_buyer, n_qtd_seller, n_neg_buyer, n_neg_seller):
    print(asset_id.ticker + ' | DailySignal | ' + date + ' Open: ' + str(s_open) + ' High: ' + str(s_high) + ' Low: ' + str(s_low) + ' Close: ' + str(s_close))
    return

def descript_price_array(price_array):
    price_array_descripted = []
    n_qtd = price_array[0]
    n_tam = price_array[1]
    print(f"qtd: {n_qtd}, n_tam: {n_tam}")

    arr = cast(price_array, POINTER(c_char))
    frame = bytearray()
    for i in range(n_tam):
        c = arr[i]
        frame.append(c[0])
    
    start = 8
    for i in range(n_qtd):
        price = struct.unpack('d', frame[start:start + 8])[0]
        start += 8
        qtd = struct.unpack('i', frame[start:start+4])[0]
        start += 4
        agent = struct.unpack('i', frame[start:start+4])[0]
        start += 4
        offer_id = struct.unpack('q', frame[start:start+8])[0]
        start += 8
        date_length = struct.unpack('h', frame[start:start+2])[0]
        start += 2
        date = frame[start:start+date_length]
        start += date_length

        price_array_descripted.append([price, qtd, agent, offer_id, date])

    return price_array_descripted

@WINFUNCTYPE(None, TAssetID, c_int, c_int, c_int, c_int, c_int, c_longlong, c_double, c_int, c_int, c_int, c_int, c_int, c_wchar_p, POINTER(c_int), POINTER(c_int))
def offer_book_callback(asset_id, n_action, n_position, side, n_qtd, n_agent, n_offer_id, s_price, b_has_price, b_has_qtd, b_has_date, b_has_offer_id, b_has_agent, date, p_array_sell, p_array_buy):
    global price_array_buy
    global price_array_sell

    if bool(p_array_sell):
        price_array_sell = descript_price_array(p_array_sell)

    if bool(p_array_buy):
        price_array_buy = descript_price_array(p_array_buy)

    if side == 0:
        lst_book = price_array_buy
    else:
        lst_book = price_array_sell

    if lst_book and 0 <= n_position <= len(lst_book):
        """
        atAdd = 0
        atEdit = 1
        atDelete = 2
        atDeleteFrom = 3
        atFullBook = 4
        """
        if n_action == 0:
            group = [s_price, n_qtd, n_agent]
            idx = len(lst_book) - n_position
            lst_book.insert(idx, group)
        elif n_action == 1:
            group = lst_book[-n_position - 1]
            group[1] = group[1] + n_qtd
            group[2] = group[2] + n_agent
        elif n_action == 2:
            del lst_book[-n_position - 1]
        elif n_action == 3:
            del lst_book[-n_position - 1:]
    return

@WINFUNCTYPE(None, TAssetID, c_wchar_p, c_uint, c_double)
def change_cotation_callback(asset_id, date, trade_number, s_price):
    print(f'asset_id: {asset_id} | price: {s_price}')
    # print("todo - changeCotationCallback")
    return

@WINFUNCTYPE(None, TAssetID, c_wchar_p)
def asset_list_callback(asset_id, str_name):
    print ("assetListCallback: Ticker =" + str(asset_id.ticker) + " Name =" + str(str_name))
    return