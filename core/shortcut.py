# -*- coding: utf-8 -*-

#各类函数的快捷方式

import logging

from wolfox.fengine.extern import *
from wolfox.fengine.internal import *
from wolfox.fengine.core.d1idiom import B0S0,B0S1,B1S0,B1S1,BS_DUMMY
from wolfox.fengine.core.trade import match_trades

logger = logging.getLogger('wolfox.fengine.core.shortcut')

def csc_func(stock,buy_signal,threshold=75,**kwargs):   #kwargs目的是吸收无用参数，便于cruiser
    t = stock.transaction
    return d1id.confirmedsellc(buy_signal,t[OPEN],t[CLOSE],t[HIGH],t[LOW],threshold)


def create_evaluator(matcher=match_trades):
    def efunc(trades,**kwargs):         #kwargs目的是吸收无用参数，便于cruiser
        return evaluate(trades,matcher)
    return efunc

normal_evaluate = create_evaluator()


#以下deprecated,使用Mediator替代
def normal_calc_template_deprecated(sdata,dates,buy_func,sell_func,trade_func):
    trades = []
    for s in sdata.values():
        try:    #捕捉某些异常，如未划入任何板块的股票在计算板块相关信号时会出错
            sbuy = buy_func(s)
            ssell = sell_func(s,sbuy)
            #sbuy,ssell = smooth2(s.transaction[VOLUME],sbuy,ssell) #这个处理被划入bMsN_trade_func中
            trades.extend(trade_func(dates,s,sbuy,ssell))
        except Exception,inst:
            print '%s except : %s' % (s.code,inst)
            logger.warning('%s calc error : %s',s.code,inst)
    return trades

def _trade_func_deprecated(dates,stock,sbuy,ssell,prepare_func,begin=0,taxrate=125,**kwargs):  #kwargs目的是吸收无用参数，便于cruiser
    ''' prepare_func是对sbuy和ssell进行预处理，如买卖都是次日交易则为B1S1 
    '''
    t = stock.transaction
    sbuy,ssell = prepare_func(t,sbuy,ssell)
    ssignal = make_trade_signal(sbuy,ssell)
    return make_trades(stock.code,ssignal,dates,t[CLOSE],t[CLOSE],begin,taxrate)

dummy_trade_func_deprecated = fcustom(_trade_func_deprecated,prepare_func=BS_DUMMY)  
b1s1_trade_func_deprecated = fcustom(_trade_func_deprecated,prepare_func=B1S1)  
b0s0_trade_func_deprecated = fcustom(_trade_func_deprecated,prepare_func=B0S0)
b0s1_trade_func_deprecated = fcustom(_trade_func_deprecated,prepare_func=B0S1)
b1s0_trade_func_deprecated = fcustom(_trade_func_deprecated,prepare_func=B1S0)
normal_trade_func_deprecated = b1s1_trade_func_deprecated   #一般情形买卖信号都是延后一日发生




