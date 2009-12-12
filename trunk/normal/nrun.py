# -*- coding: utf-8 -*-

#完整的运行脚本
#采用NMediator,结果发现成功率显然小了(次日上涨的看来挺多，导致止损比预计上移),看来需要加大atr系数 ==>1200比较贴近之前的结果
#不过有个特点，大部分情形，选出交易数越多的方法，稳定性越好

from wolfox.fengine.core.d1 import subd

from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *
import wolfox.fengine.normal.funcs as f
import wolfox.fengine.normal.sfuncs as s
import wolfox.fengine.normal.hfuncs as h
from wolfox.fengine.core.d1indicator import atr

import logging
logger = logging.getLogger('wolfox.fengine.normal.run')    

#1 缩小止损，止损和跟随建议为1600/2400
#2 信号出来后打到55/120均线附近


def prepare_temp_configs(seller,pman=None,dman=None):
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []

    #import wolfox.fengine.normal.xrun as x
    configs.append(config(buyer=fcustom(s.emv1b,base=120,fast=15)))
    configs.append(config(buyer=fcustom(s.emv2,slow=290,fast=128)))
    configs.append(config(buyer=fcustom(s.emv2,slow=96,fast=125)))
    configs.append(config(buyer=fcustom(s.emv1b,base=120,fast=27)))
    configs.append(config(buyer=fcustom(s.emv1b,base=120,fast=40)))
    configs.append(config(buyer=fcustom(s.emv1b,base=120,fast=75)))
    configs.append(config(buyer=fcustom(s.emv1,fast=98)))
    configs.append(config(buyer=fcustom(s.emv1,fast=120)))
    configs.append(config(buyer=fcustom(s.emv1,fast=143)))
    configs.append(config(buyer=fcustom(s.emv2,slow=88,fast=17)))
    configs.append(config(buyer=fcustom(s.emv2,slow=100,fast=10)))
    configs.append(config(buyer=fcustom(s.emv2,slow=86,fast=124)))
    configs.append(config(buyer=fcustom(s.emv2,slow=8,fast=3)))
    configs.append(config(buyer=fcustom(s.emv2,slow=275,fast=75)))
    configs.append(config(buyer=fcustom(s.emv2,slow=226,fast=126)))
    configs.append(config(buyer=fcustom(s.emv2,slow=132,fast=194)))
    configs.append(config(buyer=fcustom(s.emv2,slow=292,fast=72)))
    configs.append(config(buyer=fcustom(s.emv2s,slow=30,fast=7)))
    configs.append(config(buyer=fcustom(s.emv1,fast=227)))    

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

def prepare_catalog_buyers():
    buyers=[]
    buyers.append(fcustom(s.tsvama2c,bxatr=30,slow=73,fast=49))
    buyers.append(fcustom(s.ma2s,follow=5,slow=11,fast=6))
    buyers.append(fcustom(s.ldxc,aend=85,astart=50,mlen=55))
    buyers.append(fcustom(s.ma2c,follow=9,slow=134,fast=101))
    buyers.append(fcustom(s.ma2c,follow=3,slow=121,fast=85))
    buyers.append(fcustom(s.emv1c,fast=133))
    buyers.append(fcustom(s.emv2c,slow=36,fast=21))
    return buyers

