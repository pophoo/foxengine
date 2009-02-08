# -*- coding: utf-8 -*-

''' 头寸管理
    通过过滤matchedtrades来实现
'''

import operator
import logging

import numpy as np
from wolfox.fengine.base.common import Trade
from wolfox.fengine.core.base import BaseObject
from wolfox.fengine.core.utils import fcustom
from wolfox.fengine.core.d1ex import extend2next

logger = logging.getLogger('wolfox.fengine.core.postion_manager')

POS_BASE = 1000

NULL_TRADE = Trade(0,0,0,0) #用于占位的空TRADE
class Position(object): #只能用于管理单边头寸(即卖出都是pop，买入都是push或相反)，否则需要调用者判断某个买卖动作是push还是pop
    def __init__(self):
        self.holdings = {}  #现有仓位: code ==> [trade,....]    各trade都是同向操作
        self.history = []   #元素为一次封闭交易[trade_buy,trade_buy,...trade_sell]的列表

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
        #print wanted_size
        if wanted_size * trade.tprice > size_limit:
            wanted_size = size_limit / trade.tprice * 990 / POS_BASE #预留的tax
        wanted_size = (wanted_size / 100) * 100     #交易量向100取整
        if trade.tvolume < 0:
            wanted_size = -wanted_size
        #print wanted_size
        if wanted_size == 0:
            logger.debug('wanted volume is too smal : %s %s',trade.tstock,trade.tdate)
            trade.set_volume(0)
            return 0
        trade.set_volume(wanted_size)
        self.holdings[trade.tstock] = [trade]
        return trade.calc()

    def pop(self,trade):
        ''' 确定卖出交易的额度,正常为全额. 子类可以定制这个方法,但需要maketrade函数的配合,以便部分卖出时有后续的卖出动作
            返回交易金额，正数
        '''
        holdeds = self.holdings.pop(trade.tstock,[NULL_TRADE])
        hv = sum([holded.tvolume for holded in holdeds] )
        trade.set_volume(-hv)   #方向相反
        if trade.tvolume:   #如果发生交易,则添加到历史
            self.history.append(holdeds + [trade])
        return trade.calc(),sum([holded.calc() for holded in holdeds])

    def cost(self): #持仓成本
        total = 0
        for vs in self.holdings.values():
            total -= sum([v.calc() for v in vs])   #计算所的是收入数(小于0)
        return total


def half_of_first_sizer(trades):
    return abs(trades[0].tvolume / 2)

def half_of_total_sizer(trades):
    total = sum([t.tvolume for t in trades])
    return abs(total / 2)

class AdvancedPosition(Position):
    def __init__(self,sizer = half_of_first_sizer):
        Position.__init__(self)
        self.sizer = sizer

    def push(self,trade,lostavg,risk,size_limit):    
        ''' trade为标准交易
            返回根据lostavg,risk计算的实际的交易额,但不能超过size_limit
            lostavg是平均损失比例(千分位表示)
            risk是能够承担的风险值,以0.001元表示
            size_limit为上限交易额,也以0.001元表示
        '''
        if trade.tstock not in self.holdings:   
            return Position.push(self,trade,lostavg,risk,size_limit)
        tolds = self.holdings[trade.tstock]
        direct = 1 if tolds[0].tvolume >= 0 else -1  #1买入-1卖出
        if (direct == 1 and trade.tprice <= tolds[-1].tprice) or (direct == -1 and trade.tprice >= tolds[-1].tprice):  
            #买入后下降中不再买入或卖出后上升中不再卖出
            return 0
        wanted_size = self.sizer(tolds)
        if wanted_size * trade.tprice > size_limit:
            wanted_size = size_limit / trade.tprice * 990 / POS_BASE #预留的tax
        wanted_size = (wanted_size / 100) * 100     #交易量向100取整
        if direct == -1:
            wanted_size = - wanted_size
        if wanted_size == 0:
            logger.debug('second wanted volume is too smal : %s %s',trade.tstock,trade.tdate)
            trade.set_volume(0)
            return 0
        trade.set_volume(wanted_size)
        tolds.append(trade)
        return trade.calc()


#平均损失函数，返回的是千分比表示的平均损失
def ev_lost(trade): 
    return trade.parent.evaluation.lostavg

def atr_lost(trade,times=1):
    return trade.atr * times * POS_BASE / trade.price

atr_lost_2 = fcustom(atr_lost,times=2)

from math import sqrt
def RPR(xt,y):  #净值评估函数,xt为日期维x,y为相应净值
    '''#根据海龟交易法则
       计算方法来自http://www.scipy.org/Cookbook/LinearRegression
    '''
    (ar,br)=np.polyfit(xt,y,1)  #一阶拟合
    xr = np.polyval([ar,br],xt)
    err=sqrt(sum((xr-xt)**2)/len(xt)) #标准差
    (a_s,b_s,r,tt,stderr)=stats.linregress(xt,y)
    year_inc_rate = int(a_s * 365 * POS_BASE/b_s)
    logger.debug('rar:year_inc_rate=%s,a=%s,b=%s,k=a/b=%s,stderr=%s,err=%s',year_inc_rate,a_s,b_s,a_s/b_s,stderr,err)
    return year_inc_rate

