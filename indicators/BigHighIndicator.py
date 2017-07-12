from indicators.Indicator import Indicator


class BigHighIndicator(Indicator):


    def     __init__(self, printPlot=False, buyCode=1):
        self.high_perc = 1.02
        self.last_max_index = 0
        self.printPlot = printPlot
        self.buyCode = buyCode


    def preSetup(self):
        self.last_max_index = 0
        self.big_high = False
        self.count = 0

    def predict(self, orderState, df, i):

        min_price = df[self.last_max_index:i]['weightedAverage'].min()
        idx_min_price = df[self.last_max_index:i]['weightedAverage'].idxmin()
        max_price =  df[self.last_max_index:i]['weightedAverage'].max()
        idx_max_price =  df[self.last_max_index:i]['weightedAverage'].idxmax()

        df.loc[i, 'max_price'] = max_price
        df.loc[i, 'min_price'] = min_price

        if idx_max_price > idx_min_price:

            if max_price / min_price > self.high_perc:
                second_low = df[idx_max_price:i]['weightedAverage'].min()
                idx_second_low = df[idx_max_price:i]['weightedAverage'].idxmin()
                df.loc[i, 'second_low'] = second_low

                if idx_second_low > idx_max_price:
                    self.count = 0
                    self.big_high = True

                    if orderState.actual_price >= max_price:
                        df.loc[i, 'bigHigh'] = df.iloc[i - 1]['weightedAverage']
                        self.big_high = False
                        self.last_max_index = i
                        return self.buyCode

        return 0

            # return self.buyCode

    def plot(self, df, plt):

        if self.printPlot:
            super(BigHighIndicator, self).plot(df ,plt)

            if 'second_low' in df.columns:
                # plt.plot(df['timestamp'] - df['timestamp'][0], df['bigHigh'])
                plt.plot(df['timestamp'] - df['timestamp'][0], df['max_price'])
                plt.plot(df['timestamp'] - df['timestamp'][0], df['min_price'])
                plt.plot(df['timestamp'] - df['timestamp'][0], df['second_low'])


            plt.show()



