from thread import start_new_thread
import Bitfinex
import sched, time
import threading
import time
import pandas as pd
from ..models import Exchange

exitFlag = 0



class MarketThread (threading.Thread):


    def __init__(self, threadID, name, currency_pair, marketExchange):
      threading.Thread.__init__(self)
      self.marketExchange = marketExchange

      self.threadID = threadID
      self.name = name
      self.orderBookDict = ""
      self.currency_pair = currency_pair
      self.df_lastOrderBook = pd.DataFrame()

    # def run(self):
    #   # print "Starting " + self.name
    #   # self.startTicker()
    #   # print "Exiting " + self.name
    #
    #
    # def startTicker(self):
    #
    #     self.start = True
    #
    #     s = sched.scheduler(time.time, time.sleep)
    #
    #     def execute(sc):
    #
    #         if self.start:
    #
    #             listExchanges = []
    #             ticker = self.marketExchange.getTicker(self.currency_pair)
    #             listExchanges.append(ticker)
    #
    #             self.df_ticker = pd.DataFrame(listExchanges)
    #             s.enter(5, 0, execute, (sc,))
    #
    #
    #     s.enter(5, 0, execute, (s,))
    #     s.run()
    #
    # def stopTicker(self):
    #     self.start = False


    def getLastPrice(self):

        try:
            # price = float(self.df_ticker['last_price'])
            ticker = self.marketExchange.getTicker(self.currency_pair)
            return float(ticker['last_price'])
        except:
            return -1


    def sendBuyOrder(self, exchange, orderState):
        print 'Enviando ordem de compra...'

        amount = orderState.current_btc / self.getLastPrice()

        print 'Current default coin', orderState.current_btc
        print 'Last Price', self.getLastPrice()
        print 'amount ', amount

        orderNumber = self.marketExchange.sendBuyOrder(exchange.currency_pair, amount)

        return orderNumber



    def buyOrderWasExecuted(self, orderNumber):

        print 'Verificando se ordem de compra foi realizada...'

        orderExecuted = self.marketExchange.isOrderExecuted(orderNumber)

        return orderExecuted

    def sellOrderWasExecuted(self, orderNumber):

        print 'Verificando se ordem de venda foi realizada....'

        orderExecuted = self.marketExchange.isOrderExecuted(orderNumber)

        return orderExecuted

    def getBuyPrice(self, orderNumber):
        print 'Buscando preco de compra...'

        buyPrice = float(self.marketExchange.getBuyPrice(orderNumber))

        return buyPrice

    def getBuyAmount(self, orderNumber):
        print 'Buscando quantidade de compra...'

        buyAmount = float(self.marketExchange.getBuyAmount(orderNumber))

        print buyAmount

        return buyAmount

    def getSellPrice(self, orderNumber):
        print 'Buscando preco de venda...'

        sellPrice = float(self.marketExchange.getSellPrice(orderNumber))

        print sellPrice

        return sellPrice

    def sendGainingSellOrder(self, exchange, price):

        print 'Enviando ordem de venda com ganho...'

        orderNumber = self.marketExchange.sendSellAllOrder(exchange.currency_pair, price, False)

        return orderNumber

    def sendLosingSellOrder(self, exchange, price):

        print 'Enviando ordem de venda com perda...'

        orderNumber = self.marketExchange.sendSellAllOrder(exchange.currency_pair, price, True)

        return orderNumber

    def cancelOrder(self, orderNumber):

        print 'Cancelando ordem...'

        orderNumber = self.marketExchange.cancelOrder(orderNumber)

        return orderNumber

    def transferPiggy(self, piggyValue):

        print 'Transferindo ganhos para cofre...'
        resp = self.marketExchange.transferPiggy(piggyValue)

        print resp