class SetupPreProcessingInfos(object):
    def __init__(self, setup: 'Setup') -> None:
        self.__setup = setup

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

        # self.__result = None

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

    def __str__(self):
        return f'Setup: {self.__setup}'

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



    def get_setup_take_profit(self, ticket) -> float:
        return self.__setup.get_take_profit(ticket)

    def get_setup_stop_loss(self) -> float:
        return self.__setup.get_stop_loss()

    def get_position_modify(self) -> float:
        return self.__position_modify

    def get_position_close(self) -> float:
        return self.__position_close

    def get_setup_position_side(self) -> str:
        return self.__setup.get_position_side()

    def get_setup_signal_buy(self, price, **kwargs):
        return self.__setup.get_signal_buy_from_setup(price, kwargs=kwargs['kwargs'])

    def get_setup_signal_sell(self, price, **kwargs):
        return self.__setup.get_signal_sell_from_setup(price, kwargs=kwargs['kwargs'])

    def get_is_take_profit(self) -> bool:
        return self.__is_take_profit
    
    def get_is_stop_loss(self) -> bool:
        return self.__is_stop_loss

    def get_is_position_modify(self) -> bool:
        return self.__is_position_modify

    def get_is_position_close(self) -> bool:
        return self.__is_position_closed

    def have_positions(self):
        return self.__setup.get_any_position()

    def get_orders(self):
        return self.__setup.get_orders()

    def is_date_valid(self, date: str) -> bool:
        return True

        if self.__start_date != None or self.__end_data != None:
            if date <= self.__end_date and date >= self.__start_date:
                return True

        return False

    def param_validation(self, param: any) -> bool:
        return True if param is not None else False

    def verify_setup_params(self):
        params = self.__setup.get_setup_params()
        
        valid_params = {}

        for element in params.keys():
            if params[element] != None:
                valid_params[element] = params[element]

        return valid_params