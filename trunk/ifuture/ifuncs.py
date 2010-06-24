# -*- coding: utf-8 -*-

'''

主力合约、次月合约与半年合约的成交量还可以，下季合约严重没量，被操控
但因为次月合约开张日晚，如if1007在0524才开张，所以测试不准

#数据准备
from wolfox.fengine.ifuture.ifreader import read_ifs

from wolfox.fengine.ifuture.ibase import *
from wolfox.fengine.ifuture.ifreader import *
import wolfox.fengine.ifuture.iftrade as iftrade
import wolfox.fengine.ifuture.ifuncs as ifuncs
import wolfox.fengine.ifuture.tfuncs as tfuncs
from wolfox.fengine.ifuture.ifuncs import *


ifmap = read_ifs()  # fname ==> BaseObject(name='$name',transaction=trans)


###计算
i05 = ifmap['IF1005']
i06 = ifmap['IF1006']
i07 = ifmap['IF1007']
i09 = ifmap['IF1009']
i12 = ifmap['IF1012']

trans = i06.transaction

i_cof5 = np.where(trans[ITIME]%5==0)    #5分钟收盘线,不考虑隔日的因素
i_cofd = np.where(trans[ITIME]==1514)   #日收盘线


#单个测试
#trades = iftrade.itrade(i06,[ifuncs.xx],[ifuncs.daystop_long,ifuncs.daystop_short,ifuncs.atr_xstop_15_6])
#trades = iftrade.itrade3x(i06,[ifuncs.xx])
trades = iftrade.itrade3x(i06,[tfuncs.tfunc])


sum([trade.profit for trade in trades])
sum([trade.profit>0 for trade in trades])
sum([trade.profit for trade in trades])/len(trades)
len(trades)
iftrade.R(trades)

iftrade.max_drawdown(trades)    #最大连续回撤和单笔回撤
iftrade.max_win(trades)         #最大连续盈利和单笔盈利

for trade in trades:print trade.profit,trade.actions[0].date,trade.actions[0].time,trade.actions[0].position,trade.actions[0].price,trade.actions[1].date,trade.actions[1].time,trade.actions[1].position,trade.actions[1].price


#整体
trades = iftrade.itrade3x(i06,[ifuncs.ipmacd_longt,ifuncs.ipmacd_short,ifuncs.ipmacd_shortt,ifuncs.ipmacd_short_b,ifuncs.ipmacdx_short,ifuncs.ipmacd_long5,ifuncs.ipmacd_short5,ifuncs.dmacd_short2,ifuncs.dmacd_long,ifuncs.dmacd_short5,ifuncs.emv_short,ifuncs.emv_short2,ifuncs.xmacd_short,ifuncs.down02,ifuncs.down01,ifuncs.xldevi2,ifuncs.xhdevi1,ifuncs.emv_long])

#减法##优选###########

#顺势品种
xfollow = [ifuncs.ipmacd_short,ifuncs.down01,ifuncs.dmacd_short5,ifuncs.ipmacdx_short,ifuncs.ipmacd_short5,ifuncs.ma30_short]

#逆势品种
d22 = fcustom(ifuncs.dmacd_short2,rolled=2)
xagainst = [ifuncs.ipmacd_longt,ifuncs.ipmacd_long_devi1,ifuncs.dmacd_long,ifuncs.dmacd_short2,d22,ifuncs.down30]

#中间品种
xmiddle = [ifuncs.ipmacd_long5,ifuncs.ipmacd_long_f,ifuncs.xldevi2,ifuncs.ipmacd_short_devi1,ifuncs.ma60_short]


trades1 = iftrade.itrade3x(i07,xfollow)
trades2 = iftrade.itrade3x(i07,xagainst)
trades3 = iftrade.itrade3x(i07,xmiddle)

trades =  iftrade.itrade3x(i07,xfollow+xagainst+xmiddle)

tradesy =  iftrade.itrade3y(i07,xfollow+xagainst+xmiddle)    #xfollow作为平仓信号，且去掉了背离平仓的信号

优先级：xfollow最高，xmiddle次之，xagainst最后。 即如果现有持仓是xagainst/xmiddle 来的，那么之后的xfollow的反向信号将导致平仓并反向开仓

把xfollow作为平仓条件加入。因为xfollow为顺势信号，所以一般不会出现一个xfollow信号干掉另一个xfollow信号的情况，除非在diff30穿越0线的过程中；


#s_short = [ifuncs.ipmacd_short,ifuncs.ipmacdx_short,ifuncs.ipmacd_short5,ifuncs.dmacd_short2,ifuncs.down02,ifuncs.down01,ifuncs.xhdevi1,ifuncs.ipmacd_short_devi1,ifuncs.dmacd_short5]
#down02和xdevi1被吸收了,ipmacd_short_f被抵制(ipmacd_short的失败信号要失败两次)

d22 = fcustom(ifuncs.dmacd_short2,rolled=2)

s_short = [ifuncs.ipmacd_short,ifuncs.down01,ifuncs.dmacd_short2,d22,ifuncs.ipmacd_short_devi1,ifuncs.dmacd_short5,ifuncs.ipmacdx_short,ifuncs.ipmacd_short5,ifuncs.ma30_short,ifuncs.ma60_short]

s_long=[ifuncs.ipmacd_longt,ifuncs.ipmacd_long_devi1,ifuncs.ipmacd_long5,ifuncs.dmacd_long,ifuncs.ipmacd_long_f,ifuncs.xldevi2]#,ifuncs.ma60_long]

#RU1011
s_short =[ifuncs.ipmacd_short,ifuncs.dmacd_short5]
s_long=[ifuncs.ipmacd_long5,ifuncs.ipmacd_long_f]   #稳定于RU1011

#FU1009稳定
#CU1009不稳定
#跨市场特性比较难，只能是同一类的跨时间市场


trades = iftrade.itrade3x(i06,s_long+s_short)


#s_short = [ifuncs.ipmacd_short,ifuncs.ipmacdx_short,ifuncs.ipmacd_short5,ifuncs.dmacd_short2,ifuncs.dmacd_short5,ifuncs.down02,ifuncs.down01,ifuncs.xhdevi1,ifuncs.ipmacd_short_devi1]#,ifuncs.ipmacd_short_f]

#s_long = [ifuncs.ipmacd_longt,ifuncs.ipmacd_long5,ifuncs.dmacd_long,ifuncs.xldevi2,ifuncs.emv_long,ifuncs.ipmacd_long_devi1]#,ifuncs.ipmacd_long_f]

#需要删减

trades = iftrade.itrade3x(i06,s_long+s_short)

#反向平仓，未必优


>>> trades = iftrade.itrade3x(i06,[ifuncs.ipmacd_longt,ifuncs.ipmacd_short,ifunc
s.ipmacdx_short,ifuncs.ipmacd_long5,ifuncs.ipmacd_short5,ifuncs.dmacd_short2,ifu
ncs.dmacd_long,ifuncs.dmacd_short5,ifuncs.down02,ifuncs.down01,ifuncs.xldevi2],[
ifuncs.daystop_short,ifuncs.xdevi_stop_short1,ifuncs.xmacd_stop_short1],[ifuncs.
daystop_long,ifuncs.xdevi_stop_long1,ifuncs.xmacd_stop_long1])


'''


