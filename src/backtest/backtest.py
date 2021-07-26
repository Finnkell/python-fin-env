import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn')

class Backtest:
    def __init__(self, dataframe, flag='OHLC'):
        self.dataframe = dataframe
        self.resultado = None
        self.flag = flag

    def __del__(self):
        pass

    def verify_dataframe(self):
        if self.dataframe.loc['Signal'] == False:
            raise("Don\'t have the Signal Column in the dataframe")
        elif self.dataframe.loc['TP'] == False or self.dataframe.loc['SL'] == False:
            raise("Don\'t have the TP/SL Column in the dataframe")
        elif self.dataframe.loc['Signal_Type'] == False:
            raise("Don\'t have the Signal Type in the dataframe")

        return True
        
    def calculate_result(self):
        variacao = []
        data_entrada = []
        data_saida = []

        df = self.dataframe

        tam_df = len(df) 
        volume = 1.0
        rows_counter = df.index[0]
        pos_aberta = False

        while rows_counter < tam_df:
            if df.loc[rows_counter, 'Signal'] == True or pos_aberta == True:
                data_entrada.append(df.loc[rows_counter, 'Date'] + ' ' + df.loc[rows_counter, 'Time'])
                preco_entrada = df.loc[rows_counter, 'Close']
                pos_aberta = True

                if self.flag == 'TICK':
                    df, rows_counter, pos_aberta, data_saida, variacao, volume = self.__ohlc_signal(df, rows_counter, preco_entrada, pos_aberta, data_saida, variacao, volume)

                if self.flag == 'OHLC':
                    df, rows_counter, pos_aberta, data_saida, variacao, volume = self.__tick_signal(df, rows_counter, preco_entrada, pos_aberta, data_saida, variacao, volume)
            else:
                rows_counter = rows_counter + 1

        resultado = pd.DataFrame(data={'Entry': data_entrada, 'Out': data_saida, 'Variation': variacao})
        
        self.create_new_dataframe(resultado)

        print(f'Last 20 results: {resultado.tail(20)}')

    def create_new_dataframe(self, resultado):
        self.resultado = resultado

    def performance_stats(self):
        total_op = len(self.resultado)
        print(f'Total de Operações: {total_op}')

        self.resultado.loc[self.resultado['Variation'] > 0, 'Type'] = 'Profit'
        self.resultado.loc[self.resultado['Variation'] < 0, 'Type'] = 'Loss'
        self.resultado.loc[self.resultado['Variation'] == 0, 'Type'] = 'None'
        
        total = self.resultado.groupby('Type')['Variation'].sum()
        total_profit = total['Profit']
        total_loss = total['Loss']
        total_none = total['None']

        qnt = self.resultado.groupby('Type')['Variation'].size()
        qnt_profit = qnt['Profit']
        qnt_loss = qnt['Loss']
        qnt_none = qnt['None']

        print(f'Total de Lucro bruto: {round(total_profit, 2)}')
        print(f'Total de trades vencedores: {qnt_profit}')

        print(f'Total de perda bruto: {round(total_loss, 2)}')
        print(f'Total de trades perdedores: {qnt_loss}')

        percent_profit = 100*qnt_profit/total_op

        print(f'Percentual de Lucro: {round(percent_profit, 2)}%')

    def plot_backtest(self):
        pass

    def run_backtest(self, dataframe):
        pass

    def __tick_signal(self, df, rows_counter, preco_entrada, pos_aberta, data_saida, variacao, volume):
        if df.loc[rows_counter, 'Signal_Type'] == 'BUY' or pos_aberta == True:
            if df.loc[rows_counter, 'Open'] >= df.loc[rows_counter, 'Tp'] or df.loc[rows_counter, 'High'] >= df.loc[rows_counter, 'Tp'] or df.loc[rows_counter, 'Low'] >= df.loc[rows_counter, 'Tp'] or df.loc[rows_counter, 'Close'] >= df.loc[rows_counter, 'Tp']:
                data_saida.append(df.loc[rows_counter, 'Date'] + ' ' + df.loc[rows_counter, 'Time'])
                preco_saida = df.loc[rows_counter, 'Close']
                variacao.append(volume*(-preco_entrada + preco_saida))
                pos_aberta = False

            elif df.loc[rows_counter, 'Open'] <= df.loc[rows_counter, 'Sl'] or df.loc[rows_counter, 'High'] <= df.loc[rows_counter, 'Sl'] or df.loc[rows_counter, 'Low'] <= df.loc[rows_counter, 'Sl'] or df.loc[rows_counter, 'Close'] <= df.loc[rows_counter, 'Sl']:
                data_saida.append(df.loc[rows_counter, 'Date'] + ' ' + df.loc[rows_counter, 'Time'])
                preco_saida = df.loc[rows_counter, 'Close']
                variacao.append(volume*(-preco_entrada + preco_saida))
                pos_aberta = False

            rows_counter = rows_counter + 1

        elif df.loc[rows_counter, 'Signal_Type'] == 'SELL' or pos_aberta == True:
            if df.loc[rows_counter, 'Open'] >= df.loc[rows_counter, 'Tp'] or df.loc[rows_counter, 'High'] >= df.loc[rows_counter, 'Tp'] or df.loc[rows_counter, 'Low'] >= df.loc[rows_counter, 'Tp'] or df.loc[rows_counter, 'Close'] >= df.loc[rows_counter, 'Tp']:
                data_saida.append(df.loc[rows_counter, 'Date'] + ' ' + df.loc[rows_counter, 'Time'])
                preco_saida = df.loc[rows_counter, 'Close']
                variacao.append(volume*(preco_entrada - preco_saida))
                pos_aberta = False

            elif df.loc[rows_counter, 'Open'] <= df.loc[rows_counter, 'Sl'] or df.loc[rows_counter, 'High'] <= df.loc[rows_counter, 'Sl'] or df.loc[rows_counter, 'Low'] <= df.loc[rows_counter, 'Sl'] or df.loc[rows_counter, 'Close'] <= df.loc[rows_counter, 'Sl']:
                data_saida.append(df.loc[rows_counter, 'Date'] + ' ' + df.loc[rows_counter, 'Time'])
                preco_saida = df.loc[rows_counter, 'Close']
                variacao.append(volume*(preco_entrada - preco_saida))
                pos_aberta = False

            rows_counter = rows_counter + 1

        return rows_counter, pos_aberta, data_saida, variacao, volume
    
    def __ohlc_signal(self, df, rows_counter, preco_entrada, pos_aberta, data_saida, variacao, volume):
        if df.loc[rows_counter, 'Signal_Type'] == 'BUY' or pos_aberta == True:
            if df.loc[rows_counter, 'Last'] >= df.loc[rows_counter, 'Tp']:
                data_saida.append(df.loc[rows_counter, 'Date'] + ' ' + df.loc[rows_counter, 'Time'])
                preco_saida = df.loc[rows_counter, 'Last']
                variacao.append(volume*(-preco_entrada + preco_saida))
                pos_aberta = False

            elif df.loc[rows_counter, 'Last'] <= df.loc[rows_counter, 'Sl']:
                data_saida.append(df.loc[rows_counter, 'Date'] + ' ' + df.loc[rows_counter, 'Time'])
                preco_saida = df.loc[rows_counter, 'Last']
                variacao.append(volume*(-preco_entrada + preco_saida))                          
                pos_aberta = False
            
            rows_counter = rows_counter + 1

        elif df.loc[rows_counter, 'Signal_Type'] == 'SELL' or pos_aberta == True:
            if df.loc[rows_counter, 'Last'] <= df.loc[rows_counter, 'Tp']:
                data_saida.append(df.loc[rows_counter, 'Date'] + ' ' + df.loc[rows_counter, 'Time'])
                preco_saida = df.loc[rows_counter, 'Last']
                variacao.append(volume*(preco_entrada - preco_saida))
                pos_aberta = False

            elif df.loc[rows_counter, 'Last'] >= df.loc[rows_counter, 'Sl']:
                data_saida.append(df.loc[rows_counter, 'Date'] + ' ' + df.loc[rows_counter, 'Time'])
                preco_saida = df.loc[rows_counter, 'Last']
                variacao.append(volume*(preco_entrada - preco_saida))
                pos_aberta = False
                
            rows_counter = rows_counter + 1

        return rows_counter, pos_aberta, data_saida, variacao, volume