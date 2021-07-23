import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn')

class Backtest(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    def calculate_result(self):
        variacao = []
        data_entrada = []
        data_saida = []

        tam_df = len(df) 
        quantidade_ativos = 1
        dia = df.index[0]
        pos_aberta = False

        while dia < tam_df:
            if df.loc[dia, 'MMS8xMMS20'] == True:
                data_entrada.append(df.loc[dia, 'Date'] + ' ' + df.loc[dia, 'Time'])
                preco_entrada = df.loc[dia, 'Close']
                pos_aberta = True

                while dia < tam_df:
                    if df.loc[dia, 'MMS20xMMS8'] == True:
                        data_saida.append(df.loc[dia, 'Date'] + ' ' + df.loc[dia, 'Time'])
                        preco_saida = df.loc[dia, 'Close']
                        variacao.append(quantidade_ativos*(-preco_entrada + preco_saida))
                        pos_aberta = False
                        break
                    dia = dia + 1
            else:
                dia = dia + 1


        if pos_aberta:
            data_entrada = data_entrada[:-1]

        resultado = pd.DataFrame(data={'Entry': data_entrada, 'Out': data_saida, 'Variation': variacao})

        resultado.tail(20)

    def create_new_dataframe(self):
        pass

    def performance_stats(self):
        pass

    def plot_backtest(self):
        pass

    def run_backtest(self, dataframe):
        pass