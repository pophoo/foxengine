# -*-coding:utf-8 -*-

VOLUME_BASE = 100L; #手
AMOUNT_BASE = 1000000L; #千元 = 100000分 = 1000000厘

class asdict(object):
    def __getitem__(self,key):  #允许dict的调用方法
        #print "getitem:" + key
        if(self.has_key(key)):  
            return getattr(self,key)

    def has_key(self,key):
        return  key in self.__slots__ #如果有继承容器父类，则也需要验证父类的

    def __str__(self):
        """只有以cvs方式保存的时候(测试环境)才用到"""
        return ",".join((str(getattr(self,slot)) for slot in self.__slots__))

    def asdict(self):
        ad = {}
        for slot in self.__slots__:
            ad[slot] = getattr(self,slot)
        return ad

class DatedStock(asdict):
    __slots__ = "none"  #必须设置slots，否则子类即便设置了slots属性，也会存在__dict__

    def __cmp__(self,other):
        #print "in cmp"
        return self.tdate - other.tdate or self.tstock > other.tstock

    def __eq__(self,other): #以便用于Set或者用做dict的key
        #print "in eq"
        return self.tstock == other.tstock and self.tdate == other.tdate

    def __hash__(self):
        #print "in hash"
        return hash(str(self.tstock) + str(self.tdate))

def createQuoteFromSrc(tstock,tdate,topen,tclose,thigh,tlow,tvolume,tamount): #从数据源读取数据创建对象，传入的价格和量的数据都是float型的
    quote = Quote()
    (quote.tstock,quote.tdate,quote.topen,quote.tclose,quote.thigh,quote.tlow,quote.tvolume,quote.tamount) =  (tstock,tdate,f2_milli(topen),f2_milli(tclose),f2_milli(thigh),f2_milli(tlow),tvolume,f2_100(tamount))
    quote.calcAvg()
    return quote

def createQuoteFromDb(tstock,tdate,topen,tclose,thigh,tlow,tvolume,tamount,tavg): #从数据表读取数据创建对象,传入参数都已经是1/1000为单位的整数
    quote = Quote()
    (quote.tstock,quote.tdate,quote.topen,quote.tclose,quote.thigh,quote.tlow,quote.tvolume,quote.tamount,quote.tavg) =  (tstock,tdate,topen,tclose,thigh,tlow,tvolume,tamount,tavg)
    return quote

xunitbase = 1000

class Quote(DatedStock):  #在属性名字前加t的目的是在保证属性名和字段名同名的同时，避免与数据库的关键字冲突
    """行情数据: 价格单位都是厘,成交量为手,成交金额为百元"""
    __slots__ = 'tstock','tdate','topen','tclose','thigh','tlow','tavg','tvolume','tamount'

    def __init__(self):
        #super(DatedStock,self).__init__(self)
        self.tstock = "AAAAAA"
        self.tdate = 99999999
        self.topen = self.tclose = self.thigh = self.tlow = self.tavg = self.tvolume = self.tamount = 0

    def calcAvg(self):
        if self.tvolume != 0:
            #先将成交金额单位调整为分(*100000)，然后去除以成交量，得到以分为单位均价
            self.tavg = int((self.tamount * AMOUNT_BASE + self.tvolume * VOLUME_BASE/2)/(self.tvolume*VOLUME_BASE))
        else:
	        self.tavg = self.tclose;
 
    def to_tuple(self):
        return self.tstock,self.tdate,self.topen,self.tclose,self.thigh,self.tlow,self.tavg,self.tvolume,self.tamount


def createXInfoFromSrc(tstock,tregisterday,texecuteday,tpgbl,tsgbl,tfhbl,tpgj,tzfs=0,tzfj=0):
    #从数据源读取数据创建对象，传入的价格和量的数据都是float型的
    xinfo = XInfo()
    (xinfo.tstock,xinfo.tregisterday,xinfo.texecuteday,xinfo.tpgbl,xinfo.tsgbl,xinfo.tfhbl,xinfo.tpgj,xinfo.tzfs,xinfo.tzfj) =  (tstock,tregisterday,texecuteday,f2_milli(tpgbl),f2_milli(tsgbl),f2_milli(tfhbl),f2_milli(tpgj),f2_milli(tzfs),f2_milli(tzfj))
    return xinfo

def createXInfoFromDb(id,tstock,tregisterday,texecuteday,tpgbl,tsgbl,tfhbl,tpgj,tzfs,tzfj,tstate,tremark):
    #从数据表读取数据创建对象,传入参数都已经是1/1000为单位的整数
    xinfo = XInfo()
    (xinfo.id,xinfo.tstock,xinfo.tregisterday,xinfo.texecuteday,xinfo.tpgbl,xinfo.tsgbl,xinfo.tfhbl,xinfo.tpgj,xinfo.tzfs,xinfo.tzfj,xinfo.tstate,xinfo.tremark) =  (id,tstock,tregisterday,texecuteday,tpgbl,tsgbl,tfhbl,tpgj,tzfs,tzfj,tstate,tremark)
    return xinfo

