# -*- coding: utf-8 -*-

#指定股票的测试运行脚本

from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *
from wolfox.fengine.core.d1ex import tmax,derepeatc,derepeatc_v,equals,msum
from wolfox.fengine.core.d1match import *
from wolfox.fengine.core.d1idiom import *
from wolfox.fengine.core.d1indicator import cmacd,score2
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

def tsvama2a(stock,fast=20,slow=100):
    ''' svama两线交叉
        加vfilter
    '''
    t = stock.transaction
    svap,v2i = stock.svap_ma_67 
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)

    ss = cross_fast_slow
    msvap = transform(ss,v2i,len(t[VOLUME]))
    linelog('%s:%s' % (tsvama2.__name__,stock.code))

    vdiff,vdea = cmacd(t[VOLUME])

    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = vma_s < vma_l * 7/8
 
    linelog('%s:%s' % (tsvama2a.__name__,stock.code))
    return gand(stock.golden,msvap,stock.above,vfilter)


def tsvama2b(stock,fast=20,slow=170):
    ''' svama两线交叉
        另加smacd,vfilter
    '''
    t = stock.transaction
    svap,v2i = stock.svap_ma_67 
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)

    sdiff,sdea = cmacd(svap)
    ss = gand(cross_fast_slow,strend(sdiff-sdea)>0)
    #ss = cross_fast_slow
    msvap = transform(ss,v2i,len(t[VOLUME]))
    linelog('%s:%s' % (tsvama2.__name__,stock.code))

    vdiff,vdea = cmacd(t[VOLUME])

    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = gand(vma_s < vma_l * 7/8)  #t[CLOSE]>stock.ma1无好处
 
    linelog('%s:%s' % (tsvama2b.__name__,stock.code))
    return gand(stock.golden,msvap,stock.above,vfilter)


def pmacd(stock):
    t = stock.transaction
    pdiff,pdea = cmacd(t[CLOSE])
    dcross = gand(cross(pdea,pdiff),strend(pdiff)>0,strend(pdea>0))
    linelog(stock.code)
    #return gand(dcross,stock.golden,stock.above,cs,pdea>0,pdea<12000)
    return gand(dcross,stock.thumb,stock.above,stock.silver,pdea>0,pdea<12000)

def nhigh(stock):#60高点
    t = stock.transaction
    mline = rollx(tmax(t[HIGH],60)) #以昨日的60高点为准
    dcross = cross(mline,t[HIGH])>0    
    g = gand(stock.g5>=stock.g20,stock.thumb)
    #linelog(stock.code)
    return gand(g,stock.silver,dcross,strend(stock.ma4)>0,stock.above)

def xma60(stock):
    ''' 碰到ma4后回升
        cs,g = gand(stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)    ##最佳
        评估:总盈亏值=13321,交易次数=45 期望值=6040
                总盈亏率(1/1000)=13321,平均盈亏率(1/1000)=296,盈利交易率(1/1000)=622
                赢利次数=28,赢利总值=14170
                亏损次数=17,亏损总值=849
                平盘次数=0
        
        #金手指
        评估:总盈亏值=33283,交易次数=173        期望值=2493
                总盈亏率(1/1000)=33283,平均盈亏率(1/1000)=192,盈利交易率(1/1000)=526
                赢利次数=91,赢利总值=39607
                亏损次数=82,亏损总值=6324
                平盘次数=0

        #金手指+cs<6600
        评估:总盈亏值=5530,交易次数=17  期望值=8333
                总盈亏率(1/1000)=5530,平均盈亏率(1/1000)=325,盈利交易率(1/1000)=705
                赢利次数=12,赢利总值=5727
                亏损次数=5,亏损总值=197
                平盘次数=0
        
        #银手指
        评估:总盈亏值=23766,交易次数=87 期望值=4706
                总盈亏率(1/1000)=23766,平均盈亏率(1/1000)=273,盈利交易率(1/1000)=574
                赢利次数=50,赢利总值=25929
                亏损次数=37,亏损总值=2163
                平盘次数=0

        sync,stock.above,stock.t5,s.g20 >= s.g60,s.g60 >= s.g120,s.g120 >= s.g250,s.g5>=3000,s.g5<=8000,stock.silver
        评估:总盈亏值=11019,交易次数=36 期望值=4781
                总盈亏率(1/1000)=11019,平均盈亏率(1/1000)=306,盈利交易率(1/1000)=777
                赢利次数=28,赢利总值=11535
                亏损次数=8,亏损总值=516
                平盘次数=0
                
    '''
    t = stock.transaction
    water_line = stock.ma4*115/100   #上方15处
    dcross = cross(water_line,t[LOW])
    up_cross = dcross > 0
    down_cross = dcross < 0
    sync = sfollow(down_cross,up_cross,7)
    linelog(stock.code)
    #return gand(sync,stock.above,stock.t5,stock.golden,cs)    
    return gand(sync,stock.above,stock.t5,stock.thumb,stock.silver)

