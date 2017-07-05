from sklearn import svm
import pandas as pd
import Service as s
from indicators.Indicator import Indicator


class SVMIndicator(Indicator):

    def __init__(self, currencyPair, period, timestamp):

        self.iDistance = 4
        self.gainLimit = 1.015

        self.trained = False
        self.currencyPair = currencyPair
        self.period = period
        self.timestamp = timestamp



    def trainML(self, marketExchange, chartDataAnalyzer):

        if self.trained == False:

            file_name = 'svm/svm' + self.currencyPair + self.timestamp[0] + self.timestamp[1] + self.period + '.csv'

            try:
                self.knn_df = pd.read_csv(file_name)
            except:
                self.knn_df = marketExchange.get_chart_data(self.timestamp[0], self.timestamp[1])

            chartDataAnalyzer.run_feature_engineer(self.knn_df)
            self.clf = svm.SVC()
            self.knn_df = self.setShouldBuy(self.knn_df)

            print 'train SVM'

            self.clf.fit(self.getInput(self.knn_df), self.knn_df['svm'])

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

        df['svm'] = 0

        print 'setting SHoould BuY SVM'

        for i, row in df.iterrows():

            if i > self.iDistance:

                if  df['weightedAverage'].iloc[i] / df['weightedAverage'].iloc[i - self.iDistance] > self.gainLimit:
                    df.loc[i - self.iDistance, 'svm'] = 1
                else:
                    df.loc[i - self.iDistance, 'svm'] = 0

        return df

    def train(self, orderState, df, i):
        doNoting = True


    def predict(self , orderState, df, i):
        pred = self.clf.predict(self.getInput(df.loc[i]).reshape(1, -1))


        return pred
