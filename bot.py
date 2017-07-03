import ChartAnalyzer

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
# currencyPair = 'BTC_LTC'
# currencyPair = 'BTC_XRP'
# currencyPair = 'BTC_XMR'
timestamp = \
    [
        '1496448000',  # 03/6
        '1496534400',  # 04/6
        '1496620800',  # 05/6
        '1496707200',  # 06/6
        '1496793600',  # 07/6
        '1496880000',  # 08/6
        '1496966400',  # 09/6
        '1497052800',  # 10/6
        '1497139200',  # 11/6
        '1497225600',  # 12/6
        '1497312000',  # 13/6
        '1497398400',  # 14/6
        '1497484800',  # 15/6
        '1497571200',  # 16/6
        '1497657600',  # 17/6
        '1497744000',  # 18/6
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

print_chart       = False
printOrders       = False
printRow          = False
printIteration    = True

iterations_per_day = 1

btc= 1.0
objective_gain = 1.02
limit_loss = 0.95
gain = 0.03
loss = 0.02
dif_open_close_perc = 1.005
resistance_tolerance = 1.005 # tem que ser maior q 1
buy_perc  = 0.0015
sell_perc = 0.0030

total_gain_all_curr_perc = 0.0
total_bot_gain_all_curr_perc = 0.0


for y, currencyPair in enumerate(currencyPairList):

    total_gain_perc = 0.0
    total_bot_gain_perc = 0.0
    total_avg_algo_gain = 0.0


    for i, val in enumerate(timestamp):


        for iteration in range(0,iterations_per_day):

            chart_analyzer = ChartAnalyzer.ChartAnalyzer()
            start = int(timestamp[i]) + ((86400 / iterations_per_day) * iteration)
            end   = int(timestamp[i]) + ((86400 / iterations_per_day) * (iteration + 1))
            chart_analyzer.init(currencyPair, str(start), str(end), period, btc, printOrders, printRow)
            chart_analyzer.decide_action(objective_gain,limit_loss,  gain , loss, dif_open_close_perc, resistance_tolerance, buy_perc, sell_perc)

            if print_chart:
                chart_analyzer.printChart(chart_analyzer.df)


            total_trades        = chart_analyzer.df["gained"].sum()
            open_quote          = chart_analyzer.df['open'][0]
            close_quote         = chart_analyzer.df['close'].iloc[-1]
            support_quote       = chart_analyzer.df['supportQuote'].iloc[1]
            gain_period         = ((close_quote / open_quote) - 1) * 100
            ups_downs           = chart_analyzer.df["isUp"].sum()
            piggy_safe          = chart_analyzer.piggy_safe
            bot_gain_period_btc = ((chart_analyzer.btc + piggy_safe) / btc - 1) * 100
            bot_gain_period_cur = ((((chart_analyzer.actual_price * chart_analyzer.actualCurrency) - (chart_analyzer.actual_price * chart_analyzer.actualCurrency * chart_analyzer.sell_perc)) / btc)   - 1) * 100
            algorithm_gain      = chart_analyzer.df['perGain'].sum()
            avg_algo_trade      = ((algorithm_gain / total_trades)) if total_trades != 0 else 0

            total_gain_perc = total_gain_perc + gain_period
            total_bot_gain_perc = total_bot_gain_perc + (bot_gain_period_btc if bot_gain_period_btc != -100 else bot_gain_period_cur)
            total_avg_algo_gain = total_avg_algo_gain + avg_algo_trade

            if printIteration:
                print ' CurrencyPair', currencyPair
                print ' Date', chart_analyzer.df['date'].iloc[0]
                print ' Numer of trades', total_trades
                print ' Support Quote', support_quote
                print ' Open 1st period', open_quote
                print ' Close  last period', close_quote
                print " Ups and Downs period" , ups_downs
                print ' Gain period', gain_period
                print ' Bot gain', bot_gain_period_btc if bot_gain_period_btc != -100 else bot_gain_period_cur , '' if bot_gain_period_btc != -100 else '( estimate - no last sell)'
                print ' Piggy safe', piggy_safe
                print ' Average Algorithm gain per trade', avg_algo_trade if total_trades != 0 else 'zero trades'
                print ''

    total_gain_all_curr_perc = total_gain_all_curr_perc + total_gain_perc
    total_bot_gain_all_curr_perc = total_bot_gain_all_curr_perc + total_bot_gain_perc

    print ' CurrencyPair', currencyPair
    print 'TOTAL gain    ', total_gain_perc
    print 'TOTAL bot gain', total_bot_gain_perc
    print 'TOTAL Algo gain per trade', total_avg_algo_gain / len(timestamp)
    print ''


print 'TOTAL ALL gain    ', total_gain_all_curr_perc
print 'TOTAL ALLbot gain', total_bot_gain_all_curr_perc
print ''