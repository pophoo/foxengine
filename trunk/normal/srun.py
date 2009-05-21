# -*- coding: utf-8 -*-

#指定股票的测试运行脚本

#106493077@sis
#catknight_by_MiMiP2P@18p2p@SIS@Touch99
from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *
from wolfox.fengine.normal.nrun import prepare_order,prepare_common
from wolfox.fengine.core.d1ex import tmax,derepeatc,derepeatc_v,equals,msum,tmin,extend,extend2next
from wolfox.fengine.core.d1match import *
from wolfox.fengine.core.d1 import lesser
from wolfox.fengine.core.d1indicator import cmacd,score2
from wolfox.fengine.core.d1idiom import down_period
from wolfox.fengine.core.d2 import increase,extract_collect
from wolfox.foxit.base.tutils import linelog
from time import time

import logging
logger = logging.getLogger('wolfox.fengine.normal.run')    

def check(stock,dates,tail=30):
    f = open('check.txt','a+')
    f.write('\n#############################')
    f.write(stock.code)
    f.write('#############################\n')    
    for d,g20,g60,g120 in zip(dates,stock.g20,stock.g60,stock.g120)[-tail:]:
        print >>f,d,g20,g60,g120
    f.close()

def check2(sdata,sname,dates,tail=30):
    stock = sdata[code2id[sname]]
    f = open('check.txt','a+')
    f.write('\n#############################')
    f.write(stock.code)
    f.write('#############################\n')    
    for d,g5,g20,g60,g120,g250 in zip(dates,stock.g5,stock.g20,stock.g60,stock.g120,stock.g250)[-tail:]:
        print >>f,d,g5,g20,g60,g120,g250
    f.close()

sbuyer = fcustom(svama3,fast=185,mid=260,slow=1800)
def swrap(stock,dates):
    linelog(stock.code)
    sbuy = sbuyer(stock)
    return sbuy
    #g = gand(stock.g20>=3000,stock.g20<=8000)    
    #return gand(g,sbuy)

def attack(stock,dates):
    linelog(stock.code)
    t = stock.transaction
    o,c,h,l = t[OPEN],t[CLOSE],t[HIGH],t[LOW]
    ldown = lesser(l,rollx(l))
    ldown2 = equals(ldown + rollx(ldown),2)
    hdown = lesser(h,rollx(h))
    hdown2 = equals(hdown + rollx(hdown),2)
    cl = lesser(c,rollx(l))   #收盘小于昨天最低
    sprepare = gand(ldown2,hdown2,cl)
    ch = greater(c,rollx(h))  #收盘大于昨天最高
    signal = band(rollx(sprepare),ch) #连续两天下跌之后，第三天收盘超过昨日最高
    sbuy = gand(signal,stock.golden,stock.above,stock.t120)
    return sbuy

def macd3(stock,dates):
    linelog(stock.code)
    t = stock.transaction
    pdiff,pdea = cmacd(t[CLOSE])
    ds = strend(pdea) - 3
    base = cached_zeros(len(t[CLOSE]))
    x = greater(cross(base,ds))
    signal = gand(x,stock.thumb,stock.silver,stock.above,stock.t120)
    return signal

def spring(stock,dates):
    threshold = -30
    t = stock.transaction
    linelog('spring:%s' % stock.code)
    
    s11 = gand(stock.ks >=-5,stock.ks<0,stock.ref.ks<=threshold)
    s12 = gand(stock.ks >=5,stock.ks<20,stock.ref.ks<=threshold)
    s1 = bor(s11,s12)
    s_tt = gand(s1,stock.thumb,stock.t120)
    s21 = gand(stock.ks>=5,stock.ks<75,stock.ref.ks<=threshold)
    s_aa = gand(s21,stock.thumb,stock.above)

    signals = bor(s_aa,s_tt)

    ref = stock.ref
    sbuy = signals #gand(signals,greater(ref.ma10,ref.ma20),greater(ref.ma20,ref.ma60))

    return sbuy

def spring2(stock,dates):
    ''' 
        大盘跌幅从最高点开始度量
        t=idata[1].transaction
        rc = rollx(t[CLOSE])
        lhigh = np.select([rc>t[HIGH],rc<=t[HIGH]],[rc,t[HIGH]])
        ks = (t[CLOSE]-lhigh) * BASE / lhigh
        idata[1].ks2 = ks
        效果不如spring
    '''
    threshold=-30
    t = stock.transaction
    linelog('spring:%s' % stock.code)
    
    s11 = gand(stock.ks >=-5,stock.ks<0,stock.ref.ks2<=threshold)
    s12 = gand(stock.ks >=5,stock.ks<20,stock.ref.ks2<=threshold)
    s1 = bor(s11,s12)
    s_tt = gand(s1,stock.thumb,stock.t120)
    s21 = gand(stock.ks>=5,stock.ks<75,stock.ref.ks2<=threshold)
    s_aa = gand(s21,stock.thumb,stock.above)

    signals = bor(s_aa,s_tt)

    ref = stock.ref
    sbuy = gand(signals,greater(ref.ma10,ref.ma20),greater(ref.ma20,ref.ma60))

    return sbuy