from wolfox.fengine.ifuture.ibase import *

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


def ma60_short_old(sif,sopened=None):
    ''' ma60拐头
    '''
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)
    
    msignal = gand(strend(sif.ma60) == -1,rollx(strend(sif.ma60))<10)
    fsignal = gand(cross(sif.dea1,sif.diff1)<0,strend(sif.diff5-sif.dea5)>0,sfilter,sif.xatr<20)
    signal = sfollow(msignal,fsignal,15)
    return signal * XSELL

def ma60_short(sif,sopened=None):
    ''' ma60拐头
    '''
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)
    
    msignal = gand(strend(sif.ma60) == -1,rollx(strend(sif.ma60))<10)
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


def ma60_long_old(sif,sopened=None):
    ''' ma60拐头
    '''
    trans = sif.transaction
    msignal = gand(strend(sif.ma60) == 1,rollx(strend(sif.ma60))<-10)
    fsignal = gand(cross(sif.dea1,sif.diff1)>0,strend(sif.diff5-sif.dea5)>0,strend(sif.diff30-sif.dea30)>0)
    signal = sfollow(msignal,fsignal,15)
    return signal * XBUY

def ipmacd_longt(sif,sopened=None):#+
    trans = sif.transaction
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200) #向上突变过滤
    signal = gand(cross(sif.dea1,sif.diff1)>0,sif.diff5<0,strend(sif.diff5-sif.dea5)>0,sif.diff30<sif.dea30,sif.diff30<0,sif.ma5>sif.ma13,strend(sif.ma5)>2,strend(sif.ma5-sif.ma30)>0)
    signal = gand(signal,sif.xatr<15,sfilter)
    return signal * XBUY

