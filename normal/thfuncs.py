# -*- coding: utf-8 -*-

#算法测试

from numpy import select

from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *
from wolfox.fengine.core.d1 import lesser,bnot,gmax,gmin
from wolfox.fengine.core.d1ex import tmax,derepeatc,derepeatc_v,equals,msum,scover,xfollow
from wolfox.fengine.core.d1match import *
from wolfox.fengine.core.d1idiom import *
from wolfox.fengine.core.d1indicator import cmacd,score2
from wolfox.foxit.base.tutils import linelog
from time import time

import logging
logger = logging.getLogger('wolfox.fengine.normal.sfuncs')    

def prepare_slup(stocks):
    for stock in stocks:
        prepare_slup1(stock)
        prepare_slup2(stock)
        prepare_slup3(stock)
        prepare_slup4(stock)        

def prepare_slup1(stock):
    linelog('prepare hour:%s' % stock.code)
    slup1 = np.sign(stock.hour * 10000 / rollx(stock.hour,1) >= 10990)  
    stock.slup1 = xfollow(hour2day1(slup1),stock.transaction[VOLUME])   #第1小时涨停. 确保第二天停盘也能够使信号延递

def prepare_slup2(stock):
    linelog('prepare hour:%s' % stock.code)
    slup2 = np.sign(stock.hour * 10000 / rollx(stock.hour,2) >= 10990)  
    stock.slup2 = xfollow(hour2day2(slup2),stock.transaction[VOLUME])   #第1小时涨停. 确保第二天停盘也能够使信号延递

def prepare_slup3(stock):
    linelog('prepare hour:%s' % stock.code)
    slup3 = np.sign(stock.hour * 10000 / rollx(stock.hour,3) >= 10990)  
    stock.slup3 = xfollow(hour2day3(slup3),stock.transaction[VOLUME])   #第1小时涨停. 确保第二天停盘也能够使信号延递

def prepare_slup4(stock):
    linelog('prepare hour:%s' % stock.code)
    slup4 = np.sign(stock.hour * 10000 / rollx(stock.hour,4) >= 10990)  
    stock.slup4 = xfollow(hour2day4(slup4),stock.transaction[VOLUME])   #第1小时涨停. 确保第二天停盘也能够使信号延递

def prepare_touch_high(stocks):
    for stock in stocks:
        prepare_touch1(stock)
        prepare_touch2(stock)
        prepare_touch3(stock)
        prepare_touch3(stock)        


def prepare_touch1(stock):
    linelog('prepare hour:%s' % stock.code)
    touch1 = np.sign(stock.hour_high * 10000 / rollx(stock.hour,1) >= 10990)  
    stock.touch1 = xfollow(hour2day1(touch1),stock.transaction[VOLUME])   #第1小时涨停. 确保第二天停盘也能够使信号延递

def prepare_touch2(stock):
    linelog('prepare hour:%s' % stock.code)
    touch2 = np.sign(stock.hour_high * 10000 / rollx(stock.hour,2) >= 10990)  
    stock.touch2 = xfollow(hour2day2(touch2),stock.transaction[VOLUME])   #第1小时涨停. 确保第二天停盘也能够使信号延递

def prepare_touch3(stock):
    linelog('prepare hour:%s' % stock.code)
    touch3 = np.sign(stock.hour_high * 10000 / rollx(stock.hour,3) >= 10990)  
    stock.touch3 = xfollow(hour2day3(touch3),stock.transaction[VOLUME])   #第1小时涨停. 确保第二天停盘也能够使信号延递

def prepare_touch4(stock):
    linelog('prepare hour:%s' % stock.code)
    touch4 = np.sign(stock.hour_high * 10000 / rollx(stock.hour,4) >= 10990)  
    stock.touch4 = xfollow(hour2day4(touch4),stock.transaction[VOLUME])   #第1小时涨停. 确保第二天停盘也能够使信号延递

def prepare_up1(stock):
    linelog('prepare hour:%s' % stock.code)
    #up = stock.hour * 10000 / rollx(stock.hour,1) >= 10200
    down =stock.hour_high - stock.hour < (stock.hour-stock.hour_open)*2/3
    ol = stock.hour > stock.hour_open
    tk = stock.hour_low > rollx(stock.hour_high)
    up = stock.hour * 10000 / gmin(rollx(stock.hour,1),stock.hour_open) > 10200
    stock.up1 =  xfollow(hour2day1(gand(up,down,ol,tk)),stock.transaction[VOLUME])
    stock.open2 = hour2day2(stock.hour_open)

