# -*- coding: utf-8 -*-

#完整的运行脚本

from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *

import logging
logger = logging.getLogger('wolfox.fengine.normal.run')    


#1 缩小止损，止损和跟随建议为1600/2400
#2 信号出来后打到55/120均线附近

def prepare_temp_configs(seller,pman=None,dman=None):
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []

    configs.append(config(buyer=fcustom(svama2,fast= 14,slow=  8,ma_standard=  5))) 	#balance=1007,times=485
    configs.append(config(buyer=fcustom(svama2,fast= 32,slow=  8,ma_standard=  5))) 	#balance=1641,times=130
    configs.append(config(buyer=fcustom(svama2,fast= 31,slow=  7,ma_standard=  5))) 	#balance=1777,times=114
    configs.append(config(buyer=fcustom(svama2,fast= 32,slow=  8,ma_standard= 22))) 	#balance=1468,times=100

    configs.append(config(buyer=fcustom(svama2,fast= 32,slow=  8,ma_standard= 67))) 	#balance=1208,times= 47
    configs.append(config(buyer=fcustom(svama2,fast= 31,slow=  7,ma_standard= 67))) 	#balance=1226,times= 45
    
    configs.append(config(buyer=fcustom(svama2,fast= 16,slow=  7,ma_standard=250))) 	#balance=1186,times=  7
    configs.append(config(buyer=fcustom(svama2,fast= 31,slow= 11,ma_standard=250))) 	#balance=1390,times= 11
    configs.append(config(buyer=fcustom(svama2,fast= 31,slow=  7,ma_standard=250))) 	#balance=5314,times=  5
    configs.append(config(buyer=fcustom(svama2,fast= 31,slow=  9,ma_standard=250))) 	#balance=10598,times=  3
    configs.append(config(buyer=fcustom(svama2,fast= 30,slow=  7,ma_standard=250))) 	#balance=17363,times=  2
    
    #svama3
    configs.append(config(buyer=fcustom(svama3,fast=6,mid=42,slow=69,sma=22,ma_standard=227,extend_days=13)))   #mm:(30880, 16830, 545, 4)  [1461,95,650] 20
    configs.append(config(buyer=fcustom(svama3,fast= 28,mid= 93,slow= 76,sma=113,ma_standard=195,extend_days=  5))) 	#balance=2854,times=  9    # [692,54,333] 9
    configs.append(config(buyer=fcustom(svama3,fast= 29,mid= 26,slow=143,sma= 79,ma_standard=175,extend_days= 19))) 	#balance=4901,times= 11      [1227,108,545] 11
    configs.append(config(buyer=fcustom(svama3,fast=  2,mid= 90,slow=175,sma= 11,ma_standard=195,extend_days= 13))) 	#balance=8442,times=  2    ##
    configs.append(config(buyer=fcustom(svama3,fast= 42,mid= 25,slow= 76,sma= 97,ma_standard=195,extend_days=  5))) 	#balance=3049,times= 19
    configs.append(config(buyer=fcustom(svama3,fast= 42,mid= 30,slow= 76,sma= 97,ma_standard=195,extend_days= 35))) 	#balance=5359,times=  5    #

    #svama2
    configs.append(config(buyer=fcustom(svama2,fast= 15,slow=  7,sma= 92,ma_standard=232))) #   #balance=69244,times=  2
    configs.append(config(buyer=fcustom(svama2,fast=  3,slow= 97,sma=115,ma_standard= 83))) 	#balance=6713,times=  9

    #svama2x
    configs.append(config(buyer=fcustom(svama2x,base=55,fast= 27,slow=175,sma= 85,ma_standard= 72,extend_days=1))) 	
    configs.append(config(buyer=fcustom(svama2x,base=55,fast= 14,slow=128,sma=120,ma_standard= 84,extend_days=1)))
    configs.append(config(buyer=fcustom(svama2x,fast=  5,slow= 62,base= 62,sma=107,ma_standard= 30,extend_days=1))) 	#balance=6675,times= 57
    configs.append(config(buyer=fcustom(svama2x,fast=  8,slow= 61,base= 44,sma= 77,ma_standard= 65,extend_days=1))) 	#balance=7726,times= 15
    configs.append(config(buyer=fcustom(svama2x,fast=  1,slow= 61,base=  8,sma= 75,ma_standard= 85,extend_days=1))) 	#balance=15853,times=  4

    configs.append(config(buyer=fcustom(svama2x,fast=  1,slow=  8,base= 82,sma= 33,ma_standard= 20))) 	#balance=3509,times= 11
    
    configs.append(config(buyer=fcustom(svama2c,fast= 15,slow=  7,sma= 92,ma_standard=232,threshold=7500))) #   #balance=69244,times=  2
    configs.append(config(buyer=fcustom(svama2c,fast=  3,slow= 97,sma=115,ma_standard= 83,threshold=7500))) 	#balance=6713,times=  9
    
    configs.append(config(buyer=fcustom(svama2c,fast=  1,slow= 55,sma=115,ma_standard= 45,threshold=7500))) 	#balance=2097,times= 82 #A 1/6 1/3
    configs.append(config(buyer=fcustom(svama2c,fast=  7,slow= 68,sma= 66,ma_standard=207,threshold=7500))) 	#balance=2994,times= 22 #AA 22/22 10/8
    configs.append(config(buyer=fcustom(svama2c,fast=  1,slow= 48,sma= 55,ma_standard= 45,threshold=7500))) 	#balance=4230,times= 25 #A 4/5 2/3
    configs.append(config(buyer=fcustom(svama2c,fast=  1,slow= 53,sma= 59,ma_standard= 45,threshold=7500))) 	#balance=4588,times= 17 #A 2/3 2/2
    configs.append(config(buyer=fcustom(svama2c,fast=  1,slow= 39,sma= 51,ma_standard= 45,threshold=7500))) 	#balance=5292,times= 90 #A 4/6 2/6
    configs.append(config(buyer=fcustom(svama2c,fast=  1,slow= 21,sma= 51,ma_standard= 45,threshold=7500))) 	#balance=6323,times= 98 #A 3/2  2/1
    configs.append(config(buyer=fcustom(svama2c,fast=  1,slow= 14,sma= 51,ma_standard= 41,threshold=7500))) 	#balance=6447,times=158 #A 2/9  1/3
    configs.append(config(buyer=fcustom(svama2c,fast=  1,slow= 63,sma= 83,ma_standard= 97,threshold=7500))) 	#balance=8389,times=  9 # 5/4  2/1
    configs.append(config(buyer=fcustom(svama2c,fast=  1,slow= 55,sma= 51,ma_standard= 45,threshold=7500))) 	#balance=47126,times=  3 #A 2/3 2/3
    #svama3
    configs.append(config(buyer=fcustom(svama3,fast= 23,mid= 75,slow=222,sma= 19,ma_standard=180,extend_days= 25))) 	#balance=4287,times=  7    #
    configs.append(config(buyer=fcustom(svama3,fast= 29,mid= 26,slow=143,sma= 79,ma_standard=175,extend_days= 19))) 	#balance=4901,times= 11      [1227,108,545] 11

    #svama2
    configs.append(config(buyer=fcustom(svama2,fast=  4,slow= 91,sma=122,ma_standard= 80))) 	#balance=6461,times= 13
    configs.append(config(buyer=fcustom(svama2,fast= 27,slow=175,sma= 85,ma_standard= 72))) 	#balance=5523,times= 36
    configs.append(config(buyer=fcustom(svama2,fast=  4,slow=128,sma=120,ma_standard= 80))) 	#balance=4648,times= 12
    configs.append(config(buyer=fcustom(svama2,fast= 14,slow=128,sma=120,ma_standard= 84))) 	#balance=5205,times= 28

    #以下为svama2s
    configs.append(config(buyer=fcustom(vama3,fast= 11,mid= 28,slow= 99,pre_length= 21,ma_standard=160,extend_days= 29))) 	#balance=2760,times= 54

    #vama2
    configs.append(config(buyer=fcustom(vama2,fast= 23,slow=127,pre_length= 36,ma_standard=190))) 	#balance=3913,times= 25
    
    #ma3
    configs.append(config(buyer=fcustom(ma3,fast= 23,mid= 26,slow=150,ma_standard=240,extend_days= 31))) 	#balance=2857,times=1622

    #svama2x
    configs.append(config(buyer=fcustom(svama2x,fast= 18,slow= 62,base= 10,sma= 47,ma_standard= 65,extend_days=1))) 	#balance=3325,times= 21
    configs.append(config(buyer=fcustom(svama2x,fast=  2,slow= 53,base= 58,sma= 75,ma_standard= 50,extend_days=1))) 	#balance=5184,times= 58
    configs.append(config(buyer=fcustom(svama2x,fast=  9,slow= 62,base= 44,sma= 75,ma_standard= 65,extend_days=1))) 	#balance=9509,times= 12
    configs.append(config(buyer=fcustom(svama2x,fast= 44,slow=  7,base=190,sma= 43,ma_standard=225,extend_days=  7))) 	#balance=9140,times= 11     

    #svama2c
    configs.append(config(buyer=fcustom(svama2c,fast=  7,slow=100,sma= 50,ma_standard=111,threshold=7500))) 	#balance=2384,times= 27 #B 15/24 9/17
    configs.append(config(buyer=fcustom(svama2c,fast=  7,slow= 86,sma= 52,ma_standard=117,threshold=6500))) 	#balance=2507,times= 29 #B  15/32   11/22
    configs.append(config(buyer=fcustom(svama2c,fast=  6,slow=161,sma= 83,ma_standard=116,threshold=7500))) 	#balance=2572,times= 45 #B 20/28 9/16
    
    return configs

