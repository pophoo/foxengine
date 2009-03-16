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

    
    return configs

def prepare_configs_A(seller,pman,dman):    #R>=400,winrate>400 or R>=1000,winrate>333
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    
    #候选A winrate>=400且R>=600,times>5 or  R>500且winrate>500
    
    configs.append(config(buyer=fcustom(csvama2,fast= 13,slow=125,rstart= 1000,rend=5000))) 	#2268-188-609-41    #9078/988
    configs.append(config(buyer=fcustom(svama3,fast= 39,mid= 71,slow=490,ma_standard=120,extend_days=  1))) 	#balance=2262,times=  4    #4103-119-571-7
    configs.append(config(buyer=fcustom(svama3,fast= 39,mid= 71,slow=490,ma_standard=500,extend_days=  1))) 	#balance=4129,times=  3    #4421-168-600-5
    configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 80,slow=145,ma_standard= 55,extend_days=  1))) 	#balance=1000,times= 11 #986-70-583-12
    configs.append(config(buyer=fcustom(vama3,fast= 20,mid= 55,slow= 95,ma_standard=500,extend_days=  1))) 	#balance=1140,times=  5 #928-65-500-8
    configs.append(config(buyer=fcustom(vama3,fast= 17,mid= 38,slow=125,ma_standard=500,extend_days=  1))) 	#balance=1254,times=  2 #3609-231-400-5
    configs.append(config(buyer=fcustom(vama3,fast= 21,mid= 56,slow=105,ma_standard=500,extend_days=  1))) 	#balance=1276,times=  3 #1410-213-500-6
    configs.append(config(buyer=fcustom(vama3,fast= 18,mid= 57,slow=115,ma_standard=500,extend_days=  1))) 	#balance=1347,times=  4 #3771-264-500-12
    configs.append(config(buyer=fcustom(vama3,fast= 19,mid= 56,slow=105,ma_standard=500,extend_days=  1))) 	#balance=2314,times=  5 #1315-171-571-7
    configs.append(config(buyer=fcustom(vama3,fast= 20,mid= 56,slow=105,ma_standard=500,extend_days=  1))) 	#balance=2416,times=  7 #3494-325-625-8
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 78,slow=125,ma_standard= 55,extend_days=  1))) 	#balance=3214,times=  9 #920-58-500-14
    configs.append(config(buyer=fcustom(svama3,fast=  2,mid= 95,slow=130,ma_standard=120,extend_days=  1))) 	#balance=1244,times= 10    #594-60-444-9
    configs.append(config(buyer=fcustom(svama3,fast=  7,mid= 91,slow=300,ma_standard=500,extend_days=  1))) 	#balance=4343,times=  2#   #555-35-666-3
    configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 54,slow= 85,ma_standard= 55,extend_days=  1))) 	#balance=1006,times= 14 #723-47-413-29
    configs.append(config(buyer=fcustom(vama3,fast= 17,mid= 46,slow= 85,ma_standard= 55,extend_days=  1))) 	#balance=1204,times= 25 #1025-81-535-28
    
    return configs

def prepare_configs_A1(seller,pman,dman):    #候选A1 winrate>=400且R>=800,times<5
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []

    #候选A1 winrate>=400且R>=800,times<5
    configs.append(config(buyer=fcustom(svama3,fast= 23,mid= 79,slow= 10,ma_standard=120,extend_days=  1))) 	#balance=2488,times=  2#   #1000-277-1000-1
    configs.append(config(buyer=fcustom(svama2s,fast= 48,slow=500,ma_standard= 67,extend_days= 13))) 	#balance=1162,times=  2 #1843-59-500-2
    configs.append(config(buyer=fcustom(svama2s,fast= 26,slow=430,ma_standard= 67,extend_days=  5))) 	#balance=2503,times=  4 #1000-84-1000-1
    configs.append(config(buyer=fcustom(svama2x,fast= 11,slow=  5,base=198,ma_standard=500))) 	#1000-116-1000-1
    configs.append(config(buyer=fcustom(svama2x,fast= 18,slow=  5,base=198,ma_standard= 10))) 	#1800-99-666-3
    configs.append(config(buyer=fcustom(svama2x,fast=  6,slow=  5,base=240,ma_standard=500))) 	#1000-148-1000-4
    configs.append(config(buyer=fcustom(svama2x,fast= 28,slow=  5,base=240,ma_standard= 10))) 	#2328-177-500-4
    configs.append(config(buyer=fcustom(svama2x,fast= 15,slow=  5,base=228,ma_standard=250))) 	#balance=30406,times=  5 #1000-131-1000-2
    configs.append(config(buyer=fcustom(csvama3,fast= 44,mid= 23,slow=250,rstart=7500,rend=8000))) 	#1948-152-500-2 #383/78

    return configs

