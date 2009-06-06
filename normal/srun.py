# -*- coding: utf-8 -*-

#指定股票的测试运行脚本

#106493077@sis
#catknight_by_MiMiP2P@18p2p@SIS@Touch99
from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *
from wolfox.fengine.normal.nrun import prepare_order,prepare_common
from wolfox.fengine.core.d1ex import tmax,derepeatc,derepeatc_v,equals,msum,tmin,extend,extend2next,pzoom_out,vzoom_out,zoom_in
from wolfox.fengine.core.d1match import *
from wolfox.fengine.core.d1 import lesser
from wolfox.fengine.core.d1indicator import cmacd,score2,rsi,obv
from wolfox.fengine.core.d1idiom import down_period,macd_ru,macd_ru2,macd_ruv,xc_ru,xc_ru2
from wolfox.fengine.core.d2 import increase,extract_collect
from wolfox.foxit.base.tutils import linelog
from time import time

import logging
logger = logging.getLogger('wolfox.fengine.normal.run')    

def check(stock,dates,tail=30):
    f = open('check.txt','a+')
    f.write('\n#############################')
    f.write(stock.code)
    f.write('#############################\n')    
    for d,g20,g60,g120 in zip(dates,stock.g20,stock.g60,stock.g120)[-tail:]:
        print >>f,d,g20,g60,g120
    f.close()

def check2(sdata,sname,dates,tail=30):
    stock = sdata[code2id[sname]]
    f = open('check.txt','a+')
    f.write('\n#############################')
    f.write(stock.code)
    f.write('#############################\n')    
    for d,g5,g20,g60,g120,g250 in zip(dates,stock.g5,stock.g20,stock.g60,stock.g120,stock.g250)[-tail:]:
        print >>f,d,g5,g20,g60,g120,g250
    f.close()

sbuyer = fcustom(svama3,fast=185,mid=260,slow=1800)
def swrap(stock,dates):
    linelog(stock.code)
    sbuy = sbuyer(stock)
    return sbuy
    #g = gand(stock.g20>=3000,stock.g20<=8000)    
    #return gand(g,sbuy)

def breakout(stock):
    ''' 带量突破走势,没戏
    '''
    t = stock.transaction
    lma = ma(t[CLOSE],250)
    linelog(stock.code)

    sma = ma(t[CLOSE],3)

    xc = cross(lma,sma) > 0

    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)

    vfilter = gand(svma > vma /2,svma<vma*2)

    signal = gand(xc,vfilter)
    
    return signal

def fractal(stock):
    ''' 谐振
    '''
    t = stock.transaction
    zc = pzoom_out(t[CLOSE])
    zma_s = ma(zc,5)
    zma_m = ma(zc,13)
    zfilter = zoom_in(zma_s > zma_m,len(t[CLOSE]))


def xru(stock):
    ''' 测试ru系列
        macd_ru: svma < vma*1/2
            评估:总盈亏值=2257,交易次数=37  期望值=1297     #20080601-20090602
                总盈亏率(1/1000)=2257,平均盈亏率(1/1000)=61,盈利交易率(1/1000)=540
                赢利次数=20,赢利总值=3012
                亏损次数=16,亏损总值=755
                平盘次数=1
                闭合交易明细:
            评估:总盈亏值=4074,交易次数=109 期望值=672      #20010701-20081231
                总盈亏率(1/1000)=4074,平均盈亏率(1/1000)=37,盈利交易率(1/1000)=302
                赢利次数=33,赢利总值=8249
                亏损次数=75,亏损总值=4175
        #svma<vma
            评估:总盈亏值=86328,交易次数=899        期望值=1391 #20010701-20081231
                总盈亏率(1/1000)=86328,平均盈亏率(1/1000)=96,盈利交易率(1/1000)=420
                赢利次数=378,赢利总值=122205
                亏损次数=517,亏损总值=35877
                平盘次数=4
            评估:总盈亏值=7037,交易次数=301 期望值=370  #20080601-20090602
                总盈亏率(1/1000)=7037,平均盈亏率(1/1000)=23,盈利交易率(1/1000)=431
                赢利次数=130,赢利总值=17530
                亏损次数=168,亏损总值=10493
                平盘次数=3
        #1/3-1/2
            评估:总盈亏值=2334,交易次数=34  期望值=1416
                总盈亏率(1/1000)=2334,平均盈亏率(1/1000)=68,盈利交易率(1/1000)=588
                赢利次数=20,赢利总值=3012
                亏损次数=14,亏损总值=678
                平盘次数=0
            评估:总盈亏值=3264,交易次数=86  期望值=637
                总盈亏率(1/1000)=3264,平均盈亏率(1/1000)=37,盈利交易率(1/1000)=290
                赢利次数=25,赢利总值=6757
                亏损次数=60,亏损总值=3493
                平盘次数=1
        
        #1/3-2/3
            评估:总盈亏值=5223,交易次数=113 期望值=938
                总盈亏率(1/1000)=5223,平均盈亏率(1/1000)=46,盈利交易率(1/1000)=522
                赢利次数=59,赢利总值=7907
                亏损次数=54,亏损总值=2684
        
            评估:总盈亏值=35252,交易次数=296        期望值=1750
                总盈亏率(1/1000)=35252,平均盈亏率(1/1000)=119,盈利交易率(1/1000)=405
                赢利次数=120,赢利总值=47120
                亏损次数=174,亏损总值=11868
                平盘次数=2
        #1/2-2/3
            评估:总盈亏值=33744,交易次数=217        期望值=2094
            总盈亏率(1/1000)=33744,平均盈亏率(1/1000)=155,盈利交易率(1/1000)=465
                赢利次数=101,赢利总值=42292
                亏损次数=115,亏损总值=8548
                平盘次数=1
            评估:总盈亏值=3138,交易次数=81  期望值=760
                总盈亏率(1/1000)=3138,平均盈亏率(1/1000)=38,盈利交易率(1/1000)=493
                赢利次数=40,赢利总值=5219
                亏损次数=41,亏损总值=2081
                平盘次数=0
        ru2: 1/2-2/3
            评估:总盈亏值=30198,交易次数=215        期望值=2058
                总盈亏率(1/1000)=30198,平均盈亏率(1/1000)=140,盈利交易率(1/1000)=432
                赢利次数=93,赢利总值=38520
                亏损次数=121,亏损总值=8322
                平盘次数=1
            评估:总盈亏值=4399,交易次数=73  期望值=1176
                总盈亏率(1/1000)=4399,平均盈亏率(1/1000)=60,盈利交易率(1/1000)=547
                赢利次数=40,赢利总值=6102
                亏损次数=33,亏损总值=1703
                平盘次数=0
            #svma<vma/2
            评估:总盈亏值=2416,交易次数=36  期望值=1456
                总盈亏率(1/1000)=2416,平均盈亏率(1/1000)=67,盈利交易率(1/1000)=555
                赢利次数=20,赢利总值=3071
                亏损次数=14,亏损总值=655
                平盘次数=2
                闭合交易明细:
        
            评估:总盈亏值=5029,交易次数=108 期望值=793
                总盈亏率(1/1000)=5029,平均盈亏率(1/1000)=46,盈利交易率(1/1000)=324
                赢利次数=35,赢利总值=9257
                亏损次数=72,亏损总值=4228
                平盘次数=1
            #svma: 1/3-1/2
            评估:总盈亏值=2466,交易次数=34  期望值=1565
                总盈亏率(1/1000)=2466,平均盈亏率(1/1000)=72,盈利交易率(1/1000)=588
                赢利次数=20,赢利总值=3071
                亏损次数=13,亏损总值=605
                平盘次数=1
            评估:总盈亏值=4511,交易次数=87  期望值=894
                总盈亏率(1/1000)=4511,平均盈亏率(1/1000)=51,盈利交易率(1/1000)=321
                赢利次数=28,赢利总值=7870
                亏损次数=58,亏损总值=3359
                平盘次数=1
            #1/2-1
            评估:总盈亏值=80090,交易次数=748        期望值=1528
                总盈亏率(1/1000)=80090,平均盈亏率(1/1000)=107,盈利交易率(1/1000)=438
                赢利次数=328,赢利总值=109606
                亏损次数=417,亏损总值=29516
                平盘次数=3
            评估:总盈亏值=6709,交易次数=265 期望值=390
                总盈亏率(1/1000)=6709,平均盈亏率(1/1000)=25,盈利交易率(1/1000)=433
                赢利次数=115,赢利总值=16168
                亏损次数=147,亏损总值=9459
                平盘次数=3

        ruv:    gand(svma < vma*7/8)
               评估:总盈亏值=5311,交易次数=69  期望值=1357     #20080601-20090602
                总盈亏率(1/1000)=5311,平均盈亏率(1/1000)=76,盈利交易率(1/1000)=594
                赢利次数=41,赢利总值=6889
                亏损次数=28,亏损总值=1578
               评估:总盈亏值=14747,交易次数=160        期望值=1352      #20010701-20081231
                总盈亏率(1/1000)=14747,平均盈亏率(1/1000)=92,盈利交易率(1/1000)=443
                赢利次数=71,赢利总值=20791
                亏损次数=88,亏损总值=6044
                平盘次数=1
           gand(svma < vma*2/3)                        
                评估:总盈亏值=1999,交易次数=14  期望值=3837     #20080601-20090602
                    总盈亏率(1/1000)=1999,平均盈亏率(1/1000)=142,盈利交易率(1/1000)=571
                    赢利次数=8,赢利总值=2221
                    亏损次数=6,亏损总值=222
                    平盘次数=0
                评估:总盈亏值=-36,交易次数=21   期望值=-27      #20010701-20081231
                    总盈亏率(1/1000)=-36,平均盈亏率(1/1000)=-2,盈利交易率(1/1000)=333
                    赢利次数=7,赢利总值=1021
                    亏损次数=14,亏损总值=1057
            svma: 2/3-7/8
            评估:总盈亏值=14942,交易次数=141        期望值=1567     #20010701-20081231
                总盈亏率(1/1000)=14942,平均盈亏率(1/1000)=105,盈利交易率(1/1000=460
                赢利次数=65,赢利总值=20034
                亏损次数=75,亏损总值=5092
                平盘次数=1
                    
            评估:总盈亏值=3312,交易次数=55  期望值=983       #20080601-20090602
                总盈亏率(1/1000)=3312,平均盈亏率(1/1000)=60,盈利交易率(1/1000)=600
                赢利次数=33,赢利总值=4668
                亏损次数=22,亏损总值=1356
                平盘次数=0

            svma:1/2-7/8
            评估:总盈亏值=14711,交易次数=156        期望值=1424 #20010701-20081231
                总盈亏率(1/1000)=14711,平均盈亏率(1/1000)=94,盈利交易率(1/1000)=435
                赢利次数=68,赢利总值=20533
                亏损次数=87,亏损总值=5822
                平盘次数=1
            评估:总盈亏值=5159,交易次数=68  期望值=1339     #20080601-20090602
                总盈亏率(1/1000)=5159,平均盈亏率(1/1000)=75,盈利交易率(1/1000)=588
                赢利次数=40,赢利总值=6737
                亏损次数=28,亏损总值=1578
                平盘次数=0
            1/3-7/8
            评估:总盈亏值=14854,交易次数=158        期望值=1424
                总盈亏率(1/1000)=14854,平均盈亏率(1/1000)=94,盈利交易率(1/1000)=443
                赢利次数=70,赢利总值=20676
                亏损次数=87,亏损总值=5822
                平盘次数=1
            评估:总盈亏值=5311,交易次数=69  期望值=1357
                总盈亏率(1/1000)=5311,平均盈亏率(1/1000)=76,盈利交易率(1/1000)=594
                赢利次数=41,赢利总值=6889
                亏损次数=28,亏损总值=1578
                平盘次数=0

        xc_ru2: gand(svma < vma*2/3)
            评估:总盈亏值=2680,交易次数=34  期望值=1322     #20080601-20090602
                总盈亏率(1/1000)=2680,平均盈亏率(1/1000)=78,盈利交易率(1/1000)=676
                赢利次数=23,赢利总值=3336
                亏损次数=11,亏损总值=656
                平盘次数=0
                闭合交易明细:
            评估:总盈亏值=5403,交易次数=51  期望值=1944     #20010701-20081231
                总盈亏率(1/1000)=5403,平均盈亏率(1/1000)=105,盈利交易率(1/1000)=470
                赢利次数=24,赢利总值=6863
                亏损次数=27,亏损总值=1460
                平盘次数=0
            
            1/3-2/3
            评估:总盈亏值=2653,交易次数=31  期望值=1574
                总盈亏率(1/1000)=2653,平均盈亏率(1/1000)=85,盈利交易率(1/1000)=709
                赢利次数=22,赢利总值=3141
                亏损次数=9,亏损总值=488
                平盘次数=0
            评估:总盈亏值=4952,交易次数=44  期望值=2113
                总盈亏率(1/1000)=4952,平均盈亏率(1/1000)=112,盈利交易率(1/1000)=454
                赢利次数=20,赢利总值=6236
                亏损次数=24,亏损总值=1284
                平盘次数=0
            1/2-2/3
            评估:总盈亏值=5687,交易次数=31  期望值=4066
                总盈亏率(1/1000)=5687,平均盈亏率(1/1000)=183,盈利交易率(1/1000)=612
                赢利次数=19,赢利总值=6231
                亏损次数=12,亏损总值=544
                平盘次数=0
            评估:总盈亏值=2057,交易次数=24  期望值=1700
                总盈亏率(1/1000)=2057,平均盈亏率(1/1000)=85,盈利交易率(1/1000)=708
                赢利次数=17,赢利总值=2407
                亏损次数=7,亏损总值=350
                平盘次数=0
            1/2-1
            评估:总盈亏值=3360,交易次数=97  期望值=548
                总盈亏率(1/1000)=3360,平均盈亏率(1/1000)=34,盈利交易率(1/1000)=556
                赢利次数=54,赢利总值=6056
                亏损次数=43,亏损总值=2696
                平盘次数=0
            评估:总盈亏值=26272,交易次数=207        期望值=1909
                总盈亏率(1/1000)=26272,平均盈亏率(1/1000)=126,盈利交易率(1/1000)=487
                赢利次数=101,赢利总值=33217
                亏损次数=105,亏损总值=6945
                平盘次数=1
            1/2-7/8                
            评估:总盈亏值=3070,交易次数=63  期望值=786
                总盈亏率(1/1000)=3070,平均盈亏率(1/1000)=48,盈利交易率(1/1000)=571
                赢利次数=36,赢利总值=4725
                亏损次数=27,亏损总值=1655
                平盘次数=0
            评估:总盈亏值=20889,交易次数=138        期望值=2475
                总盈亏率(1/1000)=20889,平均盈亏率(1/1000)=151,盈利交易率(1/1000)=536
                赢利次数=74,赢利总值=24761
                亏损次数=63,亏损总值=3872
                平盘次数=1

        xc_ru:  gand(svma < vma*2/3)
            评估:总盈亏值=1905,交易次数=30  期望值=1260     #20080601-20090602
                总盈亏率(1/1000)=1905,平均盈亏率(1/1000)=63,盈利交易率(1/1000)=600
                赢利次数=18,赢利总值=2457
                亏损次数=11,亏损总值=552
                平盘次数=1
            
            评估:总盈亏值=5049,交易次数=68  期望值=1013     #20010701-20081231
                总盈亏率(1/1000)=5049,平均盈亏率(1/1000)=74,盈利交易率(1/1000)=411
                赢利次数=28,赢利总值=7978
                亏损次数=40,亏损总值=2929
                平盘次数=0
            1/3-2/3
            评估:总盈亏值=1753,交易次数=28  期望值=1240
                总盈亏率(1/1000)=1753,平均盈亏率(1/1000)=62,盈利交易率(1/1000)=607
                赢利次数=17,赢利总值=2262
                亏损次数=10,亏损总值=509
                平盘次数=1
            评估:总盈亏值=4973,交易次数=57  期望值=1279
                总盈亏率(1/1000)=4973,平均盈亏率(1/1000)=87,盈利交易率(1/1000)=403
                赢利次数=23,赢利总值=7303
                亏损次数=34,亏损总值=2330
                平盘次数=0
            1/2-2/3
            评估:总盈亏值=5055,交易次数=42  期望值=1518 #20010701-20081231
                总盈亏率(1/1000)=5055,平均盈亏率(1/1000)=120,盈利交易率(1/1000)=452
                赢利次数=19,赢利总值=6889
                亏损次数=23,亏损总值=1834
                平盘次数=0
            
            评估:总盈亏值=591,交易次数=19   期望值=632  #20080601-20090601
                总盈亏率(1/1000)=591,平均盈亏率(1/1000)=31,盈利交易率(1/1000)=421
                赢利次数=8,赢利总值=1082
                亏损次数=10,亏损总值=491
                平盘次数=1
            1/3-1/2
            评估:总盈亏值=1187,交易次数=10  期望值=4538 #20080601-20090601
                总盈亏率(1/1000)=1187,平均盈亏率(1/1000)=118,盈利交易率(1/1000)=900
                赢利次数=9,赢利总值=1213
                亏损次数=1,亏损总值=26
                平盘次数=0
                闭合交易明细:
            
            评估:总盈亏值=-82,交易次数=15   期望值=-134 #20010701-20081231
                总盈亏率(1/1000)=-82,平均盈亏率(1/1000)=-6,盈利交易率(1/1000)=266
                赢利次数=4,赢利总值=414
                亏损次数=11,亏损总值=496
                平盘次数=0
            
        
    '''
    t = stock.transaction
    #mdiff,mdea = macd_ru2(t[OPEN],t[CLOSE],t[HIGH],t[LOW])
    #mxc = cross(mdea,mdiff) > 0
    mxc = xc_ru(t[OPEN],t[CLOSE],t[HIGH],t[LOW],t[VOLUME]) > 0
    

    vma = ma(t[VOLUME],30)
    svma = ma(t[VOLUME],3)

    vfilter = gand(svma>vma*1/3,svma<vma*1/2)

    signal = gand(mxc,vfilter,stock.thumb,stock.above,strend(stock.ma60)>0,stock.t120)
    linelog(stock.code)
    return signal



