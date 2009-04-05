# -*- coding: utf-8 -*-

#指定股票的测试运行脚本

from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *
from wolfox.fengine.core.d1ex import tmax,derepeatc,derepeatc_v,equals
from wolfox.fengine.core.d1match import *
from wolfox.fengine.core.d1indicator import cmacd
from wolfox.foxit.base.tutils import linelog
from time import time

import logging
logger = logging.getLogger('wolfox.fengine.normal.run')    

#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s>=3300,s<=6600)

#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,s<=6600)

c_extractor = lambda c,s:gand(c.g5 >= c.g20+500,c.g20>=c.g60+500,c.g60>=c.g120+500,c.g120>=c.g250+500)

def svap_macd(stock,dates):
    t = stock.transaction
    g = gand(stock.g120 >= stock.g250,stock.g20 >= stock.g60,stock.g60 >= stock.g120)
    #g = np.ones_like(stock.g5)
    
    skey = 'svap_ma_%s' % 65
    if not stock.has_attr(skey): #加速
        stock.set_attr(skey,svap_ma(t[VOLUME],t[CLOSE],65))
    svap,v2i = stock.get_attr(skey) 

    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))

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

c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=6600)
def tsvama2(stock,dates):
    ''' svama两线交叉
    '''
    fast=20
    slow=100
    t = stock.transaction
    #g = gand(stock.g20 >= stock.g60,stock.g60 >= stock.g120)
    g = gand(stock.g20 >= stock.g60+1000,stock.g60 >= stock.g120+1000,stock.g20>=3000,stock.g20<=8000)
    
    skey = 'svap_ma_%s' % 65
    if not stock.has_attr(skey): #加速
        stock.set_attr(skey,svap_ma(t[VOLUME],t[CLOSE],65))
    svap,v2i = stock.get_attr(skey) 

    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))

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
    
    ma5 = ma(t[CLOSE],5)

    linelog(stock.code)
    #cs = catalog_signal_cs(stock.c60,c_extractor)
    
    #return gand(g,msvap,t120,ma_above)
    return gand(g,msvap,ma_above)
    #return gand(g,cs,msvap,ma_above)
    #return gand(g,cs,msvap,ma_above)

def gcs(stock,dates):
    t = stock.transaction
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
    
    g = gand(stock.g20 >= stock.g60+1000,stock.g60 >= stock.g120+1000,stock.g20>=3000,stock.g20<=8000)
    #cs = catalog_signal_cs(stock.c60,c_extractor)

    signals = gand(g,ma_above)
    #sbuy = rollx(derepeatc(signals),10)
    sbuy = signals
    gcs.sum += np.sum(sbuy)
    return sbuy

