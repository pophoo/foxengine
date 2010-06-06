# -*- coding: utf-8 -*-

from wolfox.fengine.ifuture.ibase import *


def read_if_as_np(filename):
    records = read_if(filename)
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
        narrays[IVOL][i] = record.vopen
        narrays[IHOLDING][i] = record.vclose
        narrays[IMID][i] = (record.close*4 + record.low + record.high)/6
        i += 1
    return narrays

def read_if(filename):
    records = []
    for line in file(filename):
        if len(line.strip()) > 0:
            records.append(extract_if(line))
    return records


def extract_if(line):
    items = line.split(',')
    record = BaseObject()
    record.date = int(items[0].replace('/',''))
    record.time = int(items[1].replace(':',''))
    record.open = int(float(items[2])*10 + 0.1)
    record.high = int(float(items[3])*10 + 0.1)
    record.low = int(float(items[4])*10 + 0.1)
    record.close = int(float(items[5])*10 + 0.1)
    record.vopen = int(float(items[6]) + 0.1)
    record.vclose = int(float(items[7]) + 0.1)
    return record

FPATH = 'D:/work/applications/gcode/wolfox/data/ifuture/'
prefix = 'SF'
IFS = 'IF1006','IF1007','IF1009','IF1012',
SUFFIX = '.txt'

def read_ifs():
    ifs = {}
    for ifn in IFS:
        ifs[ifn] = BaseObject(name=ifn,transaction=read_if_as_np(FPATH + prefix + ifn + SUFFIX))
        prepare_index(ifs[ifn])
        #prepare_index2(ifs[ifn])
    return ifs

FBASE=10    #只用于macd提高精度，因为是整数运算，再往上就要溢出了

def prepare_index(sif):
    trans = sif.transaction
    sif.diff1,sif.dea1 = cmacd(trans[ICLOSE]*FBASE)
    sif.diff5,sif.dea5 = cmacd(trans[ICLOSE]*FBASE,60,130,45)
    sif.diff15,sif.dea15 = cmacd(trans[ICLOSE]*FBASE,180,390,135)
    sif.diff30,sif.dea30 = cmacd(trans[ICLOSE]*FBASE,360,780,270)
    sif.diff60,sif.dea60 = cmacd(trans[ICLOSE]*FBASE,720,1560,540)
    sif.ma3 = ma(trans[ICLOSE],3)
    sif.ma5 = ma(trans[ICLOSE],5)
    sif.ma10 = ma(trans[ICLOSE],10)
    sif.ma7 = ma(trans[ICLOSE],7)
    sif.ma13 = ma(trans[ICLOSE],13)    
    sif.ma20 = ma(trans[ICLOSE],20)
    sif.ma30 = ma(trans[ICLOSE],30)
    sif.ma60 = ma(trans[ICLOSE],60)
    sif.atr = atr(trans[ICLOSE],trans[IHIGH],trans[ILOW],20)
    sif.atr2 = atr2(trans[ICLOSE],trans[IHIGH],trans[ILOW],20)    
    sif.xatr = sif.atr * XBASE * XBASE / trans[ICLOSE]
    sif.mxatr = ma(sif.xatr,13)

def prepare_index2(sif):
    trans = sif.transaction
    sif.diff1,sif.dea1 = cmacd(trans[IMID]*FBASE)
    sif.diff5,sif.dea5 = cmacd(trans[IMID]*FBASE,60,130,45)
    sif.diff15,sif.dea15 = cmacd(trans[IMID]*FBASE,180,390,135)
    sif.diff30,sif.dea30 = cmacd(trans[IMID]*FBASE,360,780,270)
    sif.diff60,sif.dea60 = cmacd(trans[IMID]*FBASE,720,1560,540)
    sif.ma3 = ma(trans[IMID],3)
    sif.ma5 = ma(trans[IMID],5)
    sif.ma10 = ma(trans[IMID],10)
    sif.ma7 = ma(trans[IMID],7)
    sif.ma13 = ma(trans[IMID],13)    
    sif.ma20 = ma(trans[IMID],20)
    sif.ma30 = ma(trans[IMID],30)
    sif.ma60 = ma(trans[IMID],60)
    sif.atr = atr(trans[IMID],trans[IHIGH],trans[ILOW],20)
    sif.atr2 = atr2(trans[IMID],trans[IHIGH],trans[ILOW],20)    
    sif.xatr = sif.atr * XBASE * XBASE / trans[IMID]
    sif.mxatr = ma(sif.xatr,13)    
