class SetupPreProcessingInfos(object):
    def __init__(self, setup: 'Setup') -> None:
        self.__setup = None

        self.__take_profit = 0.0
        self.__stop_loss = 0.0
        

        self.__is_take_profit = False
        self.__is_stop_loss = False
        self.__is_position_closed = False
        self.__is_position_modify = False
        self.__is_breakeven = False
        self.__is_trailing_stop = False

        self.__start_date = None
        self.__end_data = None


    def __del__(self):
        del self.__setup

        del self.__take_profit
        del self.__stop_loss

        del self.__is_take_profit
        del self.__is_stop_loss
        del self.__is_position_closed
        del self.__is_position_modify
        del self.__is_breakeven
        del self.__is_trailing_stop
        
        del self.__start_date
        del self.__end_data

    def set_take_profit(self, tp: float) -> None:
        if self.param_validation(tp):
            self.__take_profit = tp
        else:
            self.__take_profit = None
    
    def set_stop_loss(self, sl: float) -> None:
        if self.param_validation(sl):
            self.__stop_loss = sl
        else:
            self.__stop_loss = None

    def set_position_modify(self, value: float) -> None:
        if self.param_validation(value):
            self.__position_modify = value
        else:
            self.__position_modify = None

    def set_position_close(self, value: float) -> None:
        if self.param_validation(value):
            self.__position_close = value
        else:
            self.__position_close = None



    def get_take_profit(self) -> float:
        return self.__take_profit

    def get_stop_loss(self) -> float:
        return self.__stop_loss

    def get_position_modify(self) -> float:
        return self.__position_modify

    def get_position_close(self) -> float:
        return self.__position_close



    def get_is_take_profit(self) -> bool:
        return self.__is_take_profit
    
    def get_is_stop_loss(self) -> bool:
        return self.__is_stop_loss

    def get_is_position_modify(self) -> bool:
        return self.__is_position_modify

    def get_is_position_close(self) -> bool:
        return self.__is_position_closed



    def is_date_valid(self, date: str) -> bool:
        if self.__start_date != None or self.__end_data != None:
            if date <= self.__end_date and date >= self.__start_date:
                return True

        return False

    def param_validation(self, param: any) -> bool:
        return True if param is not None else False

    def verify_setup_params(self):
        params = self.__setup.get_setup_params()

        valid_params = {}

        for i in range(len(params)):
            if params[i] != None:
                valid_params[i] = params[i]

        return valid_params