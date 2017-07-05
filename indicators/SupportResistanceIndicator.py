import Converter
from indicators.Indicator import Indicator


class SupportResistanceIndicator(Indicator):

    resistance_tolerance = 1.05
    dif_open_close_perc = 1.005
    resistance = 0
    support = 0

    # def train(self, df, dif_open_close_tolerance_perc):
    #     self.df = df
    #     self.dif_open_close_tolerance_perc = dif_open_close_tolerance_perc

    def trainML(self, marketExchange, chartDataAnalyzer):
        doNoting = True


    def calculateMoment(self, i, orderState, df):

        dif_open_close_1 = abs(df['close'].iloc[i - 3] - df['open'].iloc[i - 3])
        dif_open_close_2 = abs(df['close'].iloc[i - 2] - df['open'].iloc[i - 2])
        dif_open_close_3 = df['close'].iloc[i - 1] - df['open'].iloc[i - 1]

        if dif_open_close_1 + dif_open_close_2 > 0.000001:

            if dif_open_close_3 > 0:
                if dif_open_close_3 > (dif_open_close_1 + dif_open_close_2) * self.dif_open_close_perc:
                    self.support = df['open'].iloc[i - 1]

                    if df['close'].iloc[i - 1] > self.resistance or self.resistance == 0:
                        self.resistance = df['close'].iloc[i - 1]

            elif dif_open_close_3 < 0:

                if abs(dif_open_close_3) > (dif_open_close_1 + dif_open_close_2) * self.dif_open_close_perc:
                    self.resistance = df['open'].iloc[i - 1]

                    if df['close'].iloc[i - 1] < self.support or self.support == 0:
                        self.support = df['close'].iloc[i - 1]

            if orderState.inBuy:
                if orderState.actual_price < self.support:
                    self.support = orderState.actual_price

                if orderState.actual_price > self.resistance:
                    self.resistance = orderState.actual_price

        df.loc[i, 'supportQuote'] = self.support
        df.loc[i, 'resistanceQuote'] = self.resistance


    def train(self,orderState, df, i):
        self.calculateMoment(i, orderState, df)

    def predict(self, orderState, df, i):

        self.calculateMoment(i , orderState, df)

        if self.support != 0 and orderState.actual_price > self.support and orderState.actual_price < self.support * self.resistance_tolerance:

            if self.support != 0:

                return 1

        return 0

    def plot(self, df, plt):

        super(SupportResistanceIndicator, self).plot(df, plt)

        plt.plot(df['timestamp'] - df['timestamp'][0],df['supportQuote'].apply(Converter.convert_zero_to_none))
        plt.plotdf['timestamp'] - df['timestamp'][0],df['resistanceQuote'].apply(Converter.convert_zero_to_none)



