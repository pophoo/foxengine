# -*- coding: utf-8 -*-

'''
#控制模块

from wolfox.fengine.ifuture.ibase import *
import wolfox.fengine.ifuture.ifreader as ifreader
import wolfox.fengine.ifuture.iftrade as iftrade
import wolfox.fengine.ifuture.ifuncs2 as ifuncs2
import wolfox.fengine.ifuture.ifuncs as ifuncs
import wolfox.fengine.ifuture.ifuncs1a as ifuncs1
import wolfox.fengine.ifuture.tfuncs as tfuncs
import wolfox.fengine.ifuture.fcontrol as control
import wolfox.fengine.ifuture.dynamic as dynamic
import wolfox.fengine.ifuture.evaluate as ev
import wolfox.fengine.ifuture.xfuncs as xfuncs
import wolfox.fengine.ifuture.xfuncs2 as xfuncs2
import wolfox.fengine.ifuture.xtfuncs as xtfuncs
import wolfox.fengine.ifuture.utrade as utrade
import wolfox.fengine.ifuture.ufuncs as ufuncs
import wolfox.fengine.ifuture.ufuncs2 as ufuncs2
import wolfox.fengine.ifuture.utrade2 as utrade2


from wolfox.fengine.ifuture.ifuncs import *


ifmap = ifreader.read_ifs_zip()  # fname ==> BaseObject(name='$name',transaction=trans)


###计算
i00 = ifmap['IF0001']   #当月连续
#i05 = ifmap['IF1005']
#i06 = ifmap['IF1006']
#i07 = ifmap['IF1007']
#i08 = ifmap['IF1008']
#i09 = ifmap['IF1009']
#i12 = ifmap['IF1012']
#i01 = ifmap['IF1101']
#i10 = ifmap['IF1010']
#i11 = ifmap['IF1011']

#tradesy =  control.itradex8_yt(i00,ifuncs2.xxx2)
#tradesy =  control.itradex8_zt(i00,ifuncs2.xxx2)
#tradesy =  control.itradex8_yy(i00,xfuncs.xxx)
#tradesy =  utrade.utrade_n(i00,ufuncs.xxx)
tradesy =  utrade2.utrade2_n(i00,ufuncs2.mbreak)

#iftrade.limit_profit(tradesy,-90)

lx = lambda ii,trade:ii.xatr[trade.actions[0].index]
lm = lambda ii,trade:ii.mxatr[trade.actions[0].index]
lx30 = lambda ii,trade:ii.xatr30x[trade.actions[0].index]
lm30 = lambda ii,trade:ii.mxatr30x[trade.actions[0].index]
lx15 = lambda ii,trade:ii.xatr15x[trade.actions[0].index]
lm15 = lambda ii,trade:ii.mxatr15x[trade.actions[0].index]
lx10 = lambda ii,trade:ii.xatr10x[trade.actions[0].index]
lm10 = lambda ii,trade:ii.mxatr10x[trade.actions[0].index]
lx5 = lambda ii,trade:ii.xatr5x[trade.actions[0].index]
lm5 = lambda ii,trade:ii.mxatr5x[trade.actions[0].index]


for trade in tradesy:print trade.profit,trade.actions[0].date,trade.actions[0].time,trade.actions[0].position,trade.actions[0].price,trade.actions[1].time,trade.actions[1].price,trade.actions[1].index-trade.actions[0].index,trade.orignal.name

#for trade in tradesy:print trade.profit,trade.actions[0].date,trade.actions[0].time,trade.actions[0].position,trade.actions[0].price,trade.actions[1].time,trade.actions[1].price,trade.actions[1].index-trade.actions[0].index,str(trade.functor)[10:-14],str(trade.orignal)[10:-14],lx(i00,trade),lm(i00,trade),lx5(i00,trade),lm5(i00,trade),lx15(i00,trade),lm15(i00,trade),lx30(i00,trade),lm30(i00,trade)

sum([trade.profit for trade in tradesy])
sum([trade.profit>0 for trade in tradesy])
sum([trade.profit for trade in tradesy])/len(tradesy)
len(tradesy)
iftrade.R(tradesy)

iftrade.max_drawdown(tradesy)    #最大连续回撤和单笔回撤
iftrade.max_win(tradesy)         #最大连续盈利和单笔盈利





#5月合约
sum([trade.profit for trade in tradesy if trade.actions[0].date<=20100517])
#6月合约
sum([trade.profit for trade in tradesy if trade.actions[0].date>20100517 and trade.actions[0].date<=20100617])
#7月合约
sum([trade.profit for trade in tradesy if trade.actions[0].date>20100617 and trade.actions[0].date<=20100714])
#8月合约
sum([trade.profit for trade in tradesy if trade.actions[0].date>20100714 and trade.actions[0].date<=20100818])


#输出到文件
fo = open('d:/temp/201000.txt','w+')
for trade in tradesy:print >>fo,'%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (trade.profit,trade.actions[0].date,trade.actions[0].time,trade.actions[0].position,trade.actions[0].price,trade.actions[1].date,trade.actions[1].time,trade.actions[1].position,trade.actions[1].price,trade.actions[1].index-trade.actions[0].index,trade.orignal.name)
fo.close()

'''

