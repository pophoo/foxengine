# -*- coding: utf-8 -*-
'''
止损策略在风险管理上的一致性
1. 设定三类止损：
   初始止损I、保本止损C和跟踪止盈W
2. 一致性原则
   三者是逐步放宽的关系
   如I=6, C=12, W=15, 则初始止损为6,运动到12之前，如11则最大回退为17
   到15之后，回退变成15
   这个是不一致的, W至少为18

   但从另一个角度，开仓时的风险最大，上升后风险应该逐级减少. 则最小止盈15也可接受

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

default_stop_closer  = iftrade.atr5_uxstop_kF

def gothrough_filter(sif):  #直通函数
    return cached_ints(1,len(sif.close))

gofilter = gothrough_filter

class XFilter(object):  #为保持系统简单性,不建议用多个过滤器
    '''AND过滤器
    '''
    def __init__(self,*filters):
        self.filters = filters
        self.name = 'XFilter'

    def __call__(self,sif):
        sfs = [f(sif) for f in self.filters]
        return gand(*sfs)

    def add(self,sfilter):
        self.filters.append(sfilter)

class XRFilter(object):  #为保持系统简单性,不建议用多个过滤器
    ''' OR过滤器
    '''
    def __init__(self,*filters):
        self.filters = filters
        self.name = 'XFilter'

    def __call__(self,sif):
        sfs = [f(sif) for f in self.filters]
        return gor(*sfs)

    def add(self,sfilter):
        self.filters.append(sfilter)



class XFunc(object):
    def __init__(self
        ,direction  #方向
        ,fstate = gothrough_filter     #状态确定函数
        ,fwave = gothrough_filter      #波动性过滤函数
        ,fsignal = gothrough_filter   #信号发生函数
        ,ffilter = iftrade.ocfilter   #过滤函数
        ,fstop = default_stop_closer     #止损函数
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
        ,fstop = default_stop_closer    #止损函数
        ,priority = 1500
        ):
        XFunc.__init__(self,fstate=fstate,fwave=fwave,fsignal=fsignal,ffilter=ffilter,fstop=fstop,direction=XBUY,priority=priority)

class SXFuncA(XFunc):#包含全部信号
    def __init__(self
        ,fstate = gothrough_filter     #状态确定函数
        ,fwave = gothrough_filter      #波动性过滤函数
        ,fsignal = gothrough_filter   #信号发生函数
        ,ffilter = iftrade.ocfilter   #过滤函数
        ,fstop = default_stop_closer     #止损函数
        ,priority = 1500        
        ):
        XFunc.__init__(self,fstate=fstate,fwave=fwave,fsignal=fsignal,ffilter=ffilter,fstop=fstop,direction=XSELL,priority=priority)

class CFunc(XFunc):
    '''同类函数的组合
       用于相关性比较强的函数的组合，避免同类信号次第发生 
    '''
    def __init__(self,name,func1,*funcs):
        '''必须提供第一个函数'''
        self.name = name
        self.funcs = [func1]
        self.funcs.extend(funcs)
        self.direction = func1.direction
        self.priority = func1.priority
        self.stop_closer = func1.stop_closer
        #print self.stop_closer

    def __call__(self,sif,sopened=None):
        signal = gor(*[func(sif,sopened) for func in self.funcs])
        signal = self.signal_filter(sif,signal)
        return signal * self.direction


def dc_filter(sif,signal):  #去除连续信号
    return derepeatc(signal)

def d1_filter(sif,signal):  #当日第一次
    signal_s = sum2diff(extend2diff(signal,sif.date),sif.date)
    signal = gand(signal_s == 1)
    return signal

def df1_b_filter(sif,signal): #当时失败停止, 多头. 存在问题：成功后下去也导致不能开仓
    signal1 = d1_filter(sif,signal)
    sopen = np.select([signal!=0],[(sif.open+sif.high)/2],0)
    sopen = rollx(sopen)    #绕过信号位置
    sopens = extend2diff(sopen,sif.date)
    sfailed = d1_filter(sif,sif.low < sopens-80)   #第一个失败
    sfailed = extend2diff(sfailed,sif.date)
    return gand(bnot(sfailed),signal)    #失败之前

def df1_s_filter(sif,signal): #当时失败停止, 空头
    signal1 = d1_filter(sif,signal)
    sopen = np.select([signal!=0],[(sif.open+sif.low)/2],0)
    sopen = rollx(sopen)    #绕过信号位置
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

class CXFunc(CFunc):#去除连续
    def signal_filter(self,sif,signal):
        return dc_filter(sif,signal)

class BXFuncD1(BXFuncA):#每日第一次
    def signal_filter(self,sif,signal):
        return d1_filter(sif,signal)

class SXFuncD1(SXFuncA):#每日第一次
    def signal_filter(self,sif,signal):
        return d1_filter(sif,signal)

class CFuncD1(CFunc):#每日第一次
    def signal_filter(self,sif,signal):
        return d1_filter(sif,signal)

class BXFuncF1(BXFuncA):#每日只失败一次
    def signal_filter(self,sif,signal):
        return df1_b_filter(sif,signal)

class SXFuncF1(SXFuncA):#每日只失败一次
    def signal_filter(self,sif,signal):
        return df1_s_filter(sif,signal)

class CBFuncF1(CFunc):#每日只失败一次
    def signal_filter(self,sif,signal):
        return df1_b_filter(sif,signal)

class CSFuncF1(CFunc):#每日只失败一次
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
                sif.s30 < 0
                ,sif.t120 < 0
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

def followD44(sif):
    #需要首盈继续，首亏歇手
    return gand(
                sif.s30 < 0,
                sif.s5<0,
                sif.t120 < 0,
                sif.r60 < 0,
                sif.r13<0,
                strend2(sif.ma60)<0,
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

def ZC(sif):
    return gand(strend2(sif.mxatr)>0,
            sif.xatr < sif.mxatr
        )

def ZD(sif):
    return gand(
            sif.xatr30x <10000,
        )

def ZE(sif):
    return gand(
            sif.xatr < sif.mxatr,
            sif.xatr < 2500,
        )

def ZF(sif):
    return gand(
            strend2(sif.mxatr30x)<0,
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

def exfilter2(sif):
    return gor(gand(sif.time>916,sif.time<1000),gand(sif.time>=1300,sif.time<=1330))

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
                sif.low < rollx(sif.low,2),
                sif.high < rollx(sif.high,2),
            )


def dlx(sif):
    return gand(
                sif.close < rollx(sif.close),
                sif.close < sif.open,
                sif.close < rollx(tmin(sif.low,30)),
                tmax(sif.high,10) > tmax(sif.high,30) - 30
            )
        
def dx(sif):
    return gand(
                sif.close < rollx(sif.close),
                sif.close < sif.open,
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


#信号发生组合
uub1 = XFilter(uu,ldhigh)
uub2 = XFilter(uu,lhigh120)

dds1 = XFilter(dd,down_filter,gdlow)
dds2 = XFilter(dd,down_filter,glow120)
dds4 = XFilter(dd,down_filter)

dbreak_m5xd = XFilter(dbreak,macd5xd)
dbreak_m3xd = XFilter(dbreak,macd3xd)

    
xxx = []
#突破系列必须用ALL
ua_fa = BXFuncD1(fstate=followU2,fsignal=XFilter(ubreak),fwave=upW2,ffilter=n1430filter)   #1400之前的更可靠
ua_fa_m = BXFuncA(fstate=followU2_2,fsignal=ubreak_m,fwave=nx2000,ffilter=n1400filter)   #1400之前的更可靠
ua_fa_a = BXFuncA(fstate=followU30,fsignal=XFilter(ubreak_a),fwave=ZA,ffilter=e1400filter2)   #1400之前的更可靠,总体不甚可靠
da_fa = SXFuncF1(fstate=followD2,fsignal=XFilter(dbreak,dd2),fwave=downW2,ffilter=n1400filter)  #这个被覆盖了

ua_fc = [ua_fa,ua_fa_m,ua_fa_a]


#这些可以用D1/F1
da_m30 = SXFuncA(fstate=followD3,fsignal=dbreak_m5xd,fwave=downA,ffilter=n1430filter)
da_m30b = SXFuncA(fstate=followD32,fsignal=dbreak_m5xd,ffilter=n1430filter)
dbrb = BXFuncA(fstate=followU2_3,fsignal=nhd,fwave=upW3,ffilter=n1430filter)

da_fc = [da_m30,da_m30b]

ua_fx = CBFuncF1(u'ua集合',ua_fa,ua_fa_m,ua_fa_a)
da_fx = CSFuncF1(u'da集合',da_m30,da_m30b)

xxx_break = [ua_fx,da_fx,dbrb]

xxx_break_candidate = [ua_fa,ua_fa_m,dbrb,ua_fa_a,da_m30,da_m30b,da_fa]

###xxx_orb

xuub = BXFuncA(fstate=followU3,fsignal=uub1,fwave=narrowW,ffilter=exfilter)
xuub2 = BXFuncA(fstate=followU3_2,fsignal=uub2,fwave=narrowW,ffilter=ixfilter)
xdds = SXFuncA(fstate=followD4,fsignal=dds1,fwave=nx2000,ffilter=exfilter)
xdds2 = SXFuncD1(fstate=followD41,fsignal=dds2,fwave=nx2000,ffilter=ixfilter)
xdds3 = SXFuncF1(fstate=followD44,fsignal=dd2,fwave=downW2,ffilter=n1430filter)
xdds4 = SXFuncA(fstate=followD42,fsignal=dds4,fwave=nx2000B,ffilter=e1430filter)    #1430
xds = SXFunc(fstate=followD43,fsignal=dlx,fwave=ZB,ffilter=e1430filter)     #1430

xuub_x = CFunc(u'XUUB集合',xuub,xuub2)   #这两个时间叉开
xdds_x = CSFuncF1(u'xdds集合',xdds,xdds2,xdds3,xdds4,xds)

xxx_orb = [xuub,xuub2,xdds,xdds2,xdds3,xdds4,xds]   #没有必要使用CFunc

xxx_orb_candidate = [xuub,xuub2,xdds,xdds2,xdds3,xdds4,xds]

#指标系列 增益不大
#信号
def T_D0(sif,sopened=None): #++
    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1)<0)
    return signal

def T_U0(sif,sopened=None):
    '''
        上穿0线
    '''
    signal = gand(cross(cached_zeros(len(sif.diff1)),sif.diff1)>0)
    return signal


#状态
def SD0(sif):
    return gand(
            sif.t120<0,
            sif.r60<0,
            sif.sdiff30x<0,
            strend(sif.ma30)<0,
        )

def SU0(sif):
    return gand(
            sif.s30>0,
            sif.s3>0,
            strend2(sif.diff1)>3,
            sif.sdiff5x<0,
            strend2(sif.ma30)>0,
        )


#波动过滤
def WD0(sif):
    return gand(
            strend2(sif.mxatr30x)<0,
            strend2(sif.mxatr)>0,
            sif.xatr < 2500,
            sif.xatr30x<12000,
        )

def WU0(sif):
    return gand(
            sif.xatr < 1500,
            sif.xatr30x>6000,
        )
    
xdown01 = SXFunc(fstate=SD0,fsignal=T_D0,fwave=WD0,ffilter=efilter)
xup01 = BXFunc(fstate=SU0,fsignal=T_U0,fwave=WU0,ffilter=efilter2)

xmacd3s = SXFuncD1(fstate = followD1,fsignal=macd3xd,fwave=nx1600B,ffilter=n1400filter)

xxx_index  = [xdown01,xup01]
xxx_index_candidate =[xmacd3s]


###K线
###3分钟K线3连阴，且打到diff<dea
#顺势K系列
#信号
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

def T15_H1(sif,sopened=None):
    '''
        15分钟调整模式
        这里最强的筛选条件是 xatr30x>8000
        说明震荡非常大. 通常是顶部震荡
        效果不错，但是叠加不好
    '''
    
    ma15_30 = ma(sif.close15,30)
    signal15 = gand(#上15分钟为最高点
                rollx(sif.high15,1) > rollx(sif.high15,2),
                rollx(sif.high15,1) > sif.high15,
                sif.close15 < rollx(sif.close15),
                strend2(ma15_30)<0,
                )

    delay = 30

    bline15 = rollx(sif.low15,1)
    bline = dnext_cover(np.select([signal15>0],[bline15],[0]),sif.close,sif.i_cof15,delay)
    
    #mask = dnext_cover(np.select([rollx(signal15)>0],[1],[0]),sif.close,sif.i_cof15,15) 
    #signal = gand(sif.close < bline,mask)  #貌似后移效果较好
    signal = gand(sif.low < bline)
    
    return signal

def T15_M3(sif,sopened=None,delay=30):
    signal15 = gand(
                rollx(sif.high15) == tmax(sif.high15,3)
                ,sif.low15 < rollx(sif.low15)
                )

    bline15 = gmin(sif.close15,sif.open15)  #sif.low15
    bline = dnext_cover(np.select([signal15>0],[bline15],[0]),sif.close,sif.i_cof15,delay)


    signal = sif.close < bline
    return signal    

T15_M3B = fcustom(T15_M3,delay=15)


def T10_H1(sif,sopened=None):
    '''
        10分钟调整模式
        这里最强的筛选条件是 xatr30x>8000
        说明震荡非常大. 通常是顶部震荡
        适合振荡期 nsocfilter
    '''
    
    signal10 = gand(
                rollx(sif.high10,1) >= rollx(sif.high10,2)
                ,rollx(sif.high10,1) >= sif.high10
                ,rollx(sif.high10,1) == tmax(sif.high10,4)
                )

    delay = 30
    
    bline10 = rollx(gmin(sif.open10,sif.close10),1)
    bline = dnext_cover(np.select([signal10>0],[bline10],[0]),sif.close,sif.i_cof10,delay)

    signal = sif.close < bline
    return signal

def T10_L1(sif,sopened=None):
    '''
        10分钟调整后上涨模式
        这里最强的筛选条件是strend2(sif.mxatr30x)>0
        说明震荡在加大
    '''
    
    signal10 = gand(
                rollx(sif.low10,1) < rollx(sif.low10,2)
                ,rollx(sif.low10,1) < sif.low10
                )

    delay = 30

    bline10 = sif.high10#gmax(sif.close10,sif.open10)#sif.high10
    bline = dnext_cover(np.select([signal10>0],[bline10],[0]),sif.close,sif.i_cof10,delay)

    signal = gand(sif.close > bline,bline>0)
    return signal

def T5_P3(sif,sopened=None):
    '''
        顶部衰竭模式c
    '''
    signal5 = gand(sif.close5 < sif.open5,
                   rollx(sif.close5) < rollx(sif.open5),
                   rollx(sif.close5,2) < rollx(sif.open5,2),
                   sif.high5 < rollx(sif.high5,2),
                   rollx(sif.high5)<rollx(sif.high5,2),
                   sif.close5 < rollx(sif.close5,2),
                   sif.low5 == tmin(sif.low5,10),
                )
    signal = dnext_cover(signal5,sif.close,sif.i_cof5,1)
    return signal

def T3_H10(sif,sopened = None):
    '''
        下降
    '''
    signal3 = gand(rollx(sif.high3,1) == tmax(sif.high3,10),
                   sif.close3 <= rollx(gmin(sif.open3,sif.close3),1),    #下一个点
                )

    signal = dnext_cover(signal3,sif.close,sif.i_cof3,1)
    return signal

def T1_RD(sif,sopened = None):
    '''
        #注意，这里的high是最近30分钟中的最低,而不是最高
        这是一个误输入而来的指标
        是一个下跌中继形态
    '''
    signal = gand(rollx(sif.high) == tmin(sif.high,30)   #前一分钟是前n-1分钟最小值，且小于当前分钟
                ,rollx(sif.close)<rollx(sif.open)   #下行
                ,sif.close < rollx(sif.low)
                )
    return signal

def T1_RU(sif,sopened = None):
    '''
        上升中继
    '''
    signal = gand(rollx(sif.low) == tmax(sif.low,20)   
                ,rollx(sif.close)>rollx(sif.open)   
                ,sif.close > rollx(sif.high)
                )
    return signal

def T1_DVB(sif,sopened=None):
    signal = gand(
                sif.close > rollx(sif.high)
                ,sif.close - rollx(gmax(sif.open,sif.close)) < 150
                )
    return signal    

def T1_UUX(sif,sopened=None):
    '''
        2上一调整
    '''
    signal = gand(rollx(sif.close,2) > rollx(sif.close,3)
                ,rollx(sif.close,1) > rollx(sif.close,2)
                ,rollx(sif.close,2) > rollx(sif.open,2)
                ,sif.low < rollx(sif.low)
                ,sif.low > rollx(sif.low,3)
                ,(sif.close - rollx(sif.close,3))*XBASE*XBASE / sif.close < 10
                )
    return signal

def T1_DUU(sif,sopened=None):
    '''
        2上一调整
    '''
    signal = gand(rollx(sif.close,2) < rollx(sif.close,3)
                ,rollx(sif.close,1) > rollx(sif.close,2)
                ,sif.close > rollx(sif.close)                
                ,rollx(sif.low,2) > rollx(sif.low,3)
                )
    return signal

def T1_DDUUD(sif,sopened=None):
    '''
        两下两上下
    '''
    signal = gand(rollx(sif.close,4) < rollx(sif.close,5)
                ,rollx(sif.close,3) < rollx(sif.close,4)
                ,rollx(sif.close,2) > rollx(sif.close,3)
                ,rollx(sif.close,1) > rollx(sif.close,2)
                ,sif.close < rollx(sif.close)
                ,sif.low == tmin(sif.low,5)
                )
    return signal

def T1_UUD(sif,sopened=None):
    signal = gand(
                rollx(sif.close,2) > rollx(sif.close,3)
                ,rollx(sif.close,1) > rollx(sif.close,2)
                ,sif.close < rollx(sif.close)
                ,sif.close < rollx(sif.close,3)
                )
    return signal

def T1_DDD(sif,sopened=None):
    signal = gand(
                rollx(sif.close,2) < rollx(sif.open,2)
                ,rollx(sif.close,1) < rollx(sif.open,1)
                ,sif.close < sif.open
                #,sif.close < rollx(sif.open,2)
                )
    return signal

def T1_DDX(sif,sopened=None):
    signal = gand(rollx(sif.close,2) < rollx(sif.close,3)
                ,rollx(sif.close,1) < rollx(sif.close,2)
                ,sif.high > rollx(sif.high)
                ,sif.high < rollx(sif.high,3)
                )
    return signal

def T1_DDX2(sif,sopened=None):
    signal = gand(rollx(sif.close,2) < rollx(sif.close,3)
                ,rollx(sif.close,1) < rollx(sif.close,2)
                ,sif.high > rollx(sif.high)
                ,sif.high < rollx(sif.high,3)
                ,sif.low <= tmin(sif.low,10)
                )
    return signal

def T1_DIIU(sif,sopened=None):
    signal = gand(
                rollx(sif.high,2) < rollx(sif.high,3)
                ,rollx(sif.low,2) > rollx(sif.low,3) 
                ,rollx(sif.high,1) < rollx(sif.high,3)
                ,rollx(sif.low,1) > rollx(sif.low,3) 
                ,sif.close > rollx(sif.high,3)
                )
    return signal

def T1_D4ID(sif,sopened=None):
    signal = gand(
                rollx(sif.high,4) < rollx(sif.high,5)
                ,rollx(sif.low,4) > rollx(sif.low,5) 
                ,rollx(sif.high,3) < rollx(sif.high,5)
                ,rollx(sif.low,3) > rollx(sif.low,5) 
                ,rollx(sif.high,2) < rollx(sif.high,5)
                ,rollx(sif.low,2) > rollx(sif.low,5) 
                ,rollx(sif.high,1) < rollx(sif.high,5)
                ,rollx(sif.low,1) > rollx(sif.low,5) 
                ,sif.close < rollx(sif.low,5)
                )
    return signal

#状态
def S5A(sif):
    return gand(sif.s3<0,
                sif.t120<0,
        )


def S15A(sif):
    return gand(
            sif.t120<0,
            sif.r60<0,
            sif.r13<0,
            sif.s15<0,
            sif.s3<0,
        )

def S15M3(sif):
    return gand(
        sif.t120<0,
        sif.r13<0,
        sif.ma3 < sif.ma13,
        sif.sdiff30x<0,
        sif.sdiff3x<0,
    )

def S15M3B(sif):
    return gand(
            sif.t120<0,
            sif.r30< 0,
            sif.s3<0,
            sif.s5<0,
            sif.ma3<sif.ma13,
        )
    

def S10H1(sif):
    return gand(
            sif.r60<0,
            sif.mtrend>0,
            sif.xstate == 0,
        )            

def S10L1(sif):
    return gand(
            sif.r60>0,
            sif.xstate !=0,
            sif.s1>0,
        )

def S5P3(sif):
    return gand(
            sif.sdiff3x<0,
            sif.s30<0,
            sif.t120<0,
            sif.r60<0,
            sif.r13<0,
        )


    
def S3H10(sif):
    return gand(
            sif.t120<0,
            sif.r60<0,
            sif.ma13<sif.dma,
        )
 
def S1RD(sif):
    return gand(
            sif.r120<0,
            #sif.r30<0,
            sif.r13<0,
        )
    
def S1RU(sif):
    return gand(
            sif.r120>0,
            sif.xtrend>0,
            #sif.close > sif.dma
        )

def S1DVB(sif):
    return gand(
            sif.r60>0,
            sif.r20>0,
            sif.s5>0,
            sif.s3>0,
            sif.xstate>0,
        )
 
def S1UUX(sif):
    return gand(
            sif.r60>0,
            sif.sdma>0,
            sif.s3>0,
        )
    

def S1DUU(sif):
    return gand(
            sif.r60>0,
            sif.sdma>0,
            sif.s1>0,
            sif.xtrend>0,
        )        

def S1DDUUD(sif):
    return gand(
            sif.t120<0,
        )

def S1UUD(sif):
    return gand(
            sif.r30<0,
            sif.r120<0,
        )

def S1DDD(sif):
    return gand(
            sif.r60 < 0,
            sif.r120<0,
            strend2(sif.ma60)<0,
            sif.sdma<0,
        )
        
def S1DDD1(sif):
    return gand(
            sif.r120<0,
            sif.r60<0,
            sif.r13<0,
            sif.s30<0,
        )


def S1DDX(sif):
    return gand(
            sif.r30<0,
            sif.r60<0,
            sif.t120<0,
            strend2(sif.ma30)<0,
            sif.s1<0,
        )
 
def S1DDX2(sif):
    return gand(
            sif.r60<0,
            sif.t120<0,
        )
    
def S1DIIU(sif):
    return gand(
            sif.r120 > 0,
            sif.ma3 > sif.ma13,
            strend2(sif.ma30)>0,
        )
def S1D4ID(sif):
    return gand(
            sif.t120<0,
            sif.s30<0,
        )


#波动过滤

def W5A(sif):
    return gand(
                sif.xatr30x <10000,
                #strend2(sif.mxatr)<0,
            )

def W5A2(sif):
    return gand(
                sif.xatr30x <10000,
                strend2(sif.mxatr)<0,
            )

def W15M3(sif):
    return gand(
            sif.xatr < 2500,
            sif.xatr30x < 10000,
            strend2(sif.mxatr)>0,
            sif.xatr<sif.mxatr,
            #strend2(sif.mxatr30x)<0,   #添加这个条件之后，效果太好以至于不敢使用
        )

def W15M3B(sif):
    return gand(
            strend2(sif.mxatr)>0,
            strend2(sif.mxatr30x)<0,
            sif.xatr < 2500,
            sif.xatr30x < 10000,
        )

def W10H1(sif):
    return gand(
            sif.xatr<1500,
            sif.xatr30x < 10000,
            sif.xatr30x < sif.mxatr30x,
            strend2(sif.mxatr30x)<0,
        )
 
def W10L1(sif):
    return gand(
            sif.xatr30x < 6000,
            strend2(sif.mxatr30x)>0,
        )
    

def W3H10(sif):
    return gand(
            sif.xatr < 2000,
            sif.xatr > sif.mxatr,
            sif.xatr30x < sif.mxatr30x,
        )

def W1DVB(sif):
    return gand(
            strend2(sif.mxatr)<0,
            sif.xatr<sif.mxatr,
            sif.xatr < 1500,
            sif.xatr30x<12000,
        )            

def W1UUX(sif):
    return gand(
            strend2(sif.mxatr)>0,
            sif.xatr > 1200,
            sif.xatr30x < 12000,
        )

def W1DUU(sif):
    return gand(
            sif.xatr > sif.mxatr,
            sif.xatr > 1200,
        )
    
def W1DDUUD(sif):
    return gand(
            sif.xatr30x < sif.mxatr30x,
            strend2(sif.mxatr30x)<0,
            sif.xatr < sif.mxatr,
            sif.xatr > 1200,
        )

def W1UUD(sif):
    return gand(
            sif.xatr > sif.mxatr,
            sif.xatr30x < 6000,
            sif.xatr < 900,
        )

def W1DDD(sif):
    return gand(
            sif.xatr30x < 12000,
            sif.xatr > 1500,
            sif.xatr30x < sif.mxatr30x,
        )

def W1DDD1(sif):
    return gand(
            strend2(sif.mxatr30x)<0,
            sif.xatr < 1500,
        )
 
def W1DDX(sif):
    return gand(
            sif.xatr < 1800,
            sif.xatr30x < 10000,
            strend2(sif.mxatr)<0,
        )
        
def W1DIIU(sif):
    return gand(
            sif.xatr30x < sif.mxatr30x,
            sif.xatr > sif.mxatr,
            sif.xatr < 1500,
            sif.mxatr30x < 12000,
        )
        

k3_d3 = SXFuncD1(fstate=followD44,fsignal=k3d3,fwave=downW2,ffilter=n1430filter)  #无好设置

k5_d3 = SXFuncD1(fstate=S5A,fsignal=k5d3,fwave=W5A,ffilter=n1430filter) #回撤比较大

k5_d3b = SXFuncD1(fstate=S5A,fsignal=k5d3,fwave=W5A2,ffilter=n1430filter)

K15_H1 = SXFunc(fstate=S15A,fsignal=T15_H1,fwave=ZC,ffilter=nfilter)   #顺势的交易
K15_M3 = SXFuncA(fstate=S15M3,fsignal=T15_M3,fwave=W15M3,ffilter=nfilter) #
K15_M3B = SXFuncA(fstate=S15M3B,fsignal=T15_M3B,fwave=W15M3B,ffilter=nfilter) #


K10_H1 = SXFuncF1(fstate=S10H1,fsignal=T10_H1,fwave=W10H1,ffilter=e1430filter) #单个看有点用处，回撤太大，不用

K10_L1 = BXFuncF1(fstate=S10L1,fsignal=T10_L1,fwave=W10L1,ffilter=efilter)   #顺势的交易

K5_P3 = SXFuncF1(fstate=S5P3,fsignal=T5_P3,fwave=ZD,ffilter=n1430filter)

K3_H10 = SXFuncF1(fstate=S3H10,fsignal=T3_H10,fwave=W3H10,ffilter=exfilter) #进入候选

K1_RD = SXFuncF1(fstate=S1RD,fsignal=T1_RD,fwave=nx2000,ffilter=efilter2)   #顺势的交易
K1_RU = BXFuncF1(fstate=S1RU,fsignal=T1_RU,fwave=nx2000,ffilter=efilter2)   #顺势的交易

K1_DVB  = BXFuncF1(fstate=S1DVB,fsignal=T1_DVB,fwave=W1DVB,ffilter=efilter2)   #顺势的交易
K1_UUX  = BXFuncF1(fstate=S1UUX,fsignal=T1_UUX,fwave=W1UUX,ffilter=efilter)   #顺势的交易
K1_DUU  = BXFuncF1(fstate=S1DUU,fsignal=T1_DUU,fwave=W1DUU,ffilter=efilter)   #顺势的交易
K1_DIIU  = BXFuncF1(fstate=S1DIIU,fsignal=T1_DIIU,fwave=W1DIIU,ffilter=n1430filter)   #顺势的交易


K1_DDUUD  = SXFuncF1(fstate=S1DDUUD,fsignal=T1_DDUUD,fwave=W1DDUUD,ffilter=efilter)   #顺势的交易,样本数=10
K1_DDD  = SXFuncF1(fstate=S1DDD,fsignal=T1_DDD,fwave=W1DDD,ffilter=efilter)   #顺势的交易,样本数=14
K1_D4ID = SXFuncF1(fstate=S1D4ID,fsignal=T1_D4ID,fwave=nx2000,ffilter=e1430filter)   #顺势的交易,样本数=12,合并无作用


K1_DDD1  = SXFuncD1(fstate=S1DDD1,fsignal=T1_DDD,fwave=W1DDD1,ffilter=e1430filter)   #顺势交易,样本数较多,但合并效果不好
K1_DDX  = SXFuncF1(fstate=S1DDX,fsignal=T1_DDX,fwave=W1DDX,ffilter=e1430filter2)   #顺势的交易,样本数较多,合并有反作用
K1_DDX2  = SXFuncF1(fstate=S1DDX2,fsignal=T1_DDX2,fwave=ZF,ffilter=e1430filter)   #顺势的交易,合并有反作用


K1_UUD  = SXFuncF1(fstate=S1UUD,fsignal=T1_UUD,fwave=W1UUD,ffilter=efilter2)   #顺势的交易,样本数=10

def TX(sif,sopened=None):
    signal = gand(
                rollx(sif.high,4) < rollx(sif.high,5)
                ,rollx(sif.low,4) > rollx(sif.low,5) 
                ,rollx(sif.high,3) < rollx(sif.high,5)
                ,rollx(sif.low,3) > rollx(sif.low,5) 
                ,rollx(sif.high,2) < rollx(sif.high,5)
                ,rollx(sif.low,2) > rollx(sif.low,5) 
                ,rollx(sif.high,1) < rollx(sif.high,5)
                ,rollx(sif.low,1) > rollx(sif.low,5) 
                ,sif.close < rollx(sif.low,5)
                )
    signal = gand(signal,
                sif.t120<0,
                sif.s30<0,
                sif.xatr<2000,
            )

    return signal

K1_TX = SXFuncF1(fstate=gofilter,fsignal=TX,fwave=gofilter,ffilter=n1430filter)



ks_15_x = CSFuncF1(u'K15顺势空头组合',K15_H1,K15_M3,K15_M3B)
ks_15_c = [K15_H1,K15_M3,K15_M3B]

ks_5_x = CSFuncF1(u'低阶K顺势空头组合',K5_P3,K1_RD)
ks_5_c = [K5_P3,K1_RD]

k1b_x = CBFuncF1(u'K1顺势多头组合',K1_RU,K1_DVB,K1_UUX)
k1b_c = [K1_RU,K1_DVB,K1_UUX,K1_DUU,K1_DIIU]#,K1_TX]

#k1b_y = CBFuncF1(u'K1顺势多头组合',K1_UUX,K1_DUU)
#k1b_d = [K1_UUX,K1_DUU]

k1s_x = CSFuncF1(u'K1顺势空头组合',K1_UUD,K1_DDD)#,K1_D4ID)#,K1_TX)
k1s_c = [K1_UUD,K1_DDD,K1_D4ID]

k1s_x2 = CSFuncF1(u'K1顺势空头组合',K1_DDD,K1_DDD1,K1_DDX)#,K1_TX)  #合并有反作用
k1s_c2 = [K1_DDD,K1_DDD1,K1_DDX]


xxx_k = [k3_d3,k5_d3b,ks_15_x,K10_L1,ks_5_x,k1s_x] + k1b_c
xxx_k_candidate = [k3_d3,k5_d3,K15_H1,K15_M3,
        K15_M3B,K5_P3,K3_H10,K1_RD,K1_RU,K1_DUU,K1_DVB,K1_UUX,K1_DDUUD,K1_UUD,K1_DDD,K1_DDD1,K1_DIIU,K1_D4ID]

#逆势
#信号
def T15_120h(sif):
    #不在震荡市中
    ma15_30 = ma(sif.close15,30)
    signal15 = gand(sif.high15>rollx(sif.high15)
                ,sif.low15>rollx(sif.low15)
                ,sif.high15 == tmax(sif.high15,8)   #半日新高
                ,strend2(ma15_30)>0,
                )

    delay = 15

    bline = dnext_cover(np.select([signal15>0],[sif.low15],[0]),sif.close,sif.i_cof15,delay)
    
    signal = sif.close < bline
    return signal    


def T15_M(sif,sopened=None):
    '''
        15分钟新高后,15分钟内1分钟跌破前15分钟的开盘价(收盘价的低者)/最低价
    '''
    ma15_60 = ma(sif.close15,60) 
    ma15_30 = ma(sif.close15,30) 
    ma15_3 = ma(sif.close15,3)         
    
    signal15 = gand(
                sif.low15>rollx(sif.low15)
                ,sif.high15 - gmax(sif.open15,sif.close15) > np.abs(sif.open15-sif.close15) #上影线长于实体
                ,sif.high15 == tmax(sif.high15,6)
                ,sif.high15 > gmax(ma15_3,ma15_30,ma15_60)
                ,strend2(sif.diff15x-sif.dea15x)>0
                )

    delay = 15


    bline15 = gmin(sif.open15,sif.close15)
    bline = dnext_cover(np.select([signal15>0],[bline15],[0]),sif.close,sif.i_cof15,delay)

    signal = sif.close < bline
    return signal

def T15_H5(sif,sopened=None):
    '''
        15分钟调整模式
            创新高后7分钟内跌回，并且rsi下叉
        其中主条件是下叉时，跌破该15分钟的最低线            
    '''
    
    signal15 = gand(sif.high15 == tmax(sif.high15,5)
                )

    delay = 15

    bline15 = sif.low15
    bline = dnext_cover(np.select([signal15>0],[bline15],[0]),sif.close,sif.i_cof15,delay)

    rsia = sif.rsi7 
    rsib = sif.rsi19 

    signal = gand(sif.low < bline
                ,cross(rsib,rsia)<0
                ,strend2(rsia)<0
                )
    return signal

def T5_H36(sif,sopened=None):
    '''
        顶部衰竭模式
    '''
 
    signal5 = gand(
                rollx(sif.high5) == tmax(sif.high5,36) #上周期是顶点
             )

    delay = 4

    bline5 = gmin(sif.open5,sif.close5) #sif.low5
    bline = dnext_cover(np.select([signal5>0],[bline5],[0]),sif.close,sif.i_cof5,delay)

    signal = sif.close < bline #-100
    return signal

def T3_L12(sif,sopened=None):
    signal3 = gand(rollx(sif.low3) == tmin(sif.low3,12),
                   sif.close3 >= rollx(sif.high3,2), 
                   rollx(sif.high3)<rollx(sif.high3,2)  #不是马上扑回的. 令见k3_u_b
                )

    signal = dnext_cover(signal3,sif.close,sif.i_cof3,1)
    return signal


#状态
def AS15A(sif):
    return gand(
            sif.r120 > 0,
            sif.r30 > 0,
            sif.xstate >0,
        )

def AS15A2(sif):
    return gand(
            sif.xstate >0,
        )

def AS15M(sif):
    return gand(
            #sif.strend<0,
            sif.r13<0,
            sif.r120>0,
            sif.r60>0,
          )
    
def AS15H5(sif):
    return gand(
            sif.ma5 < sif.ma13,
            sif.r120>0,
        )


def AS3L12(sif):
    return gand(
          sif.close < sif.dma,
          sif.xstate < 0,
        )

def AS5H36(sif):
    return gand(
            strend2(sif.ma13)<0,
            sif.s5<0,
            sif.s1<0,
            sif.r60 > 0,
        )

            

#波动过滤
def W15A(sif):
    return gand(
            #sif.xatr > sif.mxatr,
            sif.mxatr > rollx(sif.mxatr,270),
            sif.xatr30x < 10000,
            #sif.xatr30x < sif.mxatr30x
        )

def W15A2(sif): #ZA
    return gand(
            sif.xatr < 2000,
            sif.xatr30x < sif.mxatr30x,
        )


def W15M(sif):
    return gand(
            sif.xatr < 2000,
            sif.xatr30x < 12000,
          )

def W15H5(sif):
    return gand(
            sif.xatr > sif.mxatr,
            sif.xatr > 800,
        )

def W3L12(sif):
    return gand(
             sif.xatr < sif.mxatr,
             #sif.xatr > 800,
             #strend2(sif.mxatr)>0,
             #strend2(sif.mxatr30x)>0,
        )
 

FA_15_120 = SXFunc(fstate=AS15A,fsignal=T15_120h,fwave=W15A,ffilter=n1430filter)
FA_15_120B = SXFunc(fstate=AS15A2,fsignal=T15_120h,fwave=ZA,ffilter=nfilter)


FA_15_M = SXFuncA(fstate=AS15M,fsignal=T15_M,fwave=gofilter,ffilter=nfilter) 
FA_15_H5 = SXFuncA(fstate=AS15H5,fsignal=T15_H5,fwave=W15H5,ffilter=efilter)    #样本数太少

FA_5_H36 = SXFuncD1(fstate=AS5H36,fsignal=T5_H36,fwave=ZA,ffilter=nfilter)

FA_3_L12 = BXFunc(fstate=AS3L12,fsignal=T3_L12,fwave=ZE,ffilter=nfilter)

FA_15_120_C = [FA_15_120,FA_15_120B]


#逆势同周期同方向每天只做一次
FA_S_X = CFuncD1(u'FA15集合',FA_15_120,FA_15_120B,FA_15_M,FA_5_H36)


xxx_against = [FA_S_X,FA_3_L12]

xxx_against_candidate = [FA_15_120,FA_15_120B,FA_15_M,FA_5_H36,FA_S_X,FA_3_L12]


for x in xxx_against:
    x.ftype = TAGAINST


#需要选定专门找1430后的策略

xxx = xxx_break+xxx_orb + xxx_k + xxx_against + xxx_index
xxx_candidate = xxx_break_candidate + xxx_orb_candidate + xxx_k_candidate + xxx_against_candidate + xxx_index_candidate

xxx2 = xxx


for x in xxx+xxx_candidate:
    #x.stop_closer = iftrade.atr5_uxstop_k0 #40/60
    #x.stop_closer = iftrade.atr5_uxstop_kC #60/60   
    #x.stop_closer = iftrade.atr5_uxstop_kD #60/80       
    x.stop_closer = iftrade.atr5_uxstop_kF #60/120       
    #x.stop_closer = iftrade.atr5_uxstop_k60 #60/90
    #x.stop_closer = iftrade.atr5_uxstop_k90 #60/90
    #x.stop_closer = iftrade.atr5_uxstop_k120 #60/20
    x.cstoper = iftrade.F60  #初始止损,目前只在动态显示时用
