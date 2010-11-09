# -*- coding: utf-8 -*-

'''

主力合约、次月合约与半年合约的成交量还可以，下季合约严重没量，被操控
但因为次月合约开张日晚，如if1007在0524才开张，所以测试不准

主力合约转换
    当月合约最后3天左右开始转换。具体转换日为：
        下月合约持仓量超过当月合约的次日


#数据准备
from wolfox.fengine.ifuture.ifreader import read_ifs

from wolfox.fengine.ifuture.ibase import *
from wolfox.fengine.ifuture.ifreader import *
import wolfox.fengine.ifuture.ifreader as ifreader
import wolfox.fengine.ifuture.iftrade as iftrade
import wolfox.fengine.ifuture.ifuncs as ifuncs
import wolfox.fengine.ifuture.tfuncs as tfuncs
import wolfox.fengine.ifuture.dynamic as dynamic

from wolfox.fengine.ifuture.ifuncs import *


ifmap = read_ifs()  # fname ==> BaseObject(name='$name',transaction=trans)


###计算
i05 = ifmap['IF1005']
i06 = ifmap['IF1006']
i07 = ifmap['IF1007']
i08 = ifmap['IF1008']
i09 = ifmap['IF1009']
i12 = ifmap['IF1012']

trans = i08.transaction

i_cof5 = np.where(trans[ITIME]%5==0)    #5分钟收盘线,不考虑隔日的因素
i_cofd = np.where(trans[ITIME]==1514)   #日收盘线

sif = i08

#单个测试
#trades = iftrade.itrade(i06,[ifuncs.xx],[ifuncs.daystop_long,ifuncs.daystop_short,ifuncs.atr_xstop_15_6])
#trades = iftrade.itrade3x(i06,[ifuncs.xx])
tradesy = iftrade.itrade3x(i06,[tfuncs.tfunc])


sum([trade.profit for trade in tradesy])
sum([trade.profit>0 for trade in tradesy])
sum([trade.profit for trade in tradesy])/len(tradesy)
len(tradesy)
iftrade.R(tradesy)

iftrade.max_drawdown(tradesy)    #最大连续回撤和单笔回撤
iftrade.max_win(tradesy)         #最大连续盈利和单笔盈利

for trade in tradesy:print trade.profit,trade.actions[0].date,trade.actions[0].time,trade.actions[0].position,trade.actions[0].price,trade.actions[1].date,trade.actions[1].time,trade.actions[1].position,trade.actions[1].price,trade.actions[1].index-trade.actions[0].index



#顺势品种
xfollow = [ifuncs.ipmacd_short_1,ifuncs.ipmacd_short_2,ifuncs.ipmacd_short_3,ifuncs.ma3x10_short,ifuncs.down01,ifuncs.dmacd_short5,ifuncs.ipmacdx_short,ifuncs.ipmacd_short5,ifuncs.ma30_short,ifuncs.ma60_short]

#逆势品种. 慎用，不能依赖，只能在没有其它系列的情况下非常谨慎的使用
d22 = fcustom(ifuncs.dmacd_short2,rolled=2)
#xagainst = [ifuncs.ipmacd_long_devi1,ifuncs.dmacd_long,ifuncs.dmacd_short2,d22,ifuncs.down30]
xagainst = [ifuncs.dmacd_short2,d22,ifuncs.down30,ifuncs.up05] #dmacd_long被dms取代

#xagainst = [ifuncs.dmacd_short2,d22,ifuncs.down30]

#中间品种 dms基本被吸收，但在long_f和dms之间，选择dms
xmiddle = [ifuncs.ipmacd_longt,ifuncs.ipmacd_long5,ifuncs.xldevi2,ifuncs.dms,ifuncs.ipmacd_long_1,ifuncs.up0,ifuncs.dmacd_long5,ifuncs.ma60_long,ifuncs.ipmacd_long_devi1,ifuncs.xud30,ifuncs.xud30c]

#一般效益的品种, 主力品种, xud15存疑?  但是看起来xud15在其他市场的适应性不错?RU/CU/FU

trades1 = iftrade.itrade3x(i07,xfollow)
trades2 = iftrade.itrade3x(i07,xagainst)
trades3 = iftrade.itrade3x(i07,xmiddle)

###trades =  iftrade.itrade3x(i07,xfollow+xagainst+xmiddle)

#tradesy =  iftrade.itrade3y(i07,xfollow+xagainst+xmiddle)    #xfollow作为平仓信号，且去掉了背离平仓的信号
###tradesy =  iftrade.itrade3y05_25(i07,xfollow+xagainst+xmiddle)    #xfollow作为平仓信号，且去掉了背离平仓的信号

#貌似trade3x和trade3y不分上下

#优先级：xfollow最高，xmiddle次之，xagainst最后。 即如果现有持仓是xagainst/xmiddle 来的，那么之后的xfollow的反向信号将导致平仓并反向开仓

#把xfollow作为平仓条件加入。因为xfollow为顺势信号，所以一般不会出现一个xfollow信号干掉另一个xfollow信号的情况，除非在diff30穿越0线的过程中；

#优先级: xnormal > xpattern2 > xuds > xpattern >> xnormal2. 如果该优先级内出现反向信号，反向操作
# >xpattern3/xpattern4
#xpattern4与其它组合无增益
xnormal = [ifuncs.ipmacd_short_5,ifuncs.ipmacd_short_6a,ifuncs.ipmacd_long_5,ifuncs.gd30,ifuncs.gu30,ifuncs.ipmacd_long_5k,ifuncs.cci_up15]

#xpattern对远期合约的效果要好于近期的

#xpattern: 基于信号发出后再捕捉1分钟同向叉
xpattern = [ifuncs.godown5,ifuncs.godown30,ifuncs.inside_up,ifuncs.br30,ifuncs.ipmacd_short_devi1,ifuncs.ipmacd_long_devi1_o5]
xpattern2 = [ifuncs.goup5,ifuncs.opendown,ifuncs.openup,ifuncs.gapdown5,ifuncs.gapdown,ifuncs.skdj_bup,ifuncs.xdown30,ifuncs.xdown60]  

#xpattern2:直接根据信号动作
xpattern3 = [ifuncs.gapdown15,ifuncs.br75]  #互有出入
kpattern = [ifuncs.k5_lastup,ifuncs.k15_lastdown,ifuncs.k5_lastdown,ifuncs.k3_lastdown,ifuncs.k15_relay]

#xpattern4 = [ifuncs.xup,ifuncs.xdown,ifuncs.up3]   #与其它组合有矛盾? 暂不使用。盈利部分被其它覆盖，亏损部分没有，导致副作用

xuds = [ifuncs.xud30,ifuncs.xud30c,ifuncs.xud15]#,ifuncs.xud10s]

xnormal2 = [ifuncs.ipmacd_short_x,ifuncs.ipmacd_long_6,ifuncs.ipmacd_short5,ifuncs.ma30_short,ifuncs.ma60_short,ifuncs.down01,ifuncs.up0,ifuncs.rsi3x,ifuncs.skdj_bup,ifuncs.ipmacd_longt]

tradesy =  iftrade.itradex5_y(i05,xnormal+xnormal2+xpattern+xpattern2+xuds+xpattern3+kpattern)

#RU1011
ru = ifmap['RU1011']
fu = ifmap['FU1009']
cu = ifmap['CU1011']

s_short =[ifuncs.ipmacd_short,ifuncs.dmacd_short5]
s_long=[ifuncs.ipmacd_long5,ifuncs.ipmacd_long_f]   #稳定于RU1011

#输出到文件
fo = open('d:/temp/08xx.txt')
>>> for trade in tradesy:print >>fo,'%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (trade.profit,trade.actions[0].date,trade.actions[0].time,trade.actions[0].position,trade.actions[0].price,trade.actions[1].date,trade.actions[1].time,trade.actions[1].position,trade.actions[1].price,trade.actions[1].index-trade.actions[0].index,trade.functor)
fo.close()

#FU1009稳定
#CU1009不稳定
#跨市场特性比较难，只能是同一类的跨时间市场

#反向平仓，未必优

#合约交换日: 下月合约持仓量或成交量大于当月合约的次日
if1005:->517止
if1006:->617止
if1007:->714止
if1008:

#5月合约
sum([trade.profit for trade in tradesy if trade.actions[0].date<=20100517])
#6月合约
sum([trade.profit for trade in tradesy if trade.actions[0].date>20100517 and trade.actions[0].date<=20100617])
#7月合约
sum([trade.profit for trade in tradesy if trade.actions[0].date>20100617 and trade.actions[0].date<=20100714])
#8月合约
sum([trade.profit for trade in tradesy if trade.actions[0].date>20100714 and trade.actions[0].date<=20100818])

'''


