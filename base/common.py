# -*-coding:utf-8 -*-

from wolfox.foxit.base.common import *
from copy import copy as ccopy

class Trade(object):
    #__slots__ = 'tstock','tdate','tprice','tvolume','ttax' #不太方便，去掉, 也不再需要继承asdict(已经没有slot了)

    def __init__(self,tstock,tdate,tprice,tvolume,taxrate = 125): #taxrate默认值为千分之八(1000/125). tvolume正为买入，负为卖出
        self.tstock = tstock
        self.tdate = tdate
        self.tprice = tprice if tprice > 0 else 1 #避免除权除成负/0的出现(会影响仓位计算) 600497,200509以前情形
        self.taxrate = taxrate
        self.set_volume(tvolume)
        self.type = 'native'    #内生的，区别于后面的追加

    def copy(self):
        return ccopy(self)

    def set_volume(self,tvolume):
        self.tvolume = tvolume
        self.ttax = (self.tprice * abs(self.tvolume)  + self.taxrate/2)/ self.taxrate if abs(tvolume) > 0 else 0
        #实际上前一个公式也蕴含了整数情形下abs(tvolume)=0时ttax=0，但为避免浮点等复杂情形，适用判断

    def calc(self): #计算收入现金数(方向与tvolume相反)
        #print 'tax:',self.ttax,',amount:',self.tprice * (-self.tvolume)
        return self.tprice * (-self.tvolume) - self.ttax

    def __str__(self):  #调用者必须用unicode(trade)而非str(trade)以避免stdout时的编码问题
        #direct = self.tvolume>0 and u'买入' or u'卖出'
        #方法1  调用者必须用unicode(trade)而非str(trade)以避免编码问题
        #return (u'%s\t%s\t%s\t价格=%s\t数量=%s\n' % (self.tstock,direct,self.tdate,self.tprice,self.tvolume))
        #方法2   这个返回值只能适用于str(trade)而非unicode(trade)
        #return (u'%s\t%s\t%s\t价格=%s\t数量=%s\n' % (self.tstock,direct,self.tdate,self.tprice,self.tvolume)).encode('gbk')
        #方法3   字符串中不使用中文,避免编码问题
        direct = self.tvolume>0 and u'B' or u'S'
        return u'%s\t%s\t%s\tprice=%s\tvolume=%s\n' % (self.tstock,direct,self.tdate,self.tprice,self.tvolume)

    def __eq__(self,t):
        return t.tstock==self.tstock and t.tdate==self.tdate and t.tprice==self.tprice and t.tvolume==self.tvolume and t.taxrate == self.taxrate

    @staticmethod
    def balanceit(trades):  #计算一组trades的盈亏值
        balance = 0
        sum = 0
        for trade in trades:
            #print trade.calc()
            balance += trade.calc()
            sum += trade.tvolume
        assert sum == 0
        #print balance
        if len(trades)>0 and trades[0].tprice<=100 and balance>1000:#对因除权使得的price过低导致的高收益率，设置上限为50%.并可能因多次买入而小于该值
            balance = trades[0].tvolume / 2
        return balance


