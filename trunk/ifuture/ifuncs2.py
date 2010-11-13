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

    signal_da = np.select([sif.time>944],[signal_da],0)


    signal = gand(signal_da
                  ,dnext_cover(cross(sif.dea5x,sif.diff5x)<0,sif.close,sif.i_cof5,1)
                  ,sif.sdiff30x<0
                  ,sif.sdiff3x < sif.sdea3x
                )

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

    signal_da = np.select([sif.time>944],[signal_da],0)


    signal = gand(signal_da
                  ,dnext_cover(cross(sif.dea5x,sif.diff5x)<0,sif.close,sif.i_cof5,1)
                  ,gor(strend2(sif.sdiff30x-sif.sdea30x)<0,sif.s30<0)
                  #,sif.xatr30x < 15000  #越小越好
                  #,sif.xatr < 3000  #越小越好
                  #,sif.xatr3x > sif.mxatr3x
                  #,sif.sdiff30x < sif.sdea30x
                  ,strend2(sif.diff1-sif.dea1)<0
                 )

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

    signal_da = np.select([sif.time>944],[signal_da],0)


    mmxatr = ma(sif.xatr,15)    #以15分钟为平均

    signal = gand(signal_da
                  ,sif.s30 < 0
                  ,sif.t120 < -1    #排除波动
                  ,sif.r60 < -4     #排除波动
                  #,strend2(sif.ma270)<0
                  
                  #,sif.mxatr > rollx(sif.mxatr,270) #在放大中
                  ,mmxatr > rollx(mmxatr,270)
                  ,sif.mxadtr > sif.mxautr
                  ,sif.mxadtr30x > sif.mxautr30x
                  ,sif.xatr<3600
                  ,sif.xatr30x<15000
                )

    return signal * da_cover.direction
da_cover.direction = XSELL
da_cover.priority = 1200

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

    signal = np.select([sif.time>944],[signal],0)
    

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


xxx_break =[
            da_m30,
            da_m30_0,            
            da_cover,
            ua_cover,
            ua_s5,
        ]

xxx_trend = [
            cr3_30b,
            cr3_30s,
        ]

import wolfox.fengine.ifuture.ifuncs2a as ifuncs2a

xxx2 = xxx_trend + xxx_break + ifuncs2a.xfollow + ifuncs2a.xagainst + ifuncs2a.xorb + ifuncs2a.k1s + ifuncs2a.k1s2 + ifuncs2a.xbreak
xxx3 = xxx_trend + xxx_break
xxx2a = xxx_trend + xxx_break

for x in xxx2:
    pass
    #x.stop_closer = atr5_uxstop_t_08_25_B2
    #x.stop_closer = iftrade.atr5_uxstop_t_08_25_B_10
    #x.stop_closer = atr5_uxstop_t_08_25_B26
    #x.priority = 1500
    #x.stop_closer = iftrade.atr5_uxstop_f_A
    #x.stop_closer = iftrade.atr5_uxstop_k_A
    x.stop_closer = iftrade.atr5_uxstop_k_B
    #x.cstoper = iftrade.FBASE_30  #初始止损,目前只在动态显示时用
    #x.cstoper = iftrade.F30  #初始止损
    #x.filter = iftrade.socfilter
    #x.filter = iftrade.nsocfilter
    #x.stop_closer = iftrade.atr5_uxstop_k_oscillating  #震荡期的止损方式




'''
16402 17617 17826 18228 18173 18494 18655 18663
'''


'''
    需要判断一直在创新高的情况
'''