from wolfox.fengine.ifuture.ibase import *
from wolfox.fengine.ifuture.iftrade import delay_filter,atr5_uxstop_1_25,atr5_uxstop_08_25,atr5_uxstop_05_25
import wolfox.fengine.ifuture.iftrade as iftrade


#5分钟系列以strend(ma60)为判断
#1分钟系列以strend(ma30)为判断

def fmacd1_long(sif,covered=3,sfilter=None):
    if sfilter != None:
        msignal = gand(cross(sif.dea1,sif.diff1)>0,sfilter)
    else:
        msignal = gand(cross(sif.dea1,sif.diff1)>0)

    fsignal = gand(strend(sif.diff1-sif.dea1) >= covered)   #上叉后仍然连续增长中
    signal = gand(rollx(msignal,covered),fsignal)
    return signal

def fmacd1_short(sif,covered=3,sfilter=None):
    if sfilter != None:
        msignal = gand(cross(sif.dea1,sif.diff1)<0,sfilter)
    else:
        msignal = gand(cross(sif.dea1,sif.diff1)<0)

    fsignal = gand(strend(sif.diff1-sif.dea1) <= -covered)   #上叉后仍然连续增长中

    signal = gand(rollx(msignal,covered),fsignal)
    return signal

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

    return signal * up3.direction
up3.direction = XBUY
up3.priority = 10000


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

    return signal * rsi3x.direction
rsi3x.direction = XBUY
rsi3x.priority = 3000  #

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
            #,sif.sdiff5x < sif.sdea5x
            )

    return signal * openup.direction
openup.direction = XBUY
openup.priority = 1000


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
godown30.priority = 2000

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
            ,ksfilter
            )
    
    return signal * xdown60.direction
xdown60.direction = XSELL
xdown60.priority = 1200 


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
            )


    return signal * inside_up.direction
inside_up.direction = XBUY
inside_up.priority = 2000



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

    return signal * gu30.direction
gu30.direction = XBUY
gu30.priority = 500




