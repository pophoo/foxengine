# -*- coding: utf-8 -*-
'''

#######
开始调整算法，以稳定性和趋势发现的必然性为要

因此，主要算法为此类的趋势算法，以及k线算法

其中，趋势不明确时以保守做法，较为可取

#######
小结：
    牛市中，mxatr30x是逐级放大的
            xatr也很大
            震荡和后面的持续上升通常没有atr收紧的环节
    熊市中，比较猥琐，大幅下跌后需要酝酿，将atr收紧后继续下跌
            ???


收盘操作:
    如果到收盘的时候还有持仓，就把平仓的下限条件单开在15:00价格的上下3点上
        上限条件单开在前15分钟最高/低点
        假定15:00的价格为A, 14:45-15:00的最高价为P，最低价为B
    如果是持买仓:
        则下限条件单为 价格低于等于A-3，则以A-4卖出平仓
        上限条件单位为 价格高于等于P，则以P-1卖出平仓
    如果是持卖仓:
        则上限条件单为 价格高于等于A+3，则以A+4买入评仓
        下限条件单位为 价格低于等于B，则以B+1买入平仓
        


'''


from wolfox.fengine.ifuture.ibase import *
import wolfox.fengine.ifuture.iftrade as iftrade


def da_m30(sif,sopened=None):
    '''
        以sdiff30x<0为条件
    '''
    wave = np.zeros_like(sif.close)
    wave[sif.i_cof10] = rollx(sif.atr10) /2/XBASE  #掠过914-919的atr10
    wave = extend2next(wave)
    
    UA,DA,xhigh10,xlow10 = range_a(sif,914,929,wave)

    signal_da = gand(sif.close <= DA
                    )

    #signal_da = np.select([sif.time>944],[signal_da],0)

    signal = gand(signal_da
                  ,dnext_cover(cross(sif.dea5x,sif.diff5x)<0,sif.close,sif.i_cof5,1)
                  ,sif.sdiff30x<0
                  ,sif.sdiff3x < sif.sdea3x
                )
    signal = np.select([sif.time>944],[signal],0)

    return signal * da_m30.direction
da_m30.direction = XSELL
da_m30.priority = 1200


def da_m30_0(sif,sopened=None):
    '''
        以s30为条件
    '''
    wave = np.zeros_like(sif.close)
    wave[sif.i_cof10] = rollx(sif.atr10) /2/XBASE  #掠过914-919的atr10
    wave = extend2next(wave)
    
    UA,DA,xhigh10,xlow10 = range_a(sif,914,929,wave)

    signal_da = gand(sif.close <= DA
                    )

    signal = gand(signal_da
                  ,dnext_cover(cross(sif.dea5x,sif.diff5x)<0,sif.close,sif.i_cof5,1)
                  ,gor(strend2(sif.sdiff30x-sif.sdea30x)<0,sif.s30<0)
                  #,sif.xatr30x < 15000  #越小越好
                  #,sif.xatr < 3000  #越小越好
                  #,sif.xatr3x > sif.mxatr3x
                  #,sif.sdiff30x < sif.sdea30x
                  ,strend2(sif.diff1-sif.dea1)<0
                 )
    
    signal = np.select([sif.time>944],[signal],0)

    return signal * da_m30_0.direction
da_m30_0.direction = XSELL
da_m30_0.priority = 1200


def da_cover(sif,sopened=None):
    '''
        兜底. 
        振荡在放大中
        这里有一个看起来太强的条件: 
            ,mmxatr > rollx(mmxatr,270)
        需要观察效果
    '''
    wave = np.zeros_like(sif.close)
    wave[sif.i_cof10] = rollx(sif.atr10) /2/XBASE  #掠过914-919的atr10
    wave = extend2next(wave)
    
    UA,DA,xhigh10,xlow10 = range_a(sif,914,929,wave)

    signal_da = gand(sif.close <= DA
                    )

    mmxatr = ma(sif.xatr,15)    #以15分钟为平均

    #dmxatr = dsma(sif.xatr,np.select([sif.time==915],[1],0))

    signal = gand(signal_da
                  ,sif.s30 < 0
                  ,sif.t120 < -1    #排除波动
                  ,sif.r60 < -4     #排除波动
                  #,strend2(sif.ma270)<0
                  
                  #,sif.mxatr > rollx(sif.mxatr,270) #在放大中
                  ,mmxatr > rollx(mmxatr,270)  #xatr在放大中,这个条件在单个很有用，合并时被处理掉
                  #,dmxatr > rollx(dmxatr,270)
                  ,sif.mxadtr > sif.mxautr
                  ,sif.mxadtr30x > sif.mxautr30x
                  ,sif.xatr<3600
                  ,sif.xatr30x<15000
                )
    
    signal = np.select([sif.time>944],[signal],0)

    return signal * da_cover.direction
da_cover.direction = XSELL
da_cover.priority = 1200


def cr3_30rb(sif,sopened=None):
    '''
        以s30为条件
        效果差
    '''
    rshort = 7
    rlong = 19
    rsia = rsi2(sif.close3,rshort)   #7,19/13,41
    rsib = rsi2(sif.close3,rlong)
    rsignal = dnext_cover(cross(rsib,rsia)>0,sif.close,sif.i_cof3,1)

    signal = gand(
                  sif.sdma>0
                  #,dnext_cover(cross(sif.dea3x,sif.diff3x)>0,sif.close,sif.i_cof3,1)
                  ,rsignal
                  ,gor(sif.s30>0,strend2(sif.sdiff30x-sif.sdea30x)>0)
                  ,sif.xatr <2000
                  ,sif.xatr15x < 7500
                )

    return signal * cr3_30rb.direction
cr3_30rb.direction = XBUY
cr3_30rb.priority = 1200


def cr3_30rs(sif,sopened=None):
    '''
        以s30为条件
        效果差 
    '''
    rshort = 7
    rlong = 19
    rsia = rsi2(sif.close3,rshort)   #7,19/13,41
    rsib = rsi2(sif.close3,rlong)
    rsignal = dnext_cover(cross(rsib,rsia)<0,sif.close,sif.i_cof3,1)

    signal = gand(
                  sif.sdma<0
                  #,dnext_cover(cross(sif.dea3x,sif.diff3x)>0,sif.close,sif.i_cof3,1)
                  ,rsignal
                  ,sif.r60<0
                  ,strend2(sif.sdiff30x-sif.sdea30x)<0
                  ,sif.xatr <2000
                  ,sif.xatr15x < 7500
                  ,sif.ltrend<0
                  ,sif.mtrend<0
                )

    return signal * cr3_30rs.direction
