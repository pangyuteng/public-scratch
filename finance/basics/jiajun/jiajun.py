
import sys
import datetime
import pandas as pd
import matplotlib.pyplot as plt

csv_file = '/mnt/hd2/data/finance/ohlc_1m_full_market/1y/2023-09-07-through-2024-09-06/SPY.csv'
df = pd.read_csv(csv_file)
print(df.columns)
print(df.shape)


df.start_time = df.start_time.apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S+00'))
df.end_time = df.end_time.apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S+00'))

for d in sorted(list(set([x.date() for x in df.start_time.unique()]))):
    date_filter = df.start_time.apply(lambda x: x.date())==d
    day_df = df[date_filter].reset_index()
    time_series = day_df.start_time.apply(lambda x: x.time())
    #print(time_series)
    #sys.exit(1)
    plt.plot(day_df.start_time,day_df.close,alpha=0.2)
plt.figsave('ok.png')