from wolfox.fengine.ifuture.ibase import *
import wolfox.fengine.ifuture.iftrade as iftrade
import wolfox.fengine.ifuture.ifuncs as ifuncs

itrade3u = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_15_6,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])

#平仓：买入后macd马上下叉，则卖出;卖出后macd马上上叉，也平仓；另持多仓时出现新的买入点，但macd即刻下叉，则将持仓卖出,反之亦然
#diff5<0,diff30<0的顶背离作为平多仓条件，把特定底背离当作平空仓条件

itrade3x = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_15_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1,ifuncs.ipmacd_long_devi1],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])

#itrade3y = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_15_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=[ifuncs.daystop_long,ifuncs.ipmacd_short,ifuncs.down01,ifuncs.dmacd_short5,ifuncs.ipmacdx_short,ifuncs.ipmacd_short5,ifuncs.ma30_short,ifuncs.ma60_short,ifuncs.xmacd_stop_long1])

#sycloser = [ifuncs.daystop_long,ifuncs.ipmacd_short_1,ifuncs.ipmacd_short_2,ifuncs.ipmacd_short_3,ifuncs.ma3x10_short,ifuncs.down01,ifuncs.dmacd_short5,ifuncs.ipmacdx_short,ifuncs.ipmacd_short5,ifuncs.ma30_short,ifuncs.ma60_short,ifuncs.xmacd_stop_long1]

sycloser = [ifuncs.daystop_long]


#动态止损，去掉daystop_long
#sycloser_d = [ifuncs.ipmacd_short_1,ifuncs.ipmacd_short_2,ifuncs.ipmacd_short_3,ifuncs.ma3x10_short,ifuncs.down01,ifuncs.dmacd_short5,ifuncs.ipmacdx_short,ifuncs.ipmacd_short5,ifuncs.ma30_short,ifuncs.ma60_short]

sycloser_d = []

#sycloser_k = [ifuncs.daystop_long,ifuncs.ipmacd_short_1,ifuncs.ipmacd_short_2,ifuncs.ipmacd_short_3,ifuncs.ma3x10_short,ifuncs.down01,ifuncs.dmacd_short5,ifuncs.ipmacdx_short,ifuncs.ipmacd_short5,ifuncs.ma30_short,ifuncs.ma60_short]

sycloser_k = sycloser

#sycloser_kd = [ifuncs.ipmacd_short_1,ifuncs.ipmacd_short_2,ifuncs.ipmacd_short_3,ifuncs.ma3x10_short,ifuncs.down01,ifuncs.dmacd_short5,ifuncs.ipmacdx_short,ifuncs.ipmacd_short5,ifuncs.ma30_short,ifuncs.ma60_short]

sycloser_kd = []


lycloser = [r for r in sycloser]
del lycloser[0] #去掉daystop_long

itrade3y = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_15_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)


ltrade3y = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_15_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=iftrade.last_trades,longfilter=iftrade.last_filter,shortfilter=iftrade.last_filter)



#空头不把macd即刻反叉作为平仓条件
itrade3yk = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_15_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser_k)

itrade3x1 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_1_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1,ifuncs.ipmacd_long_devi1],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])

itrade3y1 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_1_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y2 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_2_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y3 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_3_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y4 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_4_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)
itrade3y6 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_6_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)