def ctest(stock,dates):
    fast,mid,slow,rstart,rend = 33,5,40,2000,4500
    ma_standard=500
    extend_days=10
    sma=55
    linelog('ctest:%s' % stock.code)
    t = stock.transaction

    if rstart >= rend:
        return np.zeros_like(t[CLOSE])

    try:
        stock.catalog
    except:
        return np.zeros_like(t[CLOSE])

    c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s>=rstart,s<=rend)

    #print stock.code,len(t[CLOSE]),sum(t[CLOSE])
    skey = 'svap_ma_%s' % sma
    if not stock.has_attr(skey): #加速
        stock.set_attr(skey,svap_ma(t[VOLUME],t[CLOSE],sma))
    svap,v2i = stock.get_attr(skey)
    
    ma_svapfast = ma(svap,fast)
    ma_svapmid = ma(svap,mid)    
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapmid = strend(ma_svapmid) > 0    
    trend_ma_svapslow = strend(ma_svapslow) > 0
    
    #ma_standard = ma(svap,ma_standard)
    #trend_ma_standard = strend(ma_standard) > 0    
    mskey = 'svap_ma_%s_%s' % (sma,ma_standard)
    if not stock.has_attr(mskey):
        ma_standard = ma(svap,ma_standard)
        trend_ma_standard = strend(ma_standard) > 0    
        stock.set_attr(mskey,trend_ma_standard)
    trend_ma_standard = stock.get_attr(mskey)

    #cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    cross_fast_mid = band(cross(ma_svapmid,ma_svapfast)>0,trend_ma_svapfast)
    cross_fast_slow = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast)    
    cross_mid_slow = band(cross(ma_svapslow,ma_svapmid)>0,trend_ma_svapmid)
    sync_fast_2 = sfollow(cross_fast_mid,cross_fast_slow,extend_days)
    sync3 = sfollow(sync_fast_2,cross_mid_slow,extend_days)
    vsignal = band(sync3,trend_ma_standard)
    msvap = transform(vsignal,v2i,len(t[VOLUME]))

    cs = catalog_signal_cs(stock.c60,c_extractor)
    g = gand(stock.g20 >= stock.g60+1000,stock.g60 >= stock.g120+1000,stock.g20-stock.g60>=stock.g60-stock.g120,stock.g20>=3000,stock.g20<=8000)

    if not stock.has_attr('ma'):
        ma10 = ma(t[CLOSE],10)
        ma20 = ma(t[CLOSE],20)
        ma60 = ma(t[CLOSE],60)
        ma120 = ma(t[CLOSE],120)
        t120 = strend(ma120)>0
        ma_above = gand(greater(ma10,ma20),greater(ma20,ma60),greater(ma60,ma120))        
        stock.set_attr('ma',{'10':ma10,'20':ma20,'60':ma60,'120':ma120,'t120':t120,'above':ma_above})
    t120,ma_above = stock.ma['t120'],stock.ma['above']
    
    return gand(cs,g,msvap,ma_above)


#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s>=3300,s<=6600)

#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=6600)

#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,s<=6600)

#c_extractor = lambda c,s:gand(c.g5 >= c.g20+500,c.g20>=c.g60+500,c.g60>=c.g120+500,c.g120>=c.g250+500)

def svap_macd(stock,dates,gfilter):
    t = stock.transaction
    g = gand(stock.g20 >= stock.g60+1000,stock.g60 >= stock.g120+1000,stock.g20>=3000,stock.g20<=8000)
    #g = np.ones_like(stock.g5)
    
    skey = 'svap_ma_%s' % 65
    if not stock.has_attr(skey): #加速
        stock.set_attr(skey,svap_ma(t[VOLUME],t[CLOSE],65))
    svap,v2i = stock.get_attr(skey) 

    diff,dea = cmacd(svap,50,120)
    dcross = gand(cross(dea,diff)>0,strend(diff)>0,strend(dea)>0)

    msvap = transform(dcross,v2i,len(t[VOLUME]))

    if not stock.has_attr('ma'):
        ma10 = ma(t[CLOSE],10)
        ma20 = ma(t[CLOSE],20)
        ma60 = ma(t[CLOSE],60)
        ma120 = ma(t[CLOSE],120)
        t120 = strend(ma120)>0
        ma_above = gand(greater(ma10,ma20),greater(ma20,ma60),greater(ma60,ma120))        
        stock.set_attr('ma',{'10':ma10,'20':ma20,'60':ma60,'120':ma120,'t120':t120,'above':ma_above})
    t120,ma_above = stock.ma['t120'],stock.ma['above']
    ma10,ma20,ma60,ma120 = stock.ma['10'],stock.ma['20'],stock.ma['60'],stock.ma['120']

    linelog(stock.code)

    return gand(g,ma_above,msvap,gfilter)


#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=6600)
def tsvama2(stock,dates):
    ''' svama两线交叉
    '''
    fast=20
    slow=100
    t = stock.transaction
    
    #g = gand(stock.g20 >= stock.g60+1000,stock.g60 >= stock.g120+1000,stock.g20>=3000,stock.g20<=8000)

    g = stock.golden

    svap,v2i = stock.svap_ma_67

    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))

    
    linelog('%s:%s' % (tsvama2.__name__,stock.code))
    return gand(g,msvap,stock.above)

def gcs(stock,dates):
    t = stock.transaction
    linelog(stock.code)
    s = stock
    #g = gand(s.g20 >= s.g120+2000,s.g120 >= s.g60,s.g20>=3000,s.g20<=8000)
    #g = gand(s.g20 >= s.g60+1000,s.g60 >= s.g120+1000,s.g120 >= s.g250,s.g120>=1000,s.g20<=2*s.g60,s.g60<=2*s.g120,s.g20>=3000,s.g20<=8000)
    #g = gand(s.g20 >= s.g60,s.g20 <= s.g60+500,s.g60 >= s.g120,s.g60>=s.g120+500,s.g120>=s.g250+500,s.g250>=1000,s.g20<=8000)
    #silver2 = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250)    
    #cs = catalog_signal_cs(stock.c60,stock.silver)
    #ks = np.abs((s.g20-s.g60) * 1000/(s.g60-s.g120))
    g = gand(s.g20 >= s.g60,s.g60 >= s.g120,s.g20>=3000,s.g20<=8000,s.g20<=s.g120+1000) 

    pdiff,pdea = cmacd(t[CLOSE])

    #ma5=ma(t[CLOSE],5)
    #signals = gand(stock.golden,stock.silver,stock.above,ma5>stock.ma10,stock.ref.t120)
    #signals = gand(g,stock.silver,stock.above,ma5>stock.ma10,stock.ref.t120)
    #signals = gand(g,stock.above,stock.ref.t120)
    #signals = gand(stock.golden,stock.ref.t120,strend(stock.ref.ma60)>0,strend(stock.ref.ma20)>0,strend(ma(stock.ref.transaction[CLOSE],250))>0)
    #signals = gand(g,stock.ref.t120,strend(stock.ref.ma60)>0,strend(stock.ref.ma20)>0,strend(ma(stock.ref.transaction[CLOSE],250))>0)
    signals = gand(g,pdiff>=300,pdiff<=600,stock.above,stock.ref.t120,strend(stock.ma20)>0,strend(stock.ma60)>0,stock.t120,stock.ref.above)

    #signals = gand(stock.golden,cs,stock.t120)
    #signals = gand(g,stock.above)
    #sbuy = derepeatc(signals)
    sbuy = signals
    gcs.sum += np.sum(sbuy)
    gcs.total += np.sum(t[VOLUME]>0)
    return sbuy

