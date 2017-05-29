import time


def compare_exchange(tradeclient, bitfinex, exch2):
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