def prepare_configs_1000(seller,pman,dman):
    ''' #成功率为1000，或者>900且平均盈利/亏损>6
    gmacd5	1000:5274:18:1000:269:0
    ldx:aend=95,astart=65,mlen=39	5820:5820:21:952:308:50
    ldx2:aend=80,astart=70,mlen=41	1000:7860:16:1000:393:0
    ldx2:aend=100,astart=65,mlen=30	11352:7568:10:900:433:34
    xud:astart=0	1000:8541:26:1000:410:0
    xud:astart=0,xfunc=xc0c	5935:7666:24:958:387:62
    xud:astart=0,xfunc=xc02	1000:6568:12:1000:289:0
    emv1b:base=120,fast=15	6631:7411:22:954:266:38
    emv2:slow=290,fast=128	1000:18766:2:1000:1445:0
    emv2:slow=96,fast=125	19500:6348:14:928:296:14
    tsvama3:follow=6,slow=106,mid=73,fast=6	1000:10166:5:1000:244:0
    tsvama3:follow=6,slow=10,mid=21,fast=7	1000:6742:8:1000:236:0
    tsvama2sbv:follow=2,slow=42,fast=7	1000:6500:8:1000:221:0
    tsvama2sbv:follow=3,slow=10,fast=15	1000:4727:10:1000:156:0
    tsvama3b:follow=7,slow=32,mid=133,fast=7	1000:6411:5:1000:327:0
    ###??? 存疑但放宽
    '''

    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []

    configs.append(config(buyer=s.gmacd5))
    configs.append(config(buyer=fcustom(s.ldx,aend=95,astart=65,mlen=39)))
    configs.append(config(buyer=fcustom(s.ldx2,aend=80,astart=70,mlen=41)))
    configs.append(config(buyer=fcustom(s.ldx2,aend=100,astart=65,mlen=30)))
    configs.append(config(buyer=s.mxru3)) 

    configs.append(config(buyer=fcustom(s.xud,astart=0)))
    configs.append(config(buyer=fcustom(s.xud,xfunc=s.xc0c,astart=0)))  #4/9
    configs.append(config(buyer=fcustom(s.xud,xfunc=s.xc0,astart=0)))  #1/5 类同xc02，但xc02更好  ###??? 
    configs.append(config(buyer=fcustom(s.xud,xfunc=s.xc02,astart=0)))  #1/5
    configs.append(config(buyer=fcustom(s.emv1b,base=120,fast=15)))
    configs.append(config(buyer=fcustom(s.emv2,slow=290,fast=128)))
    configs.append(config(buyer=fcustom(s.emv2,slow=96,fast=125)))
    configs.append(config(buyer=fcustom(s.tsvama3,follow=6,slow=106,mid=73,fast=6)))
    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=2,slow=42,fast=7)))
    configs.append(config(buyer=s.eff)) 

    configs.append(config(buyer=h.hxud))
    #configs.append(config(buyer=h.hdev))       ###??? R=.762,W=.537
    configs.append(config(buyer=h.hmxru3))
    configs.append(config(buyer=h.hmxru))
    configs.append(config(buyer=h.mxru3)) 
    configs.append(config(buyer=h.mxru)) 
    configs.append(config(buyer=fcustom(h.emv2,slow=100,fast=10)))
    configs.append(config(buyer=fcustom(h.emv2,slow=88,fast=17)))
    configs.append(config(buyer=h.xud)) 
    configs.append(config(buyer=h.mag)) 
    configs.append(config(buyer=h.heff))     #要小心从事   ###???

    return configs


def prepare_configs_best(seller,pman,dman):
    ''' #wrate>=800,且clost<100
    gmacd	4660:5744:39:948:263:53
    xru0	6760:10666:13:846:580:71
    mxru3	2904:5300:10:900:244:73
    xud0	7333:7542:26:961:276:36
    xudj	9937:6360:9:888:181:16
    ldx:glimit=3000,mlen=60	5595:5465:32:968:244:42
    ldx2:glimit=3333,mlen=30	3518:6347:20:800:386:83
    ldx2:glimit=3333,aend=50,astart=0,mlen=120	1000:6823:4:1000:348:0
    emv1b:base=120,fast=27	5750:7666:18:833:341:48
    emv1b:base=120,fast=40	4076:5578:24:958:224:52
    emv1b:base=120,fast=75	8241:11950:12:916:527:58
    emv1:fast=98	4909:8181:12:833:335:55
    emv1:fast=120	4447:6772:11:909:334:67
    emv1:fast=143	3400:7620:8:875:262:65
    emv2:slow=88,fast=17	3523:5585:13:846:283:65
    emv2:slow=100,fast=10	4112:8588:23:826:368:71
    emv2:slow=86,fast=124	8064:5434:15:866:294:31
    emv2:slow=8,fast=3	3745:5305:55:800:252:51
    tsvama2:bxatr=50,slow=33,fast=3	3260:6521:7:857:365:92
    tsvama2:bxatr=50,slow=75,fast=15	2226:4068:6:833:152:53
    tsvama3:follow=4,slow=14,mid=29,fast=7	2279:6739:23:826:203:68
    tsvama3:follow=10,slow=228,mid=11,fast=7	2932:5580:8:875:206:59
    tsvama2sb:follow=2,slow=192,fast=6	8260:5757:5:800:244:23
    '''
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    

    configs.append(config(buyer=s.gmacd))
    configs.append(config(buyer=s.xru0))
    configs.append(config(buyer=s.xud0))
    configs.append(config(buyer=s.xudj))

    configs.append(config(buyer=fcustom(s.ldx,glimit=3000,mlen=60)))
    configs.append(config(buyer=fcustom(s.ldx2,glimit=3333,mlen=30)))
    configs.append(config(buyer=fcustom(s.ldx2,glimit=3333,aend=50,astart=0,mlen=120)))    ###???
    configs.append(config(buyer=fcustom(s.ldx,aend=95,astart=45,mlen=135)))
    configs.append(config(buyer=fcustom(s.ldx,aend=85,astart=65,mlen=92)))  ###???
    configs.append(config(buyer=fcustom(s.ldx,aend=75,astart=60,mlen=55))) ###???

    configs.append(config(buyer=fcustom(s.emv1b,base=120,fast=40)))
    configs.append(config(buyer=fcustom(s.emv1,fast=98)))
    configs.append(config(buyer=fcustom(s.emv1,fast=120)))
    configs.append(config(buyer=fcustom(s.emv1,fast=143)))
    configs.append(config(buyer=fcustom(s.emv2,slow=86,fast=124)))  ####???
    configs.append(config(buyer=fcustom(s.tsvama2,bxatr=50,slow=33,fast=3)))
    configs.append(config(buyer=fcustom(s.tsvama2,bxatr=50,slow=75,fast=15)))
    configs.append(config(buyer=fcustom(s.tsvama3,follow=4,slow=14,mid=29,fast=7))) ###???
    configs.append(config(buyer=fcustom(s.tsvama3,follow=10,slow=228,mid=11,fast=7)))  ###???
    configs.append(config(buyer=fcustom(s.tsvama2sb,follow=2,slow=192,fast=6)))    ###???
    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=3,slow=10,fast=15)))   ###???
    configs.append(config(buyer=fcustom(s.tsvama3b,follow=7,slow=32,mid=133,fast=7)))   
    configs.append(config(buyer=fcustom(s.tsvama3,follow=6,slow=10,mid=21,fast=7)))

    return configs



