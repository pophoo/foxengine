# -*- coding: utf-8 -*-


'''
    测试orb
    未测试orb的开盘直接卖出(根据日模式以及与前一日收盘的关系)
    须进一步测试
'''

from wolfox.fengine.ifuture.ibase import *
from wolfox.fengine.ifuture.iftrade import *


###ORB

def orb_normal_day_b(sif,sopened=None):
    dstretch = ma(gmin(sif.opend-sif.lowd,sif.highd-sif.opend),10)
    stretch = dnext(dstretch,sif.close,sif.i_cofd)
    opend = dnext(sif.opend,sif.close,sif.i_oofd)

    signal = cross(opend+stretch,sif.close)
    signal = gand(signal
            )

    return signal * orb_normal_b.direction

orb_normal_day_b.direction = XBUY
orb_normal_day_b.priority = 2480

def orb_normal_5min_b(sif,sopened=None):
    dstretch = ma(gmin(sif.opend-sif.lowd,sif.highd-sif.opend),10)
    stretch = dnext(dstretch,sif.close,sif.i_cofd)
    open5 = np.select([sif.time[sif.i_cof5]==919],[sif.high5],0)
    open5d = dnext(open5,sif.close,sif.i_cof5)

    signal = cross(open5d+stretch,sif.close)
    signal = gand(signal
            )
    return signal * orb_normal_5min_b.direction
orb_normal_5min_b.direction = XBUY
orb_normal_5min_b.priority = 2480

def orb_normal_day_nr_b(sif,sopened=None):
    dstretch = ma(gmin(sif.opend-sif.lowd,sif.highd-sif.opend),10)
    stretch = dnext(dstretch,sif.close,sif.i_cofd)
    opend = dnext(sif.opend,sif.close,sif.i_oofd)

    rd = sif.highd-sif.lowd
    nr = rd<rollx(rd)
    sfilter = dnext_cover(nr,sif.close,sif.i_cofd,265)

    signal = cross(opend+stretch,sif.close)
    signal = gand(signal
                ,sfilter
                )

    return signal * orb_normal_day_nr_b.direction

orb_normal_day_nr_b.direction = XBUY
orb_normal_day_nr_b.priority = 2480

def orb_normal_day_nrx_b(sif,sopened=None,length=4):
    dstretch = ma(gmin(sif.opend-sif.lowd,sif.highd-sif.opend),10)
    stretch = dnext(dstretch,sif.close,sif.i_cofd)
    opend = dnext(sif.opend,sif.close,sif.i_oofd)

    rd = sif.highd-sif.lowd
    nr = rd<rollx(tmin(rd,length-1))
    sfilter = dnext2diff(rollx(nr),sif.close,sif.i_oofd,sif.date)

    signal = cross(opend+stretch,sif.close)
    signal = gand(signal
                ,sfilter
                )

    return signal * orb_normal_day_nrx_b.direction

orb_normal_day_nrx_b.direction = XBUY
orb_normal_day_nrx_b.priority = 2480

def pattern_ux(sopen,sclose):
    return gand(
                rollx(sclose) > rollx(sclose,2)
              )


def pattern_uu(sopen,sclose):
    return gand(sopen > rollx(sclose)
               ,rollx(sclose) > rollx(sclose,2)
              )

def pattern_dd(sopen,sclose):
    return gand(sopen < rollx(sclose)
               ,rollx(sclose) < rollx(sclose,2)
              )

def pattern_ud(sopen,sclose):
    return gand(sopen < rollx(sclose)
               ,rollx(sclose) > rollx(sclose,2)
              )

def pattern_du(sopen,sclose):
    return gand(sopen > rollx(sclose)
               ,rollx(sclose) < rollx(sclose,2)
              )

def pattern_uuu(sopen,sclose):
    return gand(sopen > rollx(sclose)
               ,rollx(sclose) > rollx(sclose,2)
               ,rollx(sclose,2) > rollx(sclose,3) 
              )

def pattern_uux(sopen,sclose):
    return gand(
               rollx(sclose) > rollx(sclose,2)
               ,rollx(sclose,2) > rollx(sclose,3) 
              )

def pattern_dux(sopen,sclose):
    return gand(
               rollx(sclose) > rollx(sclose,2)
               ,rollx(sclose,2) < rollx(sclose,3) 
              )

def pattern_udd(sopen,sclose):
    return gand(sopen < rollx(sclose)
               ,rollx(sclose) < rollx(sclose,2)
               ,rollx(sclose,2) > rollx(sclose,3)  
            )

def pattern_uud(sopen,sclose):
    return gand(sopen < rollx(sclose)
               ,rollx(sclose) > rollx(sclose,2)
               ,rollx(sclose,2) > rollx(sclose,3)                
              )

def pattern_udu(sopen,sclose):
    return gand(sopen > rollx(sclose)
               ,rollx(sclose) < rollx(sclose,2)
               ,rollx(sclose,2) > rollx(sclose,3)                
              )

def pattern_duu(sopen,sclose):
    return gand(sopen > rollx(sclose)
               ,rollx(sclose) > rollx(sclose,2)
               ,rollx(sclose,2) < rollx(sclose,3) 
              )

