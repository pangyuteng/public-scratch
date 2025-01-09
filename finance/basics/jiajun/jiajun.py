import pandas as pd
import matplotlib.pyplot as plt

csv_file = '/mnt/hd2/data/finance/ohlc_1m_full_market/1y/2023-09-07-through-2024-09-06/SPY.csv'
df = pd.read_csv(csv_file)
print(df.columns)
print(df.shape)