def attack2c(stock):#
    ''' 跳空高开并且全日收盘未补缺口，且收盘大于开盘，并收于相对高位
    '''
    linelog('%s:%s' % (attack2.__name__,stock.code))
    t = stock.transaction
    
    last = rollx(t[CLOSE],1) #CLOSE?
    tk = gand(t[OPEN] > last*102/100,t[LOW]>last)   
    down = t[HIGH]-t[CLOSE] < (t[CLOSE]-t[OPEN])*2/3
    ol = t[CLOSE] > t[OPEN]

    cup = gand(tk,down,ol)


    #三线理顺
    #tt = rollx(gand(stock.t4,stock.t5),1)
    fm = rollx(gand(stock.diff < stock.dea))

    g = rollx(gand(stock.g20>stock.g60,stock.g60>stock.g120))

    smarket = gand(stock.ref.t2,stock.ref.t1,stock.ref.t0)
    signal = gand(cup,t[VOLUME]>0,g)#smarket)#,rama) #,rama  #,tt,peak)#,fmacd,xmacd)  #rama

    dsignal = decover(signal,3)
    #stock.buyprice = select([dsignal>0],[t[HIGH]])     #涨停价
    #stock.buyprice = select([dsignal>0],[stock.open2])     #第二小时开盘
    #print signal
    return dsignal


def attack2b(stock):#
    ''' 盘中第二小时追跳高不变者
        使用fseller(信号次日卖出)
        bo_pricer = (lambda s : s.buyprice,lambda s : s.transaction[OPEN])
        myMediator=nmediator_factory(trade_strategy=B0S1,pricer = bo_pricer)    
        使用fseller_t(信号当日卖出)
        my_pricer = (lambda s : s.buyprice,lambda s : s.sellprice)
        myMediator=nmediator_factory(trade_strategy=B0S0_N,pricer = my_pricer)    
        使用follow_seller(信号当日卖出)
        my_pricer = (lambda s : s.buyprice,lambda s : s.sellprice)
        myMediator=nmediator_factory(trade_strategy=B0S0_N,pricer = my_pricer)    

    '''
    linelog('%s:%s' % (attack2.__name__,stock.code))
    t = stock.transaction
    
    #第一个涨停 #确保没有稍长的下影线

    cup = gand(stock.up1,bnot(gand(stock.stoped2,stock.stoped3,stock.stoped4)))


    #三线理顺
    #tt = rollx(gand(stock.t4,stock.t5),1)
    fm = rollx(gand(stock.diff < stock.dea))

    g = rollx(gand(stock.g20>stock.g60,stock.g60>stock.g120))

    tref = rollx(gand(stock.ref.t3))

    signal = gand(cup,t[VOLUME]>0,stock.ref.up1,tref,strend(stock.ref.diff)>0,fm,g)#smarket)#,rama) #,rama  #,tt,peak)#,fmacd,xmacd)  #rama

    dsignal = decover(signal,3)
    #stock.buyprice = select([dsignal>0],[t[HIGH]])     #涨停价
    stock.buyprice = select([dsignal>0],[stock.open2])     #第二小时开盘
    #print signal

    return dsignal



