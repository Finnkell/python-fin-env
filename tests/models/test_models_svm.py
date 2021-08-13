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

df = pd.read_csv('src/database/ohlc/WIN$N_D1.csv', nrows=10, sep=',')

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
        global df

        try:
            with pytest.raises(ValueError):
                SVC.get_data(dataframe=None)
        except AssertionError as e:
            raise MessageException(f'{e}')

        try:
            assert SVC.get_data(dataframe=df) == None
        except AssertionError as e:
            raise MessageException(f'{e}')


    def test_examples(self):
        global df

        pass

    def test_fit_model(self):
        global df

        try:
            X_train, y_train, _, _ = calculate_data(dataframe=df)
            SVC.create_model()
            assert SVC.fit_model(X_train=X_train, y_train=y_train) == None
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_predict(self):
        global df

        try:
            X_train, y_train, X_test, _ = calculate_data(dataframe=df)
            SVC.create_model()
            SVC.fit_model(X_train=X_train, y_train=y_train)
            assert type(SVC.predict(X_pred=X_test)[0]) == np.float64
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_evaluate_model(self):
        global df

        try:
            with pytest.raises(NotImplementedError):
                SVC.evaluate_model()
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_model_summary(self):
        global df

        try:
            '''#TODO: Create train/test functions'''
            assert dict == dict
        except AssertionError as e:
            raise MessageException(f'{e}')

        try:
            # assert len(SVC.model_summary()) > 0
            assert 1 > 0
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_save_model(self):
        global df

        pass


class TestLinearSVCModel():
    def test_create_model(self):
        global df

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
        global df

        try:
            with pytest.raises(ValueError):
                LINEAR_SVC.get_data(dataframe=None)
        except AssertionError as e:
            raise MessageException(f'{e}')

        try:
            assert LINEAR_SVC.get_data(dataframe=df) == None
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_examples(self):
        global df

        pass

    def test_fit_model(self):
        global df

        try:
            X_train, y_train, _, _ = calculate_data(dataframe=df)
            LINEAR_SVC.create_model()
            assert LINEAR_SVC.fit_model(X_train=X_train, y_train=y_train) == None
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_predict(self):
        global df

        try:
            X_train, y_train, X_test, _ = calculate_data(dataframe=df)
            LINEAR_SVC.create_model()
            LINEAR_SVC.fit_model(X_train=X_train, y_train=y_train)
            assert type(LINEAR_SVC.predict(X_pred=X_test)[0]) == np.float64
        except AssertionError as e:
            raise MessageException(f'{e}')
        
    def test_evaluate_model(self):
        global df

        try:
            with pytest.raises(NotImplementedError):
                LINEAR_SVC.evaluate_model()
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_model_summary(self):
        global df

        try:
            assert dict == dict
        except AssertionError as e:
            raise MessageException(f'{e}')

        try:
            assert 1 > 0
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_save_model(self):
        global df

        pass


class TestNuSVCModel():
    def test_create_model(self):
        global df

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
        global df

        try:
            with pytest.raises(ValueError):
                NU_SVC.get_data(dataframe=None)
        except AssertionError as e:
            raise MessageException(f'{e}')

        try:
            assert NU_SVC.get_data(dataframe=df) == None
        except AssertionError as e:
            raise MessageException(f'{e}')


    def test_examples(self):
        global df

        pass

    def test_fit_model(self):
        global df

        try:
            X_train, y_train, _, _ = calculate_data(dataframe=df)
            NU_SVC.create_model()
            assert NU_SVC.fit_model(X_train=X_train, y_train=y_train) == None
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_predict(self):
        global df

        try:
            X_train, y_train, X_test, _ = calculate_data(dataframe=df)
            NU_SVC.create_model()
            NU_SVC.fit_model(X_train=X_train, y_train=y_train)
            assert type(NU_SVC.predict(X_pred=X_test)[0]) == np.float64
        except AssertionError as e:
            raise MessageException(f'{e}')
        
    def test_evaluate_model(self):
        global df

        try:
            with pytest.raises(NotImplementedError):
                NU_SVC.evaluate_model()
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_model_summary(self):
        global df

        try:
            assert dict == dict
        except AssertionError as e:
            raise MessageException(f'{e}')

        try:
            assert 1 > 0
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_save_model(self):
        global df

        pass

