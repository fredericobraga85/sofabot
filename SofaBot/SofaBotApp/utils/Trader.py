import threading
import OrderStatus
from ..utils.MarketThread import MarketThread
from ..models import Exchange
from django.utils import timezone
from ..indicators.LoseAndWinIndicator import LoseAndWinIndicator
import time
import pandas as pd
import pdb;


class Trader(threading.Thread):
  
    # objective_gain = 10
    # limit_loss = 0
    
    indicators = [
        LoseAndWinIndicator(False, 1)
    ]

    test = True

    class BotConfig:

        printOrders = True
        gain = 0.03
        loss = 0.10
        periodStart = 144


    def __init__(self, exchange_id, marketExchange):
        threading.Thread.__init__(self)
        self.exchange_id = exchange_id
        self.botConfig = Trader.BotConfig()
        self.marketExchange = marketExchange


    def run(self):
        print "Starting Trading" + self.name
        self.startTrading()
        print "Exiting Trading" + self.name
   



    def startTrading(self):

        e = Exchange.objects.get(id=self.exchange_id)

        self.marketThread = MarketThread(1, "Thread-" + e.currency_pair, e.currency_pair, self.marketExchange)
        self.marketThread.start()

        self.isActive = True

        actualPeriod = 0
        lastPriceHistory = []

        try:
            while self.isActive :

                e = Exchange.objects.get(id=self.exchange_id)
                orderState = e.orderstate_set.last()

                self.isActive = e.isActive
                lastPriceHistory.append(self.marketThread.getLastPrice())

                if self.isActive and len(lastPriceHistory) > self.botConfig.periodStart:

                    lastPriceHistory.pop(0)

                    self.df_history_price =  pd.DataFrame(lastPriceHistory)

                    if orderState.statusCode == OrderStatus.waiting_buying_opportunity :

                        self.waitingBuyingOpportunity(e, orderState)

                    elif orderState.statusCode == OrderStatus.sent_buy_order:

                        self.waitingSellingOpportunity(e, orderState)

                    elif orderState.statusCode == OrderStatus.sent_sell_order_is_gaining:

                        self.waitingGainingSellExecution(e, orderState)

                    elif orderState.statusCode == OrderStatus.sent_sell_order_is_losing:

                        self.waitingLosingSellExecution(e, orderState)

                else:
                    self.wait(e, orderState)

                actualPeriod = actualPeriod + 1

                print 'waiting 5 minutes...actual Period', actualPeriod
                time.sleep(60 * 5)

        except Exception as ex:
            print 'Error Trader:', ex

            e = Exchange.objects.get(id=self.exchange_id)
            e.isActive = False
            e.save()





    def waitingBuyingOpportunity(self, e, orderState):
        print "waiting_buying_opportunity"
        if self.indicators_predict_buy():

            print "Indicators predict SHOULD buy"

            try:

                orderNumber = self.marketThread.sendBuyOrder(e, orderState)

                if orderNumber != None:

                    e.orderstate_set.create(orderNumber=orderNumber,
                                            buy_value     = 0.0,
                                            sell_value    = 0.0,
                                            actual_price  = self.marketThread.getLastPrice(),
                                            perGain       = 0.0,
                                            statusCode    = OrderStatus.sent_buy_order,
                                            state_date    = timezone.now(),
                                            current_btc   = orderState.current_btc,
                                            current_coin  = 0.0,
                                            piggy         = orderState.piggy,
                                            currency_pair = e.currency_pair)
                    e.save()



            except Exception as ex:
                print 'Error Sending Buy Order:', ex
                self.wait(e, orderState)


        else:
            print "Indicators predict NOT TO buy"
            self.wait(e, orderState)




    def waitingSellingOpportunity(self, e, orderState):
        print "waitingSellingOpportunity"
        actual_price = self.marketThread.getLastPrice()
        if self.marketThread.buyOrderWasExecuted(orderState.orderNumber):

            print "buy Order Was Executed"

            buy_value = self.marketThread.getBuyPrice(orderState.orderNumber)
            amount_buy = self.marketThread.getBuyAmount(orderState.orderNumber)

            try:
                orderNumber = self.marketThread.sendGainingSellOrder(e, self.getGainingSellPrice(buy_value))

                e.orderstate_set.create(orderNumber=orderNumber,
                                        buy_value     = buy_value,
                                        sell_value    = 0.0,
                                        actual_price  = actual_price,
                                        perGain       = ((actual_price / buy_value - 1) * 100),
                                        statusCode    = OrderStatus.sent_sell_order_is_gaining,
                                        state_date    = timezone.now(),
                                        current_btc   = orderState.current_btc - (amount_buy * buy_value),
                                        current_coin  = amount_buy,
                                        piggy         = orderState.piggy,
                                        currency_pair = e.currency_pair)
                e.save()

            except Exception as ex:
                print 'Error Sending Gainig Sell Order:', ex
                self.wait(e, orderState)
        else:

            print "buy Order was not executed"

            try:
                self.marketThread.cancelOrder(orderState.orderNumber)

                e.orderstate_set.create(orderNumber   = 0,
                                        buy_value     = 0.0,
                                        sell_value    = 0.0,
                                        actual_price  = actual_price,
                                        perGain       = 0.0,
                                        statusCode    = OrderStatus.waiting_buying_opportunity,
                                        state_date    = timezone.now(),
                                        current_btc   = orderState.current_btc,
                                        current_coin  = 0.0,
                                        piggy         = orderState.piggy,
                                        currency_pair = e.currency_pair)
                e.save()

            except Exception as ex:
                print 'Error cancelling Gaining Buy Order:', ex
                self.wait(e, orderState)




    def waitingGainingSellExecution(self, e, orderState):

        print "sent_sell_order_is_gaining"

        if self.marketThread.sellOrderWasExecuted(orderState.orderNumber):

            print "sell Gaining Order Was Executed"

            sell_value = self.marketThread.getSellPrice(orderState.orderNumber)

            result = sell_value * orderState.current_coin
            piggy = orderState.piggy

            if result > e.initial_btc:
                piggy = orderState.piggy + (result - e.initial_btc)
                result = e.initial_btc
                # self.marketThread.transferPiggy(piggy)

            e.orderstate_set.create(orderNumber   = orderState.orderNumber,
                                    buy_value     = orderState.buy_value,
                                    sell_value    = sell_value,
                                    actual_price  = self.marketThread.getLastPrice(),
                                    perGain       = ((sell_value / orderState.buy_value - 1) * 100),
                                    statusCode    = OrderStatus.waiting_buying_opportunity,
                                    state_date    = timezone.now(),
                                    current_btc   = result,
                                    current_coin  = 0.0,
                                    piggy         = piggy,
                                    currency_pair = e.currency_pair)
            e.save()


        elif self.isLosing(orderState):

            print "Limite de perda excedido..."

            self.marketThread.cancelOrder(orderState.orderNumber)

            try:
                actual_price = self.marketThread.getLastPrice()
                orderNumber = self.marketThread.sendLosingSellOrder(e, actual_price)

                e.orderstate_set.create(orderNumber   = orderNumber,
                                        buy_value     = orderState.buy_value,
                                        sell_value    = 0.0,
                                        actual_price  = actual_price,
                                        perGain       = ((actual_price / orderState.buy_value - 1) * 100),
                                        statusCode    = OrderStatus.sent_sell_order_is_losing,
                                        state_date    = timezone.now(),
                                        current_btc   = orderState.current_btc,
                                        current_coin  = orderState.current_coin,
                                        piggy         = orderState.piggy,
                                        currency_pair = e.currency_pair)
                e.save()
            except Exception as ex:
                print 'Error sending Losing Sell Order:', ex
                self.wait(e, orderState)

        else:
            print 'Ordem de venda com ganho nao realizado...'
            self.wait(e, orderState)





    def waitingLosingSellExecution(self, e, orderState):

        print "sent_sell_order_is_losing"

        if self.marketThread.sellOrderWasExecuted(orderState.orderNumber):

            print "sell Losing Order Was Executed"

            sell_value = self.marketThread.getSellPrice(orderState.orderNumber)

            result = sell_value * orderState.current_coin
            piggy = orderState.piggy

            if result > e.initial_btc:
                piggy = orderState.piggy + (result - e.initial_btc)
                result = e.initial_btc
                self.marketThread.transferPiggy(piggy)

            e.orderstate_set.create(orderNumber   = orderState.orderNumber,
                                    buy_value     = orderState.buy_value,
                                    sell_value    = sell_value,
                                    actual_price  = self.marketThread.getLastPrice(),
                                    perGain       = ((sell_value / orderState.buy_value - 1) * 100),
                                    statusCode    = OrderStatus.waiting_buying_opportunity,
                                    state_date    = timezone.now(),
                                    current_btc   = result,
                                    current_coin  = 0.0,
                                    piggy         = piggy,
                                    currency_pair = e.currency_pair)
            e.save()

        else:
            print 'Ordem de venda com perda nao realizado...'
            self.wait(e, orderState)




    def wait(self, e, orderState):

        print "wait"

        actual_price = self.marketThread.getLastPrice()
        perGain = ((actual_price / orderState.buy_value - 1) * 100) if orderState.buy_value > 0 else 0.0

        e.orderstate_set.create(orderNumber   = orderState.orderNumber,
                                buy_value     = orderState.buy_value,
                                sell_value    = orderState.sell_value,
                                actual_price  = actual_price,
                                perGain       = perGain,
                                statusCode    = orderState.statusCode,
                                state_date    = timezone.now(),
                                current_btc   = orderState.current_btc,
                                current_coin  = orderState.current_coin,
                                piggy         = orderState.piggy,
                                currency_pair = e.currency_pair)
        e.save()


    def getGainingSellPrice(self, buy_value):
        return buy_value * ( 1 + self.botConfig.gain)


    def isLosing(self, orderState):

        print 'Verificando se excedeu limite de perda...'

        # return self.marketThread.getLastPrice() / orderState.buy_value  <= 1 - self.botConfig.loss
        print 'teste'
        return True



    def indicators_predict_buy(self):

        print 'Predicting buy...'

        shouldBuyCount = 0

        actualPrice = self.marketThread.getLastPrice()

        for indicator in self.indicators:

            shouldBuyCount = shouldBuyCount + indicator.predict(actualPrice, self.df_history_price)

        return True if shouldBuyCount >= 1 else False