cr3_30rs.direction = XSELL
cr3_30rs.priority = 1200


def cr3_30b(sif,sopened=None):
    '''
        以s30为条件
    '''

    signal = gand(
                  sif.sdma>0
                  ,dnext_cover(cross(sif.dea3x,sif.diff3x)>0,sif.close,sif.i_cof3,1)
                  ,gor(sif.s30>0,strend2(sif.sdiff30x-sif.sdea30x)>0)
                )

    return signal * cr3_30b.direction
cr3_30b.direction = XBUY
cr3_30b.priority = 1200


def cr3_30s(sif,sopened=None):
    '''
        以s30为条件
    '''

    signal = gand(
                  dnext_cover(cross(sif.dea5x,sif.diff5x)<0,sif.close,sif.i_cof5,1)
                  ,sif.sdma<0
                  ,sif.r60<0
                  ,strend2(sif.sdiff30x-sif.sdea30x)<0
                )

    return signal * cr3_30s.direction
cr3_30s.direction = XSELL
cr3_30s.priority = 1200

cr3_30b.filter = iftrade.socfilter
cr3_30s.filter = iftrade.socfilter


'''
非基本周期rsi的计算
    rshort = 7
    rlong = 19
    rsia = rsi2(sif.close3,rshort)   #7,19/13,41
    rsib = rsi2(sif.close3,rlong)
    rsignal = dnext_cover(cross(rsib,rsia)<0,sif.close,sif.i_cof3,1)

'''

def ua_cover(sif,sopened=None):
    '''
        向上兜底
    '''
    wave = np.zeros_like(sif.close)
    wave[sif.i_cof10] = rollx(sif.atr10) /4/XBASE  #向下放宽
    wave = extend2next(wave)

    UA,DA,xhigh10,xlow10 = range_a(sif,914,929,wave)

    signal_ua = gand(sif.close >= UA
                    )

    signal = gand(signal_ua
                  ,sif.sdma>0
                  ,sif.xstate>0
                  ,sif.s30>0
                  ,sif.xatr15x < 7500
                  ,sif.strend>0
                )

    signal = np.select([sif.time>944],[signal],0)

    return signal * ua_cover.direction
ua_cover.direction = XBUY
ua_cover.priority = 1200


def ua_s5(sif,sopened=None):
    '''
        向上兜底
    '''
    wave = np.zeros_like(sif.close)
    wave[sif.i_cof10] = rollx(sif.atr10) /4/XBASE  #向下放宽
    wave = extend2next(wave)

    UA,DA,xhigh10,xlow10 = range_a(sif,914,944,wave)

    signal_ua = gand(sif.close >= UA
                    )

    signal = gand(signal_ua
                  ,sif.sdma>0
                  ,sif.xstate>0
                  ,sif.s30>0
                  ,sif.xatr15x < 6000
                  ,sif.strend>0
                  ,sif.s5>0
                )

    #signal = np.select([sif.time>944],[signal],0)
    

    return signal * ua_s5.direction
ua_s5.direction = XBUY
ua_s5.priority = 1200

def range_a(sif,tbegin,tend,wave,mlength=0):
    if mlength == 0:
        mlength = tend - tbegin + 1 
    high10 = np.select([gand(sif.time>=tbegin,sif.time<=tend)],[sif.high],default=0)
    low10 = np.select([gand(sif.time>=tbegin,sif.time<=tend)],[sif.low],default=99999999)    


    xhigh10 = np.select([sif.time==tend],[tmax(high10,mlength)],0)
    xlow10 = np.select([sif.time==tend],[tmin(low10,mlength)],0)    

    UA = np.select([sif.time==tend],[xhigh10+wave],0)        
    DA = np.select([sif.time==tend],[xlow10-wave],0)    

    xhigh10 = extend2next(xhigh10)
    xlow10  = extend2next(xlow10)
    UA = extend2next(UA)
    DA = extend2next(DA)

    return UA,DA,xhigh10,xlow10

def br30(sif,sopened=None):
    '''
        5分钟最高突破开盘前30分钟最高之后，下一次1分钟上叉
        属于突破回调的模式
    '''
    
    high30 = np.select([sif.time[sif.i_cof30]==944],[sif.high30],default=0)

    xhigh30,xlow30 = np.zeros_like(sif.diff1),np.zeros_like(sif.diff1)
    xhigh30[sif.i_cof30] = high30   #因为屏蔽了前30分钟，所以i_cof30和i_oof30效果一样

    xhigh30 = extend2next(xhigh30)

    signal = np.zeros_like(sif.diff1)

    signal[sif.i_cof5] = cross(xhigh30[sif.i_cof5],sif.high5)>0

    #signal = sfollow(signal,cross(sif.dea1,sif.diff1)>0,15)
    rshort = 7
    rlong = 19
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    
    signal = sfollow(signal,cross(sif.dea1,sif.diff1)>0,15)    
    #signal = sfollow(signal,cross(rsib,rsia)>0,15)    

    signal = gand(signal
            ,sif.s30>0
            ,sif.mtrend>0
            ,sif.time < 1400    #1400以后突破基本无效
            )

    return signal * br30.direction
br30.direction = XBUY
br30.priority = 1200

def acd_ua(sif,sopened=None):
    '''
        发现前两天不能有信号(不论前次信号胜负)，否则必败
    '''
    wave = np.zeros_like(sif.close)
    wave[sif.i_cof10] = rollx(sif.atr10) *2/3/XBASE  #掠过914-919的atr10
    wave = extend2next(wave)
    
    UA,DA,xhigh10,xlow10 = range_a(sif,914,924,wave)

    xcontinue = 5

    signal_ua = gand(sif.close >= UA
                    ,msum2(sif.close>=UA,xcontinue)>4
                    ,rollx(sif.close,xcontinue)>=UA
                    )

    signal_ua = np.select([sif.time>944],[signal_ua],0) #924之前的数据因为xhigh10是extend2next来的，所以不准

    signal_da = gand(sif.close <= DA
                    ,msum2(sif.close<DA,xcontinue)>=4
                    ,rollx(sif.close,xcontinue)<=DA
                    )

    signal_da = np.select([sif.time>944],[signal_da],0)

    ms_ua = sum2diff(extend2diff(signal_ua,sif.date),sif.date)
    ms_da = sum2diff(extend2diff(signal_da,sif.date),sif.date)

    signal = gand(ms_ua==1         #第一个ua
                ,bnot(ms_da)       #没出现过da 
                ,sif.s30>0
                ,sif.xatr30x<sif.mxatr30x
                )

    return signal * acd_ua.direction
