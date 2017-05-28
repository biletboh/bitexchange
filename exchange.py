import logging
import sys
import time
from btfxwss import BtfxWss

logging.basicConfig(level=logging.DEBUG, filename='test.log')
log = logging.getLogger(__name__)

fh = logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)

log.addHandler(sh)
log.addHandler(fh)
    
wss = BtfxWss(key='5CnSpKOMYC7bKwy6SgINaxtKjqlLmmlQC2ch2HB6Nck', secret='3rfRtXQ7mltimnBRt8pc9SqnbRlHk10r6OBErl3zGKZ')
wss.start()
time.sleep(1)  # give the client some prep time to set itself up.
    
# Subscribe to some channels
wss.ticker('BTCUSD')
wss.order_book('BTCUSD')
    
# Send a ping - if this returns silently, everything's fine.
wss.ping()
    
# Do something else
t = time.time()

while True:
    tick = wss.tickers['BTCUSD']
    time.sleep(1)
    if tick:
        bid = tick[0][0]
        ask = tick[0][2]
        print(bid, ask)
