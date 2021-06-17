from src.server import MetaTraderConnection
from src.charts.renko_chart import Renko

renko = Renko('WIN$N')
server = MetaTraderConnection()

renko.create_chart()