from indicators.Indicator import Indicator
import numpy as np

class WinAndLoseIndicator(Indicator):


    def __init__(self, printPlot=False, buyCode=1):

        self.iDistance = 5
        self.printPlot = printPlot
        self.buyCode = buyCode

    def preSetup(self, df):
        for i, row in df.iterrows():
            if i < len(df) - self.iDistance:
                max = df.iloc[i + self.iDistance]['weightedAverage'] / df.iloc[i]['weightedAverage']
                # min = (df[i+1:i + self.iDistance]['weightedAverage'].min() / df.iloc[i]['weightedAverage'])
                df.loc[i, 'win_lose_max_indicator'] = ((max - (max % 0.0001)) - 1) * 100
                # df.loc[i, 'win_lose_min_indicator'] = ((min - (min % 0.0001)) - 1) * 100



    def predict(self, orderState, df, i):


        return 0

    def higherThanZero (self,value):
        if value > 0:
            return value

        return None

    def lowerThanZero(self, value):
        if value < 0:
            return value

        return None

    def plot(self, df, plt):

        if self.printPlot:
            # super(WinAndLoseIndicator, self).plot(df ,plt)

            # if 'win_lose_indicator' in df.columns:
            #     plt.plot(df['timestamp'] - df['timestamp'][0], df['volume_indicator']/ df.iloc[0]['weightedAverage'], color='r')
            #     # plt.plot(df['timestamp'] - df['timestamp'][0], df['volume'])


            s = df['win_lose_max_indicator'].fillna(0)
            rslt =  ((df['sellValue'].fillna(0) / df['buyValue'].fillna(0) ) - 1 ) * 100

            # s_min = df['win_lose_min_indicator'].fillna(0)
            # s = s_max.append(s_min,ignore_index=True)

            range = 8

            n, bins, patches = plt.hist(s, bins=range * 2 * 4, range=(range * - 1,range), rwidth='scalar')
            n, bins, patches = plt.hist(rslt, bins=range * 2 * 4, range=(range * - 1, range), rwidth='scalar')

            print 'higher than zedro:', len(s.apply(self.higherThanZero).dropna())
            print 'lower  than zedro:', len(s.apply(self.lowerThanZero).dropna())
            print 'std :',              s.std()
            print 'mean:',              s.mean()



            plt.xlabel('% Gain')
            plt.ylabel('Qtde')
            # plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
            # plt.axis([-5.0, 5.0, 0,200 ])
            # plt.xticks(range(-5,5))
            plt.grid(True)

            plt.show()

