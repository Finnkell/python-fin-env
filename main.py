# %%
import threading
import concurrent.futures
import subprocess
import time
import random
from datetime import datetime
from src.models.svm import SVRModel, NuSVRModel, LinearSVRModel, SVCModel, NuSVCModel, LinearSVCModel
from src.setups.mfi import MFISetup


model_1 = SVRModel()
model_2 = NuSVRModel()
model_3 = LinearSVRModel()
model_4 = SVCModel()
model_5 = NuSVCModel()
model_6 = LinearSVCModel()

start = time.perf_counter()

# t1 = threading.Thread(target=model_1.example_model_diabetes)
# t2 = threading.Thread(target=model_2.example_model_diabetes)
# t3 = threading.Thread(target=model_3.example_model_diabetes)
# t4 = threading.Thread(target=model_4.example_model_breast_cancer)
# t5 = threading.Thread(target=model_5.example_model_breast_cancer)
# t6 = threading.Thread(target=model_6.example_model_breast_cancer)


# t1.start()
# t2.start()
# t3.start()
# t4.start()
# t5.start()
# t6.start()

# t1.join()
# t2.join()
# t3.join()
# t4.join()
# t5.join()
# t6.join()

setup = MFISetup()

setup.example()

setup.calculations()

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')