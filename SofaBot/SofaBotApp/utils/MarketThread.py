from thread import start_new_thread
import Poloniex2
import sched, time
import threading
import time
import pandas as pd
import json
import pdb

exitFlag = 0



class MarketThread (threading.Thread):
    def __init__(self, threadID, name, currency_pair):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.orderBookDict = ""
      self.marketExchange = Poloniex2.Poloniex2()
      self.currency_pair = currency_pair
      self.df_lastOrderBook = pd.DataFrame()

    def run(self):
      print "Starting " + self.name
      self.startTicker()
      print "Exiting " + self.name


    def startTicker(self):

        self.start = True

        s = sched.scheduler(time.time, time.sleep)

        def execute(sc):

            if self.start:
                self.orderBookDict = self.marketExchange.returnOrderBook(self.currency_pair, 1)
                self.df_lastOrderBook = pd.DataFrame(self.orderBookDict)
                s.enter(5, 0, execute, (sc,))

        s.enter(5, 0, execute, (s,))
        s.run()

    def stopTicker(self):
        self.start = False

    def getLastAskPrice(self):

        try:
            price = float(self.df_lastOrderBook['asks'].iloc[0][0])
            return price
        except:
            return -1


    def getLastBidPrice(self):

        try:
            price = float(self.df_lastOrderBook['bids'].iloc[0][0])
            return price
        except:
            return -1