def wvad(stock):
    t = stock.transaction
    vad = (t[CLOSE]-t[OPEN])*t[VOLUME]/(t[HIGH]-t[LOW]) / 10000
    svad = msum2(vad,24)
    ma_svad = ma(svad,6)
    #ecross = gand(stock.golden,cs,cross(ma_svad,vad)>0,strend(ma_svad)>0,stock.t5,stock.above)
    ecross = gand(stock.thumb,stock.silver,cross(ma_svad,vad)>0,strend(ma_svad)>0,stock.t5,stock.above)
    linelog(stock.code)
    return ecross

def temv(stock):
    '''
    name:Mediator:<temv:atr_seller:up_sector=2,trace_times=3000,stop_times=1200,covered=10:make_trade_signal_advanced:B1S1>
    pre_ev:	评估:总盈亏值=2244,交易次数=14	期望值=4210	
		总盈亏率(1/1000)=2244,平均盈亏率(1/1000)=160,盈利交易率(1/1000)=428
		赢利次数=6,赢利总值=2555
		亏损次数=8,亏损总值=311
		平盘次数=0
		闭合交易明细:
    
    '''
    t = stock.transaction
    ts = cached_zeros(len(t[CLOSE]))
    ekey = 'emv'
    em = emv(t[HIGH],t[LOW],t[VOLUME])
    mv = msum2(em,14)
    semv = ma(mv,9)
    ecross = gand(stock.thumb,stock.silver,cross(ts,mv)>0,strend(semv)>0,stock.t5,stock.above)
    linelog(stock.code)
    return ecross
    
def vmacd_ma4(stock):
    t = stock.transaction
    
    vdiff,vdea = cmacd(t[VOLUME])
    dcross = gand(cross(vdea,vdiff)>0,strend(vdiff)>0,strend(vdea)>0)

    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)

    c_ex = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=8500)
    cs = catalog_signal_cs(stock.c60,c_ex)    
    return gand(g,cs,dcross,stock.above,strend(stock.ma4)>0,vdea>=0,vdea<=12000)

def ma4(stock): #3X10
    t = stock.transaction
    fma = ma(t[CLOSE],3)
    dcross = gand(cross(stock.ma2,fma),strend(fma)>0,strend(stock.ma2)>0,strend(stock.ma3)>0,strend(stock.ma4)>0,stock.t5>0)
    linelog(stock.code)
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    #return gand(stock.golden,cs,dcross,stock.above,stock.t5)
    return gand(g,stock.silver,dcross,stock.above)    

def vmacd(stock):
    t = stock.transaction
    vdiff,vdea = cmacd(t[VOLUME])
    dcross = gand(cross(vdea,vdiff),strend(vdiff)>0,strend(vdea>0))
    linelog(stock.code)
    return gand(dcross,stock.golden,stock.t5,stock.silver,vdea>0,vdea<12000)

def gx60(stock,fast=5,slow=20):
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    g60 = stock.g60
    ma_fast = ma(g60,fast)
    ma_slow = ma(g60,slow)
    trend_ma_fast = strend(ma_fast) > 0
    trend_ma_slow = strend(ma_slow) > 0    
    cross_fast_slow = gand(cross(ma_slow,ma_fast)>0,trend_ma_fast,trend_ma_slow)

    #c_ex = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=6600)

    linelog(stock.code)

    ma_120 = ma(stock.g120,5)   #平滑一下
    ma_250 = ma(stock.g250,5)
    trend_ma_120 = strend(ma_120) > 0
    trend_ma_250 = strend(ma_250) > 0

    return gand(cross_fast_slow,g,stock.silver,stock.above,stock.t5,trend_ma_120,trend_ma_250)

def gx250(stock,fast=10,slow=67):
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    gx = stock.g250
    ma_fast = ma(gx,fast)
    ma_slow = ma(gx,slow)
    trend_ma_fast = strend(ma_fast) > 0
    trend_ma_slow = strend(ma_slow) > 0    
    cross_fast_slow = gand(cross(ma_slow,ma_fast)>0,trend_ma_fast,trend_ma_slow)

    #c_ex = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=6600)

    linelog(stock.code)

    ma_120 = ma(stock.g120,5)   #平滑一下
    ma_250 = ma(stock.g250,5)
    trend_ma_120 = strend(ma_120) > 0
    trend_ma_250 = strend(ma_250) > 0

    return gand(cross_fast_slow,stock.golden,stock.silver,stock.above,stock.t5,trend_ma_120,trend_ma_250)


def gcs(stock):
    '''
        20000101-20090101
        评估:总盈亏值=29163,交易次数=206        期望值=1880
                总盈亏率(1/1000)=29163,平均盈亏率(1/1000)=141,盈利交易率(1/1000)=422
                赢利次数=87,赢利总值=38080
                亏损次数=118,亏损总值=8917
                平盘次数=1
    '''
    t = stock.transaction
    #ma5 = ma(t[CLOSE],5)
    linelog(stock.code)
    sbuy = gand(stock.golden,stock.silver,stock.above,stock.ma1>stock.ma2,stock.ref.t5)
    return sbuy

def xgcs(stock):
    t = stock.transaction
    #ma5 = ma(t[CLOSE],5)
    linelog(stock.code)
    si = score2(t[CLOSE],t[VOLUME])
    mxi = gand(msum(si,5)>=-100,msum(si,5)<=0)
    sbuy = gand(stock.golden,stock.silver,stock.above,stock.ma1>stock.ma2,stock.ref.t5,mxi)
    return sbuy

