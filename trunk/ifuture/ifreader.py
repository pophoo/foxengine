# -*- coding: utf-8 -*-

import zipfile

from wolfox.fengine.ifuture.ibase import *
import wolfox.fengine.ifuture.fcore as fcore


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

def extract_if_wh(line):
    items = line.split(',')
    record = BaseObject()
    xdate = items[0].replace('/','')   #从mm/dd/yyyy转为yyyymmdd
    record.date = int(xdate[-4:] + xdate[:-4])
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
    #items[6]为平均价
    record.vol = int(float(items[7]) + 0.1)
    record.holding = int(float(items[8]) + 0.1)

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
            if record.time < 1516 and record.time > 900:  #排除错误数据
                records.append(record)
    return records

def read_if_as_np(filename,extractor=extract_if,readfunc = read_if):
    records = readfunc(filename,extractor)
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

FPATH = 'D:/work/applications/gcode/wolfox/data/ifuture/'
FPATH2 = 'D:/work/applications/gcode/wolfox/fengine/ifuture/data/'
prefix = 'SF'
#IFS = 'IF0001','IF1005','IF1006','IF1007','IF1008','IF1009','IF1010','IF1012','IF1103'#,'RU1011','FU1009','CU1011','CU1009'
IFS = 'IF0001','IF1012','IF1101'
#IF0000:当月连续，当某日收盘下月合约持仓超过本月90%时切换
SUFFIX = '.txt'
SUFFIX_ZIP = '.zip'

def readp(path,name,extractor=extract_if,readfunc=read_if,suffix=SUFFIX):
    ifs = {}
    ifs[name] = BaseObject(name=name,transaction=read_if_as_np(path + name + suffix,extractor=extractor,readfunc=readfunc))
    prepare_index(ifs[name])
    return ifs

def read1(name,extractor=extract_if,readfunc=read_if,suffix=SUFFIX):
    ifs = {}
    ifs[name] = BaseObject(name=name,transaction=read_if_as_np(FPATH + prefix + name + suffix,extractor=extractor,readfunc=readfunc))
    prepare_index(ifs[name])
    return ifs

def read_ifs(extractor=extract_if,names=IFS,path=FPATH,readfunc=read_if,suffix=SUFFIX):
    ifs = {}
    for ifn in names:
        ifs[ifn] = BaseObject(name=ifn,transaction=read_if_as_np(path + prefix + ifn + suffix,extractor=extractor,readfunc=readfunc))
        prepare_index(ifs[ifn])
    return ifs

read_ifs2 = fcustom(read_ifs,path=FPATH2)
read_ifs = fcustom(read_ifs,path=FPATH2)

read_ifs2_zip = fcustom(read_ifs,path=FPATH2,readfunc=read_if_zip,suffix=SUFFIX_ZIP)
read_ifs_zip = fcustom(read_ifs,path=FPATH2,readfunc=read_if_zip,suffix=SUFFIX_ZIP)


FBASE=10    #只用于macd提高精度，因为是整数运算，再往上就要溢出了

