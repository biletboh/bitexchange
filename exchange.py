import logging
import sys
import time
import requests
import json
import base64
import hashlib
import hmac
import os
import configparser

from btfxwss import BtfxWss
from bitfinex.client import TradeClient

# Set up configuration 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
conf = configparser.ConfigParser()
conf.read(os.path.join(BASE_DIR, 'settings.ini'))

# API keys
client_api = conf.get('bitexchange', 'API_KEY')
client_secret = conf.get('bitexchange', 'API_SECRET')


# Set up Trade Client
tradeclient = TradeClient(client_api, client_secret)

# Set up Bitfinex websocket

logging.basicConfig(level=logging.DEBUG, filename='bfx_websocket.log')
log = logging.getLogger(__name__)

fh = logging.FileHandler('bfx_websocket.log')
fh.setLevel(logging.DEBUG)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)

log.addHandler(sh)
log.addHandler(fh)

wss = BtfxWss(key=client_api, secret=client_secret)
wss.start()
time.sleep(1)  # Give the client some prep time to set itself up
    
# Subscribe to ticker channel 
wss.ticker('BTCUSD')
    
# Send a ping - if this returns silently, everything's fine
wss.ping()


def compare_exchange(bitfinex, exch2):
    """ Compare exchange rates at bitfinex and ___
    Buy bitcoins at the exchange with lower rates.
    Sell bitcoins at the exchange with higher rates.
    """
    
    # Check if the difference between rates is higher than 1.5% 
    if (float(bitfinex[1])-float(exch2[0]))*100/float(bitfinex[1]) > 1.5:

        # Deposit USD funds to bitfinex
        print('deposit funds to USD account')

        # Buy bitcoins at bitfinex
        print('buy at exchange2')
        
        # Deposit bitcoins to bitfinex
        deposit_btc = tradeclient.deposit_btc('bitcoin', 'exchange')

        # Sell bitcoins at bitfinex
        place_order = tradeclient.place_order('1', str(bitfinex[1]), 'sell', 'exchange market')

        # Withdraw funds from USD account when an order is done 
        while True:

            if isinstance(place_order, str):  # Check for error messages
                print('Error Message: ', place_order)
            else:
                order_id=place_order['order_id']

            try:
                status_order = tradeclient.status_order(order_id)
            except:
                print('Provide valid order id for a withdrawal')
                break

            if status_order['remaining_amount'] == 0:
                if bank_account_number:
                    withdraw_usd = tradeclient.withdraw_usd('bitcoin', 'exchange', '1', bank_account_number, bank_name, bank_address, bank_city, bank_country)
                    break
                else:
                    print('Set up bank account detail for USD withdrawal')  
                    break
                time.sleep(1)

    elif (float(exch2[1])-float(bitfinex[0]))*100/float(exch2[1]) > 1.5:

        # Deposit USD funds to bitfinex
        print('Deposit funds to USD account')  # Wire deposits at Bitinex have been paused. 

        # Buy bitcoins at bitfinex
        place_order = tradeclient.place_order('1', str(bitfinex[1]), 'buy', 'exchange market')

        # Deposit bitcoins to __ 
        print('deposit bitcoins to __')

        # Sell bitcoins at __ 
        print('sell at __')

        # Withdraw funds from USD account when an order is done 
        print('withdraw funds')

    else:
        print('Exchange rate difference is lower than 1.5%')
        pass


# Tests

# first exchange is cheaper than second
bitfinex = [2000, 2010]
bitstamp = [2300, 2310]

#print('first test')
compare_exchange(bitfinex, bitstamp)

# second exchange is cheaper than first
bitfinex = [2300, 2310]
bitstamp = [2000, 2010]

#print('second test')
compare_exchange(bitfinex, bitstamp)

# an exchange difference is below 1.5% 
bitfinex = [2000, 2010]
bitstamp = [2020, 2030]

#print('third test')
compare_exchange(bitfinex, bitstamp)

# Algorithm 
    
#while True:
#    tick = wss.tickers['BTCUSD']
#    if tick:
#        bitfinex_bid = tick[0][0]
#        bitfinex_ask = tick[0][2]
#        exchange = [bifinex_bid, bitfinex_ask]

#    time.sleep(1)

