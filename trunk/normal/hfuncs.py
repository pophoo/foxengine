# -*- coding: utf-8 -*-

#60分钟处理

from wolfox.fengine.core.shortcut import *
from wolfox.foxit.base.tutils import linelog
from time import time

import logging
logger = logging.getLogger('wolfox.fengine.normal.hfuncs')    

def prepare_hour(stock,begin,end):
    t = get_hour(stock.code,begin,end)
    pdiff,pdea = cmacd(t[CLOSE])
    upcross = gand(cross(pdea,pdiff)>0,strend(pdiff)>0)
    downcross = gand(cross(pdea,pdiff)<0,strend(pdiff)<0) 
    stock.mup = hour2day(upcross)
    stock.mdown = hour2day(downcross)

def tsvama2_old(stock,fast,slow):
    t = stock.transaction
    svap,v2i = stock.svap_ma_67 
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))
    linelog('%s:%s' % (tsvama2.__name__,stock.code))
    return gand(stock.golden,msvap,stock.above)    
