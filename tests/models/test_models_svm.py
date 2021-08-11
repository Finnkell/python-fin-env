import pytest

from src.models.svm import *

class MessageException(Exception):
    def __init__(self, message: str):
        self.msg = message
        super().__init__(self.msg)

SVC = SVCModel()
SVR = SVRModel()
LINEAR_SVC = LinearSVCModel()
LINEAR_SVR = LinearSVRModel()
NU_SVC = NuSVCModel()
NU_SVR = NuSVRModel()

'''
>>> Classification Models: SVC, LinearSVC, NuSVC
'''
class TestSVCModel():
    def test_create_model(self):
        try:
            with pytest.raises(TypeError):
                SVC.create_model(C='1.01')
                SVC.create_model(kernel=1)
                SVC.create_model(degree='1.01')
                SVC.create_model(gamma=1)
                SVC.create_model(coef0='1.01')
                SVC.create_model(tol='1.01')
                SVC.create_model(tol=False)
                SVC.create_model(epsilon='1.01')
                SVC.create_model(shrinking='1.01')
                SVC.create_model(shrinking=1)
                SVC.create_model(shrinking=1.5)
                SVC.create_model(cache_size='1.01')
                SVC.create_model(max_iter='1.01')
                SVC.create_model(max_iter=False)
        except AssertionError as e:
            raise MessageException(f'{e}')

        try:
            assert SVC.create_model(C=1.01) == None
            assert SVC.create_model(kernel='linear') == None
            assert SVC.create_model(degree=1) == None
            assert SVC.create_model(gamma='scale') == None
            assert SVC.create_model(coef0=1.01) == None
            assert SVC.create_model(tol=1.01) == None
            assert SVC.create_model(epsilon=1.01) == None
            assert SVC.create_model(shrinking=True) == None
            assert SVC.create_model(cache_size=100.0) == None
            assert SVC.create_model(max_iter=10) == None
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_get_data(self):
        pass

    def test_examples(self):
        pass

    def test_fit_model(self):
        pass

    def test_predict(self):
        pass

    def test_evaluate_model(self):
        pass

    def test_model_summary(self):
        pass

    def test_save_model(self):
        pass


class TestLinearSVCModel():
    def test_create_model(self):
        try:
            with pytest.raises(TypeError):
                LINEAR_SVC.create_model(C='1.01')
                LINEAR_SVC.create_model(kernel=1)
                LINEAR_SVC.create_model(degree='1.01')
                LINEAR_SVC.create_model(gamma=1)
                LINEAR_SVC.create_model(coef0='1.01')
                LINEAR_SVC.create_model(tol='1.01')
                LINEAR_SVC.create_model(tol=False)
                LINEAR_SVC.create_model(epsilon='1.01')
                LINEAR_SVC.create_model(shrinking='1.01')
                LINEAR_SVC.create_model(shrinking=1)
                LINEAR_SVC.create_model(shrinking=1.5)
                LINEAR_SVC.create_model(cache_size='1.01')
                LINEAR_SVC.create_model(max_iter='1.01')
                LINEAR_SVC.create_model(max_iter=False)
        except AssertionError as e:
            raise MessageException(f'{e}')

        try:
            assert LINEAR_SVC.create_model(C=1.01) == None
            assert LINEAR_SVC.create_model(kernel='linear') == None
            assert LINEAR_SVC.create_model(degree=1) == None
            assert LINEAR_SVC.create_model(gamma='scale') == None
            assert LINEAR_SVC.create_model(coef0=1.01) == None
            assert LINEAR_SVC.create_model(tol=1.01) == None
            assert LINEAR_SVC.create_model(epsilon=1.01) == None
            assert LINEAR_SVC.create_model(shrinking=True) == None
            assert LINEAR_SVC.create_model(cache_size=100.0) == None
            assert LINEAR_SVC.create_model(max_iter=10) == None
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_get_data(self):
        pass

    def test_examples(self):
        pass

    def test_fit_model(self):
        pass

    def test_predict(self):
        pass
        
    def test_evaluate_model(self):
        pass

    def test_model_summary(self):
        pass

    def test_save_model(self):
        pass


