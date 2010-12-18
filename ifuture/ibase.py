# -*- coding: utf-8 -*-

IDATE,ITIME,IOPEN,ICLOSE,IHIGH,ILOW,IVOL,IHOLDING,IMID = 0,1,2,3,4,5,6,7,8

#position的标记
LONG,SHORT,EMPTY = -1,1,0   #多仓出钱,淡仓收钱
#是否仅是头寸操作信号. 即不带价格
is_only_position_signal = lambda uprice : np.abs(uprice) == 1


#买入卖出信号的标记
XBUY,XSELL = 1,-1   #买入，卖出信号

#开平仓的标记
XOPEN,XCLOSE = -1,1 #开仓,平仓

#策略趋势 : 顺势、中性、逆势
TFOLLOW,TNORMAL,TAGAINST = 1,0,-1


XBASE = 100 #用于一般化的除数基数

TAX = 10    #tax为0.8个点,设为1

XFOLLOW,XBREAK,XAGAINST,XORB = 1000,500,-500,800

TREND_UP,TREND_DOWN = 1,-1

import numpy as np

from wolfox.fengine.core.base import BaseObject;
from wolfox.fengine.core.d1 import *;
from wolfox.fengine.core.d1ex import *;
from wolfox.fengine.core.d1indicator import *;
from wolfox.fengine.core.d1idiom import *;
from wolfox.fengine.core.utils import *;


def dnext(xsource,xbase,xindex):
    '''
        将长周期的抽样点xsource分派到基础周期xbase，其中这些点的坐标是xindex
        抽样点进行信号覆盖，直到下一信号
    '''
    result = np.zeros_like(xbase)
    result[xindex] = xsource
    result = extend2next(result)
    return result

def dnext2diff(xsource,xbase,xindex,diffbase):
    '''
        将长周期的抽样点xsource分派到基础周期xbase，其中这些点的坐标是xindex
        抽样点进行信号覆盖到diffbase差异日
            xindex最好不是i_cofd，否则马上换日
    '''
    result = np.zeros_like(xbase)
    result[xindex] = xsource
    result = extend2diff(result,diffbase)
    return result


def dnext_cover(xsource,xbase,xindex,length):
    '''
        将长周期的抽样点xsource分派到基础周期xbase，其中这些点的坐标是xindex
        抽样点进行信号覆盖length点
    '''
    result = np.zeros_like(xbase)
    result[xindex] = xsource
    result = extend(result,length)
    return result

import functools

def get_func_attr(func,attr_name):
    cfunc = func
    while(isinstance(cfunc,functools.partial)):
        cfunc = cfunc.func
    return cfunc.__dict__[attr_name]

def get_func(func):
    cfunc = func
    while(isinstance(cfunc,functools.partial)):
        cfunc = cfunc.func
    return cfunc

def func_name(func):
    if 'name' in func.__dict__:
        return func.name
    cfunc = func
    while(isinstance(cfunc,functools.partial)):
        cfunc = cfunc.func
    return str(cfunc)[10:-15]

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

