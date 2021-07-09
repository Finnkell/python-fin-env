# Imports para execução da DLL
import time
import gc
from ctypes import *
from ctypes.wintypes import UINT
import struct
from src.servers.utils.utils_profit import *
from time import sleep

from datetime import datetime

# Caminho para a DLL, python tem que ser 32bits
profit_dll = WinDLL('./ProfitDLL.dll')
profit_dll.argtypes = None

# Globals
b_ativo = False
b_market_connected = False
b_connected = False
b_broker_connected = False
n_count = 0

price_array_sell = []
price_array_buy = []

ticker_flag = None

c_open = 0
c_high = 0
c_low = 0
c_close = 0

last_price = 0.0

agent_index = {
    '3': 'XP',
    '4': 'Alfa',
    '8': 'UBS',
    '13': 'Merrill',
    '15': 'Guide',
    '16': 'JP Morgan',
    '21': 'Votorantim',
    '23': 'Necton',
    '27': 'Santander',
    '39': 'Agora',
    '40': 'Morgan',
    '45': 'Credit',
    '58': 'Socopa',
    '59': 'Safra',
    '63': 'Novinvest',
    '72': 'Bradesco',
    '77': 'Citigroup',
    '85': 'BTG',
    '88': 'Capital',
    '90': 'Easynvest',
    '92': 'Renascenca',
    '93': 'Nova Futura',
    '106': 'Merc.',
    '107': 'Terra',
    '114': 'Itau',
    '115': 'H.commcor',
    '120': 'Genial',
    '122': 'BGC Liquidez',
    '127': 'Tullett',
    '129': 'Planner',
    '131': 'Fator',
    '147': 'Ativa',
    '172': 'Banrisul',
    '174': 'Elite',
    '177': 'Solidus',
    '186': 'Geral',
    '187': 'Sita',
    '190': 'Warren',
    '191': 'Senso',
    '226': 'Amaril',
    '234': 'Codepe',
    '238': 'Goldman',
    '254': 'BB',
    '262': 'Mirae',
    '308': 'Clear',
    '386': 'Rico',
    '735': 'ICAP',
    '1089': 'RB Capital',
    '1099': 'Inter',
    '1130': 'Intl',
    '1618': 'Ideal',
    '1855': 'Vitreo',
    '1982': 'Modal',
    '2659': 'BB',
    '3701': 'Orama',
    '4090': 'Toro',
    '6003': 'C6',
}

class ProfitConnection:
    # %%
    def __init__(self, key, password=1234):
        global profit_dll

        self.key = str(key)
        self.api = profit_dll
        self.result = None

        try:
            b_roteamento = True

            if b_roteamento:
                try:
                    self.result = self.api.DLLInitialize(c_wchar_p(self.key),
                                                         state_callback,
                                                         history_callback,
                                                         order_change_callback,
                                                         account_callback,
                                                         new_trade_callback,
                                                         new_daily_callback,
                                                         price_book_callback,
                                                         offer_book_callback,
                                                         history_trade_callback,
                                                         progress_callback,
                                                         tinybook_callback,
                                                         change_cotation_callback,
                                                         theoretical_price_callback
                                                         )
                except Exception as e:
                    print(f'ERROR: {e}')

            else:
                try:
                    self.result = self.api.InitializeMarket(c_wchar_p(self.key),
                                                            state_callback,
                                                            new_trade_callback,
                                                            new_daily_callback,
                                                            price_book_callback,
                                                            offer_book_callback,
                                                            history_trade_callback,
                                                            progress_callback,
                                                            tinybook_callback)
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

        self.candle = []
        self.order_history = {}
        self.last_price = 0.0

        self.agent_buy_id = 0
        self.agent_sell_id = 0
# %%
    def __del__(self):
        sleep(5)
        result = self.api.DLLFinalize()
        del self.api

        print('DLLFinalize: ' + str(result))
