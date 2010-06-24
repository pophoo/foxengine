# -*- coding: utf-8 -*-

'''

主力合约、次月合约与半年合约的成交量还可以，下季合约严重没量，被操控
但因为次月合约开张日晚，如if1007在0524才开张，所以测试不准


'''


from wolfox.fengine.ifuture.ibase import *
from wolfox.fengine.ifuture.ifuncs import fmacd1_long,fmacd1_short

ama1 = ama_maker()
ama2 = ama_maker(covered=30,dfast=6,dslow=100)

def tfunc(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)

    #signal = gand(xc_ru0s(trans[IOPEN],trans[ICLOSE],trans[IHIGH],trans[ILOW],trans[IVOL])>0)
    #xdiff,xdea = macd_ru(trans[IOPEN],trans[ICLOSE],trans[IHIGH],trans[ILOW])
    #signal = gand(cross(xdea,xdiff)<0)
    #fsignal = gand(cross(sif.dea1,sif.diff1)<0,strend(sif.diff30-sif.dea30)<0,sif.diff30>0,sif.diff30<sif.dea30)

    #signal = sfollow(signal,fsignal,30)
    #signal = gand(strend(sif.diff5-sif.dea5)<0,strend(sif.diff30<sif.dea30)<0)
    #signal = gand(signal,ksfilter,sif.xatr<20)

    signal = ldevi(trans[ILOW],sif.diff1,sif.dea1,sif.diff5)
    signal = gand(signal,sif.diff5<0,strend(sif.diff30-sif.dea30)>0,strend(sif.ma5-sif.ma30)>0)


    return signal*XBUY

def down30(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)

    msignal = gand(cross(sif.dea30,sif.diff30)<0)
    fsignal = gand(cross(cached_zeros(len(sif.dea1)),sif.diff1)<0,sif.diff30>0)
    
    signal = sfollow(msignal,fsignal,120)

    signal = gand(signal,ksfilter,sif.xatr<20)

    return signal*XSELL



def svap(sif,sopened=None):
    trans = sif.transaction
    svap,v2i = svap_ma(trans[IVOL],trans[ICLOSE],67)
    ma_svapfast = ma(svap,5)
    ma_svapslow = ma(svap,13)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    msvap = transform(cross_fast_slow,v2i,len(trans[IVOL]))
    s1 = cross(sif.dea1,sif.diff1)>0
    signal = sfollow(msvap,s1,10)
    signal = gand(signal,strend(sif.diff5-sif.dea5)>0,strend(sif.ma5)>2)
    return signal


def long5x(sif,sopened=None):#
    '''
    '''
    trans = sif.transaction
    s15 = strend(sif.diff15x-sif.dea15x)
    s15x = np.zeros_like(sif.diff1)
    s15x[sif.i_cof15] = s15
    s15x = extend2next(s15x)

    #signal = gand(cross(sif.sdea5x,sif.sdiff5x)>0,sif.sdiff15x>0,sif.sdiff30x>sif.sdea30x,sif.sdiff15x>sif.sdea15x)#,sif.xatr<20)#,strend(sif.diff15-sif.dea15)>0,strend(sif.diff30-sif.dea30)>0)
    signal = gand(cross(sif.sdea5x,sif.sdiff5x)>0,s15x,sif.sdiff30x>sif.sdea30x,sif.sdiff15x>sif.sdea15x)#,sif.xatr<20)#,strend(sif.diff15-sif.dea15)>0,strend(sif.diff30-sif.dea30)>0)
    return signal * XBUY

def ipmacd_long_f(sif,sopened=None):
    '''
        过滤后的macd1上叉
        操作方式:
            1. 1分钟下叉
            2. 3分钟后macd仍然在延续往下,
            3. 5分钟macd>0且上行中,diff5<0
               30分钟macd<0,但在上行中
    '''

    trans = sif.transaction

    sfilter = gand(strend(sif.diff5-sif.dea5)>0,sif.diff5>sif.dea5,sif.diff5<0,sif.diff30<sif.dea30,strend(sif.diff30-sif.dea30)>0)    
    sfilter2 = gand(trans[IOPEN] - trans[ICLOSE] < 100,rollx(trans[IOPEN]) - trans[ICLOSE] < 200)
    signal = gand(fmacd1_long(sif,3,sfilter),sif.xatr<15,sfilter2)

    return signal * XBUY


def short5x(sif,sopened=None):#
    '''
    '''
    trans = sif.transaction
    s15 = strend(sif.diff15x-sif.dea15x)
    s15x = np.zeros_like(sif.diff1)
    s15x[sif.i_cof15] = s15
    s15x = extend2next(s15x)

    signal = gand(cross(sif.sdea5x,sif.sdiff5x)<0,sif.diff30<0,sif.sdiff30x<sif.sdea30x,sif.sdiff15x<sif.sdea15x)#,sif.xatr<20)#,strend(sif.diff15-sif.dea15)>0,strend(sif.diff30-sif.dea30)>0)
    return signal * XSELL


def long5x2(sif,sopened=None):#
    '''
    '''
    trans = sif.transaction
    signal = gand(cross(sif.sdea5x,sif.sdiff5x)>0,strend(sif.sdiff30x-sif.sdea30x)>0,strend(sif.sdiff15x-sif.sdea15x)>0)
    return signal * XBUY


def ipmacd_long50(sif,sopened=None):#+
    '''
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea5,sif.diff5)>0,sif.diff1>0,strend(sif.ma5)>2,sif.ma5>sif.ma13,sif.ma5>sif.ma30,strend(sif.diff30-sif.dea30)>0)
    #signal = gand(signal,sif.xatr<15)
    return signal * XBUY


def ipmacd_long_old(sif,sopened=None):#
    ''' 
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea1,sif.diff1)>0,sif.diff5>sif.dea5,sif.diff30>0,strend(sif.diff30-sif.dea30)>0)#,sif.diff1>0)#,strend(sif.diff5)>0)
    signal = gand(signal,strend(sif.ma5)>1,sif.ma5>sif.ma30,strend(sif.ma60)>5,sif.xatr<20)#,strend(sif.diff5-sif.dea5)<0)
    return signal * XBUY

def up1_0(sif,sopened=None):#
    trans = sif.transaction
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤
    
    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1),sif.diff30<0,sif.diff5<0,strend(sif.diff5-sif.dea5)>0,strend(sif.diff30-sif.dea30)>0,strend(sif.ma5)>1,sif.ma5>sif.ma13)
    signal = gand(signal,sif.xatr<15,sfilter,strend(sif.ma5-sif.ma30)>0)
    return signal * XBUY

def up5_0(sif,sopened=None):#
    trans = sif.transaction
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤
    
    signal = gand(cross(cached_zeros(len(sif.diff5)),sif.diff5))
    ss= gand(strend(sif.diff5-sif.dea5)>0,strend(sif.diff30-sif.dea30)>0,strend(sif.ma5)>1,sif.ma5>sif.ma13)
    fsignal = gand(cross(sif.dea1,sif.diff1)>0,ss)
    signal = gand(sfollow(signal,fsignal,15),sif.xatr<15,sfilter,strend(sif.ma5-sif.ma30)>0)
    return signal * XBUY

def up(sif,sopened=None):
    trans = sif.transaction
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤

    signal = gand(strend(sif.diff1-sif.dea1)>2,strend(sif.diff5-sif.dea5)>4,strend(sif.diff30-sif.dea30)>0,strend(sif.ma5-sif.ma30)>0,sif.ma5>sif.ma13,sif.ma13>sif.ma30)

    signal = gand(signal,sfilter,sif.xatr<15)
    return signal * XBUY

def ipmacd_long(sif,sopened=None):#
    ''' 
    '''
    trans = sif.transaction
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤    
    signal = gand(cross(sif.dea5,sif.diff5)>0,strend(sif.diff30-sif.dea30)>0,sif.diff5<0)
    fsignal = gand(cross(sif.dea1,sif.diff1)>0)
    #signal = gand(signal,sif.xatr<20,sfilter)
    signal = gand(sfollow(signal,fsignal,30),sif.xatr<20,sfilter)
    return signal * XBUY



