# -*- coding: utf-8 -*-


'''
    新高/新低系统
    当出现信号开仓后，如果未平仓前出现第二个信号，则止损要按照这几个信号最宽的一个来放
    L: 0.018手续费

    Xfuncs2的测试版本

'''

from wolfox.fengine.ifuture.ibase import *
import wolfox.fengine.ifuture.iftrade as iftrade
import wolfox.fengine.ifuture.fcontrol as control
from wolfox.fengine.ifuture.xfuncs import *

#一些补充
def n1445filter(sif):
    return gand(
            sif.time > 944,
            sif.time < 1445,
            )

def mfilter(sif):   #主要时间
    return gand(
            sif.time > 1029,
            sif.time < 1430,
        )

def rfilter(sif):   #主要时间
    return gor(
            gand(
                sif.time > 944,
                sif.time < 1029,
            ),
            gand(
                sif.time > 1430,
                sif.time < 1500,
            )
        )


def n1130filter(sif):
    return gand(
            sif.time > 1130,
            sif.time < 1500,
        )

def n1030filter(sif):
    return gand(
            sif.time > 1030,
            sif.time < 1500,
        )

###算法
def nhh0(sif):
    #使用最高点
    return gand(
            #cross(rollx(sif.dhigh+30),sif.high)>0
            sif.high > rollx(sif.dhigh+10),
        )

def nll0(sif):
    #使用最低点
    return gand(
            #cross(rollx(sif.dlow-30),sif.low)<0
            sif.low < rollx(sif.dlow-10),
        )


def nhh(sif):
    #使用最高点
    return gand(
            #cross(rollx(sif.dhigh+30),sif.high)>0
            sif.high > rollx(sif.dhigh+30),
        )
 
def nhc(sif):
    #使用收盘价
    return gand(
            #cross(rollx(sif.dhigh-30),sif.close)>0
            sif.close > rollx(sif.dhigh-30),
        )

def nll(sif):
    #使用最低点
    return gand(
            #cross(rollx(sif.dlow-30),sif.low)<0
            sif.low < rollx(sif.dlow-30),
        )

def nll2(sif):
    #使用最低点
    return gand(
            #cross(rollx(sif.dlow-30),sif.low)<0
            sif.low < rollx(sif.dlow+20,3), #比close要小点
        )
    
def nlc(sif):
    #使用收盘价,而且是前面倒数第三次的dlow
    return gand(
            #cross(rollx(sif.dlow+30,3),sif.close)<0
            sif.close < rollx(sif.dlow+30,3),
        )

def nhc_fake(sif):  
    #使用收盘价并且用条件单时，必须面对的假突破。即盘中突破收盘拉回
    return gand(
            #cross(rollx(sif.dhigh-30),sif.close)>0
            sif.high > rollx(sif.dhigh-30),
            sif.close < rollx(sif.dhigh-30),
        )


