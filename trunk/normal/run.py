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

    #configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=155,rstart=0,rend=4500))) 	###1786-134-676-34 #5386/830

    return configs

def prepare_configs_A(seller,pman,dman):    #R>=400,winrate>400 or R>=1000,winrate>333
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    
    #候选A winrate>=400且R>=800,times>5 or  R>500且winrate>500
    
    configs.append(config(buyer=fcustom(csvama2,fast= 13,slow=125,rstart= 1000,rend=5000))) 	#2268-188-609-41    #9078/988
    configs.append(config(buyer=fcustom(svama3,fast= 39,mid= 71,slow=490,ma_standard=120,extend_days=  1))) 	#4103-119-571-7
    configs.append(config(buyer=fcustom(svama3,fast= 39,mid= 71,slow=490,ma_standard=500,extend_days=  1))) 	#4421-168-600-5
    configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 80,slow=145,ma_standard= 55,extend_days=  1))) 	#986-70-583-12
    configs.append(config(buyer=fcustom(vama3,fast= 20,mid= 55,slow= 95,ma_standard=500,extend_days=  1))) 	#928-65-500-8
    configs.append(config(buyer=fcustom(vama3,fast= 18,mid= 57,slow=115,ma_standard=500,extend_days=  1))) 	##3771-264-500-12
    configs.append(config(buyer=fcustom(vama3,fast= 20,mid= 56,slow=105,ma_standard=500,extend_days=  1))) 	#3494-325-625-8
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 78,slow=125,ma_standard= 55,extend_days=  1))) 	#920-58-500-14
    configs.append(config(buyer=fcustom(svama3,fast=  7,mid= 91,slow=300,ma_standard=500,extend_days=  1))) 	#555-35-666-3
    configs.append(config(buyer=fcustom(vama3,fast= 17,mid= 46,slow= 85,ma_standard= 55,extend_days=  1))) 	#1025-81-535-28
    configs.append(config(buyer=fcustom(csvama2,fast= 13,slow=125,rstart=  0,rend=1500))) 	##4750-76-800-5
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=140,rstart=5000,rend=6000))) 	##2314-162-571-14
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=155,rstart=0,rend=4500))) 	###1786-134-676-34 #5386/830
    configs.append(config(buyer=fcustom(csvama2,fast=  1,slow=180,rstart=1000,rend=3000))) 	##1884-196-636-11
    configs.append(config(buyer=fcustom(csvama2,fast=184,slow=305,rstart=4000,rend=5500))) 	##2933-132-500-8
    configs.append(config(buyer=fcustom(csvama2,fast= 31,slow=385,rstart=3500,rend=6500))) 	##1279-87-500-30
    configs.append(config(buyer=fcustom(csvama2,fast=128,slow=405,rstart=2500,rend=5500))) 	##1000-79-647-17
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=475,rstart=5000,rend=6000))) 	##1073-44-500-14
    configs.append(config(buyer=fcustom(csvama2,fast= 33,slow=670,rstart=5000,rend=6000))) 	##1863-136-600-5
    configs.append(config(buyer=fcustom(csvama2,fast=790,slow=810,rstart=2000,rend=4500))) 	##74500-298-857-7
    configs.append(config(buyer=fcustom(csvama2,fast= 33,slow=1120,rstart=1000,rend=6000))) ##1480-74-545-11
    configs.append(config(buyer=fcustom(csvama2,fast= 48,slow=385,rstart=2500,rend=4000))) 	##1243-153-500-8
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=680,rstart=3500,rend=6000))) 	##560-42-538-13
    configs.append(config(buyer=fcustom(csvama2,fast= 41,slow=360,rstart=500,rend=3000))) 	##538-35-700-10
    configs.append(config(buyer=fcustom(csvama3,fast= 33,mid=  5,slow= 40,rstart=2000,rend=4500))) 	##5031-473-625-8
    configs.append(config(buyer=fcustom(csvama3,fast= 33,mid=  9,slow= 40,rstart=2500,rend=4500))) 	##3819-317-545-11
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 45,slow= 95,rstart=1500,rend=9000))) 	##2014-135-576-26
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 26,slow=100,rstart=4000,rend=8500))) 	##2560-169-521-23
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 25,slow=410,rstart=5500,rend=9000))) 	##962-76-538-13
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=705,slow=1110,rstart=  0,rend=8500))) 	##11370-307-625-8
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 63,slow=730,rstart=5000,rend=10000))) ##1080-107-545-11
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 92,slow=1110,rstart=8000,rend=9500)))	##1201-166-571-7
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 48,slow=1120,rstart=4500,rend=8500)))	##1862-82-500-10
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 48,slow=1140,rstart=4000,rend=8500))) ##1744-75-615-13
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 57,slow=1270,rstart=4000,rend=8500))) ##2576-152-583-12
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 48,slow=1440,rstart=4000,rend=8500))) ##1000-28-500-10
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid= 54,slow=1770,rstart=5000,rend=8500))) ##983-61-600-10
    configs.append(config(buyer=fcustom(svama3,fast=165,mid=184,slow=1960))) 	##587-47-472-36

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
    configs.append(config(buyer=fcustom(csvama3,fast= 44,mid= 23,slow=250,rstart=7500,rend=8000))) 	#1948-152-500-2 #383/78

    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=705,slow=790,rstart=2500,rend=8500))) 	#4000-192-333-3
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=765,slow=1110,rstart=500,rend=7000))) 	#1000-407-1000-2
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=655,slow=770,rstart=4000,rend=8500))) 	#1000-162-1000-1
    configs.append(config(buyer=fcustom(csvama3,fast=108,mid=176,slow=500,rstart=500,rend=7000))) 	#1307-51-666-3
    configs.append(config(buyer=fcustom(csvama3,fast= 44,mid= 23,slow=250,rstart=7500,rend=8000))) 	#1948-152-500-2
    configs.append(config(buyer=fcustom(csvama3,fast=195,mid=335,slow=1350,rstart=7000,rend=10000)))#3790-235-500-2
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 27,slow=270,rstart=7500,rend=8000))) 	#687-55-500-2
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=215,slow=1050,rstart=2500,rend=9000))) #732-63-285-14
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 85,slow=165,rstart=5000,rend=5500))) 	#1000-1776-1000-1
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 76,slow=410,rstart=3500,rend=8500))) 	#788-71-500-2
    configs.append(config(buyer=fcustom(csvama3,fast= 11,mid= 82,slow=410,rstart=5500,rend=6000))) 	#1000-137-1000-1
    configs.append(config(buyer=fcustom(csvama3,fast=210,mid=300,slow=530,rstart=4500,rend=9500))) 	#636-21-333-3
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid=385,slow=950,rstart=500,rend=8500))) 	#1904-200-333-6
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=350,slow=950,rstart=8500,rend=9500))) 	#4724-104-500-2
    configs.append(config(buyer=fcustom(csvama3,fast=140,mid=430,slow=790,rstart=500,rend=9500))) 	#733-44-250-12
    configs.append(config(buyer=fcustom(csvama3,fast=215,mid=375,slow=485,rstart=2500,rend=9000))) 	#39076-508-500-2

    return configs

