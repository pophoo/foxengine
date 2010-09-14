# -*- coding: utf-8 -*-

IDATE,ITIME,IOPEN,ICLOSE,IHIGH,ILOW,IVOL,IHOLDING,IMID = 0,1,2,3,4,5,6,7,8

#position的标记
LONG,SHORT,EMPTY = -1,1,0   #多仓出钱,淡仓收钱

#买入卖出信号的标记
XBUY,XSELL = 1,-1   #买入，卖出信号

#开平仓的标记
XOPEN,XCLOSE = -1,1 #开仓,平仓

XBASE = 100 #用于一般化的除数基数

TAX = 10    #tax为0.8个点,设为1

XFOLLOW,XBREAK,XAGAINST = 1000,500,-500

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

def dnext_cover(xsource,xbase,xindex,length):
    '''
        将长周期的抽样点xsource分派到基础周期xbase，其中这些点的坐标是xindex
        抽样点进行信号覆盖length点
    '''
    result = np.zeros_like(xbase)
    result[xindex] = xsource
    result = extend(result,length)
    return result

