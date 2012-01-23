# -*- coding:utf-8 -*-

from pylab import *
from matplotlib.ticker import NullFormatter,NullLocator
#from matplotlib.finance import quotes_historical_yahoo,candlestick,plot_day_summary, candlestick2
from matplotlib.finance import quotes_historical_yahoo,plot_day_summary, candlestick2
from wolfox.fengine.ifuture.ui.finance import candlestick,candlestick2

date1 = ( 2004, 2, 1)
date2 = ( 2008, 4, 12 )

quotes = quotes_historical_yahoo('INTC', date1, date2)[:150]
if len(quotes) == 0:
    raise SystemExit

fig = figure(figsize=(16,7))
fig.subplots_adjust(bottom=0.1)

ax = fig.add_subplot(111)

ax.patch.set_color('black')
nlocator = NullLocator()
ax.xaxis.set_major_locator(nlocator)

st,sopen,sclose,shigh,slow = np.transpose(quotes)[:5]
candlestick2(ax, sopen,sclose,shigh,slow, width=0.6)

ax.autoscale_view()

show()



