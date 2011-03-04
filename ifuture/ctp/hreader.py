# -*- coding: utf-8 -*-

import zipfile

from base import *

def extract_if(line):
    items = line.split(',')
    record = BaseObject()
    record.date = int(items[0].replace('/',''))
    record.time = int(items[1].replace(':',''))
    if float(items[2]) < 10000:
        record.open = int(float(items[2])*10 + 0.1)
        record.high = int(float(items[3])*10 + 0.1)
        record.low = int(float(items[4])*10 + 0.1)
        record.close = int(float(items[5])*10 + 0.1)
    else:
        record.open = int(float(items[2]) + 0.1)
        record.high = int(float(items[3]) + 0.1)
        record.low = int(float(items[4]) + 0.1)
        record.close = int(float(items[5]) + 0.1)
    record.vol = int(float(items[6]) + 0.1)
    record.holding = int(float(items[7]) + 0.1)
    return record

def read_if(filename,extractor=extract_if):
    file = open(filename,'r')
    data = file.read()
    file.close()
    return read_records(data,extractor)

def read_if_zip(filename,extractor=extract_if):
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

def read_if_as_list(filename,length,extractor=extract_if,readfunc = read_if):
    records = readfunc(filename,extractor)
    n = min(len(records),length)
    tran_data = [[0]*n,[0]*n,[0]*n,[0]*n,[0]*n,[0]*n,[0]*n,[0]*n,[0]*n,]
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

def read1(name,length=3900,path='data/',extractor=extract_if,readfunc=read_if,suffix=SUFFIX):
    #3900是13天，足够应付120个30分钟
    hdata = BaseObject(name=name,transaction=read_if_as_list(path + prefix + name + suffix,length=length,extractor=extractor,readfunc=readfunc))
    return hdata

read1_zip = fcustom(read1,readfunc=read_if_zip,suffix=SUFFIX_ZIP)

