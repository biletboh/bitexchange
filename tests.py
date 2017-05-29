import time
import os
import configparser

from bitfinex.client import TradeClient

from compare import compare_exchange

# Set up configuration 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
conf = configparser.ConfigParser()
conf.read(os.path.join(BASE_DIR, 'settings.ini'))

# API keys
client_api = conf.get('bitexchange', 'API_KEY')
client_secret = conf.get('bitexchange', 'API_SECRET')


# Set up Trade Client
tradeclient = TradeClient(client_api, client_secret)


# Simple Tests
print("Run simple tests")

# first exchange is cheaper than second
bitfinex = [2000, 2010]  # data is in a format [bid, ask]
bitstamp = [2300, 2310]

print('Test 1:')
compare_exchange(tradeclient, bitfinex, bitstamp)

# second exchange is cheaper than first
bitfinex = [2300, 2310]
bitstamp = [2000, 2010]

print('Test 2:')
compare_exchange(tradeclient, bitfinex, bitstamp)

# an exchange difference is below 1.5% 
bitfinex = [2000, 2010]
bitstamp = [2020, 2030]

print('Test 3:')
compare_exchange(tradeclient, bitfinex, bitstamp)

