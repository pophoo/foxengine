# -*- coding: utf-8 -*-

#完整的演示脚本

from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *

import logging
logger = logging.getLogger('wolfox.fengine.normal.run')    

def run_body(sdata,dates,begin,end):
    
    from time import time
    tbegin = time()

    pman = AdvancedATRPositionManager()
    dman = DateManager(begin,end)
    myMediator=mediator_factory(trade_strategy=B1S1,pricer = oo_pricer)
    seller = atr_seller_factory(stop_times=1500)
    #seller = csc_func
    #pman = AdvancedPositionManager()

    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    #configs.append(config(buyer=fcustom(vama3,fast=12,mid=45,slow=100)))    #mm=2030,times=7

    #-34745 4 [('extend_days', 13), ('fast', 6), ('ma_standard', 227), ('mid', 34), ('slow', 69), ('sma', 21)]
    configs.append(config(buyer=fcustom(svama3,fast=6,mid=34,slow=69,sma=21,ma_standard=227,extend_days=13)))
    #<<lambda>:slow=69,sma=22,ma_standard=227,extend_days=13,fast=6,mid=42:atr_seller:slow=69,sma=22,ma_standard=227,extend_days=13,fast=6,mid=42:make_trade_signal:B1S1>:mm:(30880, 16830, 545, 4)
    configs.append(config(buyer=fcustom(svama3,fast=6,mid=42,slow=69,sma=22,ma_standard=227,extend_days=13)))

    #<<lambda>:slow=34,sma=20,ma_standard=48,extend_days=26,fast=8,mid=90:atr_seller:slow=34,sma=20,ma_standard=48,extend_days=26,fast=8,mid=90:make_trade_signal:B1S1>:mm:(3968, 55501, 13985, 17)
    configs.append(config(buyer=fcustom(svama3,fast=8,mid=90,slow=34,sma=20,ma_standard=48,extend_days=26)))


    configs.append(config(buyer=fcustom(svama3,fast=12,mid=42,slow=127)))    #mm=2489,times=5
    configs.append(config(buyer=fcustom(svama3,fast=15,mid=94,slow=209,sma=24,ma_standard=202,extend_days=30)))    

    configs.append(config(buyer=fcustom(svama3,fast=20,mid=64,slow=119)))    #mm=1622,times=4
    configs.append(config(buyer=fcustom(svama3,fast=23,mid=64,slow=120)))   #mm=1611,times=5    #基本同上

    #svama3:slow=193,sma=129,ma_standard=140,mid=78,fast=35,extend_days=19:atr_seller:slow=193,sma=129,ma_standard=140,mid=78,fast=35,extend_days=19:make_trade_signal:B1S1
    configs.append(config(buyer=fcustom(svama3,fast=35,mid=78,slow=193,sma=129,ma_standard=140,extend_days=19)))
    configs.append(config(buyer=fcustom(svama3,fast=35,mid=80,slow=200,sma=120,ma_standard=140,extend_days=20)))
    #<<lambda>:slow=85,sma=53,ma_standard=65,extend_days=5,fast=38,mid=74:atr_seller:slow=85,sma=53,ma_standard=65,extend_days=5,fast=38,mid=74:make_trade_signal:B1S1>:mm:(5241, 99303, 18945, 26)
    configs.append(config(buyer=fcustom(svama3,fast=38,mid=74,slow=85,sma=53,ma_standard=65,extend_days=5)))

    #slow=85,sma=54,ma_standard=64,extend_days=5,fast=44,mid=74:atr_seller:slow=85,sma=54,ma_standard=64,extend_days=5,fast=44,mid=74:make_trade_signal:B1S1>:mm:(3894, 118997, 30557, 33)
    configs.append(config(buyer=fcustom(svama3,fast=44,mid=74,slow=85,sma=54,ma_standard=64,extend_days=5)))

    #新的一批
    #<<lambda>:slow=238,sma=90,ma_standard=126,extend_days=10,fast=28,mid=58:atr_seller:slow=238,sma=90,ma_standard=126,extend_days=10,fast=28,mid=58:make_trade_signal:B1S1>:mm:(9462, 17647, 1865, 5)
    configs.append(config(buyer=fcustom(svama3,fast=28,mid=58,slow=238,sma=90,ma_standard=126,extend_days=10)))
    #<<lambda>:slow=31,sma=59,ma_standard=35,extend_days=18,fast=44,mid=91:atr_seller:slow=31,sma=59,ma_standard=35,extend_days=18,fast=44,mid=91:make_trade_signal:B1S1>:mm:(4448, 26197, 5889, 8)
    configs.append(config(buyer=fcustom(svama3,fast=44,mid=91,slow=31,sma=59,ma_standard=35,extend_days=18)))
    #<<lambda>:slow=161,sma=62,ma_standard=126,extend_days=5,fast=34,mid=50:atr_seller:slow=161,sma=62,ma_standard=126,extend_days=5,fast=34,mid=50:make_trade_signal:B1S1>:mm:(3003, 49892, 16610, 11)
    configs.append(config(buyer=fcustom(svama3,fast=34,mid=50,slow=161,sma=62,ma_standard=126,extend_days=5)))
    #<<lambda>:slow=161,sma=59,ma_standard=129,extend_days=8,fast=40,mid=53:atr_seller:slow=161,sma=59,ma_standard=129,extend_days=8,fast=40,mid=53:make_trade_signal:B1S1>:mm:(5332, 13742, 2577, 6)
    configs.append(config(buyer=fcustom(svama3,fast=40,mid=53,slow=161,sma=59,ma_standard=129,extend_days=8)))
    #<<lambda>:slow=238,sma=59,ma_standard=126,extend_days=5,fast=40,mid=58:atr_seller:slow=238,sma=59,ma_standard=126,extend_days=5,fast=40,mid=58:make_trade_signal:B1S1>:mm:(3127, 17142, 5481, 7)
    configs.append(config(buyer=fcustom(svama3,fast=40,mid=58,slow=238,sma=59,ma_standard=126,extend_days=5)))

    #<<lambda>:slow=64,sma=102,ma_standard=228,extend_days=14,fast=45,mid=6:atr_seller:slow=64,sma=102,ma_standard=228,extend_days=14,fast=45,mid=6:make_trade_signal:B1S1>:(22750, 8486, 373, 4)
    configs.append(config(buyer=fcustom(svama3,fast=45,mid=6,slow=64,sma=102,ma_standard=228,extend_days=14)))
    #<<lambda>:slow=196,sma=46,ma_standard=132,extend_days=22,fast=27,mid=70:atr_seller:slow=196,sma=46,ma_standard=132,extend_days=22,fast=27,mid=70:make_trade_signal:B1S1>:(27508, 35568, 1293, 2)#
    configs.append(config(buyer=fcustom(svama3,fast=27,mid=70,slow=196,sma=46,ma_standard=132,extend_days=22)))
    ##<<lambda>:slow=122,sma=102,ma_standard=228,extend_days=32,fast=47,mid=7:atr_seller:slow=122,sma=102,ma_standard=228,extend_days=32,fast=47,mid=7:make_trade_signal:B1S1>:(98558, 7589, 77, 2)
    configs.append(config(buyer=fcustom(svama3,fast=47,mid=7,slow=122,sma=102,ma_standard=228,extend_days=32)))
    ##<<lambda>:slow=196,sma=46,ma_standard=132,extend_days=7,fast=27,mid=70:atr_seller:slow=196,sma=46,ma_standard=132,extend_days=7,fast=27,mid=70:make_trade_signal:B1S1>:(15764, 40624, 2577, 4)
    configs.append(config(buyer=fcustom(svama3,fast=27,mid=7,slow=196,sma=46,ma_standard=132,extend_days=7)))    
    ##<<lambda>:slow=122,sma=28,ma_standard=239,extend_days=29,fast=11,mid=23:atr_seller:slow=122,sma=28,ma_standard=239,extend_days=29,fast=11,mid=23:make_trade_signal:B1S1>:(7321, 37698, 5149, 11)
    configs.append(config(buyer=fcustom(svama3,fast=11,mid=23,slow=122,sma=28,ma_standard=239,extend_days=29)))    
    #<<lambda>:slow=122,sma=100,ma_standard=239,extend_days=21,fast=45,mid=87:atr_seller:slow=122,sma=100,ma_standard=239,extend_days=21,fast=45,mid=87:make_trade_signal:B1S1>:(3283, 16557, 5042, 7)
    configs.append(config(buyer=fcustom(svama3,fast=45,mid=87,slow=122,sma=100,ma_standard=239,extend_days=21)))
    ##<<lambda>:slow=196,sma=47,ma_standard=128,extend_days=6,fast=44,mid=86:atr_seller:slow=196,sma=47,ma_standard=128,extend_days=6,fast=44,mid=86:make_trade_signal:B1S1>:(5143, 9387, 1825, 2)
    configs.append(config(buyer=fcustom(svama3,fast=44,id=86,slow=196,sma=47,ma_standard=128,extend_days=6)))
    ##<<lambda>:slow=196,sma=111,ma_standard=240,extend_days=26,fast=12,mid=22:atr_seller:slow=196,sma=111,ma_standard=240,extend_days=26,fast=12,mid=22:make_trade_signal:B1S1>:(2979, 15747, 5286, 6)
    configs.append(config(buyer=fcustom(svama3,fast=12,mid=22,slow=196,sma=111,ma_standard=240,extend_days=26)))
    ##<<lambda>:slow=124,sma=28,ma_standard=236,extend_days=29,fast=1,mid=23:atr_seller:slow=124,sma=28,ma_standard=236,extend_days=29,fast=1,mid=23:make_trade_signal:B1S1>:(2830, 32933, 11635, 12)
    configs.append(config(buyer=fcustom(svama3,fast=1,mid=23,slow=124,sma=28,ma_standard=236,extend_days=29)))    
    ##<<lambda>:slow=45,sma=101,ma_standard=225,extend_days=19,fast=1,mid=6:atr_seller:slow=45,sma=101,ma_standard=225,extend_days=19,fast=1,mid=6:make_trade_signal:B1S1>:(2550, 39291, 15407, 18)
    configs.append(config(buyer=fcustom(svama3,fast=1,mid=6,slow=45,sma=101,ma_standard=225,extend_days=19)))    
    #<<lambda>:slow=66,sma=100,ma_standard=207,extend_days=19,fast=11,mid=23:atr_seller:slow=66,sma=100,ma_standard=207,extend_days=19,fast=11,mid=23:make_trade_signal:B1S1>:(2459, 27465, 11167, 12)
    configs.append(config(buyer=fcustom(svama3,fast=11,mid=23,slow=66,sma=100,ma_standard=207,extend_days=19)))    
    ##<<lambda>:slow=250,sma=28,ma_standard=83,extend_days=32,fast=47,mid=23:atr_seller:slow=250,sma=28,ma_standard=83,extend_days=32,fast=47,mid=23:make_trade_signal:B1S1>:(1993, 40470, 20304, 13)
    configs.append(config(buyer=fcustom(svama3,fast=47,mid=23,slow=250,sma=28,ma_standard=83,extend_days=32)))    
    #<<lambda>:slow=196,sma=48,ma_standard=111,extend_days=6,fast=27,mid=87:atr_seller:slow=196,sma=48,ma_standard=111,extend_days=6,fast=27,mid=87:make_trade_signal:B1S1>:(2008, 28953, 14418, 11)
    configs.append(config(buyer=fcustom(svama3,fast=27,mid=87,slow=196,sma=48,ma_standard=111,extend_days=6)))    
    ##<<lambda>:slow=16,sma=70,ma_standard=228,extend_days=22,fast=33,mid=6:atr_seller:slow=16,sma=70,ma_standard=228,extend_days=22,fast=33,mid=6:make_trade_signal:B1S1>:(1940, 17272, 8899, 8)
    configs.append(config(buyer=fcustom(svama3,fast=33,mid=6,slow=16,sma=70,ma_standard=228,extend_days=22)))
    ##<<lambda>:slow=125,sma=45,ma_standard=17,extend_days=8,fast=1,mid=54:atr_seller:slow=125,sma=45,ma_standard=17,extend_days=8,fast=1,mid=54:make_trade_signal:B1S1>:(1854, 131575, 70943, 49)
    configs.append(config(buyer=fcustom(svama3,fast=1,mid=54,slow=125,sma=45,ma_standard=17,extend_days=8)))    
    ##<<lambda>:slow=132,sma=47,ma_standard=20,extend_days=6,fast=28,mid=46:atr_seller:slow=132,sma=47,ma_standard=20,extend_days=6,fast=28,mid=46:make_trade_signal:B1S1>:(1642, 148830, 90637, 61)
    configs.append(config(buyer=fcustom(svama3,fast=28,mid=46,slow=132,sma=47,ma_standard=20,extend_days=6)))    
    #<<lambda>:slow=101,sma=37,ma_standard=55,extend_days=5,fast=24,mid=55:atr_seller:slow=101,sma=37,ma_standard=55,extend_days=5,fast=24,mid=55:make_trade_signal:B1S1>:(1562, 115000, 73590, 45)
    configs.append(config(buyer=fcustom(svama3,fast=24,mid=55,slow=101,sma=37,ma_standard=55,extend_days=5)))    
    ##<<lambda>:slow=68,sma=92,ma_standard=228,extend_days=21,fast=1,mid=7:atr_seller:slow=68,sma=92,ma_standard=228,extend_days=21,fast=1,mid=7:make_trade_signal:B1S1>:(1516, 50833, 33519, 25)
    configs.append(config(buyer=fcustom(svama3,fast=1,mid=7,slow=68,sma=92,ma_standard=228,extend_days=21)))    
    #<<lambda>:slow=61,sma=109,ma_standard=145,extend_days=21,fast=45,mid=6:atr_seller:slow=61,sma=109,ma_standard=145,extend_days=21,fast=45,mid=6:make_trade_signal:B1S1>:(1512, 32844, 21719, 16)
    configs.append(config(buyer=fcustom(svama3,fast=45,mid=6,slow=61,sma=109,ma_standard=145,extend_days=21)))    
    ##<<lambda>:slow=132,sma=36,ma_standard=9,extend_days=8,fast=2,mid=45:atr_seller:slow=132,sma=36,ma_standard=9,extend_days=8,fast=2,mid=45:make_trade_signal:B1S1>:(1374, 123999, 90234, 56)    
    configs.append(config(buyer=fcustom(svama3,fast=2,mid=45,slow=132,sma=36,ma_standard=9,extend_days=8)))

    #configs = [config1,config2,config3]
    #configs = [config3]
    #configs = [config1,config2]
    batch(configs,sdata,dates,begin,cmediator=myMediator)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    

    save_configs('atr_ev_svama3.txt',configs,begin,end)