def prepare_configs_A2(seller,pman,dman):    #winrate>=400且R>=600,times>5 or  R>500且winrate>500
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    
    #A2 存在RP问题的参数配置
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

    #B R>500且400 < winrate < 500
    configs.append(config(buyer=fcustom(svama2,fast=  9,slow=1160))) 	##756-59-417-249    
    configs.append(config(buyer=fcustom(vama3,fast= 17,mid= 38,slow=125,ma_standard=500,extend_days=  1))) 	#3609-231-400-5
    configs.append(config(buyer=fcustom(svama3,fast=  2,mid= 95,slow=130,ma_standard=120,extend_days=  1))) 	#594-60-444-9
    configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 54,slow= 85,ma_standard= 55,extend_days=  1))) 	#723-47-413-29
    configs.append(config(buyer=fcustom(csvama2,fast=  6,slow= 55,rstart=3000,rend=5000))) 	##1815-138-466-45
    configs.append(config(buyer=fcustom(csvama2,fast= 20,slow= 95,rstart=5000,rend=7500))) 	##1811-125-411-51
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=125,rstart=4500,rend=6500))) 	##1157-103-444-27
    configs.append(config(buyer=fcustom(csvama2,fast=  8,slow=150,rstart=2500,rend=6000))) 	##1535-129-425-47
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=160,rstart=3000,rend=6500))) 	##1094-93-431-51
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=165,rstart=5000,rend=6500))) 	##604-58-461-26
    configs.append(config(buyer=fcustom(csvama2,fast=  4,slow=170,rstart=5000,rend=6500))) 	##739-68-416-24
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=170,rstart=3000,rend=6500))) 	##1131-103-422-45
    configs.append(config(buyer=fcustom(csvama2,fast=  8,slow=175,rstart=5000,rend=8000))) 	##674-56-409-44
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=170,rstart=4000,rend=6500))) 	##1122-101-472-36
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=180,rstart=500,rend=3000))) 	##739-54-400-5
    configs.append(config(buyer=fcustom(csvama2,fast=116,slow=210,rstart=2000,rend=5000))) 	##1456-118-437-16
    configs.append(config(buyer=fcustom(csvama2,fast=112,slow=385,rstart=2500,rend=6000))) 	##882-45-444-27
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=395,rstart=3500,rend=5500))) 	##2064-128-444-18
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=400,rstart=5000,rend=6500))) 	##852-52-458-24
    configs.append(config(buyer=fcustom(csvama2,fast= 37,slow=400,rstart=1000,rend=6000))) 	##857-67-500-36
    configs.append(config(buyer=fcustom(csvama2,fast= 32,slow=480,rstart=5000,rend=6500))) 	##596-31-440-25
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=480,rstart=5000,rend=6000))) 	##850-34-416-12
    configs.append(config(buyer=fcustom(csvama2,fast=128,slow=500,rstart=3500,rend=5000))) 	##790-49-437-16
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=670,rstart=3000,rend=8000))) 	##989-93-454-22
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=670,rstart=3500,rend=6000))) 	##2408-171-416-12
    configs.append(config(buyer=fcustom(csvama2,fast= 26,slow=680,rstart=2000,rend=8000))) 	##931-82-407-27
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=720,rstart=3500,rend=6000))) 	##1000-55-461-13
    configs.append(config(buyer=fcustom(csvama2,fast=690,slow=980,rstart=5000,rend=9000))) 	##2229-165-454-11
    configs.append(config(buyer=fcustom(csvama2,fast=635,slow=1110,rstart=1500,rend=7000))) ##2937-188-400-10
    configs.append(config(buyer=fcustom(csvama2,fast= 26,slow=660,rstart=3000,rend=8000))) 	##867-85-428-28
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid= 30,slow= 50,rstart=4000,rend=5500))) 	##3324-256-428-14
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid= 78,slow=500,rstart=4000,rend=8500))) 	##1292-115-428-14
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid= 48,slow=520,rstart=4000,rend=8500))) 	##1566-83-400-25
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 33,slow=630,rstart=4000,rend=8500))) 	##761-67-482-29
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=325,slow=640,rstart=4000,rend=8500))) 	##704-62-500-6
    configs.append(config(buyer=fcustom(csvama3,fast=150,mid=260,slow=710,rstart=2000,rend=9000))) 	##850-51-444-9
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 57,slow=730,rstart=4000,rend=9000))) 	##1242-123-444-9
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid= 45,slow=740,rstart=4000,rend=9000))) 	##1216-90-428-14
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 48,slow=740,rstart=4000,rend=8500))) 	##2918-216-454-11
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 92,slow=1110,rstart=  0,rend=8500))) 	##1492-100-411-17
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid= 84,slow=1110,rstart=  0,rend=8500))) 	##1500-90-450-20
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 92,slow=1120,rstart=2500,rend=9000))) ##1863-123-416-12
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=345,slow=1030,rstart=  0,rend=9500))) 	##4128-161-400-10
    configs.append(config(buyer=fcustom(svama3,fast=190,mid=245,slow=1790))) 	##851-46-464-28
    configs.append(config(buyer=fcustom(svama3,fast=185,mid=340,slow=1800))) 	##515-34-478-23
    configs.append(config(buyer=fcustom(svama3,fast=165,mid=184,slow=1960))) 	##587-47-472-36
    configs.append(config(buyer=fcustom(svama3,fast=180,mid=340,slow=1800))) 	##571-36-434-23

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
    dman = XDateManager(dates)
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
    dman = XDateManager(dates)
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

    save_mm_configs('mm_ev_b.txt',configs,xbegin,end)
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
    logging.basicConfig(filename="run_x4a.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    #测试时间段 [19980101,19990101-20010801],[20000101,20010701-20050901],[20040601,20050801-20071031],[20060601,20071031-20090101]
    #总时间段   [20000101,20010701,20090101]    #一个完整的周期+一个下降段
    #分段测试的要求，段mm > 1000-1500或抑制，总段mm > 2000
    
    #begin,xbegin,end = 20000101,20010701,20090101
    #begin,xbegin,end = 19980101,20010701,20090101
    #begin,xbegin,end = 20000101,20010701,20050901
    #begin,xbegin,end = 19980101,19990701,20010801    
    #begin,xbegin,end = 20040601,20050801,20071031
    #begin,xbegin,end = 20060601,20071031,20090101
    #begin,xbegin,end = 19980101,19990101,20090101
    begin,xbegin,end,lbegin = 20070101,20080601,20090327,20090201
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

    #run_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    #run_merge_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    run_mm_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    #run_last(dates,sdata,idata,catalogs,begin,end,xbegin,lbegin)

    #近期工作 将svama2x/vama2x改造为syntony

    #prepare_order(sdata.values())
    #prepare_order(catalogs)
    #dummy_catalogs('catalog',catalogs)
    #for c in sdata[816].catalog:
    #    print c.name,c.g20
