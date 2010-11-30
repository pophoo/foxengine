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

def gothrough_filter(sif):  #直通函数
    return cached_ints(1,len(sif.close))

class XFilter(object):  #为保持系统简单性,不建议用多个过滤器
    def __init__(self,*filters):
        self.filters = filters
        self.name = 'XFilter'

    def __call__(self,sif):
        sfs = [f(sif) for f in self.filters]
        return gand(*sfs)

    def add(self,sfilter):
        self.filters.append(sfilter)

class XFunc(object):
    def __init__(self
        ,direction  #方向
        ,fstate = gothrough_filter     #状态确定函数
        ,fwave = gothrough_filter      #波动性过滤函数
        ,fsignal = gothrough_filter   #信号发生函数
        ,ffilter = iftrade.ocfilter   #过滤函数
        ,fstop = iftrade.atr5_uxstop_k_250     #止损函数
        ,priority = 1500    #默认，兼容性默认
        ):
        self.name = u'%s:%s:%s:%s' % (func_name(fstate),func_name(fwave),func_name(fsignal),func_name(ffilter))
        self.fstate = fstate
        self.fwave = fwave
        self.fsignal = fsignal
        self.fstop = fstop
        self.direction = direction
        self.priority = priority
        self.ffilter = ffilter

    def __call__(self,sif,sopened=None):
        sstate = self.cached_func(self.fstate,sif)      #self.fstate(sif)
        swave = self.cached_func(self.fwave,sif)        #self.fwave(sif)
        ssignal = self.cached_func(self.fsignal,sif)    #self.fsignal(sif)
        sfilter = self.cached_func(self.ffilter,sif)     #self.ffilter(sif)
        signal = gand(sstate,swave,ssignal,sfilter)
        return signal * self.direction
 
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

class BXFunc(XFunc):
    def __init__(self
        ,fstate = gothrough_filter     #状态确定函数
        ,fwave = gothrough_filter      #波动性过滤函数
        ,fsignal = gothrough_filter   #信号发生函数
        ,ffilter = iftrade.ocfilter   #过滤函数
        ,fstop = iftrade.atr5_uxstop_k_250    #止损函数
        ,priority = 1500
        ):
        XFunc.__init__(self,fstate=fstate,fwave=fwave,fsignal=fsignal,ffilter=ffilter,fstop=fstop,direction=XBUY,priority=priority)

class SXFunc(XFunc):
    def __init__(self
        ,fstate = gothrough_filter     #状态确定函数
        ,fwave = gothrough_filter      #波动性过滤函数
        ,fsignal = gothrough_filter   #信号发生函数
        ,ffilter = iftrade.ocfilter   #过滤函数
        ,fstop = iftrade.atr5_uxstop_k_250     #止损函数
        ,priority = 1500        
        ):
        XFunc.__init__(self,fstate=fstate,fwave=fwave,fsignal=fsignal,ffilter=ffilter,fstop=fstop,direction=XSELL,priority=priority)

###状态判断集合
def followU30(sif):
    return gand(sif.s30>0
            )

def followU2(sif):
    return gand(
              sif.diff1>0  
              ,sif.s30>0
              ,sif.ma13 > sif.ma30
              ,strend2(sif.ma60)>0
              ,sif.r20>0
              ,sif.xstate>0              
    )

def followU2_2(sif):
    return gand(sif.s30>0
            ,sif.mtrend>0
          )
        


def followD2(sif):
    return gand(sif.diff1<0  #以强为主
                ,sif.s30 < -1
                ,sif.t120 < 0    #排除波动
                ,sif.r60 < -4     #排除波动
                ,sif.r20 < 0
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
            )


### 波动性过滤集合
def downA(sif):
    return gand(
            sif.xatr30x < sif.mxatr30x
         )

def upW1(sif):
    return gand(sif.xatr<2000
            )
    
def upW2(sif):
    return gand(sif.xatr<2000
            ,strend2(sif.mxatr30x)>0
            )

def ZA(sif):
    return gand(
            sif.xatr30x < sif.mxatr30x
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
    
    

###过滤器集合

def nfilter(sif):
    return gand(sif.time>944,sif.time<1500)

def efilter(sif):
    return gand(sif.time>914,sif.time<1500)

def n1400filter(sif):
    return gand(sif.time>944,sif.time<1400)

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
    return dnext_cover(cross(sif.dea5x,sif.diff5x)<0,sif.close,sif.i_cof5,1)

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
              ,bnot(ms_da)       #没出现过da 
       )
    

def nhd(sif):   #日内新高+1点
    return cross(rollx(sif.dhigh)+10,sif.close)>0
    

dbreak_m5xd = XFilter(dbreak,macd5xd)

    
xxx = []
ua_fa = BXFunc(fstate=followU2,fsignal=ubreak,fwave=upW2,ffilter=nfilter)   #1400之前的更可靠
ua_fa_m = BXFunc(fstate=followU2_2,fsignal=ubreak_m,fwave=upW1,ffilter=n1400filter)   #1400之前的更可靠
ua_fa_a = BXFunc(fstate=followU30,fsignal=ubreak_a,fwave=ZA,ffilter=n1400filter)   #1400之前的更可靠,总体不甚可靠
da_fa = SXFunc(fstate=followD2,fsignal=dbreak,fwave=downW2,ffilter=nfilter)
da_m30 = SXFunc(fstate=followD3,fsignal=dbreak_m5xd,ffilter=nfilter,fwave=downA)
da_m30b = SXFunc(fstate=followD32,fsignal=dbreak_m5xd,ffilter=nfilter)
dbrb = BXFunc(fstate=followU2_2,fsignal=nhd,fwave=upW1,ffilter=nfilter)

xxx_break = [ua_fa,da_fa,da_m30,da_m30b,ua_fa_m,ua_fa_a]



