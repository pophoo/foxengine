# -*- coding: utf-8 -*-

#完整的运行脚本
#采用NMediator,结果发现成功率显然小了(次日上涨的看来挺多，导致止损比预计上移),看来需要加大atr系数 ==>1200比较贴近之前的结果
#不过有个特点，大部分情形，选出交易数越多的方法，稳定性越好

from wolfox.fengine.core.d1 import subd

from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *
import wolfox.fengine.normal.funcs as f
import wolfox.fengine.normal.sfuncs as s

import logging
logger = logging.getLogger('wolfox.fengine.normal.run')    


#1 缩小止损，止损和跟随建议为1600/2400
#2 信号出来后打到55/120均线附近


def prepare_temp_configs(seller,pman=None,dman=None):
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []

    configs.append(config(buyer=fcustom(svama3,fast=190,mid=350,slow=1790))) 	#691-65-650-20      ##1095-103-650-20  #691-65-650-20 #从seller2000转入,但与上一参数类似
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=165,rstart=5000,rend=6500))) 	#2490-132-555-27    #与上一参数类似

    configs.append(config(buyer=fcustom(csvama3,fast= 33,mid=  9,slow= 40,rstart=2500,rend=4500))) 	#2291-424-833-6
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=705,slow=1110,rstart=  0,rend=8500))) 	#2231-179-700-10
    configs.append(config(buyer=fcustom(csvama2,fast=635,slow=1110,rstart=1500,rend=7000))) #3148-170-600-10
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=125,rstart=4500,rend=6500))) 	#1241-77-500-34
    configs.append(config(buyer=fcustom(csvama3,fast=150,mid=260,slow=710,rstart=2000,rend=9000))) 	#1658-68-500-8
    configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 80,slow=145,ma_standard= 55,extend_days=  1))) 	#1302-99-545-11
    configs.append(config(buyer=fcustom(vama3,fast= 18,mid= 57,slow=115,ma_standard=500,extend_days=  1))) 	#4238-267-500-12
    configs.append(config(buyer=fcustom(csvama2,fast=  1,slow=180,rstart=1000,rend=3000))) 	#1378-113-500-10    
    configs.append(config(buyer=fcustom(csvama2,fast=790,slow=810,rstart=2000,rend=4500))) 	#92450-377-666-3
    configs.append(config(buyer=fcustom(csvama3,fast= 33,mid=  5,slow= 40,rstart=2000,rend=4500))) 	#5185-363-500-8
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 45,slow= 95,rstart=1500,rend=9000))) 	#2517-146-516-31
    configs.append(config(buyer=fcustom(csvama2,fast= 39,slow=1300,rstart=500,rend=9000))) 	#727-40-476-21
    configs.append(config(buyer=fcustom(svama3,fast=116,mid=350,slow=2000))) 	#1283-104-518-27
    configs.append(config(buyer=fcustom(svama3,fast=116,mid=420,slow=1790))) 	#1150-84-538-39


    configs.append(config(buyer=fcustom(svama3,fast= 39,mid= 71,slow=490,ma_standard=120,extend_days=  1))) #6046-205-500-8 #5522-243-714-7    
    configs.append(config(buyer=fcustom(vama3,fast= 17,mid= 46,slow= 85,ma_standard= 55,extend_days=  1))) 	#1107-62-500-28     #853-76-535-28
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=155,rstart=0,rend=4500))) 	#1597-115-628-35    #@1671-127-657-35   #限底之后不够稳定
    configs.append(config(buyer=fcustom(csvama2,fast= 31,slow=385,rstart=3500,rend=6500))) 	#1037-82-516-31     #1174-74-451-31
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 26,slow=100,rstart=4000,rend=8500))) 	#2615-170-521-23    #2617-178-565-23
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 92,slow=1120,rstart=2500,rend=9000))) #2058-140-500-12   #1455-115-416-12
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=140,rstart=5000,rend=6000))) 	#2150-129-400-15    ##1975-158-600-15
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 25,slow=410,rstart=5500,rend=9000))) 	#691-47-461-13      #891-74-538-13
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid= 30,slow= 50,rstart=4000,rend=5500))) 	#4071-285-461-13    ##4054-300-538-13
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid= 45,slow=740,rstart=4000,rend=9000))) 	#959-71-357-14      ##1761-148-500-14
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 48,slow=740,rstart=4000,rend=8500))) 	#2604-211-454-11    ##3756-293-545-11
    configs.append(config(buyer=fcustom(svama3,fast= 22,mid=350,slow=1990))) 	#                   #827-67-506-83
    configs.append(config(buyer=fcustom(csvama2,fast= 33,slow=670,rstart=5000,rend=6000))) 	#1529-104-500-6     #1529-104-500-6
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 92,slow=1110,rstart=8000,rend=9500)))	#1178-165-571-7     #1282-168-571-7
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 57,slow=1270,rstart=4000,rend=8500))) #2314-125-500-12    #2540-155-600-12
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid= 84,slow=1110,rstart=  0,rend=8500))) 	#1792-95-500-20    #1296-83-450-20
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=460,slow=790,rstart=1000,rend=9500))) 	#7132-378-666-6 #13607-381-666-6
    configs.append(config(buyer=fcustom(csvama2,fast= 13,slow=125,rstart= 1000,rend=5000))) 	#975-80-418-43  #1292-115-500-42
    configs.append(config(buyer=fcustom(svama3,fast= 39,mid= 71,slow=490,ma_standard=500,extend_days=  1))) #4243-157-400-5 #3772-166-600-5
    configs.append(config(buyer=fcustom(csvama2,fast=184,slow=305,rstart=4000,rend=5500))) 	#-108   ##2716-144-666-9
    configs.append(config(buyer=fcustom(csvama2,fast=128,slow=405,rstart=2500,rend=5500))) 	#208-14-473-19      ##1558-106-684-19   #对除权不稳定，解决这个问题后再处理
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=475,rstart=5000,rend=6000))) 	#340-17-400-15      #1000-48-533-15
    configs.append(config(buyer=fcustom(csvama2,fast= 48,slow=385,rstart=2500,rend=4000))) 	#1039-109-400-10    #1504-179-500-10
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 63,slow=730,rstart=5000,rend=10000))) #168-126-545-11     #1107-113-545-11
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=215,slow=1050,rstart=2500,rend=9000))) #750-69-357-14  #897-88-500-14
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=720,rstart=3500,rend=6000))) 	#345-19-307-13      ##1256-98-538-13
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=325,slow=640,rstart=4000,rend=8500))) 	#729-62-500-6       ##1901-289-833-6
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 57,slow=730,rstart=4000,rend=9000))) 	#1521-108-333-9     ##2056-220-555-9
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=345,slow=1030,rstart=  0,rend=9500))) 	#2648-143-300-10    ##2981-164-500-10
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=670,rstart=5000,rend=6000))) 	#               #2000-72-500-8
    configs.append(config(buyer=fcustom(csvama2,fast= 57,slow=720,rstart=2000,rend=4500))) 	#               #905-124-714-7
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid= 78,slow=500,rstart=4000,rend=8500))) 	#1564-133-500-14   #1287-139-571-14
    
    return configs

