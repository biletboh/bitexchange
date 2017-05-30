import logging
import sys
import time
import os
import configparser

from btfxwss import BtfxWss
from bitfinex.client import Client, TradeClient
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

# Set up bitfinex Client
bitfinexclient = Client()

# Set up bitfinex Trade Client
tradeclient = TradeClient(bitfinex_api, bitfinex_secret)

# Set up Exmo Trade Client
tradeclient2 = ExmoTradeClient(exmo_api, exmo_secret)

# Set up Bitfinex websocket

logging.basicConfig(level=logging.DEBUG, filename='bfx_websocket.log')
log = logging.getLogger(__name__)

fh = logging.FileHandler('bfx_websocket.log')
fh.setLevel(logging.DEBUG)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)

log.addHandler(sh)
log.addHandler(fh)

wss = BtfxWss(key=bitfinex_api, secret=bitfinex_secret)
wss.start()
time.sleep(1)  # Give the client some prep time to set itself up
    
# Subscribe to ticker channel 
wss.ticker('BTCUSD')
    
# Send a ping - if this returns silently, everything's fine
wss.ping()


# Algorithm 
    
while True:
    tick = bitfinexclient.ticker('btcusd')
    if tick:
        bitfinex_bid = tick['bid']
        bitfinex_ask = tick['ask']
        data_bitfinex = [bitfinex_bid, bitfinex_ask]
        print('bitfinex', data_bitfinex)
    
    tick2 = tradeclient2.ticker()
    if tick2:
        exmo_bid = tick2['last_trade']
        exmo_ask = tick2['sell_price']
        data_exmo = [exmo_bid, exmo_ask] 
        print('exmo', data_exmo)
    if data_bitfinex and data_exmo:
        compare_exchange(tradeclient, tradeclient2, data_bitfinex, data_exmo)

    time.sleep(1)

