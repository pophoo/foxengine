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
#print [(s.id,s.code) for s in sdata.values()]
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

c_posort = cdispatch(lambda v,distance=1:percent_sort(percent(v,distance)))
d_posort = dispatch(lambda v,distance=1:percent_sort(percent(v,distance)))

c_posort('test',catalogs,distance=10)
d_posort('gtest',sdata.values(),distance=10)

for c in catalogs:
    pass
    #print c.index


for s in sdata.values():
    try:
        #print s.test
        #print s.code,s.gtest #,s.transaction[CLOSE]
        pass
    except:
        pass

#for cs in ctree:
#    for c in 

ss = 0


for s in sdata.values():
    #print s.code
    t = s.transaction
    g = s.gtest >= 7500
    cma_5 = d1e.ma(t[CLOSE],5)
    cma_22 = d1e.ma(t[CLOSE],12)
    c_5_22 = d1e.cross(cma_22,cma_5) > 0
    c_trend_22 = d1e.strend(cma_22) > 0
    c_trend_5 = d1e.strend(cma_5) > 0
    #signal = gand(c_5_22,c_trend_22,c_trend_5)
    sbuy = gand(g,c_5_22,c_trend_22,c_trend_5)
    #print sbuy.dtype,g.dtype,c_5_22.dtype,c_trend_22.dtype,c_trend_5.dtype
    ssell = d1id.confirmedsellc(sbuy,t[OPEN],t[CLOSE],t[HIGH],t[LOW],75)
    #print s.code,zip(signal,t[CLOSE])
    sbuy = d1.smooth(sbuy,t[VOLUME])
    ssell = d1.smooth(ssell,t[VOLUME])
    ssignal = d1m.make_trade_signal(sbuy,ssell)


print 'signal sum = ',ss
