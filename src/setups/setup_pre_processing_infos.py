class SetupPreProcessingInfos(object):
    def __init__(self, setup: 'Setup') -> None:
        self.__setup = setup

        self.__start_date = None
        self.__end_data = None

    def __del__(self):
        del self.__setup

        del self.__start_date
        del self.__end_data

    def __str__(self):
        return f'Setup: {self.__setup}'

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

    def have_positions(self) -> bool:
        return self.__setup.get_any_position()

    def get_orders(self) -> list:
        return self.__setup.get_orders()

    def is_date_valid(self, date: str) -> bool:
        '''
        TODO: Validate datetime from setup
        '''
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