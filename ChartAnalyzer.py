
class ChartAnalyzer:



    def calculateSupport(self, i):

        if self.df.iloc[i - 3]['isUp'] == False and self.df.iloc[i - 2]['isUp'] == False and self.df.iloc[i - 1]['isUp'] == True and self.df.iloc[i]['isUp'] == True:
            self.support = self.df.iloc[i - 2]['weightedAverage']
            self.df.loc[i, 'supportQuote'] = self.support


    def calculateResistance(self, i):

        if self.df.iloc[i - 1]['isUp'] == True and self.df.iloc[i]['isUp'] == False:
            self.resistance = self.df.iloc[i - 1]['weightedAverage']

            self.df.loc[i, 'resistanceQuote'] = self.resistance

    def calculate_growth(self, series, index=1):
        return (series / series.shift(index) - 1) * 100

    def calculate_growth_1st_period(self, series):
        return (series / series[0] - 1) * 100

    def isUp(self, series, index=1):
        return series > series.shift(index)


    def feature_engineer(self):
        self.df['volumeGrowth'] = self.calculate_growth(self.df['volume'])
        self.df['quoteGrowth'] = self.calculate_growth(self.df['weightedAverage'])
        self.df['quoteGrowth'] = self.calculate_growth(self.df['weightedAverage'])
        self.df['quoteGrowth1stPeriod'] = self.calculate_growth_1st_period(self.df['weightedAverage'])
        self.df['isUp'] = self.isUp(self.df['quoteGrowth1stPeriod'])

    def decide_action(self, gain=0.01, loss=0.01):

        self.gain = gain
        self.loss = loss
        self.initial_gain = self.gain
        self.initial_loss = self.loss

        self.inBuy = False
        self.buy_value = 0.0
        self.buy_index = 0
        self.support = self.df.iloc[0]['weightedAverage']
        self.resistance = 0.0

        self.df['indexGain'] = 0
        self.df['perGain'] = 0
        self.df['buyValue'] = 0
        self.df['gained'] = False
        self.df['Buy'] = 0

        for i, row in self.df.iterrows():
            if i > 0 and (i < len(self.df.index) - 1):


                self.getActualPrice(i)
                self.calculateSupport(i)
                self.calculateResistance(i)

                if self.shouldBuy(i):

                    self.buy(i)

                elif self.shouldSell(i):

                    self.sell(i)

                else:
                    self.wait(i)



    def getActualPrice(self, i):
        self.actual_price = self.df.iloc[i]['weightedAverage']


    def shouldBuy(self, i):

        buy = False

        if self.inBuy == False:

            if self.df.iloc[i - 2]['isUp'] == False:
                if self.df.iloc[i - 1]['isUp'] == False:
                    if self.df.iloc[i]['isUp'] == True:
                        if self.df.iloc[i - 1]['weightedAverage'] < self.support:
                            buy = True
                elif self.df.iloc[i - 1]['isUp'] == True:
                    if self.df.iloc[i]['isUp'] == True:
                        if self.actual_price > (self.support + (self.support * self.gain)):
                            buy = True

        return buy

    def buy(self, i):

        self.buy_value = self.actual_price
        self.sell_value = self.buy_value
        self.buy_index = i
        self.df.loc[i, 'Buy'] = 1
        self.inBuy = True


    def shouldSell(self, i):

        if self.inBuy == True:

            if self.execute_stop_limit() == False:

                perc = self.actual_price / self.buy_value
                uhu = perc >= (1 + self.gain)

                if uhu:

                    self.gain = self.gain * 1.5
                    self.set_stop_limit()

            else:
                return True



        return False

    def set_stop_limit(self):
        self.sell_value = self.actual_price
        self.loss = 0.0

    def execute_stop_limit(self):

        self.perGain = self.actual_price / self.sell_value <= (1 - self.loss)
        return self.perGain

    def sell(self, i):

        if self.loss == 0.0:
            self.df.loc[i, 'perGain'] = (self.sell_value / self.buy_value - 1) * 100
        else:
            self.df.loc[i, 'perGain'] = self.loss * 100 * -1

        self.df.loc[i, 'indexGain'] = i - self.buy_index
        self.df.loc[i, 'buyValue'] = self.buy_value
        self.df.loc[i, 'gained'] = True
        self.df.loc[i, 'Buy'] = 0
        self.inBuy = False
        self.perGain = 0
        self.buy_value = 0.0
        self.buy_index = 0
        self.gain = self.initial_gain
        self.loss = self.initial_loss

    def wait(self, i):

        self.df.loc[i, 'Buy'] = self.df.iloc[i - 1]['Buy']
