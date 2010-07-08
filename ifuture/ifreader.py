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
        narrays[IVOL][i] = record.vol
        narrays[IHOLDING][i] = record.holding
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
    record.vol = int(float(items[6]) + 0.1)
    record.holding = int(float(items[7]) + 0.1)

    return record

FPATH = 'D:/work/applications/gcode/wolfox/data/ifuture/'
prefix = 'SF'
IFS = 'IF1005','IF1006','IF1007','IF1009','IF1012' #,'RU1011','FU1009','CU1009'
SUFFIX = '.txt'

def read1(name):
    ifs = {}
    ifs[name] = BaseObject(name=name,transaction=read_if_as_np(FPATH + prefix + name + SUFFIX))
    prepare_index(ifs[name])
    return ifs

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
    sif.diff2,sif.dea2 = cmacd(trans[ICLOSE]*FBASE,19,39,15)    
    sif.diff5,sif.dea5 = cmacd(trans[ICLOSE]*FBASE,60,130,45)
    sif.diff15,sif.dea15 = cmacd(trans[ICLOSE]*FBASE,180,390,135)
    sif.diff30,sif.dea30 = cmacd(trans[ICLOSE]*FBASE,360,780,270)
    sif.diff60,sif.dea60 = cmacd(trans[ICLOSE]*FBASE,720,1560,540)
    sif.di30,sif.de30 = smacd(trans[ICLOSE]*FBASE,360,780,270)  #计算误差太大，改用非指数版
    sif.di60,sif.de60 = smacd(trans[ICLOSE]*FBASE,720,1560,540)  #计算误差太大，改用非指数版

    sif.macd1 = sif.diff1-sif.dea1
    sif.macd5 = sif.diff5-sif.dea5
    sif.macd15 = sif.diff15-sif.dea15
    sif.macd30 = sif.diff30-sif.dea30    
    sif.macd60 = sif.diff60-sif.dea60    

    sif.ma3 = ma(trans[ICLOSE],3)
    sif.ma5 = ma(trans[ICLOSE],5)
    sif.ma10 = ma(trans[ICLOSE],10)
    sif.ma7 = ma(trans[ICLOSE],7)
    sif.ma13 = ma(trans[ICLOSE],13)    
    sif.ma20 = ma(trans[ICLOSE],20)
    sif.ma30 = ma(trans[ICLOSE],30)
    sif.ma60 = ma(trans[ICLOSE],60)
    sif.ma135 = ma(trans[ICLOSE],135)    
    sif.ma270 = ma(trans[ICLOSE],270)        
    sif.atr = atr(trans[ICLOSE]*XBASE,trans[IHIGH]*XBASE,trans[ILOW]*XBASE,20)
    sif.atr2 = atr2(trans[ICLOSE]*XBASE,trans[IHIGH]*XBASE,trans[ILOW]*XBASE,20)    
    sif.xatr = sif.atr * XBASE * XBASE / trans[ICLOSE]
    sif.mxatr = ma(sif.xatr,13)
    sif.i_cof5 = np.where(
            gor(gand(trans[ITIME]%5==0,trans[ITIME]%1000 != 915)
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


    sif.i_cof30 = np.where(gor(
        gand(trans[ITIME]%10000==1514,rollx(trans[ITIME],-1)%10000!=1515)   #当不存在1515时，1514
        ,trans[ITIME]%10000==1515
        ,trans[ITIME]%10000==1415
        ,trans[ITIME]%10000==1315
        ,trans[ITIME]%10000==1115
        ,trans[ITIME]%10000==1015
        #,trans[ITIME]%10000==915
        ,trans[ITIME]%100==45))[0]    #30分钟收盘线,不考虑隔日的因素
    sif.i_oof30 = roll0(sif.i_cof30)+1    
    sif.i_oof30[0] = 0    
    sif.close30 = trans[ICLOSE][sif.i_cof30]
    #sif.open30 = rollx(sif.close30)   #open5看作是上一个的收盘价,其它方式对应open和close以及还原的逻辑比较复杂
    sif.open30 = trans[IOPEN][sif.i_oof30]
    #sif.high30 = tmax(trans[IHIGH],30)[sif.i_cof30]
    #sif.low30 = tmin(trans[ILOW],30)[sif.i_cof30]
    sif.high30,sif.low30,sif.vol30 = calc_high_low_vol(trans,sif.i_oof30,sif.i_cof30)
    sif.holding30 = trans[IHOLDING][sif.i_cof30]


    sif.atr30 = atr(sif.close30*XBASE,sif.high30*XBASE,sif.low30*XBASE,20)
    sif.xatr30 = sif.atr30 * XBASE * XBASE / sif.close30
    sif.mxatr30 = ma(sif.xatr30,13)
    sif.diff30x,sif.dea30x = cmacd(sif.close30*FBASE)

    sif.sdiff30x,sif.sdea30x = np.zeros_like(trans[ICLOSE]),np.zeros_like(trans[ICLOSE])
    sif.sdiff30x[sif.i_cof30] = sif.diff30x
    sif.sdea30x[sif.i_cof30] = sif.dea30x
    sif.sdiff30x=extend2next(sif.sdiff30x)
    sif.sdea30x=extend2next(sif.sdea30x)


    sif.i_cof15 = np.where(
            gand(
                gor(trans[ITIME]%100==15
                    ,trans[ITIME]%100==30
                    ,trans[ITIME]%100==45
                    ,trans[ITIME]%100==0
                    ,gand(trans[ITIME]%10000 == 1514,rollx(trans[ITIME],-1)%10000!=1515)   #当不存在1515时，取1514
                    )
                ,trans[ITIME]%1000!=915
            )
        )[0]    #5分钟收盘线,不考虑隔日的因素
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
    sif.diff15x,sif.dea15x = cmacd(sif.close15*FBASE)
    sif.diff15x5,sif.dea15x5 = cmacd(sif.close15*FBASE,60,130,45)    

    sif.sdiff15x,sif.sdea15x = np.zeros_like(trans[ICLOSE]),np.zeros_like(trans[ICLOSE])
    sif.sdiff15x[sif.i_cof15] = sif.diff15x
    sif.sdea15x[sif.i_cof15] = sif.dea15x
    sif.sdiff15x=extend2next(sif.sdiff15x)
    sif.sdea15x=extend2next(sif.sdea15x)

    sif.i_cofd = np.append(np.nonzero(trans[IDATE]-rollx(trans[IDATE])>0)[0]-1,len(trans[IDATE])-1)
    sif.i_oofd = roll0(sif.i_cofd)+1
    sif.i_oofd[0]=0
    sif.opend = trans[IOPEN][sif.i_oofd]
    sif.closed = trans[ICLOSE][sif.i_cofd]
    sif.highd,sif.lowd,sif.vold = calc_high_low_vol(trans,sif.i_oofd,sif.i_cofd)
    sif.holdingd = trans[IHOLDING][sif.i_cofd]


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
    sif.atr = atr(trans[IMID]*XBASE,trans[IHIGH]*XBASE,trans[ILOW]*XBASE,20)
    sif.atr2 = atr2(trans[IMID]*XBASE,trans[IHIGH]*XBASE,trans[ILOW]*XBASE,20)    
    sif.xatr = sif.atr * XBASE * XBASE / trans[IMID]
    sif.mxatr = ma(sif.xatr,13)