# %%

    def wait_login(self):
        bWaiting = True
        global b_market_connected

        while bWaiting:
            if b_market_connected:
                self.api.SetAssetListCallback(asset_list_callback)
                print("DLL Conected")

                bWaiting = False

# %%
    def get_account(self):
        return f'Account: {self.api.GetAccount()}'

# %%
    def buy_limit_order(self, volume=1, ticker='WINQ21', bolsa='F', price=0, sl=0, tp=0):
        '''TODO: Create Stop and Take'''
        if self.api == None: return None

        price = float(price)
        volume = int(volume)

        result = self.api.SendBuyOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticker), c_wchar_p(bolsa), c_double(price), c_int(volume))

        self.order_history[result] = {
            'order_type': 'BUY',
            'price': (price, result)
        }

        return result

# %%
    def sell_limit_order(self, volume=1, ticker='WINQ21', bolsa='F', price=0, sl=0, tp=0):
        if self.api == None: return None

        price = float(price)
        volume = int(volume)

        result = self.api.SendSellOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticker), c_wchar_p(self.bolsa), c_double(price), c_int(volume))

        self.order_history[result] = {
            'order_type': 'SELL',
            'price': (price, result)
        }

        return result

    def buy_market_order(self, volume=1, ticker='WINQ21', bolsa='F', price=0, sl=0, tp=0):
        if self.api == None: return None, None, None

        # if sl < price or tp > price:
        #     return None, None, None

        volume = int(volume)

        price = float(price)
        sl = float(sl)
        tp = float(tp)

        print(f'\nPrice = {price} | Sl = {sl} | Tp = {tp}\n')

        result_tp = self.api.SendSellOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticker), c_wchar_p(bolsa), c_double(tp), c_int(volume))
        result_sl = self.api.SendStopSellOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticker), c_wchar_p(bolsa), c_double(float(sl - 100.0)), c_double(float(sl)),c_int(volume))
        result = self.api.SendBuyOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticker), c_wchar_p(bolsa), c_double(price), c_int(volume))

        print(f'market = {str(result)} | tp = {str(result_tp)} | sl = {str(result_sl)}')

        self.order_history[result] = {
            'order_type': 'BUY',
            'price': (price, result),
            'tp': (tp, result_tp),
            'sl': (sl, result_sl)
        }

        return result, result_sl, result_tp

    def sell_market_order(self, volume=1, ticker='WINQ21', bolsa='F', price=0, sl=0, tp=0):
        if self.api == None: return None

        if sl > price or tp < price:
            return None

        volume = int(volume)

        price = float(price)
        sl = float(sl)
        tp = float(tp)

        print(f'\nPrice = {price} | Sl = {sl} | Tp = {tp}\n')

        result_tp = self.api.SendBuyOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticker), c_wchar_p(bolsa), c_double(tp), c_int(volume))
        result_sl = self.api.SendStopBuyOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticker), c_wchar_p(bolsa), c_double(float(sl + 100.0)), c_double(sl), c_int(volume))
        result = self.api.SendSellOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticker), c_wchar_p(bolsa), c_double(price), c_int(volume))

        print(f'SendSellMarketOrder = {str(result)} | sl = {str(result_sl)} | tp = {str(result_tp)}')

        self.order_history[result] = {
            'order_type': 'SELL',
            'price': (price, result),
            'tp': (tp, result_tp),
            'sl': (sl, result_sl)
        }

        return result, result_sl, result_tp

# %%
    def buy_stop_order(self, volume=1, ticker='WINQ21', bolsa='F', price=0, stop_price=0, sl=0, tp=0):
        if self.api == None: return None

        price = float(price)
        s_price = float(stop_price)
        volume = int(volume)

        result = self.api.SendStopBuyOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticker), c_wchar_p(bolsa), c_double(price), c_double(s_price), c_int(volume))

        self.order_history[result] = {
            'order_type': 'BUY',
            'price': (price, result)
        }

        return result