gcs.sum=0
gcs.total = 0


def xgcs(stock,dates):
    '''
    '''
    t = stock.transaction
    ma5 = ma(t[CLOSE],5)
    linelog(stock.code)

    si = score2(t[CLOSE],t[VOLUME])
    mxi = gand(msum(si,5)>=-100,msum(si,5)<=0)

    sbuy = gand(stock.golden,stock.silver,stock.above,ma5>stock.ma10,stock.ref.t120,mxi)
    return sbuy


def xgcsx(stock,dates):
    '''
    '''
    t = stock.transaction
    ma5 = ma(t[CLOSE],5)
    linelog(stock.code)

    si = score2(t[CLOSE],t[VOLUME])
    mxi = gand(msum(si,5)>=-100,msum(si,5)<=0)

    signal = gand(stock.golden,stock.silver,stock.above,ma5>stock.ma10,stock.ref.t120,mxi)

    sbuy = sfollow(signal,x30(t),10)
    
    return sbuy


def xgcs0(stock,dates):
    ''' 下穿0线
        评估:总盈亏值=23464,交易次数=81 期望值=4013
                总盈亏率(1/1000)=23464,平均盈亏率(1/1000)=289,盈利交易率(1/1000)=617
                赢利次数=50,赢利总值=25703
                亏损次数=31,亏损总值=2239
                平盘次数=0
    '''
    t = stock.transaction
    ma5 = ma(t[CLOSE],5)
    linelog(stock.code)

    si = score2(t[CLOSE],t[VOLUME])
    #mxi = gand(msum(si,5)>=-100,msum(si,5)<=0)
    z1 = np.ones_like(t[CLOSE])
    z1 = z1-3
    mxi = cross(z1,si)<0

    sbuy = gand(stock.golden,stock.silver,stock.above,ma5>stock.ma10,stock.ref.t120,mxi)
    return sbuy

def xgcs0x(stock,dates):
    ''' 下穿0线
        评估:总盈亏值=23464,交易次数=81 期望值=4013
                总盈亏率(1/1000)=23464,平均盈亏率(1/1000)=289,盈利交易率(1/1000)=617
                赢利次数=50,赢利总值=25703
                亏损次数=31,亏损总值=2239
                平盘次数=0
    '''
    t = stock.transaction
    ma5 = ma(t[CLOSE],5)
    linelog(stock.code)

    si = score2(t[CLOSE],t[VOLUME])
    zs = cached_zeros(len(t[CLOSE]))
    mxi = cross(zs,si)<0

    signal = gand(stock.golden,stock.silver,stock.above,ma5>stock.ma10,stock.ref.t120,mxi)
    
    #sbuy = signal
    sbuy= gand(sfollow(signal,x30(t),5),stock.above)
    return sbuy


def xgcs5(stock,dates):
    '''
    
    '''
    t = stock.transaction
    ma5 = ma(t[CLOSE],5)
    linelog(stock.code)

    si = score2(t[CLOSE],t[VOLUME])
    zs = cached_zeros(len(t[CLOSE]))
    mxi = cross(zs,si)<0
    
    s = stock
    g = gand(s.g20 >= s.g60,s.g20 <= s.g60+500,s.g60 >= s.g120,s.g60<=s.g120+500,s.g120>=s.g250+500,s.g250>=1000,s.g20<=8000)

    #sbuy = gand(stock.golden,stock.silver,stock.above,ma5>stock.ma10,stock.ref.t120,mxi)
    #sbuy = gand(g,stock.above,stock.ref.t120,mxi)
    signals = gand(g,mxi,stock.ref.above,stock.ref.t120,strend(stock.ref.ma60)>0,strend(stock.ref.ma10)>0,strend(stock.ref.ma20)>0,strend(ma(stock.ref.transaction[CLOSE],250))>0)
    
    sbuy = signals
    return sbuy


def pmacd(stock,dates):
    t = stock.transaction
    pdiff,pdea = cmacd(t[VOLUME])
    dcross = gand(cross(pdea,pdiff),strend(pdiff)>0,strend(pdea>0))
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    linelog(stock.code)
    
    if not stock.has_attr('ma'):
        ma10 = ma(t[CLOSE],10)
        ma20 = ma(t[CLOSE],20)
        ma60 = ma(t[CLOSE],60)
        ma120 = ma(t[CLOSE],120)
        t120 = strend(ma120)>0
        ma_above = gand(greater(ma10,ma20),greater(ma20,ma60),greater(ma60,ma120))        
        stock.set_attr('ma',{'10':ma10,'20':ma20,'60':ma60,'120':ma120,'t120':t120,'above':ma_above})
    t120,ma_above = stock.ma['t120'],stock.ma['above']
    ma20,ma60,ma120 = stock.ma['20'],stock.ma['60'],stock.ma['120']
    
    cs = catalog_signal_cs(stock.c60,c_extractor)

    #return dcross
    #return gand(dcross,g,trend_ma_standard)
    return gand(dcross,g,ma_above,cs,pdea>0,pdea<12000)


def nhigh(stock,dates):#60高点
    linelog(stock.code)
    t = stock.transaction
    mline = rollx(tmax(t[CLOSE],60)) #以昨日的60高点为准
    dcross = cross(mline,t[CLOSE])>0    
    g = gand(stock.g5>=stock.g20,stock.thumb)
    #linelog(stock.code)
    return gand(g,stock.silver,dcross,strend(stock.ma60)>0,stock.above,stock.t120)

