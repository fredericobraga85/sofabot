from indicators.Indicator import Indicator


class BigFallIndicator(Indicator):


    def __init__(self, printPlot=False, buyCode=1):
        self.fall_perc = 0.97
        self.last_max_index = 0
        self.printPlot = printPlot
        self.buyCode = buyCode


    def preSetup(self, df):
        self.last_max_index = 0
        self.big_fall = False
        self.count = 0

    def predict(self, orderState, df, i):

        max_price =  df[self.last_max_index:i]['weightedAverage'].max()
        df.loc[i, 'max_price'] = max_price

        if df['timestamp'][i] - df['timestamp'][0] >= 25000:
            stop = True

        if orderState.actual_price / max_price < self.fall_perc:

            self.count = 0
            self.big_fall = True


            # return self.buyCode

        if self.big_fall == True:

            self.count = self.count + 1

            if self.count <= 3:
                if orderState.actual_price >  df.iloc[i - 1]['weightedAverage'] or  orderState.actual_price >  df.iloc[i - 2]['weightedAverage'] :

                    df.loc[i, 'bigFall'] = df.iloc[i - 1]['weightedAverage']
                    # if df.iloc[i - 1]['weightedAverage'] > df.iloc[i - 2]['weightedAverage']:

                    self.last_max_index = i
                    return self.buyCode
                else:
                    return 0
            else:
                self.big_fall = False
                return 0
        else:
            return 0


    def plot(self, df, plt):

        if self.printPlot:
            super(BigFallIndicator, self).plot(df ,plt)

            if 'bigFall' in df.columns:
                plt.plot(df['timestamp'] - df['timestamp'][0], df['bigFall']  / df.iloc[0]['weightedAverage'])
                # plt.plot(df['timestamp'] - df['timestamp'][0], df['max_price']/ df.iloc[0]['weightedAverage'])


            plt.show()



