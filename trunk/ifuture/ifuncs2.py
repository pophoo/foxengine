# -*- coding: utf-8 -*-

from wolfox.fengine.ifuture.ibase import *
from wolfox.fengine.ifuture.iftrade import delay_filter,atr5_uxstop_1_25,atr5_uxstop_08_25,atr5_uxstop_05_25

def ipmacd_short_5(sif,sopened=None):
    ksfilter = gand(sif.open - sif.close < 60,rollx(sif.open - sif.close) < 120,sif.xatr<2000)

    signal = gand(cross(sif.dea1,sif.diff1)<0
            ,sif.mtrend < 0
            ,sif.ltrend<0
            ,sif.strend<0
            ,sif.sdiff30x<0
            ,sif.sdiff5x<0
            )
    signal = gand(signal
            ,sif.ma5 < sif.ma13
            ,strend2(sif.ma30)<0
            ,ksfilter
            )

    return signal * ipmacd_short_5.direction
ipmacd_short_5.direction = XSELL
ipmacd_short_5.priority = 1000

def ipmacd_short_6a(sif,sopened=None):
    ksfilter = gand(sif.open - sif.close < 60,rollx(sif.open - sif.close) < 120,sif.xatr<2000) 

    signal = gand(cross(sif.dea1,sif.diff1)<0
            ,sif.mtrend<0
            ,sif.ltrend<0
            ,sif.strend<0            
            ,sif.sdiff5x<sif.sdea5x
            ,sif.s30<0 
            )
    signal = gand(signal
            ,sif.ma5 < sif.ma13
            ,strend2(sif.ma30)<0
            ,sif.ma60 < sif.ma270
            ,ksfilter
            )
    return signal * ipmacd_short_6a.direction 
ipmacd_short_6a.direction = XSELL
ipmacd_short_6a.priority = 2000

def ipmacd_short_x(sif,sopened=None):
    ksfilter = gand(sif.open - sif.close < 60,rollx(sif.open - sif.close) < 120,sif.xatr<2000) 
    signal = gand(cross(sif.dea1,sif.diff1)<0
            ,sif.mtrend<0
            ,sif.ltrend<0
            ,strend2(sif.sdiff30x-sif.sdea30x)<0    #
            ,sif.sdiff5x<0
            )
    signal = gand(signal
            ,sif.ma5 < sif.ma13
            ,sif.ma13 < sif.ma60
            ,strend2(sif.ma30)<0
            ,strend2(sif.ma270)<0
            ,ksfilter
            )
    return signal * ipmacd_short_x.direction
ipmacd_short_x.direction = XSELL
ipmacd_short_x.priority = 2000

def ipmacd_short_x2(sif,sopened=None):
    ksfilter = gand(sif.open - sif.close < 60,rollx(sif.open - sif.close) < 120,sif.xatr<2000) 

    signal = gand(cross(sif.dea1,sif.diff1)<0
            ,sif.mtrend < 0
            ,sif.ltrend<0
            #,sif.strend<0
            ,sif.s10<0
            )
    signal = gand(signal
            ,sif.ma3 < sif.ma13
            ,sif.ma13 < sif.ma60
            ,strend2(sif.ma30)<0
            ,strend2(sif.ma270)<0
            ,ksfilter
            )
    return signal * ipmacd_short_x2.direction
ipmacd_short_x2.direction = XSELL
ipmacd_short_x2.priority = 1600


def gd30(sif,sopened=None):
    ''' 
        向下跳空
        并且收盘小于30分钟内的最低价
    '''

    signal = gand(sif.high < rollx(sif.low)
            ,sif.time > 915
        )

    signal = gand(signal
            ,sif.close < rollx(tmin(sif.low,30))
            )

    signal = gand(signal
            ,strend2(sif.sdiff30x - sif.sdea30x)<0
            ,sif.sdiff5x < sif.sdea5x
            ,strend2(sif.ma135)<0
            ,sif.ltrend<0
            )

    return signal * gd30.direction
gd30.direction = XSELL
gd30.priority = 500

def godown5(sif,sopened=None):
    '''
        5分钟收盘击穿昨日低点后30分钟内1分钟下叉卖空
    '''
    
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

 
    lowd = sif.lowd #- sif.atrd/XBASE/8 #gmin(sif.closed,sif.opend)-sif.atrd/XBASE/8

    xlowd = np.zeros(len(sif.diff1),np.int32)
    xlowd[sif.i_cofd] = lowd

    xlowd = extend(xlowd,260)

    signal = np.zeros_like(sif.diff1)

    signal[sif.i_cof5] = gand(cross(xlowd[sif.i_cof5],sif.close5)<0)

    signal = sfollow(signal,cross(sif.dea1,sif.diff1)<0,20)

    signal = gand(signal
            #,strend(sif.ma270)<0
            ,strend(sif.sdiff30x-sif.sdea30x)<0
            #,sif.s30<0
            ,sif.ma5<sif.ma13
            #,strend(sif.ma30)<0
            )


    return signal * godown5.direction
godown5.direction = XSELL
godown5.priority = 2000