def ipmacd_5x13(sif,sopened=None):
    '''
    '''
    trans = sif.transaction
    signal = gand(cross(sif.ma30,sif.ma5)>0,sif.ma5>sif.ma13,trans[ICLOSE]>sif.ma5,sif.diff1>sif.dea1,strend(sif.diff1-sif.dea1)>5,strend(sif.diff5-sif.dea5)>0)
    return signal * XBUY

def ipmacd_longt(sif,sopened=None):#+
    trans = sif.transaction
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200) #向上突变过滤
    signal = gand(cross(sif.dea1,sif.diff1)>0,sif.diff5<0,strend(sif.diff5-sif.dea5)>0,sif.diff30<sif.dea30,strend(sif.diff30-sif.dea30)>0,sif.ma5>sif.ma13,strend(sif.ma5)>1,strend(sif.ma5-sif.ma30)>0)
    signal = gand(signal,sif.xatr<15,sfilter)
    return signal * XBUY


def ipmacd_longt2(sif,sopened=None):#+
    '''
        R=488,w/t = 7/11,s=2498
        物极必反? ma5>ma13的反弹
        添加 sif.diff30<0之后, R=226,times=15,wtimes/times = 5/15
        发现很奇怪，1分钟上叉的需要diff5>dea5比较好，
        而下叉反而是diff5<0为好
        忽略超过10点的瞬间拔高导致的上叉

        用fmacd1_long过滤无增效
    '''
    trans = sif.transaction
    msignal = gand(cross(sif.dea1,sif.diff1)>0)#
    fsignal = gand(strend(sif.diff5-sif.dea5)>2,sif.diff30<sif.dea30,trans[ICLOSE] - trans[IOPEN] < 60,sif.ma5>sif.ma13,strend(sif.ma5)>2)#,sif.ma13>sif.ma60)#,strend(sif.diff5)>0)
    fsignal = gand(fsignal,sif.xatr<15,strend(sif.diff1-sif.dea1)>0,sif.diff1>sif.dea1)
    signal = sfollow(msignal,fsignal,5)
    return signal * XBUY


def ipmacd_long_c(sif,sopened=None):#-
    '''
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea1,sif.diff1)>0,sif.diff1<0,sif.diff5<0,sif.diff5<sif.dea5,sif.diff30<0,sif.diff30>sif.dea30,trans[ICLOSE] - trans[IOPEN] < 100,sif.ma5>sif.ma13)#,sif.ma13>sif.ma60)#,strend(sif.diff5)>0)
    #signal = gand(signal,sif.xatr<15)
    return signal * XBUY


def ma4_short(sif,sopened=None):
    ''' 
        5/13/30/60向下理顺
    '''
    trans = sif.transaction
    #signal = gand(cross(sif.dea1,sif.diff1)<0,sif.ma5<sif.ma13,sif.ma13<sif.ma60)
    signal = cross(sif.dea1,sif.diff1)<0
    #signal = gand(signal,sif.ma5<sif.ma13,sif.ma13<sif.ma30,sif.ma30<sif.ma60)
    signal = gand(signal,sif.diff1<0,sif.diff5<0,strend(sif.diff5)<0,strend(sif.diff1)<0,strend(sif.diff30)<0)
    return signal * XSELL

def ma30_short(sif,sopened=None):
    ''' 下行中下叉30线
    '''
    trans = sif.transaction
    signal = gand(cross(sif.ma30,trans[IHIGH])<0,strend(sif.ma30)<0)
    sf = msum(trans[IHIGH]>sif.ma30,5) < 3
    signal = gand(signal,sf)
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)
    fsignal = gand(cross(sif.dea1,sif.diff1)<0,sif.diff1<0,sif.diff5<0,strend(sif.diff30-sif.dea30)<0,sfilter,strend(sif.ma13-sif.ma60)<0)
    signal = sfollow(signal,fsignal,10)
    return signal * XSELL


def ma30_long(sif,sopened=None):
    ''' 上行中上叉30线
    '''
    trans = sif.transaction
    signal = gand(cross(sif.ma30,trans[ILOW])>0,strend(sif.ma30)>0,sif.diff5>0,sif.ma13>sif.ma30,sif.ma30>sif.ma60)
    sf = msum(trans[ILOW]<sif.ma30,5) < 3
    signal = gand(signal,sf)
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)
    fsignal = gand(cross(sif.dea1,sif.diff1)>0,sif.diff1>0,sif.diff5>0,strend(sif.diff30)>0,sfilter)
    #fsignal = gand(cross(sif.ma13,sif.ma5)<0,sif.diff1<0,sif.diff5<0,strend(sif.diff30)<0)
    signal = sfollow(signal,fsignal,10)
    return signal * XBUY

def ma60_short(sif,sopened=None):
    ''' ma60拐头
    '''
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)
    
    msignal = gand(strend(sif.ma60) == -1,rollx(strend(sif.ma60))<10)
    fsignal = gand(cross(sif.dea1,sif.diff1)<0,strend(sif.diff5-sif.dea5)>0,sfilter,sif.xatr<20)
    signal = sfollow(msignal,fsignal,15)
    return signal * XSELL


def ma30_short2(sif,sopened=None):
    ''' ma30拐头
    '''
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)
    
    msignal = gand(strend(sif.ma30) == -1,rollx(strend(sif.ma30))<10)
    fsignal = gand(cross(sif.dea1,sif.diff1)<0,strend(sif.diff5-sif.dea5)>0,sfilter,sif.xatr<20)
    signal = sfollow(msignal,fsignal,15)
    return signal * XSELL


def ma60_long(sif,sopened=None):
    ''' ma60拐头
    '''
    trans = sif.transaction
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤
    msignal = gand(strend(sif.ma60) == 1,rollx(strend(sif.ma60))<-10)
    fsignal = gand(cross(sif.dea1,sif.diff1)>0,strend(sif.diff5-sif.dea5)>0,strend(sif.diff30-sif.dea30)>0)
    signal = gand(sfollow(msignal,fsignal,10),sfilter,sif.xatr<15)
    return signal * XBUY


def rmlong(sif,sopened=None):#+++
    ''' 
        RU1011
    '''
    trans = sif.transaction
    sfilter = gand(sif.diff5>0,sif.diff30>sif.dea30)
    signal = gand(fmacd1_long(sif,0,sfilter))#,strend(sif.diff5)>0)

    return signal * XBUY


def ipmacd_short_x5(sif,sopened=None):#+++
    ''' 
        R=187,times=9/18,2788
        忽略超过10点的瞬间下行导致的下叉
        diff5/30均小于0，且ma5在下叉前已经下行，ma5<ma13/30, ma60已经下行5分钟以上
        ma5<ma13/30实际上和diff1<0可能性质类同?
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea1,sif.diff1)<0,sif.diff5<0,sif.diff30<0,sif.diff1<0,trans[IOPEN] - trans[ICLOSE] < 60)#,strend(sif.diff5)>0)
    signal = gand(signal,rollx(strend(sif.ma5))<0,sif.ma5<sif.ma13,sif.ma5<sif.ma30,strend(sif.ma60)<-5,sif.xatr<20)#,strend(sif.diff5-sif.dea5)<0)

    fsignal = gand(strend(sif.diff1-sif.dea1) <= -1)   #下叉后仍然连续下行中
    signal = gand(rollx(signal,1),fsignal,sif.diff5<0,sif.diff30<0)

    return signal * XSELL


