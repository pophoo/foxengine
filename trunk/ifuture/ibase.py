# -*- coding: utf-8 -*-

IDATE,ITIME,IOPEN,ICLOSE,IHIGH,ILOW,IVOPEN,IVCLOSE = 0,1,2,3,4,5,6,7

LONG,SHORT,EMPTY = -1,1,0   #多仓出钱,淡仓收钱

XBUY,XSELL = 1,-1   #买入，卖出信号

XOPEN,XCLOSE = -1,1 #开仓,平仓

XBASE = 100 #用于一般化的除数基数

TAX = 10    #tax为0.8个点,设为1

import numpy as np

from wolfox.fengine.core.base import BaseObject;
from wolfox.fengine.core.d1 import *;
from wolfox.fengine.core.d1ex import *;
from wolfox.fengine.core.d1indicator import *;
from wolfox.fengine.core.utils import *;