# %%
    def sell_stop_order(self, volume=1, ticket='WINQ21', bolsa='F', price=0):
        if self.api == None: return None
        
        price = float(price)
        s_price = float(stop_price)
        volume = int(volume)

        result = self.api.SendStopSellOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticker), c_wchar_p(self.bolsa), c_double(price), c_double(s_price), c_int(volume))

        # print(f'SendSellStopOrder = {str(result)}')

        self.order_history[result] = {
            'order_type': 'SELL',
            'price': (price, result)
        }

        return result


# %%
    def send_cancel_order(self, order_id):
        if self.api == None: return None

        result = self.api.SendCancelOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(str(order_id)), c_wchar_p(self.password))

        # print(f'Cancel Order = {str(result)}')

        return result

# %%
    def send_cancel_orders(self, ticker, bolsa):
        if self.api == None: return None

        result = self.api.SendCancelOrders(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(ticker), c_wchar_p(bolsa))

        # print(f'Cancel Orders: {result}')

        return result

# %%
    def subscribe_ticker(self, ticker, bolsa, flag='OHLC'):
        if self.api == None: return None

        global ticker_flag

        ticker_flag = flag

        self.asset = ticker
        self.bolsa = bolsa

        result = self.api.SubscribeTicker(c_wchar_p(ticker), c_wchar_p(bolsa))
        
        # print("Ticker Subscribed: " + str(result))

        return result

# %%
    def unsubscribe_ticker(self):
        if self.api == None: return None

        result = self.api.UnsubscribeTicker(c_wchar_p(self.asset), c_wchar_p(self.bolsa))
        
        # print("Ticker Unsubscribed: " + str(result))

        return result

# %%
    def subscribe_offer_book(self, ticker, bolsa):
        if self.api == None: return None

        self.asset = ticker
        self.bolsa = bolsa

        result = self.api.SubscribeOfferBook(c_wchar_p(ticker), c_wchar_p(bolsa))

        # print("Book Offer Subscribed: " + str(result))

        return result

# %%
    def unsubscribe_offer_book(self):
        if self.api == None: return None

        result = self.api.UnsubscribeOfferBook(c_wchar_p(self.asset), c_wchar_p(self.bolsa))

        print("Book Offer Unsubscribed: " + str(result))

        return result

# %%
    def subscribe_price_book(self, ticker, bolsa, flag='TRADE'):
        if self.api == None: return None

        global ticker_flag

        self.asset = ticker
        self.bolsa = bolsa

        ticker_flag = flag

        result = self.api.SubscribePriceBook(c_wchar_p(ticker), c_wchar_p(bolsa))

        # print(f'Price Book Subscribe: {str(result)}')

        return result

# %%
    def unsubscribe_price_book(self):
        if self.api == None: return None

        result = self.api.UnsubscribedPriceBook()

        # print(f'Price Book Unsubscribed: {str(result)}')

        return result

#%%
    def subscribe_adjust_history(self, ticker, bolsa):
        if self.api == None: return None

        global ticker_flag

        self.asset = ticker
        self.bolsa = bolsa

        result = self.api.SubscribeAdjustHistory(c_wchar_p(ticker), c_wchar_p(bolsa))

        # print(f'Adjust History Subscribe: {str(result)}')

        return result

#%%
    def unsubscribe_adjust_history(self):
        if self.api == None: return None

        result = self.api.UnsubscribeAdjustHistory(c_wchar_p(self.asset), c_wchar_p(self.bolsa))

        # print(f'Adjust History UnSubscribe: {str(result)}')

        return result

# %%
    def get_ticker_info(self, ticker, bolsa):
        if self.api == None: return None

        self.asset = ticker
        self.bolsa = bolsa

        result = self.api.RequestTickerInfo(c_wchar_p(ticker), c_wchar_p(bolsa))

        print(f'Ticker Info Request: {str(result)}')

        return result