def nlc_fake(sif):  
    #使用收盘价并且用条件单时，必须面对的假突破。即盘中突破收盘拉回
    return gand(
            #cross(rollx(sif.dlow+30),sif.low)<0,
            sif.low   <  rollx(sif.dlow+30,3),            
            sif.close >=  rollx(sif.dlow+30,3)
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

#用atr的绝对值效果不行    
def na2000(sif):
    return gand(
                sif.atr < 8000,
                sif.atr5x < 15000,
                sif.atr30x < 30000,
            )

#原始突破系统，以1个点位过滤
nbreak_nhh0 = BXFuncA(fstate=gofilter,fsignal=nhh0,fwave=gofilter,ffilter=nfilter)
nbreak_nll0 = SXFuncA(fstate=gofilter,fsignal=nll0,fwave=gofilter,ffilter=nfilter)

nhbreak_nhh0 = BXFuncA(fstate=gofilter,fsignal=nhh0,fwave=gofilter,ffilter=mfilter)
nhbreak_nll0 = SXFuncA(fstate=gofilter,fsignal=nll0,fwave=gofilter,ffilter=mfilter)

nbreak0 = [nbreak_nhh0,nbreak_nll0]
nhbreak0 = [nhbreak_nhh0,nhbreak_nll0]

##反向使用，抄底摸顶
rbreak_nhh0 = SXFuncA(fstate=gofilter,fsignal=nhh0,fwave=gofilter,ffilter=nfilter)
rbreak_nll0 = BXFuncA(fstate=gofilter,fsignal=nll0,fwave=gofilter,ffilter=nfilter)



nbreak_nhh = BXFuncA(fstate=gofilter,fsignal=nhh,fwave=gofilter,ffilter=nfilter)
nbreak_nll = SXFuncA(fstate=gofilter,fsignal=nll,fwave=gofilter,ffilter=nfilter)
nbreak_nll2 = SXFuncA(fstate=gofilter,fsignal=nll2,fwave=gofilter,ffilter=nfilter)

nhbreak_nhh = BXFuncA(fstate=gofilter,fsignal=nhh,fwave=gofilter,ffilter=mfilter)
nhbreak_nll = SXFuncA(fstate=gofilter,fsignal=nll,fwave=gofilter,ffilter=mfilter)
nhbreak_nll2 = SXFuncA(fstate=gofilter,fsignal=nll2,fwave=gofilter,ffilter=mfilter)

nbreak_nhc = BXFuncA(fstate=gofilter,fsignal=nhc,fwave=gofilter,ffilter=nfilter)  
nbreak_nlc = SXFuncA(fstate=gofilter,fsignal=nlc,fwave=gofilter,ffilter=nfilter)  

nbreak = [nbreak_nhh,nbreak_nll]
nbreak2 = [nbreak_nhh,nbreak_nll2]  #效果比nbreak差
nhbreak = [nhbreak_nhh,nhbreak_nll]
nhbreak2 = [nhbreak_nhh,nhbreak_nll2]  #效果比nbreak差

break_nhh = BXFuncA(fstate=gofilter,fsignal=nhh,fwave=nx2500X,ffilter=nfilter)  ##选择
break_nhh.name = u'向上突破新高'
hbreak_nhh = BXFuncA(fstate=gofilter,fsignal=nhh,fwave=nx2500X,ffilter=mfilter)  ##主要时段

break_nll = SXFuncA(fstate=gofilter,fsignal=nll,fwave=nx2500X,ffilter=nfilter)

break_nhc = BXFuncA(fstate=gofilter,fsignal=nhc,fwave=nx2500X,ffilter=nfilter)  #F1好
break_nlc = SXFuncA(fstate=gofilter,fsignal=nlc,fwave=nx2500X,ffilter=nfilter)  #F1效果明显，但总收益下降

break_nhc_fake = BXFuncA(fstate=gofilter,fsignal=nhc_fake,fwave=nx2500X,ffilter=nfilter)  #F1好
break_nlc_fake = SXFuncA(fstate=gofilter,fsignal=nlc_fake,fwave=nx2500X,ffilter=nfilter)  #F1效果明显，但总收益下降

abreak_nhh = BXFuncA(fstate=gofilter,fsignal=nhh,fwave=na2000,ffilter=nfilter)
abreak_nll = SXFuncA(fstate=gofilter,fsignal=nll,fwave=na2000,ffilter=nfilter)

abreak_nhc = BXFuncA(fstate=gofilter,fsignal=nhc,fwave=na2000,ffilter=nfilter)  #F1好
abreak_nlc = SXFuncA(fstate=gofilter,fsignal=nlc,fwave=na2000,ffilter=nfilter)  #F1效果明显，但总收益下降

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

sbreak_nhh = BXFuncA(fstate=sup,fsignal=nhh,fwave=nx2500X,ffilter=nfilter)
#sbreak_nhh.stop_closer = iftrade.atr5_uxstop_kV
#sbreak_nhc = BXFuncA(fstate=sup,fsignal=nhc,fwave=nx2500X,ffilter=nfilter)

sbreak_nll = SXFuncA(fstate=sdown,fsignal=nll,fwave=nx2500X,ffilter=nfilter)    #这个R高，但是次数少
sbreak_nll.name = u'向下突破'

sbreak_nlc = SXFuncA(fstate=sdown,fsignal=nlc,fwave=nx2500X,ffilter=nfilter)    #这个R小，次数多
sbreak_nlc.name = u'即将向下突破'

sbreak_nlc_fake = SXFuncA(fstate=sdown,fsignal=nlc_fake,fwave=nx2500X,ffilter=nfilter)    #F1效果明显
sbreak_nlc_fake.name = u'向下假突破'    #假突破时需要马上平仓

sbreak_nll2 = SXFuncA(fstate=sdown,fsignal=nll2,fwave=nx2500X,ffilter=nfilter)    #这个R高，但是次数少
sbreak_nll2.name = u'向下突破2'
#sbreak_nlc + sbreak_nlc_break = sbreak_nll2


lbreak = [break_nhh,break_nll]
lbreak2 = [break_nhc,break_nlc]

xbreak = [break_nhh,break_nlc]  #这个比较好，顶底不对称
xbreak2 = [break_nhc,break_nll]

zbreak = [break_nhh,sbreak_nll2] #这个最好,理念最清晰

zbreak2 = [break_nhh,sbreak_nll] #这个效果差一点
zbreak0 = [sbreak_nhh,sbreak_nll2] #比较投机

lcandidate = [sbreak_nll]

#

def pinfo(sif,trades):
    ss = 0  
    mas = 0
    mis = 9999
    nn = 0
    for trade in trades:
        ia0 = trade.actions[0].index
        ia1 = trade.actions[1].index
        a0 = trade.actions[0]
        a1 = trade.actions[1]
        direction = a0.position
        topen = sif.open[ia0]
        thigh = sif.high[ia0]
        tlow = sif.low[ia0]
        tclose = sif.close[ia0]
        #滑点是与系统开仓价即止损基准价的差别
        #ia0-1是信号发生分钟，ia0-2是信号发生之前的dhigh/dlow基准
        if direction == LONG:
            tprice = sif.dhigh[ia0-2] + 30
            tskip = tprice - topen
        else:
            tprice = sif.dlow[ia0-2] + 30
            tskip = topen - tprice
        ss += tskip
        if tskip > mas:
            mas = tskip
        if tskip < mis:
            mis = tskip
        nn += 1
        print trade.profit,a0.date,a0.time,direction,a0.price,a1.time,a1.price,ia1-ia0,'|',tskip,tprice#,thigh,sif.dhigh[ia0-1]
    print u'总次数=%s,滑点总数=%s,最大滑点=%s,最大有利滑点=%s' % (nn,ss,mas,mis)
    
def save(sif,trades,fname):
    ff = open(fname,'w+')
    mm = 200000
    for trade in trades:
        ia0 = trade.actions[0].index
        ia1 = trade.actions[1].index
        a0 = trade.actions[0]
        a1 = trade.actions[1]
        mm = mm + trade.profit * 30
        od = u'买开' if a0.position==LONG else u'卖开'
        print >>ff,u'%s,%s,%s,%d,%s,%d,%d,%d' % (sif.date[ia0],sif.time[ia0],od,a0.price,sif.time[a1.index],a1.price,trade.profit,mm)
    ff.close()

def max_drawdown(trades):
    ms = 0
    cur = 0
    for trade in trades:
        cur += trade.profit
        if cur >0:
            cur = 0
        elif cur < ms:
            ms = cur
    return ms


######考虑用tmax(60)
mlen = 75
def mhh(sif,length=mlen):
    #使用最高点
    return gand(
            #sif.time>1115,
            cross(rollx(tmax(sif.high,length)+30),sif.high)>0
        )
 
mhh30 = fcustom(mhh,length=30)
mhh20 = fcustom(mhh,length=20)
mhh10 = fcustom(mhh,length=10)
mhh45 = fcustom(mhh,length=45)
mhh60 = fcustom(mhh,length=60)
mhh90 = fcustom(mhh,length=90)


def mhc(sif,length=mlen):
    #使用收盘价
    return gand(
            sif.time>1115,
            cross(rollx(tmax(sif.high,length)-30),sif.close)>0
        )

def mll(sif,length=mlen):
    #使用最低点
    return gand(
            sif.time>1115,
            cross(rollx(tmin(sif.low,length)-30),sif.low)<0
        )
mll30 = fcustom(mll,length=30)
mll20 = fcustom(mll,length=20)
mll10 = fcustom(mll,length=10)
mll45 = fcustom(mll,length=45)
mll60 = fcustom(mll,length=60)
mll90 = fcustom(mll,length=90)

def mll2(sif,length=mlen):
    #使用最低点
    return gand(
            #sif.time>1029,
            cross(rollx(tmin(sif.low,length)+20),sif.low)<0
        )

mll2_30 = fcustom(mll2,length=30)
mll2_20 = fcustom(mll2,length=20)
mll2_10 = fcustom(mll2,length=10)
mll2_45 = fcustom(mll2,length=45)
mll2_60 = fcustom(mll2,length=60)
mll2_90 = fcustom(mll2,length=90)

def mlc(sif,length=mlen):
    #使用收盘价
    return gand(
            sif.time>1115,
            cross(rollx(tmin(sif.low,length)+30),sif.close)<0
        )

break_mhh = BXFuncA(fstate=gofilter,fsignal=mhh,fwave=nx2500X,ffilter=nfilter)  #差于nhh
break_mll = SXFuncA(fstate=gofilter,fsignal=mll,fwave=nx2500X,ffilter=nfilter)  #差于nll
break_mll2 = SXFuncA(fstate=gofilter,fsignal=mll,fwave=nx2500X,ffilter=nfilter)  #差于nll

break_mll2_90 = SXFuncA(fstate=gofilter,fsignal=mll2_90,fwave=nx2500X,ffilter=nfilter)  #差于nhh

mbreak = [break_mhh,break_mll]

hbreak_mhh = BXFuncA(fstate=gofilter,fsignal=mhh,fwave=nx2500X,ffilter=mfilter)  #差于nhh


break_mhc = BXFuncA(fstate=gofilter,fsignal=mhc,fwave=nx2500X,ffilter=nfilter)  #差于nhc
break_mlc = SXFuncA(fstate=gofilter,fsignal=mlc,fwave=nx2500X,ffilter=nfilter)  #差于nlc

sbreak_mll = SXFuncA(fstate=sdown,fsignal=mll,fwave=nx2500X,ffilter=nfilter)    #差于nll
sbreak_mll2 = SXFuncA(fstate=sdown,fsignal=mll2,fwave=nx2500X,ffilter=n1430filter)    #优于nll
sbreak_mlc = SXFuncA(fstate=sdown,fsignal=mlc,fwave=nx2500X,ffilter=nfilter)    #差于nlc

sbreak_mll2_90 = SXFuncA(fstate=sdown,fsignal=mll2_90,fwave=nx2500X,ffilter=mfilter)    


mbreak2 = [break_mhh,sbreak_mll2]   #这个很不错

zxbreak = [break_nhh,sbreak_mll2]

#mxxx = [break_mhh,break_mhc,break_mll,break_mlc]
mxxx = [break_mhh,sbreak_mll]   #这个叠加反效果

#####混合使用
shbreak_mll2 = SXFuncA(fstate=sdown,fsignal=mll2,fwave=nx2500X,ffilter=mfilter)    #优于nll
shbreak_mll2.stop_closer = iftrade.atr5_uxstop_kV #60/120/333

shbreak_nll2 = SXFuncA(fstate=sdown,fsignal=nll2,fwave=nx2500X,ffilter=mfilter)    #这个R高，但是次数少
shbreak_nllr = SXFuncA(fstate=sdown,fsignal=nll2,fwave=nx2500X,ffilter=mfilter)    #这个R高，但是次数少
shbreak_nll2.stop_closer = iftrade.atr5_uxstop_kV #60/120/333
shbreak_nllr.stop_closer = iftrade.atr5_uxstop_kV #60/120/333

wopt = [shbreak_mll2,shbreak_nllr]


##下跌采用75分钟的底部+2, 上涨采用日顶部+3(均在10:30-14:30)


hbreak = [shbreak_mll2,break_nhh]  #利润比较好
hbreak2 = [shbreak_mll2,hbreak_nhh]  #这个最大回撤最小


####尝试使用30分钟高低点止损
def m30s(sif,sopened=None):
    bline = rollx(tmin(sif.low,20))
    signal = sif.low < bline
    return signal * XSELL

def m30b(sif,sopened=None):
    bline = rollx(tmax(sif.high,20))
    signal = sif.high > bline
    return signal * XBUY

m30s_closer = lambda cc: cc+[m30s]
m30b_closer = lambda cc: cc+[m30b]

#效果不好，容易丢失大波段
#shbreak_mll2.closer = m30b_closer
#hbreak_nhh.closer = m30s_closer



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

#iftrade.atr5_uxstop_X = fcustom(iftrade.atr_uxstop_k,fkeeper=iftrade.F180,win_times=250,natr=5,flost_base=iftrade.F60)      #120-60


for x in xxx2+mxxx+mbreak+mbreak2:
    #x.stop_closer = iftrade.atr5_uxstop_kF #60/120       
    #x.stop_closer = iftrade.atr5_uxstop_kQ #10/120       
    x.stop_closer = iftrade.atr5_uxstop_kV #60/120/333
    x.cstoper = iftrade.F60  #初始止损,目前只在动态显示时用
    if 'lastupdate' not in x.__dict__:
        x.lastupdate = 20101209
    
