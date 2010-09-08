# -*- coding: utf-8 -*-
'''
使用当月连续
    当某日收盘下月合约的持仓大于本月的90%时，切换
筛选条件:
    xatr
    如果是突破，则5分钟内稳定

    strend2(sif.ma13)
    strend2(sif.ma30)    
    sif.ma3 >/< sif.ma13

优先级：
    普通 1500
    逆势 >==2000
    突破 <=1200
        突破的附属 <2000

'''


from wolfox.fengine.ifuture.ibase import *
from wolfox.fengine.ifuture.iftrade import delay_filter,atr5_uxstop_1_25,atr5_uxstop_08_25,atr5_uxstop_05_25


###顺势
def rsi_short_x(sif,sopened=None,rshort=7,rlong=19):
    '''
        每天的第一次符合条件的机会为最佳机会
        一旦第一次失败，后面的都被屏蔽
        比较妥当的是 7/19和13/41参数,其中前者明显优于后者
        但是合并有副作用
    '''

    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    signal = cross(rsib,rsia)<0    

    signal = gand(signal
            ,sif.s30<0
            ,sif.rs_trend<0
            ,sif.ms<0
            ,strend2(sif.ma30)<0
            ,sif.xatr30x<6000
            ,sif.mtrend<0
            )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal==1)

    return signal * rsi_short_x.direction
rsi_short_x.direction = XSELL
rsi_short_x.priority = 1500

def rsi_short_x2(sif,sopened=None,rshort=7,rlong=19):
    '''
        每天的第一次符合条件的机会为最佳机会
        一旦第一次失败，后面的都被屏蔽
        去掉s30<0的限制
        以sdiff30x<0为条件
        且s30>0 #s30<0的由rsi_short_x去捕捉
    '''

    rsia = rsi2(sif.close,rshort)   
    rsib = rsi2(sif.close,rlong)
    signal = cross(rsib,rsia)<0    

    signal = gand(signal
            ,sif.strend<0
            ,sif.sdiff30x<0
            ,sif.s30>0  #s30<0的由rsi_short_x去捕捉
            ,strend2(sif.ma30)<0
            ,sif.xatr30x<6000
            ,sif.ma5<sif.ma13
            )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal==1)

    return signal * rsi_short_x.direction
rsi_short_x2.direction = XSELL
rsi_short_x2.priority = 1500


def macd_short_x(sif,sopened=None):
    '''
        操作策略，失败一次之后当日就不应该再操作
        成功的话，可以继续操作，参见macd_short_x2
    '''
    signal = cross(sif.dea1,sif.diff1)<0    

    signal = gand(signal
            ,sif.ltrend<0            
            ,sif.mtrend < 0
            ,strend2(sif.ma30)<0
            ,sif.ma5 < sif.ma13
            ,sif.xatr>800
            ,sif.sdiff30x<0
            )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal == 1)

    return signal * macd_short_x.direction
macd_short_x.direction = XSELL
macd_short_x.priority = 1500

def macd_short_x2(sif,sopened=None):
    '''
        试图找到在盈利退出后的继续开仓
        没找到好办法. 
        用状态和时间来模拟
            1. 因为前次盈利，所以是绝对空头
            2. 因为前次退出，所以出现一小波的反弹. 但不影响中期左右趋势
            3. 时间在1345之后
        操作策略，失败一次之后当日就不应该再操作
    '''
    signal = cross(sif.dea1,sif.diff1)<0    

    signal = gand(signal
            ,sif.ltrend<0            
            ,sif.mtrend < 0
            ,strend2(sif.ma30)<0
            ,sif.ma5 < sif.ma13
            ,sif.xatr>800
            ,sif.sdiff30x<0
            ,sif.mm<0   #处于绝对空头状态
            ,sif.ms<0
            )

    signal = np.select([sif.time>1345],[signal],0)    
    #signal = sum2diff(extend2diff(signal,sif.date),sif.date)

    signal = gand(signal == 1)

    return signal * macd_short_x2.direction
macd_short_x2.direction = XSELL
macd_short_x2.priority = 1600   #优先级低于本级



#####多头
def rsi_long_x(sif,sopened=None,rshort=7,rlong=19):
    '''
        比较妥当的是 7/19和13/41参数,其中前者明显优于后者
    '''

    #signal = cross(sif.dea1,sif.diff1)>0
    rshort = 7
    rlong = 19
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    signal = cross(rsib,rsia)>0    

    signal = gand(signal
                ,sif.ltrend>0
                ,sif.mtrend>0                
                ,sif.t7_30>0
                ,sif.s30>0
                ,sif.s10>0                
                ,sif.s3>0
            )

    return signal * rsi_long_x.direction
rsi_long_x.direction = XBUY
rsi_long_x.priority = 1500