def attack(stock,dates):
    linelog(stock.code)
    t = stock.transaction
    o,c,h,l = t[OPEN],t[CLOSE],t[HIGH],t[LOW]
    ldown = lesser(l,rollx(l))
    ldown2 = equals(ldown + rollx(ldown),2)
    hdown = lesser(h,rollx(h))
    hdown2 = equals(hdown + rollx(hdown),2)
    cl = lesser(c,rollx(l))   #收盘小于昨天最低
    sprepare = gand(ldown2,hdown2,cl)
    ch = greater(c,rollx(h))  #收盘大于昨天最高
    signal = band(rollx(sprepare),ch) #连续两天下跌之后，第三天收盘超过昨日最高
    sbuy = gand(signal,stock.golden,stock.above,stock.t120)
    return sbuy

def macd3(stock,dates):
    linelog(stock.code)
    t = stock.transaction
    pdiff,pdea = cmacd(t[CLOSE])
    ds = strend(pdea) - 3
    base = cached_zeros(len(t[CLOSE]))
    x = greater(cross(base,ds))
    signal = gand(x,stock.thumb,stock.silver,stock.above,stock.t120)
    return signal

def spring(stock):
    threshold = -30
    t = stock.transaction
    linelog('spring:%s' % stock.code)
    
    s11 = gand(stock.ks >=-5,stock.ks<0,stock.ref.ks<=threshold)
    s12 = gand(stock.ks >=5,stock.ks<20,stock.ref.ks<=threshold)
    s1 = bor(s11,s12)
    s_tt = gand(s1,stock.thumb,stock.t120)
    s21 = gand(stock.ks>=5,stock.ks<75,stock.ref.ks<=threshold)
    s_aa = gand(s21,stock.thumb,stock.above)

    signals = bor(s_aa,s_tt)

    svap,v2i = stock.svap_ma_67
    sdiff,sdea = cmacd(svap,19,39)
    ssignal = gand(strend(sdiff)>0,strend(sdiff-sdea)>0)

    msvap = transform(ssignal,v2i,len(t[VOLUME]))

    ref = stock.ref
    sbuy = signals #gand(signals,greater(ref.ma10,ref.ma20),greater(ref.ma20,ref.ma60))

    zc = pzoom_out(t[CLOSE])
    zma_s = ma(zc,5)
    zma_m = ma(zc,13)
    zfilter = zoom_in(zma_s > zma_m,len(t[CLOSE]))


    return gand(sbuy,msvap,zfilter)