def pattern_ddd(sopen,sclose):
    return gand(sopen < rollx(sclose)
               ,rollx(sclose) < rollx(sclose,2)
               ,rollx(sclose,2) < rollx(sclose,3)  
            )

def pattern_dud(sopen,sclose):
    return gand(sopen < rollx(sclose)
               ,rollx(sclose) > rollx(sclose,2)
               ,rollx(sclose,2) < rollx(sclose,3)                
              )

def pattern_ddu(sopen,sclose):
    return gand(sopen > rollx(sclose)
               ,rollx(sclose) < rollx(sclose,2)
               ,rollx(sclose,2) < rollx(sclose,3)                
              )


def null_filter(shigh,slow,length):
    return cached_ints(len(shigh),1)

def nr_filter(shigh,slow,length):
    rd = shigh-slow
    nr = rd<rollx(tmin(rd,length-1))
    return nr

def ws_filter(shigh,slow,length):
    rd = shigh-slow
    ws = rd>rollx(tmax(rd,length-1))
    return ws

def id_filter(shigh,slow,length):
    return gand(shigh<rollx(shigh),slow>rollx(slow))

def idnr_filter(shigh,slow,length):
    return gand(shigh<rollx(shigh),slow>rollx(slow),nr_filter(shigh,slow,length))


def orb_normal_day_pattern_nw_b(sif,sopened=None,length=2,pfunc=pattern_uu,filter=null_filter):
    '''
        nr: 
            ++: R=362       
            --: R=130
                ---: 3次全中
                +--: 110 
            +-: 122
                ++-: 一次不中
                -+-: 113
            -+: 0
        另，下叉买入也可,但出击日与上叉在同日
            ++: R=156
            --: R=64
            +-:盈利只靠一次
            -+: R=7
        nr4: 同上 样本太少
        nr7: 同上
        ws: 
            ++: 89
                加上首日限制: R=239
            --:-26 / -100
            +-: -100
            -+: -27
        ws4/7: 均不可
    '''

    dstretch = ma(gmin(sif.opend-sif.lowd,sif.highd-sif.opend),10)
    stretch = dnext(dstretch,sif.close,sif.i_cofd)
    opend = dnext(sif.opend,sif.close,sif.i_oofd)


    pattern = pfunc(sif.opend,sif.closed)

    dpattern = dnext2diff(pattern,sif.close,sif.i_oofd,sif.date)

    sfilter = dnext2diff(rollx(filter(sif.highd,sif.lowd,length)),sif.close,sif.i_oofd,sif.date)

    signal = cross(opend+stretch,sif.close) >0
    signal = gand(signal
                ,sfilter
                ,dpattern
                )

    signal = np.select([gand(sif.time>914,sif.time<1510)],[signal],0)
    
    #signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    #signal = gand(signal_s==1)

    return signal * orb_normal_day_pattern_nw_b.direction
orb_normal_day_pattern_nw_b.direction = XBUY
orb_normal_day_pattern_nw_b.priority = 1400

dnr1_uu_b = fcustom(orb_normal_day_pattern_nw_b,filter=nr_filter)
dnr4_uu_b = fcustom(orb_normal_day_pattern_nw_b,filter=nr_filter,length=4)
dnr1_dd_b = fcustom(orb_normal_day_pattern_nw_b,filter=nr_filter,pfunc=pattern_dd)
dnr4_dd_b = fcustom(orb_normal_day_pattern_nw_b,filter=nr_filter,length=4,pfunc=pattern_dd)
dnr1_ud_b = fcustom(orb_normal_day_pattern_nw_b,filter=nr_filter,pfunc=pattern_ud)
dnr4_ud_b = fcustom(orb_normal_day_pattern_nw_b,filter=nr_filter,pfunc=pattern_ud,length=4)
dws1_uu_b = fcustom(orb_normal_day_pattern_nw_b,filter=ws_filter)

didnr1_uu_b = fcustom(orb_normal_day_pattern_nw_b,filter=idnr_filter)

def orb_normal_day_pattern_nw_s(sif,sopened=None,length=2,pfunc=pattern_uu,filter=null_filter):
    '''
        nr: 
            ++: R=362       
            --: R=130
                ---: 3次全中
                +--: 110 
            +-: 122
                ++-: 一次不中
                -+-: 113
            -+: 0
        另，下叉买入也可,但出击日与上叉在同日
            ++: R=156
            --: R=64
            +-:盈利只靠一次
            -+: R=7
        nr4: 同上 样本太少
        nr7: 同上
        ws: 
            ++: 89
                加上首日限制: R=239
            --:-26 / -100
            +-: -100
            -+: -27
        ws4/7: 均不可
    '''

    dstretch = ma(gmin(sif.opend-sif.lowd,sif.highd-sif.opend),10)
    stretch = dnext(dstretch,sif.close,sif.i_cofd)
    opend = dnext(sif.opend,sif.close,sif.i_oofd)


    pattern = pfunc(sif.opend,sif.closed)

    dpattern = dnext2diff(pattern,sif.close,sif.i_oofd,sif.date)

    sfilter = dnext2diff(rollx(filter(sif.highd,sif.lowd,length)),sif.close,sif.i_oofd,sif.date)

    signal = cross(opend-stretch,sif.close) <0
    signal = gand(signal
                ,sfilter
                ,dpattern
                )

    signal = np.select([gand(sif.time>914,sif.time<1510)],[signal],0)
    
    #signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    #signal = gand(signal_s==1)

    return signal * orb_normal_day_pattern_nw_s.direction
