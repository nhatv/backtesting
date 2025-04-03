from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG
import yfinance as yf
import pandas as pd

data = yf.download("AAPL", start="2024-01-01", end="2025-01-01")
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
data.index = pd.to_datetime(data.index)
data.dropna(inplace=True)


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


bt = Backtest(GOOG, SmaCross,
              cash=10000, commission=.002,
              exclusive_orders=True)


print((GOOG))
print(type(data.columns))
#output = bt.run()
#print(output)
#print(yf.download("AAPL", period='1mo'))
#bt.plot()