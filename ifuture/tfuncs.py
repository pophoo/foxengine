# -*- coding: utf-8 -*-

'''

主力合约、次月合约与半年合约的成交量还可以，下季合约严重没量，被操控
但因为次月合约开张日晚，如if1007在0524才开张，所以测试不准




'''


from wolfox.fengine.ifuture.ibase import *
from wolfox.fengine.ifuture.ifuncs import fmacd1_long,fmacd1_short
from wolfox.fengine.ifuture.iftrade import delay_filter,atr5_uxstop_1_25,atr5_uxstop_08_25,atr5_uxstop_05_25


ama1 = ama_maker()
ama2 = ama_maker(covered=30,dfast=6,dslow=100)



#TODO
# 5分钟的180周期线上行途中被穿越，或向上移动3点穿越
#       实际上等于15分钟的60周期线
#创本日新低后回跳，前高-高点>高点-低点



def s1(sif,sopened=None):
    trans = sif.transaction
    signal = gand(cross(sif.dea1,sif.diff1)<0)
    #md = sif.diff1-sif.dea1
    #signal = gand(md<rollx(md))#,rollx(md)>rollx(md,2))
    return signal * XSELL

def s90(sif,sopened=None):
    trans = sif.transaction
    signal = gand(cross(sif.ma90,sif.low)<0
                ,sif.ma60>sif.ma90
                ,sif.ma30>sif.ma90
                )
    return signal * XSELL

def s3(sif,sopened=None):
    
    ma_a = ma(sif.close5,5)
    ma_b = ma(sif.close5,13)
    ma_c = ma(sif.close5,30)


    signal = cross(sif.dea1,sif.diff1)>0

    signal = gand(signal
              ,sif.mtrend>0
              ,sif.ltrend>0
              ,strend2(sif.sdiff30x-sif.sdea30x)>0
            )

    return signal * s3.direction
s3.direction = XBUY
s3.priority = 1200


def tfunc(sif,sopened=None):
    '''
    '''

    signalx = gand(hdevi(sif.high30,sif.diff30x,sif.dea30x)
                )

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof30] = signalx


    fsignalx = cross(sif.dea3x,sif.diff3x)<0
    fsignal = np.zeros_like(sif.close)
    fsignal[sif.i_cof3] = fsignalx

    signal = sfollow(signal,fsignal,240)

    signal = gand(signal
            ,sif.mm<0
            )
    
    return signal * tfunc.direction
tfunc.direction = XSELL
tfunc.priority = 2400
#tfunc.closer = lambda c:[s1] #lambda c:c+[s3]


def devi30x3(sif,sopened=None):
    ''' 30分钟顶背离后3分钟下叉
    '''

    signalx = gand(hdevi(sif.high30,sif.diff30x,sif.dea30x)
                )

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof30] = signalx


    fsignalx = cross(sif.dea3x,sif.diff3x)<0
    fsignal = np.zeros_like(sif.close)
    fsignal[sif.i_cof3] = fsignalx

    signal = sfollow(signal,fsignal,240)

    signal = gand(signal
            ,sif.mm<0
            )
    
    return signal * devi30x3.direction
devi30x3.direction = XSELL
devi30x3.priority = 900


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
            ,sif.ma5 < sif.ma13
            ,strend2(sif.diff1-sif.dea1)<0
            ,strend2(sif.ma270)<0
            ,strend2(sif.sdiff5x-sif.sdea5x)<0
            ,strend2(sif.sdiff15x-sif.sdea15x)<0
            ,sif.mtrend<0            
            ,sif.ltrend<0
            ,ksfilter
            )
    
    return signal * xdown60.direction
xdown60.direction = XSELL
xdown60.priority = 2410 

def xup60(sif,sopened=None):
    '''
        连续5分钟内出现60分钟最低点4个以上
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    
    covered = 60

    snewhigh = sif.high > rollx(tmax(sif.high,covered))

    msnl = msum2(snewhigh,5)

    signal = gand(msnl>3)

    s30_13 = np.zeros_like(sif.diff1)
    s30_13[sif.i_cof30] = strend2(ma(sif.close30,13))
    s30_13 = extend2next(s30_13)


    signal = gand(signal
            ,s30_13>0
            ,sif.ma5 > sif.ma13
            #,strend2(sif.diff1-sif.dea1)>0
            #,sif.diff5<0
            ,strend2(sif.ma270)>0
            #,strend2(sif.ma30)<0
            #,strend2(sif.ma13)<0            
            #,strend2(sif.sdiff5x-sif.sdea5x)>0
            #,strend2(sif.sdiff15x-sif.sdea15x)>0
            ,dsfilter
            )
    
    return signal * xup60.direction
xup60.direction = XBUY
xup60.priority = 1200 

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


def xup30(sif,sopened=None):
    '''
        30分钟的稳定下挫
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
 
    covered = 30

    snewlow = sif.high > rollx(sif.high,covered)

    msnl = msum2(snewlow,5)

    #signal = gand(msnl>4)   #最大值就是5
    signal = equals(msnl,5)

    s30_13 = np.zeros_like(sif.diff1)
    s30_13[sif.i_cof30] = strend2(ma(sif.close30,13))
    s30_13 = extend2next(s30_13)


    #fsignal = cross(rsi14,rsi7)>0
    fsignal = cross(sif.dea1,sif.diff1)>0
    #fsignal = cross(sif.sd,sif.sk)>0   

    signal = sfollow(signal,fsignal,5)


    signal = gand(signal
            ,s30_13>0
            ,sif.ma5 > sif.ma13
            #,strend2(sif.diff1-sif.dea1)<0
            #,sif.diff5>0
            ,strend2(sif.ma270)>0
            #,strend2(sif.ma60)>0
            ,strend2(sif.ma30)>0
            ,strend2(sif.sdiff30x-sif.sdea30x)>0
            ,sif.sdiff5x>0
            )
    
    return signal * xup30.direction
xup30.direction = XBUY
xup30.priority = 900


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
            ,sif.s30>0
            ,strend2(sif.ma13)>0
            ,sif.rs_trend>0
            ,sif.rm_trend>0            
            ,sif.mm>0
            )

    return signal * cci_up15.direction
cci_up15.direction = XBUY
cci_up15.priority = 1900 



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
            ,strend2(sif.diff1-sif.dea1)>0
            ,strend(sif.ma7)>0
            ,rollx(strend2(sif.sdiff5x-sif.sdea5x),5)>0
            )

    return signal * k5_relay.direction
k5_relay.direction = XBUY
k5_relay.priority = 2400 #对i07效果很差
#tfunc.closer = lambda c:[s1] #lambda c:c+[s3]

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
            ,sif.s30>0#strend2(sif.sdiff30x-sif.sdea30x)>0
            ,sif.diff1>0
            ,sif.sdiff5x>0
            ,sif.mtrend>0
            ,sif.ltrend>0            
            #,strend(sif.ma7)>0
            #,rollx(strend2(sif.sdiff5x-sif.sdea5x),5)>0
            )

    return signal * k5_relay.direction
k15_relay.direction = XBUY
k15_relay.priority = 1800 

def k15_lastdownb(sif,sopened=None):
    '''
        新高衰竭模式
        15分钟新高后,15分钟内1分钟跌破前15分钟的开盘价(收盘价的低者)/最低价
        15分钟判断是连续的，而不是离散的
    '''
    
    trans = sif.transaction

    
    length = 15
    sopen = rollx(sif.open,length-1)
    sclose = sif.close
    shigh = tmax(sif.high,length-1)
    slow = tmin(sif.low,length-1)
    svol = msum2(sif.vol,length)

    ssignal = gand(shigh> rollx(shigh,length)
                ,slow>rollx(slow,length)
                ,shigh - gmax(sopen,sclose) > np.abs(sopen-sclose) #上影线长于实体
                ,shigh == tmax(shigh,length*5)
                #,sif.t3<0
                ,sif.s3<0
                ,sif.s15>0
                ,svol < rollx(svol,length)
                #,strend2(sif.ma30-sif.ma135)>0
                )

    #print np.nonzero(signal15)
    delay = 15

    ssh = gmin(sopen,sclose)
    bline = np.select([ssignal>0],[ssh],0)
    bline = extend(bline,delay)
    
    #fsignal = cross(bline,sif.high)>0
    fsignal = sif.close < bline


    signal = sfollow(ssignal,fsignal,delay)
    #signal = ssignal
    signal = gand(signal
            #,strend2(sif.ma13)<0
            ,strend2(sif.diff1-sif.dea1)<0
            #,rollx(strend2(sif.sdiff5x-sif.sdea5x),5)<0
            )
    signal = derepeatc(signal)

    return signal * k15_lastdownb.direction
k15_lastdownb.direction = XSELL
k15_lastdownb.priority = 2100 #对i09时200即优先级最高的效果最好
#k15_lastdown.stop_closer = atr5_uxstop_05_25

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
            #,strend2(sif.diff1-sif.dea1)<0
            #,sif.ma5<sif.ma13
            #,strend2(sif.sdiff5x-sif.sdea5x)<0
            #,strend2(sif.ma270)<0
            #,sif.rm_trend>0 #
            
            #,strend2(sif.sdiff30x-sif.sdea30x)<0
            #,gor(sif.sdiff30x-sif.sdea30x<0,strend2(sif.sdiff30x-sif.sdea30x)<0)
            #,strend(sif.ma7)<0
            #,rollx(strend2(sif.sdiff5x-sif.sdea5x),5)<0
            )
    signal = derepeatc(signal)
    return signal * k5_lastdown.direction
k5_lastdown.direction = XSELL
k5_lastdown.priority = 2400 
#k5_lastdown.stop_closer = atr5_uxstop_05_25


def k5_lastdown2(sif,sopened=None):
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
    
    signal5 = gand(sif.high5>rollx(tmax(sif.high5,10))
                #,sif.close5>rollx(sif.close5)
                #,sif.low5>rollx(sif.low5)
                ,sif.high5 - gmax(sif.open5,sif.close5) > np.abs(sif.open5-sif.close5)*2/3 #上影线长于实体的2/3
                #,np.abs(sif.open5-sif.close5) > gmin(sif.open5,sif.close5) - sif.low5#上影线长于实体
                #,sif.high5 - gmax(sif.open5,sif.close5) > gmin(sif.open5,sif.close5) - sif.low5#上影线长于实体
                )

    #print np.nonzero(signal5)
    delay = 20

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
            ,sif.s1<0
            ,strend2(sif.ma270)<0
            ,strend2(sif.ma13)<0
            ,sif.s5<0
            ,sif.rm_trend>0 #
            )
    signal = derepeatc(signal)
    return signal * k5_lastdown2.direction
k5_lastdown2.direction = XSELL
k5_lastdown2.priority = 2400 #对i09时200即优先级最高的效果最好
#k5_lastdown2.stop_closer = atr5_uxstop_05_25


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
                ,sif.high15 > gmax(ma15_3,ma15_30,ma15_60)
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

def x5_lastdown(sif,sopened=None):
    '''
        新高衰竭模式
        1. 3分钟长上影新高后,5分钟内1分钟跌破前5分钟的最低价
    '''
    
    trans = sif.transaction

    ma5_60 = ma(sif.close5,60)

    xsignal = gand(cross(ma5_60,sif.close5)<0
                ,sif.close5 < sif.open5
                ,strend2(ma5_60)<0
                )

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof5] = xsignal

    #fsignal = cross(sif.sd,sif.sk)<0
    #signal = sfollow(signal,fsignal,15)
    signal = gand(signal
            ,strend2(sif.diff1-sif.dea1)<0
            ,sif.ma3<sif.ma13
            ,strend2(sif.sdiff5x-sif.sdea5x)<0
            #,strend2(sif.sdiff3x-sif.sdea3x)<0
            #,strend2(sif.ma270)<0
            #,strend2(sif.sdiff30x-sif.sdea30x)<0
            )

    return signal * x5_lastdown.direction
