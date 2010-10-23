# -*- coding: utf-8 -*-
'''

#######
小结：
    牛市中，mxatr30x是逐级放大的
            xatr也很大
            震荡和后面的持续上升通常没有atr收紧的环节
    熊市中，比较猥琐，大幅下跌后需要酝酿，将atr收紧后继续下跌

todo:
        检验 上升幅度和下降幅度 
        A. 使用supdownc  ==>cexpma ==>x/m
        B. 使用autr,adtr ==>x/m

for d,t,ic,iau,imau,iad,imad,iup,imup,idown,imdown in zip(i00.date[i00.i_cof30],i00.time[i00.i_cof30],i00.close[i00.i_cof30],i00.xautr30,i00.mxautr30,i00.xadtr30,i00.mxadtr30,i00.xup30,i00.mxup30,i00.xdown30,i00.mxdown30):
    print d,t,ic,iau,imau,iad,imad,iup,imup,idown,imdown

of = open('d:/temp/au.txt','w+')
for d,t,ic,iau,imau,iad,imad,iup,imup,idown,imdown in zip(i00.date[i00.i_cof30],i00.time[i00.i_cof30],i00.close[i00.i_cof30],i00.xautr30,i00.mxautr30,i00.xadtr30,i00.mxadtr30,i00.xup30,i00.mxup30,i00.xdown30,i00.mxdown30):
    print >>of,'%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d' %(d,t,ic,iau,imau,iad,imad,iup,imup,idown,imdown)
of.close()

    发现: mxup30x/mxdown30x   的比较  
          mxautr30x/mxadtr30x 的比较
    是比较好的搭配
    且可以与 xatr30x/mxatr30x的比较/趋势 搭配使用

    根据图形观察，发现规律:
        强上升趋势中，xatr30>mxatr30/mxatr30上升为涨，xatr30<mxatr30/mxatr30下降为跌
        强下跌趋势中，xatr30>mxatr30/mxatr30上升为跌，xatr30<mxatr30/mxatr30下降为涨
        转势过程中，按前一趋势处理
    而
        mxautr30/mxadtr30以及mxup30/mxdown30则为短期的强弱
    反过来说，如果xatr30>mxatr30且mxatr30上升是涨的话，可以确认为上升趋势
    在使用上，用r120来表示趋势?
        

todo:   检验1-3-5-10-15-30的xatr和mxatr,以及xatr的短期平均的趋势的影响
        目测 mxatr30x向下助涨，而向上助跌
        mxatr5x向上助涨向下助跌

        xatr5x/30x可能更加直接?

        寻找
            xatr30x > mxatr30x
        和  xatr30x > 6000
        是的可用策略

        判断对xatr30x > mxatr30x/xatr30x > 6000是否是由于单边行动导致的
            排除这个原因
            而只保留由于震荡导致的?
            有无必要?

        感觉上xatr30x,mxatr30x变化太慢,不如15分钟效率高
            
        ####
        发现xatr/mxatr的交叉点可以用来判断短期顶和底,然后做底部抬高或顶部下跌的判断?

        ####
        测试 mxatr30x / mxatr 的变化走势. 这个没有意义。因为mxatr30x每30分钟一变，而mxatr每分钟一变
            所以反映的只是mxatr的变化. 除非有变得方法来处理这个问题
        尝试不反映走势，反映倍数. 反映的是震荡的张离度
            ,sif.mxatr30x/sif.mxatr < 6


todo:   这个基本完成，但是貌似走入了一个误区。未采纳结果
        测试macd的不同参数
        测试ma的不同参数的折返效应. 以及收盘突破均线
        测试svama不同参数的折返效应，以及交叉效应

todo:   测试向上9个点(或X个点)以上,如果回退到1/0个点就平掉
    这样，止损分为三类:
        止损:   彻底的开仓方向错误
        保护性止损: 开仓后正向运行，且超过9个点，回退到开仓点+/-1/0时
        跟踪止损:  盈利时的止损 

todo:   研究逆势时止盈点位是否需要重新设置
#######

使用当月连续
    当某日收盘下月合约的持仓大于本月的90%时，切换
筛选条件:
    xatr
    如果是突破，则5分钟内稳定

    strend2(sif.ma13)
    strend2(sif.ma30)    
    sif.ma3 >/< sif.ma13

优先级：
    普通 1500
    逆势 >==2000
    突破 <=1200
        突破的附属 <2000

趋势确立后
    xatr60x < mxatr60x  (45/30也可)表示需要紧缩后才能继续趋势
趋势确立前
    xatr30x > mxatr30x  表示比较震荡, 震荡的周期要短

    而且不论趋势是否确立，短期应该震荡? xatr>mxatr?


收盘操作:
    如果到收盘的时候还有持仓，就把平仓的下限条件单开在15:00价格的上下3点上
        上限条件单开在前15分钟最高/低点
        假定15:00的价格为A, 14:45-15:00的最高价为P，最低价为B
    如果是持买仓:
        则下限条件单为 价格低于等于A-3，则以A-4卖出平仓
        上限条件单位为 价格高于等于P，则以P-1卖出平仓
    如果是持卖仓:
        则上限条件单为 价格高于等于A+3，则以A+4买入评仓
        下限条件单位为 价格低于等于B，则以B+1买入平仓
        


'''


from wolfox.fengine.ifuture.ibase import *
from wolfox.fengine.ifuture.iftrade import *

from wolfox.fengine.ifuture.orb import dnr1_uu_b,dnr1_dd_b,dnr1_ud_b,dp_uu_b,dp_ud_b,dpt_ux_b
from wolfox.fengine.ifuture.orb import dpt_uu_s,n30pt_dud_b,n30pt_du_s,n15pt_dd_b,n15pt_du_s,n60pt_uu_b
from wolfox.fengine.ifuture.orb import n60pt_uud_b,n60pt_dd_b,n60pt_duu_s,nr30s,nr30b

from wolfox.fengine.ifuture.xopt import *

xorb = [dnr1_uu_b,dnr1_dd_b,dnr1_ud_b,dp_uu_b,dp_ud_b,dpt_ux_b
        ,dpt_uu_s,n30pt_dud_b,n30pt_du_s,n15pt_dd_b,n15pt_du_s,n60pt_uu_b
        ,n60pt_uud_b,n60pt_dd_b,n60pt_duu_s,nr30s,nr30b
        ]

###顺势
def rsi_short_x(sif,sopened=None,rshort=7,rlong=19):
    '''
        每天的第一次符合条件的机会为最佳机会
        一旦第一次失败，后面的都被屏蔽
        比较妥当的是 7/19和13/41参数,其中前者明显优于后者
        但是合并有副作用
    '''

    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    #signal = cross(rsib,rsia)<0    
    signal = gand(cross(rsib,rsia)<0,strend2(rsia)<0)

    signal = gand(signal
            ,sif.s30<0
            ,sif.rs_trend<0
            ,sif.ms<0
            ,strend2(sif.ma30)<0
            ,sif.xatr30x<8000
            ,sif.mtrend<0

            #,sif.mxup30x < sif.mxdown30x
            #,sif.mxautr30x < sif.mxadtr30x
            #,sif.xatr30x > sif.mxatr30x
            #,sif.r60<0
            #,strend2(sif.mxatr30x)<0
            )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal==1)

    return signal * rsi_short_x.direction
rsi_short_x.direction = XSELL
rsi_short_x.priority = 1500


def rsi_short_xt(sif,sopened=None,rshort=7,rlong=19):
    '''
        每天的第一次符合条件的机会为最佳机会
        一旦第一次失败，后面的都被屏蔽
        比较妥当的是 7/19和13/41参数,其中前者明显优于后者
        但是合并有副作用
    '''

    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    #signal = cross(rsib,rsia)<0    
    signal = gand(cross(rsib,rsia)<0,strend2(rsia)<0)

    signal = gand(signal
            ,sif.s30<0
            ,strend2(sif.ma30)<0
            #,sif.xatr30x<8000
            ,sif.mtrend<0
            ,sif.xatr < sif.mxatr
            #,sif.xatr < 1200
            #,strend2(sif.xatr30x - sif.mxatr30x)>0
            ,strend2(sif.mxatr)>0
            )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal==1)

    return signal * rsi_short_xt.direction
rsi_short_xt.direction = XSELL
rsi_short_xt.priority = 1500


def rsi_short_yt(sif,sopened=None,rshort=7,rlong=19):
    '''
        每天的第一次符合条件的机会为最佳机会
        一旦第一次失败，后面的都被屏蔽
        比较妥当的是 7/19和13/41参数,其中前者明显优于后者
        但是合并有副作用
    '''

    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    #signal = cross(rsib,rsia)<0    
    signal = gand(cross(rsib,rsia)<0,strend2(rsia)<0)

    signal = gand(signal
            ,strend2(sif.ma30)<0

            #,sif.mxautr30x < sif.mxadtr30x
            #,sif.xatr30x<8000
            #,sif.mtrend<0
            #,sif.xatr < sif.mxatr
            #,sif.xatr < 1200
            #,strend2(sif.xatr30x - sif.mxatr30x)>0
            #,strend2(sif.mxatr)>0
            #,strend2(sif.mxadtr30x)<0
            #,strend2(sif.mxautr30x)<0            
            #,strend2(sif.mxatr30x)<0
            #,strend2(sif.mxdown30x)<0
            #,sif.xadtr30x < sif.mxadtr30x
            #,sif.xdown30x > sif.mxdown30x
            #,sif.xup30x < sif.mxup30x
            #,sif.xup < sif.xdown
            #,strend2(sif.mxdown-sif.mxup)>0
            )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal==1)

    return signal * rsi_short_yt.direction
rsi_short_yt.direction = XSELL
rsi_short_yt.priority = 1500


def rsi_short_x3(sif,sopened=None,rshort=7,rlong=19):
    '''
       使用sif.xatr30x>sif.mxatr30x 
       表示跌势确立初步时，大幅震荡
    '''

    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    
    #signal = cross(rsib,rsia)<0    
    signal = gand(cross(rsib,rsia)<0,strend2(rsia)<0)

    signal = gand(signal
            ,sif.xatr30x<6000
            ,sif.ms<0
            ,sif.mtrend<0
            ,sif.xatr30x>sif.mxatr30x
            ,sif.xatr>sif.mxatr
            )

    signal = np.select([sif.time>944],[signal],0)


    return signal * rsi_short_x3.direction
rsi_short_x3.direction = XSELL
rsi_short_x3.priority = 1500


def rsi_short_x2(sif,sopened=None,rshort=7,rlong=19):
    '''
        每天的第一次符合条件的机会为最佳机会
        一旦第一次失败，后面的都被屏蔽
        去掉s30<0的限制
        以sdiff30x<0为条件
        且s30>0 #s30<0的由rsi_short_x去捕捉

        ###已经废弃
    '''

    rsia = rsi2(sif.close,rshort)   
    rsib = rsi2(sif.close,rlong)
    #signal = cross(rsib,rsia)<0    
    signal = gand(cross(rsib,rsia)<0,strend2(rsia)<0)

    signal = gand(signal
            ,sif.strend<0
            ,sif.sdiff30x<0
            ,sif.s30>0  #s30<0的由rsi_short_x去捕捉
            ,strend2(sif.ma30)<0
            ,sif.xatr30x<6000
            ,sif.ma5<sif.ma13
            )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal==1)

    return signal * rsi_short_x2.direction
rsi_short_x2.direction = XSELL
rsi_short_x2.priority = 1500

def rsi_short_x2x(sif,sopened=None,rshort=7,rlong=19):
    '''
        使用了xatr30x<mxatr30x
        表示跌势确立后，再次下跌需要酝酿
        包含了rsi_short_x2
    '''

    rsia = rsi2(sif.close,rshort)   
    rsib = rsi2(sif.close,rlong)
    #signal = cross(rsib,rsia)<0    
    signal = gand(cross(rsib,rsia)<0,strend2(rsia)<0)

    signal = gand(signal
            ,sif.sdiff30x<0            
            ,sif.xatr30x<6000
            ,sif.xatr60x<sif.mxatr60x
            ,sif.strend<0
            ,strend2(sif.ma30)<0
            #,strend2(sif.xatr5x- sif.mxatr5x)>0
            )

    return signal * rsi_short_x2x.direction
rsi_short_x2x.direction = XSELL
rsi_short_x2x.priority = 1500
#rsi_short_x2x.stop_closer = atr5_uxstop_08_25_A

def macd_short_5(sif,sopened=None):
    '''
        高度顺势放空操作
        历史最悠久的方法
    '''
    ksfilter = gand(sif.open - sif.close < 60,rollx(sif.open - sif.close) < 120,sif.xatr<2000)

    signal = gand(cross(sif.dea1,sif.diff1)<0
            ,sif.mtrend < 0
            #,sif.ltrend<0
            ,sif.strend<0
            ,sif.sdiff30x<0
            ,sif.sdiff5x<0
            )
    signal = gand(signal
            ,sif.ma5 < sif.ma13
            ,strend2(sif.ma30)<0
            ,ksfilter
            ,sif.xatr30x<6000
            #,sif.xatr30x < sif.mxatr30x    #单独效果很好，但是合并效果不好
            )

    return signal * macd_short_5.direction
macd_short_5.direction = XSELL
macd_short_5.priority = 1500

def macd_short_x(sif,sopened=None):
    '''
        操作策略，失败一次之后当日就不应该再操作
        成功的话，可以继续操作，参见macd_short_x2
    '''
    signal = gand(cross(sif.dea1,sif.diff1)<0,strend2(sif.diff1)<0)

    signal = gand(signal
            ,sif.ltrend<0            
            ,sif.mtrend < 0
            ,strend2(sif.ma30)<0
            ,sif.ma5 < sif.ma13
            ,sif.xatr>800
            ,sif.sdiff30x<0
            )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal == 1)

    return signal * macd_short_x.direction
macd_short_x.direction = XSELL
macd_short_x.priority = 1500

def macd_short_xt(sif,sopened=None):
    '''
        操作策略，失败一次之后当日就不应该再操作
        成功的话，可以继续操作，参见macd_short_x2
    '''
    signal = gand(cross(sif.dea1,sif.diff1)<0,strend2(sif.diff1)<0)

    signal = gand(signal
            ,sif.ltrend<0            
            #,sif.mtrend < 0
            ,strend2(sif.ma30)<0
            ,sif.ma5 < sif.ma13
            #,sif.xatr>800
            ,sif.sdiff30x<0
            #,sif.xatr30x < sif.mxatr30x
            ,strend2(sif.mxatr30x)<0
            )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal == 1)

    return signal * macd_short_xt.direction