def gd30(sif,sopened=None):
    ''' 
        向下跳空
        并且收盘小于30分钟内的最低价
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    signal = gand(trans[IHIGH] < rollx(trans[ILOW])
            #,trans[IOPEN] > rollx(trans[IHIGH])
            ,trans[ITIME] > 915
        )

    signal = gand(signal
            ,trans[ICLOSE] < rollx(tmin(trans[ILOW],30))
            )

    signal = gand(signal
            ,strend2(sif.sdiff30x - sif.sdea30x)<0
            ,sif.sdiff5x < sif.sdea5x
            ,strend2(sif.ma135)<0
            #,sif.ma5<sif.ma13
            )

    return signal * gd30.direction
gd30.direction = XSELL
gd30.priority = 500


def gapdown(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    high30 = np.select([trans[ITIME][sif.i_cof30]==944],[sif.high30],default=0)

    xhighd,xlowd = np.zeros_like(sif.diff1),np.zeros_like(sif.diff1)
    xhighd[sif.i_cofd] = sif.highd

    xhighd = extend2next(xhighd)

    hgap = gand(trans[ILOW]>xhighd,trans[ITIME]==915)


    hgap = scover(hgap,260)   #当日信号都在缺口内发出

    signal = np.zeros_like(sif.diff1)

    signal = gand(cross(xhighd,sif.low)<0,hgap)

    signal = gand(signal
            ,sif.ma5  < sif.ma13
            ,strend(sif.ma30)<0
            )


    return signal * gapdown.direction
gapdown.direction = XSELL
gapdown.priority = 2400


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


    return signal * gapdown15.direction
gapdown15.direction = XSELL
gapdown15.priority = 2600



def gapdown5(sif,sopened=None):
    '''
        向上跳开后，5分钟补缺
        一次补失败后还可以补第二次
    '''


    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)
    
    high30 = np.select([trans[ITIME][sif.i_cof30]==944],[sif.high30],default=0)

    xhighd,xlowd = np.zeros_like(sif.diff1),np.zeros_like(sif.diff1)
    xhighd[sif.i_cofd] = sif.highd

    xhighd = extend2next(xhighd)

    hgap = gand(trans[ILOW]>xhighd,trans[ITIME]==915)


    hgap = scover(hgap,260)   #当日信号都在缺口内发出

    signal = np.zeros_like(sif.diff1)

    signal[sif.i_cof5] = gand(cross(xhighd[sif.i_cof5],sif.low5)<0,hgap[sif.i_cof5])


    return signal * gapdown5.direction
gapdown5.direction = XSELL
gapdown5.priority = 2400


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
            )


    return signal * br75.direction
br75.direction = XBUY
br75.priority = 2400


def xup(sif,sopened=None):
    '''
        创30分钟新高
    '''
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
              #,strend(sif.ma270)>0
            )

    return signal * xup.direction
xup.direction = XBUY
xup.priority = 10000


def xdown(sif,sopened=None):
    '''
        创30分钟新低
    '''
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
              #,strend(sif.ma270)<0
            )

    return signal * xdown.direction
xdown.direction = XSELL
xdown.priority = 10000


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
            )

    return signal * br30.direction
br30.direction = XBUY
br30.priority = 2410


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
            ,dsfilter
            )

    return signal * up0.direction
up0.direction = XBUY
up0.priority = 500  #叠加时，远期互有盈亏


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


def ma30_short_0630(sif,sopened=None):
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


def ma60_short_0715(sif,sopened=None):
    ''' ma60拐头
    '''
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)
 
    msignal = gand(strend(sif.ma60) == -1
                )
    fsignal = gand(cross(sif.dea1,sif.diff1)<0
                ,sif.diff30<0
                ,strend(sif.diff5-sif.dea5)>0
                ,strend(sif.ma5-sif.ma30)<0
                ,ksfilter                
                )
    signal = sfollow(msignal,fsignal,5)
    return signal * XSELL


def ma60_short_old(sif,sopened=None):
    ''' ma60拐头
    '''
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)
    
    msignal = gand(strend(sif.ma60) == -1,rollx(strend(sif.ma60))<10)
    fsignal = gand(cross(sif.dea1,sif.diff1)<0,strend(sif.diff5-sif.dea5)>0,sfilter,sif.xatr < 2000)
    signal = sfollow(msignal,fsignal,15)
    return signal * XSELL

def ma60_short_0630(sif,sopened=None):
    ''' ma60拐头
    '''
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)
    
    msignal = gand(strend(sif.ma60) == -1,rollx(strend(sif.ma60))<10)
    fsignal = gand(cross(sif.dea1,sif.diff1)<0,ksfilter,sif.diff30<0,strend(sif.diff5-sif.dea5)>0)
    signal = sfollow(msignal,fsignal,5)
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


def ma60_long_0630(sif,sopened=None):
    ''' ma60拐头
    '''
    trans = sif.transaction
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤
    msignal = gand(strend(sif.ma60) == 1,rollx(strend(sif.ma60))<-10)
    fsignal = gand(cross(sif.dea1,sif.diff1)>0,strend(sif.diff5-sif.dea5)>0,strend(sif.diff30-sif.dea30)>0)
    signal = gand(sfollow(msignal,fsignal,10),sfilter,sif.xatr<1500)
    return signal * XBUY


def ma60_long_old(sif,sopened=None):
    ''' ma60拐头
    '''
    trans = sif.transaction
    msignal = gand(strend(sif.ma60) == 1,rollx(strend(sif.ma60))<-10)
    fsignal = gand(cross(sif.dea1,sif.diff1)>0,strend(sif.diff5-sif.dea5)>0,strend(sif.diff30-sif.dea30)>0)
    signal = sfollow(msignal,fsignal,15)
    return signal * XBUY


def ipmacd_long_1(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤

    signal = gand(cross(sif.dea1,sif.diff1)>0
            ,sif.diff5>0
            ,strend(sif.diff30-sif.dea30)>0
            ,strend(sif.diff1)>2
            )
    signal = gand(signal
            ,strend(sif.ma30)>4
            ,strend(sif.ma13-sif.ma60)>0            
            ,strend(sif.ma135-sif.ma270)>0            
            ,dsfilter
            )

    return signal * XBUY


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

def ipmacd_longt_0630(sif,sopened=None):#+
    trans = sif.transaction
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200) #向上突变过滤
    ssma = gor(strend(sif.ma270)>0,strend(sif.ma135)>0)

    signal = gand(cross(sif.dea1,sif.diff1)>0,strend(sif.diff5-sif.dea5)>0,sif.sdiff30x<sif.sdea30x,sif.ma5>sif.ma13,strend(sif.ma5)>2,strend(sif.ma5-sif.ma30)>0,ssma)
    signal = gand(signal,sif.xatr<1500,sfilter)
    return signal * XBUY


def ipmacd_longt_old_a(sif,sopened=None):#+
    trans = sif.transaction
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200) #向上突变过滤
    signal = gand(cross(sif.dea1,sif.diff1)>0,strend(sif.diff5-sif.dea5)>0,sif.diff30<sif.dea30,sif.diff30<0,sif.ma5>sif.ma13,strend(sif.ma5)>2,strend(sif.ma5-sif.ma30)>0)
    signal = gand(signal,sif.xatr<1500,sfilter)
    return signal * XBUY

def ipmacd_longt_old_b(sif,sopened=None):#+
    trans = sif.transaction
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200) #向上突变过滤
    signal = gand(cross(sif.dea1,sif.diff1)>0,strend(sif.diff5-sif.dea5)>0,sif.diff30<sif.dea30,sif.diff30<0,sif.ma5>sif.ma13,strend(sif.ma5)>2,sfilter)
    signal = gand(signal,sif.xatr<1500)
    return signal * XBUY


def ipmacd_longt_old(sif,sopened=None):#+
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
    signal = gand(cross(sif.dea1,sif.diff1)>0,strend(sif.diff5-sif.dea5)>0,sif.diff30<sif.dea30,trans[ICLOSE] - trans[IOPEN] < 60,sif.ma5>sif.ma13,strend(sif.ma5)>2)#,sif.ma13>sif.ma60)#,strend(sif.diff5)>0)
    signal = gand(signal,sif.xatr<1500)
    return signal * XBUY

def ipmacd_long_devi1_old(sif,sopened=None):
    '''
        底背离操作，去掉了诸多条件
        操作方式:
            1. 底背离之后，必须macd连续增长4次或以上,过滤掉假突破
            2. 确保diff30<0,但是在增长，即macd>0或者macd向上
    '''

    trans = sif.transaction

    msignal = ldevi(trans[ILOW],sif.diff1,sif.dea1)
    fsignal = gand(strend(sif.diff1-sif.dea1) >= 3)   #上叉后仍然连续增长中

    signal = gand(rollx(msignal,3),fsignal,sif.diff30<0,gor(strend(sif.diff30-sif.dea30)>0,sif.diff30>sif.dea30),trans[ICLOSE]<sif.ma60)

    return signal * XBUY

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


def ipmacd_long_devi1(sif,sopened=None):
    '''
        底背离操作，去掉了诸多条件
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

    return signal * XBUY



def ipmacd_long_f_old(sif,sopened=None):
    '''
        过滤后的macd1下叉
        操作方式:
            1. 1分钟下叉
            2. 3分钟后macd仍然在延续往下,
            3. 5分钟macd(非1分钟扩大版)>0且上行中,5分钟diff<0
               30分钟(1分钟扩大版)macd<0,但在上行中
        貌似与emv_long冲突，因emv_long过于复杂，故选用ipmacd_long_f
    '''

    trans = sif.transaction

    sfilter = gand(strend(sif.sdiff5x-sif.sdea5x)>0,sif.sdiff5x>sif.sdea5x,sif.sdiff5x<0,sif.diff30<sif.dea30,strend(sif.diff30-sif.dea30)>0)
    #msignal = gand(cross(sif.dea1,sif.diff1)>0)
    #fsignal = gand(strend(sif.diff1-sif.dea1) >= 3)   #上叉后仍然连续增长中

    #signal = gand(rollx(msignal,3),fsignal,sfilter)
    signal = gand(fmacd1_long(sif,3),sfilter)

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

    sfilter = gand(strend(sif.diff5-sif.dea5)>0,sif.diff5>sif.dea5,sif.diff5<0,sif.diff30<sif.dea30,strend(sif.diff30-sif.dea30)>0)    
    sfilter2 = gand(trans[IOPEN] - trans[ICLOSE] < 100,rollx(trans[IOPEN]) - trans[ICLOSE] < 200)
    signal = gand(fmacd1_long(sif,3,sfilter),sif.xatr<1500,sfilter2)

    return signal * XBUY

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


def ipmacd_short_1_0712(sif,sopened=None):#+++
    trans = sif.transaction

    xopen=np.zeros(len(sif.diff1),np.int32)
    xopen[sif.i_oofd] = sif.opend
    xopen = extend2next(xopen)


    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)
    signal = gand(cross(sif.dea1,sif.diff1)<0
            ,sif.diff5<0
            ,sif.diff30<0
            ,strend(sif.diff1)<-2
            )
    signal = gand(signal
            ,strend2(sif.ma30)<=-4
            ,trans[IHIGH]<xopen
            ,ksfilter)
    signal = gand(signal
            #,strend(sif.ma13-sif.ma60)<0
            )#

    return signal * XSELL