x5_lastdown.direction = XSELL
x5_lastdown.priority = 1600 #对i09时200即优先级最高的效果最好


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
            ,strend2(sif.ma270)<0
            ,strend2(sif.sdiff30x-sif.sdea30x)<0
            )
    signal = derepeatc(signal)

    return signal * k3_lastdown.direction
k3_lastdown.direction = XSELL
k3_lastdown.priority = 1600 #对i09时200即优先级最高的效果最好





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
            ,strend(sif.ma13)>0
            ,sif.ltrend>0
            ,sif.mtrend<0
            ,sif.rl_trend>0
            ,sif.rm_trend>0
            )
    signal = derepeatc(signal)

    return signal * k5_lastup.direction
k5_lastup.direction = XBUY
k5_lastup.priority = 1900

def k5_lastup2(sif,sopened=None):
    '''
        底部衰竭模式
        5分钟底部出现长下影
        30分钟之内收盘突破最高价
    '''
    trans = sif.transaction
 
    ma5_500 = ma(sif.close5,500)
    ma5_200 = ma(sif.close5,200)
    ma5_60 = ma(sif.close5,60) 
    ma5_13 = ma(sif.close5,13)     
    ma5_30 = ma(sif.close5,30) 
    ma5_7 = ma(sif.close5,7)         
    ma5_3 = ma(sif.close5,3)         
    
    signal5 = gand(
                gmin(sif.open5,sif.close5) - sif.low5 > np.abs(sif.open5-sif.close5) #下影大于实体
                ,sif.low5 < rollx(tmin(sif.low5,20))
                ,sif.vol5 > rollx(sif.vol5)  
                )

    delay = 5

    bline = np.select([signal5>0],[sif.high5],0)
    bline = extend(bline,delay)
    
    #fsignal = cross(bline,sif.high)>0
    fsignal5 = sif.close5 > bline

    #signal = np.zeros_like(sif.close)
    #signal[sif.i_cof5] = signal5

    signal5 = sfollow(signal5,fsignal5,delay)
    signal = np.zeros_like(sif.close)
    signal[sif.i_cof5] = signal5

    signal = gand(signal
            ,strend(sif.ma13)>0
            ,sif.ltrend>0
            ,sif.mtrend<0
            #,sif.rl_trend>0
            #,sif.rm_trend>0
            )
    #signal = derepeatc(signal)

    return signal * k5_lastup2.direction
k5_lastup2.direction = XBUY
k5_lastup2.priority = 1900


def k5_lastup3(sif,sopened=None):
    '''
        底部衰竭模式
        5分钟底部阴线后出现孕线，后10分钟内1分钟最高线突破该孕线前线的最高点
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
                ,rollx(sif.low5) == tmin(rollx(sif.low5,1),20)
                #,rollx(sif.vol5) > sif.vol5
                #,rollx(sif.vol5) > rollx(sif.vol5,2)
                #,rollx(sif.close5)<rollx(sif.open5)
                #,strend2(ma5_60)<-20
                #,strend2(ma5_30)<0
                #,strend2(sif.diff5x)<0
                #,strend2(ma5_13)<0                
                #,strend2(ma5_7)<0                                
                #,ma5_30 < ma5_60
                #,ma5_7 < ma5_13
                #,strend2(ma5_500)>0
                )

    delay = 10

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof5] = signal5
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof5] = rollx(sif.high5)   #sif.close5#(sif.high5 + sif.close5)/2
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
            )

    return signal * k5_lastup3.direction
k5_lastup3.direction = XBUY
k5_lastup3.priority = 1000


def m2700(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)
 
    ma2700 = ma(sif.close,2700)

    signal = cross(ma2700+10,sif.low)>0
    #signal = cross(sif.dea1,sif.diff1) > 0
    #fsignal = gand(sif.close>sif.ma5)

    #signal = sfollow(signal,fsignal,5)

    signal = gand(signal
            ,strend2(ma2700)>0
            #,sif.ma5>sif.ma13
            #,strend2(sif.ma13)>0
            )
    return signal * m2700.direction
m2700.direction = XBUY
m2700.priority = 1000


def sks(sif,sopened=None):
    #k,d = skdj(sif.high5,sif.low5,sif.close5)
    #lsignal = gand(cross(d,k)<0)
    #signal = np.zeros_like(sif.close)
    #signal[sif.i_cof5] = lsignal
    signal = rollx(sopened,15)
    return signal * XSELL
    

def skdj30(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    k,d = skdj(sif.high5,sif.low5,sif.close5)
    lsignal = gand(cross(d,k)>0)#,k<50)
    signal = np.zeros_like(sif.close)
    signal[sif.i_cof5] = lsignal
    signal = gand(signal
            #,sif.ma5>sif.ma13
            #,strend2(sif.ma60)<0
            )
    return signal * skdj30.direction
skdj30.direction = XBUY
skdj30.priority = 1000



def lastbuy(sif,sopened=None):
    '''
        最后的买入防线. 叠加效果比较差
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)
 
    signal = gand(sif.close>sif.ma5
            ,strend2(sif.ma5)>0
            ,strend2(sif.ma13)>0
            ,strend2(sif.ma30)>0
            ,strend2(sif.ma60)>0
            ,strend2(sif.ma135)>0
            ,strend2(sif.ma270)>0
            ,sif.ma5>sif.ma13
            ,sif.ma13>sif.ma30
            ,sif.ma30>sif.ma60
            ,sif.ma60>sif.ma135
            ,sif.ma135>sif.ma270
            )
    return signal * tfunc.direction
lastbuy.direction = XBUY
lastbuy.priority = 1000
#tfunc.closer = lambda c:c+[s1]


def xud10s(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    mxc = xc0s(sif.open10,sif.close10,sif.high10,sif.low10,13) < 0
    signal = np.zeros_like(sif.diff1)
    signal[sif.i_cof10] = mxc

    signal = gand(signal
            ,sif.ltrend<0
            ,sif.mtrend<0
            ,strend2(sif.ma30)<0
            ,sif.s30<0
            ,sif.ma5<sif.ma13
            ,sif.diff5<0
            )

    return signal * xud10s.direction
xud10s.direction = XSELL
xud10s.priority = 2100


def ipmacd_short_6a(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)
    
    s30_13 = np.zeros_like(sif.diff1)
    s30_13[sif.i_cof30] = strend2(ma(sif.close30,13))
    s30_13 = extend2next(s30_13)

    signal = gand(cross(sif.dea1,sif.diff1)<0
            ,sif.sdiff5x<sif.sdea5x
            #,sif.s30<0 #strend2(sif.sdiff30x-sif.sdea30x)<0
            #,sif.sdiff30x<sif.sdea30x
            ,sif.mtrend<0
            ,sif.s10<0
            )
    signal = gand(signal
            ,sif.ma5 < sif.ma13
            ,strend2(sif.ma30)<0
            ,strend2(sif.ma270)<0
            ,ksfilter
            )
    return signal * ipmacd_short_6a.direction 
ipmacd_short_6a.direction = XSELL
ipmacd_short_6a.priority = 1000

def ipmacd_short_6b(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)
    
    s30_13 = np.zeros_like(sif.diff1)
    s30_13[sif.i_cof30] = strend2(ma(sif.close30,13))
    s30_13 = extend2next(s30_13)

    signal = gand(cross(sif.dea1,sif.diff1)<0
            #,gor(strend2(sif.sdiff30x-sif.sdea30x)<0,sif.sdiff30x<sif.sdea30x)
            #,strend2(sif.sdiff5x-sif.sdea5x)<0
            ,sif.sdiff5x<sif.sdea5x
            #,strend2(sif.sdiff30x-sif.sdea30x)<0
            ,sif.sdiff30x<sif.sdea30x
            ,s30_13 < 0
            )
    signal = gand(signal
            ,sif.ma5 < sif.ma13
            ,strend2(sif.ma30)<0
            ,strend2(sif.ma270)<0
            ,ksfilter
            )
    return signal * ipmacd_short_6b.direction 
ipmacd_short_6b.direction = XSELL
ipmacd_short_6b.priority = 1000

def ipmacd_short_6c(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)
    

    sm = sif.ma270 - rollx(sif.ma270)
    ss2 = msum(sm,20)
    
    s30_13 = np.zeros_like(sif.diff1)
    s30_13[sif.i_cof30] = strend2(ma(sif.close30,13))
    s30_13 = extend2next(s30_13)

    signal = gand(cross(sif.dea1,sif.diff1)<0
            #,gor(strend2(sif.sdiff30x-sif.sdea30x)<0,sif.sdiff30x<sif.sdea30x)
            #,strend2(sif.sdiff5x-sif.sdea5x)<0
            ,strend2(sif.sdiff5x-sif.sdea5x)<0
            #,sif.sdiff5x<sif.sdea5x
            #,strend2(sif.diff30-sif.dea30)<0
            #,sif.sdiff30x<sif.sdea30x
            #,sif.sdiff60x<sif.sdea60x
            #,strend2(sif.sdiff60x-sif.sdea60x)<0
            #,s30_13 < 0
            #,ss2<0
            )
    signal = gand(signal
            #,sif.ma5 < sif.ma13
            #,strend2(sif.ma30)<0
            #,strend2(sif.ma270)<0
            #,ksfilter
            )
    return signal * ipmacd_short_6c.direction 
ipmacd_short_6c.direction = XSELL
ipmacd_short_6c.priority = 1000


def ldevi30(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)
    
    s30_13 = np.zeros_like(sif.diff1)
    s30_13[sif.i_cof30] = strend2(ma(sif.close30,13))
    s30_13 = extend2next(s30_13)


    xs = np.zeros_like(sif.close)
    l30 = ldevi(sif.low30,sif.diff30x,sif.dea30x)
    sc = cross(sif.dea30x,sif.diff30x)
    scc = np.select([sc<0],[sc],0)  #下叉为-1

    xs[sif.i_cof30] = l30 + scc   
    
    xs = extend2next(xs)    #5分钟底背离的有效期是下一次下叉之前

    signal = gand(cross(sif.dea1,sif.diff1)>0)
    signal = gand(signal
                ,xs > 0
                ,sif.ma3>sif.ma13  
                ,strend(sif.sdiff5x-sif.sdea5x)>0            
                #,strend(sif.sdiff15x-sif.sdea15x)>0            
                ,strend(sif.sdiff30x-sif.sdea30x)>0
                ,strend(sif.ma30)>0
                ,strend(sif.ma13)>0
                ,strend(sif.ma7-sif.ma30)>0              
                #,dsfilter
                )
    return signal * ldevi30.direction
ldevi30.direction = XBUY
ldevi30.priority = 1000
#tfunc.closer = lambda c:c+[s1]


def ipmacd_long_6(sif,sopened=None):
    trans = sif.transaction
    
    s30_13 = np.zeros_like(sif.diff1)
    s30_13[sif.i_cof30] = strend2(ma(sif.close30,13))
    s30_13 = extend2next(s30_13)
    
    signal = cross(sif.dea1,sif.diff1)>0

    signal = gand(signal
              ,sif.ma3>sif.ma13  
              ,sif.s5>0
              ,strend2(sif.diff1-sif.dea1)>0
              ,strend(sif.ma30)>0
              ,strend(sif.ma13)>0
              ,sif.ltrend>0
              ,sif.diff1>0
            )

    return signal * XBUY
ipmacd_long_6.direction = XBUY
ipmacd_long_6.priority = 2430#2430




def ipmacd_long_x(sif,sopened=None):
    signal = cross(sif.dea1,sif.diff1)>0

    signal = gand(signal
              ,sif.ma3>sif.ma13  
              #,strend2(sif.sdiff30x-sif.sdea30x)>0
              ,sif.s30>0
              ,sif.s5>0
              ,strend2(sif.ma30)>0
              ,sif.ms>0
              ,sif.ltrend>0
            )

    return signal * ipmacd_long_x.direction
ipmacd_long_x.direction = XBUY
ipmacd_long_x.priority = 1800

def ipmacd_long_t2(sif,sopened=None):#+
    signal = gand(cross(sif.dea1,sif.diff1)>0
                ,sif.s5>0
                ,sif.sdiff30x<sif.sdea30x
                ,strend2(sif.diff30-sif.dea30)>0
                ,sif.ma5>sif.ma13
                ,strend(sif.ma3)>2
                ,sif.ms>0
                ,sif.s15>0
                )
    return signal * ipmacd_long_t2.direction
ipmacd_long_t2.direction= XBUY
ipmacd_long_t2.priority = 2000



def rsi_long_x(sif,sopened=None,rshort=7,rlong=19):
    '''
        比较妥当的是 7/19和13/41参数,其中前者明显优于后者
    '''

    #signal = cross(sif.dea1,sif.diff1)>0
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    signal = cross(rsib,rsia)>0    

    signal = gand(signal
              ,sif.t7_30>0
              ,sif.ltrend>0
              ,sif.mtrend>0
              #,sif.strend>0
              ,sif.ma3>sif.ma13  
              ,sif.ma7> sif.ma30              
              ,sif.s30>0
            )

    return signal * rsi_long_x.direction
rsi_long_x.direction = XBUY
rsi_long_x.priority = 1200

def rsi_long_x2(sif,sopened=None,rshort=7,rlong=19):
    '''
        比较妥当的是 7/19和13/41参数,其中前者明显优于后者
    '''

    #signal = cross(sif.dea1,sif.diff1)>0
    rshort = 7
    rlong = 19
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    signal = cross(rsib,rsia)>0    

    signal = gand(signal
              ,sif.rs_trend>0
              ,sif.rm_trend>0
              #,sif.rl_trend>0
              ,sif.ltrend>0
              ,sif.ms>0
              ,sif.ma3>sif.ma13  
              ,sif.ma7> sif.ma30              
              ,sif.s30>0
            )

    return signal * rsi_long_x2.direction
rsi_long_x2.direction = XBUY
rsi_long_x2.priority = 1500


def rsi_long_x2a(sif,sopened=None,rshort=7,rlong=19):
    '''
        比较妥当的是 7/19和13/41参数,其中前者明显优于后者
        是rsi_long_x2的增条件版本，添加了rl_trend>0,mtrend>0
    '''

    #signal = cross(sif.dea1,sif.diff1)>0
    rshort = 7
    rlong = 19
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    signal = cross(rsib,rsia)>0    

    signal = gand(signal
              ,sif.rs_trend>0
              ,sif.rm_trend>0
              ,sif.rl_trend>0
              ,sif.ltrend>0              
              ,sif.mtrend>0
              ,sif.ms>0
              ,sif.ma3>sif.ma13  
              ,sif.ma7> sif.ma30              
              ,sif.s30>0
            )

    return signal * rsi_long_x2a.direction
rsi_long_x2a.direction = XBUY
rsi_long_x2a.priority = 1410




def rsi_short_x(sif,sopened=None,rshort=7,rlong=19):
    '''
        比较妥当的是 7/19和13/41参数,其中前者明显优于后者
    '''

    #signal = cross(sif.dea1,sif.diff1)>0
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    signal = cross(rsib,rsia)<0    

    signal = gand(signal
              ,sif.rm_trend<0
              ,sif.rs_trend<0
              ,sif.mm<0
              ,sif.ms<0
              #,sif.rl_trend<0
              #,sif.strend>0
              #,sif.ma3<sif.ma13  
              #,sif.ma7< sif.ma30              
              ,sif.s30<0
              #,sif.s15<0
              ,sif.sdiff30x<0
            )

    return signal * rsi_short_x.direction
rsi_short_x.direction = XSELL
rsi_short_x.priority = 1800



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
              #,sif.s30>0
              #,sif.s15>0
              ,sif.rm_trend>0
              ,sif.mm>0
              #,strend2(sif.sdiff30x-sif.sdea30x)>0
            )

    return signal * ma2x.direction
