# -*- coding: utf-8 -*-

#与交易和评估相关的函数

import numpy as np
from wolfox.fengine.base.common import Trade,Evaluation

import logging
logger = logging.getLogger('wolfox.fengine.core.trade')

VOLUME_BASE = 1000

def buy_first(signal):  #确认是否前进一步以废除第一个卖出信号
    return 1 if signal < 0 else 0

def sell_first(signal):  #确认是否前进一步以废除第一个买入信号
    return 1 if signal > 0 else 0

def double_first(signal):  #双向
    return 0

def make_trades(tstock,signal,tdate,tpositive,tnegative,begin=0,taxrate=125,trade_strategy=buy_first):
    ''' tstock为stock_code
        ssingal为买卖信号,对于次日买卖的信号，输入前需要将signal roll(1)
        tpositive,tnegative为信号值为正和负时的选择价格
        taxrate为税率，默认为千分之八
        begin为起始交易日
        trade_strategy为交易方式，先买后卖，先卖后买，还是均可
        以买入开始计算
    '''
    assert len(tpositive) == len(tnegative) == len(signal)
    sis = signal.nonzero()[0]  #非0信号的index    
    slen = len(sis)    
    if slen == 0:
        return []
    tbegin = tdate.searchsorted(begin)
    ibegin = sis.searchsorted(tbegin)   #tbegin在非0索引中的插入位置
    #print tbegin,ibegin
    if ibegin >= slen: #空信号
        return []
    should_skip = trade_strategy(signal[sis[ibegin]])
    ibegin += should_skip
    if ibegin >= slen: #仍然是空信号
        return []
    #print signal[tbegin:].tolist(),sis,ibegin,tbegin
    tbegin = sis[ibegin]
    trades = []
    for i in xrange(ibegin,slen):
        ci = sis[i]
        cs = signal[ci]
        price = tpositive[ci] if cs>0 else tnegative[ci]
        trades.append(Trade(tstock,tdate[ci],price,cs*VOLUME_BASE,taxrate))        
    if sum(signal[tbegin:]) != 0: #最后一个未平仓,不计算
        #print sum(signal[tbegin:]),signal[tbegin:].tolist()
        trades.pop()
    return trades

def last_trade(tstock,signal,tdate,tpositive,tnegative,begin=0,taxrate=125):
    ''' 返回值为[x]形式(无时为[])
    '''
    assert len(tpositive) == len(tnegative) == len(signal)
    sis = signal.nonzero()[0]  #非0信号的index
    tbegin = tdate.searchsorted(begin)
    ibegin = sis.searchsorted(tbegin)   #tbegin在非0索引中的插入位置
    slen = len(sis)
    if slen == 0 or sum(signal[tbegin:]) == 0 or tdate[sis[-1]] < begin: #空信号序列(实际上也是sum(signal)==0)或都已经匹配，无悬挂之买入/卖出
        return []
    last_index = sis[-1]
    cs = signal[last_index]
    price = tpositive[last_index] if cs > 0 else tnegative[last_index]
    trades= [Trade(tstock,tdate[last_index],price,cs*VOLUME_BASE,taxrate)]
    return trades

def evaluate(trades):
    ''' 对交易进行匹配和评估
        一次交易可以允许多次买卖，以单个股票存续数量为0为交易完成标志
        filter为对已经匹配成功的交易进行
        matchedtrades列表中的元素形式为：
            trade1,trade2,....,traden
            满足    所有trade的volume之和为0，并且任何前m个trade的volume之和不为0(对于买先策略为大于0)
            这个evaluate函数只有trade1,trade2两个成分，如果要一次买入多次卖出的，需要另一个evaluate
            并且要有相应的新的make_trades函数
    '''
    matchedtrades = []
    contexts = {}
    for trade in trades:
        if(trade.tstock in contexts):
            sum,items = contexts[trade.tstock]
            items.append(trade)
            sum += trade.tvolume
            if(sum == 0):#交易完成
                del contexts[trade.tstock] #以触发下一次的else (如果设置为None则第一次和每次新交易的判断不同)
                matchedtrades.append(items) 
            else:
                contexts[trade.tstock] = (sum,items)
        else:
            contexts[trade.tstock] = (trade.tvolume,[trade])
    #print matchedtrades
    for matchedtrade in matchedtrades:
        logger.debug('matched trade:%s,%s',matchedtrade[0],matchedtrade[1])
    #print '交易情况',matchedtrades,wincount,winamount,lostcount,lostamount
    return Evaluation(matchedtrades)

DEFAULT_EVALUATE_FILTER = lambda mts:mts
def gevaluate(trades,filter=DEFAULT_EVALUATE_FILTER):
    ''' 对交易进行匹配和评估
        一次交易可以允许多次买卖，以单个股票存续数量为0为交易完成标志
        filter为对已经匹配成功的交易进行
        matchedtrades列表中的元素形式为：
            trade1,trade2,....,traden
            满足    所有trade的volume之和为0，并且任何前m个trade的volume之和不为0(对于买先策略为大于0)
            这个evaluate函数只有trade1,trade2两个成分，如果要一次买入多次卖出的，需要另一个evaluate
            并且要有相应的新的make_trades函数
    '''
    matchedtrades = []
    contexts = {}
    for trade in trades:
        if(trade.tstock in contexts):
            sum,items = contexts[trade.tstock]
            items.append(trade)
            sum += trade.tvolume
            if(sum == 0):#交易完成
                del contexts[trade.tstock] #以触发下一次的else (如果设置为None则第一次和每次新交易的判断不同)
                matchedtrades.append(items) 
            else:
                contexts[trade.tstock] = (sum,items)
        else:
            contexts[trade.tstock] = (trade.tvolume,[trade])
    #print matchedtrades
    matchedtrades = filter(matchedtrades)
    for matchedtrade in matchedtrades:
        logger.debug('matched trade:%s,%s',matchedtrade[0],matchedtrade[1])
    #print '交易情况',matchedtrades,wincount,winamount,lostcount,lostamount
    return Evaluation(matchedtrades)