def ipmacd_short_2(sif,sopened=None):#+++
    trans = sif.transaction

    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)
    signal = gand(cross(sif.dea1,sif.diff1)<0
            ,sif.diff5<0
            ,sif.diff30<0
            ,strend(sif.diff1)<-2)
    signal = gand(signal,sif.xatr < 2000
            ,strend2(sif.ma30)<=-4
            ,ksfilter)
    sdmacd = strend2(sif.macd1 - rollx(sif.macd1))
    signal = gand(signal
            ,sdmacd<-1
            )#
    #print signal[-50:]
    return signal * XSELL


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


def ipmacd_short_5(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)


    s30_13 = np.zeros_like(sif.diff1)
    s30_13[sif.i_cof30] = strend2(ma(sif.close30,13))
    s30_13 = extend2next(s30_13)

    signal = gand(cross(sif.dea1,sif.diff1)<0
            #,sif.diff30<0
            #,sif.diff5<0
            ,sif.sdiff30x<0
            ,sif.sdiff5x<0
            ,s30_13 < 0
            )
    signal = gand(signal
            ,sif.ma5 < sif.ma13
            ,sif.ma135<sif.ma270
            ,strend2(sif.ma30)<0
            ,ksfilter
            )
    return signal * ipmacd_short_5.direction
ipmacd_short_5.direction = XSELL
ipmacd_short_5.priority = 1000
#ipmacd_short_5.xfilter = fcustom(iftrade.delay_filter,delayed=15)

def ipmacd_long_5k(sif,sopened=None):
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

    signal = gand(cross(sif.sd,sif.sk)>0
            #,strend2(sif.diff1-sif.dea1)>0            
            ,strend2(sif.sdiff3x-sif.sdea3x)>0            
            #,strend2(sif.sdiff5x-sif.sdea5x)>0
            ,strend2(sif.sdiff30x-sif.sdea30x)>0            
            ,s30_13 > 0
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


def ipmacd_short_6a(sif,sopened=None):
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
            ,strend2(sif.sdiff30x-sif.sdea30x)<0
            #,sif.sdiff30x<sif.sdea30x
            ,s30_13 < 0
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
#ipmacd_short_6a.xfilter = fcustom(iftrade.delay_filter,delayed=10)

def ipmacd_short_x(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)


    s30_13 = np.zeros_like(sif.diff1)
    s30_13[sif.i_cof30] = strend2(ma(sif.close30,13))
    s30_13 = extend2next(s30_13)

    signal = gand(cross(sif.dea1,sif.diff1)<0
            ,strend2(sif.sdiff30x-sif.sdea30x)<0    #
            ,sif.sdiff5x<0
            ,s30_13 < 0
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


def ipmacd_long_5(sif,sopened=None):
    trans = sif.transaction

    dsfilter2 = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<2000)

    s30_13 = np.zeros_like(sif.diff1)
    s30_13[sif.i_cof30] = strend2(ma(sif.close30,13))
    s30_13 = extend2next(s30_13)

    signal = gand(cross(sif.dea1,sif.diff1)>0
            #,sif.diff30>0
            ,strend2(sif.sdiff30x-sif.sdea30x)>0
            #,sif.diff5>0
            ,sif.sdiff5x>0            
            ,s30_13 >0
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
              ,strend(sif.sdiff5x-sif.sdea5x)>0            
              ,strend(sif.sdiff30x-sif.sdea30x)>0
              ,strend(sif.ma30)>0
              ,strend(sif.ma13)>0
              ,strend(sif.ma7-sif.ma30)>0 
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

def skdj_bup3b(sif,sopened=None):
    '''
        底部抬高
        确定底部对左侧不需要一底比一底低，只需要该底低于前三个底即可
        叠加后无用
    '''

    trans = sif.transaction

    hh = hpeak(sif.high,sif.sk,sif.sd)
    ll = lpeak(sif.low,sif.sk,sif.sd)

    ihh = np.nonzero(hh)[0]
    ill = np.nonzero(ll)[0]
    
    xll = ll[ill]

    sh = np.zeros_like(sif.close)
    sl = np.zeros_like(sif.close)
    ssl = np.zeros_like(sif.close)
    sl3 = np.zeros_like(sif.close)

    sh[ihh] = strend2(hh[ihh])
    sl[ill] = strend2(ll[ill])
    #sl3[ill] = rollx(strend2(ll[ill]),3)

    
    sl3 = gand(xll<rollx(xll),xll<rollx(xll,2),xll<rollx(xll,3))
    lll = gand(strend2(ll[ill])==3,rollx(sl3,3))


    #print len(xll),len(lll),ill[np.nonzero(lll)]

    ssl[ill[np.nonzero(lll)]] = 1

    sh = extend2next(sh)

    signal = gand(sh>0,
                  ssl
                  )

    fsignal= gand(cross(sif.sd,sif.sk)>0
                ,sl>0
                )
    signal = sfollow(signal,fsignal,10)

    signal = gand(signal
                #,sif.diff1>0
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

skdj_bup3b.direction = XBUY
skdj_bup3b.priority = 12400


def ma3x10_short(sif,sopened=None):#
    '''
        无进一步增益，但胜在判断简单
    '''
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


def ipmacd_short_old(sif,sopened=None):#+++
    ''' 
        R=187,times=9/18,2788
        忽略超过10点的瞬间下行导致的下叉
        fmacd1_short无增益
    '''
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)
    signal = gand(cross(sif.dea1,sif.diff1)<0,sif.diff5<0,sif.diff30<0,sif.diff1<0,sfilter)#,strend(sif.diff5)>0)
    signal = gand(signal,strend(sif.ma5)<-1,sif.ma5<sif.ma13,sif.ma5<sif.ma30,strend(sif.ma60)<-5,sif.xatr < 2000)#,strend(sif.diff5-sif.dea5)<0)
    return signal * XSELL

def ipmacd_short_0630(sif,sopened=None):#+++
    trans = sif.transaction

    #ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)
    #signal = gand(cross(sif.dea1,sif.diff1)<0,strend(sif.diff1)<0,sif.diff5<0,sif.diff30<0,ksfilter) 
    #signal = gand(signal,strend(sif.ma30)<-4,strend(sif.ma13-sif.ma60)<0)
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)
    signal = gand(cross(sif.dea1,sif.diff1)<0,sif.diff5<0,sif.diff30<0,sfilter,strend(sif.diff1)<-2)#,strend(sif.diff5)>0)
    signal = gand(signal,sif.xatr < 2000,sif.ma5<sif.ma13,strend(sif.ma30)<-4,strend(sif.ma13-sif.ma60)<0)

    return signal * XSELL


def ipmacd_short_f(sif,sopened=None):#+
    ''' 
        带过滤的1分钟下叉
        1. 下叉后3分钟内仍然下行
        2. 5分钟macd<0,且macd下行中(这里的5分钟macd不是1分钟macd的扩周期版,而是真正的5分钟macd)
           diff30<0, 白线在上,但macd在下行中. 应该是反弹失败的类型
        不能和ipmacd_short共用，貌似short瞬间失败的那些会被short_f再次启用,会失败两次
            两者只能取一，目前舍弃short_f
    '''
    trans = sif.transaction
    #msignal = gand(cross(sif.dea1,sif.diff1)<0)#,sif.diff5<0,sif.diff30<0,sif.diff1<0,trans[IOPEN] - trans[ICLOSE] < 60)#,strend(sif.diff5)>0)
    #fsignal = gand(strend(sif.diff1-sif.dea1) <= -3)   #下叉后仍然连续下行中
    #signal = gand(rollx(msignal,3),fsignal)
    
    sfilter = gand(sif.sdiff5x<sif.sdea5x,strend(sif.sdiff5x-sif.sdea5x)<0,sif.diff30<0,strend(sif.diff30-sif.dea30)<0,sif.diff30>sif.dea30)
    #signal = gand(fmacd1_long(sif,3),sfilter,trans[IOPEN] - trans[ICLOSE] < 60)
    sfilter2 = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)
    signal = gand(fmacd1_short(sif,3),sfilter,sfilter2)#trans[IOPEN] - trans[ICLOSE] < 60)
    #signal = gand(signal,strend(sif.ma5)<-1,sif.ma5<sif.ma13,sif.ma5<sif.ma30,strend(sif.ma60)<-5,sif.xatr < 2000)#,strend(sif.diff5-sif.dea5)<0)
    return signal * XSELL