ma2x.direction = XBUY
ma2x.priority = 800

def ems(sif,sopened=None):
    ''' 过滤条件的完全集合
    '''

    signal = cross(sif.ma60,sif.close)>0

    signal = gand(
              sif.mtrend>0
              ,sif.ltrend>0              
              ,sif.rm_trend>0              
              ,sif.s30>0
              ,sif.s5>0
              ,sif.ms>0
              ,sif.mm>0
              ,sif.t7_30>0
            )
    signal = derepeatc(signal)
    return signal * ems.direction
ems.direction = XBUY
ems.priority = 2400

def ma1xs(sif,sopened=None):
    '''
    '''

    signal = cross(sif.ma30,sif.ma5)<0

    #fsignal = cross(sif.sd,sif.sk)>0
    #signal = sfollow(signal,fsignal,30)

    signal = gand(signal
              ,sif.mtrend<0
              ,sif.ltrend<0 
              ,strend2(sif.ma30)<0
              ,strend2(sif.ma13-sif.ma60)<0
              ,sif.s30<0
            )

    return signal * ma1xs.direction
ma1xs.direction = XSELL
ma1xs.priority = 800


def xs5(sif,sopened=None):
    
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
              ,sif.s30>0
              ,sif.s10>0
            )

    return signal * xs5.direction
xs5.direction = XBUY
xs5.priority = 1200


