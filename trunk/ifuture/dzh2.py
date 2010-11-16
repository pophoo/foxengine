# -*- coding: utf-8 -*-
'''
大智慧全推行情数据说明
从上周六开始安装大智慧(8月28),经过两天测试,大概判断如下:
1. 大智慧的全推模式是相对可靠的
我的测试方法是,首先把所有股指期货品种放入到自选股
然后打开IF1009
测试数据是否被完整刷入到大智慧的reportl.dat文件中
当时因为疏忽,所以在9:21分以后才打开大智慧
在日中曾数次用程序读写该数据文件,发现IF1010/1012/1103确实在同步更新,包括当月/下月/当季/隔季连续
同时,从股票数据文件中读取了两个不曾浏览过的股票,其行情也是完整的.

2.大智慧主力合约的实时数据是相对详细的. 但存在数据溢出后已过行情数据被裁减(但不影响一致性)的情况.
实时情形下,一秒钟刷好几下的也有.

3. 如果是盘中打开软件的情况, 前面已经过去的行情数据不会自动补全
数据补全的方式也不太清楚.
IF1009补全了09:14之后的数据,但其它合约没有. 可能需要手工浏览停留过.

4. 基本可用于实时提醒处理
应该算是唯一官方免费的全推行情了


附录:
大智慧(新一代)股指期货实时行情数据格式

1. 路径
安装目录/data/sf/reportl.dat
注意：股票行情数据的数据文件名为report.dat，股指期货是reportl.dat
这两哥们的数据页大小不同. 
网上流传的是report.dat的格式，每页数据为236个数据块
股指期货数据文件每页大小为630个数据

实际上，即便如此，也是存在问题的。后面会谈到，每个品种有25个页索引，指向25页，
也就是说，最大的记录容量是25*630 = 15750
而股指期货每日交易秒数为 60 * 270 = 16200
对于交易频繁的期指主力合约，非常容易引起溢出. 
溢出后大智慧会重新整理数据，按删减掉之前的部分行情数据(但不影响一致性)，然后在已占用的数据块中按顺序完全从头刷入(老数据不清零)
这里需要注意的是,25个页索引值是不变的, 也就是说后面的某些索引页的数据可能是无效的老数据.
如果自己编写读取程序,这个需要谨慎处理. 
我今天一开始就发出了5-6个错误信号.原因就是1分钟数据出现了重复,从914-1440,然后又从11xx-1440,某些数据被抽取了两遍.

2. 文件结构
文件结构同一般的大智慧数据
    文件头  24 字节
    索引块  从0x24开始 
        64 字节一块，每块表示一个品种。
    数据体  从0x41000开始，按页存储
        每页为32760字节，包含630个数据，每个数据52字节

3. 具体数据格式
3.1 文件头
0x0-0x3字节为标志F49B13FC
0xc-0xf字节为整数，表示品种总数
其它字节作用不明

3.2 索引块
0-0x9: 品种名称
0xa-0xd:整数，表示记录总数
0xe-0x34: 每两字节为一短整数，表示数据页号. 共25个数据块
    其中ffff表示空
    该品种当日行情数据即由这些数据页组成
    每页的具体地址计算为:
        数据页起始地址 = 0x41000 + 数据页号 * 32760

3.3 数据页
每个数据页由630个数据块组成
每块格式如下：
0-0x3: 整型，自1970/1/1以来的秒数
0x4-0x7:浮点，成交价
0x8-0xb:浮点，累计成交量    #这种累计量的方式，即便中间丢失了记录，也能确保区间成交量数据的一致性
0xc-0xf:浮点，累计成交金额
0x10-0x11:短整型, 当前持仓量
0x12-0x13:没用
0x14:持仓量溢出标志, 目前还没用. 持仓没超过65535
0x15:买卖标志，没用。因为分笔是逐笔的合计，这个标志标的是最后一个逐笔的方向
0x16-0x17: 短整型, 买1量，无实际用处
0x20-0x21: 短整型, 卖1量，无实际用处
0x2a: 单字节整数,买一价差，无实际用处
0x2f: 单字节整数,卖一价差，无实际用处

'''