acd_ua.direction = XBUY
acd_ua.priority = 1200

def dbrb(sif,sopened=None):
    '''
        日内新高 + 1点
        日内段刨掉开盘30分钟
    '''
    #di = np.zeros_like(sif.close)
    #di[sif.i_oofd] = 1
    di = np.select([sif.time==944],[1],0)
    dhigh = dmax(sif.high,di)

    signal = cross(rollx(dhigh)+10,sif.close)>0

    signal = gand(signal
            ,sif.r60>20
            #,sif.r120>0
            ,strend2(sif.mxatr)>0
            ,sif.xatr30x < 10000
            ,strend2(sif.ma30)>10
            )

    return signal * dbrb.direction
dbrb.direction = XBUY
dbrb.priority = 1500


####反向模式
def k15_d_a(sif,sopened=None):
    '''
        转折点
        15分钟创120新高后,15分钟内1分钟跌破前最低价
    '''
    
    signal15 = gand(sif.high15>rollx(sif.high15)
                ,sif.low15>rollx(sif.low15)
                ,sif.high15 == tmax(sif.high15,8)   #半日新高
                )

    delay = 15

    bline = dnext_cover(np.select([signal15>0],[sif.low15],[0]),sif.close,sif.i_cof15,delay)
    
    signal = sif.close < bline
    
    signal = gand(signal
            ,sif.r120 > 0
            ,sif.r30 > 0
            ,sif.xatr >sif.mxatr
            ,sif.mxatr > rollx(sif.mxatr,270)
            )
    signal = extend(signal,delay)  #去除delay时间段内的重复信号
    signal = derepeatc(signal)

    return signal * k15_d_a.direction
k15_d_a.direction = XSELL
k15_d_a.priority = 2100 

k15_d_a.filter = iftrade.socfilter

def k15_d_b(sif,sopened=None):
    '''
        15分钟新高后,15分钟内1分钟跌破前15分钟的开盘价(收盘价的低者)/最低价
    '''
    
    trans = sif.transaction

    ma15_60 = ma(sif.close15,60) 
    ma15_30 = ma(sif.close15,30) 
    ma15_3 = ma(sif.close15,3)         
    
    signal15 = gand(
                sif.low15>rollx(sif.low15)
                ,sif.high15 - gmax(sif.open15,sif.close15) > np.abs(sif.open15-sif.close15) #上影线长于实体
                ,sif.high15 == tmax(sif.high15,6)
                ,sif.high15 > gmax(ma15_3,ma15_30,ma15_60)
                ,strend2(sif.diff15x-sif.dea15x)>0
                )

    delay = 20


    bline15 = gmin(sif.open15,sif.close15)
    bline = dnext_cover(np.select([signal15>0],[bline15],[0]),sif.close,sif.i_cof15,delay)

    signal = sif.close < bline

    signal = gand(signal
            ,sif.strend<0
            ,sif.xatr < 1800
            ,sif.xatr30x < 12000
            )
    signal = derepeatc(signal)

    return signal * k15_d_b.direction
k15_d_b.direction = XSELL
k15_d_b.priority = 2100

def k15_d_c(sif,sopened=None):
    '''
        15分钟调整模式
        这里最强的筛选条件是 xatr30x>8000
        说明震荡非常大. 通常是顶部震荡
        效果不错，但是叠加不好
    '''
    
    signal15 = gand(#上15分钟为最高点
                rollx(sif.high15,1) > rollx(sif.high15,2)
                ,rollx(sif.high15,1) > sif.high15
                )

    delay = 30

    bline15 = rollx(sif.low15,1)
    bline = dnext_cover(np.select([signal15>0],[bline15],[0]),sif.close,sif.i_cof15,delay)
    
    signal = sif.close < bline
 
    signal = gand(signal
            ,strend2(sif.mxatr)>0
            ,sif.xatr < sif.mxatr
            ,sif.r60<0       
            ,sif.r20>0
            ,sif.r7<0
           )
    
    signal = derepeatc(signal)

    signal = np.select([sif.time>944],[signal],0)  #如果信号是从93x延续到945以后，那945是必须忽略的

    return signal * k15_d_c.direction
k15_d_c.direction = XSELL
k15_d_c.priority = 2100 

def k15_d_x(sif,sopened=None):
    '''
        15分钟调整模式
        说明震荡非常大. 通常是顶部震荡
    '''
    
    signal15 = gand(
                rollx(sif.high15) == tmax(sif.high15,3)
                ,sif.low15 < rollx(sif.low15)
                )

    delay = 30

    bline15 = sif.low15
    bline = dnext_cover(np.select([signal15>0],[bline15],[0]),sif.close,sif.i_cof15,delay)


    signal = sif.close < bline

    signal = gand(signal
            ,strend2(sif.mxatr)>0
            ,strend2(sif.mxatr30x)<0
            ,sif.xatr<sif.mxatr
            ,sif.sdma<0
            ,sif.r120<0
            ,sif.ma3 < sif.ma13
            ,sif.sdiff30x<0
           )
    signal = derepeatc(signal)

    return signal * k15_d_x.direction
k15_d_x.direction = XSELL
k15_d_x.priority = 2100 


def k15_d_y(sif,sopened=None):
    '''
        15分钟调整模式
        说明震荡非常大. 通常是顶部震荡
    '''
    
    signal15 = gand(
                rollx(sif.high15) == tmax(sif.high15,3)
                ,sif.low15 < rollx(sif.low15)
                )

    delay = 15

    bline15 = sif.low15
    bline = dnext_cover(np.select([signal15>0],[bline15],[0]),sif.close,sif.i_cof15,delay)


    signal = sif.close < bline

    signal = gand(signal
            ,strend2(sif.mxatr)>0
            ,strend2(sif.mxatr30x)<0
            ,sif.xatr<sif.mxatr
            ,sif.ma3<sif.ma13
            ,sif.r30< 0 
           )
    signal = derepeatc(signal)

    return signal * k15_d_y.direction
k15_d_y.direction = XSELL
k15_d_y.priority = 2100 

def k15_d_z(sif,sopened=None):
    '''
        15分钟调整模式
            创新高后7分钟内跌回，并且rsi下叉
        其中主条件是下叉时，跌破该15分钟的最低线            
    '''
    
    signal15 = gand(sif.high15 == tmax(sif.high15,5)
                )

    delay = 15

    bline15 = sif.low15
    bline = dnext_cover(np.select([signal15>0],[bline15],[0]),sif.close,sif.i_cof15,delay)

    rshort,rlong = 7,19
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)

    signal = gand(sif.low < bline
                ,cross(rsib,rsia)<0
                ,strend2(rsia)<0
                )

    signal = gand(signal
            ,sif.xatr > sif.mxatr
            ,sif.xatr > 800
            ,sif.ma5 < sif.ma13
            )

    return signal * k15_d_z.direction