ltrade3y1 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_1_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=iftrade.last_trades,longfilter=iftrade.last_filter,shortfilter=iftrade.last_filter)
ltrade3y2 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_2_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=iftrade.last_trades,longfilter=iftrade.last_filter,shortfilter=iftrade.last_filter)
ltrade3y3 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_3_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=iftrade.last_trades,longfilter=iftrade.last_filter,shortfilter=iftrade.last_filter)
ltrade3y4 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_4_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=iftrade.last_trades,longfilter=iftrade.last_filter,shortfilter=iftrade.last_filter)
ltrade3y6 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_6_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=iftrade.last_trades,longfilter=iftrade.last_filter,shortfilter=iftrade.last_filter)



itrade3x45 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_15_6_45,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1,ifuncs.ipmacd_long_devi1],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])


itrade1525 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_15_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])

itrade256 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_15_6,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])



#空头不把即刻反叉作为平仓选项
itrade3xk = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_15_6,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])


#import wolfox.fengine.ifuture.tfuncs as tfuncs

#itrade3xkx = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_15_6,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1,tfuncs.xdevi_stop_long12])





itrade3y_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_15_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)


ltrade3y_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_15_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=iftrade.last_trades,longfilter=iftrade.last_filter,shortfilter=iftrade.last_filter)



#空头不把macd即刻反叉作为平仓条件
itrade3yk_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_15_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser_k)

itrade3x1_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_1_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1,ifuncs.ipmacd_long_devi1],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])

itrade3y05_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_05_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y05_15 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_05_15,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y05_1 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_05_10,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)
itrade3y05_05 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_05_05,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)


itrade3y05_2 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_05_20,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y05_25 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_05_25,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser) ###最好的搭配

itrade3y05_25b = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_05_25b,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser) ###最好的搭配

itrade3y05_25c = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_05_25c,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser) ###最好的搭配

itrade3y05_3 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_05_3,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)
itrade3y05_4 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_05_4,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y1_2 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_1_2,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)
itrade3y1_15 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_1_15,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y1_25 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_1_25,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)


itrade3y1_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_1_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y2_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_2_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y3_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_3_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y4_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_4_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)
itrade3y6_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_6_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)


ltrade3y1_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_1_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=iftrade.last_trades,longfilter=iftrade.last_filter,shortfilter=iftrade.last_filter)
ltrade3y2_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_2_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=iftrade.last_trades,longfilter=iftrade.last_filter,shortfilter=iftrade.last_filter)
ltrade3y3_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_3_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=iftrade.last_trades,longfilter=iftrade.last_filter,shortfilter=iftrade.last_filter)
ltrade3y4_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_4_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=iftrade.last_trades,longfilter=iftrade.last_filter,shortfilter=iftrade.last_filter)
ltrade3y6_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_6_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=iftrade.last_trades,longfilter=iftrade.last_filter,shortfilter=iftrade.last_filter)

ltrade3y0525_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_05_25,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=iftrade.last_trades,longfilter=iftrade.last_filter,shortfilter=iftrade.last_filter)

ltrade3y0520_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_05_20,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=iftrade.last_trades,longfilter=iftrade.last_filter,shortfilter=iftrade.last_filter)

ltrade3y0515_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_05_15,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=iftrade.last_trades,longfilter=iftrade.last_filter,shortfilter=iftrade.last_filter)

ltrade3y0530_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_05_3,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=iftrade.last_trades,longfilter=iftrade.last_filter,shortfilter=iftrade.last_filter)

ltrade3y1025_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_1_25,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=iftrade.last_trades,longfilter=iftrade.last_filter,shortfilter=iftrade.last_filter)

ltrade3y1525_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_15_25,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=iftrade.last_trades,longfilter=iftrade.last_filter,shortfilter=iftrade.last_filter)


itrade3x45_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_15_6_45,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1,ifuncs.ipmacd_long_devi1],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])


itrade1525_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_15_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])

itrade256_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_15_6,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])



#空头不把即刻反叉作为平仓选项
itrade3xk_5 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_15_6,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])

#相比较物
itrade3yx = fcustom(iftrade.itrade3,stop_closer=iftrade.atr_uxstop_15_6,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itrade3yx_0525 = fcustom(iftrade.itrade3,stop_closer=iftrade.atr5_uxstop_05_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])

#############新的方式

itradex_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr_uxstop_15_6,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex5_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_05_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex7_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_07_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex8_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_08_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex6_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_06_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex3_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_03_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex15_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_15_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex12_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_12_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex20_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_20_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])

