from indicators.Indicator import Indicator


class VolumeIndicator(Indicator):


    def __init__(self, printPlot=False, buyCode=1):

        self.perc_tolerance = 0.7
        self.printPlot = printPlot
        self.buyCode = buyCode


    def predict(self, orderState, df, i):

        if i > 2:
            if df.iloc[i]['volume'] > (df.iloc[i-1]['volume'] * self.perc_tolerance):

                if orderState.actual_price > df.iloc[i - 1]['weightedAverage']:
                    df.loc[i, 'volume_indicator'] = orderState.actual_price / df.iloc[0]['weightedAverage']
                    return self.buyCode

        return 0



    def plot(self, df, plt):

        if self.printPlot:
            super(VolumeIndicator, self).plot(df ,plt)

            if 'volume_indicator' in df.columns:
                plt.plot(df['timestamp'] - df['timestamp'][0], df['volume_indicator'], color='r')
                # plt.plot(df['timestamp'] - df['timestamp'][0], df['volume'])


            plt.show()
