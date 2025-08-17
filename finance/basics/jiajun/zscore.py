import os
import sys
import json
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf

from low_vix_daily_low_vol import prepare,csv_file

def foobar(regime):
    json_file = 'static/expiration-dates.json'
    with open(json_file,'r') as f:
        expiration_list = json.loads(f.read())
        expiration_list = [datetime.datetime.strptime(x,'%Y-%m-%d') for x in expiration_list]

    df = pd.read_csv(csv_file)
    df.tstamp = df.tstamp.apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d'))

    # regime emprically set based on volume (assuming volume is number of contracts traded)
    if regime == 'all':
        pass
    elif regime == 'le2008':
        df = df[df.tstamp.apply(lambda x:x.year <= 2008)]
        expiration_list = [x for x in expiration_list if x.year <= 2008]
    elif regime == 'gt2008lt2020':
        df = df[df.tstamp.apply(lambda x: (x.year > 2008)&(x.year < 2020))]
        expiration_list = [x for x in expiration_list if (x.year > 2008)&(x.year < 2020)]
    elif regime == 'ge2020':
        df = df[df.tstamp.apply(lambda x:x.year >= 2020)]
        expiration_list = [x for x in expiration_list if x.year >= 2020]
    else:
        raise NotImplementedError()

    min_tstamp = df.tstamp.min().strftime('%Y-%m-%d')
    max_tstamp = df.tstamp.max().strftime('%Y-%m-%d')
    plt.close()

    fig = plt.figure(figsize=(15,15))
    plt.subplot(511)
    plt.plot(df.tstamp,df.spx_open)
    plt.ylabel('spx_open')
    plt.grid(True)

    plt.subplot(512)
    plt.plot(df.tstamp,df.spx_volume)
    plt.ylabel('spx_volume')
    plt.grid(True)

    plt.scatter(expiration_list,[0.5*1e10]*len(expiration_list),color='blue',alpha=0.5)
    plt.xlabel('(vix expirations in blue)')

    
    plt.subplot(513)
    plt.plot(df.tstamp,df.volume_z_score)
    plt.axhline(0,color='red')
    plt.ylabel('volume_z_score')
    plt.grid(True)

    plt.scatter(expiration_list,[1]*len(expiration_list),color='blue')
    plt.xlabel('(vix expirations in blue)')

    
    plt.subplot(514)
    plt.plot(df.tstamp,df.vix_open)
    plt.ylabel('vix_open')
    plt.grid(True)

    plt.scatter(expiration_list,[20]*len(expiration_list),color='blue',alpha=0.5)
    plt.xlabel('(vix expirations in blue)')

    plt.subplot(515)
    plt.plot(df.tstamp,df.vix_z_score)
    plt.axhline(0,color='red')
    plt.ylabel('vix_z_score')
    plt.grid(True)

    plt.scatter(expiration_list,[1]*len(expiration_list),color='blue')
    plt.xlabel('(vix expirations in blue)')

    plt.tight_layout()
    plt.savefig(f"tmp/3-zscore-{regime}.png")
    plt.close()

    plt.scatter(df.vix_z_score,df.volume_z_score,s=1,alpha=1,marker='.')
    plt.xlabel('vix_z_score')
    plt.ylabel('volume_z_score')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"tmp/4-iv-zscore-vs-volume-zscore-{regime}.png")
    plt.close()

    plt.scatter(df.vix_open,df.volume_z_score,s=1,alpha=1,marker='.')
    plt.xlabel('vix_open')
    plt.ylabel('volume_z_score')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"tmp/5-viz-vs-volume-zscore-{regime}.png")
    plt.close()

    df['yesterday_volume_z_score'] = df.volume_z_score.shift()
    plt.scatter(df.yesterday_volume_z_score,df.prct_change,s=1,alpha=1,marker='.')
    plt.xlabel("yesterdays volume_z_score (window=252days)")
    plt.ylabel('spx prct_change')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"tmp/6-prior-day-zscore-volume-with-price-change-{regime}.png")
    plt.close()

    plt.scatter(df.vix_open,df.yesterday_volume_z_score,s=1,alpha=1,marker='.')
    plt.xlabel('vix_open')
    plt.ylabel("yesterdays volume_z_score (window=252days)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"tmp/7-prior-day-zscore-volume-with-vix-open-{regime}.png")
    plt.close()


    markers = {'.':'.'}
    df['sz']=0.1
    df['style']='.'
    sns.scatterplot(df,x='vix_open',y='prct_change',hue='yesterday_volume_z_score',
        sizes='sz',style="style",markers=markers,
        alpha=0.7,palette='RdYlGn',
    )
    plt.xlabel('vix_open')
    plt.ylabel('prct_change')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"tmp/7.1-prct_change-vix_open-yesterday-volume-zscore-{regime}.png")
    plt.close()



    # https://www.statsmodels.org/stable/examples/notebooks/generated/mixed_lm_example.html
    # https://www.statsmodels.org/stable/examples/notebooks/generated/ols.html
    # https://statistiknachhilfe.ch/en/2024/02/27/linear-mixed-models-vs-ols-modelle-ein-vergleich-und-leitfaden-zur-auswahl/
    """
    OLS models are best suited for exploratory analyses in data sets where all observations are assumed to be independent and identically distributed.
    LMMs are the better choice when the data structure is complex, for example with repeated measures, nested data or when the independence of observations is violated.
    ... They (LMMs) provide a nuanced analysis of the data that takes into account the inherent group structure and potential correlation within groups.
    """
    df["abs_prct_change"] = df.prct_change.abs()
    df = df.dropna()
    model = sm.OLS(df["abs_prct_change"],df[['vix_open','yesterday_volume_z_score']])
    results = model.fit()
    print(results.summary())

    # md = smf.mixedlm("abs_prct_change ~ vix_open + yesterday_volume_z_score ", df, groups=df["Pig"])
    # mdf = md.fit(method=["lbfgs"])
    # print(mdf.summary())

def main():
    if not os.path.exists(csv_file):
        prepare()
    #for regime in ['all','le2008','gt2008lt2020','ge2020']:
    for regime in ['all','ge2020']:
        print(f'-----------------------period:{regime}-------------------------')
        foobar(regime)

if __name__ == "__main__":
    main()
