import pandas as pd
import yfinance as yf

for ticker,tickerstr in [('SPY','SPY'),('^VIX','VIX'),('^SPX','SPX')]:
    df = yf.Ticker(ticker).history(period="max")
    df.to_csv(f"{tickerstr}.csv")