def prepare_configs_normal(seller,pman,dman):
    ''' #wrate>=666, 或wrate>=800且clost>100
    xma60	2621:6653:9:666:293:66
    xru	4814:7222:41:731:376:54
    mxru	6764:10147:24:791:449:51
    tsvama2a:slow=100,fast=20	2413:5285:12:750:164:46
    tsvama2b:slow=170,fast=20	2191:4515:9:777:211:68
    emv2:slow=275,fast=75	1000:4653:1:1000:121:0
    emv2:slow=226,fast=126	1000:0:0:0:0:0
    emv2:slow=132,fast=194	1000:0:0:0:0:0
    emv2:slow=292,fast=72	1000:0:0:0:0:0
    emv2s:slow=30,fast=7	4538:5709:26:730:256:39
    tsvama2:bxatr=50,slow=61,fast=7	4020:5583:8:750:285:50
    tsvama2:bxatr=50,slow=105,fast=17	6872:7511:3:666:509:47
    tsvama3:follow=7,slow=24,mid=25,fast=53	1000:5131:5:1000:195:0
    tsvama2sb:follow=4,slow=178,fast=16	1000:6571:3:1000:230:0
    tsvama2sb:follow=3,slow=174,fast=8	3086:4057:10:700:222:46
    tsvama2sb:follow=2,slow=206,fast=6	2131:5062:4:750:242:76
    tsvama2sbv:follow=7,slow=54,fast=36	2692:5600:21:666:236:52
    tsvama2sbv:follow=5,slow=28,fast=10	3775:8423:29:724:324:58
    tsvama2sbv:follow=5,slow=70,fast=18	2115:4230:21:666:191:52
    tsvama2sbv:follow=9,slow=268,fast=12	1000:0:0:0:0:0
    tsvama2sbv:follow=3,slow=42,fast=6	2795:5480:21:714:212:49
    tsvama2sbv:follow=9,slow=26,fast=8	2754:5840:107:728:221:53
    tsvama2sbv:follow=5,slow=282,fast=12	1000:0:0:0:0:0
    tsvama2sbv:follow=1,slow=26,fast=8	1000:736:1:1000:14:0
    ma2s:follow=2,slow=16,fast=3	2000:5600:18:666:196:56
    ma2sv:follow=2,slow=8,fast=1	3420:5516:38:736:251:50
    tsvama3b:follow=1,slow=60,mid=35,fast=9	1774:4782:6:833:145:62
    tsvama3b:follow=3,slow=64,mid=93,fast=11	1573:3692:10:800:136:61
    tsvama3b:follow=1,slow=60,mid=107,fast=5	813:4037:3:666:230:134
    tsvama3b:follow=7,slow=32,mid=149,fast=5	1000:6361:2:1000:229:0
    tsvama3b:follow=3,slow=72,mid=107,fast=8	1758:4541:10:700:183:62    
    '''
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []

    #configs.append(config(buyer=s.xma60))
    configs.append(config(buyer=s.xru))
    configs.append(config(buyer=s.mxru))
    #configs.append(config(buyer=fcustom(s.ldx,aend=80,astart=0,mlen=55)))
    configs.append(config(buyer=fcustom(s.ldx2,aend=80,astart=45,mlen=138)))
    configs.append(config(buyer=fcustom(s.tsvama2a,slow=100,fast=20)))
    configs.append(config(buyer=fcustom(s.tsvama2b,slow=170,fast=20)))

    configs.append(config(buyer=fcustom(s.emv1b,base=120,fast=27))) 
    configs.append(config(buyer=fcustom(s.emv1b,base=120,fast=75)))

    configs.append(config(buyer=fcustom(s.emv2,slow=88,fast=17)))
    configs.append(config(buyer=fcustom(s.emv2,slow=100,fast=10)))
    configs.append(config(buyer=fcustom(s.emv2,slow=8,fast=3)))    

    configs.append(config(buyer=fcustom(s.emv2,slow=275,fast=75)))
    configs.append(config(buyer=fcustom(s.emv2,slow=226,fast=126)))
    #configs.append(config(buyer=fcustom(s.emv2,slow=132,fast=194)))
    configs.append(config(buyer=fcustom(s.emv2,slow=292,fast=72)))
    configs.append(config(buyer=fcustom(s.emv2s,slow=30,fast=7)))

    configs.append(config(buyer=fcustom(s.tsvama2,bxatr=50,slow=61,fast=7)))
    configs.append(config(buyer=fcustom(s.tsvama2,bxatr=50,slow=105,fast=17)))
    configs.append(config(buyer=fcustom(s.tsvama3,follow=7,slow=24,mid=25,fast=53)))
    #configs.append(config(buyer=fcustom(s.tsvama2sb,follow=4,slow=178,fast=16)))
    #configs.append(config(buyer=fcustom(s.tsvama2sb,follow=3,slow=174,fast=8)))
    #configs.append(config(buyer=fcustom(s.tsvama2sb,follow=2,slow=206,fast=6)))
    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=7,slow=54,fast=36)))
    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=5,slow=28,fast=10)))
    #configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=5,slow=70,fast=18)))
    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=9,slow=268,fast=12)))
    #configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=3,slow=42,fast=6)))
    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=9,slow=26,fast=8)))
    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=5,slow=282,fast=12)))
    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=1,slow=26,fast=8)))
    #configs.append(config(buyer=fcustom(s.ma2s,follow=2,slow=16,fast=3)))
    configs.append(config(buyer=fcustom(s.ma2sv,follow=2,slow=8,fast=1)))
    configs.append(config(buyer=fcustom(s.tsvama3b,follow=1,slow=60,mid=35,fast=9)))
    configs.append(config(buyer=fcustom(s.tsvama3b,follow=3,slow=64,mid=93,fast=11)))    
    #configs.append(config(buyer=fcustom(s.tsvama3b,follow=1,slow=60,mid=107,fast=5)))
    configs.append(config(buyer=fcustom(s.tsvama3b,follow=7,slow=32,mid=149,fast=5)))
    #configs.append(config(buyer=fcustom(s.tsvama3b,follow=3,slow=72,mid=107,fast=8)))

    return configs


