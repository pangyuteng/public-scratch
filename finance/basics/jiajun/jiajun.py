
import sys
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")

csv_file = '/mnt/hd2/data/finance/ohlc_1m_full_market/1y/2023-09-07-through-2024-09-06/SPY.csv'
df = pd.read_csv(csv_file)
print(df.columns)
print(df.shape)

df.start_time = df.start_time.apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S+00'))
df.end_time = df.end_time.apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S+00'))
df = df.sort_values(['start_time'])

df['mydate'] = df.start_time.apply(lambda x: x.date())
df['mytime'] = df.start_time.apply(lambda x: x.time())
df['seconds'] = df.start_time.apply(lambda x: (x.replace(year=2000,month=1,day=1)-datetime.datetime(2000,1,1,0,0,0)).total_seconds())
df['weekday'] = df.start_time.apply(lambda x: x.weekday())
df['close'] = df['close'].astype(float)

print(df['mytime'].unique())
print(df['weekday'].unique())

sns.lineplot(x="seconds",y="close",hue="weekday",data=df)
plt.savefig('ok.png')

"""
#tstamp_list = pd.date_range(start="2000-01-01 09:30:00",end="2000-01-01 16:00:00",freq='m')
date_list = sorted(list(df.mydate.unique()))
mylist = []
for date_item in date_list:
    day_df = df[df.mydate==date_item].reset_index()

    time_list = list([x.replace(year=2000,month=1,day=1) for x in day_df.mydate])
    price_list = np.array(list(day_df.close))
    if len(price_list) > 600:
        price_list = price_list/price_list[120]
        mylist.append(price_list[:600])
        plt.plot(price_list,alpha=0.2)

mylist = np.array(mylist)
mean_price = np.median(mylist,axis=0)


plt.plot(mean_price,linewidth=2)

plt.grid(True)
plt.savefig('ok.png')
"""
