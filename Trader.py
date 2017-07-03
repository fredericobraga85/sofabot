
from OrderState import OrderState
from Poloniex import Poloniex
import Visualizer
from ChartDataAnalyzer import ChartDataAnalyzer
from Wallet import Wallet

class Trader:


    def __init__(self, indicators, marketExchange , botConfig):

        self.indicators        = indicators
        self.marketExchange    = marketExchange
        self.chartDataAnalyzer = ChartDataAnalyzer()
        self.botConfig = botConfig

        self.df = self.marketExchange.get_chart_data()
        self.df = self.chartDataAnalyzer.run_feature_engineer(self.df)


    def startTrading(self, btc , currencyPair, objective_gain, limit_loss, gain, loss):

        self.orderState = OrderState(currencyPair)
        self.wallet     = Wallet(self.orderState.fromDigitalCurr, self.orderState.toDigitalCurr, btc)

        self.objective_gain = objective_gain
        self.limit_loss     = limit_loss
        self.gain           = gain
        self.loss           = loss
        self.stop = False

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

                        self.getActualPrice(i)

                        if self.reached_objective() or self.reached_limit_loss():
                            return False
                        elif self.indicators_predict_buy(i):
                            self.sendBuyOrder()
                            self.orderState.setBuyOrderStatus(True)
                        else:
                            self.wait(i)

                    elif self.orderState.waitingForBuyOrderToBeExecuted():

                        if self.buyOrderWasExecuted():

                            self.getBuyPrice()
                            self.orderState.setInBuyStatus()
                            self.wallet.exchange(Wallet.BTC, self.orderState.toDigitalCurr,self.orderState.buy_value, self.marketExchange.getActiveBuyFeePerc())

                            self.df.loc[i, 'Buy'] = 1
                            self.df.loc[i, 'btc'] = self.wallet.wallet[Wallet.BTC]
                            self.df.loc[i, 'buyValue'] = self.orderState.buy_value
                            self.df.loc[i, 'actualCurrency'] = self.wallet.wallet[self.orderState.toDigitalCurr]

                    elif self.orderState.waitingForSellOpportunity():

                        if self.isGaining():

                            self.sendSellOrder(True)
                            self.orderState.setSellOrderStatus(True)

                        elif self.isLosing():

                            self.sendSellOrder(False)
                            self.orderState.setSellOrderStatus(True)

                        else:

                            self.wait(i)

                    elif self.orderState.waitingForSellOrderToBeExecuted():

                        if self.sellOrderWasExecuted():

                            self.getSellPrice()
                            self.orderState.setInSellStatus()
                            self.wallet.exchange(self.orderState.fromDigitalCurr, Wallet.BTC, self.orderState.sell_value, self.marketExchange.getActiveSellFeePerc())

                            self.df.loc[i, 'perGain'] = (self.orderState.sell_value / self.orderState.buy_value - 1) * 100
                            self.df.loc[i, 'btc'] = self.wallet.wallet[self.orderState.fromDigitalCurr]
                            self.df.loc[i, 'actualCurrency'] = self.wallet.wallet[self.orderState.toDigitalCurr]
                            self.df.loc[i, 'buyValue'] = self.orderState.buy_value
                            self.df.loc[i, 'sellValue'] = self.orderState.sell_value
                            self.df.loc[i, 'gained'] = True
                            self.df.loc[i, 'Buy'] = 0

                            self.orderState.resetValues()

                if self.botConfig.printRow:
                    self.printChart(self.df.iloc[i])

    def reached_objective(self):

        if self.orderState.inBuy == True:

            current_btc = (self.orderState.actual_price * self.wallet.getDigitalCurrency(self.orderState.toDigitalCurr) - (self.orderState.actual_price * self.wallet.getDigitalCurrency(self.orderState.toDigitalCurr) * self.marketExchange.getActiveSellFeePerc()))

            if current_btc / self.wallet.initialDeposit >= self.objective_gain:
                self.stop = False

        else:

            if self.wallet.getDigitalCurrency(self.orderState.fromDigitalCurr) / self.wallet.initialDeposit >= self.objective_gain:
                self.stop = True

        return self.stop

    def reached_limit_loss(self):

        if self.orderState.inBuy:

            current_btc = (self.orderState.actual_price * self.wallet.getDigitalCurrency(self.orderState.toDigitalCurr)) - (self.orderState.actual_price * self.wallet.getDigitalCurrency(self.orderState.toDigitalCurr) * self.marketExchange.getActiveSellFeePerc())

            if current_btc / self.wallet.initialDeposit <= self.limit_loss:
                return True

        else:

            if self.wallet.getDigitalCurrency(self.orderState.fromDigitalCurr)  / self.wallet.initialDeposit <= self.limit_loss:
                return True

        return False

    def getActualPrice(self, i):

        if self.botConfig.printOrders:
            print 'Buscando preco atual...'

        self.orderState.actual_price = self.df.iloc[i]['weightedAverage']
        # self.actual_price = self.poloniex.get_ticker(self, self.currencyPair)['last']

    def getBuyPrice(self):

        if self.botConfig.printOrders:
            print 'Buscando preco de compra...'

        print 'Setando Fake buy value...'
        self.orderState.buy_value = self.orderState.actual_price

    def getSellPrice(self):


        if self.botConfig.printOrders:
            print 'Buscando preco de venda...'

        print 'Setando Fake sell value...'
        if self.reached_objective() or self.reached_limit_loss():

            self.orderState.sell_value = self.orderState.actual_price

            if self.botConfig.printOrders:
                print 'Ordem de venda realizada alcance objetivo ' + str(self.orderState.sell_value) + ' Preco atual ' + str(self.orderState.actual_price)

        elif self.didGain():

            if self.orderState.sell_order_gain_active:
                self.orderState.sell_value = self.orderState.buy_value * (1 + self.gain)

                if self.botConfig.printOrders:
                    print 'Ordem de venda de ganho realizada ' + str(self.orderState.sell_value) + ' Preco atual ' + str(self.orderState.actual_price)
            else:
                self.orderState.sell_value = self.orderState.actual_price

                if self.botConfig.printOrders:
                    print 'Ordem de venda realizada ganho emergencial ' + str(self.orderState.sell_value) + ' Preco atual ' + str(self.orderState.actual_price)

        elif self.didLose():

            if self.orderState.sell_order_loss_active:
                self.orderState.sell_value = self.orderState.buy_value * (1 - self.loss)

                if self.botConfig.printOrders:
                    print 'Ordem de venda de perda realizada ' + str(self.orderState.sell_value) + ' Preco atual ' + str(self.orderState.actual_price)
            else:
                self.orderState.sell_value = self.orderState.actual_price

                if self.botConfig.printOrders:
                    print 'Ordem de venda realizada perda emergencial ' + str(self.orderState.sell_value) + ' Preco atual ' + str(self.orderState.actual_price)



    def wait(self, i):

        self.df.loc[i, 'Buy'] = self.df.iloc[i - 1]['Buy']
        self.df.loc[i, 'btc'] = self.wallet.wallet[self.orderState.fromDigitalCurr]
        self.df.loc[i, 'buyValue'] = self.orderState.buy_value
        self.df.loc[i, 'sellValue'] = self.orderState.sell_value
        self.df.loc[i, 'actualCurrency'] = self.wallet.wallet[self.orderState.toDigitalCurr]


    def isGaining(self):
        return self.orderState.getGainPerc()> 1 and self.orderState.getGainPerc() < 1 + self.gain

    def didGain(self):
        return self.orderState.getGainPerc() > 1 + self.gain


    def isLosing(self):
        return self.orderState.getGainPerc() < 1 and  self.orderState.getGainPerc() > 1 - self.loss

    def didLose(self):
        return self.orderState.getGainPerc() < 1 - self.loss

    def buyOrderWasExecuted(self):
        if self.botConfig.printOrders:
            print 'Verificando se ordem de compra foi realizada....'

        return True


    def sellOrderWasExecuted(self):
        if self.botConfig.printOrders:
            print 'Verificando se ordem de venda foi realizada....'

        return True

    def cancelLastSellOrder(self):
        if self.botConfig.printOrders:
            print 'Ordem de venda anterior cancelada'

    def sendBuyOrder(self):

        if self.botConfig.printOrders:
            print 'Enviando ordem de comprea...'


    def sendSellOrder(self, gain):

        self.cancelLastSellOrder()

        if self.botConfig.printOrders:
            if gain:
                print 'Enviando ordem de venda ganho ' + str(self.orderState.buy_value * (1 + self.gain)) + ' Preco atual ' + str(self.orderState.actual_price)
            else:
                print 'Enviando ordem de venda perda ' + str(self.orderState.buy_value * (1 - self.loss)) + ' Preco atual ' + str(self.orderState.actual_price)

    def indicators_predict_buy(self, i):

        shouldBuyCount = 0

        for indicator in self.indicators:
            shouldBuyCount = shouldBuyCount + indicator.predict(self.orderState, self.df, i)

        return True if shouldBuyCount > 0 else False



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