import json
import pandas as pd
import Service as s
import Converter
from time import sleep

class Poloniex:

    def get_chart_data(self, currencyPair, start, end, period):

        file_name = currencyPair + start + end + period + '.csv'

        try:
            chart = pd.read_csv(file_name)

        except:

            params = {'currencyPair': currencyPair, 'start': start, 'end': end, 'period': period}
            json = s.get_url('https://poloniex.com/public?command=returnChartData', params)
            chart = pd.read_json(json)

            chart.to_csv(file_name, index=False)

        chart_edited = self.chart_feature_engineering(chart)

        return chart_edited


    def chart_feature_engineering(self, chart):

        chart['quoteVolume'] = chart['quoteVolume'].apply(Converter.convert_to_float)
        chart['date'] = chart['date'].apply(Converter.convert_to_timestamp)

        return chart

    def get_ticker(self, currencyPair):

        # sleep(0.1)
        params = {}
        j = s.get_url('https://poloniex.com/public?command=returnTicker', params)
        return self.ticker_feature_engineering(j, currencyPair)

    def ticker_feature_engineering(self, j, currencyPair):


        df_ticker = pd.read_json(j)

        return df_ticker[currencyPair]
