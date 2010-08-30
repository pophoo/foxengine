# -*- coding: utf-8 -*-

import struct
import time
import calendar as cal
import numpy as np
import urllib2

from wolfox.fengine.ifuture.ibase import *
import wolfox.fengine.ifuture.ifreader as ifreader
import wolfox.fengine.ifuture.iftrade as iftrade
import wolfox.fengine.ifuture.ifuncs2 as ifuncs
import wolfox.fengine.ifuture.fcontrol as control
import wolfox.fengine.ifuture.dynamic as dynamic

trade_strategy = ifuncs.xxx3
trade_functor = control.ltrade3x0825
trade_priority = 2500

HEAD_SIZE = 0x18
INDEX_BLOCK_SIZE = 0x40
DATA_BEGIN = 0x41000
DATA_BLOCK_SIZE = 0x34
DATA_BLOCK_NUM = 0x276  #630
DATA_PAGE_SIZE = DATA_BLOCK_NUM * 0x34  #数据页面大小

class DataObject:
    pass

class SecReader:
    '''
        大智慧分笔数据(秒)
    '''

    def __init__(self,path):
        #self.fh = open(path,'rb')
        self.path = path

    def open(self):
        self.fh = open(self.path,'rb')

    def close(self):
        try:
            self.fh.close()
        except:
            pass

    def read_header(self):
        '''
            返回
                name -> info(name,record_nums,indice)
        '''
        self.fh.seek(0)
        header = self.fh.read(HEAD_SIZE)
        flag,ctime,nums = struct.unpack('I4x2I8x',header)
        assert flag == 0xfc139bf4
        #print flag,ctime,nums
        return self.read_infos(nums)

    def read_infos(self,nums):
        '''
            获取索引信息
        '''
        self.fh.seek(HEAD_SIZE)
        indices = {}
        for i in range(nums):
            ib = self.fh.read(INDEX_BLOCK_SIZE)
            sib = struct.unpack('=10sI25H',ib)
            info = DataObject()
            info.name = sib[0][:6] #前6位
            info.record_nums = sib[1]
            info.indice = []
            ii = 2
            ssize = len(sib)
            while(ii<ssize and sib[ii]!=0xFFFF):
                info.indice.append(sib[ii])
                ii += 1
            #indices.append(info)
            indices[info.name] = info
        return indices

    def read_records(self,info,seclast):
        '''
            info:索引信息
            seclast:自纪元以来的秒数. 大于该秒数的才读取(即开区间)
                一般取某分钟的起始时间 - 1秒. 以便取全数据
        '''
        records = []
        for index in info.indice:
            if self.check_page(index,seclast):  #确定是否滤过整块
                records.extend(self.read_page(self.fh,index,seclast))
            else:
                pass
                print 'skip a block'
        #对成交量和成交额做差额调整, 大智慧给的是累计值
        return records

    def check_page(self,index,seclast):
        '''
            index:索引块号
            seclast: 起始秒数(开区间)
            确认该数据块中是否有需要的数据
            这个判断有问题。reportl.dat是覆盖方式的，一个块里面可能有前一天的数据
        '''
        self.fh.seek(DATA_BEGIN + (index+1) * DATA_PAGE_SIZE - DATA_BLOCK_SIZE)
        dt = self.fh.read(4)
        ltime = struct.unpack('I',dt)[0]
        #return ltime > seclast
        return True

    @staticmethod
    def read_page(fh,index,seclast):
        '''
            index:索引块号
            seclast: 起始秒数(开区间)

            成交量和成交金额需要根据累计成交量和累计成交金额差分计算
            成交笔数为持仓总量
            此时，增仓量由持仓总量差分而得
            而开仓，平仓数根据 成交量、增仓量、成交方向计算得到
                开仓数 - 平仓数 = 增仓数
                开仓数 + 平仓数 = 成交量
                先计算开仓数 = (增仓数 + 成交量)/2，需要四舍五入
                然后再得到平仓数
            
            从这里来看，根据分笔数据计算一分钟数据的最高价和最低价必然是不准确的。
            逐笔数据有准确度，分笔数据时每统计时刻末的逐笔数据的累加，且价格以最后一笔为准
            必然会丢失实际的最高价和最低价

            数据格式:
            41000 - 41003 35 FA DF 46 1970.01.01 00:00:00 始的秒数 int
            41004 - 41007 00 00 18 41 最新价 float
            41008 - 4100B 00 80 B4 43 累计成交量 float
            4100C - 4100F 80 46 A7 48 累计成交金额 float

            41010 - 41011 51 9C 累计成交笔数/期指为持仓总量 char
            41012 - 41013 00 00 未知 char
            41014 10 累计成交笔数的溢出标志（00|10） byte
            41015 80 买入,卖出标识(80|E0买入，C0|A0卖出) byte

            41016 - 41017 23 01 委买量1 char
            41018 - 41019 8E 5B 委买量2 char
            4101A - 4101B 80 27 委买量3 char
            4101C - 4101D 8E 5B 委买量4 char
            4101E - 4101F B8 40 委买量5 char

            41020 - 41021 23 01 委卖量1 char
            41022 - 41023 8E 5B 委卖量2 char
            41024 - 41025 80 27 委卖量3 char
            41026 - 41027 8E 5B 委卖量4 char
            41028 - 41029 B8 40 委卖量5 char

            4102A 16 委买价1 与成交价的差 byte
            4102B 9A 委买价2 与成交价的差 byte
            4102C 80 委买价3 与成交价的差 byte
            4102D 40 委卖价4 与成交价的差 byte
            4102E 30 委卖价5 与成交价的差 byte

            4102F 57 委卖价1 与成交价的差 byte
            41030 68 委卖价2 与成交价的差 byte
            41031 69 委卖价3 与成交价的差 byte
            41032 7A 委卖价4 与成交价的差 byte
            41033 81 委卖价5 与成交价的差 byte
                
        '''
        records = []
        fh.seek(DATA_BEGIN + index * DATA_PAGE_SIZE)    
        for i in range(DATA_BLOCK_NUM):
            db = fh.read(DATA_BLOCK_SIZE)
            sdb = struct.unpack('I3f2H2b10h10b',db)
            if sdb[0] == 0:
                break
            if sdb[0] <= seclast:   
                continue
            record = DataObject()
            stime = time.gmtime(sdb[0])
            record.date = stime.tm_year*10000 + stime.tm_mon*100 + stime.tm_mday
            record.time = stime.tm_hour*10000 + stime.tm_min*100 + stime.tm_sec
            record.price = sdb[1]
            record.svol = sdb[2]
            record.samount = sdb[3]
            record.holding = sdb[4]
            record.vol_buy1 = sdb[8]
            record.vol_sell1 = sdb[13]
            record.price_buy1 = record.price + sdb[18]/100.0
            record.price_sell1 = record.price + sdb[23]/100.0
            record.seq = i
            records.append(record)        
        return records

    @staticmethod
    def sec2min(records):
        if len(records) == 0:
            return []
        mrecords = []
        min_high = min_low = records[0].price
        begin_record = records[0]
        end_record = records[0]
        for record in records:
            if record.date == end_record.date and record.time/100 == end_record.time/100:
                if record.price > min_high:
                    min_high = record.price
                if record.price < min_high:
                    min_low = record.price
            elif record.date > end_record.date or (record.date == end_record.date and record.time/100 > end_record.time/100):
                mrecords.append(SecReader.create_record(end_record.date,end_record.time/100,min_high,min_low,begin_record.price,end_record.price,end_record.svol,end_record.holding))
                min_high = min_low = record.price
                begin_record = record
            end_record = record
        mrecords.append(SecReader.create_record(end_record.date,end_record.time/100,min_high,min_low,begin_record.price,end_record.price,end_record.svol,end_record.holding))
        return mrecords

    @staticmethod
    def create_record(cur_date,cur_min,min_high,min_low,min_open,min_close,min_svol,min_holding):
        mrecord = DataObject()
        mrecord.date = cur_date
        mrecord.time = cur_min
        mrecord.high = int(min_high*10+0.1)
        mrecord.low = int(min_low*10+0.1)
        mrecord.open = int(min_open*10+0.1)
        mrecord.close = int(min_close*10+0.1)
        mrecord.svol = int(min_svol+0.1) #累计成交量
        mrecord.holding = int(min_holding)# 
        return mrecord

    @staticmethod
    def read_all(fh):
        '''
            探索数据格式用
            >>> for record in records:
            ...     if record.seq != pre+1 : print record.seq
            ...     pre = record.seq
            ...
            0
            3150
            5670
            20790
            37800
            38430
            55440
            >>> records[630].time
            91849
            >>> records[629].time
            92712
            >>> records[1260].time
            72234
            >>> records[1259].time
            93109
            各连续纪录集合的开始位置的最小公约数为630，估算连续块大小为630?
            基本确定
            经验证，确实如此。
            由此导致的问题是，期指分笔数据理论最大数为270*60=16200
            而大智慧数据索引结构的最大容量为 630 * 250 = 15750，当数据放不下时，将冲掉早盘数据(20100827的if1009就有这个问题)
            如果是股票，因为交易时间只有240分钟，理论最大值为 240 * 60 = 14400，不会溢出
        '''
        fh.seek(DATA_BEGIN)
        records=[]
        i = -1
        while(True):
            try:
                db = fh.read(DATA_BLOCK_SIZE)
            except:
                break
            if len(db)<52:
                break
            i += 1
            sdb = struct.unpack('I3f2H2c10H10c',db)
            if sdb[0] == 0:
                continue
            record = DataObject()
            stime = time.gmtime(sdb[0])
            record.date = stime.tm_year*10000 + stime.tm_mon*100 + stime.tm_mday
            record.time = stime.tm_hour*10000 + stime.tm_min*100 + stime.tm_sec
            record.price = sdb[1]
            record.svol = sdb[2]
            record.samount = sdb[3]
            record.ssize = sdb[4]
            record.seq = i
            records.append(record)        
        return records

    
