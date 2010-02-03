# -*- coding: utf-8 -*-

"""
常用的算法的组合
各组合只测试是否能够执行，不测试其逻辑
"""

import numpy as np

from wolfox.fengine.core.utils import fcustom
from wolfox.fengine.core.base import *
from wolfox.fengine.core.d1 import *
from wolfox.fengine.core.d1ex import *
from wolfox.fengine.core.d1indicator import *
from wolfox.fengine.core.d1kline import *
import wolfox.fengine.core.future as f
import wolfox.fengine.core.d1ex as de

def down_period(source,covered=60):
    ''' 计算下跌周期
        covered为计算的覆盖长度
        如果当前点是covered日内的新高，则rev[i]=0
        否则rev[i]=rev[i-1]+1
    '''
    hline = rollx(tmax(source,covered)) #以前covered日为基准
    cline = greater_equals(source,hline)
    return distance(cline)

def swingin(shigh,slow,covered,threshold):
    ''' 测试shigh,slow最近covered天内的波动幅度小于threshold
        对任意i属于[0:len(shigh)),有shigh[i] >= slow[i]
        用于振幅测试，不能确认是涨上来的还是跌下去
    '''
    #print swing2(shigh,slow,covered)
    return lesser_equals(swing2(shigh,slow,covered),threshold)
    
def swingin1(source,covered,threshold):
    ''' 测试source最近covered天内的波动幅度小于threshold
        用于振幅测试，不能确认是涨上来的还是跌下去
    '''
    return lesser_equals(swing(source,covered),threshold)

def up_under(shigh,slow,covered,threshold):
    ''' 测试shigh,slow最近covered天内上升幅度小于threshold
        对任意i属于[0:len(shigh)),有shigh[i] >= slow[i]
        用于涨幅测试
    '''
    srange,sdiff = iswing2(shigh,slow,covered)
    #print srange,sdiff
    up2threshold = band(srange >= threshold,sdiff >= 0)
    #print up2threshold
    return bnot(up2threshold)

def upconfirm(sopen,sclose,shigh):#阳线突破确认
    sksize = ksize(sopen,sclose)
    sksign = ksign(sopen,sclose)
    
    posconsecutive = consecutive(sksign,'a')  #连续阳线数目
    middleconsecutive = consecutive(sksize,'b')  #连续中等实体数目

    #单根大阳线
    onebigpos = np.logical_and(sksign == 'a',sksize == 'a')
    #连续2根中等阳线
    twomiddlepos = np.logical_and( posconsecutive > 1, middleconsecutive > 1)
    #连续3根阳线
    threepos = posconsecutive > 2
    ###否决项
    #长上影三天
    threeupextend = kscmp(sopen,sclose,shigh,sclose,tbig=3000) == 'a'  #上影/实体 > 3为长

    #print kscmp(sopen,sclose,shigh,tmax(sopen,sclose),tbig=3000)
    sconfirm = gor(onebigpos,twomiddlepos,threepos)
    #return sconfirm
    return band(sconfirm,np.logical_not(threeupextend))

def upveto(sopen,sclose,shigh,slow):   #上升否决情况
    sksize = ksize(sopen,sclose)
    sksign = ksign(sopen,sclose)

    negconsecutive = consecutive(sksign,'b')  #连续阴线数目
    middleconsecutive = consecutive(sksize,'b')  #连续中等实体数目
    smallconsecutive = consecutive(sksize,'c')  #连续小实体数目
    
    #大阴线
    onebig = np.logical_and(sksign == 'b',sksize == 'a')
    #连续两根中阴线
    twomiddle = np.logical_and(negconsecutive > 1,middleconsecutive > 1)
    #连续三根小阴线
    threesmall = np.logical_and(negconsecutive > 2,smallconsecutive > 2)

    return gor(onebig,twomiddle,threesmall)

def sellconfirm(sopen,sclose,shigh,slow):   #卖出确认情况：非大阳或者中阳
    sksize = ksize(sopen,sclose)
    sksign = ksign(sopen,sclose)
    #大或中阳线
    big_or_middle = np.logical_or(sksize == 'a',sksize =='b')
    bm_and_pos = np.logical_and(sksign == 'a',big_or_middle)
    return bnot(bm_and_pos)

####sell_func必须对stock.downlimit进行赋值
def simplesell(sbuy,shigh,slow,threshold):
    downl = downlimit(shigh,sbuy,threshold)
    return slow - downl < 0

