# -*- coding: utf-8 -*-

"""
常用的算法的组合
各组合只测试是否能够执行，不测试其逻辑
"""

import numpy as np

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
    return np.logical_and(sconfirm,np.logical_not(threeupextend))

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
    return np.logical_not(bm_and_pos)

def simplesell(sbuy,shigh,slow,threshold):
    downl = downlimit(shigh,sbuy,threshold)
    return slow - downl < 0

def tsimplesell(sbuy,shigh,slow,threshold):
    downl = tdownlimit(shigh,sbuy,threshold)
    return slow - downl < 0

def confirmedsell(sbuy,sopen,sclose,shigh,slow,ssignal,threshold):  #ssignal为出发卖出界限的那条线，一般为sclose或slow
    downl = downlimit(shigh,sbuy,threshold)
    return np.sign(np.logical_and(ssignal-downl <0,sellconfirm(sopen,sclose,shigh,slow)))   #返回int值便于参加运算和转换

def confirmedselll(sbuy,sopen,sclose,shigh,slow,threshold): #以slow为出发条件
    downl = downlimit(shigh,sbuy,threshold)
    return np.sign(np.logical_and(slow-downl <0,sellconfirm(sopen,sclose,shigh,slow)))   #返回int值便于参加运算和转换

def confirmedsellc(sbuy,sopen,sclose,shigh,slow,threshold): #以sclose为出发条件
    downl = downlimit(shigh,sbuy,threshold)
    return np.sign(np.logical_and(sclose-downl <0,sellconfirm(sopen,sclose,shigh,slow))) #返回int值便于参加运算和转换

def downup(source1,source2,belowdays,crossdays=3):
    ''' 判断source2先在source1之上，然后crossdays日内(为避免重合，默认为3)翻下，停留n天后翻上
    '''
    s2_1 = source2 - source1
    s2_lt_1 = s2_1 < 0 #tfilter_lt(s2_1)
    s2_gt_1 = s2_1 > 0 # tfilter_gt(s2_1)
    sdown = sfollow(s2_gt_1,s2_lt_1,crossdays)
    sdown_up = sfollow(sdown,s2_gt_1,belowdays)  #belowdays之内回去
    return sdown_up

