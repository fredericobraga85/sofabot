class OrderState:


    def __init__(self, currencyPair):

        self.resetValues()
        self.currencyPair = currencyPair
        self.fromDigitalCurr = currencyPair.split('_')[0]
        self.toDigitalCurr  = currencyPair.split('_')[1]

    def resetValues(self):

        self.inBuy = False
        self.perGain = 0
        self.actual_price = 0.0
        self.buy_value = 0.0
        self.sell_value = 0.0

        self.buy_order_active            = False
        self.sell_order_gain_active      = False
        self.sell_order_loss_active      = False
        self.sell_order_objective_active = False


    def waitingForBuyOpportunity(self):
        return self.inBuy == False and self.buy_order_active == False

    def waitingForBuyOrderToBeExecuted(self):
        return self.buy_order_active

    def waitingForSellOpportunity(self):
        return self.inBuy == True and self.sell_order_active == False

    def waitingForSellOrderToBeExecuted(self):
        return self.sell_order_active

    def setInBuyStatus(self):

        self.inBuy = True

        self.buy_order_active  = False
        self.sell_order_active = False


    def setSoldStatus(self):

        self.inBuy = False

        self.buy_order_active  = False
        self.sell_order_active = False


    def getGainPerc(self):
        return self.actual_price / self.buy_value


    def setBuyOrderStatus(self, activate):
        self.buy_order_active = activate
        self.sell_order_active = False

    def setSellOrderStatus(self, activate):
        self.buy_order_active = False
        self.sell_order_active = activate


    def setSellOrderGain(self, activate):
        self.buy_order_active            = False
        self.sell_order_gain_active      = activate
        self.sell_order_loss_active      = False
        self.sell_order_objective_active = False

    def setSellOrderLoss(self, activate):
        self.buy_order_active = False
        self.sell_order_gain_active = False
        self.sell_order_loss_active = activate
        self.sell_order_objective_active = False

    def setSellOrderObjective(self, activate):
        self.buy_order_active = False
        self.sell_order_gain_active = False
        self.sell_order_loss_active = False
        self.sell_order_objective_active = activate