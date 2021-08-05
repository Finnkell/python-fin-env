from src.setups.setup_pre_processing_infos import SetupPreProcessingInfos

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn')


class Backtest(object):
    def __init__(self, setup: 'Setup()', dataframe: pd.DataFrame()) -> None:
        self.__setup = setup

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

        print(self.__backtest_log_report_infos)

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

        print(f'Total de operações: {total_op}')
        
        print(f'Total de Lucro Bruto: R$ {lucro_bruto}')
        print(f'Total de trades lucrativos: {qtd_profit}')

        print(f'Total de Perda Bruto: R$ {perda_bruta}')
        print(f'Total de trades prejudicial: {qtd_loss}')

        print(f'Lucro Liquido total: R$ {lucro_bruto + perda_bruta}')
        

    def export_backtest_log_report(self, results: dict) -> print:
        self.__backtest_log_report_infos.append(results)
        self.__log_list.append(results)

    def run_backtest(self) -> None:
        self.send_setup_stack_info()
        self.processing_backtest_info_from_setup()