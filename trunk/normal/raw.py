# -*- coding: utf-8 -*-

#完整的起始脚本

from wolfox.fengine.extern import *
from wolfox.fengine.internal import *

begin,end = 20010101,20030101
dates = cs.get_ref_dates(begin,end)
sdata = cs.prepare_data(begin,end)
idata = cs.prepare_data(begin,end,'INDEX')


#svector = cs.extract_collect(sdata.values(),cs.CLOSE)

#print dates
#print [ v.transaction for v in sdata.values()]
print [(s.id,s.code) for s in sdata.values()]
##print [(i.id,i.code) for i in idata.values()]
#sh = idata[1] 
#sh_close = cs.extract_collect([sz])[0]
sh_close = cs.extract_collect1(idata[1])
#print sz_close

closes = cs.extract_collect(sdata.values())
volumes = cs.extract_collect(sdata.values(),VOLUME)

#print closes
gi = calc_index(sdata.values())
#print zip(dates,gi,sh_close,sh_close/gi)


ctree = cs.get_catalog_tree(sdata)
catalogs = get_all_catalogs(ctree)

for c in catalogs:
    #print [ (s.id,s.code) for s in c.stocks]
    data = cs.extract_collect(c.stocks)
    c.index = calc_index(c.stocks)    

d2.c_posort('test',catalogs)

for c in catalogs:
    pass
    #print c.index

for s in sdata.values():
    try:
        print s.test
    except:
        pass

#for cs in ctree:
#    for c in 
