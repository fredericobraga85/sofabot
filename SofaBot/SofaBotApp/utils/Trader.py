import threading
import OrderStatus
from ..models import Exchange
from django.utils import timezone
from ..indicators.LoseAndWinIndicator import LoseAndWinIndicator
import time
import pdb;


class Trader(threading.Thread):
  
    # objective_gain = 10
    # limit_loss = 0
    gain = 0.03
    loss = 0.10
    
    indicators = [
        LoseAndWinIndicator(False, 1)
    ]

    class BotConfig:

        shouldBuyAccept = 1
        print_chart = True
        printOrders = False
        printRow = False
        printIteration = True
        printPlot = False

    def __init__(self, marketExchange, exchange_id):
        threading.Thread.__init__(self)
        self.marketExchange = marketExchange
        self.exchange_id = exchange_id
        self.botConfig = Trader.BotConfig()


    def run(self):
        print "Starting Trading" + self.name
        self.startTrading()
        print "Exiting Trading" + self.name
   

    def startTrading(self):

        self.isActive = True


        testcont = 144

        while self.isActive :

            e = Exchange.objects.get(id=self.exchange_id)
            orderState = e.orderstate_set.last()
            self.isActive = e.isActive

            if testcont == 144:
                self.test_df = self.marketExchange.returnChartData(e.currency_pair, "1500940800", "1501977600", "300")
                e.initial_btc = 1.0
                orderState.current_btc = 1.0

            if self.isActive and len(self.test_df) > testcont:


                testcont = testcont + 1
                self.df =  self.test_df[:testcont]


                if orderState.statusCode == OrderStatus.waiting_buying_opportunity :

                    print "waiting_buying_opportunity"

                    if self.indicators_predict_buy():

                        print "indicators_predict_buy"

                        self.sendBuyOrder()

                        e.orderstate_set.create(buy_value=0.0,
                                                sell_value=0.0,
                                                actual_price = self.getActualPrice(e.currency_pair),
                                                perGain=0.0,
                                                statusCode=OrderStatus.sent_buy_order,
                                                state_date=timezone.now(),
                                                current_btc=orderState.current_btc,
                                                current_coin=0.0,
                                                piggy=orderState.piggy)
                        e.save()

                    else:
                        e.orderstate_set.create(buy_value=0.0,
                                                sell_value=0.0,
                                                actual_price=self.getActualPrice(e.currency_pair),
                                                perGain=0.0,
                                                statusCode=orderState.statusCode,
                                                state_date=timezone.now(),
                                                current_btc=orderState.current_btc,
                                                current_coin=orderState.current_coin,
                                                piggy=orderState.piggy)
                        e.save()

                elif orderState.statusCode == OrderStatus.sent_buy_order:

                    print "sent_buy_order"

                    if self.buyOrderWasExecuted():

                        print "buyOrderWasExecuted"

                        buy_value = self.getBuyPrice(e.currency_pair)
                        current_coin = self.getCurrentCoin(e.currency_pair)

                        e.orderstate_set.create(buy_value=buy_value,
                                                sell_value=0.0,
                                                actual_price=self.getActualPrice(e.currency_pair),
                                                perGain=((self.getActualPrice(e.currency_pair) / buy_value - 1) * 100),
                                                statusCode=OrderStatus.waiting_sell_opporuntity,
                                                state_date=timezone.now(),
                                                current_btc=0.0,
                                                current_coin=orderState.current_btc / buy_value,
                                                piggy=orderState.piggy)
                        e.save()
                    else:
                        self.wait(e, orderState)

                elif orderState.statusCode == OrderStatus.waiting_sell_opporuntity:

                    print "waiting_sell_opporuntity"

                    if self.isGaining(orderState, e.currency_pair):
                        print "isGaining"

                        self.sendSellOrder(True)

                        e.orderstate_set.create(buy_value=orderState.buy_value,
                                                sell_value=0.0,
                                                actual_price=self.getActualPrice(e.currency_pair),
                                                perGain=((self.getActualPrice(e.currency_pair)/ buy_value - 1) * 100),
                                                statusCode=OrderStatus.sent_sell_order_is_gaining,
                                                state_date=timezone.now(),
                                                current_btc=0.0,
                                                current_coin=orderState.current_coin,
                                                piggy=orderState.piggy)
                        e.save()

                    elif self.isLosing(orderState, e.currency_pair):

                        print "isLosing"

                        self.sendSellOrder(False)

                        e.orderstate_set.create(buy_value=orderState.buy_value,
                                                sell_value=0.0,
                                                actual_price=self.getActualPrice(e.currency_pair),
                                                perGain=((self.getActualPrice(e.currency_pair) / buy_value - 1) * 100),
                                                statusCode=OrderStatus.sent_sell_order_is_losing,
                                                state_date=timezone.now(),
                                                current_btc=0.0,
                                                current_coin=orderState.current_coin,
                                                piggy=orderState.piggy)
                        e.save()

                    else:
                        self.wait(e, orderState)

                elif orderState.statusCode == OrderStatus.sent_sell_order_is_gaining or orderState.statusCode == OrderStatus.sent_sell_order_is_losing:

                    print "sent_sell_order_is_gaining || sent_sell_order_is_losing"

                    if self.sellOrderWasExecuted(orderState):

                        print "sellOrderWasExecuted"

                        current_btc = self.getCurrentBtc()
                        sell_value = self.getSellPrice()

                        result = sell_value * orderState.current_coin
                        piggy = orderState.piggy

                        if result > e.initial_btc:
                            piggy = orderState.piggy + (result - e.initial_btc)
                            result = e.initial_btc

                        # self.wallet.transferToPiggy()

                        e.orderstate_set.create(buy_value=orderState.buy_value,
                                                sell_value=sell_value,
                                                actual_price=self.getActualPrice(e.currency_pair),
                                                perGain = (( sell_value/buy_value - 1) * 100),
                                                statusCode=OrderStatus.waiting_buying_opportunity,
                                                state_date=timezone.now(),
                                                current_btc= result,
                                                current_coin=0.0,
                                                piggy=piggy)
                        e.save()

                    else:
                        self.wait(e, orderState)


                # time.sleep(1)


    def wait(self, e, orderState):

        print "wait"

        e.orderstate_set.create(buy_value=orderState.buy_value,
                                sell_value=orderState.sell_value,
                                actual_price=self.getActualPrice(e.currency_pair),
                                perGain=((self.getActualPrice(e.currency_pair) / orderState.buy_value - 1) * 100),
                                statusCode=orderState.statusCode,
                                state_date=timezone.now(),
                                current_btc=orderState.current_btc,
                                current_coin=orderState.current_coin,
                                piggy=orderState.piggy)
        e.save()

    def getActualPrice(self, currency_pair):

        if self.botConfig.printOrders:
            print 'Buscando preco atual...'

        print 'fake actual price'

        return self.df.iloc[-1]['close']
        # return self.marketExchange.returnLastPrice(currency_pair)

    def getBuyPrice(self, currency_pair):

        if self.botConfig.printOrders:
            print 'Buscando preco de compra...'
            print 'Setando Fake buy value...'

        # return self.marketExchange.returnLastPrice(currency_pair)

        print 'fake buy price'
        return self.df.iloc[-1]['close']

    def getCurrentCoin(self, currency_pair):

        if self.botConfig.printOrders:
            print 'Buscando current coin...'

        return self.marketExchange.returnLastPrice(currency_pair)

    def getCurrentBtc(self):

        if self.botConfig.printOrders:
            print 'Buscando current btc ...'

        print 'fake current btc'
        return 0.0

    def getSellPrice(self):

        if self.botConfig.printOrders:
            print 'Buscando preco de venda...'

        print 'fake sell price'
        return self.df.iloc[-1]['close']

    def isGaining(self, orderState, currency_pair):

        return self.getActualPrice(currency_pair) / orderState.buy_value >= 1 + self.gain

    def didGain(self, orderState):
        return orderState.sell_value / orderState.buy_value >= 1 + self.gain


    def isLosing(self, orderState, currency_pair):
        return self.getActualPrice(currency_pair) / orderState.buy_value  <= 1 - self.loss

    def didLose(self, orderState):
        return orderState.sell_value / orderState.buy_value <= 1 - self.loss

    def buyOrderWasExecuted(self):
        if self.botConfig.printOrders:
            print 'Verificando se ordem de compra foi realizada....'

        return True


    def sellOrderWasExecuted(self, orderState):

        if self.botConfig.printOrders:
            print 'Verificando se ordem de venda foi realizada....'
            print 'Setando Fake sell value...'

        if self.didGain(orderState):

            if self.botConfig.printOrders:
                print 'Ordem de venda de ganho realizada'


            return True

        elif self.didLose(orderState):

            if self.botConfig.printOrders:
                print 'Ordem de venda de perda realizada '

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
                print 'Enviando ordem de venda ganho '
            else:
                print 'Enviando ordem de venda perda '

    def indicators_predict_buy(self):

        shouldBuyCount = 0

        for indicator in self.indicators:

            shouldBuyCount = shouldBuyCount + indicator.predict(self.df)

        return True if shouldBuyCount >= 1 else False