k15_d_z.direction = XSELL
k15_d_z.priority = 2100 

def k15_u_a(sif,sopened=None):
    '''
        15分钟调整后上涨模式
    '''
    
    signal15 = gand(
                rollx(sif.low15,1) < rollx(sif.low15,2)
                ,rollx(sif.low15,1) < sif.low15
                )

    delay = 30

    bline15 = rollx(gmax(sif.open15,sif.close15),1)
    bline = dnext_cover(np.select([signal15>0],[bline15],[0]),sif.close,sif.i_cof15,delay)

    signal = sif.close > bline

    signal = gand(signal
            ,sif.xatr>1000
            ,sif.xatr30x < 6000
            ,strend2(sif.mxatr30x)>0
            ,sif.r60>0
            ,sif.sdma>0
            )
    signal = derepeatc(signal)

    return signal * k15_u_a.direction
k15_u_a.direction = XBUY
k15_u_a.priority = 2100   #r60>0相当于顺势

def k10_d_a(sif,sopened=None):
    '''
        10分钟调整模式
        这里最强的筛选条件是 xatr30x>8000
        说明震荡非常大. 通常是顶部震荡
        适合振荡期 nsocfilter
    '''
    
    signal10 = gand(
                rollx(sif.high10,1) > rollx(sif.high10,2)
                ,rollx(sif.high10,1) > sif.high10
                ,rollx(sif.high10,1) == tmax(sif.high10,4)
                )

    delay = 30
    
    bline10 = rollx(gmin(sif.open10,sif.close10),1)
    bline = dnext_cover(np.select([signal10>0],[bline10],[0]),sif.close,sif.i_cof10,delay)

    signal = sif.close < bline

    signal = gand(signal
            ,sif.xatr<1500
            ,sif.xatr30x > 8000
            ,strend2(sif.mxatr)>0
            ,sif.mtrend>0   #说明是顶，不是途中
            ,sif.r60<0
            )
    signal = derepeatc(signal)

    return signal * k10_d_a.direction
k10_d_a.direction = XSELL
k10_d_a.priority = 2100 

def k10_u_a(sif,sopened=None):
    '''
        10分钟调整后上涨模式
        这里最强的筛选条件是strend2(sif.mxatr30x)>0
        说明震荡在加大
    '''
    
    signal10 = gand(
                rollx(sif.low10,1) < rollx(sif.low10,2)
                ,rollx(sif.low10,1) < sif.low10
                )

    delay = 90

    bline10 = gmax(sif.close10,sif.open10)#sif.high10
    bline = dnext_cover(np.select([signal10>0],[bline10],[0]),sif.close,sif.i_cof10,delay)

    signal = sif.close > bline

    signal = gand(signal
            ,sif.xatr>1000
            ,sif.xatr30x < 6000
            ,strend2(sif.mxatr30x)>0
            ,sif.xatr>sif.mxatr
            ,sif.r60>0
            )
    signal = derepeatc(signal)

    return signal * k10_u_a.direction
k10_u_a.direction = XBUY
k10_u_a.priority = 2100 

def k5_d_a(sif,sopened=None):
    '''
        顶部衰竭模式
        5分钟连续上涨时
            就是说这个一个返回时的支撑点，3分钟内击穿就击穿了
        8分钟吞没是假突破
    '''
    trans = sif.transaction
 
    signal5 = gand(
                #rollx(sif.high5) == tmax(sif.high5,12) #上周期是顶点
                sif.high5 == tmax(sif.high5,12)
             )

    delay = 10

    bline5 = gmin(sif.open5,sif.close5)
    bline = dnext_cover(np.select([signal5>0],[bline5],[0]),sif.close,sif.i_cof5,delay)

    signal = sif.close < bline #-100
    signal = gand(signal
            ,sif.xatr>sif.mxatr
            ,sif.xatr30x > 8000
            ,sif.xatr < 1800
            ,sif.ma3 < sif.ma13
            )

    signal = np.select([sif.time>944],[signal],0)

    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal_s==1)
    
    signal = derepeatc(signal)

    return signal * k5_d_a.direction
k5_d_a.direction = XSELL
k5_d_a.priority = 2100

def k5_d_b(sif,sopened=None):
    '''
        顶部衰竭模式
        5分钟连续上涨时
            就是说这个一个返回时的支撑点
        在下一个五分钟之后的5分钟内击穿
        
    '''
    trans = sif.transaction
 
    signal5 = gand(
                rollx(sif.high5) == tmax(sif.high5,36) #上周期是顶点
             )

    delay = 5

    bline5 = gmin(sif.open5,sif.close5)
    bline = dnext_cover(np.select([signal5>0],[bline5],[0]),sif.close,sif.i_cof5,delay)

    signal = sif.close < bline #-100

    signal = gand(signal
            ,sif.xatr30x < sif.mxatr30x
            ,strend2(sif.ma13)<0
            ,sif.s5<0
            ,sif.r60 > 0
            )

    signal = np.select([sif.time>944],[signal],0)

    #signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    #signal = gand(signal_s==1)
    
    signal = derepeatc(signal)

    return signal * k5_d_b.direction
k5_d_b.direction = XSELL
k5_d_b.priority = 2100

def k5_d_c(sif,sopened=None):
    '''
        顶部衰竭模式c
    '''
    trans = sif.transaction
 
    signal5 = gand(sif.low5>rollx(sif.low5) #孕线
                ,rollx(sif.high5) == tmax(sif.high5,12) #上周期是顶点
             )

    delay = 3

    bline5 = gmin(sif.open5,sif.close5)
    bline = dnext_cover(np.select([signal5>0],[bline5],[0]),sif.close,sif.i_cof5,delay)

    signal = sif.low < bline #-100

    signal = gand(signal
            ,sif.xatr>sif.mxatr
            ,sif.xatr30x > 8000
            ,sif.ma3 < sif.ma13
            )

    signal = np.select([sif.time>944],[signal],0)

    #signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    #signal = gand(signal_s==1)
    
    signal = derepeatc(signal)

    return signal * k5_d_c.direction
k5_d_c.direction = XSELL
k5_d_c.priority = 2100