def shigh(stock,dates):
    linelog(stock.code)
    t = stock.transaction
    #mline = rollx(tmax(t[HIGH],60)) #以昨日的60高点为准
    #nh = greater(t[HIGH],mline)
    mline = rollx(tmax(t[HIGH],67)) #以昨日的60高点为准
    nh = greater(t[HIGH],mline)
    stock.shigh = nh
    #stock.v = greater(t[VOLUME])

def slow(stock,dates):
    linelog(stock.code)
    t = stock.transaction
    #mline = rollx(tmax(t[HIGH],60)) #以昨日的60高点为准
    #nh = greater(t[HIGH],mline)
    mline = rollx(tmin(t[LOW],67)) #以昨日的60高点为准
    nl = lesser(t[LOW],mline)
    stock.slow = nl
    #stock.v = greater(t[VOLUME])

def ma3(stock,dates):
    ''' ma三线金叉
        不要求最慢的那条线在被快线交叉时趋势必须向上，但要求被中线交叉时趋势向上
    '''
    ma_standard=120
    extend_days = 10    
    #logger.debug('ma3 calc: %s ' % stock.code)    
    t = stock.transaction
    #g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    #g对这个没效果
    fast,mid,slow=5,10,20
    ma_fast = ma(t[CLOSE],fast)
    ma_mid = ma(t[CLOSE],mid)
    ma_slow = ma(t[CLOSE],slow)
    trend_fast = strend(ma_fast) > 0
    trend_mid = strend(ma_mid) > 0    
    trend_slow = strend(ma_slow) > 0
    cross_fast_mid = band(cross(ma_mid,ma_fast)>0,trend_mid)
    cross_fast_slow = band(cross(ma_slow,ma_fast)>0,trend_fast)
    cross_mid_slow = band(cross(ma_slow,ma_mid)>0,trend_mid)
    cross_fm_fs = sfollow(cross_fast_mid,cross_fast_slow,extend_days)
    confirm_cross = sfollow(cross_fm_fs,cross_mid_slow,extend_days)
    trend_ma_standard = strend(ma(t[CLOSE],ma_standard)) > 0
    linelog(stock.code)
    #cs = catalog_signal_cs(stock.c60,c_extractor)
    
    return gand(trend_ma_standard,confirm_cross)

#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=6600)
def xma60(stock,dates):

    t = stock.transaction
    water_line = stock.ma60*115/100   #上方15处
    dcross = cross(water_line,t[LOW])
    up_cross = dcross > 0
    down_cross = dcross < 0
    sync = sfollow(down_cross,up_cross,7)
    linelog(stock.code)
    s = stock
    #return gand(sync,stock.above,stock.t120,stock.golden,cs)    
    return gand(sync,stock.above,stock.t120,stock.thumb,stock.silver)


def x30(t):
    water_line = ma(t[CLOSE],30)
    dcross = cross(water_line,t[LOW])
    up_cross = dcross > 0
    down_cross = dcross < 0
    sync = sfollow(down_cross,up_cross,7)
    return sync


def tsvama2x(stock,dates):
    ''' svama两线交叉
    '''
    fast=20
    slow=100
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

def xma30(stock,dates):
    t = stock.transaction
    water_line = ma(t[CLOSE],30)
    dcross = cross(water_line,t[LOW])
    up_cross = dcross > 0
    down_cross = dcross < 0
    sync = sfollow(down_cross,up_cross,10)
    linelog(stock.code)
    s = stock
    #return gand(sync,stock.above,stock.t120,stock.golden,cs)    
    g = gand(s.g20 >= s.g60,s.g20 <= s.g60+500,s.g60 >= s.g120,s.g60<=s.g120+500,s.g120>=s.g250+500,s.g250>=1000,s.g20<=8000)

    return gand(sync,stock.above,stock.t120,g)


def cma2(stock,dates):  #传统的ma2
    t = stock.transaction
    #water_line = stock.ma20  #上方15处,这个位置起始有点远，但居然起作用
    water_line = ma(t[CLOSE],20)
    dcross = cross(water_line,ma(t[CLOSE],5))

    up_cross = dcross > 0
    down_cross = dcross < 0

    sync = up_cross
    linelog(stock.code)
    return gand(sync,stock.above,stock.t120,stock.g5>=stock.g20+500,stock.g20>=stock.g60+500,stock.g60>=stock.g120,stock.g5>4000,stock.g5<8000)


def cma_30(stock,dates):  #
    t = stock.transaction
    
    water_line = ma(t[CLOSE],30)
    dcross = cross(water_line,t[LOW])
    up_cross = dcross > 0
    down_cross = dcross < 0
    sync = sfollow(down_cross,up_cross,7)
    return gand(sync,stock.above,stock.t120,stock.thumb,stock.silver)


def cma2x(stock,dates):  #传统的ma2
    t = stock.transaction
    water_line = ma(t[CLOSE],20)
    dcross = cross(water_line,ma(t[CLOSE],5))

    up_cross = dcross > 0
    down_cross = dcross < 0

    sync = up_cross
    linelog(stock.code)

    s=stock
    g = gand(s.g20 >= s.g60,s.g20 <= s.g60+500,s.g60 >= s.g120,s.g60<=s.g120+500,s.g120>=s.g250+500,s.g250>=1000,s.g20<=8000)

    return gand(sync,g,stock.g5>=stock.g20+500,stock.above,stock.t120)


def wvad(stock,dates):
    t = stock.transaction
    
    vad = (t[CLOSE]-t[OPEN])*t[VOLUME]/(t[HIGH]-t[LOW]) / 10000
    svad = msum2(vad,24)
    ma_svad = ma(svad,6)

    ecross = gand(stock.thumb,stock.silver,cross(ma_svad,vad)>0,strend(ma_svad)>0,stock.t120,stock.above)
    linelog(stock.code)
    sbuy = sfollow(ecross,x30(t),10)

    return sbuy


