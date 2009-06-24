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

    configs.append(config(buyer=s.xma60))   #1040-390-64

    return configs

def prepare_configs_A1200(seller,pman,dman):    
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    
    #候选A_1200 winrate>=500且R>=800,times>5 如果1200和2000都满足，优先为1200
    #暂时停止<550,以及次数小于15的方法

    #以下提升率都为0
    #configs.append(config(buyer=fcustom(vama3,fast= 20,mid= 56,slow=105,ma_standard=500,extend_days=  1))) 	#3585-600-10
    #configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 76,slow=410,rstart=3500,rend=8500))) 	#838-600-10
    #configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=670,rstart=5000,rend=6000))) 	#625-538-13
    #configs.append(config(buyer=fcustom(svama3,fast=160,mid=300,slow=1800))) 	#927-500-12
    #configs.append(config(buyer=fcustom(svama3,fast=185,mid=260,slow=1800))) 	#840-583-12

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
    ''' 实际上需要暂停平均盈亏率<100的
        手工巡游成果    19990701-20010701       20010701-20081231           20080701-20090612
        gx250	        1000-1-1000-9-0-9	    1971-7-71-1093-138-136	    2200-2-50-27-5-11
        spring	        -1000-1-0-0-21—21	    5483-96-65-33627-1997-329	1927-16-62-3072-503-160
        xgcs0	        0	                    4097-48-66-15341-1157-295	2421-6-67-628-76-92
        tsvama2b	    0	                    1879-12-500-2598-546-171	1779-8-75-1107-136-121
        gmacd	        -96-16-312-646-746- -6	1551-56-41-10457-2891-135	4113-39-95-8622-106-218
        gmacd5	        -485-6-333-79-266- -32	1408-15-53-3247-808-162	    1000-17-100-4287-0-252
        xru	            21-11-272-387-372-1	    3816-37-56-9449-971-229	    3613-37-65-6495-578-159
        xru0	        1000-1-100-83-0-83	    5089-12-66-3657-227-285	    5197-13-85-4943-143-369
        mxru	        0	                    1550-47-48-7722-1853-124	5313-19-73-5410-259-271
        mxru3	        0	                    1186-19-26-3155-1205-102	1000-8-100-1908-0-238
        xud	            1000-2-100-734-2-367	1181-12-66-2109-464-137	    1000-19-100-6140-0-323
        xud(xc0c)	    1000-1-100-417-0-417	2262-14-57-3025-483-181	    1000-18-100-5865-0-325
        xud(xc0)	    0	                    1510-8-50-1486-368-139	    同xc02
        xud(xc02)	    0	                    2177-8-62-1619-239-172	    1000-10-100-1710-0-171
        ldx	            0                   	6850-10-70-4294-180-411	    4619-32-97-6279-42-194
        ldx2(30,3333)	0	                    4698-28-82-8616-319-296	    3769-20-80-5163-263-245
        ldx2(120,3333)	184-2-500-52-38-7	    1020-11-27-965-402-51	    19250-4-75-1248-16-308
        xma60	        -1000-1-0-0-96--96	    1440-53-45-7935-2178-108	7034-6-66-1285-58-204
        这里xud系列的都是xatr>45条件下，但是应用中用xatr>0, 近期效果是一样的，后者的失败日只是买入截断引起的。        
    '''
    #暂时停止<600,以及次数小于15的方法,但保留超过150的
    
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []

    
    #configs.append(config(buyer=s.gx250))   #
    configs.append(config(buyer=s.spring))  #5/16
    #configs.append(config(buyer=s.xgcs0))   #平均收益率太低
    configs.append(config(buyer=fcustom(s.tsvama2b,fast=20,slow=170)))   #1/4
    configs.append(config(buyer=s.xma60))   #
    configs.append(config(buyer=s.gmacd))    #1/4
    configs.append(config(buyer=s.gmacd5))   #1/3
    configs.append(config(buyer=s.xru))      #1/5
    configs.append(config(buyer=s.xru0))      #1/3
    #configs.append(config(buyer=fcustom(s.xru0,xfunc=s.xc_ru02)))      #都不够稳定
    #configs.append(config(buyer=fcustom(s.xru0,xfunc=s.xc_ru0s)))      #1/3
    #configs.append(config(buyer=fcustom(s.xru0,xfunc=s.xc_ru0c)))      #
    configs.append(config(buyer=s.mxru))     #1/4
    configs.append(config(buyer=s.mxru3))     #3/8
    configs.append(config(buyer=fcustom(s.ldx,mlen=60,glimit=3000)))     #1/10
    configs.append(config(buyer=fcustom(s.ldx2,mlen=30,glimit=3333)))     #2/5
    configs.append(config(buyer=fcustom(s.ldx2,mlen=120,glimit=3333,astart=0,aend=50)))     #1/4
    configs.append(config(buyer=fcustom(s.xud,astart=0)))      #1/2
    configs.append(config(buyer=fcustom(s.xud,xfunc=s.xc0c,astart=0)))  #4/9
    #configs.append(config(buyer=fcustom(s.xud,xfunc=s.xc0,astart=0)))  #1/5 类同xc02，但xc02更好
    configs.append(config(buyer=fcustom(s.xud,xfunc=s.xc02,astart=0)))  #1/5
    configs.append(config(buyer=s.xud0))  #蓝筹
    configs.append(config(buyer=s.xudj))  #基金


    #configs.append(config(buyer=fcustom(s.tsvama2,fast=20,slow=100)))   #3230-562-183   #20080701以来萎靡
    #configs.append(config(buyer=fcustom(s.cma2,fast=5,slow=20,gfrom=4000,gto=8000))) #@3691-707-41
    #configs.append(config(buyer=s.cma1))    #1971-500-30    #593-295-44 ??
    #configs.append(config(buyer=s.tsvama2x))    #1628-800-10    #1778-444-9 ??          #次数太少
    #configs.append(config(buyer=fcustom(s.tsvama2a,fast=20,slow=100)))   #2714-541-24, 近期成功率升高   #1/20提升率
    #configs.append(config(buyer=s.smacd))    #2618/511/45                   #1/10提升率

    #configs.append(config(buyer=s.ma4))     #1111-388-54
    #configs.append(config(buyer=s.pmacd))   #671-307-78
    #configs.append(config(buyer=s.wvad))    #816-437-32

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
def prepare_common_old(sdata,ref):
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

