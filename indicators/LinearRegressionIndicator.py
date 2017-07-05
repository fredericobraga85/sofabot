from sklearn import  linear_model
import pandas as pd
import Service as s
from indicators.Indicator import Indicator


class LinearRegressionIndicator(Indicator):

    tag = 'linearReg'


    def __init__(self, currencyPair, period, timestamp):



        self.iDistance = 4
        self.gainLimit = 1.025

        self.trained = False
        self.currencyPair = currencyPair
        self.period = period
        self.timestamp = timestamp



    def trainML(self, marketExchange, chartDataAnalyzer):

        if self.trained == False:

            file_name = self.tag + '/' + self.tag  + self.currencyPair + self.timestamp[0] + self.timestamp[1] + self.period + '.csv'

            try:
                self.train_df = pd.read_csv(file_name)
            except:
                self.train_df = marketExchange.get_chart_data(self.timestamp[0], self.timestamp[1])

            chartDataAnalyzer.run_feature_engineer(self.train_df)
            self.clf = linear_model.LinearRegression()
            self.train_df = self.setShouldBuy(self.train_df)

            print 'train ' + self.tag

            self.clf.fit(self.getInput(self.train_df), self.train_df[self.tag])

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

        df[self.tag] = 0

        print 'setting Should BuY ' + self.tag

        for i, row in df.iterrows():

            if i > self.iDistance:

                if  df['weightedAverage'].iloc[i] / df['weightedAverage'].iloc[i - self.iDistance] > self.gainLimit:
                    df.loc[i - self.iDistance, self.tag] = 1
                else:
                    df.loc[i - self.iDistance, self.tag] = 0

        return df

    def train(self, orderState, df, i):
        doNoting = True


    def predict(self , orderState, df, i):
        pred = self.clf.predict(self.getInput(df.loc[i]).reshape(1, -1))


        return pred