def up3(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    #ma33 = ma(sif.close3,3)

    signal3 = gand(sif.low3>rollx(sif.low3)
                ,rollx(sif.low3)>rollx(sif.low3,2)
                ,sif.high3 > rollx(sif.high3)
                #,sif.high3 > rollx(sif.high3,2)
                ,rollx(sif.high3)>rollx(sif.high3,2)
                #,rollx(sif.high3,2)>rollx(sif.high3,3)
                ,sif.diff3x>sif.dea3x
                #,strend(ma33)>1
                #,sif.close3 > sif.open3
                #,rollx(sif.close3)>rollx(sif.close3,2)
            )

    signal = np.zeros_like(sif.close)

    signal[sif.i_cof3] = signal3

    signal = gand(signal
              ,strend(sif.sdiff5x-sif.sdea5x)>0            
              ,strend(sif.sdiff30x-sif.sdea30x)>0
              ,strend(sif.ma30)>0
            )

    return signal * XBUY


def rsi3x(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    rsi6 = rsi2(sif.close3,6)
    rsi24 = rsi2(sif.close3,24)

    signal = np.zeros_like(sif.close)

    signal[sif.i_cof3] = gand(cross(rsi24,rsi6)>0
                            ,cross(sif.dea3x,sif.diff3x)>0
                            )

    
    signal = gand(signal
              ,strend(sif.ma270)>0
              ,strend(sif.sdiff30x-sif.sdea30x)>0
              ,sif.sdiff5x>0
              ,sif.sdiff30x>sif.sdea30x
            )

    return signal * XBUY


def rsi5x(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    rsis = rsi2(sif.close5,7)
    rsil = rsi2(sif.close5,14)

    signal = np.zeros_like(sif.close)

    signal[sif.i_cof5] = gand(cross(rsil,rsis)>0
                            #,cross(sif.dea5x,sif.diff5x)>0
                            )

    
    signal = gand(signal
              ,strend(sif.ma270)>0
              ,strend(sif.sdiff30x-sif.sdea30x)>0
              #,sif.sdiff5x>0
              ,sif.sdiff30x>sif.sdea30x
            )

    return signal * XBUY
rsi5x.direction = XBUY
rsi5x.priority = 2000  #


def xup(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)


    signal = cross(sif.dea1,sif.diff1)>0
    xhigh = rollx(tmax(sif.high,30))
 
    signal = gand(signal
              ,sif.high>xhigh
              #,x945>0
              ,strend(sif.ma30)>0
              ,strend(sif.sdiff30x-sif.sdea30x)>0
              ,sif.sdiff5x>0
              #,strend(sif.sdiff5x - sif.sdea5x)>0
              #,sif.sdiff5x > sif.sdea5x
              ,sif.ma5 > sif.ma13
            )

    return signal * XBUY


def xdown(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)


    signal = cross(sif.dea1,sif.diff1)<0
    xlow = rollx(tmin(sif.low,30))
 
    xopend = np.zeros_like(sif.close)

    xopend[sif.i_oofd] = sif.opend
    xopend = extend2next(xopend)
 
    x945 = np.select([sif.time==945],[sif.close-xopend],0)
    x945 = extend2next(x945)


    signal = gand(signal
              ,sif.low<xlow
              ,x945<0
              ,strend(sif.ma30)<0
              ,strend(sif.sdiff30x-sif.sdea30x)<0
              ,strend(sif.sdiff5x - sif.sdea5x)>0
              ,sif.sdiff5x < sif.sdea5x
              ,sif.ma5 < sif.ma13
            )

    return signal * XSELL


def opendown(sif,sopened=None):
    '''
        跌破开盘线，且是新低
    '''
    xopend = np.zeros_like(sif.close)

    xopend[sif.i_oofd] = sif.opend
    xopend = extend2next(xopend)

    xlow = rollx(tmin(sif.low,15),1)

    signal = gand(cross(xopend,sif.close)<0
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
opendown.priority = 2000


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
            ,strend2(sif.diff1-sif.dea1)>0
            ,sif.s5>0
            ,sif.s30>0
            ,sif.diff1 > 0
            ,sif.mm>0
            )

    return signal * openup.direction
openup.direction = XBUY
openup.priority = 1800


def dmi15(sif,sopened=None):
    '''
        没啥用
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)


    pdm,ndm = dm(sif.high15,sif.low15)
    xtr = msum(tr(sif.close15,sif.high15,sif.low15),6)
    pdi,ndi = di(pdm,ndm,xtr,14)
    adxx = xadx(pdi,ndi,6)

    signalx = gand(strend2(adxx) == -1
                ,pdi<ndi
                )

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof15] = signalx

    #signal = sfollow(signal,cross(sif.dea1,sif.diff1)>0,30)

    signal = gand(signal
            ,sif.diff1<0
            ,sif.diff30<0
            #,sif.ma5>sif.ma13
            #,strend(sif.ma5)>0
            #,strend(sif.ma5-sif.ma30)>0
            #,strend(sif.diff5-sif.dea5)>0
            #,dsfilter
            )


    return signal * XSELL


def demark1(sif,sopened=None):
    #不起作用
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<00)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    ibs = sif.close < rollx(sif.close,4)
    bsetup = equals(msum(ibs,9),9)

    iss = sif.close > rollx(sif.close,4)
    ssetup = equals(msum(iss,9),9)

    lhv3 = tmax(sif.low,3)
    xx = sif.high > rollx(lhv3,3)

    sbs = gand(bsetup
            ,gor(xx,rollx(xx))
            )

    ibs2 = sif.close < rollx(tmin(sif.low,2),2)

    hhv9 = tmax(sif.high,9)

    signal = np.zeros_like(sif.close)

    signal[sif.i_cof] = demark(sbs,bsetup,sif.close,ibs2,ssetup,hhv9)

    signal = sfollow(signal,cross(sif.dea1,sif.diff1)>0,30)

    return signal * XBUY

def demark(sbs,bsetup,sclose,ibs2,ssetup,hhv9):
    #暂不考虑numpy方式
    
    rev = np.zeros_like(bsetup)
    
    bb = 0
    count = 0
    chigh = 0

    for i in xrange(len(sbs)):
        xi = sbs[i]
        bi = bsetup[i]        
        if xi == 1:#开始
            print u'开始:',i
            bb = 1
            count = 0
            chigh = hhv9[i]
            bi = 0  #用于不激发下面的取消条件
        elif bb == 0:   #未进入
            continue
        if bi or ssetup[i] or sclose[i]>chigh: #取消计数
            print u'取消:',i
            bb = 0
            continue
        if ibs2[i]:
            count += 1
            print u'计数:', count
            if count == 13:
                rev[i] = 1
    return rev


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
            ,strend2(sif.sdiff30x - sif.sdea30x)>0
            ,sif.sdiff5x > sif.sdea5x
            ,strend2(sif.ma60)>0
            )

    return signal * XBUY

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
            ,sif.s3<0
            )

    return signal * gd30.direction
gd30.direction = XSELL
gd30.priority = 1800



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
            ,strend2(sif.sdiff30x-sif.sdea30x)>0
            ,strend(sif.ma13-sif.ma60)>0
            ,sif.ma3>sif.ma13
            ,sif.mtrend>0
            )


    return signal * br75.direction
br75.direction = XBUY
br75.priority = 2400



def goup5(sif,sopened=None):
    ''' 
        5分钟冲击昨日高点时买入, 过滤器向下浮动. 即不论是否突破，都介入
    ''' 
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

 
    highd = gmax(sif.closed,sif.opend) #- sif.atrd/XBASE/8 #gmax(sif.closed,sif.opend)+sif.atrd/XBASE/10
    #highd = sif.highd


    xhighd = np.zeros(len(sif.diff1),np.int32)
    xhighd[sif.i_cofd] = highd

    xup = np.zeros(len(sif.diff1),np.int32)
    xup[sif.i_cofd] = sif.closed>rollx(sif.closed)

    xhighd = extend(xhighd,260)
    xup = extend(xup,260)

    signal = np.zeros_like(sif.diff1)

    signal[sif.i_cof5] = gand(cross(xhighd[sif.i_cof5],sif.close5)>0)

    #signal = sfollow(signal,cross(sif.dea1,sif.diff1)>0,30)

    signal = gand(signal
            ,xup>0
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
            ,sif.ma5<sif.ma13
            ,strend(sif.ma30)<0
            ,sif.ltrend<0
            ,sif.ms<0
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
            ,sif.s30<0
            ,sif.s10<0
            ,strend(sif.ma30)<0
            ,sif.ltrend<0
            ,sif.mtrend<0            
            )


    return signal * godown30.direction
godown30.direction = XSELL
godown30.priority = 2000



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
            #,strend(sif.ma270)>0
            ,sif.rs_trend>0
            )


    return signal * inside_up.direction
inside_up.direction = XBUY
inside_up.priority = 2000

def gapdown(sif,sopened=None):
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

    signal[sif.i_cof] = gand(cross(xhighd[sif.i_cof],sif.low)<0,hgap[sif.i_cof])

    signal = gand(signal
            ,sif.ma5  < sif.ma13
            ,strend(sif.ma30)<0
            )


    return signal * XSELL


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

    signal[sif.i_cof15] = gand(cross(xhighd[sif.i_cof15],sif.low15)<0,hgap[sif.i_cof15])


    return signal * XSELL


def gapdown5(sif,sopened=None):
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

    signal[sif.i_cof5] = gand(cross(xhighd[sif.i_cof5],sif.low5)<0,hgap[sif.i_cof5])


    return signal * XSELL


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

    signal = sfollow(signal,cross(sif.dea1,sif.diff1)>0,20)

    signal = gand(signal
            ,strend(sif.sdiff30x-sif.sdea30x)>0
            ,strend(sif.diff5-sif.dea5)>0
            ,strend(sif.ma30)>0
            ,sif.ma5>sif.ma13
            ,sif.mtrend>0
            #,sif.ms>0
            )

    return signal * br30.direction
br30.direction = XBUY
br30.priority = 300

def bd30(sif,sopened=None):
    '''
        5分钟最高突破开盘前30分钟最高之后，下一次1分钟上叉
        属于突破回调的模式
        难以周期化
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)
    
    low30 = np.select([trans[ITIME][sif.i_cof30]==945],[sif.low30],default=0)

    xhigh30,xlow30 = np.zeros_like(sif.diff1),np.zeros_like(sif.diff1)
    xlow30[sif.i_cof30] = low30

    xlow30 = extend2next(xlow30)

    signal = np.zeros_like(sif.diff1)

    signal[sif.i_cof5] = cross(xlow30[sif.i_cof5],sif.low5)<0

    #signal = sfollow(signal,cross(sif.dea1,sif.diff1)<0,20)
    #signal = sfollow(signal,cross(sif.sd,sif.sk)<0,30)    #20虽然更好，叠加不佳

    signal = gand(signal
            ,strend(sif.diff30-sif.dea30)<0
            ,strend(sif.ma30)<0
            ,sif.ma5<sif.ma13
            ,sif.rs_trend<0
            ,sif.ms<0
            ,sif.mm<0
            ,sif.diff1<0
            )

    return signal * bd30.direction
bd30.direction = XSELL
bd30.priority = 300


def lwr15(sif,sopened=None):

    c,mc = lwr(sif.high15,sif.low15,sif.close15)

    signal = np.zeros_like(sif.diff1)
    signal[sif.i_cof15] = cross(mc,c)<0

    signal = gand(
            signal
            ,sif.rl_trend>0
            ,sif.rm_trend>0            
            ,sif.ml>0
            ,strend(sif.diff30-sif.dea30)>0
            )

    return signal * XBUY
lwr15.direction = XBUY
lwr15.priority = 1500

def lwr15s(sif,sopened=None):

    c,mc = lwr(sif.high15,sif.low15,sif.close15)

    signal = np.zeros_like(sif.diff1)
    signal[sif.i_cof15] = cross(mc,c)>0

    signal = gand(signal
            ,sif.ml<0
            ,sif.ms<0
            ,sif.mm<0
            ,sif.rl_trend<0            
            ,sif.sdiff30x<0
            ,sif.sdiff5x<0
            )

    return signal * XSELL
lwr15s.direction = XSELL
lwr15s.priority = 300



def xud10(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)


    mxc = xc0s(sif.open10,sif.close10,sif.high10,sif.low10,13) > 0
    signal = np.zeros_like(sif.diff1)
    signal[sif.i_cof10] = mxc

    signal = gand(signal
            ,strend(sif.diff1)>0
            ,strend(sif.ma60)>0
            ,strend(sif.ma30)>0
            #,dsfilter
            )


    return signal * xud10.direction
xud10.direction = XBUY
xud10.priority = 500


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

def xud15c(sif,sopened=None):
    trans = sif.transaction

    mxc = xc0c(sif.open15,sif.close15,sif.high15,sif.low15,13) > 0
    signal = np.zeros_like(sif.diff1)
    signal[sif.i_cof15] = mxc

    signal = gand(signal
            ,strend(sif.diff1)>0
            ,strend(sif.ma270)>0
            #,sif.s30>0
            #,dsfilter
            )

    return signal * XBUY
xud15c.direction = XBUY
xud15c.priority = 1601


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
            #,sif.ma5>sif.ma13
            #,strend(sif.ma5)>0
            #,strend(sif.ma5-sif.ma30)>0
            #,strend(sif.diff5-sif.dea5)>0
            #,dsfilter
            )


    return signal * XBUY


def xud30(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    mxc = xc0c(sif.open15,sif.close15,sif.high15,sif.low15,13) < 0
    signal = np.zeros_like(sif.diff1)
    signal[sif.i_cof15] = mxc

    signal = gand(signal
            ,strend(sif.diff1-sif.dea1)<0
            #,strend(sif.ma30)<0
            #,strend2(sif.sdiff5x-sif.sdea5x)<0
            #,sif.mtrend<0
            #,dsfilter
            )

    return signal * xud30.direction
xud30.direction = XSELL
xud30.priority = 1601

def xud30c(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    mxc = xc0c(sif.open30,sif.close30,sif.high30,sif.low30,13) > 0
    signal = np.zeros_like(sif.diff1)
    signal[sif.i_cof30] = mxc

    signal = gand(signal
            ,strend(sif.diff1)>0
            ,strend(sif.ma270)>0
            #,dsfilter
            )

    return signal * XBUY



def ipmacd_long_5(sif,sopened=None):
    trans = sif.transaction

    dsfilter2 = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<2000)

    s30_13 = np.zeros_like(sif.diff1)
    s30_13[sif.i_cof30] = strend2(ma(sif.close30,13))
    s30_13 = extend2next(s30_13)

    sm = sif.ma270 - rollx(sif.ma270)
    ss2 = msum(sm,20)
    sss = strend(ss2)


    signal = gand(cross(sif.dea1,sif.diff1)>0
            #,sif.diff30>0
            ,strend2(sif.sdiff30x-sif.sdea30x)>0
            ,sif.sdiff5x>0
            ,s30_13 >0
            )
    signal = gand(signal
            ,sif.ma5 > sif.ma13
            ,strend2(sif.ma13-sif.ma60)>0
            ,strend2(sif.ma30)>0
            ,strend2(sif.ma135)>0
            ,sss>0
            ,dsfilter2
            )
    return signal * XBUY
ipmacd_long_5.direction = XBUY
ipmacd_long_5.priority = 2400



def ipmacd_short_4(sif,sopened=None):
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)


    s30_13 = np.zeros_like(sif.diff1)
    s30_13[sif.i_cof30] = strend2(ma(sif.close30,13))
    s30_13 = extend2next(s30_13)

    signal = gand(cross(sif.dea1,sif.diff1)<0
            ,sif.diff30<0
            ,sif.diff5<0
            ,s30_13 < 0
            )
    signal = gand(signal
            ,sif.ma5 < sif.ma13
            ,sif.ma135<sif.ma270
            ,strend2(sif.ma30)<=-10
            ,ksfilter
            )
    
    return signal * XSELL
ipmacd_short_4.direction = XSELL
ipmacd_short_4.priority = 2400


def ipmacd_short_3(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)


    signal = gand(cross(sif.dea1,sif.diff1)<0
            ,sif.diff30<0
            ,sif.diff5<0
            ,strend2(sif.diff5-sif.dea5)>0
            )
    signal = gand(signal
            ,sif.ma5 < sif.ma13
            ,sif.ma135<sif.ma270
            ,strend2(sif.ma30)<=-4
            ,strend(sif.ma270)<0
            ,ksfilter
            )

    return signal * XSELL


def sms(sif,sopened=None):
    '''
        R比较平均，但都不高
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤

    dsignal = gand(strend(sif.diff1-sif.dea1)<0
                ,strend(sif.diff5-sif.dea5)<0
                ,strend(sif.diff30-sif.dea30)<0
                ,strend(sif.diff1)<0
                ,strend(sif.diff5)<0
                ,strend(sif.diff30)<0
                )
    msignal = gand(sif.ma5<sif.ma13
                ,sif.ma13<sif.ma30
                ,sif.ma30<sif.ma60
                )
    ssignal = gand(strend(sif.ma5-sif.ma30)<0
                ,strend(sif.ma13-sif.ma60)<0
                ,strend(sif.ma135-sif.ma270)<0
                ,strend(sif.ma30)<-4
                )

    signal = gand(dsignal
                ,msignal
                ,ssignal
                ,sif.diff30<0
                ,sif.diff5<0
                ,sif.diff1<0
                ,ksfilter)


    return signal * XSELL

def up0(sif,sopened=None):
    '''
        上穿0线
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤

    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1)>0
            ,sif.diff5<0
            #,strend(sif.diff30-sif.dea30)>1
            ,sif.s30>0
            ,strend(sif.diff5-sif.dea5)>1
            ,strend(sif.diff1)>4
            ,strend(sif.ma30)>0
            ,dsfilter
            )

    return signal * up0.direction
up0.direction = XBUY
up0.priority = 1800  #叠加时，远期互有盈亏


def dmacd_long5(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤

    sdd = strend(sif.diff5 - sif.dea5)
    signal = gand(sdd==1,rollx(sdd)<-4
            ,sif.diff1 < 0
            ,sif.diff5 < 0
            ,strend(sif.diff30-sif.dea30)>0
            ,strend(sif.diff1-sif.dea1)>0
            ,strend(sif.diff5-sif.dea5)>0            
            )
    signal = gand(signal
            ,strend(sif.ma135-sif.ma270)>0
            ,strend(sif.ma13-sif.ma60)>0
            ,sif.ma5>sif.ma13
            ,dsfilter
            )

    return signal * XBUY

def up02(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤

    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1)>0
            ,strend(sif.ma30)>0
            ,sif.ma3>sif.ma13
            ,sif.ltrend>0
            ,sif.s30>0
            )

    return signal * up02.direction
