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

    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 33,slow=630,rstart=4000,rend=8500))) 	##946-71-500-30     #720-67-500-25
    configs.append(config(buyer=fcustom(svama3,fast=185,mid=260,slow=1800))) 	#830-59-500-32      #638-60-593-32
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid= 54,slow=1770,rstart=5000,rend=8500))) #880-37-500-10      #626-52-600-10
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 48,slow=1140,rstart=4000,rend=8500))) #1425-57-538-13     #1193-74-692-13
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 48,slow=1120,rstart=4500,rend=8500)))	#1948-76-500-10     #1461-91-600-10
    configs.append(config(buyer=fcustom(vama3,fast= 20,mid= 56,slow=105,ma_standard=500,extend_days=  1))) 	#3395-275-500-8     #2524-313-625-8
    #
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 92,slow=1110,rstart=  0,rend=8500))) 	#1619-102-411-17    #1150-84-352-17
    configs.append(config(buyer=fcustom(svama3,fast=165,mid=184,slow=1960))) 	#506-40-461-39      #766-79-641-39
    configs.append(config(buyer=fcustom(vama3,fast= 17,mid= 38,slow=125,ma_standard=500,extend_days=  1))) 	#1990-207-400-5     #1990-207-400-5
    configs.append(config(buyer=fcustom(svama3,fast=  2,mid= 95,slow=130,ma_standard=120,extend_days=  1))) 	#-23    #339-39-333-9
    configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 54,slow= 85,ma_standard= 55,extend_days=  1))) 	#687-44-400-30      #277-25-366-30
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid= 48,slow=520,rstart=4000,rend=8500))) 	#1673-77-360-25     #1387-86-440-25
    configs.append(config(buyer=fcustom(csvama3,fast=150,mid=260,slow=710,rstart=2000,rend=9000))) 	#729-35-333-9       #594-44-444-9
    configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 80,slow=145,ma_standard= 55,extend_days=  1))) 	#1289-98-583-12 #459-68-583-12
    configs.append(config(buyer=fcustom(vama3,fast= 20,mid= 55,slow= 95,ma_standard=500,extend_days=  1))) 	#782-61-500-8   #662-57-500-8
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 78,slow=125,ma_standard= 55,extend_days=  1))) 	#784-62-428-14      #278-39-500-14
    configs.append(config(buyer=fcustom(svama3,fast=  7,mid= 91,slow=300,ma_standard=500,extend_days=  1))) 	#555-35-666-3   #555-35-666-3
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 48,slow=1440,rstart=4000,rend=8500))) #621-23-500-10      #564-22-500-10
    configs.append(config(buyer=fcustom(svama3,fast=150,mid=245,slow=315))) 	#605-46-389-77      #644-58-389-77
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=705,slow=790,rstart=2500,rend=8500))) 	#3481-188-333-3 #3481-188-333-3
    configs.append(config(buyer=fcustom(csvama3,fast=108,mid=176,slow=500,rstart=500,rend=7000))) 	#-362   #386-34-666-3
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 27,slow=270,rstart=7500,rend=8000))) 	#532-49-500-2   #532-49-500-2
    configs.append(config(buyer=fcustom(csvama3,fast=140,mid=430,slow=790,rstart=500,rend=9500))) 	#1196-61-309-13     #616-45-309-13
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid=385,slow=950,rstart=500,rend=8500))) 	#3035-255-428-7     #1479-219-428-7
    configs.append(config(buyer=fcustom(csvama3,fast=215,mid=375,slow=485,rstart=2500,rend=9000))) 	#-1010      #2978-280-333-3
    configs.append(config(buyer=fcustom(csvama3,fast=210,mid=300,slow=530,rstart=4500,rend=9500))) 	#-x     #-z
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 83,slow= 20,ma_standard=500,extend_days=  5))) 	#818-72-328-76   #724-84-373-75
    configs.append(config(buyer=fcustom(svama2x,fast= 47,slow=  5,base=168,ma_standard=500))) 	#701-80-400-5       #871-88-400-5
    configs.append(config(buyer=fcustom(vama3,fast= 16,mid= 78,slow= 45,ma_standard=500,extend_days= 13))) 	#1907-145-348-158   #1716-182-423-156
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 71,slow= 55,ma_standard=500,extend_days= 25))) 	#588-50-329-176     #981-106-404-173
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 67,slow= 45,ma_standard=500,extend_days= 27))) 	#1150-84-405-348    #1204-112-451-328
    configs.append(config(buyer=fcustom(vama3,fast=  9,mid= 68,slow= 45,ma_standard=500,extend_days= 21))) 	#1239-88-418-289    #1300-117-459-274
    configs.append(config(buyer=fcustom(svama3,fast=165,mid=300,slow=1750))) 	#               #597-55-500-28
    configs.append(config(buyer=fcustom(svama3,fast=165,mid=184,slow=1950))) 	#                   #577-63-619-42
    configs.append(config(buyer=fcustom(svama3,fast=180,mid=300,slow=1810))) 	#428-33-517-29      #602-53-586-29
    configs.append(config(buyer=fcustom(svama3,fast=160,mid=300,slow=1800))) 	#                   #463-38-500-36
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid= 25,slow=410,rstart=5500,rend=8000))) 	#               #602-56-625-8
    configs.append(config(buyer=fcustom(csvama3,fast= 42,mid=270,slow=1020,rstart=1500,rend=5500))) #391-54-500-4
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=300,slow=950,rstart=500,rend=8500))) 	#               #675-50-500-10
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=215,slow=1030,rstart=  0,rend=9500))) 	#               #746-94-500-16
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=172,slow=630,rstart=7000,rend=8500))) 	#425-37-500-2
    configs.append(config(buyer=fcustom(csvama3,fast= 39,mid= 48,slow=1160,rstart=4000,rend=8500))) #518-28-500-14    
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
    seller1200 = atr_xseller_factory(stop_times=1200,trace_times=3000)
    seller2000 = atr_xseller_factory(stop_times=2000,trace_times=3000)    
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
    seller1200 = atr_xseller_factory(stop_times=1200,trace_times=3000) 
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


