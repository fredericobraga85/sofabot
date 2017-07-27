import pandas as pd
import Service as s

class Poloniex:


    def __init__(self, currencyPair, start=0, end=0, period=0):

        self.currencyPair = currencyPair
        self.start = start
        self.end = end
        self.period = period

    def get_chart_data_(self):

        return self.get_chart_data(self.start, self.end)

    def get_chart_data(self, start, end):

        file_name = 'history/'+ self.currencyPair + start + end + self.period + '.csv'

        try:
            chart = pd.read_csv(file_name)

        except:

            try:
                params = {'currencyPair': self.currencyPair, 'start': start, 'end': end, 'period': self.period}
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

    def getPassiveSellFeePerc(self):
        return 0.0015