class XInfo(DatedStock): #除权信息
    __slots__="id",'tstock','tsgbl','tpgbl','tfhbl','tpgj','tzfs','tzfj','tjjs','tregisterday','texecuteday','tstate','tremark'

    def __init__(self):
        self.id = 0
        self.tstock = "AAAAAA"
        self.tregisterday = self.texecuteday = 99999999
        self.tremark = ""
        self.tstate = 0;    #未除权
        self.tsgbl = self.tpgbl = self.tfhbl = self.tpgj = self.tzfs = self.tzfj = self.tjjs = 0

    def __getattr__(self,name): #以便DateFilter
        if(name == "tdate"):
            return self.texecuteday

def createReportFromSrc(tstock,ttype,treleaseday,tdate,tzgb,tbg,thg,tag,tmgwfplr,tmgsy,tmgjzc,tmggjj):
    #从数据源读取数据创建对象，传入的价格和量的数据都是float型的
    report = Report()
    (report.tstock,report.ttype,report.treleaseday,report.tdate,report.tzgb,report.tbg,report.thg,report.tag,report.tmgwfplr,report.tmgsy,report.tmgjzc,report.tmggjj) = (tstock,ttype,treleaseday,tdate,int(tzgb),int(tbg),int(thg),int(tag),f2_milli(tmgwfplr),f2_milli(tmgsy),f2_milli(tmgjzc),f2_milli(tmggjj))
    #assert report.zgb < 2000000000
    return report

def createReportFromDb(tstock,ttype,treleaseday,tdate,tzgb,tbg,thg,tag,tmgwfplr,tmgsy,tmgjzc,tmggjj,tremark):
    #从数据表读取数据创建对象,传入参数都已经调整完毕
    report = Report()
    (report.tstock,report.ttype,report.treleaseday,report.tdate,report.tzgb,report.tbg,report.thg,report.tag,report.tmgwfplr,report.tmgsy,report.tmgjzc,report.tmggjj,report.tremark) = (tstock,ttype,treleaseday,tdate,tzgb,tbg,thg,tag,tmgwfplr,tmgsy,tmgjzc,tmggjj,tremark)
    return report

class Report(DatedStock): #报表信息
    __slots__= 'tstock','ttype','treleaseday','tzgb','tbg','thg','tag','tmgwfplr','tmgsy','tmgjzc','tmggjj','tremark'
    
    def __init__(self):
        self.tstock = "AAAAAA"
        self.ttype = 1 #1年2半年3季4月 0未知
        self.tremark = ""
        self.treleaseday = 99999999
        self.tdate = 9999
        self.tzgb = self.tbg = self.thg = self.tag = self.tmgwfplr = self.tmgsy = self.tmgjzc = self.tmggjj = 0

    def __getattr__(self,name): #以便DateFilter
        if(name == "tdate"):
            print self.treleaseday//100
            return self.treleaseday//100

def f2_milli(fsrc):    # float转换为0.001为单位的整数
    return int(fsrc*1000 + 0.5)

def f2_centi(fsrc):   # float转换为0.01为单位的整数
    return int(fsrc * 100 + 0.5)

def f2_100(fsrc):   # float转换为100为单位的整数
    return int(fsrc/100.0 + 0.5)

def f2_10000(fsrc):   # float转换为100为单位的整数
    return int(fsrc/10000.0 + 0.5)

class Trade(DatedStock):
    __slots__ = 'tstock','tdate','tprice','tvolume','ttax'

    def __init__(self,tstock,tdate,tprice,tvolume,taxrate = 125): #taxrate默认值为千分之八(1000/125). tvolume正为买入，负为卖出
        self.tstock = tstock
        self.tdate = tdate
        self.tprice = tprice
        self.tvolume = tvolume
        self.ttax = (self.tprice * abs(self.tvolume)  + taxrate/2)/ taxrate

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


class Evaluation(asdict):
    __slots__ = 'matchedtrades','count','balance','balances','wincount','winamount','lostcount','lostamount','deucecount','ratesum','rateavg','winrate','remark','lostavg','R'  #w赢利值inamount,亏损值lostamount都用正数表示

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
\t\t平盘次数=%(deucecount)s\n''' % self

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
        return sum > 0 and sum or 99999999   #避免出现sum=0的情形。因为除权的原因，有可能出现买入价为0的情形，特别是基金

    def __lt__(self,other): #只用于排序
        #print 'in < self=%s,other=%s' % (self.rateavg,other.rateavg)
        #return self.rateavg < other.rateavg
        return self.R < other.R

    def __gt__(self,other): #只用于排序
        #print 'in > self=%s,other=%s' % (self.rateavg,other.rateavg)
        #return self.rateavg > other.rateavg
        return self.R > other.R
