import matplotlib.pyplot as plt
from Poloniex import Poloniex
from Trader import Trader
from KNNIndicator import KNNIndicator
from SVMIndicator import SVMIndicator
from LinearRegressionIndicator import  LinearRegressionIndicator
from SupportResistanceIndicator import SupportResistanceIndicator
from KMeansIndicator import KMeansIndicator
from MomentumIndicator import MomentumIndicator
from RandomForrestIndicator import  RandomForrestIndicator

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
        '1497830400',  # 19/6
        '1497916800',  # 20/6
        '1498003200',  # 21/6
        '1498089600',  # 22/6
        '1498176000',  # 23/6
        '1498262400',  # 24/6
        '1498348800',  # 25/6
        '1498435200',  # 26/6
        '1498521600',  # 27/6
        '1498608000',  # 28/6
        '1498694400',  # 29/6
        '1498780800',  # 30/6
        '1498867200',  # 31/6
        '1498867200',  # 01/7
        # '9999999999',

    ]

period = '300'

class BotConfig:

    shouldBuyAccept   = 2
    print_chart       = True
    printOrders       = False
    printRow          = False
    printIteration    = True

iterations_per_day = 1

btc= 1.0
objective_gain = 1.03
limit_loss = 0.95
gain = 0.03
loss = 0.015


total_gain_all_curr_perc = 0.0
total_bot_gain_all_curr_perc = 0.0


for y, currencyPair in enumerate(currencyPairList):

    total_gain_perc = 0.0
    total_bot_gain_perc = 0.0
    total_trades_all = 0.0


    indicators = [
        KNNIndicator(currencyPair, period),
        # SVMIndicator(currencyPair, period),
        # LinearRegressionIndicator(currencyPair, period),
        RandomForrestIndicator(currencyPair, period),
        # KMeansIndicator(currencyPair,period),
        # MomentumIndicator()
        # SupportResistanceIndicator(),
    ]

    for i, val in enumerate(timestamp):


        for iteration in range(0,iterations_per_day):

            start = str(int(timestamp[i]) + ((86400 / iterations_per_day) * iteration))
            end   = str(int(timestamp[i]) + ((86400 / iterations_per_day) * (iteration + 1)))

            marketExchange = Poloniex(currencyPair, start, end, period)


            trader = Trader(indicators, marketExchange, BotConfig())
            trader.startTrading(btc, currencyPair,objective_gain, limit_loss, gain, loss)

            if BotConfig.print_chart:
                trader.printChart(trader.df)

            # plt.plot(trader.df['date'][2:], trader.df['weightedAverage'][2:])
            # plt.plot(trader.df['date'][2:], trader.df['resistanceQuote'][2:])
            # plt.plot(trader.df['date'][2:], trader.df['supportQuote'][2:])
            # plt.show()

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
                print ' CurrencyPair', currencyPair
                print ' Date', trader.df['date'].iloc[0]
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
    print ''


print 'TOTAL ALL gain    ', total_gain_all_curr_perc
print 'TOTAL ALLbot gain', total_bot_gain_all_curr_perc
print ''