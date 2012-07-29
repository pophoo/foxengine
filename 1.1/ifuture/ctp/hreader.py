# -*- coding: utf-8 -*-

import zipfile
import time
import logging


from base import *

logger = logging.getLogger('ctp.hreader')    

DATA_PATH = 'data/'


def make_tick_filename(instrument,tday=0,suffix='txt'):
    if tday == 0:
        tday = time.strftime('%Y%m%d')
    return '%s%s_%s_tick.%s' % (DATA_PATH,instrument,tday,suffix)

def make_min_filename(instrument,suffix='txt'):
    return '%s%s_%s_min.%s' % (DATA_PATH,instrument,time.strftime('%Y%m%d'),suffix)

#################################################################
## 历史数据读取
#################################################################
def extract_std(line):
    items = line.split(',')
    record = BaseObject()
    record.date = int(items[0].replace('/',''))
    record.time = int(items[1].replace(':',''))
    record.open = int(float(items[2])*10 + 0.1)
    record.high = int(float(items[3])*10 + 0.1)
    record.low = int(float(items[4])*10 + 0.1)
    record.close = int(float(items[5])*10 + 0.1)
    record.vol = int(float(items[6]) + 0.1)
    record.holding = int(float(items[7]) + 0.1)
    return record

def read_data(filename,extractor=extract_std):
    file = open(filename,'r')
    data = file.read()
    file.close()
    return read_records(data,extractor)

def read_data_zip(filename,extractor=extract_std):
    df = zipfile.ZipFile(filename,'r')
    data = df.read(df.namelist()[0])    #只包含一个文件
    data = data.replace('\r','')  #去掉zip文件读出的\r，因为直接读文本没有\r这个符号
    df.close()
    return read_records(data,extractor)

def read_records(data,extractor):    
    '''
        根据传入的文本数据切割成record数组
    '''
    data = data.split('\n')
    records = []
    for line in data:
        if len(line.strip()) > 0:
            record = extractor(line)
            if record.time < 1516 and record.time > 850:  #排除错误数据
                records.append(record)
    return records

def read_min_as_list(filename,length,extractor=extract_std,readfunc = read_data):
    try:
        records = readfunc(filename,extractor)
    except Exception,inst:#读不到数据,默认都为1(避免出现被0除)
        logger.error(u'文件打开错误，文件名=%s,错误信息=%s' % (filename,str(inst)))
        n = 0
        return [[0]*n,[0]*n,[0]*n,[0]*n,[0]*n,[0]*n,[0]*n,[0]*n]
    else:   #正常读取到数据
        n = min(len(records),length)
        tran_data = [[0]*n,[0]*n,[0]*n,[0]*n,[0]*n,[0]*n,[0]*n,[0]*n]
        i = 0
        for record in records[-length:]:
            tran_data[IDATE][i] = record.date
            tran_data[ITIME][i] = record.time
            tran_data[IOPEN][i] = record.open        
            tran_data[ICLOSE][i] = record.close
            tran_data[IHIGH][i] = record.high
            tran_data[ILOW][i] = record.low       
            tran_data[IVOL][i] = record.vol
            tran_data[IHOLDING][i] = record.holding
            i += 1
    return tran_data


prefix = ''
SUFFIX = '.txt'
SUFFIX_ZIP = '.zip'

make_his_filename = lambda path,prefix,name,suffix:path + prefix + name + suffix

def read1(instrument,length=6000,path=DATA_PATH,extractor=extract_std,readfunc=read_data,suffix=SUFFIX):
    #6000是22天，足够应付日ATR计算
    hdata = BaseObject(name=instrument,instrument=instrument,transaction=read_min_as_list(make_his_filename(path,prefix,instrument,suffix),length=length,extractor=extractor,readfunc=readfunc))
    return hdata

#不从zip读数据
#read1_zip = fcustom(read1,readfunc=read_data_zip,suffix=SUFFIX_ZIP)


def read_history(instrument_id,path):
    return read1(instrument_id,path=path)

#####################################################
#分钟数据写入, 暂时写入到当日的分钟文件，而不是写到历史分钟文件中
#####################################################
def i2s(iv):    #将.1转化为正常点. 以与从文化财经保存的一致
    return '%s.%s' % (iv/10,iv%10)