up02.direction = XBUY
up02.priority = 600  #


def ipmacd_long_1(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤

    xopen=np.zeros(len(sif.diff1),np.int32)
    xopen[sif.i_oofd] = sif.opend
    xopen = extend2next(xopen)


    signal = gand(cross(sif.dea1,sif.diff1)>0
            ,sif.diff5>0
            ,strend(sif.diff30-sif.dea30)>0
            ,strend(sif.diff1)>2
            #,trans[ICLOSE]>xopen
            )
    signal = gand(signal
            ,strend(sif.ma30)>4
            ,strend(sif.ma13-sif.ma60)>0            
            ,strend(sif.ma135-sif.ma270)>0            
            ,dsfilter
            )

    return signal * XBUY



def dms(sif,sopened=None):
    '''
        全部信号走好,唯一一点就是diff5<0
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤

    dsignal = gand(strend(sif.diff1-sif.dea1)>0
                ,strend(sif.diff5-sif.dea5)>0
                ,strend(sif.diff30-sif.dea30)>0
                ,strend(sif.diff1)>0
                ,strend(sif.diff5)>0
                ,strend(sif.diff30)>0
                )
    msignal = gand(sif.ma5>sif.ma13
                ,sif.ma13>sif.ma30
                ,sif.ma30>sif.ma60
                )
    ssignal = gand(strend(sif.ma5-sif.ma30)>0
                ,strend(sif.ma13-sif.ma60)>0
                ,strend(sif.ma135-sif.ma270)>0
                ,strend(sif.ma30)>4
                )

    signal = gand(dsignal
                ,msignal
                ,ssignal
                ,sif.diff5<0
                ,dsfilter)

    return signal * XBUY


def dmss(sif,sopened=None):
    '''
        全部信号走坏，不成
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    dsignal = gand(strend(sif.diff1-sif.dea1)<0,strend(sif.diff5-sif.dea5)<0,strend(sif.diff30-sif.dea30)<0,strend(sif.diff1)<0,strend(sif.diff5)<0,strend(sif.diff30)<0)
    msignal = gand(sif.ma5<sif.ma13,sif.ma13<sif.ma30,sif.ma30<sif.ma60)
    ssignal = gand(strend(sif.ma5-sif.ma30)<0,strend(sif.ma13-sif.ma60)<0)

    signal = gand(dsignal,msignal,ssignal,sif.diff5<0,sif.diff30<0,sif.diff1<0,dsfilter)

    return signal * XSELL


def mx(sif,sopened=None):
    '''
        全部均线走好
        6.03以后走入损失期        
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    mfilter = gand(sif.ma13>sif.ma30,sif.ma30>sif.ma60,sif.ma60>sif.ma135,sif.ma135>sif.ma270)

    signal = gand(cross(sif.ma13,sif.ma5)>0,mfilter)

    fsignal = gand(cross(sif.dea1,sif.diff1)>0,mfilter,sif.ma5>sif.ma13)

    signal = sfollow(signal,fsignal,15)

    return signal * XBUY

def mxs(sif,sopened=None):
    '''
        全部均线走坏
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    msignal = gand(sif.ma5<sif.ma13,sif.ma13<sif.ma30,sif.ma30<sif.ma60,sif.ma60<sif.ma135,sif.ma135<sif.ma270)


    signal = gand(cross(sif.dea1,sif.diff1)<0,msignal,sif.diff30<0)#,strend(sif.diff30-sif.dea30)>0)#,dsfilter)

    return signal * XSELL



def down30(sif,sopened=None):
    '''
        macd30下叉时
    '''
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    msignal = cross(sif.dea30,sif.diff30)<0
    
    fsignal = cross(cached_zeros(len(sif.dea1)),sif.diff1)<0
    
    signal = sfollow(msignal,fsignal,135)

    signal = gand(signal
                ,sif.diff30>0
                ,strend(sif.ma135-sif.ma270)<0
                ,ksfilter)

    return signal*XSELL




def xsvap(sif,sopened=None):
    trans = sif.transaction
    svap,v2i = svap_ma(sif.vol,sif.close,120)
    ma_svapfast = ma(svap,30)
    ma_svapslow = ma(svap,60)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    msvap = transform(cross_fast_slow,v2i,len(trans[IVOL]))
    signal = np.zeros_like(sif.close)
    signal[sif.i_cof] = msvap
    s1 = cross(sif.sd,sif.sk)>0
    signal = sfollow(signal,s1,10)
    signal = gand(signal
                ,strend(sif.sdiff5x-sif.sdea5x)>0
                ,strend(sif.diff1-sif.dea1)>0
                ,sif.ma3>sif.ma7
                ,sif.ma7>sif.ma13
                ,strend(sif.ma13)>0
                ,sif.diff1<0
            )
    return signal * xsvap.direction
xsvap.direction = XBUY
xsvap.priority = 1000
#xsvap.closer= lambda c:c+[s90]

def long5x(sif,sopened=None):#
    '''
    '''
    trans = sif.transaction
    s15 = strend(sif.diff15x-sif.dea15x)
    s15x = np.zeros_like(sif.diff1)
    s15x[sif.i_cof15] = s15
    s15x = extend2next(s15x)

    #signal = gand(cross(sif.sdea5x,sif.sdiff5x)>0,sif.sdiff15x>0,sif.sdiff30x>sif.sdea30x,sif.sdiff15x>sif.sdea15x)#,sif.xatr<2000)#,strend(sif.diff15-sif.dea15)>0,strend(sif.diff30-sif.dea30)>0)
    signal = gand(cross(sif.sdea5x,sif.sdiff5x)>0,s15x,sif.sdiff30x>sif.sdea30x,sif.sdiff15x>sif.sdea15x)#,sif.xatr<2000)#,strend(sif.diff15-sif.dea15)>0,strend(sif.diff30-sif.dea30)>0)
    return signal * XBUY

def ipmacd_long_f(sif,sopened=None):
    '''
        过滤后的macd1上叉
        操作方式:
            1. 1分钟上叉
            2. 3分钟后macd仍然在延续往上,
            3. 5分钟macd>0且上行中,diff5<0
               30分钟macd<0,但在上行中
    '''

    trans = sif.transaction
    dsfilter = gand(trans[IOPEN] - trans[ICLOSE] < 100,rollx(trans[IOPEN]) - trans[ICLOSE] < 200,sif.xatr<1500)

    sfilter = gand(strend(sif.diff5-sif.dea5)>0
                ,sif.diff5>sif.dea5
                ,sif.diff5<0
                ,sif.diff30<sif.dea30
                ,strend(sif.diff30-sif.dea30)>0
                #,sif.ma5>sif.ma13
                #,strend(sif.ma135-sif.ma270)>0
            )

    signal = gand(fmacd1_long(sif,3,sfilter)
                ,dsfilter
                ,sif.ma5>sif.ma13
                ,strend(sif.ma135-sif.ma270)>0
                ,strend(sif.diff5-sif.dea5)>0
            )

    return signal * XBUY


def short5x(sif,sopened=None):#
    '''
    '''
    trans = sif.transaction
    s15 = strend(sif.diff15x-sif.dea15x)
    s15x = np.zeros_like(sif.diff1)
    s15x[sif.i_cof15] = s15
    s15x = extend2next(s15x)

    signal = gand(cross(sif.sdea5x,sif.sdiff5x)<0,sif.diff30<0,sif.sdiff30x<sif.sdea30x,sif.sdiff15x<sif.sdea15x)#,sif.xatr<2000)#,strend(sif.diff15-sif.dea15)>0,strend(sif.diff30-sif.dea30)>0)
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
    #signal = gand(signal,sif.xatr<1500)
    return signal * XBUY


def ipmacd_long_old(sif,sopened=None):#
    ''' 
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea1,sif.diff1)>0,sif.diff5>sif.dea5,sif.diff30>0,strend(sif.diff30-sif.dea30)>0)#,sif.diff1>0)#,strend(sif.diff5)>0)
    signal = gand(signal,strend(sif.ma5)>1,sif.ma5>sif.ma30,strend(sif.ma60)>5,sif.xatr<2000)#,strend(sif.diff5-sif.dea5)<0)
    return signal * XBUY

def up1_0(sif,sopened=None):#
    trans = sif.transaction
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤
    
    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1),sif.diff30<0,sif.diff5<0,strend(sif.diff5-sif.dea5)>0,strend(sif.diff30-sif.dea30)>0,strend(sif.ma5)>1,sif.ma5>sif.ma13)
    signal = gand(signal,sif.xatr<1500,sfilter,strend(sif.ma5-sif.ma30)>0)
    return signal * XBUY

def up5_0(sif,sopened=None):#
    trans = sif.transaction
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤
    
    signal = gand(cross(cached_zeros(len(sif.diff5)),sif.diff5))
    ss= gand(strend(sif.diff5-sif.dea5)>0,strend(sif.diff30-sif.dea30)>0,strend(sif.ma5)>1,sif.ma5>sif.ma13)
    fsignal = gand(cross(sif.dea1,sif.diff1)>0,ss)
    signal = gand(sfollow(signal,fsignal,15),sif.xatr<1500,sfilter,strend(sif.ma5-sif.ma30)>0)
    return signal * XBUY

def up(sif,sopened=None):
    trans = sif.transaction
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤

    signal = gand(strend(sif.diff1-sif.dea1)>2,strend(sif.diff5-sif.dea5)>4,strend(sif.diff30-sif.dea30)>0,strend(sif.ma5-sif.ma30)>0,sif.ma5>sif.ma13,sif.ma13>sif.ma30)

    signal = gand(signal,sfilter,sif.xatr<1500)
    return signal * XBUY

def ipmacd_long(sif,sopened=None):#
    ''' 
    '''
    trans = sif.transaction
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤    
    signal = gand(cross(sif.dea5,sif.diff5)>0,strend(sif.diff30-sif.dea30)>0,sif.diff5<0)
    fsignal = gand(cross(sif.dea1,sif.diff1)>0)
    #signal = gand(signal,sif.xatr<2000,sfilter)
    signal = gand(sfollow(signal,fsignal,30),sif.xatr<2000,sfilter)
    return signal * XBUY



def ipmacd_5x13(sif,sopened=None):
    '''
    '''
    trans = sif.transaction
    signal = gand(cross(sif.ma30,sif.ma5)>0,sif.ma5>sif.ma13,trans[ICLOSE]>sif.ma5,sif.diff1>sif.dea1,strend(sif.diff1-sif.dea1)>5,strend(sif.diff5-sif.dea5)>0)
    return signal * XBUY

def ipmacd_longt(sif,sopened=None):#+
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500) #向上突变过滤

    signal = gand(cross(sif.dea1,sif.diff1)>0
                ,strend(sif.sdiff5x-sif.sdea5x)>0
                #,sif.sdiff30x<sif.sde30x
                ,strend(sif.sdiff30x-sif.sdea30x)>0 #+
                ,sif.ma5>sif.ma13
                ,strend(sif.ma5)>2 #
                ,gor(strend(sif.ma270)>0,strend(sif.ma135)>0)
                ,dsfilter
                )
    return signal * ipmacd_longt.direction
ipmacd_longt.direction= XBUY
ipmacd_longt.priority = 2000

def ipmacd_longta(sif,sopened=None):#+
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500) #向上突变过滤

    signal = gand(cross(sif.dea1,sif.diff1)>0
                ,strend(sif.diff5-sif.dea5)>0
                ,sif.diff30<sif.dea30
                #,strend(sif.diff30-sif.dea30)>0 #+
                ,sif.ma5>sif.ma13
                ,strend(sif.ma5)>2 #
                #,gor(strend(sif.ma270)>0,strend(sif.ma135)>0)
                #,dsfilter
                )

    rsi7 = rsi2(sif.close,7)
    rsi14 = rsi2(sif.close,14)
    
    fsignal = cross(sif.sd,sif.sk)>0
    #fsignal = cross(rsi14,rsi7)>0
    signal = sfollow(signal,fsignal,15)
    signal = gand(signal
                ,sif.ma3>sif.ma13
                ,strend(sif.ma13)>0
                )
    return signal * ipmacd_longta.direction
ipmacd_longta.direction= XBUY
ipmacd_longta.priority = 2000


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
    fsignal = gand(fsignal,sif.xatr<1500,strend(sif.diff1-sif.dea1)>0,sif.diff1>sif.dea1)
    signal = sfollow(msignal,fsignal,5)
    return signal * XBUY


def ipmacd_long_c(sif,sopened=None):#-
    '''
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea1,sif.diff1)>0,sif.diff1<0,sif.diff5<0,sif.diff5<sif.dea5,sif.diff30<0,sif.diff30>sif.dea30,trans[ICLOSE] - trans[IOPEN] < 100,sif.ma5>sif.ma13)#,sif.ma13>sif.ma60)#,strend(sif.diff5)>0)
    #signal = gand(signal,sif.xatr<1500)
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
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)

    sf = msum(trans[IHIGH]>sif.ma30,5) < 2

    signal = gand(cross(sif.ma30,trans[IHIGH])<0
            ,strend(sif.ma30)<0
            ,sf
            )
    fsignal = gand(cross(sif.dea1,sif.diff1)<0
            ,sif.sdiff5x<0
            ,sif.s30<0
            ,sif.ma5<sif.ma13
            ,sif.strend<0
            #,sif.rm_trend<0
            #,sif.s15<0
            ,ksfilter
            )
    signal = sfollow(signal,fsignal,10)
    return signal * ma30_short.direction
