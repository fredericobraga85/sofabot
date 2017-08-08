import pandas as pd
import pdb

class LoseAndWinIndicator:


    def __init__(self, printPlot=False, buyCode=1):

        self.index_to_predict = 144
        self.percentage_loss = 0.92
        self.df_list_gain = pd.DataFrame([])
        self.buy = 0

    def predict(self, df):

        # pdb.set_trace()

        if len(df) > self.index_to_predict:

            shouldBuy = df['close'].iloc[len(df) - 1] / df['close'].iloc[len(df) - self.index_to_predict]

            if shouldBuy < self.percentage_loss:
                self.buy = 1

            else:
                self.buy = 0


        return self.buy






