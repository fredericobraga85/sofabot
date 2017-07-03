import json
import pandas as pd
import Service as s
import Converter
from time import sleep

class Poloniex:


    def __init__(self, currencyPair, start, end, period):

        self.currencyPair = currencyPair
        self.start = start
        self.end = end
        self.period = period


    def get_chart_data(self):

        file_name = 'history/'+ self.currencyPair + self.start + self.end + self.period + '.csv'

        try:
            chart = pd.read_csv(file_name)

        except:

            try:
                params = {'currencyPair': self.currencyPair, 'start': self.start, 'end': self.end, 'period': self.period}
                json = s.get_url('https://poloniex.com/public?command=returnChartData', params)
                chart = pd.read_json(json)

                chart.to_csv(file_name, index=False)

            except:
                print 'Error loading ',  self.currencyPair
                return  None

        return chart


    def get_ticker(self):

        # sleep(0.1)
        params = {}
        j = s.get_url('https://poloniex.com/public?command=returnTicker', params)
        df_ticker = pd.read_json(j)
        return df_ticker[self.currencyPair]


    def getActiveBuyFeePerc(self):
        return 0.0030

    def getPassiveBuyFeePerc(self):
        return 0.0015

    def getActiveSellFeePerc(self):
        return 0.0030

    def getActiveSellFeePerc(self):
        return 0.0015