orb_normal_day_pattern_nw_s.direction = XSELL
orb_normal_day_pattern_nw_s.priority = 1400

dnr1_uu_s = fcustom(orb_normal_day_pattern_nw_s,filter=nr_filter)
dnr1_dd_s = fcustom(orb_normal_day_pattern_nw_s,filter=nr_filter,pfunc=pattern_dd)
dnr1_ud_s = fcustom(orb_normal_day_pattern_nw_s,filter=nr_filter,pfunc=pattern_ud)

dnr1_du_s = fcustom(orb_normal_day_pattern_nw_s,filter=nr_filter,pfunc=pattern_du)

#R=171
dnr4_du_s = fcustom(orb_normal_day_pattern_nw_s,filter=nr_filter,pfunc=pattern_du,length=4)
#R=109
dws1_uu_s = fcustom(orb_normal_day_pattern_nw_s,filter=ws_filter)

dws1_ud_s = fcustom(orb_normal_day_pattern_nw_s,filter=ws_filter,pfunc=pattern_ud)
dws1_dd_s = fcustom(orb_normal_day_pattern_nw_s,filter=ws_filter,pfunc=pattern_dd)
dws1_du_s = fcustom(orb_normal_day_pattern_nw_s,filter=ws_filter,pfunc=pattern_du)

def orb_normal_day_pattern_b(sif,sopened=None,pfunc=pattern_uu):
    '''
        ++ R=232
        +- R=131
        -- R=18
        -+ R=-5
        +++ R=158,不如++
        -++ R=878,> ++, 
            去掉每日首次的约束 R=246
        ++- R=-100
        -+- R=153,> +-
        --- R=15
        +-- R=33
            去掉首次约束更好 R=33
        +-+ R=35
        --+ R=-34
        以下去掉首次约束
        ++++ R=59
        -+++ R=66
        +-++ R=60
        --++ R=100,次数=1
    '''

    dstretch = ma(gmin(sif.opend-sif.lowd,sif.highd-sif.opend),10)
    stretch = dnext(dstretch,sif.close,sif.i_cofd)
    opend = dnext(sif.opend,sif.close,sif.i_oofd)

    pattern = pfunc(sif.opend,sif.closed)

    dpattern = dnext2diff(pattern,sif.close,sif.i_oofd,sif.date)

    signal = cross(opend+stretch,sif.close) > 0
    signal = gand(signal
                ,dpattern
                )

    signal = np.select([gand(sif.time>914,sif.time<1510)],[signal],0)

    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal_s==1)

    return signal * orb_normal_day_pattern_b.direction
orb_normal_day_pattern_b.direction = XBUY
orb_normal_day_pattern_b.priority = 1400

#R=221, times=12
dp_uu_b = fcustom(orb_normal_day_pattern_b)
#R=131,times=11
dp_ud_b = fcustom(orb_normal_day_pattern_b,pfunc=pattern_ud)
dp_dd_b = fcustom(orb_normal_day_pattern_b,pfunc=pattern_dd)
dp_du_b = fcustom(orb_normal_day_pattern_b,pfunc=pattern_du)

#R=355, times=4
dp_duu_b = fcustom(orb_normal_day_pattern_b,pfunc=pattern_duu)

#R=153
dp_dud_b = fcustom(orb_normal_day_pattern_b,pfunc=pattern_dud)

def orb_normal_day_pattern_s(sif,sopened=None,pfunc=pattern_uu):
    '''
    '''

    dstretch = ma(gmin(sif.opend-sif.lowd,sif.highd-sif.opend),10)
    stretch = dnext(dstretch,sif.close,sif.i_cofd)
    opend = dnext(sif.opend,sif.close,sif.i_oofd)

    pattern = pfunc(sif.opend,sif.closed)

    dpattern = dnext2diff(pattern,sif.close,sif.i_oofd,sif.date)

    signal = cross(opend-stretch,sif.close) < 0
    signal = gand(signal
                ,dpattern
                ,sif.ltrend<0
                )

    signal = np.select([gand(sif.time>914,sif.time<1510)],[signal],0)

    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal_s==1)

    return signal * orb_normal_day_pattern_s.direction
orb_normal_day_pattern_s.direction = XSELL
orb_normal_day_pattern_s.priority = 1400

dp_uu_s = fcustom(orb_normal_day_pattern_s)
dp_ud_s = fcustom(orb_normal_day_pattern_s,pfunc=pattern_ud)
dp_dd_s = fcustom(orb_normal_day_pattern_s,pfunc=pattern_dd)

#R=25
dp_du_s = fcustom(orb_normal_day_pattern_s,pfunc=pattern_du)
dp_udu_s = fcustom(orb_normal_day_pattern_s,pfunc=pattern_ddu)

dp_dud_s = fcustom(orb_normal_day_pattern_s,pfunc=pattern_dud)


