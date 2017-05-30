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
exmo_api = conf.get('bitexchange', 'EXMO_API_KEY')
exmo_secret = conf.get('bitexchange', 'EXMO_API_SECRET')

# Set up Exmo Trade Client
tradeclient2 = ExmoTradeClient(exmo_api, exmo_secret)

# Simple Tests
print("Run exmoclient methods simple tests")

# Test 1
print('Test 1:')
print(tradeclient2.place_order('BTC_USD', 1, 2000, 'buy'))


# Test 2
print('Test 2:')
print(tradeclient2.trade_deals('BTC_USD', 1))

# Test 3
print('Test 3:')
print(tradeclient2.deposit_usd())

# Test 4
print('Test 4:')
print(tradeclient2.deposit_btc())

# Test 5
print('Test 5:')
print(tradeclient2.withdraw_crypto(1, 'BTC', 'af82hfhp2hpSDFKHUIEH'))

# Test 6
print('Test 6:')
print(tradeclient2.withdraw_usd())


