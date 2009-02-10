# -*- coding:utf-8 -*-

''' 协调者，封装各类参数和函数
    取代之前shortcut.py中的若干功能
'''

import logging

from wolfox.fengine.core.d1indicator import atr
from wolfox.fengine.core.d1idiom import B0S0,B0S1,B1S0,B1S1,BS_DUMMY
from wolfox.fengine.core.d1match import make_trade_signal,make_trade_signal_advanced
from wolfox.fengine.core.trade import make_trades,last_trade,default_extra,atr_extra
from wolfox.fengine.core.base import CLOSE,OPEN,HIGH,LOW
from wolfox.fengine.core.utils import fcustom

logger = logging.getLogger('wolfox.fengine.core.mediator')

default_pricer = (lambda s : s.transaction[CLOSE],lambda s : s.transaction[CLOSE])

class Mediator(object):
    def __init__(self,buy_signal_maker,sell_signal_maker
            ,taxrate=125
            ,trade_signal_maker=make_trade_signal,trade_strategy=B1S1
            ,pricer = default_pricer,extra_func=atr_extra):
        self.buy_signal_maker = buy_signal_maker
        self.sell_signal_maker = sell_signal_maker
        self.trade_signal_maker = trade_signal_maker
        self.trade_strategy = trade_strategy
        self.buy_pricer = pricer[0]
        self.sell_pricer = pricer[1]
        self.extra_func = extra_func
        self.taxrate = taxrate
        self.make_trades = fcustom(make_trades,taxrate=taxrate,extra_func=extra_func)
        self.last_trade = fcustom(last_trade,taxrate=taxrate,extra_func=extra_func)

    def name(self):
        return 'Mediator:<%s:%s:%s:%s>' % (self.buy_signal_maker.__name__,self.sell_signal_maker.__name__,
                self.trade_signal_maker.__name__,self.trade_strategy.__name__)

    def calc(self,sdata,dates,begin=0,**kwargs):
        return self._calc(self.make_trades,sdata,dates,begin,**kwargs)

    def calc_last(self,sdata,dates,begin=0,**kwargs):
        return self._calc(self.last_trade,sdata,dates,begin,**kwargs)

    def _calc(self,tmaker,sdata,dates,begin=0,**kwargs):
        trades = []
        for s in sdata.values():
            try:    #捕捉某些异常，如未划入任何板块的股票在计算板块相关信号时会出错
                self.prepare(s)
                sbuy = self.buy_signal_maker(s)
                ssell = self.sell_signal_maker(s,sbuy)
                #sbuy,ssell = smooth2(s.transaction[VOLUME],sbuy,ssell) #这个处理被划入bMsN_trade_func中
                trades.extend(self.trade_maker(tmaker,dates,s,sbuy,ssell,begin=begin))
            except Exception,inst:
                print 'mediator _calc %s except : %s' % (s.code,inst)
                logger.warning('%s calc error : %s',s.code,inst)
        return trades
    
    def trade_maker(self,tmaker,dates,stock,sbuy,ssell,begin=0):  #kwargs目的是吸收无用参数，便于cruiser
        ''' trade_strategy是对sbuy和ssell进行预处理，如买卖都是次日交易则为B1S1 
        '''
        t = stock.transaction
        sbuy,ssell = self.trade_strategy(t,sbuy,ssell)
        ssignal = self.trade_signal_maker(sbuy,ssell)
        return tmaker(stock,ssignal,dates,self.buy_pricer(stock),self.sell_pricer(stock),begin=begin)

    def prepare(self,stock):
        trans = stock.transaction
        stock.atr = atr(trans[CLOSE],trans[HIGH],trans[LOW],20)

#收盘价买入，下限突破价卖出，必须有下限突破线
cl_pricer = (lambda s : s.transaction[CLOSE],lambda s : s.down_limit)

#定制的Mediator
#一次买入一次买出，买入信号次日有效，卖出信号当日起效
Mediator10 = fcustom(Mediator,trade_strategy=B1S0,pricer = cl_pricer)
#允许连续买入一次卖出，买入信号次日有效，卖出信号当日起效
CMediator10 = fcustom(Mediator,trade_signal_maker=make_trade_signal_advanced
        ,trade_strategy=B1S0,pricer = cl_pricer)

