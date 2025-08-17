import warnings
import os
import sys
import json
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

from low_vix_daily_low_vol import prepare,csv_file

def main(regime):
    if not os.path.exists(csv_file):
        prepare()

    df = pd.read_csv(csv_file)
    df.tstamp = df.tstamp.apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d'))

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

    def intraday_vix_std(row):
        return np.std([row.vix_open,row.vix_high,row.vix_low,row.vix_close])

    def intraday_spx_std(row):
        return np.std([row.spx_open,row.spx_high,row.spx_low,row.spx_close])

    df['intraday_vix_std'] = df.apply(intraday_vix_std,axis=1)
    df['intraday_spx_std'] = df.apply(intraday_spx_std,axis=1)

    fig = plt.figure(figsize=(7,7))
    ax = fig.add_subplot(1,1,1)

    plt.scatter(df.prct_change,df.intraday_vix_std,s=1,alpha=1,marker='.')
    plt.xlabel('prct_change')
    plt.ylabel("intraday_vix_std")
    ax.set_xscale('symlog')
    ax.set_yscale('log')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"tmp/8-prct_change-vs-intraday_vix_std-{regime}.png")
    plt.close()


    plt.scatter(df.intraday_spx_std,df.intraday_vix_std,s=1,alpha=1,marker='.')
    plt.xlabel('intraday_spx_std')
    plt.ylabel("intraday_vix_std")
    ax.set_xscale('symlog')
    ax.set_yscale('log')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"tmp/9-intraday_spx_std-vs-intraday_vix_std-{regime}.png")
    plt.close()


    # ... squeeze more from ohlc
    """
    rate ohlc relative to high,low
    no need to compre with close
    or abs since we will have prct_change on y axis
    """
    def category_via_ohlc(row):
        rowclass = ''
        if row.spx_close <= row.spx_low:
            rowclass+='closeislow.'
        if row.spx_close >= row.spx_high:
            rowclass+='closeishigh.'
        if row.spx_open >= row.spx_high:
            rowclass+='openishigh.'
        if row.spx_open <= row.spx_low:
            rowclass+='openislow.'
        if rowclass == '':
            rowclass = 'na'
        return rowclass        

    df['category_via_ohlc'] = df.apply(category_via_ohlc,axis=1)

    markers = {'.':'.'}
    df['sz']=0.1
    df['style']='.'
    
    sns.scatterplot(df,x='vix_open',y='prct_change',
        hue="category_via_ohlc",
        sizes='sz',style="style",markers=markers,
        alpha=0.5,legend=True)

    title="""
    
    during down days (prct change < 0), 
    open will mark the low of the day (`---+-` red)
    while during up days,
    rarely will close mark the high (`++---` green)

    """
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"tmp/10-ohlc-{regime}.png")
    plt.close()
    


    # with above, you can infer prior day net negative and positive gamma

    # openishigh and prct_change < 0 : negative gamma
    # closeislow and prct_change < 0 : negative gamma

    # closeishigh and prct_change > 0 : positive gamma
    # openislow and prct_change > 0 : positive gamma


    def guess_net_gamma_exposure(row):
        rowclass = 0
        if row.prct_change > 0:
            if row.spx_open==row.spx_low:
                rowclass = 1
            if row.spx_close==row.spx_high:
                rowclass = 2
        else:
            if row.spx_open==row.spx_high:
                rowclass = -1
            if row.spx_close==row.spx_low:
                rowclass = -2
        return rowclass

    df['net_gex'] = df.apply(guess_net_gamma_exposure,axis=1)

    plt.scatter(df.vix_open,df.prct_change,s=1,alpha=0.1,marker='.',color='black')
    print(df.shape)
    print(df[df.net_gex==1].shape)
    print(df[df.net_gex==-1].shape)
    plt.scatter(df[df.net_gex==1].vix_open,df[df.net_gex==1].prct_change,s=0.1,alpha=1,color='green')
    plt.scatter(df[df.net_gex==2].vix_open,df[df.net_gex==2].prct_change,s=0.1,alpha=1,color='blue')
    plt.scatter(df[df.net_gex==-1].vix_open,df[df.net_gex==-1].prct_change,s=0.1,alpha=1,color='red')
    plt.scatter(df[df.net_gex==-2].vix_open,df[df.net_gex==-2].prct_change,s=0.1,alpha=1,color='purple')
    plt.xlabel('vix_open')
    plt.ylabel('prct_change')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"tmp/10-ohlc-again-{regime}.png")
    plt.close()



    df['yesterday_net_gex'] = df.net_gex.shift()
    df = df.dropna()
    plt.scatter(df.vix_open,df.prct_change,s=1,alpha=0.1,marker='.',color='black')
    plt.scatter(df[df.yesterday_net_gex==1].vix_open,df[df.yesterday_net_gex==1].prct_change,s=0.1,alpha=1,color='green')
    plt.scatter(df[df.yesterday_net_gex==-1].vix_open,df[df.yesterday_net_gex==-1].prct_change,s=0.1,alpha=1,color='red')

    plt.xlabel("vix_open")
    plt.ylabel('spx prct_change')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"tmp/11-prior-day-guess-gex-{regime}.png")
    plt.close()

    # https://www.statsmodels.org/stable/examples/notebooks/generated/mixed_lm_example.html
    # https://www.statsmodels.org/stable/examples/notebooks/generated/ols.html

    model = sm.OLS(df["prct_change"],df[['yesterday_net_gex']])
    results = model.fit()
    print(results.summary())

    df["abs_prct_change"] = df.prct_change.abs()
    model = sm.OLS(df["abs_prct_change"],df[['yesterday_net_gex']])
    results = model.fit()
    print(results.summary())


todos = """

can we classify daily data to below using only OHLC SPX and VIX?

+ up only days

+ up and down super volatile via vix ohlc

+ down only days 

+ other days

"""

warnings.warn(f"TODOS:{todos}")

if __name__ == "__main__":
    
    #for regime in ['all','le2008','gt2008lt2020','ge2020']:
    for regime in ['all','ge2020']:
        print(f'-----------------------period:{regime}-------------------------')
        main(regime)
