# -*- coding: utf-8 -*-

#完整的起始脚本

from wolfox.fengine.extern import *
from wolfox.fengine.internal import *

begin,end = 20010101,20030101
dates = cs.get_ref_dates(begin,end)
sdata = cs.prepare_data(begin,end)
idata = cs.prepare_data(begin,end,'INDEX')

svector = cs.extract_collect(sdata.values(),cs.CLOSE)




