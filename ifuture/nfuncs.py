# -*- coding: utf-8 -*-

'''

主力合约、次月合约与半年合约的成交量还可以，下季合约严重没量，被操控
但因为次月合约开张日晚，如if1007在0524才开张，所以测试不准

去掉macd15/30的影响，因为这个计算和图形有很大的不同

from wolfox.fengine.ifuture.ifreader import read_ifs

from wolfox.fengine.ifuture.ibase import *
from wolfox.fengine.ifuture.ifreader import *
import wolfox.fengine.ifuture.iftrade as iftrade
import wolfox.fengine.ifuture.ifuncs as ifuncs
import wolfox.fengine.ifuture.nfuncs as nfuncs
import wolfox.fengine.ifuture.tfuncs as tfuncs
from wolfox.fengine.ifuture.ifuncs import *


ifmap = read_ifs()  # fname ==> BaseObject(name='$name',transaction=trans)


###计算
i05 = ifmap['IF1005']
i06 = ifmap['IF1006']
i07 = ifmap['IF1007']
i09 = ifmap['IF1009']
i12 = ifmap['IF1012']

trans = i07.transaction

i_cof5 = np.where(trans[ITIME]%5==0)    #5分钟收盘线,不考虑隔日的因素
i_cofd = np.where(trans[ITIME]==1514)   #日收盘线

trades = iftrade.itrade3x(i06,[nfuncs.nfunc])

sum([trade.profit for trade in trades])
sum([trade.profit>0 for trade in trades])
sum([trade.profit for trade in trades])/len(trades)
len(trades)
iftrade.R(trades)

iftrade.max_drawdown(trades)    #最大连续回撤和单笔回撤
iftrade.max_win(trades)         #最大连续盈利和单笔盈利

for trade in trades:print trade.profit,trade.actions[0].date,trade.actions[0].time,trade.actions[0].position,trade.actions[0].price,trade.actions[1].date,trade.actions[1].time,trade.actions[1].position,trade.actions[1].price


xmiddle = [ifuncs.dms]


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

#########################XFOLLOW###################################
def ipmacd_short(sif,sopened=None):#+++
    trans = sif.transaction

    sfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)
    signal = gand(cross(sif.dea1,sif.diff1)<0,sif.diff5<0,sif.di30<0,sfilter,strend(sif.diff1)<-2)#,strend(sif.diff5)>0)
    signal = gand(signal,sif.xatr<20,sif.ma5<sif.ma13,strend(sif.ma30)<-4,strend(sif.ma13-sif.ma60)<0)
    return signal * XSELL

def down01(sif,sopened=None): #++
    ''' 
        30分钟<0且下行
        5分钟>0且下行
        1分钟下叉, 且一分钟下行3分钟或以上
    '''
    trans = sif.transaction
    sfilter= gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120)#  向下突变过滤

    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1)<0,strend(sif.diff5-sif.dea5)<0,sif.diff5>0,sif.diff30<0,strend(sif.diff30-sif.dea30)<0,strend(sif.diff1)<-2)
    return signal * XSELL


#########################XMIDDLE###################################
def dms(sif,sopened=None):
    '''
        全部信号走好,唯一一点就是diff5<0
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<15)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<20)

    dsignal = gand(strend(sif.diff1-sif.dea1)>0,strend(sif.diff5-sif.dea5)>0,strend(sif.diff1)>0,strend(sif.diff5)>0,strend(sif.di30)>0)
    msignal = gand(sif.ma5>sif.ma13,sif.ma13>sif.ma30,sif.ma30>sif.ma60)
    ssignal = gand(strend(sif.ma5-sif.ma30)>0,strend(sif.ma13-sif.ma60)>0,strend(sif.ma135-sif.ma270)>0)

    signal = gand(dsignal,msignal,ssignal,sif.diff5<0,dsfilter)
    return signal * XBUY



#########################XAGAINST###################################
