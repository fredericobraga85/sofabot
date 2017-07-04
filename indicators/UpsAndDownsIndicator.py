

class UpsAndDownsIndicators:


    def trainML(self, marketExchange, chartDataAnalyzer):
        doNothing = True

    def train(self,orderState, df, i):
        doNothing = True

    def predict(self, orderState, df, i):

        if df[0:i]['isUp'].sum() < -3:
                return 1

        return 0