def attack2(stock,xup=200):#
    ''' 盘中追第二个涨停
    '''
    linelog('%s:%s' % (attack2.__name__,stock.code))
    t = stock.transaction
    
    ama = fama(t[CLOSE])
    rama = rollx(t[CLOSE]*1000/rollx(ama)>=1030)   #-284, p=342

    lup1 = gand((limitup1(t[CLOSE])),t[OPEN]*10000/t[LOW]<10050)

    climit = xfollow(lup1,t[VOLUME])
    #climit = xfollow(limitup2(t[HIGH],t[LOW]),t[VOLUME])   #一字板
    #yup = rollx(gand(stock.slup2,climit,bnot(stock.slup1)),1)  #昨日第二小时涨停并且收盘封住
    yup = rollx(gand(stock.slup2,stock.stoped3,climit,bnot(stock.slup1)),1)  #昨日第二小时涨停并且至收盘都没打开过，含第一小时

    #大盘因素
    #smarket = rollx(gand(stock.ref.t2,stock.ref.t1,stock.ref.t0),1)
    smarket = gand(stock.ref.t2,stock.ref.t1,stock.ref.t0)
    #smarket = gand(strend(stock.ref.diff)>0,strend(stock.ref.diff-stock.ref.dea)>0)

    #yup = gand(stock.slup3,bnot(stock.stoped4))  #前3小时涨停,并且在第四小时打开过
    #yup2 = gand(stock.slup2,bnot(gand(stock.stoped3,stock.stoped4)),bnot(stock.slup1))  #第2小时开始涨停,并且在第3-4小时打开过，否则买不到
    #yup3 = gand(stock.slup3,bnot(stock.stoped4),bnot(gand(stock.slup1,stock.slup2))) 
    #yup2 = gand(stock.touch2,bnot(stock.slup1))  #第2小时开始触及涨停
    #yup3 = gand(stock.touch3,bnot(gand(stock.slup1,stock.slup2))) 
    #yup=gor(yup2,yup3)
    cup = gand(stock.up1,yup,bnot(gand(stock.stoped3,stock.stoped4,stock.stoped2)))

    #因为此时追击点在下午开盘，所以可以观察大盘

    #yup = gand(stock.slup1,bnot(gand(stock.stoped2,stock.stoped3,stock.stoped4)))  #前1小时涨停,并且在第四小时打开过
    #无法判断第四小时涨停的个股涨停后是否打开过

    #必须是跳空且缺口不补

    pre=rollx(t[CLOSE],1)
    tup = np.sign(t[OPEN] * 10000 / pre <= xup + 10000)    #今日开盘大于xup,这个条件是反作用

    #c_ex = lambda c,s:gand(c.g60>3000,s>3000)
    #cs = catalog_signal_cs(stock.c60,c_ex)    

    signal = gand(cup,t[VOLUME]>0,stock.ref.up1)#smarket)#,rama) #,rama  #,tt,peak)#,fmacd,xmacd)  #rama
    #signal = gand(cup,t[VOLUME]>0,rama,r1,smarket,tup)#,rama)   #,tt,peak)#,fmacd,xmacd)  #rama

    dsignal = decover(signal,3)
    #stock.buyprice = select([dsignal>0],[t[HIGH]])     #涨停价
    stock.buyprice = select([dsignal>0],[stock.open2])     #第二小时开盘
    #print signal

    return dsignal


def follow_up2(stock):
    '''第n小时涨停，且涨停板在后两个小时打开过
       第1/2/3小时涨停，后面打开过
       第二小时最好，但仍然只有1/3的概率
        1
        评估:总盈亏值=-5945,交易次数=370        期望值=-396
                总盈亏率(1/1000)=-5945,平均盈亏率(1/1000)=-17,盈利交易率(1/1000)=283
                平均持仓时间=1,持仓效率(1/1000000)=-17000
                赢利次数=105,赢利总值=5427
                亏损次数=262,亏损总值=11372
                平盘次数=3

        2
        评估:总盈亏值=-1925,交易次数=278        期望值=-185
                总盈亏率(1/1000)=-1925,平均盈亏率(1/1000)=-7,盈利交易率(1/1000)=345
                平均持仓时间=1,持仓效率(1/1000000)=-7000
                赢利次数=96,赢利总值=5064
                亏损次数=180,亏损总值=6989
                平盘次数=2

        3
        评估:总盈亏值=-4560,交易次数=413        期望值=-325
                总盈亏率(1/1000)=-4560,平均盈亏率(1/1000)=-12,盈利交易率(1/1000)=288
                平均持仓时间=1,持仓效率(1/1000000)=-12000
                赢利次数=119,赢利总值=6388
                亏损次数=294,亏损总值=10948
                平盘次数=0
       
    '''
    linelog('%s:%s' % (follow_up2.__name__,stock.code))
    t = stock.transaction
    #yup = gand(stock.slup2,bnot(stock.slup1),bnot(gand(stock.stoped3,stock.stoped4)))  #开盘第二小时涨停,并且在第三四小时打开过
    #yup = gand(stock.slup1,bnot(gand(stock.stoped2,stock.stoped3,stock.stoped4)))  #开盘第1小时涨停,并且在第2三四小时打开过
    #yup = gand(stock.slup3,bnot(gor(stock.slup1,stock.slup2)),bnot(stock.stoped4))  #第3小时涨停,并且在第四小时打开过
    
    #开盘涨停
    oup = t[OPEN]*10000 / rollx(t[CLOSE],1) >= 10990
    cup = t[CLOSE]*10000 / rollx(t[CLOSE],1) >= 10990
    hup = t[HIGH]*10000 / rollx(t[CLOSE],1) >= 10990
    lup = t[LOW]*10000 / rollx(t[CLOSE],1) >= 10990
    yup = gand(bnot(oup),cup)


    #无法判断第四小时涨停的个股涨停后是否打开过
    tt = gand(stock.t5,stock.t4,strend(ma(t[CLOSE],250))>0)    #不采用跳点法，可能这是一个敏感位置

    smarket = gand(stock.ref.t2,stock.ref.t1,stock.ref.t0)  #使用当日的大盘情况，差别巨大

    ama = fama(stock.ref.transaction[CLOSE])
    #rama = stock.ref.transaction[CLOSE]*1000/rollx(ama)>=1000   #-284, p=342

    c_ex = lambda c,s:gand(c.g60>5000,s>8000)
    cs = catalog_signal_cs(stock.c60,c_ex)    

    signal = gand(yup,t[VOLUME]>0,smarket,rollx(cs))   #,tt,peak)#,fmacd,xmacd)  #rama

    dsignal = decover(signal,3)

    stock.buyprice = select([dsignal>0],[t[HIGH]])     #涨停价
    
    #print signal

    return dsignal