def prepare_common(sdata,ref):
    for s in sdata:
        #print s.code
        s.ref = ref
        c = s.transaction[CLOSE]
        v = s.transaction[VOLUME]
        s.ma1= ma(c,7)
        s.ma2 = ma(c,13)
        s.ma3 = ma(c,30)
        s.ma4 = ma(c,60)
        s.ma5 = ma(c,120)
        s.t5 = strend(s.ma5) > 0
        s.t4 = strend(s.ma4) > 0
        s.t3 = strend(s.ma4) > 0
        s.t2 = strend(s.ma2) > 0
        s.t1 = strend(s.ma1) > 0
        s.above = gand(s.ma2>s.ma3,s.ma3>s.ma4,s.ma4>s.ma5)
        #将golden和above分开
        s.golden = gand(s.g20 >= s.g60+1000,s.g60 >= s.g120+1000,s.g20>=3000,s.g20<=8000)
        s.thumb = gand(s.g20 >= s.g60,s.g60 >= s.g120,s.g120 >= s.g250,s.g20>=3000,s.g20<=8000)
        s.svap_ma_67 = svap_ma(v,c,67)
        s.vap_ma_67 = vap_pre(v,c,67)
        s.ks = subd(c) * BASE / rollx(c)
        s.diff,s.dea = cmacd(c)
        try:    #计算
            s.silver = catalog_signal_cs(s.c60,csilver)
        except:
            s.silver = cached_zeros(len(c))
        try:    #计算换手率
            s.xchange = v*BASE/s.ag
        except:
            s.xchange = v / 10  #假设s.ag=10000

def prepare_index(index):
    index.pdiff,index.pdea = cmacd(index.transaction[CLOSE])

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
    configs = prepare_configs_A0(seller1200,pman,dman)
    #configs = prepare_configs_A1200(seller1200,pman,dman)
    #configs.extend(prepare_configs_A0(seller1200,pman,dman))    
    #configs.extend(prepare_configs_A1(seller1200,pman,dman))
    #configs.extend(prepare_configs_A2(seller1200,pman,dman))    
    
    #seller3600 = atr_xseller_factory(stop_times=600,trace_times=2000)
    #configs = prepare_configs_A1200(seller3600,pman,dman)
    #configs.extend(prepare_configs_A0(seller3600,pman,dman))    

    batch(configs,sdata,dates,xbegin,cmediator=myMediator)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    

    #save_configs('atr_ev_nm_1200.txt',configs,xbegin,end)
    save_configs('atr_ev_v0v3a.txt',configs,xbegin,end)    

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

    seller2000 = atr_xseller_factory(stop_times=2000,trace_times=3000) 
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
    prepare_index(idata[1])
    dummy_catalogs('catalog',catalogs)
    run_body(sdata,dates,begin,end,xbegin)

def run_merge_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata.values())
    prepare_order(idata.values())    
    prepare_order(catalogs)    
    prepare_common(sdata.values(),idata[ref_id])   #准备ma10/20/60/120,golden,silver,vap_pre,svap_ma
    prepare_common(idata.values(),idata[ref_id])   #准备ma10/20/60/120,golden,silver,vap_pre,svap_ma    
    prepare_index(idata[1])
    dummy_catalogs('catalog',catalogs)
    run_merge_body(sdata,dates,begin,end,xbegin)

def run_last(dates,sdata,idata,catalogs,begin,end,xbegin,lbegin=0):
    prepare_order(sdata.values())
    prepare_order(idata.values())    
    prepare_order(catalogs) 
    prepare_common(sdata.values(),idata[ref_id])   #准备ma10/20/60/120,golden,silver,vap_pre,svap_ma
    prepare_common(idata.values(),idata[ref_id])   #准备ma10/20/60/120,golden,silver,vap_pre,svap_ma    
    prepare_index(idata[1])
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

    #configs_a = prepare_configs_A1200(seller1200,pman,dman)
    #dtrades_a = batch_last(configs_a,sdata,dates,xbegin,cmediator=myMediator)
    #save_last('atr_last_a1200x.txt',dtrades_a,xbegin,end,lbegin)

    #configs_a = prepare_configs_A2000(seller2000,pman,dman)
    #dtrades_a = batch_last(configs_a,sdata,dates,xbegin,cmediator=myMediator)
    #save_last('atr_last_a2000.txt',dtrades_a,xbegin,end,lbegin)
    configs_a0 = prepare_configs_A0(seller1200,pman,dman)
    dtrades_a0 = batch_last(configs_a0,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_a0y.txt',dtrades_a0,xbegin,end,lbegin)
    
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

def catalog_macd(catalogs):
    for c in catalogs:
        x = c.transaction[0]
        xdiff,xdea = cmacd(x)
        xc = cross(xdea,xdiff)
        c.xc = xc
        if xc[-1]==1:
            print u'macd:',c.name


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
    begin,xbegin,end,lbegin = 20060101,20080701,20091201,20090201    
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
    catalog_macd(catalogs)

