import bot
from OrderState import OrderState
from Poloniex import Poloniex
import Visualizer
import ChartDataAnalyzer
import Wallet

class Trader:


    def __init__(self,btc, indicators, marketExchange):

        self.wallet            = Wallet(Wallet.BTC,btc)
        self.indicators        = indicators
        self.chartDataAnalyzer = ChartDataAnalyzer()

        self.df = marketExchange.get_chart_data()
        self.df = self.chartDataAnalyzer.run_feature_engineer(self.df)


    def startTrading(self, currencyPair, objective_gain, limit_loss, gain, loss):

        self.orderState = OrderState(currencyPair)

        self.objective_gain = objective_gain
        self.limit_loss     = limit_loss
        self.gain           = gain
        self.loss           = loss

        self.df['indexGain'] = 0
        self.df['perGain'] = 0
        self.df['buyValue'] = 0
        self.df['sellValue'] = 0
        self.df['gained'] = False
        self.df['Buy'] = 0

        for i, row in self.df.iterrows():

            if (i < len(self.df.index) - 1):

                self.getActualPrice(i)

                if i >= 16:

                    if self.orderState.waitingForBuyOpportunity():

                        if self.reached_objective() or self.reached_limit_loss():
                            return False
                        elif self.indicators_predict_buy():
                            self.sendBuyOrder()
                            self.orderState.setBuyOrder(True)

                    elif self.orderState.waitingForBuyOrderToBeExecuted():

                        if self.buyOrderWasExecuted():

                            self.orderState.setInBuyStatus()
                            self.wallet.exchange(Wallet.BTC, self.orderState.digialCurrency,self.orderState.actual_price, self.buy_perc)

                            self.df.loc[i, 'Buy'] = 1
                            self.df.loc[i, 'btc'] = self.wallet[Wallet.BTC]
                            self.df.loc[i, 'buyValue'] = self.orderState.buy_value
                            self.df.loc[i, 'actualCurrency'] = self.actualCurrency

                    elif self.orderState.waitingForSellOpportunity():

                        if self.isGaining():

                            self.sendSellOrder(True)
                            self.orderState.setSellOrder(True)

                        elif self.isLosing():

                            self.sendSellOrder(False)
                            self.orderState.setSellOrder(True)


                    elif self.orderState.waitingForSellOrderToBeExecuted():

                        self.df.loc[i, 'perGain'] = (self.sell_value / self.buy_value - 1) * 100
                        self.df.loc[i, 'btc'] = self.btc
                        self.df.loc[i, 'actualCurrency'] = self.actualCurrency
                        self.df.loc[i, 'indexGain'] = i - self.buy_index
                        self.df.loc[i, 'buyValue'] = self.buy_value
                        self.df.loc[i, 'sellValue'] = self.sell_value
                        self.df.loc[i, 'gained'] = True
                        self.df.loc[i, 'Buy'] = 0

                        self.reset_values()

                    else:
                        self.wait(i)

                    if self.stop:
                        break

                else:
                    self.wait(i)

                self.df.loc[i, 'supportQuote'] = self.support
                self.df.loc[i, 'resistanceQuote'] = self.resistance

                if bot.printRow:
                    self.printChart(self.df.iloc[i])

    def reached_objective(self):

        if self.inBuy:

            current_btc = (self.actual_price * self.actualCurrency) - (self.actual_price * self.actualCurrency * self.sell_perc)

            if current_btc / self.initial_btc >= self.objective_gain:
                self.stop = False

        else:

            if self.btc / self.initial_btc >= self.objective_gain:
                self.stop = True

        return self.stop

    def reached_limit_loss(self):

        if self.inBuy:

            current_btc = (self.actual_price * self.actualCurrency) - (self.actual_price * self.actualCurrency * self.sell_perc)

            if current_btc / self.initial_btc <= self.limit_loss:
                return True

        else:

            if self.btc / self.initial_btc <= self.limit_loss:
                return True

        return False

    def getActualPrice(self, i):

        if bot.printOrders:
            print 'Buscando preço atual...'

        self.orderState.actual_price = self.df.iloc[i]['weightedAverage']
        # self.actual_price = self.poloniex.get_ticker(self, self.currencyPair)['last']


    def sell(self, i):

        if self.orderState.inBuy == True:

            if self.reached_objective() or self.reached_limit_loss():

                self.sell_value = self.actual_price

                if bot.printOrders:
                    print 'Ordem de venda realizada alcance objetivo '+ str(self.sell_value) + ' Preco atual ' +  str(self.actual_price)

            elif self.didGain():

                if self.sell_order_gain_active:
                    self.sell_value = self.buy_value  * (1 + self.gain)

                    if bot.printOrders:
                        print 'Ordem de venda de ganho realizada ' + str(self.sell_value) + ' Preco atual ' + str(self.actual_price)
                else:
                    self.sell_value = self.actual_price

                    if bot.printOrders:
                        print 'Ordem de venda realizada ganho emergencial ' + str(self.sell_value) + ' Preco atual ' + str(self.actual_price)

            elif self.didLose():

                if self.sell_order_loss_active:
                    self.sell_value = self.buy_value * (1 - self.loss)

                    if bot.printOrders:
                        print 'Ordem de venda de perda realizada ' + str(self.sell_value) + ' Preco atual ' + str(self.actual_price)
                else:
                    self.sell_value = self.actual_price

                    if bot.printOrders:
                        print 'Ordem de venda realizada perda emergencial ' + str(self.sell_value) + ' Preco atual ' + str(self.actual_price)


            else:
                return False

            self.inBuy = False
            self.btc = (self.sell_value * self.actualCurrency) - (self.sell_value * self.actualCurrency * self.sell_perc)
            self.actualCurrency = 0

            return True


    def wait(self, i):

        self.df.loc[i, 'Buy'] = self.df.iloc[i - 1]['Buy']
        self.df.loc[i, 'btc'] = self.btc
        self.df.loc[i, 'buyValue'] = self.buy_value
        self.df.loc[i, 'sellValue'] = self.sell_value
        self.df.loc[i, 'actualCurrency'] = self.actualCurrency

        if self.inBuy:
            self.df.loc[i, 'perGain'] = ((self.actual_price / self.buy_value) - 1) * 100

    def isGaining(self):
        return self.orderState.getGainPerc()> 1 and self.orderState.getGainPerc() < 1 + self.gain

    def didGain(self):
        return self.orderState.getGainPerc() > 1 + self.gain


    def isLosing(self):
        return self.orderState.getGainPerc() < 1 and  self.orderState.getGainPerc() > 1 - self.loss

    def didLose(self):
        return self.orderState.getGainPerc() < 1 - self.loss

    def buyOrderWasExecuted(self):
        if bot.printOrders:
            print 'Verificando se ordem de compra foi realizada....'

        return True


    def sellOrderWasExecuted(self):
        if bot.printOrders:
            print 'Verificando se ordem de venda foi realizada....'

        return True

    def cancelLastSellOrder(self):
        if bot.printOrders:
            print 'Ordem de venda anterior cancelada'

    def sendBuyOrder(self):

        if bot.printOrders:
            print 'Enviando ordem de comprea...'


    def sendSellOrder(self, gain):

        self.cancelLastSellOrder()

        if bot.printOrders:
            if gain:
                print 'Enviando ordem de venda ganho ' + str(self.orderState.buy_value * (1 + self.orderState.gain)) + ' Preco atual ' + str(self.orderState.actual_price)
            else:
                print 'Enviando ordem de venda perda ' + str(self.orderState.buy_value * (1 - self.orderState.loss)) + ' Preco atual ' + str(self.orderState.actual_price)

    def indicators_predict_buy(self):

        shouldBuyCount = 0

        for indicator in self.indicators:
            shouldBuyCount = shouldBuyCount + indicator.predict()

        return True if shouldBuyCount > 0 else False


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