def nextseller(stock,buy_signal):
    t = stock.transaction
    stock.sellprice = t[CLOSE]
    return rollx(buy_signal)

def fseller_t(stock,buy_signal,stop_times=3*BASE/2,trace_times=2*BASE,**kwargs):
    '''
        应用于B0的ATR止损
        原ATR止损买入信号和卖出信号相抵消, 只适用于B1S1系列
        本函数将同日信号平移一位
    '''
    t = stock.transaction
    trans = t

    dlimit = tracelimit((trans[OPEN]+trans[CLOSE])/2,trans[HIGH],trans[LOW],buy_signal,stock.atr,stop_times,trace_times)

    sdown = under_cross(buy_signal,dlimit,trans[LOW])

    sell_signal = sdown #不能再有确认，因为不知道后面会怎么走

    bs = gand(buy_signal >0,sell_signal >0)

    ssignal = select([bs],[0],default=sell_signal) + rollx(bs)  #如果同日发出，则后移一日
    stock.sellprice = select([rollx(bs)],[t[OPEN]],default=dlimit)  #当日卖出

    return ssignal

def fseller(stock,buy_signal,stop_times=3*BASE/2,trace_times=2*BASE,**kwargs):
    '''
        应用于B0的ATR止损
        原ATR止损买入信号和卖出信号相抵消, 只适用于B1S1系列
        但因为有收盘确认，所以只能用作S1系列
        本函数将同日信号平移一位
    '''
    t = stock.transaction
    trans = t

    dlimit = tracelimit((trans[OPEN]+trans[CLOSE])/2,trans[HIGH],trans[LOW],buy_signal,stock.atr,stop_times,trace_times)

    sdown = under_cross(buy_signal,dlimit,trans[LOW])

    sell_signal = band(sdown,sellconfirm(trans[OPEN],trans[CLOSE],trans[HIGH],trans[LOW]))

    bs = gand(buy_signal >0,sell_signal >0)

    ssignal = select([bs],[0],default=sell_signal) + rollx(bs)  #如果同日发出，则后移一日

    return ssignal

def follow_seller(stock,buy_signal,xstop=25,ret=50,**kwargs):
    '''
        如果价格小于最近5日高点5%，则卖出
        xstop为根据买入价的止损
        ret为从高点向下的回退值
    '''
    t = stock.transaction

    #从顶下落处理,前5天的收盘/开盘的高者和今天的开盘的高者 回落ret之后

    #hhret = gmax(rollx(tmax(gmax(t[OPEN],t[CLOSE]),5),1),t[OPEN])* (1000-ret)/1000
    hhret = gmax(rollx(tmax(t[HIGH],5),1),t[OPEN])* (1000-ret)/1000
    
    #hhret = rollx(tmax(t[HIGH],5),1) * (1000-ret)/1000
    sdl = t[LOW] < hhret
 
    #止损处理2.5%
    stop_price = extend2next(rollx(stock.buyprice,1) * (1000-xstop)/1000)
    stopl = t[LOW] < stop_price

    cut_price = gmin(gmax(hhret,stop_price),t[HIGH])    #首先，止损线和退回线高者先被触及，同时，穿越时可能跳低，所以找与t[HIGH]的低点
    cut_signal = gor(sdl,stopl)

    cut_signal = select([t[VOLUME]>0],[cut_signal]) #默认为0，即未交易的日子卖出信号不能发出，否则会合并到下一交易日

    bs = gand(buy_signal,cut_signal)
    rbs = rollx(bs)

    sell_signal = select([bs],[0],default=cut_signal) + rbs #如果当日冲销，则后推一日，但如果前一日也是当日，则信号被屏蔽

    stock.sellprice = select([cut_signal],[cut_price],default=t[OPEN])
    #止损和退回用cut_price, 当日卖出信号平移用开盘价，停牌平移用开盘价

    return cut_signal