ma30_short.direction = XSELL
ma30_short.priority = 2400

def ma60_short2(sif,sopened=None):
    ''' 下行中下叉60线
    '''
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    sf = msum(trans[IHIGH]>sif.ma60,5) < 3

    signal = gand(cross(sif.ma30,trans[IHIGH])<0
            ,strend(sif.ma60)<0
            ,sf
            )
    fsignal = gand(cross(sif.dea1,sif.diff1)<0
            ,sif.diff1<0
            ,sif.diff5<0
            #,strend(sif.diff30-sif.dea30)<0
            ,strend(sif.ma13-sif.ma60)<0
            #,sif.ma5<sif.ma13
            ,ksfilter
            )
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
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)
 
    msignal = gand(strend(sif.ma60) == -1
                )
    fsignal = gand(cross(sif.dea1,sif.diff1)<0
                ,strend2(sif.sdiff5x-sif.sdea5x)>0
                ,sif.ltrend<0
                ,sif.mtrend<0
                ,sif.ms<0
                ,sif.strend<0
                ,ksfilter                
                )
    signal = sfollow(msignal,fsignal,5)
    return signal * ma60_short.direction
ma60_short.direction = XSELL
ma60_short.priority = 2401


def ma30_short2(sif,sopened=None):
    ''' ma30拐头
    '''
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)
    
    msignal = gand(strend(sif.ma30) == -1,rollx(strend(sif.ma30))<10)
    fsignal = gand(cross(sif.dea1,sif.diff1)<0,strend(sif.diff5-sif.dea5)>0,sfilter,sif.xatr<2000)
    signal = sfollow(msignal,fsignal,15)
    return signal * XSELL


def ma60_long(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤


    msignal = gand(strend(sif.ma60) == 1
                ,rollx(strend(sif.ma60))<-10
                )
    fsignal = gand(cross(sif.dea1,sif.diff1)>0
                ,strend(sif.diff30-sif.dea30)>0
                ,strend(sif.diff5-sif.dea5)>0
                ,strend(sif.diff1-sif.dea1)>0
                ,strend(sif.ma30)>4
                ,sif.ma5>sif.ma13
                ,dsfilter                
                )
    signal = sfollow(msignal,fsignal,10)

    return signal * XBUY



def ma60_long_old(sif,sopened=None):
    ''' ma60拐头
    '''
    trans = sif.transaction
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤
    msignal = gand(strend(sif.ma60) == 1,rollx(strend(sif.ma60))<-10)
    fsignal = gand(cross(sif.dea1,sif.diff1)>0,strend(sif.diff5-sif.dea5)>0,strend(sif.diff30-sif.dea30)>0)
    signal = gand(sfollow(msignal,fsignal,10),sfilter,sif.xatr<1500)
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
    signal = gand(signal,rollx(strend(sif.ma5))<0,sif.ma5<sif.ma13,sif.ma5<sif.ma30,strend(sif.ma60)<-5,sif.xatr<2000)#,strend(sif.diff5-sif.dea5)<0)

    fsignal = gand(strend(sif.diff1-sif.dea1) <= -1)   #下叉后仍然连续下行中
    signal = gand(rollx(signal,1),fsignal,sif.diff5<0,sif.diff30<0)

    return signal * XSELL

def ipmacd_short_x(sif,sopened=None):
    ksfilter = gand(sif.open - sif.close < 60,rollx(sif.open - sif.close) < 120,sif.xatr<2000) 
    signal = gand(cross(sif.dea1,sif.diff1)<0
            ,sif.mtrend<0
            ,sif.sdiff30x>0
            ,sif.s3<0
            )
    signal = gand(signal
            ,sif.ma3 < sif.ma13
            ,sif.ma13 < sif.ma60
            ,strend2(sif.ma30)<0
            ,strend2(sif.ma270)<0
            ,ksfilter
            )
    return signal * ipmacd_short_x.direction
ipmacd_short_x.direction = XSELL
ipmacd_short_x.priority = 1500


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
    #signal = gand(signal,strend(sif.ma5)<-1,sif.ma5<sif.ma13,sif.ma5<sif.ma30,strend(sif.ma60)<-5,sif.xatr<2000)#,strend(sif.diff5-sif.dea5)<0)
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
    #signal = gand(signal,rollx(strend(sif.ma5))<0)#,sif.ma5<sif.ma13,sif.ma5<sif.ma30,sif.xatr<2000)#,strend(sif.diff5-sif.dea5)<0)
    return signal * XSELL

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
                ,sif.s5<0
                ,strend2(sif.sdiff30x)<0
            )
    return signal * ipmacd_short_devi1.direction
ipmacd_short_devi1.direction = XSELL
ipmacd_short_devi1.priority = 400


def ipmacd_short_devi1k(sif,sopened=None):
    '''
        顶背离操作，去掉了诸多条件
        尤其是xatr<2000
    '''

    trans = sif.transaction

    th = tmax(trans[IHIGH],120)
    th2 = tmax(trans[IHIGH],10)

    signal = gand(hdevi(trans[IHIGH],sif.sk,sif.sd)
                ,th2 == th
                )

    hh = hpeak(sif.high,sif.sk,sif.sd)

    ihh = np.nonzero(hh)[0]
    
    sh = np.zeros_like(sif.close)

    sh[ihh] = strend2(hh[ihh])

    sh = extend2next(sh)

    fsignal = strend2(sif.sk-sif.sd)<-1

    signal = sfollow(signal,fsignal,15)

    signal = gand(signal
                #,sh<0
                #,strend2(sif.sdiff5x)>0
                ,sif.diff1>0
                ,strend2(sif.diff1-sif.dea1)<0
                ,strend2(sif.sdiff5x-sif.sdea5x)<0  
                ,sif.ma3<sif.ma7
                ,strend2(sif.ma5)<0
                ,sif.ma5<sif.ma13
            )
    return signal * ipmacd_short_devi1.direction
ipmacd_short_devi1k.direction = XSELL
ipmacd_short_devi1k.priority = 1000


def ipmacd_long_devi1(sif,sopened=None):
    '''
        底背离操作，去掉了诸多条件
    '''

    trans = sif.transaction

    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤

    msignal = ldevi(trans[ILOW],sif.diff1,sif.dea1)

    s30_13 = np.zeros_like(sif.diff1)
    s30_13[sif.i_cof30] = strend2(ma(sif.close30,13))
    s30_13 = extend2next(s30_13)


    signal = gand(msignal
            ,s30_13 > 0
            #,dsfilter
            )

    return signal * XBUY
ipmacd_long_devi1.direction = XBUY
ipmacd_long_devi1.priority = 1000

def macd_bup(sif,sopened=None):
    '''
        底部抬高
        且前一个底部至少是中期低点
    '''

    trans = sif.transaction

    hh5 = hpeak(sif.high5,sif.diff5x,sif.dea5x)
    ll5 = lpeak(sif.low5,sif.diff5x,sif.dea5x,covered=15)

    ill = np.nonzero(ll5)[0]
    
    xll = ll5[ill]
    rxll = rollx(xll)
    rll5 = np.zeros_like(sif.close5)
    rll5[ill] = rxll


    ssl = np.zeros_like(sif.close5)
    sfilter = xll < rollx(tmin(xll,3))
    isignal = gand(xll>rxll
                ,rxll < rollx(tmin(xll,3),2)
                )
    ssl[ill[np.nonzero(isignal)]] = 1


    signal5 = gand(ssl
                )

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof5] = signal5

    signal = gand(signal
                #,sif.diff1>0
                #,sif.diff1>sif.dea1
                #,sif.sdiff5x>sif.sdea5x
                #,sif.ma3>sif.ma7
                #,strend(sif.ma13)>0
                #,strend(sif.ma30)>0
                #,strend(sif.ma13-sif.ma60)>0   
                #,strend(sif.diff1-sif.dea1)>0
                #,strend2(sif.sdiff5x)>0
                #,strend(sif.sdiff5x-sif.sdea5x)>0   
                #,strend(sif.sdiff30x-sif.sdea30x)>0
            )
    return signal * macd_bup.direction
macd_bup.direction = XBUY
macd_bup.priority = 2400

def skdj_bup3(sif,sopened=None):
    '''
        长期底部抬高
        长期底部的发现点是发现处，而不是底部处。如果是底部处，则会有未来数据
    '''

    trans = sif.transaction

    hh = hpeak(sif.high,sif.sk,sif.sd)
    ll = lpeak(sif.low,sif.sk,sif.sd)

    ihh = np.nonzero(hh)[0]
    ill = np.nonzero(ll)[0]
    
    sll = strend2(ll[ill])
    shh = strend2(hh[ihh])    

    i2ll = ill[np.nonzero(sll==3)[0]] #2阶底部
    sh = np.zeros_like(sif.close)
    sh[ihh] = shh
    sh = extend2next(sh)


    signal = np.zeros_like(sif.close)

    signal[i2ll] = 1

    signal = gand(signal
                #,sh>0
                #,strend2(sif.ma135)>0
                #,tmin(sif.low,60) == tmin(sif.low,300)
                ,sif.diff1>sif.dea1
                ,strend2(sif.diff1-sif.dea1)>0
                ,sif.sdiff5x>sif.sdea5x
                ,sif.ma3>sif.ma7
                ,strend(sif.ma13)>0
                #,strend(sif.ma30)>0
                #,strend(sif.ma13-sif.ma60)>0   
                #,strend(sif.diff1-sif.dea1)>0
                #,strend2(sif.sdiff5x)>0
                #,strend(sif.sdiff5x-sif.sdea5x)>0   
                #,strend(sif.sdiff30x-sif.sdea30x)>0
            )
    return signal * skdj_bup3.direction

skdj_bup3.direction = XBUY
skdj_bup3.priority = 2400


def ipmacd_long_devi1_o5(sif,sopened=None):
    '''
        底背离操作，使用了diff5
    '''

    trans = sif.transaction

    ksfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤

    msignal = ldevi(trans[ILOW],sif.diff1,sif.dea1)

    signal = gand(msignal
            #,strend(sif.diff1-sif.dea1) >= 3
            #,strend(sif.ma135-sif.ma270)>0
            #,strend(sif.diff5-sif.dea5)>0
            #,sif.s5>0
            #,ksfilter
            #,sif.s30>0
            #,sif.sdiff30x>0
            #,sif.sdiff5x<0
            )

    return signal * ipmacd_long_devi1_o5.direction
