from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG
import pandas as pd

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
    tp = 2
    sl = -1
    
    def init(self):
        self.ema1 = self.I(EMA, self.data.Close, self.n1)
        self.ema2 = self.I(EMA, self.data.Close, self.n2)
        self.positionActive = False

    def next(self):
        if crossover(self.ema1, self.ema2) and self.positionActive == False:# get IN to the trade
            self.position.close()
            self.buy()
            self.positionActive = True
        elif (self.position.pl_pct >= self.tp or self.position.pl_pct <= self.sl) and self.positionActive == True: # check if its time to get OUT
            self.position.close()
            self.sell()
            self.positionActive = False

    #def next(self):
        #if Condition to buy exists AND not already in trade:
            #self.buy()
            #turn on flag to signal 'in a trade' flag = 1
        #elif self.position.close:
            #TP or SL