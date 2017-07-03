
class Wallet:

    BTC = 'BTC'
    FTC = 'FTC'

    wallet = {}

    def __init__(self, fromDigitalCurr , toDigitalCurr, volume):

        self.wallet[fromDigitalCurr] = volume
        self.wallet[toDigitalCurr]   = 0.0
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