def gup(stock,percent=8500):
    linelog('%s:%s' % (gup.__name__,stock.code))
    t = stock.transaction
    sp = cached_ints(len(t[CLOSE]),percent)
    xcross = gand(cross(sp,stock.g60)>0,strend(stock.g60)>0,t[VOLUME]>0)
    gs = gand(xcross,stock.g20<stock.g60,strend(stock.g20)>0)

    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],60)

    vfilter = rollx(vma_s < vma_l * 4/5,1)

    xatr = stock.atr * BASE / t[CLOSE]

    xref = stock.ref.transaction[CLOSE] >= stock.ref.ma0

    signal = gand(gs,xatr<50,stock.t4,stock.t5,vfilter,stock.ma4>stock.ma5,strend(stock.diff)>0,stock.xup,xref)
    
    return signal

fama = ama_maker()

def up_in_day(stock,xup=200):#xup为涨停次日的开盘涨幅，万分位表示
    ''' 次日开盘小于x%则不追，追进次日开盘小于2%则卖出,收盘未涨停也卖出
        需要屏蔽一字涨停的情况
        my_pricer = (lambda s : s.buyprice,lambda s : s.sellprice)
        myMediator=nmediator_factory(trade_strategy=B0S0_N,pricer = my_pricer)    

        200/-25,-50
        评估:总盈亏值=-10690,交易次数=1194      期望值=-237
                总盈亏率(1/1000)=-10690,平均盈亏率(1/1000)=-9,盈利交易率(1/1000)=268
                平均持仓时间=1,持仓效率(1/1000000)=-9000
                赢利次数=321,赢利总值=22580
                亏损次数=862,亏损总值=33270
                平盘次数=11


        最后发现，第一小时涨停的，第二天追击的风险最大，第二小时涨停的最好,但也都是负的
        
    '''
    linelog('%s:%s' % (up_in_day.__name__,stock.code))
    t = stock.transaction
    climit = xfollow(limitup1(t[CLOSE]),t[VOLUME])
    #yup = rollx(gand(stock.slup1,climit),1)  #昨日开盘前两小时涨停并且收盘封住
    yup = rollx(climit,1)
    pre = rollx(t[CLOSE],1)
    tup = np.sign(t[OPEN] * 10000 / pre >= xup + 10000)    #今日开盘大于xup
    tx = np.sign(t[LOW] * 10000 / pre <= 10990)    #非一字涨停，追
    #tv = xfollow(t[VOLUME].copy(),t[VOLUME])    #不能更改t[VOLUME]本身

    #xmacd = rollx((stock.diff-stock.dea) * 1000 / stock.ma3 > 10,1)
    #fmacd = rollx(stock.diff > stock.dea,1)
    #tdea = strend(stock.dea) < 30

    #u30 = rollx(t[CLOSE]>stock.ma3,1)
    #fma = rollx(gand(stock.ma1 > stock.ma2),1)#,stock.ma2>stock.ma4,stock.ma3>stock.ma4),1)

    #lol = rollx( t[OPEN] * 97 < t[LOW]*100,1) #昨日涨停，但反向震荡不超过3%

    #tlimit = tv / 6 < rollx(tv,1)       #量不能超过前日6倍，越等于开盘量小于前日1/3?
    #tt = rollx(gand(stock.t5,stock.t4,stock.t3,strend(ma(t[CLOSE],250))>0),1) #以昨日趋势为准
    tt = gand(stock.t5,stock.t4,strend(ma(t[CLOSE],250))>0)    #不采用跳点法，可能这是一个敏感位置
    #mg5 = ma(stock.g5,5)
    #xcross = gand(cross(mg5,stock.g5)>0,strend(stock.g5)>0)
    #g = rollx(gand(stock.g60>9000,stock.g20>9000,xcross),1)
    
    #涨停需要领袖群雄10天
    #hh10 = tmax(t[HIGH],10)
    #peak = pre > rollx(hh10,2)
    
    ama = fama(t[CLOSE])
    rama = rollx(ama*1000/rollx(ama)>995)   #-284, p=342

    signal = gand(yup,tup,tx,t[VOLUME]>0,tt)#,rama)   #,tt,peak)#,fmacd,xmacd)  #rama

    dsignal = decover(signal,3)
    stock.buyprice = select([dsignal>0],[t[OPEN]])
    #print signal

    return dsignal


