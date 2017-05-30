import time
import os
import configparser

from bitfinex.client import TradeClient
from exmoclient import ExmoTradeClient

from compare import compare_exchange

# Set up configuration 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
conf = configparser.ConfigParser()
conf.read(os.path.join(BASE_DIR, 'settings.ini'))

# Get API keys
bitfinex_api = conf.get('bitexchange', 'BITFINEX_API_KEY')
bitfinex_secret = conf.get('bitexchange', 'BITFINEX_API_SECRET')
exmo_api = conf.get('bitexchange', 'EXMO_API_KEY')
exmo_secret = conf.get('bitexchange', 'EXMO_API_SECRET')


# Set up bitfinex Trade Client
tradeclient = TradeClient(bitfinex_api, bitfinex_secret)

# Set up Exmo Trade Client
tradeclient2 = ExmoTradeClient(exmo_api, exmo_secret)

# Simple Tests
print("Run compare algorithm simple tests")

# second exchange is cheaper than first
bitfinex_data = [2300, 2310]
exmo_data = [2000, 2010]

print('Test 1:')
compare_exchange(tradeclient, tradeclient2, bitfinex_data, exmo_data)

# first exchange is cheaper than second
bitfinex_data = [2000, 2010]  # data is in a format [bid, ask]
exmo_data = [2300, 2310]

print('Test 2:')
compare_exchange(tradeclient, tradeclient2, bitfinex_data, exmo_data)

# an exchange difference is below 1.5% 
bitfinex_data = [2000, 2010]
exmo_data = [2020, 2030]

print('Test 3:')
compare_exchange(tradeclient, tradeclient2, bitfinex_data, exmo_data)

