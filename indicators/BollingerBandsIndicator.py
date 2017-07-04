from sklearn import svm
import pandas as pd
import Service as s

class BollingerBandsIndicator:

    def __init__(self):

        self.iDistance = 12


    def calculateMoment(self, i, orderState, df):

        self.sva = 0

        if i > self.iDistance:

            self.sva = df[i-self.iDistance:i]['close'].mean()

        df.loc[i, 'bb']      = self.sva
        std = df.iloc[i - self.iDistance: i + 1]['bb'].std()
        df.loc[i, 'upperbb'] = df.loc[i, 'bb'] + (std * 2)
        df.loc[i, 'lowerbb'] = df.loc[i, 'bb'] - (std * 2)

    def trainML(self, marketExchange, chartDataAnalyzer):
        doNothing = True

    def train(self,orderState, df, i):
        self.calculateMoment(i, orderState, df)

    def predict(self, orderState, df, i):


        if i > 0:
            self.calculateMoment(i , orderState, df)

            if df.iloc[i]['bb']  > 0 :

                if df.iloc[i - 1]['lowerbb'] > df.iloc[i - 1]['close']:

                    if df.iloc[i]['lowerbb'] < orderState.actual_price:
                        return 1

        return 0