def ipmacd_short_x1(sif,sopened=None):#---
    ''' 
        先下叉，然后小于0(2个周期内)
        总体不佳
    '''
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.diff5<0,sif.diff30<0)
    signal = gand(cross(sif.dea1,sif.diff1)<0,sfilter,sif.diff1>0)#,strend(sif.diff5)>0)
    #signal = gand(signal,strend(sif.ma5)<-1,sif.ma5<sif.ma13,sif.ma5<sif.ma30,strend(sif.ma60)<-5,sif.xatr < 2000)#,strend(sif.diff5-sif.dea5)<0)

    #signal = gor(gand(rollx(signal,2),sif.diff1<0),gand(rollx(signal,1),sif.diff1<0))
    fsignal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1),sfilter,strend(sif.diff1-sif.dea1)<-2)
    signal = sfollow(signal,fsignal,3)

    return signal * XSELL



def ipmacd_shortt(sif,sopened=None):#+++
    ''' 
        R=828,times=4/5,2072
        30分钟下降途中反弹失败的情形
        忽略超过10点的瞬间下行导致的下叉
        被蕴含在ipmacd_short中, 添加了diff1<0,diff30>dea30
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea1,sif.diff1)<0,sif.diff1<0,sif.diff30>sif.dea30,sif.diff5<0,sif.diff30<0,trans[IOPEN] - trans[ICLOSE] < 60)#,strend(sif.diff5)>0)
    #signal = gand(signal,sif.ma5<sif.ma13,sif.xatr < 2000)#,strend(sif.diff5-sif.dea5)<0)
    signal = gand(signal,strend(sif.ma5)<-1,sif.ma5<sif.ma13,sif.ma5<sif.ma30,strend(sif.ma60)<-5,sif.xatr < 2000)#,strend(sif.diff5-sif.dea5)<0)
    
    return signal * XSELL

def ipmacd_short_devi1_old(sif,sopened=None):
    '''
        顶背离操作，去掉了诸多条件
        操作方式:
            1. 顶背离时买入, 必须diff5<0
            2. 买入后被卖出，则如果在背离发生的15分钟内出现绿柱减少后的增长，继续买入
               即向上反抽失败 
        R=171,w/t=5/9,1207

    '''

    trans = sif.transaction

    signal = gand(hdevi(trans[IHIGH],sif.diff1,sif.dea1),sif.diff5<0,trans[IOPEN] - trans[ICLOSE] < 60)


    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)
    fsignal = gand(strend(sif.diff1-sif.dea1)==-1,sif.diff5<0,sfilter)#trans[IOPEN] - trans[ICLOSE] < 60)

    signal = gor(signal,sfollow(signal,fsignal,15))

    return signal * XSELL

def ipmacd_short_devi1_0630(sif,sopened=None):
    '''
        顶背离操作，去掉了诸多条件
        0630废弃
    '''

    trans = sif.transaction

    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)

    signal = gand(hdevi(trans[IHIGH],sif.diff1,sif.dea1))

    fsignal = gand(strend(sif.diff1-sif.dea1)==-1)

    signal = gor(signal,gand(sfollow(signal,fsignal,15),msum(sif.diff1<sif.dea1,15)>9))

    signal = gand(signal,sif.diff5<0,sfilter,strend(sif.diff5-sif.dea5)<0,strend(sif.ma5-sif.ma13)<0)

    return signal * XSELL


def ipmacd_short_b(sif,sopened=None):#+
    '''
        R=163,times=4/8
        忽略超过10点的瞬间下行导致的下叉
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea1,sif.diff1)<0,sif.diff1>0,sif.diff5<sif.dea5,sif.diff30>sif.dea30,trans[IOPEN] - trans[ICLOSE] < 60)#,strend(sif.diff5)>0)
    signal = gand(signal,strend(sif.ma60)<0,sif.xatr < 2000)#,strend(sif.diff5-sif.dea5)<0)
    return signal * XSELL


def ipmacdx_short_old(sif,sopened=None):#+
    ''' 柱线变化
        R=176,w/t=6/9
    '''
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)

    signal = gand(strend(sif.diff1-sif.dea1)==-3,sif.diff1>sif.dea1,sif.diff30<0,strend(sif.diff5-sif.dea5)>0,sif.diff5<0,sif.diff1<0,sfilter)#trans[IOPEN] - trans[ICLOSE] < 60)
    #signal = gand(strend(sif.diff1-sif.dea1)==3,sif.diff1<sif.dea1,sif.diff1>0,sif.diff5>sif.dea5, trans[ICLOSE] - trans[IOPEN] < 100,sif.ma5>sif.ma13)#,sif.ma13>sif.ma60)#,strend(sif.diff5)>0)
    signal = gand(signal,strend(sif.ma5)<-1,sif.ma5<sif.ma30,sif.xatr < 2000)#,strend(sif.diff5-sif.dea5)<0)
    return signal * XSELL

def ipmacdx_short(sif,sopened=None):#+
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)

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


def ipmacdx_short_0630(sif,sopened=None):#+
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)

    signal = gand(strend(sif.diff1-sif.dea1)==-3,sif.diff1>sif.dea1,sif.diff30<0,strend(sif.diff5-sif.dea5)>0,sif.diff5<0,sif.diff1<0,sif.diff5<sif.dea5)
    signal = gand(signal,strend(sif.ma5)<-1,sif.ma5<sif.ma30,strend(sif.ma5-sif.ma30)<0,sif.xatr < 2000,sfilter)
    return signal * XSELL



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

def ipmacd_long5_0630(sif,sopened=None):#+
    '''
        R=432,times=4/6, 1195
    '''
    trans = sif.transaction

    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤

    signal = gand(cross(sif.dea5,sif.diff5)>0,sif.diff5>0)

    sfilter2 = gand(strend(sif.diff5)>2,sif.diff5>0,sfilter,strend(sif.diff30-sif.dea30)>0,sif.ma5>sif.ma13)
    #s1 = gand(cross(sif.dea1,sif.diff1)>0,sfilter)#,sif.xatr<1500)
    s1 = gand(fmacd1_long(sif,3),sfilter2,sif.xatr<1500)
    #s1 = gand(cross(sif.dea1,sif.diff1)>0)
    signal = sfollow(signal,s1,60)
    return signal * XBUY

