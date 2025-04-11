from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG
import yfinance as yf
import pandas as pd

data = yf.download("BTC-USD", start="2024-01-01", end="2025-01-01", multi_level_index=False, interval= "1h")
# data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
# data.index = pd.to_datetime(data.index)
# data.dropna(inplace=True)

def EMA(arr: pd.Series, n: int) -> pd.Series:
    return pd.Series(arr).ewm(span=n).mean()


class SmaCross(Strategy):
    n1 = 10
    n2 = 20

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell()

class EmaCross(Strategy):
    n1 = 50
    n2 = 200
    
    def init(self):
        self.ema1 = self.I(EMA, self.data.Close, self.n1)
        self.ema2 = self.I(EMA, self.data.Close, self.n2)
        self.positionActive = False

    def next(self):
        if crossover(self.ema1, self.ema2) and self.positionActive == False:# get IN to the trade
            self.position.close()
            self.buy()
            self.positionActive = True
        elif self.position.pl_pct >= 2 or self.position.pl_pct <= -1: # check if its time to get OUT
            self.position.close()
            self.sell()
            self.positionActive = False

    #def next(self):
        #if Condition to buy exists AND not already in trade:
            #self.buy()
            #turn on flag to signal 'in a trade' flag = 1
        #elif self.position.close:
            #TP or SL


bt = Backtest(data, EmaCross,
              cash=1000000, commission=.002,
              exclusive_orders=True)


print(data)
# print(type(data.columns))

output = bt.run()
print(output)


bt.plot()