def xgcs0(stock):
    ''' 下穿0线
        评估:总盈亏值=23464,交易次数=81 期望值=4013
                总盈亏率(1/1000)=23464,平均盈亏率(1/1000)=289,盈利交易率(1/1000)=617
                赢利次数=50,赢利总值=25703
                亏损次数=31,亏损总值=2239
                平盘次数=0
    '''
    t = stock.transaction
    #ma5 = ma(t[CLOSE],5)
    linelog(stock.code)

    si = score2(t[CLOSE],t[VOLUME])
    zs = cached_zeros(len(t[CLOSE]))
    mxi = cross(zs,si)<0

    sbuy = gand(stock.golden,stock.silver,stock.above,stock.ma1>stock.ma2,stock.ref.t5,mxi,t[CLOSE]<stock.ma1)
    return sbuy


def mgcs(stock):
    t = stock.transaction
    linelog(stock.code)
    s = stock
    g = gand(s.g20 >= s.g60,s.g60 >= s.g120,s.g20>=3000,s.g20<=8000,s.g20<=s.g120+1000)     ######
    pdiff,pdea = cmacd(t[CLOSE])
    sbuy = gand(g,pdiff>=225,pdiff<=350,stock.above,stock.ref.t5,strend(stock.ma3)>0,strend(stock.ma4)>0,stock.t5,stock.ref.above)
    return sbuy

def spring(stock,threshold=-30):
    ''' 对于结果
        下影越短越好，close-low/close 也是越短越好
    '''
    t = stock.transaction
    linelog('spring:%s' % stock.code)
    
    s11 = gand(stock.ks >=-5,stock.ks<0,stock.ref.ks<=threshold)
    s12 = gand(stock.ks >=5,stock.ks<20,stock.ref.ks<=threshold)
    s1 = bor(s11,s12)
    s_tt = gand(s1,stock.thumb,stock.t5)
    s21 = gand(stock.ks>=5,stock.ks<75,stock.ref.ks<=threshold)
    s_aa = gand(s21,stock.thumb,stock.above)

    signals = bor(s_aa,s_tt)

    ref = stock.ref
    sbuy = signals #gand(signals,greater(ref.ma2,ref.ma3),greater(ref.ma3,ref.ma4))

    svap,v2i = stock.svap_ma_67
    sdiff,sdea = cmacd(svap,19,39)
    ssignal = gand(strend(sdiff)>0,strend(sdiff-sdea)>0)

    msvap = transform(ssignal,v2i,len(t[VOLUME]))


    return gand(sbuy,msvap)


def cma2(stock,fast,slow,gfrom=0,gto=8500):  
    ''' 传统的ma2
        5 X 20
        评估:总盈亏值=11488,交易次数=54 期望值=3164
                总盈亏率(1/1000)=11488,平均盈亏率(1/1000)=212,盈利交易率(1/1000)=685
                赢利次数=37,赢利总值=12628
                亏损次数=17,亏损总值=1140
                平盘次数=0
            g5: 4000-8000
            评估:总盈亏值=10980,交易次数=38 期望值=4571
                总盈亏率(1/1000)=10980,平均盈亏率(1/1000)=288,盈利交易率(1/1000)=763
                赢利次数=29,赢利总值=11547
                亏损次数=9,亏损总值=567
                平盘次数=0
        5 X 13
        评估:总盈亏值=39727,交易次数=213        期望值=2952
                总盈亏率(1/1000)=39727,平均盈亏率(1/1000)=186,盈利交易率(1/1000)=553
                赢利次数=118,赢利总值=45746
                亏损次数=95,亏损总值=6019
                平盘次数=0
            #g5:7000-8500
            评估:总盈亏值=33922,交易次数=149        期望值=3603
                总盈亏率(1/1000)=33922,平均盈亏率(1/1000)=227,盈利交易率(1/1000)=617
                赢利次数=92,赢利总值=37550
                亏损次数=57,亏损总值=3628
                平盘次数=0
 
    '''
    t = stock.transaction
    water_line = ma(t[CLOSE],slow)
    dcross = cross(water_line,ma(t[CLOSE],fast))

    up_cross = dcross > 0

    linelog(stock.code)
    return gand(up_cross,stock.above,stock.t5,stock.g5>=stock.g20+500,stock.g20>=stock.g60+500,stock.g60>=stock.g120,stock.g5>=gfrom,stock.g5<=gto)


def cma1(stock,length=30,covered=7):  #
    t = stock.transaction
    
    water_line = ma(t[CLOSE],length)
    dcross = cross(water_line,t[LOW])
    up_cross = dcross > 0
    down_cross = dcross < 0
    sync = sfollow(down_cross,up_cross,covered=7)
    return gand(sync,stock.above,stock.t5,stock.thumb,stock.silver)


def x30(t):
    water_line = ma(t[CLOSE],30)
    dcross = cross(water_line,t[LOW])
    up_cross = dcross > 0
    down_cross = dcross < 0
    sync = sfollow(down_cross,up_cross,7)
    return sync

def tsvama2x(stock,fast=20,slow=100):
    ''' svama两线交叉
    '''
    t = stock.transaction
    g = stock.golden
    svap,v2i = stock.svap_ma_67
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))
    signal = msvap
    s2 = x30(t)
    sbuy = sfollow(signal,s2,10)
    linelog('%s:%s' % (tsvama2x.__name__,stock.code))
    return gand(sbuy,stock.above,stock.thumb,stock.silver)


