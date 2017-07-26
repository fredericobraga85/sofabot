from indicators.Indicator import Indicator
import pandas as pd

class WinAndLoseIndicator(Indicator):


    def __init__(self, printPlot=False, buyCode=1):

        self.iDistance = 5
        self.printPlot = printPlot
        self.buyCode = buyCode
        self.mean_series = pd.Series()
        self.mean_index = 2
        self.list_mean = []
        self.df_list_gain = pd.DataFrame([])
        self.buy = 0

    def preSetup(self, df):
        for i, row in df.iterrows():
            if i < len(df) - self.iDistance:
                max = df.iloc[i + self.iDistance]['weightedAverage'] / df.iloc[i]['weightedAverage']
                # min = (df[i+1:i + self.iDistance]['weightedAverage'].min() / df.iloc[i]['weightedAverage'])
                df.loc[i, 'win_lose_max_indicator'] = ((max - (max % 0.0001)) - 1) * 100
                # df.loc[i, 'win_lose_min_indicator'] = ((min - (min % 0.0001)) - 1) * 100



    def predict(self, orderState, df, i):

        if i > 288:

            # if len(self.df_list_gain) > 1:
        #
        #         # if len(self.mean_series) > self.mean_index + 1:
        #         #
        #         #
        #         #     mean1 = self.mean_series.iloc[(self.mean_index * -1 ):].mean()
        #         #     mean2 = self.mean_series.iloc[(self.mean_index * -1 - 1):-1].mean()
        #         #
        #         #     print 'mean1',mean1
        #         #     print 'mean2',mean2
        #         #     print 'mean dif ', mean1 - mean2
        #         #
        #         #     if mean1 - mean2 < -0.06:
        #         #             return 1
        #
        #         # if (self.df_list_gain.iloc[-1] < self.df_list_gain.iloc[-2]).bool() and (self.df_list_gain.iloc[-2] < self.df_list_gain.iloc[-3]).bool():
        #         #         return 1
        #
        #         if (self.df_list_gain.iloc[-1] < -10).bool() :
        #             return 1
        #
        #
        # return 0
            return self.buy

        return 0

    def train(self,orderState, df, i):
        if i > 144:
            if df['close'].iloc[i-1]/df['close'].iloc[i-144] <  0.92 :
                self.buy = 1

            else:
                self.buy = 0


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

        self.mean = s.mean()

        print 'higher than zedro:', len(s.apply(self.higherThanZero).dropna())
        print 'lower  than zedro:', len(s.apply(self.lowerThanZero).dropna())
        print 'std :',              s.std()
        print 'mean:',              self.mean

        self.list_mean.append(self.mean)

        # if self.printPlot:
        #     plt.xlabel('% Gain')
        #     plt.ylabel('Qtde')
        #     # plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
        #     # plt.axis([-5.0, 5.0, 0,200 ])
        #     # plt.xticks(range(-5,5))
        #     plt.grid(True)
        #
        #     plt.show()

    def plot_value(self, list, plt):

        self.df_list_gain = pd.DataFrame(list)
        self.df_list_mean = pd.DataFrame(self.list_mean)

        if self.printPlot:
            fig, ax1 = plt.subplots()

            ax1.plot(self.df_list_gain, 'b-')
            ax1.set_xlabel('periodos')
            # Make the y-axis label, ticks and tick labels match the line color.
            ax1.set_ylabel('gain', color='b')
            ax1.tick_params('y', colors='b')

            ax2 = ax1.twinx()
            ax2.plot(self.df_list_mean, 'r--')
            ax2.set_ylabel('media up and down', color='r')
            ax2.tick_params('y', colors='r')

            fig.tight_layout()
            plt.show()