def prepare_configs_A1200(seller,pman,dman):    
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    
    #候选A_1200 winrate>=500且R>=800,times>5 如果1200和2000都满足，优先为1200
    #暂时停止<550,以及次数小于15的方法

    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=170,rstart=4000,rend=6500))) 	#1430-93-558-34
    #configs.append(config(buyer=fcustom(svama3,fast=190,mid=350,slow=1790))) 	#691-65-650-20      ##1095-103-650-20  #691-65-650-20 #从seller2000转入,但与上一参数类似
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=170,rstart=3000,rend=6500))) 	#1646-107-550-40
    #configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=165,rstart=5000,rend=6500))) 	#2490-132-555-27    #与上一参数类似

    #configs.append(config(buyer=fcustom(csvama3,fast= 33,mid=  9,slow= 40,rstart=2500,rend=4500))) 	#2291-424-833-6
    #configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=705,slow=1110,rstart=  0,rend=8500))) 	#2231-179-700-10
    #configs.append(config(buyer=fcustom(csvama2,fast=635,slow=1110,rstart=1500,rend=7000))) #3148-170-600-10
    #configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=125,rstart=4500,rend=6500))) 	#1241-77-500-34
    #configs.append(config(buyer=fcustom(csvama3,fast=150,mid=260,slow=710,rstart=2000,rend=9000))) 	#1658-68-500-8
    #configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 80,slow=145,ma_standard= 55,extend_days=  1))) 	#1302-99-545-11
    #configs.append(config(buyer=fcustom(vama3,fast= 18,mid= 57,slow=115,ma_standard=500,extend_days=  1))) 	#4238-267-500-12
    #configs.append(config(buyer=fcustom(csvama2,fast=  1,slow=180,rstart=1000,rend=3000))) 	#1378-113-500-10    
    #configs.append(config(buyer=fcustom(csvama2,fast=790,slow=810,rstart=2000,rend=4500))) 	#92450-377-666-3
    #configs.append(config(buyer=fcustom(csvama3,fast= 33,mid=  5,slow= 40,rstart=2000,rend=4500))) 	#5185-363-500-8
    #configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 45,slow= 95,rstart=1500,rend=9000))) 	#2517-146-516-31
    #configs.append(config(buyer=fcustom(csvama2,fast= 39,slow=1300,rstart=500,rend=9000))) 	#727-40-476-21
    #configs.append(config(buyer=fcustom(svama3,fast=116,mid=350,slow=2000))) 	#1283-104-518-27
    #configs.append(config(buyer=fcustom(svama3,fast=116,mid=420,slow=1790))) 	#1150-84-538-39

    return configs