def godown30(sif,sopened=None):
    '''
        30分钟最低击穿昨日低点后30分钟内1分钟下叉卖空
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

 
    lowd = sif.lowd - sif.atrd/XBASE/8 #gmin(sif.closed,sif.opend)-sif.atrd/XBASE/8


    xlowd = np.zeros(len(sif.diff1),np.int32)
    xlowd[sif.i_cofd] = lowd

    xlowd = extend(xlowd,260)

    signal = np.zeros_like(sif.diff1)

    signal[sif.i_cof30] = gand(cross(xlowd[sif.i_cof30],sif.low30)<0)

    signal = sfollow(signal,cross(sif.dea1,sif.diff1)<0,30)

    

    signal = gand(signal
            ,strend(sif.ma270)<0
            #,strend(sif.diff30-sif.dea30)<0
            ,strend(sif.sdiff30x-sif.sdea30x)<0            
            ,strend(sif.ma30)<0
            )


    return signal * godown30.direction
godown30.direction = XSELL
godown30.priority = 20000

def ipmacd_long_5(sif,sopened=None):
    trans = sif.transaction

    dsfilter2 = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<2000)

    signal = gand(cross(sif.dea1,sif.diff1)>0
            ,strend2(sif.sdiff30x-sif.sdea30x)>0
            ,sif.sdiff5x>0            
            ,sif.mtrend>0
            )
    signal = gand(signal
            ,sif.ma3 > sif.ma13
            ,strend2(sif.ma13-sif.ma60)>0
            ,strend2(sif.ma30)>0
            ,strend2(sif.ma135)>0
            ,dsfilter2
            )
    return signal * ipmacd_long_5.direction
ipmacd_long_5.direction = XBUY
ipmacd_long_5.priority = 1000

def ipmacd_long_6(sif,sopened=None):
    trans = sif.transaction
    
    s30_13 = np.zeros_like(sif.diff1)
    s30_13[sif.i_cof30] = strend2(ma(sif.close30,13))
    s30_13 = extend2next(s30_13)
    
    signal = cross(sif.dea1,sif.diff1)>0

    signal = gand(signal
              ,sif.ma3>sif.ma13  
              ,sif.s5>0
              ,sif.s30>0
              ,strend(sif.ma30)>0
              ,strend(sif.ma13)>0
              ,strend(sif.ma7-sif.ma30)>0 
              ,sif.mtrend>0
              #,s30_13>0
              #,sif.sdiff5x>0
            )

    return signal * XBUY
ipmacd_long_6.direction = XBUY
ipmacd_long_6.priority = 2430#2430

def ipmacd_long_x(sif,sopened=None):
    trans = sif.transaction
    
    
    signal = cross(sif.dea1,sif.diff1)>0

    signal = gand(signal
              ,sif.ma3>sif.ma13  
              ,sif.ma7> sif.ma30              
              ,sif.ma30>sif.ma135
              ,sif.sdiff5x>0            
              ,strend(sif.sdiff15x-sif.sdea15x)>0
              ,strend(sif.ma30)>0
              ,sif.s30>0
              ,gor(sif.mtrend>0,sif.ltrend>0)
            )

    return signal * ipmacd_long_x.direction
ipmacd_long_x.direction = XBUY
ipmacd_long_x.priority = 1800

def gu30(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    signal = gand(trans[ILOW] > rollx(trans[IHIGH])
            ,trans[ITIME] > 915
        )

    signal = gand(signal
            ,trans[ICLOSE] > rollx(tmax(trans[IHIGH],120))
            )

    signal = gand(signal
            #,strend2(sif.sdiff30x - sif.sdea30x)>0
            ,sif.s30>0
            ,sif.sdiff5x > sif.sdea5x
            ,strend2(sif.ma60)>0
            )

    return signal * gu30.direction
gu30.direction = XBUY
gu30.priority = 500

def ipmacd_long_5k(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤

    sm = sif.ma270 - rollx(sif.ma270)
    ss2 = msum(sm,3)
    sss = strend(ss2)

    sk5,sd5 = skdj(sif.high5,sif.low5,sif.close5)

    signal = gand(cross(sif.sd,sif.sk)>0
            #,strend2(sif.diff1-sif.dea1)>0            
            ,strend2(sif.sdiff3x-sif.sdea3x)>0            
            #,strend2(sif.sdiff5x-sif.sdea5x)>0
            ,strend2(sif.sdiff30x-sif.sdea30x)>0            
            ,sif.mtrend > 0
            )
    signal = gand(signal
            ,sif.ma3 > sif.ma7
            #,strend2(sif.ma13)>0
            ,strend(sif.ma30)>0
            ,strend(sif.ma7-sif.ma30)>0
            ,dsfilter
            )

    #signal = gand(rollx(signal,1),sif.diff1<sif.dea1)
    return signal * ipmacd_long_5k.direction
ipmacd_long_5k.direction = XBUY
ipmacd_long_5k.priority = 1200


def cci_up15(sif,sopened=None):
    '''
        15分钟cci上穿110
        叠加貌似无增强，但除if1005之外也无削弱. 即使是if1005，也只是略微削弱
    '''
    
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)
 

    scci = cci(sif.high15,sif.low15,sif.close15,14)

    signal15 = gand(cross(cached_ints(len(sif.close15),110),scci/BASE)>0
                ,strend2(sif.diff15x-sif.dea15x)>0
                )


    ss = np.zeros_like(sif.close)
    ss[sif.i_cof15] = signal15

    signal = ss
    #fsignal = cross(sif.sd,sif.sk)>0
    #signal = sfollow(signal,fsignal,15)

    signal = gand(signal
            ,strend2(sif.diff1-sif.dea1)>0
            #,strend(sif.ma7)>0
            #,rollx(strend2(sif.sdiff5x-sif.sdea5x),5)<0
            #,strend2(sif.sdiff30x-sif.sdea30x)>0
            ,sif.s30>0
            ,strend2(sif.ma13)>0
            ,sif.ltrend>0
            )

    return signal * cci_up15.direction
cci_up15.direction = XBUY
cci_up15.priority = 2400#900 

def ma2x(sif,sopened=None):
    
    ma5_5 = ma(sif.close15,5)
    ma5_10 = ma(sif.close15,10)
    ma5_20 = ma(sif.close15,20)

    m5x10 = cross(ma5_10,ma5_5)>0
    m5x20 = cross(ma5_20,ma5_5)>0
    m10x20 = cross(ma5_20,ma5_10)>0

    signal30 = sfollow(m5x10,m5x20,2)
    signal30 = sfollow(signal30,m10x20,2)

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof15] = signal30

    fsignal = cross(sif.sd,sif.sk)>0
    signal = sfollow(signal,fsignal,15)

    signal = gand(signal
              ,sif.mtrend>0
              #,strend2(sif.sdiff30x-sif.sdea30x)>0
            )

    return signal * ma2x.direction
ma2x.direction = XBUY
ma2x.priority = 800

def ma1x(sif,sopened=None):
    ''' 只适用于当月合约和远期合约
    '''

    signal = cross(sif.ma60,sif.ma5)>0

    #fsignal = cross(sif.sd,sif.sk)>0
    #signal = sfollow(signal,fsignal,30)

    signal = gand(signal
              ,sif.mtrend>0
              ,sif.ltrend>0 #sif.mtrend
              ,strend2(sif.ma270)>0
              ,sif.s30>0
              #,strend2(sif.sdiff5x-sif.sdea5x)>0              
              #,sif.diff1>0#sif.dea1
            )

    return signal * ma1x.direction
ma1x.direction = XBUY
ma1x.priority = 800

def s5(sif,sopened=None):
    
    ma_a = ma(sif.close5,5)
    ma_b = ma(sif.close5,13)
    ma_c = ma(sif.close5,30)


    signala = gand(cross(ma_b,ma_a)>0
                ,strend2(ma_c)>0
                )

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof5] = signala


    signal = gand(signal
              ,sif.mtrend>0
              #,sif.ltrend>0
              ,strend2(sif.sdiff30x-sif.sdea30x)>0
              ,sif.s10>0
              ,sif.diff1>0
              ,sif.ma5>sif.ma13
              ,strend(sif.ma30)>0
            )

    return signal * s5.direction
s5.direction = XBUY
s5.priority = 1200

def inside_up(sif,sopened=None):
    '''
        内移日次日向上
            
        15分钟高点突破内移日开收盘价的高者后15分钟内1分钟上叉,270线向上
        日ATR的1/10作为突破过滤
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

 
    sday = gand(sif.highd<rollx(sif.highd),sif.lowd>rollx(sif.lowd))
    
    highd = np.select([sday],[gmax(sif.closed,sif.opend)+sif.atrd/XBASE/10],default=0)

    #highd = np.select([sday],[sif.highd],default=0)

    xhighd = np.zeros(len(sif.diff1),np.int32)
    xhighd[sif.i_cofd] = highd

    xhighd = extend(xhighd,260)

    signal = np.zeros_like(sif.diff1)

    signal[sif.i_cof15] = gand(cross(xhighd[sif.i_cof15],sif.high15)>0)

    signal = sfollow(signal,cross(sif.dea1,sif.diff1)>0,15)


    signal = gand(signal
            ,strend(sif.ma270)>0
            ,sif.mtrend>0
            )


    return signal * inside_up.direction
