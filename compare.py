import time


def compare_exchange(tradeclient, tradeclient2, bitfinex, exmo):
    """ Compare exchange rates at bitfinex and ___
    Buy bitcoins at the exchange with lower rates.
    Sell bitcoins at the exchange with higher rates.
    """
    
    # Check if the difference between rates is higher than 1.5% 
    
    # Case 1: second exchange is cheaper than first
    if (float(bitfinex[1])-float(exmo[0]))*100/float(bitfinex[1]) > 1.5:

        # Buy bitcoins at exmo 
        buy_order = tradeclient2.place_order('BTC_USD', 1, exmo[0], 'buy')
        
        # Get bitcoin deposit address at bitfinex
        deposit_btc_bitfinex = tradeclient.deposit_btc('bitcoin', 'exchange', renew=0)

        # Withdraw bitcoins from exmo to bitfinex
        while True:
            if isinstance(buy_order, str):  # Check for error messages
                print('Error Message: ', buy_order)
            else:
                order_id=buy_order['order_id']

            try:
                status_order = tradeclient2.open_orders(order_id)
            except:
                print('Error Message: Provide valid order id for a withdrawal.')
                break

            if status_order['remaining_amount'] == 0:
                if deposit_btc_bitfinex:
                    withdraw = tradeclient2.withdraw_crypto(1, 'BTC', deposit_btc_bitfinex) 
                    break
                else:
                    print('Set up bitfinex deposit address')  
                    break
            time.sleep(1)

        # Sell bitcoins at bitfinex
        sell_order = tradeclient.place_order('1', str(bitfinex[1]), 'sell', 'exchange market')

        # Get Deposit address for USD funds at exmo 
        dpt_usd_exmo = tradeclient2.deposit_usd()

        # Withdraw funds from bitfinex USD account when an order is done 
        while True:

            if isinstance(sell_order, str):  # Check for error messages
                print('Error Message: ', sell_order)
            else:
                order_id = sell_order['order_id']

            try:
                status_order = tradeclient.status_order(order_id)
            except:
                print('Error Message: Provide valid order id for a withdrawal.')
                break

            if status_order['remaining_amount'] == 0:
                try:
                    dpt_usd_exmo['bank_account']
                    withdraw_usd = tradeclient.withdraw_usd(
                                                'bitcoin', 'exchange', '1',
                                                dpt_usd_exmo['bank_account'],
                                                dpt_usd_exmo['bank_name'],
                                                dpt_usd_exmo['bank_address'],
                                                dpt_usd_exmo['usdbank_city'],
                                                dpt_usd_exmo['bank_country']
                                                )
                    break
                except:
                    print('Error Message: Set up exmo usd account details for the withdrawal.')  
                    break
            time.sleep(1)
    
    # Case 2: first exchange is cheaper than second
    elif (float(exmo[1])-float(bitfinex[0]))*100/float(exmo[1]) > 1.5:
        
        # Buy bitcoins at bitfinex
        sell_order = tradeclient.place_order('1', str(bitfinex[0]), 'buy', 'exchange market')

        # Get bitcoin deposit address at exmo 
        deposit_btc_exmo = tradeclient2.deposit_btc()
        
        # Withdraw funds from bitfinex BTC account when an order is done 
        while True:

            if isinstance(sell_order, str):  # Check for error messages
                print('Error Message: ', sell_order)
            else:
                order_id=sell_order['order_id']

            try:
                status_order = tradeclient.status_order(order_id)
            except:
                print('Error Message: Provide valid order id for a withdrawal')
                break

            if status_order['remaining_amount'] == 0:
                if deposit_btc_exmo:
                    withdraw_usd = tradeclient.withdraw_crypto('bitcoin', 'exchange', '1', deposit_btc_exmo)
                    break
                else:
                    print('Error Message: Set up exmo btc address')  
                    break
                time.sleep(1)

        # Sell bitcoins at exmo 
        sell_order = tradeclient2.place_order('BTC_USD', 1, exmo[1], 'sell')
        
        # Deposit USD funds to bitfinex
        # Wire deposits at Bitinex have been paused.
        print('Error Message: Cannot deposit USD funds. USD depoist at bitfinex is currently unavailable.')

        # Withdraw usd from exmo to bitfinex
        while True:
            if isinstance(sell_order, str):  # Check for error messages
                print('Error Message: ', sell_order)
            else:
                order_id=sell_order['order_id']
            
            try:
                order_id=sell_order['order_id']
            except:
                print('Error: Provide valid order id')
                break

            try:
                status_order = tradeclient2.trade_deals('BTC_USD', 1)[0]['trade_id']
            except:
                print('Error Message: you have no trade deals')
                break

            if status_order[0]['trade_id'] == order_id:
                if deposit_btc_bitfinex:
                    withdraw = tradeclient2.withdraw_crypto(1, 'BTC', deposit_btc_bitfinex) 
                    break
                else:
                    print('Set up bitfinex deposit address')  
                    break
            time.sleep(1)
    
    # Case 3: an exchange difference is below 1.5%
    else:
        # Do nothing if the rate diffrence is lower than 1.5%
        print('Exchange rate difference is lower than 1.5%')
        pass

