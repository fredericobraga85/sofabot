from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import Service as s
from indicators.Indicator import Indicator


class KNNIndicator(Indicator):



    def __init__(self, currencyPair, period, timestamp, printPlot=False, buyCode=1):
        self.printPlot = printPlot
        self.buyCode = buyCode

        self.nNeigbors = 3
        self.iDistance = 4
        self.gainLimit = 1.015

        self.trained = False
        self.currencyPair = currencyPair
        self.period = period
        self.timestamp = timestamp



    def trainML(self, marketExchange, chartDataAnalyzer):

        if self.trained == False:

            file_name = 'knn/knn' + self.currencyPair + self.timestamp[0] + self.timestamp[1] + self.period + '.csv'

            try:
                self.knn_df = pd.read_csv(file_name)
            except:
                self.knn_df = marketExchange.get_chart_data(self.timestamp[0], self.timestamp[1])

            chartDataAnalyzer.run_feature_engineer(self.knn_df)
            self.clf = KNeighborsClassifier(self.nNeigbors)
            self.knn_df = self.setShouldBuy(self.knn_df)

            print 'train'

            self.clf.fit(self.getInput(self.knn_df), self.knn_df['knn'])

            # self.knn_df.to_csv(file_name, index=False)

            self.trained = True



    def getInput(self,df):
        input_df =   df[[
            # 'date',
            # 'timestamp'
            'close',
            'high',
            'low',
            'open',
            # 'supportQuote',
            # 'resistanceQuote',
            'quoteVolume',
            'volume',
            'isUp',
            'quoteGrowth1stPeriod',
            'weightedAverage'

        ]]


        return input_df

    def setShouldBuy(self, df):

        df['knn'] = 0

        print 'setting SHoould BuY KNN'

        for i, row in df.iterrows():

            if i > self.iDistance:

                if  df['weightedAverage'].iloc[i] / df['weightedAverage'].iloc[i - self.iDistance] > self.gainLimit:

                    df.loc[i - self.iDistance, 'knn'] = self.buyCode
                # else:
                    # df.loc[i - self.iDistance, 'knn'] = 0

        return df

    def train(self, orderState, df, i):
        doNoting = True


    def predict(self , orderState, df, i):
        pred = self.clf.predict(self.getInput(df.loc[i]).reshape(1, -1))


        return pred

    def plot(self, df, plt):

        if self.printPlot:
            super(KNNIndicator, self).plot(df, plt)

            if 'knn' in df.columns:
                plt.plot(df['timestamp'] - df['timestamp'][0], df['knn'], color='r')

            plt.show()