class Evaluation(object):
    #__slots__ = 'matchedtrades','count','balance','balances','wincount','winamount','lostcount','lostamount','deucecount','ratesum','rateavg','winrate','remark','lostavg','R'  #w赢利值inamount,亏损值lostamount都用正数表示

    def __init__(self,matchedtrades,datemap,remark=''): 
        ''' datemap为xdate==>交易日当前排序号的dict
            matchedtrades中每个元素都是完整的trades,参见gevaluate
        '''
        self.matchedtrades = matchedtrades  
        self.datemap = datemap
        #print matchedtrades
        self.count = len(matchedtrades) #交易次数
        self.balances,self.wincount,self.winamount,self.lostcount,self.lostamount,self.holdings = self.calcwinlost()
        self.balance = self.winamount - self.lostamount   #总收益率
        self.deucecount = self.count - (self.wincount + self.lostcount) #平局次数
        self.holdingavg = sum(self.holdings) / len(self.holdings) if self.holdings else 1
        #print 'calc ratesum'
        self.ratesum = self.sumrate()   
        assert int(self.ratesum) == int(self.balance) #ratesum等于balance. 因为目前balances也以收益率来计，而不是收益值
        self.rateavg = self.count > 0 and self.ratesum / self.count or 0
        self.winrate = self.count > 0 and self.wincount * 1000 / self.count or 0
        self.remark = remark
        self.lostavg = self.lostamount / self.lostcount if self.lostcount else 0
        self.R = self.rateavg * 1000 / self.lostavg if self.lostavg else 1000   #平均净收益/平均亏损，若没有亏损，则设为1000,即R=10
        #print '胜负次数',self.wincount,self.lostcount
        self.E = self.rateavg * 1000 / self.holdingavg if self.holdingavg else 0    #总收益率/总持仓时间

    def copy_header(self):
        ne = ccopy(self)
        ne.matchedtrades = []   #清除trades
        ne.datemap = {}         #清除datemap   
        return ne

    def calcwinlost(self):  #内中的balance必须返回int值
        wincount = winamount = lostcount = lostamount = 0
        balances = [0] * len(self.matchedtrades)
        holdings = [0] * len(self.matchedtrades)
        for i in range(len(self.matchedtrades)):
            balance = int(Trade.balanceit(self.matchedtrades[i]) * 1000/self.sumtrades(self.matchedtrades[i]))  #不加转换，则当成交金额略大时，成为long类型
            #print balance,Trade.balanceit(self.matchedtrades[i]) * 1000,self.sumtrades(self.matchedtrades[i])
            if(balance > 0):
                wincount += 1
                winamount += balance
            elif(balance < 0):
                lostcount +=1
                lostamount += (-balance)
            else:   #平盘
                pass
            balances[i] = balance
            holdings[i] = self.sumholding(self.matchedtrades[i],self.datemap)
        return balances,wincount,winamount,lostcount,lostamount,holdings

    def header(self):
         return u'''\t评估:总盈亏值=%(balance)s,交易次数=%(count)s\t期望值=%(R)s%(remark)s
\t\t总盈亏率(1/1000)=%(ratesum)s,平均盈亏率(1/1000)=%(rateavg)s,盈利交易率(1/1000)=%(winrate)s
\t\t平均持仓时间=%(holdingavg)s,持仓效率(1/1000000)=%(E)s
\t\t赢利次数=%(wincount)s,赢利总值=%(winamount)s
\t\t亏损次数=%(lostcount)s,亏损总值=%(lostamount)s
\t\t平盘次数=%(deucecount)s\n''' % self.__dict__

    def __str__(self):
        smatchedtrades = u'\t\t闭合交易明细:\n'
        for trades,balance in zip(self.matchedtrades,self.balances):  #多个闭合交易的集合
            #if(balance*1000/self.sumtrades(trades) < 100):
            #    continue
            smatchedtrades += u'\t\t\tstock=%s 盈亏值=%s:,盈亏率(1/1000):%s\n' % (trades[0].tstock,Trade.balanceit(trades),balance)
            for trade in trades:#一个闭合交易中的各个交易点
                smatchedtrades += '\t\t\t\t%s' % str(trade)
        return self.header() + smatchedtrades

    def sumrate(self):
        ratesum = 0
        #for trades,balance in zip(self.matchedtrades,self.balances):  #多个闭合交易的集合
            #print 'preratesum',ratesum,',curbalance:',balance,',sum',self.sumtrades(trades)
        #    ratesum += balance*1000/self.sumtrades(trades)
        #print 'ratesum',ratesum            
        #return ratesum
        return sum(self.balances)

    @staticmethod
    def sumholding(trades,datemap): #持仓时间
        '''
            多次买入一次卖出
            统算为一次交易，持仓时间按照总量折算,折算为总量的持仓时间。
            按成交量而非成交额
        '''
        if len(trades) <= 1:
            return 0
        vsum = trades[0].tvolume    #交易量累计
        dsum = 0    #交易量的时间累计
        cur = pre = datemap[trades[0].tdate]
        for trade in trades[1:-1]: #最后一个必然是反向交易，因此不须计在dsum中
            cur = datemap[trade.tdate]
            dsum += (cur-pre)*vsum
            pre = cur
            vsum += trade.tvolume
            #print dsum,vsum
        dsum += (datemap[trades[-1].tdate]-pre)*vsum
        #print dsum,vsum
        return dsum/vsum    #holding

    @staticmethod
    def sumholding_old(trades,datemap): #持仓时间
        '''
            多次买入一次卖出
            假设每次买入都是一次交易且等量，因此持仓时间等于多次交易的累计持仓时间
        '''
        sum = 0 
        if len(trades) <= 1:
            return sum
        pre = datemap[trades[0].tdate]
        for i,trade in list(enumerate(trades))[1:]:
            cur = datemap[trade.tdate]
            #print sum,cur,pre,i
            sum += (cur-pre)*i
            pre = cur
        return sum


    @staticmethod
    def sumtrades(trades):
        sum = 0 #买价总数
        for trade in trades:
            #print trade
            if(trade.tvolume > 0):
                #print trade.tprice,trade.tvolume,trade.calc()
                sum -= trade.calc() #买入时收入现金数为负数
        #print 'len(trades):%s,sum:%s' % (len(trades),sum)
        return sum if sum > 0 else 99999999   #避免出现sum=0的情形。因为除权的原因，有可能出现买入价为0的情形，特别是基金

    def __lt__(self,other): #只用于排序
        #print 'in < self=%s,other=%s' % (self.rateavg,other.rateavg)
        #return self.rateavg < other.rateavg
        return self.R < other.R

    def __gt__(self,other): #只用于排序
        #print 'in > self=%s,other=%s' % (self.rateavg,other.rateavg)
        #return self.rateavg > other.rateavg
        return self.R > other.R
