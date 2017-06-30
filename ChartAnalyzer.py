from Poloniex import Poloniex
import Converter
import Visualizer

class ChartAnalyzer:


    def init(self, currencyPair , start, end , period, btc):

        self.currencyPair = currencyPair
        self.btc = btc
        self.initial_btc = self.btc
        self.actualCurrency = 0.0
        self.piggy_safe = 0.0
        self.support = 0.0
        self.resistance = 0.0


        self.poloniex = Poloniex()
        self.df = self.poloniex.get_chart_data(currencyPair, start, end, period)
        self.feature_engineer()




    def calculateSupportAndResistance(self, i):

        dif_open_close_1 = abs(self.df['close'].iloc[i - 3] - self.df['open'].iloc[i - 3])
        dif_open_close_2 = abs(self.df['close'].iloc[i - 2] - self.df['open'].iloc[i - 2])
        dif_open_close_3 =     self.df['close'].iloc[i - 1] - self.df['open'].iloc[i - 1]

        if dif_open_close_1 + dif_open_close_2 > 0.000001:

            if dif_open_close_3 > 0 :
                if dif_open_close_3 > (dif_open_close_1 + dif_open_close_2) * self.support_resistance_dif_tolerance:
                    self.support = self.df['open'].iloc[i - 1]

                    if self.df['close'].iloc[i - 1] > self.resistance or self.resistance == 0:
                        self.resistance = self.df['close'].iloc[i - 1]

            elif dif_open_close_3 < 0:

                if abs(dif_open_close_3) > (dif_open_close_1 + dif_open_close_2) * self.support_resistance_dif_tolerance:
                    self.resistance = self.df['open'].iloc[i - 1]

                    if self.df['close'].iloc[i - 1] < self.support or self.support == 0:
                        self.support = self.df['close'].iloc[i - 1]


            if self.inBuy:
                if self.actual_price < self.support:
                    self.support = self.actual_price

                if self.actual_price > self.resistance:
                    self.resistance = self.actual_price


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

    def decide_action(self, objective_gain,limit_loss,  gain, loss, support_resistance_dif_tolerance, resistance_tolerance, buy_perc , sell_perc):

        self.objective_gain = objective_gain
        self.limit_loss = limit_loss
        self.gain = gain
        self.loss = loss
        self.support_resistance_dif_tolerance = support_resistance_dif_tolerance
        self.resistance_tolerance = resistance_tolerance
        self.buy_perc = buy_perc
        self.sell_perc = sell_perc

        self.reset_values()

        self.df['indexGain'] = 0
        self.df['perGain'] = 0
        self.df['buyValue'] = 0
        self.df['sellValue'] = 0
        self.df['gained'] = False
        self.df['Buy'] = 0

        for i, row in self.df.iterrows():
            if (i < len(self.df.index) - 1):

                self.getActualPrice(i)
                self.calculateSupportAndResistance(i)

                if i >= 16:
                    if self.buy(i):

                        self.df.loc[i, 'Buy'] = 1
                        self.df.loc[i, 'btc'] = self.btc
                        self.df.loc[i, 'buyValue'] = self.buy_value
                        self.df.loc[i, 'actualCurrency'] = self.actualCurrency

                    elif self.sell(i):

                        self.df.loc[i, 'perGain'] = (self.sell_value / self.buy_value - 1) * 100
                        self.df.loc[i, 'btc'] = self.btc
                        self.df.loc[i, 'actualCurrency'] = self.actualCurrency
                        self.df.loc[i, 'indexGain'] = i - self.buy_index
                        self.df.loc[i, 'buyValue'] = self.buy_value
                        self.df.loc[i, 'sellValue'] = self.sell_value
                        self.df.loc[i, 'gained'] = True
                        self.df.loc[i, 'Buy'] = 0

                        self.reset_values()

                        if self.reached_objective() or self.reached_limit_loss():
                            break

                    else:
                        self.wait(i)

                        if self.reached_objective() or self.reached_limit_loss():
                            break

                else:
                    self.wait(i)

                self.df.loc[i, 'supportQuote'] = self.support
                self.df.loc[i, 'resistanceQuote'] = self.resistance

                # self.printChart(self.df.iloc[i])

    def reached_objective(self):

        if self.btc == 0:

            current_btc = (self.actual_price * self.actualCurrency) - (self.actual_price * self.actualCurrency * self.sell_perc)

            if current_btc / self.initial_btc >= self.objective_gain:
                return True

        else:

            if self.btc / self.initial_btc >= self.objective_gain:
                return True

        return False

    def reached_limit_loss(self):

        if self.btc == 0:

            current_btc = (self.actual_price * self.actualCurrency) - (self.actual_price * self.actualCurrency * self.sell_perc)

            if current_btc / self.initial_btc <= self.limit_loss:
                return True

        else:

            if self.btc / self.initial_btc <= self.limit_loss:
                return True

        return False

    def getActualPrice(self, i):
        self.actual_price = self.df.iloc[i]['weightedAverage']
        # self.actual_price = self.poloniex.get_ticker(self, self.currencyPair)['last']

    def buy(self, i):

        if self.inBuy == False:

            if self.resistance != 0 and self.actual_price > self.resistance * self.resistance_tolerance:

                self.inBuy = True
                self.resistance_on_buy = self.resistance * self.resistance_tolerance
                self.buy_value = self.resistance_on_buy
                self.actualCurrency = (self.btc / self.buy_value) - (self.btc / self.buy_value * self.buy_perc)
                self.btc = 0
                self.buy_index = i

            return self.inBuy

        return  False

    def sell(self, i):

        if self.inBuy == True:

            if self.actual_price / self.buy_value > 1 + self.gain:
                self.sell_value = self.buy_value * (1 + self.gain)
            elif self.actual_price / self.buy_value < 1 - self.loss:
                self.sell_value = self.buy_value * (1 - self.loss)

            else:
                return False

            self.inBuy = False
            self.btc = (self.sell_value * self.actualCurrency) - (self.sell_value * self.actualCurrency * self.sell_perc)
            self.actualCurrency = 0

            return True

    def reset_values(self):
        self.inBuy = False
        self.perGain = 0
        self.buy_value = 0.0
        self.sell_value = 0.0
        self.buy_index = 0
        self.resistance_on_buy = 0.0



    def wait(self, i):

        self.df.loc[i, 'Buy'] = self.df.iloc[i - 1]['Buy']
        self.df.loc[i, 'btc'] = self.btc
        self.df.loc[i, 'buyValue'] = self.buy_value
        self.df.loc[i, 'sellValue'] = self.sell_value
        self.df.loc[i, 'actualCurrency'] = self.actualCurrency

        if self.inBuy:
            self.df.loc[i, 'perGain'] = ((self.actual_price / self.buy_value) - 1) * 100


    def send_to_piggy_safe(self):
        if self.btc > self.inital_btc :
            self.piggy_safe = self.btc - self.inital_btc
            self.btc = self.inital_btc


    def printChart(self, df):
        Visualizer.print_full(df[[
            'date',
            # 'timestamp'
            'close',
            # 'high',
            # 'low',
            'open',
            'supportQuote',
            'resistanceQuote',
            # 'quoteVolume',
            # 'volume',
            'isUp',
            'quoteGrowth1stPeriod',
            'weightedAverage',
            'buyValue',
            'sellValue',
            'perGain',
            'btc',
            'actualCurrency',
            'Buy',

        ]])