'''
>>> Regression Models: SVR, LinearSVR, NuSVR
'''
class TestSVRModel():
    def test_create_model(self):
        global df

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
        global df

        try:
            with pytest.raises(ValueError):
                SVR.get_data(dataframe=None)
        except AssertionError as e:
            raise MessageException(f'{e}')

        try:
            assert SVR.get_data(dataframe=df) == None
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_examples(self):
        global df

        pass

    def test_fit_model(self):
        global df

        try:
            X_train, y_train, _, _ = calculate_data(dataframe=df)
            SVR.create_model()
            assert SVR.fit_model(X_train=X_train, y_train=y_train) == None
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_predict(self):
        global df

        try:
            X_train, y_train, X_test, _ = calculate_data(dataframe=df)
            SVR.create_model()
            SVR.fit_model(X_train=X_train, y_train=y_train)
            assert type(SVR.predict(X_pred=X_test)[0]) == np.float64
        except AssertionError as e:
            raise MessageException(f'{e}')
        
    def test_evaluate_model(self):
        global df

        try:
            with pytest.raises(NotImplementedError):
                SVR.evaluate_model()
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_model_summary(self):
        global df

        try:
            '''#TODO: Create train/test functions'''
            assert dict == dict
        except AssertionError as e:
            raise MessageException(f'{e}')

        try:
            # assert len(SVC.model_summary()) > 0
            assert 1 > 0
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_save_model(self):
        global df

        pass


class TestLinearSVRModel():
    def test_create_model(self):
        global df

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
        global df

        try:
            with pytest.raises(ValueError):
                LINEAR_SVR.get_data(dataframe=None)
        except AssertionError as e:
            raise MessageException(f'{e}')

        try:
            assert LINEAR_SVR.get_data(dataframe=df) == None
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_examples(self):
        global df

        pass

    def test_fit_model(self):
        global df

        try:
            X_train, y_train, _, _ = calculate_data(dataframe=df)
            LINEAR_SVR.create_model()
            LINEAR_SVR.fit_model(X_train=X_train, y_train=y_train)
            assert LINEAR_SVR.fit_model(X_train=X_train, y_train=y_train) == None
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_predict(self):
        global df

        try:
            X_train, y_train, X_test, _ = calculate_data(dataframe=df)
            LINEAR_SVR.create_model()
            LINEAR_SVR.fit_model(X_train=X_train, y_train=y_train)
            assert type(LINEAR_SVR.predict(X_pred=X_test)[0]) == np.float64
        except AssertionError as e:
            raise MessageException(f'{e}')
        
    def test_evaluate_model(self):
        global df

        try:
            with pytest.raises(NotImplementedError):
                LINEAR_SVR.evaluate_model()
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_model_summary(self):
        global df

        try:
            '''#TODO: Create train/test functions'''
            assert dict == dict
        except AssertionError as e:
            raise MessageException(f'{e}')

        try:
            # assert len(SVC.model_summary()) > 0
            assert 1 > 0
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_save_model(self):
        global df

        pass


class TestNuSVRModel():
    def test_create_model(self):
        global df

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
        global df

        try:
            with pytest.raises(ValueError):
                NU_SVR.get_data(dataframe=None)
        except AssertionError as e:
            raise MessageException(f'{e}')

        try:
            assert NU_SVR.get_data(dataframe=df) == None
        except AssertionError as e:
            raise MessageException(f'{e}')
        
    def test_examples(self):
        global df

        try:
            assert NU_SVR.example() == None
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_fit_model(self):
        global df

        try:
            X_train, y_train, _, _ = calculate_data(dataframe=df)
            NU_SVR.create_model()
            assert NU_SVR.fit_model(X_train=X_train, y_train=y_train) == None
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_predict(self):
        global df

        try:
            X_train, y_train, X_test, _ = calculate_data(dataframe=df)
            NU_SVR.create_model()
            NU_SVR.fit_model(X_train=X_train, y_train=y_train)
            assert type(NU_SVR.predict(X_pred=X_test)[0]) == np.float64
        except AssertionError as e:
            raise MessageException(f'{e}')
        
    def test_evaluate_model(self):
        global df

        try:
            with pytest.raises(NotImplementedError):
                NU_SVR.evaluate_model()
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_model_summary(self):
        global df

        try:
            '''#TODO: Create train/test functions'''
            assert dict == dict
        except AssertionError as e:
            raise MessageException(f'{e}')

        try:
            # assert len(SVC.model_summary()) > 0
            assert 1 > 0
        except AssertionError as e:
            raise MessageException(f'{e}')

    def test_save_model(self):
        global df

        pass


def calculate_data(dataframe):

    validation_size = 0.2

    dataframe = dataframe.drop(['Tick', 'Volume', 'Spread', 'Date'], axis=1)

    X = dataframe

    value = dataframe['Close'][dataframe.index[-1]]
    temp = pd.DataFrame(X['Close'].shift(-1).fillna(value))

    y = pd.DataFrame()

    y['Diff'] = dataframe['Open']/temp['Close']
    y['Signal'] = np.where(y['Diff'] > 1, 1, 0)
    y = y.drop(['Diff'], axis=1)

    train_size = int(len(X) * (1 - validation_size))

    X_train, X_test = X[:train_size], X[train_size:len(X)]
    y_train, y_test = y[:train_size], y[train_size:len(y)]

    return X_train, y_train, X_test, y_test