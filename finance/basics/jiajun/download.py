import os
import pandas as pd
import yfinance as yf

os.makedirs("tmp",exist_ok=True)

for ticker,tickerstr in [('SPY','SPY'),('^VIX','VIX'),('^SPX','SPX')]:
    csv_file = f"tmp/{tickerstr}.csv"
    if not os.path.exists(csv_file):
        df = yf.Ticker(ticker).history(period="max")
        df.to_csv(csv_file)
    else:
        print(f"file found, will not download: {csv_file}")