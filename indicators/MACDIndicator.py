from sklearn import svm
import pandas as pd

import Converter
import Service as s
from indicators.Indicator import Indicator


class MACDIndicator(Indicator):

    def __init__(self):

        self.period_1 = 26
        self.period_2 = 12
        self.period_3 = 9
        self.latency_perc = 1.02



    def trainML(self, marketExchange, chartDataAnalyzer):
        doNothing = True

    def train(self,orderState, df, i):
        self.calculateMoment(i, orderState, df)

    def predict(self, orderState, df, i):

        if i > self.period_1 + self.period_3:
            df.loc[i, 'macd']             = df.iloc[i - self.period_1:i]['weightedAverage'].mean() - df.iloc[i - self.period_2:i]['weightedAverage'].mean()
            df.loc[i, 'macd_signal_line'] = df.iloc[i - self.period_3:i]['macd'].mean()

            if df.loc[i - 1, 'macd'] < df.loc[i - 1, 'macd_signal_line']:

                if df.loc[i, 'macd'] > df.loc[i, 'macd_signal_line']:

                    return 1


        return 0



    def plot(self, df, plt):

        super(MACDIndicator, self).plot(df ,plt)

        # if 'macd' in df.columns:
        #     plt.plot(df['timestamp'] - df['timestamp'][0], df['macd'])
        #     plt.plot(df['timestamp'] - df['timestamp'][0], df['macd_signal_line'])

        plt.show()