def tsimplesell(sbuy,shigh,slow,threshold):
    downl = tdownlimit(shigh,sbuy,threshold)
    return slow - downl < 0

def confirmedsell(sbuy,sopen,sclose,shigh,slow,ssignal,threshold):  #ssignal为出发卖出界限的那条线，一般为sclose或slow
    downl = downlimit(shigh,sbuy,threshold)
    return band(ssignal-downl <0,sellconfirm(sopen,sclose,shigh,slow))   #返回int值便于参加运算和转换

def confirmedselll(sbuy,sopen,sclose,shigh,slow,threshold): #以slow为出发条件
    downl = downlimit(shigh,sbuy,threshold)
    return band(slow-downl <0,sellconfirm(sopen,sclose,shigh,slow))   #返回int值便于参加运算和转换

def confirmedsellc(sbuy,sopen,sclose,shigh,slow,threshold): #以sclose为出发条件
    downl = downlimit(shigh,sbuy,threshold)
    return band(sclose-downl <0,sellconfirm(sopen,sclose,shigh,slow)) #返回int值便于参加运算和转换

def downup(source1,source2,belowdays,crossdays=3):
    ''' 判断source2先在source1之上，然后crossdays日内(为避免重合，默认为3)翻下，停留n天后翻上
    '''
    s2_1 = source2 - source1
    s2_lt_1 = s2_1 < 0 #tfilter_lt(s2_1)
    s2_gt_1 = s2_1 > 0 # tfilter_gt(s2_1)
    sdown = sfollow(s2_gt_1,s2_lt_1,crossdays)
    sdown_up = sfollow(sdown,s2_gt_1,belowdays)  #belowdays之内回去
    return sdown_up

def _limit_adjuster_deprecated(css,cls,covered):#covered不能大于127否则会溢出, np.sign(bool array)返回的是int8数组
    ''' css:压缩后的source_signal,cls:压缩后的limit_signal
        屏蔽cls非空日的那些css信号,使其延后到covered之内的非停板日,或者取消(后面的covered日都停板)
        返回处理后的css
        这里的做法是先按covered段展开信号，挖空其停板日，然后再进行derepeat。这个做法太无聊了，废弃
        存在问题是信号的吸收，本来相隔covered-1有2个卖出信号，后一个信号本来应该延续covered个位置,但这里被忽略了. 
            这个忽略因为是在covered之内的新信号,当covered较小时,不会有实质影响(因为可能这个间隔还没出现卖出信号,故此新买入为无效信号)
            如果采用cover来替代repeat,使得这类信号延续,则转换后会因为停板的存在导致中间断开从而这个信号被推迟,更为不妥
    '''
    css_covered = repeat(css,covered)
    #print css,cls,css_covered,derepeat(band(css_covered>0,bnot(cls)))
    #print '_ad',band(css_covered > 0,bnot(cls))[-20:-5].tolist(),derepeat(band(css_covered > 0,bnot(cls)),covered)[-20:-5].tolist()
    return derepeat(band(css_covered > 0,bnot(cls)),covered)    
    
def limit_adjust_deprecated(source_signal,limit_signal,trans_signal,covered=10):#covered不能大于127否则会溢出, np.sign(bool array)返回的是int8数组
    ''' 根据停板信号limit_signal和交易日信号trans_signal调整原始信号，使原始信号避开停板到开板日
        可能因covered的原因导致连续非停板日中间出现停板日后,信号多发. 但这个可由makke_trade之类的函数处理掉
        只有covered=2时,不会出现这个情况
        covered=10，最多10个停板，超过则可能导致跌停情况下卖出信号被忽略
    '''
    adjuster = fcustom(_limit_adjuster_deprecated,covered=covered)
    return smooth(trans_signal,source_signal,limit_signal,sfunc=adjuster)

def limit_adjust(source_signal,limit_signal,trans_signal):
    ''' 根据停板信号limit_signal和交易日信号trans_signal调整原始信号，使原始信号避开停板到开板日
        将停板日也视同停牌日
    '''
    signal2 = band(trans_signal,limit_signal==0) #交易日必须满足不是同向停板日
    return smooth_simple(signal2,source_signal)

def BS_DUMMY(trans,sbuy,ssell):
    return sbuy,ssell

