# -*- coding: utf-8 -*-

#完整的演示脚本

from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *

import logging
logger = logging.getLogger('wolfox.fengine.normal.run')    

def prepare_configs(seller,pman,dman):
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []

    #svama3
    #-34745 4 [('extend_days', 13), ('fast', 6), ('ma_standard', 227), ('mid', 34), ('slow', 69), ('sma', 21)]
    configs.append(config(buyer=fcustom(svama3,fast=6,mid=34,slow=69,sma=21,ma_standard=227,extend_days=13)))
    #<<lambda>:slow=69,sma=22,ma_standard=227,extend_days=13,fast=6,mid=42:atr_seller:slow=69,sma=22,ma_standard=227,extend_days=13,fast=6,mid=42:make_trade_signal:B1S1>:mm:(30880, 16830, 545, 4)
    configs.append(config(buyer=fcustom(svama3,fast=6,mid=42,slow=69,sma=22,ma_standard=227,extend_days=13)))
    configs.append(config(buyer=fcustom(svama3,fast=20,mid=64,slow=119)))    #mm=1622,times=4
    configs.append(config(buyer=fcustom(svama3,fast=23,mid=64,slow=120)))   #mm=1611,times=5    #基本同上
    ##<<lambda>:slow=196,sma=47,ma_standard=128,extend_days=6,fast=44,mid=86:atr_seller:slow=196,sma=47,ma_standard=128,extend_days=6,fast=44,mid=86:make_trade_signal:B1S1>:(5143, 9387, 1825, 2)
    configs.append(config(buyer=fcustom(svama3,fast=44,mid=86,slow=196,sma=47,ma_standard=128,extend_days=6)))
    ##<<lambda>:slow=132,sma=36,ma_standard=9,extend_days=8,fast=2,mid=45:atr_seller:slow=132,sma=36,ma_standard=9,extend_days=8,fast=2,mid=45:make_trade_signal:B1S1>:(1374, 123999, 90234, 56)    
    configs.append(config(buyer=fcustom(svama3,fast=2,mid=45,slow=132,sma=36,ma_standard=9,extend_days=8)))

    #以下是svama2
    configs.append(config(buyer=fcustom(svama2,fast= 13,slow=176,sma= 69,ma_standard=242))) 	#balance=9290,times=  5
    configs.append(config(buyer=fcustom(svama2,fast= 22,slow=166,sma=  3,ma_standard=229))) 	#balance=44708,times=  8
    configs.append(config(buyer=fcustom(svama2,fast= 13,slow=238,sma= 78,ma_standard=232))) 	#balance=2253,times=  6
    configs.append(config(buyer=fcustom(svama2,fast= 35,slow=  9,sma= 31,ma_standard=162))) 	#balance=2794,times=  3
    configs.append(config(buyer=fcustom(svama2,fast=  6,slow=171,sma=105,ma_standard=244))) 	#balance=2854,times=  7
    configs.append(config(buyer=fcustom(svama2,fast=  8,slow=114,sma= 44,ma_standard=231))) 	#balance=83106,times=  6
    configs.append(config(buyer=fcustom(svama2,fast=  5,slow=192,sma= 86,ma_standard=240))) 	#balance=2021,times=  5
    configs.append(config(buyer=fcustom(svama2,fast=  5,slow=160,sma=  6,ma_standard=232))) 	#balance=15205,times=  7

    #以下是svama2s
    configs.append(config(buyer=fcustom(svama2s,fast=  5,slow= 97,sma= 63,ma_standard=231,extend_days= 23))) 	#balance=2113,times= 17
    configs.append(config(buyer=fcustom(svama2s,fast= 13,slow= 79,sma= 41,ma_standard=231,extend_days= 23))) 	#balance=2406,times= 20
    configs.append(config(buyer=fcustom(svama2s,fast=  8,slow= 98,sma= 64,ma_standard=232,extend_days= 27))) 	#balance=2557,times= 19
    configs.append(config(buyer=fcustom(svama2s,fast= 13,slow= 95,sma= 65,ma_standard=231,extend_days= 23))) 	#balance=2565,times= 10
    configs.append(config(buyer=fcustom(svama2s,fast=  4,slow=100,sma= 63,ma_standard=254,extend_days= 16))) 	#balance=2766,times=  6
    configs.append(config(buyer=fcustom(svama2s,fast=  4,slow= 58,sma=106,ma_standard=232,extend_days= 17))) 	#balance=4453,times= 23
    configs.append(config(buyer=fcustom(svama2s,fast= 16,slow= 57,sma=127,ma_standard=230,extend_days=  5))) 	#balance=2333,times= 20
    configs.append(config(buyer=fcustom(svama2s,fast= 13,slow= 57,sma=127,ma_standard=245,extend_days=  7))) 	#balance=4522,times=  7
    configs.append(config(buyer=fcustom(svama2s,fast= 31,slow= 77,sma= 25,ma_standard=240,extend_days=  3))) 	#balance=2819,times=  7
    configs.append(config(buyer=fcustom(svama2s,fast= 14,slow= 56,sma= 85,ma_standard=230,extend_days= 25))) 	#balance=2798,times= 13
    
    #以下是vama3
    configs.append(config(buyer=fcustom(vama3,fast=  3,mid= 51,slow= 67,pre_length= 11,ma_standard=225,extend_days= 19))) 	#balance=2032,times= 10
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 59,slow=195,pre_length=  6,ma_standard=180,extend_days= 21))) 	#balance=3782,times=  3
    configs.append(config(buyer=fcustom(vama3,fast= 37,mid= 17,slow=119,pre_length=176,ma_standard= 75,extend_days=  7))) 	#balance=2116,times= 13
    configs.append(config(buyer=fcustom(vama3,fast=  4,mid= 75,slow=237,pre_length= 26,ma_standard=170,extend_days= 11))) 	#balance=2356,times=  3
    configs.append(config(buyer=fcustom(vama3,fast= 40,mid=  9,slow=219,pre_length= 46,ma_standard=170,extend_days= 31))) 	#balance=2929,times=  2
    configs.append(config(buyer=fcustom(vama3,fast= 31,mid= 28,slow=143,pre_length=171,ma_standard=180,extend_days= 21))) 	#balance=3553,times=  4
    configs.append(config(buyer=fcustom(vama3,fast=  7,mid= 55,slow= 14,pre_length= 46,ma_standard= 60,extend_days=  5))) 	#balance=4730,times=  6
    configs.append(config(buyer=fcustom(vama3,fast= 23,mid= 92,slow=143,pre_length=176,ma_standard=180,extend_days=  5))) 	#balance=7901,times=  2
    configs.append(config(buyer=fcustom(vama3,fast=  7,mid= 56,slow= 14,pre_length= 51,ma_standard=180,extend_days=  9))) 	#balance=10663,times=  2
    
    #以下是vama2, 未经过20071001-20090101以及20020101-20090101的筛选
    configs.append(config(buyer=fcustom(vama2,fast= 27,slow=140,pre_length=101,ma_standard=230))) 	#balance=2031,times=  3
    configs.append(config(buyer=fcustom(vama2,fast=  1,slow= 18,pre_length= 31,ma_standard=250))) 	#balance=2050,times=  4
    configs.append(config(buyer=fcustom(vama2,fast=  8,slow= 38,pre_length=  1,ma_standard=245))) 	#balance=2102,times=  8
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow= 16,pre_length= 36,ma_standard=250))) 	#balance=2301,times=  5
    configs.append(config(buyer=fcustom(vama2,fast= 34,slow=202,pre_length= 46,ma_standard=250))) 	#balance=2386,times=  7
    configs.append(config(buyer=fcustom(vama2,fast=  8,slow= 38,pre_length= 31,ma_standard=225))) 	#balance=2620,times= 21
    configs.append(config(buyer=fcustom(vama2,fast= 10,slow=200,pre_length= 46,ma_standard=250))) 	#balance=2784,times=  5
    configs.append(config(buyer=fcustom(vama2,fast=  8,slow= 67,pre_length=  1,ma_standard=245))) 	#balance=2812,times=  6
    configs.append(config(buyer=fcustom(vama2,fast= 34,slow= 38,pre_length= 46,ma_standard=250))) 	#balance=2831,times=  9
    configs.append(config(buyer=fcustom(vama2,fast= 34,slow= 38,pre_length= 46,ma_standard=245))) 	#balance=3028,times= 13
    configs.append(config(buyer=fcustom(vama2,fast= 34,slow=200,pre_length= 46,ma_standard=250))) 	#balance=3074,times=  6
    configs.append(config(buyer=fcustom(vama2,fast=  8,slow= 46,pre_length= 36,ma_standard=225))) 	#balance=3227,times= 14
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow=102,pre_length= 36,ma_standard=245))) 	#balance=3423,times=  3
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow=166,pre_length= 76,ma_standard=245))) 	#balance=3423,times=  3
    configs.append(config(buyer=fcustom(vama2,fast=  9,slow=202,pre_length= 46,ma_standard=250))) 	#balance=3634,times=  5
    configs.append(config(buyer=fcustom(vama2,fast= 33,slow=202,pre_length= 46,ma_standard=250))) 	#balance=3964,times=  4
    configs.append(config(buyer=fcustom(vama2,fast= 34,slow=184,pre_length=126,ma_standard=250))) 	#balance=8877,times=  2
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow= 67,pre_length= 46,ma_standard=245))) 	#balance=21599,times=  7
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow= 58,pre_length=  6,ma_standard=245))) 	#balance=31915,times=  4
    configs.append(config(buyer=fcustom(vama2,fast=  1,slow= 55,pre_length= 46,ma_standard=245))) 	#balance=40533,times=  6
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow= 40,pre_length= 46,ma_standard=250))) 	#balance=54369,times=  5
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow=234,pre_length= 46,ma_standard=250))) 	#balance=89137,times=  4
    configs.append(config(buyer=fcustom(vama2,fast=  4,slow= 42,pre_length= 26,ma_standard=250))) 	#balance=277724,times=  5
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow= 38,pre_length= 36,ma_standard=245))) 	#balance=517134,times=  4
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow=198,pre_length= 46,ma_standard=245))) 	#balance=517134,times=  4
    configs.append(config(buyer=fcustom(vama2,fast=  1,slow=208,pre_length= 46,ma_standard=250))) 	#balance=517134,times=  4
    configs.append(config(buyer=fcustom(vama2,fast= 11,slow=150,pre_length= 81,ma_standard=180))) 	#balance=2094,times= 11
    configs.append(config(buyer=fcustom(vama2,fast= 23,slow=152,pre_length=  1,ma_standard=220))) 	#balance=2339,times= 11
    configs.append(config(buyer=fcustom(vama2,fast=  6,slow= 23,pre_length=151,ma_standard=225))) 	#balance=3340,times= 14
    configs.append(config(buyer=fcustom(vama2,fast=  4,slow=144,pre_length= 71,ma_standard=225))) 	#balance=3792,times=  5
    configs.append(config(buyer=fcustom(vama2,fast=  6,slow=152,pre_length= 71,ma_standard=225))) 	#balance=4537,times=  7
    configs.append(config(buyer=fcustom(vama2,fast= 24,slow=152,pre_length=  1,ma_standard=225))) 	#balance=6746,times=  7
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow= 55,pre_length=151,ma_standard=225))) 	#balance=9026,times= 12
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow= 27,pre_length=151,ma_standard=225))) 	#balance=9395,times= 23
    configs.append(config(buyer=fcustom(vama2,fast=  1,slow= 23,pre_length=151,ma_standard=225))) 	#balance=9613,times= 18
    configs.append(config(buyer=fcustom(vama2,fast= 46,slow=152,pre_length= 71,ma_standard=225))) 	#balance=9830,times=  4
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow= 31,pre_length=151,ma_standard=225))) 	#balance=13337,times= 21
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow=136,pre_length=141,ma_standard=225))) 	#balance=51614,times=  4
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow=150,pre_length=141,ma_standard=225))) 	#balance=51614,times=  4
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow= 23,pre_length=151,ma_standard=225))) 	#balance=71538,times= 17
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow=151,pre_length=151,ma_standard=235))) 	#balance=885500,times=  3    
    return configs

