from thread import start_new_thread
import Poloniex2
import sched, time
import threading
import time
import pandas as pd
import json

exitFlag = 0



class TickerThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.df = pd.DataFrame()
      self.resp_dict = ""
      self.p = Poloniex2.Poloniex2(key, secret)

   def run(self):
      print "Starting " + self.name
      startTicker(self)
      print "Exiting " + self.name


def startTicker(t):

    s = sched.scheduler(time.time, time.sleep)

    def execute(sc):
        t.resp_dict = t.p.returnTicker()

        s.enter(20, 0, execute, (sc,))

    s.enter(20, 0, execute, (s,))
    s.run()


# Create new threads
thread1 = TickerThread(1, "Thread-1", 1)

# Start new Threads
thread1.start()


print "Exiting Main Thread"