def B0S0(trans,sbuy,ssell):
    ''' 买卖信号都在当日实现
        t为stock.transaction
        返回经过信号延续、停板和停牌处理的sbuy,ssell
    '''
    #print 'input rolled:',sbuy,ssell
    up_limit_line = limitup1(trans[CLOSE])
    down_limit_line = limitdown1(trans[CLOSE])
    #print 'begin adjust:',up_limit_line,down_limit_line
    sbuy = limit_adjust(sbuy,up_limit_line,trans[VOLUME])
    #print ssell[-20:-5].tolist(),down_limit_line[-20:-5]
    ssell = limit_adjust(ssell,down_limit_line,trans[VOLUME])
    #print ssell[-20:-5].tolist()
    #print 'end adjust:',ssell
    return sbuy,ssell

def B0S0_N(trans,sbuy,ssell):
    ''' 买卖信号都在当日实现
        t为stock.transaction
        买入不对停板进行处理
        卖出只限制一字板
    '''
    down_limit_line = limitdown2(trans[HIGH],trans[LOW])
    ssell = limit_adjust(ssell,down_limit_line,trans[VOLUME])
    return sbuy,ssell

def B0S1(trans,sbuy,ssell):
    ''' 买入信号当日,卖出信号次日
        t为stock.transaction
        返回经过信号延续、停板和停牌处理的sbuy,ssell
    '''
    ssell = roll0(ssell)
    #print 'input rolled:',sbuy,ssell
    up_limit_line = limitup1(trans[CLOSE])
    down_limit_line = limitdown2(trans[HIGH],trans[LOW])
    #print 'begin adjust:',up_limit_line,down_limit_line,trans[VOLUME]
    sbuy = limit_adjust(sbuy,up_limit_line,trans[VOLUME])
    ssell = limit_adjust(ssell,down_limit_line,trans[VOLUME])
    #print 'end adjust:',ssell
    return sbuy,ssell

def B1S0(trans,sbuy,ssell):
    ''' 买入次日,卖出当日
        t为stock.transaction
        返回经过信号延续、停板和停牌处理的sbuy,ssell
        次日买入只受到一字线影响，而当日卖出受到收盘跌停影响
    '''
    #print 'input:%s',sbuy.tolist()
    sbuy = roll0(sbuy)
    #print 'input,after roll:%s',sbuy.tolist()
    #print 'input rolled:',sbuy,ssell
    up_limit_line = limitup2(trans[HIGH],trans[LOW])
    down_limit_line = limitdown1(trans[CLOSE])
    #print 'begin adjust:',up_limit_line,down_limit_line,trans[VOLUME],sbuy
    sbuy = limit_adjust(sbuy,up_limit_line,trans[VOLUME])
    ssell = limit_adjust(ssell,down_limit_line,trans[VOLUME])
    #print 'after limit adjust:%s',sbuy.tolist()    
    #print 'end adjust:',ssell
    return sbuy,ssell

def B1S1(trans,sbuy,ssell):
    ''' 买卖信号都是次日实现
        trans为stock.transaction
        返回经过信号延续、停板和停牌处理的sbuy,ssell
        次日买卖则只受到一字线的影响
    '''
    #print sbuy,np.sum(sbuy)
    sbuy,ssell = roll0(sbuy),roll0(ssell)
    #print ssell
    #print 'input rolled:',sbuy,ssell
    up_limit_line = limitup2(trans[HIGH],trans[LOW])
    down_limit_line = limitdown2(trans[HIGH],trans[LOW])
    #print trans[VOLUME]
    #print 'begin adjust:',up_limit_line,down_limit_line
    sbuy = limit_adjust(sbuy,up_limit_line,trans[VOLUME])
    ssell = limit_adjust(ssell,down_limit_line,trans[VOLUME])
    #print 'end adjust:',ssell
    #print sbuy,np.sum(sbuy)
    #print ssell
    return sbuy,ssell

B0S0.bshift = B0S0_N.bshift = B0S1.bshift = lambda s : s   #bshift是对buy信号的处理,生成卖出信号用. B0系列不用偏移。
B1S0.bshift = B1S1.bshift = lambda s : rollx(s)   #bshift是对buy信号的处理,生成卖出信号用. B1系列右移一位