gcs.sum=0

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
    ma20,ma60,ma120 = stock.ma['20'],stock.ma['60'],stock.ma['120']
    
    mline = rollx(tmax(t[HIGH],60)) #以昨日的60高点为准
    #dcross = band(cross(mline,t[HIGH])>0,strend(mline)>=0)    #60高点可能在向下走，退出的点正好是最高点
    dcross = cross(mline,t[HIGH])>0    
    #print strend(mline).tolist()   
    linelog(stock.code)

    g = gand(stock.g5>=stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    cs = catalog_signal_cs(stock.c60,c_extractor)

    return gand(g,cs,dcross,strend(ma60)>0,ma_above)


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

def xma60(stock,dates):
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
    ma20,ma60,ma120 = stock.ma['20'],stock.ma['60'],stock.ma['120']

    water_line = ma60*115/100   #上方15处

    dcross = cross(water_line,t[LOW])

    up_cross = dcross > 0
    down_cross = dcross < 0

    sync = sfollow(down_cross,up_cross,5)

    linelog(stock.code)
    g = gand(stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    #g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60)
    #g = gand(stock.g5>=stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    cs = catalog_signal_cs(stock.c60,c_extractor)

    return gand(sync,ma_above,t120)

def wvad(stock,dates):
    t = stock.transaction
    
    vad = (t[CLOSE]-t[OPEN])*t[VOLUME]/(t[HIGH]-t[LOW]) / 10000
    svad = msum2(vad,24)
    ma_svad = ma(svad,6)

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
    g = gand(stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    cs = catalog_signal_cs(stock.c60,c_extractor)
 
    ecross = gand(g,cs,cross(ma_svad,vad)>0,strend(ma_svad)>0,t120,ma_above)
    linelog(stock.code)
    return ecross



#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=6600)
#ts = None
def temv(stock,dates):
    t = stock.transaction
    global ts
    if ts == None:
        ts = np.zeros(len(t[CLOSE]),int)
    ekey = 'emv'
    if not stock.has_attr(ekey):
        em = emv(t[HIGH],t[LOW],t[VOLUME])
        mv = msum2(em,14)
        semv = ma(mv,9)
        stock.set_attr(ekey,{'mv':mv,'semv':semv})
    if not stock.has_attr('ma'):
        ma10 = ma(t[CLOSE],10)
        ma20 = ma(t[CLOSE],20)
        ma60 = ma(t[CLOSE],60)
        ma120 = ma(t[CLOSE],120)
        t120 = strend(ma120)>0
        ma_above = gand(greater(ma10,ma20),greater(ma20,ma60),greater(ma60,ma120))        
        stock.set_attr('ma',{'10':ma10,'20':ma20,'60':ma60,'120':ma120,'t120':t120,'above':ma_above})
    mv,semv = stock.emv['mv'],stock.emv['semv']
    t120,ma_above = stock.ma['t120'],stock.ma['above']
    g = gand(stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    cs = catalog_signal_cs(stock.c60,c_extractor)

    #ecross = gand(g,cs,cross(semv,mv)<0,strend(semv)>0,t120,ma_above)
    ecross = gand(g,cs,cross(ts,mv)>0,strend(semv)>0,t120,ma_above)
    linelog(stock.code)
    return ecross
    

#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=6600)
def vmacd_ma4(stock,dates):
    t = stock.transaction
    
    if not stock.has_attr('cma'): #加速
        linelog('calc cma')
        g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
        vdiff,vdea = cmacd(t[VOLUME])
        dcross = gand(cross(vdea,vdiff),strend(vdiff)>0,strend(vdea>0))

        #ma5 = ma(t[CLOSE],5)
        ma10 = ma(t[CLOSE],10)
        ma20 = ma(t[CLOSE],20)
        ma60 = ma(t[CLOSE],60)
        ma120 = ma(t[CLOSE],120)
        t120 = strend(ma120)>0

        stock.set_attr('cma',{'10':ma10,'20':ma20,'60':ma60,'120':ma120,'t120':t120,'g':g,'dcross':dcross,'vdea':vdea})
    else:
        linelog('find cache......')

    ma10,ma20,ma60,ma120,t120,g,dcross,vdea = stock.cma['10'],stock.cma['20'],stock.cma['60'],stock.cma['120'],stock.cma['t120'],stock.cma['g'],stock.cma['dcross'],stock.cma['vdea']

    #ma_cross = gand(cross(ma10,ma5),strend(ma5)>0,strend(ma10)>0,strend(ma20)>0,strend(ma60)>0,strend(ma120)>0)


    ma_above = gand(greater(ma10,ma20),greater(ma20,ma60),greater(ma60,ma120))


    linelog(stock.code)

    cs = catalog_signal_cs(stock.c60,c_extractor)
    #return gand(g,cs,dcross,ma_above,t120)
    return gand(g,dcross,ma_above,t120,vdea>0,vdea<12000)
    #return gand(g,dcross,ma_above)

#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250)
#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s>=3300,s<=6600)
def ma4(stock,dates):
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    
    ma5 = ma(t[CLOSE],5)
    ma10 = ma(t[CLOSE],10)
    ma20 = ma(t[CLOSE],20)
    ma60 = ma(t[CLOSE],60)
    ma120 = ma(t[CLOSE],120)
    dcross = gand(cross(ma10,ma5),strend(ma5)>0,strend(ma10)>0,strend(ma20)>0,strend(ma60)>0,strend(ma120)>0)
    #dcross = gand(cross(ma10,ma5),strend(ma5)>0,strend(ma10)>0,strend(ma20)>0,strend(ma60)>0)
    dabove = gand(greater(ma10,ma20),greater(ma20,ma60),greater(ma60,ma120))
    #dabove = gand(greater(ma10,ma20),greater(ma20,ma60))
    cs = catalog_signal_cs(stock.c60,c_extractor)
    linelog(stock.code)
    return gand(g,cs,dcross,dabove)

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

def gtest2(stock,dates):
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

    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)

    gx = stock.g69
    ma_fast = ma(gx,5)
    ma_slow = ma(gx,20)
    trend_ma_fast = strend(ma_fast) > 0
    trend_ma_slow = strend(ma_slow) > 0    
    cross_fast_slow = gand(cross(ma_slow,ma_fast)>0,trend_ma_fast,trend_ma_slow)
    
    cs = catalog_signal_cs(stock.c60,c_extractor)

    linelog(stock.code)

    
    #return gand(g,cs,cross_fast_slow,t120,ma_above)
    return gand(g,cs,cross_fast_slow,ma_above)    

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
    #return fcustom(gtest,fast=5,slow=60,dates=dates)
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
    return fcustom(tsvama2,dates=dates)

def prepare_order(sdata):
    d_posort('g5',sdata,distance=5)
    d_posort('g10',sdata,distance=10)    
    d_posort('g20',sdata,distance=20)    
    d_posort('g120',sdata,distance=120)     
    d_posort('g250',sdata,distance=250)     

def run_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata.values())
    prepare_order(catalogs)
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

