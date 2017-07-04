from sklearn import svm
import pandas as pd
import Service as s

class SMAIndicator:

    def __init__(self):

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
                    return 1
                elif self.sva / df.iloc[i-self.iDistance]['sva'] < self.lossLimit:
                    return 1
        return 0