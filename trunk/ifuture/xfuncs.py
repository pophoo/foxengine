# -*- coding: utf-8 -*-
'''
   重构算法
1. 在方向上更加注重于连续回撤，而不是R和收益率
2. 在方法上，按
   策略 = 状态 + 波动性 + 信号发生
   来定义, 解耦这三个方面，并可独立演进


tradesy =  control.itradex8_yy(i00,xfuncs.xxx)


##技巧
空头要素
    xatr30x < mxatr30x

'''

from wolfox.fengine.ifuture.ibase import *
import wolfox.fengine.ifuture.iftrade as iftrade

#atr5_uxstop_t_08_25_B2
#atr5_uxstop_t_08_25_B10
#atr5_uxstop_kx

def gothrough_filter(sif):  #直通函数
    return cached_ints(1,len(sif.close))

gofilter = gothrough_filter

class XFilter(object):  #为保持系统简单性,不建议用多个过滤器
    def __init__(self,*filters):
        self.filters = filters
        self.name = 'XFilter'

    def __call__(self,sif):
        sfs = [f(sif) for f in self.filters]
        return gand(*sfs)

    def add(self,sfilter):
        self.filters.append(sfilter)

class XFilterD1(XFilter): #每日第一次, 已经废弃，合成到XFunc中
    def __call__(self,sif):
        sfs = [f(sif) for f in self.filters]
        signal =  gand(*sfs)
        signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
        signal = gand(signal_s == 1)
        return signal
        


class XFunc(object):
    def __init__(self
        ,direction  #方向
        ,fstate = gothrough_filter     #状态确定函数
        ,fwave = gothrough_filter      #波动性过滤函数
        ,fsignal = gothrough_filter   #信号发生函数
        ,ffilter = iftrade.ocfilter   #过滤函数
        ,fstop = iftrade.atr5_uxstop_kx     #止损函数
        ,priority = 1500    #默认，兼容性默认
        ):
        self.name = u'%s:%s:%s:%s' % (func_name(fstate),func_name(fwave),func_name(fsignal),func_name(ffilter))
        self.fstate = fstate
        self.fwave = fwave
        self.fsignal = fsignal
        self.fstop = fstop
        self.stop_closer = fstop
        self.direction = direction
        self.priority = priority
        self.ffilter = ffilter

    def __call__(self,sif,sopened=None):
        sstate = self.cached_func(self.fstate,sif)      #self.fstate(sif)
        swave = self.cached_func(self.fwave,sif)        #self.fwave(sif)
        ssignal = self.cached_func(self.fsignal,sif)    #self.fsignal(sif)
        sfilter = self.cached_func(self.ffilter,sif)     #self.ffilter(sif)
        signal = gand(sstate,swave,ssignal,sfilter)
        signal = self.signal_filter(sif,signal)
        return signal * self.direction
 
    def signal_filter(self,sif,signal):    #信号过滤,  如去重或每天第一次
        return signal

    @staticmethod
    def reset():#清空缓存
        XFunc.cache = {}

    @staticmethod
    def cached_func(func,sif):
        #if str(func) not in XFunc.cache:
        #   XFunc.cache[str(func)] = func(sif)
        XFunc.cache[str(func)] = func(sif)
        return XFunc.cache[str(func)]

XFunc.cache = {}

class BXFuncA(XFunc):#包含全部信号
    def __init__(self
        ,fstate = gothrough_filter     #状态确定函数
        ,fwave = gothrough_filter      #波动性过滤函数
        ,fsignal = gothrough_filter   #信号发生函数
        ,ffilter = iftrade.ocfilter   #过滤函数
        ,fstop = iftrade.atr5_uxstop_kx    #止损函数
        ,priority = 1500
        ):
        XFunc.__init__(self,fstate=fstate,fwave=fwave,fsignal=fsignal,ffilter=ffilter,fstop=fstop,direction=XBUY,priority=priority)

class SXFuncA(XFunc):#包含全部信号
    def __init__(self
        ,fstate = gothrough_filter     #状态确定函数
        ,fwave = gothrough_filter      #波动性过滤函数
        ,fsignal = gothrough_filter   #信号发生函数
        ,ffilter = iftrade.ocfilter   #过滤函数
        ,fstop = iftrade.atr5_uxstop_kx     #止损函数
        ,priority = 1500        
        ):
        XFunc.__init__(self,fstate=fstate,fwave=fwave,fsignal=fsignal,ffilter=ffilter,fstop=fstop,direction=XSELL,priority=priority)

