# -*- coding: utf-8 -*-

"""
常用的算法的组合
各组合只测试是否能够执行，不测试其逻辑
"""

import numpy as np

from wolfox.fengine.core.utils import fcustom
from wolfox.fengine.core.base import *
from wolfox.fengine.core.d1 import *
from wolfox.fengine.core.d1ex import *
from wolfox.fengine.core.d1indicator import *
from wolfox.fengine.core.d1kline import *


def swingin(shigh,slow,covered,threshold):
    ''' 测试shigh,slow最近covered天内的波动幅度小于threshold
        对任意i属于[0:len(shigh)),有shigh[i] >= slow[i]
        用于涨幅测试
    '''
    return swing2(shigh,slow,covered) > threshold
    

def swingin1(source,covered,threshold):
    ''' 测试source最近covered天内的波动幅度小于threshold
        用于涨幅测试
    '''
    return swing(source,covered) > threshold

def upconfirm(sopen,sclose,shigh):#阳线突破确认
    sksize = ksize(sopen,sclose)
    sksign = ksign(sopen,sclose)
    
    posconsecutive = consecutive(sksign,'a')  #连续阳线数目
    middleconsecutive = consecutive(sksize,'b')  #连续中等实体数目

    #单根大阳线
    onebigpos = np.logical_and(sksign == 'a',sksize == 'a')
    #连续2根中等阳线
    twomiddlepos = np.logical_and( posconsecutive > 1, middleconsecutive > 1)
    #连续3根阳线
    threepos = posconsecutive > 2
    ###否决项
    #长上影三天
    threeupextend = kscmp(sopen,sclose,shigh,sclose,tbig=3000) == 'a'  #上影/实体 > 3为长

    #print kscmp(sopen,sclose,shigh,tmax(sopen,sclose),tbig=3000)
    sconfirm = gor(onebigpos,twomiddlepos,threepos)
    #return sconfirm
    return band(sconfirm,np.logical_not(threeupextend))

def upveto(sopen,sclose,shigh,slow):   #上升否决情况
    sksize = ksize(sopen,sclose)
    sksign = ksign(sopen,sclose)

    negconsecutive = consecutive(sksign,'b')  #连续阴线数目
    middleconsecutive = consecutive(sksize,'b')  #连续中等实体数目
    smallconsecutive = consecutive(sksize,'c')  #连续小实体数目
    
    #大阴线
    onebig = np.logical_and(sksign == 'b',sksize == 'a')
    #连续两根中阴线
    twomiddle = np.logical_and(negconsecutive > 1,middleconsecutive > 1)
    #连续三根小阴线
    threesmall = np.logical_and(negconsecutive > 2,smallconsecutive > 2)

    return gor(onebig,twomiddle,threesmall)

def sellconfirm(sopen,sclose,shigh,slow):   #卖出确认情况：非大阳或者中阳
    sksize = ksize(sopen,sclose)
    sksign = ksign(sopen,sclose)
    #大或中阳线
    big_or_middle = np.logical_or(sksize == 'a',sksize =='b')
    bm_and_pos = np.logical_and(sksign == 'a',big_or_middle)
    return bnot(bm_and_pos)

def simplesell(sbuy,shigh,slow,threshold):
    downl = downlimit(shigh,sbuy,threshold)
    return slow - downl < 0

def tsimplesell(sbuy,shigh,slow,threshold):
    downl = tdownlimit(shigh,sbuy,threshold)
    return slow - downl < 0

def confirmedsell(sbuy,sopen,sclose,shigh,slow,ssignal,threshold):  #ssignal为出发卖出界限的那条线，一般为sclose或slow
    downl = downlimit(shigh,sbuy,threshold)
    return band(ssignal-downl <0,sellconfirm(sopen,sclose,shigh,slow))   #返回int值便于参加运算和转换

def confirmedselll(sbuy,sopen,sclose,shigh,slow,threshold): #以slow为出发条件
    downl = downlimit(shigh,sbuy,threshold)
    return band(slow-downl <0,sellconfirm(sopen,sclose,shigh,slow))   #返回int值便于参加运算和转换

def confirmedsellc(sbuy,sopen,sclose,shigh,slow,threshold): #以sclose为出发条件
    downl = downlimit(shigh,sbuy,threshold)
    return band(sclose-downl <0,sellconfirm(sopen,sclose,shigh,slow)) #返回int值便于参加运算和转换

def downup(source1,source2,belowdays,crossdays=3):
    ''' 判断source2先在source1之上，然后crossdays日内(为避免重合，默认为3)翻下，停留n天后翻上
    '''
    s2_1 = source2 - source1
    s2_lt_1 = s2_1 < 0 #tfilter_lt(s2_1)
    s2_gt_1 = s2_1 > 0 # tfilter_gt(s2_1)
    sdown = sfollow(s2_gt_1,s2_lt_1,crossdays)
    sdown_up = sfollow(sdown,s2_gt_1,belowdays)  #belowdays之内回去
    return sdown_up

