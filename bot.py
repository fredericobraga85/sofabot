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
timestamp = ['1496448000', '1496793600', '1498089600', '1498176000', '1498262400', '1498348800', '1498521600', '9999999999']
period = '300'

btc= 1.0
gain = 0.03
loss = 0.02
loss_after_gain = 0.02

for i, val in enumerate(timestamp):

    if i > 0:
        chart_analyzer = ChartAnalyzer.ChartAnalyzer()
        chart_analyzer.init(currencyPair, timestamp[i - 1], timestamp[i], period, btc)
        chart_analyzer.decide_action(gain , loss , loss_after_gain)

        # Visualizer.print_full(chart_analyzer.df[['isUp', 'weightedAverage','buyValue','perGain', 'btc' , 'actualCurrency',  'Buy']]) #'supportQuote', 'resistanceQuote'

        print 'Numer of trades', chart_analyzer.df["gained"].sum()
        print 'Open 1st period', chart_analyzer.df['open'][0]
        print 'Close  last period', chart_analyzer.df['close'].iloc[-1]
        print 'Gain period', (chart_analyzer.df['close'].iloc[-1]/ chart_analyzer.df['open'][0] - 1) * 100
        print 'Bot gain', (chart_analyzer.btc / btc - 1) * 100, (chart_analyzer.actualCurrency * chart_analyzer.actual_price / btc - 1) * 100
        print 'Algorithm gain',chart_analyzer.df['perGain'].sum()
        print ''