def spring2(stock,dates):
    ''' 
        大盘跌幅从最高点开始度量
        t=idata[1].transaction
        rc = rollx(t[CLOSE])
        lhigh = np.select([rc>t[HIGH],rc<=t[HIGH]],[rc,t[HIGH]])
        ks = (t[CLOSE]-lhigh) * BASE / lhigh
        idata[1].ks2 = ks
        效果不如spring
    '''
    threshold=-30
    t = stock.transaction
    linelog('spring:%s' % stock.code)
    
    s11 = gand(stock.ks >=-5,stock.ks<0,stock.ref.ks2<=threshold)
    s12 = gand(stock.ks >=5,stock.ks<20,stock.ref.ks2<=threshold)
    s1 = bor(s11,s12)
    s_tt = gand(s1,stock.thumb,stock.t120)
    s21 = gand(stock.ks>=5,stock.ks<75,stock.ref.ks2<=threshold)
    s_aa = gand(s21,stock.thumb,stock.above)

    signals = bor(s_aa,s_tt)

    ref = stock.ref
    sbuy = gand(signals,greater(ref.ma10,ref.ma20),greater(ref.ma20,ref.ma60))

    return sbuy


def ctest(stock,dates):
    fast,mid,slow,rstart,rend = 33,5,40,2000,4500
    ma_standard=500
    extend_days=10
    sma=55
    linelog('ctest:%s' % stock.code)
    t = stock.transaction

    if rstart >= rend:
        return np.zeros_like(t[CLOSE])

    try:
        stock.catalog
    except:
        return np.zeros_like(t[CLOSE])

    c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s>=rstart,s<=rend)

    #print stock.code,len(t[CLOSE]),sum(t[CLOSE])
    skey = 'svap_ma_%s' % sma
    if not stock.has_attr(skey): #加速
        stock.set_attr(skey,svap_ma(t[VOLUME],t[CLOSE],sma))
    svap,v2i = stock.get_attr(skey)
    
    ma_svapfast = ma(svap,fast)
    ma_svapmid = ma(svap,mid)    
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapmid = strend(ma_svapmid) > 0    
    trend_ma_svapslow = strend(ma_svapslow) > 0
    
    #ma_standard = ma(svap,ma_standard)
    #trend_ma_standard = strend(ma_standard) > 0    
    mskey = 'svap_ma_%s_%s' % (sma,ma_standard)
    if not stock.has_attr(mskey):
        ma_standard = ma(svap,ma_standard)
        trend_ma_standard = strend(ma_standard) > 0    
        stock.set_attr(mskey,trend_ma_standard)
    trend_ma_standard = stock.get_attr(mskey)

    #cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    cross_fast_mid = band(cross(ma_svapmid,ma_svapfast)>0,trend_ma_svapfast)
    cross_fast_slow = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast)    
    cross_mid_slow = band(cross(ma_svapslow,ma_svapmid)>0,trend_ma_svapmid)
    sync_fast_2 = sfollow(cross_fast_mid,cross_fast_slow,extend_days)
    sync3 = sfollow(sync_fast_2,cross_mid_slow,extend_days)
    vsignal = band(sync3,trend_ma_standard)
    msvap = transform(vsignal,v2i,len(t[VOLUME]))

    cs = catalog_signal_cs(stock.c60,c_extractor)
    g = gand(stock.g20 >= stock.g60+1000,stock.g60 >= stock.g120+1000,stock.g20-stock.g60>=stock.g60-stock.g120,stock.g20>=3000,stock.g20<=8000)

    if not stock.has_attr('ma'):
        ma10 = ma(t[CLOSE],10)
        ma20 = ma(t[CLOSE],20)
        ma60 = ma(t[CLOSE],60)
        ma120 = ma(t[CLOSE],120)
        t120 = strend(ma120)>0
        ma_above = gand(greater(ma10,ma20),greater(ma20,ma60),greater(ma60,ma120))        
        stock.set_attr('ma',{'10':ma10,'20':ma20,'60':ma60,'120':ma120,'t120':t120,'above':ma_above})
    t120,ma_above = stock.ma['t120'],stock.ma['above']
    
    return gand(cs,g,msvap,ma_above)


#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s>=3300,s<=6600)

#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=6600)

#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,s<=6600)

#c_extractor = lambda c,s:gand(c.g5 >= c.g20+500,c.g20>=c.g60+500,c.g60>=c.g120+500,c.g120>=c.g250+500)

def smacd(stock):
    '''
        36,78
        评估:总盈亏值=45847,交易次数=379        期望值=1643
                总盈亏率(1/1000)=45847,平均盈亏率(1/1000)=120,盈利交易率(1/1000)=448
                赢利次数=170,赢利总值=61166
                亏损次数=209,亏损总值=15319
                平盘次数=0
    
        36,78,     vfilter = vma_s < vma_l 
        评估:总盈亏值=22086,交易次数=126        期望值=2302
                总盈亏率(1/1000)=22086,平均盈亏率(1/1000)=175,盈利交易率(1/1000)=539
                赢利次数=68,赢利总值=26550
                亏损次数=58,亏损总值=4464
                平盘次数=0
            #20080701-20090531:
            评估:总盈亏值=811,交易次数=63   期望值=214
                总盈亏率(1/1000)=811,平均盈亏率(1/1000)=12,盈利交易率(1/1000)=396
                赢利次数=25,赢利总值=2976
                亏损次数=38,亏损总值=2165
                平盘次数=0
            
        36,78,     vfilter = vma_s < vma_l * 7/8
        评估:总盈亏值=8997,交易次数=45  期望值=2618
                总盈亏率(1/1000)=8997,平均盈亏率(1/1000)=199,盈利交易率(1/1000)=511
                赢利次数=23,赢利总值=10690
                亏损次数=22,亏损总值=1693
                平盘次数=0
                闭合交易明细:
            #20080701-20090531:
                评估:总盈亏值=1067,交易次数=20  期望值=1060
                总盈亏率(1/1000)=1067,平均盈亏率(1/1000)=53,盈利交易率(1/1000)=600
                赢利次数=12,赢利总值=1470
                亏损次数=8,亏损总值=403
                平盘次数=0

        #默认参数和19,39都不是很好
    '''
    t = stock.transaction
    g = gand(stock.g20 >= stock.g60+1000,stock.g60 >= stock.g120+1000,stock.g20>=3000,stock.g20<=8000)
    #g = np.ones_like(stock.g5)
 
    svap,v2i = stock.svap_ma_67 

    diff,dea = cmacd(svap,36,78)
    dcross = gand(cross(dea,diff)>0,strend(diff)>0,strend(dea)>0)

    msvap = transform(dcross,v2i,len(t[VOLUME]))

    linelog(stock.code)
    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = vma_s < vma_l * 7/8

    return gand(stock.golden,stock.above,msvap,vfilter)


#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=6600)
def tsvama2(stock):
    ''' svama两线交叉
    '''
    fast=20
    slow=170
    t = stock.transaction
    svap,v2i = stock.svap_ma_67 
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)

    sdiff,sdea = cmacd(svap)
    ss = gand(cross_fast_slow,strend(sdiff-sdea)>0)
    #ss = cross_fast_slow
    msvap = transform(ss,v2i,len(t[VOLUME]))
    linelog('%s:%s' % (tsvama2.__name__,stock.code))

    vdiff,vdea = cmacd(t[VOLUME])

    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = vma_s < vma_l * 7/8
 
    linelog('%s:%s' % (tsvama2.__name__,stock.code))
    return gand(stock.golden,msvap,stock.above,vfilter)

def gcs(stock,dates):
    t = stock.transaction
    linelog(stock.code)
    s = stock
    #g = gand(s.g20 >= s.g120+2000,s.g120 >= s.g60,s.g20>=3000,s.g20<=8000)
    #g = gand(s.g20 >= s.g60+1000,s.g60 >= s.g120+1000,s.g120 >= s.g250,s.g120>=1000,s.g20<=2*s.g60,s.g60<=2*s.g120,s.g20>=3000,s.g20<=8000)
    #g = gand(s.g20 >= s.g60,s.g20 <= s.g60+500,s.g60 >= s.g120,s.g60>=s.g120+500,s.g120>=s.g250+500,s.g250>=1000,s.g20<=8000)
    #silver2 = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250)    
    #cs = catalog_signal_cs(stock.c60,stock.silver)
    #ks = np.abs((s.g20-s.g60) * 1000/(s.g60-s.g120))
    g = gand(s.g20 >= s.g60,s.g60 >= s.g120,s.g20>=3000,s.g20<=8000,s.g20<=s.g120+1000) 

    pdiff,pdea = cmacd(t[CLOSE])

    #ma5=ma(t[CLOSE],5)
    #signals = gand(stock.golden,stock.silver,stock.above,ma5>stock.ma10,stock.ref.t120)
    #signals = gand(g,stock.silver,stock.above,ma5>stock.ma10,stock.ref.t120)
    #signals = gand(g,stock.above,stock.ref.t120)
    #signals = gand(stock.golden,stock.ref.t120,strend(stock.ref.ma60)>0,strend(stock.ref.ma20)>0,strend(ma(stock.ref.transaction[CLOSE],250))>0)
    #signals = gand(g,stock.ref.t120,strend(stock.ref.ma60)>0,strend(stock.ref.ma20)>0,strend(ma(stock.ref.transaction[CLOSE],250))>0)
    signals = gand(g,pdiff>=300,pdiff<=600,stock.above,stock.ref.t120,strend(stock.ma20)>0,strend(stock.ma60)>0,stock.t120,stock.ref.above)

    #signals = gand(stock.golden,cs,stock.t120)
    #signals = gand(g,stock.above)
    #sbuy = derepeatc(signals)
    sbuy = signals
    gcs.sum += np.sum(sbuy)
    gcs.total += np.sum(t[VOLUME]>0)
    return sbuy

gcs.sum=0
gcs.total = 0


def xgcs(stock):
    '''
    '''
    t = stock.transaction
    ma5 = ma(t[CLOSE],5)
    linelog(stock.code)

    si = score2(t[CLOSE],t[VOLUME])
    mxi = gand(msum(si,5)>=-100,msum(si,5)<=0)

    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = gand(vma_s > vma_l * 3/2)

    sbuy = gand(stock.golden,stock.silver,stock.above,ma5>stock.ma10,stock.ref.t120,mxi,vfilter)

    return sbuy


def xgcsx(stock,dates):
    '''
    '''
    t = stock.transaction
    ma5 = ma(t[CLOSE],5)
    linelog(stock.code)

    si = score2(t[CLOSE],t[VOLUME])
    mxi = gand(msum(si,5)>=-100,msum(si,5)<=0)

    signal = gand(stock.golden,stock.silver,stock.above,ma5>stock.ma10,stock.ref.t120,mxi)

    sbuy = sfollow(signal,x30(t),10)
    
    return sbuy