def _limit_adjuster(css,cls,covered):#covered不能大于127否则会溢出, np.sign(bool array)返回的是int8数组
    ''' css:压缩后的source_signal,cls:压缩后的limit_signal
        屏蔽cls非空日的那些css信号,使其延后到covered之内的非停板日,或者取消(后面的covered日都停板)
        返回处理后的css
        存在问题是信号的吸收，本来相隔covered-1有2个卖出信号，后一个信号本来应该延续covered个位置,但这里被忽略了. 
            这个忽略因为是在covered之内的新信号,当covered较小时,不会有实质影响(因为可能这个间隔还没出现卖出信号,故此新买入为无效信号)
            如果采用cover来替代repeat,使得这类信号延续,则转换后会因为停板的存在导致中间断开从而这个信号被推迟,更为不妥
    '''
    css_covered = repeat(css,covered)
    #print css,cls,css_covered,derepeat(band(css_covered>0,bnot(cls)))
    return derepeat(band(css_covered > 0,bnot(cls)),covered)    
    
def limit_adjust(source_signal,limit_signal,trans_signal,covered=3):#covered不能大于127否则会溢出, np.sign(bool array)返回的是int8数组
    ''' 根据停板信号limit_signal和交易日信号trans_signal调整原始信号，使原始信号避开停板到开板日
        可能因covered的原因导致连续非停板日中间出现停板日后,信号多发. 但这个可由makke_trade之类的函数处理掉
        只有covered=2时,不会出现这个情况
    '''
    adjuster = fcustom(_limit_adjuster,covered=covered)
    return smooth(trans_signal,source_signal,limit_signal,sfunc=adjuster)

def BS_DUMMY(trans,sbuy,ssell):
    return sbuy,ssell

def B0S0(trans,sbuy,ssell):
    ''' 买卖信号都在当日实现
        t为stock.transaction
        返回经过信号延续、停板和停牌处理的sbuy,ssell
    '''
    #print 'input rolled:',sbuy,ssell
    up_limit_line = limitup1(trans[CLOSE])
    down_limit_line = limitdown1(trans[CLOSE])
    #print 'begin adjust:',up_limit_line,down_limit_line
    sbuy = limit_adjust(sbuy,up_limit_line,trans[VOLUME])
    ssell = limit_adjust(ssell,down_limit_line,trans[VOLUME])
    #print 'end adjust:',ssell
    return sbuy,ssell

def B0S1(trans,sbuy,ssell):
    ''' 买入信号当日,卖出信号次日
        t为stock.transaction
        返回经过信号延续、停板和停牌处理的sbuy,ssell
    '''
    ssell = roll0(ssell)
    #print 'input rolled:',sbuy,ssell
    up_limit_line = limitup1(trans[CLOSE])
    down_limit_line = limitdown2(trans[HIGH],trans[LOW])
    #print 'begin adjust:',up_limit_line,down_limit_line
    sbuy = limit_adjust(sbuy,up_limit_line,trans[VOLUME])
    ssell = limit_adjust(ssell,down_limit_line,trans[VOLUME])
    #print 'end adjust:',ssell
    return sbuy,ssell

def B1S0(trans,sbuy,ssell):
    ''' 买入次日,卖出当日
        t为stock.transaction
        返回经过信号延续、停板和停牌处理的sbuy,ssell
        次日买入只受到一字线影响，而当日卖出受到收盘跌停影响
    '''
    sbuy = roll0(sbuy)
    #print 'input rolled:',sbuy,ssell
    up_limit_line = limitup2(trans[HIGH],trans[LOW])
    down_limit_line = limitdown1(trans[CLOSE])
    #print 'begin adjust:',up_limit_line,down_limit_line
    sbuy = limit_adjust(sbuy,up_limit_line,trans[VOLUME])
    ssell = limit_adjust(ssell,down_limit_line,trans[VOLUME])
    #print 'end adjust:',ssell
    return sbuy,ssell

def B1S1(trans,sbuy,ssell):
    ''' 买卖信号都是次日实现
        trans为stock.transaction
        返回经过信号延续、停板和停牌处理的sbuy,ssell
        次日买卖则只受到一字线的影响
    '''
    #print sbuy,np.sum(sbuy)
    sbuy,ssell = roll0(sbuy),roll0(ssell)
    #print 'input rolled:',sbuy,ssell
    up_limit_line = limitup2(trans[HIGH],trans[LOW])
    down_limit_line = limitdown2(trans[HIGH],trans[LOW])
    #print 'begin adjust:',up_limit_line,down_limit_line
    sbuy = limit_adjust(sbuy,up_limit_line,trans[VOLUME])
    ssell = limit_adjust(ssell,down_limit_line,trans[VOLUME])
    #print 'end adjust:',ssell
    #print sbuy,np.sum(sbuy)
    return sbuy,ssell

def atr_seller(sbuy,trans,satr,times=1000,covered=20): 
    ''' kwargs目的是吸收无用参数，便于cruiser
        times为以0.001为单位的倍数
    '''
    down_limit = tmax(trans[HIGH] - satr * times / 1000,covered)    #最近n天波动下限的最大值
    sdown = equals(cross(down_limit,trans[LOW]),-1)
    return band(sdown,sellconfirm(trans[OPEN],trans[CLOSE],trans[HIGH],trans[LOW]))
        
