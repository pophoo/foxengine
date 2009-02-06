# -*- coding: utf-8 -*-

''' 头寸管理
    通过过滤matchedtrades来实现
'''

import operator
import logging

from wolfox.fengine.base.common import Trade
from wolfox.fengine.core.base import BaseObject

logger = logging.getLogger('wolfox.fengine.core.postion_manager')

POS_BASE = 1000

class PositionManager(object):
    def __init__(self,init_size=100000000,max_proportion=200,risk=10):
        self.init_size = init_size     #现金,#以0.001元为单位
        self.max_proportion = max_proportion    #单笔占总金额的最大占比(千分比)
        self.risk = risk    #每笔交易承担的风险占总金额的比例(千分比)
        self.position = Position()  #现有仓位: code ==> trade
        self.cash = init_size
        self.earning = 0        #当前盈利

    def assets(self):
        return self.init_size + self.earning

    def cur_limit(self): #计算当前的最大单笔占比,不能大于当前现金数
        v = int(self.assets() * self.max_proportion / POS_BASE)
        return v if v<= self.cash else self.cash    
    
    def cur_risk(self):
        return int(self.assets() * self.risk / POS_BASE)

    def income_rate(self):
        return int(self.earning * POS_BASE / self.init_size)

    def organize_trades(self,named_trades):
        ''' 输入是元素如下的列表：
                parent: BaseObject
                trades:[[trade1,trade2,...],[trade3,trade4,...],....] 闭合交易列表
            转换合并按日期排序后返回
                [(trade1,parent),(trade2,parent),...]
        '''
        trades = []
        for nt in named_trades:
            if nt:
                cur_trades = reduce(operator.add,nt.trades)
                trades.extend([(t,nt.parent) for t in cur_trades])
        trades.sort(cmp=lambda x,y:x[0].tdate-y[0].tdate)                
        return trades        

    def filter(self,named_trades):
        self.run(self.organize_trades(named_trades))
        return self.position.history

    def run(self,trades):
        for trade,parent in trades:
            climit = self.cur_limit()
            crisk = self.cur_risk()
            if trade.tvolume > 0:   #买入
                #print u'买入,before cash:',self.cash,'tstock:',trade.tstock
                self.cash += self.position.push(trade,parent.evaluation.lostavg,crisk,climit)
                #print u'买入,after cash:',self.cash                
            else:   #卖出
                income,cost = self.position.pop(trade)
                self.cash += income
                self.earning += (income + cost)


NULL_TRADE = Trade(0,0,0,0) #用于占位的空TRADE
class Position(object):
    def __init__(self):
        self.holdings = {}  #现有仓位: code ==> trade
        self.history = []   #元素为一次封闭交易[trade_buy,trade_sell]的列表

    def clear(self):
        self.holdings = {}  #比clear快
        self.history = []

    def push(self,trade,lostavg,risk,size_limit):    
        ''' trade为标准交易
            返回根据lostavg,risk计算的实际的交易额,但不能超过size_limit
            lostavg是平均损失比例(千分位表示)
            risk是能够承担的风险值,以0.001元表示
            size_limit为上限交易额,也以0.001元表示
        '''
        if trade.tstock in self.holdings:   #已经在持股. 对于多个来源的交易集合可能出现这种情况
            logger.debug('repeated buy in : %s %s',trade.tstock,trade.tdate)
            trade.set_volume(0)
            return 0
        wanted_size = risk / (trade.tprice * lostavg / POS_BASE)
        if wanted_size * trade.tprice > size_limit:
            wanted_size = size_limit / trade.tprice * 990 / POS_BASE #预留的tax
        wanted_size = (wanted_size / 100) * 100     #交易量向100取整
        if wanted_size == 0:
            logger.debug('wanted volume is too smal : %s %s',trade.tstock,trade.tdate)
            trade.set_volume(0)
            return 0
        trade.set_volume(wanted_size)
        self.holdings[trade.tstock] = trade
        return trade.calc()

    def pop(self,trade):
        ''' 确定卖出交易的额度,正常为全额. 子类可以定制这个方法,但需要maketrade函数的配合,以便部分卖出时有后续的卖出动作
            返回交易金额，正数
        '''
        holded = self.holdings.pop(trade.tstock,NULL_TRADE)
        trade.set_volume(-holded.tvolume)   #方向相反
        if trade.tvolume:   #如果发生交易,则添加到历史
            self.history.append([holded,trade])
        return trade.calc(),holded.calc()

    def cost(self): #持仓成本
        total = 0
        for v in self.holdings.values():
            total -= v.calc()   #计算所的是收入数(小于0)
        return total