macd_short_xt.direction = XSELL
macd_short_xt.priority = 1500


def macd_short_xx(sif,sopened=None):
    '''
        跌势确立后需要缩小震荡然后继续下跌
        这个被macd_short_x包含
    '''
    signal = gand(cross(sif.dea1,sif.diff1)<0,strend2(sif.diff1)<0)

    signal = gand(signal
            ,sif.ltrend<0            
            ,sif.mtrend<0
            ,strend2(sif.ma30)<0
            ,sif.ma5 < sif.ma13
            ,sif.xatr>800
            ,sif.sdiff30x<0
            ,sif.xatr60x<sif.mxatr60x
            )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal == 1)

    return signal * macd_short_xx.direction
macd_short_xx.direction = XSELL
macd_short_xx.priority = 1000   #提高优先级
#macd_short_xx.stop_closer = atr5_uxstop_08_25_A

def macd_short_x2(sif,sopened=None):
    '''
        试图找到在盈利退出后的继续开仓
        没找到好办法. 
        用状态和时间来模拟
            1. 因为前次盈利，所以是绝对空头
            2. 因为前次退出，所以出现一小波的反弹. 但不影响中期左右趋势
            3. 时间在1345之后
        操作策略，失败一次之后当日就不应该再操作
    '''
    signal = gand(cross(sif.dea1,sif.diff1)<0,strend2(sif.diff1)<0)

    signal = gand(signal
            ,sif.ltrend<0            
            ,sif.mtrend < 0
            ,strend2(sif.ma30)<0
            ,sif.ma5 < sif.ma13
            ,sif.xatr>800
            ,sif.sdiff30x<0
            ,sif.mm<0   #处于绝对空头状态
            ,sif.ms<0
            )

    signal = np.select([sif.time>1345],[signal],0)    
    #signal = sum2diff(extend2diff(signal,sif.date),sif.date)

    signal = gand(signal == 1)

    return signal * macd_short_x2.direction
macd_short_x2.direction = XSELL
macd_short_x2.priority = 1600   #优先级低于本级



#####多头
def rsi_long_x(sif,sopened=None,rshort=7,rlong=19):
    '''
        比较妥当的是 7/19和13/41参数,其中前者明显优于后者
    '''

    #signal = cross(sif.dea1,sif.diff1)>0
    #rshort = 7
    #rlong = 19
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    #signal = cross(rsib,rsia)>0    
    signal = gand(cross(rsib,rsia)>0,strend2(rsia)>0)

    signal = gand(signal
                ,sif.ltrend>0
                ,sif.mtrend>0                
                ,sif.t7_30>0
                ,sif.s30>0
                ,sif.s10>0                
                ,sif.s3>0
            )

    return signal * rsi_long_x.direction
rsi_long_x.direction = XBUY
rsi_long_x.priority = 1500

rsi_long_x_1341 = fcustom(rsi_long_x,rshort=13,rlong=41)

def rsi_long_hl(sif,sopened=None,rshort=7,rlong=19):
    '''
        计算创当日新高后，从暴力起涨点算起回撤不到40%，然后再上升
        要求在上涨途中，即30分钟的120线向上
    '''
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    #signal = cross(rsib,rsia)>0    
    signal = gand(cross(rsib,rsia)>0,strend2(rsia)>0)

    signal = gand(signal
            ,sif.xatr < sif.mxatr
            ,sif.xatr < 1200 #越小越好
            ,sif.high > sif.dhigh - (sif.dhigh - sif.dlow2) *0.4    #回撤越小越好
            ,sif.xatr30x < 10000    #这个条件几乎等于没有
            #,strend2(sif.mxatr-sif.mxatr30x)>0

            ,sif.idhigh >= sif.idlow    #高点后于低点,必要性不大。
            ,sif.r120 > 10 #去掉毛刺
            #,sif.r90 > 10

            #加成效果明显，但为简单起见,暂时去掉
            #,sif.xatr3x<sif.mxatr3x
            )

    return signal * rsi_long_hl.direction
rsi_long_hl.direction = XBUY
rsi_long_hl.priority = 1500

def rsi_long_hl2(sif,sopened=None,rshort=7,rlong=19):
    '''
        计算创当日新高后，从暴力起涨点算起回撤不到40%，然后再上升
        要求在上涨途中，即30分钟的120线向上
    '''
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    #signal = cross(rsib,rsia)>0    
    signal = gand(cross(rsib,rsia)>0,strend2(rsia)>0)

    signal = gand(signal
            #,sif.xatr < sif.mxatr
            ,sif.xatr < 1800 #越大越好
            ,sif.xatr> 1200
            ,sif.high > sif.dhigh - (sif.dhigh - sif.dlow2) *0.4    #回撤越小越好
            ,strend2(sif.mxatr30x)>0
            #,strend2(sif.mxatr-sif.mxatr30x)>0

            #,sif.idhigh >= sif.idlow    #高点后于低点,必要性不大。
            ,sif.r120 > 10 #去掉毛刺
            #,sif.r90 > 10

            #加成效果明显，但为简单起见,暂时去掉
            #,sif.xatr3x<sif.mxatr3x
            )

    return signal * rsi_long_hl2.direction
rsi_long_hl2.direction = XBUY
rsi_long_hl2.priority = 1500


rsi_long_hl_1341 = fcustom(rsi_long_hl2,rshort=13,rlong=41)

def rsi_short_hl(sif,sopened=None,rshort=7,rlong=19):
    '''
        计算创当日新低后，从暴力起跌点算起回撤不到40%，然后再下降
        要求在下降途中，即30分钟的120线向下
        与上涨不同的是，下跌一半比较墨迹，所以容易缩量
    '''
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    #signal = cross(rsib,rsia)>0    
    signal = gand(cross(rsib,rsia)>0,strend2(rsia)>0)

    signal = gand(signal
            ,sif.xatr<1200  #越小越好
            ,sif.low < sif.dlow + (sif.dhigh2 - sif.dlow) *0.3  #低点先冲破. 下跌的时候一般比较狠
            #,sif.idlow >= sif.idhigh    #低点后于高点,必要性不大。如果跌破.4线，不论何时都一样
            ,sif.r120 < 0   #下跌具有自由落体情况，不惧毛刺, 甚至有吸引力，吸到<10的
            #,sif.r90 < 0

            #有效加成的条件，也可为简单起见暂时去掉
            ,strend2(sif.mxatr30x)<0   #加成效果极好. 说明下跌的时候是比较猥琐的，一般的会缩摆震荡。必要时放开这个限制
            
            #加成效果一般的条件, 暂时禁止
            #,sif.xatr30x < sif.mxatr30x    #加成效果比较好
            #,sif.xatr30x < 9000 #越小越好            

            #加成效果不明显的条件, 删除之
            #,sif.xatr > sif.mxatr   #暂且屏蔽一部分
            )

    return signal * rsi_short_hl.direction
rsi_short_hl.direction = XSELL
rsi_short_hl.priority = 1500

rsi_short_hl_1341 = fcustom(rsi_short_hl,rshort=13,rlong=41)



def rsi_long_xx(sif,sopened=None,rshort=7,rlong=19):
    '''
    '''

    #signal = cross(sif.dea1,sif.diff1)>0
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    #signal = cross(rsib,rsia)>0    
    signal = gand(cross(rsib,rsia)>0,strend2(rsia)>0)

    signal = gand(signal
                #,sif.t120>0
                ,sif.ltrend>0
                #,sif.mtrend>0                
                #,sif.t7_30>0
                #,sif.s30>0
                ,sif.s10>0                
                ,sif.s3>0
                ,sif.xatr30x<sif.mxatr30x
                ,sif.xatr<sif.mxatr
                #,sif.xatr>1000
                ,sif.xatr30x < 8000
                ,strend2(sif.mxatr)<0
                ,strend2(sif.mxatr30x)<0
            )
    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal==1)

    return signal * rsi_long_xx.direction
rsi_long_xx.direction = XBUY
rsi_long_xx.priority = 1000

rsi_long_xx_1341 = fcustom(rsi_long_xx,rshort=13,rlong=41)


def rsi_long_y2(sif,sopened=None,rshort=7,rlong=19):
    '''
        去掉s30限制
        比较妥当的是 7/19和13/41参数,其中前者明显优于后者
    '''

    #signal = cross(sif.dea1,sif.diff1)>0
    rshort = 13
    rlong = 41
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    signal = gand(cross(rsib,rsia)>0,strend2(rsia)>0)

    signal = gand(signal
                ,sif.s3>0
                ,sif.s15>0
                ,sif.ma3>sif.ma13
                ,sif.xatr30x<6000
                ,strend2(sif.ma13)>0
                ,sif.mxatr30x/sif.mxatr < 8
                ,sif.mtrend>0
            )
    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal==1)

    return signal * rsi_long_y2.direction
rsi_long_y2.direction = XBUY
rsi_long_y2.priority = 1500

def rsi_long_x2(sif,sopened=None,rshort=7,rlong=19):
    '''
        去掉s30限制
        比较妥当的是 7/19和13/41参数,其中前者明显优于后者
        这个一个主力算法，虽然R比较低
    '''

    #signal = cross(sif.dea1,sif.diff1)>0
    #rshort = 7
    #rlong = 19
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    signal = gand(cross(rsib,rsia)>0,strend2(rsia)>0)

    signal = gand(signal
                ,sif.s3>0
                ,sif.s15>0
                ,sif.ma3>sif.ma13
                ,sif.xatr30x<6000
                ,sif.ms>0
                )
    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal==1)

    return signal * rsi_long_x2.direction
rsi_long_x2.direction = XBUY
rsi_long_x2.priority = 1500

rsi_long_x2_1341 = fcustom(rsi_long_x2,rshort=13,rlong=41)

def rsi_long_x3(sif,sopened=None,rshort=7,rlong=19):
    '''
        去掉s30限制
        比较妥当的是 7/19和13/41参数,其中前者明显优于后者
        这个感觉太宽松了
    '''

    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    signal = gand(cross(rsib,rsia)>0,strend2(rsia)>0)

    signal = gand(signal
            ,strend2(sif.mxatr30x)>0
            ,strend2(sif.mxatr)>0
            ,sif.r60>20
            ,strend2(sif.ma30)>0
            ,sif.idhigh2 > sif.idlow2
            #,sif.mxatr30x / sif.mxatr < 7
            )
    signal = np.select([sif.time>944],[signal],0)

    #signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    #signal = gand(signal==1)

    return signal * rsi_long_x3.direction
rsi_long_x3.direction = XBUY
rsi_long_x3.priority = 1500

rsi_long_x3_1341 = fcustom(rsi_long_x3,rshort=13,rlong=41)

def macd_long_x(sif,sopened=None):
    '''
        居然添加任何ltrend/mtrend/strend条件都会使结果变坏
        经观察，这是个逆势的方法，所以不能加趋势
    '''
    signal = cross(sif.dea1,sif.diff1)>0    

    signal = gand(signal
                    ,sif.s30>0
                    ,sif.s10>0
                    ,sif.s3>0
                    ,sif.xatr<1200
                    ,strend2(sif.ma13)>0
            )

    return signal * macd_long_x.direction
macd_long_x.direction = XBUY
macd_long_x.priority = 2100

def macd_long_x2(sif,sopened=None):
    '''
        去掉s30>0条件
    '''
    signal = cross(sif.dea1,sif.diff1)>0    

    signal = gand(signal
                    ,sif.ltrend>0
                    ,sif.mtrend>0
                    ,sif.strend>0
                    ,sif.mm>0
                    ,sif.ms>0
                    ,sif.s10>0
                    ,sif.xatr<1200
            )

    return signal * macd_long_x2.direction
macd_long_x2.direction = XBUY
macd_long_x2.priority = 1500

def macd_long_x3(sif,sopened=None):
    '''
        去掉s30>0条件
        上升途中diff到达<0处后上插
    '''
    signal = cross(sif.dea1,sif.diff1)>0    

    signal = gand(signal
                    ,sif.s30>0
                    ,sif.s15>0
                    ,sif.diff1<0
                    ,sif.ltrend>0
                    ,sif.xatr<1200
                    ,sif.ma3>sif.ma13
                    ,sif.xatr60x<sif.mxatr60x
            )

    return signal * macd_long_x3.direction
macd_long_x3.direction = XBUY
macd_long_x3.priority = 1500