def rsi_long_x2(sif,sopened=None,rshort=7,rlong=19):
    '''
        去掉s30限制
        比较妥当的是 7/19和13/41参数,其中前者明显优于后者
    '''

    #signal = cross(sif.dea1,sif.diff1)>0
    rshort = 7
    rlong = 19
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    signal = cross(rsib,rsia)>0    

    signal = gand(signal
                ,sif.s3>0
                ,sif.s15>0
                ,sif.ma3>sif.ma13
                ,sif.xatr30x<6000
                ,sif.ms>0
            )
    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal==1)

    return signal * rsi_long_x2.direction
rsi_long_x2.direction = XBUY
rsi_long_x2.priority = 1500

def macd_long_x(sif,sopened=None):
    '''
        居然添加任何ltrend/mtrend/strend条件都会使结果变坏
        经观察，这是个逆势的方法，所以不能加趋势
    '''
    signal = cross(sif.dea1,sif.diff1)>0    

    signal = gand(signal
                    ,sif.s30>0
                    ,sif.s10>0
                    ,sif.s3>0
                    ,sif.xatr<1200
                    ,strend2(sif.ma13)>0                                    
            )

    return signal * macd_long_x.direction
macd_long_x.direction = XBUY
macd_long_x.priority = 1900

def macd_long_x2(sif,sopened=None):
    '''
        去掉s30>0条件
    '''
    signal = cross(sif.dea1,sif.diff1)>0    

    signal = gand(signal
                    ,sif.ltrend>0
                    ,sif.mtrend>0
                    ,sif.strend>0
                    ,sif.mm>0
                    ,sif.ms>0
                    ,sif.s10>0
                    ,sif.xatr<1200
            )

    return signal * macd_long_x2.direction
macd_long_x2.direction = XBUY
macd_long_x2.priority = 1500

def macd_long_x3(sif,sopened=None):
    '''
        去掉s30>0条件
    '''
    signal = cross(sif.dea1,sif.diff1)>0    

    rshort = 7
    rlong = 19
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    #signal = cross(rsib,rsia)>0    

    signal = gand(signal
                    ,sif.s30>0
                    ,sif.diff1<0
                    ,sif.ltrend>0
                    ,sif.xatr<1200
                    ,sif.s15>0
                    ,sif.ma3>sif.ma13
            )

    return signal * macd_long_x3.direction
macd_long_x3.direction = XBUY
macd_long_x3.priority = 1500