itradex8_yn = fcustom(iftrade.itradex
                ,stop_closer=iftrade.atr5_uxstop_08_25
                ,bclosers=[ifuncs.daystop_short]
                ,sclosers=[ifuncs.daystop_long]
                ,longfilter=iftrade.ocfilter_null
                ,shortfilter=iftrade.ocfilter_null
                )

itradex8_yt = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_t_08_25_B2,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])


itradex8_zt = fcustom(iftrade.itradez,stop_closer=iftrade.atr5_uxstop_t_08_25_B2,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex8_ztp = fcustom(iftrade.itradezp,stop_closer=iftrade.atr5_uxstop_t_08_25_B2,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])

#itradex8_yy = fcustom(iftrade.itradey,stop_closer=iftrade.atr5_uxstop_t_08_25_B2,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])

#itradex8_yy = fcustom(iftrade.itradey,stop_closer=iftrade.atr5_uxstop_kN,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex8_yy = fcustom(iftrade.itradey,stop_closer=iftrade.atr5_uxstop_kV,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])

itradex8_nx = fcustom(iftrade.itradey,stop_closer=iftrade.atr5_uxstop_nx,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])

itradex8_n70 = fcustom(iftrade.itradey,stop_closer=iftrade.atr5_uxstop_n70,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex8_n100 = fcustom(iftrade.itradey,stop_closer=iftrade.atr5_uxstop_n100,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex8_n2 = fcustom(iftrade.itradey,stop_closer=iftrade.atr5_uxstop_n2,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])


itradex8_yt_a = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_t_08_25_A,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex827_yt = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_t_08_25_B27,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])

itrade_ft = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_f_A,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])


itradex8_y6 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_08_25_6,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])


itradex8_y_r83 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_rxstop_08_3_83,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])

itradex5_y_30 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_05_25_30,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex7_y_30 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_07_25_30,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex8_y_30 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_08_25_30,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex6_y_30 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_06_25_30,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex3_y_30 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_03_25_30,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])

itradex5_y_25 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_05_25_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex7_y_25 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_07_25_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex8_y_25 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_08_25_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex6_y_25 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_06_25_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex3_y_25 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_03_25_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])

itradex5_y_325 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_05_3_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex7_y_325 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_07_3_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex8_y_325 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_08_3_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex6_y_325 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_06_3_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex3_y_325 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_03_3_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])


itradex5_y_3530 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_05_35_30,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex7_y_3530 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_07_35_30,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex8_y_3530 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_08_35_30,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex6_y_3530 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_06_35_30,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex3_y_3530 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_03_35_30,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])

itradex5_y_330 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_05_3_30,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex7_y_330 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_07_3_30,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex8_y_330 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_08_3_30,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex6_y_330 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_06_3_30,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex3_y_330 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_03_3_30,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])

itradex525_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_05_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])

itradex1_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_1_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex1525_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_15_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex1515_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_15_15,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex515_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_05_15,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex510_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_05_10,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex520_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_05_20,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])

itradex315_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_03_15,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex310_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_03_10,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
itradex305_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_03_05,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])

ltrade3x0525 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_05_25,bclosers=[ifuncs.xdaystop_short],sclosers=[ifuncs.xdaystop_long],make_trades=iftrade.last_trades,longfilter=iftrade.last_filter,shortfilter=iftrade.last_filter,sync_trades=iftrade.null_sync_tradess)
ltrade3x156 = fcustom(iftrade.itradex,stop_closer=iftrade.atr_uxstop_15_6,bclosers=[ifuncs.xdaystop_short],sclosers=[ifuncs.xdaystop_long],make_trades=iftrade.last_trades,longfilter=iftrade.last_filter,shortfilter=iftrade.last_filter,sync_trades=iftrade.null_sync_tradess)
ltrade3x0825 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_08_25,bclosers=[ifuncs.xdaystop_short],sclosers=[ifuncs.xdaystop_long],make_trades=iftrade.last_trades,longfilter=iftrade.last_filter,shortfilter=iftrade.last_filter,sync_trades=iftrade.null_sync_tradess)

ltradey = fcustom(iftrade.itradey,stop_closer=iftrade.atr5_uxstop_kN,bclosers=[ifuncs.xdaystop_short],sclosers=[ifuncs.xdaystop_long],make_trades=iftrade.last_trades,sync_trades=iftrade.null_sync_tradess)



