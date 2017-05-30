import requests
import urllib
import json
import base64
import hmac
import hashlib
import time

PROTOCOL = "https"
HOST = "api.exmo.com"
VERSION = "v1"

# HTTP request timeout in seconds
TIMEOUT = 5.0

class ExmoTradeClient:
    """
    Authenticate client 
    for trading through Exmo API
    """

    def __init__(self, key, secret):
        self.URL = "{0:s}://{1:s}/{2:s}".format(PROTOCOL, HOST, VERSION)
        self.KEY = key
        self.SECRET = secret
        pass

    @property
    def _nonce(self):
        """
        Returns a nonce
        Used in authentication
        """
        return int(round(time.time()*1000)) 

    def _sign_payload(self, payload):
        payload = urllib.parse.urlencode(payload)
        H = hmac.new(self.SECRET.encode('utf8'), digestmod=hashlib.sha512)
        H.update(payload.encode('utf8'))
        sign = H.hexdigest()

        return {
                "Content-type": "application/x-www-form-urlencoded",
                "Key": self.KEY,
                "Sign": sign
                }

    def place_order(self, pair, quantity, price, order_type):
        """
        Submit a new order.
        :param pair:
        :param quantity:
        :param price:
        :param ord_type:
        :return:
        """
        params = {
            "nonce": self._nonce,
            "pair": pair,
            "quantity": quantity,
            "price": price,
            "type": order_type
        }

        headers = self._sign_payload(params)

        api_url = '/order_create'
        r = requests.post(self.URL+api_url, params, headers=headers, verify=True)
        json_resp = r.json()

        try:
            json_resp['order_id']
        except:
            return json_resp['error']

        return json_resp 

    def open_orders(self):
        """
        Order's status.
        :return:
        """
        params = {
            "nonce": self._nonce,
        }

        headers = self._sign_payload(params)

        api_url = '/user_open_orders'
        r = requests.post(self.URL+api_url, params, headers=headers, verify=True)
        json_resp = r.json()
        if json_resp:
            return json_resp 
        else:
            return 'Message: You have no active orders' 
 
    def deposit_usd(self):
        return 'Refer to the third party deposit addresses. Exmo uses services such as Epay and MoneyPolo' 

    def deposit_btc(self, *params):
        """
        Get btc address.
        :return:
        """
        params = {
            "nonce": self._nonce,
        }

        headers = self._sign_payload(params)

        api_url = '/deposit_address'
        r = requests.post(self.URL+api_url, params, headers=headers, verify=True)
        json_resp = r.json()

        try:
            json_resp['BTC']
            return json_resp['BTC']
        except:
            return 'Message: Create BTC address' 

    def withdraw_crypto(self, amount, currency, address):
        print('ATTENTION!!! This API function is available only after request to the Exmo Technical Support.')
        """
        Withdraw BTC from exmo account.
        :param amount:
        :param currency:
        :param address:
        :return:
        """
        params = {
            "nonce": self._nonce,
            "amount": amount,
            "currency": currency,
            "address": address
        }

        headers = self._sign_payload(params)

        api_url = '/withdraw_crypt'
        r = requests.post(self.URL+api_url, params, headers=headers, verify=True)
        json_resp = r.json()

        try:
            json_resp['task_id']
        except:
            return json_resp['error']

        return json_resp 

    def withdraw_usd(self):
        return 'No API available for usd withdrawal at exmo'
