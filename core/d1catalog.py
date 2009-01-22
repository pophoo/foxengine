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

class dispatch(object):
    """ 将(name,stocks,*args,**kwargs)形式的调用结果(array形式)dispatch到stock中相应name的属性中
        要求被修饰函数的签名为(stocks,*args,**kwargs)
    """
    def __init__(self, func):
        self.func = func
    
    def __call__(self,name,stocks,*args,**kwargs):
        datas = self.func(stocks,*args,**kwargs)
        #print datas
        for s,data in zip(stocks,datas):
            s.__dict__[name] = data
        return datas

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__


class cdispatch(object):
    """ 将(name,catalogs,*args,**kwargs)形式的调用结果(array形式)dispatch到stock中相应name属性表示的dict中，dict[catalog_id] = v
        要求被修饰函数的签名为(stocks,*args,**kwargs)
        #需要一个准集成测试
    """
    def __init__(self, func):
        self.func = func
    
    def __call__(self,name,catalogs,*args,**kwargs):
        for c in catalogs:
            self._dispatch(name,c,*args,**kwargs)

    def _dispatch(self,name,catalog,*args,**kwargs):
        datas = self.func(catalog.stocks,*args,**kwargs)
        #print datas
        for s,data in zip(catalog.stocks,datas):
            s.__dict__.setdefault(name,{})[catalog] = data  #这样，这个dict的item就是(catalog,data)
        return datas

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__


@dispatch
def dispatch_example(stocks,ma=10):
    try:
        return extract_collect(stocks)
    except Exception,inst: #没有交易数据
        #print np.array([[] for s in stocks]).tolist()
        return np.array([[] for s in stocks])

@wcache
def calc_index(stocks,sector=CLOSE,weight=AMOUNT,wave = 10,alen=10):
    ''' 计算catalog指数并返回该指数及相关成员的序列，以第一日为基础
        stocks为各成员stock的d2array数组的集合
        返回d1的指数序列和d2array的每日百分排序(array序同传入的stocks序)
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
    scores[zero_pos] = sma[zero_pos]
    #print zero_pos
    #print scores
    s_weights = scores * RFACTOR / scores.sum(0)
    waves = cmp_percent(sectors) / 1.0 / PERCENT_BASE
    index = (waves * s_weights).sum(0)* INDEX_BASE + 0.5    #以便下步取整时四舍五入
    return np.cast['int'](index)

@wcache
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

@wcache
def avg_price(stocks):
    ''' 计算stocks的平均价格，基数大时可忽略个体新增和停牌误差
    '''
    amount = extract_collect(stocks,AMOUNT) * 1.0   #避免溢出
    volume = extract_collect(stocks,VOLUME)
    sa = amount.sum(0)  #单位为百元
    sv = volume.sum(0)  #单位为手
    return np.cast['int'](sa / sv *100) #单位为分

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


