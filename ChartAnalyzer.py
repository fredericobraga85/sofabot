from Poloniex import Poloniex
import Converter

class ChartAnalyzer:


    def init(self, currencyPair , start, end , period, btc):

        self.inital_btc = btc
        self.btc = btc
        self.actualCurrency = 0.0
        self.currencyPair = currencyPair
        self.piggy_safe = 0.0

        self.poloniex = Poloniex()
        self.df = self.poloniex.get_chart_data(currencyPair, start, end, period)
        self.feature_engineer()


    def calculateSupport(self, i):

        start_i = 0 if i < 3 else i - 3


        # if i > 10:
        #     if self.df['isUp'].iloc[-10:i].sum < -3:
        #         self.support = self.actual_price * 1.001
        #     else:
        #         if abs(self.df['open'].iloc[start_i:i].max() - self.df['close'].iloc[start_i:i].max()) < self.actual_price * 0.015:
        #             self.support = self.actual_price

        if abs(self.df['open'].iloc[start_i:i].max() - self.df['close'].iloc[start_i:i].min()) < self.actual_price * 0.025:
            self.support = self.actual_price
        # else:
        #     self.support = self.actual_price * 1.01

        self.df.loc[i, 'supportQuote'] = self.support

    #     self.support = self.df['weightedAverage'].iloc[-20].min()
    #
    # self.df.loc[i, 'supportQuote'] = self.support

    def calculateResistance(self, i):

        last_i = i - 1
        start_i = 0 if last_i < 3 else last_i - 3

        if abs(self.df['open'].iloc[start_i:i].max() - self.df['close'].iloc[start_i:i].max()) < self.actual_price * 0.015:
            self.resistance = self.actual_price

        self.df.loc[i, 'resistanceQuote'] = self.resistance



    def calculate_growth(self, series, index=1):
        return (series / series.shift(index) - 1) * 100

    def calculate_growth_1st_period(self, series):
        return (series / series[0] - 1) * 100

    def isUp(self, series, index=1):
        return (series > series.shift(index)).apply(Converter.convert_to_up_or_down)



    def feature_engineer(self):
        self.df['volumeGrowth'] = self.calculate_growth(self.df['volume'])
        self.df['quoteGrowth'] = self.calculate_growth(self.df['weightedAverage'])
        self.df['quoteGrowth1stPeriod'] = self.calculate_growth_1st_period(self.df['weightedAverage'])
        self.df['isUp'] = self.isUp(self.df['quoteGrowth1stPeriod'])

    def decide_action(self, gain, loss, loss_after_gain, gain_turbo_perc):

        self.gain = gain
        self.loss = loss
        self.loss_after_gain = loss_after_gain
        self.initial_gain = self.gain
        self.initial_loss = self.loss
        self.gain_turbo_perc = gain_turbo_perc
        self.support = 0.0

        self.inBuy = False
        self.buy_value = 0.0
        self.buy_index = 0
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

                    #last
                    # self.sell(len(self.df.index -1))
                    # self.send_to_piggy_safe()


    def getActualPrice(self, i):
        self.actual_price = self.df.iloc[i]['weightedAverage']
        # self.actual_price = self.poloniex.get_ticker(self, self.currencyPair)['last']

    def shouldBuy(self, i):

        buy = False

        if self.inBuy == False:

            if self.actual_price < self.support :
                buy = True


        return buy

    def buy(self, i):

        self.buy_value = self.actual_price
        self.sell_value = self.buy_value
        self.actualCurrency = (self.btc/self.buy_value) - (self.btc/self.buy_value * 0.00300)
        self.btc = 0
        self.buy_index = i
        self.df.loc[i, 'Buy'] = 1
        self.df.loc[i, 'btc'] = self.btc
        self.df.loc[i, 'actualCurrency'] = self.actualCurrency
        self.inBuy = True


    def shouldSell(self, i):

        if self.inBuy == True:

            if self.execute_stop_limit() == False:

                perc = self.actual_price / self.buy_value
                uhu = perc >= (1 + self.gain)

                if uhu:

                    self.gain = self.gain * self.gain_turbo_perc
                    self.set_stop_limit()

            else:

                return True


        return False

    def set_stop_limit(self):
        self.sell_value = self.actual_price
        self.loss = self.loss_after_gain

    def execute_stop_limit(self):

        self.perGain = self.actual_price / self.sell_value <= (1 - self.loss)
        return self.perGain

    def sell(self, i):

        if self.inBuy == True:

            self.sell_value = self.actual_price

            if self.loss == self.loss_after_gain:
                self.df.loc[i, 'perGain'] = (self.sell_value / self.buy_value - 1) * 100
                self.btc = (self.sell_value * self.actualCurrency) - (self.sell_value * self.actualCurrency * 0.00150)
                self.actualCurrency = 0
            else:
                self.df.loc[i, 'perGain'] = self.loss * 100 * -1
                self.btc = (self.buy_value * self.actualCurrency) - (self.buy_value * self.actualCurrency * self.loss) - (self.buy_value * self.actualCurrency * 0.00150)
                self.actualCurrency = 0



            self.df.loc[i, 'btc'] = self.btc
            self.df.loc[i, 'actualCurrency'] = self.actualCurrency
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
        self.df.loc[i, 'btc'] = self.btc
        self.df.loc[i, 'actualCurrency'] = self.actualCurrency

    def send_to_piggy_safe(self):
        if self.btc > self.inital_btc :
            self.piggy_safe = self.btc - self.inital_btc
            self.btc = self.inital_btc