def up0(sif,sopened=None):
    '''
        上穿0线
        是逆势的
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤

    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1)>0
            ,sif.s30>0
            ,sif.s3>0
            ,sif.sdiff5x<0
            ,strend2(sif.ma30)>0
            ,strend2(sif.diff1)>3
            ,dsfilter
            )

    return signal * up0.direction
up0.direction = XBUY
up0.priority = 1800  #叠加时，远期互有盈亏

def down01(sif,sopened=None): #++
    ''' 
        30分钟<0且下行
        5分钟>0且下行
    '''

    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1)<0
            ,sif.sdiff5x>0
            ,sif.sdiff30x<0
            ,strend(sif.diff1-sif.dea1)<-2            
            ,strend(sif.ma5-sif.ma30)<0
            ,strend(sif.ma135-sif.ma270)<0            
            ,strend(sif.ma30)<0
            ,sif.ltrend<0
            )
    return signal * down01.direction
down01.direction = XSELL
down01.priority = 1600

def xdown60(sif,sopened=None):
    '''
        连续5分钟内出现60分钟最低点4个以上
    '''
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)

    covered = 60

    snewlow = sif.low < rollx(tmin(sif.low,covered))

    msnl = msum2(snewlow,5)

    signal = gand(msnl>3)

    signal = gand(signal
            ,sif.ma5 < sif.ma13
            ,strend2(sif.diff1-sif.dea1)<0
            ,strend2(sif.ma270)<0
            ,strend2(sif.sdiff5x-sif.sdea5x)<0
            ,strend2(sif.sdiff15x-sif.sdea15x)<0
            ,sif.mtrend<0            
            ,sif.ltrend<0
            ,ksfilter
            ,sif.xatr>1000
            )
    
    return signal * xdown60.direction
xdown60.direction = XSELL
xdown60.priority = 1600 



def ipmacd_short5(sif,sopened=None):
    '''
        最古老的方法
    '''
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)
    
    signal = gand(cross(sif.dea5,sif.diff5)<0
            ,sif.diff5>0
            ,sif.diff30<0
            ,strend(sif.diff30-sif.dea30)<0
            )
    signal = gand(signal
            ,strend(sif.ma13-sif.ma60)<0
            ,strend(sif.ma135-sif.ma270)<0
            ,ksfilter
            )   
    return signal * ipmacd_short5.direction
ipmacd_short5.direction = XSELL
ipmacd_short5.priority = 1800


def ma60_short(sif,sopened=None):
    ''' ma60拐头
    '''
    trans = sif.transaction
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr < 2000)
 
    msignal = gand(strend(sif.ma60) == -1
                )
    fsignal = gand(cross(sif.dea1,sif.diff1)<0
                ,strend2(sif.sdiff5x-sif.sdea5x)>0
                ,ksfilter                
                ,sif.xatr3x>sif.mxatr3x
                )
    signal = sfollow(msignal,fsignal,5)
    return signal * ma60_short.direction
ma60_short.direction = XSELL
ma60_short.priority = 2401

def xud30b(sif,sopened=None):
    '''
        顺势
    '''

    mxc = xc0c(sif.open30,sif.close30,sif.high30,sif.low30,13) > 0
    signal30 = gand(mxc
                ,sif.xatr30<sif.mxatr30
                ,sif.xatr30<8000    #这个条件可以放宽?
                )

    signal = np.zeros_like(sif.diff1)
    signal[sif.i_cof30] = signal30

    signal = gand(signal
            ,sif.s15>0
            )

    return signal * xud30b.direction
xud30b.direction = XBUY
xud30b.priority = 1200


ama1 = ama_maker()
ama2 = ama_maker(covered=30,dfast=6,dslow=100)

def ama_short(sif,sopened=None): #+
    trans = sif.transaction
    xama1 = ama1(trans[ICLOSE])
    xama2 = ama2(trans[ICLOSE])
    signal = gand(cross(xama2,xama1)<0
            #,sif.s10<0
            ,sif.xatr<1200
            ,sif.mtrend<0
            ,sif.xatr<sif.mxatr
            )
    return signal * XSELL
ama_short.direction = XSELL
ama_short.priority = 1600



###acd系列,属于突破算法
##辅助函数
def range_a(sif,tbegin,tend,wave):
    high10 = np.select([gand(sif.time>=tbegin,sif.time<=tend)],[sif.high],default=0)
    low10 = np.select([gand(sif.time>=tbegin,sif.time<=tend)],[sif.low],default=0)    

    xhigh10 = np.select([sif.time==924],[tmax(high10,11)],0)
    xlow10 = np.select([sif.time==924],[tmin(low10,11)],0)    

    UA = np.select([sif.time==tend],[xhigh10+wave],0)        
    DA = np.select([sif.time==tend],[xlow10-wave],0)    

    xhigh10 = extend2next(xhigh10)
    xlow10  = extend2next(xlow10)
    UA = extend2next(UA)
    DA = extend2next(DA)
    return UA,DA,xhigh10,xlow10

def acd_ua(sif,sopened=None):
    '''
        发现前两天不能有信号(不论前次信号胜负)，否则必败
    '''
    wave = np.zeros_like(sif.close)
    wave[sif.i_cof10] = rollx(sif.atr10) *2/3/XBASE  #掠过914-919的atr10
    wave = extend2next(wave)
    
    UA,DA,xhigh10,xlow10 = range_a(sif,914,924,wave)

    xcontinue = 5

    signal_ua = gand(sif.close >= UA
                    ,msum2(sif.close>=UA,xcontinue)>4
                    ,rollx(sif.close,xcontinue)>=UA
                    )

    signal_ua = np.select([sif.time>944],[signal_ua],0) #924之前的数据因为xhigh10是extend2next来的，所以不准

    signal_da = gand(sif.close <= DA
                    ,msum2(sif.close<DA,xcontinue)>=4
                    ,rollx(sif.close,xcontinue)<=DA
                    )

    signal_da = np.select([sif.time>944],[signal_da],0)

    ms_ua = sum2diff(extend2diff(signal_ua,sif.date),sif.date)
    ms_da = sum2diff(extend2diff(signal_da,sif.date),sif.date)

    signal = gand(ms_ua==1         #第一个ua
                ,bnot(ms_da)       #没出现过da 
                ,sif.s30>0
                ,sif.xatr30x<sif.mxatr30x
                #,sif.xatr<1800
                )

    return signal * acd_ua.direction
acd_ua.direction = XBUY
acd_ua.priority = 1200

def acd_da(sif,sopened=None):
    '''
        +
    '''
    wave = np.zeros_like(sif.close)
    wave[sif.i_cof10] = rollx(sif.atr10) *2/3/XBASE  #掠过914-919的atr10
    wave = extend2next(wave)
    
    UA,DA,xhigh10,xlow10 = range_a(sif,914,924,wave)

    xcontinue = 5

    signal_ua = gand(sif.close >= UA
                    ,msum2(sif.close>=UA,xcontinue)>4
                    ,rollx(sif.close,xcontinue)>=UA
                    )

    signal_ua = np.select([sif.time>944],[signal_ua],0) #924之前的数据因为xhigh10是extend2next来的，所以不准

    signal_da = gand(sif.close <= DA
                    ,msum2(sif.close<=DA,xcontinue)>4
                    ,rollx(sif.close,xcontinue)<=DA
                    )

    signal_da = np.select([sif.time>944],[signal_da],0)

    ms_ua = sum2diff(extend2diff(signal_ua,sif.date),sif.date)
    ms_da = sum2diff(extend2diff(signal_da,sif.date),sif.date)

    signal = gand(ms_da==1         #第一个da
                ,bnot(ms_ua)       #没出现过ua 
                ,sif.s30<0
                ,strend2(sif.ma13)<0
                ,sif.xatr<1000
                )

    return signal * acd_da.direction
acd_da.direction = XSELL
acd_da.priority = 1200

def acd_ua_sz(sif,sopened=None):
    '''
        A点大于枢轴
        +   add
    '''

    
    wave = np.zeros_like(sif.close)
    wave[sif.i_cof10] = rollx(sif.atr10) *2/3/XBASE  #掠过914-919的atr10
    wave = extend2next(wave)
    
    UA,DA,xhigh10,xlow10 = range_a(sif,914,924,wave)

    xcontinue = 5

    signal_ua = gand(sif.close >= UA
                    ,msum2(sif.close>=UA,xcontinue)>4
                    ,rollx(sif.close,xcontinue)>=UA
                    )

    signal_ua = np.select([sif.time>944],[signal_ua],0) #924之前的数据因为xhigh10是extend2next来的，所以不准

    signal_da = gand(sif.close <= DA
                    ,msum2(sif.close<=DA,xcontinue)>4
                    ,rollx(sif.close,xcontinue)<=DA
                    )

    signal_da = np.select([sif.time>944],[signal_da],0)


    sz0 = (sif.closed+sif.highd+sif.lowd)/3
    sz2 = (sif.highd+sif.lowd)/2
    sf = np.abs(sz0-sz2)
    
    szh = np.zeros_like(sif.close)
    szh[sif.i_cofd] = sz0 + sf
    szh = extend2next(szh)

    szl = np.zeros_like(sif.close)
    szl[sif.i_cofd] = sz0 - sf
    szl = extend2next(szl)

    ms_ua = sum2diff(extend2diff(signal_ua,sif.date),sif.date)
    ms_da = sum2diff(extend2diff(signal_da,sif.date),sif.date)

    signal = gand(ms_ua == 1
                    ,bnot(ms_da)
                    ,UA >= szh
                    ,sif.ms>0
                    #,sif.xatr<1800
                    ,sif.xatr30x<sif.mxatr30x
                    )


    return signal * acd_ua_sz.direction
acd_ua_sz.direction = XBUY
acd_ua_sz.priority = 1900

def acd_ua_sz_b(sif,sopened=None):
    '''
        枢轴上限大于价幅上限，但是小于A点
        +
    '''

    wave = np.zeros_like(sif.close)
    wave[sif.i_cof10] = rollx(sif.atr10) *2/3/XBASE  #掠过914-919的atr10
    wave = extend2next(wave)
    
    UA,DA,xhigh10,xlow10 = range_a(sif,914,924,wave)

    xcontinue = 5

    signal_ua = gand(sif.close >= UA
                    ,msum2(sif.close>=UA,xcontinue)>4
                    ,rollx(sif.close,xcontinue)>=UA
                    )

    signal_ua = np.select([sif.time>944],[signal_ua],0) #924之前的数据因为xhigh10是extend2next来的，所以不准

    signal_da = gand(sif.close <= DA
                    ,msum2(sif.close<=DA,xcontinue)>4
                    ,rollx(sif.close,xcontinue)<=DA
                    )

    signal_da = np.select([sif.time>944],[signal_da],0)


    sz0 = (sif.closed+sif.highd+sif.lowd)/3
    sz2 = (sif.highd+sif.lowd)/2
    sf = np.abs(sz0-sz2)
    
    szh = np.zeros_like(sif.close)
    szh[sif.i_cofd] = sz0 + sf
    szh = extend2next(szh)

    szl = np.zeros_like(sif.close)
    szl[sif.i_cofd] = sz0 - sf
    szl = extend2next(szl)


    ms_ua = sum2diff(extend2diff(signal_ua,sif.date),sif.date)
    ms_da = sum2diff(extend2diff(signal_da,sif.date),sif.date)

    signal = gand(ms_ua == 1
                    ,bnot(ms_da)
                    ,szh>=xhigh10 #szl>=xhigh10
                    ,UA >= szh
                    ,sif.s15>0
                    ,sif.xatr<1800                    
                    )

    return signal * acd_ua_sz_b.direction
acd_ua_sz_b.direction = XBUY
acd_ua_sz_b.priority = 1900

def acd_da_sz_b(sif,sopened=None):
    '''
        枢轴下限小于A点
        过枢轴        
        +   add
    '''

    wave = np.zeros_like(sif.close)
    wave[sif.i_cof10] = rollx(sif.atr10) *2/3/XBASE  #掠过914-919的atr10
    wave = extend2next(wave)
    
    UA,DA,xhigh10,xlow10 = range_a(sif,914,924,wave)

    sz0 = (sif.closed+sif.highd+sif.lowd)/3
    sz2 = (sif.highd+sif.lowd)/2
    sf = np.abs(sz0-sz2)
    
    szh = np.zeros_like(sif.close)
    szh[sif.i_cofd] = sz0 + sf
    szh = extend2next(szh)

    szl = np.zeros_like(sif.close)
    szl[sif.i_cofd] = sz0 - sf
    szl = extend2next(szl)


    xcontinue = 5

    signal_ua = gand(sif.close >= UA
                    ,msum2(sif.close>=UA,xcontinue)>4
                    ,rollx(sif.close,xcontinue)>=UA
                    )

    signal_ua = np.select([sif.time>944],[signal_ua],0) #924之前的数据因为xhigh10是extend2next来的，所以不准

    signal_da = gand(sif.close <= szl
                    ,szl<=DA
                    ,msum2(sif.close<=szl,xcontinue)>4
                    ,rollx(sif.close,xcontinue)<=szl
                    )

    signal_da = np.select([sif.time>944],[signal_da],0)




    ms_ua = sum2diff(extend2diff(signal_ua,sif.date),sif.date)
    ms_da = sum2diff(extend2diff(signal_da,sif.date),sif.date)

    signal = gand(ms_da == 1
                    ,bnot(ms_ua)
                    ,strend2(sif.ma30)<0
                    ,sif.xatr>800
                    )

    return signal * acd_da_sz_b.direction
acd_da_sz_b.direction = XSELL
acd_da_sz_b.priority = 1900

#####突破算法
def br30(sif,sopened=None):
    '''
        5分钟最高突破开盘前30分钟最高之后，下一次1分钟上叉
        属于突破回调的模式
    '''
    
    high30 = np.select([sif.time[sif.i_cof30]==944],[sif.high30],default=0)

    xhigh30,xlow30 = np.zeros_like(sif.diff1),np.zeros_like(sif.diff1)
    xhigh30[sif.i_cof30] = high30   #因为屏蔽了前30分钟，所以i_cof30和i_oof30效果一样

    xhigh30 = extend2next(xhigh30)

    signal = np.zeros_like(sif.diff1)

    signal[sif.i_cof5] = cross(xhigh30[sif.i_cof5],sif.high5)>0

    #signal = sfollow(signal,cross(sif.dea1,sif.diff1)>0,15)
    rshort = 7
    rlong = 19
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    
    signal = sfollow(signal,cross(sif.dea1,sif.diff1)>0,15)    
    #signal = sfollow(signal,cross(rsib,rsia)>0,15)    

    signal = gand(signal
            ,sif.s30>0
            ,sif.mtrend>0
            )

    return signal * br30.direction
br30.direction = XBUY
br30.priority = 1200

def br30_old(sif,sopened=None):
    '''
        5分钟最高突破开盘前30分钟最高之后，下一次1分钟上叉
        属于突破回调的模式
    '''
    trans = sif.transaction
    dsfilter = gand(trans[ICLOSE] - trans[IOPEN] < 100,rollx(trans[ICLOSE]) - trans[IOPEN] < 200,sif.xatr<1500)#: 向上突变过滤
    ksfilter = gand(trans[IOPEN] - trans[ICLOSE] < 60,rollx(trans[IOPEN]) - trans[ICLOSE] < 120,sif.xatr<2000)
    
    high30 = np.select([trans[ITIME][sif.i_cof30]==944],[sif.high30],default=0)

    xhigh30,xlow30 = np.zeros_like(sif.diff1),np.zeros_like(sif.diff1)
    xhigh30[sif.i_cof30] = high30   #因为屏蔽了前30分钟，所以i_cof30和i_oof30效果一样

    xhigh30 = extend2next(xhigh30)

    signal = np.zeros_like(sif.diff1)

    signal[sif.i_cof5] = cross(xhigh30[sif.i_cof5],sif.high5)>0

    #signal = sfollow(signal,cross(sif.dea1,sif.diff1)>0,15)
    signal = sfollow(signal,cross(sif.dea1,sif.diff1)>0,15)    #20虽然更好，叠加不佳

    signal = gand(signal
            ,strend(sif.diff30-sif.dea30)>0
            ,strend(sif.diff5-sif.dea5)>0
            ,strend(sif.ma30)>0
            ,sif.ma5>sif.ma13
            ,sif.mtrend>0
            )

    return signal * br30.direction
br30_old.direction = XBUY
br30_old.priority = 1200


def godown(sif,sopened=None):
    '''
        1分钟收盘稳定击穿昨日低点后
    '''
    
 
    lowd = sif.lowd - sif.atrd/XBASE/8 

    xlowd = np.zeros(len(sif.diff1),np.int32)
    xlowd[sif.i_cofd] = lowd 

    xlowd = extend2diff(rollx(xlowd),sif.date)

    signal = gand(sif.close < xlowd
                ,msum(sif.close<xlowd,3)>1
                )

    
    signal = sum2diff(extend2diff(signal,sif.date),sif.date)    #略过了直接跳高的
    #signal = np.select([sif.time>944],[extend2diff(signal,sif.date)],0)
    #signal = sum2diff(signal,sif.date)

    signal = gand(signal==1
            #,sif.s30<0
            #,strend2(sif.ma30)<0
            #,sif.ma3<sif.ma13
            #,strend2(sif.sdiff3x-sif.sdea3x)<0
            ,sif.xatr30x<6000
            )


    return signal * godown.direction
godown.direction = XSELL
godown.priority = 1200

###逆势算法
##沿日线上行或下降
def xma_long(sif,sopened=None,length=5):
    '''
    '''

    md = ma(sif.closed,length)
    smd = strend2(md)

    xmd = np.zeros_like(sif.close)
    xmd[sif.i_cofd] = md
    xmd = extend2next(xmd)

    xsmd = np.zeros_like(sif.close)
    xsmd[sif.i_cofd] = smd
    xsmd = extend2next(xsmd)

    signal = gand(cross(xmd+sif.atr/XBASE,sif.close)>0
                ,xsmd>0
                #,sif.s5>0
                ,sif.ma3>sif.ma13
                #,strend2(sif.ma30)>0
                )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)


    signal = gand(signal==1
            )
    
    return signal * xma_long.direction
xma_long.direction = XBUY
xma_long.priority = 2100


def xma_short(sif,sopened=None,length=20):
    '''
        下行途中上传阻力线后下破该线
        单独效果不好，合成效果很好
    '''
    md = ma(sif.closed,length)
    smd = strend2(md)

    xmd = np.zeros_like(sif.close)
    xmd[sif.i_cofd] = md
    xmd = extend2next(xmd)

    xsmd = np.zeros_like(sif.close)
    xsmd[sif.i_cofd] = smd
    xsmd = extend2next(xsmd)


    signal = gand(cross(xmd-sif.atr/XBASE,sif.close)<0
                ,xsmd<0
                )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)

    signal = gand(signal==1
            ,sif.mtrend<0
            ,sif.ml<0
            )
    
    return signal * xma_short.direction
xma_short.direction = XSELL
xma_short.priority = 2400

def xdma_long(sif,sopened=None,length=20):
    '''
        动态均线，如dma5是前四日收盘价之和加上当前分钟收盘价，然后除以5，即为当时的dma5            
        合并效果一般
    '''
    mbase = ma(sif.closed,length)
    
    mds = msum(sif.closed,length-1)

    xmds = np.zeros_like(sif.close)
    xmds[sif.i_cofd] = mds
    xmds = extend2next(xmds)

    xbase = np.zeros_like(sif.close)
    xbase[sif.i_cofd] = mbase
    xbase = extend2next(xbase)

    dma = (xmds + sif.close)/length

    signal = gand(cross(dma+sif.atr/XBASE,sif.close)>0
                ,dma>xbase
                )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)

    signal = gand(signal==1
            )
    
    return signal * xdma_long.direction
xdma_long.direction = XBUY
xdma_long.priority = 2400

def xdma_short(sif,sopened=None,length=5):
    '''
        动态均线，如dma5是前四日收盘价之和加上当前分钟收盘价，然后除以5，即为当时的dma5
    '''
    mbase = ma(sif.closed,length)
    
    mds = msum(sif.closed,length-1)

    xmds = np.zeros_like(sif.close)
    xmds[sif.i_cofd] = mds
    xmds = extend2next(xmds)

    xbase = np.zeros_like(sif.close)
    xbase[sif.i_cofd] = mbase
    xbase = extend2next(xbase)

    dma = (xmds + sif.close)/length

    signal = gand(cross(dma+sif.atr/XBASE,sif.close)<0
                ,dma<xbase
                )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)

    signal = gand(signal==1
            ,sif.xatr<1500
            )
    
    return signal * xdma_short.direction
xdma_short.direction = XSELL
xdma_short.priority = 2400

def ma1x(sif,opened=None,length=60):
    ''' 
        1分钟均线
        第一次碰线
    '''
    bma = ma(sif.close,length)
    
    signal = cross(bma,sif.low)>0

    signal = gand(signal
                ,strend2(bma)>0
                ,sif.ltrend>0
                ,sif.mtrend>0
                ,sif.s30>0
            )
    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal==1)
    
    signal = derepeatc(signal)

    return signal * ma1x.direction
ma1x.direction = XBUY
ma1x.priority = 2100


def k15_lastdown(sif,sopened=None):
    '''
        新高衰竭模式
        1. 15分钟新高后,15分钟内1分钟跌破前15分钟的开盘价(收盘价的低者)/最低价
    '''
    
    trans = sif.transaction

    ma15_500 = ma(sif.close15,500)
    ma15_200 = ma(sif.close15,200)
    ma15_60 = ma(sif.close15,60) 
    ma15_13 = ma(sif.close15,13)     
    ma15_30 = ma(sif.close15,30) 
    ma15_7 = ma(sif.close15,7)         
    ma15_3 = ma(sif.close15,3)         
    
    signal15 = gand(sif.high15>rollx(sif.high15)
                ,sif.low15>rollx(sif.low15)
                ,sif.high15 - gmax(sif.open15,sif.close15) > np.abs(sif.open15-sif.close15) #上影线长于实体
                ,sif.high15 == tmax(sif.high15,6)
                ,sif.high15 > gmax(ma15_3,ma15_30,ma15_60)
                #,rollx(sif.vol15) > sif.vol15
                #,rollx(sif.vol5) > rollx(sif.vol5,2)
                #,rollx(sif.close5)<rollx(sif.open5)
                ,strend2(ma15_60)>0
                ,strend2(sif.diff15x-sif.dea15x)>0
                #,sif.diff15x>sif.dea15x
                #,strend2(ma15_7)>0                                
                #,ma15_7 > ma15_13
                #,strend2(ma15_500)>0
                )

    #print np.nonzero(signal15)
    delay = 15

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof15] = signal15
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof15] = gmin(sif.open15,sif.close15)
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)
    
    #fsignal = cross(bline,sif.close)<0
    fsignal = (sif.high+sif.low+sif.close)/3 < bline
    #fsignal = cross(bline,(sif.high+sif.low+sif.close)/3)<0
    fsignal  = msum(fsignal,3)>1

    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            ,sif.xatr5x>2000
            )
    signal = extend(signal,delay)  #去除delay时间段内的重复信号
    signal = derepeatc(signal)

    return signal * k15_lastdown.direction
k15_lastdown.direction = XSELL
k15_lastdown.priority = 2100 #对i09时200即优先级最高的效果最好
#k15_lastdown.stop_closer = atr5_uxstop_05_25

def k15_lastdown_s(sif,sopened=None):
    '''
        新高衰竭模式
        1. 15分钟新高后,15分钟内1分钟跌破前15分钟的开盘价(收盘价的低者)/最低价
    '''
    
    trans = sif.transaction

    ma15_500 = ma(sif.close15,500)
    ma15_200 = ma(sif.close15,200)
    ma15_60 = ma(sif.close15,60) 
    ma15_13 = ma(sif.close15,13)     
    ma15_30 = ma(sif.close15,30) 
    ma15_7 = ma(sif.close15,7)         
    ma15_3 = ma(sif.close15,3)         
    
    signal15 = gand(sif.high15>rollx(sif.high15)
                ,sif.low15>rollx(sif.low15)
                ,sif.high15 - gmax(sif.open15,sif.close15) > np.abs(sif.open15-sif.close15) #上影线长于实体
                ,sif.high15 == tmax(sif.high15,5)
                ,sif.high15 > gmax(ma15_3,ma15_30,ma15_60)
                #,rollx(sif.vol5) > sif.vol5
                #,rollx(sif.vol5) > rollx(sif.vol5,2)
                #,rollx(sif.close5)<rollx(sif.open5)
                ,strend2(ma15_60)>0
                ,strend2(sif.diff15x-sif.dea15x)>0
                #,sif.diff15x>sif.dea15x
                #,strend2(ma15_7)>0                                
                #,ma15_7 > ma15_13
                #,strend2(ma15_500)>0
                )

    #print np.nonzero(signal15)
    delay = 15

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof15] = signal15
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof15] = gmin(sif.open15,sif.close15)
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)
    
    #fsignal = cross(bline,sif.high)>0
    fsignal = sif.close < bline


    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            #,sif.xatr5x>1800
            #,sif.s3<0
            ,sif.strend<0
            #,sif.ma3<sif.ma13
            )
    signal = derepeatc(signal)

    return signal * k15_lastdown_s.direction
k15_lastdown_s.direction = XSELL
k15_lastdown_s.priority = 2105

def k5_lastup(sif,sopened=None):
    '''
        底部衰竭模式
        5分钟底部阴线后出现孕线，后10分钟内1分钟最高线突破该孕线(high+close)/2
        长期顺势，中期逆势，短期顺势
    '''
    trans = sif.transaction
 
    ma5_500 = ma(sif.close5,500)
    ma5_200 = ma(sif.close5,200)
    ma5_60 = ma(sif.close5,60) 
    ma5_13 = ma(sif.close5,13)     
    ma5_30 = ma(sif.close5,30) 
    ma5_7 = ma(sif.close5,7)         
    ma5_3 = ma(sif.close5,3)         
    
    signal5 = gand(sif.high5<rollx(sif.high5)
                ,sif.low5>rollx(sif.low5)
                ,rollx(sif.low5) == tmin(sif.low5,20)
                ,rollx(sif.vol5) > sif.vol5
                ,rollx(sif.vol5) > rollx(sif.vol5,2)
                ,rollx(sif.close5)<rollx(sif.open5)
                )

    delay = 10

    ss = np.zeros_like(sif.close)
    ss[sif.i_cof5] = signal5
    ssh = np.zeros_like(sif.close)
    ssh[sif.i_cof5] = (sif.high5 + sif.close5)/2
    bline = np.select([ss>0],[ssh],0)
    bline = extend(bline,delay)
    
    #fsignal = cross(bline,sif.high)>0
    fsignal = sif.high > bline

    #signal = np.zeros_like(sif.close)
    #signal[sif.i_cof5] = signal5

    signal = sfollow(ss,fsignal,delay)
    signal = gand(signal
            ,sif.ltrend>0
            ,sif.mtrend<0            
            ,sif.mm<0
            ,strend2(sif.ma13)>0
            ,sif.ma3>sif.ma13
            ,sif.xatr<1500
            )

    signal = np.select([sif.time>944],[signal],0)

    signal = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal==1)
    
    signal = derepeatc(signal)

    return signal * k5_lastup.direction
k5_lastup.direction = XBUY
k5_lastup.priority = 2100

def xud30s_r(sif,sopened=None):
    '''
        逆势
    '''

    mxc = xc0c(sif.open30,sif.close30,sif.high30,sif.low30,13) < 0
    signal30 = gand(mxc
                ,sif.high30 == tmax(sif.high30,9)
                )

    signal = np.zeros_like(sif.diff1)
    signal[sif.i_cof30] = signal30

    signal = gand(signal
            )

    return signal * xud30s_r.direction
xud30s_r.direction = XSELL
xud30s_r.priority = 2010


##背离
def ipmacd_long_devi1(sif,sopened=None):
    '''
    '''

    msignal = ldevi(sif.low,sif.diff1,sif.dea1)

    signal = gand(msignal
            ,sif.xatr30x<6666
            ,sif.s30<0
            ,sif.s10<0
            ,sif.s3>0
            ,sif.ma3>sif.ma7
            )

    return signal * ipmacd_long_devi1.direction
ipmacd_long_devi1.direction = XBUY
ipmacd_long_devi1.priority = 2100

def ipmacd_short_devi1(sif,sopened=None):
    '''
        顶背离操作，去掉了诸多条件
        尤其是xatr<2000
    '''

    trans = sif.transaction

    th = tmax(trans[IHIGH],120)
    th2 = tmax(trans[IHIGH],10)
    delta = 10 #2点

    signal = gand(hdevi(trans[IHIGH],sif.diff1,sif.dea1,delta=delta)
                ,th2 >= th - delta
                )

    fsignal = strend2(sif.diff1-sif.dea1)<0

    signal = sfollow(signal,fsignal,15)

    signal = gand(signal
                ,strend2(sif.sdiff5x)>0
                ,sif.s5<0
                ,strend2(sif.sdiff30x)<0
            )
    return signal * ipmacd_short_devi1.direction
ipmacd_short_devi1.direction = XSELL
ipmacd_short_devi1.priority = 400

def ipmacd_short_devi1x(sif,sopened=None):#+++
    ''' 
    '''

    signal = gand(hdevi(sif.high,sif.diff1,sif.dea1,delta=10)   #即便新高离上一高点低1点，仍然可视为新高
                ,sif.s30<0
                ,sif.mm<0
                ,sif.xatr30x<6666
                )
    return signal * ipmacd_short_devi1x.direction
ipmacd_short_devi1x.direction = XSELL
ipmacd_short_devi1x.priority = 2480



####集合
xfollow = [#多头
            rsi_long_x,
            rsi_long_x2,    
            macd_long_x2,   #样本数太少，暂缓
           #空头
            rsi_short_x,
            rsi_short_x2,
            macd_short_x,
            macd_short_x2,
           #其它
            down01,     #样本数太少，暂缓
            xdown60,    #有合并损失
            xud30b,     #趋势不明
            ma1x,            
            ma60_short,  
            ama_short, #样本数太少，
          ]

xbreak = [#多头
            acd_ua,
            acd_ua_sz, 
            #acd_ua_sz_b, #样本太少，暂缓
            br30,
          #空头
            godown,
            #acd_da, #样本太少，暂缓
            #acd_da_sz_b,#样本太少，暂缓
         ]

##xagainst必须提高成功率，否则会引起最大连续回撤的快速放大. 因此对样本数暂不作限制
xagainst = [#多头
            xma_long,  
            xdma_long, 
            macd_long_x,
            up0,            
            #空头
            xma_short, #样本数太少，暂缓
            xdma_short,    #
            k15_lastdown,
            k15_lastdown_s,    #样本数太少，暂缓
            k5_lastup, 
            ipmacd_long_devi1,#有效放大了回撤? ##样本数太少
            ipmacd_short_devi1,##样本数太少
            ipmacd_short_devi1x, ##样本数太少，暂缓,但即将满足0907
            xud30s_r,  ##样本数太少
           ]

xxx2 = xfollow + xbreak + xagainst
xxx3 = xfollow + xbreak + xagainst

'''
16402 17617 17826 18228 18173 18494 18655 18663

5231
8150
4562
6817
5493
5526

'''