def ipmacd_longt_old_b(sif,sopened=None):#+
    trans = sif.transaction
    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200) #向上突变过滤
    signal = gand(cross(sif.dea1,sif.diff1)>0,strend(sif.diff5-sif.dea5)>0,sif.diff30<sif.dea30,sif.diff30<0,sif.ma5>sif.ma13,strend(sif.ma5)>2,sfilter)
    signal = gand(signal,sif.xatr<15)
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
    signal = gand(signal,sif.xatr<15)
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

def ipmacd_long_devi1(sif,sopened=None):
    '''
        底背离操作，去掉了诸多条件
        操作方式:
            1. 底背离之后，必须macd连续增长4次或以上,过滤掉假突破
            2. 确保diff30<0,但是在增长，即macd>0或者macd向上
    '''

    trans = sif.transaction

    sfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤

    msignal = ldevi(trans[ILOW],sif.diff1,sif.dea1)
    fsignal = gand(strend(sif.diff1-sif.dea1) >= 3)   #上叉后仍然连续增长中

    signal = gand(rollx(msignal,3),fsignal,sif.diff30<0,gor(strend(sif.diff30-sif.dea30)>0,sif.diff30>sif.dea30),sfilter,sif.xatr<15)

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
    signal = gand(fmacd1_long(sif,3,sfilter),sif.xatr<15,sfilter2)

    return signal * XBUY



def ipmacd_short_old(sif,sopened=None):#+++
    ''' 
        R=187,times=9/18,2788
        忽略超过10点的瞬间下行导致的下叉
        fmacd1_short无增益
    '''
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)
    signal = gand(cross(sif.dea1,sif.diff1)<0,sif.diff5<0,sif.diff30<0,sif.diff1<0,sfilter)#,strend(sif.diff5)>0)
    signal = gand(signal,strend(sif.ma5)<-1,sif.ma5<sif.ma13,sif.ma5<sif.ma30,strend(sif.ma60)<-5,sif.xatr<20)#,strend(sif.diff5-sif.dea5)<0)
    return signal * XSELL

def ipmacd_short(sif,sopened=None):#+++
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)
    signal = gand(cross(sif.dea1,sif.diff1)<0,sif.diff5<0,sif.diff30<0,sfilter,strend(sif.diff1)<-2)#,strend(sif.diff5)>0)
    signal = gand(signal,sif.xatr<20,sif.ma5<sif.ma13,strend(sif.ma30)<-4,strend(sif.ma13-sif.ma60)<0)
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
    #signal = gand(signal,strend(sif.ma5)<-1,sif.ma5<sif.ma13,sif.ma5<sif.ma30,strend(sif.ma60)<-5,sif.xatr<20)#,strend(sif.diff5-sif.dea5)<0)
    return signal * XSELL

def ipmacd_short_x1(sif,sopened=None):#---
    ''' 
        先下叉，然后小于0(2个周期内)
        总体不佳
    '''
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.diff5<0,sif.diff30<0)
    signal = gand(cross(sif.dea1,sif.diff1)<0,sfilter,sif.diff1>0)#,strend(sif.diff5)>0)
    #signal = gand(signal,strend(sif.ma5)<-1,sif.ma5<sif.ma13,sif.ma5<sif.ma30,strend(sif.ma60)<-5,sif.xatr<20)#,strend(sif.diff5-sif.dea5)<0)

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
    #signal = gand(signal,sif.ma5<sif.ma13,sif.xatr<20)#,strend(sif.diff5-sif.dea5)<0)
    signal = gand(signal,strend(sif.ma5)<-1,sif.ma5<sif.ma13,sif.ma5<sif.ma30,strend(sif.ma60)<-5,sif.xatr<20)#,strend(sif.diff5-sif.dea5)<0)
    
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


