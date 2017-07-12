import Converter
from Poloniex import Poloniex
from Trader import Trader
from matplotlib import pyplot as plt

from indicators.BigFallIndicator import BigFallIndicator
from indicators.BigFallRecoverIndicator import BigFallRecoverIndicator
from indicators.BigUpIndicator import BigUpIndicator
from indicators.BollingerBandsIndicator import BollingerBandsIndicator
from indicators.FibonacciIndicator import FibonnaciIndicator
from indicators.FirstPeriodIndicator import FirstPeriodIndicator
from indicators.KMeansIndicator import KMeansIndicator
from indicators.KNNIndicator import KNNIndicator
from indicators.LinearRegressionIndicator import LinearRegressionIndicator
from indicators.MACDIndicator import MACDIndicator
from indicators.MomentumIndicator import MomentumIndicator
from indicators.RandomForrestIndicator import RandomForrestIndicator
from indicators.SMAIndicator import SMAIndicator
from indicators.SVMIndicator import SVMIndicator
from indicators.SupportResistanceIndicator import SupportResistanceIndicator
from indicators.UpsAndDownsIndicator import UpsAndDownsIndicators
from indicators.VolumeIndicator import VolumeIndicator
from indicators.WinAndLoseIndicator import WinAndLoseIndicator

currencyPairList = \
    [
        # 'BTC_BTS',
        # 'BTC_DASH',
        # 'BTC_ETH',
        'BTC_FCT',
        # 'BTC_MAID',
        # 'BTC_LTC',
        # 'BTC_XRP',
        # 'BTC_XMR',
        # 'BTC_ZEC',
        ]

timestampTrain = \
    [
        '1496448000',  # 03/6
        # '1496534400',  # 04/6
        # '1496620800',  # 05/6
        # '1496707200',  # 06/6
        # '1496793600',  # 07/6
        # '1496880000',  # 08/6
        # '1496966400',  # 09/6
        # '1497052800',  # 10/6
        # '1497139200',  # 11/6
        # '1497225600',  # 12/6
        # '1497312000',  # 13/6
        # '1497398400',  # 14/6
        # '1497484800',  # 15/6
        # '1497571200',  # 16/6
        # '1497657600',  # 17/6
        '1497744000',  # 18/6
        # '1497830400',  # 19/6
        # '1497916800',  # 20/6
        # '1498003200',  # 21/6
        # '1498089600',  # 22/6
        # '1498176000',  # 23/6
        # '1498262400',  # 24/6
        # '1498348800',  # 25/6
        # '1498435200',  # 26/6
        # '1498521600',  # 27/6
        # '1498608000',  # 28/6
        # '1498694400',  # 29/6
        # '1498780800',  # 30/6
        # '1498867200',  # 31/6
        # '1498867200',  # 01/7
        # '9999999999',
    ]



timestamp = \
    [
        # '1496448000',  # 03/6
        # '1496534400',  # 04/6
        # '1496620800',  # 05/6
        # '1496707200',  # 06/6
        # '1496793600',  # 07/6
        # '1496880000',  # 08/6
        # '1496966400',  # 09/6
        # '1497052800',  # 10/6
        # '1497139200',  # 11/6
        # '1497225600',  # 12/6
        # '1497312000',  # 13/6
        # '1497398400',  # 14/6
        # '1497484800',  # 15/6
        # '1497571200',  # 16/6
        # '1497657600',  # 17/6
        # '1497744000',  # 18/6
        # '1497830400',  # 19/6
        '1497916800',  # 20/6
        '1498003200',  # 21/6
        # '1498089600',  # 22/6
        # '1498176000',  # 23/6
        # '1498262400',  # 24/6
        # '1498348800',  # 25/6
        # '1498435200',  # 26/6
        # '1498521600',  # 27/6
        # '1498608000',  # 28/6
        # '1498694400',  # 29/6
        # '1498780800',  # 30/6
        # '1498867200',  # 01/7
        # '1499472000', # 08/7
        # '1499644800', # 10/7
        # '1499731200', # 11/7
        # '9999999999',

    ]

period = '300'


iterations_per_day = 1

btc= 1.0
objective_gain = 1.03
limit_loss = 0.98
gain = 0.01
loss = 0.01


total_gain_all_curr_perc = 0.0
total_bot_gain_all_curr_perc = 0.0


