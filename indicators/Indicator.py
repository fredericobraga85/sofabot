from sklearn import svm
import pandas as pd

import Converter
import Service as s

class Indicator(object):

    def __init__(self):

        doNothing = True

    def calculateMoment(self, i, orderState, df):
        doNothing = True

    def trainML(self, marketExchange, chartDataAnalyzer):
        doNothing = True

    def train(self,orderState, df, i):
        doNothing = True

    def predict(self, orderState, df, i):
        doNothing = True
        return 0

    def plot(self, df, plt):
        plt.plot(df['timestamp'] - df['timestamp'][0], df['weightedAverage'])

        if 'buyValue' in df.columns:
            if df['buyValue'].sum() > 0:
                plt.plot(df['timestamp'] - df['timestamp'][0], df['buyValue'].apply(Converter.convert_zero_to_none))

        doNothing = True