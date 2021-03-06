from sklearn.ensemble import RandomForestClassifier
import pandas as pd

from indicators.Indicator import Indicator


class RandomForrestIndicator(Indicator):

    tag = 'randomForrest'


    def __init__(self, currencyPair, period, timestamp, printPlot=False, buyCode=1):
        self.printPlot = printPlot
        self.buyCode = buyCode

        self.iDistance = 5
        self.gainLimit = 1.02

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
            self.clf = RandomForestClassifier(n_estimators=10)
            self.train_df = self.setShouldBuy(self.train_df)

            print 'train ' + self.tag

            self.clf.fit(self.getInput(self.train_df), self.train_df[self.tag])


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

                if  df['weightedAverage'].iloc[i] / df[i-self.iDistance:i]['weightedAverage'].min() > self.gainLimit:
                    df.loc[i - self.iDistance, self.tag] = self.buyCode
                else:
                    df.loc[i - self.iDistance, self.tag] = 0

        return df

    def train(self, orderState, df, i):
        doNoting = True


    def predict(self , orderState, df, i):
        pred = self.clf.predict(self.getInput(df.loc[i]).reshape(1, -1))

        if pred == self.buyCode:
            df.loc[i, 'randomF'] = orderState.actual_price

        return pred

    def plot(self, df, plt):

        if self.printPlot:
            super(RandomForrestIndicator, self).plot(df, plt)

            if 'randomF' in df.columns:
                plt.plot(df['timestamp'] - df['timestamp'][0], df['randomF']/df.iloc[0]['weightedAverage'], color='r')

            plt.show()