def gmacd_old(stock): #
    ''' 
        20010701-20090101效果不好，但能持平
        20080701开始效果非常好
        ll5 = rollx(t[LOW],5),   hinc = t[HIGH] * 1000 / ll5
        ll10 = rollx(t[LOW],10),    hh10 = tmax(t[HIGH],10), rhl10 = hh10 * 1000/ll10
        lfilter = hinc<1200 and rhl10<1500
        ss1=sfollow(cross(mdea,mdiff) > 0,vdiff<vdea), 然后再sfollow(ss1,cross(ma(t[CLOSE],30),t[LOW]),5),之后+lfilter,2115/704/846
        ss1=sfollow(cross(mdea,mdiff) > 0,vdiff<vdea), 然后再sfollow(ss1,cross(ma(t[CLOSE],30)<0,t[LOW]),5),之后+lfilter,2213/759/595
            g60:4500-8500:  2946/821/286
        ss1=sfollow(cross(mdea,mdiff) > 0,vdiff<vdea), 然后再sfollow(ss1,cross(ma(t[CLOSE],30)<0,t[LOW]),10),之后+lfilter,2392/746/844    
            g60:0-3000:1457/670/273
            g60:3000-6000: 2709/788/402
            g60:6000-!: 2696/758/273
            g60:6000-8500: 2781/775/232
            g60:>8500:  2193/632/49
            g60:4500-8500:  3078/793/411
            g60:4500-7500:  2888/797/345
            g60:5000-8000:  2925/796/324
            数量太多,需要进一步筛选
        ss1=sfollow(cross(mdea,mdiff) > 0,gand(vdiff>vdea,pdiff>pdea)), 然后再sfollow(ss1,cross(ma(t[CLOSE],30)<0,t[LOW]),10),2392/746/844    
            mdiff>=mdea
            g60:4500-8500:3036/800/451
            g20:4500-8500:3886/817/465  #不需要hinc<1200，只需要rhl10<1500,而且效果也有限
            但这个滤掉了600121,600756,000961,600997等
            g20:5000-9000:3877/845/297   
            ####g20:5000-9500:3937/840/300    #去掉mdiff>=mdea,3571/841/416
                添加 strend(stock.ref.ma4)>0   4063/847/295
                above改为13>30>60>120
                #above = gand(stock.ma2 > stock.ma3,stock.ma3>stock.ma4,stock.ma4>stock.ma5)
                signal = gand(ss,stock.above,stock.t5,t[VOLUME]>0,gf1,rhl10<1500,mdiff>=mdea,strend(stock.ref.ma4)>0)
                4217/860/294
            g20:5000-10000:3425/833/306
            g20:6000-9500:3500/847/203
            g20:5000-6000:4097/840/113
            g20:4500-9500:3933/803/346
        仍然无法继续甄别超级强势股,如600756,000961的启动阶段,能够通过cmacd(mdea,mdiff)>0找到初始信号,但无法从噪声中甄别出来
        因为他们不触碰30线,需要进一步考虑
        ss1不变.
        x3 = gand(strend(ma(t[CLOSE],5))>0,strend(stock.ma2)>0,strend(stock.ma3)>0,strend(stock.ma4)>0)
        ss = sfollow(ss1,x3,10)
        
    '''
    t = stock.transaction
    
    mdiff,mdea = cmacd(stock.g60)
    ldiff,ldea = cmacd(stock.g120)
    lldiff,lldea = cmacd(stock.g250)

    vdiff,vdea = cmacd(t[VOLUME])
    pdiff,pdea = cmacd(t[CLOSE])


    #sfilter = vdiff<vdea
    #sfilter = vdiff<vdea
    sfilter = gand(vdiff>vdea,pdiff>pdea)

    xcross = cross(mdea,mdiff) > 0  
    #xcross = cross(mdiff,mdea) > 0  

    linelog(stock.code)


    ll10 = rollx(t[LOW],10)
    hh10 = tmax(t[HIGH],10)
    rhl10 = hh10 * 1000/ll10

    ss1 = sfollow(xcross,sfilter,5)
    
    x2 = cross(ma(t[CLOSE],30),t[LOW]) < 0
    
    ss = sfollow(ss1,x2,10)

    gf1 = gand(stock.g20>5000,stock.g20<9500)

    #signal = gand(xcross,stock.above,stock.t5,t[VOLUME]>0,hinc<1200,rhl10<1500,gfilter)
    signal = gand(ss,stock.above,stock.t5,t[VOLUME]>0,gf1,rhl10<1500,mdiff>=mdea,strend(stock.ref.ma4)>0)
    
    return signal