def save1(instrument,min_data,path=DATA_PATH):
    filename = make_min_filename(instrument)
    ff = open(filename,'a+')
    sdate = '%s/%02d/%02d' % (min_data.vdate/10000,min_data.vdate/100%100,min_data.vdate%100)
    stime = '%02d:%02d' % (min_data.vtime/100,min_data.vtime%100)
    ff.write('%s,%s,%s,%s,%s,%s,%s,%s\n' % (sdate,stime,i2s(min_data.vopen),i2s(min_data.vhigh),i2s(min_data.vlow),i2s(min_data.vclose),min_data.vvolume,min_data.vholding))
    ff.close()

##############################################################################
##基本数据准备
##############################################################################
def prepare_data(instruments,path=DATA_PATH):
    data = {}
    for inst in instruments:
        if inst[:2] == 'IF' or inst[:2] == 'if':
            PREPARER = IF_PREPARER
        else:
            break   #目前未实现
        tdata = read_history(inst,path)
        tdata.m1 = tdata.transaction
        ###基本序列按1分钟设定,方便快捷查找
        tdata.sdate = tdata.m1[IDATE]
        tdata.stime = tdata.m1[ITIME]
        tdata.sopen = tdata.m1[IOPEN]
        tdata.sclose = tdata.m1[ICLOSE]
        tdata.shigh = tdata.m1[IHIGH]
        tdata.slow = tdata.m1[ILOW]
        tdata.svolume = tdata.m1[IVOL]
        tdata.sholding = tdata.m1[IHOLDING]
        ###其它周期
        oc_index_3 = PREPARER.p3(tdata.transaction[ITIME])
        tdata.m3 = compress(tdata.transaction,oc_index_3)
        oc_index_5 = PREPARER.p5(tdata.transaction[ITIME])
        tdata.m5 = compress(tdata.transaction,oc_index_5)
        oc_index_15 = PREPARER.p15(tdata.transaction[ITIME])
        tdata.m15 = compress(tdata.transaction,oc_index_15)
        oc_index_30 = PREPARER.p30(tdata.transaction[ITIME])
        tdata.m30 = compress(tdata.transaction,oc_index_30)
        data[inst] = tdata
        oc_index_d = PREPARER.pd(tdata.transaction[ITIME])
        tdata.d1 = compress(tdata.transaction,oc_index_d)
        if len(tdata.d1[IDATE])>0:
            tdata.cur_day = BaseObject(
                        vdate= tdata.d1[IDATE][-1],
                        vtime = tdata.stime[-1],    #最后的交易分钟
                        vopen = tdata.d1[IOPEN][-1],
                        vclose = tdata.d1[ICLOSE][-1],
                        vhigh = tdata.d1[IHIGH][-1],    #根据tick中出现价格的最大/最小比较而来
                        vlow = tdata.d1[ILOW][-1],
                        vhighd = tdata.d1[IHIGH][-1],   #根据tick中的当日最大/最小, 是服务器计算的
                        vlowd = tdata.d1[ILOW][-1],
                        vholding = tdata.d1[IHOLDING][-1],
                        vvolume = tdata.d1[IVOL][-1],
                    )
        else:
            tdata.cur_day = BaseObject(
                        vdate= 0,
                        vtime = 0,
                        vopen = 0,
                        vclose = 0,
                        vhigh = 0,
                        vlow = 0,
                        vhighd = 0,
                        vlowd = 0,
                        vholding = 0,
                        vvolume = 0,
                    )
        if len(tdata.sdate)>0:
            tdata.cur_min = BaseObject(
                        vdate = tdata.sdate[-1],
                        vtime = tdata.stime[-1],
                        vopen = tdata.sopen[-1],
                        vclose = tdata.sclose[-1],
                        vhigh = tdata.shigh[-1],
                        vlow = tdata.slow[-1],
                        vholding = tdata.sholding[-1],
                        vvolume = tdata.svolume[-1],
                    )
        else:
            tdata.cur_min = BaseObject(
                        vdate = 0,
                        vtime = 0,
                        vopen = 0,
                        vclose = 0,
                        vhigh = 0,
                        vlow = 0,
                        vholding = 0,
                        vvolume = 0,
                    )
        data[inst] = tdata
    return data