def atr_sell_func(sbuy,trans,satr,stop_times=3*BASE/2,trace_times=2*BASE,covered=10,up_sector=HIGH): 
    ''' 
        times为以0.001为单位的倍数
        存在问题：如果当日开盘最低收盘涨停，而之前的atr很小，则会被触发。
        解决方法是downlimit延后一天,或者判断当日是否是此种情况。延后一天也有问题，即第一日问题（其down_limit未修正）
        目前的做法是以开盘+收盘/2即中间价为downlimit的起始基准
    '''
    #down_limit = tmax(trans[HIGH] - satr * times / BASE,covered)    #最近covered天波动下限的最大值
    down_limit = tracelimit((trans[OPEN]+trans[CLOSE])/2,trans[up_sector],trans[LOW],sbuy,satr,stop_times,trace_times) 
    #sdown = equals(cross(down_limit,trans[LOW]),-1)     #触及
    sdown = under_cross(sbuy,down_limit,trans[LOW])
    #return band(sdown,sellconfirm(trans[OPEN],trans[CLOSE],trans[HIGH],trans[LOW])),down_limit
    return sdown,down_limit

def atr_sell_func_old(sbuy,trans,satr,times=BASE,covered=10,sector=LOW): 
    ''' 
        times为以0.001为单位的倍数
    '''
    down_limit = tmax(trans[HIGH] - satr * times / BASE,covered)    #最近covered天波动下限的最大值
    #sdown = equals(cross(down_limit,trans[sector]),-1)     #最低价触及
    sdown = under_cross(sbuy,down_limit,trans[sector])
    return band(sdown,sellconfirm(trans[OPEN],trans[CLOSE],trans[HIGH],trans[LOW])),down_limit

def atr_seller(stock,buy_signal,stop_times=3*BASE/2,trace_times=2*BASE,covered=10,up_sector=HIGH,**kwargs): 
    ''' kwargs目的是吸收无用参数，便于cruiser
        times为0.001为单位的倍数
        covered是求最近最高点的范围长
        是d1idiom.atr_seller的简单包装
    '''
    trans = stock.transaction
    ssignal,down_limit = atr_sell_func(buy_signal,trans,stock.atr,stop_times,trace_times,covered,up_sector)
    stock.down_limit = down_limit
    #print buy_signal - ssignal
    return ssignal

def atr_seller_factory(stop_times=3*BASE/2,trace_times=2*BASE,covered=10,up_sector=HIGH):
    return fcustom(atr_seller,stop_times=stop_times,trace_times=trace_times,covered=covered,up_sector=up_sector)

def atr_xseller_factory(stop_times=3*BASE/2,trace_times=2*BASE,covered=10,up_sector=HIGH):
    ''' 用于评估的seller_factory
        将倒数第二个信号位置位，使得所有开仓合约平仓
    '''
    inner_seller = fcustom(atr_seller,stop_times=stop_times,trace_times=trace_times,covered=covered,up_sector=up_sector)
    def seller(stock,buy_signal,**kwargs):
        ss = inner_seller(stock,buy_signal,*kwargs)
        twhere = np.where(stock.transaction[VOLUME] > 0)[0]
        if len(twhere) and twhere[-1] - 1 >= 0:
            ss[twhere[-1]-1] = 1  #最后交易日之前的那一天置位，以便最后卖出平仓。
        return ss
    return seller

def sellers_wrapper(*sellers):
    def seller(stock,buy_signal,**kwargs):
        ss = np.zeros_like(buy_signal)
        for s in sellers:
            cs = s(stock,buy_signal,**kwargs)
            ss = bor(ss,cs)
        return ss
    return seller
    
def vdis(sopen,sclose,shigh,slow,svolume):
    ''' 功率含义的比较，但是很难应用
        up,uf,dp,df = vdis(t[OPEN],t[CLOSE],t[HIGH],t[LOW],t[VOLUME])
    '''
    su,sd = supdown(sopen,sclose,shigh,slow)
    x = f.xpeak_points_2(shigh,slow,11)
    uv = svolume * su / (su+sd)
    dv = svolume - uv
    uvx = de.rsum2(uv,x)
    dvx = de.rsum2(dv,x)
    cl = np.log(sclose)
    clx = de.rsub(cl,x)
    dx = de.distance2(x)
    xd = np.where(x!=0)[0]
    #ue1 = (uv/clx/dx)[xd]
    #ue2 = (uv/clx/dx/dx)[xd]
    #de1 = (dv/clx/dx)[xd]
    #de2 = (dv/clx/dx/dx)[xd]
    #return xd,ue1,ue2,de1,de2
    #e1 = (np.abs((uv-dv))/clx/dx)[xd]
    #e2 = (np.abs((uv-dv))/clx/dx/dx)[xd]
    #return xd,e1,e2,uv-dv
    return (uv/dx)[xd],(uv/clx)[xd],(dv/dx)[xd],(dv/clx)[xd]