def gmacd(stock,ldown=30): #
    ''' g60 macd的同时试探ldown均线
        mxi: (-100,0], vfilter:>1.5
                2001.7-2008.12
                评估:总盈亏值=3070,交易次数=57  期望值=670
                总盈亏率(1/1000)=3070,平均盈亏率(1/1000)=53,盈利交易率(1/1000)=298
                赢利次数=17,赢利总值=6164
                亏损次数=39,亏损总值=3094
                平盘次数=1
                2008-2009.5
                评估:总盈亏值=1415,交易次数=8   期望值=1000
                总盈亏率(1/1000)=1415,平均盈亏率(1/1000)=176,盈利交易率(1/1000)=1000
                赢利次数=8,赢利总值=1415
                亏损次数=0,亏损总值=0

        mxi: (-100,0], vfilter:>1.33
                2001.7-2008.12
                评估:总盈亏值=6520,交易次数=26  期望值=41666
                总盈亏率(1/1000)=6520,平均盈亏率(1/1000)=250,盈利交易率(1/1000)=961
                赢利次数=25,赢利总值=6526
                亏损次数=1,亏损总值=6
                平盘次数=0
                2008-2009.5
                评估:总盈亏值=3926,交易次数=111 期望值=492
                总盈亏率(1/1000)=3926,平均盈亏率(1/1000)=35,盈利交易率(1/1000)=279
                赢利次数=31,赢利总值=9542
                亏损次数=79,亏损总值=5616
                平盘次数=1
            macd: 35,77
            评估:总盈亏值=5074,交易次数=91  期望值=763
                总盈亏率(1/1000)=5074,平均盈亏率(1/1000)=55,盈利交易率(1/1000)=296
                赢利次数=27,赢利总值=9624
                亏损次数=63,亏损总值=4550
                平盘次数=1
            36:78
            评估:总盈亏值=4841,交易次数=84  期望值=780
                总盈亏率(1/1000)=4841,平均盈亏率(1/1000)=57,盈利交易率(1/1000)=297
                赢利次数=25,赢利总值=9103
                亏损次数=58,亏损总值=4262
                平盘次数=1
        
            g60 ma3之后：
            评估:总盈亏值=5823,交易次数=97  期望值=845
                总盈亏率(1/1000)=5823,平均盈亏率(1/1000)=60,盈利交易率(1/1000)=329
                赢利次数=32,赢利总值=10401
                亏损次数=64,亏损总值=4578
                平盘次数=1

            评估:总盈亏值=6929,交易次数=31  期望值=5068 #20080601-20090602
                总盈亏率(1/1000)=6929,平均盈亏率(1/1000)=223,盈利交易率(1/1000)=903
                赢利次数=28,赢利总值=7063
                亏损次数=3,亏损总值=134
                平盘次数=0
                
                #之前是
                评估:总盈亏值=5997,交易次数=25  期望值=4596
                总盈亏率(1/1000)=5997,平均盈亏率(1/1000)=239,盈利交易率(1/1000)920
                赢利次数=23,赢利总值=6102
                亏损次数=2,亏损总值=105
            ma5:
                评估:总盈亏值=6850,交易次数=115 期望值=842
                总盈亏率(1/1000)=6850,平均盈亏率(1/1000)=59,盈利交易率(1/1000)=330
                赢利次数=38,赢利总值=12295
                亏损次数=77,亏损总值=5445
                平盘次数=0
            
                评估:总盈亏值=7564,交易次数=34  期望值=5045
                总盈亏率(1/1000)=7564,平均盈亏率(1/1000)=222,盈利交易率(1/1000)=911
                赢利次数=31,赢利总值=7698
                亏损次数=3,亏损总值=134
                平盘次数=0

        目前取1.33
        改成cmacd(svap,19,39)无改进                
    '''

    t = stock.transaction
    
    #mdiff,mdea = cmacd(stock.g5)   
    mdiff,mdea = cmacd(ma(stock.g60,5)) #平滑以去掉首尾效应


    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = gand(vma_s > vma_l * 4/3)
    
    xcross = cross(mdea,mdiff) > 0

    linelog(stock.code)

    ll10 = rollx(t[LOW],10)
    hh10 = tmax(t[HIGH],10)
    rhl10 = hh10 * 1000/ll10

    svap,v2i = stock.svap_ma_67
    sdiff,sdea = cmacd(svap,36,78)
    ssignal = gand(sdiff < sdea,strend(sdiff)<0,strend(sdiff-sdea)>0)

    msvap = transform(ssignal,v2i,len(t[VOLUME]))

    x2 = cross(ma(t[CLOSE],ldown),t[LOW]) < 0

    ss = sfollow(xcross,x2,10)
    
    gf1 = gand(stock.g20>5000,stock.g20<9500)

    si = score2(t[CLOSE],t[VOLUME])
    msi = msum(si,5)
    mxi = gand(msi>=-100,msi<=0)
    
    signal = gand(ss,stock.above,stock.t5,strend(stock.ma4)>0,t[VOLUME]>0,gf1,rhl10<1500,mdiff>=mdea,strend(stock.ref.ma4)>0,vfilter,msvap,mxi)
    
    return signal