def dc_filter(sif,signal):  #去除连续信号
    return derepeatc(signal)

def d1_filter(sif,signal):  #当日第一次
    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal_s == 1)
    return signal

def df1_b_filter(sif,signal): #当时失败停止, 多头. 存在问题：成功后下去也导致不能开仓
    signal1 = d1_filter(sif,signal)
    sopen = np.select([signal!=0],[(sif.open+sif.high)/2],0)
    sopens = extend2diff(sopen,sif.date)
    sfailed = d1_filter(sif,sif.low < sopens-80)   #第一个失败
    sfailed = extend2diff(sfailed,sif.date)
    return gand(bnot(sfailed),signal)    #失败之前

def df1_s_filter(sif,signal): #当时失败停止, 空头
    signal1 = d1_filter(sif,signal)
    sopen = np.select([signal!=0],[(sif.open+sif.low)/2],0)
    sopens = extend2diff(sopen,sif.date)
    sopens = np.select([sopens!=0],[sopens],99999999)   #在当日第一个信号之前的数据应当设置为最大值
    sfailed = d1_filter(sif,sif.high > sopens+80)   #第一个失败
    sfailed = extend2diff(sfailed,sif.date)
    return gand(bnot(sfailed),signal)    #失败之前

def d1c_filter(sif,signal):
        signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
        signal = gand(signal_s == 1)
        return derepeatc(signal)

class BXFunc(BXFuncA):#去除连续
    def signal_filter(self,sif,signal):
        return dc_filter(sif,signal)

class SXFunc(SXFuncA):#去除连续
    def signal_filter(self,sif,signal):
        return dc_filter(sif,signal)

class BXFuncD1(BXFuncA):#每日第一次
    def signal_filter(self,sif,signal):
        return d1_filter(sif,signal)

class SXFuncD1(SXFuncA):#每日第一次
    def signal_filter(self,sif,signal):
        return d1_filter(sif,signal)

class BXFuncF1(BXFuncA):#每日只失败一次
    def signal_filter(self,sif,signal):
        return df1_b_filter(sif,signal)

class SXFuncF1(SXFuncA):#每日只失败一次
    def signal_filter(self,sif,signal):
        return df1_s_filter(sif,signal)




###状态判断集合
def followU30(sif):
    return gand(
           sif.s30>0
    )

def followU2(sif):
    return gand(
              sif.s30>0
              ,strend2(sif.ma60)>0
              ,sif.xstate>0              
              ,sif.ma13 > sif.ma30
    )

def followU2_2(sif):
    return gand(sif.s30>0
            ,sif.mtrend>0
            ,sif.sdma>0
          )
        
def followU2_3(sif):
    return gand(sif.r60>20
            ,strend2(sif.ma30)>10   #这个差异非常大
            ,sif.s1>0
         )

def followU3(sif):
    return gand(sif.s30>0
                ,sif.s3>0
                ,sif.s1>0
                ,sif.r7>0
        )

def followU3_2(sif):
    return gand(sif.s30>0
                ,sif.s3>0
                ,sif.s1>0
                ,sif.r120>0
        )


def followD2(sif):
    #需要首盈继续，首亏歇手
    return gand(
                sif.diff1<0  #以强为主
                ,sif.s30 < 0
                ,sif.s5<0
                ,sif.t120 < 0
                ,sif.r120< 0
                ,sif.r60 < 0    
                ,strend2(sif.ma60)<0
            )

def followD3(sif):
    return gand(
               sif.sdiff30x<0
               ,sif.sdiff3x < sif.sdea3x
               ,sif.r60<0
           )
 
def followD32(sif):
    return  gand(gor(strend2(sif.sdiff30x-sif.sdea30x)<0,sif.s30<0)
                  ,strend2(sif.diff1-sif.dea1)<0
                  ,sif.xstate<0
                  ,sif.s1<0
            )


def followD4(sif):
    return gand(sif.sdiff30x<0
                ,sif.sdiff5x<0
                ,sif.sdiff3x<0
                ,sif.s3<-2
                ,sif.r120<0
                ,sif.r60<0
            )


def followD41(sif):
    return gand(sif.sdiff30x<0
                ,sif.sdiff5x<0
                ,sif.diff1<0
                ,sif.s30<0
                ,sif.s3<0
                ,sif.r120<0
                ,sif.r13<0
            )

