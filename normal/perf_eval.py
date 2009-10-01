
from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *
from wolfox.fengine.core.d1match import *
from wolfox.fengine.core.d1idiom import atr_xseller_factory
from wolfox.fengine.core.d1indicator import cmacd
from wolfox.foxit.base.tutils import linelog
from time import time

import logging
logging.basicConfig(filename="xx4c.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
#begin,xbegin,end = 19980101,20010701,20091231
#begin,xbegin,end = 20000101,20010701,20090101
##begin,xbegin,end = 20000101,20010701,20091231
#begin,xbegin,end = 20050101,20060701,20091231
#begin,xbegin,end = 20070101,20080601,20091231
#begin,xbegin,end = 20060101,20080601,20091231
begin,xbegin,end = 20060101,20090201,20091201
#begin,xbegin,end = 20000101,20010701,20090101
#begin,xbegin,end = 19970101,19980101,20010701

tbegin = time()
    
#dates,sdata,idata,catalogs = prepare_all(begin,end,[],[ref_code])
dates,sdata,idata,catalogs = prepare_all(begin,end,[],[])
#sdata.update(idata)
import psyco
psyco.full()

import wolfox.fengine.normal.sfuncs as s
import wolfox.fengine.normal.hfuncs as h


def body():
    for stock in sdata.values():
        stock.m = h.prepare_hour(stock,20060101,20090932)

import cProfile
cProfile.run('body()')