def gmacd5(stock,ldown=30): #
    ''' g60 macd的同时试探ldown均线
                gf1 = gand(stock.g20>5000,stock.g20<9500)
                #使用g5,ma3
                评估:总盈亏值=5437,交易次数=19  期望值=71500
                    总盈亏率(1/1000)=5437,平均盈亏率(1/1000)=286,盈利交易率(1/1000)=947
                赢利次数=18,赢利总值=5441
                亏损次数=1,亏损总值=4

                评估:总盈亏值=6564,交易次数=68  期望值=1333 #20010701-20081231
                总盈亏率(1/1000)=6564,平均盈亏率(1/1000)=96,盈利交易率(1/1000)=397
                赢利次数=27,赢利总值=9476
                亏损次数=40,亏损总值=2912
                平盘次数=1

            ma5:
                评估:总盈亏值=5764,交易次数=23  期望值=10000
                总盈亏率(1/1000)=5764,平均盈亏率(1/1000)=250,盈利交易率(1/1000)=869
                赢利次数=20,赢利总值=5841
                亏损次数=3,亏损总值=77
                平盘次数=0
    
                评估:总盈亏值=6049,交易次数=84  期望值=888
                总盈亏率(1/1000)=6049,平均盈亏率(1/1000)=72,盈利交易率(1/1000)=357
                赢利次数=30,赢利总值=10372
                亏损次数=53,亏损总值=4323
                平盘次数=1
            直接计算:       #近期表现绝对彪悍
                评估:总盈亏值=3970,交易次数=14  期望值=1000
                总盈亏率(1/1000)=3970,平均盈亏率(1/1000)=283,盈利交易率(1/1000)=1000
                赢利次数=14,赢利总值=3970
                亏损次数=0,亏损总值=0
                平盘次数=0
                
            评估:总盈亏值=3132,交易次数=33  期望值=1146     #20010701-20081231
                总盈亏率(1/1000)=3132,平均盈亏率(1/1000)=94,盈利交易率(1/1000)=424
                赢利次数=14,赢利总值=4701
                亏损次数=19,亏损总值=1569
                平盘次数=0
            去掉msvap: 无此必要
                评估:总盈亏值=6936,交易次数=24  期望值=13136
                    总盈亏率(1/1000)=6936,平均盈亏率(1/1000)=289,盈利交易率(1/1000)=958
                    赢利次数=23,赢利总值=6958
                    亏损次数=1,亏损总值=22
                    平盘次数=0
                评估:总盈亏值=6766,交易次数=83  期望值=1125
                总盈亏率(1/1000)=6766,平均盈亏率(1/1000)=81,盈利交易率(1/1000)=373
                赢利次数=31,赢利总值=10560
                亏损次数=52,亏损总值=3794
                平盘次数=0
                
        目前取1.33
        改成cmacd(svap,19,39)无改进
    '''
    t = stock.transaction
    
    mdiff,mdea = cmacd(stock.g5)   

    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = gand(vma_s > vma_l * 4/3)
    
    xcross = cross(mdea,mdiff) > 0

    linelog(stock.code)

    ll10 = rollx(t[LOW],10)
    hh10 = tmax(t[HIGH],10)
    rhl10 = hh10 * 1000/ll10

    #above = gand(stock.ma2 > stock.ma3,stock.ma3>stock.ma4,stock.ma4>stock.ma5)


    svap,v2i = stock.svap_ma_67
    sdiff,sdea = cmacd(svap,36,78)
    ssignal = gand(sdiff < sdea,strend(sdiff)<0,strend(sdiff-sdea)>0)

    msvap = transform(ssignal,v2i,len(t[VOLUME]))

    x2 = cross(ma(t[CLOSE],ldown),t[LOW]) < 0

    ss = sfollow(xcross,x2,10)
    
    gf1 = gand(stock.g20>5000,stock.g20<9500)

    si = score2(t[CLOSE],t[VOLUME])
    msi = msum(si,5)
    mxi = gand(msi>=-100,msi<=0)
    
    signal = gand(ss,stock.above,stock.t5,strend(stock.ma4)>0,t[VOLUME]>0,gf1,rhl10<1500,mdiff>=mdea,strend(stock.ref.ma4)>0,vfilter,msvap,mxi)
    #signal = gand(ss,stock.above,stock.t5,strend(stock.ma4)>0,t[VOLUME]>0,gf1,rhl10<1500,mdiff>=mdea,strend(stock.ref.ma4)>0,vfilter,mxi)
    
    return signal


def smacd(stock):
    '''
        36,78
        评估:总盈亏值=45847,交易次数=379        期望值=1643
                总盈亏率(1/1000)=45847,平均盈亏率(1/1000)=120,盈利交易率(1/1000)=448
                赢利次数=170,赢利总值=61166
                亏损次数=209,亏损总值=15319
                平盘次数=0
    
        36,78,     vfilter = vma_s < vma_l 
        评估:总盈亏值=22086,交易次数=126        期望值=2302
                总盈亏率(1/1000)=22086,平均盈亏率(1/1000)=175,盈利交易率(1/1000)=539
                赢利次数=68,赢利总值=26550
                亏损次数=58,亏损总值=4464
                平盘次数=0
            #20080701-20090531:
            评估:总盈亏值=811,交易次数=63   期望值=214
                总盈亏率(1/1000)=811,平均盈亏率(1/1000)=12,盈利交易率(1/1000)=396
                赢利次数=25,赢利总值=2976
                亏损次数=38,亏损总值=2165
                平盘次数=0
            
        ####36,78,     vfilter = vma_s < vma_l * 7/8
        评估:总盈亏值=8997,交易次数=45  期望值=2618
                总盈亏率(1/1000)=8997,平均盈亏率(1/1000)=199,盈利交易率(1/1000)=511
                赢利次数=23,赢利总值=10690
                亏损次数=22,亏损总值=1693
                平盘次数=0
                闭合交易明细:
            #20080701-20090531:
                评估:总盈亏值=1067,交易次数=20  期望值=1060
                总盈亏率(1/1000)=1067,平均盈亏率(1/1000)=53,盈利交易率(1/1000)=600
                赢利次数=12,赢利总值=1470
                亏损次数=8,亏损总值=403
                平盘次数=0
    '''
    t = stock.transaction
    #g = gand(stock.g20 >= stock.g60+1000,stock.g60 >= stock.g120+1000,stock.g20>=3000,stock.g20<=8000)
    #g = np.ones_like(stock.g5)
 
    svap,v2i = stock.svap_ma_67 

    diff,dea = cmacd(svap,36,78)
    dcross = gand(cross(dea,diff)>0,strend(diff)>0,strend(dea)>0)

    msvap = transform(dcross,v2i,len(t[VOLUME]))

    linelog(stock.code)
    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = vma_s < vma_l * 7/8

    return gand(stock.golden,stock.above,msvap,vfilter)