def up_in_hour4(stock,xup=200):#xup为涨停次日的开盘涨幅，万分位表示
    '''第4小时涨停'''
    linelog('%s:%s' % (up_in_hour4.__name__,stock.code))
    t = stock.transaction
    climit = xfollow(limitup1(t[CLOSE]),t[VOLUME])
    y123 = gor(stock.slup1,stock.slup2,stock.slup3)
    yup = rollx(gand(stock.slup4,climit,bnot(y123)),1)  #昨日收盘最后一个小时涨停并且收盘封住
    pre = rollx(t[CLOSE],1)
    tup = np.sign(t[OPEN] * 10000 / pre >= xup + 10000)    #今日开盘大于xup
    tx = np.sign(t[LOW] * 10000 / pre <= 10990)    #非一字涨停，追
    tt = gand(stock.t5,stock.t4,strend(ma(t[CLOSE],250))>0)    #不采用跳点法，可能这是一个敏感位置

    signal = gand(yup,tup,tx,t[VOLUME]>0,tt)#,rama)   #,tt,peak)#,fmacd,xmacd)  #rama

    dsignal = decover(signal,3)
    stock.buyprice = select([dsignal>0],[t[OPEN]])
    #print signal

    return dsignal


def up_in_hour3(stock,xup=200):#xup为涨停次日的开盘涨幅，万分位表示
    '''第3小时涨停'''
    linelog('%s:%s' % (up_in_hour3.__name__,stock.code))
    t = stock.transaction
    climit = xfollow(limitup1(t[CLOSE]),t[VOLUME])
    y12 = gor(stock.slup1,stock.slup2)
    yup = rollx(gand(stock.slup3,climit,bnot(y12)),1)  #昨日开盘第三小时涨停并且收盘封住
    #yup = rollx(gand(stock.slup3,climit),1)  #昨日开盘第三小时及之前涨停并且收盘封住
    pre = rollx(t[CLOSE],1)
    tup = np.sign(t[OPEN] * 10000 / pre >= xup + 10000)    #今日开盘大于xup
    tx = np.sign(t[LOW] * 10000 / pre <= 10990)    #非一字涨停，追
    tt = gand(stock.t5,stock.t4,strend(ma(t[CLOSE],250))>0)    #不采用跳点法，可能这是一个敏感位置

    signal = gand(yup,tup,tx,t[VOLUME]>0,tt)#,rama)   #,tt,peak)#,fmacd,xmacd)  #rama

    dsignal = decover(signal,3)
    stock.buyprice = select([dsignal>0],[t[OPEN]])
    #print signal

    return dsignal