def prepare_configs_A2000(seller,pman,dman):    #R>=400,winrate>400 or R>=1000,winrate>333
    ''' 目前逐渐与A1200合并
    '''
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    
    #候选A_2000 winrate>=500且R>=800,times>5 
    #暂时停止<600,以及次数小于15的方法
    #configs.append(config(buyer=fcustom(svama3,fast=190,mid=350,slow=1790))) 	#691-65-650-20      ##1095-103-650-20 
    
    return configs

def prepare_configs_A0(seller,pman,dman):    
    ''' 手工巡游成果
    '''
    #暂时停止<600,以及次数小于15的方法,但保留超过150的
    
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []

    configs.append(config(buyer=s.ma4))     #@1609-600-35    #3X10  #对初始条件太敏感
    #configs.append(config(buyer=s.wvad))    #1554-520-25    #
    configs.append(config(buyer=s.xma60))   #@5239-621-37    #
    #configs.append(config(buyer=s.pmacd))   #1179-500-52    #
    configs.append(config(buyer=fcustom(s.tsvama2,fast=20,slow=100)))   #3724-566-157
    #configs.append(config(buyer=s.nhigh))     #1527-500-76
    #configs.append(config(buyer=s.gx60))    #1305-516-31

    #configs.append(config(buyer=s.vmacd_ma4))   #2521-473-57
    #configs.append(config(buyer=s.gx250))   #@12000-764-17 #限底之后不稳定
    configs.append(config(buyer=s.spring))  #@4935-606-132

    configs.append(config(buyer=fcustom(s.cma2,fast=5,slow=13,gfrom=7000,gto=8500))) #@3603-617-149   #g5-20-60差别越大越好
    configs.append(config(buyer=fcustom(s.cma2,fast=5,slow=20,gfrom=4000,gto=8000))) #@4671-763-38    #g5-20-60差别越大越好
    configs.append(config(buyer=s.xgcs))   #3836-234-600-65
    configs.append(config(buyer=s.xgcs0))   #@4013-617-81   #对初始条件敏感
    configs.append(config(buyer=s.mgcs))   #3577-545-229

    #埋伏,因为xgcs/mgcs系列的加入，暂时忽略埋伏部分
    #configs.append(config(buyer=s.gcs))   #1880-422-206

    #舍弃
    #configs.append(config(buyer=s.temv))    #4210-428-14   
    #configs.append(config(buyer=fcustom(s.tsvama2,fast=12,slow=170)))   #1581-427-117

    return configs

def prepare_configs_A1(seller,pman,dman):   
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []

    #候选A1 winrate>=500且R>=800,times<5    #atr=1200
    #暂时停止<600,以及次数小于15的方法


    return configs

def prepare_configs_A2(seller,pman,dman):    
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    
    #暂时停止<600,以及次数小于15的方法
    #A2 存在RP问题的参数配置    atr=1200
    
    return configs