def xru(stock):
    ''' 成交量分配后的上叉
    '''
    t = stock.transaction
    mxc = xc_ru2(t[OPEN],t[CLOSE],t[HIGH],t[LOW],t[VOLUME]) > 0
    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)
    vfilter = gand(svma>vma*1/2,svma<vma*2/3,t[CLOSE]>stock.ma1)
    signal = gand(mxc,vfilter,stock.thumb,stock.above,strend(stock.ma4)>0,stock.t5)
    linelog(stock.code)
    return signal

def xru0(stock):
    ''' 成交量分配后的上叉
    '''
    t = stock.transaction
    #mxc = xc_ru2(t[OPEN],t[CLOSE],t[HIGH],t[LOW],t[VOLUME]) > 0
    mxc1 = xc_ru0(t[OPEN],t[CLOSE],t[HIGH],t[LOW],t[VOLUME]) > 0
    #mxc2 = xc_ru02(t[OPEN],t[CLOSE],t[HIGH],t[LOW],t[VOLUME]) > 0
    mxc = mxc1
    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)
    cf = (t[OPEN]-t[LOW] + t[HIGH]-t[CLOSE])*1000 / (t[HIGH]-t[LOW])   #向下的动力  
    #cf = (t[CLOSE]-t[LOW] + t[HIGH]-t[OPEN])*1000 / (t[HIGH]-t[LOW])   #向上的动力，如果取反，完全等效
    mcf = ma(cf,5)
    vfilter = gand(svma>vma*1/2,svma<vma*2/3,t[CLOSE]>stock.ma1,strend(mcf)<0)
    #signal = gand(mxc,vfilter,stock.thumb,stock.above,strend(stock.ma4)>0,stock.t5)
    signal = gand(mxc,vfilter,stock.thumb,stock.above,stock.t5)
    linelog(stock.code)
    return signal

def mxru(stock):
    ''' 成交量分配后的macd
    '''
    t = stock.transaction
    mdiff,mdea = macd_ruv(t[OPEN],t[CLOSE],t[HIGH],t[LOW],t[VOLUME])
    mxc = cross(mdea,mdiff) > 0
    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)
    #vfilter = gand(svma>vma*1/3,svma<vma*7/8)
    vfilter = gand(svma<vma*7/8,svma>vma/2,t[VOLUME]<=vma,t[VOLUME]>vma*2/3,t[CLOSE]>stock.ma1) #cf无效果
    signal = gand(mxc,vfilter,stock.thumb,stock.above,strend(stock.ma4)>0,stock.t5)
    linelog(stock.code)
    return signal

def mxru3(stock):
    ''' 成交量分配后的macd,采用supdown3
    '''
    t = stock.transaction
    mdiff,mdea = macd_ruv3(t[OPEN],t[CLOSE],t[HIGH],t[LOW],t[VOLUME])
    mxc = cross(mdea,mdiff) > 0
    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)
    #cf = (t[CLOSE]-t[LOW])*1000 / (t[HIGH]-t[LOW]) < 900    #物极必反
    cf = (t[CLOSE]-t[LOW])*1000 / (t[HIGH]-t[LOW]) < 900    #物极必反, 如果是大阳线，不能收高
    vfilter = gand(svma<vma*7/8,svma>vma/2,t[VOLUME]<=vma,t[CLOSE]>stock.ma1,cf)
    signal = gand(mxc,vfilter,stock.thumb,stock.above,strend(stock.ma4)>0,stock.t5)
    linelog(stock.code)
    return signal