for y, currencyPair in enumerate(currencyPairList):

    total_gain_perc = 0.0
    total_bot_gain_perc = 0.0
    total_trades_all = 0.0
    first_open = 0.0
    last_close = 0.0

    indicators = [
        # KNNIndicator(currencyPair, period, timestampTrain,True, 1),
        # SVMIndicator(currencyPair, period, timestampTrain,True, 1),
        # LinearRegressionIndicator(currencyPair, period, timestampTrain,True, 1),
        # RandomForrestIndicator(currencyPair, period, timestampTrain,False, 1),
        # KMeansIndicator(currencyPair,period, timestampTrain,True, 1),
        # MomentumIndicator(True, 1),
        # SupportResistanceIndicator(True, 1),
        # SMAIndicator(True, 1),
        # FibonnaciIndicator(True, 1),
        # UpsAndDownsIndicators(True, 1),
        # FirstPeriodIndicator(True, 1),
        # BigFallIndicator(False, 1),
        BigUpIndicator(True, 1),
        # BigFallRecoverIndicator(False, 1),
        # BollingerBandsIndicator(True, 1),
        # MACDIndicator(False, 1),
        # VolumeIndicator(False, 1),
        # WinAndLoseIndicator(True,0)
    ]



    class BotConfig:

        shouldBuyAccept = 2
        print_chart = True
        printOrders = False
        printRow = False
        printIteration = True
        printPlot = True

    for i, val in enumerate(timestamp):

        if i < len(timestamp) - 1 :

            for iteration in range(0,iterations_per_day):


                dif = (int(timestamp[i + 1]) - int(timestamp[i])) / (iterations_per_day)

                start = str(int(timestamp[i]) + (dif * iteration))
                end   = str(int(timestamp[i]) + (dif * (iteration + 1)))

                marketExchange = Poloniex(currencyPair, start, end, period)

                trader = Trader(indicators, marketExchange, BotConfig())
                trader.startTrading(btc, currencyPair,objective_gain, limit_loss, gain, loss)

                if BotConfig.print_chart:
                    trader.printChart(trader.df)

                if BotConfig.printPlot:
                    for indicator in indicators:
                        indicator.plot(trader.df, plt)

                if i == 0:
                    first_open = trader.df.iloc[0]["open"]
                last_close = trader.df.iloc[len(trader.df) - 1]["close"]

                total_trades        = trader.df["gained"].sum()
                open_quote          = trader.df['open'][0]
                close_quote         = trader.df['close'].iloc[-1]
                # support_quote       = trader.df['supportQuote'].iloc[1]
                gain_period         = ((close_quote / open_quote) - 1) * 100
                ups_downs           = trader.df["isUp"].sum()
                bot_gain_period_btc = ((trader.wallet.wallet[trader.orderState.fromDigitalCurr]) / btc - 1) * 100
                bot_gain_period_cur = ((((trader.orderState.actual_price * trader.wallet.wallet[trader.orderState.toDigitalCurr]) - (trader.orderState.actual_price * trader.wallet.wallet[trader.orderState.toDigitalCurr] * trader.marketExchange.getActiveSellFeePerc())) / btc)   - 1) * 100
                algorithm_gain      = trader.df['perGain'].sum()
                avg_algo_trade      = ((algorithm_gain / total_trades)) if total_trades != 0 else 0

                total_gain_perc = total_gain_perc + gain_period
                total_bot_gain_perc = total_bot_gain_perc + (bot_gain_period_btc if bot_gain_period_btc != -100 else bot_gain_period_cur)
                total_trades_all = total_trades_all + total_trades

                if BotConfig.printIteration:
                    print 'Start Date', trader.df['date'].iloc[0]
                    print 'End Date', trader.df['date'].iloc[len(trader.df) - 1]
                    print ' CurrencyPair', currencyPair
                    print ' Numer of trades', total_trades
                    # print ' Support Quote', support_quote
                    print ' Open 1st period', open_quote
                    print ' Close  last period', close_quote
                    print " Ups and Downs period" , ups_downs
                    print ' Gain period', gain_period
                    print ' Bot gain', bot_gain_period_btc if bot_gain_period_btc != -100 else bot_gain_period_cur , '' if bot_gain_period_btc != -100 else '( estimate - no last sell)'
                    print ' Average Algorithm gain per trade', avg_algo_trade if total_trades != 0 else 'zero trades'
                    print ''

    total_gain_all_curr_perc = total_gain_all_curr_perc + total_gain_perc
    total_bot_gain_all_curr_perc = total_bot_gain_all_curr_perc + total_bot_gain_perc

    print ' CurrencyPair', currencyPair
    print 'TOTAL gain    ', total_gain_perc
    print 'TOTAL bot gain', total_bot_gain_perc
    print 'TOTAL Trade trade', total_trades_all
    print 'TOTAL Total gin straight', (last_close / first_open - 1)*100
    print ''


print 'TOTAL ALL gain    ', total_gain_all_curr_perc
print 'TOTAL ALLbot gain', total_bot_gain_all_curr_perc
print ''