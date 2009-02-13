# -*- coding: utf-8 -*-

''' 定制的buy,sell func
'''

import logging
logger = logging.getLogger('wolfox.fengine.normal.funcs')

import numpy as np
from wolfox.fengine.internal import *

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
    logger.debug('ma3 calc: %s ' % stock.code)    
    t = stock.transaction
    #g = gand(stock.g5 > stock.g20,stock.g20 > stock.g60,stock.g60 > stock.g120,stock.g120 > stock.g250)    
    #g对这个没效果
    ma_fast = ma(t[CLOSE],fast)
    ma_mid = ma(t[CLOSE],mid)
    ma_slow = ma(t[CLOSE],slow)
    trend_fast = trend(ma_fast) > 0
    trend_mid = trend(ma_mid) > 0    
    trend_slow = trend(ma_slow) > 0
    cross_fast_mid = band(cross(ma_mid,ma_fast),trend_fast)
    cross_fast_slow = band(cross(ma_slow,ma_fast),trend_fast)
    cross_mid_slow = band(cross(ma_slow,ma_mid),trend_mid)
    cross_fm_fs = sfollow(cross_fast_mid,cross_fast_slow,extend_days)
    confirm_cross = sfollow(cross_fm_fs,cross_mid_slow,extend_days)
    trend_ma_standard = trend(ma(t[CLOSE],ma_standard)) > 0
    return gand(trend_ma_standard,confirm_cross)

def svama2(stock,fast,slow,sma=22,ma_standard=120):
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
    g = gand(stock.g5 > stock.g20,stock.g20 > stock.g60,stock.g60 > stock.g120,stock.g120 > stock.g250)
    svap,v2i = svap_ma(t[VOLUME],t[CLOSE],sma)
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = trend(ma_svapfast) > 0
    trend_ma_svapslow = trend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))
    ma_standard = ma(t[CLOSE],ma_standard)
    trend_ma_standard = trend(ma_standard) > 0
    return gand(g,msvap,trend_ma_standard)

def svama2s(stock,fast,slow,sma=22,ma_standard=120,extend_days = 10):
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
    g = gand(stock.g5 > stock.g20,stock.g20 > stock.g60,stock.g60 > stock.g120,stock.g120 > stock.g250)
    svap,v2i = svap_ma(t[VOLUME],t[CLOSE],sma)
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = trend(ma_svapfast) > 0
    trend_ma_svapslow = trend(ma_svapslow) > 0
    #cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    cross_fast_slow = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast)
    cross_slow_fast = band(cross(ma_svapfast,ma_svapslow)>0,trend_ma_svapslow)
    synced = sfollow(cross_fast_slow,cross_slow_fast,extend_days)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))
    ma_standard = ma(t[CLOSE],ma_standard)
    trend_ma_standard = trend(ma_standard) > 0
    return gand(g,msvap,trend_ma_standard)

def svama3(stock,fast,mid,slow,sma=22,ma_standard=120,extend_days=10):
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
    '''
    t = stock.transaction
    g = gand(stock.g5 > stock.g20,stock.g20 > stock.g60,stock.g60 > stock.g120,stock.g120 > stock.g250)
    svap,v2i = svap_ma(t[VOLUME],t[CLOSE],sma)
    ma_svapfast = ma(svap,fast)
    ma_svapmid = ma(svap,mid)    
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = trend(ma_svapfast) > 0
    trend_ma_svapmid = trend(ma_svapmid) > 0    
    trend_ma_svapslow = trend(ma_svapslow) > 0

    #cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    cross_fast_mid = band(cross(ma_svapmid,ma_svapfast)>0,trend_ma_svapfast)
    cross_fast_slow = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast)    
    cross_mid_slow = band(cross(ma_svapslow,ma_svapmid)>0,trend_ma_svapmid)
    sync_fast_2 = sfollow(cross_fast_mid,cross_fast_slow,extend_days)
    sync3 = sfollow(sync_fast_2,cross_mid_slow,extend_days)
    msvap = transform(sync3,v2i,len(t[VOLUME]))

    ma_standard = ma(t[CLOSE],ma_standard)
    trend_ma_standard = trend(ma_standard) > 0
    return gand(g,msvap,trend_ma_standard)

def vama2(stock,fast,slow,pre_length=120,ma_standard=120):
    ''' vama双叉
        argnames = ['slow','fast']
        arggroups = [ [2,113],
            [26,123],
            [22,3],
            [58,3] ]    
    '''
    t = stock.transaction
    g = gand(stock.g5 > stock.g20,stock.g20 > stock.g60,stock.g60 > stock.g120,stock.g120 > stock.g250)    
    svap,v2i = vap_pre(t[VOLUME],t[CLOSE],pre_length)
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = trend(ma_svapfast) > 0
    trend_ma_svapslow = trend(ma_svapslow) > 0
    #cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapslow)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))

    ma_standard = ma(t[CLOSE],ma_standard)
    trend_ma_standard = trend(ma_standard) > 0
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
    g = gand(stock.g5 > stock.g20,stock.g20 > stock.g60,stock.g60 > stock.g120,stock.g120 > stock.g250)    
    svap,v2i = vap_pre(t[VOLUME],t[CLOSE],pre_length)

    ma_svapfast = ma(svap,fast)
    ma_svapmid = ma(svap,mid)    
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = trend(ma_svapfast) > 0
    trend_ma_svapmid = trend(ma_svapmid) > 0    
    trend_ma_svapslow = trend(ma_svapslow) > 0

    #cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    cross_fast_mid = band(cross(ma_svapmid,ma_svapfast)>0,trend_ma_svapfast)
    cross_fast_slow = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast)    
    cross_mid_slow = band(cross(ma_svapslow,ma_svapmid)>0,trend_ma_svapmid)
    sync_fast_2 = sfollow(cross_fast_mid,cross_fast_slow,extend_days)
    sync3 = sfollow(sync_fast_2,cross_mid_slow,extend_days)
    msvap = transform(sync3,v2i,len(t[VOLUME]))

    ma_standard = ma(t[CLOSE],ma_standard)
    trend_ma_standard = trend(ma_standard) > 0
    return gand(g,msvap,trend_ma_standard)


