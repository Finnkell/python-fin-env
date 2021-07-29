import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn')


class Backtest(object):
    def __init__(self, setup: 'Setup', dataframe: pd.DataFrame) -> None:
        self.setup = setup
        self.setup_dataframe = dataframe


    def __del__(self):
        pass


    def is_stack_empty(self, stack: list) -> bool:
        if len(stack) == 0:
            return True
          
        return False

    def is_dataframe_empty(self, dataframe: pd.DataFrame) -> bool:
        if len(dataframe) == 0:
            return True

        return False

    def setup_pre_processing_infos(self, stack_info: tuple) -> dict:
        setup_pre_processing = SetupPreProcessingInfos(self.__setup)

        results = {}

        signal = self.setup_dataframe.index[stack[0]]

        if setup_infos.is_date_valid():
            restults['date'] = stack_info[1]

            if stack_info[2] == 'BUY':
                results['take_profit'] = True if stack_info[0] <= setup_infos.get_take_profit() else False
                results['stop_loss'] = True if stack_info[0] >= setup_infos.get_stop_loss() else False

                results['position_modify'] = True if stack_info[0] >= setup_infos.get_position_modify() else False
                results['position_close'] = True if stack_info[0] >= setup_infos.get_position_close() else False

            elif stack_info[2] == 'SELL':
                results['take_profit'] = True if stack_info[0] <= setup_infos.get_take_profit() else False
                results['stop_loss'] = True if stack_info[0] >= setup_infos.get_stop_loss() else False

                results['position_modify'] = True if stack_info[0] >= setup_infos.get_position_modify() else False
                results['position_close'] = True if stack_info[0] >= setup_infos.get_position_close() else False

            else:
                results['take_profit'] = False
                results['stop_loss'] = False
                results['position_modify'] = False
                results['position_close'] = False

        return results


    def send_setup_stack_info(self, dataframe: pd.DataFrame) ->  None:
        stack = []

        while not self.is_dataframe_empty(dataframe=dataframe):
            if self.is_stack_empty(stack=stack):
                stack = list(dataframe.iloc[0]) 
                dataframe = dataframe.drop(labels=data.index[0], axis=0, inplace=True)
                time = stack[0]
                stack.remove(time)
            
            value = stack[0]
            stack.remove(value)

            stack_info = (time, value)

            results = self.setup_pre_processing_infos(stack_info)

            self.processing_backtest_info_from_setup(results=results)
            self.export_backtest_log_report(results)


    def processing_backtest_info_from_setup(self, results: dict):
        return

    def export_backtest_log_report(self, results: dict):
        return

    def run_backtest(self):
        return
