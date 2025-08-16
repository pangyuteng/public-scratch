import os
import sys
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


csv_file = "tmp/history.csv"

def mergedf():

    # Date,Open,High,Low,Close,Volume,Dividends,Stock Splits
    # 1927-12-30 00:00:00-05:00,17.65999984741211,17.65999984741211,17.65999984741211,17.65999984741211,0,0.0,0.0

    spx_df = pd.read_csv("tmp/SPX.csv")
    
    spx_df['tstamp'] = spx_df.Date.apply(lambda x: datetime.datetime.strptime(x.split(" ")[0],"%Y-%m-%d"))
    spx_df = spx_df.rename(columns={"Open":"spx_open","High":"spx_high","Low":"spx_low","Close":"spx_close"})
    cols = ['tstamp','spx_open','spx_high','spx_low','spx_close']
    spx_df = spx_df[cols]
    print(spx_df.shape)

    vix_df = pd.read_csv("tmp/VIX.csv")
    vix_df['tstamp'] = vix_df.Date.apply(lambda x: datetime.datetime.strptime(x.split(" ")[0],"%Y-%m-%d"))
    vix_df = vix_df.rename(columns={"Open":"vix_open","High":"vix_high","Low":"vix_low","Close":"vix_close"})
    cols = ['tstamp','vix_high','vix_open','vix_low','vix_close']
    vix_df = vix_df[cols]
    print(vix_df.shape)

    df = vix_df.merge(spx_df,how='left',on=['tstamp'])
    df = df.dropna()
    print(df.head())
    print(df.shape)

    df['prct_change'] = 100*(df.spx_close-df.spx_open)/df.spx_open

    # https://www.tastylive.com/concepts-strategies/implied-volatility-rank-percentile
    def iv_rank(w):
        return 100* ( w.iloc[-1] - np.min(w) ) / (np.max(w)-np.min(w))

    df['iv_rank'] =df.vix_open.rolling(252).apply(iv_rank)
    df.to_csv(csv_file,index=False)

def verify_jiajun_lox_vix_daily_low_vol():
    df = pd.read_csv(csv_file)
    df.tstamp = df.tstamp.apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d'))
    min_tstamp = df.tstamp.min().strftime('%Y-%m-%d')
    max_tstamp = df.tstamp.max().strftime('%Y-%m-%d')

    print(min_tstamp,max_tstamp)

    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(2,1,1)

    # palette = sns.color_palette("bwr", as_cmap=True) # red is vol spike
    # sns.scatterplot(df,x='vix_open',y='prct_change',palette=palette,markers='+',
    #     hue='prior_day_vix_prct_change',hue_norm=(-0.5,0.5),alpha=0.5,size=1,ax=ax,legend=False)

    #sns.scatterplot(df,x='vix_open',y='prct_change',alpha=0.1,size=0.2,ax=ax,markers=['+']*len(df))
    plt.scatter(df.vix_open,df.prct_change,s=0.1,alpha=0.7,marker='.')
    ax.set_yscale('symlog')
    plt.xlabel('vix open price')
    plt.ylabel('spx daily prct change')
    plt.title(f"n={len(df)}, {min_tstamp} to {max_tstamp}")
    plt.grid(True)

    ax = fig.add_subplot(2,1,2)
    #sns.scatterplot(df,x='iv_rank',y='prct_change',alpha=0.5,size=0.2,ax=ax)
    plt.scatter(df.iv_rank,df.prct_change,s=0.1,alpha=0.7,marker='.')
    ax.set_yscale('symlog')
    plt.xlabel('IV rank')
    plt.ylabel('spx daily prct change')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("tmp/1-prct_change-vs-iv.png")
    plt.close()

    fig = plt.figure()
    plt.subplot(311)
    plt.plot(df.tstamp,df.spx_close)
    plt.title("SPX")
    plt.grid(True)
    plt.subplot(312)
    plt.plot(df.tstamp,df.vix_close)
    plt.title("VIX")
    plt.grid(True)
    plt.subplot(313)
    plt.plot(df.tstamp,df.iv_rank)
    plt.title("IV rank")
    plt.grid(True)
    plt.savefig("tmp/0-validation.png")
    plt.close()

def main():
    if not os.path.exists(csv_file):
        merge_df()
    verify_jiajun_lox_vix_daily_low_vol()


if __name__ == "__main__":
    main()
