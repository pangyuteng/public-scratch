from schwab.auth import easy_client, client_from_manual_flow, client_from_token_file
from schwab.client import Client
from schwab.streaming import StreamClient

import os
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

account_id = int(os.environ['ACCOUNTID'])
print(account_id,type(account_id))
stream_client = StreamClient(client, account_id=account_id)

async def read_stream():
    await stream_client.login()

    def print_message(message):
      print(json.dumps(message, indent=4))

    # Always add handlers before subscribing because many streams start sending
    # data immediately after success, and messages with no handlers are dropped.
    stream_client.add_nasdaq_book_handler(print_message)
    await stream_client.nasdaq_book_subs(['GOOG'])

    while True:
        await stream_client.handle_message()

asyncio.run(read_stream())