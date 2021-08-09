import pytest

from src.models.svm import *

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
            assert SVC.create_model() != None
        except Exception as e:
            print(f'Exception: {e}')

        try:
            assert SVC.create_model(C='Test') == None
        except Exception as e:
            print(f'Exception: {e}')

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
    def test():
        pass


class TestNuSVCModel():
    def test():
        pass

'''
>>> Regression Models: SVR, LinearSVR, NuSVR
'''
class TestSVCModel():
    def test_create_model(self):
        try:
            assert SVC.create_model() != None
        except Exception as e:
            print(f'Exception: {e}')

        try:
            assert SVC.create_model(C='Test') == None
        except Exception as e:
            print(f'Exception: {e}')


class TestLinearSVCModel():
    def test():
        pass


class TestNuSVCModel():
    def test():
        pass