def compress(trans_data,oc_index):
    '''
        将trans_data的各数据根据oc_index压缩成相应的X分钟数据
    '''
    n = len(oc_index)
    xdata = [[0]*n,[0]*n,[0]*n,[0]*n,[0]*n,[0]*n,[0]*n,[0]*n,]
    xdata[IDATE] = [trans_data[IDATE][c] for o,c in oc_index]
    xdata[ITIME] = [trans_data[ITIME][c] for o,c in oc_index]   #收盘时间点
    xdata[IOPEN] = [trans_data[IOPEN][o] for o,c in oc_index]        
    xdata[ICLOSE] = [trans_data[ICLOSE][c] for o,c in oc_index]
    xdata[IHIGH] = [max(trans_data[IHIGH][o:c+1]) for o,c in oc_index]
    xdata[ILOW] = [min(trans_data[ILOW][o:c+1]) for o,c in oc_index]
    xdata[IVOL] = [sum(trans_data[IVOL][o:c+1]) for o,c in oc_index]
    xdata[IHOLDING] = [trans_data[IHOLDING][c] for o,c in oc_index]
    return xdata


##是否是IF的X分钟收盘分钟
IF_XPREPARER = BaseObject()
IF_XPREPARER.ISEND_3 = lambda x:(x%100%3==2 or x%10000==1514) and x%1000!=914
IF_XPREPARER.ISEND_5 = lambda x: x%5==4 and x%1000!=914
IF_XPREPARER.ISEND_15 = lambda x:x%100%15 == 14 and x%1000!=914
IF_XPREPARER.ISEND_30 = lambda x:x%100%30 == 14 and x%1000!=914
IF_XPREPARER.ISEND_DAY = lambda x:x%10000 == 1514

##是否是CM的X分钟收盘分钟
CM_XPREPARER = BaseObject()
CM_XPREPARER.ISEND_3 = lambda x:(x%100%3==2 or x%10000==1459) and x%1000!=859
CM_XPREPARER.ISEND_5 = lambda x: x%5==4 and x%1000!=859
CM_XPREPARER.ISEND_15 = lambda x:x%100%15 == 14 and x%1000!=859
CM_XPREPARER.ISEND_30 = lambda x:(x%100%30 == 29 or x%10000 == 1014) and x%1000!=859
CM_XPREPARER.ISEND_DAY = lambda x:x%10000 == 1459

def is_if(instrument):#判断是否是IF
    return instrument[:2] == 'IF'

class XPREPARER(object):
    def __init__(self,fpreparer):
        self.fpreparer = fpreparer

    def pd(self,xtimes):#切日
        poss = filter(lambda x:x[0]>x[1],zip(xtimes,xtimes[1:]+[0],range(len(xtimes))))
        cposs = [z for (x,y,z) in poss]   #close
        oposs = [c+1 if c-1>0 else 0 for c in cposs] #close
        return zip(oposs,cposs[1:])
    
    def p3(self,xtimes):#切3分钟,返回3分钟(3分开盘index,3分收盘index)
        poss = filter(lambda x:self.fpreparer.ISEND_3(x[0]),zip(xtimes,range(len(xtimes))))
        cposs = [y for (x,y) in poss]   #close
        oposs = [c+1 if c-1>0 else 0 for c in cposs] #close
        return zip(oposs,cposs[1:])

    def p5(self,xtimes):#切5分钟,返回5分钟(5分开盘index,5分收盘index)
        poss = filter(lambda x:self.fpreparer.ISEND_5(x[0]),zip(xtimes,range(len(xtimes))))
        cposs = [y for (x,y) in poss]   #close
        oposs = [c+1 if c-1>0 else 0 for c in cposs] #close
        return zip(oposs,cposs[1:])

    def p15(self,xtimes):#切15分钟,返回15分钟(15分开盘index,15分收盘index)
        poss = filter(lambda x:self.fpreparer.ISEND_15(x[0]),zip(xtimes,range(len(xtimes))))
        cposs = [y for (x,y) in poss]   #close
        oposs = [c+1 if c-1>0 else 0 for c in cposs] #close
        return zip(oposs,cposs[1:])

    def p30(self,xtimes):#切30分钟,返回30分钟(30分开盘index,30分收盘index)
        poss = filter(lambda x:self.fpreparer.ISEND_30(x[0]),zip(xtimes,range(len(xtimes))))
        cposs = [y for (x,y) in poss]   #close
        oposs = [c+1 if c-1>0 else 0 for c in cposs] #close
        return zip(oposs,cposs[1:])