def prepare_configs_A2(seller,pman,dman):    #winrate>=400且R>=600,times>5 or  R>500且winrate>500
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    
    #存在RP问题的参数配置
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 83,slow= 20,ma_standard=500,extend_days=  5))) 	#balance=1129,times= 23 #1746-124-394-76 ##
    configs.append(config(buyer=fcustom(svama2x,fast=  6,slow=  5,base=240,ma_standard= 10))) 	#balance=6106,times=  5 #2603-139-625-8
    configs.append(config(buyer=fcustom(svama2x,fast= 47,slow=  5,base=168,ma_standard=500))) 	#balance=26391,times=  3 #701-80-400-5
    configs.append(config(buyer=fcustom(vama3,fast= 16,mid= 78,slow= 45,ma_standard=500,extend_days= 13))) 	#2493-182-387-155
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 62,slow= 45,ma_standard=500,extend_days=  1))) 	#853-76-470-17
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 71,slow= 55,ma_standard=500,extend_days= 25))) 	#1172-95-377-172
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 67,slow= 45,ma_standard=500,extend_days= 27))) 	#1724-118-418-332 ##
    configs.append(config(buyer=fcustom(vama3,fast=  9,mid= 68,slow= 45,ma_standard=500,extend_days= 21))) 	#1815-118-431-278
    
    return configs

