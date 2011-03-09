# -*-coding:utf-8 -*-
'''
用到的指标/计算的集合
来自core/d1,d1ex,d1indiactor, 是np版本的list化版

其中 XXX为序列运算版本(list). XXX的参照对象是numpy的运算版本(用于回测)
     XXX1为即时运算版本(计算最后一个值)
        XXX1的函数的最后一个顺序参数都是target, 即要计算的值的已有序列. 其最后一个值会在函数中被设置
    序列函数/动态函数中必须妥善处理输入序列比较短或为空的情况
'''


CBASE = 1000 #整数运算的放大倍数

def cexpma(source,n): 
    ''' 计算cexpma序列
        国内使用的expma,直接用n作为参数
        内部用整数计算
        用于整数的source,有四舍五入因子(n+1)/2. 因此不能传入浮点数，会因为该因子而导致数据变化
    '''
    #rev = np.zeros_like(source)
    rev = [0] * len(source)
    if len(source) == 0:
        return rev
    
    cur = source[0]
    for i in xrange(0,len(source)):
        cur = (source[i]*2 + cur*(n-1) + (n+1)/2)/(n+1) 
        rev[i] = cur
    return rev


def cexpma1(source,n,target): 
    ''' 计算最新值
        其中target[:-2]是已经计算的结果
        用于整数的source,有四舍五入因子(n+1)/2. 因此不能传入浮点数，会因为该因子而导致数据变化
    '''
    assert len(source) == len(target),u'源序列与目标序列长度不相等,%s:%s' % (len(source),len(target))
    if(len(source) < 2):
        return 0  
    target[-1] = (source[-1]*2 + target[-2] *(n-1) + (n+1)/2)/(n+1) 
    return target[-1]

def tr(sclose,shigh,slow):
    ''' 真实波幅. 结果被放大CBASE倍
        sclose = rollx(sclose)
        shl = np.abs(shigh - slow)
        shc = np.abs(shigh - sclose)
        slc = np.abs(slow - sclose)
        return gmax(shl,shc,slc)
    '''
    if(len(sclose) < 1):
        return []
    sclose = [sclose[0]] + sclose[:-1]
    shl = [abs(sh-sl) * CBASE for sh,sl in zip(shigh,slow)]
    shc = [abs(sh-sc) * CBASE for sh,sc in zip(shigh,sclose)]
    slc = [abs(sl-sc) * CBASE for sl,sc in zip(slow,sclose)]
    return [max(hl,hc,lc) for hl,hc,lc in zip(shl,shc,slc)]

def tr1(sclose,shigh,slow,target):
    assert len(sclose) == len(target),u'源序列与目标序列长度不相等,%s:%s' % (len(sclose),len(target))
    if(len(sclose) < 2):
        return 0
    hl = abs(shigh[-1] - slow[-1]) * CBASE
    hc = abs(shigh[-1] - sclose[-2]) * CBASE
    lc = abs(slow[-1] - sclose[-2]) * CBASE
    target[-1] = max(hl,hc,lc)
    return target[-1]

def atr(ltr,length=20):
    return cexpma(ltr,length)

def atr1(ltr,target,length=20):
    if len(ltr)<1:
        return 0
    assert len(ltr) == len(target),u'源序列与目标序列长度不相等,%s:%s' % (len(ltr),len(target))
    cexpma1(ltr,length,target)
    return target[-1]
 
def xatr(latr,sclose):
    return [ia * CBASE * CBASE / ic for ia,ic in zip(latr,sclose)]

def xatr1(latr,sclose,lxatr):
    if len(latr)<1:
        return 0
    assert len(latr) == len(sclose) == len(lxatr),u'源序列与目标序列长度不相等,%s:%s' % (len(latr),len(target))
    lxatr[-1] = latr[-1] * CBASE * CBASE / sclose[-1]
    return lxatr[-1]

def accumulate(source):
    if(len(source) < 1):
        return []
    rev = [0] * len(source)
    rev[0] = source[0]
    for i in range(len(source)):
        rev[i] = rev[i-1] + source[i]
    return rev

def accumulate1(source,target):
    assert len(source) == len(target),u'源序列与目标序列长度不相等,%s:%s' % (len(source),len(target))
    if(len(source) < 1):
        return 0
    if(len(source) == 1):
        target[-1] = source[-1]
    else:
        target[-1] = target[-2] + source[-1]
    return target[-1]

