from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG
import yfinance as yf
import pandas as pd
from datetime import date, datetime
from Strategies import *

if __name__ == "__main__":
    strat = EmaCross
    interval = "15m"
    start = "2025-03-21" #2025-03-01
    end = "2025-04-01"   #2025-04-01
    data = yf.download("BTC-USD", start=start, end=end, multi_level_index=False, interval=interval)
    bt = Backtest(data, strat, cash=1000000, commission=.004, exclusive_orders=True)

    # print(data)
    # print(type(data.columns))

    output = bt.run()

    important_ls = ["Take Profit [%]", 
                    "Stop Loss [%]", 
                    "Interval", 
                    "Start", 
                    "End", 
                    "Duration", 
                    "Equity Final [$]", 
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
    output["Take Profit [%]"], output["Stop Loss [%]"], output["Interval"] = strat.tp , strat.sl, interval
    output["Start"] = output["Start"].strftime("%Y/%m/%d")
    output["End"] = output["End"].strftime("%Y/%m/%d")
    important = output[important_ls].to_frame().T.rename(columns={"_strategy": "Strategy"}).set_index("Strategy")
    print(important.T)

    write_bool = input("Write to excel? (y/n)\n")
    if write_bool.lower() == "y" or write_bool == "":
        try:
            # Append to excel file
            with pd.ExcelWriter("out.xlsx", engine="openpyxl", mode= "a", if_sheet_exists="overlay",  
                                date_format="yyyy/mm/dd", datetime_format="yyyy/mm/dd hh:mm:ss") as writer:
                important.to_excel(writer, sheet_name="Sheet1", startrow=writer.sheets['Sheet1'].max_row, header=False)
        except (FileNotFoundError, KeyError) as e: # Create one if there is no excel file
            important.to_excel("out.xlsx")