class Wallet:

    BTC = 'BTC'
    FTC = 'FTC'

    wallet = {}

    def __init__(self, currDeposit, volume):
        self.wallet[currDeposit] = volume

    def exchange(self, fromDigitalCurr , toDigitalCurr, buy_value, fee):

        if fromDigitalCurr == Wallet.BTC:

            volume                       = self.wallet[fromDigitalCurr]
            self.wallet[toDigitalCurr]   = (volume / buy_value) - (volume/ buy_value * fee)
            self.wallet[fromDigitalCurr] = self.wallet[fromDigitalCurr] - volume

        else:
            volume = self.wallet[fromDigitalCurr]
            self.wallet[toDigitalCurr] = (volume * buy_value) - (volume * buy_value * fee)
            self.wallet[fromDigitalCurr] = self.wallet[fromDigitalCurr] - volume