def ma(source,length):
    """ 计算移动平均线
        @param source 源数组
        @param length 均线跨度
        @return 移动平均序列
    """
    slen = len(source)
    rev = [0] * slen
    if slen < length:
        return rev
    
    pps = length/2 #用于整数四舍五入尾数

    acc = [0] + accumulate(source)
    rev = [0]*(length-1) + [((sl-sf)+pps)/length for sl,sf in zip(acc[length:],acc[:slen-length+1])]

    return rev

def ma1(source,length,target):
    if len(source)<1:
        return 0
    assert len(source) == len(target),u'源序列与目标序列长度不相等,%s:%s' % (len(source),len(target))
    target[-1] = (sum(source[-length:]) + length/2) / length
    return target[-1]

def strend2(source):
    ''' 简单累积趋势2
        与strend相比，上升过程中，平也当作上,下降中平作下
        若当前趋势为上升或0，trend值为n>0
        则新trend值为：
            n+1 当前值 >= pre
            -1  当前值 < pre
        若当前趋势为下降，trend值为n(负数)
        则下一trend值为：
            n-1 当前值 <= pre
            1   当前值 > pre
        0为初始趋势(缺少判断时)
    '''
    rev = [0] * len(source)
    if len(source) == 0:
        return rev
    pre_v = source[0]
    cur = 0
    for i in range(1,len(source)):
        cur_v = source[i]
        if cur_v > pre_v:
            cur = cur + 1 if cur > 0 else 1
        elif cur_v < pre_v:
            cur = cur - 1 if cur < 0 else -1
        else: #curv == pre_v
            cur = cur + 1 if cur >= 0 else cur-1 #最初为0时，也算上升
        rev[i] = cur
        pre_v = cur_v
    return rev    

def strend2_1(source,target):
    assert len(source) == len(target),u'源序列与目标序列长度不相等,%s:%s' % (len(source),len(target))
    if len(source) < 1:
        return 0
    elif len(source) == 1:
        target[0] = 0
        return 0
    cur_v,pre_v = source[-1],source[-2]
    cur = target[-2]
    if cur_v > pre_v:
        target[-1] = cur + 1 if cur > 0 else 1
    elif cur_v < pre_v:
        target[-1] = cur - 1 if cur < 0 else -1
    else: #curv == pre_v
        target[-1] = cur + 1 if cur >= 0 else cur-1 #最初为0时，也算上升
    return target[-1]

###包装类
from base import *
def ATR(data):
    '''
        计算ATR序列
    '''
    data.tr1 = tr(data.m1[ICLOSE],data.m1[IHIGH],data.m1[ILOW])
    data.atr1 = atr(data.tr1,20)
    data.xatr1 = xatr(data.atr1,data.m1[ICLOSE])
    #data.tr3 = tr(data.m3[ICLOSE],data.m3[IHIGH],data.m3[ILOW])
    #data.atr3 = atr(data.tr3,20)
    #data.xatr3 = xatr(data.atr3,data.m3[ICLOSE])
    data.tr5 = tr(data.m5[ICLOSE],data.m5[IHIGH],data.m5[ILOW])
    data.atr5 = atr(data.tr5,20)
    data.xatr5 = xatr(data.atr5,data.m5[ICLOSE])
    #data.tr15 = tr(data.m15[ICLOSE],data.m15[IHIGH],data.m15[ILOW])
    #data.atr15 = atr(data.tr15,20)
    #data.xatr15 = xatr(data.atr15,data.m15[ICLOSE])
    data.tr30 = tr(data.m30[ICLOSE],data.m30[IHIGH],data.m30[ILOW])
    data.atr30 = atr(data.tr30,20)
    data.xatr30 = xatr(data.atr30,data.m30[ICLOSE])
    data.trd1 = tr(data.d1[ICLOSE],data.d1[IHIGH],data.d1[ILOW])
    data.atrd1 = atr(data.trd1,20)
    data.xatrd1 = xatr(data.atrd1,data.d1[ICLOSE])
    