import struct
import time
import calendar as cal
import datetime as dt
import numpy as np
import urllib2
import win32api

from wolfox.fengine.ifuture.ibase import *
import wolfox.fengine.ifuture.ifreader as ifreader
import wolfox.fengine.ifuture.iftrade as iftrade
import wolfox.fengine.ifuture.ifuncs2 as ifuncs
import wolfox.fengine.ifuture.fcontrol as control
import wolfox.fengine.ifuture.dynamic as dynamic
from wolfox.foxit.base.tutils import linelog

trade_strategy = ifuncs.xxx3
trade_functor = control.ltrade3x0825
trade_priority = 2500

HEAD_SIZE = 0x18
INDEX_BLOCK_SIZE = 0x40
DATA_BEGIN = 0x41000
DATA_BLOCK_SIZE = 0x34
DATA_BLOCK_NUM = 0x276  #630
DATA_PAGE_SIZE = DATA_BLOCK_NUM * 0x34  #数据页面大小

STOCK_DATA_BLOCK_NUM = 0xec  #236
STOCK_DATA_PAGE_SIZE = STOCK_DATA_BLOCK_NUM * 0x34  #数据页面大小



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

    def read_records(self,info,seclast=0):
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
                #print 'skip a block'
        records = self.adjust_records(records)   #整理record
        return records

    @staticmethod
    def adjust_records(records):
        if len(records) == 0:
            return records
        i = 1
        pre_time = records[0].time
        for record in records[1:]:
            if record.time < pre_time:
                #linelog(u'发现断层:%s-%s' % (pre_time,record.time))
                #print u'发现断层:%s-%s' % (pre_time,record.time)
                break
            i += 1
            pre_time = record.time
        return records[:i]

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
            record.vol = 0  #未设置前为0
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
                if record.price < min_low:
                    min_low = record.price
            elif record.date > end_record.date or (record.date == end_record.date and record.time/100 > end_record.time/100):
                mrecords.append(SecReader.create_record(end_record.date,end_record.time/100,min_high,min_low,begin_record.price,end_record.price,end_record.svol,end_record.holding))
                min_high = min_low = record.price
                begin_record = record
            elif record.date < end_record.date:
                break   #发现之前的数据
            end_record = record
        mrecords.append(SecReader.create_record(end_record.date,end_record.time/100,min_high,min_low,begin_record.price,end_record.price,end_record.svol,end_record.holding))
        SecReader.save_mrecords(mrecords)
        return mrecords

    @staticmethod
    def sec2min2(records):
        ''' 
            大智慧在开盘后打开程序时，会出现当日之前的数据均只有59秒的情形
            此时必须以上分钟59秒为开盘数据，否则ochl四个数据都是本分钟59秒的
                现在用上一分钟的来算，搞定了open/close，但不能搞定h/l,勉强用
                但实际上因为ATR的问题，这个很难解决
                可能需要删除以后再重新补齐? 
                尝试在开盘期间在行情软件工具菜单数据管理项里面清空当天行情数据，
                    再在工具菜单的下载项里选中需要下载的个股下载当天分笔，
                    不做这步的话可能之前的成交分笔明细不能补充，或者数据会混乱。
        '''
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
                if record.price < min_low:
                    min_low = record.price
            elif record.date > end_record.date or (record.date == end_record.date and record.time/100 > end_record.time/100):#切换分钟
                mrecords.append(SecReader.create_record(end_record.date,end_record.time/100,min_high,min_low,begin_record.price,end_record.price,end_record.svol,end_record.holding))
                min_high = min_low = record.price
		        #print record.time
                if record.time % 100 == 59:    #begin就是最后一秒
                    begin_record = end_record   #则begin_record采用上分钟的最后一秒
                    if record.price > begin_record.price:
                        min_low = begin_record.price
                    else:
                        min_high = begin_record.price
                else:
                    begin_record = record
            elif record.date < end_record.date:
                break   #发现之前的数据
            end_record = record
        mrecords.append(SecReader.create_record(end_record.date,end_record.time/100,min_high,min_low,begin_record.price,end_record.price,end_record.svol,end_record.holding))
        return mrecords


    @staticmethod
    def save_mrecords(mrecords):
        wf = open('d:/temp/min.txt','a+')
        wf.write('\n')
        for record in mrecords:
            #wf.write('%s-%s:%s-%s,%s-%s\n'%(record.date,record.time,record.open,record.close,record.high,record.low))
            wf.write('%s/%s/%s,%s:%s,%s,%s,%s,%s,%s,%s\n' % (record.date/10000,record.date/100%100,record.date%100,record.time/100,record.time%100,record.open,record.high,record.low,record.close,record.vol,record.holding))
        wf.close()

    @staticmethod
    def save_records(records):
        wf = open('d:/temp/detail%s.txt' % records[-1].time,'w')
        for record in records:
            wf.write('%s-%s:%s,%s,%s\n'%(record.date,record.time,record.price,record.svol,record.holding))
        wf.close()

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

    def save_all(self,fname):
        self.open()
        infos = self.read_header()
        if fname in infos:
            records = self.read_records(infos[fname])
            self.save_records(records)
            mrecords = self.sec2min2(records)
            DynamicScheduler.calc_vol(mrecords,0)
            self.save_mrecords(mrecords)
        else:
            print u'没有 %s 的动态数据' % fname
        self.close()



