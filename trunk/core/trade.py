# -*- coding: utf-8 -*-

#与交易和评估相关的函数

import numpy as np
from wolfox.common.tcommon import Trade,Evaluation

VOLUMEBASE = 1000

def make_trades(tstock,signal,tdate,tpositive,tnegative,begin=0,taxrate=125):
    ''' tstock为stock_id
        ssingal为买卖信号,对于次日买卖的信号，输入前需要将signal roll(1)
        tpositive,tnegative为信号值为正和负时的选择价格
        taxrate为税率，默认为千分之八
        begin为起始交易日
    '''
    assert len(tpositive) == len(tnegative) == len(signal)
    sis = signal.nonzero()[0]  #非0信号的index    
    tbegin = tdate.searchsorted(begin)
    ibegin = sis.searchsorted(tbegin)   #tbegin在非0索引中的插入位置
    #print tbegin,ibegin
    slen = len(sis)
    if slen == 0 or ibegin == slen: #空信号
        return []
    trades = []
    for i in xrange(ibegin,slen):
        ci = sis[i]
        cs = signal[ci]
        price = tpositive[ci] if cs>0 else tnegative[ci]
        trades.append(Trade(tstock,tdate[ci],price,cs*VOLUMEBASE,taxrate))        
    if sum(signal[tbegin:]) != 0: #最后一个未平仓,不计算
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
    trades= [Trade(tstock,tdate[last_index],price,cs*VOLUMEBASE,taxrate)]
    return trades

def evaluate(trades):#一次交易可以允许多次买卖，以单个股票数量为0为交易完成标志
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
    #print '交易情况',matchedtrades,wincount,winamount,lostcount,lostamount
    return Evaluation(matchedtrades)