def orb_normal_day_pattern_trend_b(sif,sopened=None,pfunc=pattern_uu):
    '''
        ++ R=350
        +- R=106    #首次约束: 265,但只有3个
        -- R=60     #首次约束: 98
        -+ R=-11    #首次约束: 62
    '''

    dstretch = ma(gmin(sif.opend-sif.lowd,sif.highd-sif.opend),10)
    stretch = dnext(dstretch,sif.close,sif.i_cofd)
    opend = dnext(sif.opend,sif.close,sif.i_oofd)

    trend_line1 = gtrend1(sif.highd,sif.lowd)
    dtrend = strend2(trend_line1)
    thigh = np.select([dtrend>0],[trend_line1])

    dtrend = dnext2diff(rollx(dtrend),sif.close,sif.i_oofd,sif.date)
    dline1 = dnext2diff(rollx(trend_line1),sif.close,sif.i_oofd,sif.date)

    thigh = extend2next(thigh)
    dthigh = dnext2diff(rollx(thigh),sif.close,sif.i_oofd,sif.date)

    pattern = pfunc(sif.opend,sif.closed)

    dpattern = dnext2diff(pattern,sif.close,sif.i_oofd,sif.date)


    signal = cross(opend+stretch,sif.close) > 0
    signal = gand(signal
                ,dpattern
                #,dtrend>0
                ,opend>dline1   #不论是跌涨，都大于dline1
                )

    signal = np.select([gand(sif.time>914,sif.time<1510)],[signal],0)

    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    #signal = gand(signal_s==1)

    return signal * orb_normal_day_pattern_trend_b.direction
orb_normal_day_pattern_trend_b.direction = XBUY
orb_normal_day_pattern_trend_b.priority = 1400

#350/483
dpt_uu_b = fcustom(orb_normal_day_pattern_trend_b,pfunc=pattern_uu)
#106/265
dpt_ud_b = fcustom(orb_normal_day_pattern_trend_b,pfunc=pattern_ud)

#汇合uu和ud R=210, 采用这个
dpt_ux_b = fcustom(orb_normal_day_pattern_trend_b,pfunc=pattern_ux)


dpt_uux_b = fcustom(orb_normal_day_pattern_trend_b,pfunc=pattern_uux)
dpt_dux_b = fcustom(orb_normal_day_pattern_trend_b,pfunc=pattern_dux)

#60/94
dpt_dd_b = fcustom(orb_normal_day_pattern_trend_b,pfunc=pattern_dd)
#-9/69
dpt_du_b = fcustom(orb_normal_day_pattern_trend_b,pfunc=pattern_du)


def orb_normal_day_pattern_trend_s(sif,sopened=None,pfunc=pattern_uu):
    '''
        +-:-
        --:-
        ++:R=111 不取第一个195
        -+:11   不取第一个42
    '''

    dstretch = ma(gmin(sif.opend-sif.lowd,sif.highd-sif.opend),10) 
    stretch = dnext(dstretch,sif.close,sif.i_cofd)
    opend = dnext(sif.opend,sif.close,sif.i_oofd)

    trend_line1 = gtrend1(sif.highd,sif.lowd)
    dtrend = strend2(trend_line1)
    thigh = np.select([dtrend>0],[trend_line1])

    dtrend = dnext2diff(rollx(dtrend),sif.close,sif.i_oofd,sif.date)
    dline1 = dnext2diff(rollx(trend_line1),sif.close,sif.i_oofd,sif.date)

    thigh = extend2next(thigh)
    dthigh = dnext2diff(rollx(thigh),sif.close,sif.i_oofd,sif.date)

    pattern = pfunc(sif.opend,sif.closed)

    dpattern = dnext2diff(pattern,sif.close,sif.i_oofd,sif.date)

    signal = cross(opend-stretch,sif.close) < 0
    signal = gand(signal
                ,dpattern
                #,dtrend<0
                ,opend<dline1   #不论是跌涨，都大于dline1
                )

    signal = np.select([gand(sif.time>914,sif.time<1510)],[signal],0)

    #不取第一个
    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal==1,signal_s>1)

    return signal * orb_normal_day_pattern_trend_s.direction

orb_normal_day_pattern_trend_s.direction = XSELL
orb_normal_day_pattern_trend_s.priority = 1400

#89/195
dpt_uu_s = fcustom(orb_normal_day_pattern_trend_s,pfunc=pattern_uu)
#-66
dpt_ud_s = fcustom(orb_normal_day_pattern_trend_s,pfunc=pattern_ud)
#-19
dpt_dd_s = fcustom(orb_normal_day_pattern_trend_s,pfunc=pattern_dd)
#11/35
dpt_du_s = fcustom(orb_normal_day_pattern_trend_s,pfunc=pattern_du)