def ipmacd_short_b(sif,sopened=None):#+
    '''
        R=163,times=4/8
        忽略超过10点的瞬间下行导致的下叉
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea1,sif.diff1)<0,sif.diff1>0,sif.diff5<sif.dea5,sif.diff30>sif.dea30,trans[IOPEN] - trans[ICLOSE] < 60)#,strend(sif.diff5)>0)
    signal = gand(signal,strend(sif.ma60)<0,sif.xatr<20)#,strend(sif.diff5-sif.dea5)<0)
    return signal * XSELL


def ipmacdx_short_old(sif,sopened=None):#+
    ''' 柱线变化
        R=176,w/t=6/9
    '''
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)

    signal = gand(strend(sif.diff1-sif.dea1)==-3,sif.diff1>sif.dea1,sif.diff30<0,strend(sif.diff5-sif.dea5)>0,sif.diff5<0,sif.diff1<0,sfilter)#trans[IOPEN] - trans[ICLOSE] < 60)
    #signal = gand(strend(sif.diff1-sif.dea1)==3,sif.diff1<sif.dea1,sif.diff1>0,sif.diff5>sif.dea5, trans[ICLOSE] - trans[IOPEN] < 100,sif.ma5>sif.ma13)#,sif.ma13>sif.ma60)#,strend(sif.diff5)>0)
    signal = gand(signal,strend(sif.ma5)<-1,sif.ma5<sif.ma30,sif.xatr<20)#,strend(sif.diff5-sif.dea5)<0)
    return signal * XSELL

def ipmacdx_short(sif,sopened=None):#+
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)

    signal = gand(strend(sif.diff1-sif.dea1)==-3,sif.diff1>sif.dea1,sif.diff30<0,strend(sif.diff5-sif.dea5)>0,sif.diff5<0,sif.diff1<0,sif.diff5<sif.dea5)
    signal = gand(signal,strend(sif.ma5)<-1,sif.ma5<sif.ma30,strend(sif.ma5-sif.ma30)<0,sif.xatr<20,sfilter)
    return signal * XSELL


def ipmacd_long5_old(sif,sopened=None):#+
    '''
        R=432,times=4/6, 1195
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea5,sif.diff5)>0,sif.diff5>0)
    #s1 = gand(cross(sif.dea1,sif.diff1)<0,sif.diff5>sif.dea5,sif.diff5>0,trans[ICLOSE] - trans[IOPEN] < 100)
    sfilter = gand(sif.diff5>sif.dea5,sif.diff5>0,trans[ICLOSE] - trans[IOPEN] < 100,strend(sif.diff30-sif.dea30)>0)
    #s1 = gand(cross(sif.dea1,sif.diff1)>0,sfilter)#,sif.xatr<15)
    s1 = gand(fmacd1_long(sif,2),sfilter)#,sif.xatr<15)
    signal = sfollow(signal,s1,60)
    signal = gand(sif.ma5>sif.ma13,signal)
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

def ipmacd_short5_old(sif,sopened=None):#-
    '''
        R=166,w/t=6/12
    '''
    trans = sif.transaction
    signal = gand(cross(sif.dea5,sif.diff5)<0,sif.diff5>0,trans[IOPEN] - trans[ICLOSE] < 60)#,strend(sif.diff5)>0)
    #s1 = gand(cross(sif.dea1,sif.diff1)<0,sif.diff5<sif.dea5,sif.xatr<20)
    #signal = sfollow(signal,s1,60)
    signal = gand(signal,strend(sif.ma60)<0,strend(sif.ma30)<0,sif.ma5<sif.ma13,sif.ma5<sif.ma30,sif.xatr<20)#,strend(sif.diff5-sif.dea5)<0)
    
    return signal * XSELL

def ipmacd_short5(sif,sopened=None):#-
    trans = sif.transaction
    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)
    
    signal = gand(cross(sif.dea5,sif.diff5)<0,sif.diff5>0,sif.diff30<0,strend(sif.diff30-sif.dea30)<0)
    signal = gand(signal,strend(sif.ma13-sif.ma60)<0,sfilter,sif.xatr<20)   
    return signal * XSELL


