from sklearn import svm
import pandas as pd

import Converter
import Service as s
from indicators.Indicator import Indicator


class BollingerBandsIndicator(Indicator):

    def __init__(self):

        self.iDistance = 10
        self.latency_perc = 1.02

    def calculateMoment(self, i, orderState, df):

        self.sva = 0

        if i > self.iDistance:

            self.sva = df[i-self.iDistance:i + 1]['weightedAverage'].mean()

            df.loc[i, 'bb']      = self.sva
            std = df.iloc[i - self.iDistance : i + 1]['bb'].std()
            df.loc[i, 'upperbb'] = df.loc[i, 'bb'] + (std * 2)
            df.loc[i, 'lowerbb'] = df.loc[i, 'bb'] - (std * 2)

    def trainML(self, marketExchange, chartDataAnalyzer):
        doNothing = True

    def train(self,orderState, df, i):
        self.calculateMoment(i, orderState, df)

    def predict(self, orderState, df, i):


        if i > self.iDistance:
            # self.calculateMoment(i , orderState, df)
            #
            # if df.iloc[i]['bb']  > 0 :
            #
            #     if df.iloc[i - 1]['lowerbb'] > df.iloc[i - 1]['weightedAverage']:
            #
                    # if df.iloc[i]['lowerbb'] <= orderState.actual_price:
            #
            #             if df.iloc[i - 1]['weightedAverage'] < orderState.actual_price:

            if df.iloc[i]['lowerbb'] > orderState.actual_price * 0.99:

                if df.iloc[i]['upperbb'] / df.iloc[i]['lowerbb'] > self.latency_perc:
                    return 1

        return 0

    def plot(self, df, plt):

        super(BollingerBandsIndicator, self).plot(df ,plt)
        #
        # if 'bb' in df.columns:
        #     plt.plot(df['timestamp'] - df['timestamp'][0], df['bb'])
        #     plt.plot(df['timestamp'] - df['timestamp'][0], df['upperbb'])
        #     plt.plot(df['timestamp'] - df['timestamp'][0], df['lowerbb'])
        #
        # plt.show()