# %%
    def order_change(self, order_id, price, volume):
        if self.api == None: return None

        order_id = str(order_id)
        price = float(price)
        volume = int(volume)

        result = self.api.SendChangeOrder(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(self.password), c_wchar_p(order_id), c_float(price), c_int(volume) )

        # print(f'Change Order: {str(result)}')

        return result

# %%
    def send_zero_position(self, ticker, bolsa, price):
        if self.api == None: return None

        print(f'ticker: {ticker} | bolsa: {bolsa} | price: {price}')

        result = self.api.SendZeroPosition(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(ticker), c_wchar_p(bolsa), c_wchar_p(self.password), c_double(price))

        # print(f'Zero Position: {str(result)}')

        return result

# %%
    def get_order_profit_id(self, profit_id):
        if self.api == None: return None

        # profit_id = int(profit_id)

        result = self.api.GetOrderProfitID(c_int64(profit_id))

        # print(f'Order Profit ID: {str(result)}')

        return result

# %%
    def get_order(self, order_id):
        if self.api == None: return None

        return self.api.GetOrder(c_wchar_p(order_id))

# %%
    def get_orders_total(self, datetime_start, datetime_end):
        if self.api == None: return None

        result = self.api.GetOrders(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(datetime_start), c_wchar_p(datetime_end))

        return result

# %%
    def get_position(self, ticker, bolsa):
        if self.api == None: return None

        result = self.api.GetPosition(c_wchar_p(self.conta), c_wchar_p(self.broker), c_wchar_p(ticker), c_wchar_p(bolsa))

        return result

# %%
    def get_history_trades(self, ticker, bolsa, datetime_start, datetime_end):
        if self.api == None: return None

        result = self.api.GetHistoryTrades(c_wchar_p(ticker), c_wchar_p(bolsa), c_wchar_p(datetime_start), c_wchar_p(datetime_end))

        print(f'History Trade: {result}')

#%%
    def get_serie_history(self, ticker, bolsa, datetime_start, datetime_end, qnt_number_start, qnt_number_end):
        if self.api == None: return None

        qnt_number_start = int(qnt_number_start)
        qnt_number_end = int(qnt_number_end)

        result = self.api.GetSerieHistory(c_wchar_p(ticker), c_wchar_p(bolsa), c_wchar_p(datetime_start), c_wchar_p(datetime_end), c_uint(qnt_number_start), c_uint(qnt_number_end))

        return result

# %%
    def get_open_price(self):
        if self.candle == []: return -1

        last = self.candle.pop()

        if last == []: return -1

        return last[-4]

    def get_high_price(self):

        if self.candle == []: return -1

        last = self.candle.pop()

        if last == []: return -1

        return last[-3]

    def get_low_price(self):
        if self.candle == []: return -1

        last = self.candle.pop()

        if last == []: return -1

        return last[-2]

    def get_close_price(self):
        if self.candle == []: return -1

        last = self.candle.pop()

        if last == []: return -1

        return last[-1]

# %%
    def get_last_price(self):
        return self.last_price

# %%
    def set_candle(self):
        global c_open
        global c_high
        global c_low
        global c_close

        c_list = []

        c_list.append(c_open)
        c_list.append(c_high)
        c_list.append(c_low)
        c_list.append(c_close)

        self.candle.append(c_list)

# %%
    def set_last_price(self):
        global last_price
        self.last_price = last_price


# %%
    def set_theoretical_price(self):
        result = self.api.SetTheoreticalPriceCallback(theoretical_price_callback)
        
        return result
# %%

    def ohlc_by_timeframe(self, timeframe):
        '''TODO: Create an OHLC return by timeframe'''
        pass

# %%
    def get_history():
        if self.api == None: return None

        return self.api.SetAdjustHistoryCallback()

# %%
    def change_cotation(self):
        if self.api == None: return None

        result = self.api.SetChangeCotationCallback(change_cotation_callback)

        # print(f'Change Cotation: {str(result)}')

        return result