def up_in_hour2(stock,xup=200):#xup为涨停次日的开盘涨幅，万分位表示
    '''第2小时涨停,接近有利可图
        评估:总盈亏值=-172,交易次数=268 期望值=-27
                总盈亏率(1/1000)=-172,平均盈亏率(1/1000)=-1,盈利交易率(1/1000)=309
                平均持仓时间=1,持仓效率(1/1000000)=-1000
                赢利次数=83,赢利总值=6739
                亏损次数=180,亏损总值=6911
                平盘次数=5

    12.
        评估:总盈亏值=-8219,交易次数=700        期望值=-286
                总盈亏率(1/1000)=-8219,平均盈亏率(1/1000)=-12,盈利交易率(1/1000)=255
                平均持仓时间=1,持仓效率(1/1000000)=-12000
                赢利次数=179,赢利总值=13627
                亏损次数=515,亏损总值=21846
                平盘次数=6
    
    前面如果是一字涨停，则可忽略大盘
    '''
    linelog('%s:%s' % (up_in_hour2.__name__,stock.code))
    t = stock.transaction
    climit = xfollow(limitup1(t[CLOSE]),t[VOLUME])
    #climit = xfollow(limitup2(t[HIGH],t[LOW]),t[VOLUME])   #一字板
    #yup = rollx(gand(stock.slup2,climit,bnot(stock.slup1)),1)  #昨日第二小时涨停并且收盘封住
    yup = rollx(gand(stock.slup2,climit),1)  #昨日第二小时涨停并且至收盘都没打开过，含第一小时
    #yup = rollx(climit,1)
    pre = rollx(t[CLOSE],1)
    tup = np.sign(t[OPEN] * 10000 / pre >= xup + 10000)    #今日开盘大于xup
    
    tx = np.sign(t[LOW] * 10000 / pre < 10990)    #非一字涨停，追
    #tt = gand(stock.t5,stock.t4,stock.t3,strend(ma(t[CLOSE],250))>0)    #不采用跳点法，可能这是一个敏感位置
    tt = gand(stock.t5,stock.t4,strend(ma(t[CLOSE],250))>0)    #不采用跳点法，可能这是一个敏感位置

    ama = fama(t[CLOSE])
    rama = rollx(ama*1000/rollx(ama)<=1000)   #-284, p=342

    #cswing = t[CLOSE] * 1000 / pre - 1000  #涨幅
    #cup = select([cswing>0],[cswing])
    #mcup1 = ma(cup,13)
    #mcup2 = ma(cup,30)
    #sm = rollx(gand(mcup1<mcup2),1)

    
    rlimit = limitup1(t[CLOSE])
    times = msum2(rlimit,5)
    r1 = rollx(gand(times==2),1)  #第n个涨停

    #大盘因素
    #smarket = rollx(gand(stock.ref.t2,stock.ref.t1,stock.ref.t0),1)
    #smarket = gand(stock.ref.t2,stock.ref.t1,stock.ref.t0)  #使用当日的大盘情况，差别巨大
    smarket = rollx(gand(stock.ref.t2,stock.ref.t1,stock.ref.t0),1)  #使用当日的大盘情况，差别巨大

    #smart优于tt,这两类条件貌似重合,叠加无效果
    #signal = gand(yup,tup,tx,t[VOLUME]>0,smarket,tt)#,r1)   #,tt,peak)#,fmacd,xmacd)  #rama
    signal = gand(yup,tup,tx,t[VOLUME]>0,smarket,r1,rama)   #,tt,peak)#,fmacd,xmacd)  #rama


    #一字涨停,忽略大盘
    pup = rollx(t[LOW]*10000/pre >=10990,1)
    psignal =  gand(yup,tup,tx,t[VOLUME]>0,r1,rama,pup)

    signal = gor(signal,psignal)

    dsignal = decover(signal,3)
    stock.buyprice = select([dsignal>0],[t[OPEN]])
    #print signal

    return dsignal


def up_in_hour1(stock,xup=200):#xup为涨停次日的开盘涨幅，万分位表示
    '''第1小时涨停'''
    linelog('%s:%s' % (up_in_hour1.__name__,stock.code))
    t = stock.transaction
    climit = xfollow(limitup1(t[CLOSE]),t[VOLUME])
    yup = rollx(gand(stock.slup1,climit),1)  #昨日开盘第一小时涨停并且收盘封住
    pre = rollx(t[CLOSE],1)
    tup = np.sign(t[OPEN] * 10000 / pre >= xup + 10000)    #今日开盘大于xup
    tx = np.sign(t[LOW] * 10000 / pre <= 10990)    #非一字涨停，追
    tt = gand(stock.t5,stock.t4,strend(ma(t[CLOSE],250))>0)    #不采用跳点法，可能这是一个敏感位置

    signal = gand(yup,tup,tx,t[VOLUME]>0,tt)#,rama)   #,tt,peak)#,fmacd,xmacd)  #rama

    dsignal = decover(signal,3)
    stock.buyprice = select([dsignal>0],[t[OPEN]])
    #print signal

    return dsignal