def prepare_configs_others(seller,pman,dman):
    ''' #剩余部分
    spring	2216:6133:16:625:345:83
    emv1:fast=227	1000:0:0:0:0:0
    tsvama2:bxatr=50,slow=21,fast=7	4094:6382:8:625:379:53
    tsvama2:bxatr=50,slow=49,fast=3	3000:5647:11:545:407:64
    #tsvama3:follow=5,slow=26,mid=23,fast=63	2301:5370:24:625:270:63 #参数不合理
    tsvama3:follow=10,slow=108,mid=75,fast=48	11529:14000:4:500:409:17
    tsvama2sb:follow=10,slow=176,fast=8	3097:4233:25:600:239:41
    tsvama2sb:follow=3,slow=280,fast=15	1000:0:0:0:0:0
    tsvama2sb:follow=3,slow=130,fast=24	1000:6220:1:1000:423:0
    #tsvama2sbv:follow=3,slow=28,fast=19	1835:5590:9:555:275:67  #走坏
    tsvama2sbv:follow=5,slow=16,fast=2	2775:5440:118:644:238:49
    #tsvama2sbv:follow=3,slow=12,fast=6	2207:5571:68:500:287:53     #走坏
    tsvama3b:follow=1,slow=208,mid=25,fast=11	1000:8920:2:1000:223:0
    '''
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    configs.append(config(buyer=s.spring))  ##??
    configs.append(config(buyer=fcustom(s.emv1,fast=227)))
    configs.append(config(buyer=fcustom(s.tsvama2,bxatr=50,slow=21,fast=7)))
    #configs.append(config(buyer=fcustom(s.tsvama2,bxatr=50,slow=49,fast=3)))
    #configs.append(config(buyer=fcustom(s.tsvama3,follow=5,slow=26,mid=23,fast=63)))
    #configs.append(config(buyer=fcustom(s.tsvama3,follow=10,slow=108,mid=75,fast=48)))
    #configs.append(config(buyer=fcustom(s.tsvama2sb,follow=10,slow=176,fast=8)))
    configs.append(config(buyer=fcustom(s.tsvama2sb,follow=3,slow=280,fast=15)))
    configs.append(config(buyer=fcustom(s.tsvama2sb,follow=3,slow=130,fast=24)))
    #configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=3,slow=28,fast=19)))
    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=5,slow=16,fast=2)))
    #configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=3,slow=12,fast=6)))
    #configs.append(config(buyer=fcustom(s.tsvama3b,follow=1,slow=208,mid=25,fast=11)))
    
    return configs


