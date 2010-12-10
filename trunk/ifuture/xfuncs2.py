# -*- coding: utf-8 -*-


'''
    新高/新低系统
    当出现信号开仓后，如果未平仓前出现第二个信号，则止损要按照这几个信号最宽的一个来放
    L: 0.018手续费

'''

from wolfox.fengine.ifuture.ibase import *
import wolfox.fengine.ifuture.iftrade as iftrade
import wolfox.fengine.ifuture.fcontrol as control
from wolfox.fengine.ifuture.xfuncs import *

#主要时间过滤
def mfilter(sif):   
    return gand(
            sif.time > 1029,
            sif.time < 1430,
        )

def nhh(sif):
    #使用最高点+30, 也就是说必须一下拉开3点
    return gand(
            #cross(rollx(sif.dhigh+30),sif.high)>0
            sif.high > rollx(sif.dhigh+30),
        )
    
    
def nx2000X(sif):
    return gand(
                sif.xatr < 2000,
                sif.xatr30x < 10000,
                sif.xatr5x< 4000,
           )

def nx2500X(sif):
    return gand(
                sif.xatr < 2500,
                sif.xatr30x < 10000,
                sif.xatr5x< 4000,
           )


break_nhh = BXFuncA(fstate=gofilter,fsignal=nhh,fwave=nx2500X,ffilter=nfilter)  ##选择
break_nhh.name = u'向上突破新高'
hbreak_nhh = BXFuncA(fstate=gofilter,fsignal=nhh,fwave=nx2500X,ffilter=mfilter)  ##主要时段

def sdown(sif):
    return gand(
            sif.t120 < 30,
            #sif.t120 < -200,    #周期为1个月，末期会不明,有点太投机
        )

def sup(sif):
    return gand(
            sif.t120 < 200, #200均可 这个有点太投机
            #sif.s30>0,
        )

sbreak_nll2 = SXFuncA(fstate=sdown,fsignal=nll2,fwave=nx2500X,ffilter=nfilter)    #这个R高，但是次数少
sbreak_nll2.name = u'向下突破2'
#sbreak_nlc + sbreak_nlc_break = sbreak_nll2

zbreak = [break_nhh,sbreak_nll2] #这个最好,理念最清晰

###时间低点突破
mlen = 75

def mll2(sif):
    #使用最低点
    return gand(
            #sif.time>1029,
            cross(rollx(tmin(sif.low,mlen)+20),sif.low)<0
        )


sbreak_mll2 = SXFuncA(fstate=sdown,fsignal=mll2,fwave=nx2500X,ffilter=n1430filter)    #优于nll

#主要时段
shbreak_mll2 = SXFuncA(fstate=sdown,fsignal=mll2,fwave=nx2500X,ffilter=mfilter)    #优于nll

##下跌采用75分钟的底部+2, 上涨采用日顶部+3(均在10:30-14:30)
hbreak = [shbreak_mll2,break_nhh]  #利润比较好
hbreak2 = [shbreak_mll2,hbreak_nhh]  #这个最大回撤最小


####添加老系统
wxxx = [xds,xdds3,k5_d3b,xuub,K1_DDD1,K1_UUX,K1_RU,Z5_P2,xmacd3s,xup01,ua_fa,FA_15_120]

wxxx_s = [xds,xdds3,k5_d3b,K1_DDD1,Z5_P2,xmacd3s,FA_15_120]
wxxx_b = [xuub,K1_UUX,K1_RU,xup01,ua_fa]

wxss = CSFuncF1(u'向下投机组合',*wxxx_s)
wxbs = CBFuncF1(u'向上投机组合',*wxxx_b)

wxfs = [wxss,wxbs]

#xxx = zbreak

xxx = hbreak2    

xxx2 = xxx +wxfs #+ wxxx

xxx3 = zbreak + mbreak2

for x in xxx2+wxxx:
    #x.stop_closer = iftrade.atr5_uxstop_kF #60/120       
    #x.stop_closer = iftrade.atr5_uxstop_kQ #10/120       
    x.stop_closer = iftrade.atr5_uxstop_kV #60/120/333
    x.cstoper = iftrade.F60  #初始止损,目前只在动态显示时用