def xgcs0(stock):
    ''' 下穿0线
        评估:总盈亏值=23464,交易次数=81 期望值=4013
                总盈亏率(1/1000)=23464,平均盈亏率(1/1000)=289,盈利交易率(1/1000)=617
                赢利次数=50,赢利总值=25703
                亏损次数=31,亏损总值=2239
                平盘次数=0
    '''
    t = stock.transaction
    ma5 = ma(t[CLOSE],5)
    linelog(stock.code)

    si = score2(t[CLOSE],t[VOLUME])
    #mxi = gand(msum(si,5)>=-100,msum(si,5)<=0)
    z1 = np.ones_like(t[CLOSE])
    z1 = z1-3
    mxi = cross(z1,si)<0

    sbuy = gand(stock.golden,stock.silver,stock.above,ma5>stock.ma10,stock.ref.t120,mxi)
    return sbuy

def xgcs0x(stock):
    ''' 下穿0线
        评估:总盈亏值=23464,交易次数=81 期望值=4013
                总盈亏率(1/1000)=23464,平均盈亏率(1/1000)=289,盈利交易率(1/1000)=617
                赢利次数=50,赢利总值=25703
                亏损次数=31,亏损总值=2239
                平盘次数=0
    '''
    t = stock.transaction
    ma5 = ma(t[CLOSE],5)
    linelog(stock.code)

    si = score2(t[CLOSE],t[VOLUME])
    zs = cached_zeros(len(t[CLOSE]))
    mxi = cross(zs,si)<0

    signal = gand(stock.golden,stock.silver,stock.above,ma5>stock.ma10,stock.ref.t120,mxi)
    
    #sbuy = signal
    sbuy= gand(sfollow(signal,x30(t),5),stock.above)
    return sbuy


def xgcs5(stock,dates):
    '''
    
    '''
    t = stock.transaction
    ma5 = ma(t[CLOSE],5)
    linelog(stock.code)

    si = score2(t[CLOSE],t[VOLUME])
    zs = cached_zeros(len(t[CLOSE]))
    mxi = cross(zs,si)<0
    
    s = stock
    g = gand(s.g20 >= s.g60,s.g20 <= s.g60+500,s.g60 >= s.g120,s.g60<=s.g120+500,s.g120>=s.g250+500,s.g250>=1000,s.g20<=8000)

    #sbuy = gand(stock.golden,stock.silver,stock.above,ma5>stock.ma10,stock.ref.t120,mxi)
    #sbuy = gand(g,stock.above,stock.ref.t120,mxi)
    signals = gand(g,mxi,stock.ref.above,stock.ref.t120,strend(stock.ref.ma60)>0,strend(stock.ref.ma10)>0,strend(stock.ref.ma20)>0,strend(ma(stock.ref.transaction[CLOSE],250))>0)
    
    sbuy = signals
    return sbuy


def pmacd(stock,dates):
    t = stock.transaction
    pdiff,pdea = cmacd(t[VOLUME])
    dcross = gand(cross(pdea,pdiff),strend(pdiff)>0,strend(pdea>0))
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    linelog(stock.code)
    
    if not stock.has_attr('ma'):
        ma10 = ma(t[CLOSE],10)
        ma20 = ma(t[CLOSE],20)
        ma60 = ma(t[CLOSE],60)
        ma120 = ma(t[CLOSE],120)
        t120 = strend(ma120)>0
        ma_above = gand(greater(ma10,ma20),greater(ma20,ma60),greater(ma60,ma120))        
        stock.set_attr('ma',{'10':ma10,'20':ma20,'60':ma60,'120':ma120,'t120':t120,'above':ma_above})
    t120,ma_above = stock.ma['t120'],stock.ma['above']
    ma20,ma60,ma120 = stock.ma['20'],stock.ma['60'],stock.ma['120']
    
    cs = catalog_signal_cs(stock.c60,c_extractor)

    #return dcross
    #return gand(dcross,g,trend_ma_standard)
    return gand(dcross,g,ma_above,cs,pdea>0,pdea<12000)


def nhigh(stock,dates):#60高点
    linelog(stock.code)
    t = stock.transaction
    mline = rollx(tmax(t[CLOSE],60)) #以昨日的60高点为准
    dcross = cross(mline,t[CLOSE])>0    
    g = gand(stock.g5>=stock.g20,stock.thumb)
    #linelog(stock.code)
    return gand(g,stock.silver,dcross,strend(stock.ma60)>0,stock.above,stock.t120)

def shigh(stock,dates,sector=HIGH):
    linelog(stock.code)
    t = stock.transaction
    #mline = rollx(tmax(t[HIGH],60)) #以昨日的60高点为准
    #nh = greater(t[HIGH],mline)
    mline = rollx(tmax(t[HIGH],67)) #以昨日的60高点为准
    nh = greater(t[sector],mline)
    stock.shigh = nh
    #stock.v = greater(t[VOLUME])

def slow(stock,dates):
    linelog(stock.code)
    t = stock.transaction
    #mline = rollx(tmax(t[HIGH],60)) #以昨日的60高点为准
    #nh = greater(t[HIGH],mline)
    mline = rollx(tmin(t[LOW],67)) #以昨日的60高点为准
    nl = lesser(t[LOW],mline)
    stock.slow = nl
    #stock.v = greater(t[VOLUME])

def ma3(stock,dates):
    ''' ma三线金叉
        不要求最慢的那条线在被快线交叉时趋势必须向上，但要求被中线交叉时趋势向上
    '''
    ma_standard=120
    extend_days = 10    
    #logger.debug('ma3 calc: %s ' % stock.code)    
    t = stock.transaction
    #g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    #g对这个没效果
    fast,mid,slow=5,10,20
    ma_fast = ma(t[CLOSE],fast)
    ma_mid = ma(t[CLOSE],mid)
    ma_slow = ma(t[CLOSE],slow)
    trend_fast = strend(ma_fast) > 0
    trend_mid = strend(ma_mid) > 0    
    trend_slow = strend(ma_slow) > 0
    cross_fast_mid = band(cross(ma_mid,ma_fast)>0,trend_mid)
    cross_fast_slow = band(cross(ma_slow,ma_fast)>0,trend_fast)
    cross_mid_slow = band(cross(ma_slow,ma_mid)>0,trend_mid)
    cross_fm_fs = sfollow(cross_fast_mid,cross_fast_slow,extend_days)
    confirm_cross = sfollow(cross_fm_fs,cross_mid_slow,extend_days)
    trend_ma_standard = strend(ma(t[CLOSE],ma_standard)) > 0
    linelog(stock.code)
    #cs = catalog_signal_cs(stock.c60,c_extractor)
    
    return gand(trend_ma_standard,confirm_cross)

#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=6600)
def xma60(stock,dates):

    t = stock.transaction
    water_line = stock.ma60*115/100   #上方15处
    dcross = cross(water_line,t[LOW])
    up_cross = dcross > 0
    down_cross = dcross < 0
    sync = sfollow(down_cross,up_cross,7)
    linelog(stock.code)
    s = stock
    #return gand(sync,stock.above,stock.t120,stock.golden,cs)    
    return gand(sync,stock.above,stock.t120,stock.thumb,stock.silver)


def x30(t):
    water_line = ma(t[CLOSE],30)
    dcross = cross(water_line,t[LOW])
    up_cross = dcross > 0
    down_cross = dcross < 0
    sync = sfollow(down_cross,up_cross,7)
    return sync


def tsvama2x(stock,dates):
    ''' svama两线交叉
    '''
    fast=20
    slow=100
    t = stock.transaction
    g = stock.golden
    svap,v2i = stock.svap_ma_67
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))
    signal = msvap
    s2 = x30(t)
    sbuy = sfollow(signal,s2,10)
    linelog('%s:%s' % (tsvama2x.__name__,stock.code))
    return gand(sbuy,stock.above,stock.thumb,stock.silver)

def xma30(stock,dates):
    t = stock.transaction
    water_line = ma(t[CLOSE],30)
    dcross = cross(water_line,t[LOW])
    up_cross = dcross > 0
    down_cross = dcross < 0
    sync = sfollow(down_cross,up_cross,10)
    linelog(stock.code)
    s = stock
    #return gand(sync,stock.above,stock.t120,stock.golden,cs)    
    g = gand(s.g20 >= s.g60,s.g20 <= s.g60+500,s.g60 >= s.g120,s.g60<=s.g120+500,s.g120>=s.g250+500,s.g250>=1000,s.g20<=8000)

    return gand(sync,stock.above,stock.t120,g)


def cma2(stock,dates):  #传统的ma2
    t = stock.transaction
    #water_line = stock.ma20  #上方15处,这个位置起始有点远，但居然起作用
    water_line = ma(t[CLOSE],20)
    dcross = cross(water_line,ma(t[CLOSE],5))

    up_cross = dcross > 0
    down_cross = dcross < 0

    sync = up_cross
    linelog(stock.code)
    return gand(sync,stock.above,stock.t120,stock.g5>=stock.g20+500,stock.g20>=stock.g60+500,stock.g60>=stock.g120,stock.g5>4000,stock.g5<8000)


def cma_30(stock):  #
    t = stock.transaction
    
    water_line = ma(t[CLOSE],30)
    dcross = cross(water_line,t[LOW])
    up_cross = dcross > 0
    down_cross = dcross < 0
    sync = sfollow(down_cross,up_cross,7)
    return gand(sync,stock.above,stock.t120,stock.thumb,stock.silver)


def cma2x(stock,dates):  #传统的ma2
    t = stock.transaction
    water_line = ma(t[CLOSE],20)
    dcross = cross(water_line,ma(t[CLOSE],5))

    up_cross = dcross > 0
    down_cross = dcross < 0

    sync = up_cross
    linelog(stock.code)

    s=stock
    g = gand(s.g20 >= s.g60,s.g20 <= s.g60+500,s.g60 >= s.g120,s.g60<=s.g120+500,s.g120>=s.g250+500,s.g250>=1000,s.g20<=8000)

    return gand(sync,g,stock.g5>=stock.g20+500,stock.above,stock.t120)


def wvad(stock,dates):
    t = stock.transaction
    
    vad = (t[CLOSE]-t[OPEN])*t[VOLUME]/(t[HIGH]-t[LOW]) / 10000
    svad = msum2(vad,24)
    ma_svad = ma(svad,6)

    ecross = gand(stock.thumb,stock.silver,cross(ma_svad,vad)>0,strend(ma_svad)>0,stock.t120,stock.above)
    linelog(stock.code)
    sbuy = sfollow(ecross,x30(t),10)

    return sbuy