class TestNuSVCModel():
    def test_create_model(self):
        try:
            with pytest.raises(TypeError):
                NU_SVC.create_model(C='1.01')
                NU_SVC.create_model(kernel=1)
                NU_SVC.create_model(degree='1.01')
                NU_SVC.create_model(gamma=1)
                NU_SVC.create_model(coef0='1.01')
                NU_SVC.create_model(tol='1.01')
                NU_SVC.create_model(tol=False)
                NU_SVC.create_model(epsilon='1.01')
                NU_SVC.create_model(shrinking='1.01')
                NU_SVC.create_model(shrinking=1)
                NU_SVC.create_model(shrinking=1.5)
                NU_SVC.create_model(cache_size='1.01')
                NU_SVC.create_model(max_iter='1.01')
                NU_SVC.create_model(max_iter=False)
        except AssertionError as e:
            raise MessageException(f'{e}')

        try:
            assert NU_SVC.create_model(C=1.01) == None
            assert NU_SVC.create_model(kernel='linear') == None
            assert NU_SVC.create_model(degree=1) == None
            assert NU_SVC.create_model(gamma='scale') == None
            assert NU_SVC.create_model(coef0=1.01) == None
            assert NU_SVC.create_model(tol=1.01) == None
            assert NU_SVC.create_model(epsilon=1.01) == None
            assert NU_SVC.create_model(shrinking=True) == None
            assert NU_SVC.create_model(cache_size=100.0) == None
            assert NU_SVC.create_model(max_iter=10) == None
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_get_data(self):
        pass

    def test_examples(self):
        pass

    def test_fit_model(self):
        pass

    def test_predict(self):
        pass
        
    def test_evaluate_model(self):
        pass

    def test_model_summary(self):
        pass

    def test_save_model(self):
        pass

'''
>>> Regression Models: SVR, LinearSVR, NuSVR
'''
class TestSVRModel():
    def test_create_model(self):
        try:
            with pytest.raises(TypeError):
                SVR.create_model(C='1.01')
                SVR.create_model(kernel=1)
                SVR.create_model(degree='1.01')
                SVR.create_model(gamma=1)
                SVR.create_model(coef0='1.01')
                SVR.create_model(tol='1.01')
                SVR.create_model(tol=False)
                SVR.create_model(epsilon='1.01')
                SVR.create_model(shrinking='1.01')
                SVR.create_model(shrinking=1)
                SVR.create_model(shrinking=1.5)
                SVR.create_model(cache_size='1.01')
                SVR.create_model(max_iter='1.01')
                SVR.create_model(max_iter=False)
        except AssertionError as e:
            raise MessageException(f'{e}')

        try:
            assert SVR.create_model(C=1.01) == None
            assert SVR.create_model(kernel='linear') == None
            assert SVR.create_model(degree=1) == None
            assert SVR.create_model(gamma='scale') == None
            assert SVR.create_model(coef0=1.01) == None
            assert SVR.create_model(tol=1.01) == None
            assert SVR.create_model(epsilon=1.01) == None
            assert SVR.create_model(shrinking=True) == None
            assert SVR.create_model(cache_size=100.0) == None
            assert SVR.create_model(max_iter=10) == None
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_get_data(self):
        pass

    def test_examples(self):
        pass

    def test_fit_model(self):
        pass

    def test_predict(self):
        pass
        
    def test_evaluate_model(self):
        pass

    def test_model_summary(self):
        pass

    def test_save_model(self):
        pass