class SecReaderStock(SecReader):    #貌似有所不同
    def check_page(self,index,seclast):
        '''
            index:索引块号
            seclast: 起始秒数(开区间)
            确认该数据块中是否有需要的数据
            这个判断有问题。reportl.dat是覆盖方式的，一个块里面可能有前一天的数据
        '''
        return True


    @staticmethod
    def read_page(fh,index,seclast):
        '''
            index:索引块号
            seclast: 起始秒数(开区间)
                
        '''
        records = []
        fh.seek(DATA_BEGIN + index * STOCK_DATA_PAGE_SIZE)    
        for i in range(STOCK_DATA_BLOCK_NUM):
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

    
class DynamicScheduler:
    '''
        调度者
        scheduler = dzh2.DynamicScheduler('d:/dzh2/data/sf/reportl.dat',['IF1009'])        
    '''
    def __init__(self,dyn_path,names,sms_begin=915):
        '''
            his_path:历史数据路径
            dyn_path:动态数据路径
            names: his_name ==> dyn_name的映射
                目前, his_name为IF0001，即修改后的当月连续(当下月合约持仓量>当月90%时，下月提前为当月)
                      dyn_name为当月. 但当下月合约持仓量>当月90%时，移至下月  
        '''
        self.his_datas = ifreader.read_ifs2_zip(names=names.keys())   #返回 name=>transaction的映射
        self.reader = SecReader(dyn_path)
        self.names = names
        self.dyn_datas = self.init_dyn(names)
        self.sms_begin = sms_begin
        self.pre_time = 0
        self.pre_fname = ''

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
            print u'历史数据:%s-%s:%s' % (ldate,ltime,hdata.close[-1])
            ddata = DataObject()
            ddata.pre_svol = 0
            ddata.lastsecs = cal.timegm((ldate/10000,(ldate%10000)/100,ldate%100,ltime/100,ltime%100,0,0,0,0))
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
        while(self.get_itime()<2359):
            self.prepare_data()
            #print u'读取数据成功,最新时间:%s' % self.dyn_datas[self.names[0]].transaction[ITIME][-1]
            today = dt.date.today()
            tt = today.year*10000 + today.month*100 + today.day
            ct = self.dyn_datas[self.names.keys()[0]].transaction
            if ct[IDATE][-1] < tt:
                win32api.MessageBox(0,u'请检查时间是否正确......',u'提示',0x00001000L)
            if len(ct[IDATE])>0:
                linelog(u'读取数据成功,%s-%s:%s-%s,%s-%s' % (ct[IDATE][-1],ct[ITIME][-1],ct[IOPEN][-1],ct[ICLOSE][-1],ct[IHIGH][-1],ct[ILOW][-1]))
                self.check_signal()
            else:
                linelog(u'无当日动态数据')
            time.sleep(5)    #计算需要10秒，因此总延迟15秒

    def prepare_data(self):
        '''
            数据准备
        '''
        self.reader.open()
        infos = self.reader.read_header()
        for name in self.names:
            if name in infos:
                self.prepare_data1(infos[self.names[name]],self.dyn_datas[name])
            else:
                print u'没有 %s 的动态数据' % name
        self.reader.close()
            
    def prepare_data1(self,info,dyn_data):
        records = self.reader.read_records(info,dyn_data.lastsecs)
        if len(records)>0:
            #SecReader.save_records(records)            
            ldate = records[-1].date
            ltime = records[-1].time
            dyn_data.lastsecs = cal.timegm((ldate/10000,(ldate%10000)/100,ldate%100,ltime/10000,(ltime%10000)/100,0,0,0,0))
            mrecords = SecReader.sec2min2(records)
            dyn_data.pre_svol = self.calc_vol(mrecords,dyn_data.pre_svol)
            SecReader.save_mrecords(mrecords)            
            dyn_data.transaction = self.concatenate(dyn_data.transaction,self.records2arrays(mrecords))

    def check_signal(self):
        for name in self.names:
            dyn_data = self.dyn_datas[name]
            his_data = self.his_datas[name] #必然要求有
            sms_actions = self.check_signal1(name,his_data,dyn_data)
            self.inform(name,sms_actions,self.sms_begin)

    def check_signal1(self,name,his_data,dyn_data):
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

    def inform(self,name,sms_actions,sms_begin):
        ''' 屏蔽掉20分钟内连续的同类算法信号, 但不屏蔽最后一个
            返回发送的条数
        '''
        if len(sms_actions) == 0:
            return 0
        mq = sms_actions[::-1]  #变回顺序
        successed = 0
        mnum = 0
        msged = False
        for action in mq:
            atime = cal.timegm((action.date/10000,(action.date%10000)/100,action.date%100
                ,action.time/100,action.time%100,0,0,0,0))  #转化为纪元后秒数
            #print '\ntest:',action.fname,self.pre_fname,atime,self.pre_time
            if action.fname == self.pre_fname and atime - self.pre_time <= 1200:   #1800秒,20分钟
                print u'\n忽略20分钟之内的同类信号 : %s:%s' % (action.fname,action.time)
                #win32api.MessageBox(0,u'请注意眼睛休息',u'提示',0x00001000L)
                continue
            self.pre_fname = action.fname
            self.pre_time = atime
            
            direction = u'买入' if action.position == LONG else u'卖出'
            #trend = u'顺势' if action.functor.strategy in (XFOLLOW,XBREAK,XORB) else u'逆势'
            trend = u'顺势' if action.xfollow else u'逆势'
            trend = u'%s:%s' % (trend,iftrade.fpriority(action.functor))
            #msg = u'%s|%s:%s%s开仓%s,算法:%s,优先级:%s,止损:%s,条件单:%s' % (name,action.date,action.time,direction,action.price,action.fname,action.functor.priority,action.stop,action.mstop)
            #msg = u'%s|%s%s开仓%s,算法:%s,优先级:%s,止损:%s,条件单:%s,%s' % (name,action.time,direction,action.price,action.fname,action.functor.priority,action.stop,action.mstop,trend)
            msg = u'%s|%s:%s%s开仓%s,平仓%s:%s,条件单:%s%s,%s' % (name,action.date%10000,action.time,direction,action.price,action.close,action.stop,action.condition,action.mstop,trend) 
            print action.fname,msg
            if action.time < sms_begin:
                print u'\n忽略%s之前的信号:%s,%s,%s' % (sms_begin,action.time,msg,action.fname)
                #print action.time,sms_begin,type(action.time),int(action.time)>int(sms_begin)
                continue
            if not msged :
                win32api.MessageBox(0,u'请注意眼睛休息',u'提示',0x00001000L)
                msged = True
            successed += DynamicScheduler.send_sms1(msg,action.fname)
            #successed += DynamicScheduler.sms_stub(msg,action.fname)
            mnum += 1
            #break  #测试短信用
        print u'\n计划发送 %s 条，成功发送 %s 条' % (mnum,successed)
        if msum>0:
            pass
            #win32api.MessageBox(0,u'请注意眼睛休息',u'提示',0x00001000L)
        return successed

    @staticmethod
    def sms_stub(msg,fname):
        print msg,fname
        return 1

    @staticmethod
    def send_sms1(msg,fname):
        '''
            发送成功返回1,否则为0
        '''
        #template = 'http://smsapi.qxt100.com/dapi/send_simple.php?name=wycharon&pwd=88107672&dest=13586682052&content=%s'
        #mobiles = (13586682052,15968464619)
        mobiles = (15968464619,)

        successed = failed = 0
        try:
            for number in mobiles:
                template = 'http://smsapi.qxt100.com/dapi/send_simple.php?name=wycharon&pwd=88107672&dest=%s&content=%s'
                p = urllib2.urlopen(template % (number,msg))
                rmsg = p.read()
                #rmsg = 'success' #'error'
                if rmsg[:7] == 'success':
                    successed += 1
                    #print u'\n发送成功,%s,%s' % (msg,fname)
                else:
                    failed += 1
                    #print u'\n发送失败,%s,%s' % (msg,fname)
        except:
            pass
        finally:
            #print u'发送: %s,%s,成功:%s 条' % (msg,fname,successed)
            print u'发送%s,成功:%s 条' % (fname,successed)
            if failed > 0:
                return 0
        return 1

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

