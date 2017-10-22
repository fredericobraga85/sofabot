from indicators.Indicator import Indicator


class BigFallRecoverIndicator(Indicator):


    def __init__(self, printPlot=False, buyCode=1):

        self.printPlot = printPlot
        self.buyCode = buyCode
        self.iDistnce = 20
        self.dif_price_perc = 1.03


    def preSetup(self, df):
        self.last_max_index = 0
        self.count = 0

    def predict(self, orderState, df, i):

        top_price = df[0:i]['weightedAverage'].max()
        low_price = df[0:i]['weightedAverage'].min()
        idx_top_price = df[0:i]['weightedAverage'].idxmax()
        idx_low_price = df[0:i]['weightedAverage'].idxmin()

        df.loc[i, 'topPrice'] = df.iloc[idx_top_price]['weightedAverage']

        if idx_low_price > idx_top_price:
            if top_price/low_price > self.dif_price_perc:
                if orderState.actual_price > low_price:
                    # if i - idx_low_price >= idx_top_price - idx_low_price:
                    df.loc[i, 'bigFallRecover'] = orderState.actual_price

                    return self.buyCode

        return 0


    def plot(self, df, plt):

        if self.printPlot:
            super(BigFallRecoverIndicator, self).plot(df ,plt)

            if 'bigFallRecover' in df.columns:
                plt.plot(df['timestamp'] - df['timestamp'][0], df['bigFallRecover'], color='r')
                plt.plot(df['timestamp'] - df['timestamp'][0], df['topPrice'])


            plt.show()



