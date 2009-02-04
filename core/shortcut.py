# -*- coding: utf-8 -*-

#各类函数的快捷方式

import logging

from wolfox.fengine.extern import *
from wolfox.fengine.internal import *

logger = logging.getLogger('wolfox.fengine.core.shortcut')

def normal_calc_template(sdata,dates,buy_func,sell_func,trade_func):
    trades = []
    for s in sdata.values():
        try:    #捕捉某些异常，如未划入任何板块的股票在计算板块相关信号时会出错
            sbuy = buy_func(s)
            ssell = sell_func(s,sbuy)
            sbuy,ssell = smooth2(sbuy,ssell,s.transaction[VOLUME])
            trades.extend(trade_func(dates,s,sbuy,ssell))
        except Exception,inst:
            print '%s except : %s' % (s.code,inst)
            logger.warning('%s calc error : %s',s.code,inst)
    return trades

def csc_func(stock,buy_signal,threshold=75,**kwargs):   #kwargs目的是吸收无用参数，便于cruiser
    t = stock.transaction
    return d1id.confirmedsellc(buy_signal,t[OPEN],t[CLOSE],t[HIGH],t[LOW],threshold)

def normal_trade_func(dates,stock,sbuy,ssell,begin=0,taxrate=125,**kwargs):  #kwargs目的是吸收无用参数，便于cruiser
    t = stock.transaction
    ssignal = make_trade_signal(sbuy,ssell)
    return make_trades(stock.id,ssignal,dates,t[CLOSE],t[CLOSE],begin,taxrate)

def normal_evaluate(trades,**kwargs):   #kwargs目的是吸收无用参数，便于cruiser
    return evaluate(trades)

ppsort = lambda v,distance=1:percent_sort(percent(v,distance))

c_posort = cdispatch(ppsort)
d_posort = dispatch(ppsort)


