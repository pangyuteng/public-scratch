import os
import sys
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


csv_file = "tmp/history.csv"

def prepare():

    # Date,Open,High,Low,Close,Volume,Dividends,Stock Splits
    # 1927-12-30 00:00:00-05:00,17.65999984741211,17.65999984741211,17.65999984741211,17.65999984741211,0,0.0,0.0

    spx_df = pd.read_csv("tmp/SPX.csv")
    
    spx_df['tstamp'] = spx_df.Date.apply(lambda x: datetime.datetime.strptime(x.split(" ")[0],"%Y-%m-%d"))
    spx_df = spx_df.rename(columns={"Open":"spx_open","High":"spx_high","Low":"spx_low","Close":"spx_close","Volume":"spx_volume"})
    cols = ['tstamp','spx_open','spx_high','spx_low','spx_close','spx_volume']
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

    # https://en.wikipedia.org/wiki/Standard_score
    def z_score(w):
        return ( w.iloc[-1] - np.mean(w) ) / np.std(w)
    df['iv_z_score'] =df.vix_open.rolling(252).apply(z_score)
    df['volume_z_score'] =df.spx_volume.rolling(252).apply(z_score)
    df.to_csv(csv_file,index=False)

# ref jiajun's spx research 
# https://www.tastylive.com/news-insights/vix-explosion-2024-insights-market-impact

def verify_low_vix_daily_low_vol(regime):

    df = pd.read_csv(csv_file)
    df.tstamp = df.tstamp.apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d'))
    
    # regime emprically set based on volume (assuming volume is number of contracts traded)
    if regime == 'all':
        pass
    elif regime >= 'le2008':
        df = df[df.tstamp.apply(lambda x:x.year <= 2008)]
    elif regime >= 'gt2008lt2020':
        df = df[df.tstamp.apply(lambda x: (x.year > 2008)&(x.year < 2020))]
    elif regime >= 'ge2020':
        df = df[df.tstamp.apply(lambda x:x.year >= 2020)]

    min_tstamp = df.tstamp.min().strftime('%Y-%m-%d')
    max_tstamp = df.tstamp.max().strftime('%Y-%m-%d')

    print(min_tstamp,max_tstamp)

    fig = plt.figure(figsize=(7,7))
    ax = fig.add_subplot(2,1,1)

    # palette = sns.color_palette("bwr", as_cmap=True) # red is vol spike
    # sns.scatterplot(df,x='vix_open',y='prct_change',palette=palette,markers='+',
    #     hue='prior_day_vix_prct_change',hue_norm=(-0.5,0.5),alpha=0.5,size=1,ax=ax,legend=False)

    markers = {'.':'.'}
    df['sz']=10
    df['style']='.'
    sns.scatterplot(df,x='vix_open',y='prct_change',sizes='sz',style="style", markers=markers,
        alpha=0.1,ax=ax,legend=False)
    #plt.scatter(df.vix_open,df.prct_change,s=0.1,alpha=0.7,marker='.')
    ax.set_yscale('symlog')
    plt.xlabel('vix open price')
    plt.ylabel('spx daily prct change')
    plt.title(f"n={len(df)}, {min_tstamp} to {max_tstamp}")
    plt.grid(True)

    ax = fig.add_subplot(2,1,2)
    sns.scatterplot(df,x='iv_rank',y='prct_change',sizes='sz',style="style", markers=markers,
        alpha=0.1,ax=ax,legend=False)
    ax.set_yscale('symlog')
    plt.xlabel('IV rank')
    plt.ylabel('spx daily prct change')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(f"tmp/1-prct_change-vs-iv-{regime}.png")
    plt.close()

    fig = plt.figure()
    plt.subplot(411)
    plt.plot(df.tstamp,df.spx_close)
    plt.ylabel("SPX")
    plt.grid(True)
    plt.subplot(412)
    plt.plot(df.tstamp,df.vix_close)
    plt.ylabel("VIX")
    plt.grid(True)
    plt.subplot(413)
    plt.plot(df.tstamp,df.iv_rank)
    plt.ylabel("IV rank")
    plt.grid(True)
    plt.subplot(414)
    plt.plot(df.tstamp,df.spx_volume)
    plt.ylabel("spx volume")
    plt.grid(True)

    plt.savefig(f"tmp/0-validation-{regime}.png")
    plt.close()



def verify_low_vix_daily_low_vol_heatmap(regime):

    df = pd.read_csv(csv_file)
    df.tstamp = df.tstamp.apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d'))
    
    # regime emprically set based on volume (assuming volume is number of contracts traded)
    if regime == 'all':
        pass
    elif regime == 'le2008':
        df = df[df.tstamp.apply(lambda x:x.year <= 2008)]
    elif regime == 'gt2008lt2020':
        df = df[df.tstamp.apply(lambda x: (x.year > 2008)&(x.year < 2020))]
    elif regime == 'ge2020':
        df = df[df.tstamp.apply(lambda x:x.year >= 2020)]
    else:
        raise NotImplementedError()
    min_tstamp = df.tstamp.min().strftime('%Y-%m-%d')
    max_tstamp = df.tstamp.max().strftime('%Y-%m-%d')

    print(min_tstamp,max_tstamp)

    fig = plt.figure(figsize=(7,5))
    ax = fig.add_subplot(1,1,1)

    sns.histplot(
        df, x="vix_open", y="prct_change",
        bins=[50,200], discrete=(False, False), log_scale=(False, False),
        binrange=[(0,50),(-3,3)],
        ax=ax,legend=False,cbar=True, cbar_kws=dict(shrink=.75),
    )

    plt.xlabel('vix open price')
    plt.ylabel('spx daily prct change')
    plt.title(f"n={len(df)}, {min_tstamp} to {max_tstamp}")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(f"tmp/2-heatmap-prct_change-vs-iv-{regime}.png")
    plt.close()

def main():
    if not os.path.exists(csv_file):
        prepare()

    for regime in ['all','le2008','gt2008lt2020','ge2020']:
        verify_low_vix_daily_low_vol(regime)
        verify_low_vix_daily_low_vol_heatmap(regime)


if __name__ == "__main__":
    main()