import wolfox.fengine.core.d1indicator as d1in
#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=6600)
def temv(stock,dates):
    t = stock.transaction
    ts = cached_zeros(len(t[CLOSE]))
    ekey = 'emv'
    em = d1in.emv(t[HIGH],t[LOW],t[VOLUME])
    mv = msum2(em,14)
    ssemv = ma(mv,9)
    ecross = gand(stock.golden,cross(ts,mv)>0,strend(ssemv)>0,stock.t120,stock.above)
    sbuy = ecross   #sfollow(ecross,x30(t),10)
    linelog(stock.code)
    return sbuy

def vmacd_ma4(stock,dates):
    t = stock.transaction
    
    vdiff,vdea = cmacd(t[VOLUME])
    dcross = gand(cross(vdea,vdiff)>0,strend(vdiff)>0,strend(vdea)>0)

    #g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    g = gand(stock.g20>=7500,stock.g60>=7500)

    c_ex = lambda c,s:gand(c.g20>=7500,s>=8000)
    cs = catalog_signal_cs(stock.c60,c_ex)    
    return gand(g,cs,dcross,stock.above,strend(stock.ma60)>0,vdea>=0,vdea<=12000)

def gcx(stock,dates):
    t = stock.transaction
    
    #g = gand(stock.g60>=8000)
    gma = ma(stock.g60,5)
    waterline = cached_ints(len(t[CLOSE]),6000)
    xs = cross(waterline,gma) 
    #xs = extend2next(xs)

    ll5 = rollx(t[LOW],3)
    hinc = t[HIGH] * 1000 / ll5

    #c_ex = lambda c,s:gand(c.g20>=7500,s>=8000)
    #cs = catalog_signal_cs(stock.c60,c_ex)    
    cx = stock.c60.keys()[1].g60
    cma = ma(cx,3)
    xc = cma > 6000
    xc = extend2next(xc) > 0
    #signal = derepeatc(gand(xs>0,xc>0))
    #print signal
    return gand(xs>0,xc>0,stock.c60.values()[1]>8500,stock.above,stock.t120,hinc<1200)

def gmacd_old(stock,dates): #这里dea,diff是全反的,但是全反居然收益很好，成功率不错。晕倒
    t = stock.transaction
    
    mdea,mdiff = cmacd(stock.g60)
    ldea,ldiff = cmacd(stock.g120)
    lldea,lldiff = cmacd(stock.g250)

    vdea,vdiff = cmacd(t[VOLUME])
    pdea,pdiff = cmacd(t[CLOSE])

    sfilter = gand(vdiff>vdea,pdiff>pdea)

    xcross = cross(mdea,mdiff) > 0

    linelog(stock.code)

    ll5 = rollx(t[LOW],5)
    hinc = t[HIGH] * 1000 / ll5

    ll10 = rollx(t[LOW],10)
    hh10 = tmax(t[HIGH],10)
    rhl10 = hh10 * 1000/ll10

    ss = sfollow(xcross,sfilter,5)

    signal = gand(ss,stock.above,stock.t120,t[VOLUME]>0,hinc<1200,rhl10<1500,stock.g60>4500)
    return signal
    #410/498/1584
    #全部750/520
    #需要测试中国软件/浪潮软件/000961
    #return gand(xcross,stock.above,stock.t120,t[VOLUME]>0,stock.g60>4500,stock.g60<7500)   #94-392


def gmacd(stock,dates): #
    ''' ss1=sfollow(cross(mdea,mdiff) > 0,vdiff<vdea), 然后再sfollow(ss1,cross(ma(t[CLOSE],30),t[LOW]),5),2115/704/846
        ss1=sfollow(cross(mdea,mdiff) > 0,vdiff<vdea), 然后再sfollow(ss1,cross(ma(t[CLOSE],30)<0,t[LOW]),5),2213/759/595
            4500-8500:  2946/821/286
        ss1=sfollow(cross(mdea,mdiff) > 0,vdiff<vdea), 然后再sfollow(ss1,cross(ma(t[CLOSE],30)<0,t[LOW]),10),2392/746/844    
            0-3000:1457/670/273
            3000-6000: 2709/788/402
            6000-!: 2696/758/273
            6000-8500: 2781/775/232
            >8500:  2193/632/49
            4500-8500:  3078/793/411
            4500-7500:  2888/797/345
            5000-8000:  2925/796/324
            数量太多,需要进一步筛选
        仍然无法继续甄别超级强势股,如600756,000961的启动阶段,能够通过cmacd(mdea,mdiff)>0找到初始信号,但无法从噪声中甄别出来
        因为他们不触碰30线,需要进一步考虑
        ss1不变.
        x3 = gand(strend(ma(t[CLOSE],5))>0,strend(stock.ma10)>0,strend(stock.ma20)>0,strend(stock.ma60)>0)
        ss = sfollow(ss1,x3,10)
        
    '''
    t = stock.transaction
    
    mdiff,mdea = cmacd(stock.g60)
    ldiff,ldea = cmacd(stock.g120)
    lldiff,lldea = cmacd(stock.g250)

    vdiff,vdea = cmacd(t[VOLUME])
    pdiff,pdea = cmacd(t[CLOSE])


    sfilter = vdiff<vdea
    #sfilter = vdiff<vdea
    #sfilter = gand(vdiff>vdea,pdiff>pdea)

    xcross = cross(mdea,mdiff) > 0  
    #xcross = cross(mdiff,mdea) > 0  

    linelog(stock.code)

    ll5 = rollx(t[LOW],5)
    hinc = t[HIGH] * 1000 / ll5

    ll10 = rollx(t[LOW],10)
    hh10 = tmax(t[HIGH],10)
    rhl10 = hh10 * 1000/ll10

    ss1 = sfollow(xcross,sfilter,5)
    #ss = derepeatc(ss)
    
    x2 = cross(ma(t[CLOSE],30),t[LOW]) < 0

    ss = sfollow(ss1,x2,10)

    signal = gand(ss,stock.above,stock.t120,t[VOLUME]>0,hinc<1200,rhl10<1500,stock.g60>4500,stock.g60<8500)
    
    #1151/638/886
    return signal