def orb_normal_30_pattern_trend_b(sif,sopened=None,pfunc=pattern_uu,filter=null_filter,length=2):
    ''' 3*stretch30
        ++ R=-
        +- R=111 首次:133, s(ma60)>0:166
        -- R=-
        -+ R=-

        stretch_d/2
        +-: sma60>0:179
            -+-:322 #可去掉首次
    '''

    dstretch = ma(gmin(sif.open30-sif.low30,sif.high30-sif.open30),10)
    stretch = dnext_cover(dstretch,sif.close,sif.i_cof30,30)
    
    #dstretch = ma(gmin(sif.opend-sif.lowd,sif.highd-sif.opend),10)/2
    #stretch = dnext(dstretch,sif.close,sif.i_cofd)
    
    open30 = dnext_cover(sif.open30,sif.close,sif.i_cof30,30)

    trend_line1 = gtrend1(sif.high30,sif.low30)
    dtrend = strend2(trend_line1)
    thigh = np.select([dtrend>0],[trend_line1])

    dtrend = dnext_cover(dtrend,sif.close,sif.i_cof30,30)
    dline1 = dnext_cover(trend_line1,sif.close,sif.i_cof30,30)

    thigh = extend2next(thigh)
    dthigh = dnext_cover(thigh,sif.close,sif.i_cof30,30)

    pattern = pfunc(sif.open30,sif.close30)

    dpattern = dnext_cover(pattern,sif.close,sif.i_oof30,30)

    sfilter = dnext_cover(filter(sif.high30,sif.low30,length),sif.close,sif.i_cof30,30)

    signal = cross(open30+stretch,sif.close) > 0
    signal = gand(signal
                ,dpattern
                #,dtrend<0
                ,open30>dline1   #不论是跌涨，都大于dline1
                ,strend2(sif.ma60)>0
                ,sif.strend<0
                ,sfilter
                )

    signal = np.select([gand(sif.time>914,sif.time<1510)],[signal],0)

    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    #signal = gand(signal_s==1)

    return signal * orb_normal_30_pattern_trend_b.direction
orb_normal_30_pattern_trend_b.direction = XBUY
orb_normal_30_pattern_trend_b.priority = 1400

n30pt_uu_b = fcustom(orb_normal_30_pattern_trend_b,pfunc=pattern_uu,filter=nr_filter)
#91 /sma60 R=188
n30pt_ud_b = fcustom(orb_normal_30_pattern_trend_b,pfunc=pattern_ud,filter=null_filter)
#/sma60 R=329
n30pt_dud_b = fcustom(orb_normal_30_pattern_trend_b,pfunc=pattern_dud,filter=null_filter)
#-9
n30pt_du_b = fcustom(orb_normal_30_pattern_trend_b,pfunc=pattern_du,filter=nr_filter)
#-71
n30pt_dd_b = fcustom(orb_normal_30_pattern_trend_b,pfunc=pattern_dd,filter=nr_filter)


def orb_normal_30_pattern_trend_s(sif,sopened=None,pfunc=pattern_uu,filter=null_filter,length=2):
    ''' stretch30
        -+:   sma13<0:    R=112
        --:
        stretch_d/2
    '''

    dstretch = ma(gmin(sif.open30-sif.low30,sif.high30-sif.open30),10) 
    stretch = dnext_cover(dstretch,sif.close,sif.i_cof30,30)
    
    #dstretch = ma(gmin(sif.opend-sif.lowd,sif.highd-sif.opend),10)/2 
    #stretch = dnext(dstretch,sif.close,sif.i_cofd)
    
    open30 = dnext_cover(sif.open30,sif.close,sif.i_cof30,30)

    trend_line1 = gtrend1(sif.high30,sif.low30)
    dtrend = strend2(trend_line1)
    thigh = np.select([dtrend>0],[trend_line1])

    dtrend = dnext_cover(dtrend,sif.close,sif.i_cof30,30)
    dline1 = dnext_cover(trend_line1,sif.close,sif.i_cof30,30)

    thigh = extend2next(thigh)
    dthigh = dnext_cover(thigh,sif.close,sif.i_cof30,30)

    pattern = pfunc(sif.open30,sif.close30)

    dpattern = dnext_cover(pattern,sif.close,sif.i_oof30,30)

    sfilter = dnext_cover(filter(sif.high30,sif.low30,length),sif.close,sif.i_cof30,30)

    signal = cross(open30-stretch,sif.close) < 0
    signal = gand(signal
                ,dpattern
                #,dtrend<0
                ,open30 < dline1   #不论是跌涨，都大于dline1
                ,strend2(sif.ma13) < 0
                ,sif.strend<0
                ,sfilter
                )

    signal = np.select([gand(sif.time>914,sif.time<1510)],[signal],0)

    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    #signal = gand(signal_s==1)

    return signal * orb_normal_30_pattern_trend_s.direction

orb_normal_30_pattern_trend_s.direction = XSELL
orb_normal_30_pattern_trend_s.priority = 1400

n30pt_uu_s = fcustom(orb_normal_30_pattern_trend_s,pfunc=pattern_uu,filter=null_filter)
n30pt_ud_s = fcustom(orb_normal_30_pattern_trend_s,pfunc=pattern_ud,filter=null_filter)
n30pt_dd_s = fcustom(orb_normal_30_pattern_trend_s,pfunc=pattern_dd,filter=null_filter)
#R=112, #继续分解无意义
n30pt_du_s = fcustom(orb_normal_30_pattern_trend_s,pfunc=pattern_du,filter=null_filter)


