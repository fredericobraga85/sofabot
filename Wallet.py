
class Wallet:

    BTC = 'BTC'
    FTC = 'FTC'

    wallet = {}

    def __init__(self, currDeposit, volume):

        self.wallet[currDeposit] = volume
        self.initialDeposit = volume

    def exchange(self, fromDigitalCurr , toDigitalCurr, value_btc, fee):

        if fromDigitalCurr == Wallet.BTC:

            volume                       = self.wallet[fromDigitalCurr]
            self.wallet[toDigitalCurr]   = (volume / value_btc) - (volume/ value_btc * fee)
            self.wallet[fromDigitalCurr] = self.wallet[fromDigitalCurr] - volume

        else:
            volume = self.wallet[fromDigitalCurr]
            self.wallet[toDigitalCurr] = (volume * value_btc) - (volume * value_btc * fee)
            self.wallet[fromDigitalCurr] = self.wallet[fromDigitalCurr] - volume

    def getDigitalCurrency(self, digitalCurrency):
        return self.wallet[digitalCurrency]

