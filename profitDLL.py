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

# @dataclass
class TAssetID(Structure):
    _fields_ = [("ticker", c_wchar_p),
                ("bolsa", c_wchar_p),
                ("feed", c_int)]

# @dataclass
class TGroupOffer(Structure):
    _fields_ = [("nPosition", c_int),
                ("nQtd", c_int),
                ("nOfferID", c_int),
                ("nAgent", c_int),
                ("sPrice", c_double),
                ("strDtOffer", c_int)]


# @dataclass
class TGroupPrice(Structure):
    _fields_ = [("nQtd", c_int),
                ("nCount", c_int),
                ("sPrice", c_double)]

# @dataclass
class TNewTradeCallback(Structure):
    _fields_ = [("assetId", TAssetID),
                ("date", c_wchar_p),
                ("tradeNumber", c_uint),
                ("price", c_double),
                ("vol", c_double),
                ("qtd", c_int),
                ("buyAgent", c_int),
                ("sellAgent", c_int),
                ("tradeType", c_int),
                ("bIsEdit", c_int)]



# @dataclass
class TNewDailyCallback(Structure):
    _fields_ = [("tAssetIDRec", TAssetID),
                ("date", c_wchar_p),
                ("sOpen", c_double),
                ("sHigh", c_double),
                ("sLow", c_double),
                ("sClose", c_double),
                ("sVol", c_double),
                ("sAjuste", c_double),
                ("sMaxLimit", c_double),
                ("sMinLimit", c_double),
                ("sVolBuyer", c_double),
                ("sVolSeller", c_double),
                ("nQtd", c_int),
                ("nNegocios", c_int),
                ("nContratosOpen", c_int),
                ("nQtdBuyer", c_int),
                ("nQtdSeller", c_int),
                ("nNegBuyer", c_int),
                ("nNegSeller", c_int)]



# @dataclass
class TNewHistoryCallback(Structure):
    _fields_ = [("assetId", TAssetID),
                ("date", c_wchar_p),
                ("tradeNumber", c_uint),
                ("price", c_double),
                ("vol", c_double),
                ("qtd", c_int),
                ("buyAgent", c_int),
                ("sellAgent", c_int),
                ("tradeType", c_int)]



# @dataclass
class TProgressCallBack(Structure):
    _fields_ = [("assetId", TAssetID),
                ("nProgress", c_int)]


# @dataclass
class TNewTinyBookCallBack(Structure):
    _fields_ = [("assetId", TAssetID),
                ("price", c_double),
                ("qtd", c_int),
                ("side", c_int)]



# @dataclass
class TPriceBookCallback(Structure):
    _fields_ = [("assetId", TAssetID),
                ("nAction", c_int),
                ("nPosition", c_int),
                ("side", c_int),
                ("nQtd", c_int),
                ("ncount", c_int),
                ("sprice", c_double),
                ("pArraySell", POINTER(c_int)),
                ("pArrayBuy", POINTER(c_int))]



# @dataclass
class TOfferBookCallback(Structure):
    _fields_ = [("assetId", TAssetID),
                ("nAction", c_int),
                ("nPosition", c_int),
                ("side", c_int),
                ("nQtd", c_int),
                ("nAgent", c_int),
                ("nOfferID", c_longlong),
                ("sPrice", c_double),
                ("bHasPrice", c_int),
                ("bHasQtd", c_int),
                ("bHasDate", c_int),
                ("bHasOfferId", c_int),
                ("bHasAgent", c_int),
                ("date", c_wchar_p),
                ("pArraySell", POINTER(c_int)),
                ("pArrayBuy", POINTER(c_int))]


#Variaveis de Controle 
bAtivo = False
bMarketConnected = False
bConnectado = False
bBrokerConnected = False
nCount = 0

#BEGIN DEF
@WINFUNCTYPE(None, c_int32, c_int32)
def stateCallback(nType, nResult):
    global bAtivo
    global bMarketConnected
    global bConnectado
    global bBrokerConnected
    
    nConnStateType = nType
    result = nResult
        
    if nConnStateType == 0: # notificacoes de login
        if result == 0:
            bConnectado = True
            print("Login: conectado")
        else :
            bConnectado = False
            print('Login: ' + str(result))
    elif nConnStateType == 1:
        if result == 5:
            bBrokerConnected = True
            print("Broker: Conectado.")            
        elif result > 2:
            bBrokerConnected = False
            print("Broker: Sem conexão com corretora.")            
        else:
            bBrokerConnected = False
            print("Broker: Sem conexão com servidores (" + str(result) + ")")
            
    elif nConnStateType == 2:  # notificacoes de login no Market
        if result == 4:
            print("Market: Conectado" )        
            bMarketConnected = True
        else:
            print("Market: " + str(result))
            bMarketConnected = False

    elif nConnStateType == 3: # notificacoes de login
        if result == 0:
            print("Ativação: OK")
            bAtivo = True
        else:
            print("Ativação: " + str(result))
            bAtivo = False    
        
    if bMarketConnected and bAtivo and bConnectado:
        print("Serviços Conectados")

    return