#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250)
#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s>=3300,s<=6600)
def ma4(stock,dates):
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    
    ma5 = ma(t[CLOSE],5)
    ma10 = stock.ma10
    ma20 = stock.ma20
    ma60 = stock.ma60
    ma120 = stock.ma120
    dcross = gand(cross(ma10,ma5),strend(ma5)>0,strend(ma10)>0,strend(ma20)>0,strend(ma60)>0,strend(ma120)>0)
    #dcross = gand(cross(ma10,ma5),strend(ma5)>0,strend(ma10)>0,strend(ma20)>0,strend(ma60)>0)
    #dabove = gand(greater(ma10,ma20),greater(ma20,ma60))
    cs = catalog_signal_cs(stock.c60,stock.silver)
    linelog(stock.code)
    return gand(g,cs,dcross,stock.above)

#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s>=3300,s<=6600)
#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250)
#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=3300)
def vmacd(stock,dates):
    t = stock.transaction
    vdiff,vdea = cmacd(t[VOLUME])
    dcross = gand(cross(vdea,vdiff),strend(vdiff)>0,strend(vdea>0))
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    linelog(stock.code)
    
    trend_ma_standard = strend(ma(t[CLOSE],120)) > 0    
    cs = catalog_signal_cs(stock.c60,c_extractor)

    #return dcross
    #return gand(dcross,g,trend_ma_standard)
    return gand(dcross,g,trend_ma_standard,cs,vdea>0,vdea<12000)


def dma(stock,dates):
    t = stock.transaction
    dif = ma(t[CLOSE],10) - ma(t[CLOSE],67)
    mas = ma(dif,22)
    dcross = gand(cross(mas,dif)>0,strend(dif)>0)
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    linelog(stock.code)
    
    ma_standard = ma(t[CLOSE],60)
    trend_ma_standard = strend(ma_standard) > 0    

    return gand(dcross,g,ma_standard)


#configs.append(config(buyer=fcustom(svama3,fast=165,mid=184,slow=1950))) 	#                   #577-63-619-42
def psvama3(stock,fast,mid,slow,dates):
    t = stock.transaction
    sbuy = svama3(stock,fast,mid,slow)

    #trend_psy = strend(ma(psy(t[CLOSE]),6)) > 0
    mpsy = ma(psy(t[CLOSE],12),6)
    #spsy = psy(t[CLOSE])
    state_psy =  mpsy>500

    logger.debug(stock.code)
    linelog(stock.code)
    return gand(sbuy,state_psy)

def psvama2(stock,fast,slow,dates,ma_standard=500,sma=65):
    ''' svama两线交叉
    '''
    t = stock.transaction
    sbuy = svama2(stock,fast,slow)

    #trend_psy = strend(ma(psy(t[CLOSE]),6)) > 0
    mpsy = ma(psy(t[CLOSE],12),6)
    #spsy = psy(t[CLOSE])
    state_psy =  mpsy<300

    logger.debug(stock.code)
    linelog(stock.code)
    return gand(sbuy,state_psy)

def psy_test(stock,dates,ma_standard=60):
    #另，psy(55)的5X55, psy(12),psy(67)的ma5的叉
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    g60 = stock.g60
    spsy1 = psy(t[CLOSE],67)
    spsy2 = psy(t[CLOSE],67)

    ma_psy1 = ma(spsy1,5)
    ma_psy2 = ma(spsy2,5)
    trend_1 = strend(ma_psy1) > 0
    trend_2 = strend(ma_psy2) > 0    
    cross_psy = gand(cross(ma_psy2,ma_psy1)>0,trend_1,trend_2)

    ma_standard = ma(t[CLOSE],ma_standard)
    trend_ma_standard = strend(ma_standard) > 0    
 
    sbuy = gand(cross_psy,g,trend_ma_standard)
    #sbuy = gand(cross_psy,g)
    #sbuy = gand(cross_psy,g)
    linelog(stock.code)
    #for d,v,m,b,ms in zip(dates,ma_psy1,ma_psy2,sbuy,ma_standard):print d,v,m,b,ms

    return sbuy

def gtest3(stock,dates):
    t = stock.transaction

    if not stock.has_attr('ma'):
        ma10 = ma(t[CLOSE],10)
        ma20 = ma(t[CLOSE],20)
        ma60 = ma(t[CLOSE],60)
        ma120 = ma(t[CLOSE],120)
        t120 = strend(ma120)>0
        ma_above = gand(greater(ma10,ma20),greater(ma20,ma60),greater(ma60,ma120))        
        stock.set_attr('ma',{'10':ma10,'20':ma20,'60':ma60,'120':ma120,'t120':t120,'above':ma_above})
    t120,ma_above = stock.ma['t120'],stock.ma['above']
    ma10,ma20,ma60,ma120 = stock.ma['10'],stock.ma['20'],stock.ma['60'],stock.ma['120']

    g = gand(stock.g20 >= stock.g60+1000,stock.g60 >= stock.g120+1000,stock.g20>=3000,stock.g20<=8000)

    gma20 = ma(stock.g20,5)
    gma60 = ma(stock.g60,5)
    cross_fast_slow = gand(cross(gma60,gma20)>0,strend(gma20)>0,strend(gma60)>0)
    
    linelog(stock.code)
    #cs = catalog_signal_cs(stock.c60,c_extractor)
    
    #return gand(g,cs,cross_fast_slow,t120,ma_above)
    #return gand(g,cross_fast_slow,ma_above)    
    return gand(g,t120,ma_above)    