inside_up.direction = XBUY
inside_up.priority = 2000

def br30(sif,sopened=None):
    '''
        5分钟最高突破开盘前30分钟最高之后，下一次1分钟上叉
        属于突破回调的模式
        难以周期化
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)
    
    high30 = np.select([trans[ITIME][sif.i_cof30]==945],[sif.high30],default=0)

    xhigh30,xlow30 = np.zeros_like(sif.diff1),np.zeros_like(sif.diff1)
    xhigh30[sif.i_oof30] = high30

    xhigh30 = extend2next(xhigh30)

    signal = np.zeros_like(sif.diff1)

    signal[sif.i_cof5] = cross(xhigh30[sif.i_cof5],sif.high5)>0

    signal = sfollow(signal,cross(sif.dea1,sif.diff1)>0,15)

    signal = gand(signal
            ,strend(sif.diff30-sif.dea30)>0
            ,strend(sif.diff5-sif.dea5)>0
            ,strend(sif.ma30)>0
            ,sif.ma5>sif.ma13
            ,sif.mtrend>0
            )

    return signal * br30.direction
br30.direction = XBUY
br30.priority = 300

def br75(sif,sopened=None):
    '''
        突破1030前的最高点
        使用iftrade.itrade3y1_25更好
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

 
    xhigh = rollx(tmax(trans[IHIGH],75))
    sxhigh = np.select([gor(trans[ITIME]==1031)],[xhigh],default=0)

    sxhigh = np.select([trans[ITIME]>1030],[extend(sxhigh,180)],default=0)
 
    signal = np.zeros_like(sif.diff1)

    signal[sif.i_cof5] = gand(cross(sxhigh[sif.i_cof5],sif.high5)>0)
    

    signal = gand(signal
            ,strend(sif.ma135)>0
            ,strend2(sif.sdiff30x-sif.sdea30x)>0
            ,strend(sif.ma13-sif.ma60)>0
            ,sif.sdiff5x>0
            ,sif.ma5>sif.ma13
            ,sif.mtrend>0
            )


    return signal * br75.direction
br75.direction = XBUY
br75.priority = 2400

def ipmacd_short_devi1(sif,sopened=None):
    '''
        顶背离操作，去掉了诸多条件
        尤其是xatr<2000
    '''

    trans = sif.transaction

    th = tmax(trans[IHIGH],120)
    th2 = tmax(trans[IHIGH],10)

    signal = gand(hdevi(trans[IHIGH],sif.diff1,sif.dea1)
                ,th2 == th
                )

    fsignal = strend2(sif.diff1-sif.dea1)<0

    signal = sfollow(signal,fsignal,15)

    signal = gand(signal
                ,strend2(sif.sdiff5x)>0
                ,strend(sif.sdiff5x-sif.sdea5x)<0   #diff5在上行，但macd5已经开始向下
                ,strend(sif.sdiff30x)<0
            )
    return signal * ipmacd_short_devi1.direction
ipmacd_short_devi1.direction = XSELL
ipmacd_short_devi1.priority = 400

