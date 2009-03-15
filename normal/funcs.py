# -*- coding: utf-8 -*-

''' 定制的buy,sell func
'''

import logging
logger = logging.getLogger('wolfox.fengine.normal.funcs')

import numpy as np
from wolfox.fengine.internal import *


def cvama3(stock,fast,mid,slow,rstart=3300,rend=6600,ma_standard=500,extend_days=10,pre_length=67):
    ''' vama三叉
    '''
    t = stock.transaction
    if rstart >= rend:
        return np.zeros_like(t[CLOSE])

    c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s>=rstart,s<=rend)

    svap,v2i = vap_pre(t[VOLUME],t[CLOSE],pre_length)
    ma_svapfast = ma(svap,fast)
    ma_svapmid = ma(svap,mid)    
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapmid = strend(ma_svapmid) > 0    
    trend_ma_svapslow = strend(ma_svapslow) > 0

    #cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    cross_fast_mid = band(cross(ma_svapmid,ma_svapfast)>0,trend_ma_svapfast)
    cross_fast_slow = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast)    
    cross_mid_slow = band(cross(ma_svapslow,ma_svapmid)>0,trend_ma_svapmid)
    sync_fast_2 = sfollow(cross_fast_mid,cross_fast_slow,extend_days)
    sync3 = sfollow(sync_fast_2,cross_mid_slow,extend_days)

    ma_standard = ma(svap,ma_standard)
    trend_ma_standard = strend(ma_standard) > 0    
    vsignal = band(sync3,trend_ma_standard)
    msvap = transform(vsignal,v2i,len(t[VOLUME]))
    
    cs = catalog_signal_cs(stock.c60,c_extractor)
    #sup = up_under(t[HIGH],t[LOW],10,300)    

    #g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    
    return gand(cs,msvap)


def csvama3(stock,fast,mid,slow,rstart=3300,rend=6600,ma_standard=500,extend_days=10,sma=55):
    ''' svama三叉
        可以考虑信号发出n天内，突然放水10-20%到下位支撑(20,55,120)[附近]然后向上
            或者强势盘整幅度越来越小    见600117 20030115的信号(6,12,69,ex=13,ma=227,sma=21)
            另四线理顺也是启动的强势附件
            并考虑筛选条件，如10内涨幅超过20-25%

    '''
    t = stock.transaction

    if rstart >= rend:
        return np.zeros_like(t[CLOSE])

    c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s>=rstart,s<=rend)

    #print stock.code,len(t[CLOSE]),sum(t[CLOSE])
    svap,v2i = svap_ma(t[VOLUME],t[CLOSE],sma)
    ma_svapfast = ma(svap,fast)
    ma_svapmid = ma(svap,mid)    
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapmid = strend(ma_svapmid) > 0    
    trend_ma_svapslow = strend(ma_svapslow) > 0

    ma_standard = ma(svap,ma_standard)
    trend_ma_standard = strend(ma_standard) > 0    

    #cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    cross_fast_mid = band(cross(ma_svapmid,ma_svapfast)>0,trend_ma_svapfast)
    cross_fast_slow = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast)    
    cross_mid_slow = band(cross(ma_svapslow,ma_svapmid)>0,trend_ma_svapmid)
    sync_fast_2 = sfollow(cross_fast_mid,cross_fast_slow,extend_days)
    sync3 = sfollow(sync_fast_2,cross_mid_slow,extend_days)
    vsignal = band(sync3,trend_ma_standard)
    msvap = transform(vsignal,v2i,len(t[VOLUME]))

    cs = catalog_signal_cs(stock.c60,c_extractor)
    #g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    g = gand(stock.g5 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    
    return gand(cs,g,msvap)


def csvama2(stock,fast,slow,rstart=3300,rend=6600,ma_standard=500,sma=65):
    ''' svama两线交叉
    '''
    t = stock.transaction

    if rstart >= rend:
        return np.zeros_like(t[CLOSE])

    c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s>=rstart,s<=rend)
    
    svap,v2i = svap_ma(t[VOLUME],t[CLOSE],sma)
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    ma_standard = ma(svap,ma_standard)
    trend_ma_standard = strend(ma_standard) > 0    
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    vsignal = band(cross_fast_slow,trend_ma_standard)
    msvap = transform(vsignal,v2i,len(t[VOLUME]))
    cs = catalog_signal_cs(stock.c60,c_extractor)
    #g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    g = gand(stock.g5 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    return gand(cs,g,msvap)

