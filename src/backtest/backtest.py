from src.setups.setup_pre_processing_infos import SetupPreProcessingInfos

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn')


class Backtest(object):
    def __init__(self, setup: 'Setup()', dataframe: pd.DataFrame()) -> None:
        self.__setup = setup
        self.__setup_dataframe = dataframe

        self.__log_list = []

    def __del__(self):
        del self.__setup
        del self.__setup_dataframe

        del self.__log_list


    def is_stack_empty(self, stack: list) -> bool:
        if len(stack) == 0:
            return True
        
        return False

    def is_dataframe_empty(self, dataframe: pd.DataFrame()) -> bool:
        if len(dataframe) == 0:
            return True

        return False

    def setup_pre_processing_infos(self, stack_info: tuple, row: list) -> dict:
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
                if stack_info[2] == 'BUY':
                    results['order_entry'] = True
                    results['side'] = 'BUY'
                    results['take_profit'] = False
                    results['stop_loss'] = False
                    results['position_modify'] = False
                    results['position_close'] = False
                    results['positions_to_close'] = []
                elif stack_info[2] == 'SELL':
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
        
        while not self.is_dataframe_empty( dataframe ):
            if self.is_stack_empty(stack=stack):
                stack = [dataframe.iloc[0][0] + ' ' + dataframe.iloc[0][1], dataframe.iloc[0][2], dataframe.iloc[0][3], dataframe.iloc[0][4], dataframe.iloc[0][5]]

                signal = [i for i in dataframe.iloc[0][-1]]

                dataframe = dataframe.drop(labels=dataframe.index[0], axis=0, 
                inplace=False)

                time = stack[0]
                stack.remove(time)

            if len(dataframe) == 0:
                    break

            value = stack[0]
            stack.remove(value)

            stack_info = (time, value, signal)

            results = self.setup_pre_processing_infos(stack_info, dataframe.iloc[0])

            self.__setup.get_stack_info_from_pre_setup_processing(stack_info, results)


            infos = self.__setup.export_backtesting_info()

            self.processing_backtest_info_from_setup(results=infos)
            self.export_backtest_log_report(infos)


    def processing_backtest_info_from_setup(self, results: dict) -> None:
        return

    def export_backtest_log_report(self, results: dict) -> print:
        self.__log_list.append(results)

    def run_backtest(self, dataframe: pd.DataFrame()) -> None:
        self.__setup_dataframe = dataframe
        self.send_setup_stack_info()