def gtest2(stock,dates):
    t = stock.transaction

    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)

    gx = stock.g60
    ma_fast = ma(gx,5)
    ma_slow = ma(gx,20)
    trend_ma_fast = strend(ma_fast) > 0
    trend_ma_slow = strend(ma_slow) > 0    
    cross_fast_slow = gand(cross(ma_slow,ma_fast)>0,trend_ma_fast,trend_ma_slow)
    
    c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s>=3300,s<=6600)
    cs = catalog_signal_cs(stock.c60,c_extractor)

    linelog(stock.code)
    
    #return gand(g,cs,cross_fast_slow,t120,ma_above)
    return gand(g,cs,cross_fast_slow,stock.above,stock.t120)    

def gtest(stock,fast,slow,dates,ma_standard=120):
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    g60 = stock.g60
    ma_fast = ma(g60,fast)
    ma_slow = ma(g60,slow)
    trend_ma_fast = strend(ma_fast) > 0
    trend_ma_slow = strend(ma_slow) > 0    
    cross_fast_slow = gand(cross(ma_slow,ma_fast)>0,trend_ma_fast,trend_ma_slow)

    ma_standard = ma(t[CLOSE],ma_standard)
    trend_ma_standard = strend(ma_standard) > 0    
 
    ma_120 = ma(stock.g120,5)   #平滑一下
    ma_250 = ma(stock.g250,5)
    trend_ma_120 = strend(ma_120) > 0
    trend_ma_250 = strend(ma_250) > 0

    print stock.code

    return gand(cross_fast_slow,g,trend_ma_120,trend_ma_250,g60>5000,g60<8000)

#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s>=3300,s<=6600)

def ext_factory(sbegin,send):
    return lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s>=sbegin,s<=send)

def func_test(stock,fast,mid,slow,ma_standard=500,extend_days=10,pre_length=67,**kwargs):
    ''' vama三叉
    '''
    dates = kwargs['dates'] #打印输出用
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    #svap,v2i = vap_pre(t[VOLUME],t[CLOSE],pre_length)
    skey = 'vap_pre_%s' % pre_length
    if not stock.has_attr(skey): #加速
        stock.set_attr(skey,vap_pre(t[VOLUME],t[CLOSE],pre_length))
    svap,v2i = stock.get_attr(skey) 
    
    ma_svapfast = ma(svap,fast)
    ma_svapmid = ma(svap,mid)    
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapmid = strend(ma_svapmid) > 0    
    trend_ma_svapslow = strend(ma_svapslow) > 0

    cross_fast_mid = band(cross(ma_svapmid,ma_svapfast)>0,trend_ma_svapfast)
    cross_fast_slow = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast)    
    cross_mid_slow = band(cross(ma_svapslow,ma_svapmid)>0,trend_ma_svapmid)
    sync_fast_2 = sfollow(cross_fast_mid,cross_fast_slow,extend_days)
    sync3 = sfollow(sync_fast_2,cross_mid_slow,extend_days)

    ma_standard = ma(svap,ma_standard)
    trend_ma_standard = strend(ma_standard) > 0    
    
    diff,dea = cmacd(svap)
    trend_macd = gand(diff>dea,strend(diff)>0,strend(dea)>0)
    #vsignal = gand(sync3,trend_ma_standard,trend_macd)
    vsignal = gand(sync3,trend_ma_standard,trend_macd)

    msvap = transform(vsignal,v2i,len(t[VOLUME]))

    #cs = catalog_signal_cs(stock.c120,cextractor)
    #cs = catalog_signal_cs(stock.c20,cextractor)
    #cx = catalog_signal_c(stock.catalog, lambda c:gand(c.g20>5000,c.g20<9000,c.g20>c.g60))
    
    #func = lambda a,b,c,d,e:gand(a>b,b>c,c>d,d>e)
    #cy = catalog_signal_m(func,stock.c5,stock.c20,stock.c60,stock.c120,stock.c250)

    #cs = gand(cx,cy)

    gtrend = gand(strend(stock.g5)>0,strend(ma(stock.g20,5))>0,strend(ma(stock.g60,5))>0)
    
    
    #sbuy = msvap
    #sbuy = gand(g,msvap)
    sbuy = gand(g,gtrend,msvap,cs)
    #sbuy = gand(g,cs,msvap)
    #down_limit = tracelimit((t[OPEN]+t[LOW])/2,t[HIGH],sbuy,stock.atr,600,3000)

    #seller = atr_seller_factory(stop_times=600,trace_times=3000)    
    #ssell = seller(stock,sbuy)

    #sb = make_trade_signal_advanced(sbuy,ssell)      
    #for x in zip(dates,sbuy,down_limit,t[LOW],t[OPEN],t[CLOSE],stock.atr*600/1000,t[OPEN]-stock.atr*600/1000,ssell,sb)[-80:]:
    #    print x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9]

    #sup = up_under(t[HIGH],t[LOW],10,300)    
    #return gand(g,msvap)
    #for x in zip(dates,t[CLOSE],stock.g5,stock.g20,stock.g60,stock.g120,stock.g250):
    #    print '%s,%s,%s,%s,%s,%s,%s' % (x[0],x[1],x[2],x[3],x[4],x[5],x[6])

    #f.close()

    linelog(stock.code)
    return sbuy

def func_test_old(stock,fast,slow,base,sma=55,ma_standard=120,extend_days=5,**kwargs):
    ''' svama二叉,extend_days天内再有日线底线叉ma(base)
    '''
    dates = kwargs['dates'] #打印输出用
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    svap,v2i = svap_ma(t[VOLUME],t[CLOSE],sma)
    #print len(svap),len(v2i),len(dates)
    print stock.code
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0

    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    #for s,v,f,sl,c in zip(svap,v2i,ma_svapfast,ma_svapslow,cross_fast_slow):
    #    print '%s,%s,%s,%s,%s' % (dates[v],s,f,sl,c)
    for s,v in zip(svap,v2i):
        print '%s,%s' % (dates[v],s)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))
    print np.sum(msvap),np.sum(cross_fast_slow)
    ma_standard = ma(t[CLOSE],ma_standard)
    trend_ma_standard = strend(ma_standard) > 0

    ma_fast = t[LOW]
    ma_base = ma(t[CLOSE],base)
    trend_base = strend(ma_base) > 0    
    xcross = band(cross(ma_base,ma_fast),trend_base)
    #sf = sfollow(msvap,xcross,extend_days)  #syntony
    sf = syntony(msvap,xcross,extend_days)
    
    #sbuy = gand(g,sf,trend_ma_standard)
    sbuy = msvap
    #print dates[sbuy>0]
    down_limit = tracelimit((t[OPEN]+t[LOW])/2,t[HIGH],sbuy,stock.atr,600,3000)
    
    #for x in zip(dates,sbuy,down_limit,t[LOW],t[OPEN],t[CLOSE],stock.atr*600/1000,t[OPEN]-stock.atr*600/1000):
    #    print x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7]
    return sbuy