def k5_d_x(sif,sopened=None):
    '''
        顶部衰竭模式
        5分钟连续上涨时
            单根新高阴线
    '''
    trans = sif.transaction
 
    signal5 = gand(
                sif.high5 == tmax(sif.high5,5) #上周期是顶点
                #,sif.close5 - sif.open5 < 30
             )

    delay = 4

    bline5 = sif.low5
    bline = dnext_cover(np.select([signal5>0],[bline5],[0]),sif.close,sif.i_cof5,delay)
    
    signal = sif.low < bline #-100

    signal = gand(signal
            ,sif.xatr>sif.mxatr
            ,sif.xatr30x > 8000
            ,strend2(sif.mxatr30x)<0
            ,sif.r120<0
            )

    signal = derepeatc(signal)

    return signal * k5_d_x.direction
k5_d_x.direction = XSELL
k5_d_x.priority = 2100

def k5_d_y(sif,sopened=None):
    '''
        顶部衰竭模式3
        5分钟连续上涨衰竭
        
    '''
    trans = sif.transaction
 
    signal5 = gand(sif.close5<rollx(sif.low5) 
                ,rollx(sif.high5) == tmax(sif.high5,54) #上周期是顶点
                ,sif.close5 < sif.open5
             )

    delay = 3

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof5] = signal5

    signal = gand(signal
            ,sif.xatr30x < sif.mxatr30x
            ,strend2(sif.xatr30x)>0
            ,strend2(sif.ma13)<0
            )

    signal = np.select([sif.time>944],[signal],0)

    signal = derepeatc(signal)

    return signal * k5_d_y.direction
k5_d_y.direction = XSELL
k5_d_y.priority = 2100

def k5_u_a(sif,sopened=None):
    '''
        底部衰竭模式
        5分钟底部阴线后出现孕线，后10分钟内1分钟最高线突破该孕线(high+close)/2
        长期顺势，中期逆势，短期顺势
    '''
    trans = sif.transaction
 
    signal5 = gand(sif.high5<rollx(sif.high5)
                ,sif.low5>rollx(sif.low5)
                ,rollx(sif.low5) == tmin(sif.low5,20)
                ,rollx(sif.close5)<rollx(sif.open5)
                )

    delay = 10

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof5] = signal5
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof5] = gmax(sif.open5,sif.close5)#sif.high5#(sif.high5 + sif.close5)/2
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)
    
    #fsignal = cross(bline,sif.high)>0
    fsignal = sif.high > bline

    #signal = np.zeros_like(sif.close)
    #signal[sif.i_cof5] = signal5

    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            ,sif.xatr<2000
            ,sif.xatr>1200
            ,sif.xatr<sif.mxatr
            ,sif.xatr30x > 5000
            ,sif.r120>0
            ,strend2(sif.mxatr)>0
            )

    signal = np.select([sif.time>944],[signal],0)

    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal_s==1)
    
    signal = derepeatc(signal)

    return signal * k5_u_a.direction
k5_u_a.direction = XBUY
k5_u_a.priority = 900

def k5_u_b(sif,sopened=None):
    '''
        底部衰竭模式
        5分钟底部阴线后出现孕线，后10分钟内1分钟最高线突破该孕线(high+close)/2
        效果不佳，稳定性不好
        很难取舍，虽然稳定性不好，但叠加效果好
    '''
    trans = sif.transaction
 
    ma5_60 = ma(sif.close5,60) 
    
    signal5 = gand(sif.high5<rollx(sif.high5)
                ,sif.low5>rollx(sif.low5)
                ,rollx(sif.low5) == tmin(sif.low5,20)
                ,rollx(sif.close5)<rollx(sif.open5)
                ,strend2(ma5_60)<-20
                )

    delay = 10


    ss = np.zeros_like(sif.close)
    ss[sif.i_cof5] = signal5
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof5] = sif.close5 #(sif.high5 + sif.close5)/2
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)
    
    #fsignal = cross(bline,sif.high)>0
    fsignal = sif.high > bline

    #signal = np.zeros_like(sif.close)
    #signal[sif.i_cof5] = signal5

    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            #,strend(sif.ma7)>0
            #,rollx(strend2(sif.sdiff5x-sif.sdea5x),5)<0
            ,sif.xatr > 1200
            ,strend2(sif.ma13)>0
            )

    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal_s==1)
    
    signal = derepeatc(signal)


    return signal * k5_u_b.direction
k5_u_b.direction = XBUY
k5_u_b.priority = 2400  #优先级最低

def k1_u_a(sif,sopened = None):
    '''
        一分钟探底上升的K线模式: 单针底
    '''
    asignal = gand(rollx(sif.low) == tmin(sif.low,9)   #前一分钟是前n-1分钟最小值，且大于当前分钟
                )

    sup = np.select([asignal],[rollx(sif.high)],default=0)
    sup = extend2next(sup)
    sdown = np.select([asignal],[rollx(sif.low)],default=0)
    sdown = extend2next(sdown)
    
    delay = 10

    fsignal = gand(sif.close > sup
                ,tmin(sif.low,5) > sdown    #至少5分钟后才突破
                #,sif.low > sdown
                )

    signal = sfollow(asignal,fsignal,delay)

    signal = gand(signal
                ,sif.xatr2 < sif.mxatr2
                ,sif.xatr2_30x < sif.mxatr2_30x
                ,strend2(sif.mxatr2_30x)>0
                ,sif.r120>0
                ,sif.mtrend<0   #短期反向
                )

    return signal * k1_u_a.direction

k1_u_a.direction = XBUY
k1_u_a.priority = 2100 

def k1_rd_a(sif,sopened = None):
    '''
        #注意，这里的high是最近30分钟中的最低,而不是最高
        这是一个误输入而来的指标
        是一个中继形态
    '''
    signal = gand(rollx(sif.high) == tmin(sif.high,30)   #前一分钟是前n-1分钟最小值，且小于当前分钟
                ,rollx(sif.close)<rollx(sif.open)   #下行
                ,sif.close < rollx(sif.low)
                )

    signal = gand(signal
                ,sif.xatr < 2000
                ,sif.r120<0
                )

    return signal * k1_rd_a.direction

k1_rd_a.direction = XSELL
k1_rd_a.priority = 1500 

def k1_ru_a(sif,sopened = None):
    '''
        上升中继
    '''
    signal = gand(rollx(sif.low) == tmax(sif.low,20)   
                ,rollx(sif.close)>rollx(sif.open)   
                ,sif.close > rollx(sif.high)
                )

    signal = gand(signal
                ,sif.r30>0
                ,sif.r120>0
                )

    return signal * k1_ru_a.direction

k1_ru_a.direction = XBUY
k1_ru_a.priority = 1500 