####ru系列指标的-1信号都是重要的卖出信号，尤其是前导1无后续1的-1
def xc_ru(sopen,sclose,shigh,slow,svolume,ma1=13,ma2=9,udfunc=supdown):
    '''
        上升比例的交叉值
        xc = xc_ru(t[OPEN],t[CLOSE],t[HIGH],t[LOW],t[VOLUME])
        如果直接用 ru = uv/(uv+ud) = su/(su+sd),则信号太过频繁
        目前的结果是必须再等一天看看是否有反向信号
    '''
    su,sd = udfunc(sopen,sclose,shigh,slow)
    uv = svolume * 1.0 *su / (su+sd)
    dv = svolume - uv
    uvma=nma(uv,ma1)
    dvma=nma(dv,ma1)
    ru = uvma*1.0/(uvma+dvma)
    ruma=msum2(ru,ma2)/ma2  #nma只能计算整数
    xc = cross(ruma,ru)
    return np.cast['int32'](xc)

def xc_ru2(sopen,sclose,shigh,slow,svolume,ma1=13,ma2=9):
    '''
        上升比例的交叉值，采用supdown2
        xc = xc_ru(t[OPEN],t[CLOSE],t[HIGH],t[LOW],t[VOLUME])
        如果直接用 ru = uv/(uv+ud) = su/(su+sd),则信号太过频繁
        目前的结果是必须再等一天看看是否有反向信号
        效果不如xc_ru
    '''
    return xc_ru(sopen,sclose,shigh,slow,svolume,ma1,ma2,supdown2)    

def xc_ru0(sopen,sclose,shigh,slow,svolume,ma1=13,udfunc=supdown):
    '''
        上升比例穿越0线
    '''
    su,sd = udfunc(sopen,sclose,shigh,slow)
    uv = svolume * 1.0 * su / (su+sd)
    dv = svolume - uv
    mru = ma(uv-dv,ma1)
    zx = cached_zeros(len(sclose))
    xc = cross(zx,mru)
    return np.cast['int32'](xc)

def xc_ru02(sopen,sclose,shigh,slow,svolume,ma1=13):
    '''
        上升比例穿越0线,supdown2
    '''
    return xc_ru0(sopen,sclose,shigh,slow,svolume,ma1,supdown2)

def xc_ru0s(sopen,sclose,shigh,slow,svolume,ma1=13):
    '''
        上升比例穿越0线,supdowns
    '''
    return xc_ru0(sopen,sclose,shigh,slow,svolume,ma1,supdowns)    

def xc_ru0c(sopen,sclose,shigh,slow,svolume,ma1=13):
    '''
        上升比例穿越0线,supdownc
    '''
    return xc_ru0(sopen,sclose,shigh,slow,svolume,ma1,supdownc)    

def xc0(sopen,sclose,shigh,slow,ma1=13,udfunc=supdown):
    '''
        上升比例穿越0线
    '''
    su,sd = udfunc(sopen,sclose,shigh,slow)
    zx = cached_zeros(len(sclose))
    msu = cexpma(su,ma1)
    msd = cexpma(sd,ma1)
    xc = cross(zx,msu-msd)
    return xc

def xc02(sopen,sclose,shigh,slow,ma1=13):
    '''
        上升比例穿越0线,supdown2
    '''
    return xc0(sopen,sclose,shigh,slow,ma1,supdown2)

def xc0s(sopen,sclose,shigh,slow,ma1=13):
    '''
        上升比例穿越0线,supdowns
    '''
    return xc0(sopen,sclose,shigh,slow,ma1,supdowns)    

def xc0c(sopen,sclose,shigh,slow,ma1=13):
    '''
        上升比例穿越0线,supdownc
    '''
    return xc0(sopen,sclose,shigh,slow,ma1,supdownc)    

def macd_ru(sopen,sclose,shigh,slow,udfunc=supdown):
    '''
        上升比例的macd
        vdiff,vdea = macd_ru(t[OPEN],t[CLOSE],t[HIGH],t[LOW])        
        貌似没有xc_ru有效
    '''
    su,sd = udfunc(sopen,sclose,shigh,slow)
    ru = su *BASE / (su+sd)
    return cmacd(ru)

