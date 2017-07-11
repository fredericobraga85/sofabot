from indicators.Indicator import Indicator


class FibonnaciIndicator(Indicator):


    def __init__(self, printPlot=False, buyCode=1):
        self.printPlot = printPlot
        self.buyCode = buyCode
        self.last_period_interval = 1
        self.second_period_interval = self.last_period_interval  + 1#* 2
        self.first_period_interval = self.second_period_interval + 1# * 2
        self.latency_perc = 1.02


    def trainML(self, marketExchange, chartDataAnalyzer):
        doNothing = True

    def train(self, orderState, df, i):
        # self.calculateMoment(i, orderState, df)
        doNothing = True

    def predict(self, orderState, df, i):

        if i >= self.first_period_interval + self.second_period_interval + self.last_period_interval:

            self.price_1 = df.iloc[i - (self.first_period_interval + self.second_period_interval + self.last_period_interval)]['weightedAverage']
            self.price_2 = df.iloc[i - (self.second_period_interval + self.last_period_interval)]['weightedAverage']
            self.price_3 = df.iloc[i - self.last_period_interval]['weightedAverage']

            # if self.price_2 > self.price_3 and self.price_3 > self.price_1:
            #
            #     # if self.top_price / self.bottom_price > self.latency_perc:
            #
            #     if self.price_3 / self.price_2 > 0.7:
            #
            #         if orderState.actual_price > self.price_3:
            #             df.loc[i, 'fibo'] = df.iloc[i - 1]['weightedAverage']
            #
            #             return self.buyCode
            # el
            if self.price_2 < self.price_3 and self.price_3 < self.price_1:

                if self.price_3 / self.price_2 < 1.3:

                    if orderState.actual_price > self.price_3:
                        df.loc[i, 'fibo'] = df.iloc[i - 1]['weightedAverage']

                        return self.buyCode

        return 0



    def plot(self, df, plt):

        if self.printPlot:
            super(FibonnaciIndicator, self).plot(df ,plt)

            if 'fibo' in df.columns:
                plt.plot(df['timestamp'] - df['timestamp'][0], df['fibo']/df.iloc[0]['weightedAverage'], color='r')

            plt.show()