def prepare_configs_B(seller,pman,dman):    #R>=500,winrate<400
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    #候选C R>800,或R>500且winrate>400
    configs.append(config(buyer=fcustom(vama3,fast= 29,mid= 78,slow= 65,ma_standard=500,extend_days= 29))) 	#1315-100-325-270
    configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 81,slow= 65,ma_standard=500,extend_days= 29))) 	#1259-97-348-264
    configs.append(config(buyer=fcustom(vama3,fast= 31,mid= 91,slow= 65,ma_standard=500,extend_days= 25))) 	#1027-76-365-205
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 59,slow= 50,ma_standard=500,extend_days= 27))) 	#1250-90-361-501
    configs.append(config(buyer=fcustom(vama3,fast= 17,mid= 69,slow= 65,ma_standard=500,extend_days= 31))) 	#1040-78-312-432
    configs.append(config(buyer=fcustom(vama3,fast= 11,mid=  8,slow= 65,ma_standard=500,extend_days= 27))) 	#750-60-346-124
    configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 72,slow= 45,ma_standard=500,extend_days= 25))) 	#1257-88-298-134
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 80,slow= 45,ma_standard=500,extend_days= 29))) 	#2289-158-262-80
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 79,slow= 55,ma_standard=500,extend_days=  1))) 	#7714-270-333-3
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 79,slow= 45,ma_standard=500,extend_days= 17))) 	#928-65-288-90
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 69,slow= 45,ma_standard=500,extend_days= 23))) 	#1089-68-304-115
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 91,slow= 50,ma_standard=500,extend_days= 27))) 	#1000-74-350-248
    configs.append(config(buyer=fcustom(vama3,fast=  4,mid= 78,slow= 60,ma_standard=500,extend_days= 27))) 	#1065-81-325-393
    configs.append(config(buyer=fcustom(vama3,fast= 31,mid= 68,slow= 65,ma_standard=500,extend_days= 29))) 	#949-75-326-315
    configs.append(config(buyer=fcustom(vama3,fast=  8,mid= 78,slow= 45,ma_standard=500,extend_days= 29))) 	#2138-154-369-222
    configs.append(config(buyer=fcustom(vama3,fast= 17,mid= 56,slow= 45,ma_standard=500,extend_days= 13))) 	#1426-97-354-237
    configs.append(config(buyer=fcustom(vama3,fast= 29,mid= 78,slow= 45,ma_standard=500,extend_days= 29))) 	#2109-154-284-95
    configs.append(config(buyer=fcustom(vama3,fast= 17,mid= 55,slow= 50,ma_standard=500,extend_days= 27))) 	#910-61-345-385
    configs.append(config(buyer=fcustom(vama3,fast= 18,mid= 91,slow= 50,ma_standard=500,extend_days= 27))) 	#1200-90-368-160
    configs.append(config(buyer=fcustom(svama3,fast= 17,mid= 95,slow=130,ma_standard= 10,extend_days=  1))) 	#962-76-333-15
    configs.append(config(buyer=fcustom(svama3,fast= 17,mid= 95,slow=130,ma_standard=120,extend_days=  1))) 	#1036-85-357-14
    configs.append(config(buyer=fcustom(svama2,fast= 20,slow=  5,ma_standard=500))) 	#1411-72-285-49
    configs.append(config(buyer=fcustom(svama2c,fast= 32,slow=  5,ma_standard= 22))) 	#1285-72-307-13
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 83,slow= 15,ma_standard=500,extend_days= 13))) 	#1394-99-272-66
    configs.append(config(buyer=fcustom(vama3,fast= 24,mid= 55,slow=105,ma_standard= 55,extend_days=  1))) 	#1333-100-333-15
    configs.append(config(buyer=fcustom(vama3,fast= 33,mid= 84,slow=345,ma_standard=500,extend_days= 27))) 	#936-74-323-241
    configs.append(config(buyer=fcustom(vama3,fast=  1,mid= 78,slow=365,ma_standard=500,extend_days= 29))) 	#1025-80-317-173
    configs.append(config(buyer=fcustom(vama3,fast=  4,mid= 88,slow=425,ma_standard=500,extend_days= 33))) 	#1146-102-303-158
    configs.append(config(buyer=fcustom(vama3,fast= 27,mid= 60,slow=335,ma_standard=500,extend_days= 17))) 	#1012-80-313-217
    configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 68,slow=465,ma_standard=500,extend_days= 21))) 	#800-60-275-156
    configs.append(config(buyer=fcustom(vama3,fast= 16,mid= 78,slow=445,ma_standard=500,extend_days= 21))) 	#932-83-339-115
    configs.append(config(buyer=fcustom(vama3,fast= 33,mid= 72,slow=445,ma_standard=500,extend_days= 17))) 	#1213-91-258-155
    configs.append(config(buyer=fcustom(vama3,fast=  8,mid= 78,slow=445,ma_standard=500,extend_days= 21))) 	#897-79-289-107
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 78,slow=450,ma_standard=500,extend_days= 17))) 	#883-68-284-130
    configs.append(config(buyer=fcustom(vama3,fast=  1,mid= 69,slow=465,ma_standard=500,extend_days= 31))) 	#759-60-278-201
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 78,slow=445,ma_standard=500,extend_days= 29))) 	#1024-85-277-144
    configs.append(config(buyer=fcustom(vama2,fast= 29,slow=  5,ma_standard=250))) 	#954-63-264-34
    configs.append(config(buyer=fcustom(vama2,fast= 35,slow= 20,ma_standard=500))) 	#1064-83-325-172
    configs.append(config(buyer=fcustom(vama2,fast= 35,slow= 15,ma_standard=500))) 	#845-60-285-77
    configs.append(config(buyer=fcustom(vama2x,fast= 25,slow=  5,base=214,ma_standard=120))) 	#1622-86-250-4
    configs.append(config(buyer=fcustom(svama2x,fast= 31,slow= 10,base=170,ma_standard=120))) 	#253-16-428-7
    configs.append(config(buyer=fcustom(csvama2,fast= 37,slow=115,rstart=3000,rend=8000))) 	#1202-95-367-68

    return configs

