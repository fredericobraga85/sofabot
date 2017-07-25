from indicators.Indicator import Indicator
import pandas as pd

class WinAndLoseIndicator(Indicator):


    def __init__(self, printPlot=False, buyCode=1):

        self.iDistance = 5
        self.printPlot = printPlot
        self.buyCode = buyCode
        self.mean_series = pd.Series()
        self.mean_index = 2

    def preSetup(self, df):
        for i, row in df.iterrows():
            if i < len(df) - self.iDistance:
                max = df.iloc[i + self.iDistance]['weightedAverage'] / df.iloc[i]['weightedAverage']
                # min = (df[i+1:i + self.iDistance]['weightedAverage'].min() / df.iloc[i]['weightedAverage'])
                df.loc[i, 'win_lose_max_indicator'] = ((max - (max % 0.0001)) - 1) * 100
                # df.loc[i, 'win_lose_min_indicator'] = ((min - (min % 0.0001)) - 1) * 100



    def predict(self, orderState, df, i):

        if i == 0:

            if len(self.mean_series) > self.mean_index + 1:


                mean1 = self.mean_series.iloc[(self.mean_index * -1 ):].mean()
                mean2 = self.mean_series.iloc[(self.mean_index * -1 - 1):-1].mean()

                print 'mean1',mean1
                print 'mean2',mean2
                print 'mean dif ', mean1 - mean2

                if mean1 - mean2 < -0.06:
                        return 1


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

        s = df['win_lose_max_indicator'].fillna(0)
        rslt =  ((df['sellValue'].fillna(0) / df['buyValue'].fillna(0) ) - 1 ) * 100


        self.mean_series.set_value(len(self.mean_series), s.mean())


        range = 8

        n, bins, patches = plt.hist(s, bins=range * 2 * 4, range=(range * - 1,range), rwidth='scalar')
        n, bins, patches = plt.hist(rslt, bins=range * 2 * 4, range=(range * - 1, range), rwidth='scalar')

        print 'higher than zedro:', len(s.apply(self.higherThanZero).dropna())
        print 'lower  than zedro:', len(s.apply(self.lowerThanZero).dropna())
        print 'std :',              s.std()
        print 'mean:', s.mean()




        if self.printPlot:
            plt.xlabel('% Gain')
            plt.ylabel('Qtde')
            # plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
            # plt.axis([-5.0, 5.0, 0,200 ])
            # plt.xticks(range(-5,5))
            plt.grid(True)

            plt.show()