#%%
    def get_last_history_order(self, order_id):
        if not self.order_history[order_id]:
            return None

        return self.order_history[order_id]
        
# %% CALLBACKS
@WINFUNCTYPE(None, c_int32, c_int32)
def state_callback(n_type, n_result):

    global b_ativo
    global b_market_connected
    global b_connected

    n_connection_state_type = n_type
    result = n_result

    if n_connection_state_type == 0:  # notificacoes de login
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
            print("Market: Conectado")
            b_market_connected = True
        else:
            # print("Market: " + str(result))
            b_market_connected = False

        # print(f'MarketConnected: {b_market_connected}')

    elif n_connection_state_type == 3:  # notificacoes de login
        if result == 0:
            print("Ativação: OK")
            b_ativo = True
        else:
            # print("Ativação: " + str(result))
            b_ativo = False

    if b_market_connected and b_ativo and b_connected:
        print("Serviços Conectados")


@WINFUNCTYPE(None, TAssetID, c_wchar_p, c_uint, c_double, c_double, c_int, c_int, c_int, c_int)
def history_trade_callback(asset_id, date, trade_number, price, vol, qtd, buy_agent, sell_agent, trade_type):
    print(f'| History Trade | -> | {asset_id.ticker} | Date: {date} | Trade Number: {trade_number} | Price: {price}')
    return


@WINFUNCTYPE(None, TAssetID, c_int)
def progress_callback(asset_id, n_progress):
    print(asset_id.ticker + ' | Progress | ' + str(n_progress))
    return


@WINFUNCTYPE(None, TAssetID, c_int, c_int, c_int, c_int, c_int, c_double, c_double, c_double, c_long, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p)
def history_callback(r_asset_id, n_corretora, n_qtd, n_trade_qtd, n_leaves_qtd, side, s_price, s_stop_price, s_avg_price, n_profit_id, tipo_ordem, conta, titular, cl_ord_id, status, date):
    print(f'| History Callback | -> | Corretora: {n_corretora} | Conta: {conta} | Quantidade: {n_qtd} | Quantidade executada: {n_trade_qtd} | Side: {side} | Price: {s_price} | Avg Price: {s_avg_price} |Tipo de Ordem: {tipo_ordem} | Order ID: {cl_ord_id} Status: {status} | Date: {date}\n')
    return


# @WINFUNCTYPE(None, TAssetID, c_wchar_p, c_uint, c_double, c_double, c_int, c_int, c_int, c_int)
# def history_trade_callback(asset_id, data, trade_number, price, volume, n_qtd, n_buy_agent, n_sell_agent, n_trade_type):
#     print(f'Date: {date} | Trade number: {trade_number} | Price: {price} | Volume: {volume} | Quantidade: {n_qtd} | Buy Agent: {n_buy_agent} | Sell Agent: {n_sell_agent} | Trade Type: {n_trade_type}')
#     return

@WINFUNCTYPE(None, TAssetID, c_int, c_int, c_int, c_int, c_int, c_double, c_double, c_double, c_long, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p)
def order_change_callback(r_asset_id, n_corretora, n_qtd, n_trade_qtd, n_leaves_qtd, side, s_price, s_stop_price, s_avg_price, n_profit_id, tipo_ordem, conta, titular, cl_ord_id, status, date, text_message):
    print(f'| Order Change | -> | Conta: {str(conta)} | Price Average: {float(s_avg_price)} | Order ID: {str(cl_ord_id)} | Status: {str(date)} | Message: {str(text_message)}')
    return