import wolfox.fengine.core.d1indicator as d1in
#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=6600)
def temv(stock,dates):
    t = stock.transaction
    ts = cached_zeros(len(t[CLOSE]))
    ekey = 'emv'
    em = d1in.emv(t[HIGH],t[LOW],t[VOLUME])
    mv = msum2(em,14)
    ssemv = ma(mv,9)
    ecross = gand(stock.golden,cross(ts,mv)>0,strend(ssemv)>0,stock.t120,stock.above)
    sbuy = ecross   #sfollow(ecross,x30(t),10)
    linelog(stock.code)
    return sbuy

def vmacd_ma4(stock,dates):
    t = stock.transaction
    
    vdiff,vdea = cmacd(t[VOLUME])
    dcross = gand(cross(vdea,vdiff)>0,strend(vdiff)>0,strend(vdea)>0)

    #g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    g = gand(stock.g20>=7500,stock.g60>=7500)

    c_ex = lambda c,s:gand(c.g20>=7500,s>=8000)
    cs = catalog_signal_cs(stock.c60,c_ex)    
    return gand(g,cs,dcross,stock.above,strend(stock.ma60)>0,vdea>=0,vdea<=12000)

def gcx(stock,dates):
    t = stock.transaction
    
    #g = gand(stock.g60>=8000)
    gma = ma(stock.g60,5)
    waterline = cached_ints(len(t[CLOSE]),6000)
    xs = cross(waterline,gma) 
    #xs = extend2next(xs)

    ll5 = rollx(t[LOW],3)
    hinc = t[HIGH] * 1000 / ll5

    #c_ex = lambda c,s:gand(c.g20>=7500,s>=8000)
    #cs = catalog_signal_cs(stock.c60,c_ex)    
    cx = stock.c60.keys()[1].g60
    cma = ma(cx,3)
    xc = cma > 6000
    xc = extend2next(xc) > 0
    #signal = derepeatc(gand(xs>0,xc>0))
    #print signal
    return gand(xs>0,xc>0,stock.c60.values()[1]>8500,stock.above,stock.t120,hinc<1200)

def gmacd_old(stock): #这里dea,diff是全反的,但是全反居然收益很好，成功率不错。晕倒
    t = stock.transaction
    
    mdea,mdiff = cmacd(stock.g60)
    ldea,ldiff = cmacd(stock.g120)
    lldea,lldiff = cmacd(stock.g250)

    vdea,vdiff = cmacd(t[VOLUME])
    pdea,pdiff = cmacd(t[CLOSE])

    sfilter = gand(vdiff>vdea,pdiff>pdea)

    xcross = cross(mdea,mdiff) > 0

    linelog(stock.code)

    ll5 = rollx(t[LOW],5)
    hinc = t[HIGH] * 1000 / ll5

    ll10 = rollx(t[LOW],10)
    hh10 = tmax(t[HIGH],10)
    rhl10 = hh10 * 1000/ll10

    ss = sfollow(xcross,sfilter,5)

    signal = gand(ss,stock.above,stock.t120,t[VOLUME]>0,hinc<1200,rhl10<1500,stock.g60>4500)
    return signal
    #410/498/1584
    #全部750/520
    #需要测试中国软件/浪潮软件/000961
    #return gand(xcross,stock.above,stock.t120,t[VOLUME]>0,stock.g60>4500,stock.g60<7500)   #94-392


def gmacd_s(stock): #
    ''' 
        ll5 = rollx(t[LOW],5),   hinc = t[HIGH] * 1000 / ll5
        ll10 = rollx(t[LOW],10),    hh10 = tmax(t[HIGH],10), rhl10 = hh10 * 1000/ll10
        lfilter = hinc<1200 and rhl10<1500
        ss1=sfollow(cross(mdea,mdiff) > 0,vdiff<vdea), 然后再sfollow(ss1,cross(ma(t[CLOSE],30),t[LOW]),5),之后+lfilter,2115/704/846
        ss1=sfollow(cross(mdea,mdiff) > 0,vdiff<vdea), 然后再sfollow(ss1,cross(ma(t[CLOSE],30)<0,t[LOW]),5),之后+lfilter,2213/759/595
            g60:4500-8500:  2946/821/286
        ss1=sfollow(cross(mdea,mdiff) > 0,vdiff<vdea), 然后再sfollow(ss1,cross(ma(t[CLOSE],30)<0,t[LOW]),10),之后+lfilter,2392/746/844    
            g60:0-3000:1457/670/273
            g60:3000-6000: 2709/788/402
            g60:6000-!: 2696/758/273
            g60:6000-8500: 2781/775/232
            g60:>8500:  2193/632/49
            g60:4500-8500:  3078/793/411
            g60:4500-7500:  2888/797/345
            g60:5000-8000:  2925/796/324
            数量太多,需要进一步筛选
        ss1=sfollow(cross(mdea,mdiff) > 0,gand(vdiff>vdea,pdiff>pdea)), 然后再sfollow(ss1,cross(ma(t[CLOSE],30)<0,t[LOW]),10),2392/746/844    
            g60:4500-8500:3036/800/451
            g20:4500-8500:3886/817/465  #不需要hinc<1200，只需要rhl10<1500,而且效果也有限
            但这个滤掉了600121,600756,000961,600997等
        
        仍然无法继续甄别超级强势股,如600756,000961的启动阶段,能够通过cmacd(mdea,mdiff)>0找到初始信号,但无法从噪声中甄别出来
        因为他们不触碰30线,需要进一步考虑
        ss1不变.
        x3 = gand(strend(ma(t[CLOSE],5))>0,strend(stock.ma10)>0,strend(stock.ma20)>0,strend(stock.ma60)>0)
        ss = sfollow(ss1,x3,10)
        
    '''
    t = stock.transaction
    
    mdiff,mdea = cmacd(stock.g60)
    ldiff,ldea = cmacd(stock.g120)
    lldiff,lldea = cmacd(stock.g250)

    vdiff,vdea = cmacd(t[VOLUME])
    pdiff,pdea = cmacd(t[CLOSE])


    #sfilter = vdiff<vdea
    #sfilter = vdiff<vdea
    sfilter = gand(vdiff>vdea,pdiff>pdea)

    xcross = cross(mdea,mdiff) > 0  
    #xcross = cross(mdiff,mdea) > 0  

    linelog(stock.code)

    ll5 = rollx(t[LOW],5)
    hinc = t[HIGH] * 1000 / ll5

    ll10 = rollx(t[LOW],10)
    hh10 = tmax(t[HIGH],10)
    rhl10 = hh10 * 1000/ll10

    ss1 = sfollow(xcross,sfilter,5)
    #ss = derepeatc(ss)
    
    x2 = cross(ma(t[CLOSE],30),t[LOW]) < 0

    ss = sfollow(ss1,x2,10)

    gf1 = gand(stock.g20>4500,stock.g20<8500)
    gf2 = gand(stock.g60>4500,stock.g60<8500)
    gfilter = bor(gf1,gf2)


    #signal = gand(xcross,stock.above,stock.t120,t[VOLUME]>0,hinc<1200,rhl10<1500,gfilter)
    signal = gand(ss,stock.above,stock.t120,t[VOLUME]>0,gf1,rhl10<1500)
    
    return signal


def gmacd(stock): #
    '''
    #之前
                评估:总盈亏值=6850,交易次数=115 期望值=842
                总盈亏率(1/1000)=6850,平均盈亏率(1/1000)=59,盈利交易率(1/1000)=330
                赢利次数=38,赢利总值=12295
                亏损次数=77,亏损总值=5445
                平盘次数=0
            
                评估:总盈亏值=7564,交易次数=34  期望值=5045
                总盈亏率(1/1000)=7564,平均盈亏率(1/1000)=222,盈利交易率(1/1000)=911
                赢利次数=31,赢利总值=7698
                亏损次数=3,亏损总值=134
                平盘次数=0
    
    去掉msvap
        评估:总盈亏值=10402,交易次数=43 期望值=6025
                总盈亏率(1/1000)=10402,平均盈亏率(1/1000)=241,盈利交易率(1/1000)=930
                赢利次数=40,赢利总值=10523
                亏损次数=3,亏损总值=121
                平盘次数=0
        评估:总盈亏值=11803,交易次数=226        期望值=764
                总盈亏率(1/1000)=11803,平均盈亏率(1/1000)=52,盈利交易率(1/1000)=305
                赢利次数=69,赢利总值=22487
                亏损次数=157,亏损总值=10684
                平盘次数=0
        不妥
    '''
    t = stock.transaction
    
    #mdiff,mdea = cmacd(stock.g5)   
    mdiff,mdea = cmacd(ma(stock.g60,5)) #平滑以去掉首尾效应


    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = gand(vma_s > vma_l * 4/3)
    
    xcross = cross(mdea,mdiff) > 0

    linelog(stock.code)

    ll10 = rollx(t[LOW],10)
    hh10 = tmax(t[HIGH],10)
    rhl10 = hh10 * 1000/ll10

    c = t[CLOSE]
    ma30 = ma(c,30)
    above = gand(ma(c,13) > ma30,ma30>stock.ma60,stock.ma60>stock.ma120)


    #svap,v2i = stock.svap_ma_67
    #sdiff,sdea = cmacd(svap,36,78)
    #ssignal = gand(sdiff < sdea,strend(sdiff)<0,strend(sdiff-sdea)>0)

    #msvap = transform(ssignal,v2i,len(t[VOLUME]))

    x2 = cross(ma(t[CLOSE],30),t[LOW]) < 0

    ss = sfollow(xcross,x2,10)
    
    gf1 = gand(stock.g20>5000,stock.g20<9500)

    si = score2(t[CLOSE],t[VOLUME])
    msi = msum(si,5)
    mxi = gand(msi>=-100,msi<=0)
    
    #signal = gand(ss,above,stock.t120,strend(stock.ma60)>0,t[VOLUME]>0,gf1,rhl10<1500,mdiff>=mdea,strend(stock.ref.ma60)>0,vfilter,msvap,mxi)
    signal = gand(ss,above,stock.t120,strend(stock.ma60)>0,t[VOLUME]>0,gf1,rhl10<1500,mdiff>=mdea,strend(stock.ref.ma60)>0,vfilter,mxi)

    return signal


