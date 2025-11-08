import os
import sys
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")


spx_file = sys.argv[1]
vix_file = sys.argv[2]

spx_df = pd.read_csv(spx_file)[['tstamp','spx_close','dayofweek']]
vix_df = pd.read_csv(vix_file)[['tstamp','vix_close']]

def set_return_zero_at_open(row):
    if row.tstamp.hour == 8 and row.tstamp.minute == 30 and row.spx_close is not None: # Centrfal Time Open
        row['spx_log_ret'] = 0.0
        row['vix_log_ret'] = 0.0
    return row

merged_file = 'tmp/cached.csv'
if not os.path.exists(merged_file):
    df = spx_df.merge(vix_df,how='left',on=['tstamp'])
    df = df.dropna()
    df.tstamp = df.tstamp.apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S')+datetime.timedelta(hours=1))
    # aggregate by 15min
    df = df.groupby(pd.Grouper(key="tstamp", freq="15Min")).last().reset_index()
    df['spx_log_ret'] = np.log(df.spx_close/df.spx_close.shift())
    df['vix_log_ret'] = np.log(df.vix_close/df.vix_close.shift())
    # keep open
    df = df.apply(lambda x: set_return_zero_at_open(x),axis=1)
    # remove holidays
    df['date'] = df.tstamp.apply(lambda x: x.strftime('%Y-%m-%d'))
    to_del_list = []
    for itemdate in df.date.unique():
        rowdf = df[df.date==itemdate]
        set_spx_log_ret_len = len(rowdf.spx_log_ret.unique())
        if set_spx_log_ret_len <= 2:
            to_del_list.append(itemdate)
    df['to_delete'] = df.date.apply(lambda x: True if x in to_del_list else False)
    df = df[df.to_delete==False]
    df = df.dropna()
    df.drop(['to_delete'], axis=1, inplace=True)

    dailydf = df[['date','spx_close','vix_close']]
    dailydf = dailydf.groupby(['date']).agg(
        daily_spx_open=pd.NamedAgg(column="spx_close", aggfunc="first"),
        daily_spx_high=pd.NamedAgg(column="spx_close", aggfunc="max"),
        daily_spx_low=pd.NamedAgg(column="spx_close", aggfunc="min"),
        daily_spx_close=pd.NamedAgg(column="spx_close", aggfunc="last"),
        daily_vix_open=pd.NamedAgg(column="vix_close", aggfunc="first"),
        daily_vix_high=pd.NamedAgg(column="vix_close", aggfunc="max"),
        daily_vix_low=pd.NamedAgg(column="vix_close", aggfunc="min"),
        daily_vix_close=pd.NamedAgg(column="vix_close", aggfunc="last"),
    ).reset_index()
    df = df.merge(dailydf,how='left',on=['date'])
    df.to_csv(merged_file,index=False)

df = pd.read_csv(merged_file)
df.tstamp = df.tstamp.apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
df['timeofday'] = df.tstamp.apply(lambda x: x.time())

# tstamp,spx_close,dayofweek,vix_close,spx_log_ret,vix_log_ret

df['spx_daily_prct_change'] = (df.daily_spx_close-df.daily_spx_open)/df.daily_spx_open
df['spx_relative_to_high'] = (df.spx_close-df.daily_spx_high)/df.daily_spx_high
df['spx_relative_to_low'] = (df.spx_close-df.daily_spx_low)/df.daily_spx_low


###################


if True:
    f, ax = plt.subplots(figsize=(10, 20))
    plt.subplot(311)
else:
    f, ax = plt.subplots(figsize=(10, 10))

sns.stripplot(df, x="timeofday", y="spx_log_ret", size=1, color=".3",alpha=0.5)
sns.boxplot(
    df, x="timeofday", y="spx_log_ret",
    width=.6, whis=1.5
)
plt.ylabel("15min log return")
plt.xlabel("time of day")
plt.xticks(rotation=45)
plt.yticks(rotation=45)
ax.xaxis.grid(True)
sns.despine(trim=True, left=True)
if True:
    plt.subplot(312)
    sns.boxplot(
        df[df.spx_daily_prct_change>=0], x="timeofday", y="spx_log_ret",
        width=.6, whis=1.5
    )
    plt.ylabel("15min log return")
    plt.xlabel("time of day ET (spx_daily_prct_change >= 0)")
    plt.xticks(rotation=45)
    plt.yticks(rotation=45)
    ax.xaxis.grid(True)
    sns.despine(trim=True, left=True)

    plt.subplot(313)
    sns.boxplot(
        df[df.spx_daily_prct_change<0], x="timeofday", y="spx_log_ret",
        width=.6, whis=1.5
    )

    plt.ylabel("15min log return")
    plt.xlabel("time of day ET (spx_daily_prct_change < 0)")

    plt.xticks(rotation=45)
    plt.yticks(rotation=45)
    ax.xaxis.grid(True)
    sns.despine(trim=True, left=True)

plt.tight_layout()
plt.savefig("tmp/01-spx_15min_log_ret.png")
plt.close()


###################