###指标系列
def rsi_u_a(sif,sopened=None,rshort=7,rlong=19):
    '''
        计算创当日新高后，从暴力起涨点算起回撤不到40%，然后再上升
        要求在上涨途中，即30分钟的120线向上
    '''
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    #signal = cross(rsib,rsia)>0    
    signal = gand(cross(rsib,rsia)>0,strend2(rsia)>0)

    signal = gand(signal
            ,sif.xatr < sif.mxatr
            ,sif.xatr < 1800 #越小越好
            ,sif.high > sif.dhigh - (sif.dhigh - sif.dlow2) *0.4    #回撤越小越好
            ,sif.xatr30x < 12000    #这个条件几乎等于没有

            ,sif.idhigh >= sif.idlow    #高点后于低点,必要性不大。
            ,sif.r120 > 0 #去掉毛刺
            
            ,sif.sdma > 0
            ,sif.ma3 > sif.ma13
            )

    return signal * rsi_u_a.direction
rsi_u_a.direction = XBUY
rsi_u_a.priority = 1500

def rsi_u_b(sif,sopened=None,rshort=7,rlong=19):
    '''
        计算创当日新高后，从暴力起涨点算起回撤不到40%，然后再上升
        要求在上涨途中，即30分钟的120线向上
    '''
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    #signal = cross(rsib,rsia)>0    
    signal = gand(cross(rsib,rsia)>0,strend2(rsia)>0)

    signal = gand(signal
            ,sif.xatr < 1800 #越大越好
            ,sif.xatr > 1200 
            ,sif.high > sif.dhigh - (sif.dhigh - sif.dlow2) *0.4    #回撤越小越好
            ,strend2(sif.mxatr30x)>0

            ,sif.r120 > 10 #去掉毛刺
            ,sif.r60>10

            )

    return signal * rsi_u_b.direction
rsi_u_b.direction = XBUY
rsi_u_b.priority = 1500


def rsi_d_a(sif,sopened=None,rshort=7,rlong=19):
    '''
        计算创当日新低后，从暴力起跌点算起回撤不到40%，然后再下降
        要求在下降途中，即30分钟的120线向下
        与上涨不同的是，下跌一半比较墨迹，所以容易缩量
    '''
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    #signal = cross(rsib,rsia)>0    
    signal = gand(cross(rsib,rsia)>0,strend2(rsia)>0)

    signal = gand(signal
            #,sif.xatr<2000  #越小越好
            ,sif.xatr < sif.mxatr
            ,sif.xatr30x < 12000
            ,sif.low < sif.dlow + (sif.dhigh2 - sif.dlow) *0.3  #低点先冲破. 下跌的时候一般比较狠
            ,sif.r120 < 10 
            ,sif.sdma < 0
            ,sif.r30 < 0
            ,sif.xatr < 1500
    )

    return signal * rsi_d_a.direction
rsi_d_a.direction = XSELL
rsi_d_a.priority = 1500

def rsi_u_c(sif,sopened=None,rshort=7,rlong=19):
    '''
    '''

    #signal = cross(sif.dea1,sif.diff1)>0
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    #signal = cross(rsib,rsia)>0    
    signal = gand(cross(rsib,rsia)>0,strend2(rsia)>0)

    signal = gand(signal
                ,sif.ltrend>0
                ,sif.s10>0                
                ,sif.s3>0
                ,sif.xatr30x<sif.mxatr30x
                ,sif.xatr<sif.mxatr
                ,sif.xatr > 600
                ,sif.xatr30x < 8000
                ,strend2(sif.mxatr)<0
                ,sif.sdma>0
            )
    signal = np.select([sif.time>944],[signal],0)

    return signal * rsi_u_c.direction
rsi_u_c.direction = XBUY
rsi_u_c.priority = 1500

def rsi_u_x(sif,sopened=None,rshort=7,rlong=19):
    '''
        去掉s30限制
        比较妥当的是 7/19和13/41参数,其中前者明显优于后者
        这个一个主力算法，虽然R比较低
    '''

    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    signal = gand(cross(rsib,rsia)>0,strend2(rsia)>0)

    signal = gand(signal
                ,sif.s3>0
                ,sif.s15>0
                ,sif.xatr30x<6000
                ,strend2(sif.mxatr)>0
                ,sif.r20>0
                ,sif.sdiff5x>0
                )
    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal==1)

    return signal * rsi_u_x.direction
rsi_u_x.direction = XBUY
rsi_u_x.priority = 1500

def rsi_u_y(sif,sopened=None,rshort=7,rlong=19):
    '''
    '''

    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    signal = gand(cross(rsib,rsia)>0,strend2(rsia)>0)


    signal = gand(signal
            ,strend2(sif.mxatr30x)>0
            ,strend2(sif.mxatr)>0
            ,sif.r60>20
            ,strend2(sif.ma30)>0
            ,sif.idhigh2 > sif.idlow2
            ,gand(sif.close - sif.open < 120,rollx(sif.close) - sif.open < 200)#: 快速拉升过滤
            )
    signal = np.select([sif.time>944],[signal],0)

    #signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    #signal = gand(signal==1)

    return signal * rsi_u_y.direction
rsi_u_y.direction = XBUY
rsi_u_y.priority = 1500


def rsi_d_b(sif,sopened=None,rshort=7,rlong=19):
    rsia = rsi2(sif.close,rshort)   
    rsib = rsi2(sif.close,rlong)
    #signal = cross(rsib,rsia)<0    
    signal = gand(cross(rsib,rsia)<0,strend2(rsia)<0)

    signal = gand(signal
            ,sif.sdiff30x<0            
            ,sif.xatr30x<6000
            ,sif.strend<0
            ,strend2(sif.ma30)<0
            ,sif.xatr < 1000
            ,sif.xatr < sif.mxatr
            ,sif.r120<0
            )

    return signal * rsi_d_b.direction
rsi_d_b.direction = XSELL
rsi_d_b.priority = 1500

def rsi_d_c(sif,sopened=None,rshort=7,rlong=19):
    '''
       使用sif.xatr30x>sif.mxatr30x 
       表示跌势确立初步时，大幅震荡
    '''

    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    
    #signal = cross(rsib,rsia)<0    
    signal = gand(cross(rsib,rsia)<0,strend2(rsia)<0)

    signal = gand(signal
            ,sif.xatr30x<6000
            ,sif.ms<0
            ,sif.mtrend<0
            ,sif.xatr30x>sif.mxatr30x
            ,sif.xatr>sif.mxatr
            )

    signal = np.select([sif.time>944],[signal],0)


    return signal * rsi_d_c.direction