@WINFUNCTYPE(None, TAssetID, c_wchar_p, c_uint, c_double, c_double, c_int, c_int, c_int, c_int)
def newHistoryCallback(assetId, date, tradeNumber, price, vol, qtd, buyAgent, sellAgent, tradeType):    
    print(assetId.ticker + ' | Trade History | ' + date + ' (' + str(tradeNumber) + ') ' + str(price))
    return

@WINFUNCTYPE(None, TAssetID, c_int)
def progressCallBack(assetId, nProgress):
    print(assetId.ticker + ' | Progress | ' + str(nProgress))
    return


@WINFUNCTYPE(None, TAssetID,
             c_int, c_int, c_int, c_int, c_int,
             c_double, c_double, c_double,
             c_long, 
             c_wchar_p, c_wchar_p , c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p)
def historyCallBack(rAssetID,
                    nCorretora, nQtd, nTradedQtd, nLeavesQtd, Side,
                    sPrice, sStopPrice, sAvgPrice,
                    nProfitID,
                    tipoOrdem, conta, titular, clOrdID, status, date):
    
    print("history_call_back Corretora=" + str(tipoOrdem))
    return


                                                    
@WINFUNCTYPE(None, TAssetID,
             c_int, c_int, c_int, c_int, c_int,
             c_double, c_double, c_double,
             c_long, 
             c_wchar_p, c_wchar_p , c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p)
def orderChangeCallBack(rAssetID,
                        nCorretora, nQtd, nTradedQtd, nLeavesQtd, Side, sPrice, sStopPrice, sAvgPrice,
                        nProfitID, tipoOrdem, conta, titular, clOrdID, status, date, textMessage):
    print("todo - orderChangeCallBack Conta=" + str(conta))
    return


@WINFUNCTYPE(None, c_int, c_wchar_p, c_wchar_p, c_wchar_p)
def accountCallback(nCorretora, corretoraNomeCompleto, accountID, nomeTitular):
    print("Conta | " + accountID + ' - ' + nomeTitular + ' | Corretora ' + str(nCorretora) + ' - ' + corretoraNomeCompleto)
    return

@WINFUNCTYPE(None, TAssetID, c_int, c_int, c_int, c_int, c_int, c_double, POINTER(c_int), POINTER(c_int))
def priceBookCallback(assetId, nAction, nPosition, Side, nQtd, nCount, sPrice, pArraySell, pArrayBuy):
    if pArraySell is not None:
        print("todo - priceBookCallBack")
    return


@WINFUNCTYPE(None, TAssetID, c_wchar_p, c_uint, c_double, c_double, c_int, c_int, c_int, c_int, c_wchar)
def newTradeCallback(assetId, date, tradeNumber, price, vol, qtd, buyAgent, sellAgent, tradeType, bIsEdit):
    print(assetId.ticker + ' | Trade | ' + str(date) + '(' + str(tradeNumber) + ') ' + str(price))
    return


@WINFUNCTYPE(None, TAssetID, c_double, c_int, c_int)
def newTinyBookCallBack(assetId, price, qtd, side):
    if side == 0 :
        print(assetId.ticker + ' | TinyBook | Buy: ' + str(price) + ' ' + str(qtd))
    else :
        print(assetId.ticker + ' | TinyBook | Sell: ' + str(price) + ' ' + str(qtd))
        
    return


@WINFUNCTYPE(None, TAssetID, c_wchar_p, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double,
           c_double, c_int, c_int, c_int, c_int, c_int, c_int, c_int)
def newDailyCallback(assetID, date, sOpen, sHigh, sLow, sClose, sVol, sAjuste, sMaxLimit, sMinLimit, sVolBuyer,
                     sVolSeller, nQtd, nNegocios, nContratosOpen, nQtdBuyer, nQtdSeller, nNegBuyer, nNegSeller):
    print(assetID.ticker + ' | DailySignal | ' + date + ' Open: ' + str(sOpen) + ' High: ' + str(sHigh) + ' Low: ' + str(sLow) + ' Close: ' + str(sClose))
    return

price_array_sell = []
price_array_buy = []

def descript_price_array(price_array):
    global profit_dll

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