def ipmacd_long5_old(sif,sopened=None):#+
    '''
        R=432,times=4/6, 1195
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea5,sif.diff5)>0,sif.diff5>0)
    #s1 = gand(cross(sif.dea1,sif.diff1)<0,sif.diff5>sif.dea5,sif.diff5>0,trans[ICLOSE] - trans[IOPEN] < 100)
    sfilter = gand(sif.diff5>sif.dea5,sif.diff5>0,trans[ICLOSE] - trans[IOPEN] < 100,strend(sif.diff30-sif.dea30)>0)
    #s1 = gand(cross(sif.dea1,sif.diff1)>0,sfilter)#,sif.xatr<1500)
    s1 = gand(fmacd1_long(sif,2),sfilter)#,sif.xatr<1500)
    signal = sfollow(signal,s1,60)
    signal = gand(sif.ma5>sif.ma13,signal)
    return signal * XBUY

def ipmacd_short5_old(sif,sopened=None):#-
    '''
        R=166,w/t=6/12
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea5,sif.diff5)<0,sif.diff5>0,trans[IOPEN] - trans[ICLOSE] < 60)#,strend(sif.diff5)>0)
    #s1 = gand(cross(sif.dea1,sif.diff1)<0,sif.diff5<sif.dea5,sif.xatr < 2000)
    #signal = sfollow(signal,s1,60)
    signal = gand(signal,strend(sif.ma60)<0,strend(sif.ma30)<0,sif.ma5<sif.ma13,sif.ma5<sif.ma30,sif.xatr < 2000)#,strend(sif.diff5-sif.dea5)<0)
    
    return signal * XSELL



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
ipmacd_short5.priority = 2000


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
            #,sif.ma5>sif.ma13
            #,dsfilter
            )


    return signal * xud15.direction
xud15.direction = XBUY
xud15.priority = 3001


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


def dmacd_short2_old(sif,sopened=None):#++
    '''
        R=304,times=4/5
        回抽时未下叉又上涨
    '''
    trans = sif.transaction
    sdd = strend(sif.diff1 - sif.dea1)
    signal = gand(sdd==1,rollx(sdd)<-1,sif.diff1>sif.dea1, trans[IOPEN] - trans[ICLOSE] < 60,sif.diff5>0,sif.diff30>0,sif.diff1>0,sif.xatr < 2000)

    return signal * XSELL

def dmacd_long5(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤

    sdd = strend(sif.diff5 - sif.dea5)
    signal = gand(sdd==1,rollx(sdd)<-4
            ,sif.diff1 < 0
            ,sif.diff5 < 0
            #,sif.diff1>sif.dea1
            ,strend(sif.diff1-sif.dea1)>0
            ,strend(sif.diff5-sif.dea5)>0            
            ,strend(sif.diff30-sif.dea30)>0
            )
    signal = gand(signal
            ,strend(sif.ma135-sif.ma270)>0
            ,strend(sif.ma13-sif.ma60)>0
            ,sif.ma5>sif.ma13
            ,dsfilter
            )

    return signal * XBUY


def dmacd_short5(sif,sopened=None):#+++
    '''
        macd5上行5周期或之上后下行, 下行时macd5<0 (一直是绿线)
    '''

    trans = sif.transaction
    ksfilter= gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)#  向下突变过滤    

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


def dmacd_short5_0630(sif,sopened=None):#+++
    trans = sif.transaction
    sfilter= gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)#  向下突变过滤    

    sdd = strend(sif.diff5 - sif.dea5)
    signal = gand(sdd==-1,rollx(sdd)>4,sif.diff5<sif.dea5,sif.diff1<sif.dea1,sif.diff30>sif.dea30,sif.diff30<0,strend(sif.diff30-sif.dea30)<0)
    signal = gand(signal,sif.ma5<sif.ma13,sfilter,sif.xatr < 2000,strend(sif.ma13-sif.ma60)<0)
    
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
                ,sif.diff5>0
                ,sif.diff30>0
                ,sif.diff30-sif.dea30<0
                ,ksfilter)

    return signal * XSELL


def dmacd_short2_0630(sif,sopened=None,rolled=1):#++
    '''
        rolled=1/2均可
    '''
    trans = sif.transaction
    sfilter= gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)#  向下突变过滤    
    sdd = strend(sif.diff1 - sif.dea1)
    signal = gand(sdd==rolled,rollx(sdd,rolled)<-4,sif.diff1-sif.dea1>0,rollx(sif.diff5,rolled)>0,rollx(sif.diff30,rolled)>0,rollx(sif.diff1,rolled)>0,sif.xatr < 2000,sfilter)

    return signal * XSELL


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
    signal = gand(signal,strend(sif.ma30)>0,sif.xatr<1500)

    return signal * XBUY


def dmacd_short5_old(sif,sopened=None):#+++
    ''' 
        R=436,times=5/8,2072
        回抽时未上叉又回落
    '''
    trans = sif.transaction
    sdd = strend(sif.diff5 - sif.dea5)
    signal = gand(sdd==-1,rollx(sdd)>4,sif.diff5<sif.dea5,trans[IOPEN] - trans[ICLOSE] < 60,sif.diff30>sif.dea30,sif.diff30<0,strend(sif.diff30-sif.dea30)<0)
    #signal = gand(signal,strend(sif.ma60)<0,sif.xatr < 2000)#,strend(sif.diff5-sif.dea5)<0)
    #signal = sfollow(signal,fmacd1_short(sif,3))
    signal = gand(signal,strend(sif.ma60)<0,sif.xatr < 2000,sif.ma5<sif.ma13)
    
    return signal * XSELL

def emv_short(sif,sopened=None):#+
    '''
        R=120,w/t=5/12,1035
        #与其它叠加有反作用
        #这个貌似是抄底的
    '''
    trans = sif.transaction
    semv = emv(trans[HIGH],trans[LOW],trans[IVOL])
    signal = gand(cross(cached_zeros(len(semv)),semv)<0,sif.diff5<sif.dea5,sif.diff5>0,strend(sif.diff5-sif.dea5)>0) 
    signal = gand(signal,strend(sif.ma30)<0,sif.ma5>sif.ma30)
    return signal * XSELL

def emv_short2(sif,sopened=None):#+
    '''
        R=181,w/t=3/7,551
        #与其它叠加有反作用
    '''
    trans = sif.transaction
    semv = emv(trans[HIGH],trans[LOW],trans[IVOL])
    signal = gand(cross(cached_zeros(len(semv)),semv)<0,sif.diff5<sif.dea5,sif.diff5>0,strend(sif.diff5-sif.dea5)>0) 
    signal1 = gand(cross(sif.dea1,sif.diff1)<0,sif.diff5<sif.dea5,strend(sif.diff5-sif.dea5)>0,trans[IOPEN] - trans[ICLOSE] < 60)
    signal = sfollow(signal,signal1,30)
    signal = gand(signal,strend(sif.ma60)<0)
    
    return signal * XSELL

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

def down30_0630(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)

    msignal = gand(cross(sif.dea30,sif.diff30)<0)
    fsignal = gand(cross(cached_zeros(len(sif.dea1)),sif.diff1)<0,sif.diff30>0)
    
    signal = sfollow(msignal,fsignal,120)

    signal = gand(signal,ksfilter,sif.xatr < 2000)

    return signal*XSELL

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
            ,strend2(sif.sdiff30x-sif.sdea30x)>0
            ,strend2(sif.ma13)>0
            )

    return signal * cci_up15.direction
cci_up15.direction = XBUY
cci_up15.priority = 2900#900 


def down30(sif,sopened=None):
    '''
        macd30下叉时
    '''
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)

    msignal = cross(sif.dea30,sif.diff30)<0
    
    fsignal = cross(cached_zeros(len(sif.dea1)),sif.diff1)<0
    
    signal = sfollow(msignal,fsignal,135)

    signal = gand(signal
                ,sif.diff30>0
                ,strend(sif.ma135-sif.ma270)<0
                ,ksfilter)

    return signal*XSELL

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
ipmacd_short_devi1.priority = 1000