f, ax = plt.subplots(figsize=(10, 10))
hue_order = ['Monday','Tuesday','Wednesday','Thursday','Friday']

sns.boxplot(
    df, x="timeofday", y="spx_log_ret",hue='dayofweek',hue_order=hue_order,
    width=.6, whis=1.5
)

plt.ylabel("15min log return")
plt.xlabel("time of day")
plt.xticks(rotation=45)
plt.yticks(rotation=45)
sns.despine(left=True, bottom=True)
plt.savefig("tmp/02-spx_15min_log_ret-by-day-of-week.png")
plt.close()

###################


if True:
    f, ax = plt.subplots(figsize=(10, 20))
    plt.subplot(311)
else:
    f, ax = plt.subplots(figsize=(10, 10))
sns.boxplot(
    df, x="timeofday", y="spx_relative_to_high",
    width=.6, whis=1.5
)
plt.ylabel("price relative to daily high")
plt.xlabel("time of day")
plt.xticks(rotation=45)
plt.yticks(rotation=45)
ax.xaxis.grid(True)
sns.despine(trim=True, left=True)
if True:
    plt.subplot(312)
    sns.boxplot(
        df[df.daily_vix_open<20], x="timeofday", y="spx_relative_to_high",
        width=.6, whis=1.5
    )
    plt.ylabel("price relative to daily high")
    plt.xlabel("time of day (VIX open < 20 )")
    plt.xticks(rotation=45)
    plt.yticks(rotation=45)
    ax.xaxis.grid(True)
    sns.despine(trim=True, left=True)

    plt.subplot(313)
    sns.boxplot(
        df[df.daily_vix_open>=20], x="timeofday", y="spx_relative_to_high",
        width=.6, whis=1.5
    )
    plt.ylabel("price relative to daily high")
    plt.xlabel("time of day (VIX open >= 20)")
    plt.xticks(rotation=45)
    plt.yticks(rotation=45)
    ax.xaxis.grid(True)
    sns.despine(trim=True, left=True)

plt.tight_layout()
plt.savefig("tmp/03-spx_relative_to_high.png")
plt.close()

###################
if True:
    f, ax = plt.subplots(figsize=(10, 20))
    plt.subplot(311)
else:
    f, ax = plt.subplots(figsize=(10, 10))

sns.boxplot(
    df, x="timeofday", y="spx_relative_to_low",
    width=.6, whis=1.5
)
plt.ylabel("price relative to daily low")
plt.xlabel("time of day")
plt.xticks(rotation=45)
plt.yticks(rotation=45)
ax.xaxis.grid(True)
sns.despine(trim=True, left=True)
if True:
    plt.subplot(312)
    sns.boxplot(
        df[df.daily_vix_open<20], x="timeofday", y="spx_relative_to_low",
        width=.6, whis=1.5
    )
    plt.ylabel("price relative to daily low")
    plt.xlabel("time of day (VIX open < 20)")
    plt.xticks(rotation=45)
    plt.yticks(rotation=45)
    ax.xaxis.grid(True)
    sns.despine(trim=True, left=True)

    plt.subplot(313)
    sns.boxplot(
        df[df.daily_vix_open>=20], x="timeofday", y="spx_relative_to_low",
        width=.6, whis=1.5
    )
    plt.ylabel("price relative to daily low")
    plt.xlabel("time of day (VIX open >= 20)")
    plt.xticks(rotation=45)
    plt.yticks(rotation=45)
    ax.xaxis.grid(True)
    sns.despine(trim=True, left=True)

plt.tight_layout()
plt.savefig("tmp/04-spx_relative_to_low.png")
plt.close()


##############
hue_order = ['Monday','Tuesday','Wednesday','Thursday','Friday']

f, ax = plt.subplots(figsize=(10, 10))
sns.boxplot(
    df, x="timeofday", y="spx_relative_to_high",hue='dayofweek',hue_order=hue_order,
    width=.6, whis=1.5
)
plt.ylabel("price relative to daily high")
plt.xlabel("time of day")
plt.xticks(rotation=45)
plt.yticks(rotation=45)
ax.xaxis.grid(True)
sns.despine(trim=True, left=True)
plt.tight_layout()
plt.savefig("tmp/05-spx_relative_to_high-dayofweek.png")
plt.close()


f, ax = plt.subplots(figsize=(10, 10))
sns.boxplot(
    df, x="timeofday", y="spx_relative_to_low",hue='dayofweek',hue_order=hue_order,
    width=.6, whis=1.5
)
plt.ylabel("price relative to daily low")
plt.xlabel("time of day")
plt.xticks(rotation=45)
plt.yticks(rotation=45)
ax.xaxis.grid(True)
sns.despine(trim=True, left=True)
plt.tight_layout()
plt.savefig("tmp/05-spx_relative_to_low-dayofweek.png")
plt.close()


# plot price change relative to open
# plot percent change variance by time

# group by open-close up or down, absolute vix open 15,15-20,20-30,30 and above.
# 
#spx_close dayofweek  vix_close

# vix spx intraday trend by the hour.

print(df.head())



"""

python exploratory.py tmp/spx.csv tmp/vix.csv

"""