def prepare_configs_C(seller,pman,dman): # 0<=R<500 且winrate<400  R/avg income/win rate #只做储备
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []

    configs.append(config(buyer=fcustom(ma3,fast= 23,mid= 26,slow=150,ma_standard=240,extend_days= 31))) 	#480/25/296
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

    configs = prepare_temp_configs(seller,pman,dman)
    #configs = prepare_configs_A(seller,pman,dman)
    #configs = prepare_configs_B(seller,pman,dman)
    #configs.extend(prepare_configs_A1(seller,pman,dman))
    #configs.extend(prepare_configs_A2(seller,pman,dman))    
    #configs.extend(prepare_configs_B(seller,pman,dman))
    batch(configs,sdata,dates,xbegin,cmediator=myMediator)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    

    save_configs('atr_ev_n.txt',configs,xbegin,end)

def run_merge_body(sdata,dates,begin,end,xbegin):
    
    from time import time
    tbegin = time()

    pman = AdvancedATRPositionManager()
    dman = DateManager(begin,end)
    myMediator=mediator_factory(trade_strategy=B1S1,pricer = oo_pricer)
    seller = atr_seller_factory(stop_times=600,trace_times=3000) 
    #seller = csc_func

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
    #configs = prepare_configs_A(seller,None,None)
    #configs.extend(prepare_configs_B(seller,None,None))
    
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

    configs_a = prepare_configs_A(seller,pman,dman)
    dtrades_a = batch_last(configs_a,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_a.txt',dtrades_a,xbegin,end,lbegin)

    configs_a1 = prepare_configs_A1(seller,pman,dman)
    dtrades_a1 = batch_last(configs_a1,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_a1.txt',dtrades_a1,xbegin,end,lbegin)

    configs_a2 = prepare_configs_A2(seller,pman,dman)
    dtrades_a2 = batch_last(configs_a2,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_a2.txt',dtrades_a2,xbegin,end,lbegin)

    configs_b = prepare_configs_B(seller,pman,dman)
    dtrades_b = batch_last(configs_b,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_b.txt',dtrades_b,xbegin,end,lbegin)

    #configs_t = prepare_temp_configs(seller,pman,dman)
    #dtrades_t = batch_last(configs_t,sdata,dates,xbegin,cmediator=myMediator)
    #save_last('atr_last_t.txt',dtrades_t,xbegin,end,lbegin)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    


if __name__ == '__main__':
    logging.basicConfig(filename="run_x4f.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    #测试时间段 [19980101,19990101-20010801],[20000101,20010701-20050901],[20040601,20050801-20071031],[20060601,20071031-20090101]
    #总时间段   [20000101,20010701,20090101]    #一个完整的周期+一个下降段
    #分段测试的要求，段mm > 1000-1500或抑制，总段mm > 2000
    
    begin,xbegin,end = 20000101,20010701,20090101
    #begin,xbegin,end = 19980101,20010701,20090101
    #begin,xbegin,end = 20000101,20010701,20050901
    #begin,xbegin,end = 19980101,19990701,20010801    
    #begin,xbegin,end = 20040601,20050801,20071031
    #begin,xbegin,end = 20060601,20071031,20090101
    #begin,xbegin,end = 19980101,19990101,20090101
    #begin,xbegin,end,lbegin = 20070101,20080601,20090327,20081101
    #begin,xbegin,end,lbegin = 20060101,20070901,20090327,20090201
    #begin,xbegin,end = 20080701,20090101,20090301
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
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600766'],[ref_code])
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
