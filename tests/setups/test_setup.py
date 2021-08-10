import pytest
import pandas as pd

import os
print(f"caminho: {os.getcwd()}")

try:
    from src.setups.cross_mm import CrossMMSetupWIN
except Exception as e:
    print(f"Exception: {e}")

class MessageException(Exception):
    def __init__(self, message: str):
        self.msg = message
        super().__init__(self.msg)

df = pd.read_csv("src\database\ohlc\WIN$N_M1.csv", nrows=25)
setup = CrossMMSetupWIN()

class TestSetup():
    def __init__(self):
        pass

    def test_create_strategy(self):
        global df
        global setup
        # df = df.rename(columns={"Date": "DIA"})

        try:
            # with pytest.raises(ValueError):
            teste = setup.create_strategy(dataframe=df)
            print(teste)
            # print("f"teste: {type(teste)}")
            # print(f"df: {type(pd.DataFrame())}")
            assert teste != None
        except AssertionError as e:
            raise MessageException(f"PEGA O RAISE ERRO: {e}")


testset = TestSetup()
testset.test_create_strategy()