def prepare_order(sdata):   #g60/c60在prepare_catalogs中计算
    d_posort('g5',sdata,distance=5)
    d_posort('g20',sdata,distance=20)    
    d_posort('g120',sdata,distance=120)     
    d_posort('g60',sdata,distance=60)    
    d_posort('g250',sdata,distance=250)     

csilver = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=6600)
def prepare_common(sdata,ref):
    for s in sdata:
        #print s.code
        s.ref = ref
        c = s.transaction[CLOSE]
        v = s.transaction[VOLUME]
        s.ma10 = ma(c,10)
        s.ma20 = ma(c,20)
        s.ma60 = ma(c,60)
        s.ma120 = ma(c,120)
        s.t120 = strend(s.ma120) > 0
        s.t60 = strend(s.ma60) > 0
        s.t20 = strend(s.ma20) > 0
        s.above = gand(s.ma10>=s.ma20,s.ma20>=s.ma60,s.ma60>=s.ma120)
        #将golden和above分开
        s.golden = gand(s.g20 >= s.g60+1000,s.g60 >= s.g120+1000,s.g20>=3000,s.g20<=8000)
        s.thumb = gand(s.g20 >= s.g60,s.g60 >= s.g120,s.g120 >= s.g250,s.g20>=3000,s.g20<=8000)
        s.svap_ma_67 = svap_ma(v,c,67)
        s.vap_ma_67 = vap_pre(v,c,67)
        s.ks = subd(c) * BASE / rollx(c)
        try:    #计算
            s.silver = catalog_signal_cs(s.c60,csilver)
        except:
            s.silver = cached_zeros(len(c))

def run_body(sdata,dates,begin,end,xbegin):
    from time import time
    tbegin = time()

    pman = AdvancedATRPositionManager()
    dman = DateManager(begin,end)
    myMediator=nmediator_factory(trade_strategy=B1S1,pricer = oo_pricer)
    seller1200 = atr_seller_factory(stop_times=1200,trace_times=3000)
    seller2000 = atr_seller_factory(stop_times=2000,trace_times=3000)    
    #seller = csc_func
    #seller = fcustom(csc_func,threshold=100)
    
    configs = prepare_temp_configs(seller1200,pman,dman)
    #configs = prepare_temp_configs(seller2000,pman,dman)
    #configs = prepare_configs_A2000(seller2000,pman,dman)
    #configs.extend(prepare_configs_A2000(seller2000,pman,dman))
    #configs = prepare_configs_A1200(seller1200,pman,dman)
    #configs.extend(prepare_configs_A0(seller1200,pman,dman))    
    #configs.extend(prepare_configs_A1(seller1200,pman,dman))
    #configs.extend(prepare_configs_A2(seller1200,pman,dman))    
    
    #seller3600 = atr_seller_factory(stop_times=600,trace_times=2000)
    #configs = prepare_configs_A1200(seller3600,pman,dman)
    #configs.extend(prepare_configs_A0(seller3600,pman,dman))    

    batch(configs,sdata,dates,xbegin,cmediator=myMediator)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    

    #save_configs('atr_ev_nm_1200.txt',configs,xbegin,end)
    save_configs('atr_ev_vc.txt',configs,xbegin,end)    

def run_merge_body(sdata,dates,begin,end,xbegin):
    
    from time import time
    tbegin = time()

    pman = AdvancedATRPositionManager()
    dman = DateManager(begin,end)
    myMediator=mediator_factory(trade_strategy=B1S1,pricer = oo_pricer)
    seller1200 = atr_seller_factory(stop_times=1200,trace_times=3000) 
    #seller = csc_func

    configs1200 = prepare_configs_A1200(seller1200,pman,dman)
    configs1200.extend(prepare_configs_A1(seller1200,pman,dman))
    configs1200.extend(prepare_configs_A2(seller1200,pman,dman))
    
    result1200,strade1200 = merge(configs1200,sdata,dates,xbegin,pman,dman,cmediator=myMediator)

    save_merged('atr_merged_1200.txt',result1200,strade1200,xbegin,end)

    seller2000 = atr_seller_factory(stop_times=2000,trace_times=3000) 
    configs2000 = prepare_configs_A2000(seller2000,pman,dman)
    result2000,strade2000 = merge(configs2000,sdata,dates,xbegin,pman,dman,cmediator=myMediator)
    save_merged('atr_merged_2000.txt',result2000,strade2000,xbegin,end)
    
    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    