def ldx(stock,mlen=60,glimit=3000): #low down xcross 
    ''' 破60日线
                20010701--
                评估:总盈亏值=4858,交易次数=23  期望值=4137
                总盈亏率(1/1000)=4858,平均盈亏率(1/1000)=211,盈利交易率(1/1000)=652
                赢利次数=15,赢利总值=5269
                亏损次数=8,亏损总值=411
                平盘次数=0
                20080701-- 
                评估:总盈亏值=7552,交易次数=84  期望值=1618
                总盈亏率(1/1000)=7552,平均盈亏率(1/1000)=89,盈利交易率(1/1000)=833
                赢利次数=70,赢利总值=8276
                亏损次数=13,亏损总值=724

                将pdiff<pdea改成strend(pdiff-pdea)<0
                    评估:总盈亏值=4969,交易次数=21  期望值=4720
                    总盈亏率(1/1000)=4969,平均盈亏率(1/1000)=236,盈利交易率(1/1000)=714
                    赢利次数=15,赢利总值=5273
                    亏损次数=6,亏损总值=304
                    平盘次数=0
                
                    评估:总盈亏值=7169,交易次数=83  期望值=1653     #####
                    总盈亏率(1/1000)=7169,平均盈亏率(1/1000)=86,盈利交易率(1/1000)=819
                    赢利次数=68,赢利总值=7952
                    亏损次数=15,亏损总值=783
                    平盘次数=0
        

    #破30日线   
        gf1: <3333
            20080701--
            评估:总盈亏值=9474,交易次数=75  期望值=2739
                总盈亏率(1/1000)=9474,平均盈亏率(1/1000)=126,盈利交易率(1/1000)=826
                赢利次数=62,赢利总值=10026
                亏损次数=12,亏损总值=552
                平盘次数=1
                
            20010701--
            评估:总盈亏值=10510,交易次数=55 期望值=3410
                总盈亏率(1/1000)=10510,平均盈亏率(1/1000)=191,盈利交易率(1/1000)=672
                赢利次数=37,赢利总值=11529
                亏损次数=18,亏损总值=1019
                平盘次数=0
            
            将pdiff<pdea改成strend(pdiff-pdea)<0        ##说明对30日线破的情况不适用
            20080701-
            评估:总盈亏值=6452,交易次数=87  期望值=1720
                总盈亏率(1/1000)=6452,平均盈亏率(1/1000)=74,盈利交易率(1/1000)=643
                赢利次数=56,赢利总值=7750
                亏损次数=30,亏损总值=1298
                平盘次数=1
            
            评估:总盈亏值=11927,交易次数=57 期望值=3732
                总盈亏率(1/1000)=11927,平均盈亏率(1/1000)=209,盈利交易率(1/1000)=684
                赢利次数=39,赢利总值=12936
                亏损次数=18,亏损总值=1009
                平盘次数=0


        #120: glimit=3333   
        20010701-20081231
        评估:总盈亏值=811,交易次数=12   期望值=1456
                总盈亏率(1/1000)=811,平均盈亏率(1/1000)=67,盈利交易率(1/1000)=666
                赢利次数=8,赢利总值=995
                亏损次数=4,亏损总值=184
                平盘次数=0
        20080701-20090605
        评估:总盈亏值=1025,交易次数=5   期望值=1198
                总盈亏率(1/1000)=1025,平均盈亏率(1/1000)=205,盈利交易率(1/1000)=800
                赢利次数=4,赢利总值=1196
                亏损次数=1,亏损总值=171
                平盘次数=0
        

    '''

    t = stock.transaction
    
    vma_l = ma(t[VOLUME],30)
    vma_5 = ma(t[VOLUME],5)

    vfilter = gand(vma_5>vma_l*3/5,t[VOLUME] < vma_l*2/3)   

    linelog(stock.code)

    #c = t[LOW]
    #ma30 = ma(c,30)
    #above = gand(ma(c,13) > ma30,ma30>stock.ma4,stock.ma4>stock.ma5)
    
    ma_s = ma(t[CLOSE],mlen)
    x2 = gand(cross(ma_s,t[LOW])< 0,t[CLOSE]>ma_s)

    gf1 = gand(stock.g60<glimit)

    pdiff,pdea = stock.ref.pdiff,stock.ref.pdea

    si = score2(t[CLOSE],t[VOLUME])
    msi = msum(si,5)
    mxi = gand(msi>=-100,msi<=0)
    
    signal = gand(x2,stock.above,stock.t5,strend(stock.ma4)>0,t[VOLUME]>0,gf1,strend(pdiff-pdea)<0,vfilter,mxi)

    return signal


def ldx2(stock,mlen=30,glimit=3333): #low down xcross
    ''' 30日线，使用pdiff<pdea条件
    '''

    t = stock.transaction
    
    vma_l = ma(t[VOLUME],30)
    vma_5 = ma(t[VOLUME],5)

    vfilter = gand(vma_5>vma_l*3/5,t[VOLUME] < vma_l*2/3)   

    linelog(stock.code)

    #c = t[LOW]
    #ma30 = ma(c,30)
    #above = gand(ma(c,13) > ma30,ma30>stock.ma4,stock.ma4>stock.ma5)
    
    ma_s = ma(t[CLOSE],mlen)
    x2 = gand(cross(ma_s,t[LOW])< 0,t[CLOSE]>ma_s)

    gf1 = gand(stock.g60<glimit)

    pdiff,pdea = stock.ref.pdiff,stock.ref.pdea

    si = score2(t[CLOSE],t[VOLUME])
    msi = msum(si,5)
    mxi = gand(msi>=-100,msi<=0)
    
    signal = gand(x2,stock.above,stock.t5,strend(stock.ma4)>0,t[VOLUME]>0,gf1,pdiff<pdea,vfilter,mxi)

    return signal