def up0(sif,sopened=None):
    '''
        上穿0线
        是逆势的
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤

    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1)>0
            ,sif.s30>0
            ,sif.s3>0
            ,sif.sdiff5x<0
            ,strend2(sif.ma30)>0
            ,strend2(sif.diff1)>3
            ,dsfilter
            
            #,gor(sif.xatr60x<sif.mxatr60x,sif.xatr>sif.mxatr)
            )

    return signal * up0.direction
up0.direction = XBUY
up0.priority = 2100  #叠加时，远期互有盈亏

def down01(sif,sopened=None): #++
    ''' 
        30分钟<0且下行
        5分钟>0且下行
    '''

    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1)<0
            ,sif.sdiff5x>0
            ,sif.sdiff30x<0
            ,strend(sif.diff1-sif.dea1)<-2            
            ,strend(sif.ma5-sif.ma30)<0
            ,strend(sif.ma135-sif.ma270)<0            
            ,strend(sif.ma30)<0
            ,sif.ltrend<0
            )
    return signal * down01.direction
down01.direction = XSELL
down01.priority = 1600

def down01x(sif,sopened=None): #++
    ''' 
        30分钟<0且下行
        5分钟>0且下行
    '''

    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1)<0
            ,sif.ltrend<0
            ,sif.sdiff30x<0
            ,sif.sdiff5x>0
            ,sif.xatr60x<sif.mxatr60x
            ,sif.xatr>sif.mxatr
            )
    return signal * down01x.direction
down01x.direction = XSELL
down01x.priority = 1600


def xdown60(sif,sopened=None):
    '''
        连续5分钟内出现60分钟最低点4个以上
    '''
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    covered = 60

    snewlow = sif.low < rollx(tmin(sif.low,covered))

    msnl = msum2(snewlow,5)

    signal = gand(msnl>3)

    signal = gand(signal
            #,sif.ma5 < sif.ma13
            #,strend2(sif.diff1-sif.dea1)<0
            ,strend2(sif.ma270)<0
            #,strend2(sif.sdiff5x-sif.sdea5x)<0
            #,strend2(sif.sdiff15x-sif.sdea15x)<0
            ,sif.mtrend<0            
            ,sif.ltrend<0
            ,ksfilter
            ,sif.xatr>1000
            ,strend2(sif.mxatr30x)<0
            )
    
    return signal * xdown60.direction
xdown60.direction = XSELL
xdown60.priority = 1600 

def ipmacd_short5(sif,sopened=None):
    '''
        最古老的方法
    '''
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)
    
    signal = gand(cross(sif.dea5,sif.diff5)<0
            ,sif.diff5>0
            ,sif.diff30<0
            ,strend(sif.diff30-sif.dea30)<0
            )
    signal = gand(signal
            ,strend(sif.ma13-sif.ma60)<0
            ,strend(sif.ma135-sif.ma270)<0
            ,ksfilter
            )   
    return signal * ipmacd_short5.direction
ipmacd_short5.direction = XSELL
ipmacd_short5.priority = 1800


def ma60_short(sif,sopened=None):
    ''' ma60拐头
    '''
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)
 
    msignal = gand(strend(sif.ma60) == -1
                )
    fsignal = gand(cross(sif.dea1,sif.diff1)<0
                ,strend2(sif.sdiff5x-sif.sdea5x)>0
                ,ksfilter                
                ,sif.xatr3x>sif.mxatr3x
                )
    signal = sfollow(msignal,fsignal,5)
    return signal * ma60_short.direction
ma60_short.direction = XSELL
ma60_short.priority = 1901

def xud30b(sif,sopened=None):
    '''
        顺势
    '''

    mxc = xc0c(sif.open30,sif.close30,sif.high30,sif.low30,13) > 0
    signal30 = gand(mxc
                ,sif.xatr30<sif.mxatr30
                ,sif.xatr30<8000    #这个条件可以放宽?
                #,strend2(sif.mxatr30)<0
                )

    signal = np.zeros_like(sif.diff1)
    signal[sif.i_cof30] = signal30

    signal = gand(signal
            ,sif.s15>0
            #,sif.s30>0
            )

    return signal * xud30b.direction
xud30b.direction = XBUY
xud30b.priority = 1200


ama1 = ama_maker()
ama2 = ama_maker(covered=30,dfast=6,dslow=100)

def ama_short(sif,sopened=None): #+
    trans = sif.transaction
    xama1 = ama1(trans[ICLOSE])
    xama2 = ama2(trans[ICLOSE])
    signal = gand(cross(xama2,xama1)<0
            #,sif.s10<0
            ,sif.xatr<1200
            ,sif.mtrend<0
            ,sif.xatr<sif.mxatr
            ,strend2(sif.mxatr)<0
            )
    return signal * XSELL
ama_short.direction = XSELL
ama_short.priority = 1600


###acd系列,属于突破算法
##辅助函数
def range_a(sif,tbegin,tend,wave):
    high10 = np.select([gand(sif.time>=tbegin,sif.time<=tend)],[sif.high],default=0)
    low10 = np.select([gand(sif.time>=tbegin,sif.time<=tend)],[sif.low],default=0)    

    xhigh10 = np.select([sif.time==924],[tmax(high10,11)],0)
    xlow10 = np.select([sif.time==924],[tmin(low10,11)],0)    

    UA = np.select([sif.time==tend],[xhigh10+wave],0)        
    DA = np.select([sif.time==tend],[xlow10-wave],0)    

    xhigh10 = extend2next(xhigh10)
    xlow10  = extend2next(xlow10)
    UA = extend2next(UA)
    DA = extend2next(DA)
    return UA,DA,xhigh10,xlow10

def acd_ua(sif,sopened=None):
    '''
        发现前两天不能有信号(不论前次信号胜负)，否则必败
    '''
    wave = np.zeros_like(sif.close)
    wave[sif.i_cof10] = rollx(sif.atr10) *2/3/XBASE  #掠过914-919的atr10
    wave = extend2next(wave)
    
    UA,DA,xhigh10,xlow10 = range_a(sif,914,924,wave)

    xcontinue = 5

    signal_ua = gand(sif.close >= UA
                    ,msum2(sif.close>=UA,xcontinue)>4
                    ,rollx(sif.close,xcontinue)>=UA
                    )

    signal_ua = np.select([sif.time>944],[signal_ua],0) #924之前的数据因为xhigh10是extend2next来的，所以不准

    signal_da = gand(sif.close <= DA
                    ,msum2(sif.close<DA,xcontinue)>=4
                    ,rollx(sif.close,xcontinue)<=DA
                    )

    signal_da = np.select([sif.time>944],[signal_da],0)

    ms_ua = sum2diff(extend2diff(signal_ua,sif.date),sif.date)
    ms_da = sum2diff(extend2diff(signal_da,sif.date),sif.date)

    signal = gand(ms_ua==1         #第一个ua
                ,bnot(ms_da)       #没出现过da 
                ,sif.s30>0
                ,sif.xatr30x<sif.mxatr30x
                #,sif.ltrend<0
                #,sif.xatr>sif.mxatr
                #,strend2(sif.mxatr15x)<0
                #,sif.ltrend<0
                )

    return signal * acd_ua.direction
acd_ua.direction = XBUY
acd_ua.priority = 1200

def acd_da(sif,sopened=None):
    '''
        +
    '''
    wave = np.zeros_like(sif.close)
    wave[sif.i_cof10] = rollx(sif.atr10) *2/3/XBASE  #掠过914-919的atr10
    wave = extend2next(wave)
    
    UA,DA,xhigh10,xlow10 = range_a(sif,914,924,wave)

    xcontinue = 5

    signal_ua = gand(sif.close >= UA
                    ,msum2(sif.close>=UA,xcontinue)>4
                    ,rollx(sif.close,xcontinue)>=UA
                    )

    signal_ua = np.select([sif.time>944],[signal_ua],0) #924之前的数据因为xhigh10是extend2next来的，所以不准

    signal_da = gand(sif.close <= DA
                    ,msum2(sif.close<=DA,xcontinue)>4
                    ,rollx(sif.close,xcontinue)<=DA
                    )

    signal_da = np.select([sif.time>944],[signal_da],0)

    ms_ua = sum2diff(extend2diff(signal_ua,sif.date),sif.date)
    ms_da = sum2diff(extend2diff(signal_da,sif.date),sif.date)

    signal = gand(ms_da==1         #第一个da
                ,bnot(ms_ua)       #没出现过ua 
                #,sif.s30<0
                ,strend2(sif.ma13)<0
                ,sif.xatr<1000
                )

    return signal * acd_da.direction
acd_da.direction = XSELL
acd_da.priority = 1200


def acd_da2(sif,sopened=None):
    '''
        +
    '''
    wave = np.zeros_like(sif.close)
    wave[sif.i_cof10] = rollx(sif.atr10) *2/3/XBASE  #掠过914-919的atr10
    wave = extend2next(wave)
    
    UA,DA,xhigh10,xlow10 = range_a(sif,914,924,wave)

    xcontinue = 5

    signal_ua = gand(sif.close >= UA
                    ,msum2(sif.close>=UA,xcontinue)>4
                    ,rollx(sif.close,xcontinue)>=UA
                    )

    signal_ua = np.select([sif.time>944],[signal_ua],0) #924之前的数据因为xhigh10是extend2next来的，所以不准

    signal_da = gand(sif.close <= DA
                    ,msum2(sif.close<=DA,xcontinue)>4
                    ,rollx(sif.close,xcontinue)<=DA
                    )

    signal_da = np.select([sif.time>944],[signal_da],0)

    ms_ua = sum2diff(extend2diff(signal_ua,sif.date),sif.date)
    ms_da = sum2diff(extend2diff(signal_da,sif.date),sif.date)

    signal = gand(ms_da==1         #第一个da
                #,bnot(ms_ua)       #没出现过ua 
                ,sif.xatr>sif.mxatr
                )

    return signal * acd_da2.direction
acd_da2.direction = XSELL
acd_da2.priority = 1200

def acd_ua_sz(sif,sopened=None):
    '''
        A点大于枢轴
        +   add
    '''

    
    wave = np.zeros_like(sif.close)
    wave[sif.i_cof10] = rollx(sif.atr10) *2/3/XBASE  #掠过914-919的atr10
    wave = extend2next(wave)
    
    UA,DA,xhigh10,xlow10 = range_a(sif,914,924,wave)

    xcontinue = 5

    signal_ua = gand(sif.close >= UA
                    ,msum2(sif.close>=UA,xcontinue)>4
                    ,rollx(sif.close,xcontinue)>=UA
                    )

    signal_ua = np.select([sif.time>944],[signal_ua],0) #924之前的数据因为xhigh10是extend2next来的，所以不准

    signal_da = gand(sif.close <= DA
                    ,msum2(sif.close<=DA,xcontinue)>4
                    ,rollx(sif.close,xcontinue)<=DA
                    )

    signal_da = np.select([sif.time>944],[signal_da],0)


    sz0 = (sif.closed+sif.highd+sif.lowd)/3
    sz2 = (sif.highd+sif.lowd)/2
    sf = np.abs(sz0-sz2)
    
    szh = np.zeros_like(sif.close)
    szh[sif.i_cofd] = sz0 + sf
    szh = extend2next(szh)

    szl = np.zeros_like(sif.close)
    szl[sif.i_cofd] = sz0 - sf
    szl = extend2next(szl)

    ms_ua = sum2diff(extend2diff(signal_ua,sif.date),sif.date)
    ms_da = sum2diff(extend2diff(signal_da,sif.date),sif.date)

    signal = gand(ms_ua == 1
                    ,bnot(ms_da)
                    ,UA >= szh
                    ,sif.ml>0
                    #,sif.xatr<1800
                    #,sif.xatr30x<sif.mxatr30x
                    ,sif.s30>0
                    )


    return signal * acd_ua_sz.direction
acd_ua_sz.direction = XBUY
acd_ua_sz.priority = 1900

def acd_ua_sz_b(sif,sopened=None):
    '''
        枢轴上限大于价幅上限，但是小于A点
        +
    '''

    wave = np.zeros_like(sif.close)
    wave[sif.i_cof10] = rollx(sif.atr10) *2/3/XBASE  #掠过914-919的atr10
    wave = extend2next(wave)
    
    UA,DA,xhigh10,xlow10 = range_a(sif,914,924,wave)

    xcontinue = 5

    signal_ua = gand(sif.close >= UA
                    ,msum2(sif.close>=UA,xcontinue)>4
                    ,rollx(sif.close,xcontinue)>=UA
                    )

    signal_ua = np.select([sif.time>944],[signal_ua],0) #924之前的数据因为xhigh10是extend2next来的，所以不准

    signal_da = gand(sif.close <= DA
                    ,msum2(sif.close<=DA,xcontinue)>4
                    ,rollx(sif.close,xcontinue)<=DA
                    )

    signal_da = np.select([sif.time>944],[signal_da],0)


    sz0 = (sif.closed+sif.highd+sif.lowd)/3
    sz2 = (sif.highd+sif.lowd)/2
    sf = np.abs(sz0-sz2)
    
    szh = np.zeros_like(sif.close)
    szh[sif.i_cofd] = sz0 + sf
    szh = extend2next(szh)

    szl = np.zeros_like(sif.close)
    szl[sif.i_cofd] = sz0 - sf
    szl = extend2next(szl)


    ms_ua = sum2diff(extend2diff(signal_ua,sif.date),sif.date)
    ms_da = sum2diff(extend2diff(signal_da,sif.date),sif.date)

    signal = gand(ms_ua == 1
                    ,bnot(ms_da)
                    ,szh>=xhigh10 #szl>=xhigh10
                    ,UA >= szh
                    ,sif.s15>0
                    ,sif.xatr<1800                    
                    )

    return signal * acd_ua_sz_b.direction
acd_ua_sz_b.direction = XBUY
acd_ua_sz_b.priority = 1900

def acd_da_sz_b(sif,sopened=None):
    '''
        枢轴下限小于A点
        过枢轴        
        +   add
    '''

    wave = np.zeros_like(sif.close)
    wave[sif.i_cof10] = rollx(sif.atr10) *2/3/XBASE  #掠过914-919的atr10
    wave = extend2next(wave)
    
    UA,DA,xhigh10,xlow10 = range_a(sif,914,924,wave)

    sz0 = (sif.closed+sif.highd+sif.lowd)/3
    sz2 = (sif.highd+sif.lowd)/2
    sf = np.abs(sz0-sz2)
    
    szh = np.zeros_like(sif.close)
    szh[sif.i_cofd] = sz0 + sf
    szh = extend2next(szh)

    szl = np.zeros_like(sif.close)
    szl[sif.i_cofd] = sz0 - sf
    szl = extend2next(szl)


    xcontinue = 5

    signal_ua = gand(sif.close >= UA
                    ,msum2(sif.close>=UA,xcontinue)>4
                    ,rollx(sif.close,xcontinue)>=UA
                    )

    signal_ua = np.select([sif.time>944],[signal_ua],0) #924之前的数据因为xhigh10是extend2next来的，所以不准

    signal_da = gand(sif.close <= szl
                    ,szl<=DA
                    ,msum2(sif.close<=szl,xcontinue)>4
                    ,rollx(sif.close,xcontinue)<=szl
                    )

    signal_da = np.select([sif.time>944],[signal_da],0)




    ms_ua = sum2diff(extend2diff(signal_ua,sif.date),sif.date)
    ms_da = sum2diff(extend2diff(signal_da,sif.date),sif.date)

    signal = gand(ms_da == 1
                    ,bnot(ms_ua)
                    ,strend2(sif.ma30)<0
                    ,sif.xatr>800
                    )

    return signal * acd_da_sz_b.direction
acd_da_sz_b.direction = XSELL
acd_da_sz_b.priority = 1900

#####突破算法
def br30(sif,sopened=None):
    '''
        5分钟最高突破开盘前30分钟最高之后，下一次1分钟上叉
        属于突破回调的模式
    '''
    
    high30 = np.select([sif.time[sif.i_cof30]==944],[sif.high30],default=0)

    xhigh30,xlow30 = np.zeros_like(sif.diff1),np.zeros_like(sif.diff1)
    xhigh30[sif.i_cof30] = high30   #因为屏蔽了前30分钟，所以i_cof30和i_oof30效果一样

    xhigh30 = extend2next(xhigh30)

    signal = np.zeros_like(sif.diff1)

    signal[sif.i_cof5] = cross(xhigh30[sif.i_cof5],sif.high5)>0

    #signal = sfollow(signal,cross(sif.dea1,sif.diff1)>0,15)
    rshort = 7
    rlong = 19
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    
    signal = sfollow(signal,cross(sif.dea1,sif.diff1)>0,15)    
    #signal = sfollow(signal,cross(rsib,rsia)>0,15)    

    signal = gand(signal
            ,sif.s30>0
            ,sif.mtrend>0
            ,sif.time < 1400    #1400以后突破基本无效
            )

    return signal * br30.direction
br30.direction = XBUY
br30.priority = 1200

def br30_old(sif,sopened=None):
    '''
        5分钟最高突破开盘前30分钟最高之后，下一次1分钟上叉
        属于突破回调的模式
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)
    
    high30 = np.select([trans[ITIME][sif.i_cof30]==944],[sif.high30],default=0)

    xhigh30,xlow30 = np.zeros_like(sif.diff1),np.zeros_like(sif.diff1)
    xhigh30[sif.i_cof30] = high30   #因为屏蔽了前30分钟，所以i_cof30和i_oof30效果一样

    xhigh30 = extend2next(xhigh30)

    signal = np.zeros_like(sif.diff1)

    signal[sif.i_cof5] = cross(xhigh30[sif.i_cof5],sif.high5)>0

    #signal = sfollow(signal,cross(sif.dea1,sif.diff1)>0,15)
    signal = sfollow(signal,cross(sif.dea1,sif.diff1)>0,15)    #20虽然更好，叠加不佳

    signal = gand(signal
            ,strend(sif.diff30-sif.dea30)>0
            ,strend(sif.diff5-sif.dea5)>0
            ,strend(sif.ma30)>0
            ,sif.ma5>sif.ma13
            ,sif.mtrend>0
            )

    return signal * br30.direction
