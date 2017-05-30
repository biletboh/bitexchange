## Demo for bitfinex and exmo exchange. 

The package helps to automatically buy bitcoin on the exchange, where it is cheaper and sell it on the exchange, where it is more expensive.

### Running 

0. Set up virtual environment. `conda create --name virtenv python=3.5`
1. Activate virtual environment `source activate virtenv`
2. Install requirements `pip install -r requirements`
3. Create `settings.ini` file with configuration (provide keys without any quotes):

```
[bitexchange]
BITFINEX_API_KEY = your-Bitfinex-api-key 
BITFINEX_API_SECRET = your-Bitfinex-api-secret 
EXMO_API_KEY = your-EXMO-api-key
EXMO_API_SECRET = your-EXMO-api-secret
```

### Usage

Run script `python exchange.py`

### Tests

To test exmo client that access exmo API run `python test_exmoclient.py`

To test compare algorithm that evaluate the best exchange to buy and sell bitcoins run `python test_compare.py`

### Take into the consideration!

Some API options are unavailable

