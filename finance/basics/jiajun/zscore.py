import os
import sys
import json
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    plt.plot(df.tstamp,df.spx_close)
    plt.ylabel('spx_close')
    plt.grid(True)
    plt.subplot(512)
    plt.plot(df.tstamp,df.spx_volume)
    plt.ylabel('spx_volume')    
    plt.grid(True)
    plt.subplot(513)
    plt.plot(df.tstamp,df.volume_z_score)
    plt.axhline(0,color='red')
    plt.ylabel('volume_z_score')
    plt.grid(True)
    
    plt.scatter(expiration_list,[200]*len(expiration_list),color='blue')
    plt.xlabel('(vix expirations in blue)')
    
    plt.subplot(514)
    plt.plot(df.tstamp,df.vix_close)
    plt.ylabel('vix_close')
    plt.grid(True)
    plt.subplot(515)
    plt.plot(df.tstamp,df.iv_z_score)
    plt.axhline(0,color='red')
    plt.ylabel('iv_z_score')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(f"tmp/3-zscore-{regime}.png")
    plt.close()

    plt.scatter(df.iv_z_score,df.volume_z_score,s=1,alpha=1,marker='.')
    plt.xlabel('iv_z_score')
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
    plt.savefig(f"tmp/6-zscore-volume-with-price-change-{regime}.png")
    plt.close()

def main():
    if not os.path.exists(csv_file):
        prepare()
    for regime in ['all','le2008','gt2008lt2020','ge2020']:
        foobar(regime)


if __name__ == "__main__":
    main()