def prepare_order(sdata):
    d_posort('g5',sdata.values(),distance=5)        
    d_posort('g20',sdata.values(),distance=20)    
    d_posort('g120',sdata.values(),distance=120)     
    d_posort('g250',sdata.values(),distance=250)     

def run_body(sdata,dates,begin,end,xbegin):
    
    from time import time
    tbegin = time()

    pman = AdvancedATRPositionManager()
    dman = DateManager(begin,end)
    myMediator=mediator_factory(trade_strategy=B1S1,pricer = oo_pricer)
    seller = atr_seller_factory(stop_times=2000,trace_times=3000)
    #seller = csc_func

    configs = prepare_configs(seller,pman,dman)
    batch(configs,sdata,dates,xbegin,cmediator=myMediator)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    

    save_configs('atr_ev.txt',configs,xbegin,end)

def run_merge_body(sdata,dates,begin,end,xbegin):
    
    from time import time
    tbegin = time()

    pman = AdvancedATRPositionManager()
    dman = DateManager(begin,end)
    myMediator=mediator_factory(trade_strategy=B1S1,pricer = oo_pricer)
    seller = atr_seller_factory(stop_times=2000,trace_times=3000)
    #seller = csc_func

    configs = prepare_configs(seller,pman,dman)
    result,strade = merge(configs,sdata,dates,xbegin,pman,dman,cmediator=myMediator)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    
    save_merged('atr_merged.txt',result,strade,xbegin,end)

