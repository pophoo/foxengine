# -*- coding:utf-8 -*-

''' 协调者，封装各类参数和函数
    取代之前shortcut.py中的若干功能
'''

import numpy as np

import logging

from wolfox.fengine.base.common import Trade
from wolfox.fengine.core.d1 import greater,rollx
from wolfox.fengine.core.d1indicator import atr
from wolfox.fengine.core.future import mm_ratio,mm_sum
from wolfox.fengine.core.d1idiom import B0S0,B0S1,B1S0,B1S1,BS_DUMMY
from wolfox.fengine.core.d1match import make_trade_signal,make_trade_signal_advanced
from wolfox.fengine.core.trade import make_trades,last_trade,match_trades,default_extra,atr_extra
from wolfox.fengine.core.base import CLOSE,OPEN,HIGH,LOW
from wolfox.fengine.core.utils import fcustom

logger = logging.getLogger('wolfox.fengine.core.mediator')

default_pricer = (lambda s : s.transaction[CLOSE],lambda s : s.transaction[CLOSE])

class Mediator(object):
    def __init__(self,buy_signal_maker,sell_signal_maker
            ,taxrate=125
            ,trade_signal_maker=make_trade_signal
            ,matcher = match_trades
            ,trade_strategy=B1S1
            ,pricer = default_pricer,extra_func=atr_extra):
        self.buy_signal_maker = buy_signal_maker
        self.sell_signal_maker = sell_signal_maker
        self.trade_signal_maker = trade_signal_maker
        self.matcher = matcher
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

    def calc_matched(self,sdata,dates,begin=0,**kwargs):
        return self.matcher(self._calc(self.make_trades,sdata,dates,begin,**kwargs))

    def calc_last(self,sdata,dates,begin=0,**kwargs):
        return self._calc(self.last_trade,sdata,dates,begin,**kwargs)

    def _calc(self,tmaker,sdata,dates,begin=0,**kwargs):
        trades = []
        for s in sdata.values():
            try:    #捕捉某些异常，如未划入任何板块的股票在计算板块相关信号时会出错
                self.prepare(s,**kwargs)
                sbuy = self.buy_signal_maker(s)
                ssell = self.sell_signal_maker(s,sbuy)
                #logger.debug('sbuy:%s',sbuy.tolist())                
                #sbuy,ssell = smooth2(s.transaction[VOLUME],sbuy,ssell) #这个处理被划入limit_adjust
                trades.extend(self.trade_maker(tmaker,dates,s,sbuy,ssell,begin=begin))
                self.finishing(s,sbuy,ssell)
            except Exception,inst:
                print u'mediator _calc %s except : %s' % (s.code,inst)
                logger.exception(u'%s calc error : %s',s.code,inst)
        return trades
    
    def trade_maker(self,tmaker,dates,stock,sbuy,ssell,begin=0):  #kwargs目的是吸收无用参数，便于cruiser
        ''' trade_strategy是对sbuy和ssell进行预处理，如买卖都是次日交易则为B1S1 
        '''
        t = stock.transaction
        sbuy,ssell = self.trade_strategy(t,sbuy,ssell)
        #logger.debug(u'sbuy,after strategy:%s',sbuy.tolist())
        #logger.debug(u'ssell,after strategy:%s',ssell.tolist())
        ssignal = self.trade_signal_maker(sbuy,ssell)
        return tmaker(stock,ssignal,dates,self.buy_pricer(stock),self.sell_pricer(stock),begin=begin)

    def prepare(self,stock,atr_covered=20,mm_covered=20,**kwargs):  #kwargs吸收无用参数
        trans = stock.transaction
        stock.atr = atr(trans[CLOSE],trans[HIGH],trans[LOW],atr_covered)
        stock.mfe,stock.mae = mm_ratio(trans[CLOSE],trans[HIGH],trans[LOW],stock.atr,covered=mm_covered)

    def finishing(self,stock,sbuy,ssell):
        stock.mfe_sum,stock.mae_sum = mm_sum(sbuy,stock.mfe,stock.mae)
        stock.mm_count = int(np.sum(greater(sbuy)))



#收盘价买入，下限突破价卖出，必须有下限突破线
cl_pricer = (lambda s : s.transaction[CLOSE],lambda s : s.down_limit)
#开盘价买入，下限突破价卖出，必须有下限突破线
ol_pricer = (lambda s : s.transaction[OPEN],lambda s : s.down_limit)
#开盘价买入，开盘价卖出
oo_pricer = (lambda s : s.transaction[OPEN],lambda s : s.transaction[OPEN])
#收盘价买入，开盘价卖出
co_pricer = (lambda s : s.transaction[CLOSE],lambda s : s.transaction[OPEN])

#定制的Mediator
#一次买入一次买出，买入信号次日有效，卖出信号当日起效
Mediator10 = fcustom(Mediator,trade_strategy=B1S0,pricer = cl_pricer)
#允许连续买入一次卖出，买入信号次日有效，卖出信号当日起效
CMediator10 = fcustom(Mediator,trade_signal_maker=make_trade_signal_advanced
        ,trade_strategy=B1S0,pricer = cl_pricer)
OMediator10 = fcustom(Mediator,trade_signal_maker=make_trade_signal_advanced
        ,trade_strategy=B1S0,pricer = cl_pricer)

def mediator_factory(trade_signal_maker=make_trade_signal_advanced,trade_strategy=B1S0,pricer = cl_pricer):
    return fcustom(Mediator,trade_signal_maker = trade_signal_maker,trade_strategy = trade_strategy,pricer=pricer)

dummy_trades = [Trade(-1,0,0,1),Trade(-1,0,0,-1)]
class MM_Mediator(Mediator):
    ''' 只用于计算mm_ratio的mediator
    '''
    def _calc(self,tmaker,sdata,dates,begin=0,**kwargs):
        raise NotImplementedError(u'MM_Mediator不能调用_calc')

    def calc_matched(self,sdata,dates,begin=0,**kwargs):
        trades = []
        for s in sdata.values():
            try:    #捕捉某些异常，如未划入任何板块的股票在计算板块相关信号时会出错
                self.prepare(s,**kwargs)
                sbuy = self.buy_signal_maker(s)
                for i in range(np.sum(sbuy)):   #假Trade数据
                    trades.append(dummy_trades)
                self.finishing(s,sbuy,None)
            except Exception,inst:
                print u'dummy mediator _calc %s except : %s' % (s.code,inst)
                logger.exception(u'%s calc error : %s',s.code,inst)
        return trades