def followD42(sif):
    return gand(sif.s15< 0
                ,sif.s5<0
                ,sif.s1<0
                ,strend2(sif.ma13 - sif.ma30)<0 #差距扩大中
                ,sif.r60 < 0
                ,sif.t120<0
                #,sif.r30<0
            )

def followD43(sif):
    return gand(sif.r120<0
                ,sif.s3<0
                ,sif.s1<0
                ,sif.r60<0
        )

def followD1(sif):
    return gand(
            sif.s1<-5
            ,sif.s3<-2
            ,strend2(sif.ma30)<0
            ,sif.t120<-2
            ,sif.r60<20
           )

def followU1(sif):

    return gand(
            sif.diff1>sif.dea1
            ,sif.t120>0
            ,sif.s30>0
           )

### 波动性过滤集合
def downA(sif):
    return gand(
            sif.xatr30x < sif.mxatr30x
         )

def nx2000(sif):
    return gand(sif.xatr<2000
            )

def nx1600B(sif):
    return gand(sif.xatr<1600
            ,sif.xatr30x<12000
    )
    
def nx2000B(sif):
    return gand(sif.xatr < 2000
                ,sif.xatr30x < 10000
            )

def upW2(sif):
    return gand(sif.xatr<2000
            ,strend2(sif.mxatr30x)>0
        )

def upW3(sif):
    return gand(
            strend2(sif.mxatr)>0
            ,sif.xatr30x < 10000
            )

def ZA(sif):
    return gand(
            sif.xatr30x < sif.mxatr30x
            ,sif.xatr < 2000
         )

def ZB(sif):
    return gand(sif.xatr > sif.mxatr
                ,strend2(sif.mxatr30x)<0
                ,sif.xatr30x < sif.mxatr30x
        )


def downW2(sif):
    return gand(
             #sif.mxadtr30x > sif.mxautr30x
             #sif.xatr30x < sif.mxatr30x
             sif.xatr<3600
             ,sif.xatr30x<12000
             ,sif.mxatr > rollx(sif.mxatr,270)  #xatr在放大中,这个条件在单个很有用，合并时被处理掉             
             ,sif.mxadtr > sif.mxautr
        )

def narrowW(sif):
    return gand(
            sif.xatr > sif.mxatr
            ,strend2(sif.mxatr)>0
            ,sif.xatr > 666
            ,sif.xatr < 2000
        )
    

###过滤器集合

def nfilter(sif):
    return gand(sif.time>944,sif.time<1500)

def efilter(sif):
    return gand(sif.time>914,sif.time<1500)

def e1400filter(sif):
    return gand(sif.time>914,sif.time<1400)

def e1430filter(sif):
    return gand(sif.time>914,sif.time<1430)


def efilter2(sif):
    return gand(sif.time>929,sif.time<1500)

def e1400filter2(sif):
    return gand(sif.time>929,sif.time<1400)

def e1430filter2(sif):
    return gand(sif.time>929,sif.time<1430)

def n1400filter(sif):
    return gand(sif.time>944,sif.time<1400)

def n1430filter(sif):
    return gand(sif.time>944,sif.time<1430)

def exfilter(sif):
    return gor(sif.time<1000,gand(sif.time>=1300,sif.time<=1330))

def ixfilter(sif):
    return gand(sif.time>=1030,sif.time<=1300)

###信号集合
def rsiU(sif):
    return gand(cross(sif.rsi19,sif.rsi7)>0,strend2(sif.rsi7)>0)

def rsiD(sif):
    return gand(cross(sif.rsi19,sif.rsi7)<0,strend2(sif.rsi7)<0)

def macdU(sif):
    return gand(cross(sif.dea1,sif.diff1)>0,strend2(sif.diff1)>0)

def macdD(sif):
    return gand(cross(sif.dea1,sif.diff1)<0,strend2(sif.diff1)<0)

def ubreak(sif):#突破
    wave = np.zeros_like(sif.close)
    wave[sif.i_cof10] = rollx(sif.atr10) /4/XBASE  #向下放宽
    wave = extend2next(wave)

    UA,DA,xhigh10,xlow10 = range_a(sif,914,929,wave)

    return gand(sif.close >= UA)
 
def dbreak(sif):#向下突破
    wave = np.zeros_like(sif.close)
    wave[sif.i_cof10] = rollx(sif.atr10) /2/XBASE  #掠过914-919的atr10
    wave = extend2next(wave)
    
    UA,DA,xhigh10,xlow10 = range_a(sif,914,929,wave)

    return gand(sif.close <= DA)
    
