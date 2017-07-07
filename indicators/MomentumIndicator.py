from indicators.Indicator import Indicator


class MomentumIndicator(Indicator):

    def __init__(self, printPlot=False, buyCode=1):
        self.printPlot = printPlot
        self.buyCode = buyCode


    def calculateMoment(self, i, orderState, df):

        self.iDistance = 4
        self.momentum_tolerance = 0.98
        self.momentum = self.momentum_tolerance

        if i > self.iDistance:
            self.momentum = df['weightedAverage'].iloc[i] /  df['weightedAverage'].iloc[i - self.iDistance]

            df.loc[i, 'momentum'] = self.momentum

    def trainML(self, marketExchange, chartDataAnalyzer):
        doNothing = True

    def train(self,orderState, df, i):
        self.calculateMoment(i, orderState, df)

    def predict(self, orderState, df, i):

        self.calculateMoment(i , orderState, df)

        if self.momentum < self.momentum_tolerance:
            return self.buyCode


        return 0

    def plot(self, df, plt):

        if self.printPlot:
            super(MomentumIndicator, self).plot(df, plt)

            plt.show()


