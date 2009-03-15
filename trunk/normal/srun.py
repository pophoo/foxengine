# -*- coding: utf-8 -*-

#指定股票的测试运行脚本

from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *
from wolfox.fengine.core.d1match import *

import logging
logger = logging.getLogger('wolfox.fengine.normal.run')    

#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s>=3300,s<=6600)

def ext_factory(sbegin,send):
    return lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s>=sbegin,s<=send)

def gtest(stock,fast,slow,dates,ma_standard=120):
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    g60 = stock.g60
    ma_fast = ma(g60,fast)
    ma_slow = ma(g60,slow)
    trend_ma_fast = strend(ma_fast) > 0
    trend_ma_slow = strend(ma_slow) > 0    
    cross_fast_slow = gand(cross(ma_slow,ma_fast)>0,trend_ma_fast,trend_ma_slow)

    ma_standard = ma(t[CLOSE],ma_standard)
    trend_ma_standard = strend(ma_standard) > 0    
 
    ma_120 = ma(stock.g120,5)   #平滑一下
    ma_250 = ma(stock.g250,5)
    trend_ma_120 = strend(ma_120) > 0
    trend_ma_250 = strend(ma_250) > 0

    print stock.code

    return gand(cross_fast_slow,ma_standard,g,trend_ma_120,trend_ma_250,g60>5000,g60<8000)


def func_test(stock,fast,mid,slow,cextractor,ma_standard=500,extend_days=10,pre_length=67,**kwargs):
    ''' vama三叉
    '''
    dates = kwargs['dates'] #打印输出用
    t = stock.transaction
    #g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    svap,v2i = vap_pre(t[VOLUME],t[CLOSE],pre_length)
    ma_svapfast = ma(svap,fast)
    ma_svapmid = ma(svap,mid)    
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapmid = strend(ma_svapmid) > 0    
    trend_ma_svapslow = strend(ma_svapslow) > 0

    #cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    cross_fast_mid = band(cross(ma_svapmid,ma_svapfast)>0,trend_ma_svapfast)
    cross_fast_slow = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast)    
    cross_mid_slow = band(cross(ma_svapslow,ma_svapmid)>0,trend_ma_svapmid)
    sync_fast_2 = sfollow(cross_fast_mid,cross_fast_slow,extend_days)
    sync3 = sfollow(sync_fast_2,cross_mid_slow,extend_days)

    ma_standard = ma(svap,ma_standard)
    trend_ma_standard = strend(ma_standard) > 0    
    vsignal = band(sync3,trend_ma_standard)
    msvap = transform(vsignal,v2i,len(t[VOLUME]))
    
    cs = catalog_signal_cs(stock.c60,cextractor)
    #cs = catalog_signal_cs(stock.c20,cextractor)
    

    #sbuy = gand(g,cs,msvap)
    sbuy = gand(cs,msvap)
    #down_limit = tracelimit((t[OPEN]+t[LOW])/2,t[HIGH],sbuy,stock.atr,600,3000)

    #seller = atr_seller_factory(stop_times=600,trace_times=3000)    
    #ssell = seller(stock,sbuy)

    #sb = make_trade_signal_advanced(sbuy,ssell)      
    #for x in zip(dates,sbuy,down_limit,t[LOW],t[OPEN],t[CLOSE],stock.atr*600/1000,t[OPEN]-stock.atr*600/1000,ssell,sb)[-80:]:
    #    print x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9]

    #sup = up_under(t[HIGH],t[LOW],10,300)    
    #return gand(g,msvap)
    f=file('wtSH600000.csv','w+')
    for x in zip(dates,t[CLOSE],stock.g5,stock.g20,stock.g60,stock.g120,stock.g250):
        print >>f,'%s,%s,%s,%s,%s,%s,%s' % (x[0],x[1],x[2],x[3],x[4],x[5],x[6])

    f.close()
    return sbuy

