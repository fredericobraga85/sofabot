

class SupportResistanceIndicator:

    resistance_tolerance = 1.005
    dif_open_close_perc = 1.005


    def train(self, df, dif_open_close_tolerance_perc):
        self.df = df
        self.dif_open_close_tolerance_perc = dif_open_close_tolerance_perc

    def calculateMoment(self, i, orderState, df):

        dif_open_close_1 = abs(self.df['close'].iloc[i - 3] - self.df['open'].iloc[i - 3])
        dif_open_close_2 = abs(self.df['close'].iloc[i - 2] - self.df['open'].iloc[i - 2])
        dif_open_close_3 = self.df['close'].iloc[i - 1] - self.df['open'].iloc[i - 1]

        if dif_open_close_1 + dif_open_close_2 > 0.000001:

            if dif_open_close_3 > 0:
                if dif_open_close_3 > (dif_open_close_1 + dif_open_close_2) * self.dif_open_close_tolerance_perc:
                    self.support = self.df['open'].iloc[i - 1]

                    if self.df['close'].iloc[i - 1] > self.resistance or self.resistance == 0:
                        self.resistance = self.df['close'].iloc[i - 1]

            elif dif_open_close_3 < 0:

                if abs(dif_open_close_3) > (dif_open_close_1 + dif_open_close_2) * self.dif_open_close_tolerance_perc:
                    self.resistance = self.df['open'].iloc[i - 1]

                    if self.df['close'].iloc[i - 1] < self.support or self.support == 0:
                        self.support = self.df['close'].iloc[i - 1]

            if orderState.inBuy:
                if orderState.actual_price < self.support:
                    self.support = self.actual_price

                if orderState.actual_price > self.resistance:
                    self.resistance = self.actual_price

        df.loc[i, 'supportQuote'] = self.support
        df.loc[i, 'resistanceQuote'] = self.resistance


    def predict(self, orderState):

        if self.resistance != 0 and orderState.actual_price > self.resistance * self.resistance_tolerance:

            if self.resistance != 0:

                orderState.printBuyOrder()




