import logging
import sys
import time
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


# Algorithm 
    
#while True:
#    tick = wss.tickers['BTCUSD']
#    if tick:
#        bitfinex_bid = tick[0][0]
#        bitfinex_ask = tick[0][2]
#        exchange = [bifinex_bid, bitfinex_ask]

#    time.sleep(1)

