# -*- coding: utf-8 -*-


"""
解决catalog及类似问题，以及附属装置
"""

import numpy as np

from wolfox.fengine.core.d1 import *
from wolfox.fengine.core.d2 import *
from wolfox.fengine.core.source import *

RFACTOR = 1.0   #实数转换因子
INDEX_BASE = 1000

def calc_index_relative(stocks,sector=CLOSE,weight=AMOUNT,wave = 10):
    ''' 计算catalog指数并返回该指数及相关成员的序列
        按照每日的增长计算，以保持初始日期的相对稳定性
        stocks为各成员stock的d2array数组的集合
        返回d1的指数序列和
        对权重进行标准化,按排序分为1-wave共wave个级,停牌个股成交权重为nma(alen)
        这个算法因为上升放量下降缩量(导致权重变化)，导致在板块整体底部上移过程中，指数会优于个股平均
        也就是说，这个算法不具备价格稳定性
        如一个指数由两个股票组成，其价格
        A: 1000-->2000-->1000
        B: 1000-->1000-->1000
        这个过程中成交量都相等
        设第一日指数为1000，则简化运算(原理不变)，第二日指数为 (2*0.5+1*0.5)*1000 = 1500
          第三日指数为 (0.5*0.5 + 1*0.5) * 1500 = 1125
          也就是说上去一趟，下来到同一位置时指数却变化了。
          当然，一旦引入成交量因素，指数变化是必然的，但当成交量被平衡时，指数不当变化
          这个做法还是很有问题
        通过对下降段进行加权,减轻了价格波动稳定性. 其中1.25是经验数据
    '''
    csize = len(stocks)
    sectors = extract_collect(stocks,sector)
    weights = extract_collect(stocks,weight)
    #print weights
    scores = percent_sort(weights) / (PERCENT_BASE/wave) + 1 #0基改为1基, 个数少时有排序失真
    #不对停牌股进行平滑处理,是为了减轻初始日敏感性, 否则初始日停牌的个股会导致指数计算有所不同
    waves = npercent(sectors) * RFACTOR / PERCENT_BASE
    scores = np.where(waves<1.0,scores * 1.25 ,scores)   #对下降段进行加权
    s_weights = scores * RFACTOR / scores.sum(0)
    #print s_weights
    #waves = np.where(ori_waves<1.0,ori_waves*(csize-3)/(csize+3),ori_waves) #对下跌加权
    rindex = (waves * s_weights).sum(0) #当日数针对昨日数的权后增幅
    index = rindex.cumprod() * INDEX_BASE + 0.5
    return np.cast['int'](index)

calc_index = calc_index_relative    #取相对稳定性，舍弃上下一致性。因为catalog_index的用处主要在此

def calc_index_old(stocks,sector=CLOSE,weight=AMOUNT,wave = 10,alen=10):
    ''' 计算catalog指数并返回该指数及相关成员的序列，以第一日为基础
        因为初始日期的不同，而导致指数不具备相对稳定性，不同初始日计算出来的指数，连续日之间的相对比例不稳定
        stocks为各成员stock的d2array数组的集合
        返回d1的指数序列    #和d2array的每日百分排序(array序同传入的stocks序)
        对权重进行标准化,按排序分为1-wave共wave个级,停牌个股成交权重为nma(alen)
    '''
    sectors = extract_collect(stocks,sector)
    weights = extract_collect(stocks,weight)
    #print weights
    scores = percent_sort(weights) / (PERCENT_BASE/wave) + 1 #0基改为1基
    sma = nma2(scores,alen)
    #print sma
    #print scores
    zero_pos = np.where(weights == 0)
    scores[zero_pos] = sma[zero_pos]    #停牌个股
    #print zero_pos
    #print scores
    s_weights = scores * RFACTOR / scores.sum(0)
    waves = cmp_percent(sectors) / 1.0 / PERCENT_BASE
    index = (waves * s_weights).sum(0)* INDEX_BASE + 0.5    #以便下步取整时四舍五入
    return np.cast['int'](index)

