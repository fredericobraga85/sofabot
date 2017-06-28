import numpy as np
import ChartAnalyzer
import Visualizer

#BTC_FCT
#BTC_LSK
#03/06 1496448000
#07/6 1496793600
#22/6 1498089600
#23/6 1498176000
#24/6 1498262400
#25/6 1498348800
#27/6 1498521600
#99/9 9999999999

currencyPair = 'BTC_FCT'
timestamp = \
    [
        # '1496448000',#03/6
        # '1496793600',#07/6
        # '1498089600',#22/6
        # '1498176000',#23/6
        # '1498262400',#24/6
        # '1498348800',#25/6
        '1498435200',#26/6
        '1498521600',#27/6
        # '9999999999'
    ]

period = '300'

btc= 1.0
gain = 0.03
loss = 0.01
loss_after_gain = 0.005

for i, val in enumerate(timestamp):

    if i > 0:
        chart_analyzer = ChartAnalyzer.ChartAnalyzer()
        chart_analyzer.init(currencyPair, timestamp[i - 1], timestamp[i], period, btc)
        chart_analyzer.decide_action(gain , loss , loss_after_gain)


        Visualizer.print_full(chart_analyzer.df[[
            # 'date',
            # 'close',
            # 'high',
            # 'low',
            # 'open',
            # 'quoteVolume',
            # 'volume',
            'isUp',
            'weightedAverage',
            'buyValue',
            'perGain',
            'btc' ,
            'actualCurrency',
            'Buy',
            'supportQuote',
            'resistanceQuote',
        ]])


        total_trades        = chart_analyzer.df["gained"].sum()
        open_quote          = chart_analyzer.df['open'][0]
        close_quote         = chart_analyzer.df['close'].iloc[-1]
        gain_period         = ((close_quote / open_quote) - 1) * 100
        bot_gain_period_btc = (chart_analyzer.btc / btc - 1) * 100
        bot_gain_period_cur = (((chart_analyzer.actualCurrency * chart_analyzer.actual_price) / btc) - 1) * 100
        algorithm_gain      = chart_analyzer.df['perGain'].sum()
        avg_algo_trade      = ((algorithm_gain / total_trades) * 100) if total_trades != 0 else 0

        print 'Numer of trades', total_trades
        print 'Open 1st period', open_quote
        print 'Close  last period', close_quote
        print 'Gain period', gain_period
        print 'Bot gain', bot_gain_period_btc, bot_gain_period_cur
        print 'Average Algorithm gain per trade', avg_algo_trade if total_trades != 0 else 'zero trades'
        print ''