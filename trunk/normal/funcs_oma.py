# -*- coding: utf-8 -*-

''' 定制的buy,sell func
'''

import logging
logger = logging.getLogger('wolfox.fengine.normal.funcs')

import numpy as np
from wolfox.fengine.internal import *

#后续：svama/vama系列信号发出之后，下来碰到ma55/120然后向上者

def ma3(stock,fast,mid,slow,ma_standard=120,extend_days = 10):
    ''' ma三线金叉
        不要求最慢的那条线在被快线交叉时趋势必须向上，但要求被中线交叉时趋势向上
        argnames= ['slow','middle','fast']
        arggroups = [   #[21,5,1],
                #[55,21,3],
                #[30,20,10],
                #[40,30,20],
                [25,47,29],
                [88,45,4],
                [69,34,2],
                [70,45,8]#,
                #[70,45,3]
                ]
        
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


c_extractor = lambda c:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250)
def svama2(stock,fast,slow,ma_standard=120,sma=65):
    ''' svama两线交叉
        argnames = ['slow','fast','threshold']
        arggroups = [ [4,53,30],
            [108,53,15],
            [61,16,15],
            [62,7,15],
            [46,16,15],
            [9,35,15],
            [126,14,15],
            [4,29,15],
            [98,5,75],
            [68,5,75],
            [88,14,75],
            [71,8,75]
        ]
    '''
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    #c = catalog_signal_c(stock.catalog,c_extractor)    #效果不咋地，反作用
    #g = np.ones_like(stock.g5)
    svap,v2i = svap_ma(t[VOLUME],t[CLOSE],sma)
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))
    ma_standard = ma(t[CLOSE],ma_standard)
    trend_ma_standard = strend(ma_standard) > 0
    #sup = up_under(t[HIGH],t[LOW],10,300)    
    #return gand(g,msvap,trend_ma_standard,sup)
    return gand(g,msvap,trend_ma_standard)

def svama2s(stock,fast,slow,sma=55,ma_standard=120,extend_days = 10):
    ''' svama两线交叉, 先是快线叉慢线,然后是慢线叉快线
        argnames = ['slow','fast','threshold']
        arggroups = [ [4,53,30],
            [108,53,15],
            [61,16,15],
            [62,7,15],
            [46,16,15],
            [9,35,15],
            [126,14,15],
            [4,29,15],
            [98,5,75],
            [68,5,75],
            [88,14,75],
            [71,8,75]
        ]
    '''
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    svap,v2i = svap_ma(t[VOLUME],t[CLOSE],sma)
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    #cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    cross_fast_slow = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast)
    cross_slow_fast = band(cross(ma_svapfast,ma_svapslow)>0,trend_ma_svapslow)
    synced = sfollow(cross_fast_slow,cross_slow_fast,extend_days)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))
    ma_standard = ma(t[CLOSE],ma_standard)
    trend_ma_standard = strend(ma_standard) > 0
    #sup = up_under(t[HIGH],t[LOW],extend_days,300)    
    #return gand(g,msvap,trend_ma_standard,sup)
    return gand(g,msvap,trend_ma_standard)

def svama3(stock,fast,mid,slow,ma_standard=120,extend_days=10,sma=55):
    ''' svama三叉
        argnames = ['slow','middle','fast','threshold']
        arglist = [(3,128,1),(2,65,1),(1,32,1),(15,76,15)]
        arggroups = [
            [119,55,12,15],
            [103,62,12,45],
            [111,57,19,15],
            [120,64,23,15],
            [127,60,12,45],
            [127,42,12,45],
            [92,57,17,45],
            #[123,64,12,15],
            [31,57,30,15],
            [23,61,30,30],
            [31,56,28,15],
            [18,52,22,75],
            [20,60,25,30],
            [43,26,31,60],
            [68,64,28,75],
            [44,61,7,75],
            [20,48,30,60]
        ]    

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

    #cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    cross_fast_mid = band(cross(ma_svapmid,ma_svapfast)>0,trend_ma_svapfast)
    cross_fast_slow = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast)    
    cross_mid_slow = band(cross(ma_svapslow,ma_svapmid)>0,trend_ma_svapmid)
    sync_fast_2 = sfollow(cross_fast_mid,cross_fast_slow,extend_days)
    sync3 = sfollow(sync_fast_2,cross_mid_slow,extend_days)
    msvap = transform(sync3,v2i,len(t[VOLUME]))

    #print 'ma_standard:',ma_standard
    ma_standard = ma(t[CLOSE],ma_standard)
    trend_ma_standard = strend(ma_standard) > 0
    sup = up_under(t[HIGH],t[LOW],extend_days,300)    
    return gand(g,msvap,trend_ma_standard,sup)
    #sbuy = gand(g,msvap,trend_ma_standard)
    #print sum(g),sum(msvap),sum(trend_ma_standard)
    #print 'sum sbuy:',sum(sbuy)
    #return sbuy

