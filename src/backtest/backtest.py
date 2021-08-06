from src.setups.setup_pre_processing_infos import SetupPreProcessingInfos

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn')


class Backtest(object):
    def __init__(self, setup: 'Setup()', dataframe: pd.DataFrame()) -> None:
        self.__setup = setup

        self.__saldo = 100000

        if self.__setup is not None:
            self.__setup_dataframe = self.__setup.create_strategy(dataframe=dataframe)
        else: 
            raise ValueError
            
        self.__log_list = []
        self.__backtest_log_report_infos = []

    def __del__(self):
        del self.__setup
        del self.__setup_dataframe

        del self.__log_list
        del self.__backtest_log_report_infos


    def is_stack_empty(self, stack: list) -> bool:
        if len(stack) == 0:
            return True
        
        return False

    def is_dataframe_empty(self, dataframe: pd.DataFrame()) -> bool:
        if len(dataframe) == 0:
            return True

        return False

    def setup_pre_processing_infos(self, stack_info: tuple) -> dict:
        setup_pre_processing_infos = SetupPreProcessingInfos(self.__setup)

        setup_params = setup_pre_processing_infos.verify_setup_params()

        results = {}
        positions_to_close = []

        if setup_pre_processing_infos.is_date_valid(stack_info[0]):
            results['start_date'] = stack_info[0]

            if setup_pre_processing_infos.have_positions():
                for order in setup_pre_processing_infos.get_orders():
                    if order['side'] == 'BUY':
                        if order['tp'] <= stack_info[1]:
                            positions_to_close.append(
                                {
                                    'price': order['price'],
                                    'volume': order['volume'],
                                    'start_time': order['date'],
                                    'side': order['side'],
                                    'ticket': order['ticket'],
                                    'comment': 'Close by take profit'
                                }
                            )
                        elif order['sl'] >= stack_info[1]:
                            positions_to_close.append(
                                {
                                    'price': order['price'],
                                    'volume': order['volume'],
                                    'start_time': order['date'],
                                    'side': order['side'],
                                    'ticket': order['ticket'],
                                    'comment': 'Close by stop loss'
                                }
                            )
                    elif order['side'] == 'SELL':
                        if order['tp'] >= stack_info[1]:
                            positions_to_close.append(
                                {
                                    'price': order['price'],
                                    'volume': order['volume'],
                                    'start_time': order['date'],
                                    'side': order['side'],
                                    'ticket': order['ticket'],
                                    'comment': 'Close by take profit'
                                }
                            )
                        elif order['sl'] <= stack_info[1]:
                            positions_to_close.append(
                                {
                                    'price': order['price'],
                                    'volume': order['volume'],
                                    'start_time': order['date'],
                                    'side': order['side'],
                                    'ticket': order['ticket'],
                                    'comment': 'Close by stop loss'
                                }
                            )

                results['positions_to_close'] = positions_to_close
                results['order_entry'] = False
                results['side'] = False
                results['take_profit'] = False
                results['stop_loss'] = False
                results['position_modify'] = False
                results['position_close'] = False
            else:
                if stack_info[3] == 'BUY':
                    results['order_entry'] = True
                    results['side'] = 'BUY'
                    results['take_profit'] = False
                    results['stop_loss'] = False
                    results['position_modify'] = False
                    results['position_close'] = False
                    results['positions_to_close'] = []
                elif stack_info[3] == 'SELL':
                    results['order_entry'] = True
                    results['side'] = 'SELL'
                    results['take_profit'] = False
                    results['stop_loss'] = False
                    results['position_modify'] = False
                    results['position_close'] = False
                    results['positions_to_close'] = []
                else:
                    results['order_entry'] = False
                    results['side'] = False
                    results['take_profit'] = False
                    results['stop_loss'] = False
                    results['position_modify'] = False
                    results['position_close'] = False
                    results['positions_to_close'] = []

        return results


    def send_setup_stack_info(self) ->  None:
        stack = []

        dataframe = self.__setup_dataframe
        tam = len(dataframe)
        volume = self.__setup.get_volume()
        
        while not self.is_dataframe_empty(dataframe):
            if self.is_stack_empty(stack=stack):
                stack = [dataframe.iloc[0][0] + ' ' + dataframe.iloc[0][1], dataframe.iloc[0][2], dataframe.iloc[0][3], dataframe.iloc[0][4], dataframe.iloc[0][5]]
                # stack = [dataframe.iloc[0][0], dataframe.iloc[0][1], dataframe.iloc[0][2], dataframe.iloc[0][3], dataframe.iloc[0][4]]

                signal = dataframe.iloc[0][-1]

                dataframe = dataframe.drop(labels=dataframe.index[0], axis=0, 
                inplace=False)

                time = stack[0]
                stack.remove(time)

            if len(dataframe) == 0:
                break

            if len(dataframe) == 1:
                signal = 'CLOSE_ALL'

            # print(f'{len(dataframe)} from {tam*4}')

            value = stack[0]
            stack.remove(value)

            stack_info = (time, value, volume, signal)

            results = self.setup_pre_processing_infos(stack_info)

            self.__setup.get_stack_info_from_pre_setup_processing(stack_info, results)

            infos = self.__setup.export_backtesting_info()

            self.export_backtest_log_report(results=infos)


    def processing_backtest_info_from_setup(self) -> None:
        self.__backtest_log_report_infos = pd.DataFrame.from_dict(self.__backtest_log_report_infos[-1]['position_closed'])

        self.__backtest_log_report_infos['saldo'] = self.__backtest_log_report_infos['result']

        for i in range(len(self.__backtest_log_report_infos['result'])):
            self.__saldo = self.__saldo + self.__backtest_log_report_infos['result'][i]
            self.__backtest_log_report_infos['saldo'][i] = self.__saldo

        total_op = len(self.__backtest_log_report_infos)

        profit = []
        loss = []

        for price in self.__backtest_log_report_infos['result']:
            if price > 0:
                profit.append(price)
            elif price < 0:
                loss.append(price)

        qtd_profit = len(profit)
        qtd_loss = len(loss)

        lucro_bruto = round(sum(profit), 2)
        perda_bruta = round(sum(loss), 2)

        perc_lucro = 100*qtd_profit/total_op
        perc_loss = 100*qtd_loss/total_op

        fator_lucro = abs(lucro_bruto/perda_bruta)

        max_profit = max(profit)
        max_loss = min(loss)

        media_lucro = sum(profit)/len(profit)
        media_perda = sum(loss)/len(loss)

        razao = abs(round(media_lucro/media_perda, 2))

        retorno = round((qtd_profit*media_lucro) + (qtd_loss*media_perda), 2)

        print(f'Total de operações: {total_op}')
        
        print(f'Total de Lucro Bruto: R$ {lucro_bruto}')
        print(f'Total de trades lucrativos: {qtd_profit}')

        print(f'Total de Perda Bruto: R$ {perda_bruta}')
        print(f'Total de trades prejudicial: {qtd_loss}')

        print(f'Lucro Liquido total: R$ {lucro_bruto + perda_bruta}')
        
        print(f'Percentual lucrativo: {round(perc_lucro, 2)}%')
        print(f'Percentual prejudicial: {round(perc_loss, 2)}%')

        print(f'Fator de Lucro: {fator_lucro}')

        print(f'Ganho Máximo: R$ {round(max_profit, 2)}')
        print(f'Perda Máxima: R$ {round(max_loss, 2)}')
        
        print(f'Média de ganhos: R$ {round(media_lucro, 2)}')
        print(f'Média de perdas: R$ {round(media_perda, 2)}')

        print(f'Razão ganho/perda: {razao}')
        
        print(f'Retorno: R$ {retorno}')

        '''
        >>> Gráficos auxiliares
        '''
        fig = plt.figure(figsize=(20, 10))

        pizza = fig.add_subplot(2, 2, 1)
        barra = fig.add_subplot(2, 2, 2)
        hist = fig.add_subplot(2, 2, 3)
        scatter = fig.add_subplot(2, 2, 4)

        pizza.set_title('Percentual de Ganhos e Prejuízos')
        barra.set_title('Média dos saldos positivos e negativos (R$)')
        hist.set_title('Distribuição dos saldos (R$)')
        scatter.set_title('Scatter dos saldos (R$)')

        sizes = [qtd_profit, qtd_loss]
        labels = ['Lucro', 'Perda']

        pizza.pie(sizes, labels=labels, autopct='%1.2f%%', colors=['#33FF74', '#FF9933'])
        
        sns.barplot(data=self.__backtest_log_report_infos, x='in', y='result', palette=['#33FF74', '#FF9933'], ax=barra)

        sns.distplot(a=self.__backtest_log_report_infos['result'], ax=hist)
        
        sns.scatterplot(data=self.__backtest_log_report_infos, x='start_date', y='result', ax=scatter)

        plt.show()


        self.__backtest_log_report_infos['saldo_max'] = self.__backtest_log_report_infos['saldo'].cummax()
        self.__backtest_log_report_infos['saldo_min'] = self.__backtest_log_report_infos['saldo'].cummin()

        self.__backtest_log_report_infos['saldo_ant'] = self.__backtest_log_report_infos['saldo_min'].shift(-1)

        self.__backtest_log_report_infos['drawdowns_calc'] = (self.__backtest_log_report_infos['saldo_max'] - self.__backtest_log_report_infos['saldo_ant'])/self.__backtest_log_report_infos['saldo_max']*100

        self.__backtest_log_report_infos['drawdowns'] = self.__backtest_log_report_infos['saldo'] - self.__backtest_log_report_infos['drawdowns_calc']*100

        sns.lineplot(data=self.__backtest_log_report_infos, x='start_date', y='drawdowns', label='Drawdowns')
        sns.lineplot(data=self.__backtest_log_report_infos, x='start_date', y='saldo', label='Saldo')

        print(self.__backtest_log_report_infos.tail(5))

        plt.legend()
        plt.show()


        

    def export_backtest_log_report(self, results: dict) -> print:
        self.__backtest_log_report_infos.append(results)
        self.__log_list.append(results)

    def run_backtest(self) -> None:
        self.send_setup_stack_info()
        self.processing_backtest_info_from_setup()