import os
import traceback
import datetime
import awswrangler as wr
import pandas as pd

from plotly.offline import plot
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from flask import Flask, render_template, request, jsonify,url_for

from utils import get_data, sector_list


BUCKET_NAME = os.environ.get("BUCKET_NAME")

def df_s3_dump(df,s3_path):
    s3 = s3fs.S3FileSystem()
    with s3.open(s3_path,'w') as f:
        df.to_csv(f)

def df_s3_load(s3_path):
    return pd.read_csv(s3_path)

app = Flask(__name__,
    static_url_path='', 
    static_folder='static',
    template_folder='templates',
)

@app.route("/ping")
def ping():
    return jsonify(success=True)

@app.route('/finance/overview_div')
def overview_div():
    try:

        roll = int(request.args.get("roll"))
        lookback = int(request.args.get("lookback"))
        if lookback > 0:
            lookback = -1*lookback

        tstamp =  datetime.datetime.now().strftime("%Y-%m-%d")
        cache_csv = f'{tstamp}-lookback{lookback}-roll{roll}.csv'
        s3_path = os.path.join("s3://",BUCKET_NAME,cache_csv)

        try:
            df = wr.s3.read_csv(s3_path)
        except:
            app.logger.info(traceback.format_exc())
            try:
                df = get_data(lookback=lookback,roll=roll)
                if len(df) < 10:
                    raise LookupError("len(df)<10 !")
                wr.s3.to_csv(df,path=s3_path)
            except:
                app.logger.error(traceback.format_exc())
                raise ValueError(traceback.format_exc())

        df = wr.s3.read_csv(s3_path)
        last_date = df.Date.tolist()[-1]
        start_date = df.Date.tolist()[-1]

        btcusd = go.Scatter(
            x=df['Date'][lookback:],
            y=df['BTC-USD'][lookback:],
            mode='lines', name='BTC-USD',
            opacity=0.8, marker_color='orange')

        m2 = go.Scatter(
            x=df['Date'][lookback:],
            y=df['M2SL'][lookback:],
            mode='lines', name='M2SL',
            opacity=0.8, marker_color='green')

        spy = go.Scatter(
            x=df['Date'][lookback:],
            y=df['SPY'][lookback:],
            mode='lines', name='SPY',
            opacity=0.8, marker_color='blue')

        qqq = go.Scatter(
            x=df['Date'][lookback:],
            y=df['QQQ'][lookback:],
            mode='lines', name='QQQ',
            opacity=0.8, marker_color='cyan')

        vix = go.Scatter(
            x=df['Date'][lookback:],
            y=df['^VIX'][lookback:],
            mode='lines', name='^VIX',
            opacity=0.8, marker_color='purple')

        yield_diff = go.Scatter(
            x=df['Date'][lookback:],
            y=(df['^TNX']-df['^IRX'])[lookback:],
            mode='lines', name='^TNX-^IRX',
            opacity=0.8, marker_color='red')

        corr_to_spy_list = []
        for x in sector_list:
            item = go.Scatter(
                x=df['Date'][lookback:],
                y=df[f'{x}_corr'][lookback:],
                mode='lines', name=f'corr({x},SPY)',
                opacity=0.8)
            corr_to_spy_list.append(item)

        fig = make_subplots(
            rows=6, cols=1, shared_xaxes=True, 
            vertical_spacing=0.02
        )

        fig.add_trace(btcusd,row=1, col=1)

        fig.add_trace(m2,row=2, col=1)

        fig.add_trace(spy,row=3, col=1)
        fig.add_trace(qqq,row=3, col=1)

        fig.add_trace(vix,row=4, col=1)

        fig.add_trace(yield_diff,row=5, col=1)

        for x in corr_to_spy_list:
            fig.add_trace(x,row=6, col=1)

        # NOTE: leave out height and width, let browser dictate figure size.
        kwargs = dict(height=960, width=1200, title_text="")
        fig.update_layout()

        fig['layout']['yaxis1'].update(domain=[0.7, 1.0])
        fig['layout']['yaxis2'].update(domain=[0.6, 0.7])
        fig['layout']['yaxis3'].update(domain=[0.5, 0.6])
        fig['layout']['yaxis4'].update(domain=[0.4, 0.5])
        fig['layout']['yaxis5'].update(domain=[0.3, 0.4])
        fig['layout']['yaxis6'].update(domain=[0.0, 0.3])
        fig.update_layout(template='plotly_dark')

        plot_div = plot(fig,output_type='div',include_plotlyjs=False)

        return render_template("overview_div.html",plot_div=plot_div,last_updated_tstamp=tstamp)

    except:
        traceback.print_exc()
        return jsonify({"message":traceback.format_exc()})

@app.route('/finance/overview')
def overview():
    try:
        lookback = int(request.args.get("lookback",0))
        roll = int(request.args.get("roll",200))

        overview_div_url = url_for("overview_div",lookback=lookback,roll=roll)
        return render_template("main.html",
            overview_div_url=overview_div_url,
        )
    except:
        traceback.print_exc()
        return jsonify({"message":traceback.format_exc()})

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")