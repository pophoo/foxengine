# -*- coding: utf-8 -*-

#指定股票的测试运行脚本

from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *
from wolfox.fengine.core.base import cache
from wolfox.fengine.core.d1ex import tmax,derepeatc,derepeatc_v,equals
from wolfox.fengine.core.d1match import *
from wolfox.fengine.core.d1indicator import cmacd
from wolfox.foxit.base.tutils import linelog
from time import time

import logging
logger = logging.getLogger('wolfox.fengine.normal.sfuncs')    

def tsvama2(stock,fast,slow):
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

def pmacd(stock):
    t = stock.transaction
    pdiff,pdea = cmacd(t[VOLUME])
    dcross = gand(cross(pdea,pdiff),strend(pdiff)>0,strend(pdea>0))
    linelog(stock.code)
    cs = catalog_signal_cs(stock.c60,stock.silver)
    return gand(dcross,stock.golden,stock.above,cs,pdea>0,pdea<12000)


def nhigh(stock):#60高点
    t = stock.transaction
    mline = rollx(tmax(t[HIGH],60)) #以昨日的60高点为准
    dcross = cross(mline,t[HIGH])>0    
    linelog(stock.code)
    cs = catalog_signal_cs(stock.c60,stock.silver)
    return gand(stock.golden,cs,dcross,strend(stock.ma60)>0,stock.above)

def xma60(stock):
    ''' 碰到ma60后回升
    '''
    t = stock.transaction
    water_line = stock.ma60*115/100   #上方15处
    dcross = cross(water_line,t[LOW])
    up_cross = dcross > 0
    down_cross = dcross < 0
    sync = sfollow(down_cross,up_cross,5)
    linelog(stock.code)
    return gand(sync,stock.above,stock.t120)

def wvad(stock):
    t = stock.transaction
    vad = (t[CLOSE]-t[OPEN])*t[VOLUME]/(t[HIGH]-t[LOW]) / 10000
    svad = msum2(vad,24)
    ma_svad = ma(svad,6)
    cs = catalog_signal_cs(stock.c60,stock.silver)
    ecross = gand(stock.golden,cs,cross(ma_svad,vad)>0,strend(ma_svad)>0,stock.t120,stock.above)
    linelog(stock.code)
    return ecross

@cache
def cached_zeros(n):
    return np.zeros(n,int)

def temv(stock):
    t = stock.transaction
    ts = cached_zeros(len(t[CLOSE]))
    ekey = 'emv'
    em = emv(t[HIGH],t[LOW],t[VOLUME])
    mv = msum2(em,14)
    semv = ma(mv,9)
    cs = catalog_signal_cs(stock.c60,stock.silver)
    ecross = gand(stock.golden,cs,cross(ts,mv)>0,strend(semv)>0,stock.t120,stock.above)
    linelog(stock.code)
    return ecross
    
def vmacd_ma4(stock):
    t = stock.transaction
    
    vdiff,vdea = cmacd(t[VOLUME])
    dcross = gand(cross(vdea,vdiff),strend(vdiff)>0,strend(vdea>0))

    cs = catalog_signal_cs(stock.c60,stock.silver)
    return gand(stock.golden,dcross,stock.above,stock.t120,vdea>0,vdea<12000)

def ma4(stock):
    t = stock.transaction
    ma5 = ma(t[CLOSE],5)
    dcross = gand(cross(stock.ma10,ma5),strend(ma5)>0,strend(stock.ma10)>0,strend(stock.ma20)>0,strend(stock.ma60)>0,stock.t120>0)
    cs = catalog_signal_cs(stock.c60,stock.silver)
    linelog(stock.code)
    return gand(stock.golden,cs,dcross,stock.above)

def vmacd(stock):
    t = stock.transaction
    vdiff,vdea = cmacd(t[VOLUME])
    dcross = gand(cross(vdea,vdiff),strend(vdiff)>0,strend(vdea>0))
    linelog(stock.code)
    cs = catalog_signal_cs(stock.c60,stock.silver)
    return gand(dcross,stock.golden,stock.t120,cs,vdea>0,vdea<12000)

