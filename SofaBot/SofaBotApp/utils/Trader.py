import threading
import OrderStatus
from ..utils.MarketThread import MarketThread
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
        printOrders = True


    def __init__(self, exchange_id):
        threading.Thread.__init__(self)
        self.exchange_id = exchange_id
        self.botConfig = Trader.BotConfig()


    def run(self):
        print "Starting Trading" + self.name
        self.startTrading()
        print "Exiting Trading" + self.name
   

    def startTrading(self):

        e = Exchange.objects.get(id=self.exchange_id)

        market = MarketThread(1, "Thread-" + e.currency_pair, e.currency_pair)
        market.start()

        self.isActive = True

        testcont = 144

        try:
            while self.isActive :


                e = Exchange.objects.get(id=self.exchange_id)
                orderState = e.orderstate_set.last()

                self.isActive = e.isActive

                if testcont == 144:
                    self.test_df = market.marketExchange.returnChartData(e.currency_pair, "1500940800", "1501977600", "300")
                    e.initial_btc = 1.0
                    orderState.current_btc = 1.0

                if self.isActive and len(self.test_df) > testcont:


                    testcont = testcont + 1
                    self.df =  self.test_df[:testcont]


                    if orderState.statusCode == OrderStatus.waiting_buying_opportunity :

                        print "waiting_buying_opportunity"

                        if self.indicators_predict_buy(market):

                            print "indicators_predict_buy"

                            orderNumber = self.sendBuyOrder(market, e, orderState)

                            if orderNumber != None:

                                e.orderstate_set.create(orderNumber = orderNumber,
                                                        buy_value=0.0,
                                                        sell_value=0.0,
                                                        actual_price = market.getLastAskPrice(),
                                                        perGain=0.0,
                                                        statusCode=OrderStatus.sent_buy_order,
                                                        state_date=timezone.now(),
                                                        current_btc=orderState.current_btc,
                                                        current_coin=0.0,
                                                        piggy=orderState.piggy,
                                                        currency_pair=e.currency_pair)
                                e.save()



                        else:
                            e.orderstate_set.create(
                                                    orderNumber=0,
                                                    buy_value=0.0,
                                                    sell_value=0.0,
                                                    actual_price=market.getLastAskPrice(),
                                                    perGain=0.0,
                                                    statusCode=orderState.statusCode,
                                                    state_date=timezone.now(),
                                                    current_btc=orderState.current_btc,
                                                    current_coin=orderState.current_coin,
                                                    piggy=orderState.piggy,
                                                    currency_pair=e.currency_pair)
                            e.save()

                    elif orderState.statusCode == OrderStatus.sent_buy_order:

                        print "sent_buy_order"

                        actual_price = market.getLastAskPrice()

                        if self.buyOrderWasExecuted():

                            print "buyOrderWasExecuted"

                            buy_value = self.getBuyPrice(e.currency_pair)
                            current_coin = self.getCurrentCoin(market)

                            orderNumber = self.sendSellOrder(True, market, buy_value * (1 + self.gain))

                            e.orderstate_set.create(orderNumber=orderState.orderNumber,
                                                    buy_value=buy_value,
                                                    sell_value=0.0,
                                                    actual_price=actual_price,
                                                    perGain=((actual_price / buy_value - 1) * 100),
                                                    statusCode=OrderStatus.waiting_sell_opporuntity,
                                                    state_date=timezone.now(),
                                                    current_btc=0.0,
                                                    current_coin=orderState.current_btc / buy_value,
                                                    piggy=orderState.piggy,
                                                    currency_pair=e.currency_pair)
                            e.save()
                        else:

                            market.marketExchange.cancel(e, orderState.orderNumber)

                            e.orderstate_set.create(orderNumber=0,
                                                    buy_value=0.0,
                                                    sell_value=0.0,
                                                    actual_price=actual_price,
                                                    perGain=0.0,
                                                    statusCode=OrderStatus.waiting_buying_opportunity,
                                                    state_date=timezone.now(),
                                                    current_btc=orderState.current_btc,
                                                    current_coin=0.0,
                                                    piggy=orderState.piggy,
                                                    currency_pair=e.currency_pair)
                            e.save()

                    elif orderState.statusCode == OrderStatus.waiting_sell_opporuntity:

                        print "waiting_sell_opporuntity"

                        if self.isLosing(orderState, market):

                            print "isLosing"

                            orderNumber = self.sendSellOrder(False, market, market.getLastBidPrice() * 0.99995)
                            actual_price = market.getLastAskPrice()

                            e.orderstate_set.create(orderNumber = orderNumber,
                                                    buy_value=orderState.buy_value,
                                                    sell_value=0.0,
                                                    actual_price=actual_price,
                                                    perGain=((actual_price / orderState.buy_value - 1) * 100),
                                                    statusCode=OrderStatus.sent_sell_order_is_losing,
                                                    state_date=timezone.now(),
                                                    current_btc=0.0,
                                                    current_coin=orderState.current_coin,
                                                    piggy=orderState.piggy,
                                                    currency_pair=e.currency_pair)
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


                            e.orderstate_set.create(orderNumber = orderState.orderNumber,
                                                    buy_value=orderState.buy_value,
                                                    sell_value=sell_value,
                                                    actual_price=market.getLastAskPrice(),
                                                    perGain = (( sell_value/orderState.buy_value - 1) * 100),
                                                    statusCode=OrderStatus.waiting_buying_opportunity,
                                                    state_date=timezone.now(),
                                                    current_btc= result,
                                                    current_coin=0.0,
                                                    piggy=piggy,
                                                    currency_pair=e.currency_pair)
                            e.save()

                        else:
                            self.wait(e, orderState)


                    time.sleep(1)

            market.stopTicker()
        except:
            market.stopTicker()
            e = Exchange.objects.get(id=self.exchange_id)
            e.isActive = False
            e.save


    def wait(self, e, orderState, market):

        print "wait"

        actual_price = market.getLastAskPrice()

        e.orderstate_set.create(orderNumber=orderState.orderNumber,
                                buy_value=orderState.buy_value,
                                sell_value=orderState.sell_value,
                                actual_price=actual_price,
                                perGain=((actual_price / orderState.buy_value - 1) * 100),
                                statusCode=orderState.statusCode,
                                state_date=timezone.now(),
                                current_btc=orderState.current_btc,
                                current_coin=orderState.current_coin,
                                piggy=orderState.piggy,
                                currency_pair=e.currency_pair)
        e.save()



    def getBuyPrice(self, currency_pair):

        if self.botConfig.printOrders:
            print 'Buscando preco de compra...'
            print 'Setando Fake buy value...'

        # return self.marketExchange.returnLastPrice(currency_pair)

        print 'fake buy price'
        return self.df.iloc[-1]['close']

    def getCurrentCoin(self, market):

        if self.botConfig.printOrders:
            print 'Buscando current coin...'

        print 'fake crrent price'
        return market.getLastAskPrice()

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

    # def isGaining(self, orderState, market):
    #
    #     return market.getLastAskPrice()/ orderState.buy_value >= 1 + self.gain

    def didGain(self, orderState):
        return orderState.sell_value / orderState.buy_value >= 1 + self.gain


    def isLosing(self, orderState, market):
        return market.getLastAskPrice() / orderState.buy_value  <= 1 - self.loss

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

    def sendBuyOrder(self,market,  exchange, orderState):

        if self.botConfig.printOrders:
            print 'Enviando ordem de compra...'

        # orderNumber = market.marketExchange.buy(exchange.currency_pair, market.getLastAskPrice() * 1.00005, orderState.current_btc)
        # return orderNumber

        print 'fake buy orderNumber'
        return 123

    def sendSellOrder(self,isGain, market, rate):

        self.cancelLastSellOrder()

        if self.botConfig.printOrders:
            if isGain:
                print 'Enviando ordem de venda ganho '
            else:
                print 'Enviando ordem de venda perda '

        print 'fake sell orderNumber'
        return 321

    def indicators_predict_buy(self, market):

        shouldBuyCount = 0

        actualPrice = market.getLastAskPrice()

        for indicator in self.indicators:

            shouldBuyCount = shouldBuyCount + indicator.predict(actualPrice, self.df)

        return True if shouldBuyCount >= 1 else False