def ipmacd_short_f(sif,sopened=None):#+
    ''' 
        带过滤的1分钟下叉
        1. 下叉后3分钟内仍然下行
        2. 5分钟macd<0,且macd下行中(这里的5分钟macd不是1分钟macd的扩周期版,而是真正的5分钟macd)
           diff30<0, 白线在上,但macd在下行中. 应该是反弹失败的类型
    '''
    trans = sif.transaction
    msignal = gand(cross(sif.dea1,sif.diff1)<0)#,sif.diff5<0,sif.diff30<0,sif.diff1<0,trans[IOPEN] - trans[ICLOSE] < 60)#,strend(sif.diff5)>0)
    fsignal = gand(strend(sif.diff1-sif.dea1) <= -3)   #下叉后仍然连续下行中
    signal = gand(rollx(msignal,3),fsignal)
    
    sfilter = gand(sif.sdiff5x<sif.sdea5x,strend(sif.sdiff5x-sif.sdea5x)<0,sif.diff30<0,strend(sif.diff30-sif.dea30)<0,sif.diff30>sif.dea30)
    signal = gand(signal,sfilter,trans[IOPEN] - trans[ICLOSE] < 60)
    #signal = gand(signal,strend(sif.ma5)<-1,sif.ma5<sif.ma13,sif.ma5<sif.ma30,strend(sif.ma60)<-5,sif.xatr<20)#,strend(sif.diff5-sif.dea5)<0)
    return signal * XSELL


def ipmacd_short_f2(sif,sopened=None):#+
    ''' 
        带过滤的1分钟下叉
        1. 下叉后3分钟内仍然下行
        2. 前一5分钟diff在上,但macd下行中(这里的5分钟macd不是1分钟macd的扩周期版,而是真正的5分钟macd)
    '''
    trans = sif.transaction
    sfilter = gand(sif.sdiff5x<sif.sdea5x,strend(sif.sdiff5x-sif.sdea5x)<0,sif.diff30<0,strend(sif.diff30-sif.dea30)<0,sif.diff30>sif.dea30)
    msignal = gand(cross(sif.dea1,sif.diff1)<0)#,sfilter)
    fsignal = gand(strend(sif.diff1-sif.dea1) <= -3)   #下叉后仍然连续下行中
    signal = gand(rollx(msignal,3),fsignal)
    
    signal = gand(msignal,sfilter,trans[IOPEN] - trans[ICLOSE] < 60)
    return signal * XSELL


def ipmacd_short_devi(sif,sopened=None):#+++
    ''' 
        R=187,times=9/18,2788
        忽略超过10点的瞬间下行导致的下叉
        diff5/30均小于0，且ma5在下叉前已经下行，ma5<ma13/30, ma60已经下行5分钟以上
        ma5<ma13/30实际上和diff1<0可能性质类同?
    '''
    trans = sif.transaction

    signal = gand(hdevi(trans[IHIGH],sif.diff1,sif.dea1),sif.diff5<0,trans[IOPEN] - trans[ICLOSE] < 60)#,strend(sif.diff5)>0)
    #signal = gand(signal,rollx(strend(sif.ma5))<0)#,sif.ma5<sif.ma13,sif.ma5<sif.ma30,sif.xatr<20)#,strend(sif.diff5-sif.dea5)<0)
    return signal * XSELL

def ipmacd_short_devi1(sif,sopened=None):
    '''
        顶背离操作，去掉了诸多条件
    '''

    trans = sif.transaction

    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)

    signal = gand(hdevi(trans[IHIGH],sif.diff1,sif.dea1))

    fsignal = gand(strend(sif.diff1-sif.dea1)==-1)

    signal = gor(signal,gand(sfollow(signal,fsignal,15),msum(sif.diff1<sif.dea1,15)>9))

    signal = gand(signal,sif.diff5<0,sfilter,strend(sif.diff5-sif.dea5)<0,strend(sif.ma5-sif.ma13)<0)

    return signal * XSELL


def ipmacd_long_devi1(sif,sopened=None):
    '''
        底背离之后，macd1连续3分钟或以上增长
        diff30<0
        macd30>0或macd30向上
        sfilter,xfilter    
    '''

    trans = sif.transaction

    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤

    msignal = ldevi(trans[ILOW],sif.diff1,sif.dea1)
    fsignal = gand(strend(sif.diff1-sif.dea1) >= 3)   #上叉后仍然连续增长中

    signal = gand(rollx(msignal,3),fsignal,sif.diff30<0,gor(strend(sif.diff30-sif.dea30)>0,sif.diff30>sif.dea30),sfilter,sif.xatr<15)

    return signal * XBUY

def ipmacd_shortt(sif,sopened=None):#+++
    ''' 
        R=828,times=4/5,2072
        30分钟下降途中反弹失败的情形
        忽略超过10点的瞬间下行导致的下叉
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea1,sif.diff1)<0,sif.diff1<0,sif.diff30>sif.dea30,sif.diff5<0,sif.diff30<0,trans[IOPEN] - trans[ICLOSE] < 60)#,strend(sif.diff5)>0)
    #signal = gand(signal,sif.ma5<sif.ma13,sif.xatr<20)#,strend(sif.diff5-sif.dea5)<0)
    signal = gand(signal,strend(sif.ma5)<-1,sif.ma5<sif.ma13,sif.ma5<sif.ma30,strend(sif.ma60)<-5,sif.xatr<20)#,strend(sif.diff5-sif.dea5)<0)
    
    return signal * XSELL


def ipmacd_short_b(sif,sopened=None):#+
    '''
        R=163,times=4/8
        忽略超过10点的瞬间下行导致的下叉

    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea1,sif.diff1)<0,sif.diff1>0,strend(sif.diff5-sif.dea5)<0,sif.diff30>sif.dea30,trans[IOPEN] - trans[ICLOSE] < 60,sif.diff5<0)#,strend(sif.diff5)>0)
    signal = gand(signal,strend(sif.ma60)<0,sif.xatr<20)#,strend(sif.diff5-sif.dea5)<0)
    return signal * XSELL

def ipmacd_short_c(sif,sopened=None):#-
    '''
        忽略超过10点的瞬间下行导致的下叉
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea1,sif.diff1)<0,sif.diff1>0,sif.diff5<0,sif.diff30<0,sif.diff30>sif.dea30,trans[IOPEN] - trans[ICLOSE] < 60)#,strend(sif.diff5)>0)
    #signal = gand(signal,sif.xatr<20)#,strend(sif.diff5-sif.dea5)<0)
    signal = gand(signal,strend(sif.ma60)<0,sif.xatr<20)#,strend(sif.diff5-sif.dea5)<0)
    
    return signal * XSELL



def ipmacd_long_b(sif,sopened=None):#-
    '''
        忽略超过10点的瞬间下行导致的上叉
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea1,sif.diff1)>0,sif.diff1<0,sif.diff5>sif.dea5,sif.diff30<0,trans[IOPEN] - trans[ICLOSE] < 60)#,strend(sif.diff5)>0)
    signal = gand(signal,sif.xatr<15)#,strend(sif.diff5-sif.dea5)<0)
    return signal * XBUY

def ipmacdx_long(sif,sopened=None):#+
    '''
        R=46,times=1/2
    '''
    trans = sif.transaction
    
    signal = gand(strend(sif.diff1-sif.dea1)==3,sif.diff1<sif.dea1,sif.diff30<sif.dea30,sif.diff5>sif.dea5,sif.diff5<0,sif.diff1<0,sif.diff1-sif.dea1 > -20,trans[ICLOSE] - trans[IOPEN] < 100)
    #signal = gand(strend(sif.diff1-sif.dea1)==3,sif.diff1<sif.dea1,sif.diff1>0,sif.diff5>sif.dea5, trans[ICLOSE] - trans[IOPEN] < 100,sif.ma5>sif.ma13)#,sif.ma13>sif.ma60)#,strend(sif.diff5)>0)
    #signal = gand(signal,sif.xatr<15)
    signal = gand(sif.ma5>sif.ma13,strend(sif.ma5)>2,sif.diff30<sif.dea30,signal)
    
    return signal * XBUY

def ipmacdx_short(sif,sopened=None):#+
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)

    signal = gand(strend(sif.diff1-sif.dea1)==-3,sif.diff1>sif.dea1,sif.diff30<0,strend(sif.diff5-sif.dea5)>0,sif.diff5<0,sif.diff1<0,sif.diff5<sif.dea5)
    signal = gand(signal,strend(sif.ma5)<-1,sif.ma5<sif.ma30,strend(sif.ma5-sif.ma30)<0,sif.xatr<20,sfilter)
    return signal * XSELL