def ma3(stock,fast,mid,slow,ma_standard=120,extend_days = 10):
    ''' ma三线金叉
        不要求最慢的那条线在被快线交叉时趋势必须向上，但要求被中线交叉时趋势向上
    '''
    #logger.debug('ma3 calc: %s ' % stock.code)    
    t = stock.transaction
    #g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    #g对这个没效果
    ma_fast = ma(t[CLOSE],fast)
    ma_mid = ma(t[CLOSE],mid)
    ma_slow = ma(t[CLOSE],slow)
    trend_fast = strend(ma_fast) > 0
    trend_mid = strend(ma_mid) > 0    
    trend_slow = strend(ma_slow) > 0
    cross_fast_mid = band(cross(ma_mid,ma_fast),trend_fast)
    cross_fast_slow = band(cross(ma_slow,ma_fast),trend_fast)
    cross_mid_slow = band(cross(ma_slow,ma_mid),trend_mid)
    cross_fm_fs = sfollow(cross_fast_mid,cross_fast_slow,extend_days)
    confirm_cross = sfollow(cross_fm_fs,cross_mid_slow,extend_days)
    trend_ma_standard = strend(ma(t[CLOSE],ma_standard)) > 0
    sup = up_under(t[HIGH],t[LOW],extend_days,300)
    return gand(trend_ma_standard,confirm_cross,sup)


def svama2(stock,fast,slow,ma_standard=250,sma=65):
    ''' svama两线交叉
    '''
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    #g = np.ones_like(stock.g5)
    svap,v2i = svap_ma(t[VOLUME],t[CLOSE],sma)
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    ma_standard = ma(svap,ma_standard)
    trend_ma_standard = strend(ma_standard) > 0    
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    vsignal = band(cross_fast_slow,trend_ma_standard)
    msvap = transform(vsignal,v2i,len(t[VOLUME]))
    #sup = up_under(t[HIGH],t[LOW],10,300)    
    return gand(g,msvap)

def svama2s(stock,fast,slow,ma_standard=250,extend_days = 10,sma=55):
    ''' svama两线交叉, 先是快线叉慢线,然后是慢线叉快线
    '''
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    svap,v2i = svap_ma(t[VOLUME],t[CLOSE],sma)
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    ma_standard = ma(svap,ma_standard)
    trend_ma_standard = strend(ma_standard) > 0    
    cross_fast_slow = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast)
    cross_slow_fast = band(cross(ma_svapfast,ma_svapslow)>0,trend_ma_svapslow)
    synced = sfollow(cross_fast_slow,cross_slow_fast,extend_days)
    vsignal = band(synced,trend_ma_standard)
    msvap = transform(vsignal,v2i,len(t[VOLUME]))
    #sup = up_under(t[HIGH],t[LOW],extend_days,300)    
    return gand(g,msvap)

def svama3(stock,fast,mid,slow,ma_standard=250,extend_days=10,sma=55):
    ''' svama三叉
        可以考虑信号发出n天内，突然放水10-20%到下位支撑(20,55,120)[附近]然后向上
            或者强势盘整幅度越来越小    见600117 20030115的信号(6,12,69,ex=13,ma=227,sma=21)
            另四线理顺也是启动的强势附件
            并考虑筛选条件，如10内涨幅超过20-25%

    '''
    t = stock.transaction
    #print stock.code,len(t[CLOSE]),sum(t[CLOSE])
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    svap,v2i = svap_ma(t[VOLUME],t[CLOSE],sma)
    ma_svapfast = ma(svap,fast)
    ma_svapmid = ma(svap,mid)    
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapmid = strend(ma_svapmid) > 0    
    trend_ma_svapslow = strend(ma_svapslow) > 0

    ma_standard = ma(svap,ma_standard)
    trend_ma_standard = strend(ma_standard) > 0    

    #cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    cross_fast_mid = band(cross(ma_svapmid,ma_svapfast)>0,trend_ma_svapfast)
    cross_fast_slow = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast)    
    cross_mid_slow = band(cross(ma_svapslow,ma_svapmid)>0,trend_ma_svapmid)
    sync_fast_2 = sfollow(cross_fast_mid,cross_fast_slow,extend_days)
    sync3 = sfollow(sync_fast_2,cross_mid_slow,extend_days)
    vsignal = band(sync3,trend_ma_standard)
    msvap = transform(vsignal,v2i,len(t[VOLUME]))

    sup = up_under(t[HIGH],t[LOW],extend_days,300)    
    return gand(g,msvap,sup)



