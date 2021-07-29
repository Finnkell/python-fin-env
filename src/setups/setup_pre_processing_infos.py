class SetupPreProcessingInfos(object):
    def __init__(self, setup: 'Setup') -> None:
        self.setup = None

        self.take_profit = 0.0
        self.stop_loss = 0.0
        

        self.is_take_profit = False
        self.is_stop_loss = False
        self.is_position_closed = False
        self.is_position_modify = False
        self.is_breakeven = False
        self.is_trailing_stop = False

        self.start_date = None
        self.end_data = None


    def __del__(self):
        del self.take_profit
        del self.stop_loss

        del self.is_take_profit
        del self.is_stop_loss
        del self.is_position_closed
        del self.is_position_modify
        del self.is_breakeven
        del self.is_trailing_stop
        
        del self.start_date
        del self.end_data

    def set_take_profit(self, tp: float) -> None:
        if self.param_validation(tp):
            self.take_profit = tp
        else:
            self.take_profit = None
    
    def set_stop_loss(self, sl: float) -> None:
        if self.param_validation(sl):
            self.stop_loss = sl
        else:
            self.stop_loss = None

    def set_position_modify(self, value: float) -> None:
        if self.param_validation(value):
            self.position_modify = value
        else:
            self.position_modify = None

    def set_position_close(self, value: float) -> None:
        if self.param_validation(value):
            self.position_close = value
        else:
            self.position_close = None



    def get_take_profit(self) -> float:
        return self.take_profit

    def get_stop_loss(self) -> float:
        return self.stop_loss

    def get_position_modify(self) -> float:
        return self.position_modify

    def get_position_close(self) -> float:
        return self.position_close



    def get_is_take_profit(self) -> bool:
        return self.is_take_profit
    
    def get_is_stop_loss(self) -> bool:
        return self.is_stop_loss

    def get_is_position_modify(self) -> bool:
        return self.is_position_modify

    def get_is_position_close(self) -> bool:
        return self.is_position_closed



    def is_date_valid(self, date: str) -> bool:
        if self.start_date != None or self.end_data != None:
            if date <= self.end_date and date >= self.start_date:
                return True

        return False

    def param_validation(self, param: any) -> bool:
        return True if param is not None else False