class TestLinearSVRModel():
    def test_create_model(self):
        try:
            with pytest.raises(TypeError):
                LINEAR_SVR.create_model(C='1.01')
                LINEAR_SVR.create_model(kernel=1)
                LINEAR_SVR.create_model(degree='1.01')
                LINEAR_SVR.create_model(gamma=1)
                LINEAR_SVR.create_model(coef0='1.01')
                LINEAR_SVR.create_model(tol='1.01')
                LINEAR_SVR.create_model(tol=False)
                LINEAR_SVR.create_model(epsilon='1.01')
                LINEAR_SVR.create_model(shrinking='1.01')
                LINEAR_SVR.create_model(shrinking=1)
                LINEAR_SVR.create_model(shrinking=1.5)
                LINEAR_SVR.create_model(cache_size='1.01')
                LINEAR_SVR.create_model(max_iter='1.01')
                LINEAR_SVR.create_model(max_iter=False)
        except AssertionError as e:
            raise MessageException(f'{e}')

        try:
            assert LINEAR_SVR.create_model(C=1.01) == None
            assert LINEAR_SVR.create_model(kernel='linear') == None
            assert LINEAR_SVR.create_model(degree=1) == None
            assert LINEAR_SVR.create_model(gamma='scale') == None
            assert LINEAR_SVR.create_model(coef0=1.01) == None
            assert LINEAR_SVR.create_model(tol=1.01) == None
            assert LINEAR_SVR.create_model(epsilon=1.01) == None
            assert LINEAR_SVR.create_model(shrinking=True) == None
            assert LINEAR_SVR.create_model(cache_size=100.0) == None
            assert LINEAR_SVR.create_model(max_iter=10) == None
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_get_data(self):
        pass

    def test_examples(self):
        pass

    def test_fit_model(self):
        pass

    def test_predict(self):
        pass
        
    def test_evaluate_model(self):
        pass

    def test_model_summary(self):
        pass

    def test_save_model(self):
        pass


class TestNuSVRModel():
    def test_create_model(self):
        try:
            with pytest.raises(TypeError):
                NU_SVR.create_model(C='1.01')
                NU_SVR.create_model(kernel=1)
                NU_SVR.create_model(degree='1.01')
                NU_SVR.create_model(gamma=1)
                NU_SVR.create_model(coef0='1.01')
                NU_SVR.create_model(tol='1.01')
                NU_SVR.create_model(tol=False)
                NU_SVR.create_model(epsilon='1.01')
                NU_SVR.create_model(shrinking='1.01')
                NU_SVR.create_model(shrinking=1)
                NU_SVR.create_model(shrinking=1.5)
                NU_SVR.create_model(cache_size='1.01')
                NU_SVR.create_model(max_iter='1.01')
                NU_SVR.create_model(max_iter=False)
        except AssertionError as e:
            raise MessageException(f'{e}')

        try:
            assert NU_SVR.create_model(C=1.01) == None
            assert NU_SVR.create_model(kernel='linear') == None
            assert NU_SVR.create_model(degree=1) == None
            assert NU_SVR.create_model(gamma='scale') == None
            assert NU_SVR.create_model(coef0=1.01) == None
            assert NU_SVR.create_model(tol=1.01) == None
            assert NU_SVR.create_model(epsilon=1.01) == None
            assert NU_SVR.create_model(shrinking=True) == None
            assert NU_SVR.create_model(cache_size=100.0) == None
            assert NU_SVR.create_model(max_iter=10) == None
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_get_data(self):
        try:
            with pytest.raises(ValueError):
                NU_SVR.get_data(dataframe=None)
        except AssertionError as e:
            raise MessageException(f'{e}')

        try:
            assert NU_SVR.create_model(dataframe=pd.read_csv('src/database/ohlc/WIN/WIN$N_M15.csv', sep=',')) == None
        except AssertionError as e:
            raise MessageException(f'{e}')
        
    def test_examples(self):
        try:
            assert NU_SVR.example() == None
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_fit_model(self):
        try:
            assert NU_SVR.fit_model() == None
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_predict(self):
        try:
            assert type(NU_SVR.predict()) == float
        except AssertionError as e:
            raise MessageException(f'{e}')
        
    def test_evaluate_model(self):
        pass

    def test_model_summary(self):
        try:
            assert NU_SVR.model_summary() == {}
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_save_model(self):
        pass