br30_old.direction = XBUY
br30_old.priority = 1200


def godown(sif,sopened=None):
    '''
        1分钟收盘稳定击穿昨日低点后
    '''
    
 
    lowd = sif.lowd - sif.atrd/XBASE/8 

    xlowd = np.zeros(len(sif.diff1),np.int32)
    xlowd[sif.i_cofd] = lowd 

    xlowd = extend2diff(rollx(xlowd),sif.date)

    signal = gand(sif.close < xlowd
                ,msum(sif.close<xlowd,3)>1
                )

    
    signal = sum2diff(extend2diff(signal,sif.date),sif.date)    #略过了直接跳高的
    #signal = np.select([sif.time>944],[extend2diff(signal,sif.date)],0)
    #signal = sum2diff(signal,sif.date)

    signal = gand(signal==1
            ,sif.xatr30x<6000
            #,sif.xatr30x < sif.mxatr30x
            #,strend2(sif.mxatr30x)<0   #单独效果好，合并效果差
            )


    return signal * godown.direction
godown.direction = XSELL
godown.priority = 1200

###逆势算法
##沿日线上行或下降
def xma_long(sif,sopened=None,length=5):
    '''
    '''

    md = ma(sif.closed,length)
    smd = strend2(md)

    xmd = np.zeros_like(sif.close)
    xmd[sif.i_cofd] = md
    xmd = extend2next(xmd)

    xsmd = np.zeros_like(sif.close)
    xsmd[sif.i_cofd] = smd
    xsmd = extend2next(xsmd)

    signal = gand(cross(xmd+sif.atr/XBASE,sif.close)>0
                ,xsmd>0
                #,sif.s5>0
                ,sif.ma3>sif.ma13
                #,strend2(sif.ma30)>0
                ,sif.xatr30x<sif.mxatr30x
                )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)


    signal = gand(signal==1
            )
    
    return signal * xma_long.direction
xma_long.direction = XBUY
xma_long.priority = 2100


def xma_short(sif,sopened=None,length=20):
    '''
        下行途中上传阻力线后下破该线
        单独效果不好，合成效果很好
    '''
    md = ma(sif.closed,length)
    smd = strend2(md)

    xmd = np.zeros_like(sif.close)
    xmd[sif.i_cofd] = md
    xmd = extend2next(xmd)

    xsmd = np.zeros_like(sif.close)
    xsmd[sif.i_cofd] = smd
    xsmd = extend2next(xsmd)


    signal = gand(cross(xmd-sif.atr/XBASE,sif.close)<0
                ,xsmd<0
                ,sif.xatr30x<sif.mxatr30x
                )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)

    signal = gand(signal==1
            ,sif.mtrend<0
            ,sif.ml<0
            )
    
    return signal * xma_short.direction
xma_short.direction = XSELL
xma_short.priority = 2400

def xdma_long(sif,sopened=None,length=20):
    '''
        动态均线，如dma5是前四日收盘价之和加上当前分钟收盘价，然后除以5，即为当时的dma5            
        合并效果一般
    '''
    mbase = ma(sif.closed,length)
    
    mds = msum(sif.closed,length-1)

    xmds = np.zeros_like(sif.close)
    xmds[sif.i_cofd] = mds
    xmds = extend2next(xmds)

    xbase = np.zeros_like(sif.close)
    xbase[sif.i_cofd] = mbase
    xbase = extend2next(xbase)

    dma = (xmds + sif.close)/length

    signal = gand(cross(dma+sif.atr/XBASE,sif.close)>0
                ,dma>xbase
                ,sif.xatr30x<sif.mxatr30x 
                )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)

    signal = gand(signal==1
            )
    
    return signal * xdma_long.direction
xdma_long.direction = XBUY
xdma_long.priority = 2400

def xdma_short(sif,sopened=None,length=5):
    '''
        动态均线，如dma5是前四日收盘价之和加上当前分钟收盘价，然后除以5，即为当时的dma5
    '''
    mbase = ma(sif.closed,length)
    
    mds = msum(sif.closed,length-1)

    xmds = np.zeros_like(sif.close)
    xmds[sif.i_cofd] = mds
    xmds = extend2next(xmds)

    xbase = np.zeros_like(sif.close)
    xbase[sif.i_cofd] = mbase
    xbase = extend2next(xbase)

    dma = (xmds + sif.close)/length

    signal = gand(cross(dma+sif.atr/XBASE,sif.close)<0
                ,dma<xbase
                ,sif.xatr10x>sif.mxatr10x
                )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)

    signal = gand(signal==1
            ,sif.xatr<1500
            )
    
    return signal * xdma_short.direction
xdma_short.direction = XSELL
xdma_short.priority = 2400

def ma1x(sif,opened=None,length=60):
    ''' 
        1分钟均线
        第一次碰线
    '''
    bma = ma(sif.close,length)
    
    signal = cross(bma,sif.low)>0

    signal = gand(signal
                ,strend2(bma)>0
                ,sif.ltrend>0
                ,sif.mtrend>0
                ,sif.s30>0
                #,sif.xatr60x<sif.mxatr60x
                #,strend2(sif.dma7)>0
            )
    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal==1)
    
    signal = derepeatc(signal)

    return signal * ma1x.direction
ma1x.direction = XBUY
ma1x.priority = 2100

ma1x_120 = fcustom(ma1x,length=120)


def ma1xb(sif,opened=None,length=60):
    ''' 
        1分钟均线
        第一次碰线
    '''
    bma = ma(sif.close,length)
    
    signal = cross(bma,sif.low)>0

    signal = gand(signal
                ,strend2(bma)>0
                ,sif.ltrend>0
                ,sif.mtrend>0
                ,sif.s30>0
                #,sif.xatr60x<sif.mxatr60x
                #,strend2(sif.dma7)>0
            )
    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal==1)
    
    signal = derepeatc(signal)

    return signal * ma1xb.direction
ma1xb.direction = XBUY
ma1xb.priority = 2100



def k15_lastdown(sif,sopened=None):
    '''
        新高衰竭模式
        1. 15分钟新高后,15分钟内1分钟跌破前15分钟的开盘价(收盘价的低者)/最低价
    '''
    
    trans = sif.transaction

    ma15_500 = ma(sif.close15,500)
    ma15_200 = ma(sif.close15,200)
    ma15_60 = ma(sif.close15,60) 
    ma15_13 = ma(sif.close15,13)     
    ma15_30 = ma(sif.close15,30) 
    ma15_7 = ma(sif.close15,7)         
    ma15_3 = ma(sif.close15,3)         
    
    signal15 = gand(sif.high15>rollx(sif.high15)
                ,sif.low15>rollx(sif.low15)
                ,sif.high15 - gmax(sif.open15,sif.close15) > np.abs(sif.open15-sif.close15) #上影线长于实体
                ,sif.high15 == tmax(sif.high15,6)
                ,sif.high15 > gmax(ma15_3,ma15_30,ma15_60)
                #,rollx(sif.vol15) > sif.vol15
                #,rollx(sif.vol5) > rollx(sif.vol5,2)
                #,rollx(sif.close5)<rollx(sif.open5)
                ,strend2(ma15_60)>0
                ,strend2(sif.diff15x-sif.dea15x)>0
                #,sif.diff15x>sif.dea15x
                #,strend2(ma15_7)>0                                
                #,ma15_7 > ma15_13
                #,strend2(ma15_500)>0
                )

    #print np.nonzero(signal15)
    delay = 15

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof15] = signal15
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof15] = gmin(sif.open15,sif.close15)
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)
    
    #fsignal = cross(bline,sif.close)<0
    fsignal = (sif.high+sif.low+sif.close)/3 < bline
    #fsignal = cross(bline,(sif.high+sif.low+sif.close)/3)<0
    fsignal  = msum(fsignal,3)>1

    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            ,sif.xatr5x>2000
            ,sif.xatr90x<sif.mxatr90x   #大尺度不能振荡
            #,strend2(sif.mxatr30x)>0
            )
    signal = extend(signal,delay)  #去除delay时间段内的重复信号
    signal = derepeatc(signal)

    return signal * k15_lastdown.direction
k15_lastdown.direction = XSELL
k15_lastdown.priority = 2100 #对i09时200即优先级最高的效果最好
#k15_lastdown.stop_closer = atr5_uxstop_05_25

def k15_lastdown_s(sif,sopened=None):
    '''
        新高衰竭模式
        1. 15分钟新高后,15分钟内1分钟跌破前15分钟的开盘价(收盘价的低者)/最低价
    '''
    
    trans = sif.transaction

    ma15_500 = ma(sif.close15,500)
    ma15_200 = ma(sif.close15,200)
    ma15_60 = ma(sif.close15,60) 
    ma15_13 = ma(sif.close15,13)     
    ma15_30 = ma(sif.close15,30) 
    ma15_7 = ma(sif.close15,7)         
    ma15_3 = ma(sif.close15,3)         
    
    signal15 = gand(sif.high15>rollx(sif.high15)
                ,sif.low15>rollx(sif.low15)
                ,sif.high15 - gmax(sif.open15,sif.close15) > np.abs(sif.open15-sif.close15) #上影线长于实体
                ,sif.high15 == tmax(sif.high15,5)
                ,sif.high15 > gmax(ma15_3,ma15_30,ma15_60)
                #,rollx(sif.vol5) > sif.vol5
                #,rollx(sif.vol5) > rollx(sif.vol5,2)
                #,rollx(sif.close5)<rollx(sif.open5)
                ,strend2(ma15_60)>0
                ,strend2(sif.diff15x-sif.dea15x)>0
                #,sif.diff15x>sif.dea15x
                #,strend2(ma15_7)>0                                
                #,ma15_7 > ma15_13
                #,strend2(ma15_500)>0
                )

    #print np.nonzero(signal15)
    delay = 15

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof15] = signal15
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof15] = gmin(sif.open15,sif.close15)
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)
    
    #fsignal = cross(bline,sif.high)>0
    fsignal = sif.close < bline


    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            #,sif.xatr5x>1800
            #,sif.s3<0
            ,sif.strend<0
            #,sif.ma3<sif.ma13
            ,sif.xatr90x<sif.mxatr90x
            )
    signal = derepeatc(signal)

    return signal * k15_lastdown_s.direction
k15_lastdown_s.direction = XSELL
k15_lastdown_s.priority = 2105

def k15_lastdown_30(sif,sopened=None):
    '''
        15分钟调整模式
        这里最强的筛选条件是 xatr30x>8000
        说明震荡非常大. 通常是顶部震荡
        效果不错，但是叠加不好
    '''
    
    signal15 = gand(
                rollx(sif.high15,1) > rollx(sif.high15,2)
                ,rollx(sif.high15,1) > sif.high15
                )

    delay = 30

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof15] = signal15
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof15] = rollx(gmin(sif.open15,sif.close15),1)
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)

    fsignal = sif.close < bline


    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            ,sif.xatr<1500
            ,sif.xatr30x > 8000
            ,strend2(sif.mxatr)>0
            ,sif.xatr < sif.mxatr
            
            #,sif.mtrend>0
            )
    #print zip(sif.time,signal)[-270:]
    
    signal = derepeatc(signal)

    signal = np.select([sif.time>944],[signal],0)  #如果信号是从93x延续到945以后，那945是必须忽略的

    return signal * k15_lastdown_30.direction
k15_lastdown_30.direction = XSELL
k15_lastdown_30.priority = 2100 #对i09时200即优先级最高的效果最好

def k15_lastdown_x(sif,sopened=None):
    '''
        15分钟调整模式
        这里最强的筛选条件是 xatr30x>8000
        说明震荡非常大. 通常是顶部震荡
        效果不错，但是叠加不好
    '''
    
    signal15 = gand(
                rollx(sif.high15,1) > rollx(sif.high15,2)
                ,rollx(sif.high15,1) > sif.high15
                ,sif.low15 < rollx(sif.low15)
                )

    delay = 30

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof15] = signal15
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof15] = rollx(gmin(sif.open15,sif.close15),1)
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)

    fsignal = sif.close < bline

    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            ,sif.r60 < -40
            ,strend2(sif.mxatr)>0
            ,strend2(sif.mxatr30x)<0
            ,sif.xatr<sif.mxatr
            ,sif.xatr<1500
            ,sif.diff1<0
            )
    signal = derepeatc(signal)

    return signal * k15_lastdown_x.direction
k15_lastdown_x.direction = XSELL
k15_lastdown_x.priority = 2100 #对i09时200即优先级最高的效果最好


def k15_lastdown_y(sif,sopened=None):
    '''
        15分钟调整模式
        这里最强的筛选条件是 xatr30x>8000
        说明震荡非常大. 通常是顶部震荡
        效果不错，但是叠加不好
    '''
    
    signal15 = gand(
                rollx(sif.high15,1) > rollx(sif.high15,2)
                ,rollx(sif.high15,1) > sif.high15
                ,sif.low15 < rollx(sif.low15)
                )

    delay = 30

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof15] = signal15
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof15] = rollx(gmin(sif.open15,sif.close15),1)
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)

    fsignal = sif.close < bline

    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            ,strend2(sif.mxatr)>0
            ,strend2(sif.mxatr30x)<0
            ,sif.xatr<sif.mxatr
            ,sif.diff1<0
            ,sif.ma3<sif.ma13
            ,sif.r30< 0 
            ,sif.xatr<1200
            )

    signal = np.select([sif.time>944],[signal]) #允许延续过来的信号
    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal_s==1)

    return signal * k15_lastdown_y.direction
