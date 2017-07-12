from indicators.Indicator import Indicator


class BigUpIndicator(Indicator):


    def __init__(self, printPlot=False, buyCode=1):
        self.up_perc = 1.02
        self.last_max_index = 0
        self.printPlot = printPlot
        self.buyCode = buyCode


    def preSetup(self, df):
        self.last_max_index = 0
        self.big_up = False
        self.count = 0

    def predict(self, orderState, df, i):

        min_price =  df[self.last_max_index:i]['weightedAverage'].min()
        max_price =  df[self.last_max_index:i]['weightedAverage'].max()
        df.loc[i, 'min_price'] = min_price

        if orderState.actual_price / min_price > self.up_perc:

            self.count = 0
            self.big_up = True


            # return self.buyCode

        if self.big_up == True:

            self.count = self.count + 1

            if self.count <= 3:
                if orderState.actual_price >  df.iloc[i - 1]['weightedAverage']:

                    if orderState.actual_price > max_price:

                        df.loc[i, 'bigUp'] = orderState.actual_price
                        # if df.iloc[i - 1]['weightedAverage'] > df.iloc[i - 2]['weightedAverage']:

                        self.last_max_index = i
                        return self.buyCode
                    else:
                        return 0
                else:
                    return 0
            else:
                self.big_up = False
                return 0
        else:
            return 0


    def plot(self, df, plt):

        if self.printPlot:
            super(BigUpIndicator, self).plot(df ,plt)

            if 'bigUp' in df.columns:
                plt.plot(df['timestamp'] - df['timestamp'][0], df['bigUp']  / df.iloc[0]['weightedAverage'], color='r')
                # plt.plot(df['timestamp'] - df['timestamp'][0], df['min_price']/ df.iloc[0]['weightedAverage'])


            plt.show()



