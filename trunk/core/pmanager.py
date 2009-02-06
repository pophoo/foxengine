# -*- coding: utf-8 -*-

''' 头寸管理
    通过过滤matchedtrades来实现
'''

from wolfox.fengine.base.common import Trade

class PostionManager(object):
    def __init__(self,evr,init_size=100000000):  #以0.001元为单位
        self.evr = evr      #evaluation映射,从 buy/sell/trade name ==> Evaluation
        self.init_size = self.init_size     #现金
        self.position = Position()  #现有仓位: code ==> trade
        self.earning = 0        #当前盈利

    def filter(matched_trades):
        return self.position.history

NULL_TRADE = Trade(0,0,0,0) #用于占位的空TRADE

class Position(object):
    def __init__(self):
        self.holdings = {}  #现有仓位: code ==> trade
        self.history = []   #元素为一次封闭交易[trade_buy,trade_sell]的列表

    def push(self,trade,avglost,risk,size_limit):    
        ''' trade为标准交易
            返回根据avglost,risk计算的实际的交易额,但不能超过size_limit
            avglost是平均损失比例(千分位表示)
            risk是能够承担的风险值
        '''
        wanted_size = risk / (trade.price * avglost / 1000)
        if wanted_size * trade.price > size_limit:
            wanted_size = size_limit / trade.price * 990 / 1000 #预留的tax
        trade.set_volume(wanted_size)
        holdings[trade.tstock] = trade
        return trade.calc()

    def pop(self,trade):
        ''' 确定卖出交易的额度,正常为全额. 子类可以定制这个方法,但需要maketrade函数的配合,以便部分卖出时有后续的卖出动作
            返回交易金额，正数
        '''
        holded = holdings.pop(trade.tstock,NULL_TRADE)
        trade.set_volume(-holded.tvolume)   #方向相反
        if trade.tvolume:   #如果发生交易,则添加到历史
            self.history.append([holded,trade])
        return trade.calc()