def gmacd5(stock): #
    '''
                gf1 = gand(stock.g20>5000,stock.g20<9500)
                #使用g5,ma3
                评估:总盈亏值=5437,交易次数=19  期望值=71500
                    总盈亏率(1/1000)=5437,平均盈亏率(1/1000)=286,盈利交易率(1/1000)=947
                赢利次数=18,赢利总值=5441
                亏损次数=1,亏损总值=4

                评估:总盈亏值=6564,交易次数=68  期望值=1333 #20010701-20081231
                总盈亏率(1/1000)=6564,平均盈亏率(1/1000)=96,盈利交易率(1/1000)=397
                赢利次数=27,赢利总值=9476
                亏损次数=40,亏损总值=2912
                平盘次数=1

            ma5:
                评估:总盈亏值=5764,交易次数=23  期望值=10000
                总盈亏率(1/1000)=5764,平均盈亏率(1/1000)=250,盈利交易率(1/1000)=869
                赢利次数=20,赢利总值=5841
                亏损次数=3,亏损总值=77
                平盘次数=0
    
                评估:总盈亏值=6049,交易次数=84  期望值=888
                总盈亏率(1/1000)=6049,平均盈亏率(1/1000)=72,盈利交易率(1/1000)=357
                赢利次数=30,赢利总值=10372
                亏损次数=53,亏损总值=4323
                平盘次数=1
            直接计算:       #近期表现绝对彪悍
                评估:总盈亏值=3970,交易次数=14  期望值=1000
                总盈亏率(1/1000)=3970,平均盈亏率(1/1000)=283,盈利交易率(1/1000)=1000
                赢利次数=14,赢利总值=3970
                亏损次数=0,亏损总值=0
                平盘次数=0
                
            评估:总盈亏值=3132,交易次数=33  期望值=1146     #20010701-20081231
                总盈亏率(1/1000)=3132,平均盈亏率(1/1000)=94,盈利交易率(1/1000)=424
                赢利次数=14,赢利总值=4701
                亏损次数=19,亏损总值=1569
                平盘次数=0

                msvap+g60>1000,g20>2000:
                    评估:总盈亏值=6642,交易次数=55  期望值=1666
                    总盈亏率(1/1000)=6642,平均盈亏率(1/1000)=120,盈利交易率(1/1000)=381
                    赢利次数=21,赢利总值=9121
                    亏损次数=34,亏损总值=2479
                    平盘次数=0

                    评估:总盈亏值=4840,交易次数=18  期望值=1000
                    总盈亏率(1/1000)=4840,平均盈亏率(1/1000)=268,盈利交易率(1/1000)=1000
                    赢利次数=18,赢利总值=4840
                    亏损次数=0,亏损总值=0
                    平盘次数=0
                
            去掉msvap:  
                评估:总盈亏值=6936,交易次数=24  期望值=13136
                    总盈亏率(1/1000)=6936,平均盈亏率(1/1000)=289,盈利交易率(1/1000)=958
                    赢利次数=23,赢利总值=6958
                    亏损次数=1,亏损总值=22
                    平盘次数=0
                评估:总盈亏值=6766,交易次数=83  期望值=1125
                总盈亏率(1/1000)=6766,平均盈亏率(1/1000)=81,盈利交易率(1/1000)=373
                赢利次数=31,赢利总值=10560
                亏损次数=52,亏损总值=3794
                平盘次数=0
            再去掉ma30的触及
                评估:总盈亏值=6313,交易次数=131 期望值=774
                总盈亏率(1/1000)=6313,平均盈亏率(1/1000)=48,盈利交易率(1/1000)=282
                赢利次数=37,赢利总值=12081
                亏损次数=93,亏损总值=5768
                平盘次数=1
                闭合交易明细:
            
                评估:总盈亏值=2525,交易次数=22  期望值=1701
                总盈亏率(1/1000)=2525,平均盈亏率(1/1000)=114,盈利交易率(1/1000)=636
                赢利次数=14,赢利总值=3065
                亏损次数=8,亏损总值=540
                平盘次数=0

        目前取1.33，去掉msvap
        改成cmacd(svap,19,39)无改进
    '''
    t = stock.transaction
    
    mdiff,mdea = cmacd(stock.g5)   

    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = gand(vma_s > vma_l * 4/3)
    
    xcross = cross(mdea,mdiff) > 0

    linelog(stock.code)

    ll10 = rollx(t[LOW],10)
    hh10 = tmax(t[HIGH],10)
    rhl10 = hh10 * 1000/ll10

    c = t[CLOSE]
    ma30 = ma(c,30)
    above = gand(ma(c,13) > ma30,ma30>stock.ma60,stock.ma60>stock.ma120)


    
    svap,v2i = stock.svap_ma_67
    sdiff,sdea = cmacd(svap,36,78)
    ssignal = gand(sdiff < sdea,strend(sdiff)<0,strend(sdiff-sdea)>0)

    msvap = transform(ssignal,v2i,len(t[VOLUME]))

    x2 = cross(ma(t[CLOSE],60),t[LOW]) < 0

    ss = sfollow(xcross,x2,10)
    #ss = xcross

    #gf1 = gand(stock.g60>1000,stock.g20>1000)
    gf1 = gand(stock.g20>2000)
    #gf1 = gand(stock.g60>5000,stock.g60<9500)
    #gf1 = gand(stock.g20 > stock.g60,stock.g60>stock.g120,stock.g120>stock.g250)

    si = score2(t[CLOSE],t[VOLUME])
    msi = msum(si,5)
    mxi = gand(msi>=-100,msi<=0)
    
    signal = gand(ss,above,stock.t120,strend(stock.ma60)>0,t[VOLUME]>0,gf1,rhl10<1500,mdiff>=mdea,strend(stock.ref.ma60)>0,vfilter,mxi,msvap)
    
    return signal


def ldx(stock,mlen=60,glimit=3000): #
    ''' 破60日线
                LOW
                vfilter = gand(vma_5>vma_l*3/5,t[VOLUME] < vma_l*2/3)   
                gf1 = gand(stock.g60<3000)#,stock.g60>2000)                
                signal = gand(x2,above,stock.t120,strend(stock.ma60)>0,t[VOLUME]>0,gf1,pdiff<pdea,vfilter,mxi)
                20010701-20081231
                评估:总盈亏值=5008,交易次数=40  期望值=2358
                总盈亏率(1/1000)=5008,平均盈亏率(1/1000)=125,盈利交易率(1/1000)=550
                赢利次数=22,赢利总值=5979
                亏损次数=18,亏损总值=971
                平盘次数=0

                20080701-20090605
                评估:总盈亏值=18987,交易次数=138        期望值=2914
                总盈亏率(1/1000)=18987,平均盈亏率(1/1000)=137,盈利交易率(1/1000)=869
                赢利次数=120,赢利总值=19794
                亏损次数=17,亏损总值=807
                平盘次数=1
            添加 t[CLOSE] < ma_s    长短期相反
                评估:总盈亏值=161,交易次数=15   期望值=172
                总盈亏率(1/1000)=161,平均盈亏率(1/1000)=10,盈利交易率(1/1000)=400
                赢利次数=6,赢利总值=687
                亏损次数=9,亏损总值=526
                平盘次数=0
            
                评估:总盈亏值=11957,交易次数=62 期望值=9600
                总盈亏率(1/1000)=11957,平均盈亏率(1/1000)=192,盈利交易率(1/1000)=935
                赢利次数=58,赢利总值=12037
                亏损次数=4,亏损总值=80
                平盘次数=0
            添加 t[CLOSE] > ma_s    长短期相反  #这个是比较均衡的结果
                评估:总盈亏值=4858,交易次数=23  期望值=4137
                总盈亏率(1/1000)=4858,平均盈亏率(1/1000)=211,盈利交易率(1/1000)=652
                赢利次数=15,赢利总值=5269
                亏损次数=8,亏损总值=411
                平盘次数=0
            
                评估:总盈亏值=7552,交易次数=84  期望值=1618
                总盈亏率(1/1000)=7552,平均盈亏率(1/1000)=89,盈利交易率(1/1000)=833
                赢利次数=70,赢利总值=8276
                亏损次数=13,亏损总值=724


    #破30日线   LOW
                gf1 = gand(stock.g60<3000)
                ref.pdiff < ref.pdea
                mxi
                vfilter = gand(vma_s>vma_l,vma_s<vma_l*4/3)
                vfilter2 = gand(vma_5<vma_s)
                t[VOLUME]<vma_s*2/3
                #20080701-20090605
                评估:总盈亏值=15003,交易次数=104        期望值=2823
                总盈亏率(1/1000)=15003,平均盈亏率(1/1000)=144,盈利交易率(1/1000)=875
                赢利次数=91,赢利总值=15677
                亏损次数=13,亏损总值=674
                平盘次数=0
                #20010701-20081231
                评估:总盈亏值=8276,交易次数=37  期望值=3430
                总盈亏率(1/1000)=8276,平均盈亏率(1/1000)=223,盈利交易率(1/1000)=594
                赢利次数=22,赢利总值=9262
                亏损次数=15,亏损总值=986
                平盘次数=0

            vfilter = gand(vma_5>vma_l*3/5,t[VOLUME] < vma_l*2/3)   
            gf1 = gand(stock.g60<3000)#,stock.g60>2000)                
            signal = gand(x2,above,stock.t120,strend(stock.ma60)>0,t[VOLUME]>0,gf1,pdiff<pdea,vfilter,mxi)
            t[CLOSE] > ma_s
            评估:总盈亏值=6493,交易次数=55  期望值=1966
                总盈亏率(1/1000)=6493,平均盈亏率(1/1000)=118,盈利交易率(1/1000)=854
                赢利次数=47,赢利总值=6919
                亏损次数=7,亏损总值=426
                平盘次数=1

            评估:总盈亏值=5857,交易次数=39  期望值=2631
                总盈亏率(1/1000)=5857,平均盈亏率(1/1000)=150,盈利交易率(1/1000)=641
                赢利次数=25,赢利总值=6655
                亏损次数=14,亏损总值=798
                平盘次数=0

        gf1: <3333
            20080701--
            评估:总盈亏值=9474,交易次数=75  期望值=2739
                总盈亏率(1/1000)=9474,平均盈亏率(1/1000)=126,盈利交易率(1/1000)=826
                赢利次数=62,赢利总值=10026
                亏损次数=12,亏损总值=552
                平盘次数=1
            20010701--
            评估:总盈亏值=10510,交易次数=55 期望值=3410
                总盈亏率(1/1000)=10510,平均盈亏率(1/1000)=191,盈利交易率(1/1000)=672
                赢利次数=37,赢利总值=11529
                亏损次数=18,亏损总值=1019
                平盘次数=0
        gf1:<3500:
            20080701--
            评估:总盈亏值=10397,交易次数=80 期望值=2744
                总盈亏率(1/1000)=10397,平均盈亏率(1/1000)=129,盈利交易率(1/1000)=825
                赢利次数=66,赢利总值=11014
                亏损次数=13,亏损总值=617
                平盘次数=1
        
            评估:总盈亏值=10450,交易次数=64 期望值=2963
                总盈亏率(1/1000)=10450,平均盈亏率(1/1000)=163,盈利交易率(1/1000)=625
                赢利次数=40,赢利总值=11789
                亏损次数=24,亏损总值=1339
                平盘次数=0
        另，120有支撑，250是真破，貌似无支撑
    '''

    t = stock.transaction
    
    #vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)
    vma_5 = ma(t[VOLUME],5)

    #vfilter = gand(vma_5>vma_l,t[VOLUME] < vma_5*2/3)  #1017-538-13
    #vfilter = gand(t[VOLUME] < vma_l*2/3)  #916-482-87
    
    #vfilter = gand(t[VOLUME] < vma_l,vma_5>vma_l*2/3)  
    vfilter = np.ones_like(t[CLOSE])#gand(vma_5>vma_l,t[VOLUME] < vma_l)   

    #vdiff,vdea = cmacd(t[VOLUME])
    #vfilter = gand(vdiff<vdea,vdiff<0)

    linelog(stock.code)

    c = t[LOW]
    ma30 = ma(c,30)
    above = gand(ma(c,13) > ma30,ma30>stock.ma60,stock.ma60>stock.ma120)
    
    #mlen=60
    ma_s = ma(t[CLOSE],mlen)
    x2 = gand(cross(ma_s,t[LOW])< 0,t[CLOSE]>ma_s)

    gf1 = gand(stock.g60<3000)#,stock.g60>2000)

    pdiff,pdea = stock.ref.pdiff,stock.ref.pdea

    si = score2(t[CLOSE],t[VOLUME])
    msi = msum(si,5)
    mxi = gand(msi>=-100,msi<=0)
    
    #signal = gand(x2,above,stock.t120,strend(stock.ma60)>0,t[VOLUME]>0,gf1,rhl10<1500,strend(stock.ref.ma60)>0,vfilter,mxi)
    #signal = gand(x2,above,stock.t120,strend(stock.ma60)>0,t[VOLUME]>0,gf1,mxi,pdiff<pdea)
    #signal = gand(x2,above,stock.t120,strend(stock.ma60)>0,t[VOLUME]>0,gf1,pdiff<pdea,vfilter,mxi)
    signal = gand(x2,above,stock.t120,strend(stock.ma60)>0,t[VOLUME]>0)

    return signal


