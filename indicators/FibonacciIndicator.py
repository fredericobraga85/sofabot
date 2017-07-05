from indicators.Indicator import Indicator


class FibonnaciIndicator(Indicator):


    def __init__(self):

        self.last_period_interval = 1
        self.second_period_interval = self.last_period_interval * 2
        self.first_period_interval = self.second_period_interval * 2
        self.latency_perc = 1.02


    def trainML(self, marketExchange, chartDataAnalyzer):
        doNothing = True

    def train(self, orderState, df, i):
        # self.calculateMoment(i, orderState, df)
        doNothing = True

    def predict(self, orderState, df, i):

        if i >= self.first_period_interval + self.second_period_interval + self.last_period_interval:

            self.bottom_price = df.iloc[i - (self.first_period_interval + self.second_period_interval + self.last_period_interval)]['weightedAverage']
            self.top_price = df.iloc[i - (self.second_period_interval + self.last_period_interval)]['weightedAverage']
            self.second_bottom_price = df.iloc[i - self.last_period_interval]['weightedAverage']

            if self.top_price > self.second_bottom_price and self.second_bottom_price > self.bottom_price:

                if self.top_price / self.bottom_price > self.latency_perc:

                    if self.second_bottom_price / self.top_price > 0.7:

                        if orderState.actual_price > self.second_bottom_price:

                            return 1

        return 0