def down01_old(sif,sopened=None): #++
    ''' 
        R=104,times=5/13
        30分钟框架下的下行，5分钟框架的上行，以及1分钟的下行
        去掉
    '''
    trans = sif.transaction
    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1)<0,sif.diff1<sif.dea1,sif.diff5>sif.dea5,sif.dea5>0,sif.diff30<sif.dea30,trans[IOPEN] - trans[ICLOSE] < 60)
    return signal * XSELL

def down01_0630(sif,sopened=None): #++
    ''' 
        30分钟<0且下行
        5分钟>0且下行
        1分钟下叉, 且一分钟下行3分钟或以上
    '''
    trans = sif.transaction
    sfilter= gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)#  向下突变过滤

    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1)<0,strend(sif.diff5-sif.dea5)<0,sif.diff5>0,strend(sif.diff30-sif.dea30)<0,sif.diff30<0,strend(sif.diff1)<-2)
    return signal * XSELL

def down01(sif,sopened=None): #++
    ''' 
        30分钟<0且下行
        5分钟>0且下行
    '''
    trans = sif.transaction
    ksfilter= gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)#  向下突变过滤

    s30_13 = np.zeros_like(sif.diff1)
    s30_13[sif.i_cof30] = strend2(ma(sif.close30,13))
    s30_13 = extend2next(s30_13)


    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1)<0
            ,sif.sdiff5x>0
            ,sif.sdiff30x<0
            ,strend(sif.diff1-sif.dea1)<-2            
            ,strend(sif.ma5-sif.ma30)<0
            ,strend(sif.ma135-sif.ma270)<0            
            ,strend(sif.ma30)<0
            ,ksfilter
            )
    return signal * down01.direction
down01.direction = XSELL
down01.priority = 250

def down01_0715(sif,sopened=None): #++
    ''' 
        30分钟<0且下行
        5分钟>0且下行
    '''
    trans = sif.transaction
    ksfilter= gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)#  向下突变过滤

    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1)<0
            ,sif.diff5>0
            ,sif.diff30<0
            ,strend(sif.diff1-sif.dea1)<-2            
            ,strend(sif.diff5-sif.dea5)<-2
            ,strend(sif.diff30-sif.dea30)<0
            ,strend(sif.ma5-sif.ma30)<0
            ,strend(sif.ma135-sif.ma270)<0            
            ,strend(sif.ma30)<0            
            ,ksfilter
            )
    return signal * XSELL


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
    return signal * xldevi2.direction
xldevi2.direction = XBUY
xldevi2.priority = 1000



def xldevi2_old(sif,sopened=None):#+
    '''
        R=100,times=2/2,501
        样本太少
    '''
    trans = sif.transaction
    xs = gand(ldevi(trans[ILOW],sif.diff5,sif.dea5),sif.diff5<0)
    s1 = gand(cross(sif.dea1,sif.diff1)>0,sif.diff5<0,sif.diff5>sif.dea5,sif.xatr<1500,strend(sif.diff30)<0)
    signal = sfollow(xs,s1,60)
    #signal = gand(signal,strend(sif.ma30)>0)
    return signal * XBUY


def xldevi2_0630(sif,sopened=None):#+
    '''
    '''
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 100,rollx(trans[IOPEN]) - trans[ICLOSE] < 200)

    xs = gand(ldevi(trans[ILOW],sif.diff5,sif.dea5))#,sif.diff5<0)
    s1 = gand(cross(sif.dea1,sif.diff1)>0,sfilter,sif.xatr<1500,strend(sif.diff5-sif.dea5)>0,sif.diff5<0,strend(sif.ma60)<0)
    signal = sfollow(xs,s1,60)
    return signal * XBUY


def xhdevi1(sif,sopened=None):#+
    '''
        弱势条件下的1分钟顶背离
    '''
    trans = sif.transaction
    xs = gand(hdevi(trans[IHIGH],sif.diff1,sif.dea1),sif.diff5<0,sif.diff30<0,sif.xatr < 2000)
    return xs * XSELL


def emv_long(sif,sopened=None):#+--
    '''
        R=136,w/t=3/6,637
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
            )

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

    rshort,rlong = 7,19
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
 
    fsignal = gand(cross(rsib,rsia)>0
            ,strend2(rsia)>0
            )

    #signal = sfollow(signal,fsignal,30)

    signal = gand(signal
            #,strend2(sif.sdiff30x-sif.sdea30x)>0
            #,sif.diff1>0
            #,sif.sdiff5x>0
            #,strend(sif.ma7)>0
            #,rollx(strend2(sif.sdiff5x-sif.sdea5x),5)>0
            ,sif.r120>0
            ,sif.s30 > 0
            #,sif.ma3 > sif.ma13
            )

    return signal * k5_relay.direction
k15_relay.direction = XBUY
k15_relay.priority = 1200 #对i07效果很差


def x5_lastdown(sif,sopened=None):
    '''
        新高衰竭模式
        1. 3分钟长上影新高后,5分钟内1分钟跌破前5分钟的最低价
        适用于远期合约?
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
x5_lastdown.priority = 21600 #对i09时200即优先级最高的效果最好


def ma2x(sif,sopened=None):
    s30_13 = np.zeros_like(sif.diff1)
    s30_13[sif.i_cof30] = strend2(ma(sif.close30,13))
    s30_13 = extend2next(s30_13)
    
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
              ,s30_13>0
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
              ,strend2(sif.sdiff30x-sif.sdea30x)>0
              ,sif.diff1>0
              ,sif.ma5>sif.ma13
              ,strend(sif.ma30)>0
            )

    return signal * s5.direction
s5.direction = XBUY
s5.priority = 1200



def imacd_stop5(sif,sopened=None):
    trans = sif.transaction
    sell_signal = lesser(cross(sif.dea5,sif.diff5),0) * XSELL
    buy_signal = greater(cross(sif.dea5,sif.diff5),0) * XBUY
    return sell_signal + buy_signal

def imacd_stop1(sif,sopened=None):
    trans = sif.transaction
    sell_signal = lesser(cross(sif.dea1,sif.diff1),0) * XSELL
    buy_signal = greater(cross(sif.dea1,sif.diff1),0) * XBUY
    return sell_signal + buy_signal

#def xdevi_stop1(sif,sopened=None):
#    trans = sif.transaction
#    sell_signal = gand(hdevi(trans[IHIGH],sif.diff1,sif.dea1)) * XSELL
#    buy_signal = gand(ldevi(trans[IHIGH],sif.diff1,sif.dea1)) * XBUY
#    return sell_signal + buy_signal
 
def xdevi_stop1(sif,sopened=None):
    trans = sif.transaction
    sell_signal = gand(hdevi(trans[IHIGH],sif.diff1,sif.dea1),sif.diff5<0,sif.diff30<0) * XSELL
    buy_signal = gand(ldevi(trans[IHIGH],sif.diff1,sif.dea1),sif.diff5>0,sif.diff30>0) * XBUY
    return sell_signal + buy_signal

def xdevi_stop_short1(sif,sopened=None):#平空头
    trans = sif.transaction
    buy_signal = gand(ldevi(trans[IHIGH],sif.diff1,sif.dea1),sif.diff5>0,sif.diff30>0,sif.diff30>sif.dea30) * XBUY
    return buy_signal