def macd_ru2(sopen,sclose,shigh,slow):
    '''
        上升比例的macd
        vdiff,vdea = macd_ru2(t[OPEN],t[CLOSE],t[HIGH],t[LOW])        
        貌似其cross比较有效
        特别是如果1/-1或-1/1近邻时，后面的那一个准确率大大提高
            如果1/-1后为0，则相当于确认了1/-1信号的有效性
        比较有效
    '''
    return macd_ru(sopen,sclose,shigh,slow,supdown2)

def macd_ruv(sopen,sclose,shigh,slow,svolume):
    '''
        上升V的macd
        vdiff,vdea = macd_ru2(t[OPEN],t[CLOSE],t[HIGH],t[LOW],t[VOLUME])        
        貌似其cross比较有效
        特别是如果1/-1或-1/1近邻时，后面的那一个准确率大大提高
            如果1/-1后为0，则相当于确认了1/-1信号的有效性
        貌似也有效
    '''
    su,sd = supdown2(sopen,sclose,shigh,slow)
    ruv = su * svolume / (su+sd)
    return cmacd(ruv)

def macd_ruv3(sopen,sclose,shigh,slow,svolume):
    '''
        上升V的macd，使用supdown3
    '''
    su,sd = de.supdown3(sopen,sclose,shigh,slow)
    ruv = su * svolume / (su+sd)
    return cmacd(ruv)

def macd_rv(sopen,sclose,shigh,slow,svolume):
    '''
        实际动力V的macd，使用supdowns
    '''
    su,sd = de.supdowns(sopen,sclose,shigh,slow)
    ruv = (su-sd) * svolume / (su+sd)
    mruv = ma(ruv,10)
    return cmacd(mruv)

def vdeviate_seller(stock,buy_signal,**kwargs): #成交量背离
    ''' >3阳线且创60日新高，成交量未创出10日正量新高
        是否c2足够？不是，如果是连创新高的情形，不需要放量
        再加筛选，如果涨幅超过7.5%，是不是不受约束? 不好
        #实际操作中，对连续上涨的情况，还需要结合前一日的情形，如果比前一日放量，则没事 #太琐碎，去掉
        违反这个背离继续上涨的(三个交易日内没有跌破5日线)，则空间很大，需要及时买回
        这个终究是小伎俩，容易错失大的上升，如600756-0324，上去了就买不回来
        作废，除非给出精炼的判断
        或者信号给出之后需要确认, 只有当n天之内确认信号出现,才可
        确认信号可以为: 
            1. 跳出阴线, 当天CLOSE<OPEN但大于前一日收盘,且比前10日最大量*1.1要大. 收盘前如果确认即可卖出
            2. 下跌阴线, 当天CLOSE<前一日CLOSE,且量>前一日量
         且确认信号的发出都在13日均线之上.之下的话直接等止损信号
    但是必须注意,在atr没有跌破之前,这个卖出只是之后买入的一次短差!!!
    因此，实际应用中，此seller只做目测。不介入到信号机制中
    '''
    t = stock.transaction
    lc = rollx(t[CLOSE])
    lv = rollx(t[VOLUME])
    c1a = t[CLOSE] > lc * 1.02 #实际上升大于2%
    lm60 = rollx(tmax(t[HIGH],60))  #最近60日高点
    positive_v = np.where(t[CLOSE] >= lc,t[VOLUME],0)  #正量
    lv10 = rollx(tmax(positive_v,10))   #最近10日正量高点
    #lv10 = rollx(tmax(t[VOLUME],10))   #最近10日高点
    c1b = gand(t[CLOSE] > lm60 * 1.005,t[VOLUME] < lv10 * 1.1)
    mv = ma(t[VOLUME],30)
    #c2 = t[VOLUME] > mv * 3
    #c2 = gand(t[VOLUME] > mv * 2.5,bor(t[CLOSE]<t[OPEN],t[CLOSE]<lc))   #大阴量，大阳量由c1a & c1b负责
    c2 = t[VOLUME] > mv * 2.5 #不论阴阳，只要被确认就有问题
    first = bor(gand(c1a,c1b),c2)
    #first = gand(c1a,c1b)
    cc1 = gand(t[CLOSE]<t[OPEN],t[CLOSE]>lc,t[VOLUME] > lv10*1.1)
    cc2 = gand(t[CLOSE]<lc,t[VOLUME] > lv)
    confirm = gand(bor(cc1,cc2),t[CLOSE]>ma(t[CLOSE],13))
    
    confirmed = gand(rollx(first),confirm)  #发生背离后立刻确认

    return confirmed