k15_lastdown_y.direction = XSELL
k15_lastdown_y.priority = 2100 #对i09时200即优先级最高的效果最好


def k15_lastdown_z(sif,sopened=None):
    '''
        15分钟调整模式
            创新高后7分钟内跌回，并且rsi下叉
        其中主条件是下叉时，跌破该15分钟的最低线            
        无任何其它附加条件
    '''
    
    signal15 = gand(sif.high15 == tmax(sif.high15,5)
                )

    delay = 7

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof15] = signal15
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof15] = sif.low15
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)

    rshort,rlong = 7,19
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)

    fsignal = gand(sif.low < bline
                ,cross(rsib,rsia)<0
                ,strend2(rsia)<0
                )

    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            )

    signal = np.select([sif.time>944],[signal]) #允许延续过来的信号
    #signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    #signal = gand(signal_s==1)

    return signal * k15_lastdown_z.direction
k15_lastdown_z.direction = XSELL
k15_lastdown_z.priority = 2100 #对i09时200即优先级最高的效果最好


def k15_lastdown_z2(sif,sopened=None):
    '''
        15分钟调整模式
            创新高后X分钟内跌回，并且rsi下叉

    '''
    
    signal15 = gand(sif.high15 == tmax(sif.high15,5)
                )

    delay = 15

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof15] = signal15
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof15] = sif.low15
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)

    rshort,rlong = 7,19
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)

    fsignal = gand(sif.low < bline
                ,cross(rsib,rsia)<0
                ,strend2(rsia)<0
                )

    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            ,strend2(sif.mxatr)>0
            #,sif.xatr > sif.mxatr
            )

    signal = np.select([sif.time>944],[signal]) #允许延续过来的信号
    #signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    #signal = gand(signal_s==1)

    return signal * k15_lastdown_z2.direction
k15_lastdown_z2.direction = XSELL
k15_lastdown_z2.priority = 2100 #对i09时200即优先级最高的效果最好


def k15_lastup_30(sif,sopened=None):
    '''
        15分钟调整后上涨模式
        这里最强的筛选条件是strend2(sif.mxatr30x)>0
        说明震荡在加大
    '''
    
    signal15 = gand(
                rollx(sif.low15,1) < rollx(sif.low15,2)
                ,rollx(sif.low15,1) < sif.low15
                )

    delay = 90

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof15] = signal15
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof15] = rollx(gmin(sif.open15,sif.close15),1)
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)

    fsignal = sif.close > bline

    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            ,sif.xatr>1000
            ,sif.xatr30x < 6000
            ,strend2(sif.mxatr30x)>0
            ,sif.xatr>sif.mxatr
            ,sif.r60>0
            )
    signal = derepeatc(signal)

    return signal * k15_lastup_30.direction
k15_lastup_30.direction = XBUY
k15_lastup_30.priority = 2100 #对i09时200即优先级最高的效果最好


def k10_lastdown_30(sif,sopened=None):
    '''
        10分钟调整模式
        这里最强的筛选条件是 xatr30x>8000
        说明震荡非常大. 通常是顶部震荡
        效果不错，但是叠加不好
    '''
    
    signal10 = gand(
                rollx(sif.high10,1) > rollx(sif.high10,2)
                ,rollx(sif.high10,1) > sif.high10
                )

    delay = 30

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof10] = signal10
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof10] = rollx(gmin(sif.open10,sif.close10),1)
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)

    fsignal = sif.close < bline

    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            ,sif.xatr<1500
            ,sif.xatr30x > 8000
            ,strend2(sif.mxatr)>0
            ,sif.mtrend>0   #说明是顶，不是途中
            ,sif.r120>0     #这个条件太强，可适当去掉以满足出现率
            )
    signal = derepeatc(signal)

    return signal * k10_lastdown_30.direction
k10_lastdown_30.direction = XSELL
k10_lastdown_30.priority = 2100 #对i09时200即优先级最高的效果最好


def k10_lastup_30(sif,sopened=None):
    '''
        10分钟调整后上涨模式
        这里最强的筛选条件是strend2(sif.mxatr30x)>0
        说明震荡在加大
    '''
    
    signal10 = gand(
                rollx(sif.low10,1) < rollx(sif.low10,2)
                ,rollx(sif.low10,1) < sif.low10
                )

    delay = 90

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof10] = signal10
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof10] = rollx(gmin(sif.open10,sif.close10),1)
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)

    fsignal = sif.close > bline

    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            ,sif.xatr>1000
            ,sif.xatr30x < 6000
            ,strend2(sif.mxatr30x)>0
            ,sif.xatr>sif.mxatr
            ,sif.r60>0
            )
    signal = derepeatc(signal)

    return signal * k10_lastup_30.direction
k10_lastup_30.direction = XBUY
k10_lastup_30.priority = 2100 #对i09时200即优先级最高的效果最好



def k5_lastup(sif,sopened=None):
    '''
        底部衰竭模式
        5分钟底部阴线后出现孕线，后10分钟内1分钟最高线突破该孕线(high+close)/2
        长期顺势，中期逆势，短期顺势
    '''
    trans = sif.transaction
 
    ma5_500 = ma(sif.close5,500)
    ma5_200 = ma(sif.close5,200)
    ma5_60 = ma(sif.close5,60) 
    ma5_13 = ma(sif.close5,13)     
    ma5_30 = ma(sif.close5,30) 
    ma5_7 = ma(sif.close5,7)         
    ma5_3 = ma(sif.close5,3)         
    
    signal5 = gand(sif.high5<rollx(sif.high5)
                ,sif.low5>rollx(sif.low5)
                ,rollx(sif.low5) == tmin(sif.low5,20)
                ,rollx(sif.vol5) > sif.vol5
                ,rollx(sif.vol5) > rollx(sif.vol5,2)
                ,rollx(sif.close5)<rollx(sif.open5)
                )

    delay = 10

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof5] = signal5
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof5] = (sif.high5 + sif.close5)/2
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)
    
    #fsignal = cross(bline,sif.high)>0
    fsignal = sif.high > bline

    #signal = np.zeros_like(sif.close)
    #signal[sif.i_cof5] = signal5

    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            ,sif.ltrend>0
            ,sif.mtrend<0            
            ,sif.mm<0
            ,strend2(sif.ma13)>0
            ,sif.ma3>sif.ma13
            ,sif.xatr<1500

            ,sif.xatr<sif.mxatr
            ,strend2(sif.mxatr)<0
            )

    signal = np.select([sif.time>944],[signal],0)

    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal_s==1)
    
    signal = derepeatc(signal)

    return signal * k5_lastup.direction
k5_lastup.direction = XBUY
k5_lastup.priority = 2100


def k5_lastup2(sif,sopened=None):
    '''
        底部衰竭模式2
        5分钟连续下跌时
            就是说这个一个返回时的压力点，10分钟内突破就突破了
        关键选择点在: r60>40
    '''
    trans = sif.transaction
 
    signal5 = gand(sif.high5<rollx(sif.high5)
                #,sif.low5>rollx(sif.low5)
                ,rollx(sif.low5) == tmin(sif.low5,12)
                #,rollx(sif.close5)<rollx(sif.open5)
             )

    delay = 10

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof5] = signal5
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof5] = sif.low5 
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)
    
    #fsignal = cross(bline,sif.high)>0
    fsignal = sif.high > bline #-100

    #signal = np.zeros_like(sif.close)
    #signal[sif.i_cof5] = signal5

    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            ,sif.mtrend<0            
            ,sif.r60>40
            ,strend2(sif.mxatr)<0
            )

    signal = np.select([sif.time>944],[signal],0)

    #signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    #signal = gand(signal_s==1)
    
    signal = derepeatc(signal)

    return signal * k5_lastup2.direction
k5_lastup2.direction = XBUY
k5_lastup2.priority = 1300  #r60>40表示是顺势


def k3_lastup2(sif,sopened=None):
    '''
        底部衰竭模式2
        5分钟连续下跌时
            就是说这个一个返回时的压力点，10分钟内突破就突破了
        关键选择点在: r60>40
    '''
    trans = sif.transaction
 
    signal3 = gand(sif.low3 == tmin(sif.low3,20)
                #,sif.high3<rollx(sif.high3)
                #,sif.low5>rollx(sif.low5)
                
                #,rollx(sif.close5)<rollx(sif.open5)
             )

    delay = 10

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof3] = signal3
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof3] = sif.high3 
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)
    
    #fsignal = cross(bline,sif.high)>0
    fsignal = sif.close > bline #-100

    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            #,sif.mtrend<0            
            #,sif.r60>40
            ,strend2(sif.mxatr)<0
            )

    signal = np.select([sif.time>944],[signal],0)

    #signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    #signal = gand(signal_s==1)
    
    signal = derepeatc(signal)

    return signal * k3_lastup2.direction
k3_lastup2.direction = XBUY
k3_lastup2.priority = 2100



def k5_lastdown(sif,sopened=None):
    '''
        顶部衰竭模式
        5分钟连续上涨时
            就是说这个一个返回时的支撑点，3分钟内击穿就击穿了
        3分钟吞没是假突破
    '''
    trans = sif.transaction
 
    signal5 = gand(
                rollx(sif.high5) == tmax(sif.high5,12) #上周期是顶点
             )

    delay = 3

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof5] = signal5
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof5] = sif.high5
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)
    
    #fsignal = cross(bline,sif.high)>0
    fsignal = sif.low < bline #-100

    #signal = np.zeros_like(sif.close)
    #signal[sif.i_cof5] = signal5

    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            ,strend2(sif.mxatr)>0
            ,sif.xatr>sif.mxatr
            ,sif.xatr30x > 8000
            ,strend2(sif.mxatr30x)>0
            ,sif.mxatr30x/sif.mxatr < 6
            )

    signal = np.select([sif.time>944],[signal],0)

    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal_s==1)
    
    signal = derepeatc(signal)

    return signal * k5_lastdown.direction
k5_lastdown.direction = XSELL
k5_lastdown.priority = 2100


def k5_lastdown2(sif,sopened=None):
    '''
        顶部衰竭模式2
        5分钟连续上涨时
            就是说这个一个返回时的支撑点，3分钟内击穿就击穿了
        3分钟吞没是假突破
    '''
    trans = sif.transaction
 
    signal5 = gand(sif.low5>rollx(sif.low5) #孕线
                ,rollx(sif.high5) == tmax(sif.high5,12) #上周期是顶点
             )

    delay = 3

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof5] = signal5
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof5] = sif.high5 
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)
    
    #fsignal = cross(bline,sif.high)>0
    fsignal = sif.low < bline #-100

    #signal = np.zeros_like(sif.close)
    #signal[sif.i_cof5] = signal5

    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            ,strend2(sif.mxatr)>0
            ,sif.xatr>sif.mxatr
            ,sif.xatr30x > 8000
            ,strend2(sif.mxatr30x)>0
            )

    signal = np.select([sif.time>944],[signal],0)

    #signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    #signal = gand(signal_s==1)
    
    signal = derepeatc(signal)

    return signal * k5_lastdown2.direction
k5_lastdown2.direction = XSELL
k5_lastdown2.priority = 2100


def k5_lastdown3(sif,sopened=None):
    '''
        顶部衰竭模式
        5分钟连续上涨时
            单根新高阴线
    '''
    trans = sif.transaction
 
    signal5 = gand(
                sif.high5 == tmax(sif.high5,5) #上周期是顶点
                #,sif.close5 - sif.open5 < 30
             )

    delay = 4

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof5] = signal5
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof5] = sif.low5
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)
    
    #fsignal = cross(bline,sif.high)>0
    fsignal = sif.low < bline #-100

    #signal = np.zeros_like(sif.close)
    #signal[sif.i_cof5] = signal5

    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            ,sif.xatr>sif.mxatr
            ,sif.xatr30x > 8000
            ,sif.xatr < 1600
            ,strend2(sif.mxatr30x)<0
            )

    #signal = np.select([sif.time>944],[signal],0)

    #signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    #signal = gand(signal_s==1)
    
    signal = derepeatc(signal)

    return signal * k5_lastdown3.direction
k5_lastdown3.direction = XSELL
k5_lastdown3.priority = 2100




def xud30s_r(sif,sopened=None):
    '''
        逆势
    '''

    mxc = xc0c(sif.open30,sif.close30,sif.high30,sif.low30,13) < 0
    signal30 = gand(mxc
                ,sif.high30 == tmax(sif.high30,9)
                )

    signal = np.zeros_like(sif.diff1)
    signal[sif.i_cof30] = signal30

    signal = gand(signal
             ,sif.xatr60x<sif.mxatr60x            
            )

    return signal * xud30s_r.direction
xud30s_r.direction = XSELL
xud30s_r.priority = 2010


##背离
def ipmacd_long_devi1(sif,sopened=None):
    '''
    '''

    msignal = ldevi(sif.low,sif.diff1,sif.dea1)

    signal = gand(msignal
            #,sif.s10<0
            ,sif.s3>0
            ,sif.xatr45x > sif.mxatr45x
            ,sif.xtrend == TREND_UP
            #,sif.xatr30x < sif.mxatr30x
            ,sif.xatr<sif.mxatr
            )

    return signal * ipmacd_long_devi1.direction
ipmacd_long_devi1.direction = XBUY
ipmacd_long_devi1.priority = 2100

def ipmacd_long_devi1b(sif,sopened=None):
    '''
    '''

    msignal = ldevi(sif.low,sif.sk,sif.sd)

    signal = gand(msignal
            ,strend2(sif.mxatr)<0
            ,sif.xatr>sif.mxatr
            ,sif.xatr30x>5000
            ,strend2(sif.mxatr30x)>0
            ,sif.xatr<1500
            )

    return signal * ipmacd_long_devi1b.direction
ipmacd_long_devi1b.direction = XBUY
ipmacd_long_devi1b.priority = 2100


def rsi_long_devi1(sif,sopened=None):
    '''
    '''

    rshort,rlong=13,41
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    signal = cross(rsib,rsia)<0    

    msignal = ldevi(sif.low,rsia,rsib)

    signal = gand(msignal
            ,sif.xatr<1200
            ,sif.s30<0
            ,sif.s3<0
            ,sif.rl_trend>0
            )

    return signal * rsi_long_devi1.direction
rsi_long_devi1.direction = XBUY
rsi_long_devi1.priority = 2100