def macd5xd(sif):
    return dnext_cover(gand(cross(sif.dea5x,sif.diff5x)<0,strend2(sif.diff5x)<0),sif.close,sif.i_cof5,1)

def macd3xd(sif):
    sk3,sd3 = skdj(sif.high3,sif.low3,sif.close3)
    sk3x = dnext_cover(sk3,sif.close,sif.i_cof3,3)
    sd3x = dnext_cover(sd3,sif.close,sif.i_cof3,3)
    
    signal = dnext_cover(gand(cross(sif.dea3x,sif.diff3x)<0,strend2(sif.diff3x)<0),sif.close,sif.i_cof3,1)
 
    return gand(signal,sk3x < sd3x)

def macd3xu(sif):
    sk3,sd3 = skdj(sif.high3,sif.low3,sif.close3)
    sk3x = dnext_cover(sk3,sif.close,sif.i_cof3,3)
    sd3x = dnext_cover(sd3,sif.close,sif.i_cof3,3)
    
    signal = dnext_cover(gand(cross(sif.dea3x,sif.diff3x)>0,strend2(sif.diff3x)>0),sif.close,sif.i_cof3,1)
    return gand(signal)#,sk3x > sd3x)


def ubreak_m(sif):  #冲高后macd上叉
    UA,DA,xhigh10,xlow10 = range_a(sif,914,944,0)
    signal = np.zeros_like(sif.diff1)
    signal[sif.i_cof5] = cross(xhigh10[sif.i_cof5],sif.high5)>0
    signal = sfollow(signal,cross(sif.dea1,sif.diff1)>0,15)        
    return signal
    
def ubreak_a(sif):
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

    return gand(ms_ua==1         #第一个ua
              #,bnot(ms_da)       #没出现过da 
       )
    

def nhd(sif):   #日内新高+1点
    return gand(cross(rollx(sif.dhigh)+10,sif.close)>0
            )
 

def uu(sif):
    return gand(rollx(sif.close,1) > rollx(sif.close,2),
                sif.close > rollx(sif.close),
                rollx(sif.close)>rollx(sif.open),
                sif.close > sif.open,
                sif.close - sif.open < 120,
            )    

def uu2(sif):
    return gand(rollx(sif.close,1) > rollx(sif.close,2),
                sif.close > rollx(sif.close),
            )    


def dd(sif):
    return gand(rollx(sif.close,1) < rollx(sif.close,2),
                sif.close < rollx(sif.close),
                rollx(sif.close)<rollx(sif.open),
                sif.close < sif.open
            )

def dd2(sif):
    return gand(rollx(sif.close,1) < rollx(sif.close,2),
                sif.close < rollx(sif.close),
                sif.close < sif.open,
            )


def dlx(sif):
    return gand(
                sif.close < rollx(sif.close),
                sif.close < sif.open,
                sif.close < rollx(tmin(sif.low,30)),
                tmax(sif.high,10) > tmax(sif.high,30) - 30
            )
        

def ldhigh(sif):
    return    sif.close > rollx(sif.dhigh)-15
        
def lhigh120(sif):
    return sif.close > rollx(tmax(sif.high,120))-30

def down_filter(sif):
    return  sif.open - sif.close < 120

def gdlow(sif):
    return  sif.close < rollx(sif.dlow)+10

def glow120(sif):
    return sif.close < rollx(tmin(sif.low,120))+60


def k3d3(sif):
    signal3 = gand(sif.close3 < sif.open3,
                   rollx(sif.close3) < rollx(sif.open3),
                   rollx(sif.close3,2) < rollx(sif.open3,2),
                   sif.high3 < rollx(sif.high3,2),
                   rollx(sif.high3)<rollx(sif.high3,2),
                   sif.close3 < rollx(sif.close3,2),
                   sif.diff3x < sif.dea3x,
                   sif.low3 == tmin(sif.low3,3),
                )
    return dnext_cover(signal3,sif.close,sif.i_cof3,1)

def k5d3(sif):
    ma5_13 = ma(sif.close5,13)
    ma5_30 = ma(sif.close5,30)    
    ma5_60 = ma(sif.close5,60)        
    signal5 = gand(sif.close5 < sif.open5,
                   rollx(sif.close5) < rollx(sif.open5),
                   rollx(sif.close5,2) < rollx(sif.open5,2),
                   sif.high5 < rollx(sif.high5,2),
                   rollx(sif.high5)<rollx(sif.high5,2),
                   sif.close5 < rollx(sif.close5,2),
                   sif.diff5x < sif.dea5x,
                   sif.low5 == tmin(sif.low5,3),
                   strend2(ma5_30)<0,
                )
    return dnext_cover(signal5,sif.close,sif.i_cof5,1)