IF_PREPARER = XPREPARER(IF_XPREPARER)
CM_PREPARER = XPREPARER(CM_XPREPARER)

##############################################
##ticks数据读取
##############################################
def extract_tick(line):
    items = line.split(',')
    rev = BaseObject()
    rev.date = int(items[1])
    rev.min1 = int(items[2])
    rev.time = rev.min1
    rev.sec = int(items[3])
    rev.msec = int(items[4])
    rev.holding = int(items[5])
    rev.dvolume = int(items[6])
    rev.price = int(items[7])
    rev.high = int(items[8])
    rev.low = int(items[9])
    rev.bid_price = int(items[10])
    rev.bid_volume = int(items[11])
    rev.ask_price = int(items[12])
    rev.ask_volume = int(items[13])
    return rev

def read_ticks(instrument,tday=0,length = 36000,extractor=extract_tick,readfunc = read_data):
    #读取指定日数据
    records = readfunc(make_tick_filename(instrument,tday),extractor)
    for record in records:
        record.instrument = instrument
    return records[-length:]


##############################################
##时间轮转
##############################################
def time_period_switch(data):
    '''
        判断分钟数据是否是3/5/15/30的卡点, 并计算相关数据
    '''
    #if(len(data.sdate) == 0):   #该合约史上第一分钟,不引起切换. 这个在外部保障
    #    return
    assert len(data.sdate)>0
    fpreparer = IF_XPREPARER if is_if(data.instrument) else CM_XPREPARER
    if fpreparer.ISEND_3(data.stime[-1]) and (len(data.m3[IDATE])==0 
                                        or data.sdate[-1] > data.m3[IDATE][-1] 
                                        or data.stime[-1] > data.m3[ITIME][-1]
                                    ):#添加新的3分钟
        append1(data.m3,data,3)
    if fpreparer.ISEND_5(data.stime[-1]) and (len(data.m5[IDATE])==0 
                                        or data.sdate[-1] > data.m5[IDATE][-1] 
                                        or data.stime[-1] > data.m5[ITIME][-1]
                                    ):#添加新的5分钟
        append1(data.m5,data,5)
    if fpreparer.ISEND_15(data.stime[-1]) and (len(data.m15[IDATE])==0 
                                        or data.sdate[-1] > data.m15[IDATE][-1] 
                                        or data.stime[-1] > data.m15[ITIME][-1]
                                    ):#添加新的15分钟
        append1(data.m15,data,15)
    if fpreparer.ISEND_30(data.stime[-1]) and (len(data.m30[IDATE])==0 
                                        or data.sdate[-1] > data.m30[IDATE][-1] 
                                        or data.stime[-1] > data.m30[ITIME][-1]
                                    ):#添加新的30分钟
        append1(data.m30,data,30)
    if fpreparer.ISEND_DAY(data.stime[-1]) and (len(data.d1[IDATE])==0 
                                        or data.sdate[-1] > data.d1[IDATE][-1] 
                                    ):#添加新的日数据
        append1(data.m15,data,270)
 
def append1(xdata,data1,length):
    '''
        将data1中最后length的数据组合以后放入xdata
    '''
    mlen = min(len(data1.sdate),length)
    xdata[IDATE].append(data1.sdate[-1])
    xdata[ITIME].append(data1.stime[-1])
    xdata[IOPEN].append(data1.sopen[-mlen])
    xdata[ICLOSE].append(data1.sclose[-1])
    xdata[IHIGH].append(max(data1.shigh[-mlen:]))
    xdata[ILOW].append(min(data1.slow[-mlen:]))
    xdata[IVOL].append(sum(data1.svolume[-mlen:]))
    xdata[IHOLDING].append(data1.sholding[-1])

