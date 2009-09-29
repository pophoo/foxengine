# -*- coding: utf-8 -*-

#60分钟处理

from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *
import wolfox.fengine.normal.sfuncs as s
from wolfox.fengine.core.d1ex import tmax,derepeatc,derepeatc_v,equals,msum,scover,rsub
from wolfox.fengine.core.d1match import *
from wolfox.fengine.core.d1idiom import *
from wolfox.fengine.core.d1indicator import cmacd,score2
from wolfox.fengine.core.d1 import lesser
from wolfox.foxit.base.tutils import linelog
from time import time

import logging
logger = logging.getLogger('wolfox.fengine.normal.hfuncs')    

def prepare_hour(stock,begin,end):
    linelog('prepare hour:%s' % stock.code)
    t = get_hour(stock.code,begin,end)
    pdiff,pdea = cmacd(t[CLOSE])
    upcross = gand(cross(pdea,pdiff)>0,strend(pdiff)>0,pdiff<10) #<0才保险
    downcross = gand(cross(pdea,pdiff)<0,strend(pdiff)<0) 
    stock.hup = hour2day(upcross)
    stock.hdown = hour2day(downcross)
    stock.hmxc = hour2day(xc0s(t[OPEN],t[CLOSE],t[HIGH],t[LOW],ma1=13) > 0)
    dsub = rsub(pdiff,upcross)
    csub = rsub(t[CLOSE],upcross)
    stock.hdev = hour2day(band(greater(dsub),lesser(csub)))
    prepare_hour2(stock,begin,end)

def prepare_hour2(stock,begin,end):
    linelog('prepare hour:%s' % stock.code)
    t = get_hour(stock.code,begin,end)
    mdiff,mdea = macd_ruv3(t[OPEN],t[CLOSE],t[HIGH],t[LOW],t[VOLUME])
    mxc = cross(mdea,mdiff) > 0
    stock.xru3 = hour2day(mxc)
    mdiff,mdea = macd_ruv(t[OPEN],t[CLOSE],t[HIGH],t[LOW],t[VOLUME])
    mxc = cross(mdea,mdiff) > 0
    stock.xru = hour2day(mxc)

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

def gmacd5(stock,ldown=30,astart=60): #
    t = stock.transaction
    
    mdiff,mdea = cmacd(stock.g5)   

    xcross = gand(cross(mdea,mdiff) > 0)

    linelog(stock.code)

    #ss = sfollow(xcross,stock.mup,3)
    ss = band(xcross,stock.mup)

    #gf1 = gand(stock.g20>5000,stock.g20<9500)

    xatr = stock.atr * BASE / t[CLOSE]     
    
    signal = gand(ss,stock.above,stock.t5,strend(stock.ma4)>0,t[VOLUME]>0,mdiff>=mdea,strend(stock.ref.ma4)>0,xatr>=astart)
    
    return signal

def hxud(stock):
    '''
        vfilter = gand(svma<vma*2/3)
        评估:总盈亏值=12444,交易次数=36 期望值=6764
                总盈亏率(1/1000)=12444,平均盈亏率(1/1000)=345,盈利交易率(1/1000)=944
                平均持仓时间=48,持仓效率(1/1000000)=7187
                赢利次数=34,赢利总值=12546
                亏损次数=2,亏损总值=102
                平盘次数=0
        vfilter = gand(svma<vma*3/5)
        评估:总盈亏值=9933,交易次数=26  期望值=10052
                总盈亏率(1/1000)=9933,平均盈亏率(1/1000)=382,盈利交易率(1/1000)=961
                平均持仓时间=53,持仓效率(1/1000000)=7207
                赢利次数=25,赢利总值=9971
                亏损次数=1,亏损总值=38
                平盘次数=0
                
    '''
    t = stock.transaction
    linelog(stock.code)
    xatr = stock.atr * BASE / t[CLOSE]     
    #mxc = xc0s(t[OPEN],t[CLOSE],t[HIGH],t[LOW],ma1=13) > 0

    ss = syntony(stock.hup,stock.hmxc,3)
    #sss = sfollow(mxc,ss,3)
    #ss = gand(stock.hup,stock.hmxc)

    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)
    vfilter = gand(svma<vma*3/5)    #2/3

    cf = (t[OPEN]-t[LOW] + t[HIGH]-t[CLOSE])*1000 / (t[HIGH]-t[LOW])   #向下的动力  
    mcf = ma(cf,7)

    s=stock
    signal = gand(ss,vfilter,mcf>1000,stock.t5,stock.above,strend(stock.ma4)>0,t[VOLUME]>0,xatr>45,stock.ma1<stock.ma2,stock.ma1>stock.ma3,s.g20 >= s.g60,s.g60 >= s.g120,s.g120 >= s.g250,s.g20<=8000,s.g5<s.g20,s.g20>=6500)
    return signal

def hxud2(stock):
    signal = s.xud(stock,astart=0)
    ss = sfollow(signal,stock.hdev,30)
    return ss

def hmacd(stock):
    linelog(stock.code)
    signal = gand(stock.above,stock.t5,stock.mup)
    return signal

def hmacd_seller(stock,buy_signal,**kwargs):
    signal = greater(msum2(stock.hdown,5),1)
    return signal