def run_main(dates,sdata,idata,catalogs,begin,end):
    d_posort('g5',sdata.values(),distance=5)        
    d_posort('g20',sdata.values(),distance=20)    
    d_posort('g120',sdata.values(),distance=120)     
    d_posort('g250',sdata.values(),distance=250)     
    run_body(sdata,dates,begin,end)

def run_mm_main(dates,sdata,idata,catalogs,begin,end):
    d_posort('g5',sdata.values(),distance=5)        
    d_posort('g20',sdata.values(),distance=20)    
    d_posort('g120',sdata.values(),distance=120)     
    d_posort('g250',sdata.values(),distance=250)     
    run_mm_body(sdata,dates,begin,end)

def run_mm_body(sdata,dates,begin,end):
    from time import time
    tbegin = time()

    kvs = dict(fast=15,mid=94,slow=209,sma=24,ma_standard=202,extend_days=30)
    seller = fcustom(atr_seller,**kvs) #atr_seller_factory(stop_times=1500)

    myMediator=MM_Mediator(fcustom(svama3,**kvs),seller)
    trades = myMediator.calc_matched(sdata,dates,begin=tbegin)
    ev = normal_evaluate(trades,**kvs)  
    mm = rate_mfe_mae(sdata)
    logger.debug('%s:mm:%s:%s:%s',myMediator.name(),mm,ev.count,unicode(ev))
    
    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    

    #save_configs('atr_ev_mm_test.txt',configs,begin,end)


if __name__ == '__main__':
    logging.basicConfig(filename="run.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    begin,end = 20010701,20060101
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

    run_main(dates,sdata,idata,catalogs,begin,end)
    #run_mm_main(dates,sdata,idata,catalogs,begin,end)