def gsvama(stock): #
    t = stock.transaction
    
    mdiff,mdea = cmacd(stock.g60)

    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = gand(vma_s > vma_l * 4/3)

    c = t[CLOSE]
    ma30 = ma(c,30)
    above = gand(ma(c,13) > ma30,ma30>stock.ma60,stock.ma60>stock.ma120)
    
    ll10 = rollx(t[LOW],10)
    hh10 = tmax(t[HIGH],10)
    rhl10 = hh10 * 1000/ll10

    svap,v2i = stock.svap_ma_67
    sdiff,sdea = cmacd(svap)
    ssignal = gand(sdiff < sdea,strend(sdiff)<0,strend(sdiff-sdea)>0)

    s20 = ma(svap,60)
    s50 = ma(svap,140)

    #sx = gand(cross(s50,s20) > 0,ssignal)

    sx = cross(s50,s20) > 0

    msvap = transform(band(sx,ssignal),v2i,len(t[VOLUME]))

    gf1 = gand(stock.g20>5000,stock.g20<9500)

    signal = gand(msvap,above,stock.t120,strend(stock.ma60)>0,t[VOLUME]>0,gf1,rhl10<1500,mdiff>=mdea,strend(stock.ref.ma60)>0,vfilter,trend(mdiff-mdea)>0)

    #signal = msvap
    
    linelog(stock.code)

    return signal


#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250)
#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s>=3300,s<=6600)
def ma4(stock,dates):
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    
    ma5 = ma(t[CLOSE],5)
    ma10 = stock.ma10
    ma20 = stock.ma20
    ma60 = stock.ma60
    ma120 = stock.ma120
    dcross = gand(cross(ma10,ma5),strend(ma5)>0,strend(ma10)>0,strend(ma20)>0,strend(ma60)>0,strend(ma120)>0)
    #dcross = gand(cross(ma10,ma5),strend(ma5)>0,strend(ma10)>0,strend(ma20)>0,strend(ma60)>0)
    #dabove = gand(greater(ma10,ma20),greater(ma20,ma60))
    cs = catalog_signal_cs(stock.c60,stock.silver)
    linelog(stock.code)
    return gand(g,cs,dcross,stock.above)

#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s>=3300,s<=6600)
#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250)
#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=3300)
def vmacd(stock,dates):
    t = stock.transaction
    vdiff,vdea = cmacd(t[VOLUME])
    dcross = gand(cross(vdea,vdiff),strend(vdiff)>0,strend(vdea>0))
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    linelog(stock.code)
    
    trend_ma_standard = strend(ma(t[CLOSE],120)) > 0    
    cs = catalog_signal_cs(stock.c60,c_extractor)

    #return dcross
    #return gand(dcross,g,trend_ma_standard)
    return gand(dcross,g,trend_ma_standard,cs,vdea>0,vdea<12000)


def dma(stock,dates):
    t = stock.transaction
    dif = ma(t[CLOSE],10) - ma(t[CLOSE],67)
    mas = ma(dif,22)
    dcross = gand(cross(mas,dif)>0,strend(dif)>0)
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    linelog(stock.code)
    
    ma_standard = ma(t[CLOSE],60)
    trend_ma_standard = strend(ma_standard) > 0    

    return gand(dcross,g,ma_standard)


#configs.append(config(buyer=fcustom(svama3,fast=165,mid=184,slow=1950))) 	#                   #577-63-619-42
def psvama3(stock,fast,mid,slow,dates):
    t = stock.transaction
    sbuy = svama3(stock,fast,mid,slow)

    #trend_psy = strend(ma(psy(t[CLOSE]),6)) > 0
    mpsy = ma(psy(t[CLOSE],12),6)
    #spsy = psy(t[CLOSE])
    state_psy =  mpsy>500

    logger.debug(stock.code)
    linelog(stock.code)
    return gand(sbuy,state_psy)

def psvama2(stock,fast,slow,dates,ma_standard=500,sma=65):
    ''' svama两线交叉
    '''
    t = stock.transaction
    sbuy = svama2(stock,fast,slow)

    #trend_psy = strend(ma(psy(t[CLOSE]),6)) > 0
    mpsy = ma(psy(t[CLOSE],12),6)
    #spsy = psy(t[CLOSE])
    state_psy =  mpsy<300

    logger.debug(stock.code)
    linelog(stock.code)
    return gand(sbuy,state_psy)

def psy_test(stock,dates,ma_standard=60):
    #另，psy(55)的5X55, psy(12),psy(67)的ma5的叉
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    g60 = stock.g60
    spsy1 = psy(t[CLOSE],67)
    spsy2 = psy(t[CLOSE],67)

    ma_psy1 = ma(spsy1,5)
    ma_psy2 = ma(spsy2,5)
    trend_1 = strend(ma_psy1) > 0
    trend_2 = strend(ma_psy2) > 0    
    cross_psy = gand(cross(ma_psy2,ma_psy1)>0,trend_1,trend_2)

    ma_standard = ma(t[CLOSE],ma_standard)
    trend_ma_standard = strend(ma_standard) > 0    
 
    sbuy = gand(cross_psy,g,trend_ma_standard)
    #sbuy = gand(cross_psy,g)
    #sbuy = gand(cross_psy,g)
    linelog(stock.code)
    #for d,v,m,b,ms in zip(dates,ma_psy1,ma_psy2,sbuy,ma_standard):print d,v,m,b,ms

    return sbuy

def gtest3(stock,dates):
    t = stock.transaction

    if not stock.has_attr('ma'):
        ma10 = ma(t[CLOSE],10)
        ma20 = ma(t[CLOSE],20)
        ma60 = ma(t[CLOSE],60)
        ma120 = ma(t[CLOSE],120)
        t120 = strend(ma120)>0
        ma_above = gand(greater(ma10,ma20),greater(ma20,ma60),greater(ma60,ma120))        
        stock.set_attr('ma',{'10':ma10,'20':ma20,'60':ma60,'120':ma120,'t120':t120,'above':ma_above})
    t120,ma_above = stock.ma['t120'],stock.ma['above']
    ma10,ma20,ma60,ma120 = stock.ma['10'],stock.ma['20'],stock.ma['60'],stock.ma['120']

    g = gand(stock.g20 >= stock.g60+1000,stock.g60 >= stock.g120+1000,stock.g20>=3000,stock.g20<=8000)

    gma20 = ma(stock.g20,5)
    gma60 = ma(stock.g60,5)
    cross_fast_slow = gand(cross(gma60,gma20)>0,strend(gma20)>0,strend(gma60)>0)
    
    linelog(stock.code)
    #cs = catalog_signal_cs(stock.c60,c_extractor)
    
    #return gand(g,cs,cross_fast_slow,t120,ma_above)
    #return gand(g,cross_fast_slow,ma_above)    
    return gand(g,t120,ma_above)    


def gtest2(stock,dates):
    t = stock.transaction

    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)

    gx = stock.g60
    ma_fast = ma(gx,5)
    ma_slow = ma(gx,20)
    trend_ma_fast = strend(ma_fast) > 0
    trend_ma_slow = strend(ma_slow) > 0    
    cross_fast_slow = gand(cross(ma_slow,ma_fast)>0,trend_ma_fast,trend_ma_slow)
    
    c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s>=3300,s<=6600)
    cs = catalog_signal_cs(stock.c60,c_extractor)

    linelog(stock.code)
    
    #return gand(g,cs,cross_fast_slow,t120,ma_above)
    return gand(g,cs,cross_fast_slow,stock.above,stock.t120)    

def gtest(stock,fast,slow,dates,ma_standard=120):
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    g60 = stock.g60
    ma_fast = ma(g60,fast)
    ma_slow = ma(g60,slow)
    trend_ma_fast = strend(ma_fast) > 0
    trend_ma_slow = strend(ma_slow) > 0    
    cross_fast_slow = gand(cross(ma_slow,ma_fast)>0,trend_ma_fast,trend_ma_slow)

    ma_standard = ma(t[CLOSE],ma_standard)
    trend_ma_standard = strend(ma_standard) > 0    
 
    ma_120 = ma(stock.g120,5)   #平滑一下
    ma_250 = ma(stock.g250,5)
    trend_ma_120 = strend(ma_120) > 0
    trend_ma_250 = strend(ma_250) > 0

    print stock.code

    return gand(cross_fast_slow,g,trend_ma_120,trend_ma_250,g60>5000,g60<8000)