def orb_normal_15_pattern_trend_b(sif,sopened=None,pfunc=pattern_uu,filter=null_filter,length=2):
    ''' stretch15
    '''

    dstretch = ma(gmin(sif.open15-sif.low15,sif.high15-sif.open15),10) 
    stretch = dnext_cover(dstretch,sif.close,sif.i_cof15,15)
    
    #dstretch = ma(gmin(sif.opend-sif.lowd,sif.highd-sif.opend),10)/3
    #stretch = dnext(dstretch,sif.close,sif.i_cofd)
    
    open15 = dnext_cover(sif.open15,sif.close,sif.i_cof15,15)

    trend_line1 = gtrend1(sif.high15,sif.low15)
    dtrend = strend2(trend_line1)
    thigh = np.select([dtrend>0],[trend_line1])

    dtrend = dnext_cover(dtrend,sif.close,sif.i_cof15,15)
    dline1 = dnext_cover(trend_line1,sif.close,sif.i_cof15,15)

    thigh = extend2next(thigh)
    dthigh = dnext_cover(thigh,sif.close,sif.i_cof15,15)

    pattern = pfunc(sif.open15,sif.close15)

    dpattern = dnext_cover(pattern,sif.close,sif.i_oof15,15)
    
    sfilter = dnext_cover(filter(sif.high15,sif.low15,length),sif.close,sif.i_cof15,15)

    signal = cross(open15+stretch,sif.close) > 0
    signal = gand(signal
                ,dpattern
                ,open15<dline1   #不论是跌涨，都大于dline1
                ,sfilter
                ,sif.ltrend>0
                )

    signal = np.select([gand(sif.time>914,sif.time<1510)],[signal],0)

    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    #signal = gand(signal_s==1)

    return signal * orb_normal_15_pattern_trend_b.direction
orb_normal_15_pattern_trend_b.direction = XBUY
orb_normal_15_pattern_trend_b.priority = 2480

#-60
n15pt_uu_b = fcustom(orb_normal_15_pattern_trend_b,pfunc=pattern_uu,filter=nr_filter)
#-6
n15pt_ud_b = fcustom(orb_normal_15_pattern_trend_b,pfunc=pattern_ud,filter=nr_filter)
#20
n15pt_du_b = fcustom(orb_normal_15_pattern_trend_b,pfunc=pattern_du,filter=nr_filter)
#49/183
n15pt_dd_b = fcustom(orb_normal_15_pattern_trend_b,pfunc=pattern_dd,filter=nr_filter)


def orb_normal_15_pattern_trend_s(sif,sopened=None,pfunc=pattern_uu,filter=null_filter,length=2):
    ''' stretch15
    '''

    dstretch = ma(gmin(sif.open15-sif.low15,sif.high15-sif.open15),10) 
    stretch = dnext_cover(dstretch,sif.close,sif.i_cof15,15)
    
    #dstretch = ma(gmin(sif.opend-sif.lowd,sif.highd-sif.opend),10)/3
    #stretch = dnext(dstretch,sif.close,sif.i_cofd)
    
    open15 = dnext_cover(sif.open15,sif.close,sif.i_cof15,15)

    trend_line1 = gtrend1(sif.high15,sif.low15)
    dtrend = strend2(trend_line1)
    thigh = np.select([dtrend>0],[trend_line1])

    dtrend = dnext_cover(dtrend,sif.close,sif.i_cof15,15)
    dline1 = dnext_cover(trend_line1,sif.close,sif.i_cof15,15)

    thigh = extend2next(thigh)
    dthigh = dnext_cover(thigh,sif.close,sif.i_cof15,15)

    pattern = pfunc(sif.open15,sif.close15)

    dpattern = dnext_cover(pattern,sif.close,sif.i_oof15,15)
    
    sfilter = dnext_cover(filter(sif.high15,sif.low15,length),sif.close,sif.i_cof15,15)

    signal = cross(open15+stretch,sif.close) < 0
    signal = gand(signal
                ,dpattern
                ,sfilter
                ,sif.ltrend<0
                ,sif.strend>0
                )

    signal = np.select([gand(sif.time>914,sif.time<1510)],[signal],0)

    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal_s==1)

    return signal * orb_normal_15_pattern_trend_s.direction
orb_normal_15_pattern_trend_s.direction = XSELL
orb_normal_15_pattern_trend_s.priority = 1400

n15pt_uu_s = fcustom(orb_normal_15_pattern_trend_s,pfunc=pattern_uu,filter=nr_filter)
n15pt_ud_s = fcustom(orb_normal_15_pattern_trend_s,pfunc=pattern_ud,filter=nr_filter)
#19/95/295
n15pt_du_s = fcustom(orb_normal_15_pattern_trend_s,pfunc=pattern_du,filter=nr_filter)
n15pt_dd_s = fcustom(orb_normal_15_pattern_trend_s,pfunc=pattern_dd,filter=nr_filter)


