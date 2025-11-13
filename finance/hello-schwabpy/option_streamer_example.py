from schwab.auth import easy_client, client_from_manual_flow, client_from_token_file
from schwab.client import Client
from schwab.streaming import StreamClient

import os
import sys
import asyncio
import json


# # Assumes you've already created a token. See the authentication page for more
# # information.

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


from schwab.orders.options import OptionSymbol
import datetime

ticker = 'TSLA'
symbol1 = OptionSymbol(ticker, datetime.date(year=2025, month=11, day=21), 'P', '430').build()
print(symbol1)
ticker = 'SPXW'
symbol2 = OptionSymbol(ticker, datetime.date(year=2025, month=11, day=21), 'P', '6850').build()
print(symbol2)

symbol_list = [symbol1,symbol2]

from_date = datetime.date(2025, 11, 13)
to_date = datetime.date(2025, 11, 15)

response = client.get_option_chain("$SPX",
    strike_count=200,
    include_underlying_quote='true',
    from_date=from_date,
    to_date=to_date)

if response.status_code != 200:
    print(response.status_code)
    sys.exit(1)
else:
    output_dict = response.json()
    with open('ok.json','w') as f:
        f.write(json.dumps(output_dict))

last_price = output_dict["underlying"]["last"]
symbol_list = []
for epiration,itemdict in output_dict["callExpDateMap"].items():
    print(epiration)
    for strike,itemlist in itemdict.items():
        for item in itemlist:
            if False:
                print(item["symbol"],item["volatility"],item["gamma"],item["last"])
            symbol_list.append(item["symbol"])

print(symbol_list[-1])
print(len(symbol_list))
symbol_list = symbol_list[:100]
print(len(symbol_list))
# API only allows you to subscribe to 100 symbols. sux.

account_id = int(os.environ['ACCOUNTID'])
stream_client = StreamClient(client, account_id=account_id)

async def read_stream():
    await stream_client.login()

    def print_message(message):
      print(json.dumps(message, indent=4))


    # Always add handlers before subscribing because many streams start sending
    # data immediately after success, and messages with no handlers are dropped.

    stream_client.add_level_one_option_handler(print_message)
    await stream_client.level_one_option_subs(symbol_list)

    stream_client.add_options_book_handler(print_message)
    await stream_client.options_book_subs(symbol_list)

    while True:
        await stream_client.handle_message()

if __name__ == "__main__":
    asyncio.run(read_stream())