import pandas as pd
import pdb

class LoseAndWinIndicator:


    def __init__(self, printPlot=False, buyCode=1):

        self.index_to_predict = 144
        self.percentage_loss = 0.92
        self.df_list_gain = pd.DataFrame([])
        self.buy = 0

    def predict(self, actualPrice , df):

        # pdb.set_trace()

        if actualPrice > 0:
            if len(df) > self.index_to_predict:

                shouldBuy = actualPrice / df.iloc[len(df) - self.index_to_predict]

                if shouldBuy < self.percentage_loss:
                    self.buy = 1

                else:
                    self.buy = 0


        return self.buy