def prepare_configs_A0(seller,pman,dman):    
    ''' 实际上需要暂停平均盈亏率<100的
    '''
    
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    
    configs.append(config(buyer=fcustom(s.tsvama2a,fast=20,slow=100)))   
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

    configs.append(config(buyer=fcustom(s.emv1b,fast=15,base=120)))      #1/5
    configs.append(config(buyer=fcustom(s.emv1b,fast=27,base=120)))      #1/4
    configs.append(config(buyer=fcustom(s.emv1b,fast=40,base=120)))      #1/3
    configs.append(config(buyer=fcustom(s.emv1b,fast=75,base=120)))      #1/3
    
    configs.append(config(buyer=fcustom(s.emv1,fast=98)))      #5/11   #emv1b,base=120更好,但排斥过多
    configs.append(config(buyer=fcustom(s.emv1,fast=120)))     #2/5
    configs.append(config(buyer=fcustom(s.emv1,fast=143)))     #3/8
    configs.append(config(buyer=fcustom(s.emv1,fast=227)))     #

    configs.append(config(buyer=fcustom(s.emv2,fast=75,slow=275)))    #1/4 
    configs.append(config(buyer=fcustom(s.emv2,fast=128,slow=290)))   #2/2  
    configs.append(config(buyer=fcustom(s.emv2,fast=126,slow=226)))   #0/0  
    configs.append(config(buyer=fcustom(s.emv2,fast=194,slow=132)))   #0/0  
    configs.append(config(buyer=fcustom(s.emv2,fast=72,slow=292)))    #0/0  
    configs.append(config(buyer=fcustom(s.emv2,fast=17,slow=88)))     #5/13  
    configs.append(config(buyer=fcustom(s.emv2,fast=10,slow=100)))    #1/8
    configs.append(config(buyer=fcustom(s.emv2,fast=124,slow=86)))    #1/3  
    configs.append(config(buyer=fcustom(s.emv2,fast=125,slow=96)))    #1/2  
    configs.append(config(buyer=fcustom(s.emv2,fast=3,slow=8)))       #3/11  

    configs.append(config(buyer=fcustom(s.emv2s,fast=7,slow=30)))     #1/5


    configs.append(config(buyer=fcustom(s.tsvama2,fast=3,slow=33,bxatr=50)))    #4/15
    configs.append(config(buyer=fcustom(s.tsvama2,fast=7,slow=61,bxatr=50)))    #3/10
    configs.append(config(buyer=fcustom(s.tsvama2,fast=7,slow=21,bxatr=50)))    #1/3
    configs.append(config(buyer=fcustom(s.tsvama2,fast=15,slow=75,bxatr=50)))   #1/7
    configs.append(config(buyer=fcustom(s.tsvama2,fast=3,slow=49,bxatr=50)))    #4/14
    configs.append(config(buyer=fcustom(s.tsvama2,fast=17,slow=105,bxatr=50)))  #1/3
    #configs.append(config(buyer=fcustom(s.tsvama2,fast=15,slow=111,bxatr=50)))  #1/7

    configs.append(config(buyer=fcustom(s.tsvama3,follow=6,slow=106,mid=73,fast=6)))
    configs.append(config(buyer=fcustom(s.tsvama3,follow=4,slow=14,mid=29,fast=7)))
    configs.append(config(buyer=fcustom(s.tsvama3,follow=10,slow=228,mid=11,fast=7)))
    configs.append(config(buyer=fcustom(s.tsvama3,follow=5,slow=26,mid=23,fast=63)))
    configs.append(config(buyer=fcustom(s.tsvama3,follow=6,slow=10,mid=21,fast=7)))
    configs.append(config(buyer=fcustom(s.tsvama3,follow=10,slow=108,mid=75,fast=48)))
    configs.append(config(buyer=fcustom(s.tsvama3,follow=7,slow=24,mid=25,fast=53)))

    configs.append(config(buyer=fcustom(s.tsvama2sb,follow=10,slow=176,fast=8)))
    configs.append(config(buyer=fcustom(s.tsvama2sb,follow=4,slow=178,fast=16)))
    configs.append(config(buyer=fcustom(s.tsvama2sb,follow=3,slow=280,fast=15)))
    configs.append(config(buyer=fcustom(s.tsvama2sb,follow=3,slow=130,fast=24)))
    configs.append(config(buyer=fcustom(s.tsvama2sb,follow=2,slow=192,fast=6)))
    configs.append(config(buyer=fcustom(s.tsvama2sb,follow=3,slow=174,fast=8)))
    configs.append(config(buyer=fcustom(s.tsvama2sb,follow=2,slow=206,fast=6)))

    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=7,slow=54,fast=36)))
    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=5,slow=28,fast=10)))
    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=2,slow=42,fast=7)))
    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=3,slow=28,fast=19)))
    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=5,slow=16,fast=2)))
    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=5,slow=70,fast=18)))
    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=9,slow=268,fast=12)))
    #configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=3,slow=28,fast=12)))
    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=3,slow=42,fast=6)))
    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=9,slow=26,fast=8)))
    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=3,slow=12,fast=6)))
    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=5,slow=282,fast=12)))
    #configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=3,slow=26,fast=4)))
    #configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=9,slow=12,fast=20)))
    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=3,slow=10,fast=15)))
    #configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=3,slow=26,fast=8)))
    #configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=11,slow=10,fast=28)))
    configs.append(config(buyer=fcustom(s.tsvama2sbv,follow=1,slow=26,fast=8)))

    configs.append(config(buyer=fcustom(s.ma2s,follow=2,slow=16,fast=3)))
    configs.append(config(buyer=fcustom(s.ma2sv,follow=2,slow=8,fast=1)))

    configs.append(config(buyer=fcustom(s.tsvama3b,follow=1,slow=60,mid=35,fast=9)))
    configs.append(config(buyer=fcustom(s.tsvama3b,follow=3,slow=64,mid=93,fast=11)))
    configs.append(config(buyer=fcustom(s.tsvama3b,follow=3,slow=72,mid=107,fast=8)))
    configs.append(config(buyer=fcustom(s.tsvama3b,follow=1,slow=60,mid=107,fast=5)))
    configs.append(config(buyer=fcustom(s.tsvama3b,follow=1,slow=208,mid=25,fast=11)))
    configs.append(config(buyer=fcustom(s.tsvama3b,follow=7,slow=32,mid=133,fast=7)))    
    configs.append(config(buyer=fcustom(s.tsvama3b,follow=7,slow=32,mid=149,fast=5)))

    #configs.append(config(buyer=fcustom(s.tsvama2,fast=20,slow=100)))   #3230-562-183   #20080701以来萎靡
    #configs.append(config(buyer=fcustom(s.cma2,fast=5,slow=20,gfrom=4000,gto=8000))) #@3691-707-41
    #configs.append(config(buyer=s.cma1))    #1971-500-30    #593-295-44 ??
    #configs.append(config(buyer=s.tsvama2x))    #1628-800-10    #1778-444-9 ??          #次数太少
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
        s.magic = gand(s.g5>s.g60,s.g20 >= s.g60,s.g60 >= s.g120,s.g120 >= s.g250,s.g20<8000)
        s.svap_ma_67 = svap_ma(v,c,67)
        s.svap_ma_67_2 = svap_ma(v,c,67,weight=2)        
        #s.vap_ma_67 = vap_pre(v,c,67)
        s.ks = subd(c) * BASE / rollx(c)
        try:    #计算
            s.silver = catalog_signal_cs(s.c60,csilver)
        except:
            s.silver = cached_zeros(len(c))