def ipmacd_long_devi1_o5(sif,sopened=None):
    '''
        底背离操作，使用了diff5
    '''

    trans = sif.transaction

    ksfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤

    msignal = ldevi(trans[ILOW],sif.diff1,sif.dea1)

    signal = gand(msignal
            ,strend(sif.diff1-sif.dea1) >= 3
            ,strend(sif.ma135-sif.ma270)>0
            ,strend(sif.diff5-sif.dea5)>0
            ,ksfilter
            )

    return signal * ipmacd_long_devi1_o5.direction
ipmacd_long_devi1_o5.direction = XBUY
ipmacd_long_devi1_o5.priority = 910

def xud30(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    mxc = xc0s(sif.open30,sif.close30,sif.high30,sif.low30,13) > 0
    signal = np.zeros_like(sif.diff1)
    signal[sif.i_cof30] = mxc

    signal = gand(signal
            ,strend(sif.diff1)>0
            ,strend(sif.ma270)>0
            ,sif.mtrend>0
            ,sif.ltrend<0
            #,dsfilter
            )

    return signal * xud30.direction
xud30.direction = XBUY
xud30.priority = 500
xud30.stop_closer = atr5_uxstop_1_25

def xud30c(sif,sopened=None):
    #xud30和xud30c通常对其他算法集合的叠加作用是一增一减，但是如果两个都一起上，则多数是增。
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    mxc = xc0c(sif.open30,sif.close30,sif.high30,sif.low30,13) > 0
    signal = np.zeros_like(sif.diff1)
    signal[sif.i_cof30] = mxc

    signal = gand(signal
            ,strend(sif.diff1)>0
            ,strend(sif.ma270)>0
            #,sif.s30>0
            ,sif.mtrend>0
            #,dsfilter
            )

    return signal * xud30c.direction
xud30c.direction = XBUY
xud30c.priority = 500
xud30c.stop_closer = atr5_uxstop_1_25

def xud10l(sif,sopened=None):
    su,sd = supdowns(sif.open10,sif.close10,sif.high10,sif.low10)

    msu = cexpma(su,13)
    msd = cexpma(sd,13)

    #msu = ma(su,7)
    #msd = ma(sd,7)


    signal = np.zeros_like(sif.close)
    signal[sif.i_cof10] = msu>msd

    fsignal = cross(sif.sd,sif.sk)>0
    signal = sfollow(signal,fsignal,15)

    signal = gand(signal
            ,sif.s30>0
            ,sif.mtrend>0
            ,sif.ltrend>0
            ,strend2(sif.ma60)>0
            #,sif.ma60 > sif.ma270
            )

    return signal * xud10l.direction
xud10l.direction = XBUY
xud10l.priority = 1601

def xud10s(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    mxc = xc0s(sif.open10,sif.close10,sif.high10,sif.low10,13) < 0
    signal = np.zeros_like(sif.diff1)
    signal[sif.i_cof10] = mxc

    #fsignal = gand(cross(sif.dea1,sif.diff1)<0)

    #signal = sfollow(signal,fsignal,15)

    signal = gand(signal
            ,strend(sif.diff1)<0
            ,sif.sdiff60x<sif.sdea60x
            ,sif.sdiff30x<sif.sdea30x
            ,strend2(sif.sdiff5x-sif.sdea5x)<0
            #,sif.ma5<sif.ma13
            ,strend(sif.ma270)<0
            ,sif.mtrend<0
            ,ksfilter
            )

    return signal * xud10s.direction
xud10s.direction = XSELL
xud10s.priority = 3100


def xud15(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)


    su,sd = supdowns(sif.open15,sif.close15,sif.high15,sif.low15)

    msu = cexpma(su,13)
    msd = cexpma(sd,13)

    sf = np.zeros_like(sif.diff1)
    sf[sif.i_cof15] = msu>msd


    signal = cross(sif.dea1,sif.diff1)>0


    signal = gand(signal
            ,sf
            ,sif.diff1>0
            ,sif.mtrend>0
            #,sif.ma5>sif.ma13
            #,dsfilter
            )


    return signal * xud15.direction
xud15.direction = XBUY
xud15.priority = 3001

def ipmacd_short5(sif,sopened=None):#-
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)
    
    signal = gand(cross(sif.dea5,sif.diff5)<0
            ,sif.diff5>0
            ,sif.diff30<0
            ,strend(sif.diff30-sif.dea30)<0
            )
    signal = gand(signal
            ,strend(sif.ma13-sif.ma60)<0
            #,strend(sif.ma30)<-4
            ,strend(sif.ma135-sif.ma270)<0
            ,ksfilter
            )   
    return signal * ipmacd_short5.direction
ipmacd_short5.direction = XSELL
ipmacd_short5.priority = 550

def ma30_short(sif,sopened=None):
    ''' 下行中下叉30线
    '''
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)

    sf = msum(trans[IHIGH]>sif.ma30,5) < 3

    signal = gand(cross(sif.ma30,trans[IHIGH])<0
            ,strend(sif.ma30)<0
            ,sf
            )
    fsignal = gand(cross(sif.dea1,sif.diff1)<0
            ,sif.diff1<0
            ,sif.sdiff5x<0
            ,strend2(sif.sdiff30x-sif.sdea30x)<0
            ,strend(sif.ma13-sif.ma60)<0
            ,sif.ma5<sif.ma13
            ,ksfilter
            )
    signal = sfollow(signal,fsignal,10)
    return signal * ma30_short.direction
ma30_short.direction = XSELL
ma30_short.priority = 2400


def ma60_short(sif,sopened=None):
    ''' ma60拐头
    '''
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)
 
    msignal = gand(strend(sif.ma60) == -1
                )
    fsignal = gand(cross(sif.dea1,sif.diff1)<0
                ,sif.sdiff30x<0
                ,strend2(sif.sdiff5x-sif.sdea5x)>0
                ,strend(sif.ma5-sif.ma30)<0
                ,ksfilter                
                )
    signal = sfollow(msignal,fsignal,5)
    return signal * ma60_short.direction
