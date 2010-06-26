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
    record.vopen = int(float(items[6]) + 0.1)
    record.vclose = int(float(items[7]) + 0.1)

    return record

FPATH = 'D:/work/applications/gcode/wolfox/data/ifuture/'
prefix = 'SF'
IFS = 'IF1005','IF1006','IF1007','IF1009','IF1012' #,'RU1011','FU1009','CU1009'
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
    sif.i_cof5 = np.where(trans[ITIME]%5==0)[0]    #5分钟收盘线,不考虑隔日的因素
    sif.i_oof5 = rollx(sif.i_cof5)+1    
    sif.close5 = trans[ICLOSE][sif.i_cof5]
    #sif.open5 = rollx(sif.close5)   #open5看作是上一个的收盘价,其它方式对应open和close以及还原的逻辑比较复杂
    sif.open5 = trans[IOPEN][sif.i_oof5]
    sif.high5 = tmax(trans[IHIGH],5)[sif.i_cof5]
    sif.low5 = tmin(trans[ILOW],5)[sif.i_cof5]
    sif.atr5 = atr(sif.close5,sif.high5,sif.low5,20)
    sif.xatr5 = sif.atr5 * XBASE * XBASE / sif.close5
    sif.mxatr5 = ma(sif.xatr5,13)
    sif.diff5x,sif.dea5x = cmacd(sif.close5*FBASE)
    sif.diff5x5,sif.dea5x5 = cmacd(sif.close5*FBASE,60,130,45)    

    sif.sdiff5x,sif.sdea5x = np.zeros_like(trans[ICLOSE]),np.zeros_like(trans[ICLOSE])
    sif.sdiff5x[sif.i_cof5] = sif.diff5x
    sif.sdea5x[sif.i_cof5] = sif.dea5x
    sif.sdiff5x=extend2next(sif.sdiff5x)
    sif.sdea5x=extend2next(sif.sdea5x)

    strend_macd5x = strend(sif.diff5x-sif.dea5x)
    sif.smacd5x = np.zeros_like(trans[ICLOSE])
    sif.smacd5x[sif.i_cof5] = strend_macd5x
    sif.seacd5x=extend2next(sif.smacd5x)


    sif.i_cof30 = np.where(gor(trans[ITIME]%100==15,trans[ITIME]%100==45))[0]    #30分钟收盘线,不考虑隔日的因素
    sif.i_oof30 = rollx(sif.i_cof30)+1    
    sif.close30 = trans[ICLOSE][sif.i_cof30]
    #sif.open30 = rollx(sif.close30)   #open5看作是上一个的收盘价,其它方式对应open和close以及还原的逻辑比较复杂
    sif.open30 = trans[IOPEN][sif.i_oof30]
    sif.high30 = tmax(trans[IHIGH],30)[sif.i_cof30]
    sif.low30 = tmin(trans[ILOW],30)[sif.i_cof30]
    sif.atr30 = atr(sif.close30,sif.high30,sif.low30,20)
    sif.xatr30 = sif.atr30 * XBASE * XBASE / sif.close30
    sif.mxatr30 = ma(sif.xatr30,13)
    sif.diff30x,sif.dea30x = cmacd(sif.close30*FBASE)

    sif.sdiff30x,sif.sdea30x = np.zeros_like(trans[ICLOSE]),np.zeros_like(trans[ICLOSE])
    sif.sdiff30x[sif.i_cof30] = sif.diff30x
    sif.sdea30x[sif.i_cof30] = sif.dea30x
    sif.sdiff30x=extend2next(sif.sdiff30x)
    sif.sdea30x=extend2next(sif.sdea30x)


    sif.i_cof15 = np.where((trans[ITIME]%100)%15==14)[0]    #5分钟收盘线,不考虑隔日的因素
    sif.i_oof15 = rollx(sif.i_cof15)+1
    sif.close15 = trans[ICLOSE][sif.i_cof15]
    #sif.open15 = rollx(sif.close15)   #open5看作是上一个的收盘价,其它方式对应open和close以及还原的逻辑比较复杂
    sif.open15 = trans[IOPEN][sif.i_oof15]
    sif.high15 = tmax(trans[IHIGH],15)[sif.i_cof15] #算上上一个收盘
    sif.low15 = tmin(trans[ILOW],15)[sif.i_cof15]
    sif.atr15 = atr(sif.close15,sif.high15,sif.low15,20)
    sif.xatr15 = sif.atr15 * XBASE * XBASE / sif.close15
    sif.mxatr15 = ma(sif.xatr15,13)
    sif.diff15x,sif.dea15x = cmacd(sif.close15*FBASE)
    sif.diff15x5,sif.dea15x5 = cmacd(sif.close15*FBASE,60,130,45)    

    sif.sdiff15x,sif.sdea15x = np.zeros_like(trans[ICLOSE]),np.zeros_like(trans[ICLOSE])
    sif.sdiff15x[sif.i_cof15] = sif.diff15x
    sif.sdea15x[sif.i_cof15] = sif.dea15x
    sif.sdiff15x=extend2next(sif.sdiff15x)
    sif.sdea15x=extend2next(sif.sdea15x)


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