def calc_index1(stocks,sector=CLOSE,weight=AMOUNT,wave = 10,alen=10):
    ''' 计算catalog指数并返回该指数及相关成员的序列，以一元为基准,以此实现相对稳定性
        stocks为各成员stock的d2array数组的集合
        返回d1的指数序列    #和d2array的每日百分排序(array序同传入的stocks序)
        对权重进行标准化,按排序分为1-wave共wave个级,停牌个股成交权重为nma(alen)
        但这个受到除权因素的影响, 因为无法对基准除权,导致除权后收盘价减低,从而存在可重复稳定性上的缺陷.
            即多日之后重新计算时,结果有所不同
    '''
    sectors = extract_collect(stocks,sector)
    weights = extract_collect(stocks,weight)
    #print weights
    scores = percent_sort(weights) / (PERCENT_BASE/wave) + 1 #0基改为1基
    sma = nma2(scores,alen)
    #print sma
    #print scores
    zero_pos = np.where(weights == 0)
    scores[zero_pos] = sma[zero_pos]    #停牌个股
    #print zero_pos
    #print scores
    s_weights = scores * RFACTOR / scores.sum(0)
    waves = sectors
    index = (waves * s_weights).sum(0) + 0.5    #以便下步取整时四舍五入
    return np.cast['int'](index)


#@wcache
def calc_drate(stocks,distance=1,sector=CLOSE,wave=100):
    ''' 计算sector的distance增长排序顺位
        用基于wave的级别表示
    '''
    sectors = extract_collect(stocks,sector)
    #print sectors
    scores = npercent(sectors,distance)
    #print percent_sort(scores)
    rate = percent_sort(scores) / (PERCENT_BASE/wave)   #0基
    return rate

#@wcache
def avg_price(stocks):
    ''' 计算stocks的平均价格，基数大时可忽略个体新增和停牌误差
    '''
    amount = extract_collect(stocks,AMOUNT) * 1.0   #避免溢出
    volume = extract_collect(stocks,VOLUME)
    sa = amount.sum(0)  #单位为百元
    sv = volume.sum(0)  #单位为手
    return np.cast['int'](sa / sv *100) #单位为分

def catalog_signal(cata_info,cata_threshold=8000,stock_threshold=8000):
    ''' 查看cata_info中是否存在catalog排序>cata_threshold,stock在该catalog中的排序>stock_threshold的信号
        cata_info:  {catalog ==> stock_order_in_catalog}
        cata_threshold: 对catalog的gorder的要求阈值
        stock_threshold: 对stock在该catalog中的排序的要求阈值，即stock_order_in_catalog
        是catalog_signal_together的特殊版本
    '''
    return gor(*[band(k.gorder >= cata_threshold,v >= stock_threshold) for k,v in cata_info.items()])

def catalog_signal_cs(cata_info,extractor):
    ''' 查看cata_info中是否存在catalog符合extractor的信号
        cata_info:  {catalog ==> stock_order_in_catalog}
        extractor: catalog,stock ==> signal序列的函数，如 lambda c,s:band(c.g60 > 5000,s.g60>5000)
    '''
    return gor(*[extractor(c,s) for c,s in cata_info.items()])

def catalog_signal_c(cata_info,extractor):
    ''' 查看cata_info中是否存在catalog符合extractor的信号
        cata_info:  {catalog ==> stock_order_in_catalog}
        extractor: catalog ==> signal序列的函数，如 lambda c:c.g60 > 5000
    '''
    return gor(*[extractor(c) for c in cata_info.keys()])

def catalog_signal_m(func,*catalogs):
    ''' 对catalogs中的各个catalog，按照顺序将其第n个value取出来，作为func的参数运算，最后or这些结果
        即gor(func(catalog1.values()[0],catalog2.values()[0],...),...,func(catalog1.values()[-1],catalog2.values()[-1]...))
        主要用于不同周期的catalog之间的比较,如c20,c60,c120的第一分量的比较
        这里依赖于不同dict之间同样的keys(插入序一致)的排序是一样的. 
            经过手工测试，这个貌似是正确的。而且理论上也该如此，key的顺序应当是稳定的(至少在插入顺序一致时)
    '''
    vvs = [ c.values() for c in catalogs ]
    pairs = zip(*vvs)
    return gor(*[func(*pair) for pair in pairs])