def dmacd_short2_old(sif,sopened=None):#++
    '''
        R=304,times=4/5
        回抽时未下叉又上涨
    '''
    trans = sif.transaction
    sdd = strend(sif.diff1 - sif.dea1)
    signal = gand(sdd==1,rollx(sdd)<-1,sif.diff1>sif.dea1, trans[IOPEN] - trans[ICLOSE] < 60,sif.diff5>0,sif.diff30>0,sif.diff1>0,sif.xatr<20)

    return signal * XSELL

def dmacd_short5(sif,sopened=None):#+++
    trans = sif.transaction
    sfilter= gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)#  向下突变过滤    

    sdd = strend(sif.diff5 - sif.dea5)
    signal = gand(sdd==-1,rollx(sdd)>4,sif.diff5<sif.dea5,sif.diff1<sif.dea1,sif.diff30>sif.dea30,sif.diff30<0,strend(sif.diff30-sif.dea30)<0)
    signal = gand(signal,sif.ma5<sif.ma13,sfilter,sif.xatr<20,strend(sif.ma13-sif.ma60)<0)
    
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


def dmacd_short5_old(sif,sopened=None):#+++
    ''' 
        R=436,times=5/8,2072
        回抽时未上叉又回落
    '''
    trans = sif.transaction
    sdd = strend(sif.diff5 - sif.dea5)
    signal = gand(sdd==-1,rollx(sdd)>4,sif.diff5<sif.dea5,trans[IOPEN] - trans[ICLOSE] < 60,sif.diff30>sif.dea30,sif.diff30<0,strend(sif.diff30-sif.dea30)<0)
    #signal = gand(signal,strend(sif.ma60)<0,sif.xatr<20)#,strend(sif.diff5-sif.dea5)<0)
    #signal = sfollow(signal,fmacd1_short(sif,3))
    signal = gand(signal,strend(sif.ma60)<0,sif.xatr<20,sif.ma5<sif.ma13)
    
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

def down30(sif,sopened=None):
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)

    msignal = gand(cross(sif.dea30,sif.diff30)<0)
    fsignal = gand(cross(cached_zeros(len(sif.dea1)),sif.diff1)<0,sif.diff30>0)
    
    signal = sfollow(msignal,fsignal,120)

    signal = gand(signal,ksfilter,sif.xatr<20)

    return signal*XSELL


def down01_old(sif,sopened=None): #++
    ''' 
        R=104,times=5/13
        30分钟框架下的下行，5分钟框架的上行，以及1分钟的下行
        去掉
    '''
    trans = sif.transaction
    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1)<0,sif.diff1<sif.dea1,sif.diff5>sif.dea5,sif.dea5>0,sif.diff30<sif.dea30,trans[IOPEN] - trans[ICLOSE] < 60)
    return signal * XSELL

def down01(sif,sopened=None): #++
    ''' 
        30分钟<0且下行
        5分钟>0且下行
        1分钟下叉, 且一分钟下行3分钟或以上
    '''
    trans = sif.transaction
    sfilter= gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)#  向下突变过滤

    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1)<0,strend(sif.diff5-sif.dea5)<0,sif.diff5>0,strend(sif.diff30-sif.dea30)<0,sif.diff30<0,strend(sif.diff1)<-2)
    return signal * XSELL


def xldevi2_old(sif,sopened=None):#+
    '''
        R=100,times=2/2,501
        样本太少
    '''
    trans = sif.transaction
    xs = gand(ldevi(trans[ILOW],sif.diff5,sif.dea5),sif.diff5<0)
    s1 = gand(cross(sif.dea1,sif.diff1)>0,sif.diff5<0,sif.diff5>sif.dea5,sif.xatr<15,strend(sif.diff30)<0)
    signal = sfollow(xs,s1,60)
    #signal = gand(signal,strend(sif.ma30)>0)
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


def xhdevi1(sif,sopened=None):#+
    '''
        弱势条件下的1分钟顶背离
    '''
    trans = sif.transaction
    xs = gand(hdevi(trans[IHIGH],sif.diff1,sif.dea1),sif.diff5<0,sif.diff30<0,sif.xatr<20)
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