def prepare_common(sdata,ref):
    for s in sdata:
        #print s.code
        s.ref = ref
        prepare_common_common(s)
        c = s.transaction[CLOSE]
        v = s.transaction[VOLUME]        
        try:    #计算
            s.silver = catalog_signal_cs(s.c60,csilver)
        except:
            s.silver = cached_zeros(len(c))
        try:    #计算换手率
            s.xchange = v*BASE/s.ag
        except:
            s.xchange = v / 10  #假设s.ag=10000

def prepare_common_catalog(catalogs,ref):
    smaker = signals_maker(prepare_catalog_buyers())
    for s in catalogs:
        #print s.code
        s.code = s.name
        s.ref = ref
        prepare_common_common(s)
        s.csignal = smaker(s)

def prepare_common_common(s):
    c = s.transaction[CLOSE]
    v = s.transaction[VOLUME]
    s.ma0 = ma(c,3)
    s.ma1= ma(c,7)
    s.ma2 = ma(c,13)
    s.ma3 = ma(c,30)
    s.ma4 = ma(c,60)
    s.ma5 = ma(c,120)
    s.t5 = strend(s.ma5) > 0
    s.t4 = strend(s.ma4) > 0
    s.t3 = strend(s.ma3) > 0
    s.t2 = strend(s.ma2) > 0
    s.t1 = strend(s.ma1) > 0
    s.t0 = strend(s.ma0) > 0
    s.above = gand(s.ma2>s.ma3,s.ma3>s.ma4,s.ma4>s.ma5)
    #将golden和above分开
    s.golden = gand(s.g20 >= s.g60+1000,s.g60 >= s.g120+1000,s.g20>=3000,s.g20<=8000)
    s.thumb = gand(s.g20 >= s.g60,s.g60 >= s.g120,s.g120 >= s.g250,s.g20>=3000,s.g20<=8000)
    s.magic = gand(s.g5>s.g60,s.g20 >= s.g60,s.g60 >= s.g120,s.g120 >= s.g250,s.g20<8000)
    s.svap_ma_67 = svap_ma(v,c,67)
    #s.vap_ma_67 = vap_pre(v,c,67)
    #s.svap_ma_67_1 = svap_ma(v,c,67,weight=1)        
    s.svap_ma_67_2 = svap_ma(v,c,67,weight=2)        
    s.ks = subd(c) * BASE / rollx(c)
    s.diff,s.dea = cmacd(c)
    s.atr = atr(c,s.transaction[HIGH],s.transaction[LOW],20)
    

