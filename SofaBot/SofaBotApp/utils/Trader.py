import threading
import OrderStatus
from ..models import Exchange, OrderState, Question, Choice
from django.utils import timezone
from indicators.WinAndLoseIndicator import WinAndLoseIndicator


class Trader(threading.Thread):
  
    # objective_gain = 10
    # limit_loss = 0
    gain = 0.03
    loss = 0.10
    
    indicators = [
        WinAndLoseIndicator(False, 1)
    ]

    def __init__(self, marketExchange, exchange_id):
        threading.Thread.__init__(self)
        self.marketExchange = marketExchange
        self.exchange_id = exchange_id
        self.df = self.marketExchange.get_chart_data_()

        for indicator in self.indicators:
            indicator.trainML(self.marketExchange, self.chartDataAnalyzer)

    def run(self):
        print "Starting " + self.name
        self.startTrading()
        print "Exiting " + self.name
   

    def startTrading(self):

        self.isActive = True

        self.getActualPrice(i)

        self.train_inidicators(i)

        while self.isActive :

            e = Exchange.objects.get(id=self.exchange_id)
            orderState = e.orderstate_get.last()

            self.isActive = e.isActive

            if self.isActive:
                if orderState.statusCode == OrderStatus.waiting_buying_opportunity :

                    if self.indicators_predict_buy(i):
                        self.sendBuyOrder()

                        e.orderstate_set.create(buy_value=0.0,
                                                sell_value=0.0,
                                                perGain=0.0,
                                                statusCode=OrderStatus.sent_buy_order,
                                                statstate_date=timezone.now(),
                                                current_btc=orderState.current_btc,
                                                current_coin=0.0,
                                                piggy=orderState.piggy)
                        e.save()

                    else:
                        self.wait(e, orderState)

                elif orderState.statusCode == OrderStatus.sent_buy_order:

                    if self.buyOrderWasExecuted():

                        buy_value = self.getBuyPrice()
                        current_coin = self.getCurrentCoin()

                        e.orderstate_set.create(buy_value=buy_value,
                                                sell_value=0.0,
                                                perGain=0.0,
                                                statusCode=OrderStatus.waiting_sell_opporuntity,
                                                statstate_date=timezone.now(),
                                                current_btc=0.0,
                                                current_coin=current_coin,
                                                piggy=orderState.piggy)
                        e.save()
                    else:
                        self.wait(e, orderState)

                elif orderState.statusCode == OrderStatus.waiting_sell_opporuntity:

                    if self.isGaining():
                        self.sendSellOrder(True)

                        e.orderstate_set.create(buy_value=orderState.buy_value,
                                                sell_value=0.0,
                                                perGain=((self.getActualPrice(i)/ buy_value - 1) * 100),
                                                statusCode=OrderStatus.sent_sell_order_is_gaining,
                                                statstate_date=timezone.now(),
                                                current_btc=0.0,
                                                current_coin=orderState.current_coin,
                                                piggy=orderState.piggy)
                        e.save()

                    elif self.isLosing():

                        self.sendSellOrder(False)

                        e.orderstate_set.create(buy_value=orderState.buy_value,
                                                sell_value=0.0,
                                                perGain=((self.getActualPrice(i) / buy_value - 1) * 100),
                                                statusCode=OrderStatus.sent_sell_order_is_losing,
                                                statstate_date=timezone.now(),
                                                current_btc=0.0,
                                                current_coin=orderState.current_coin,
                                                piggy=orderState.piggy)
                        e.save()

                    else:
                        self.wait(e, orderState)

                elif orderState.statusCode == OrderStatus.sent_sell_order_is_gaining or orderState.statusCode == OrderStatus.sent_sell_order_is_losing:

                    if self.sellOrderWasExecuted():

                        current_btc = self.getCurrentBtc()
                        sell_value = self.getSellPrice()
                        self.wallet.transferToPiggy()

                        e.orderstate_set.create(buy_value=orderState.buy_value,
                                                sell_value=sell_value,
                                                perGain = (( sell_value/buy_value - 1) * 100),
                                                statusCode=OrderStatus.waiting_buying_opportunity,
                                                statstate_date=timezone.now(),
                                                current_btc=current_btc,
                                                current_coin=0.0,
                                                piggy=orderState.piggy)
                        e.save()

                    else:
                        self.wait(e, orderState)


    def wait(self, e, orderState):

        e.orderstate_set.create(buy_value=orderState.buy_value,
                                sell_value=orderState.sell_value,
                                perGain=orderState.perGain,
                                statusCode=orderState.statusCode,
                                statstate_date=timezone.now(),
                                current_btc=orderState.current_btc,
                                current_coin=orderState.current_coin,
                                piggy=orderState.piggy)
        e.save()

    # def reached_objective(self):
    #
    #     if self.orderState.inBuy == True:
    #
    #         current_btc = (self.orderState.actual_price * self.wallet.getDigitalCurrency(self.orderState.toDigitalCurr) - (self.orderState.actual_price * self.wallet.getDigitalCurrency(self.orderState.toDigitalCurr) * self.marketExchange.getActiveSellFeePerc()))
    #
    #         if current_btc / self.wallet.initialDeposit >= self.objective_gain:
    #             return True
    #
    #     else:
    #
    #         if self.wallet.getDigitalCurrency(self.orderState.fromDigitalCurr) / self.wallet.initialDeposit >= self.objective_gain:
    #             return True
    #
    #     return False
    #
    # def reached_limit_loss(self):
    #
    #     if self.orderState.inBuy:
    #
    #         current_btc = (self.orderState.actual_price * self.wallet.getDigitalCurrency(self.orderState.toDigitalCurr)) - (self.orderState.actual_price * self.wallet.getDigitalCurrency(self.orderState.toDigitalCurr) * self.marketExchange.getActiveSellFeePerc())
    #
    #         if current_btc / self.wallet.initialDeposit <= self.limit_loss:
    #             return True
    #
    #     else:
    #
    #         if self.wallet.getDigitalCurrency(self.orderState.fromDigitalCurr)  / self.wallet.initialDeposit <= self.limit_loss:
    #             return True
    #
    #     return False

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

    def getCurrentCoin(self):

        if self.botConfig.printOrders:
            print 'Buscando current coin...'

        self.orderState.buy_value = self.orderState.actual_price

    def getCurrentBtc(self):

        if self.botConfig.printOrders:
            print 'Buscando current btc ...'

    def getSellPrice(self):

        if self.botConfig.printOrders:
            print 'Buscando preco de venda...'

    def isGaining(self):
        return self.orderState.getGainPerc() >= 1 + self.gain

    def didGain(self):
        return self.orderState.getGainPerc() >= 1 + self.gain


    def isLosing(self):
        return self.orderState.getGainPerc() <= 1 - self.loss

    def didLose(self):
        return self.orderState.getGainPerc() <= 1 - self.loss

    def buyOrderWasExecuted(self):
        if self.botConfig.printOrders:
            print 'Verificando se ordem de compra foi realizada....'

        return True


    def sellOrderWasExecuted(self):

        if self.botConfig.printOrders:
            print 'Verificando se ordem de venda foi realizada....'
            print 'Setando Fake sell value...'

        # if self.reached_objective() or self.reached_limit_loss():
        #
        #     self.orderState.sell_value = self.orderState.actual_price
        #
        #     if self.botConfig.printOrders:
        #         print 'Ordem de venda realizada alcance objetivo ' + str(
        #             self.orderState.sell_value) + ' Preco atual ' + str(self.orderState.actual_price)
        #
        #     return True
        #
        # el

        if self.didGain():

            if self.orderState.sell_order_gain_active:
                self.orderState.sell_value = self.orderState.buy_value * (1 + self.gain)

                if self.botConfig.printOrders:
                    print 'Ordem de venda de ganho realizada ' + str(
                        self.orderState.sell_value) + ' Preco atual ' + str(self.orderState.actual_price)
            else:
                self.orderState.sell_value = self.orderState.actual_price

                if self.botConfig.printOrders:
                    print 'Ordem de venda realizada ganho emergencial ' + str(
                        self.orderState.sell_value) + ' Preco atual ' + str(self.orderState.actual_price)

            # self.gain = self.initial_gain

            return True

        elif self.didLose():



            if self.orderState.sell_order_loss_active:
                self.orderState.sell_value = self.orderState.buy_value * (1 - self.loss)

                if self.botConfig.printOrders:
                    print 'Ordem de venda de perda realizada ' + str(
                        self.orderState.sell_value) + ' Preco atual ' + str(self.orderState.actual_price)
            else:
                self.orderState.sell_value = self.orderState.actual_price

                if self.botConfig.printOrders:
                    print 'Ordem de venda realizada perda emergencial ' + str(
                        self.orderState.sell_value) + ' Preco atual ' + str(self.orderState.actual_price)


            # self.gain = abs(1 - self.orderState.sell_value/self.orderState.buy_value) + self.gain

            return True

        return False

    def cancelLastSellOrder(self):
        if self.botConfig.printOrders:
            print 'Ordem de venda anterior cancelada'

    def sendBuyOrder(self):

        if self.botConfig.printOrders:
            print 'Enviando ordem de compra...'


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

        return True if shouldBuyCount >= 1 else False

    def pre_setup_indicators(self, df):
        for indicator in self.indicators:
            indicator.preSetup(df)

    def train_inidicators(self, i):
        for indicator in self.indicators:
            indicator.train(self.orderState, self.df, i)
