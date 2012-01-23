# -*- coding:utf-8 -*-

from pylab import *
from matplotlib.ticker import NullFormatter,NullLocator
#from matplotlib.finance import quotes_historical_yahoo,plot_day_summary, candlestick2
from wolfox.fengine.ifuture.ui.finance import candlestick,candlestick2
import wolfox.fengine.ifuture.ifreader as ifreader


fig = figure(figsize=(16,7))
fig.subplots_adjust(bottom=0.1)

ax = fig.add_subplot(111)

ax.patch.set_color('black')
nlocator = NullLocator()
ax.xaxis.set_major_locator(nlocator)

ifmap = ifreader.read_ifs_zip()  # fname ==> BaseObject(name='$name',transaction=trans)
i00 = ifmap['IF0001']
candlestick2(ax, i00.open,i00.close,i00.high,i00.low, width=0.6)

#ax.autoscale_view()

show()