def ipmacd_short_devi1(sif,sopened=None):
    '''
        顶背离操作，去掉了诸多条件
        尤其是xatr<2000
    '''

    trans = sif.transaction

    th = tmax(trans[IHIGH],120)
    th2 = tmax(trans[IHIGH],10)
    delta = 10 #2点

    signal = gand(hdevi(trans[IHIGH],sif.diff1,sif.dea1,delta=delta)
                ,th2 >= th - delta
                )

    fsignal = strend2(sif.diff1-sif.dea1)<0

    signal = sfollow(signal,fsignal,15)

    signal = gand(signal
                ,strend2(sif.sdiff30x)<0
                ,sif.xatr45x>sif.mxatr45x
                #,sif.xatr>sif.mxatr 
                #,strend2(sif.mxatr)>0
                #,strend2(sif.mxatr5x - sif.mxatr30x)>0
                
            )
    return signal * ipmacd_short_devi1.direction
ipmacd_short_devi1.direction = XSELL
ipmacd_short_devi1.priority = 400

def ipmacd_short_devi1x(sif,sopened=None):#+++
    ''' 
    '''

    signal = gand(hdevi(sif.high,sif.diff1,sif.dea1,delta=10)   #即便新高离上一高点低1点，仍然可视为新高
                ,sif.mm<0   #这个条件可暂时性去掉
                ,sif.xatr30x< 6666  #长期在减缩震荡,说明上行力量不够
                #震荡加大才有可能暂时下跌
                #,sif.xatr>sif.mxatr 
                #,strend2(sif.mxatr)>0
                #,strend2(sif.mxatr5x - sif.mxatr30x)>0
                )
    return signal * ipmacd_short_devi1x.direction
ipmacd_short_devi1x.direction = XSELL
ipmacd_short_devi1x.priority = 2480

def ipmacd_short_devi1y(sif,sopened=None):#+++
    ''' 
    '''

    signal = gand(hdevi(sif.high,sif.diff1,sif.dea1,delta=10)   #即便新高离上一高点低1点，仍然可视为新高
                ,sif.xatr30x< 6666  #长期在减缩震荡,说明上行力量不够
                #震荡加大才有可能暂时下跌
                ,sif.xatr>sif.mxatr 
                ,strend2(sif.mxatr)>0
                ,strend2(sif.mxatr5x - sif.mxatr30x)>0
                )
    return signal * ipmacd_short_devi1y.direction
ipmacd_short_devi1y.direction = XSELL
ipmacd_short_devi1y.priority = 2480
###from evaluate
def macd15_b(sif,sopened=None):
    sx = gand(cross(sif.dea15x,sif.diff15x)>0
                ,strend2(sif.diff15x)>0
            )
    signal = np.zeros_like(sif.close)
    signal[sif.i_cof15] = sx

    signal = gand(signal
            #,strend2(sif.ma13)>0
            #,strend2(sif.ma30)>0
            ,sif.xatr30x < sif.mxatr30x
            ,sif.xatr5x>sif.mxatr5x
            #,sif.xatr>sif.mxatr
            )
    return signal * macd15_b.direction
macd15_b.direction = XBUY
macd15_b.priority = 1500

def macd10_b(sif,sopened=None):
    sx = gand(cross(sif.dea10x,sif.diff10x)>0
                ,strend2(sif.diff10x)>0
            )
    signal = np.zeros_like(sif.close)
    signal[sif.i_cof10] = sx

    signal = gand(signal
            ,strend2(sif.ma13)>0
            ,strend2(sif.ma60)>0
            ,sif.xatr30x < sif.mxatr30x
            #,sif.xatr5x>sif.mxatr5x
            #,sif.xatr<sif.mxatr
            )
    return signal * macd10_b.direction
macd10_b.direction = XBUY
macd10_b.priority = 1500

def macd30_b(sif,sopened=None): #样本数太少
    sx = gand(cross(sif.dea30x,sif.diff30x)>0
                ,strend2(sif.diff30x)>0
            )
    signal = np.zeros_like(sif.close)
    signal[sif.i_cof30] = sx

    signal = gand(signal
            #,strend2(sif.ma13)>0
            ,strend2(sif.ma30)>0
            ,sif.xatr30x < sif.mxatr30x
            ,sif.xatr5x>sif.mxatr5x
            #,sif.xatr>sif.mxatr
            )
    return signal * macd30_b.direction
macd30_b.direction = XBUY
macd30_b.priority = 1500

def roc15_b(sif,sopened=None,length=12,malength=6):
    sr = sroc(sif.close15,length)
    msr = ma(sr,malength)

    sx = gand(cross(msr,sr)>0
             ,strend2(sr)>0
             )

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof15] = sx

    signal = gand(signal
            #,strend2(sif.ma13)>0
            ,strend2(sif.ma30)>0
            ,sif.xatr30x < sif.mxatr30x
            ,sif.xatr5x>sif.mxatr5x
            ,sif.xatr<sif.mxatr
            #,sif.xatr30x<6000
            )
    return signal * roc15_b.direction
roc15_b.direction = XBUY
roc15_b.priority = 1500

def roc5_b(sif,sopened=None,length=12,malength=6):
    sr = sroc(sif.close5,length)
    msr = ma(sr,malength)

    sx = gand(cross(msr,sr)>0
             ,strend2(sr)>0
             )

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof5] = sx

    signal = gand(signal
            ,sif.ltrend>0
            #,strend2(sif.ma13)>0
            ,strend2(sif.ma30)>0
            ,sif.s30>0
            #,sif.xatr30x < sif.mxatr30x
            ,sif.xatr5x<sif.mxatr5x
            ,sif.xatr30x<6000
            )
    return signal * roc5_b.direction
roc5_b.direction = XBUY
roc5_b.priority = 1500

def roc5_bx(sif,sopened=None,length=12,malength=6):
    sr = sroc(sif.close5,length)
    msr = ma(sr,malength)

    sx = gand(cross(msr,sr)>0
             ,strend2(sr)>0
             )

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof5] = sx

    signal = gand(signal
            ,strend2(sif.ma30)>0
            ,sif.s30>0
            ,sif.xatr30x<6000
            ,sif.xatr30x>sif.mxatr30x
            ,sif.ma13>sif.ma60
            )
    return signal * roc5_bx.direction
roc5_bx.direction = XBUY
roc5_bx.priority = 1500


def roc3_s(sif,sopened=None,length=12,malength=6):
    sr = sroc(sif.close3,length)
    msr = ma(sr,malength)

    sx = gand(#cross(msr,sr)<0
             cross(cached_zeros(len(sr)),sr)<0
             ,strend2(sr)<0
             )

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof3] = sx

    signal = gand(signal
            ,sif.mtrend<0
            ,sif.s30<0
            ,sif.s5<0
            ,sif.xatr30x<6000
            #,sif.xatr30x<sif.mxatr30x
            ,sif.xatr>sif.mxatr
            )
    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal_s==1)
    
    return signal * roc3_s.direction
roc3_s.direction = XSELL
roc3_s.priority = 1500

def roc5_s(sif,sopened=None,length=12,malength=6):
    sr = sroc(sif.close5,length)
    msr = ma(sr,malength)

    sx = gand(cross(msr,sr)<0
             ,strend2(sr)<0
             )

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof5] = sx

    signal = gand(signal
            ,sif.mtrend<0
            ,sif.s30<0
            ,sif.s5<0
            ,sif.xatr30x<6000
            ,sif.xatr>sif.mxatr
            )
    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal_s==1)
    
    return signal * roc5_s.direction
roc5_s.direction = XSELL
roc5_s.priority = 1500


def roc30_s(sif,sopened=None,length=12,malength=6):
    sr = sroc(sif.close30,length)
    msr = ma(sr,malength)

    sx = gand(#cross(msr,sr)<0
              cross(cached_zeros(len(sr)),sr)<0          
             ,strend2(sr)<0
             )

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof30] = sx

    signal = gand(signal
            #,sif.s30<0
            ,sif.s5<0
            ,sif.xatr30x<6000
            )
    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal_s==1)
    
    return signal * roc30_s.direction
roc30_s.direction = XSELL
roc30_s.priority = 1900


def roc05_s(sif,sopened=None,length=12,malength=6):
    '''穿越0线
    '''
    sr = sroc(sif.close5,length)
    msr = ma(sr,malength)

    sx = gand(#cross(msr,sr)<0
             cross(cached_zeros(len(sr)),sr)<0
             ,strend2(sr)<0
             )

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof5] = sx

    signal = gand(signal
            ,sif.mtrend<0
            ,sif.s30<0
            ,sif.s5<0
            ,sif.xatr30x<6000
            ,sif.xatr>sif.mxatr
            )
    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal_s==1)
    
    return signal * roc05_s.direction
roc05_s.direction = XSELL
roc05_s.priority = 1500


def roc10_b(sif,sopened=None,length=12,malength=6):
    sr = sroc(sif.close10,length)
    msr = ma(sr,malength)

    sx = gand(cross(msr,sr)>0
              ,strend2(sr)>0
             )

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof10] = sx

    signal = gand(signal
            #,strend2(sif.ma13)>0
            ,strend2(sif.ma30)>0
            ,sif.s30>0
            #,sif.s5>0
            ,sif.xatr30x < sif.mxatr30x
            #,sif.xatr5x<sif.mxatr5x
            ,sif.xatr<sif.mxatr
            )
    return signal * roc10_b.direction
roc10_b.direction = XBUY
roc10_b.priority = 1500

def roc1_b(sif,sopened=None,length=12,malength=6):
    sr = sroc(sif.close,length)
    msr = ma(sr,malength)

    sx = gand(cross(msr,sr)>0
             ,strend2(sr)>0
             )

    #signal = np.zeros_like(sif.close)
    #signal[sif.i_cof10] = sx
    signal = sx

    signal = gand(signal
            ,strend2(sif.ma3)>0
            ,strend2(sif.ma30)>0
            ,sif.close>rollx(sif.close)
            ,sif.s5>0
            ,sif.s10>0
            ,sif.s30>0
            ,sif.xatr<1000
            ,sif.xatr30x<6000
            #,strend2(sif.xatr30x)<0
            )
    return signal * roc1_b.direction
roc1_b.direction = XBUY
roc1_b.priority = 1500

def roc1_b000(sif,sopened=None,length=12,malength=6):
    sr = sroc(sif.close,length)/1000
    msr = ma(sr,malength)

    sx = gand(cross(msr,sr)>0
             ,strend2(sr)>0
             )

    #signal = np.zeros_like(sif.close)
    #signal[sif.i_cof10] = sx
    signal = sx

    signal = gand(signal
            #,strend2(sif.ma13)>0
            #,strend2(sif.ma30)>0
            ,sif.s5>0
            ,sif.s30>0
            ,sif.xatr30x < sif.mxatr30x
            ,sif.xatr5x<sif.mxatr5x
            #,sif.xatr<sif.mxatr
            ,sif.xatr30x>6000
            ,sif.xatr<1200
            )
    return signal * roc1_b000.direction
roc1_b000.direction = XBUY
roc1_b000.priority = 1500

def roc01_b(sif,sopened=None,length=12,malength=6):
    sr = sroc(sif.close,length)/1000
    msr = ma(sr,malength)

    sx = gand(#cross(msr,sr)>0
              cross(cached_zeros(len(sr)),sr)>0            
             ,strend2(sr)>0
             )

    #signal = np.zeros_like(sif.close)
    #signal[sif.i_cof10] = sx
    signal = sx

    signal = gand(signal
            #,strend2(sif.ma13)>0
            #,strend2(sif.ma30)>0
            ,sif.s5>0
            ,sif.s30>0
            ,sif.xatr30x < sif.mxatr30x
            #,sif.xatr5x<sif.mxatr5x
            ,sif.xatr<sif.mxatr
            )
    return signal * roc01_b.direction
roc01_b.direction = XBUY
roc01_b.priority = 1500


def mfi30s_b(sif,sopened=None,length=14,slimit=400):
    xmfi = mfi((sif.high30+sif.low30+sif.close30)/3,sif.vol30,length)
    sx = gand(cross(cached_ints(len(sif.close30),slimit),xmfi)<0,strend2(xmfi)<0)

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof30] = sx

    signal = gand(signal
            #,strend2(sif.ma13)>0
            #,strend2(sif.ma30)>0
            #,sif.s30>0
            #,sif.ltrend>0
            ,sif.xatr30x < sif.mxatr30x
            #,sif.xatr5x<sif.mxatr5x
            ,sif.xatr>sif.mxatr
            )
    return signal * mfi30s_b.direction
mfi30s_b.direction = XBUY
mfi30s_b.priority = 1500

def mfi30b_b(sif,sopened=None,length=14,slimit=400):    #样本太少
    xmfi = mfi((sif.high30+sif.low30+sif.close30)/3,sif.vol30,length)
    sx = gand(cross(cached_ints(len(sif.close30),slimit),xmfi)>0,strend2(xmfi)>0)

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof30] = sx

    signal = gand(signal
            ,strend2(sif.ma13)>0
            ,strend2(sif.ma30)>0
            ,sif.s30>0
            ,sif.xatr30x < sif.mxatr30x
            #,sif.xatr5x<sif.mxatr5x
            #,sif.xatr<sif.mxatr
            )
    return signal * mfi30b_b.direction
mfi30b_b.direction = XBUY
mfi30b_b.priority = 1500

def mfi15b_b(sif,sopened=None,length=14,slimit=700):
    xmfi = mfi((sif.high15+sif.low15+sif.close15)/3,sif.vol15,length)
    sx = gand(cross(cached_ints(len(sif.close15),slimit),xmfi)>0,strend2(xmfi)>0)

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof15] = sx

    signal = gand(signal
            ,strend2(sif.ma13)>0
            ,strend2(sif.ma30)>0
            #,sif.ltrend>0
            #,sif.s30>0
            ,sif.xatr30x < sif.mxatr30x
            #,sif.xatr5x<sif.mxatr5x
            #,sif.xatr>sif.mxatr
            )
    return signal * mfi15b_b.direction
mfi15b_b.direction = XBUY
mfi15b_b.priority = 1500

def mfi3b_b(sif,sopened=None,length=14,slimit=850):
    '''
        >700单独不错，
        >850可用于合成
    '''
    xmfi = mfi((sif.high3+sif.low3+sif.close3)/3,sif.vol3,length)
    sx = gand(cross(cached_ints(len(sif.close3),slimit),xmfi)>0,strend2(xmfi)>0)

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof3] = sx

    signal = gand(signal
            #,strend2(sif.ma13)>0
            #,strend2(sif.ma30)>0
            #,sif.ltrend>0
            ,sif.s30>0
            ,sif.xatr30x < sif.mxatr30x
            #,sif.xatr5x<sif.mxatr5x
            #,sif.xatr<sif.mxatr
            )
    return signal * mfi3b_b.direction