def ipmacdx_long5(sif,sopened=None):#-
    '''柱线变化
    '''
    trans = sif.transaction
    
    signal = gand(strend(sif.diff5-sif.dea5)==3,sif.diff5<sif.dea5,sif.diff30>sif.dea30,sif.diff5<0,trans[ICLOSE] - trans[IOPEN] < 100)
    signal = gand(sif.ma5>sif.ma30,signal)
    return signal * XBUY



def ipmacd_long5(sif,sopened=None):#+
    '''
        R=432,times=4/6, 1195
    '''
    trans = sif.transaction

    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤

    signal = gand(cross(sif.dea5,sif.diff5)>0,sif.diff5>0)

    sfilter2 = gand(strend(sif.diff5)>2,sif.diff5>0,sfilter,strend(sif.diff30-sif.dea30)>0,sif.ma5>sif.ma13)
    #s1 = gand(cross(sif.dea1,sif.diff1)>0,sfilter)#,sif.xatr<15)
    s1 = gand(fmacd1_long(sif,3),sfilter2,sif.xatr<15)
    #s1 = gand(cross(sif.dea1,sif.diff1)>0)
    signal = sfollow(signal,s1,60)
    return signal * XBUY



def ipmacd_short5(sif,sopened=None):#-
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)
    
    signal = gand(cross(sif.dea5,sif.diff5)<0,sif.diff5>0,sif.diff30<0,strend(sif.diff30-sif.dea30)<0)
    signal = gand(signal,strend(sif.ma13-sif.ma60)<0,sfilter,sif.xatr<20)   
    return signal * XSELL

