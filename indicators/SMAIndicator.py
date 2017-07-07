from sklearn import svm
import pandas as pd
import Service as s
from indicators.Indicator import Indicator


class SMAIndicator(Indicator):

    def __init__(self, printPlot=False, buyCode=1):
        self.printPlot = printPlot
        self.buyCode = buyCode


        self.iDistance = 5
        self.gainLimit = 1.01
        self.lossLimit = 0.98


    def calculateMoment(self, i, orderState, df):

        self.sva = 0

        if i > self.iDistance:

            self.sva = df[i-self.iDistance:i]['weightedAverage'].mean()

        df.loc[i, 'sva'] = self.sva

    def trainML(self, marketExchange, chartDataAnalyzer):
        doNothing = True

    def train(self,orderState, df, i):
        self.calculateMoment(i, orderState, df)

    def predict(self, orderState, df, i):


        if i > 0:
            self.calculateMoment(i , orderState, df)

            if df.iloc[i-self.iDistance]['sva']  > 0 :
                if self.sva / df.iloc[i-self.iDistance]['sva'] > self.gainLimit:
                    return self.buyCode
                elif self.sva / df.iloc[i-self.iDistance]['sva'] < self.lossLimit:
                    return self.buyCode
        return 0

    def plot(self, df, plt):

        if self.printPlot:
            super(SMAIndicator, self).plot(df, plt)

            plt.show()