mfi3b_b.direction = XBUY
mfi3b_b.priority = 1500

def skdj5s_b(sif,sopened=None):
    sk,sd = skdj(sif.high5,sif.low5,sif.close5)

    sx = gand(cross(sd,sk)<0
                ,strend2(sk)<0
              )
    
    signal = np.zeros_like(sif.close)
    signal[sif.i_cof5] = sx

    signal = gand(signal
            ,strend2(sif.ma13)>0
            ,strend2(sif.ma30)>0
            #,sif.ltrend>0
            ,sif.s30>0
            ,sif.xatr30x < sif.mxatr30x
            #,sif.xatr5x>sif.mxatr5x
            ,sif.xatr<sif.mxatr
            )
    return signal * skdj5s_b.direction
skdj5s_b.direction = XBUY
skdj5s_b.priority = 1500

def skdj3s_b(sif,sopened=None):
    sk,sd = skdj(sif.high3,sif.low3,sif.close3)

    sx = gand(cross(sd,sk)<0
                ,strend2(sk)<0
              )
    
    signal = np.zeros_like(sif.close)
    signal[sif.i_cof3] = sx

    signal = gand(signal
            ,strend2(sif.ma13)>0
            ,strend2(sif.ma30)>0
            ,sif.mtrend>0
            ,sif.s30>0
            ,sif.xatr30x < sif.mxatr30x
            ,sif.xatr5x > sif.mxatr5x
            #,sif.xatr<sif.mxatr
            )
    return signal * skdj3s_b.direction
skdj3s_b.direction = XBUY
skdj3s_b.priority = 1500

def xud30b_b(sif,sopened=None):
    mxc = xc0c(sif.open30,sif.close30,sif.high30,sif.low30,13)>0

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof30] = mxc

    signal = gand(signal
            #,strend2(sif.ma13)>0
            #,strend2(sif.ma30)>0
            ,sif.mm>0
            ,sif.xatr30x < sif.mxatr30x
            #,sif.xatr5x>sif.mxatr5x
            #,sif.xatr>sif.mxatr
            )
    return signal * xud30b_b.direction
xud30b_b.direction = XBUY
xud30b_b.priority = 1500

def skdj30s_s(sif,sopened=None):
    sk,sd = skdj(sif.high30,sif.low30,sif.close30)

    sx = gand(cross(sd,sk)<0
                ,strend2(sk)<0
              )
    
    signal = np.zeros_like(sif.close)
    signal[sif.i_cof30] = sx

    signal = gand(signal
            ,strend2(sif.ma13)<0
            ,strend2(sif.ma30)<0
            #,sif.mtrend<0
            #,sif.s30>0
            ,sif.xatr30x < sif.mxatr30x
            #,sif.xatr5x > sif.mxatr5x
            ,sif.xatr<sif.mxatr
            )
    return signal * skdj30s_s.direction
skdj30s_s.direction = XSELL
skdj30s_s.priority = 1500

def skdj15s_s(sif,sopened=None):
    sk,sd = skdj(sif.high15,sif.low15,sif.close15)

    sx = gand(cross(sd,sk)<0
                ,strend2(sk)<0
              )
    
    signal = np.zeros_like(sif.close)
    signal[sif.i_cof15] = sx

    signal = gand(signal
            ,strend2(sif.ma13)<0
            ,strend2(sif.ma30)<0
            #,sif.mtrend<0
            ,sif.s5<0
            ,sif.xatr30x < sif.mxatr30x
            ,sif.xatr5x > sif.mxatr5x
            ,sif.xatr>sif.mxatr
            )
    return signal * skdj15s_s.direction
skdj15s_s.direction = XSELL
skdj15s_s.priority = 1500

def rsi60s_s(sif,sopened=None,rshort=7,rlong=19):   #样本数太少
    rsia = rsi2(sif.close60,rshort)   #7,19/13,41
    rsib = rsi2(sif.close60,rlong)
 
    sx = gand(cross(rsib,rsia)<0,strend2(rsia)<0)
    
    signal = np.zeros_like(sif.close)
    signal[sif.i_cof60] = sx

    #sk,sd = skdj(sif.high,sif.low,sif.close)
    #signal = gand(cross(sd,sk)<0,strend2(sk)<0)

    signal = gand(signal
            ,strend2(sif.ma13)<0
            ,strend2(sif.ma30)<0
            #,sif.s5<0
            ,sif.xatr30x > sif.mxatr30x
            #,sif.xatr5x > sif.mxatr5x
            #,sif.xatr>sif.mxatr
            )
    return signal * rsi60s_s.direction
rsi60s_s.direction = XSELL
rsi60s_s.priority = 1500

def rsi10b_s(sif,sopened=None,rshort=7,rlong=19):
    rsia = rsi2(sif.close10,rshort)   #7,19/13,41
    rsib = rsi2(sif.close10,rlong)
 
    sx = gand(cross(rsib,rsia)>0,strend2(rsia)>0)
    
    signal = np.zeros_like(sif.close)
    signal[sif.i_cof10] = sx

    #sk,sd = skdj(sif.high,sif.low,sif.close)
    #signal = gand(cross(sd,sk)<0,strend2(sk)<0)

    signal = gand(signal
            ,strend2(sif.ma13)<0
            ,strend2(sif.ma30)<0
            #,sif.mm<0
            #,sif.s5<0
            #,sif.xatr30x < sif.mxatr30x
            #,sif.xatr5x > sif.mxatr5x
            ,sif.xatr<sif.mxatr
            )
    return signal * rsi10b_s.direction
rsi10b_s.direction = XSELL
rsi10b_s.priority = 1500

def rsi30s_s(sif,sopened=None,rshort=7,rlong=19):
    rsia = rsi2(sif.close30,rshort)   #7,19/13,41
    rsib = rsi2(sif.close30,rlong)
 
    sx = gand(cross(rsib,rsia)<0,strend2(rsia)<0)
    
    signal = np.zeros_like(sif.close)
    signal[sif.i_cof30] = sx

    #sk,sd = skdj(sif.high,sif.low,sif.close)
    #signal = gand(cross(sd,sk)<0,strend2(sk)<0)

    signal = gand(signal
            ,strend2(sif.ma13)<0
            ,strend2(sif.ma30)<0
            #,sif.strend<0
            #,sif.s30<0
            ,sif.xatr30x < sif.mxatr30x
            #,sif.xatr5x > sif.mxatr5x
            ,sif.xatr<sif.mxatr
            )
    return signal * rsi30s_s.direction
rsi30s_s.direction = XSELL
rsi30s_s.priority = 1500

def rsi1s_s(sif,sopened=None,rshort=7,rlong=19):
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
 
    sx = gand(cross(rsib,rsia)<0,strend2(rsia)<0)
    
    #signal = np.zeros_like(sif.close)
    #signal[sif.i_cof3] = sx

    #sk,sd = skdj(sif.high,sif.low,sif.close)
    #signal = gand(cross(sd,sk)<0,strend2(sk)<0)
    
    signal = sx
    signal = gand(signal
            ,strend2(sif.ma13)<0
            ,strend2(sif.ma30)<0
            #,sif.mtrend<0
            #,sif.s3<0
            ,sif.xatr30x < sif.mxatr30x
            ,sif.xatr30x<6000
            ,sif.xatr5x < sif.mxatr5x
            #,sif.xatr>sif.mxatr
            ,sif.xatr<800
            )
    #signal = np.select([sif.time>944],[signal],0)   #允许开盘后944以前连续到944以后的信号平移到945
    
    return signal * rsi1s_s.direction
rsi1s_s.direction = XSELL
rsi1s_s.priority = 1500

def rsi1s_s2(sif,sopened=None,rshort=7,rlong=19):
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
 
    sx = gand(cross(rsib,rsia)<0,strend2(rsia)<0)
    
    #signal = np.zeros_like(sif.close)
    #signal[sif.i_cof3] = sx

    #sk,sd = skdj(sif.high,sif.low,sif.close)
    #signal = gand(cross(sd,sk)<0,strend2(sk)<0)
    
    signal = sx
    signal = gand(signal
            #,strend2(sif.ma13)<0
            ,strend2(sif.ma30)<0
            #,sif.strend<0
            #,sif.s3<0
            ,sif.xatr30x < sif.mxatr30x
            ,sif.mxatr30x<6000  #这个约束太强
            ,sif.rs_trend<0
            )
    signal = np.select([sif.time>944],[signal],0)   #允许开盘后944以前连续到944以后的信号平移到945
    
    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)  
    signal = gand(signal_s==1)
    
    
    return signal * rsi1s_s2.direction
rsi1s_s2.direction = XSELL
rsi1s_s2.priority = 1500



def macd3sb_s(sif,sopened=None):
   
    #sx = gand(cross(sif.dea30x,sif.diff30x)>0,strend2(sif.diff30x)>0)

    sx = gand(strend2(sif.diff3x-sif.dea3x)==2
                ,sif.diff3x<sif.dea3x
                ,strend2(sif.diff3x)>0
                )
    signal = np.zeros_like(sif.close)
    signal[sif.i_cof3] = sx

    signal = gand(signal
            #,strend2(sif.ma13)<0
            #,strend2(sif.ma30)<0
            ,sif.ltrend<0
            ,sif.xatr30x < sif.mxatr30x
            ,sif.xatr5x > sif.mxatr5x
            ,sif.xatr>sif.mxatr
            )
    return signal * macd3sb_s.direction
macd3sb_s.direction = XSELL
macd3sb_s.priority = 1500

def macd15s_s(sif,sopened=None):
   
    sx = gand(cross(sif.dea15x,sif.diff15x)<0,strend2(sif.diff15x)<0)

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof15] = sx
    
    signal = gand(signal
            #,strend2(sif.ma13)<0
            #,strend2(sif.ma30)<0
            ,sif.ltrend<0
            #,sif.mtrend<0
            #,sif.ms<0
            ,sif.xatr30x < sif.mxatr30x
            ,sif.xatr>sif.mxatr
            )
    return signal * macd15s_s.direction
macd15s_s.direction = XSELL
macd15s_s.priority = 1500

def macd10s_s(sif,sopened=None):
   
    sx = gand(cross(sif.dea10x,sif.diff10x)<0,strend2(sif.diff10x)<0)

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof10] = sx
    
    signal = gand(signal
            #,strend2(sif.ma13)<0
            #,strend2(sif.ma30)<0
            ,sif.ltrend<0
            #,sif.strend<0
            #,sif.ms<0
            ,sif.xatr30x < sif.mxatr30x
            ,sif.xatr5x>sif.mxatr5x
            )
    return signal * macd10s_s.direction
macd10s_s.direction = XSELL
macd10s_s.priority = 1500

def macd1s_s(sif,sopened=None):
   
    signal = gand(cross(sif.dea1,sif.diff1)<0,strend2(sif.diff1)<0)

    signal = gand(signal
            #,strend2(sif.ma13)<0
            ,strend2(sif.ma30)<0
            ,sif.ltrend<0
            #,sif.strend<0
            #,sif.ms<0
            #,sif.xatr30x > sif.mxatr30x
            ,sif.xatr5x>sif.mxatr5x
            ,sif.xatr<sif.mxatr
            #,sif.xtrend == TREND_DOWN   #顺势更有意义但合并不妥
            )
    return signal * macd1s_s.direction
macd1s_s.direction = XSELL
macd1s_s.priority = 1500

def mfi3s_s(sif,sopened=None,length=14,slimit=200):
   
    xmfi = mfi((sif.high3+sif.low3+sif.close3)/3,sif.vol3,length)
    sx = gand(cross(cached_ints(len(sif.close3),slimit),xmfi)<0,strend2(xmfi)<0)

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof3] = sx

    signal = gand(signal
            #,strend2(sif.ma13)<0
            #,strend2(sif.ma30)<0
            ,sif.ltrend<0
            #,sif.s30>0
            ,sif.xatr30x < sif.mxatr30x
            ,sif.xatr5x>sif.mxatr5x
            #,sif.xatr<sif.mxatr
            )
    return signal * mfi3s_s.direction
mfi3s_s.direction = XSELL
mfi3s_s.priority = 1500

def mfi15s_s(sif,sopened=None,length=14,slimit=200):
   
    xmfi = mfi((sif.high15+sif.low15+sif.close15)/3,sif.vol15,length)
    sx = gand(cross(cached_ints(len(sif.close15),slimit),xmfi)<0,strend2(xmfi)<0)

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof15] = sx

    signal = gand(signal
            #,strend2(sif.ma13)<0
            #,strend2(sif.ma30)<0
            ,sif.ltrend<0
            ,sif.strend<0
            #,sif.s30>0
            #,sif.xatr30x < sif.mxatr30x
            #,sif.xatr5x<sif.mxatr5x
            #,sif.xatr<sif.mxatr
            )
    return signal * mfi15s_s.direction
mfi15s_s.direction = XSELL
mfi15s_s.priority = 1500

def mfi1s_s(sif,sopened=None,length=14,slimit=200):
   
    xmfi = mfi((sif.high+sif.low+sif.close)/3,sif.vol,length)
    signal = gand(cross(cached_ints(len(sif.close),slimit),xmfi)<0,strend2(xmfi)<0)


    signal = gand(signal
            #,strend2(sif.ma13)<0
            #,strend2(sif.ma30)<0
            ,sif.ltrend<0
            #,sif.mtrend<0
            #,sif.s30>0
            ,sif.xatr30x < sif.mxatr30x
            ,sif.xatr5x>sif.mxatr5x
            ,sif.xatr>sif.mxatr
            )
    return signal * mfi1s_s.direction
mfi1s_s.direction = XSELL
mfi1s_s.priority = 1500

def roc1s_s(sif,sopened=None,length=12,malength=6):
   
    sr = sroc(sif.close,length)
    msr = ma(sr,malength)

    signal = gand(cross(msr,sr)<0
             ,strend2(sr)<0
             )

    signal = gand(signal
            ,strend2(sif.ma13)<0
            ,strend2(sif.ma30)<0
            #,sif.ltrend<0
            ,sif.mtrend<0
            ,sif.strend<0
            #,sif.ms<0
            ,sif.xatr30x < sif.mxatr30x
            ,sif.xatr5x>sif.mxatr5x
            ,sif.xatr>sif.mxatr
            )
    return signal * roc1s_s.direction
roc1s_s.direction = XSELL
roc1s_s.priority = 1500