rsi_d_c.direction = XSELL
rsi_d_c.priority = 1500

def rsi_d_x(sif,sopened=None,rshort=7,rlong=19):
    '''
        每天的第一次符合条件的机会为最佳机会
        一旦第一次失败，后面的都被屏蔽
        比较妥当的是 7/19和13/41参数,其中前者明显优于后者
        但是合并有副作用
    '''

    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    #signal = cross(rsib,rsia)<0    
    signal = gand(cross(rsib,rsia)<0,strend2(rsia)<0)

    signal = gand(signal
            ,sif.s30<0
            ,strend2(sif.ma30)<0
            ,sif.mtrend<0
            ,sif.xatr < sif.mxatr
            ,sif.xatr < 2000
            ,strend2(sif.mxatr)>0
            ,sif.xatr30x < sif.mxatr30x
            )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal==1)

    return signal * rsi_d_x.direction
rsi_d_x.direction = XSELL
rsi_d_x.priority = 1500


def macd_d_a(sif,sopened=None):
    '''
        操作策略，失败一次之后当日就不应该再操作
        成功的话，可以继续操作，参见macd_short_x2
    '''
    signal = gand(cross(sif.dea1,sif.diff1)<0,strend2(sif.diff1)<0)

    signal = gand(signal
            ,sif.ltrend<0            
            #,sif.mtrend < 0
            ,strend2(sif.ma30)<0
            ,sif.ma5 < sif.ma13
            #,sif.xatr>800
            ,sif.sdiff30x<0
            #,sif.xatr30x < sif.mxatr30x
            ,strend2(sif.mxatr30x)<0
            )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal == 1)

    return signal * macd_d_a.direction
macd_d_a.direction = XSELL
macd_d_a.priority = 1500


def macd_d_b(sif,sopened=None):
    '''
        跌势确立后需要缩小震荡然后继续下跌
        这个被macd_short_x包含
    '''
    signal = gand(cross(sif.dea1,sif.diff1)<0,strend2(sif.diff1)<0)

    signal = gand(signal
            ,sif.ltrend<0            
            ,sif.mtrend<0
            ,sif.r120<0
            ,strend2(sif.ma30)<0
            ,sif.sdiff30x<0
            ,sif.xatr30x<10000#sif.mxatr30x
            )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal == 1)

    return signal * macd_d_b.direction
macd_d_b.direction = XSELL
macd_d_b.priority = 1000   #提高优先级


def macd_d_c(sif,sopened=None):
    '''
        高度顺势放空操作
        历史最悠久的方法
    '''
    ksfilter = gand(sif.open - sif.close < 60,rollx(sif.open - sif.close) < 120,sif.xatr<2000)

    signal = gand(cross(sif.dea1,sif.diff1)<0
            ,sif.mtrend < 0
            ,sif.strend<0
            ,sif.sdiff30x<0
            ,sif.sdiff5x<0
            )
    signal = gand(signal
            ,sif.ma3 < sif.ma13
            ,strend2(sif.ma30)<0
            ,ksfilter
            ,sif.xatr30x<6000
            ,sif.xatr < 1000
            #,sif.xatr30x < sif.mxatr30x    #单独效果很好，但是合并效果不好
            )

    return signal * macd_d_c.direction
macd_d_c.direction = XSELL
macd_d_c.priority = 1500

def up0(sif,sopened=None):
    '''
        上穿0线
        是逆势的
    '''
    trans = sif.transaction

    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1)>0
            ,sif.s30>0
            ,sif.s3>0
            ,sif.sdiff5x<0
            ,strend2(sif.ma30)>0
            ,strend2(sif.diff1)>3
            ,sif.xatr < 1500
            ,sif.xatr30x>6000
            ,gand(sif.close - sif.open < 120,rollx(sif.close) - sif.open < 200)#: 快速拉升过滤
            )

    return signal * up0.direction
up0.direction = XBUY
up0.priority = 2100  #


def allup(sif,sopened=None):
    '''
        多头排列
    '''
    signal = gand(sif.ma5>sif.ma13
            ,sif.ma13>sif.ma30
            ,sif.ma60>sif.ma120
            ,strend2(sif.ma270)>0
            ,sif.xatr>800
            ,sif.xatr30x<6000
            ,strend2(sif.mxatr30x)>0
            ,strend2(sif.mxatr)>0
            )

    signal = np.select([sif.time>944],[signal],0)

    return signal * allup.direction
allup.direction = XBUY
allup.priority = 1500


def down01x(sif,sopened=None): #++
    ''' 
        30分钟<0且下行
        5分钟>0且下行
    '''

    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1)<0
            ,sif.ltrend<0
            ,sif.sdiff30x<0
            ,sif.sdiff5x>0
            ,sif.xatr60x<sif.mxatr60x
            ,sif.xatr>sif.mxatr
            )
    return signal * down01x.direction
down01x.direction = XSELL
down01x.priority = 1500

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

    signal = gand(signal
            ,sif.mtrend<0            
            ,sif.ltrend<0
            ,strend2(sif.mxatr)<0
            )
    
    return signal * xdown60.direction
xdown60.direction = XSELL
xdown60.priority = 1500 

def xud30b(sif,sopened=None):
    '''
        顺势
    '''

    mxc = xc0c(sif.open30,sif.close30,sif.high30,sif.low30,13) > 0
    signal30 = gand(mxc
                ,sif.xatr30<sif.mxatr30
                ,sif.xatr30<8000    #这个条件可以放宽?
                #,strend2(sif.mxatr30)<0
                )

    signal = np.zeros_like(sif.diff1)
    signal[sif.i_cof30] = signal30

    signal = gand(signal
            ,sif.s15>0
            #,sif.s30>0
            )

    return signal * xud30b.direction
xud30b.direction = XBUY
xud30b.priority = 1200


def ma1x(sif,opened=None,length=60):
    ''' 
        1分钟均线
        第一次碰线
    '''
    bma = ma(sif.close,length)
    
    signal = cross(bma,sif.low)>0

    signal = gand(signal
                ,strend2(bma)>0
                ,sif.ltrend>0
                ,sif.mtrend>0
                ,sif.s30>0
                ,sif.ma3>sif.ma13
                ,sif.sdma>0
                ,sif.r120>0
            )
    signal = np.select([sif.time>944],[signal],0)

    signal = derepeatc(signal)

    return signal * ma1x.direction
ma1x.direction = XBUY
ma1x.priority = 2100