def prepare_index(index):
    index.pdiff,index.pdea = cmacd(index.transaction[CLOSE])

def run_body(sdata,dates,begin,end,xbegin):
    from time import time
    tbegin = time()

    pman = AdvancedATRPositionManager()
    dman = XDateManager(dates)
    myMediator=nmediator_factory(trade_strategy=B1S1,pricer = oo_pricer)
    seller1200 = atr_xseller_factory(stop_times=1200,trace_times=3000)
    seller2000 = atr_xseller_factory(stop_times=2000,trace_times=3000)    
    #seller = csc_func
    #seller = fcustom(csc_func,threshold=100)
    
    #configs = prepare_temp_configs(seller1200,pman,dman)
    #configs = prepare_temp_configs(seller2000,pman,dman)
    #configs = prepare_configs_A2000(seller2000,pman,dman)
    #configs.extend(prepare_configs_A2000(seller2000,pman,dman))
    #configs = prepare_configs_A0(seller1200,pman,dman)
    #configs = prepare_configs_1000(seller1200,pman,dman)    
    #configs.extend(prepare_configs_best(seller1200,pman,dman))        
    configs = prepare_configs_1000(seller2000,pman,dman)    
    configs.extend(prepare_configs_best(seller2000,pman,dman))        
    #configs.extend(prepare_configs_normal(seller1200,pman,dman))    
    #configs.extend(prepare_configs_others(seller1200,pman,dman))    
    #configs.extend(prepare_configs_normal(seller1200,pman,dman))    
    #configs.extend(prepare_configs_others(seller1200,pman,dman))    
    
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
    save_configs('atr_ev_2000b.txt',configs,xbegin,end)    