def run_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata.values())
    prepare_order(idata.values())
    prepare_order(catalogs)
    prepare_common(sdata.values(),idata[ref_id])   #准备ma10/20/60/120,golden,silver,vap_pre,svap_ma
    prepare_common(idata.values(),idata[ref_id])   #准备ma10/20/60/120,golden,silver,vap_pre,svap_ma
    dummy_catalogs('catalog',catalogs)
    run_body(sdata,dates,begin,end,xbegin)

def run_merge_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata.values())
    prepare_order(idata.values())    
    prepare_order(catalogs)    
    prepare_common(sdata.values(),idata[ref_id])   #准备ma10/20/60/120,golden,silver,vap_pre,svap_ma
    prepare_common(idata.values(),idata[ref_id])   #准备ma10/20/60/120,golden,silver,vap_pre,svap_ma    
    dummy_catalogs('catalog',catalogs)
    run_merge_body(sdata,dates,begin,end,xbegin)

def run_last(dates,sdata,idata,catalogs,begin,end,xbegin,lbegin=0):
    prepare_order(sdata.values())
    prepare_order(idata.values())    
    prepare_order(catalogs) 
    prepare_common(sdata.values(),idata[ref_id])   #准备ma10/20/60/120,golden,silver,vap_pre,svap_ma
    prepare_common(idata.values(),idata[ref_id])   #准备ma10/20/60/120,golden,silver,vap_pre,svap_ma    
    dummy_catalogs('catalog',catalogs)
    from time import time
    tbegin = time()

    pman = None
    dman = None
    myMediator=nmediator_factory(trade_strategy=B0S0,pricer = oo_pricer)
    #seller = atr_seller_factory(stop_times=2000,trace_times=3000)
    seller1200 = atr_seller_factory(stop_times=1200,trace_times=3000)
    seller2000 = atr_seller_factory(stop_times=2000,trace_times=3000)    
    #seller = csc_func
    if lbegin == 0:
        lbegin = end - 5

    configs_a = prepare_configs_A1200(seller1200,pman,dman)
    dtrades_a = batch_last(configs_a,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_a1200.txt',dtrades_a,xbegin,end,lbegin)

    #configs_a = prepare_configs_A2000(seller2000,pman,dman)
    #dtrades_a = batch_last(configs_a,sdata,dates,xbegin,cmediator=myMediator)
    #save_last('atr_last_a2000.txt',dtrades_a,xbegin,end,lbegin)
    configs_a0 = prepare_configs_A0(seller1200,pman,dman)
    dtrades_a0 = batch_last(configs_a0,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_a0.txt',dtrades_a0,xbegin,end,lbegin)
    
    #configs_a1 = prepare_configs_A1(seller1200,pman,dman)
    #dtrades_a1 = batch_last(configs_a1,sdata,dates,xbegin,cmediator=myMediator)
    #save_last('atr_last_a1.txt',dtrades_a1,xbegin,end,lbegin)

    #configs_a2 = prepare_configs_A2(seller1200,pman,dman)
    #dtrades_a2 = batch_last(configs_a2,sdata,dates,xbegin,cmediator=myMediator)
    #save_last('atr_last_a2.txt',dtrades_a2,xbegin,end,lbegin)
    #configs_t = prepare_temp_configs(seller1200,pman,dman)
    #dtrades_t = batch_last(configs_t,sdata,dates,xbegin,cmediator=myMediator)
    #save_last('atr_last_t.txt',dtrades_t,xbegin,end,lbegin)
    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    


if __name__ == '__main__':
    logging.basicConfig(filename="run_x4n_2000.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
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
    #begin,xbegin,end = 20080701,20090101,20090301
    #begin,xbegin,end = 20080701,20090101,20090301
    #begin,xbegin,end,lbegin = 20070101,20080601,20091201,20090201    
    from time import time
    tbegin = time()
    
    dates,sdata,idata,catalogs = prepare_all(begin,end,[],[ref_code])
    sdata.update(idata) #合并指数
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