def ipmacd_short52(sif,sopened=None):#-
    '''
        忽略超过10点的瞬间下行导致的下叉
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea5,sif.diff5)<0,trans[IOPEN] - trans[ICLOSE] < 60)#,strend(sif.diff5)>0)
    signal1 = gand(cross(sif.dea1,sif.diff1)<0,trans[IOPEN] - trans[ICLOSE] < 60)
    signal = sfollow(signal,signal1,60)
    signal = gand(signal,strend(sif.ma60)<0,strend(sif.ma30)<0,sif.ma5<sif.ma13,sif.ma5<sif.ma30,sif.xatr<20)#,strend(sif.diff5-sif.dea5)<0)
    
    return signal * XSELL

def ipmacd_short(sif,sopened=None):#+++
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)
    signal = gand(cross(sif.dea1,sif.diff1)<0,sif.diff5<0,sif.diff30<0,sfilter,strend(sif.diff1)<-2)#,strend(sif.diff5)>0)
    signal = gand(signal,sif.xatr<20,sif.ma5<sif.ma13,strend(sif.ma30)<-4,strend(sif.ma13-sif.ma60)<0)
    return signal * XSELL

def ipmacd_short_x1(sif,sopened=None):#+++
    ''' 
        先下叉，然后小于0(2个周期内)
    '''
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.diff5<0,sif.diff30<0)
    signal = gand(cross(sif.dea1,sif.diff1)<0,sfilter,sif.diff1>0)#,strend(sif.diff5)>0)
    #signal = gand(signal,strend(sif.ma5)<-1,sif.ma5<sif.ma13,sif.ma5<sif.ma30,strend(sif.ma60)<-5,sif.xatr<20)#,strend(sif.diff5-sif.dea5)<0)

    #signal = gor(gand(rollx(signal,2),sif.diff1<0),gand(rollx(signal,1),sif.diff1<0))
    fsignal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1),sfilter,strend(sif.diff1-sif.dea1)<-2)
    signal = sfollow(signal,fsignal,3)

    return signal * XSELL


def dmacd_short(sif,sopened=None):#++
    '''
        R=86,times=6/12
        回抽时未上叉又回落
        xatr无约束
    '''
    trans = sif.transaction
    sdd = strend(sif.diff1 - sif.dea1)
    mmacd = msum(sif.diff1 < sif.dea1,5)    #一直在水线以下
    signal = gand(sdd==-1,rollx(sdd)>4,sif.diff1<sif.dea1,trans[IOPEN] - trans[ICLOSE] < 60,sif.diff5<0,sif.diff30<0)
    signal = gand(signal,strend(sif.ma60)<0,strend(sif.ma30)<0,sif.ma5<sif.ma13,sif.ma5<sif.ma30,sif.xatr<20)#,strend(sif.diff5-sif.dea5)<0)
    
    return signal * XSELL

def dmacd_short2(sif,sopened=None,rolled=1):#++
    '''
        rolled=1/2均可
    '''
    trans = sif.transaction
    sfilter= gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)#  向下突变过滤    
    sdd = strend(sif.diff1 - sif.dea1)
    signal = gand(sdd==rolled,rollx(sdd,rolled)<-4,sif.diff1-sif.dea1>0,rollx(sif.diff5,rolled)>0,rollx(sif.diff30,rolled)>0,rollx(sif.diff1,rolled)>0,sif.xatr<20,sfilter)

    return signal * XSELL

def dmacd_long2(sif,sopened=None,rolled=1):#++
    '''
        rolled=1/2均可
    '''
    trans = sif.transaction
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤

    sdd = strend(sif.diff1 - sif.dea1)
    signal = gand(sdd==rolled,rollx(sdd,rolled)<-4,sif.diff1-sif.dea1>0,rollx(sif.diff5,rolled)>0,rollx(sif.diff1,rolled)<0,sif.xatr<15,sfilter)

    return signal * XBUY


def dmacd_long_old(sif,sopened=None):#+++
    '''
        R=179,w/t=4/7
        回抽时未下叉又上涨
    '''
    trans = sif.transaction
    sdd = strend(sif.diff1 - sif.dea1)
    signal = gand(sdd==1,rollx(sdd)<-4,sif.diff1>sif.dea1, trans[ICLOSE] - trans[IOPEN] < 60,sif.diff5>sif.dea5,sif.diff5<0,sif.diff1>0)
    signal = gand(signal,sif.ma5>sif.ma30,strend(sif.ma30)>0)#,sif.ma13>sif.ma60)#,strend(sif.diff5)>0)

    return signal * XBUY

def dmacd_long(sif,sopened=None):#+++
    '''
        R=179,w/t=4/7
        回抽时未下叉又上涨
    '''
    trans = sif.transaction
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 60,rollx(trans[ICLOSE]) - trans[IOPEN] < 120)#: 向上突变过滤

    sdd = strend(sif.diff1 - sif.dea1)
    signal = gand(sdd==1,rollx(sdd)<-4,sif.diff1>sif.dea1,sif.diff5>sif.dea5,sif.diff5<0,sfilter,strend(sif.diff30-sif.dea30)>0,sif.diff30<0) 
    signal = gand(signal,strend(sif.ma30)>0,sif.xatr<15)

    return signal * XBUY



def dmacd_long5(sif,sopened=None):#+++
    '''
        R=75,w/t=6/16
        回抽时未下叉又上涨
    '''
    trans = sif.transaction
    sdd = strend(sif.diff5 - sif.dea5)
    signal = gand(sdd==1,rollx(sdd)<-4,sif.diff5>sif.dea5,sif.diff5<0,trans[ICLOSE] - trans[IOPEN] < 100,sif.diff30<0,sif.diff30<sif.dea30)
    #signal = gand(signal,sif.ma20>sif.ma60,strend(sif.ma60)>0)#,sif.ma13>sif.ma60)#,strend(sif.diff5)>0)


    return signal * XBUY

def dmacd_short5(sif,sopened=None):#+++
    trans = sif.transaction
    sfilter= gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)#  向下突变过滤    

    sdd = strend(sif.diff5 - sif.dea5)
    signal = gand(sdd==-1,rollx(sdd)>4,sif.diff5<sif.dea5,sif.diff1<sif.dea1,sif.diff30>sif.dea30,sif.diff30<0,strend(sif.diff30-sif.dea30)<0)
    signal = gand(signal,sif.ma5<sif.ma13,sfilter,sif.xatr<20,strend(sif.ma13-sif.ma60)<0)
    
    return signal * XSELL

def ama_short(sif,sopened=None): #+
    '''
        R=62,w/t=9/24
    '''
    trans = sif.transaction
    xama1 = ama1(trans[ICLOSE])
    xama2 = ama2(trans[ICLOSE])
    signal = gand(cross(xama2,xama1)<0,strend(sif.diff5)<0)

    #s1 = gand(cross(sif.dea1,sif.diff1)<0,sif.diff5<sif.dea5,sif.diff5>0)
    #signal = sfollow(signal,s1,60)

    return signal * XSELL

def ama_short2(sif,sopened=None):#-
    ''' 与其它叠加无意义
        但作为平多头仓的选项很好
    '''
    trans = sif.transaction
    xama1 = ama1(trans[ICLOSE])
    xama2 = ama2(trans[ICLOSE])
    signal = gand(cross(xama2,trans[ICLOSE])<0,strend(sif.diff1)<0)
    return signal * XSELL

def ama_long(sif,sopened=None):#-
    trans = sif.transaction
    xama1 = ama1(trans[ICLOSE])
    xama2 = ama2(trans[ICLOSE])
    signal = gand(cross(xama2,trans[ICLOSE])>0,strend(sif.diff5)>0)
    return signal * XBUY

def emv_short(sif,sopened=None):#+
    trans = sif.transaction
    semv = emv(trans[HIGH],trans[LOW],trans[IVOL])
    signal = gand(cross(cached_zeros(len(semv)),semv)<0,sif.diff5<sif.dea5,sif.diff5>0,strend(sif.diff5-sif.dea5)>0) 
    signal = gand(signal,strend(sif.ma30)<0,sif.ma5>sif.ma30)
    return signal * XSELL

def emvx_short(sif,sopened=None):#
    '''
        R=120,w/t=5/12
        #与其它叠加有反作用
        #这个貌似是抄底的
    '''
    trans = sif.transaction
    semv = emv(trans[IHIGH],trans[ILOW],trans[IVOL])
    signal = gand(cross(cached_zeros(len(semv)),semv)<0) 
    return signal * XSELL


def emvx_long(sif,sopened=None):#
    '''
        R=120,w/t=5/12
        #与其它叠加有反作用
        #这个貌似是抄底的
    '''
    trans = sif.transaction
    xemv = temv(trans[IHIGH],trans[ILOW],trans[IVOL])
    #memv = ma(xemv,9)
    signal = gand(cross(cached_ints(len(xemv),200),xemv)>0)#,sif.ma5>sif.ma13,sif.ma13>sif.ma30,sif.ma5>sif.ma60,strend(sif.diff5-sif.dea5)>0,strend(sif.diff30-sif.dea30)>0,trans[ICLOSE]>sif.ma5)
    #signal = gand(cross(memv,xemv)>0)
    #signal = gand(cross(memv,xemv)>0)
    #s1 = gand(cross(sif.dea1,sif.diff1)>0,strend(sif.diff5-sif.dea5)>0,strend(sif.diff5)>0)
    xs1 = gand(ldevi(trans[ILOW],sif.diff1,sif.dea1,distance=1)) 
    #xs2 = gand(ldevi(trans[ILOW],sif.diff1,sif.dea1,distance=2)) 
    #s1 = gor(xs1,xs2)
    signal = sfollow(xs1,signal,10)
    #signal = xs1
    return signal * XBUY

def ma3x(sif,sopened=None):
    trans = sif.transaction
    x1 = cross(sif.ma13,sif.ma5)>0
    x2 = cross(sif.ma30,sif.ma5)>0
    x3 = cross(sif.ma30,sif.ma13)>0
    s1 = sfollow(x1,x2,5)
    s2 = sfollow(x2,x3,5)
    #xs1 = gand(ldevi(trans[ILOW],sif.diff1,sif.dea1,distance=1)) 
    xs1 = cross(sif.dea1,sif.diff1)>0
    s3 = sfollow(xs1,s2,10)
    signal = gand(s3,sif.diff1>0,strend(sif.diff5)>3,strend(sif.diff5-sif.dea5)>3,strend(sif.diff30)>3)
    return signal

def uc5(sif,sopened=None):
    trans = sif.transaction
    xc = gand(cross(sif.dea5x,sif.diff5x)>0,sif.diff5x5>sif.dea5x5)#,sif.diff5x>0,sif.diff30[sif.i_cof5]>sif.dea30[sif.i_cof5])
    sxc = np.zeros_like(trans[ICLOSE])
    sxc[sif.i_cof5] = xc
    return sxc * XBUY


def emv_short2(sif,sopened=None):#+
    '''
        R=181,w/t=3/7,551
        #与其它叠加有反作用
    '''
    trans = sif.transaction
    semv = emv(trans[IHIGH],trans[ILOW],trans[IVOL])
    signal = gand(cross(cached_zeros(len(semv)),semv)<0,sif.diff5<sif.dea5,sif.diff5>0,strend(sif.diff5-sif.dea5)>0) 
    signal1 = gand(cross(sif.dea1,sif.diff1)<0,sif.diff5<sif.dea5,strend(sif.diff5-sif.dea5)>0,trans[IOPEN] - trans[ICLOSE] < 60)
    signal = sfollow(signal,signal1,30)
    signal = gand(signal,strend(sif.ma60)<0)
    
    return signal * XSELL


def emv_long(sif,sopened=None):#+--
    '''
        R=21, w/t=8/24
    '''
    trans = sif.transaction
    semv = temv(trans[IHIGH],trans[ILOW],trans[IVOL])
    msemv = ma(semv,9)
    #signal = gand(cross(msemv,semv)>0) 
    pres =  ldevi(trans[ILOW],sif.diff1,sif.dea1)
    signal = gand(cross(cached_zeros(len(semv)),semv)>0,strend(sif.diff5-sif.dea5)>0) 
    signal = syntony(pres,signal,10)
    x0 = gand(cross(cached_zeros(len(semv)),sif.diff1)>0,sif.diff1>sif.dea1,strend(sif.diff30-sif.dea30)>0,strend(sif.diff5)>0)
    signal = sfollow(signal,x0,10)

    #signal1 = gand(cross(sif.dea1,sif.diff1)>0,sif.diff5>0,trans[IOPEN] - trans[ICLOSE] < 60)
    #signal = sfollow(signal,signal1,30)
    #signal = gand(signal,strend(sif.ma60)>0,strend(sif.ma13)>0,sif.ma5>sif.ma30)
    return signal * XBUY    #XSELL,比较失败，居然作为反向信号更好. 目前没办法处理5分钟数据?

def xmacd_short(sif,sopened=None):#+-   不可叠加
    '''
        R=85,w/t=7/12
    '''
    trans = sif.transaction
    
    dd = sif.diff5 - sif.dea5
    sdd = strend(dd)
    signal = gand(dd<-15,sif.diff30>0,sif.diff5>0,trans[IOPEN] - trans[ICLOSE] < 60)
    #signal = gand(signal,sif.ma5<sif.ma30)
    return signal * XSELL


def ihigh(sif,sopened=None):#- 60高点
    '''
        R=2,w/t=12/68
    '''
    trans = sif.transaction
    mline = rollx(tmax(trans[IHIGH],30)) #半小时高点为准
    dcross = cross(mline,trans[IHIGH])>0    
    signal = gand(dcross,sif.ma5>sif.ma10,sif.ma10>sif.ma60)
    return signal * XBUY

def xma(sif,sopened=None): #--
    trans = sif.transaction
    sx = cross(sif.ma13,sif.ma5)>0
    signal = gand(sx,sif.ma5>sif.ma30,strend(sif.ma60)>0,strend(sif.ma30)>0)
    return signal * XBUY

def mfollow_short(sif,sopened=None):   #+
    '''
        R=53,w/t=6/15,510
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea5,sif.diff5)<0,trans[IOPEN] - trans[ICLOSE] < 100,sif.diff5>0)
    s1 = gand(cross(sif.dea1,sif.diff1)<0,sif.diff5<sif.dea5,sif.diff5>0)
    signal = sfollow(signal,s1,60)
    signal = gand(signal,strend(sif.ma60)<0,sif.ma5<sif.ma13)
    return signal * XSELL

