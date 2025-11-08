import os
import httpx
from schwab.auth import client_from_manual_flow, client_from_token_file

"""
ACCOUNTID=xxx
APIKEY=xxx
APISECRET=xxx
CALLBACKURL=https://127.0.0.1:8182
TOKENPATH=/tmp/token.json
"""


if os.path.exists(os.environ['TOKENPATH']):
    print('loading client from token file')
    client = client_from_token_file(
        os.environ['TOKENPATH'],os.environ['APIKEY'],os.environ['APISECRET'],
    )
else:
    client = client_from_manual_flow(
        api_key=os.environ['APIKEY'],
        app_secret=os.environ['APISECRET'],
        callback_url=os.environ['CALLBACKURL'],
        token_path=os.environ['TOKENPATH']
    )

resp = client.get_price_history_every_day('AAPL')
assert resp.status_code == httpx.codes.OK
history = resp.json()
print(history)


"""

ssh -L 8182:127.0.0.1:8182 gtx

docker run -it --env-file=.env -w $PWD -v /mnt:/mnt \
-p 8182:8182 schwabpy bash


"""