ipmacd_long_devi1_o5.direction = XBUY
ipmacd_long_devi1_o5.priority = 910


def ipmacd_shortt(sif,sopened=None):#+++
    ''' 
        R=828,times=4/5,2072
        30分钟下降途中反弹失败的情形
        忽略超过10点的瞬间下行导致的下叉
        被蕴含在ipmacd_short中, 添加了diff1<0,diff30>dea30
    '''
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)    
    signal = gand(cross(sif.dea1,sif.diff1)<0,sif.diff30>sif.dea30,sif.diff5<0,sif.diff30<0,ksfilter)#,strend(sif.diff5)>0)
    #signal = gand(signal,sif.ma5<sif.ma13,sif.xatr<2000)#,strend(sif.diff5-sif.dea5)<0)
    signal = gand(signal,strend(sif.ma30)<-4,strend(sif.ma13-sif.ma60)<0)
    
    return signal * XSELL


def ipmacd_short_b(sif,sopened=None):#+
    '''
        R=163,times=4/8
        忽略超过10点的瞬间下行导致的下叉

    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea1,sif.diff1)<0,sif.diff1>0,strend(sif.diff5-sif.dea5)<0,sif.diff30>sif.dea30,trans[IOPEN] - trans[ICLOSE] < 60,sif.diff5<0)#,strend(sif.diff5)>0)
    signal = gand(signal,strend(sif.ma60)<0,sif.xatr<2000)#,strend(sif.diff5-sif.dea5)<0)
    return signal * XSELL

def ipmacd_short_c(sif,sopened=None):#-
    '''
        忽略超过10点的瞬间下行导致的下叉
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea1,sif.diff1)<0,sif.diff1>0,sif.diff5<0,sif.diff30<0,sif.diff30>sif.dea30,trans[IOPEN] - trans[ICLOSE] < 60)#,strend(sif.diff5)>0)
    #signal = gand(signal,sif.xatr<2000)#,strend(sif.diff5-sif.dea5)<0)
    signal = gand(signal,strend(sif.ma60)<0,sif.xatr<2000)#,strend(sif.diff5-sif.dea5)<0)
    
    return signal * XSELL



def ipmacd_long_b(sif,sopened=None):#-
    '''
        忽略超过10点的瞬间下行导致的上叉
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea1,sif.diff1)>0,sif.diff1<0,sif.diff5>sif.dea5,sif.diff30<0,trans[IOPEN] - trans[ICLOSE] < 60)#,strend(sif.diff5)>0)
    signal = gand(signal,sif.xatr<1500)#,strend(sif.diff5-sif.dea5)<0)
    return signal * XBUY

def ipmacdx_long(sif,sopened=None):#+
    '''
        R=46,times=1/2
    '''
    trans = sif.transaction
    
    signal = gand(strend(sif.diff1-sif.dea1)==3,sif.diff1<sif.dea1,sif.diff30<sif.dea30,sif.diff5>sif.dea5,sif.diff5<0,sif.diff1<0,sif.diff1-sif.dea1 > -20,trans[ICLOSE] - trans[IOPEN] < 100)
    #signal = gand(strend(sif.diff1-sif.dea1)==3,sif.diff1<sif.dea1,sif.diff1>0,sif.diff5>sif.dea5, trans[ICLOSE] - trans[IOPEN] < 100,sif.ma5>sif.ma13)#,sif.ma13>sif.ma60)#,strend(sif.diff5)>0)
    #signal = gand(signal,sif.xatr<1500)
    signal = gand(sif.ma5>sif.ma13,strend(sif.ma5)>2,sif.diff30<sif.dea30,signal)
    
    return signal * XBUY

def ipmacdx_short(sif,sopened=None):#+
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    signal = gand(strend(sif.diff1-sif.dea1)==-2
            ,sif.diff1>sif.dea1
            ,sif.diff5<0
            ,strend(sif.diff5-sif.dea5)<0
            ,sif.diff1>0
            #,sif.diff5>sif.dea5
            )
    signal = gand(signal
            ,strend(sif.ma5)<0
            ,ksfilter
            )
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
        macd5上叉后，1分钟上叉
    '''
    trans = sif.transaction

    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤

    signal = gand(cross(sif.dea5,sif.diff5)>0,sif.diff5>0)

    s1 = fmacd1_long(sif,2)
    signal = sfollow(signal,s1,60)

    signal = gand(signal
            ,sif.diff5>0
            ,strend(sif.diff5-sif.dea5)>0                        
            ,strend(sif.diff30-sif.dea30)>0
            ,strend(sif.ma60)>10
            ,dsfilter
        )
    return signal * XBUY

def ipmacd_short5(sif,sopened=None):
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)
    
    signal = gand(cross(sif.dea5,sif.diff5)<0
            ,sif.diff5>0
            ,sif.diff30<0
            ,strend(sif.diff30-sif.dea30)<0
            )
    signal = gand(signal
            ,strend(sif.ma13-sif.ma60)<0
            ,strend(sif.ma135-sif.ma270)<0
            ,ksfilter
            )   
    return signal * ipmacd_short5.direction
ipmacd_short5.direction = XSELL
ipmacd_short5.priority = 550





def ma3x10_short(sif,sopened=None):#-
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)
    

    signal = gand(cross(sif.ma10,sif.ma3)<0
            ,strend2(sif.ma30)<=-4
            ,strend2(sif.diff30-sif.dea30)<0
            ,strend2(sif.ma7-sif.ma30)<0
            ,sif.diff30<0
            ,sif.diff5<0
            ,ksfilter
            )

    return signal * XSELL


def ma3x10_long(sif,sopened=None):#-
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤


    signal = gand(cross(sif.ma10,sif.ma3)>0
            ,strend2(sif.ma30)>=3
            #,strend2(sif.diff30-sif.dea30)>0
            ,strend2(sif.ma7-sif.ma30)>0
            #,strend2(sif.ma13-sif.ma60)>0
            #,strend2(sif.ma135-sif.ma270)>0
            #,strend2(sif.ma270)>0
            #,strend2(sif.ma135)>0
            #,sif.ma135 < sif.ma270
            ,sif.diff30>0
            #,sif.diff5>0
            #,sif.ma13 > sif.ma30
            #,sif.diff30 < sif.dea30
            #,sif.diff5 < sif.dea5
            ,dsfilter
            )

    return signal * XBUY