@WINFUNCTYPE(None, c_int, c_wchar_p, c_wchar_p, c_wchar_p)
def account_callback(n_corretora, corretora_nome_completo, account_id, nome_titular):
    print(f'| Accout | -> | Conta: ( {account_id}, {nome_titular} ) | Corretora: ({str(n_corretora)}, {corretora_nome_completo})')
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

    global mt_ticker
    global mt_date
    global mt_trade_number
    global mt_price
    global mt_trade_type
    global mt_volume
    global mt_qtd
    global mt_agent_buy
    global mt_agent_sell  

    if ticker_flag != 'OHLC' and ticker_flag == 'TICK': 
        print(f'| New Trade Callback | -> | Ticker: {asset_id.ticker} | Trade : ( {date}, {trade_number}, {price} ) | Trade Type: {trade_type} | Volume: {vol} | Qtd: {qtd} | Buy agent: {agent_index[str(buy_agent)]} | Sell agent: {agent_index[str(sell_agent)]} |')

        mt_ticker = asset_id.ticker
        mt_date = date
        mt_trade_number = tradeNumber
        mt_price = price
        mt_trade_type = trade_type
        mt_volume = vol
        mt_qtd = qtd
        mt_agent_buy = agent_index[str(buy_agent)]
        mt_agent_sell = agent_index[str(sell_agent)]

    return

@WINFUNCTYPE(None, TAssetID, c_double, c_int, c_int)
def tinybook_callback(asset_id, price, qtd, side):
    global ticker_flag

    if ticker_flag != 'OHLC' and ticker_flag == 'BOOK':
        if side == 0:
            print(f'| TinyBook | -> | {asset_id.ticker} | Buy: {str(price)} - {str(qtd)}')
        else:
            print(f'| TinyBook | -> | {asset_id.ticker} | Sell: {str(price)} - {str(qtd)}')
    return


@WINFUNCTYPE(None, TAssetID, c_wchar_p, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_int, c_int, c_int, c_int, c_int, c_int, c_int)
def new_daily_callback(asset_id, date, s_open, s_high, s_low, s_close, s_vol, s_ajuste, s_max_limit, s_min_limit, s_vol_buyer, s_vol_seller, n_qtd, n_negocios, n_contratos_open, n_qtd_buyer, n_qtd_seller, n_neg_buyer, n_neg_seller):
    print(f'| New Daily | -> | Horario: {str(datetime.now())} | {asset_id.ticker} | DailySignal | {date} | Open: {str(s_open)} | High: {str(s_high)} | Low: {str(s_low)} | Close: {str(s_close)}')

    global c_open
    global c_high
    global c_low
    global c_close

    c_open = s_open
    c_high = s_high
    c_low = s_low
    c_close = s_close

    return


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
    # print(f'asset_id: ({asset_id.ticker}, {asset_id.bolsa}, {asset_id.feed}) | Trade number: {trade_number} | Price: {s_price}')

    global last_price
    last_price = s_price

    return

@WINFUNCTYPE(None, TAssetID, c_wchar_p)
def asset_list_callback(asset_id, str_name):
    print(f' | AssetList | -> | Ticker: {str(asset_id.ticker)} | Name: {str(str_name)}')
    return

@WINFUNCTYPE(None, TAssetID, c_double, c_int64)
def theoretical_price_callback(asset_id, theoretical_price, theoretical_qtd):
    print(f' | Theorical Price | -> asset: {asset_id.ticker} | theoretical price: {theoretical_price} | theoretical qtd: {theoretical_qtd}')
    return

# %% UTILS
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


# %% EXPORTS

mt_ticker = None
mt_date = None
mt_trade_number = None
mt_price = None
mt_trade_type = None
mt_volume = None
mt_qtd = None
mt_agent_buy = None
mt_agent_sell = None


def export_tick_by_tick():
    global mt_ticker
    global mt_date
    global mt_trade_number
    global mt_price
    global mt_trade_type
    global mt_volume
    global mt_qtd
    global mt_agent_buy
    global mt_agent_sell  

    return mt_ticker, mt_date, mt_trade_number, mt_price, mt_qtd, mt_volume, mt_agent_buy, mt_agent_sell, mt_trade_type