def xdevi_stop_short1x(sif,sopened=None):#平空头
    trans = sif.transaction
    buy_signal = gand(ldevi(trans[IHIGH],sif.diff1,sif.dea1),sif.diff1<0,sif.diff30>sif.dea30) * XBUY
    return buy_signal


def xdevi_stop_long1(sif,sopened=None):#平多头
    trans = sif.transaction
    sell_signal = gand(hdevi(trans[IHIGH],sif.diff1,sif.dea1),sif.diff5<0,sif.diff30<0,sif.diff30<sif.dea30) * XSELL
    return sell_signal 



def xdevi_stop5(sif,sopened=None):
    trans = sif.transaction
    sell_signal = gand(hdevi(trans[IHIGH],sif.diff5,sif.dea5)) * XSELL
    buy_signal = gand(ldevi(trans[IHIGH],sif.diff5,sif.dea5)) * XBUY
    return sell_signal + buy_signal

def xmacd_stop1(sif,sopened=None):
    '''
        如果买入当时就发生一分钟反向叉，则即刻止损
    '''
    trans = sif.transaction
    sell_signal = gand(cross(sif.dea1,sif.diff1)<0,equals(rollx(sopened),XBUY)) * XSELL
    buy_signal = gand(cross(sif.dea1,sif.diff1)>0,equals(rollx(sopened),XSELL)) * XBUY 
    return sell_signal + buy_signal

def xmacd_stop_short1(sif,sopened=None):
    '''
        平空头，买入后一分钟即刻上叉
    '''
    trans = sif.transaction
    #print 'in xmacd_stop_short'
    buy_signal = gand(cross(sif.dea1,sif.diff1)>0,equals(np.sign(sopened),SHORT)) * XBUY 
    return buy_signal

def xmacd_stop_long1(sif,sopened=None):
    '''
        平多头，买入后一分钟即刻下叉
    '''
    trans = sif.transaction
    sell_signal = gand(cross(sif.dea1,sif.diff1)<0,equals(np.sign(sopened),LONG)) * XSELL
    return sell_signal


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

def daystop_long(sif,sopened,tend=1511):
    '''
        每日收盘前的平仓,平多仓
        最后3分钟也平仓，用于兼容到期日(最后交易时间为1500)
    '''
    stime = sif.transaction[ITIME]
    sl = greater(stime,tend)
    sl[-4:] = 1
    return  sl * XSELL

daystop_long_c = fcustom(daystop_long,tend=1456)

def daystop_short(sif,sopened,tend=1511):
    '''
        每日收盘前的平仓,平空仓
        最后3分钟也平仓，用于兼容到期日(最后交易时间为1500)
    '''
    stime = sif.transaction[ITIME]
    sl = greater(stime,tend)
    sl[-4:] = 1
    return sl * XBUY

daystop_short_c = fcustom(daystop_short,tend=1456)

def xdaystop_long(sif,sopened,tend=1511):
    '''
        每日收盘前的平仓,平多仓
        最后3分钟不平仓
        用于动态计算
    '''
    stime = sif.transaction[ITIME]
    sl = greater(stime,tend)
    return  sl * XSELL

xdaystop_long_c = fcustom(xdaystop_long,tend=1456)


def xdaystop_short(sif,sopened,tend=1511):
    '''
        每日收盘前的平仓,平空仓
        最后3分钟不平仓.
        用于动态计算
    '''
    stime = sif.transaction[ITIME]
    sl = greater(stime,tend)
    return sl * XBUY

xdaystop_short_c = fcustom(xdaystop_short,tend=1456)

def atr_xstop(sif,sopened,lost_times=200,win_times=300,max_drawdown=200,min_lost=30):
    '''
        atr止损
        sif为实体
        sopen为价格序列，其中负数表示开多仓，正数表示开空仓
        谨慎处理重复开仓的问题，虽然禁止了重复开仓，但后面的同向仓会影响止损位，或抬高止损位
            即止损位会紧跟最新的那个仓，虽然未开，会有严重影响, 需要测试
        对于按照macd上叉买入的情况，如果买入时即刻下叉，则直接卖出
    '''
    trans = sif.transaction
    rev = np.zeros_like(sopened)
    isignal = np.nonzero(sopened)[0]
    ilong_closed = 0    #多头平仓日
    ishort_closed = 0   #空头平仓日
    esmacd = strend(sif.diff1-sif.dea1)
    for i in isignal:
        price = sopened[i]
        willlost = sif.atr[i] * lost_times / XBASE / XBASE
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
            win_stop = cur_high - sif.atr[i] * win_times / XBASE / XBASE
            cur_stop = lost_stop if lost_stop > win_stop else win_stop
            #print 'eval:',trans[IDATE][i],trans[ITIME][i],sif.diff1[i],sif.dea1[i]
            if trans[ICLOSE][i] < cur_stop: #or smacd[i]<0:#到达止损或买入后即刻下叉，说明买入错误
                #print '----sell----------:',trans[IDATE][i],trans[ITIME][i],cur_stop,trans[ICLOSE][i],cur_high,lost_stop
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
                        drawdown = sif.atr[j] * win_times / XBASE / XBASE
                        if drawdown > max_drawdown:
                            drawdown = max_drawdown
                        win_stop = cur_high - drawdown
                        #win_stop = cur_high - sif.atr[j] * win_times / XBASE / XBASE
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
            win_stop = cur_low + sif.atr[i] * win_times / XBASE / XBASE
            cur_stop = lost_stop if lost_stop < win_stop else win_stop
            if trans[ICLOSE][i] > cur_stop :#or smacd[i]>0:
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
                        drawdown = sif.atr[j] * win_times / XBASE / XBASE
                        if drawdown > max_drawdown:
                            drawdown = max_drawdown
                        win_stop = cur_low + drawdown
                        #print nlow,cur_stop,win_stop,sif.atr[j]
                        #win_stop = cur_low + sif.atr[j] * win_times / XBASE / XBASE
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



xnormal = [ipmacd_short_5,ipmacd_short_6a,ipmacd_long_5,ipmacd_long_x,ipmacd_short_x2,gd30,gu30,ipmacd_long_5k,cci_up15,ma2x,s5,ma1x]
xpattern = [godown5,godown30,inside_up,br30,ipmacd_short_devi1,ipmacd_long_devi1_o5]
xpattern2 = [goup5,opendown,openup,gapdown5,gapdown,skdj_bup,xdown30,xdown60]  
xpattern3 = [gapdown15,br75]  #互有出入
kpattern = [k5_lastup,k15_lastdown,k5_lastdown,k3_lastdown,k15_relay]   #逆势指标
#xpattern4 = [xup,xdown,up3]   #与其它组合有矛盾? 暂不使用。盈利部分被其它覆盖，亏损部分没有，导致副作用
xuds = [xud30,xud30c,xud15,xud10s,xud10l]
xnormal2 = [ipmacd_short_x,ipmacd_long_6,ipmacd_short5,ma30_short,ma60_short,down01,up0,rsi3x,ipmacd_longt]
xxx = xnormal+xnormal2+xpattern+xpattern2+xuds+xpattern3+kpattern
xpattern4 = [xup,xdown,up3]   #与其它组合有矛盾? 暂不使用。盈利部分被其它覆盖，亏损部分没有，导致副作用
xxx4 = xxx + xpattern4
#tradesy =  iftrade.itradex5_y(i05,xxx)
#tradesy =  iftrade.itradex5_y(i05,xxx4,priority_level=3000)
for x in xxx4:
    x.cstoper = iftrade.FBASE_30  #初始止损
