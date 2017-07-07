from indicators.Indicator import Indicator


class BigFallIndicator(Indicator):


    def __init__(self):
        self.fall_perc = 0.97
        self.last_max_index = 0


    def preSetup(self):
        self.last_max_index = 0
        self.big_fall = False
        self.count = 0

    def predict(self, orderState, df, i):

        if orderState.actual_price / df[self.last_max_index:i + 1]['weightedAverage'].max() < self.fall_perc:

            df.loc[i, 'bigFall'] = df.iloc[i - 1]['weightedAverage']
            self.count = 0
            self.big_fall = True
            self.last_max_index = i

        if self.big_fall == True:

            self.count = self.count + 1

            if self.count <= 3:
                if orderState.actual_price >  df.iloc[i - 1]['weightedAverage'] or  orderState.actual_price >  df.iloc[i - 2]['weightedAverage'] :

                    # if df.iloc[i - 1]['weightedAverage'] > df.iloc[i - 2]['weightedAverage']:


                    return 1
                else:
                    return 0
            else:
                self.big_fall = False
                return 0
        else:
            return 0


    def plot(self, df, plt):

        super(BigFallIndicator, self).plot(df ,plt)

        if 'bigFall' in df.columns:
            plt.plot(df['timestamp'] - df['timestamp'][0], df['bigFall'])

        plt.show()



