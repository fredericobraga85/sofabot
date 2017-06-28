import json
import pandas as pd
import Service as s
import Converter
from time import sleep

class Poloniex:

    def get_chart_data(self, currencyPair, start, end, period):
        params = {'currencyPair': currencyPair, 'start': start, 'end': end, 'period': period}
        json = s.get_url('https://poloniex.com/public?command=returnChartData', params)
        return self.chart_feature_engineering(json)

    def chart_feature_engineering(self, json):

        df_chart_data = pd.read_json(json)
        df_chart_data['quoteVolume'] = df_chart_data['quoteVolume'].apply(Converter.convert_to_float)
        df_chart_data['date'] = df_chart_data['date'].apply(Converter.convert_to_timestamp)

        return df_chart_data

    def get_ticker(self, currencyPair):

        # sleep(0.1)
        params = {}
        j = s.get_url('https://poloniex.com/public?command=returnTicker', params)
        return self.ticker_feature_engineering(j, currencyPair)

    def ticker_feature_engineering(self, j, currencyPair):


        df_ticker = pd.read_json(j)

        return df_ticker[currencyPair]