uub1 = XFilter(uu,ldhigh)
uub2 = XFilter(uu,lhigh120)

dds1 = XFilter(dd,down_filter,gdlow)
dds2 = XFilter(dd,down_filter,glow120)
dds4 = XFilter(dd,down_filter)

dbreak_m5xd = XFilter(dbreak,macd5xd)
dbreak_m3xd = XFilter(dbreak,macd3xd)

    
xxx = []
#突破系列必须用ALL
ua_fa = BXFuncA(fstate=followU2,fsignal=XFilter(ubreak),fwave=upW2,ffilter=n1430filter)   #1400之前的更可靠
ua_fa_m = BXFuncA(fstate=followU2_2,fsignal=ubreak_m,fwave=nx2000,ffilter=n1400filter)   #1400之前的更可靠
ua_fa_a = BXFuncA(fstate=followU30,fsignal=XFilter(ubreak_a),fwave=ZA,ffilter=e1400filter2)   #1400之前的更可靠,总体不甚可靠
da_fa = SXFuncF1(fstate=followD2,fsignal=XFilter(dbreak,dd2),fwave=downW2,ffilter=n1400filter)

#这些可以用D1/F1
da_m30 = SXFuncA(fstate=followD3,fsignal=dbreak_m5xd,fwave=downA,ffilter=n1430filter)
da_m30b = SXFuncA(fstate=followD32,fsignal=dbreak_m5xd,ffilter=n1430filter)
dbrb = BXFuncA(fstate=followU2_3,fsignal=nhd,fwave=upW3,ffilter=n1430filter)

xxx_break = [ua_fa,da_fa,da_m30,da_m30b,ua_fa_m,dbrb,ua_fa_a]

xuub = BXFuncA(fstate=followU3,fsignal=uub1,fwave=narrowW,ffilter=exfilter)
xuub2 = BXFuncA(fstate=followU3_2,fsignal=uub2,fwave=narrowW,ffilter=ixfilter)
xdds = SXFuncA(fstate=followD4,fsignal=dds1,fwave=nx2000,ffilter=exfilter)
xdds2 = SXFuncD1(fstate=followD41,fsignal=dds2,fwave=nx2000,ffilter=ixfilter)
xdds4 = SXFuncA(fstate=followD42,fsignal=dds4,fwave=nx2000B,ffilter=e1430filter)    #1430
xds = SXFunc(fstate=followD43,fsignal=dlx,fwave=ZB,ffilter=e1430filter)     #1430

xxx_orb = [xuub,xuub2,xdds,xdds2,xdds4,xds]

#这个止损要够忍，就是说上去后还要忍下来才行
xmacd3s = SXFuncD1(fstate = followD1,fsignal=macd3xd,fwave=nx1600B,ffilter=n1400filter)



xxx_index  = [xmacd3s]

###K线
###3分钟K线3连阴，且打到diff<dea

def downK5(sif):
    return gand(
                sif.xatr30x <10000,
                #sif.xatr30x > sif.mxatr30x,    #这个条件很加强
                sif.s3<-1,
                sif.t120<0,
            )

def downK3(sif):
    return gand(strend2(sif.ma30)<0,
                sif.ma13< sif.ma30,
                sif.xatr30x <10000,
                sif.sdiff3x<0,
                sif.s5<-3,
                sif.t120<0,
            )


k3_d3 = SXFuncA(fstate=downK3,fsignal=k3d3,fwave=gofilter,ffilter=nfilter)
k5_d3 = SXFuncD1(fstate=downK5,fsignal=k5d3,fwave=gofilter,ffilter=n1430filter)

xxx_k = [k5_d3]#,k3_d3]

xxx = xxx_break+xxx_orb + xxx_k

for x in xxx:
    #x.stop_closer = iftrade.atr5_uxstop_k0 #40/60
    #x.stop_closer = iftrade.atr5_uxstop_kC #60/60   
    #x.stop_closer = iftrade.atr5_uxstop_kD #60/80       
    x.stop_closer = iftrade.atr5_uxstop_kF #60/120       
    #x.stop_closer = iftrade.atr5_uxstop_k60 #60/90
    #x.stop_closer = iftrade.atr5_uxstop_k90 #60/90
    #x.stop_closer = iftrade.atr5_uxstop_k120 #60/20