#deprecated
def calc_index_adjacent(stocks,sector=CLOSE):
    ''' 邻接法计算catalog指数并返回该指数及相关成员的序列
        stocks为各成员stock的d2array数组的集合
        返回d1的指数序列和d2array的每日百分排序(array序同传入的stocks序)
        这种计算不具备稳定性，同样的价格/成交量在不同的日子导致的指数是不同的
        如
            a = np.array([(0,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(1000,1000,1000,1000)])
            b = np.array([(0,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,2000,1000)])
            c = np.array([(0,0,0,0),(700,700,300,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(1000,0,1000,1000)])
            qa = CommonObject(id=3,transaction=np.array([a,b,c]))
            则qa[:,2]如果在qa[:,1]的位置，两者的指数是不一样的，分别是885和1007
    '''
    sectors = extract_collect(stocks,sector)
    volumes = extract_collect(stocks,VOLUME)
    weights = volumes * RFACTOR / volumes.sum(0)
    #指数的计算中使用邻近法，避免处理新股和停牌调整问题。
    #对于新股，第一天因为价格不变而成为稳定因素（成交量较大）。而停牌日则当日因为成交为0权重为0，而下一个开盘日则正确计算了价格差
    #因为新股之前的价格都是第一天价格，但成交为0；而停牌日的价格为前一开盘日价格，成交也为0
    #以成交量为权，能够较为简便的解决这个问题
    diffs = (increase(sectors) * (RFACTOR / PERCENT_BASE))
    diffs += 1  #每天都是前日的增加数
    #index = (diffs.cumprod(1) * weights).sum(0)* INDEX_BASE    #等同于calc_index_base_0 
    #print diffs * weights
    index = (diffs * weights).sum(0).cumprod() * INDEX_BASE + 0.5   #以便下步取整时四舍五入
    return np.cast['int'](index)

#deprecated
def calc_index_base0_old(stocks,sector=CLOSE):
    ''' 计算catalog指数并返回该指数及相关成员的序列，以第一日为基础
        stocks为各成员stock的d2array数组的集合
        返回d1的指数序列和d2array的每日百分排序(array序同传入的stocks序)
        计算是稳定的，但如果某个累计巨幅涨跌并且成交量比例大的股票某日停牌，则会导致指数在该日前后出现异常涨落
    '''
    sectors = extract_collect(stocks,sector)
    volumes = extract_collect(stocks,VOLUME)
    weights = volumes * RFACTOR / volumes.sum(0)
    #指数的计算中使用邻近法，避免处理新股和停牌调整问题。
    #对于新股，第一天因为价格不变而成为稳定因素（成交量较大）。而停牌日则当日因为成交为0权重为0，而下一个开盘日则正确计算了价格差
    #因为新股之前的价格都是第一天价格，但成交为0；而停牌日的价格为前一开盘日价格，成交也为0
    #以成交量为权，能够较为简便的解决这个问题
    diffs = (increase(sectors) * (RFACTOR / PERCENT_BASE))
    diffs += 1  #每天都是前日的增加数
    index = (diffs.cumprod(1) * weights).sum(0)* INDEX_BASE + 0.5    #等同于calc_index_base_0 
    return np.cast['int'](index)

#deprecated
def calc_index_base0(stocks,sector=CLOSE):
    ''' 计算catalog指数并返回该指数及相关成员的序列，，以第一日为基础
        stocks为各成员stock的d2array数组的集合
        返回d1的指数序列和d2array的每日百分排序(array序同传入的stocks序)
        计算是稳定的，但如果某个累计巨幅涨跌并且成交量比例大的股票某日停牌，则会导致指数在该日前后出现异常涨落        
    '''
    sectors = extract_collect(stocks,sector)
    volumes = extract_collect(stocks,VOLUME)
    weights = volumes * RFACTOR / volumes.sum(0)
    #指数的计算中使用累计法，也能避免处理新股和停牌调整问题。
    #每日指数都等同于当日交易的个股以交易量为权的价格相对于起始价格的倍数
    waves = cmp_percent(sectors) / 1.0 / PERCENT_BASE
    index = (waves * weights).sum(0)* INDEX_BASE + 0.5  #以便下步取整时四舍五入
    return np.cast['int'](index)