def xud10s_s(sif,sopened=None,length=12,malength=6):
   
    mxc = xc0s(sif.open10,sif.close10,sif.high10,sif.low10,13) < 0
    signal = np.zeros_like(sif.diff1)
    signal[sif.i_cof10] = mxc


    signal = gand(signal
            #,strend2(sif.ma13)<0
            #,strend2(sif.ma30)<0
            ,sif.ltrend<0
            #,sif.mtrend<0
            #,sif.strend<0
            #,sif.ms<0
            ,sif.xatr30x < sif.mxatr30x
            ,sif.xatr5x>sif.mxatr5x
            ,sif.xatr>sif.mxatr
            )
    return signal * xud10s_s.direction
xud10s_s.direction = XSELL
xud10s_s.priority = 1500

def xud5s_s(sif,sopened=None,length=12,malength=6):
   
    mxc = xc0s(sif.open5,sif.close5,sif.high5,sif.low5,13) < 0
    signal = np.zeros_like(sif.diff1)
    signal[sif.i_cof5] = mxc


    signal = gand(signal
            #,strend2(sif.ma13)<0
            #,strend2(sif.ma30)<0
            ,sif.ltrend<0
            #,sif.mtrend<0
            #,sif.strend>0
            ,sif.ms<0
            ,sif.xatr30x < sif.mxatr30x
            ,sif.xatr5x>sif.mxatr5x
            ,sif.xatr<sif.mxatr
            )
    return signal * xud5s_s.direction
xud5s_s.direction = XSELL
xud5s_s.priority = 1500

def xud1s_s(sif,sopened=None,length=12,malength=6):
   
    signal = xc0s(sif.open,sif.close,sif.high,sif.low,13) < 0

    signal = gand(signal
            #,strend2(sif.ma13)<0
            ,strend2(sif.ma30)<0
            ,sif.ltrend<0
            #,sif.mtrend<0
            #,sif.strend<0
            #,sif.ms<0
            ,sif.xatr30x < sif.mxatr30x
            ,sif.xatr5x>sif.mxatr5x
            ,sif.xatr>sif.mxatr
            #,sif.xatr<1500
            ,sif.xatr30x<6000
            )
    return signal * xud1s_s.direction
xud1s_s.direction = XSELL
xud1s_s.priority = 1500

def xud30s_s(sif,sopened=None,length=12,malength=6):
   
    mxc = xc0s(sif.open30,sif.close30,sif.high30,sif.low30,13) < 0
    signal = np.zeros_like(sif.diff1)
    signal[sif.i_cof30] = mxc


    signal = gand(signal
            #,strend2(sif.ma13)<0
            #,strend2(sif.ma30)<0
            ,sif.ltrend<0
            #,sif.mtrend<0
            #,sif.strend<0
            #,sif.ms<0
            ,sif.xatr30x < sif.mxatr30x
            #,sif.xatr5x>sif.mxatr5x
            ,sif.xatr>sif.mxatr
            )
    return signal * xud30s_s.direction
xud30s_s.direction = XSELL
xud30s_s.priority = 1500

def macd3r_b(sif,sopened=None):
    signal = strend2(sif.diff1-sif.dea1) == 1

    signal = gand(signal
                ,sif.diff1<0
                ,sif.sdiff5x<0
                ,strend2(sif.sdiff5x-sif.sdea5x) > 0 
                ,strend2(sif.sdiff30x-sif.sdea30x) > 0 
                ,sif.xatr30x<sif.mxatr30x
                ,sif.xatr<sif.mxatr
                ,sif.xatr5x<sif.mxatr5x
                )
    return signal * macd3r_b.direction
macd3r_b.direction = XBUY
macd3r_b.priority = 1500

def macd3s(sif,sopened=None):
    '''
        找不到合适的
    '''
    signal = strend2(sif.sdiff5x-sif.sdea5x) == -1

    signal = gand(signal
                #,sif.diff1<0
                ,sif.sdiff5x<0
                ,strend2(sif.sdiff15x-sif.sdea15x) < 0 
                ,strend2(sif.sdiff45x-sif.sdea45x) < 0                 
                )
    #signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    #signal = gand(signal_s==1)
    
    return signal * macd3s.direction
macd3s.direction = XSELL
macd3s.priority = 1500

def waveb(sif,sopened=None):
    di = np.zeros_like(sif.close)
    di[sif.i_oofd] = 1
    dhigh = dmax(sif.high,di)
    dlow = dmin(sif.low,di)

    xwave = (dhigh-dlow) * XBASE*XBASE/dlow
    xmid = dlow + (dhigh-dlow)/3


    sx = gand(strend2(sif.diff3x-sif.dea3x)==-1,strend2(sif.diff3x)<0)
    signal = np.zeros_like(sif.close)
    signal[sif.i_cof3] = sx

    signal = gand(signal
            #,strend2(sif.ma13)<0
            #,strend2(sif.ma30)<0
            ,sif.ltrend<0
            ,sif.xatr30x < sif.mxatr30x
            ,strend2(sif.sdiff30x-sif.sdea30x)<0
            ,strend2(sif.sdiff10x-sif.sdea10x)<0            
            )

    return signal * waveb.direction
waveb.direction = XSELL
waveb.priority = 1500
waveb.stop_closer = atr5_uxstop_t_08_25_B2

def allup(sif,sopened=None):
    '''
        多头排列
    '''
    signal = gand(sif.ma5>sif.ma13
            ,sif.ma13>sif.ma30
            ,sif.ma30 > sif.ma120
            ,sif.ma60>sif.ma120
            ,sif.ma120>sif.ma270
            ,strend2(sif.ma270)>0
            ,sif.xatr>800
            ,sif.xatr30x<6000
            #,sif.xatr<sif.mxatr
            ,strend2(sif.mxatr30x)>0
            )
    return signal * allup.direction
allup.direction = XBUY
allup.priority = 1500


def alldown(sif,sopened=None):
    '''
        空头排列
    '''
    signal = gand(sif.ma5<sif.ma13
            ,sif.ma13<sif.ma30
            ,sif.ma30 < sif.ma120
            ,sif.ma60<sif.ma120
            ,sif.ma120<sif.ma270
            ,strend2(sif.ma270)<0
            ,sif.xatr<1000
            ,sif.xatr30x<6000
            #,strend2(sif.mxatr)<0
            ,sif.xatr30x<sif.mxatr30x
            ,sif.r60<0
            ,sif.xatr > sif.mxatr
            )
    return signal * alldown.direction
alldown.direction = XSELL
alldown.priority = 1500


evs = [roc1_b,
        #roc5_b,
        roc10_b,
        roc15_b,
        macd10_b,
        #macd15_b,
        #macd30_b,
        mfi30s_b,
        mfi15b_b,
        mfi3b_b,
        #skdj5s_b,
        #skdj3s_b,
        #xud30b_b,

        #skdj30s_s,
        #skdj15s_s,
        rsi10b_s,
        rsi30s_s,
        rsi1s_s,
        rsi1s_s2,
        macd3sb_s,
        #macd15s_s,
        #macd10s_s,
        macd1s_s,
        #mfi3s_s,
        #mfi15s_s,        
        #mfi1s_s,
        #roc1s_s,
        xud10s_s,
        xud5s_s,
        xud1s_s,
        xud30s_s,
       ]

for xf in evs:
    xf.stop_closer = atr5_uxstop_08_25_A
    #xf.stop_closer = atr5_uxstop_08_25

#roc1_b.stop_closer =  atr5_uxstop_08_25
#roc15_b.stop_closer =  atr5_uxstop_08_25
#xud10s_s.stop_closer =  atr5_uxstop_08_25

####集合


xfollow = [#多头
            #高度顺势
            rsi_long_hl,
            rsi_short_hl,
            rsi_long_hl2,

            allup,
            alldown,

            ##一般顺势
            rsi_long_x,
            rsi_long_x_1341,
            rsi_long_xx,    
            rsi_long_x2,    
            rsi_long_x3,
            #macd_long_x2,   #样本数太少，暂缓
            #macd_long_x3,   #样本数太少，暂缓
           #空头
            #rsi_short_x,
            rsi_short_x2x,
            rsi_short_x3,
            rsi_short_xt,
           
            macd_short_x,
            macd_short_xt,
            macd_short_xx,
            macd_short_x2,
            macd_short_5,
           #其它
            #down01,     #样本数太少，暂缓
            down01x,
            xdown60,    #有合并损失
            xud30b,     #趋势不明
            ma1x,            
            ma60_short,  
            ama_short, #样本数太少，
          ]

#for xf in xfollow:xf.stop_closer = atr5_uxstop_05_25
for xf in xfollow:
    xf.stop_closer = atr5_uxstop_08_25_A
    #xf.stop_closer = atr5_uxstop_08_30
    #xf.stop_closer = atr5_uxstop_08_25_C
    #xf.stop_closer = atr5_uxstop_08_25_D
    xf.strategy = XFOLLOW
    xf.max_drawdown=9

xbreak = [#多头
            acd_ua,
            acd_ua_sz, 
            #acd_ua_sz_b, #样本太少，暂缓
            br30,
          #空头
            godown,
            #acd_da, #样本太少，暂缓
            #acd_da_sz_b,#样本太少，暂缓
         ]
for xf in xbreak:
    xf.stop_closer = atr5_uxstop_08_25_A
    #xf.stop_closer = atr5_uxstop_08_25_C
    #xf.stop_closer = atr5_uxstop_08_30
    xf.strategy = XBREAK

##xagainst必须提高成功率，否则会引起最大连续回撤的快速放大. 因此对样本数暂不作限制
xagainst = [#多头
            #xma_long,  
            #xdma_long, 
            #macd_long_x,
            up0,            
            #空头
            #xma_short, #样本数太少，暂缓
            #xdma_short,    #
            k15_lastdown,
            k15_lastdown_s,    #样本数太少，暂缓
            k15_lastdown_30,    ##
            k15_lastdown_x,    ##
            k15_lastdown_y,
            k15_lastdown_z,
            k5_lastdown,
            k5_lastdown2,
            k5_lastdown3,

            k15_lastup_30,
            k10_lastup_30,  
            k10_lastdown_30,
            k5_lastup, 
            k5_lastup2, 
            #ipmacd_long_devi1,#有效放大了回撤? ##样本数太少
            ipmacd_short_devi1,##样本数太少
            ipmacd_short_devi1x, ##
            ipmacd_short_devi1y, ##            
            #xud30s_r,  ##样本数太少
           ]
#for xf in xagainst:xf.stop_closer = atr5_uxstop_08_25_A
#for xf in xagainst:xf.stop_closer = atr5_uxstop_05_25
for xf in xagainst:
    #xf.stop_closer = atr5_uxstop_08_25_C
    #xf.stop_closer = atr5_uxstop_08_30
    xf.strategy = XAGAINST

xorb_b = [##dnr1_dd_b,
        #dnr1_uu_b,
        #dnr1_ud_b,
        dpt_ux_b,
        #dp_uu_b,
        #dp_ud_b,
        n30pt_dud_b,  #
        n15pt_dd_b,    #
        ##n60pt_uu_b,
        #n60pt_uud_b,
        n60pt_dd_b,    #
        ]

xorb_b_all = [dnr1_dd_b,#+
        #dnr1_uu_b,
        #dnr1_ud_b,
        dpt_ux_b,   #+
        dp_uu_b,    #+
        #dp_ud_b,
        n30pt_dud_b,  #+
        #n15pt_dd_b,    #
        n60pt_uu_b, #+
        #n60pt_uud_b,
        n60pt_dd_b,    #+
        ]


xorb_s = [###dpt_uu_s,
          ##n30pt_du_s,
          n15pt_du_s,
          #n60pt_duu_s,
          ##nr30s   #实际上太耦合了
          ##nr30b,    #  这个也是卖空的
         ]


xorb_s_all = [dpt_uu_s,
          #n30pt_du_s,
          n15pt_du_s,
          #n60pt_duu_s,
          nr30s,   #实际上太耦合了
          #nr30b,    #  这个也是卖空的
         ]

xorb = xorb_b + xorb_s
xorb_all = xorb_b_all + xorb_s_all
for xf in xorb:
    xf.strategy = XORB    
    xf.stop_closer = atr5_uxstop_t_08_25_B
    #xf.stop_closer = atr5_uxstop_08_25_A    
    #xf.stop_closer = atr5_uxstop_05_25
    xf.filter = ocfilter_orb
    #if 'func' in xf.__dict__:   #fcustom过的部分类, 这个判断有问题
    if isinstance(xf,functools.partial):
        xf.func.priority = 1400
    else:
        xf.priority = 1400

for xf in xorb_all:
    xf.strategy = XORB   
    xf.stop_closer = atr5_uxstop_t_08_25_B
    #xf.stop_closer = atr5_uxstop_08_25_A    
    #xf.stop_closer = atr5_uxstop_05_25
    xf.filter = ocfilter_orb
    #if 'func' in xf.__dict__:    #fcustom过的部分类
    if isinstance(xf,functools.partial):
        xf.func.priority = 1400
    else:
        xf.priority = 1400
        

xevs = [
            roc1_b,
            roc10_b,
            roc5_b,
            #roc30_s,
            #roc3_s,
            #roc5_s,
            #roc05_s,
            #roc15_b,
            macd10_b,
            mfi30s_b,
            mfi3b_b,
            rsi1s_s,
            rsi1s_s2,
            macd3sb_s,
            macd1s_s,#?#
            xud5s_s,
            xud1s_s,
            xud30s_s,
            macd3r_b,            

            roc5_bx,    #xatr30x>mxatr30x
      ]

for xf in xevs:
    xf.strategy = XFOLLOW   
    xf.stop_closer = atr5_uxstop_08_25_A
    xf.priority = 1500


xevs_all = [
            #roc1_b,
            roc1_b000,
            roc10_b,
            roc5_b,
            roc30_s,
            roc3_s,
            roc5_s,
            roc05_s,
            roc15_b,
            macd10_b,
            mfi30s_b,
            mfi3b_b,
            rsi1s_s,
            macd3sb_s,
            macd1s_s,#?#
            xud5s_s,
            xud1s_s,
            xud30s_s,
            macd3r_b,   

            roc5_bx,    #xatr30x>mxatr30x
      ]

for x in xevs_all: 
    x.stop_closer = atr5_uxstop_t_08_25_B2

#重新划分顺势、逆势，不再由算法本身决定，由算法介入的时点决定



xxx2 = xfollow + xbreak + xagainst + xorb + xevs
xxx3 = xfollow + xbreak + xagainst + xorb + xevs

xxx2a = xfollow + xbreak + xagainst + xorb + xevs


for x in xxx2: 
    x.stop_closer = atr5_uxstop_t_08_25_B2


'''
16402 17617 17826 18228 18173 18494 18655 18663
'''


'''
    需要判断一直在创新高的情况
'''