def ma60_short(sif,sopened=None):
    ''' ma60拐头
    '''
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)
 
    msignal = gand(strend(sif.ma60) == -1
                )
    fsignal = gand(cross(sif.dea1,sif.diff1)<0
                ,strend2(sif.sdiff5x-sif.sdea5x)>0
                ,ksfilter                
                ,sif.xatr3x>sif.mxatr3x
                ,sif.r60<0
                )
    signal = sfollow(msignal,fsignal,5)
    return signal * ma60_short.direction
ma60_short.direction = XSELL
ma60_short.priority = 1901

ama1 = ama_maker()
ama2 = ama_maker(covered=30,dfast=6,dslow=100)
def ama_short(sif,sopened=None): #+
    trans = sif.transaction
    xama1 = ama1(trans[ICLOSE])
    xama2 = ama2(trans[ICLOSE])
    signal = gand(cross(xama2,xama1)<0
            ,sif.xatr<1200
            )
    return signal * XSELL
ama_short.direction = XSELL
ama_short.priority = 1600


#######filter设置

br30.filter = iftrade.ocfilter
acd_ua.filter = iftrade.ocfilter
dbrb.filter = iftrade.ocfilter


k15_d_a.filter = iftrade.socfilter
k15_d_b.filter = iftrade.ocfilter
k15_d_c.filter = iftrade.ocfilter
k15_d_x.filter = iftrade.ocfilter
k15_d_y.filter = iftrade.ocfilter
k15_d_z.filter = iftrade.ocfilter
k15_u_a.filter = iftrade.ocfilter
k10_d_a.filter = iftrade.nsocfilter
k10_u_a.filter = iftrade.socfilter
k5_d_a.filter = iftrade.nsocfilter
k5_d_b.filter = iftrade.ocfilter
k5_d_c.filter = iftrade.ocfilter
k5_d_x.filter = iftrade.ocfilter
k5_d_y.filter = iftrade.ocfilter
k5_u_a.filter = iftrade.ocfilter
k5_u_b.filter = iftrade.ocfilter
k1_u_a.filter = iftrade.ocfilter

k1_rd_a.filter = iftrade.ocfilter
k1_ru_a.filter = iftrade.ocfilter

rsi_u_a.filter = iftrade.ocfilter
rsi_u_b.filter = iftrade.ocfilter
rsi_u_c.filter = iftrade.ocfilter
rsi_u_x.filter = iftrade.ocfilter
rsi_u_y.filter = iftrade.socfilter

rsi_d_a.filter = iftrade.ocfilter
rsi_d_b.filter = iftrade.ocfilter
rsi_d_c.filter = iftrade.ocfilter
rsi_d_x.filter = iftrade.ocfilter

macd_d_a.filter = iftrade.socfilter
macd_d_b.filter = iftrade.socfilter
macd_d_c.filter = iftrade.socfilter

down01x.filter = iftrade.nsocfilter
up0.filter = iftrade.ocfilter
xdown60.filter = iftrade.ocfilter
xud30b.filter = iftrade.ocfilter
ma1x.filter = iftrade.ocfilter
ma60_short.filter = iftrade.socfilter
ama_short.filter = iftrade.socfilter
#k5_d_c.stop_closer = iftrade.atr5_uxstop_t_08_25_B2

###集合
xxx_break =[
            da_m30,
            da_m30_0,            
            da_cover,
            ua_cover,
            ua_s5,
            br30,
            acd_ua,
            dbrb,
        ]

for x in xxx_break:
    pass
    x.stop_closer = iftrade.atr5_uxstop_k_180
    #实际上只放宽了ua_s5
    if 'filter' not in x.__dict__:
        x.filter = iftrade.socfilter_k1s

xxx_against = [
            k15_d_a,
            k15_d_b,
            k15_d_c,
            k15_d_x,
            k15_d_y,
            k15_d_z,
            k15_u_a,

            k10_d_a,
            k10_u_a,

            k5_d_a,
            k5_d_b,            
            k5_d_c,
            k5_d_x,
            #k5_d_y,

            k5_u_a,
            k5_u_b,

            k1_u_a,

            k1_rd_a,
            k1_ru_a,
            
            up0,
        ]

for x in xxx_against:
    x.stop_closer = iftrade.atr5_uxstop_k_180

xxx_follow = [
            rsi_u_a,
            rsi_u_b,
            rsi_u_c,
            rsi_u_x,
            rsi_u_y,
            rsi_d_a,
            rsi_d_b,
            rsi_d_c,
            rsi_d_x,

            macd_d_a,
            macd_d_b,
            macd_d_c,
            allup,
            xdown60,
            down01x,
            xud30b,
            ma1x,
            ma60_short,
            ama_short,
        ]
for x in xxx_follow:
    x.stop_closer = iftrade.atr5_uxstop_k_180



xxx_trend = [
            cr3_30b,
            cr3_30s,
            #cr3_30rb,
            #cr3_30rs,
        ]


import wolfox.fengine.ifuture.ifuncs2a as ifuncs2a

for x in ifuncs2a.k1s + ifuncs2a.k1s2 + ifuncs2a.xorb:
    x.stop_closer = iftrade.atr5_uxstop_k_180
    x.cstoper = iftrade.FBASE_30  #初始止损,目前只在动态显示时用
    

xxx = xxx_trend + xxx_break + xxx_against + xxx_follow
xxx1 = xxx_trend + xxx_break + xxx_against + xxx_follow
xxx2 = xxx1  + ifuncs2a.k1s + ifuncs2a.k1s2 + ifuncs2a.xorb
xxx3 = xxx1+ ifuncs2a.k1s + ifuncs2a.k1s2 + ifuncs2a.xorb
xxx2a = xxx1

for x in xxx1:
    pass
    #if 'stop_closer' not in x.__dict__: #不应该有例外，否则比较难以实际操作
    #    x.stop_closer = iftrade.atr5_uxstop_k_B

for x in xxx2:
    pass
    #x.stop_closer = iftrade.atr5_uxstop_t_08_25_B2
    #x.stop_closer = iftrade.atr5_uxstop_t_08_25_B_10
    #x.stop_closer = atr5_uxstop_t_08_25_B26
    #x.priority = 1500
    #x.stop_closer = iftrade.atr5_uxstop_f_A
    #x.stop_closer = iftrade.atr5_uxstop_k_A
    #x.stop_closer = iftrade.atr5_uxstop_k_135
    x.cstoper = iftrade.FBASE_30  #初始止损,目前只在动态显示时用
    #x.cstoper = iftrade.F30  #初始止损
    #x.filter = iftrade.socfilter
    #x.filter = iftrade.nsocfilter
    #x.stop_closer = iftrade.atr5_uxstop_k_oscillating  #震荡期的止损方式



