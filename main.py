from src.servers.server_mt5 import MetaTraderConnection
from time import sleep
from datetime import datetime
from src.models.svm import SVRModel


import threading
import concurrent.futures
import subprocess

import time
import random


model = SVRModel()


start = time.perf_counter()

t1 = threading.Thread(target=model.example_model_boston)
t2 = threading.Thread(target=model.example_model_diabetes)

t1.start()
t2.start()

t1.join()
t2.join()

# model.example_model_boston()
# model.example_model_diabetes()

# with concurrent.futures.ThreadPoolExecutor() as executor:
#     secs = [random.randint(10, 12) for _ in range(5)]

#     results = executor.map(test, secs)
    
#     for result in results:
#         print(f'{result}')

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')