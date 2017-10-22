import requests
import json
import base64
import hashlib
import time
import hmac

bitfinexURL = ''
bitfinexKey = ''
bitfinexSecret = b'' #the b is deliberate, encodes to bytes

class BitFinex:

    DEFAULT_CURRENCY = 'usd'
    USD_SYMBOL = 'usd'

    shouldPrint = True

    def getTicker(self, pairCurrency):
        endpoint = '/pubticker/' + pairCurrency

        r = requests.get(bitfinexURL + endpoint)
        self.printResponse(r)
        return json.loads(r.content)

    def getPairCurrencies(self):
        endpoint = '/symbols'

        r = requests.get(bitfinexURL + endpoint)
        self.printResponse(r)
        return json.loads(r.content)


    def getTrades(self, pairCurrency, timestamp = 1505220874, limit = 2):

        endpoint = '/trades/' + pairCurrency

        # params =  {'timestamp': timestamp , 'limit_trades' : limit}

        r = requests.get(bitfinexURL + endpoint, params = {})
        self.printResponse(r)

    def getBalances(self):

        endpoint = '/balances'

        payloadObject = {
                'request':'/v1/balances',
                'nonce':str(time.time()), #convert to string
                'options':{}
        }

        resp = self.sendPost(endpoint, payloadObject)

        return json.loads(str(resp.content))

    def sendBuyOrder(self, pairCurrency, amount ):

        endpoint = '/order/new'

        payloadObject = {
                'request':'/v1/order/new',
                'nonce'    :str(time.time()), #convert to string
                'options'  :{},
                'symbol'   : pairCurrency,
                'amount'   : str(amount),
                'price'    : str(1),
                'side'     : 'buy',
                'type'     : 'exchange market',
                'exchange' : 'bitfinex',
                'ocoorder' : False,
                'buy_price_oco'  : str(0),
                'sell_price_oco' : str(0)
        }

        resp = self.sendPost(endpoint, payloadObject)

        buyOrder = json.loads(str(resp.content))

        return self.getValue(buyOrder, 'order_id')

    def sendSellAllOrder(self, pairCurrency, price, onMarketPrice):

        amount = self.getTotalAmount(pairCurrency)
        roundPrice = "%.1f" % price
        type = 'exchange market'if onMarketPrice else 'exchange limit'

        endpoint = '/order/new'

        payloadObject = {
                'request':'/v1/order/new',
                'nonce'    : str(time.time()), #convert to string
                'options'  : {},
                'symbol'   : pairCurrency,
                'amount'   : str(amount),
                'price'    : str(roundPrice),
                'side'     : 'sell',
                'type'     : type,
                'exchange' : 'bitfinex',
                'ocoorder' : False,
                'buy_price_oco'    : str(0),
                'sell_price_oco'   : str(0),
                # 'use_all_available': str(1)
        }

        resp = self.sendPost(endpoint, payloadObject)

        buyOrder = json.loads(str(resp.content))

        return self.getValue(buyOrder, 'order_id')

    def cancelOrder(self, orderNumber):

        endpoint = '/order/cancel'

        payloadObject = {
            'request'  : '/v1/order/cancel',
            'nonce'    : str(time.time()),  # convert to string
            'options'  : {},
            'order_id' : orderNumber
        }

        resp = self.sendPost(endpoint, payloadObject)

        buyOrder = json.loads(str(resp.content))

        return self.getValue(buyOrder, 'id')

    def isOrderExecuted(self, orderNumber):

        return not self.getOrderStatus(orderNumber, 'is_live')

    def getBuyPrice(self, orderNumber):
        return self.getOrderStatus(orderNumber, 'price')

    def getSellPrice(self, orderNumber):
        return self.getOrderStatus(orderNumber, 'price')

    def getBuyAmount(self, orderNumber):
        return self.getOrderStatus(orderNumber, 'original_amount')

    def getOrderStatus(self, orderNumber, key):

        endpoint = '/order/status'

        payloadObject = {
            'request': '/v1/order/status',
            'nonce': str(time.time()),  # convert to string
            'options': {},
            'order_id': orderNumber,
        }

        resp = self.sendPost(endpoint, payloadObject)

        order = json.loads(str(resp.content))

        return self.getValue(order, key)

    def transferPiggy(self, piggyValue):

        endpoint = '/transfer'

        payloadObject = {
            'request'   : '/v1/transfer',
            'nonce'     : str(time.time()),  # convert to string
            'options'   : {},
            'amount'    : str(piggyValue),
            'currency'  : self.DEFAULT_CURRENCY,
            'walletfrom': 'exchange',
            'walletto'  : 'margin',
        }

        resp = self.sendPost(endpoint, payloadObject)

        order = json.loads(str(resp.content))

        return self.getValue(order[0], 'status')

    def sendPost(self, endpoint, payloadObject):
        payload_json = json.dumps(payloadObject, indent=4, sort_keys=True)
        print "payload_json: ", payload_json
        payload = base64.b64encode(bytes(payload_json))
        # print "payload: ", payload
        m = hmac.new(bitfinexSecret, payload, hashlib.sha384)
        m = m.hexdigest()
        # headers
        headers = {
            'X-BFX-APIKEY': bitfinexKey,
            'X-BFX-PAYLOAD': base64.b64encode(bytes(payload_json)),
            'X-BFX-SIGNATURE': m
        }
        r = requests.post(bitfinexURL + endpoint, data={}, headers=headers)

        self.printResponse(r)
        return r

    def getValue(self, json , key):
        try:
            value = json[key]
            return value
        except:
            raise Exception(json['message'])

        return None

    def printResponse(self, r):

        if self.shouldPrint == True:
            print '     Response URL', r.url
            print '     Response Code: ' + str(r.status_code)
            # print 'Response Header: ' + str(r.headers)
            print '     Response Content: '+ json.dumps(json.loads(str(r.content)),indent=4, sort_keys=True)

    def parseMaxDefaultCurrency(self):

        for balance in self.getBalances():

            if balance['currency'] == self.USD_SYMBOL:
                return balance['available']

        return None


    def parseWalletsToDict(self):

        dict = {}
        for balance in self.getBalances():
                dict[balance['currency']] = balance['amount']

        return dict



# b = BitFinex()
# b.getTicker('btcusd')

    def getTotalAmount(self, pairCurrency):

        investCurrency = pairCurrency.replace(self.DEFAULT_CURRENCY,'')

        balances = self.getBalances()

        for balance in balances:
            if balance['currency'] == investCurrency:
                return balance['amount']

        return None