def up_seller(stock,buy_signal,xstop=25,ret=50,**kwargs):
    '''
        如果买入日为阴线，则开盘卖出
        如果价格小于最近5日高点5%，则卖出
        xstop为根据买入价的止损
        ret为从高点向下的回退值
    '''
    t = stock.transaction

    #阴线处理
    sol = rollx(gand(buy_signal,t[CLOSE] < t[OPEN]),1)

    #从顶下落处理,前5天的收盘/开盘的高者和今天的开盘的高者 回落ret之后

    #hhret = gmax(rollx(tmax(gmax(t[OPEN],t[CLOSE]),5),1),t[OPEN])* (1000-ret)/1000
    hhret = gmax(rollx(tmax(t[HIGH],5),1),t[OPEN])* (1000-ret)/1000
   
    sdl = t[LOW] < hhret
 
    #止损处理2.5%
    stop_price = extend2next(rollx(stock.buyprice,1) * (1000-xstop)/1000)   #要求buyprice只有在buyer日才有数据,否则extend2next无意义
    stopl = t[LOW] < stop_price

    cut_price = gmin(gmax(hhret,stop_price),t[HIGH])    #首先，止损线和退回线高者先被触及，同时，穿越时可能跳低，所以找与t[HIGH]的低点
    cut_signal = gor(sdl,stopl)

    cut_signal = select([t[VOLUME]>0],[cut_signal]) #默认为0，即未交易的日子卖出信号不能发出，否则会合并到下一交易日


    ssignal = gor(sol,cut_signal)
    stock.sellprice = select([cut_signal],[cut_price],default=t[OPEN])
    #止损和退回用cut_price, 阴线出局和停牌平移都用开盘价

    return ssignal

def up_seller_old_a(stock,buy_signal,xup=200,**kwargs):
    '''涨幅小于2%则当日开盘价卖出
       收盘未涨停则当日收盘价卖出
       盘中变负则盘中以昨日收盘价卖出
       从对称角度来说，seller:xup应该小于buyer:xup，否则买入日就该卖出，略小为好
    '''
    t = stock.transaction
    pre = rollx(t[CLOSE],1)
    ss = scover(buy_signal,7) - buy_signal    #信号日7天内必须卖出
    #print ss
    pre_low = pre * (xup+10000) / 10000
    u2 = t[OPEN] > pre_low
    uc = t[CLOSE] >= t[OPEN]   #需要排除一字涨停
    uneg = t[LOW] > pre_low
    lo5 = t[OPEN] * 9500/10000
    uol = gand(t[LOW] > lo5,t[LOW]>pre_low)
    uol2 = gand(t[LOW] < lo5,lo5>pre_low)

    #ulimit = t[LOW] > rollx(stock.down_limit,1) #down_limit是根据当天计算的，所以需要平移，有严重问题,down_limit顺序出错

    shold = gor(gand(u2,uc,uneg,uol),t[VOLUME]==0)
    ss2 = greater(ss,shold) #即ss有信号且shold无信号
    #print ss2
    sprice = select([t[OPEN] < pre_low,uol2,t[LOW] < pre_low,t[CLOSE] < t[OPEN],1]
            ,[t[OPEN],lo5,pre_low,t[CLOSE],t[CLOSE]])  
    #uol2情况下实际上可以卖的更高，如开盘后上拉，然后下挫，则下挫5%时抛掉，而不必等开盘下5%
    #这个条件没有办法公式化，因为不知道是先创新高还是先创新低,也许用小时线可以，但剧烈震荡的也仍有问题
    stock.sellprice = sprice

    ss2[-1]=1
    ssignal = ss2
    

    #print buy_signal-ss
    return ssignal

def up_seller_old(stock,buy_signal,xup=200,**kwargs):
    '''涨幅小于2%则当日开盘价卖出
       收盘未涨停则当日收盘价卖出
       盘中变负则盘中以昨日收盘价卖出
       从对称角度来说，seller:xup应该小于buyer:xup，否则买入日就该卖出，略小为好
    '''
    t = stock.transaction
    pre = rollx(t[CLOSE],1)
    l2 = np.sign(gand(t[OPEN] * 10000 / pre <= xup + 10000,t[VOLUME]>0))
    l10 = np.sign(gand(t[CLOSE] * 10000 / pre <= 990 + 10000,t[VOLUME]>0))
    lneg = np.sign(gand(t[LOW] * 10000 / pre <= xup + 10000,t[VOLUME]>0))
    ss = gor(l2,l10,lneg)
    sprice = select([l2,lneg,l10],[t[OPEN],pre*(10000+xup)/10000,t[CLOSE]]) 
    #print sprice
    #ss2 = select([ss!=buy_signal,ss==buy_signal],[ss,rollx(ss,1)])
    ss2 = select([ss!=buy_signal],[ss])
    stock.sellprice = sprice
    #print buy_signal-ss
    return ss2