def vama2(stock,fast,slow,pre_length=120,ma_standard=120):
    ''' vama双叉
        argnames = ['slow','fast']
        arggroups = [ [2,113],
            [26,123],
            [22,3],
            [58,3] ]    
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
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))

    ma_standard = ma(t[CLOSE],ma_standard)
    trend_ma_standard = strend(ma_standard) > 0
    #sup = up_under(t[HIGH],t[LOW],10,300)
    #return gand(g,msvap,trend_ma_standard,sup)
    return gand(g,msvap,trend_ma_standard)

def vama3(stock,fast,mid,slow,pre_length=120,ma_standard=120,extend_days=10):
    ''' vama三叉
        argnames = ['vama_standard','vamamiddle','vamafast']
            arggroups = [[116,59,12],
            [119,64,20],
            [100,55,29],
            [100,45,12],
            [124,53,25],
            #[90,51,14],
            [102,43,8]]
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
    msvap = transform(sync3,v2i,len(t[VOLUME]))

    ma_standard = ma(t[CLOSE],ma_standard)
    trend_ma_standard = strend(ma_standard) > 0
    #sup = up_under(t[HIGH],t[LOW],10,300)    
    #return gand(g,msvap,trend_ma_standard,sup)
    return gand(g,msvap,trend_ma_standard)


#svama2和vama2信号发出后的再确认
def svama2x(stock,fast,slow,base,sma=55,ma_standard=120,extend_days=5):
    ''' svama二叉,extend_days天内再有日线底线叉ma(base)
    '''
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    svap,v2i = svap_ma(t[VOLUME],t[CLOSE],sma)
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))
    ma_standard = ma(t[CLOSE],ma_standard)
    trend_ma_standard = strend(ma_standard) > 0

    ma_fast = t[LOW]
    ma_base = ma(t[CLOSE],base)
    trend_base = strend(ma_base) > 0    
    xcross = band(cross(ma_base,ma_fast),trend_base)
    #sf = sfollow(msvap,xcross,extend_days)  #syntony
    sf = syntony(msvap,xcross,extend_days)
    sup = up_under(t[HIGH],t[LOW],5,300)
    return gand(g,sf,trend_ma_standard)

def vama2x(stock,fast,slow,base,pre_length=120,ma_standard=120,extend_days=5):
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
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))

    ma_standard = ma(t[CLOSE],ma_standard)
    trend_ma_standard = strend(ma_standard) > 0
    #sup = up_under(t[HIGH],t[LOW],10,300)

    ma_fast = t[LOW]
    ma_base = ma(t[CLOSE],base)
    trend_base = strend(ma_base) > 0    
    xcross = band(cross(ma_base,ma_fast),trend_base)
    #sf = sfollow(msvap,xcross,extend_days) #syntony
    sf = syntony(msvap,xcross,extend_days)    

    return gand(g,sf,trend_ma_standard)


def svama2c(stock,fast,slow,sma=55,ma_standard=120,threshold=7500):
    ''' svama两线交叉
        argnames = ['slow','fast','threshold']
        arggroups = [ [4,53,30],
            [108,53,15],
            [61,16,15],
            [62,7,15],
            [46,16,15],
            [9,35,15],
            [126,14,15],
            [4,29,15],
            [98,5,75],
            [68,5,75],
            [88,14,75],
            [71,8,75]
        ]
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
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))
    ma_standard = ma(t[CLOSE],ma_standard)
    trend_ma_standard = strend(ma_standard) > 0
    #sup = up_under(t[HIGH],t[LOW],10,300)    
    #return gand(g,msvap,trend_ma_standard,sup)
    return gand(g,c,msvap,trend_ma_standard)