def hdev(stock):
    ''' 
        vfilter = gand(svma<vma*2/3)
        评估:总盈亏值=2465,交易次数=8   期望值=1000
                总盈亏率(1/1000)=2465,平均盈亏率(1/1000)=308,盈利交易率(1/1000)=1000
                平均持仓时间=39,持仓效率(1/1000000)=7897
                赢利次数=8,赢利总值=2465
                亏损次数=0,亏损总值=0
                平盘次数=0
        vfilter = gand(svma<vma*4/5)
        评估:总盈亏值=2542,交易次数=9   期望值=1000
                总盈亏率(1/1000)=2542,平均盈亏率(1/1000)=282,盈利交易率(1/1000)=1000
                平均持仓时间=37,持仓效率(1/1000000)=7621
                赢利次数=9,赢利总值=2542
                亏损次数=0,亏损总值=0
                平盘次数=0
        
    '''
    t = stock.transaction    
    linelog(stock.code)
    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)
    vfilter = gand(svma<vma*4/5)
    xatr = stock.atr * BASE / t[CLOSE]
    cf = (t[OPEN]-t[LOW] + t[HIGH]-t[CLOSE])*1000 / (t[HIGH]-t[LOW])   #向下的动力  
    mcf = ma(cf,7)
    
    s=stock
    #signal = gand(stock.hdev,stock.t5,vfilter,mcf>1000,stock.g5<stock.g60,s.g20 >= s.g60,s.g60 >= s.g120,s.g120 >= s.g250,s.g20<=8000)
    signal = gand(stock.hdev,stock.t5,strend(stock.ma4)>0,mcf>1000,vfilter,stock.g5<stock.g60,s.g20 >= s.g60,s.g60 >= s.g120,s.g120 >= s.g250,s.g20<=8000)
    return signal

def hemv1b(stock,fast=15,base=120):
    t = stock.transaction

    em = emv(t[HIGH],t[LOW],t[VOLUME])
    mv1 = msum2(em,fast)
    mvbase = msum2(em,base)

    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)

    vfilter = gand(svma<=vma*3/4)

    baseline = cached_zeros(len(t[CLOSE]))

    thumb = gand(stock.magic,stock.g20>3000)

    ss = sfollow(cross(baseline,mv1)>0,stock.hup,30)

    ecross = gand(ss,thumb,strend(mv1)>0,stock.t5,stock.above,strend(mvbase)>0,vfilter)
    linelog(stock.code)
    return ecross

def hmxru3(stock):
    ''' 成交量分配后的macd,采用supdown3
        评估:总盈亏值=6163,交易次数=22  期望值=3733
                总盈亏率(1/1000)=6163,平均盈亏率(1/1000)=280,盈利交易率(1/1000)=863
                平均持仓时间=48,持仓效率(1/1000000)=5833
                赢利次数=19,赢利总值=6389
                亏损次数=3,亏损总值=226
                平盘次数=0
    '''
    t = stock.transaction
    mxc = stock.xru3
    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)
    vfilter = gand(svma<vma*2/3,svma>vma/2,t[VOLUME]<=vma*2/3)
    xatr = stock.atr * BASE / t[CLOSE]     
    
    s = stock
    signal = gand(s.above,mxc,vfilter,strend(stock.ma4)>0,stock.t5,xatr>=50,stock.magic,stock.ma1<stock.ma2,stock.ma1>stock.ma3)
    linelog(stock.code)
    return signal

def hmxru(stock):
    ''' 成交量分配后的macd,采用supdown
        vfilter = svma < vma * 2/3    
        评估:总盈亏值=4813,交易次数=14  期望值=5444
                总盈亏率(1/1000)=4813,平均盈亏率(1/1000)=343,盈利交易率(1/1000)=928
                平均持仓时间=50,持仓效率(1/1000000)=6860
                赢利次数=13,赢利总值=4876
                亏损次数=1,亏损总值=63
                平盘次数=0
        vfilter = gand(svma<vma*2/3,t[VOLUME]<=vma*2/3)
        评估:总盈亏值=3810,交易次数=8   期望值=1000
                总盈亏率(1/1000)=3810,平均盈亏率(1/1000)=476,盈利交易率(1/1000)=1000
                平均持仓时间=65,持仓效率(1/1000000)=7323
                赢利次数=8,赢利总值=3810
                亏损次数=0,亏损总值=0
                平盘次数=0

    '''
    t = stock.transaction
    mxc = stock.xru
    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)
    vfilter = gand(svma<vma*2/3,t[VOLUME]<=vma*2/3)
    #vfilter = gand(svma<vma*2/3)
    xatr = stock.atr * BASE / t[CLOSE]     
    
    s = stock
    signal = gand(mxc,stock.above,vfilter,strend(stock.ma4)>0,stock.t5,xatr>=60,stock.magic,stock.ma1<stock.ma2,stock.ma1>stock.ma3)
    linelog(stock.code)
    return signal

def hspring(stock,threshold=-30):
    ''' 对于结果
        下影越短越好，close-low/close 也是越短越好
    '''
    t = stock.transaction
    linelog('spring:%s' % stock.code)
    
    s11 = gand(stock.ks >=-5,stock.ks<0,stock.ref.ks<=threshold)
    s12 = gand(stock.ks >=5,stock.ks<20,stock.ref.ks<=threshold)
    s1 = bor(s11,s12)
    s21 = gand(stock.ks>=5,stock.ks<75,stock.ref.ks<=threshold)

    signals = bor(s1,s21)

    ss = sfollow(signals,stock.hup,10)


    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)
    vfilter = gand(svma<vma*7/8,svma>vma/2,t[VOLUME]<=vma*2/3)    
    return gand(ss,stock.magic,stock.above,vfilter)