def run_mm_body(sdata,dates,begin,end,xbegin):
    from time import time
    tbegin = time()

    #kvs = dict(fast=15,mid=94,slow=209,sma=24,ma_standard=202,extend_days=30)
    #seller = fcustom(atr_seller,**kvs) #atr_seller_factory(stop_times=1500)
    seller = atr_seller_factory()
    myMediator=MM_Mediator
    configs = prepare_configs(seller,None,None)
    
    mm_batch(configs,sdata,dates,xbegin)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    

    save_mm_configs('mm_ev.txt',configs,xbegin,end)
    #save_configs('atr_ev_mm_test.txt',configs,begin,end)

def run_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata)
    run_body(sdata,dates,begin,end,xbegin)

def run_merge_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata)
    run_merge_body(sdata,dates,begin,end,xbegin)


def run_mm_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata)    
    run_mm_body(sdata,dates,begin,end,xbegin)




if __name__ == '__main__':
    logging.basicConfig(filename="run.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    begin,end = 20010701,20090101
    xbegin = 20020101
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
    tend = time()
    print u'数据准备耗时: %s' % (tend-tbegin)    
    import psyco
    psyco.full()

    #run_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    #run_merge(dates,sdata,idata,catalogs,begin,end,xbegin)
    run_mm_main(dates,sdata,idata,catalogs,begin,end,xbegin)
