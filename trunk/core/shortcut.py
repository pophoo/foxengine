# -*- coding: utf-8 -*-

#各类函数的快捷方式

from wolfox.fengine.extern import *
from wolfox.fengine.internal import *

def normal_template(sdata,dates,buy_func,sell_func,trade_func):
    trades = []
    for s in sdata.values():
        sbuy = buy_func(s)
        ssell = sell_func(s,sbuy)
        sbuy,ssell = smooth2(sbuy,ssell,s.transaction[VOLUME])
        trades.extend(trade_func(dates,s,sbuy,ssell))
    return trades,names(buy_func,sell_func,trade_func)

def csc_func(stock,buy_signal,threshold=75):
    t = stock.transaction
    return d1id.confirmedsellc(buy_signal,t[OPEN],t[CLOSE],t[HIGH],t[LOW],threshold)

def normal_trade_func(dates,stock,sbuy,ssell):
    t = stock.transaction
    ssignal = make_trade_signal(sbuy,ssell)
    return make_trades(stock.id,ssignal,dates,t[CLOSE],t[CLOSE])

ppsort = lambda v,distance=1:percent_sort(percent(v,distance))

c_posort = cdispatch(ppsort)
d_posort = dispatch(ppsort)


