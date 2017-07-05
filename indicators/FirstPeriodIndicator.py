from indicators.Indicator import Indicator


class FirstPeriodIndicator(Indicator):


    def __init__(self):
        self.latency_perc = 1.02

    def predict(self, orderState, df, i):

        if orderState.actual_price > df.iloc[0]['weightedAverage'] * self.latency_perc:
            return 1

        return 0


    def plot(self, df, plt):

        super(FirstPeriodIndicator, self).plot(df ,plt)
        #
        # if 'bb' in df.columns:
        #     plt.plot(df['timestamp'] - df['timestamp'][0], df['bb'])
        #     plt.plot(df['timestamp'] - df['timestamp'][0], df['upperbb'])
        #     plt.plot(df['timestamp'] - df['timestamp'][0], df['lowerbb'])
        #
        plt.show()