def orb_normal_60_pattern_trend_b(sif,sopened=None,pfunc=pattern_uu,filter=null_filter,length=2):
    ''' #/加首次约束
        d=3*
        ++ R=109/189    
        +- R=173/173    
        -- R=46
        -+ R=-22 
 
        d=2.5*
        ++:80/209
        +-:143/180
        --:28
        -+:70

        d=2*
        ++:91/201
        +-:137/144
        --:6
        -+:70

        d=1.5*
        ++:146/236
        +-:73/135
        --:15
        -+:6

        d=1*
        ++:77/130
        +-:21/105
        --:-14
        -+:3

        d=1* day's stretch
        ++:110/200
        +-:191/254
        --:21/48
        -+:16/-24
    '''

    #dstretch = ma(gmin(sif.open60-sif.low60,sif.high60-sif.open60),10) *6/2
    #stretch = dnext_cover(dstretch,sif.close,sif.i_cof60,60)
    
    dstretch = ma(gmin(sif.opend-sif.lowd,sif.highd-sif.opend),10)
    stretch = dnext(dstretch,sif.close,sif.i_cofd)
    
    open60 = dnext_cover(sif.open60,sif.close,sif.i_cof60,60)

    trend_line1 = gtrend1(sif.high60,sif.low60)
    dtrend = strend2(trend_line1)
    thigh = np.select([dtrend>0],[trend_line1])

    dtrend = dnext_cover(dtrend,sif.close,sif.i_cof60,60)
    dline1 = dnext_cover(trend_line1,sif.close,sif.i_cof60,60)

    thigh = extend2next(thigh)
    dthigh = dnext_cover(thigh,sif.close,sif.i_cof60,60)

    pattern = pfunc(sif.open60,sif.close60)

    dpattern = dnext_cover(pattern,sif.close,sif.i_cof60,60)

    sfilter = dnext_cover(filter(sif.high60,sif.low60,length),sif.close,sif.i_cof60,60)

    signal = cross(open60+stretch,sif.close) > 0
    signal = gand(signal
                ,dpattern
                ,open60>dline1   #不论是跌涨，都大于dline1
                ,sfilter
                )

    signal = np.select([gand(sif.time>914,sif.time<1510)],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    #signal = gand(signal==1)

    return signal * orb_normal_60_pattern_trend_b.direction
orb_normal_60_pattern_trend_b.direction = XBUY
orb_normal_60_pattern_trend_b.priority = 1400
#222/219
n60pt_uu_b = fcustom(orb_normal_60_pattern_trend_b,pfunc=pattern_uu,filter=null_filter)
#215/280
n60pt_ud_b = fcustom(orb_normal_60_pattern_trend_b,pfunc=pattern_ud,filter=nr_filter)
n60pt_uud_b = fcustom(orb_normal_60_pattern_trend_b,pfunc=pattern_uud,filter=nr_filter)
#-22/-8
n60pt_du_b = fcustom(orb_normal_60_pattern_trend_b,pfunc=pattern_du,filter=null_filter)
#56/32
n60pt_dd_b = fcustom(orb_normal_60_pattern_trend_b,pfunc=pattern_dd,filter=ws_filter)


def orb_normal_60_pattern_trend_s(sif,sopened=None,pfunc=pattern_uu,filter=null_filter,length=2):
    ''' #/加首次约束
        -+:77
            --+:243
        --:-90
        ++:-14
        +-:-70
    '''

    dstretch = ma(gmin(sif.open60-sif.low60,sif.high60-sif.open60),10) 
    stretch = dnext_cover(dstretch,sif.close,sif.i_cof60,60)
    
    #dstretch = ma(gmin(sif.opend-sif.lowd,sif.highd-sif.opend),10)
    #stretch = dnext(dstretch,sif.close,sif.i_cofd)
    
    open60 = dnext_cover(sif.open60,sif.close,sif.i_cof60,60)

    trend_line1 = gtrend1(sif.high60,sif.low60)
    dtrend = strend2(trend_line1)
    tlow = np.select([dtrend<0],[trend_line1])

    dtrend = dnext_cover(dtrend,sif.close,sif.i_cof60,60)
    dline1 = dnext_cover(trend_line1,sif.close,sif.i_cof60,60)

    tlow = extend2next(tlow)
    dtlow = dnext_cover(tlow,sif.close,sif.i_cof60,60)

    pattern = pfunc(sif.open60,sif.close60)

    dpattern = dnext_cover(pattern,sif.close,sif.i_cof60,60)


    sfilter = dnext_cover(filter(sif.high60,sif.low60,length),sif.close,sif.i_cof60,60)

    signal = cross(open60 - stretch,sif.close) < 0
    signal = gand(signal
                ,dpattern
                ,open60 < dline1   #不论是跌涨，都大于dline1
                ,sfilter
                ,sif.ltrend<0
                )

    signal = np.select([gand(sif.time>914,sif.time<1510)],[signal],0)

    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    #signal = gand(signal_s==1,signal==1)

    return signal * orb_normal_60_pattern_trend_s.direction

orb_normal_60_pattern_trend_s.direction = XSELL
orb_normal_60_pattern_trend_s.priority = 1400

#3/29
n60pt_uu_s = fcustom(orb_normal_60_pattern_trend_s,pfunc=pattern_uu,filter=nr_filter)
n60pt_duu_s = fcustom(orb_normal_60_pattern_trend_s,pfunc=pattern_duu,filter=nr_filter)
#-30/-41
n60pt_ud_s = fcustom(orb_normal_60_pattern_trend_s,pfunc=pattern_ud,filter=nr_filter)
#14/46  #盈利过度集中
n60pt_du_s = fcustom(orb_normal_60_pattern_trend_s,pfunc=pattern_du,filter=nr_filter)
#-59/-100
n60pt_dd_s = fcustom(orb_normal_60_pattern_trend_s,pfunc=pattern_dd,filter=nr_filter)



def orb_normal_day_pattern_s(sif,sopened=None):
    '''
        ++ R=-61
        +-  -82
        --  -14
        -+  R=25
        +++ -58
        -++ -63
        ++- -56
        -+- R=-100
        --- R=-7
        +-- R=3
        +-+ R=-22
        --+ R=98, 均由某次盈利所得
        以下去掉首次约束
        +--+ R=165  ##
        ---+ R=5
        ++-- R=190, w/l=2/3
        -+-- R=-85
    '''

    dstretch = ma(gmin(sif.opend-sif.lowd,sif.highd-sif.opend),10)
    stretch = dnext(dstretch,sif.close,sif.i_cofd)
    opend = dnext(sif.opend,sif.close,sif.i_oofd)

    pattern = gand(sif.opend > rollx(sif.closed)
                ,rollx(sif.closed) < rollx(sif.closed,2)
                ,rollx(sif.closed,2) < rollx(sif.closed,3)
                ,rollx(sif.closed,3) > rollx(sif.closed,4)
                )

    dpattern = dnext2diff(pattern,sif.close,sif.i_oofd,sif.date)


    signal = cross(opend-stretch,sif.close) < 0
    signal = gand(signal
                ,dpattern
                )

    signal = np.select([gand(sif.time>914,sif.time<1510)],[signal],0)

    #signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    #signal = gand(signal==1)

    return signal * orb_normal_day_pattern_s.direction

orb_normal_day_pattern_s.direction = XSELL
orb_normal_day_pattern_s.priority = 2480


def orb_normal_day_idnrx_b(sif,sopened=None,length=4):
    '''
        --: 338
    '''
    dstretch = ma(gmin(sif.opend-sif.lowd,sif.highd-sif.opend),10)
    stretch = dnext(dstretch,sif.close,sif.i_cofd)
    opend = dnext(sif.opend,sif.close,sif.i_oofd)

    did = dnext2diff(rollx(gand(sif.highd<=rollx(sif.highd),sif.lowd>=rollx(sif.lowd))),sif.close,sif.i_oofd,sif.date)


    rd = sif.highd-sif.lowd
    nr = rd<rollx(tmin(rd,length-1))
    sfilter = gand(dnext2diff(rollx(nr),sif.close,sif.i_oofd,sif.date)
                )
    
    pattern = gand(sif.opend < rollx(sif.closed)
                ,rollx(sif.closed) < rollx(sif.closed,2)
                )

    dpattern = dnext2diff(pattern,sif.close,sif.i_oofd,sif.date)

    signal = cross(opend+stretch,sif.close)
    signal = gand(signal
                ,sfilter
                ,did
                ,dpattern
                )

    return signal * orb_normal_day_idnrx_b.direction
orb_normal_day_idnrx_b.direction = XBUY
orb_normal_day_idnrx_b.priority = 2480


def nr30s(sif,sopened=None):
    r30 = sif.high30 - sif.low30
    
    #r30_x = tmin(r30,3)

    nr = r30<rollx(r30)
    #nr = r30<rollx(r30_x)
    
    sfilter = np.zeros_like(sif.close)
    sfilter[sif.i_cof30] = nr
    sfilter = extend(sfilter,30)

    #rshort,rlong=7,19
    #rsia = rsi2(sif.close,rshort)   #7,19/13,41
    #rsib = rsi2(sif.close,rlong)
    #signal = gand(cross(rsib,rsia)<0,strend2(rsia)<0)

    signal = cross(sif.dea1,sif.diff1)<0

    signal = gand(signal
                ,sfilter
                ,sif.xatr30x<sif.mxatr30x                
                ,sif.mtrend<0
                ,sif.strend<0
                ,sif.s5<0
                ,sif.ma3<sif.ma13
            )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal==1)
    
    return signal * nr30s.direction
nr30s.direction = XSELL
nr30s.priority = 1400


def nr30b(sif,sopened=None):
    '''
        搞，这个居然是抄顶的。全部是正向指标，最后居然是XSELL
        效果倒是不错
    '''
    r30 = sif.high30 - sif.low30
    
    r30_x = tmin(r30,3)

    #nr = r30<rollx(r30)
    nr = r30<rollx(r30_x)
    
    sfilter = np.zeros_like(sif.close)
    sfilter[sif.i_cof30] = nr
    sfilter = extend(sfilter,30)

    #rshort,rlong=7,19
    #rsia = rsi2(sif.close,rshort)   #7,19/13,41
    #rsib = rsi2(sif.close,rlong)
    #signal = gand(cross(rsib,rsia)<0,strend2(rsia)<0)

    signal = cross(sif.dea1,sif.diff1)>0

    signal = gand(signal
                ,sfilter
                ,sif.xatr30x<sif.mxatr30x                
                ,sif.mtrend>0
                ,sif.strend>0
                ,sif.s10>0
                ,strend2(sif.ma30)>0
            )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal==1)
    
    return signal * nr30b.direction
nr30b.direction = XSELL
nr30b.priority = 1400

