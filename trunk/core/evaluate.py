# -*- coding: utf-8 -*-

import logging

from wolfox.fengine.base.common import Quote,Trade,Evaluation

logger = logging.getLogger('wolfox.fengine.core.evaulate')

def evaluate(trades):
    ''' 对交易进行匹配和评估
    '''
    return Evaluation(trades)

import operator
def DEFAULT_EVALUATE_FILTER(matched_named_trades):
    ''' 输入是元素如下的列表：
            trades:[[trade1,trade2,...],[trade3,trade4,...],....] 闭合交易列表
        返回采纳的闭合交易的合并列表
            [[trade1,trade2,...],[trade3,trade4,...],....]
    '''
    if matched_named_trades:
        return reduce(operator.add,matched_named_trades)
    else:
        return []

def gevaluate(named_trades,gfilter=DEFAULT_EVALUATE_FILTER):
    ''' 对多个来源组的交易进行匹配、头寸管理和评估。一次交易可以允许多次买卖，以单个股票存续数量为0为交易完成标志
        named_trades为BaseObject列表，每个BaseObject包括name,evaluation,trades三个属性
            evalutaion用于对trades中的交易进行风险和期望管理
        gfilter为对已经匹配成功的交易进行头寸管理
        matched_named_trades列表中的元素为
            trades:[[trade1,trade2,...],[trade3,trade4,...],....]
            满足    所有trade的volume之和为0，并且任何前m个trade的volume之和不为0(对于买先策略为大于0)
                    trade有parent属性，指向其所属的named_trades
    '''
    matched_named_trades = []
    for nt in named_trades:
        tradess=nt.trades
        #print tradess
        if not tradess: continue   #貌似无此必要,但可简化头寸管理部分的操作，而且更加符合直观
        for trades in tradess:
            for ctrade in trades:
                ctrade.parent = nt
        matched_named_trades.append(tradess)
    matched_trades = gfilter(matched_named_trades)   #头寸管理并转换成[trades,trades,...]形式
    for matched_trade in matched_trades:
        #print 'matched trade:%s,%s',matched_trade[0],matched_trade[1]
        #logger.debug('matched trade:%s,%s',matched_trade[0],matched_trade[1])
        pass
    return Evaluation(matched_trades)