def prepare_configs_A(seller,pman,dman):    #R>=1000
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []

    return configs

def prepare_configs_B(seller,pman,dman): # 400<=R<1000
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    

    return configs


def prepare_configs(seller,pman,dman):
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    
    #ma3
    configs.append(config(buyer=fcustom(ma3,fast= 23,mid= 26,slow=150,ma_standard=240,extend_days= 31))) 	#balance=2857,times=1622

    return configs

def prepare_order(sdata):
    d_posort('g5',sdata,distance=5)        
    d_posort('g20',sdata,distance=20)    
    d_posort('g120',sdata,distance=120)     
    d_posort('g250',sdata,distance=250)     

def run_body(sdata,dates,begin,end,xbegin):
    
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

    #configs = prepare_configs(seller,pman,dman)
    configs = prepare_temp_configs(seller,pman,dman)
    #configs = prepare_configs_A(seller,pman,dman)
    #configs.extend(prepare_configs_B(seller,pman,dman))
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
    seller = atr_seller_factory(stop_times=600,trace_times=3000) 
    #seller = csc_func

    #configs = prepare_configs(seller,pman,dman)
    configs = prepare_configs_A(seller,pman,dman)
    #configs.extend(prepare_configs_B(seller,pman,dman))
    
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
    configs = prepare_temp_configs(seller)
    
    mm_batch(configs,sdata,dates,xbegin)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    

    save_mm_configs('mm_ev.txt',configs,xbegin,end)
    #save_configs('atr_ev_mm_test.txt',configs,begin,end)