@WINFUNCTYPE(None, TAssetID, c_int, c_int, c_int, c_int, c_int, c_longlong, c_double, c_int, c_int, c_int, c_int, c_int,
           c_wchar_p, POINTER(c_int), POINTER(c_int))
def offerBookCallback(assetId, nAction, nPosition, Side, nQtd, nAgent, nOfferID, sPrice, bHasPrice,
                      bHasQtd, bHasDate, bHasOfferID, bHasAgent, date, pArraySell, pArrayBuy):
    global price_array_buy
    global price_array_sell

    if bool(pArraySell):
        price_array_sell = descript_price_array(pArraySell)

    if bool(pArrayBuy):
        price_array_buy = descript_price_array(pArrayBuy)

    if Side == 0:
        lst_book = price_array_buy
    else:
        lst_book = price_array_sell

    if lst_book and 0 <= nPosition <= len(lst_book):
        """
        atAdd = 0
        atEdit = 1
        atDelete = 2
        atDeleteFrom = 3
        atFullBook = 4
        """
        if nAction == 0:
            group = [sPrice, nQtd, nAgent]
            idx = len(lst_book)-nPosition
            lst_book.insert(idx, group)
        elif nAction == 1:
            group = lst_book[-nPosition - 1]
            group[1] = group[1] + nQtd
            group[2] = group[2] + nAgent
        elif nAction == 2:
            del lst_book[-nPosition - 1]
        elif nAction == 3:
            del lst_book[-nPosition - 1:]
    return


@WINFUNCTYPE(None, TAssetID, c_wchar_p, c_uint, c_double)
def changeCotationCallback(assetId, date, tradeNumber, sPrice):
    print("todo - changeCotationCallback")
    return

@WINFUNCTYPE(None, TAssetID, c_wchar_p)
def assetListCallback(assetId, strName):
    print ("assetListCallback Ticker=" + str(assetId.ticker) + " Name=" + str(strName))
    return
#END DEF

#EXEMPLOS
def SenSellOrder() :
    qtd = int(1)
    preco = float(100000)
    # precoStop = float(100000)
    nProfitID = profit_dll.SendSellOrder (c_wchar_p(33001), c_wchar_p( ),
                                          c_wchar_p(System13),c_wchar_p(TRPL4F),
                                          c_wchar_p(B),
                                          c_double(25.80), c_int(qtd));

    print(str(nProfitID))

    print(profit_dll.GetPosition(c_wchar_p(33001), c_wchar_p( ), c_wchar_p(TRPL4F), c_wchar_p(B)))

def wait_login():    
    global profit_dll
    global bMarketConnected
    global bAtivo

    bWaiting = True
    while bWaiting:        
        if bMarketConnected  :
            profit_dll.SetAssetListCallback(assetListCallback);
            print("DLL Conected")        
            
            bWaiting = False

def subscribeOffer():
    global profit_dll
    print("subscribe offer book")

    asset = input('Asset: ')
    bolsa = input('Bolsa: ')

    result = profit_dll.SubscribeOfferBook(c_wchar_p(asset), c_wchar_p(bolsa))
    print ("SubscribeOfferBook: " + str(result))

def subscribeTicker():
    global profit_dll

    asset = input('Asset: ')
    bolsa = input('Bolsa: ')            
    
    result = profit_dll.SubscribeTicker(c_wchar_p(asset), c_wchar_p(bolsa))
    print ("SubscribeTicker: " + str(result))

def unsubscribeTicker():
    global profit_dll

    asset = input('Asset: ')
    bolsa = input('Bolsa: ')            
    
    result = profit_dll.UnsubscribeTicker(c_wchar_p(asset), c_wchar_p(bolsa))
    print ("UnsubscribeTicker: " + str(result))    
        

def dllStart():    
    try:
        global profit_dll
        key = str(1127858027317301205)
        
        bRoteamento = True
        
        if bRoteamento :            
            result = profit_dll.DLLInitialize(c_wchar_p(key), stateCallback, historyCallBack, orderChangeCallBack, accountCallback, newTradeCallback, newDailyCallback, priceBookCallback, offerBookCallback, newHistoryCallback, progressCallBack, newTinyBookCallBack)
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

def dllEnd():   
    global profit_dll
    result = profit_dll.DLLFinalize()

    print('DLLFinalize: ' + str(result))
    
if __name__ == '__main__':
    dllStart()
    
    strInput = ""
    while strInput != "exit":
        strInput = input()
        if strInput == 'subscribe' :
            subscribeTicker()
        elif strInput == 'unsubscribe':
            unsubscribeTicker()
        elif strInput == 'offerbook':
            subscribeOffer()
        elif strInput == 'send':
            SenSellOrder()

    dllEnd()