#ltrade3x0825z = fcustom(iftrade.itradez,stop_closer=iftrade.atr5_uxstop_08_25,bclosers=[ifuncs.xdaystop_short],sclosers=[ifuncs.xdaystop_long],make_trades=iftrade.last_trades,longfilter=iftrade.state_last_filter,shortfilter=iftrade.state_last_filter,sync_trades=iftrade.null_sync_tradess)

ltrade3x0825z = fcustom(iftrade.itradez,stop_closer=iftrade.atr5_uxstop_08_25,bclosers=[ifuncs.xdaystop_short],sclosers=[ifuncs.xdaystop_long],make_trades=iftrade.last_trades,longfilter=iftrade.state_last_filter,shortfilter=iftrade.state_last_filter,sync_trades=iftrade.pair_sync_tradess)

ltrade3x0825y = fcustom(iftrade.itradey,stop_closer=iftrade.atr5_uxstop_08_25,bclosers=[ifuncs.xdaystop_short],sclosers=[ifuncs.xdaystop_long],make_trades=iftrade.last_trades,sync_trades=iftrade.pair_sync_tradess)


citradex_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr_uxstop_15_6,bclosers=[ifuncs.daystop_short_c],sclosers=[ifuncs.daystop_long_c],longfilter=iftrade.ocfilter_c,shortfilter=iftrade.ocfilter_c)
citradex5_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_05_25,bclosers=[ifuncs.daystop_short_c],sclosers=[ifuncs.daystop_long_c],longfilter=iftrade.ocfilter_c,shortfilter=iftrade.ocfilter_c)
citradex7_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_07_25,bclosers=[ifuncs.daystop_short_c],sclosers=[ifuncs.daystop_long_c],longfilter=iftrade.ocfilter_c,shortfilter=iftrade.ocfilter_c)
citradex8_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_08_25,bclosers=[ifuncs.daystop_short_c],sclosers=[ifuncs.daystop_long_c],longfilter=iftrade.ocfilter_c,shortfilter=iftrade.ocfilter_c)
citradex6_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_06_25,bclosers=[ifuncs.daystop_short_c],sclosers=[ifuncs.daystop_long_c],longfilter=iftrade.ocfilter_c,shortfilter=iftrade.ocfilter_c)
citradex3_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_03_25,bclosers=[ifuncs.daystop_short_c],sclosers=[ifuncs.daystop_long_c],longfilter=iftrade.ocfilter_c,shortfilter=iftrade.ocfilter_c)

citradex1_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_1_25,bclosers=[ifuncs.daystop_short_c],sclosers=[ifuncs.daystop_long_c],longfilter=iftrade.ocfilter_c,shortfilter=iftrade.ocfilter_c)
citradex1525_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_15_25,bclosers=[ifuncs.daystop_short_c],sclosers=[ifuncs.daystop_long_c],longfilter=iftrade.ocfilter_c,shortfilter=iftrade.ocfilter_c)
citradex15_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_15_15,bclosers=[ifuncs.daystop_short_c],sclosers=[ifuncs.daystop_long_c],longfilter=iftrade.ocfilter_c,shortfilter=iftrade.ocfilter_c)
citradex515_y = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_05_15,bclosers=[ifuncs.daystop_short_c],sclosers=[ifuncs.daystop_long_c],longfilter=iftrade.ocfilter_c,shortfilter=iftrade.ocfilter_c)

cltrade3x0525 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_05_25,bclosers=[ifuncs.xdaystop_short_c],sclosers=[ifuncs.xdaystop_long_c],make_trades=iftrade.last_trades,longfilter=iftrade.last_filter_c,shortfilter=iftrade.last_filter_c,sync_trades=iftrade.null_sync_tradess)
cltrade3x156 = fcustom(iftrade.itradex,stop_closer=iftrade.atr_uxstop_15_6,bclosers=[ifuncs.xdaystop_short_c],sclosers=[ifuncs.xdaystop_long_c],make_trades=iftrade.last_trades,longfilter=iftrade.last_filter_c,shortfilter=iftrade.last_filter_c,sync_trades=iftrade.null_sync_tradess)
cltrade3x0825 = fcustom(iftrade.itradex,stop_closer=iftrade.atr5_uxstop_08_25,bclosers=[ifuncs.xdaystop_short_c],sclosers=[ifuncs.xdaystop_long_c],make_trades=iftrade.last_trades,longfilter=iftrade.last_filter_c,shortfilter=iftrade.last_filter_c,sync_trades=iftrade.null_sync_tradess)