def run_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata.values())
    prepare_order(catalogs)
    dummy_catalogs('catalog',catalogs)
    run_body(sdata,dates,begin,end,xbegin)

def run_merge_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata.values())
    prepare_order(catalogs)    
    dummy_catalogs('catalog',catalogs)
    run_merge_body(sdata,dates,begin,end,xbegin)

def run_mm_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata.values())
    prepare_order(catalogs)    
    dummy_catalogs('catalog',catalogs)
    run_mm_body(sdata,dates,begin,end,xbegin)

def run_last(dates,sdata,idata,catalogs,begin,end,xbegin,lbegin=0):
    prepare_order(sdata.values())
    prepare_order(catalogs)    
    dummy_catalogs('catalog',catalogs)
    from time import time
    tbegin = time()

    pman = None
    dman = None
    myMediator=mediator_factory(trade_strategy=B0S0,pricer = oo_pricer)
    #seller = atr_seller_factory(stop_times=2000,trace_times=3000)
    seller = atr_seller_factory(stop_times=600,trace_times=3000)
    #seller = csc_func
    if lbegin == 0:
        lbegin = end - 5

    #configs_a = prepare_configs_A(seller,pman,dman)
    #dtrades_a = batch_last(configs_a,sdata,dates,xbegin,cmediator=myMediator)
    #save_last('atr_last_a.txt',dtrades_a,xbegin,end,lbegin)


    configs_b = prepare_configs_B(seller,pman,dman)
    dtrades_b = batch_last(configs_b,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_b.txt',dtrades_b,xbegin,end,lbegin)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    


if __name__ == '__main__':
    logging.basicConfig(filename="run_x4c.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    #测试时间段 [19980101,19990101-20010801],[20000101,20010701-20050901],[20040601,20050801-20071031],[20060601,20071031-20090101]
    #总时间段   [20000101,20010701,20090101]    #一个完整的周期+一个下降段
    #分段测试的要求，段mm > 1000-1500或抑制，总段mm > 2000
    
    begin,xbegin,end = 20000101,20010701,20090101
    #begin,xbegin,end = 20000101,20010701,20050901
    #begin,xbegin,end = 19980101,19990701,20010801    
    #begin,xbegin,end = 20040601,20050801,20071031
    #begin,xbegin,end = 20060601,20071031,20090101
    #begin,xbegin,end = 19980101,19990101,20090101
    #begin,xbegin,end,lbegin = 20070101,20080601,20090327,20081101
    #begin,xbegin,end,lbegin = 20060701,20070901,20090327,20081101
    #begin,xbegin,end = 20080701,20090101,20090301
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
    tend = time()
    print u'数据准备耗时: %s' % (tend-tbegin)    
    import psyco
    psyco.full()

    run_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    #run_merge_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    #run_mm_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    #run_last(dates,sdata,idata,catalogs,begin,end,xbegin,lbegin)

    #近期工作 将svama2x/vama2x改造为syntony

    #prepare_order(sdata.values())
    #prepare_order(catalogs)
    #dummy_catalogs('catalog',catalogs)
    #for c in sdata[816].catalog:
    #    print c.name,c.g20
