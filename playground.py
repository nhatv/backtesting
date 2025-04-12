from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG
import yfinance as yf
import pandas as pd

data = yf.download("BTC-USD", start="2025-03-01", end="2025-04-01", multi_level_index=False, interval= "30m")
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




if __name__ == "__main__":
    bt = Backtest(data, EmaCross,
              cash=1000000, commission=.002,
              exclusive_orders=True)


    print(data)
    # print(type(data.columns))

    output = bt.run()
    important_ls = ["Equity Final [$]", 
                    "Equity Peak [$]", 
                    "Commissions [$]", 
                    "Return [%]", 
                    "Buy & Hold Return [%]", 
                    "# Trades", 
                    "Win Rate [%]", 
                    "Best Trade [%]", 
                    "Worst Trade [%]", 
                    "Avg. Trade [%]", 
                    "Max. Trade Duration", 
                    "Avg. Trade Duration", 
                    "_strategy"]
    important = output[important_ls].to_frame().T.rename(columns={"_strategy": "Strategy"}).set_index("Strategy")
    print(important.T)

    try:
        with pd.ExcelWriter("out.xlsx", mode='a', if_sheet_exists="overlay") as writer:
            important.to_excel(writer, startrow=writer.sheets['Sheet1'].max_row, header=False)
    except FileNotFoundError:
        important.to_excel("out.xlsx")