def ATR1(data):
    '''
        动态计算最新ATR
    '''
    if len(data.m1[ICLOSE]) > len(data.tr1):    #1分钟数据
        data.tr1.append(0)
        tr1(data.m1[ICLOSE],data.m1[IHIGH],data.m1[ILOW],data.tr1)
        data.atr1.append(0)
        atr1(data.tr1,data.atr1,20)
        data.xatr1.append(0)
        xatr1(data.atr1,data.m1[ICLOSE],data.xatr1)
    if len(data.m5[ICLOSE]) > len(data.tr5):    #5分钟数据
        data.tr5.append(0)
        tr1(data.m5[ICLOSE],data.m5[IHIGH],data.m5[ILOW],data.tr5)
        data.atr5.append(0)
        atr1(data.tr5,data.atr5,20)
        data.xatr5.append(0)
        xatr1(data.atr5,data.m5[ICLOSE],data.xatr5)
    if len(data.m30[ICLOSE]) > len(data.tr30):    #30分钟数据
        data.tr30.append(0)
        tr1(data.m30[ICLOSE],data.m30[IHIGH],data.m30[ILOW],data.tr30)
        data.atr30.append(0)
        atr1(data.tr30,data.atr30,20)
        data.xatr30.append(0)
        xatr1(data.atr30,data.m30[ICLOSE],data.xatr30)
    if len(data.d1[ICLOSE]) > len(data.trd1):    #d1分钟数据
        data.trd1.append(0)
        tr1(data.d1[ICLOSE],data.d1[IHIGH],data.d1[ILOW],data.trd1)
        data.atrd1.append(0)
        atr1(data.trd1,data.atrd1,20)
        data.xatrd1.append(0)
        xatr1(data.atrd1,data.d1[ICLOSE],data.xatrd1)
    

def STREND(data):
    '''
        计算趋势
    '''
    data.ma30_120 = ma(data.m30[ICLOSE],120)
    data.t120 = strend2(data.ma30_120)

def STREND1(data):
    '''
        动态计算t120的最新值
    '''
    if len(data.m30[ICLOSE]) > len(data.ma30_120):  #需要计算
        data.ma30_120.append(0)
        data.t120.append(0)
        ma1(data.m30[ICLOSE],120,data.ma30_120)
        strend2_1(data.ma30_120,data.t120)

def MA(data):
    '''
        序列计算基本均线, 1分钟的5/7/10/13/20/30/60/120/135/270均线
    '''
    data.ma_1 = ma(data.sclose,1)
    
    data.ma_5 = ma(data.sclose,5)
    #data.ma_7 = ma(data.sclose,7)
    #data.ma_10 = ma(data.sclose,10)
    data.ma_13 = ma(data.sclose,13)
    #data.ma_20 = ma(data.sclose,20)
    data.ma_30 = ma(data.sclose,30)
    data.ma_60 = ma(data.sclose,60)
    data.ma_120 = ma(data.sclose,120)
    #data.ma_135 = ma(data.sclose,135)
    data.ma_270 = ma(data.sclose,270)
 
def MA1(data):
    '''
        动态计算基本均线, 1分钟的5/7/10/13/20/30/60/120/135/270均线
    '''
    print u'before:收盘序列长度:%s,ma5序列长度:%s' % (len(data.sclose),len(data.ma_5))
    data.ma_1.append(0)
    data.ma_5.append(0)
    #data.ma_7.append(0)
    #data.ma_10.append(0)
    data.ma_13.append(0)
    #data.ma_20.append(0)
    data.ma_30.append(0)
    data.ma_60.append(0)
    data.ma_120.append(0)
    #data.ma_135.append(0)    
    data.ma_270.append(0)    
    ma1(data.sclose,1,data.ma_1)    
    ma1(data.sclose,5,data.ma_5)
    #ma1(data.sclose,7,data.ma_7)
    #ma1(data.sclose,10,data.ma_10)
    ma1(data.sclose,13,data.ma_13)
    #ma1(data.sclose,20,data.ma_20)
    ma1(data.sclose,30,data.ma_30)
    ma1(data.sclose,60,data.ma_60)
    ma1(data.sclose,120,data.ma_120)
    #ma1(data.sclose,135,data.ma_135)
    ma1(data.sclose,270,data.ma_270)
    print u'after:收盘序列长度:%s,ma5序列长度:%s' % (len(data.sclose),len(data.ma_5))