def func_test_old(stock,fast,slow,base,sma=55,ma_standard=120,extend_days=5,**kwargs):
    ''' svama二叉,extend_days天内再有日线底线叉ma(base)
    '''
    dates = kwargs['dates'] #打印输出用
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    svap,v2i = svap_ma(t[VOLUME],t[CLOSE],sma)
    #print len(svap),len(v2i),len(dates)
    print stock.code
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0

    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    #for s,v,f,sl,c in zip(svap,v2i,ma_svapfast,ma_svapslow,cross_fast_slow):
    #    print '%s,%s,%s,%s,%s' % (dates[v],s,f,sl,c)
    for s,v in zip(svap,v2i):
        print '%s,%s' % (dates[v],s)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))
    print np.sum(msvap),np.sum(cross_fast_slow)
    ma_standard = ma(t[CLOSE],ma_standard)
    trend_ma_standard = strend(ma_standard) > 0

    ma_fast = t[LOW]
    ma_base = ma(t[CLOSE],base)
    trend_base = strend(ma_base) > 0    
    xcross = band(cross(ma_base,ma_fast),trend_base)
    #sf = sfollow(msvap,xcross,extend_days)  #syntony
    sf = syntony(msvap,xcross,extend_days)
    
    #sbuy = gand(g,sf,trend_ma_standard)
    sbuy = msvap
    #print dates[sbuy>0]
    down_limit = tracelimit((t[OPEN]+t[LOW])/2,t[HIGH],sbuy,stock.atr,600,3000)
    
    #for x in zip(dates,sbuy,down_limit,t[LOW],t[OPEN],t[CLOSE],stock.atr*600/1000,t[OPEN]-stock.atr*600/1000):
    #    print x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7]
    return sbuy

def prepare_buyer(dates):
    #return fcustom(func_test,ma_standard=500,slow=50,extend_days=31,fast=30,mid=67,dates=dates)
    #return fcustom(func_test,ma_standard=500,slow=45,extend_days=17,fast=32,mid=79,dates=dates)
    #return fcustom(func_test,fast= 33,mid= 84,slow=345,ma_standard=500,extend_days= 27,dates=dates,cextractor=ext_factory(3300,6600))
    return fcustom(gtest,fast=5,slow=60,dates=dates)

def prepare_order(sdata):
    d_posort('g5',sdata,distance=5)        
    d_posort('g20',sdata,distance=20)    
    d_posort('g120',sdata,distance=120)     
    d_posort('g250',sdata,distance=250)     

def run_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata.values())
    prepare_order(catalogs)
    dummy_catalogs('catalog',catalogs)

    from time import time
    tbegin = time()

    pman = AdvancedATRPositionManager()
    dman = DateManager(begin,end)
    myMediator=mediator_factory(trade_strategy=B1S1,pricer = oo_pricer)
    #seller = atr_seller_factory(stop_times=2000,trace_times=3000)
    #seller = atr_seller_factory(stop_times=1500,trace_times=3000)
    #seller = atr_seller_factory(stop_times=1000,trace_times=3000)
    seller = atr_seller_factory(stop_times=600,trace_times=3000)
    #seller = csc_func
    #seller = fcustom(csc_func,threshold=100)

    buyer = prepare_buyer(dates)   
    name,tradess = calc_trades(buyer,seller,sdata,dates,xbegin,cmediator=myMediator)
    result,strade = ev.evaluate_all(tradess,pman,dman)
    print strade

    #tradess = myMediator(buyer,seller).calc_last(sdata,dates,xbegin)
    #print tradess[0]
    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    


if __name__ == '__main__':
    logging.basicConfig(filename="srun_x4c.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    #测试时间段 [19980101,19990101-20010801],[20000101,20010701-20050901],[20040601,20050801-20071031],[20060601,20071031-20090101]
    #总时间段   [20000101,20010701,20090101]    #一个完整的周期+一个下降段
    #分段测试的要求，段mm > 1000-1500或抑制，总段mm > 2000
    
    begin,xbegin,end = 19980101,20010701,20090101
    #begin,xbegin,end = 20000101,20010701,20090101
    #begin,xbegin,end = 20000101,20010701,20050901
    #begin,xbegin,end = 19980101,19990701,20010801    
    #begin,xbegin,end = 20040601,20050801,20071031
    #begin,xbegin,end = 20060601,20071031,20090101
    #begin,xbegin,end = 19980101,19990101,20090101
    #begin,xbegin,end,lbegin = 20070101,20080601,20090327,20080601
    #begin,xbegin,end,lbegin = 19980101,20010701,20090327,20000101
    from time import time
    tbegin = time()
    
    dates,sdata,idata,catalogs = prepare_all(begin,end,[],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH601988','SH600050'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH601988'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH601398'],[ref_code])        
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SZ000630'],[ref_code])        
    #dates,sdata,idata,catalogs = prepare_all(begin,end,get_codes(),[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,get_codes(source='SZSE'),[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SZ000792'],[ref_code])            
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600888'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SZ000020'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600002'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600433','SH600000'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH000001'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600067'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600766'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SZ002012'],[ref_code])
    #c_posort('c120',catalogs,distance=120)
    
    tend = time()
    print u'数据准备耗时: %s' % (tend-tbegin)    
    import psyco
    psyco.full()

    run_main(dates,sdata,idata,catalogs,begin,end,xbegin)



