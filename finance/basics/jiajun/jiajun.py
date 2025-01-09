
import sys
import pytz
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md
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
df = df[['start_time','close']]

df.start_time = df.start_time.apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S+00'))
df = df.sort_values(['start_time'])
df['time_utc'] = df.start_time.apply(lambda x: x.replace(year=2000,month=1,day=1))
df['date_obj'] = df.start_time.apply(lambda x: x.date())
df['time_obj'] = df.start_time.apply(lambda x: x.time())
df = df[ (df.time_obj >= datetime.time(14,30)) & (df.time_obj < datetime.time(20,30)) ].reset_index()

london_close_price_dict ={}
for date_item in list(df.date_obj.unique()):
    tmp_df = df[(df.date_obj==date_item)&(df.time_obj>=datetime.time(16,18))&(df.time_obj<datetime.time(16,21))]
    if len(tmp_df) > 0:
        london_close_price_dict[date_item] = tmp_df.close.to_list()[-1]
    else:
        london_close_price_dict[date_item] = np.nan
def get_london_close(x):
    return london_close_price_dict[x]

df['london_close']=df.date_obj.apply(lambda x: get_london_close(x))

def get_norm_price(row):
    return row.close/row.london_close

df['norm_price'] = df.apply(lambda row: get_norm_price(row),axis=1)

day_mapper = {0:'0 mon',1:'1 tue',2:'2 wed',3:'3 thu',4:'4 fri'}
def get_day_of_week(x):
    return day_mapper[x.weekday()]

df['weekday'] = df.start_time.apply(lambda x: get_day_of_week(x))

fig, ax = plt.subplots(figsize=(10, 8))
sns.lineplot(x="time_utc",y="norm_price",hue="weekday",data=df,ax=ax)
xfmt = md.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
ax.tick_params(axis='x', labelrotation=45)
plt.title("Jiajun! Trade #LIZJNY, SPY price")
plt.ylabel("price / (price at ~16:15 UTC)")
plt.xlabel("time utc")
plt.grid(True)
plt.tight_layout()
plt.savefig('intraday-spy.png')