def run_merge_body(sdata,dates,begin,end,xbegin):
    
    from time import time
    tbegin = time()

    pman = AdvancedATRPositionManager()
    dman = XDateManager(dates)
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

def prepare_next(sdata,idata,catalogs):
    prepare_order(sdata.values())
    prepare_order(idata.values())
    prepare_order(catalogs)
    ref = idata[ref_id]
    prepare_common(sdata.values(),ref)   #准备ma10/20/60/120,golden,silver,vap_pre,svap_ma
    prepare_common(idata.values(),ref)   #准备ma10/20/60/120,golden,silver,vap_pre,svap_ma
    prepare_common_catalog(catalogs,ref)
    prepare_index(idata[1])
    dummy_catalogs('catalog',catalogs)
    ref.sud = sud(sdata.values(),distance=10)
    ref.vud = vud(sdata.values())
    ref.index = calc_indices_avg(sdata.values())

def run_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    run_body(sdata,dates,begin,end,xbegin)

def run_merge_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    run_merge_body(sdata,dates,begin,end,xbegin)

def run_last(dates,sdata,idata,catalogs,begin,end,xbegin,lbegin=0):
    from time import time
    tbegin = time()

    pman = None
    dman = XDateManager(dates)
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
    #configs_a0 = prepare_configs_A0(seller1200,pman,dman)
    #dtrades_a0 = batch_last(configs_a0,sdata,dates,xbegin,cmediator=myMediator)
    #save_last('atr_last_a0y.txt',dtrades_a0,xbegin,end,lbegin)

    #configs_1000 = prepare_configs_1000(seller1200,pman,dman)
    configs_1000 = prepare_configs_1000(seller2000,pman,dman)
    dtrades_1000 = batch_last(configs_1000,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_1000.txt',dtrades_1000,xbegin,end,lbegin)

    #configs_best = prepare_configs_best(seller1200,pman,dman)
    configs_best = prepare_configs_best(seller2000,pman,dman)
    dtrades_best = batch_last(configs_best,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_best.txt',dtrades_best,xbegin,end,lbegin)
    
    #normal及以下省略
    #configs_normal = prepare_configs_normal(seller1200,pman,dman)
    #dtrades_normal = batch_last(configs_normal,sdata,dates,xbegin,cmediator=myMediator)
    #save_last('atr_last_normal.txt',dtrades_normal,xbegin,end,lbegin)

    #configs_others = prepare_configs_others(seller1200,pman,dman)
    #dtrades_others = batch_last(configs_others,sdata,dates,xbegin,cmediator=myMediator)
    #save_last('atr_last_others.txt',dtrades_others,xbegin,end,lbegin)

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
    #begin,xbegin,end = 20040101,20050101,20071031
    #begin,xbegin,end = 20050101,20070701,20091201
    #begin,xbegin,end = 19980101,19990101,20090101
    #begin,xbegin,end = 20080701,20090101,20090301
    #begin,xbegin,end = 20080701,20090101,20090301
    begin,xbegin,end,lbegin = 20060101,20071031,20191201,20090201
    #begin,xbegin,end,lbegin = 20090301,20090401,20090501,20090501
    from time import time
    tbegin = time()
    
    dates,sdata,idata,catalogs = prepare_all(begin,end,[],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH601988','SH600050'],[ref_code])    
    #sdata.update(idata) #合并指数，合并指数还是不妥，虽然可以计算指数的排序.但会紊乱其它针对stock的计算
    scatalog = dict([(c.name,c) for c in catalogs])
    prepare_next(sdata,idata,catalogs)
    
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
    
    tbegin = time()
    for st in sdata.values(): h.prepare_hour(st,begin,end)
    print u'小时数据准备耗时: %s' % (time()-tbegin)    

    #run_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    #run_main(dates,scatalog,idata,catalogs,begin,end,xbegin)
    #run_merge_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    #run_mm_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    
    run_last(dates,sdata,idata,catalogs,begin,end,xbegin,lbegin)
    #catalog_macd(catalogs)

