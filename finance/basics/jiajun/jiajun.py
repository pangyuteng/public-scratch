
import sys
import pytz
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")

utc = pytz.timezone('UTC')
eastern = pytz.timezone('US/Eastern')


csv_file = '/mnt/hd2/data/finance/ohlc_1m_full_market/1y/2023-09-07-through-2024-09-06/SPY.csv'
df = pd.read_csv(csv_file)
print(df.columns)
print(df.shape)

# .replace(tzinfo=utc).astimezone(tz=eastern)
# minute level csv file from unusualwhale, tstamp have "+00", but each day it starts at 8am, so likely eastern time.
# london close 16:30 UCT, 10:30 ET, 8:30 PT.


df.start_time = df.start_time.apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S+00'))
df = df.sort_values(['start_time'])

df['mydate'] = df.start_time.apply(lambda x: x.date())
df['mytime'] = df.start_time.apply(lambda x: x.time())
#df['seconds'] = df.start_time.apply(lambda x: (x.replace(year=2000,month=1,day=1)-datetime.datetime(2000,1,1,8,0,0,0)).total_seconds())
df['seconds'] = df.start_time.apply(lambda x: x.replace(year=2000,month=1,day=1))
df['weekday'] = df.start_time.apply(lambda x: x.weekday())
df['close'] = df['close'].astype(float)

print(df['mytime'].unique())
print(df['weekday'].unique())

sns.lineplot(x="seconds",y="close",hue="weekday",data=df)
plt.savefig('intraday-spy.png')
