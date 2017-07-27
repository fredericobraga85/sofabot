from thread import start_new_thread
import Poloniex
import sched, time
import threading
import time
import pandas as pd

exitFlag = 0

class TickerThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.df = pd.DataFrame()

   def run(self):
      print "Starting " + self.name
      startTicker(self)
      print "Exiting " + self.name


def startTicker(t):
    p = Poloniex.Poloniex("BTC_LTC")

    s = sched.scheduler(time.time, time.sleep)

    def execute(sc):
        t.df = p.get_ticker()

        print t.df

        s.enter(5, 0, execute, (sc,))

    s.enter(5, 0, execute, (s,))
    s.run()


# Create new threads
thread1 = TickerThread(1, "Thread-1", 1)

# Start new Threads
thread1.start()


print "Exiting Main Thread"