import sys
import getopt   #简单情形，不使用optparse
import time
if __name__ == '__main__':
    #scheduler = DynamicScheduler('d:/dzh2/data/sf/reportl.dat',['IF1009'])
    #scheduler = DynamicScheduler('d:/dzh2/data/sf/reportl.dat',['IF0001']) #当月连续
    #scheduler.run()
    sms_begin = -1

    try:
        opts, args = getopt.getopt(sys.argv[1:], 't:v', ['sms_begin=','verify'])
        #print opts,args
        for opt,v in opts:
            if opt in ('-t','--sms_begin'):
                sms_begin = int(v)
            if opt in ('-v','--verify'):
                reader =SecReader('d:/dzh2/data/sf/reportl.dat')
                reader.save_all('IF1012')
                exit()
    except getopt.GetoptError:
        print 'except ---'
        pass
    finally:
        if sms_begin == -1: #没设置过
            sltime = time.localtime(time.time())
            sms_begin = sltime.tm_hour*100 + sltime.tm_min
        print u'sms_begin=%s' % sms_begin
        

    #scheduler = DynamicScheduler('d:/dzh2/data/sf/reportl.dat',['IF1009'],sms_begin=sms_begin)
    #scheduler = DynamicScheduler('d:/dzh2/data/sf/reportl.dat',{'IF0001':'IF1010'},sms_begin=sms_begin)  #使用当月连续
    
    
    scheduler = DynamicScheduler('d:/dzh2/data/sf/reportl.dat',{'IF1012':'IF1012'},sms_begin=sms_begin)  #使用主力合约，节省计算时间
    scheduler.run()
    
