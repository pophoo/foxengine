# -*- coding:utf-8 -*-

''' 协调者，封装各类参数和函数
    取代之前shortcut.py中的若干功能
'''

import logging

from wolfox.fengine.core.d1idiom import B0S0,B0S1,B1S0,B1S1,BS_DUMMY
from wolfox.fengine.core.d1match import make_trade_signal,make_trade_signal_advanced
from wolfox.fengine.core.trade import make_trades,last_trade
from wolfox.fengine.core.base import CLOSE,OPEN,HIGH,LOW

logger = logging.getLogger('wolfox.fengine.core.mediator')

default_pricer = (lambda s : s.transaction[CLOSE],lambda s : s.transaction[CLOSE])

class Mediator(object):
    def __init__(self,buy_signal_maker,sell_signal_maker
            ,trade_signal_maker=make_trade_signal,trade_strategy=B1S1,pricer = default_pricer):
        self.buy_signal_maker = buy_signal_maker
        self.sell_signal_maker = sell_signal_maker
        self.trade_signal_maker = trade_signal_maker
        self.trade_strategy = trade_strategy
        self.buy_pricer = pricer[0]
        self.sell_pricer = pricer[1]

    def name(self):
        return 'Mediator:<%s:%s:%s:%s>' % (self.buy_signal_maker.__name__,self.sell_signal_maker.__name__,
                self.trade_signal_maker.__name__,self.trade_strategy.__name__)

    def calc(self,sdata,dates,begin=0,taxrate=125,**kwargs):
        return self._calc(make_trades,sdata,dates,begin,taxrate,**kwargs)

    def calc_last(self,sdata,dates,begin=0,taxrate=125,**kwargs):
        return self._calc(last_trade,sdata,dates,begin,taxrate,**kwargs)

    def _calc(self,tmaker,sdata,dates,begin=0,taxrate=125,**kwargs):
        trades = []
        for s in sdata.values():
            try:    #捕捉某些异常，如未划入任何板块的股票在计算板块相关信号时会出错
                sbuy = self.buy_signal_maker(s)
                ssell = self.sell_signal_maker(s,sbuy)
                #sbuy,ssell = smooth2(s.transaction[VOLUME],sbuy,ssell) #这个处理被划入bMsN_trade_func中
                trades.extend(self.trade_maker(tmaker,dates,s,sbuy,ssell,begin=begin,taxrate=taxrate))
            except Exception,inst:
                print '%s except : %s' % (s.code,inst)
                logger.warning('%s calc error : %s',s.code,inst)
        return trades
    
    def trade_maker(self,tmaker,dates,stock,sbuy,ssell,begin=0,taxrate=125):  #kwargs目的是吸收无用参数，便于cruiser
        ''' trade_strategy是对sbuy和ssell进行预处理，如买卖都是次日交易则为B1S1 
        '''
        t = stock.transaction
        sbuy,ssell = self.trade_strategy(t,sbuy,ssell)
        ssignal = self.trade_signal_maker(sbuy,ssell)
        return tmaker(stock.code,ssignal,dates,self.buy_pricer(stock),self.sell_pricer(stock),begin,taxrate)    