def ipmacd_short52(sif,sopened=None):#-
    '''
        忽略超过10点的瞬间下行导致的下叉
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea5,sif.diff5)<0,trans[IOPEN] - trans[ICLOSE] < 60)#,strend(sif.diff5)>0)
    signal1 = gand(cross(sif.dea1,sif.diff1)<0,trans[IOPEN] - trans[ICLOSE] < 60)
    signal = sfollow(signal,signal1,60)
    signal = gand(signal,strend(sif.ma60)<0,strend(sif.ma30)<0,sif.ma5<sif.ma13,sif.ma5<sif.ma30,sif.xatr<2000)#,strend(sif.diff5-sif.dea5)<0)
    
    return signal * XSELL

def ipmacd_short_1(sif,sopened=None):#+++
    trans = sif.transaction

    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    xopen=np.zeros(len(sif.diff1),np.int32)
    xopen[sif.i_oofd] = sif.opend
    xopen = extend2next(xopen)
    
    signal = gand(cross(sif.dea1,sif.diff1)<0
            ,sif.diff5<0
            ,sif.diff30<0
            ,strend2(sif.diff1-sif.dea1)<-2
            #,strend2(sif.diff1)<-2
            ,trans[IHIGH]<xopen
            )
    signal = gand(signal
            ,strend2(sif.ma30)<=-4
            ,ksfilter
            )
    signal = gand(signal
            #,strend(sif.ma13-sif.ma60)<0
            )#

    return signal * XSELL


def ipmacd_short_x2(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)


    signal = gand(cross(sif.dea1,sif.diff1)<0
            ,sif.mtrend < 0
            ,sif.s10<0
            ,sif.ltrend<0
            #,sif.sdiff5x<0
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

def ipmacd_short_5j(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    low60 = tmin(sif.low,60)
    flow = sif.low < rollx(low60)
    mf = msum(flow,30)

    signal = gand(cross(sif.dea1,sif.diff1)<0
            ,sif.ltrend>0
            ,sif.mtrend<0
            #,sif.sdiff5x<0
            ,sif.sdiff30x<0
            ,sif.mm<0
            ,sif.ml<0
            #,sif.diff1>0
            ,mf>0
            )
    signal = gand(signal
            ,sif.ma3 < sif.ma13
            ,strend2(sif.ma30)<0
            )
    return signal * ipmacd_short_5j.direction
ipmacd_short_5j.direction = XSELL
ipmacd_short_5j.priority = 1900


def ipmacd_short_5x(sif,sopened=None):
    '''
    '''
    ksfilter = gand(sif.open - sif.close < 60,rollx(sif.open - sif.close) < 120,sif.xatr<2000)

    rshort = 7
    rlong = 19
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    #signal = cross(rsib,rsia)<0    



    signal = gand(cross(sif.dea1,sif.diff1)<0
            #,sif.ltrend<0
            #,sif.strend<0
            ,sif.mm<0
            #,sif.ms<0
            #,sif.ml<0
            ,sif.rs_trend<0
            #,sif.s30<0
            ,strend2(sif.sdiff30x-sif.sdea30x)<0
            ,strend2(sif.sdiff5x-sif.sdea5x)<0            
            ,sif.sdiff5x<0
            ,sif.sdiff30x<sif.sdea30x
            )
    signal = gand(signal
            ,sif.ma5 < sif.ma13
            ,strend2(sif.ma30)<0
            ,sif.ma13<sif.ma30
            #,ksfilter
            )

    return signal * ipmacd_short_5x.direction
ipmacd_short_5x.direction = XSELL
ipmacd_short_5x.priority = 1000

def ipmacd_short_5k(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    sm = sif.ma270 - rollx(sif.ma270)
    ss2 = msum(sm,3)
    sss = strend(ss2)

    s30_13 = np.zeros_like(sif.diff1)
    s30_13[sif.i_cof30] = strend2(ma(sif.close30,13))
    s30_13 = extend2next(s30_13)


    sk5,sd5 = skdj(sif.high5,sif.low5,sif.close5)

    signal = gand(cross(sif.sd,sif.sk)<0
            #,strend(sif.diff1-sif.dea1)<0
            #,sif.diff1>sif.dea1
            #,strend2(sif.diff1-sif.dea1)<0
            ,strend2(sif.sdiff5x-sif.sdea5x)<0
            ,strend2(sif.sdiff30x-sif.sdea30x)<0            
            ,s30_13 < 0
            )
    signal = gand(signal
            ,sif.ma3 < sif.ma7
            ,strend2(sif.ma13)<0
            #,strend2(sif.ma270)<0            
            ,strend(sif.ma30)<0
            ,strend(sif.ma7-sif.ma30)<0
            #,ksfilter
            )

    #signal = gand(rollx(signal,1),sif.diff1<sif.dea1)
    return signal * ipmacd_short_5k.direction
ipmacd_short_5k.direction = XSELL
ipmacd_short_5k.priority = 1200

def ipmacd_short_5z(sif,sopened=None):
    '''
        顺势放空操作,长期逆势，中期顺势
    '''
    ksfilter = gand(sif.open - sif.close < 60,rollx(sif.open - sif.close) < 120,sif.xatr<2000)

    signal = gand(cross(sif.dea1,sif.diff1)<0
            ,sif.mtrend<0
            ,sif.ltrend>0
            ,sif.mm<0
            ,sif.ms<0
            )
    signal = gand(signal
            ,sif.ma5 < sif.ma13
            ,strend2(sif.ma30)<0
            ,ksfilter
            )

    return signal * ipmacd_short_5z.direction
ipmacd_short_5z.direction = XSELL
ipmacd_short_5z.priority = 1000


def ipmacd_short_5y(sif,sopened=None):
    '''
        顺势放空操作,长期逆势，短期顺势
    '''
    ksfilter = gand(sif.open - sif.close < 60,rollx(sif.open - sif.close) < 120,sif.xatr<2000)

    signal = gand(cross(sif.dea1,sif.diff1)<0
            ,sif.ms<0
            ,sif.mm<0
            ,sif.ml<0
            ,sif.rs_trend<0
            ,sif.ltrend>0
            ,sif.s1<0
            ,sif.sdiff3x<0
            ,sif.s30<0
            )
    signal = gand(signal
            ,sif.ma3<sif.ma13
            ,strend(sif.ma30)<0
            )

    return signal * ipmacd_short_5y.direction
ipmacd_short_5y.direction = XSELL
ipmacd_short_5y.priority = 1000


def ipmacd_long_5k(sif,sopened=None):
    dsfilter = gand(sif.close-sif.open<100,rollx(sif.close-sif.open)<200,sif.xatr<1500)#: 向上突变过滤

    sk5,sd5 = skdj(sif.high5,sif.low5,sif.close5)

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof5] = cross(sd5,sk5)

    signal = gand(signal
            ,strend2(sif.sdiff30x-sif.sdea30x)>0            
            ,sif.s5>0
            ,sif.s10>0
            ,sif.ma3 > sif.ma7
            ,strend(sif.ma30)>0
            ,strend(sif.ma7-sif.ma30)>0
            ,sif.rm_trend>0
            ,dsfilter
            )

    return signal * ipmacd_long_5k.direction
ipmacd_long_5k.direction = XBUY
ipmacd_long_5k.priority = 1200

def ipmacd_long_1k(sif,sopened=None):
    dsfilter = gand(sif.close-sif.open<100,rollx(sif.close-sif.open)<200,sif.xatr<1500)#: 向上突变过滤
    
    signal = gand(cross(sif.sd,sif.sk)>0
            ,sif.s30>0
            ,sif.s10>0
            ,sif.ma3 > sif.ma13
            ,strend(sif.ma30)>0
            ,strend(sif.ma7-sif.ma30)>0
            ,sif.rm_trend>0
            ,dsfilter
            )

    return signal * ipmacd_long_1k.direction
ipmacd_long_1k.direction = XBUY
ipmacd_long_1k.priority = 2250


def ipmacd_short_2(sif,sopened=None):#+++
    trans = sif.transaction

    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)
    signal = gand(cross(sif.dea1,sif.diff1)<0
            ,sif.diff5<0
            ,sif.diff30<0
            ,strend(sif.diff1)<-2)
    signal = gand(signal,sif.xatr<2000
            ,strend(sif.ma30)<=-4
            ,ksfilter)
    sdmacd = strend(sif.macd1 - rollx(sif.macd1))
    signal = gand(signal
            ,sdmacd<-1)#
    return signal * XSELL




def ipmacd_short_x1(sif,sopened=None):#+++
    ''' 
        先下叉，然后小于0(2个周期内)
    '''
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.diff5<0,sif.diff30<0)
    signal = gand(cross(sif.dea1,sif.diff1)<0,sfilter,sif.diff1>0)#,strend(sif.diff5)>0)
    #signal = gand(signal,strend(sif.ma5)<-1,sif.ma5<sif.ma13,sif.ma5<sif.ma30,strend(sif.ma60)<-5,sif.xatr<2000)#,strend(sif.diff5-sif.dea5)<0)

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
    signal = gand(signal,strend(sif.ma60)<0,strend(sif.ma30)<0,sif.ma5<sif.ma13,sif.ma5<sif.ma30,sif.xatr<2000)#,strend(sif.diff5-sif.dea5)<0)
    
    return signal * XSELL

def dmacd_short2(sif,sopened=None,rolled=1):#++
    '''
        rolled=1/2均可
        下降5或更多周期后上升rolled周期时放空
    '''
    trans = sif.transaction
    
    ksfilter= gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)#  向下突变过滤    
    
    sdd = strend(sif.diff1 - sif.dea1)
    
    signal = gand(sdd==rolled
                ,rollx(sdd,rolled)<-4
                ,sif.diff1>0
                ,sif.sdiff5x>0
                ,sif.sdiff30x>0
                ,sif.sdiff30x-sif.sdea30x<0
                ,ksfilter)

    return signal * XSELL

def dmacd_long2(sif,sopened=None,rolled=1):#++
    '''
        rolled=1/2均可
    '''
    trans = sif.transaction
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤

    sdd = strend(sif.diff1 - sif.dea1)
    signal = gand(sdd==rolled,rollx(sdd,rolled)<-4,sif.diff1-sif.dea1>0,rollx(sif.diff5,rolled)>0,rollx(sif.diff1,rolled)<0,sif.xatr<1500,sfilter)

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
    ksfilter = gand(trans[ICLOSE] - trans[IOPEN] < 60,rollx(trans[ICLOSE]) - trans[IOPEN] < 120,sif.xatr<1500)#: 向上突变过滤

    sdd = strend(sif.diff1 - sif.dea1)
    signal = gand(sdd==1
                ,rollx(sdd)<-4
                #,sif.diff1>sif.dea1
                #,sif.diff5>sif.dea5
                ,sif.diff5<0
                ,strend(sif.diff30-sif.dea30)>0
                ,strend(sif.diff5-sif.dea5)>0
                #,sif.diff30>0
                ,strend(sif.ma30)>3
                ,strend(sif.ma13-sif.ma60)>0
                ,strend(sif.ma135-sif.ma270)>0
                ,ksfilter
             ) 

    return signal * XBUY



def dmacd_long5(sif,sopened=None):#+++
    '''
        R=75,w/t=6/16
        回抽时未下叉又上涨
    '''
    trans = sif.transaction
    sdd = strend(sif.diff5 - sif.dea5)
    signal = gand(sdd==1,rollx(sdd)<-4,sif.diff5>sif.dea5,sif.diff5<0,trans[ICLOSE] - trans[IOPEN] < 100,sif.diff30<0,strend(sif.diff30<sif.dea30))
    #signal = gand(signal,sif.ma20>sif.ma60,strend(sif.ma60)>0)#,sif.ma13>sif.ma60)#,strend(sif.diff5)>0)


    return signal * XBUY

def dmacd_short5(sif,sopened=None):#+++
    trans = sif.transaction
    ksfilter= gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)#  向下突变过滤    

    sdd = strend(sif.diff5 - sif.dea5)
    signal = gand(sdd==-1,rollx(sdd)>4
            ,sif.diff5<sif.dea5
            ,sif.diff1<sif.dea1
            ,sif.diff30<0
            ,strend(sif.diff30-sif.dea30)<0
            )
    signal = gand(signal
            ,strend(sif.ma135-sif.ma270)<0            
            ,ksfilter
            )
    return signal * XSELL

def ama_short(sif,sopened=None): #+
    '''
        R=62,w/t=9/24
    '''
    trans = sif.transaction
    xama1 = ama1(trans[ICLOSE])
    xama2 = ama2(trans[ICLOSE])
    signal = gand(cross(xama2,xama1)<0
            ,strend(sif.sdiff5x-sif.sdea5x)<0
            ,strend(sif.sdiff30x-sif.sdea30x)<0
            ,strend(sif.diff1-sif.dea1)<0
            )

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
                ,sif.diff1> sif.dea1
                ,sif.s30>0
                ,sif.ma5>sif.ma13
                ,strend(sif.ma13)>0
                ,strend(sif.ma30)>0
            )
    return signal * skdj_bup.direction
skdj_bup.direction = XBUY
skdj_bup.priority = 1200



def up05_old(sif,sopened=None): #+
    '''
        抄底模式? 去掉
        R=190,w/t=5/10,1425
        [up0,up02]无叠加作用.5分钟上穿0的时候,早已经发出信号了
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    
    signal5 = gand(cross(cached_zeros(len(sif.diff5)),sif.diff5)>0,sif.diff30<0,sif.diff30<sif.dea30,dsfilter)
    signal = gand(signal5,strend(sif.ma60)>0,sif.ma5>sif.ma60,dsfilter)
    return signal * XBUY

def up05(sif,sopened=None): #+
    '''
        macd5上叉模式
        无涨幅和xatr约束
    '''
    trans = sif.transaction
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤
    
    signal = gand(cross(cached_zeros(len(sif.diff5)),sif.diff5)>0
                ,sif.diff30<0
                ,strend(sif.diff30-sif.dea30)>0
                ,strend(sif.ma60)>0
                ,sif.ma5>sif.ma13
                ,strend(sif.ma5-sif.ma30)>0                 
                ,strend(sif.ma135-sif.ma270)>0
              )
    return signal * XBUY


def up052(sif,sopened=None): #-
    '''
        R=71,w/t=4/13
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    
    signal5 = gand(cross(cached_zeros(len(sif.diff5)),sif.diff5)>0
            )
    signal1 = gand(cross(sif.dea1,sif.diff1)>0
                ,sif.diff5>0
                ,sif.diff30<0                
                ,sif.diff30<sif.dea30
                ,strend(sif.diff5-sif.dea5)>0
                ,strend(sif.diff30-sif.dea30)>0
                ,strend(sif.ma5-sif.ma30)>0
                ,strend(sif.ma135-sif.ma270)>0
                ,dsfilter
            )
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
    xs = gand(hdevi(trans[IHIGH],sif.diff1,sif.dea1),sif.diff5<0,sif.diff30<0,sif.xatr<2000)
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

    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    
    signal = ldevi(sif.low,sif.diff1,sif.dea1)
    signal = gand(signal
                #,strend2(sif.diff5)>0
                ,dsfilter
                )
    return signal * xldevi.direction
xldevi.direction = XBUY
xldevi.priority = 1000


def xldevi2(sif,sopened=None):#+
    '''

    '''
    trans = sif.transaction
    dsfilter = gand(trans[IOPEN] - trans[ICLOSE] < 100,rollx(trans[IOPEN]) - trans[ICLOSE] < 200,sif.xatr<1500)

    xs = gand(ldevi(trans[ILOW],sif.diff5,sif.dea5))#,sif.diff5<0)
    s1 = gand(cross(sif.dea1,sif.diff1)>0)
    signal = gand(sfollow(xs,s1,60)
                ,strend(sif.diff5-sif.dea5)>0
                ,sif.diff5<0
                ,strend(sif.diff30)<0
                ,strend(sif.ma60)<0
                #,strend(sif.ma135-sif.ma270)>0
                ,dsfilter
                )
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


    trans = sif.transaction
    '''

    mxc = xc0s(trans[IOPEN],trans[ICLOSE],trans[IHIGH],trans[ILOW],13)
    nx = extend2next(mxc).cumsum()
    snx = strend(nx)
    
    soc = gand(soc,snx>3)
    '''

    #xu = xcu(trans[IOPEN],trans[ICLOSE],trans[IHIGH],trans[ILOW],13,udfunc=supdowns)
    #upp = msum(xu>950,5) > 4
    
    xu = xcu(trans[IOPEN],trans[ICLOSE],trans[IHIGH],trans[ILOW],13,udfunc=supdowns)
    downp = msum(xu>950,5) > 4
    
    soc = gand(soc,downp)

    #soc = gand(soc,sif.diff5>sif.dea5)
    #soc = gand(soc,gand(sif.diff30<sif.dea30))
    return soc

def shortfilter(sif):  #在开盘前30分钟和收盘前5分钟不开仓，头三个交易日不开张
    soc = ocfilter(sif)

    trans = sif.transaction
    '''
    mxc = xc0s(trans[IOPEN],trans[ICLOSE],trans[IHIGH],trans[ILOW],13)
    nx = extend2next(mxc).cumsum()
    snx = strend(nx)
    soc = gand(soc,snx<-3)
    '''

    xu = xcu(trans[IOPEN],trans[ICLOSE],trans[IHIGH],trans[ILOW],13,udfunc=supdowns)
    downp = msum(xu<1050,5) > 4
    
    soc = gand(soc,downp)
    
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