#c_extractor = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s>=3300,s<=6600)

def ext_factory(sbegin,send):
    return lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s>=sbegin,s<=send)

def func_test(stock,fast,mid,slow,ma_standard=500,extend_days=10,pre_length=67,**kwargs):
    ''' vama三叉
    '''
    dates = kwargs['dates'] #打印输出用
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    #svap,v2i = vap_pre(t[VOLUME],t[CLOSE],pre_length)
    skey = 'vap_pre_%s' % pre_length
    if not stock.has_attr(skey): #加速
        stock.set_attr(skey,vap_pre(t[VOLUME],t[CLOSE],pre_length))
    svap,v2i = stock.get_attr(skey) 
    
    ma_svapfast = ma(svap,fast)
    ma_svapmid = ma(svap,mid)    
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapmid = strend(ma_svapmid) > 0    
    trend_ma_svapslow = strend(ma_svapslow) > 0

    cross_fast_mid = band(cross(ma_svapmid,ma_svapfast)>0,trend_ma_svapfast)
    cross_fast_slow = band(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast)    
    cross_mid_slow = band(cross(ma_svapslow,ma_svapmid)>0,trend_ma_svapmid)
    sync_fast_2 = sfollow(cross_fast_mid,cross_fast_slow,extend_days)
    sync3 = sfollow(sync_fast_2,cross_mid_slow,extend_days)

    ma_standard = ma(svap,ma_standard)
    trend_ma_standard = strend(ma_standard) > 0    
    
    diff,dea = cmacd(svap)
    trend_macd = gand(diff>dea,strend(diff)>0,strend(dea)>0)
    #vsignal = gand(sync3,trend_ma_standard,trend_macd)
    vsignal = gand(sync3,trend_ma_standard,trend_macd)

    msvap = transform(vsignal,v2i,len(t[VOLUME]))

    #cs = catalog_signal_cs(stock.c120,cextractor)
    #cs = catalog_signal_cs(stock.c20,cextractor)
    #cx = catalog_signal_c(stock.catalog, lambda c:gand(c.g20>5000,c.g20<9000,c.g20>c.g60))
    
    #func = lambda a,b,c,d,e:gand(a>b,b>c,c>d,d>e)
    #cy = catalog_signal_m(func,stock.c5,stock.c20,stock.c60,stock.c120,stock.c250)

    #cs = gand(cx,cy)

    gtrend = gand(strend(stock.g5)>0,strend(ma(stock.g20,5))>0,strend(ma(stock.g60,5))>0)
    
    
    #sbuy = msvap
    #sbuy = gand(g,msvap)
    sbuy = gand(g,gtrend,msvap,cs)
    #sbuy = gand(g,cs,msvap)
    #down_limit = tracelimit((t[OPEN]+t[LOW])/2,t[HIGH],sbuy,stock.atr,600,3000)

    #seller = atr_xseller_factory(stop_times=600,trace_times=3000)    
    #ssell = seller(stock,sbuy)

    #sb = make_trade_signal_advanced(sbuy,ssell)      
    #for x in zip(dates,sbuy,down_limit,t[LOW],t[OPEN],t[CLOSE],stock.atr*600/1000,t[OPEN]-stock.atr*600/1000,ssell,sb)[-80:]:
    #    print x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9]

    #sup = up_under(t[HIGH],t[LOW],10,300)    
    #return gand(g,msvap)
    #for x in zip(dates,t[CLOSE],stock.g5,stock.g20,stock.g60,stock.g120,stock.g250):
    #    print '%s,%s,%s,%s,%s,%s,%s' % (x[0],x[1],x[2],x[3],x[4],x[5],x[6])

    #f.close()

    linelog(stock.code)
    return sbuy

def func_test_old(stock,fast,slow,base,sma=55,ma_standard=120,extend_days=5,**kwargs):
    ''' svama二叉,extend_days天内再有日线底线叉ma(base)
    '''
    dates = kwargs['dates'] #打印输出用
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    svap,v2i = svap_ma(t[VOLUME],t[CLOSE],sma)
    #print len(svap),len(v2i),len(dates)
    print stock.code
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0

    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    #for s,v,f,sl,c in zip(svap,v2i,ma_svapfast,ma_svapslow,cross_fast_slow):
    #    print '%s,%s,%s,%s,%s' % (dates[v],s,f,sl,c)
    for s,v in zip(svap,v2i):
        print '%s,%s' % (dates[v],s)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))
    print np.sum(msvap),np.sum(cross_fast_slow)
    ma_standard = ma(t[CLOSE],ma_standard)
    trend_ma_standard = strend(ma_standard) > 0

    ma_fast = t[LOW]
    ma_base = ma(t[CLOSE],base)
    trend_base = strend(ma_base) > 0    
    xcross = band(cross(ma_base,ma_fast),trend_base)
    #sf = sfollow(msvap,xcross,extend_days)  #syntony
    sf = syntony(msvap,xcross,extend_days)
    
    #sbuy = gand(g,sf,trend_ma_standard)
    sbuy = msvap
    #print dates[sbuy>0]
    down_limit = tracelimit((t[OPEN]+t[LOW])/2,t[HIGH],sbuy,stock.atr,600,3000)
    
    #for x in zip(dates,sbuy,down_limit,t[LOW],t[OPEN],t[CLOSE],stock.atr*600/1000,t[OPEN]-stock.atr*600/1000):
    #    print x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7]
    return sbuy

def prepare_buyer(dates):
    #return fcustom(func_test,ma_standard=500,slow=50,extend_days=31,fast=30,mid=67,dates=dates)
    #return fcustom(func_test,ma_standard=500,slow=45,extend_days=17,fast=32,mid=79,dates=dates)
    #return fcustom(func_test,fast= 33,mid= 84,slow=345,ma_standard=500,extend_days= 27,dates=dates,cextractor=ext_factory(3300,6600))
    return fcustom(gtest,fast=5,slow=60,dates=dates)
    #return fcustom(psvama2,fast=  9,slow=1160,dates=dates) 
    #return fcustom(psy_test,dates=dates)
    #return fcustom(dma,dates=dates)
    #return fcustom(vmacd,dates=dates)
    #return fcustom(psvama3,fast=165,mid=184,slow=1950,dates=dates) 
    #return fcustom(ma4,dates=dates)
    #return fcustom(vmacd_ma4,dates=dates)
    #return fcustom(temv,dates=dates)
    #return fcustom(wvad,dates=dates)
    #return fcustom(ma3,dates=dates)
    #return fcustom(xma60,dates=dates)
    #return fcustom(nhigh,dates=dates)
    #return fcustom(pmacd,dates=dates)
    #return fcustom(gtest2,dates=dates)
    #return fcustom(gcs,dates=dates)
    #return fcustom(tsvama2,dates=dates)
    #return fcustom(svap_macd,dates=dates)
    #return fcustom(gtest3,dates=dates)
    #return fcustom(ctest,dates=dates)
    #return fcustom(swrap,dates=dates)



def prepare_base(sdata):
    base = BaseObject()
    sdatas = extract_collect(sdata.values(),CLOSE)
    base.g20 = (increase(sdatas,20)>0).sum(0)
    return base

def prepare_gfilter(ref):
    #diff,dea = cmacd(ref.transaction[CLOSE],50,120)
    #gfilter = greater(diff,dea)
    gfilter = strend(ma(ref.transaction[CLOSE],250))>0
    #gfilter = np.zeros_like(ref.transaction[CLOSE])
    return gfilter

def run_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata.values())
    prepare_order(catalogs)
    prepare_common(sdata.values(),idata[ref_id])
    dummy_catalogs('catalog',catalogs)

    tbegin = time()

    pman = AdvancedATRPositionManager()
    dman = DateManager(begin,end)
    myMediator=nmediator_factory(trade_strategy=B1S1,pricer = oo_pricer)
    #seller = atr_xseller_factory(stop_times=2000,trace_times=3000)
    #seller = atr_xseller_factory(stop_times=1500,trace_times=3000)
    #seller = atr_xseller_factory(stop_times=1000,trace_times=3000)
    seller = atr_xseller_factory(stop_times=600,trace_times=3000)
    #seller = csc_func
    #seller = fcustom(csc_func,threshold=100)

    buyer = prepare_buyer(dates)   
    name,tradess = calc_trades(buyer,seller,sdata,dates,xbegin,cmediator=myMediator)
    result,strade = ev.evaluate_all(tradess,pman,dman)
    #print strade

    #last_trades
    #m = cmediator(buyer,seller)
    #trades = m.calc_last(sdata,dates,xbegin)


    f = open('srun.txt','w+')
    f.write(strade)
    f.close()

    #tradess = myMediator(buyer,seller).calc_last(sdata,dates,xbegin)
    #print tradess[0]
    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    


if __name__ == '__main__':
    logging.basicConfig(filename="srun_x4c.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    #测试时间段 [19980101,19990101-20010801],[20000101,20010701-20050901],[20040601,20050801-20071031],[20060601,20071031-20090101]
    #总时间段   [20000101,20010701,20090101]    #一个完整的周期+一个下降段
    #分段测试的要求，段mm > 1000-1500或抑制，总段mm > 2000
    
    #begin,xbegin,end = 19980101,20010701,20090101
    #begin,xbegin,end = 20000101,20010701,20090101
    #begin,xbegin,end = 20000101,20010701,20050901
    #begin,xbegin,end = 19980101,19990701,20010801    
    #begin,xbegin,end = 20040601,20050801,20071031
    #begin,xbegin,end = 20060601,20071031,20090101
    #begin,xbegin,end = 19980101,19990101,20090101
    #begin,xbegin,end,lbegin = 20070101,20080601,20090327,20080601
    #begin,xbegin,end,lbegin = 19980101,20010701,20090327,20000101
    begin,xbegin,end = 20000101,20010701,20091231
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
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600433','SH600000'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH000001'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600067'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600766'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SZ002012'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600971'],[ref_code])
    #c_posort('c120',catalogs,distance=120)
    

    tend = time()
    print u'数据准备耗时: %s' % (tend-tbegin)    
    import psyco
    psyco.full()

    run_main(dates,sdata,idata,catalogs,begin,end,xbegin)

