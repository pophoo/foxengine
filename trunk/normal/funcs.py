# -*- coding: utf-8 -*-

''' 定制的buy,sell func
'''

def ma3(stock,fast,mid,slow,standard=0,extend_days = 10):
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
    #g = gand(stock.g5 > stock.g20,stock.g20 > stock.gorder,stock.gorder > stock.g120,stock.g120 > stock.g250)    
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
    if standard == 0:
        standard = slow
    trend_standard = trend(ma(t[CLOSE],55)) > 0
    return gand(g,trend_standard,confirm_cross)

def svama2(stock,fast,slow,sma=22):
    ''' vama两线交叉
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
    g = gand(stock.g5 > stock.g20,stock.g20 > stock.gorder,stock.gorder > stock.g120,stock.g120 > stock.g250)
    svap,v2i = svap_ma(t[VOLUME],t[CLOSE],sma)
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = trend(ma_svapfast) > 0
    trend_ma_svapslow = trend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))
    maslow = ma(t[CLOSE],55)
    ma120 = ma(t[CLOSE],120)
    trend_ma120 = trend(ma120) > 0
    return gand(g,msvap,trend_ma120)

def svama2s(stock,fast,slow,sma=22,extend_days = 20):
    ''' vama两线交叉, 先是快线叉慢线,然后是慢线叉快线
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
    g = gand(stock.g5 > stock.g20,stock.g20 > stock.gorder,stock.gorder > stock.g120,stock.g120 > stock.g250)
    svap,v2i = svap_ma(t[VOLUME],t[CLOSE],sma)
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = trend(ma_svapfast) > 0
    trend_ma_svapslow = trend(ma_svapslow) > 0
    #cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    cross_fast_slow = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast)
    cross_slow_fast = band(cross(ma_svapfast,ma_svapslow)>0,trend_ma_svapslow)
    synced = sfollow(cross_fast_slow,cross_slow_fast,extend_day)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))
    maslow = ma(t[CLOSE],55)
    ma120 = ma(t[CLOSE],120)
    trend_ma120 = trend(ma120) > 0
    return gand(g,msvap,trend_ma120)