#svama2和vama2信号发出后的再确认
def svama2x(stock,fast,slow,base,ma_standard=250,extend_days=5,sma=55):
    ''' svama二叉,extend_days天内再有日线底线叉ma(base)
    '''
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    svap,v2i = svap_ma(t[VOLUME],t[CLOSE],sma)
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0

    ma_standard = ma(svap,ma_standard)
    trend_ma_standard = strend(ma_standard) > 0    

    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    vsignal = band(cross_fast_slow,trend_ma_standard)
    msvap = transform(vsignal,v2i,len(t[VOLUME]))

    ma_fast = t[LOW]
    ma_base = ma(t[CLOSE],base)
    trend_base = strend(ma_base) > 0    
    xcross = band(cross(ma_base,ma_fast),trend_base)
    #sf = sfollow(msvap,xcross,extend_days)  #syntony
    sf = syntony(msvap,xcross,extend_days)
    #sup = up_under(t[HIGH],t[LOW],5,300)
    return gand(g,sf)

c_extractor = lambda c:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250)
def svama2c(stock,fast,slow,ma_standard=120,threshold=7500,sma=55):
    ''' svama两线交叉
    '''
    c_extractor = lambda c:c.g20>=threshold
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    c = catalog_signal_c(stock.catalog,c_extractor) 
    #g = np.ones_like(stock.g5)
    svap,v2i = svap_ma(t[VOLUME],t[CLOSE],sma)
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0

    ma_standard = ma(svap,ma_standard)
    trend_ma_standard = strend(ma_standard) > 0    

    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    vsignal = band(cross_fast_slow,trend_ma_standard)    
    msvap = transform(vsignal,v2i,len(t[VOLUME]))
   
    #sup = up_under(t[HIGH],t[LOW],10,300)    
    return gand(g,c,msvap)

def vama2(stock,fast,slow,ma_standard=250,pre_length=67):
    ''' vama双叉
    '''
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    svap,v2i = vap_pre(t[VOLUME],t[CLOSE],pre_length)
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    #cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapslow)

    ma_standard = ma(svap,ma_standard)
    trend_ma_standard = strend(ma_standard) > 0    
    vsignal = band(cross_fast_slow,trend_ma_standard)
    msvap = transform(vsignal,v2i,len(t[VOLUME]))

    #sup = up_under(t[HIGH],t[LOW],10,300)
    return gand(g,msvap)

def vama3(stock,fast,mid,slow,ma_standard=250,extend_days=10,pre_length=67):
    ''' vama三叉
    '''
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    svap,v2i = vap_pre(t[VOLUME],t[CLOSE],pre_length)
    ma_svapfast = ma(svap,fast)
    ma_svapmid = ma(svap,mid)    
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapmid = strend(ma_svapmid) > 0    
    trend_ma_svapslow = strend(ma_svapslow) > 0

    #cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    cross_fast_mid = band(cross(ma_svapmid,ma_svapfast)>0,trend_ma_svapfast)
    cross_fast_slow = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast)    
    cross_mid_slow = band(cross(ma_svapslow,ma_svapmid)>0,trend_ma_svapmid)
    sync_fast_2 = sfollow(cross_fast_mid,cross_fast_slow,extend_days)
    sync3 = sfollow(sync_fast_2,cross_mid_slow,extend_days)

    ma_standard = ma(svap,ma_standard)
    trend_ma_standard = strend(ma_standard) > 0    
    vsignal = band(sync3,trend_ma_standard)
    msvap = transform(vsignal,v2i,len(t[VOLUME]))

    #sup = up_under(t[HIGH],t[LOW],10,300)    
    return gand(g,msvap)

def vama2x(stock,fast,slow,base,ma_standard=250,extend_days=5,pre_length=65):
    ''' vama双叉,extend_days天内再有日线底线叉ma(base)
    '''
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    svap,v2i = vap_pre(t[VOLUME],t[CLOSE],pre_length)
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    #cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapslow)

    ma_standard = ma(svap,ma_standard)
    trend_ma_standard = strend(ma_standard) > 0    
    vsignal = band(cross_fast_slow,trend_ma_standard)
    msvap = transform(vsignal,v2i,len(t[VOLUME]))

    #sup = up_under(t[HIGH],t[LOW],10,300)

    ma_fast = t[LOW]
    ma_base = ma(t[CLOSE],base)
    trend_base = strend(ma_base) > 0    
    xcross = band(cross(ma_base,ma_fast),trend_base)
    #sf = sfollow(msvap,xcross,extend_days) #syntony
    sf = syntony(msvap,xcross,extend_days)    

    return gand(g,sf)

