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
    #configs.append(config(buyer=fcustom(ma3,fast=4,mid=45,slow=88)))
    #configs.append(config(buyer=fcustom(ma3,fast=8,mid=45,slow=70)))    #mm=1015,times=265

    #configs.append(config(buyer=fcustom(svama2,fast=53,slow=108)))
    #configs.append(config(buyer=fcustom(svama2,fast=16,slow=61)))
    #configs.append(config(buyer=fcustom(svama2,fast=7,slow=62)))
    #configs.append(config(buyer=fcustom(svama2,fast=14,slow=126)))    
    #configs.append(config(buyer=fcustom(svama2,fast=5,slow=98)))
    #configs.append(config(buyer=fcustom(svama2,fast=14,slow=88)))
    #configs.append(config(buyer=fcustom(svama2,fast=8,slow=71)))
    
    #configs.append(config(buyer=fcustom(svama2s,fast=53,slow=108)))
    #configs.append(config(buyer=fcustom(svama2s,fast=16,slow=61)))
    #configs.append(config(buyer=fcustom(svama2s,fast=7,slow=62)))
    #configs.append(config(buyer=fcustom(svama2s,fast=14,slow=126)))    
    #configs.append(config(buyer=fcustom(svama2s,fast=5,slow=98)))
    #configs.append(config(buyer=fcustom(svama2s,fast=14,slow=88)))
    #configs.append(config(buyer=fcustom(svama2s,fast=8,slow=71)))
    #configs.append(config(buyer=fcustom(svama3,fast=12,mid=55,slow=119)))   
    #configs.append(config(buyer=fcustom(svama3,fast=31,mid=57,slow=30)))
    
    #configs.append(config(buyer=fcustom(vama3,fast=12,mid=59,slow=116)))
    #configs.append(config(buyer=fcustom(vama3,fast=20,mid=64,slow=119)))    
    #configs.append(config(buyer=fcustom(vama3,fast=29,mid=55,slow=100)))    #mm=1966,times=1 
    #configs.append(config(buyer=fcustom(vama3,fast=12,mid=45,slow=100)))    #mm=2030,times=7
    #configs.append(config(buyer=fcustom(vama3,fast=25,mid=53,slow=124)))
    #configs.append(config(buyer=fcustom(vama3,fast=8,mid=43,slow=102)))
    
    #configs.append(config(buyer=fcustom(vama2,fast=2,slow=113)))
    #configs.append(config(buyer=fcustom(vama2,fast=26,slow=123)))
    #configs.append(config(buyer=fcustom(vama2,fast=3,slow=22)))
    #configs.append(config(buyer=fcustom(vama2,fast=3,slow=58)))    
    
    #configs.append(config(buyer=fcustom(svama2,fast=1,slow=3)))
    #configs.append(config(buyer=fcustom(svama2,fast=1,slow=5)))    
    #configs.append(config(buyer=fcustom(svama2,fast=47,slow=94)))    
    #onfigs.append(config(buyer=fcustom(svama2,fast=5,slow=68)))    
    #configs.append(config(buyer=fcustom(svama3,fast=12,mid=42,slow=127)))    #mm=2489,times=5
    #configs.append(config(buyer=fcustom(svama3,fast=20,mid=64,slow=119)))    #mm=1622,times=4
    #configs.append(config(buyer=fcustom(svama3,fast=23,mid=64,slow=120)))   #mm=1611,times=5    #基本同上
    #configs.append(config(buyer=fcustom(svama3,fast=12,mid=59,slow=116)))
    #configs.append(config(buyer=fcustom(svama3,fast=17,mid=57,slow=92)))    
    #configs.append(config(buyer=fcustom(vama3,fast=18,mid=52,slow=22)))    
    
    #svama3:slow=193,sma=129,ma_standard=140,mid=78,fast=35,extend_days=19:atr_seller:slow=193,sma=129,ma_standard=140,mid=78,fast=35,extend_days=19:make_trade_signal:B1S1
    #configs.append(config(buyer=fcustom(svama3,fast=35,mid=78,slow=193,sma=129,ma_standard=140,extend_days=19)))
    #configs.append(config(buyer=fcustom(svama3,fast=35,mid=80,slow=200,sma=120,ma_standard=140,extend_days=20)))
    #configs.append(config(buyer=fcustom(svama3,fast=15,mid=94,slow=209,sma=24,ma_standard=202,extend_days=30)))    
    #configs.append(config(buyer=fcustom(svama3,fast=15,mid=90,slow=210,sma=25,ma_standard=200,extend_days=30)))
    #-34745 4 [('extend_days', 13), ('fast', 6), ('ma_standard', 227), ('mid', 34), ('slow', 69), ('sma', 21)]
    configs.append(config(buyer=fcustom(svama3,fast=6,mid=34,slow=69,sma=21,ma_standard=227,extend_days=13)))
    configs.append(config(buyer=fcustom(svama3,fast=6,mid=35,slow=70,sma=20,ma_standard=220,extend_days=13)))
    #3968 17 [('extend_days', 26), ('fast', 8), ('ma_standard', 48), ('mid', 90), ('slow', 34), ('sma', 20)]
    configs.append(config(buyer=fcustom(svama3,fast=8,mid=90,slow=34,sma=20,ma_standard=48,extend_days=26)))
    configs.append(config(buyer=fcustom(svama3,fast=8,mid=90,slow=35,sma=20,ma_standard=50,extend_days=25)))
    #<<lambda>:slow=209,sma=24,ma_standard=202,extend_days=30,fast=15,mid=94:atr_seller:slow=209,sma=24,ma_standard=202,extend_days=30,fast=15,mid=94:make_trade_signal:B1S1>:mm:(13497, 12175, 902, 3)
    configs.append(config(buyer=fcustom(svama3,fast=15,mid=90,slow=94,sma=209,ma_standard=202,extend_days=30)))
    #<<lambda>:slow=69,sma=22,ma_standard=227,extend_days=13,fast=6,mid=42:atr_seller:slow=69,sma=22,ma_standard=227,extend_days=13,fast=6,mid=42:make_trade_signal:B1S1>:mm:(30880, 16830, 545, 4)
    configs.append(config(buyer=fcustom(svama3,fast=6,mid=42,slow=69,sma=22,ma_standard=227,extend_days=13)))
    #<<lambda>:slow=69,sma=21,ma_standard=227,extend_days=13,fast=6,mid=12:atr_seller:slow=69,sma=21,ma_standard=227,extend_days=13,fast=6,mid=12:make_trade_signal:B1S1>:mm:(5091, 34676, 6811, 15)
    configs.append(config(buyer=fcustom(svama3,fast=6,mid=12,slow=69,sma=21,ma_standard=227,extend_days=13)))
    #<<lambda>:slow=85,sma=53,ma_standard=65,extend_days=5,fast=38,mid=74:atr_seller:slow=85,sma=53,ma_standard=65,extend_days=5,fast=38,mid=74:make_trade_signal:B1S1>:mm:(5241, 99303, 18945, 26)
    configs.append(config(buyer=fcustom(svama3,fast=38,mid=74,slow=85,sma=53,ma_standard=65,extend_days=5)))
    #<<lambda>:slow=34,sma=20,ma_standard=48,extend_days=26,fast=8,mid=90:atr_seller:slow=34,sma=20,ma_standard=48,extend_days=26,fast=8,mid=90:make_trade_signal:B1S1>:mm:(3968, 55501, 13985, 17)
    configs.append(config(buyer=fcustom(svama3,fast=8,mid=90,slow=34,sma=20,ma_standard=48,extend_days=26)))
    #<<lambda>:slow=85,sma=53,ma_standard=65,extend_days=13,fast=38,mid=74:atr_seller:slow=85,sma=53,ma_standard=65,extend_days=13,fast=38,mid=74:make_trade_signal:B1S1>:mm:(2932, 89557, 30537, 28):28:
    configs.append(config(buyer=fcustom(svama3,fast=38,mid=74,slow=85,sma=53,ma_standard=65,extend_days=13)))
    #slow=85,sma=53,ma_standard=35,extend_days=5,fast=46,mid=74:atr_seller:slow=85,sma=53,ma_standard=35,extend_days=5,fast=46,mid=74:make_trade_signal:B1S1>:mm:(2043, 139646, 68327, 43)
    configs.append(config(buyer=fcustom(svama3,fast=46,mid=74,slow=85,sma=53,ma_standard=35,extend_days=5)))
    #<<lambda>:slow=85,sma=53,ma_standard=67,extend_days=5,fast=45,mid=74:atr_seller:slow=85,sma=53,ma_standard=67,extend_days=5,fast=45,mid=74:make_trade_signal:B1S1>:mm:(3084, 118218, 38326, 28)
    configs.append(config(buyer=fcustom(svama3,fast=45,mid=74,slow=85,sma=53,ma_standard=67,extend_days=5)))
    #slow=85,sma=54,ma_standard=64,extend_days=5,fast=44,mid=74:atr_seller:slow=85,sma=54,ma_standard=64,extend_days=5,fast=44,mid=74:make_trade_signal:B1S1>:mm:(3894, 118997, 30557, 33)
    configs.append(config(buyer=fcustom(svama3,fast=44,mid=74,slow=85,sma=54,ma_standard=64,extend_days=5)))
    #slow=199,sma=83,ma_standard=65,extend_days=5,fast=29,mid=44:atr_seller:slow=199,sma=83,ma_standard=65,extend_days=5,fast=29,mid=44:make_trade_signal:B1S1>:mm:(1202, 112546, 93610, 52):52
    configs.append(config(buyer=fcustom(svama3,fast=29,mid=44,slow=199,sma=83,ma_standard=65,extend_days=5)))
    #<<lambda>:slow=85,sma=53,ma_standard=35,extend_days=5,fast=6,mid=74:atr_seller:slow=85,sma=53,ma_standard=35,extend_days=5,fast=6,mid=74:make_trade_signal:B1S1>:mm:(2400, 136831, 56994, 39)
    configs.append(config(buyer=fcustom(svama3,fast=6,mid=74,slow=85,sma=53,ma_standard=35,extend_days=5)))
    #<<lambda>:slow=197,sma=19,ma_standard=65,extend_days=13,fast=14,mid=12:atr_seller:slow=197,sma=19,ma_standard=65,extend_days=13,fast=14,mid=12:make_trade_signal:B1S1>:mm:(1402, 144059, 102687, 62):62
    configs.append(config(buyer=fcustom(svama3,fast=14,mid=12,slow=197,sma=19,ma_standard=65,extend_days=13)))
    #<<lambda>:slow=142,sma=74,ma_standard=66,extend_days=7,fast=37,mid=49:atr_seller:slow=142,sma=74,ma_standard=66,extend_days=7,fast=37,mid=49:make_trade_signal:B1S1>:mm:(2905, 88094, 30315, 31)
    configs.append(config(buyer=fcustom(svama3,fast=37,mid=49,slow=142,sma=74,ma_standard=66,extend_days=7)))
    #slow=197,sma=58,ma_standard=65,extend_days=5,fast=45,mid=18:atr_seller:slow=197,sma=58,ma_standard=65,extend_days=5,fast=45,mid=18:make_trade_signal:B1S1>:mm:(1137, 44707, 39289, 21):21
    configs.append(config(buyer=fcustom(svama3,fast=45,mid=18,slow=197,sma=58,ma_standard=65,extend_days=5)))
    #slow=144,sma=81,ma_standard=68,extend_days=7,fast=1,mid=48:atr_seller:slow=144,sma=81,ma_standard=68,extend_days=7,fast=1,mid=48:make_trade_signal:B1S1>:mm:(2224, 81382, 36578, 26
    configs.append(config(buyer=fcustom(svama3,fast=1,mid=48,slow=144,sma=81,ma_standard=68,extend_days=7)))
    #slow=135,sma=81,ma_standard=19,extend_days=6,fast=31,mid=57:atr_seller:slow=135,sma=81,ma_standard=19,extend_days=6,fast=31,mid=57:make_trade_signal:B1S1>:mm:(1631, 108249, 66358, 44):44:
    configs.append(config(buyer=fcustom(svama3,fast=31,mid=57,slow=135,sma=81,ma_standard=19,extend_days=6)))
    #slow=134,sma=79,ma_standard=17,extend_days=13,fast=29,mid=43:atr_seller:slow=134,sma=79,ma_standard=17,extend_days=13,fast=29,mid=43:make_trade_signal:B1S1>:mm:(1339, 209007, 156009, 97):97
    configs.append(config(buyer=fcustom(svama3,fast=29,mid=43,slow=134,sma=79,ma_standard=17,extend_days=13)))
    #:slow=125,sma=18,ma_standard=65,extend_days=7,fast=17,mid=51:atr_seller:slow=125,sma=18,ma_standard=65,extend_days=7,fast=17,mid=51:make_trade_signal:B1S1>:mm:(1309, 100968, 77129, 51):51
    configs.append(config(buyer=fcustom(svama3,fast=17,mid=51,slow=125,sma=18,ma_standard=65,extend_days=7)))
    #<<lambda>:slow=155,sma=93,ma_standard=38,extend_days=18,fast=12,mid=3:atr_seller:slow=155,sma=93,ma_standard=38,extend_days=18,fast=12,mid=3:make_trade_signal:B1S1>:mm:(1133, 94956, 83773, 48):48:
    configs.append(config(buyer=fcustom(svama3,fast=12,mid=3,slow=155,sma=93,ma_standard=38,extend_days=18)))

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
    
    begin,end = 20010701,20090101
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
