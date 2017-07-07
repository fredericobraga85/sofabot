from indicators.Indicator import Indicator


class UpsAndDownsIndicators(Indicator):

    def __init__(self,printPlot=False, buyCode=1):
        self.printPlot = printPlot
        self.buyCode = buyCode

    def trainML(self, marketExchange, chartDataAnalyzer):
        doNothing = True

    def train(self,orderState, df, i):
        doNothing = True

    def predict(self, orderState, df, i):

        if df[0:i]['isUp'].sum() < -3:
                return self.buyCode

        return 0

    def plot(self, df, plt):

        if self.printPlot:
            super(UpsAndDownsIndicators, self).plot(df, plt)

            plt.show()




