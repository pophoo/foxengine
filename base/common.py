# -*-coding:utf-8 -*-

from wolfox.foxit.base.common import *

class Trade(object):
    #__slots__ = 'tstock','tdate','tprice','tvolume','ttax' #不太方便，去掉, 也不再需要继承asdict(已经没有slot了)

    def __init__(self,tstock,tdate,tprice,tvolume,taxrate = 125): #taxrate默认值为千分之八(1000/125). tvolume正为买入，负为卖出
        self.tstock = tstock
        self.tdate = tdate
        self.tprice = tprice
        self.taxrate = taxrate
        self.set_volume(tvolume)

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
        return balance


class Evaluation(object):
    #__slots__ = 'matchedtrades','count','balance','balances','wincount','winamount','lostcount','lostamount','deucecount','ratesum','rateavg','winrate','remark','lostavg','R'  #w赢利值inamount,亏损值lostamount都用正数表示

    def __init__(self,matchedtrades,remark=''): 
        self.matchedtrades = matchedtrades  
        #print matchedtrades
        self.count = len(matchedtrades) #交易次数
        self.balances,self.wincount,self.winamount,self.lostcount,self.lostamount = self.calcwinlost()
        self.balance = self.winamount - self.lostamount   #总收益率
        self.deucecount = self.count - (self.wincount + self.lostcount) #平局次数
        #print 'calc ratesum'
        self.ratesum = self.sumrate()   
        assert int(self.ratesum) == int(self.balance) #ratesum等于balance. 因为目前balances也以收益率来计，而不是收益值
        self.rateavg = self.count > 0 and self.ratesum / self.count or 0
        self.winrate = self.count > 0 and self.wincount * 1000 / self.count or 0
        self.remark = remark
        self.lostavg = self.lostamount / self.lostcount if self.lostcount else 0
        self.R = self.rateavg * 1000 / self.lostavg if self.lostavg else 1000   #平均净收益/平均亏损，若没有亏损，则设为1000,即R=10
        #print '胜负次数',self.wincount,self.lostcount

    def calcwinlost(self):
        wincount = winamount = lostcount = lostamount = 0
        balances = [0] * len(self.matchedtrades)
        for i in range(len(self.matchedtrades)):
            balance = Trade.balanceit(self.matchedtrades[i]) * 1000/self.sumtrades(self.matchedtrades[i])
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
        return balances,wincount,winamount,lostcount,lostamount            

    def header(self):
         return u'''\t评估:总盈亏值=%(balance)s,交易次数=%(count)s\t期望值=%(R)s\t%(remark)s
\t\t总盈亏率(1/1000)=%(ratesum)s,平均盈亏率(1/1000)=%(rateavg)s,盈利交易率(1/1000)=%(winrate)s
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
    def sumtrades(trades):
        sum = 0 #买价总数
        for trade in trades:
            #print trade
            if(trade.tvolume > 0):
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