def prepare_index(sif):
    trans = sif.transaction
    
    sif.close = trans[ICLOSE]
    sif.open = trans[IOPEN]
    sif.high = trans[IHIGH]
    sif.low = trans[ILOW]
    sif.vol = trans[IVOL]
    sif.holding = trans[IHOLDING]
    sif.mid = trans[IMID]
    sif.i_cof = sif.i_oof = np.arange(len(sif.close))
    sif.index = sif.i_cof
    sif.time = trans[ITIME]
    sif.date = trans[IDATE]

    
    fcore.dpeak(sif)    #设置当日的高低点及其坐标 dhigh/dlow
    fcore.dpeak2(sif)    #设置当日的暴力起涨/跌点
    fcore.dopen(sif)    #设置当日的开盘点位

    sif.diff1,sif.dea1 = cmacd(trans[ICLOSE]*FBASE)
    sif.diff2,sif.dea2 = cmacd(trans[ICLOSE]*FBASE,19,39,15)    
    sif.diff3,sif.dea3 = cmacd(trans[ICLOSE]*FBASE,36,78,27)
    sif.diff5,sif.dea5 = cmacd(trans[ICLOSE]*FBASE,60,130,45)
    sif.diff15,sif.dea15 = cmacd(trans[ICLOSE]*FBASE,180,390,135)
    sif.diff30,sif.dea30 = cmacd(trans[ICLOSE]*FBASE,360,780,270)
    sif.diff60,sif.dea60 = cmacd(trans[ICLOSE]*FBASE,720,1560,540)
    sif.di30,sif.de30 = smacd(trans[ICLOSE]*FBASE,360,780,270)  #计算误差太大，改用非指数版
    sif.di60,sif.de60 = smacd(trans[ICLOSE]*FBASE,720,1560,540)  #计算误差太大，改用非指数版

    sif.macd1 = sif.diff1-sif.dea1
    sif.macd3 = sif.diff3-sif.dea3    
    sif.macd5 = sif.diff5-sif.dea5
    sif.macd15 = sif.diff15-sif.dea15
    sif.macd30 = sif.diff30-sif.dea30    
    sif.macd60 = sif.diff60-sif.dea60    

    sif.svap1,sif.v2i1 = svap_ma(sif.vol,sif.close,67)
    sif.svap2_1,sif.v2i2_1 = svap_ma(sif.vol,sif.close,67,weight=2)

    sif.ma3 = ma(trans[ICLOSE],3)
    sif.ma5 = ma(trans[ICLOSE],5)
    sif.ma10 = ma(trans[ICLOSE],10)
    sif.ma7 = ma(trans[ICLOSE],7)
    sif.ma13 = ma(trans[ICLOSE],13)    
    sif.ma20 = ma(trans[ICLOSE],20)
    sif.ma30 = ma(trans[ICLOSE],30)
    sif.ma60 = ma(trans[ICLOSE],60)
    sif.ma90 = ma(trans[ICLOSE],90)    
    sif.ma120 = ma(trans[ICLOSE],120)  
    sif.ma135 = ma(trans[ICLOSE],135)    
    sif.ma270 = ma(trans[ICLOSE],270)        
    sif.atr = atr(trans[ICLOSE]*XBASE,trans[IHIGH]*XBASE,trans[ILOW]*XBASE,20)
    sif.atr2 = atr2(trans[ICLOSE]*XBASE,trans[IHIGH]*XBASE,trans[ILOW]*XBASE,20)    
    sif.xatr = sif.atr * XBASE * XBASE / trans[ICLOSE]
    sif.mxatr = ma(sif.xatr,13)
    sif.xatr2 = sif.atr2 * XBASE * XBASE / trans[ICLOSE]
    sif.mxatr2 = ma(sif.xatr2,13)


    sif.sk,sif.sd = skdj(sif.high,sif.low,sif.close)

    sm270 = sif.ma270 - rollx(sif.ma270)
    sif.state_270 = msum(sm270,20)
    sif.state_270s = strend(sif.state_270)

    sm135 = sif.ma135 - rollx(sif.ma135)
    sif.state_135 = msum(sm135,20)
    sif.state_135s = strend(sif.state_135)

    sm60 = sif.ma60 - rollx(sif.ma60)
    sif.state_60 = msum(sm60,20)
    sif.state_60s = strend(sif.state_60)

    sm30 = sif.ma30 - rollx(sif.ma30)
    sif.state_30 = msum(sm30,20)
    sif.state_30s = strend(sif.state_30)

    sif.i_cof5 = np.where(
            gor(
                #gand(trans[ITIME]%5==0,trans[ITIME]%1000 != 915)
                gand((trans[ITIME]+1)%5==0,trans[ITIME]%1000 != 914)
                ,gand(trans[ITIME]%10000 == 1514,rollx(trans[ITIME],-1)%10000!=1515) #如果没有1515，则取1514
            )
        )[0]    #5分钟收盘线,不考虑隔日的因素
    sif.i_oof5 = roll0(sif.i_cof5)+1    
    sif.i_oof5[0] = 0
    sif.close5 = trans[ICLOSE][sif.i_cof5]
    #sif.open5 = rollx(sif.close5)   #open5看作是上一个的收盘价,其它方式对应open和close以及还原的逻辑比较复杂
    sif.open5 = trans[IOPEN][sif.i_oof5]
    #sif.high5 = tmax(trans[IHIGH],5)[sif.i_cof5]
    #sif.low5 = tmin(trans[ILOW],5)[sif.i_cof5]
    sif.high5,sif.low5,sif.vol5 = calc_high_low_vol(trans,sif.i_oof5,sif.i_cof5)
    sif.holding5 = trans[IHOLDING][sif.i_cof5]


    sif.atr5 = atr(sif.close5*XBASE,sif.high5*XBASE,sif.low5*XBASE,20)
    sif.xatr5 = sif.atr5 * XBASE * XBASE / sif.close5
    sif.mxatr5 = ma(sif.xatr5,13)
    sif.xatr5x = np.zeros_like(trans[ICLOSE])
    sif.xatr5x[sif.i_cof5] = sif.xatr5
    sif.xatr5x = extend2next(sif.xatr5x)
    sif.mxatr5x = np.zeros_like(trans[ICLOSE])
    sif.mxatr5x[sif.i_cof5] = sif.mxatr5
    sif.mxatr5x = extend2next(sif.mxatr5x)

    sif.atr5x = np.zeros_like(trans[ICLOSE])
    sif.atr5x[sif.i_cof5] = sif.atr5
    sif.atr5x = extend2next(sif.atr5x)
    
    sif.diff5x,sif.dea5x = cmacd(sif.close5*FBASE)
    sif.diff5x5,sif.dea5x5 = cmacd(sif.close5*FBASE,60,130,45)    

    sif.sdiff5x,sif.sdea5x = np.zeros_like(trans[ICLOSE]),np.zeros_like(trans[ICLOSE])
    sif.sdiff5x[sif.i_cof5] = sif.diff5x
    sif.sdea5x[sif.i_cof5] = sif.dea5x
    sif.sdiff5x=extend2next(sif.sdiff5x)
    sif.sdea5x=extend2next(sif.sdea5x)

    strend_macd5x = strend2(sif.diff5x-sif.dea5x)
    sif.smacd5x = np.zeros_like(trans[ICLOSE])
    sif.smacd5x[sif.i_cof5] = strend_macd5x
    sif.smacd5x=extend2next(sif.smacd5x)


    ##3分钟,与文华一致
    sif.i_cof3 = np.where(
            gor(gand((trans[ITIME]%100)%3 == 2)
                ,gand(trans[ITIME]%10000 == 1514,rollx(trans[ITIME],-1)%10000!=1515) #如果没有1515，则取1514
            )
        )[0]    #5分钟收盘线,不考虑隔日的因素
    sif.i_oof3 = roll0(sif.i_cof3)+1    
    sif.i_oof3[0] = 0
    sif.close3 = trans[ICLOSE][sif.i_cof3]
    #sif.open3 = rollx(sif.close3)   #open3看作是上一个的收盘价,其它方式对应open和close以及还原的逻辑比较复杂
    sif.open3 = trans[IOPEN][sif.i_oof3]
    #sif.high3 = tmax(trans[IHIGH],3)[sif.i_cof3]
    #sif.low3 = tmin(trans[ILOW],3)[sif.i_cof3]
    sif.high3,sif.low3,sif.vol3 = calc_high_low_vol(trans,sif.i_oof3,sif.i_cof3)
    sif.holding3 = trans[IHOLDING][sif.i_cof3]


    sif.atr3 = atr(sif.close3*XBASE,sif.high3*XBASE,sif.low3*XBASE,20)
    sif.xatr3 = sif.atr3 * XBASE * XBASE / sif.close3
    sif.mxatr3 = ma(sif.xatr3,13)
    sif.xatr3x = np.zeros_like(trans[ICLOSE])
    sif.xatr3x[sif.i_cof3] = sif.xatr3
    sif.xatr3x = extend2next(sif.xatr3x)
    sif.mxatr3x = np.zeros_like(trans[ICLOSE])
    sif.mxatr3x[sif.i_cof3] = sif.mxatr3
    sif.mxatr3x = extend2next(sif.mxatr3x)

    sif.atr3x = np.zeros_like(trans[ICLOSE])
    sif.atr3x[sif.i_cof3] = sif.atr3
    sif.atr3x = extend2next(sif.atr3x)
    

    sif.diff3x,sif.dea3x = cmacd(sif.close3*FBASE)
    sif.diff3x5,sif.dea3x5 = cmacd(sif.close3*FBASE,60,130,45)    

    sif.sdiff3x,sif.sdea3x = np.zeros_like(trans[ICLOSE]),np.zeros_like(trans[ICLOSE])
    sif.sdiff3x[sif.i_cof3] = sif.diff3x
    sif.sdea3x[sif.i_cof3] = sif.dea3x
    sif.sdiff3x=extend2next(sif.sdiff3x)
    sif.sdea3x=extend2next(sif.sdea3x)

    strend_macd3x = strend2(sif.diff3x-sif.dea3x)
    sif.smacd3x = np.zeros_like(trans[ICLOSE])
    sif.smacd3x[sif.i_cof3] = strend_macd3x
    sif.smacd3x=extend2next(sif.smacd3x)

    ##10分钟
    #sif.i_cof10 = np.where(
    #        gor(gand((trans[ITIME]%10) == 0)#,trans[ITIME]%1000!=915)
    #            ,gand(trans[ITIME]%10000 == 1514,rollx(trans[ITIME],-1)%10000!=1515) #如果没有1515，则取1514
    #        )
    #    )[0]    #5分钟收盘线,不考虑隔日的因素
    sif.i_cof10 = np.where(
            gor(gand((trans[ITIME]+1)%10 == 0)#,trans[ITIME]%1000!=915)
                ,gand(trans[ITIME]%10000 == 1514,rollx(trans[ITIME],-1)%10000!=1515) #如果没有1515，则取1514
            )
        )[0]    #10分钟收盘线,不考虑隔日的因素. 文华方式(00-09为10分钟范围) 同花顺为01-10
    sif.i_oof10 = roll0(sif.i_cof10)+1    
    sif.i_oof10[0] = 0
    sif.close10 = trans[ICLOSE][sif.i_cof10]
    #sif.open10 = rollx(sif.close10)   #open10看作是上一个的收盘价,其它方式对应open和close以及还原的逻辑比较复杂
    sif.open10 = trans[IOPEN][sif.i_oof10]
    #sif.high10 = tmax(trans[IHIGH],10)[sif.i_cof10]
    #sif.low10 = tmin(trans[ILOW],10)[sif.i_cof10]
    sif.high10,sif.low10,sif.vol10 = calc_high_low_vol(trans,sif.i_oof10,sif.i_cof10)
    sif.holding10 = trans[IHOLDING][sif.i_cof10]


    sif.atr10 = atr(sif.close10*XBASE,sif.high10*XBASE,sif.low10*XBASE,20)
    sif.xatr10 = sif.atr10 * XBASE * XBASE / sif.close10
    sif.mxatr10 = ma(sif.xatr10,13)
    sif.xatr10x = np.zeros_like(trans[ICLOSE])
    sif.xatr10x[sif.i_cof10] = sif.xatr10
    sif.xatr10x = extend2next(sif.xatr10x)
    sif.mxatr10x = np.zeros_like(trans[ICLOSE])
    sif.mxatr10x[sif.i_cof10] = sif.mxatr10
    sif.mxatr10x = extend2next(sif.mxatr10x)

    sif.atr10x = np.zeros_like(trans[ICLOSE])
    sif.atr10x[sif.i_cof10] = sif.atr10
    sif.atr10x = extend2next(sif.atr10x)
    

    sif.diff10x,sif.dea10x = cmacd(sif.close10*FBASE)
    sif.diff10x5,sif.dea10x5 = cmacd(sif.close10*FBASE,60,130,45)    

    sif.sdiff10x,sif.sdea10x = np.zeros_like(trans[ICLOSE]),np.zeros_like(trans[ICLOSE])
    sif.sdiff10x[sif.i_cof10] = sif.diff10x
    sif.sdea10x[sif.i_cof10] = sif.dea10x
    sif.sdiff10x=extend2next(sif.sdiff10x)
    sif.sdea10x=extend2next(sif.sdea10x)

    strend_macd10x = strend2(sif.diff10x-sif.dea10x)
    sif.smacd10x = np.zeros_like(trans[ICLOSE])
    sif.smacd10x[sif.i_cof10] = strend_macd10x
    sif.smacd10x=extend2next(sif.smacd10x)
    
    #30分钟
    sif.i_cof30 = np.where(gor(
        gand(trans[ITIME]%10000==1514,rollx(trans[ITIME],-1)%10000!=1515)   #当不存在1515时，1514
        ,trans[ITIME]%10000==1515
        ,trans[ITIME]%10000==1415
        ,trans[ITIME]%10000==1315
        ,trans[ITIME]%10000==1115
        ,trans[ITIME]%10000==1015
        #,trans[ITIME]%10000==915
        ,trans[ITIME]%100==45))[0]    #30分钟收盘线,不考虑隔日的因素
    #sif.i_cof30 = np.where(gor(
    #    trans[ITIME]%10000==1514
    #    ,trans[ITIME]%10000==1414
    #    ,trans[ITIME]%10000==1314
    #    ,trans[ITIME]%10000==1114
    #    ,trans[ITIME]%10000==1014
    #    ,trans[ITIME]%100==45))[0]    #30分钟收盘线,不考虑隔日的因素
    sif.i_cof30 = np.where(
            gand(
                gor(
                    trans[ITIME]%100==14
                    ,trans[ITIME]%100==44
                    )
                ,trans[ITIME]%1000!=914
            )
        )[0]    #30分钟收盘线,不考虑隔日的因素
    
    sif.i_oof30 = roll0(sif.i_cof30)+1    
    sif.i_oof30[0] = 0    
    sif.close30 = trans[ICLOSE][sif.i_cof30]
    #sif.close30 = ((sif.close+sif.open)/2)[sif.i_cof30]
    #sif.open30 = rollx(sif.close30)   #open5看作是上一个的收盘价,其它方式对应open和close以及还原的逻辑比较复杂
    sif.open30 = trans[IOPEN][sif.i_oof30]
    #sif.high30 = tmax(trans[IHIGH],30)[sif.i_cof30]
    #sif.low30 = tmin(trans[ILOW],30)[sif.i_cof30]
    sif.high30,sif.low30,sif.vol30 = calc_high_low_vol(trans,sif.i_oof30,sif.i_cof30)
    sif.holding30 = trans[IHOLDING][sif.i_cof30]


    sif.atr30 = atr(sif.close30*XBASE,sif.high30*XBASE,sif.low30*XBASE,20)
    sif.xatr30 = sif.atr30 * XBASE * XBASE / sif.close30
    sif.mxatr30 = ma(sif.xatr30,13)
    sif.xatr30x = np.zeros_like(trans[ICLOSE])
    sif.xatr30x[sif.i_cof30] = sif.xatr30
    sif.xatr30x = extend2next(sif.xatr30x)
    sif.mxatr30x = np.zeros_like(trans[ICLOSE])
    sif.mxatr30x[sif.i_cof30] = sif.mxatr30
    sif.mxatr30x = extend2next(sif.mxatr30x)

    sif.atr30x = np.zeros_like(trans[ICLOSE])
    sif.atr30x[sif.i_cof30] = sif.atr30
    sif.atr30x = extend2next(sif.atr30x)
 
    sif.atr2_30 = atr2(sif.close30*XBASE,sif.high30*XBASE,sif.low30*XBASE,20)
    sif.xatr2_30 = sif.atr2_30 * XBASE * XBASE / sif.close30
    sif.mxatr2_30 = ma(sif.xatr2_30,13)
    sif.xatr2_30x = np.zeros_like(trans[ICLOSE])
    sif.xatr2_30x[sif.i_cof30] = sif.xatr2_30
    sif.xatr2_30x = extend2next(sif.xatr2_30x)
    sif.mxatr2_30x = np.zeros_like(trans[ICLOSE])
    sif.mxatr2_30x[sif.i_cof30] = sif.mxatr2_30
    sif.mxatr2_30x = extend2next(sif.mxatr2_30x)

    sif.atr2_30x = np.zeros_like(trans[ICLOSE])
    sif.atr2_30x[sif.i_cof30] = sif.atr2_30
    sif.atr2_30x = extend2next(sif.atr2_30x)


    sif.diff30x,sif.dea30x = cmacd(sif.close30*FBASE)

    sif.sdiff30x,sif.sdea30x = np.zeros_like(trans[ICLOSE]),np.zeros_like(trans[ICLOSE])
    sif.sdiff30x[sif.i_cof30] = sif.diff30x
    sif.sdea30x[sif.i_cof30] = sif.dea30x
    sif.sdiff30x=extend2next(sif.sdiff30x)
    sif.sdea30x=extend2next(sif.sdea30x)

    strend_macd30x = strend2(sif.diff30x-sif.dea30x)
    sif.smacd30x = np.zeros_like(trans[ICLOSE])
    sif.smacd30x[sif.i_cof30] = strend_macd30x
    sif.smacd30x=extend2next(sif.smacd30x)


    sif.i_cof15 = np.where(
            gand(
                gor(
                    #trans[ITIME]%100==15
                    #,trans[ITIME]%100==30
                    #,trans[ITIME]%100==45
                    #,trans[ITIME]%100==0
                    #,gand(trans[ITIME]%10000 == 1514,rollx(trans[ITIME],-1)%10000!=1515)   #当不存在1515时，取1514                    
                    trans[ITIME]%100==14
                    ,trans[ITIME]%100==29
                    ,trans[ITIME]%100==44
                    ,trans[ITIME]%100==59
                    )
                ,trans[ITIME]%1000!=914
            )
        )[0]    #15分钟收盘线,不考虑隔日的因素
    sif.i_oof15 = roll0(sif.i_cof15)+1
    sif.i_oof15[0] = 0    
    sif.close15 = trans[ICLOSE][sif.i_cof15]
    #sif.open15 = rollx(sif.close15)   #open5看作是上一个的收盘价,其它方式对应open和close以及还原的逻辑比较复杂
    sif.open15 = trans[IOPEN][sif.i_oof15]
    #sif.high15 = tmax(trans[IHIGH],15)[sif.i_cof15] #算上上一个收盘
    #sif.low15 = tmin(trans[ILOW],15)[sif.i_cof15]
    sif.high15,sif.low15,sif.vol15 = calc_high_low_vol(trans,sif.i_oof15,sif.i_cof15)
    sif.holding15 = trans[IHOLDING][sif.i_cof15]


    sif.atr15 = atr(sif.close15*XBASE,sif.high15*XBASE,sif.low15*XBASE,20)
    sif.xatr15 = sif.atr15 * XBASE * XBASE / sif.close15
    sif.mxatr15 = ma(sif.xatr15,13)
    sif.xatr15x = np.zeros_like(trans[ICLOSE])
    sif.xatr15x[sif.i_cof15] = sif.xatr15
    sif.xatr15x = extend2next(sif.xatr15x)
    sif.mxatr15x = np.zeros_like(trans[ICLOSE])
    sif.mxatr15x[sif.i_cof15] = sif.mxatr15
    sif.mxatr15x = extend2next(sif.mxatr15x)

    sif.atr15x = np.zeros_like(trans[ICLOSE])
    sif.atr15x[sif.i_cof15] = sif.atr15
    sif.atr15x = extend2next(sif.atr15x)
    

    sif.diff15x,sif.dea15x = cmacd(sif.close15*FBASE)
    sif.diff15x5,sif.dea15x5 = cmacd(sif.close15*FBASE,60,130,45)    

    sif.sdiff15x,sif.sdea15x = np.zeros_like(trans[ICLOSE]),np.zeros_like(trans[ICLOSE])
    sif.sdiff15x[sif.i_cof15] = sif.diff15x
    sif.sdea15x[sif.i_cof15] = sif.dea15x
    sif.sdiff15x=extend2next(sif.sdiff15x)
    sif.sdea15x=extend2next(sif.sdea15x)

    strend_macd15x = strend2(sif.diff15x-sif.dea15x)
    sif.smacd15x = np.zeros_like(trans[ICLOSE])
    sif.smacd15x[sif.i_cof15] = strend_macd15x
    sif.smacd15x=extend2next(sif.smacd15x)


    #60分钟线，每天最后半小时交易也算一小时
    #sif.i_cof60 = np.where(gor(
    #    gand(trans[ITIME]%10000==1514,rollx(trans[ITIME],-1)%10000!=1515)   #当不存在1515时，1514
    #    ,trans[ITIME]%10000==1515
    #    ,trans[ITIME]%10000==1445
    #    ,trans[ITIME]%10000==1345
    #    ,trans[ITIME]%10000==1115
    #    ,trans[ITIME]%10000==1015
    #    ))[0]    #60分钟收盘线,不考虑隔日的因素
    #sif.i_cof60 = np.where(gor(
    #    trans[ITIME]%10000==1514
    #    ,trans[ITIME]%10000==1444
    #    ,trans[ITIME]%10000==1344
    #    ,trans[ITIME]%10000==1114
    #    ,trans[ITIME]%10000==1014
    #    ))[0]    #60分钟收盘线,不考虑隔日的因素
    sif.i_cof60 = np.where(gor( #前半小时算一小时(考虑到可能的跳空)
        trans[ITIME]%10000==1514
        ,trans[ITIME]%10000==1414
        ,trans[ITIME]%10000==1314
        ,trans[ITIME]%10000==1044
        ,trans[ITIME]%10000==944
        ))[0]    #60分钟收盘线,不考虑隔日的因素
    sif.i_oof60 = roll0(sif.i_cof60)+1    
    sif.i_oof60[0] = 0    
    sif.close60 = trans[ICLOSE][sif.i_cof60]
    #sif.open60 = rollx(sif.close60)   #open60看作是上一个的收盘价,其它方式对应open和close以及还原的逻辑比较复杂
    sif.open60 = trans[IOPEN][sif.i_oof60]
    #sif.high60 = tmax(trans[IHIGH],60)[sif.i_cof60]
    #sif.low60 = tmin(trans[ILOW],60)[sif.i_cof60]
    sif.high60,sif.low60,sif.vol60 = calc_high_low_vol(trans,sif.i_oof60,sif.i_cof60)
    sif.holding60 = trans[IHOLDING][sif.i_cof60]


    sif.atr60 = atr(sif.close60*XBASE,sif.high60*XBASE,sif.low60*XBASE,20)
    sif.xatr60 = sif.atr60 * XBASE * XBASE / sif.close60
    sif.mxatr60 = ma(sif.xatr60,13)
    sif.xatr60x = np.zeros_like(trans[ICLOSE])
    sif.xatr60x[sif.i_cof60] = sif.xatr60
    sif.xatr60x = extend2next(sif.xatr60x)
    sif.mxatr60x = np.zeros_like(trans[ICLOSE])
    sif.mxatr60x[sif.i_cof60] = sif.mxatr60
    sif.mxatr60x = extend2next(sif.mxatr60x)

    sif.atr60x = np.zeros_like(trans[ICLOSE])
    sif.atr60x[sif.i_cof60] = sif.atr60
    sif.atr60x = extend2next(sif.atr60x)
    
    sif.diff60x,sif.dea60x = cmacd(sif.close60*FBASE)

    sif.sdiff60x,sif.sdea60x = np.zeros_like(trans[ICLOSE]),np.zeros_like(trans[ICLOSE])
    sif.sdiff60x[sif.i_cof60] = sif.diff60x
    sif.sdea60x[sif.i_cof60] = sif.dea60x
    sif.sdiff60x=extend2next(sif.sdiff60x)
    sif.sdea60x=extend2next(sif.sdea60x)

    strend_macd60x = strend2(sif.diff60x-sif.dea60x)
    sif.smacd60x = np.zeros_like(trans[ICLOSE])
    sif.smacd60x[sif.i_cof60] = strend_macd60x
    sif.smacd60x=extend2next(sif.smacd60x)


    #45钟线
    sif.i_cof45 = np.where(gor( 
        trans[ITIME]%10000==1514
        ,trans[ITIME]%10000==1429
        ,trans[ITIME]%10000==1344
        ,trans[ITIME]%10000==1129
        ,trans[ITIME]%10000==1044
        ,trans[ITIME]%10000==959
        ))[0]    #45分钟收盘线,不考虑隔日的因素
    sif.i_oof45 = roll0(sif.i_cof45)+1    
    sif.i_oof45[0] = 0    
    sif.close45 = trans[ICLOSE][sif.i_cof45]
    #sif.open45 = rollx(sif.close45)   #open45看作是上一个的收盘价,其它方式对应open和close以及还原的逻辑比较复杂
    sif.open45 = trans[IOPEN][sif.i_oof45]
    #sif.high45 = tmax(trans[IHIGH],45)[sif.i_cof45]
    #sif.low45 = tmin(trans[ILOW],45)[sif.i_cof45]
    sif.high45,sif.low45,sif.vol45 = calc_high_low_vol(trans,sif.i_oof45,sif.i_cof45)
    sif.holding45 = trans[IHOLDING][sif.i_cof45]


    sif.atr45 = atr(sif.close45*XBASE,sif.high45*XBASE,sif.low45*XBASE,20)
    sif.xatr45 = sif.atr45 * XBASE * XBASE / sif.close45
    sif.mxatr45 = ma(sif.xatr45,13)
    sif.xatr45x = np.zeros_like(trans[ICLOSE])
    sif.xatr45x[sif.i_cof45] = sif.xatr45
    sif.xatr45x = extend2next(sif.xatr45x)
    sif.mxatr45x = np.zeros_like(trans[ICLOSE])
    sif.mxatr45x[sif.i_cof45] = sif.mxatr45
    sif.mxatr45x = extend2next(sif.mxatr45x)

    sif.atr45x = np.zeros_like(trans[ICLOSE])
    sif.atr45x[sif.i_cof45] = sif.atr45
    sif.atr45x = extend2next(sif.atr45x)
    
    sif.diff45x,sif.dea45x = cmacd(sif.close45*FBASE)

    sif.sdiff45x,sif.sdea45x = np.zeros_like(trans[ICLOSE]),np.zeros_like(trans[ICLOSE])
    sif.sdiff45x[sif.i_cof45] = sif.diff45x
    sif.sdea45x[sif.i_cof45] = sif.dea45x
    sif.sdiff45x=extend2next(sif.sdiff45x)
    sif.sdea45x=extend2next(sif.sdea45x)

    strend_macd45x = strend2(sif.diff45x-sif.dea45x)
    sif.smacd45x = np.zeros_like(trans[ICLOSE])
    sif.smacd45x[sif.i_cof45] = strend_macd45x
    sif.smacd45x=extend2next(sif.smacd45x)


    #90钟线
    sif.i_cof90 = np.where(gor( 
        trans[ITIME]%10000==1514
        ,trans[ITIME]%10000==1344
        ,trans[ITIME]%10000==1044
        ))[0]    #90分钟收盘线,不考虑隔日的因素
    sif.i_oof90 = roll0(sif.i_cof90)+1    
    sif.i_oof90[0] = 0    
    sif.close90 = trans[ICLOSE][sif.i_cof90]
    #sif.open90 = rollx(sif.close90)   #open90看作是上一个的收盘价,其它方式对应open和close以及还原的逻辑比较复杂
    sif.open90 = trans[IOPEN][sif.i_oof90]
    #sif.high90 = tmax(trans[IHIGH],90)[sif.i_cof90]
    #sif.low90 = tmin(trans[ILOW],90)[sif.i_cof90]
    sif.high90,sif.low90,sif.vol90 = calc_high_low_vol(trans,sif.i_oof90,sif.i_cof90)
    sif.holding90 = trans[IHOLDING][sif.i_cof90]


    sif.atr90 = atr(sif.close90*XBASE,sif.high90*XBASE,sif.low90*XBASE,20)
    sif.xatr90 = sif.atr90 * XBASE * XBASE / sif.close90
    sif.mxatr90 = ma(sif.xatr90,13)
    sif.xatr90x = np.zeros_like(trans[ICLOSE])
    sif.xatr90x[sif.i_cof90] = sif.xatr90
    sif.xatr90x = extend2next(sif.xatr90x)
    sif.mxatr90x = np.zeros_like(trans[ICLOSE])
    sif.mxatr90x[sif.i_cof90] = sif.mxatr90
    sif.mxatr90x = extend2next(sif.mxatr90x)

    sif.atr90x = np.zeros_like(trans[ICLOSE])
    sif.atr90x[sif.i_cof90] = sif.atr90
    sif.atr90x = extend2next(sif.atr90x)
    
    sif.diff90x,sif.dea90x = cmacd(sif.close90*FBASE)

    sif.sdiff90x,sif.sdea90x = np.zeros_like(trans[ICLOSE]),np.zeros_like(trans[ICLOSE])
    sif.sdiff90x[sif.i_cof90] = sif.diff90x
    sif.sdea90x[sif.i_cof90] = sif.dea90x
    sif.sdiff90x=extend2next(sif.sdiff90x)
    sif.sdea90x=extend2next(sif.sdea90x)

    strend_macd90x = strend2(sif.diff90x-sif.dea90x)
    sif.smacd90x = np.zeros_like(trans[ICLOSE])
    sif.smacd90x[sif.i_cof90] = strend_macd90x
    sif.smacd90x=extend2next(sif.smacd90x)


    sif.i_cofd = np.append(np.nonzero(trans[IDATE]-rollx(trans[IDATE])>0)[0]-1,len(trans[IDATE])-1)
    sif.i_oofd = roll0(sif.i_cofd)+1
    sif.i_oofd[0]=0
    sif.opend = trans[IOPEN][sif.i_oofd]
    sif.closed = trans[ICLOSE][sif.i_cofd]
    sif.highd,sif.lowd,sif.vold = calc_high_low_vol(trans,sif.i_oofd,sif.i_cofd)
    sif.holdingd = trans[IHOLDING][sif.i_cofd]

    sif.atrd = atr(sif.closed*XBASE,sif.highd*XBASE,sif.lowd*XBASE,20)
    sif.xatrd = sif.atrd * XBASE * XBASE / sif.closed
    sif.mxatrd = ma(sif.xatrd,13)
    sif.xatrdx = np.zeros_like(trans[ICLOSE])
    sif.xatrdx[sif.i_cofd] = sif.xatrd
    sif.xatrdx = extend2next(sif.xatrdx)
    sif.mxatrdx = np.zeros_like(trans[ICLOSE])
    sif.mxatrdx[sif.i_cofd] = sif.mxatrd
    sif.mxatrdx = extend2next(sif.mxatrdx)

    sif.atrdx = np.zeros_like(trans[ICLOSE])
    sif.atrdx[sif.i_cofd] = sif.atrd
    sif.atrdx = extend2next(sif.atrdx)
    
    '''
    sif.svap3,sif.v2i3 = svap_ma(sif.vol3,sif.close3,67)
    sif.svap2_3,sif.v2i2_3 = svap_ma(sif.vol3,sif.close3,67,weight=2)

    sif.svap5,sif.v2i5 = svap_ma(sif.vol5,sif.close5,67)
    sif.svap2_5,sif.v2i2_5 = svap_ma(sif.vol5,sif.close5,67,weight=2)

    sif.svap10,sif.v2i10 = svap_ma(sif.vol10,sif.close10,67)
    sif.svap2_10,sif.v2i2_10 = svap_ma(sif.vol10,sif.close10,67,weight=2)

    sif.svap15,sif.v2i15 = svap_ma(sif.vol15,sif.close15,67)
    sif.svap2_15,sif.v2i2_15 = svap_ma(sif.vol15,sif.close15,67,weight=2)

    sif.svap30,sif.v2i30 = svap_ma(sif.vol30,sif.close30,67)
    sif.svap2_30,sif.v2i2_30 = svap_ma(sif.vol30,sif.close30,67,weight=2)

    sif.svap45,sif.v2i45 = svap_ma(sif.vol45,sif.close45,67)
    sif.svap2_45,sif.v2i2_45 = svap_ma(sif.vol45,sif.close45,67,weight=2)

    sif.svap60,sif.v2i60 = svap_ma(sif.vol60,sif.close60,67)
    sif.svap2_60,sif.v2i2_60 = svap_ma(sif.vol60,sif.close60,67,weight=2)

    sif.svap90,sif.v2i90 = svap_ma(sif.vol90,sif.close90,67)
    sif.svap2_90,sif.v2i2_90 = svap_ma(sif.vol90,sif.close90,67,weight=2)

    sif.svapd,sif.v2id = svap_ma(sif.vold,sif.closed,67)
    sif.svap2_d,sif.v2i2_d = svap_ma(sif.vold,sif.closed,67,weight=2)
    '''

    s30_7 = np.zeros_like(sif.close)
    s30_7[sif.i_cof30] = strend2(nma(sif.close30,7))  #nma避免strend2将初始批量0也当作正数计入的问题
    sif.strend = extend2next(s30_7)
    sif.t7 = sif.strend

    s30_13 = np.zeros_like(sif.close)
    s30_13[sif.i_cof30] = strend2(nma(sif.close30,13))  #nma避免strend2将初始批量0也当作正数计入的问题
    sif.mtrend = extend2next(s30_13)
    sif.t13 = sif.mtrend

    s30_120 = np.zeros_like(sif.close)
    s30_120[sif.i_cof30] = strend2(nma(sif.close30,120))    #nma避免strend2将初始批量0也当作正数计入的问题
    #sif.ltrend = extend2next(s30_120)
    #sif.t120 = sif.ltrend
    sif.t120 = extend2next(s30_120)

    s30_3 = np.zeros_like(sif.close)
    s30_3[sif.i_cof30] = strend2(nma(sif.close30,3))  #nma避免strend2将初始批量0也当作正数计入的问题
    sif.t3 = extend2next(s30_3)

    s30_30 = np.zeros_like(sif.close)
    s30_30[sif.i_cof30] = strend2(nma(sif.close30,30))  #nma避免strend2将初始批量0也当作正数计入的问题
    sif.t30 = extend2next(s30_30)

    s30_45 = np.zeros_like(sif.close)   #相当于5日线
    s30_45[sif.i_cof30] = strend2(nma(sif.close30,45))  #nma避免strend2将初始批量0也当作正数计入的问题
    sif.t45 = extend2next(s30_45)

    s30_60 = np.zeros_like(sif.close)
    s30_60[sif.i_cof30] = strend2(nma(sif.close30,60))  #nma避免strend2将初始批量0也当作正数计入的问题
    sif.t60 = extend2next(s30_60)
    
    sif.ltrend = sif.t120


    s30_90 = np.zeros_like(sif.close)
    s30_90[sif.i_cof30] = strend2(nma(sif.close30,90))  #nma避免strend2将初始批量0也当作正数计入的问题
    sif.t90 = extend2next(s30_90)

    s30x = np.zeros_like(sif.diff1)
    s30x[sif.i_cof30] = strend2(nma(sif.close30,7)-nma(sif.close30,30))
    sif.t7_30 = extend2next(s30x)

    d60 = strend2(ma(sif.diff60x-sif.dea60x,3))
    sd60 = np.zeros_like(sif.close)
    sd60[sif.i_cof60] = d60
    sif.s60 = extend2next(sd60)
 
    d30 = strend2(ma(sif.diff30x-sif.dea30x,3))
    sd30 = np.zeros_like(sif.close)
    sd30[sif.i_cof30] = d30
    sif.s30 = extend2next(sd30)
 
    d15 = strend2(ma(sif.diff15x-sif.dea15x,3))
    sd15 = np.zeros_like(sif.close)
    sd15[sif.i_cof15] = d15
    sif.s15 = extend2next(sd15)

    d10 = strend2(ma(sif.diff10x-sif.dea10x,3))
    sd10 = np.zeros_like(sif.close)
    sd10[sif.i_cof10] = d10
    sif.s10 = extend2next(sd10)


    d5 = strend2(ma(sif.diff5x-sif.dea5x,3))
    sd5 = np.zeros_like(sif.close)
    sd5[sif.i_cof5] = d5
    sif.s5 = extend2next(sd5)

    d3 = strend2(ma(sif.diff3x-sif.dea3x,3))
    sd3 = np.zeros_like(sif.close)
    sd3[sif.i_cof3] = d3
    sif.s3 = extend2next(sd3)

    sif.s1 = strend2(ma(sif.diff1-sif.dea1,3))

    r120 = np.zeros_like(sif.close)
    r120[sif.i_cof15] = strend2(nma(sif.close15,120))    #nma避免strend2将初始批量0也当作正数计入的问题
    sif.r120 = extend2next(r120)

    r90 = np.zeros_like(sif.close)
    r90[sif.i_cof15] = strend2(nma(sif.close15,90))    #nma避免strend2将初始批量0也当作正数计入的问题
    sif.r90 = extend2next(r90)

    r60 = np.zeros_like(sif.close)
    r60[sif.i_cof15] = strend2(nma(sif.close15,60))    #nma避免strend2将初始批量0也当作正数计入的问题
    sif.r60 = extend2next(r60)
    sif.rl_trend = sif.r60

    r30 = np.zeros_like(sif.close)
    r30[sif.i_cof15] = strend2(nma(sif.close15,30))    #nma避免strend2将初始批量0也当作正数计入的问题
    sif.r30 = extend2next(r30)
    sif.rm_trend = sif.r30

    r20 = np.zeros_like(sif.close)
    r20[sif.i_cof15] = strend2(nma(sif.close15,20))    #nma避免strend2将初始批量0也当作正数计入的问题
    sif.r20 = extend2next(r20)

    r13 = np.zeros_like(sif.close)
    r13[sif.i_cof15] = strend2(nma(sif.close15,13))    #nma避免strend2将初始批量0也当作正数计入的问题
    sif.r13 = extend2next(r13)
    sif.rs_trend = sif.r13

    r7 = np.zeros_like(sif.close)
    r7[sif.i_cof15] = strend2(nma(sif.close15,7))    #nma避免strend2将初始批量0也当作正数计入的问题
    sif.r7 = extend2next(r7)

    r3 = np.zeros_like(sif.close)
    r3[sif.i_cof15] = strend2(nma(sif.close15,3))    #nma避免strend2将初始批量0也当作正数计入的问题
    sif.r3 = extend2next(r3)

    sif.z3 = dnext(nma(sif.close5,3),sif.close,sif.i_cof5)
    sif.z5 = dnext(nma(sif.close5,5),sif.close,sif.i_cof5)
    sif.z7 = dnext(nma(sif.close5,7),sif.close,sif.i_cof5)
    sif.z13 = dnext(nma(sif.close5,13),sif.close,sif.i_cof5)
    sif.z20 = dnext(nma(sif.close5,20),sif.close,sif.i_cof5)
    sif.z30 = dnext(nma(sif.close5,30),sif.close,sif.i_cof5)
    sif.z40 = dnext(nma(sif.close5,40),sif.close,sif.i_cof5)
    sif.z60 = dnext(nma(sif.close5,60),sif.close,sif.i_cof5)
    sif.z80 = dnext(nma(sif.close5,80),sif.close,sif.i_cof5)
    sif.z120 = dnext(nma(sif.close5,120),sif.close,sif.i_cof5)
    sif.z250 = dnext(nma(sif.close5,250),sif.close,sif.i_cof5)

    dma5 = np.zeros_like(sif.close)
    dma5[sif.i_cofd] = strend2(nma(sif.closed,5))    #nma避免strend2将初始批量0也当作正数计入的问题
    sif.dma5 = extend2next(dma5)

    dma7 = np.zeros_like(sif.close)
    dma7[sif.i_cofd] = strend2(nma(sif.closed,7))    #nma避免strend2将初始批量0也当作正数计入的问题
    sif.dma7 = extend2next(dma7)

    dma10 = np.zeros_like(sif.close)
    dma10[sif.i_cofd] = strend2(nma(sif.closed,10))    #nma避免strend2将初始批量0也当作正数计入的问题
    sif.dma10 = extend2next(dma10)

    dma13 = np.zeros_like(sif.close)
    dma13[sif.i_cofd] = strend2(nma(sif.closed,13))    #nma避免strend2将初始批量0也当作正数计入的问题
    sif.dma13 = extend2next(dma13)

    dma20 = np.zeros_like(sif.close)
    dma20[sif.i_cofd] = strend2(nma(sif.closed,20))    #nma避免strend2将初始批量0也当作正数计入的问题
    sif.dma20 = extend2next(dma20)

    mx = np.zeros_like(sif.diff1)
    mx[sif.i_cof15] = strend2(nma(sif.close15,7)-nma(sif.close15,30))
    sif.m7_30 = extend2next(mx)
    sif.ms = sif.m7_30

    mx = np.zeros_like(sif.diff1)
    mx[sif.i_cof15] = strend2(nma(sif.close15,13)-nma(sif.close15,60))
    sif.m13_60 = extend2next(mx)
    sif.mm = sif.m13_60

    mx = np.zeros_like(sif.diff1)
    mx[sif.i_cof15] = strend2(nma(sif.close15,30)-nma(sif.close15,120))
    sif.m30_120 = extend2next(mx)
    sif.ml = sif.m30_120

    sif.ntrend = greater(sif.ltrend) + greater(sif.mtrend) + greater(sif.rl_trend) 
    #sif.xtrend = np.select([sif.ntrend>1],[TREND_UP],TREND_DOWN)
    #sif.xtrend = np.select([sif.t30>0,sif.t30<0],[1,-1],0)
    #sif.xtrend = np.select([strend2(ma(sif.close,780))>0],[1],-1)   #3日减第一日开盘
    #m15 = dnext(strend2(ma(sif.close15,54)),sif.close,sif.i_cof15)
    #m10 = dnext(strend2(ma(sif.close10,81)),sif.close,sif.i_cof10)  #3日为趋势判断周期
    #m10 = dnext(strend2(ma(sif.close10,40)),sif.close,sif.i_cof10)  #3日为趋势判断周期
    #m5 = dnext(strend2(ma(sif.close5,80)),sif.close,sif.i_cof5)
    #m5 = dnext(strend2(ma(sif.close5,30)),sif.close,sif.i_cof5)
    m5 = dnext(strend2(ma(sif.close5,120)),sif.close,sif.i_cof5)    #两天+1小时作为长期趋势
    #sif.xtrend = np.select([m5>0],[1],-1)
    sif.xtrend = m5
    sif.sxtrend = np.select([sif.xtrend>0,sif.xtrend<0],[1,-1],0)
    
    sif.macd3x = sif.diff3x-sif.dea3x   
    sif.macd5x = sif.diff5x-sif.dea5x
    sif.macd10x = sif.diff10x-sif.dea10x
    sif.macd15x = sif.diff15x-sif.dea15x
    sif.macd30x = sif.diff30x-sif.dea30x   
    sif.macd60x = sif.diff60x-sif.dea60x    
    sif.macd45x = sif.diff45x-sif.dea45x
    sif.macd90x = sif.diff90x-sif.dea90x    

    sif.rsi7 = rsi2(sif.close,7)
    sif.rsi19 = rsi2(sif.close,19)

    #xup/xdown
    sup,sdown = xupdownc(sif.open,sif.close,sif.high,sif.low)
    sup = sup * XBASE * XBASE * XBASE / sif.close
    sdown = sdown * XBASE * XBASE * XBASE / sif.close
    sif.xup = cexpma(sup,20)
    sif.xdown = cexpma(sdown,20)
    sif.mxup = ma(sif.xup,13)
    sif.mxdown = ma(sif.xdown,13)

    sup,sdown = xupdownc(sif.open30,sif.close30,sif.high30,sif.low30)
    sup = sup * XBASE * XBASE * XBASE / sif.close30
    sdown = sdown * XBASE * XBASE * XBASE / sif.close30
    sif.xup30 = cexpma(sup,20)
    sif.xdown30 = cexpma(sdown,20)
    sif.mxup30 = ma(sif.xup30,13)
    sif.mxdown30 = ma(sif.xdown30,13)
    sif.xup30x = dnext(sif.xup30,sif.close,sif.i_cof30)
    sif.xdown30x = dnext(sif.xdown30,sif.close,sif.i_cof30)
    sif.mxup30x = dnext(sif.mxup30,sif.close,sif.i_cof30)
    sif.mxdown30x = dnext(sif.mxdown30,sif.close,sif.i_cof30)

    #autr/adtr
    vautr = autr(sif.open,sif.close,sif.high,sif.low) * XBASE * XBASE * XBASE / sif.close
    vadtr = adtr(sif.open,sif.close,sif.high,sif.low) * XBASE * XBASE * XBASE / sif.close
    sif.xautr = cexpma(vautr,20)
    sif.xadtr = cexpma(vadtr,20)
    sif.mxautr = ma(sif.xautr,13)
    sif.mxadtr = ma(sif.xadtr,13)

    vautr = autr(sif.open30,sif.close30,sif.high30,sif.low30) * XBASE * XBASE * XBASE / sif.close30
    vadtr = adtr(sif.open30,sif.close30,sif.high30,sif.low30) * XBASE * XBASE * XBASE / sif.close30
    sif.xautr30 = cexpma(vautr,20)
    sif.xadtr30 = cexpma(vadtr,20)
    sif.mxautr30 = ma(sif.xautr30,13)
    sif.mxadtr30 = ma(sif.xadtr30,13)
    sif.xautr30x = dnext(sif.xautr30,sif.close,sif.i_cof30)
    sif.xadtr30x = dnext(sif.xadtr30,sif.close,sif.i_cof30)
    sif.mxautr30x = dnext(sif.mxautr30,sif.close,sif.i_cof30)
    sif.mxadtr30x = dnext(sif.mxadtr30,sif.close,sif.i_cof30)

    ddi = np.select([sif.time==915],[1],0)
    sif.iday = ddi
    sif.dma = dsma(sif.close,ddi)
    sif.sdma = strend2(sif.dma)
    sif.dema = cexpma_s(sif.close,ddi,26)   #没啥用处，变化太快
    sif.sdema = strend2(sif.dema)
    


    #sif.xstate = np.select([gand(sif.xtrend>0,sif.sdma>3),gand(sif.xtrend<0,sif.sdma<-3)],[1,-1],default=0)
    #对下降更有容忍度
    sif.xstate = np.select([gand(sif.xtrend>5,sif.sdma>15),gand(sif.xtrend<10,sif.sdma<-7)],[1,-1],default=0)
    #sif.xstate = np.select([gand(sif.xtrend>0,sif.sdma>0),gand(sif.xtrend<0,sif.sdma<0)],[1,-1],default=0)
    #在xstate=0的时期，效果比较差


def calc_high_low_vol(trans,i_oof,i_cof):
    xhigh = np.zeros_like(i_oof)
    xlow = np.zeros_like(i_oof)
    xvol = np.zeros_like(i_oof)    
    i = 0
    for x,y in zip(i_oof,i_cof):
        xhigh[i] = np.max(trans[IHIGH][x:y+1])
        xlow[i] = np.min(trans[ILOW][x:y+1])
        xvol[i] = np.sum(trans[IVOL][x:y+1])
        i += 1
    return xhigh,xlow,xvol



