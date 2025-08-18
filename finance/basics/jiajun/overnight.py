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

def main():
    if not os.path.exists(csv_file):
        prepare()

    vix_mylist = []
    spx_mylist = []
    #for regime in ['all','le2008','gt2008lt2020','ge2020']:
    for regime in ['all','ge2020']:

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

        df['yesterday_spx_close'] = df.spx_close.shift()
        df['yesterday_vix_close'] = df.vix_close.shift()
        df = df.dropna()

        df['yesterday_spx_close_to_spx_open_prct_change'] = ( df.spx_open - df.yesterday_spx_close ) / (df.yesterday_spx_close)
        df['spx_close_to_spx_open_prct_change'] = ( df.spx_close - df.spx_open ) / (df.spx_open)

        df['yesterday_vix_close_to_vix_open_prct_change'] = ( df.vix_open - df.yesterday_vix_close ) / (df.yesterday_vix_close)
        df['vix_close_to_vix_open_prct_change'] = ( df.vix_close - df.vix_open ) / (df.vix_open)



        df1 = pd.DataFrame([])
        df1['prct_change'] = df.yesterday_vix_close_to_vix_open_prct_change
        df1['class'] = "yesterday_vix_close_to_vix_open"

        df2 = pd.DataFrame([])
        df2['prct_change'] = df.vix_close_to_vix_open_prct_change
        df2['class'] = "today_vix_close_to_today_vix_open"

        row_df = pd.concat([df1,df2])
        row_df['regime'] = regime
        vix_mylist.append(row_df)

        df1 = pd.DataFrame([])
        df1['prct_change'] = df.yesterday_spx_close_to_spx_open_prct_change
        df1['class'] = "yesterday_spx_close_to_spx_open"

        df2 = pd.DataFrame([])
        df2['prct_change'] = df.spx_close_to_spx_open_prct_change
        df2['class'] = "spx_close_to_spx_open"

        row_df = pd.concat([df1,df2])
        row_df['regime'] = regime
        spx_mylist.append(row_df)


    vix_mdf = pd.concat(vix_mylist)
    spx_mdf = pd.concat(spx_mylist)
    
    plt.subplot(211)
    plt.title("spx prior night versus today change")
    ax = sns.violinplot(data=spx_mdf, x="regime", y="prct_change", hue='class')
    plt.grid(True)
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    plt.tight_layout()

    plt.subplot(212)
    plt.title("vix prior night versus today change")
    ax = sns.violinplot(data=vix_mdf, x="regime", y="prct_change", hue='class')
    plt.grid(True)
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    plt.tight_layout()

    plt.savefig(f"tmp/12-overnight-{regime}.png")
    plt.close()


if __name__ == "__main__":
    
    main()