def CSHARP(xt,y):   #变异夏普比率
    ''' 以回报而非超额回报为分子近似计算月比例
    '''
    indices = range(0,len(xt),30)
    m_xt = xt[indices]
    m_y = y[indices]
    (ar,br)=np.polyfit(m_xt,m_y,1)  #一阶拟合
    yr = np.polyval([ar,br],m_xt)
    err=sqrt(sum((yr-m_y)**2)/len(m_xt)) #标准差
    csharp = int(ar/br/err * POS_BASE)
    return csharp


from scipy import stats
class PositionManager(object):  #只适合先买后卖，卖空和混合方式都要由子类定制run实现
    def __init__(self,init_size=100000000,max_proportion=200,risk=10,calc_lost=ev_lost,position=Position):
        self.init_size = init_size     #现金,#以0.001元为单位
        self.max_proportion = max_proportion    #单笔占总金额的最大占比(千分比)
        self.risk = risk    #每笔交易承担的风险占总金额的比例(千分比)
        self.calc_lost = calc_lost
        self.position = position()  #现有仓位: code ==> trade
        self.cash = init_size
        self.earning = 0        #当前盈利
        self.vhistory = [BaseObject(date=0,value=self.init_size)]      #净值历史

    def clear(self):
        self.cash = self.init_size
        self.earning = 0
        self.position.clear()
        self.vhistory = [BaseObject(date=0,value=self.init_size)]

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
                trades:[[trade1,trade2,...],[trade3,trade4,...],....] 闭合交易列表
            转换合并按日期排序后返回
                [trade1,trade2,.....]
        '''
        nts = filter(lambda ts : ts,named_trades)   #滤去空元素
        if not nts: #啥也没剩下
            return []
        tradess = reduce(operator.add,nts) #转换为[[...],[...],[...]]
        trades = reduce(operator.add,tradess)   #为[......]
        trades.sort(cmp=lambda x,y:x.tdate-y.tdate)
        return trades        

    def filter(self,named_trades):
        self.run(self.organize_trades(named_trades))
        return self.position.history

    def run(self,trades):
        for trade in trades:
            climit = self.cur_limit()
            crisk = self.cur_risk()
            if trade.tvolume > 0:   #买入
                #print u'买入,before cash:',self.cash,'tstock:',trade.tstock
                self.cash += self.position.push(trade,self.calc_lost(trade),crisk,climit)
                #print u'买入,after cash:',self.cash                
            else:   #卖出
                income,cost = self.position.pop(trade)
                if income:  #非空转
                    self.cash += income
                    self.earning += (income + cost)
                    self.vhistory.append(BaseObject(date=trade.tdate,value=self.assets()))

    def calc_net_indicator(self,date_manager,func=RPR): 
        xt = np.arange(len(date_manager))    #x轴
        y = self.organize_net_array(date_manager)  #y轴
        return func(xt,y)

    def organize_net_array(self,date_manager):
        ''' 根据date_manager和vhistory获得净值数组(坐标与dates相一致)
        '''
        rev = np.zeros(len(date_manager),int)
        self.vhistory[0].date = date_manager.begin
        for b in self.vhistory: #第一个是初始值
            index = date_manager.get_index(b.date)
            rev[index] = b.value
        rev = extend2next(rev)
        return rev


import datetime
class DateManager(object):
    def __init__(self,begin=0,end=0):
        self.begin = begin
        self.end = end
        self.date_map = self.init_dates(begin,end)

    def __len__(self):
        return len(self.date_map)

    def init_dates(self,begin,end):
        if end <= begin:
            return {}
        date_map = {}
        from_date = datetime.date(begin/10000,begin%10000/100,begin%100)
        to_date = datetime.date(end/10000,end%10000/100,end%100)
        step = datetime.timedelta(1)
        cur_date = from_date
        i = 0
        while cur_date < to_date:
            idate = cur_date.year * 10000 + cur_date.month * 100 + cur_date.day
            date_map[idate] = i
            cur_date += step
            i += 1
        return date_map
    
    def get_index(self,date):
        if date in self.date_map:
            return self.date_map[date]
        else:
            logger.warn('%s not in [%s,%s)',date,self.begin,self.end)
            print '%s not in [%s,%s)' % (date,self.begin,self.end)
            raise KeyError('%s not in [%s,%s)' % (date,self.begin,self.end))

    def get_dates(self):
        return sorted(self.date_map.keys())
