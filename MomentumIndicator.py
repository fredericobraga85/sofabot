

class MomentumIndicator:


    def calculateMoment(self, i, orderState, df):

        self.momentum = df['weightedAverage'].iloc[i] - df['weightedAverage'].iloc[i - 3]

        df.loc[i, 'momentum'] = self.momentum

    def train(self,orderState, df, i):
        self.calculateMoment(i, orderState, df)

    def predict(self, orderState, df, i):

        self.calculateMoment(i , orderState, df)

        if self.momentum < 0:

                return 1

        return 0