class DynamicScheduler:
    '''
        调度者
        scheduler = dzh2.DynamicScheduler('d:/dzh2/data/sf/reportl.dat',['IF1009'])        
    '''
    def __init__(self,dyn_path,names):
        '''
            his_path:历史数据路径
            dyn_path:动态数据路径
        '''
        self.his_datas = ifreader.read_ifs(names=names)   #返回 name=>transaction的映射
        self.reader = SecReader(dyn_path)
        self.names = names
        self.dyn_datas = self.init_dyn(names)       

    def init_dyn(self,names):
        dyn_datas = {}
        for name in names:
            hdata = self.his_datas[name]
            if len(hdata.close)>0:
                ldate = hdata.date[-1]
                ltime = hdata.time[-1]
            else:
                sltime = time.localtime(time.time())
                ldate = sltime.tm_year*10000+sltime.tm_mon*100+sltime.tm_mday
                ltime = 0
            ddata = DataObject()
            ddata.pre_svol = 0
            ddata.lastsecs = cal.timegm((ldate/10000,(ldate%10000)/100,ldate%100,ltime/10000,(ltime%10000)/100,0,0,0,0))
            ddata.last_checked_date = ldate + 1 #最后信号检查时间, 前一天加1，以屏蔽前一天
            ddata.last_checked_time = 0  #最后信号检查时间
            ddata.transaction = [np.zeros(0,int),np.zeros(0,int),np.zeros(0,int),np.zeros(0,int),np.zeros(0,int),np.zeros(0,int),np.zeros(0,int),np.zeros(0,int),np.zeros(0,int)]
            dyn_datas[name] = ddata
        return dyn_datas  

    @staticmethod
    def get_itime():
        cur_stime = time.localtime(time.time())
        ctime = cur_stime.tm_hour * 100 + cur_stime.tm_min
        return ctime

    def run(self):
        '''
            调度过程
        '''
        while(self.get_itime()<1516):
            self.prepare_data()
            print u'读取数据成功,最新时间:%s' % self.dyn_datas[self.names[0]].transaction[ITIME][-1]
            self.check_signal()
            time.sleep(5)    #计算需要10秒，因此总延迟15秒

    def prepare_data(self):
        '''
            数据准备
        '''
        self.reader.open()
        infos = self.reader.read_header()
        for name in self.names:
            if name in infos:
                self.prepare_data1(infos[name],self.dyn_datas[name])
            else:
                print u'没有 %s 的动态数据' % name
        self.reader.close()
            
    def prepare_data1(self,info,dyn_data):
        records = self.reader.read_records(info,dyn_data.lastsecs)
        if len(records)>0:
            ldate = records[-1].date
            ltime = records[-1].time
            dyn_data.lastsecs = cal.timegm((ldate/10000,(ldate%10000)/100,ldate%100,ltime/10000,(ltime%10000)/100,0,0,0,0))
            mrecords = SecReader.sec2min(records)
            dyn_data.pre_svol = self.calc_vol(mrecords,dyn_data.pre_svol)
            dyn_data.transaction = self.concatenate(dyn_data.transaction,self.records2arrays(mrecords))

    def check_signal(self):
        for name in self.names:
            dyn_data = self.dyn_datas[name]
            his_data = self.his_datas[name] #必然要求有
            sms_actions = self.check_signal1(name,his_data,dyn_data)
            self.inform(name,sms_actions)

    @staticmethod
    def check_signal1(name,his_data,dyn_data):
        #print "check_signal"
        sif = DataObject()
        sif.name = name
        sif.transaction = DynamicScheduler.concatenate(his_data.transaction,dyn_data.transaction)
        ifreader.prepare_index(sif)
        #print 'prepared ok'
        tradesy = trade_functor(sif,trade_strategy,priority_level=trade_priority)
        xactions = iftrade.last_wactions(sif,tradesy)   #最新的在最前面
        sms_actions = []
        for action in xactions:
            if action.xtype == XOPEN and (action.date > dyn_data.last_checked_date 
                        or (action.date == dyn_data.last_checked_date and action.time > dyn_data.last_checked_time)):
                action.price = action.price / 10.0
                dynamic.calc_stop(sif,action)
                sms_actions.append(action)
        dyn_data.last_checked_date = xactions[0].date
        dyn_data.last_checked_time = xactions[0].time
        return sms_actions        

    @staticmethod
    def inform(name,sms_actions):
        ''' 屏蔽掉12分钟内连续的同类算法信号, 但不屏蔽最后一个
            返回发送的条数
        '''
        if len(sms_actions) == 0:
            return 0
        mq = sms_actions[::-1]  #变回顺序
        pre_time = 0
        pre_fname = ''
        successed = 0
        mnum = 0
        for action in mq:
            atime = cal.timegm((action.date/10000,(action.date%10000)/100,action.date%100
                ,action.time/100,action.time%100,0,0,0,0))  #转化为纪元后秒数
            if action.fname == pre_fname and atime - pre_time <= 720:   #720秒,15分钟
                print u'忽略10分钟之内的同类信号 : %s:%s' % (action.fname,action.time)
                continue
            pre_fname = action.fname
            pre_time = atime
            direction = u'买入' if action.position == LONG else u'卖出'
            msg = u'%s|%s:%s%s开仓%s,算法:%s' % (name,action.date,action.time,direction,action.price,action.fname)
            successed += DynamicScheduler.send_sms1(msg)
            #successed += DynamicScheduler.sms_stub(msg)
            mnum += 1
            #break  #测试短信用
        print u'计划发送 %s 条，成功发送 %s 条' % (mnum,successed)
        return successed

    @staticmethod
    def sms_stub(msg):
        print msg
        return 1

    @staticmethod
    def send_sms1(msg):
        '''
            发送成功返回1,否则为0
        '''
        #template = 'http://smsapi.qxt100.com/dapi/send_simple.php?name=wycharon&pwd=88107672&dest=13586682052&content=%s'        
        template = 'http://smsapi.qxt100.com/dapi/send_simple.php?name=wycharon&pwd=88107672&dest=15968464619&content=%s'
        p = urllib2.urlopen(template % msg)
        rmsg = p.read()
        #rmsg = 'success' #'error'
        if rmsg[:7] == 'success':
            print u'发送成功,%s' % msg
            return 1
        else:
            print u'发送失败,%s' % msg            
            return 0

    @staticmethod
    def concatenate(pre_transaction,itransaction):
        #print pre_transaction[ITIME]
        #print itransaction[ITIME]
        if len(pre_transaction[ICLOSE])>0:
            pre_date = pre_transaction[IDATE][-1]
            pre_time = pre_transaction[ITIME][-1]
        else:
            pre_date = 0
            pre_time = 0
        to_last = -1 if pre_date == itransaction[IDATE][0] and pre_time == itransaction[ITIME][0] else len(pre_transaction[IDATE])
        #print to_last
        transaction = [np.append(pre_transaction[IDATE][:to_last],itransaction[IDATE])
                ,np.append(pre_transaction[ITIME][:to_last],itransaction[ITIME])
                ,np.append(pre_transaction[IOPEN][:to_last],itransaction[IOPEN])
                ,np.append(pre_transaction[ICLOSE][:to_last],itransaction[ICLOSE])
                ,np.append(pre_transaction[IHIGH][:to_last],itransaction[IHIGH])
                ,np.append(pre_transaction[ILOW][:to_last],itransaction[ILOW])
                ,np.append(pre_transaction[IVOL][:to_last],itransaction[IVOL])
                ,np.append(pre_transaction[IHOLDING][:to_last],itransaction[IHOLDING])
                ]
        mid = (transaction[ICLOSE]*4+transaction[ILOW]+transaction[IHIGH])/6
        transaction.append(mid)
        return transaction

    @staticmethod
    def calc_vol(records,pre_svol):
        records[0].vol = records[0].svol - pre_svol
        pre_svol = records[0].svol
        for record in records[1:]:
            record.vol = record.svol - pre_svol
            pre_svol = record.svol
        return pre_svol

    @staticmethod
    def records2arrays(records):
        n = len(records)
        narrays = [np.zeros(n,int),np.zeros(n,int),np.zeros(n,int),np.zeros(n,int),np.zeros(n,int),np.zeros(n,int),np.zeros(n,int),np.zeros(n,int),np.zeros(n,int)]
        i = 0
        for record in records:
            narrays[IDATE][i] = record.date
            narrays[ITIME][i] = record.time
            narrays[IOPEN][i] = record.open        
            narrays[ICLOSE][i] = record.close
            narrays[IHIGH][i] = record.high
            narrays[ILOW][i] = record.low       
            narrays[IVOL][i] = record.vol
            narrays[IHOLDING][i] = record.holding
            narrays[IMID][i] = (record.close*4 + record.low + record.high)/6
            i += 1
        return narrays

if __name__ == '__main__':
    scheduler = DynamicScheduler('d:/dzh2/data/sf/reportl.dat',['IF1009'])
    scheduler.run()