ma60_short.direction = XSELL
ma60_short.priority = 2401

def down01(sif,sopened=None): #++
    ''' 
        30分钟<0且下行
        5分钟>0且下行
    '''
    trans = sif.transaction
    ksfilter= gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)#  向下突变过滤

    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1)<0
            ,sif.sdiff5x>0
            ,sif.sdiff30x<0
            ,strend(sif.diff1-sif.dea1)<-2            
            ,strend(sif.ma5-sif.ma30)<0
            ,strend(sif.ma135-sif.ma270)<0            
            ,strend(sif.ma30)<0
            ,sif.ltrend<0
            ,ksfilter
            )
    return signal * down01.direction
down01.direction = XSELL
down01.priority = 250

def up0(sif,sopened=None):
    '''
        难以周期化
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤

    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1)>0
            ,sif.diff5<0
            ,strend(sif.diff30-sif.dea30)>1
            ,strend(sif.diff5-sif.dea5)>1
            ,strend(sif.diff1-sif.dea1)>1
            ,strend(sif.diff1)>4
            ,strend(sif.ma5-sif.ma30)>0
            ,strend(sif.ma135-sif.ma270)>0
            ,strend(sif.ma30)>0
            #,sif.mtrend>0
            ,dsfilter
            )

    return signal * up0.direction
up0.direction = XBUY
up0.priority = 500  #叠加时，远期互有盈亏

def ipmacd_longt(sif,sopened=None):#+
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500) #向上突变过滤

    signal = gand(cross(sif.dea1,sif.diff1)>0
                ,strend(sif.diff5-sif.dea5)>0
                ,sif.diff30<sif.dea30
                #,strend(sif.diff30-sif.dea30)>0 #+
                ,sif.ma5>sif.ma13
                ,strend(sif.ma5)>2 #
                ,gor(strend(sif.ma270)>0,strend(sif.ma135)>0)
                ,dsfilter
                )
    return signal * ipmacd_longt.direction
ipmacd_longt.direction= XBUY
ipmacd_longt.priority = 2000

def gapdown15(sif,sopened=None):
    '''
        向上跳开后，15分钟补缺
        一次补失败后还可以补第二次
    '''


    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)
    
    high30 = np.select([trans[ITIME][sif.i_cof30]==945],[sif.high30],default=0)

    xhighd,xlowd = np.zeros_like(sif.diff1),np.zeros_like(sif.diff1)
    xhighd[sif.i_cofd] = sif.highd

    xhighd = extend2next(xhighd)

    hgap = gand(trans[ILOW]>xhighd,trans[ITIME]==915)


    hgap = scover(hgap,260)   #当日信号都在缺口内发出

    signal = np.zeros_like(sif.diff1)

    signal[sif.i_cof15] = gand(cross(xhighd[sif.i_cof15],sif.low15)<0
                            ,hgap[sif.i_cof15]
                            )

    signal = gand(signal
                ,sif.mtrend>0
                )

    return signal * gapdown15.direction
gapdown15.direction = XSELL
gapdown15.priority = 2600





#K线形态
def k5_lastup(sif,sopened=None):
    '''
        底部衰竭模式
        5分钟底部阴线后出现孕线，后10分钟内1分钟最高线突破该孕线(high+close)/2
        效果不佳，稳定性不好
        很难取舍，虽然稳定性不好，但叠加效果好
    '''
    trans = sif.transaction
 
    ma5_500 = ma(sif.close5,500)
    ma5_200 = ma(sif.close5,200)
    ma5_60 = ma(sif.close5,60) 
    ma5_13 = ma(sif.close5,13)     
    ma5_30 = ma(sif.close5,30) 
    ma5_7 = ma(sif.close5,7)         
    ma5_3 = ma(sif.close5,3)         
    
    signal5 = gand(sif.high5<rollx(sif.high5)
                ,sif.low5>rollx(sif.low5)
                ,rollx(sif.low5) == tmin(sif.low5,20)
                ,rollx(sif.vol5) > sif.vol5
                ,rollx(sif.vol5) > rollx(sif.vol5,2)
                ,rollx(sif.close5)<rollx(sif.open5)
                ,strend2(ma5_60)<-20
                )

    delay = 10

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof5] = signal5
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof5] = (sif.high5 + sif.close5)/2
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)
    
    #fsignal = cross(bline,sif.high)>0
    fsignal = sif.high > bline

    #signal = np.zeros_like(sif.close)
    #signal[sif.i_cof5] = signal5

    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            ,strend(sif.ma7)>0
            ,rollx(strend2(sif.sdiff5x-sif.sdea5x),5)<0
            #,sif.ltrend>0
            )
    signal = derepeatc(signal)

    return signal * k5_lastup.direction
k5_lastup.direction = XBUY
k5_lastup.priority = 900

def k15_lastdown(sif,sopened=None):
    '''
        新高衰竭模式
        1. 15分钟新高后,15分钟内1分钟跌破前15分钟的开盘价(收盘价的低者)/最低价
    '''
    
    trans = sif.transaction

    ma15_500 = ma(sif.close15,500)
    ma15_200 = ma(sif.close15,200)
    ma15_60 = ma(sif.close15,60) 
    ma15_13 = ma(sif.close15,13)     
    ma15_30 = ma(sif.close15,30) 
    ma15_7 = ma(sif.close15,7)         
    ma15_3 = ma(sif.close15,3)         
    
    signal15 = gand(sif.high15>rollx(sif.high15)
                ,sif.low15>rollx(sif.low15)
                ,sif.high15 - gmax(sif.open15,sif.close15) > np.abs(sif.open15-sif.close15) #上影线长于实体
                ,sif.high15 == tmax(sif.high15,5)
                #,sif.high15 > gmax(ma15_3,ma15_30,ma15_60)
                #,rollx(sif.vol5) > sif.vol5
                #,rollx(sif.vol5) > rollx(sif.vol5,2)
                #,rollx(sif.close5)<rollx(sif.open5)
                ,strend2(ma15_60)>0
                ,strend2(sif.diff15x-sif.dea15x)>0
                #,sif.diff15x>sif.dea15x
                #,strend2(ma15_7)>0                                
                #,ma15_7 > ma15_13
                #,strend2(ma15_500)>0
                )

    #print np.nonzero(signal15)
    delay = 15

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof15] = signal15
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof15] = gmin(sif.open15,sif.close15)
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)
    
    #fsignal = cross(bline,sif.high)>0
    fsignal = sif.close < bline


    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            #,strend2(sif.diff1-sif.dea1)<0
            #,strend(sif.ma7)>0
            #,rollx(strend2(sif.sdiff5x-sif.sdea5x),5)<0
            )
    signal = derepeatc(signal)

    return signal * k15_lastdown.direction
k15_lastdown.direction = XSELL
k15_lastdown.priority = 2100 #对i09时200即优先级最高的效果最好
k15_lastdown.stop_closer = atr5_uxstop_05_25

def k3_lastdown(sif,sopened=None):
    '''
        新高衰竭模式
        1. 3分钟长上影新高后,5分钟内1分钟跌破前5分钟的最低价
    '''
    
    trans = sif.transaction

    ma3_500 = ma(sif.close3,500)
    ma3_200 = ma(sif.close3,200)
    ma3_60 = ma(sif.close3,60) 
    ma3_13 = ma(sif.close3,13)     
    ma3_30 = ma(sif.close3,30) 
    ma3_7 = ma(sif.close3,7)         
    ma3_3 = ma(sif.close3,3)         
    
    signal3 = gand(sif.high3>rollx(tmax(sif.high3,30))
                ,sif.close3>rollx(sif.close3)
                ,sif.low3>rollx(sif.low3)
                ,sif.high3 - gmax(sif.open3,sif.close3) > np.abs(sif.open3-sif.close3) #上影线长于实体
                #,strend2(ma3_60)<0
                )

    #print np.nonzero(signal3)
    delay = 60

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof3] = signal3
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof3] = sif.close3 #gmin(sif.open5,sif.close5)
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)
    
    #fsignal = cross(bline,sif.high)>0
    #fsignal = sif.high < bline
    fsignal = sif.close < bline    


    #signal = sfollow(ss,fsignal,delay)
    signal = fsignal
    signal = gand(signal
            ,strend2(sif.diff1-sif.dea1)<0
            ,sif.ma3<sif.ma13
            ,strend2(sif.sdiff5x-sif.sdea5x)<0
            #,strend2(sif.sdiff3x-sif.sdea3x)<0
            ,strend2(sif.ma270)<0
            ,strend2(sif.sdiff30x-sif.sdea30x)<0
            )
    signal = derepeatc(signal)

    return signal * k3_lastdown.direction
k3_lastdown.direction = XSELL
k3_lastdown.priority = 1600 #对i09时200即优先级最高的效果最好


def k5_lastdown(sif,sopened=None):
    '''
        新高衰竭模式
        1. 5分钟长上影新高后,5分钟内1分钟跌破前5分钟的最低价
    '''
    
    trans = sif.transaction

    ma5_500 = ma(sif.close5,500)
    ma5_200 = ma(sif.close5,200)
    ma5_60 = ma(sif.close5,60) 
    ma5_13 = ma(sif.close5,13)     
    ma5_30 = ma(sif.close5,30) 
    ma5_7 = ma(sif.close5,7)         
    ma5_3 = ma(sif.close5,3)         
    
    signal5 = gand(sif.high5>rollx(tmax(sif.high5,15))
                ,sif.close5>rollx(sif.close5)
                #,sif.low5>rollx(sif.low5)
                ,sif.high5 - gmax(sif.open5,sif.close5) > np.abs(sif.open5-sif.close5) #上影线长于实体
                #,np.abs(sif.open5-sif.close5) > gmin(sif.open5,sif.close5) - sif.low5#上影线长于实体
                #,sif.high5 > gmax(ma5_3,ma5_30,ma5_60)
                #,rollx(sif.vol5) > sif.vol5
                #,rollx(sif.vol5) > rollx(sif.vol5,2)
                #,rollx(sif.close5)>rollx(sif.open5)
                #,strend2(ma5_60)>0
                #,strend2(sif.diff5x-sif.dea5x)>0
                #,sif.diff5x>sif.dea5x
                #,strend2(ma5_500)<0                                
                #,ma5_7 > ma5_13
                #,strend2(ma5_500)>0
                )

    #print np.nonzero(signal5)
    delay = 30

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof5] = signal5
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof5] = sif.low5 #gmin(sif.open5,sif.close5)
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)
    
    #fsignal = cross(bline,sif.high)>0
    #fsignal = sif.high < bline
    fsignal = sif.close < bline    


    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            ,strend2(sif.diff1-sif.dea1)<0
            ,sif.ma5<sif.ma13
            ,strend2(sif.sdiff5x-sif.sdea5x)<0
            ,strend2(sif.ma270)<0
            #,strend2(sif.sdiff30x-sif.sdea30x)<0
            #,gor(sif.sdiff30x-sif.sdea30x<0,strend2(sif.sdiff30x-sif.sdea30x)<0)
            #,strend(sif.ma7)<0
            #,rollx(strend2(sif.sdiff5x-sif.sdea5x),5)<0
            )
    signal = derepeatc(signal)
    return signal * k5_lastdown.direction
k5_lastdown.direction = XSELL
k5_lastdown.priority = 2400 #对i09时200即优先级最高的效果最好
#k5_lastdown.stop_closer = atr5_uxstop_05_25

def k5_relay(sif,sopened=None):
    '''
        中继模式 用于解决隔日连续上升的问题
        5分钟阳线新高后，阴线盘整，但未突破阳线开盘
        后60分钟内突破新高日收盘/盘整日开盘的高点


        对i07效果很差，其它很好
        但是叠加的效果不佳，是副作用
    '''
    
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)
 

    ma5_500 = ma(sif.close5,500)
    ma5_200 = ma(sif.close5,200)
    ma5_60 = ma(sif.close5,60) 
    ma5_13 = ma(sif.close5,13)     
    ma5_30 = ma(sif.close5,30) 
    ma5_7 = ma(sif.close5,7)         
    ma5_3 = ma(sif.close5,3)         
    
    signal5 = gand(sif.close5<rollx(sif.close5)
                ,sif.low5>rollx(sif.low5)
                ,rollx(sif.close5)>rollx(sif.open5)
                #,np.abs(sif.open5-sif.close5) > gmax(sif.open5,sif.close5)-sif.low5  #实体长于下影线
                ,rollx(sif.high5) == tmax(sif.high5,10)
                ,strend2(ma5_30)>0
                #,sif.diff5x-sif.dea5x>0
                )

    #print np.nonzero(signal5)
    delay = 15

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof5] = signal5
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof5] = gmax(sif.open5,rollx(sif.close5),sif.high5)#,rollx(sif.high5))
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)
    #print bline[-200:]
    
    #fsignal = cross(bline,sif.high)>0
    fsignal = sif.low > bline

    signal = ss
    signal = sfollow(signal,fsignal,delay)
    signal = gand(signal
            #,strend2(sif.diff1-sif.dea1)<0
            #,strend(sif.ma7)>0
            #,rollx(strend2(sif.sdiff5x-sif.sdea5x),5)<0
            )

    signal = derepeatc(signal)
    return signal * k5_relay.direction
k5_relay.direction = XBUY
k5_relay.priority = 12400 #对i07效果很差

def k15_relay(sif,sopened=None):
    '''
        两阳夹一阴
    '''
    
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)
 
    signal5 = gand(sif.close15>rollx(sif.open15)
                ,sif.close15 > sif.open15 #
                ,rollx(sif.close15)<rollx(sif.open15)
                ,rollx(sif.close15) < rollx(sif.close15,2)
                ,rollx(sif.close15) > rollx(sif.open15,2) + (rollx(sif.close15,2)-rollx(sif.open15,2))/3
                ,rollx(sif.low15) > rollx(sif.low15,2)
                ,rollx(sif.close15,2)>rollx(sif.open15,2)
                ,rollx(sif.close15,2)>rollx(tmax(sif.close15,15),3)
                )

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof15] = signal5
    signal = gand(signal
            ,strend2(sif.sdiff30x-sif.sdea30x)>0
            ,sif.diff1>0
            ,sif.sdiff5x>0
            ,sif.mtrend>0
            ,sif.ltrend>0            
            #,strend(sif.ma7)>0
            #,rollx(strend2(sif.sdiff5x-sif.sdea5x),5)>0
            )

    return signal * k5_relay.direction
k15_relay.direction = XBUY
k15_relay.priority = 1200 #对i07效果很差

def goup5(sif,sopened=None):
    ''' 
        5分钟冲击昨日高点时买入, 过滤器向下浮动. 即不论是否突破，都介入
        使用iftrade.itrade3y05_25c(即最小止损6)效果更好
    ''' 
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

 
    highd = sif.highd #- sif.atrd/XBASE/8 #gmax(sif.closed,sif.opend)+sif.atrd/XBASE/10


    xhighd = np.zeros(len(sif.diff1),np.int32)
    xhighd[sif.i_cofd] = highd

    xhighd = extend(xhighd,260)

    signal = np.zeros_like(sif.diff1)

    signal[sif.i_cof5] = gand(cross(xhighd[sif.i_cof5],sif.close5)>0)

    #signal = sfollow(signal,cross(sif.dea1,sif.diff1)>0,30)

    signal = gand(signal
            ,sif.ma5>sif.ma13
            ,strend(sif.sdiff30x-sif.sdea30x)>0
            #,strend(sif.ma30)>0
            ,strend(sif.ma60)>0
            ,strend(sif.ma270)>0
            ,strend(sif.ma13-sif.ma60)>0
            )


    return signal * goup5.direction
goup5.direction = XBUY
goup5.priority = 1500


def opendown(sif,sopened=None):
    '''
        与945无关
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)


    xopend = np.zeros_like(sif.close)

    xopend[sif.i_oofd] = sif.opend
    xopend = extend2next(xopend)

    x945 = np.select([sif.time==945],[sif.close-xopend],0)
    x945 = extend2next(x945)

    xlow = rollx(tmin(sif.low,15),1)

    signal = gand(cross(xopend,sif.close)<0
                #,x945 < 0
                ,sif.low<xlow
                )

    #signal = sfollow(signal,strend(sif.diff1-sif.dea1)==1,15)

    signal = gand(signal
            ,strend(sif.sdiff5x-sif.sdea5x)<0            
            ,sif.diff1 > 0
            ,sif.sdiff30x<0
            ,sif.ltrend<0
            )

    return signal * opendown.direction