def prepare_buyer(dates):
    #return fcustom(func_test,ma_standard=500,slow=50,extend_days=31,fast=30,mid=67,dates=dates)
    #return fcustom(func_test,ma_standard=500,slow=45,extend_days=17,fast=32,mid=79,dates=dates)
    #return fcustom(func_test,fast= 33,mid= 84,slow=345,ma_standard=500,extend_days= 27,dates=dates,cextractor=ext_factory(3300,6600))
    return fcustom(gtest,fast=5,slow=60,dates=dates)
    #return fcustom(psvama2,fast=  9,slow=1160,dates=dates) 
    #return fcustom(psy_test,dates=dates)
    #return fcustom(dma,dates=dates)
    #return fcustom(vmacd,dates=dates)
    #return fcustom(psvama3,fast=165,mid=184,slow=1950,dates=dates) 
    #return fcustom(ma4,dates=dates)
    #return fcustom(vmacd_ma4,dates=dates)
    #return fcustom(temv,dates=dates)
    #return fcustom(wvad,dates=dates)
    #return fcustom(ma3,dates=dates)
    #return fcustom(xma60,dates=dates)
    #return fcustom(nhigh,dates=dates)
    #return fcustom(pmacd,dates=dates)
    #return fcustom(gtest2,dates=dates)
    #return fcustom(gcs,dates=dates)
    #return fcustom(tsvama2,dates=dates)
    #return fcustom(svap_macd,dates=dates)
    #return fcustom(gtest3,dates=dates)
    #return fcustom(ctest,dates=dates)
    #return fcustom(swrap,dates=dates)



def prepare_base(sdata):
    base = BaseObject()
    sdatas = extract_collect(sdata.values(),CLOSE)
    base.g20 = (increase(sdatas,20)>0).sum(0)
    return base

def prepare_gfilter(ref):
    #diff,dea = cmacd(ref.transaction[CLOSE],50,120)
    #gfilter = greater(diff,dea)
    gfilter = strend(ma(ref.transaction[CLOSE],250))>0
    #gfilter = np.zeros_like(ref.transaction[CLOSE])
    return gfilter

def run_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata.values())
    prepare_order(catalogs)
    prepare_common(sdata.values(),idata[ref_id])
    dummy_catalogs('catalog',catalogs)

    tbegin = time()

    pman = AdvancedATRPositionManager()
    dman = DateManager(begin,end)
    myMediator=nmediator_factory(trade_strategy=B1S1,pricer = oo_pricer)
    #seller = atr_seller_factory(stop_times=2000,trace_times=3000)
    #seller = atr_seller_factory(stop_times=1500,trace_times=3000)
    #seller = atr_seller_factory(stop_times=1000,trace_times=3000)
    seller = atr_seller_factory(stop_times=600,trace_times=3000)
    #seller = csc_func
    #seller = fcustom(csc_func,threshold=100)

    buyer = prepare_buyer(dates)   
    name,tradess = calc_trades(buyer,seller,sdata,dates,xbegin,cmediator=myMediator)
    result,strade = ev.evaluate_all(tradess,pman,dman)
    #print strade

    #last_trades
    #m = cmediator(buyer,seller)
    #trades = m.calc_last(sdata,dates,xbegin)


    f = open('srun.txt','w+')
    f.write(strade)
    f.close()

    #tradess = myMediator(buyer,seller).calc_last(sdata,dates,xbegin)
    #print tradess[0]
    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    


if __name__ == '__main__':
    logging.basicConfig(filename="srun_x4c.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    #测试时间段 [19980101,19990101-20010801],[20000101,20010701-20050901],[20040601,20050801-20071031],[20060601,20071031-20090101]
    #总时间段   [20000101,20010701,20090101]    #一个完整的周期+一个下降段
    #分段测试的要求，段mm > 1000-1500或抑制，总段mm > 2000
    
    #begin,xbegin,end = 19980101,20010701,20090101
    #begin,xbegin,end = 20000101,20010701,20090101
    #begin,xbegin,end = 20000101,20010701,20050901
    #begin,xbegin,end = 19980101,19990701,20010801    
    #begin,xbegin,end = 20040601,20050801,20071031
    #begin,xbegin,end = 20060601,20071031,20090101
    #begin,xbegin,end = 19980101,19990101,20090101
    #begin,xbegin,end,lbegin = 20070101,20080601,20090327,20080601
    #begin,xbegin,end,lbegin = 19980101,20010701,20090327,20000101
    begin,xbegin,end = 20000101,20010701,20091231
    tbegin = time()
    
    dates,sdata,idata,catalogs = prepare_all(begin,end,[],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH601988','SH600050'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH601988'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH601398'],[ref_code])        
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SZ000630'],[ref_code])        
    #dates,sdata,idata,catalogs = prepare_all(begin,end,get_codes(),[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,get_codes(source='SZSE'),[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SZ000792'],[ref_code])            
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600888'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SZ000020'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600002'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600433','SH600000'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH000001'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600067'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600766'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SZ002012'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600971'],[ref_code])
    #c_posort('c120',catalogs,distance=120)
    

    tend = time()
    print u'数据准备耗时: %s' % (tend-tbegin)    
    import psyco
    psyco.full()

    run_main(dates,sdata,idata,catalogs,begin,end,xbegin)