def mfollow_long(sif,sopened=None):   #+, 水线以下
    '''
        R=75,w/t=6/17
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea5,sif.diff5)>0,trans[ICLOSE] - trans[IOPEN]< 60,sif.diff5<0)
    s1 = gand(cross(sif.dea1,sif.diff1)>0,sif.diff5>sif.dea5,sif.diff5<0)
    signal = sfollow(signal,s1,60)
    signal = gand(signal,sif.ma5>sif.ma13,strend(sif.ma30)>0)
    return signal * XBUY


def down02(sif,sopened=None): #+
    '''
        R=542,times=2/3
    '''
    trans = sif.transaction
    signal5 = gand(cross(cached_zeros(len(sif.diff5)),sif.diff5)<0)
    sfilter = gand(sif.diff5<0,trans[IOPEN] - trans[ICLOSE] < 60,sif.diff30>sif.dea30,sif.diff30<0)
    signal1 = gand(fmacd1_short(sif,3,sfilter))
    signal = sfollow(signal5,signal1,30)
    signal = gand(signal,strend(sif.ma30)<0)
    return signal * XSELL

def down0(sif,sopened=None): #-
    '''
        R=30,w/t=10/22
        [down0,down02]无叠加作用
        首次失败后再次介入
    '''
    trans = sif.transaction
    signal5 = gand(cross(cached_zeros(len(sif.diff5)),sif.diff5)<0)
    signal = signal5

    signal = gand(signal,strend(sif.ma30)<0)

    return signal * XSELL

def down01(sif,sopened=None): #++
    ''' 
        R=104,times=5/13
        30分钟框架下的下行，5分钟框架的上行，以及1分钟的下行
        去掉
    '''
    trans = sif.transaction
    sfilter= gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)#  向下突变过滤

    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1)<0,strend(sif.diff5-sif.dea5)<0,sif.diff5>0,strend(sif.diff30-sif.dea30)<0,sif.diff30<0,strend(sif.diff1)<-2,sfilter,sif.xatr<20)
    return signal * XSELL


def up0(sif,sopened=None): #+
    '''
        抄底模式? 去掉
        R=190,w/t=5/10,1425
        [up0,up02]无叠加作用.5分钟上穿0的时候,早已经发出信号了
    '''
    trans = sif.transaction
    signal5 = gand(cross(cached_zeros(len(sif.diff5)),sif.diff5)>0,sif.diff30<0,sif.diff30<sif.dea30,trans[ICLOSE] - trans[IOPEN] < 100)
    signal = gand(signal5,strend(sif.ma60)>0,sif.ma5>sif.ma60)
    return signal5 * XBUY

def up02(sif,sopened=None): #-
    '''
        R=71,w/t=4/13
    '''
    trans = sif.transaction
    signal5 = gand(cross(cached_zeros(len(sif.diff5)),sif.diff5)>0,sif.diff30<0,sif.diff30<sif.dea30,trans[ICLOSE] - trans[IOPEN] < 100)
    signal1 = gand(cross(sif.dea1,sif.diff1)>0,sif.diff5>0)
    #signal1 = gand(fmacd1_long(sif,3,sif.diff5>0),sif.diff5>0)
    signal = sfollow(signal5,signal1,30)
    return signal * XBUY


def xhdevi_stop(sif,sopened=None):#+--
    ''' 顶背离平多仓
    '''
    trans = sif.transaction
    xs = gand(hdevi(trans[IHIGH],sif.diff1,sif.dea1))
    return xs * XSELL

def xldevi_stop(sif,sopened=None):#+--
    ''' 顶背离平多仓
    '''
    trans = sif.transaction
    xs = gand(ldevi(trans[IHIGH],sif.diff1,sif.dea1))
    return xs * XBUY


def xhdevi(sif,sopened=None):#-
    '''
        [xhdevi,xhdevi2] 组合实现第一次失败后的再次介入，但第一次成功不再介入
        +
    '''
    trans = sif.transaction
    xs = gand(hdevi(trans[IHIGH],sif.diff5,sif.dea5))
    return xs * XSELL

def xhdevi1(sif,sopened=None):#+
    '''
        [xhdevi,xhdevi2] 组合实现第一次失败后的再次介入，但第一次成功不再介入
        +
    '''
    trans = sif.transaction
    xs = gand(hdevi(trans[IHIGH],sif.diff1,sif.dea1),sif.diff5<0,sif.diff30<0,sif.xatr<20)
    return xs * XSELL


def xhdevi2(sif,sopened=None):#-
    trans = sif.transaction
    xs = gand(hdevi(trans[IHIGH],sif.diff5,sif.dea5),sif.diff5>0)
    s1 = gand(cross(sif.dea1,sif.diff1)<0)#,sif.diff5>sif.dea5)
    signal = sfollow(xs,s1,60)
    #signal = xs
    return signal * XSELL


def xldevi(sif,sopened=None):#-
    '''
       [xldevi,xldevi2] 组合实现第一次失败后的再次介入，但第一次成功不再介入
       +
    '''
    trans = sif.transaction
    xs = gand(ldevi(trans[ILOW],sif.diff5,sif.dea5))
    signal = xs
    return signal * XBUY

def xldevi2(sif,sopened=None):#+
    '''
    '''
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 100,rollx(trans[IOPEN]) - trans[ICLOSE] < 200)

    xs = gand(ldevi(trans[ILOW],sif.diff5,sif.dea5))#,sif.diff5<0)
    s1 = gand(cross(sif.dea1,sif.diff1)>0,sfilter,sif.xatr<15,strend(sif.diff5-sif.dea5)>0,sif.diff5<0,strend(sif.ma60)<0)
    signal = sfollow(xs,s1,60)
    return signal * XBUY

def xldevi1(sif,sopened=None):#-
    '''
       一分钟底背离
    '''
    trans = sif.transaction
    xs = gand(ldevi(trans[ILOW],sif.diff1,sif.dea1),strend(sif.diff5-sif.dea5)>0,sif.diff5<0,sif.diff5<sif.dea5,sif.diff30>sif.dea30,sif.diff30<0)
    signal = xs
    return signal * XBUY


def xud(sif,sopened=None):
    trans = sif.transaction
    sxc = xc0(trans[IOPEN],trans[ICLOSE],trans[IHIGH],trans[ILOW])
    signal = gand(greater(sxc,0))
    return signal * XBUY

def imacd_stop5(sif,sopened=None):
    trans = sif.transaction
    sell_signal = lesser(cross(sif.dea5,sif.diff5),0) * XSELL
    buy_signal = greater(cross(sif.dea5,sif.diff5),0) * XBUY
    return sell_signal + buy_signal


def imacd_stop5_short(sif,sopened=None):
    trans = sif.transaction
    buy_signal = greater(cross(sif.dea5,sif.diff5),0) * XBUY
    return buy_signal


def imacd_stop1(sif,sopened=None):
    trans = sif.transaction
    sell_signal = lesser(cross(sif.dea1,sif.diff1),0) * XSELL
    buy_signal = greater(cross(sif.dea1,sif.diff1),0) * XBUY
    return sell_signal + buy_signal

def xdevi_stop1(sif,sopened=None):
    trans = sif.transaction
    sell_signal = gand(hdevi(trans[IHIGH],sif.diff1,sif.dea1)) * XSELL
    buy_signal = gand(ldevi(trans[IHIGH],sif.diff1,sif.dea1)) * XBUY
    return sell_signal + buy_signal
    
def xdevi_stop5(sif,sopened=None):
    trans = sif.transaction
    sell_signal = gand(hdevi(trans[IHIGH],sif.diff5,sif.dea5)) * XSELL
    buy_signal = gand(ldevi(trans[IHIGH],sif.diff5,sif.dea5)) * XBUY
    return sell_signal + buy_signal

def istop(sif,sopened,lost=60,win_from=100,drawdown_rate=40,max_drawdown=200):
    '''
        sif为实体
        sopen为价格序列，其中负数表示开多仓，正数表示开空仓
        lost 为止损点数
        win_from 为起始止赢点数
        win_rate为止赢回撤率,百分比
        止赢回撤 = max(win,上升值*win_rate)
    '''
    trans = sif.transaction
    rev = np.zeros_like(sopened)
    isignal = np.nonzero(sopened)[0]
    for i in isignal:
        price = sopened[i]
        if price<0: #多头止损
            buy_price = -price
            lost_stop = buy_price - lost
            cur_high = max(buy_price,trans[ICLOSE][i])
            win_stop = min(cur_high-win_from,cur_high-(cur_high-buy_price) * drawdown_rate/XBASE)
            cur_stop = lost_stop if lost_stop > win_stop else win_stop
            if trans[ICLOSE][i] < cur_stop:
                rev[i] = XSELL
                #print 'sell:',sif.transaction[IDATE][i],sif.transaction[ITIME][i],buy_price,lost_stop,cur_high,win_stop,cur_stop,trans[ILOW][i]
            else:
                for j in range(i+1,len(rev)):
                    #print buy_price,lost_stop,cur_high,win_stop,cur_stop,trans[ILOW][j]
                    if trans[ILOW][j] < cur_stop:
                        rev[j] = XSELL
                        #print 'sell:',sif.transaction[IDATE][j],sif.transaction[ITIME][j]
                        break
                    nhigh = trans[IHIGH][j]
                    if(nhigh > cur_high):
                        cur_high = nhigh
                        drawdown = (nhigh-buy_price) * drawdown_rate/XBASE
                        if drawdown > max_drawdown:
                            drawdown = max_drawdown                        
                        win_stop = min(nhigh-win_from,nhigh-drawdown)
                        if cur_stop < win_stop:
                            cur_stop = win_stop
        else:   #空头止损
            sell_price = price
            lost_stop = sell_price + lost
            cur_low = min(sell_price,trans[ICLOSE][i])
            win_stop = max(cur_low+win_from,cur_low + (sell_price-cur_low) * drawdown_rate/XBASE)            
            cur_stop = lost_stop if lost_stop < win_stop else win_stop
            if trans[ICLOSE][i] > cur_stop:
                rev[i] = XBUY
                #print 'buy:',sif.transaction[IDATE][i],sif.transaction[ITIME][i],sell_price,lost_stop,cur_low,win_stop,cur_stop,trans[IHIGH][i]
            else:
                for j in range(i+1,len(rev)):
                    #print sif.transaction[IDATE][j],sif.transaction[ITIME][j],sell_price,lost_stop,cur_low,win_stop,cur_stop,trans[IHIGH][j]
                    if trans[IHIGH][j] > cur_stop:
                        rev[j] = XBUY
                        #print 'buy:',sif.transaction[IDATE][j],sif.transaction[ITIME][j]
                        break
                    nlow = trans[ILOW][j]
                    if(nlow < cur_low):
                        cur_low = nlow
                        drawdown = (sell_price-nlow) * drawdown_rate/XBASE
                        if drawdown > max_drawdown:
                            drawdown = max_drawdown
                        win_stop = max(nlow+win_from,nlow + drawdown)
                        if cur_stop > win_stop:
                            cur_stop = win_stop
    return rev

istop_60_100_40 = fcustom(istop,lost=60,win_from=100,drawdown_rate=40,max_drawdown=250)
istop_60_100_20 = fcustom(istop,lost=60,win_from=100,drawdown_rate=20,max_drawdown=200)
istop_60_100_33 = fcustom(istop,lost=60,win_from=100,drawdown_rate=33,max_drawdown=200)

def atr_stop(sif,sopened,lost_times=200,win_times=300,max_drawdown=200):
    '''
        atr止损
        sif为实体
        sopen为价格序列，其中负数表示开多仓，正数表示开空仓
        必须谨慎处理重复开仓的问题，虽然禁止了重复开仓，但后面的同向仓会影响止损位，或抬高止损位
    '''
    trans = sif.transaction
    rev = np.zeros_like(sopened)
    isignal = np.nonzero(sopened)[0]
    for i in isignal:
        price = sopened[i]
        if price<0: #多头止损
            #print 'find long stop:',i
            buy_price = -price
            lost_stop = buy_price - sif.atr[i] * lost_times / XBASE
            cur_high = max(buy_price,trans[ICLOSE][i])
            win_stop = cur_high - sif.atr[i] * win_times / XBASE
            cur_stop = lost_stop if lost_stop > win_stop else win_stop
            if trans[ICLOSE][i] < cur_stop:
                rev[i] = XSELL            
            else:
                for j in range(i+1,len(rev)):
                    #print trans[ITIME][j],buy_price,lost_stop,cur_high,win_stop,cur_stop,trans[ILOW][j],sif.atr[j]
                    if trans[ILOW][j] < cur_stop:
                        rev[j] = XSELL
                        #print 'sell:',j
                        break
                    nhigh = trans[IHIGH][j]
                    if(nhigh > cur_high):
                        cur_high = nhigh
                        drawdown = sif.atr[j] * win_times / XBASE
                        if drawdown > max_drawdown:
                            drawdown = max_drawdown
                        win_stop = cur_high - drawdown
                        #win_stop = cur_high - sif.atr[j] * win_times / XBASE
                        
                        #print nhigh,cur_stop,win_stop,sif.atr[j]
                        if cur_stop < win_stop:
                            cur_stop = win_stop
        else:   #空头止损
            #print 'find short stop:',i
            sell_price = price
            lost_stop = sell_price + sif.atr[i] * lost_times / XBASE
            cur_low = min(sell_price,trans[ICLOSE][i])
            win_stop = cur_low + sif.atr[i] * win_times / XBASE 
            cur_stop = lost_stop if lost_stop < win_stop else win_stop
            if trans[ICLOSE][i] > cur_stop:
                rev[i] = XBUY
            else:
                for j in range(i+1,len(rev)):
                    #print trans[ITIME][j],sell_price,lost_stop,cur_low,win_stop,cur_stop,trans[IHIGH][j],sif.atr[j]                
                    if trans[IHIGH][j] > cur_stop:
                        #print 'buy:',i,price,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j]                        
                        rev[j] = XBUY
                        #print 'buy:',j
                        break
                    nlow = trans[ILOW][j]
                    if(nlow < cur_low):
                        cur_low = nlow
                        drawdown = sif.atr[j] * win_times / XBASE
                        if drawdown > max_drawdown:
                            drawdown = max_drawdown
                        win_stop = cur_low + drawdown
                        #win_stop = cur_low + sif.atr[j] * win_times / XBASE
                        if cur_stop > win_stop:
                            cur_stop = win_stop
    return rev

atr_stop_1_2 = fcustom(atr_stop,lost_times=100,win_times=200)
atr_stop_15_25 = fcustom(atr_stop,lost_times=150,win_times=250)
atr_stop_2_3 = fcustom(atr_stop,lost_times=200,win_times=300)
atr_stop_25_4 = fcustom(atr_stop,lost_times=250,win_times=400)

def daystop_long(sif,sopened):
    '''
        每日收盘前的平仓,平多仓
    '''
    stime = sif.transaction[ITIME]
    return greater(stime,1511) * XSELL

def daystop_short(sif,sopened):
    '''
        每日收盘前的平仓,平空仓
    '''
    stime = sif.transaction[ITIME]
    return greater(stime,1511) * XBUY


def atr_xstop(sif,sopened,lost_times=200,win_times=300,max_drawdown=200,min_lost=30):
    '''
        atr止损
        sif为实体
        sopen为价格序列，其中负数表示开多仓，正数表示开空仓
        谨慎处理重复开仓的问题，虽然禁止了重复开仓，但后面的同向仓会影响止损位，或抬高止损位
            即止损位会紧跟最新的那个仓，虽然未开，会有严重影响, 需要测试
    '''
    trans = sif.transaction
    rev = np.zeros_like(sopened)
    isignal = np.nonzero(sopened)[0]
    ilong_closed = 0    #多头平仓日
    ishort_closed = 0   #空头平仓日
    for i in isignal:
        price = sopened[i]
        willlost = sif.atr[i] * lost_times / XBASE
        if willlost < min_lost:
            willlost = min_lost
        if i < ilong_closed or i<ishort_closed:    #已经开了仓，且未平，不再计算            
            #print 'skiped',trans[IDATE][i],trans[ITIME][i],trans[IDATE][ilong_closed],trans[ITIME][ilong_closed]
            continue
        if price<0: #多头止损
            #print 'find long stop:',i
            #if i < ilong_closed:    #已经开了多头仓，且未平，不再计算
            #    print 'skiped',trans[IDATE][i],trans[ITIME][i],trans[IDATE][ilong_closed],trans[ITIME][ilong_closed]
            #    continue
            buy_price = -price
            lost_stop = buy_price - willlost
            cur_high = max(buy_price,trans[ICLOSE][i])
            win_stop = cur_high - sif.atr[i] * win_times / XBASE
            cur_stop = lost_stop if lost_stop > win_stop else win_stop
            if trans[ICLOSE][i] < cur_stop:
                #print '----sell----------:',cur_stop,trans[ICLOSE][i],cur_high,lost_stop
                ilong_closed = i
                rev[i] = XSELL            
            else:
                for j in range(i+1,len(rev)):
                    #print trans[ITIME][j],buy_price,lost_stop,cur_high,win_stop,cur_stop,trans[ILOW][j],sif.atr[j]
                    if trans[ILOW][j] < cur_stop or trans[ITIME][j] == 1512:    #避免atr_close跨日
                        rev[j] = XSELL
                        #print 'sell:',i,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j]
                        ilong_closed = j
                        break
                    nhigh = trans[IHIGH][j]
                    if(nhigh > cur_high):
                        cur_high = nhigh
                        drawdown = sif.atr[j] * win_times / XBASE
                        if drawdown > max_drawdown:
                            drawdown = max_drawdown
                        win_stop = cur_high - drawdown
                        #win_stop = cur_high - sif.atr[j] * win_times / XBASE
                        #print nhigh,cur_stop,win_stop,sif.atr[j]
                        if cur_stop < win_stop:
                            cur_stop = win_stop
        else:   #空头止损
            #print 'find short stop:',i
            #if i < ishort_closed:    #已经开了空头仓，且未平，不再计算
            #    print 'skiped',trans[IDATE][i],trans[ITIME][i],trans[IDATE][ishort_closed],trans[ITIME][ishort_closed]
            #    continue
            sell_price = price
            lost_stop = sell_price + willlost
            cur_low = min(sell_price,trans[ICLOSE][i])
            win_stop = cur_low + sif.atr[i] * win_times / XBASE 
            cur_stop = lost_stop if lost_stop < win_stop else win_stop
            if trans[ICLOSE][i] > cur_stop:
                #print '----buy----------:',cur_stop,trans[ICLOSE][i],cur_high,lost_stop
                ishort_closed = i
                rev[i] = XBUY
            else:
                for j in range(i+1,len(rev)):
                    #print trans[ITIME][j],sell_price,lost_stop,cur_low,win_stop,cur_stop,trans[IHIGH][j],sif.atr[j]                
                    if trans[IHIGH][j] > cur_stop or trans[ITIME][j] == 1512:#避免atr_close跨日
                        ishort_closed = j
                        rev[j] = XBUY
                        #print 'buy:',j
                        #print 'buy:',i,price,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j]                        
                        break
                    nlow = trans[ILOW][j]
                    if(nlow < cur_low):
                        cur_low = nlow
                        drawdown = sif.atr[j] * win_times / XBASE
                        if drawdown > max_drawdown:
                            drawdown = max_drawdown
                        win_stop = cur_low + drawdown
                        #print nlow,cur_stop,win_stop,sif.atr[j]
                        #win_stop = cur_low + sif.atr[j] * win_times / XBASE
                        if cur_stop > win_stop:
                            cur_stop = win_stop
    return rev

atr_xstop_15_45 = fcustom(atr_xstop,lost_times=150,win_times=450,max_drawdown=200,min_lost=30)  
atr_xstop_15_5 = fcustom(atr_xstop,lost_times=150,win_times=500,max_drawdown=200,min_lost=30)
atr_xstop_15_6 = fcustom(atr_xstop,lost_times=150,win_times=600,max_drawdown=200,min_lost=30)   #
atr_xstop_15_A = fcustom(atr_xstop,lost_times=150,win_times=1000,max_drawdown=200,min_lost=30)
atr_xstop_15_15 = fcustom(atr_xstop,lost_times=150,win_times=150,max_drawdown=200,min_lost=30)  
atr_xstop_2_2 = fcustom(atr_xstop,lost_times=200,win_times=200,max_drawdown=200,min_lost=30)  
atr_xstop_15_2 = fcustom(atr_xstop,lost_times=150,win_times=200,max_drawdown=200,min_lost=30)  
atr_xstop_2_6 = fcustom(atr_xstop,lost_times=200,win_times=600,max_drawdown=200,min_lost=30)   


atr_xstop_1_2 = fcustom(atr_xstop,lost_times=100,win_times=200,max_drawdown=200,min_lost=30)
atr_xstop_15_25 = fcustom(atr_xstop,lost_times=150,win_times=250,max_drawdown=200,min_lost=30)
atr_xstop_2_3 = fcustom(atr_xstop,lost_times=200,win_times=300,max_drawdown=200,min_lost=30)
atr_xstop_25_4 = fcustom(atr_xstop,lost_times=250,win_times=400,max_drawdown=200,min_lost=30)
atr_xstop_2_4 = fcustom(atr_xstop,lost_times=200,win_times=400,max_drawdown=200,min_lost=30)
atr_xstop_3_4 = fcustom(atr_xstop,lost_times=300,win_times=400,max_drawdown=200,min_lost=30)
atr_xstop_15_4 = fcustom(atr_xstop,lost_times=150,win_times=400,max_drawdown=200,min_lost=30)    
atr_xstop_1_4 = fcustom(atr_xstop,lost_times=100,win_times=400,max_drawdown=200,min_lost=30)
atr_xstop_05_4 = fcustom(atr_xstop,lost_times=50,win_times=400,max_drawdown=200,min_lost=30)
atr_xstop_1_5 = fcustom(atr_xstop,lost_times=100,win_times=500,max_drawdown=200,min_lost=30)
atr_xstop_05_2 = fcustom(atr_xstop,lost_times=50,win_times=200,max_drawdown=200,min_lost=30)
atr_xstop_05_15 = fcustom(atr_xstop,lost_times=50,win_times=150,max_drawdown=200,min_lost=30)
atr_xstop_05_1 = fcustom(atr_xstop,lost_times=50,win_times=100,max_drawdown=200,min_lost=30)


from wolfox.fengine.ifuture.iftrade import ocfilter

def longfilter(sif):  #在开盘前30分钟和收盘前5分钟不开仓，头三个交易日不开张
    soc = ocfilter(sif)
    #soc = gand(soc,sif.diff5>sif.dea5)
    #soc = gand(soc,gand(sif.diff30<sif.dea30))
    return soc

def shortfilter(sif):  #在开盘前30分钟和收盘前5分钟不开仓，头三个交易日不开张
    soc = ocfilter(sif)
    #soc = gand(soc,sif.diff30<0,sif.diff30>sif.dea30,sif.diff5<sif.dea5)
    #soc = gand(soc,sif.diff30<0,sif.diff30<sif.dea30,sif.diff5<sif.dea5)    
    #soc = gand(soc,sif.diff5<0)
    return soc

def nonefilter(sif):    #全清除
    return np.zeros(len(sif.diff5),int)

def xdevi_stop_long12(sif,sopened=None):#平多头
    trans = sif.transaction
    sell_signal = gand(hdevi(trans[IHIGH],sif.diff1,sif.dea1)) * XSELL
    return sell_signal 

