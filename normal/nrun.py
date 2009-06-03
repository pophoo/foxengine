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

    configs.append(config(buyer=fcustom(s.cma2,fast=5,slow=20,gfrom=4000,gto=8000))) #@3691-707-41
    
    return configs

def prepare_configs_A1200(seller,pman,dman):    
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    
    #候选A_1200 winrate>=500且R>=800,times>5 如果1200和2000都满足，优先为1200
    #暂时停止<550,以及次数小于15的方法

    configs.append(config(buyer=fcustom(vama3,fast= 20,mid= 56,slow=105,ma_standard=500,extend_days=  1))) 	#3585-600-10
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 76,slow=410,rstart=3500,rend=8500))) 	#838-600-10
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=670,rstart=5000,rend=6000))) 	#625-538-13
    configs.append(config(buyer=fcustom(svama3,fast=160,mid=300,slow=1800))) 	#927-500-12
    configs.append(config(buyer=fcustom(svama3,fast=185,mid=260,slow=1800))) 	#840-583-12

    return configs

def prepare_configs_A2000(seller,pman,dman):    #R>=400,winrate>400 or R>=1000,winrate>333
    ''' 目前逐渐与A1200合并
    '''
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    
    #候选A_2000 winrate>=500且R>=800,times>5 
    #暂时停止<600,以及次数小于15的方法
    
    return configs

def prepare_configs_A0(seller,pman,dman):    
    ''' 手工巡游成果
    '''
    #暂时停止<600,以及次数小于15的方法,但保留超过150的
    
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []

    #configs.append(config(buyer=fcustom(s.tsvama2,fast=20,slow=100)))   #3230-562-183   #20080701以来萎靡
    configs.append(config(buyer=s.gx250))   #1695-555-9
    configs.append(config(buyer=s.spring))  #5081-626-123
    configs.append(config(buyer=fcustom(s.cma2,fast=5,slow=20,gfrom=4000,gto=8000))) #@3691-707-41
    configs.append(config(buyer=s.cma1))    #1971-500-30    #593-295-44 ??
    configs.append(config(buyer=s.tsvama2x))    #1628-800-10    #1778-444-9 ??
    configs.append(config(buyer=s.xgcs0))   #2382-528-138       
    configs.append(config(buyer=fcustom(s.tsvama2a,fast=20,slow=100)))   #2714-541-24, 近期成功率升高
    configs.append(config(buyer=fcustom(s.tsvama2b,fast=20,slow=170)))   #2630-583-12, 近期成功率升高


    configs.append(config(buyer=s.gmacd))    #842-330-115,近期5045-911-34
    configs.append(config(buyer=s.gmacd5))   #1146-424-33,近期1000-1000-14    
    configs.append(config(buyer=s.smacd))    #2618/511/45
    configs.append(config(buyer=s.xru))      #4066/612/31
    configs.append(config(buyer=s.mxru))     #1424/443/158  近期1357/594/69
    #configs.append(config(buyer=s.ma4))     #1111-388-54
    #configs.append(config(buyer=s.pmacd))   #671-307-78
    #configs.append(config(buyer=s.wvad))    #816-437-32
    #configs.append(config(buyer=s.xma60))   #1040-390-64
    #configs.append(config(buyer=s.nhigh))     #720-394-147
    #configs.append(config(buyer=s.gx60))    #1205-460-76
    #configs.append(config(buyer=s.vmacd_ma4))   #267-295-115
    #configs.append(config(buyer=fcustom(s.cma2,fast=5,slow=13,gfrom=7000,gto=8500))) #2919-589-156    #近期萎靡
    #configs.append(config(buyer=s.xgcs))   #2030-487-123    
    #configs.append(config(buyer=s.mgcs))   #3564-504-212    

    #埋伏,因为xgcs/mgcs系列的加入，暂时忽略埋伏部分
    #configs.append(config(buyer=s.gcs))   #
    #舍弃
    #configs.append(config(buyer=s.temv))    #575-442-70
    #configs.append(config(buyer=fcustom(s.tsvama2,fast=12,slow=170)))   #1666-451-133
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
    
    #configs = prepare_temp_configs(seller1200,pman,dman)
    #configs = prepare_temp_configs(seller2000,pman,dman)
    #configs = prepare_configs_A2000(seller2000,pman,dman)
    #configs.extend(prepare_configs_A2000(seller2000,pman,dman))
    configs = prepare_configs_A1200(seller1200,pman,dman)
    configs.extend(prepare_configs_A0(seller1200,pman,dman))    
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
    save_configs('atr_ev_v0v2.txt',configs,xbegin,end)    

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
    save_last('atr_last_a1200x.txt',dtrades_a,xbegin,end,lbegin)

    #configs_a = prepare_configs_A2000(seller2000,pman,dman)
    #dtrades_a = batch_last(configs_a,sdata,dates,xbegin,cmediator=myMediator)
    #save_last('atr_last_a2000.txt',dtrades_a,xbegin,end,lbegin)
    configs_a0 = prepare_configs_A0(seller1200,pman,dman)
    dtrades_a0 = batch_last(configs_a0,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_a0x.txt',dtrades_a0,xbegin,end,lbegin)
    
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
    
    #begin,xbegin,end = 20000101,20010701,20090101
    #begin,xbegin,end = 19980101,20010701,20090101
    #begin,xbegin,end = 20000101,20010701,20050901
    #begin,xbegin,end = 19980101,19990701,20010801    
    #begin,xbegin,end = 20040601,20050801,20071031
    #begin,xbegin,end =  20050101,20080701,20091201
    #begin,xbegin,end = 19980101,19990101,20090101
    #begin,xbegin,end = 20080701,20090101,20090301
    #begin,xbegin,end = 20080701,20090101,20090301
    begin,xbegin,end,lbegin = 20070101,20080701,20091201,20090201    
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

    #run_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    #run_merge_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    #run_mm_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    run_last(dates,sdata,idata,catalogs,begin,end,xbegin,lbegin)


