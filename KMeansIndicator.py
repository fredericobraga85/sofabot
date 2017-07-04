from sklearn.cluster import KMeans
import pandas as pd
import Service as s

class KMeansIndicator:

    tag = 'kMeans'

    timestamp = \
        [
            '1496448000',  # 03/6
            # '1496534400',  # 04/6
            # '1496620800',  # 05/6
            # '1496707200',  # 06/6
            # '1496793600',  # 07/6
            # '1496880000',  # 08/6
            # '1496966400',  # 09/6
            # '1497052800',  # 10/6
            # '1497139200',  # 11/6
            # '1497225600',  # 12/6
            # '1497312000',  # 13/6
            # '1497398400',  # 14/6
            # '1497484800',  # 15/6
            # '1497571200',  # 16/6
            # '1497657600',  # 17/6
            '1497744000',  # 18/6
            # '1497830400',  # 19/6
            # '1497916800',  # 20/6
            # '1498003200',  # 21/6
            # '1498089600',  # 22/6
            # '1498176000',  # 23/6
            # '1498262400',  # 24/6
            # '1498348800',  # 25/6
            # '1498435200',  # 26/6
            # '1498521600',  # 27/6
            # '1498608000',  # 28/6
            # '1498694400',  # 29/6
            # '1498780800',  # 30/6
            # '1498867200',  # 31/6
            # '1498867200',  # 01/7
            # '9999999999',
        ]


    def __init__(self, currencyPair, period):



        self.iDistance = 4
        self.gainLimit = 1.015

        self.trained = False
        self.currencyPair = currencyPair
        self.period = period



    def trainML(self, marketExchange, chartDataAnalyzer):

        if self.trained == False:

            file_name = self.tag + '/' + self.tag  + self.currencyPair + self.timestamp[0] + self.timestamp[1] + self.period + '.csv'

            try:
                self.train_df = pd.read_csv(file_name)
            except:
                self.train_df = marketExchange.get_chart_data(self.timestamp[0], self.timestamp[1])

            chartDataAnalyzer.run_feature_engineer(self.train_df)
            self.clf = KMeans(n_clusters=2)
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
