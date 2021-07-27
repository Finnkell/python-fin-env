import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn')

class Backtest:
    def __init__(self, dataframe, flag='OHLC'):
        self.dataframe = dataframe
        self.resultado = None
        self.flag = flag

        self.total_op = None
        self.total = None
        self.total_profit = None
        self.total_loss = None
        self.total_none = None
        self.qnt = None
        self.qnt_profit = None
        self.qnt_loss = None
        self.qnt_none = None
        self.percent_profit = None
        self.profit_ratio = None
        self.max_profit = None
        self.max_loss = None
        self.avrg_operation_type = None
        self.profit_avrg = None
        self.loss_avrg = None
        self.none_avrg = None
        self.recurrency = None

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
                preco_entrada = df.loc[rows_counter, 'Open']
                pos_aberta = True

                while rows_counter < tam_df:
                    if self.flag == 'OHLC':
                        rows_counter, pos_aberta, data_saida, variacao = self.__ohlc_signal(df, rows_counter, preco_entrada, pos_aberta, data_saida, variacao, volume)

                    elif self.flag == 'TICK':
                        rows_counter, pos_aberta, data_saida, variacao = self.__tick_signal(df, rows_counter, preco_entrada, pos_aberta, data_saida, variacao, volume)

                    if pos_aberta == False:
                        break

                    rows_counter = rows_counter + 1
            else:
                rows_counter = rows_counter + 1

        resultado = pd.DataFrame(data={'Entry': data_entrada, 'Out': data_saida, 'Variation': variacao})
        
        self.create_new_dataframe(resultado)
        # print(f'Last 20 results: {resultado.tail(20)}')

    def create_new_dataframe(self, resultado):
        self.resultado = resultado

    def performance_stats(self):
        print(f'\n--------------------------------------REPORT-----------------------------------------')

        self.total_op = len(self.resultado)
        print(f'Total de Operações: {self.total_op}')

        self.resultado.loc[self.resultado['Variation'] > 0, 'Type'] = 'Profit'
        self.resultado.loc[self.resultado['Variation'] < 0, 'Type'] = 'Loss'
        self.resultado.loc[self.resultado['Variation'] == 0, 'Type'] = 'None'
        
        self.total = self.resultado.groupby('Type')['Variation'].sum()
        self.total_profit = self.total['Profit']
        self.total_loss = self.total['Loss']
        self.total_none = self.total['None']

        self.qnt = self.resultado.groupby('Type')['Variation'].size()
        self.qnt_profit = self.qnt['Profit']
        self.qnt_loss = self.qnt['Loss']
        self.qnt_none = self.qnt['None']

        print(f'Total de Lucro bruto: {round(self.total_profit, 2)}')
        print(f'Quatidade de trades vencedores: {self.qnt_profit}')

        print(f'Total de perda bruto: {round(self.total_loss, 2)}')
        print(f'Quantidade de trades perdedores: {self.qnt_loss}')

        self.percent_profit = 100*self.qnt_profit/self.total_op

        print(f'Percentual de Lucro: {round(self.percent_profit, 2)}%')

        self.profit_ratio = self.total_profit/self.total_loss
        print(f'Fator de Lucro: {abs(round(self.profit_ratio, 2))}')

        self.max_profit = self.resultado['Variation'].max()
        self.max_loss = self.resultado['Variation'].min()

        print(f'Ganho máximo: {round(self.max_profit, 2)}')
        print(f'Perda máxima: {round(self.max_loss, 2)}')

        self.avrg_operation_type = self.resultado.groupby('Type')['Variation'].mean()
        self.profit_avrg = self.avrg_operation_type['Profit']
        self.loss_avrg = self.avrg_operation_type['Loss']
        self.none_avrg = self.avrg_operation_type['None']

        print(f'Média de ganhos: {round(self.profit_avrg, 2)}')
        print(f'Média de perdas: {round(self.loss_avrg, 2)}')
        print(f'Razão de ganhos/perdas: {abs(round(self.profit_avrg/self.loss_avrg, 2))}')

        self.recurrency = (self.qnt_profit*self.profit_avrg) + (self.qnt_loss*self.loss_avrg)

        print(f'Retorno: {round(self.recurrency, 2)}')


    def plot_backtest(self):
        fig = plt.figure(figsize=(15, 10))

        ax_pizza = fig.add_subplot(2, 2, 1)
        ax_bar = fig.add_subplot(2, 2, 2)
        ax_histogram = fig.add_subplot(2, 2, 3)
        ax_scatter = fig.add_subplot(2, 2, 4)

        ax_pizza.set_title('Percentual de Operações de Lucro, Prejuízo e Neutras (%)')
        ax_bar.set_title('Média de Saldos Positivos e Negativos (R$)')
        ax_histogram.set_title('Distribuição de Saldos (R$)')
        ax_scatter.set_title('Scatter de Saldos (R$)')

        sizes = [self.qnt_profit, self.qnt_loss, self.qnt_none]
        labels = ['Profit', 'Loss', 'None']
        ax_pizza.pie(sizes, labels=labels, autopct='%1.2F%%', colors=['#8db600', '#e52b50', '#8c92ac'], textprops={'fontsize': 16})

        sns.barplot(data=self.resultado, x='Type', y='Variation', order=labels, palette=['#8db600', '#e52b50', '#8c92ac'], ax=ax_bar)
        sns.distplot(self.resultado['Variation'], ax=ax_histogram)
        
        self.resultado['Data Entrada'] = pd.to_datetime(self.resultado['Entry'])
        self.resultado.plot(x='Entry', y='Variation', kind='scatter', ax=ax_scatter)

        plt.savefig('result1.pdf')

        self.resultado['Backtest'] = self.resultado['Variation'].cumsum()

        ax_saldo = self.resultado.plot(x='Entry', y='Backtest', figsize=(20, 10), label='Saldo')

        ax_saldo.axhline(self.resultado['Backtest'].max(), color='#6DC75E', linestyle='--', label='Máxima')
        ax_saldo.axhline(self.resultado['Backtest'].min(), color='#6DC75E', linestyle='--', label='Mínima')
        plt.legend()

        self.resultado['Backtest Max'] = self.resultado['Backtest'].cummax()

        self.resultado['Drawdowns'] = self.resultado['Backtest Max'] - self.resultado['Backtest']

        ax_line = self.resultado.plot(x='Entry', y='Backtest Max', label='Max Acumulado', color='orange', figsize=(20, 10))
        self.resultado.plot(x='Entry', y='Backtest', label='Saldo', color='blue', ax=ax_line)

        self.resultado.plot(x='Entry', y='Drawdowns', label='Drawdows', color='green', ax=ax_line, linewidth=.8)

        max_dd = self.resultado['Drawdowns'].max()
        print(f'Máximo Drawdown: R$ {round(max_dd, 2)}')

        retorno_perc = 100*self.recurrency/max_dd
        print(f'Retorno percentual: {round(retorno_perc, 2)}%')

        plt.savefig('result2.pdf')

        import subprocess

        subprocess.run('explorer result1.pdf')
        subprocess.run('explorer result2.pdf')

    def run_backtest(self, dataframe):
        pass

    def __ohlc_signal(self, df, rows_counter, preco_entrada, pos_aberta, data_saida, variacao, volume):
        if df.loc[rows_counter, 'Signal_Type'] == 'BUY' and pos_aberta == True:
            if df.loc[rows_counter, 'Open'] >= df.loc[rows_counter, 'TP'] or df.loc[rows_counter, 'High'] >= df.loc[rows_counter, 'TP'] or df.loc[rows_counter, 'Low'] >= df.loc[rows_counter, 'TP'] or df.loc[rows_counter, 'Close'] >= df.loc[rows_counter, 'TP']:
                data_saida.append(df.loc[rows_counter, 'Date'] + ' ' + df.loc[rows_counter, 'Time'])
                preco_saida = df.loc[rows_counter, 'Close']
                variacao.append(volume*(-preco_entrada + preco_saida))
                pos_aberta = False

            elif df.loc[rows_counter, 'Open'] <= df.loc[rows_counter, 'SL'] or df.loc[rows_counter, 'High'] <= df.loc[rows_counter, 'SL'] or df.loc[rows_counter, 'Low'] <= df.loc[rows_counter, 'SL'] or df.loc[rows_counter, 'Close'] <= df.loc[rows_counter, 'SL']:
                data_saida.append(df.loc[rows_counter, 'Date'] + ' ' + df.loc[rows_counter, 'Time'])
                preco_saida = df.loc[rows_counter, 'Close']
                variacao.append(volume*(-preco_entrada + preco_saida))
                pos_aberta = False

            rows_counter = rows_counter + 1

        elif df.loc[rows_counter, 'Signal_Type'] == 'SELL' and pos_aberta == True:
            if df.loc[rows_counter, 'Open'] >= df.loc[rows_counter, 'TP'] or df.loc[rows_counter, 'High'] >= df.loc[rows_counter, 'TP'] or df.loc[rows_counter, 'Low'] >= df.loc[rows_counter, 'TP'] or df.loc[rows_counter, 'Close'] >= df.loc[rows_counter, 'TP']:
                data_saida.append(df.loc[rows_counter, 'Date'] + ' ' + df.loc[rows_counter, 'Time'])
                preco_saida = df.loc[rows_counter, 'Close']
                variacao.append(volume*(preco_entrada - preco_saida))
                pos_aberta = False

            elif df.loc[rows_counter, 'Open'] <= df.loc[rows_counter, 'SL'] or df.loc[rows_counter, 'High'] <= df.loc[rows_counter, 'SL'] or df.loc[rows_counter, 'Low'] <= df.loc[rows_counter, 'SL'] or df.loc[rows_counter, 'Close'] <= df.loc[rows_counter, 'SL']:
                data_saida.append(df.loc[rows_counter, 'Date'] + ' ' + df.loc[rows_counter, 'Time'])
                preco_saida = df.loc[rows_counter, 'Close']
                variacao.append(volume*(preco_entrada - preco_saida))
                pos_aberta = False

            rows_counter = rows_counter + 1
        else:
            rows_counter = rows_counter + 1
            
        return rows_counter, pos_aberta, data_saida, variacao
    
    
    def __tick_signal(self, df, rows_counter, preco_entrada, pos_aberta, data_saida, variacao, volume):
        if df.loc[rows_counter, 'Signal_Type'] == 'BUY' or pos_aberta == True:
            if df.loc[rows_counter, 'Last'] >= df.loc[rows_counter, 'TP']:
                data_saida.append(df.loc[rows_counter, 'Date'] + ' ' + df.loc[rows_counter, 'Time'])
                preco_saida = df.loc[rows_counter, 'Last']
                variacao.append(volume*(-preco_entrada + preco_saida))
                pos_aberta = False

            elif df.loc[rows_counter, 'Last'] <= df.loc[rows_counter, 'SL']:
                data_saida.append(df.loc[rows_counter, 'Date'] + ' ' + df.loc[rows_counter, 'Time'])
                preco_saida = df.loc[rows_counter, 'Last']
                variacao.append(volume*(-preco_entrada + preco_saida))                          
                pos_aberta = False
            
            rows_counter = rows_counter + 1

        elif df.loc[rows_counter, 'Signal_Type'] == 'SELL' or pos_aberta == True:
            if df.loc[rows_counter, 'Last'] <= df.loc[rows_counter, 'TP']:
                data_saida.append(df.loc[rows_counter, 'Date'] + ' ' + df.loc[rows_counter, 'Time'])
                preco_saida = df.loc[rows_counter, 'Last']
                variacao.append(volume*(preco_entrada - preco_saida))
                pos_aberta = False

            elif df.loc[rows_counter, 'Last'] >= df.loc[rows_counter, 'SL']:
                data_saida.append(df.loc[rows_counter, 'Date'] + ' ' + df.loc[rows_counter, 'Time'])
                preco_saida = df.loc[rows_counter, 'Last']
                variacao.append(volume*(preco_entrada - preco_saida))
                pos_aberta = False
                
            rows_counter = rows_counter + 1

        return rows_counter, pos_aberta, data_saida, variacao
