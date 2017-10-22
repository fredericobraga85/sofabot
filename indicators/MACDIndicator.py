from sklearn import svm
import pandas as pd

import Converter
import Service as s
from indicators.Indicator import Indicator


class MACDIndicator(Indicator):

    def __init__(self, printPlot=False, buyCode=1):
        self.printPlot = printPlot
        self.buyCode = buyCode


        self.period_1 = 26
        # self.period_2 = 12
        self.period_3 = 5


    def train(self,orderState, df, i):
        self.calculateMoment(i, orderState, df)

    def predict(self, orderState, df, i):

        if i > self.period_1 + self.period_3:
            df.loc[i, 'macd_long'] = df.iloc[i - self.period_1:i]['weightedAverage'].mean()
            df.loc[i, 'macd_short'] = df.iloc[i - self.period_3:i]['weightedAverage'].mean()

            if df.loc[i - 1, 'macd_long'] > df.loc[i - 1, 'macd_short']:

                if df.loc[i, 'macd_long'] < df.loc[i, 'macd_short']:

                    return self.buyCode


        return 0



    def plot(self, df, plt):

        if self.printPlot:
            super(MACDIndicator, self).plot(df ,plt)

            if 'macd_long' in df.columns:
                plt.plot(df['timestamp'] - df['timestamp'][0], df['macd_long'] / df.iloc[0]['weightedAverage'])
                plt.plot(df['timestamp'] - df['timestamp'][0], df['macd_short']/ df.iloc[0]['weightedAverage'])


            plt.show()