opendown.direction = XSELL
opendown.priority = 1000


def openup(sif,sopened=None):
    '''
        突破开盘价
        要点是945的收盘价大于开盘价
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)


    xopend = np.zeros_like(sif.close)

    xopend[sif.i_oofd] = sif.opend
    xopend = extend2next(xopend)

    x945 = np.select([sif.time==945],[sif.close-xopend],0)
    x945 = extend2next(x945)

    xhigh = rollx(tmax(sif.high,60),1)


    signal = gand(cross(xopend,sif.high)>0
                ,x945 > 0
                ,sif.high>xhigh
                )

    #signal = sfollow(signal,strend(sif.diff1-sif.dea1)==1,15)


    signal = gand(signal
            ,strend(sif.diff1-sif.dea1)>0
            ,strend(sif.sdiff5x-sif.sdea5x)>0            
            ,strend(sif.sdiff30x-sif.sdea30x)>0
            ,sif.diff1 > 0
            ,sif.ltrend>0
            #,sif.sdiff5x < sif.sdea5x
            )

    return signal * openup.direction
openup.direction = XBUY
openup.priority = 1000




def xdown30(sif,sopened=None):
    '''
        30分钟的稳定下挫
        5分钟内各最低价都低于30分钟前的最低价, 后macd下叉
    '''
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)
 
    covered = 30

    snewlow = sif.low < rollx(sif.low,covered)

    msnl = msum2(snewlow,5)

    #signal = gand(msnl>4)   #最大值就是5
    signal = equals(msnl,5)

    s30_13 = np.zeros_like(sif.diff1)
    s30_13[sif.i_cof30] = strend2(ma(sif.close30,13))
    s30_13 = extend2next(s30_13)

    rsi7 = rsi2(sif.close,7)
    rsi14 = rsi2(sif.close,14)

    #fsignal = cross(rsi14,rsi7)<0
    fsignal = cross(sif.dea1,sif.diff1)<0
    #fsignal = cross(sif.sd,sif.sk)<0   

    signal = sfollow(signal,fsignal,5)

    signal = gand(signal
            ,s30_13<0
            ,sif.ma5 < sif.ma13
            #,sif.low > rollx(sif.low,4) #还在下行,这个限制太大了，极大消灭了统计样本
            #,strend2(sif.diff1-sif.dea1)<0
            ,sif.diff5<0
            ,strend2(sif.ma270)<0
            #,strend2(sif.ma30)<0
            #,strend2(sif.ma13)<0            
            ,strend2(sif.sdiff30x-sif.sdea30x)<0
            ,sif.ltrend<0
            ,ksfilter
            )
    
    return signal * xdown30.direction
xdown30.direction = XSELL
xdown30.priority = 900

def xdown60(sif,sopened=None):
    '''
        连续5分钟内出现60分钟最低点4个以上
    '''
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    covered = 60

    snewlow = sif.low < rollx(tmin(sif.low,covered))

    msnl = msum2(snewlow,5)

    signal = gand(msnl>3)

    s30_13 = np.zeros_like(sif.diff1)
    s30_13[sif.i_cof30] = strend2(ma(sif.close30,13))
    s30_13 = extend2next(s30_13)


    signal = gand(signal
            ,s30_13<0
            ,sif.ma5 < sif.ma13
            ,strend2(sif.diff1-sif.dea1)<0
            #,sif.diff5<0
            ,strend2(sif.ma270)<0
            #,strend2(sif.ma30)<0
            #,strend2(sif.ma13)<0            
            ,strend2(sif.sdiff5x-sif.sdea5x)<0
            ,strend2(sif.sdiff15x-sif.sdea15x)<0
            ,sif.ltrend<0
            ,ksfilter
            )
    
    return signal * xdown60.direction
xdown60.direction = XSELL
xdown60.priority = 1200 

def skdj_bup(sif,sopened=None):
    '''
        底部抬高
    '''

    trans = sif.transaction

    hh = hpeak(sif.high,sif.sk,sif.sd)
    ll = lpeak(sif.low,sif.sk,sif.sd)

    ihh = np.nonzero(hh)[0]
    ill = np.nonzero(ll)[0]
    
    sh = np.zeros_like(sif.close)
    sl = np.zeros_like(sif.close)
    sl3 = np.zeros_like(sif.close)

    sh[ihh] = strend2(hh[ihh])
    sl[ill] = strend2(ll[ill])
    sl3[ill] = rollx(strend2(ll[ill]),3)

    sh = extend2next(sh)
    sl = extend2next(sl)
    sl3 = extend2next(sl3)

    signal = gand(sh>1,
                  sl==3,
                  sl3 < -2
                  )

    fsignal= gand(cross(sif.sd,sif.sk)>0
                ,sl>0
                )
    signal = sfollow(signal,fsignal,10)

    signal = gand(signal
                ,sif.diff1>sif.dea1
                ,sif.sdiff5x>sif.sdea5x
                ,sif.ma3>sif.ma7
                ,strend(sif.ma13)>0
                ,strend(sif.ma30)>0
                #,strend(sif.ma13-sif.ma60)>0   
                #,strend(sif.diff1-sif.dea1)>0
                #,strend2(sif.sdiff5x)>0
                #,strend(sif.sdiff5x-sif.sdea5x)>0   
                #,strend(sif.sdiff30x-sif.sdea30x)>0
            )
    return signal * skdj_bup.direction

skdj_bup.direction = XBUY
skdj_bup.priority = 2400



xshort = [ipmacd_short_5,ipmacd_short_x,gd30,godown5,godown30,ipmacd_short_devi1
        ,ipmacd_short5
        ,down01
        ,k15_lastdown,k5_lastdown,k3_lastdown,k15_relay
        ,opendown        
        ,xdown60#,xdown30
        ]
#xshort = [ipmacd_short_5,ipmacd_short_6a,ipmacd_short_x,ipmacd_short_x2]#,gd30,godown5]
xlong = [ipmacd_long_5,ipmacd_long_x,ipmacd_long_6
        ,gu30 #,br75
        ,ipmacd_long_5k,cci_up15,ma2x,ma1x,s5,inside_up,br30,ipmacd_long_devi1_o5
        ,xud30,xud30c,xud10s#,xud10l
        ,up0#
        ,ipmacd_longt
        ,k5_lastup
        ,skdj_bup #,goup5
        ,openup
        
        ]


xxx = xshort + xlong
