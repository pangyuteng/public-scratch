
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
df['start_date'] = df.start_time.apply(lambda x: x.date())
df['the_time'] = df.start_time.apply(lambda x: x.time())
for d in sorted(list(set([x.date() for x in df.start_time.unique()]))):
    day_df = df[df.start_date==d].reset_index()
    #print(time_series)
    #sys.exit(1)
    print(day_df.shape)
    timeline = [x.replace(year=2000,month=1,day=1) for x in day_df.start_date]
    plt.plot(timeline,day_df.close,alpha=1)
plt.grid(True)
plt.savefig('ok.png')



