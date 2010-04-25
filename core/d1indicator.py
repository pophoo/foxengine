# -*-coding:utf-8 -*-

#一维向量指标的计算(包括原common和rwarms)
#注意，四舍五入只有在整数的时候才能用 v + d45来表示(d45>0)

import numpy as np

from wolfox.fengine.core.d1 import BASE,gand,gmax,greater,subd,rollx,roll0,nsubd
from wolfox.fengine.core.d1ex import tmax,tmin,trend,msum,ma

import logging
logger = logging.getLogger('wolfox.fengine.core.d1indicator')

#serial = np.arange(10000)   #不超过10000个数据点

#expfunctor = lambda cur,expma,trate,base=BASE: (cur*trate + expma * (base-trate) + base/2)/base
def expma(source,trate):    
    ''' 指数移动平均线
        trate为今日数据在计算中所占的比重,以1/1000(1/BASE)为基数
    '''
    length = (2* BASE+trate/2)/trate -1
    #print 'trate:',trate,'length;',length
    rev = np.zeros_like(source)
    if(len(source) < length):
        return rev
    cur = source[0]
    for i in xrange(1,length-1):
        cur = (source[i] * trate + cur * (BASE - trate) + BASE/2)/BASE    
        #cur = expfunctor(source[i],cur,trate)
    for i in xrange(length-1,len(source)):
        cur = (source[i] * trate + cur * (BASE - trate)+ BASE/2)/BASE     
        #cur = expfunctor(source[i],cur,trate)
        rev[i] = cur
        #assert cur >= 0
    return rev

def cexpma(source,n):
    '''国内使用的expma,直接用n作为参数
    '''
    return expma(source,(2*BASE+(n+1)/2)/(n+1))

def vexpma(source,trate):    
    ''' 指数移动平均线, 为大数据而设
        trate为今日数据在计算中所占的比重,以1/1000(1/BASE)为基数
    '''

    length = (2* BASE+trate/2)/trate -1
    #print 'trate:',trate,'length;',length
    rev = np.zeros_like(source)
    if(len(source) < length):
        return rev
    cur = source[0]
    for i in xrange(1,length-1):
        cur = (source[i] + BASE/2)/BASE * trate + (cur+BASE/2)/BASE*(BASE - trate)
        #cur = expfunctor(source[i],cur,trate)
    for i in xrange(length-1,len(source)):
        cur = (source[i] + BASE/2)/BASE * trate + (cur+BASE/2)/BASE * (BASE - trate)     #1L防止计算中溢出
        #cur = expfunctor(source[i],cur,trate)
        rev[i] = cur
        assert cur >= 0
    return rev

def vcexpma(source,n):
    '''国内使用的expma,直接用n作为参数,为大数据而设
    '''
    return vexpma(source,(2*BASE+(n+1)/2)/(n+1))

def macd(source,ifast=150,islow=75,isignal=200):
    ''' 按照经典定义，MACD=EXPMA(1500)-EXPMA(750)
        信号线为 EXPMA(2000)
        此时，周期分别为:  fast = 12,slow = 26,signal = 9 
        返回diff,signal(dea)
    '''
    fast = expma(source,ifast)
    slow = expma(source,islow)
    diff = fast - slow
    signal = expma(diff,isignal)
    return diff,signal

def cmacd(source,ifast=12,islow=26,idiff=9):
    ''' 国内常用的算法
        1.指数平均用cexpma来计算,周期取fast=12,slow=26,diff的指数平均周期取9
        2.信号线用dif的指数平均来计算
    '''
    fast = cexpma(source,ifast)
    slow = cexpma(source,islow)
    diff = fast - slow
    dea = cexpma(diff,idiff)
    return diff,dea


def score(sprice,svolume):
    ''' 对当日进行评分
        按照价格变化和成交量变化打分
        价格上升    量上升  2分
                    否则    1分
        价格下降    量上升  -2分
                    否则    -1分
        价格平      0分
    '''
    fprice = np.sign(subd(sprice))
    fvolume = np.choose(subd(svolume) > 0,[1,2])
    return fprice * fvolume


def score2(sprice,svolume):
    si = subd(sprice) * BASE / rollx(sprice)
    fprice = np.select([si>5,si<-5],[1,-1],default=0)
    fvolume = np.choose(subd(svolume) > 0,[1,2])
    return fprice * fvolume


##用于updownlimit/d的比较函数和计算函数表
functor_map = {'down':(lambda x,y : x > y , lambda peak,factor,d45 : (peak * BASE + d45) / factor )
        ,'up':(lambda x,y : x < y , lambda peak,factor,d45 : (peak *  factor + d45) / BASE )
        }

def updownlimit(source,signal,threshold,cmp_functor,calc_functor): 
    ''' 信号日起的上下限计算
        signal序列以>0为有信号
        threshold以1/BASE为单位
        不错位
    '''
    assert len(source) == len(signal)
    rev = np.zeros_like(source)
    if(len(source) == 0):
        return rev
    peak = source[0]
    factor = BASE + threshold
    d45 = factor / 2 
    for i in xrange(len(source)):
        cv = source[i]
        if signal[i] != 0 or not cmp_functor(peak,cv):
            peak = cv
        rev[i] = calc_functor(peak,factor,d45)
    return rev

def downlimit(source,signal,threshold=60): 
    ''' 下限 
        注意，下限是 smax_value * BASE/(BASE + threshold)的四舍五入值
        而不是直接减去千分之threshold
        相当于下限值需要涨千分之threshold才能到达最高值
    '''
    return updownlimit(source,signal,threshold,*functor_map['down'])

def uplimit(source,signal,threshold=60): 
    ''' 上限 '''
    return updownlimit(source,signal,threshold,*functor_map['up'])

def tupdownlimit(source,signal,threshold,cmp_functor,calc_functor):
    ''' 跟踪型上下限
        信号signal日起根据source算定上下限,跟踪首次出现
        在source本身穿越下限之后，后面的信号日才起作用，穿越之前的信号日被屏蔽
        理论上存在漏洞，可能会导致因为下限太高，买入日就卖出的情形。但可忽略不计(太近买入或未调整完毕)，相当于防弹
        返回下限序列
    '''
    assert len(source) == len(signal)
    rev = np.zeros_like(source)
    if(len(source) == 0):
        return rev
    factor = BASE + threshold
    d45 = factor / 2 
    state = 0   #屏蔽状态标志,0未屏蔽,1屏蔽
    peak = source[0]
    for i in xrange(len(source)):
        cv = source[i]
        if(signal[i] > 0 and state == 0):
            peak = cv
            state = 1
        else:
            peak = peak if cmp_functor(peak,cv) else cv  #source[i]>0
        result = calc_functor(peak,factor,d45)
        if(cmp_functor(result,cv)): #如果是当日破，其state无法在当日表现出来.需要表现么？暂且不必
            state = 0
        rev[i] = result
    return rev

def tdownlimit(source,signal,threshold=60): 
    ''' 跟踪型下限 '''
    return tupdownlimit(source,signal,threshold,*functor_map['down'])

def tuplimit(source,signal,threshold=60): 
    ''' 跟踪型上限 '''
    return tupdownlimit(source,signal,threshold,*functor_map['up'])

def stoplimit(source,signal,satr,times): 
    ''' 信号日起的下限计算
        signal序列以>0为有信号
    '''
    assert len(source) == len(signal)
    rev = np.zeros_like(source)
    if(len(source) == 0):
        return rev
    cur_stop = 0
    for i in xrange(len(source)):
        if signal[i] > 0:
            cur_stop = source[i] - satr[i] * times/BASE
        rev[i] = cur_stop
    return rev

def tracelimit_old(source,sup,signal,satr,stop_times,trace_times):
    ''' 信号日起的追踪止损。自有信号起至下一个信号间以max值-atr*trace_times和买入值-atr*stop_times的高者为止损线
        source:买入价
        sup:上包线，为high或close
        signal:>0为有信号
        satr:atr线
        stop_times为止损时的atr倍数
        trace_times为跟踪的atr倍数
    '''
    assert len(source) == len(sup) == len(signal) == len(satr)
    rev = np.zeros_like(source)
    if(len(source) == 0):
        return rev
    cur_stop = 0
    cur_max = 0
    cur_trace = 0
    for i in xrange(len(source)):
        cur = source[i]
        cur_h = sup[i]
        cur_atr = satr[i]
        if signal[i] > 0:
            cur_max = cur   #以买入点而非当日高点，因为不能判断当日高点是否是买入之后
            cur_stop = cur - cur_atr * stop_times/BASE
        elif cur_max < cur_h:
            cur_max = cur_h
        cur_trace = cur_max - cur_atr * trace_times/BASE
        if cur_stop < cur_trace:
            cur_stop = cur_trace
        rev[i] = cur_stop
    return rev

def tracelimit(source,sup,sdown,signal,satr,stop_times,trace_times):
    ''' 信号日起的追踪止损。
        自有信号起至下一个信号间以当前值-atr*trace_times的最高者和买入值-atr*stop_times的高者为止损线
            但若至下一个信号日时仍未触发，则下一个信号日不作为止损重置的信号.
            避免之前出现的因为信号连续而导致的止损不停抬高，或者两个买入之间没有卖出间隔，导致后一买入信号引起止损的迅速提高
        source:首日估价。这个估价不是买入价，通常是开盘价+最低价/2。不能用收盘价，否则开盘最低到收盘涨停，同样会触发止损，而开盘涨停到收盘跌停，却不会触发
               用开盘价，则只有跌下去的时候会触发。 
        sup:上包线，为high或close
        sdown: 触发线，若触发线<计算所得的limit，则说明已经卖出. 建议用(close+low)/2
        signal:>0为有信号
        satr:atr线
        stop_times为止损时的atr倍数
        trace_times为跟踪的atr倍数
        避免原始的tracelimit因为从高点下来小阴小阳调整而触发的止损(atr变小)
    '''
    assert len(source) == len(sup) == len(signal) == len(satr)
    rev = np.zeros_like(source)
    if(len(source) == 0):
        return rev
    cur_stop = 0
    cur_trace = 0
    hold = False   #空仓
    for i in xrange(len(source)):
        cur = source[i]
        cur_h = sup[i]
        cur_atr = satr[i]
        if signal[i] > 0 and not hold:
            #print signal[i],hold
            cur_stop = cur - cur_atr * stop_times/BASE
            cur_h = cur #高点设为当前点，因为无法判断真正高点是否是在当前点之后出现
            hold = True
        cur_trace = cur_h - cur_atr * trace_times/BASE  #有可能最高点-当时atr*ttimes < 当前点-当前atr*ttimes
        if cur_stop < cur_trace:
            cur_stop = cur_trace
        #print i,hold,sdown[i],cur_stop
        if hold and sdown[i] < cur_stop:    #只有持仓时才判断. 只有低于才算卖出
            hold = False
            #print 'selled,hold=',hold,'cur_stop=',cur_stop
        rev[i] = cur_stop
    return rev


def tracelimit_090528(source,sup,signal,satr,stop_times,trace_times):
    ''' 信号日起的追踪止损。自有信号起至下一个信号间以当前值-atr*trace_times的最高者和买入值-atr*stop_times的高者为止损线
        source:首日估价。这个估价不是买入价，通常是开盘价+最低价/2。不能用收盘价，否则开盘最低到收盘涨停，同样会触发止损，而开盘涨停到收盘跌停，却不会触发
               用开盘价，则只有跌下去的时候会触发。 
        sup:上包线，为high或close
        signal:>0为有信号
        satr:atr线
        stop_times为止损时的atr倍数
        trace_times为跟踪的atr倍数
        避免原始的tracelimit因为从高点下来小阴小阳调整而触发的止损(atr变小)
    '''
    assert len(source) == len(sup) == len(signal) == len(satr)
    rev = np.zeros_like(source)
    if(len(source) == 0):
        return rev
    cur_stop = 0
    cur_trace = 0
    for i in xrange(len(source)):
        cur = source[i]
        cur_h = sup[i]
        cur_atr = satr[i]
        if signal[i] > 0:
            cur_stop = cur - cur_atr * stop_times/BASE
            cur_h = cur #高点设为当前点，因为无法判断真正高点是否是在当前点之后出现
        cur_trace = cur_h - cur_atr * trace_times/BASE  #有可能最高点-当时atr*ttimes < 当前点-当前atr*ttimes
        if cur_stop < cur_trace:
            cur_stop = cur_trace
        rev[i] = cur_stop
    return rev

def tracelimit_r(source,sup,signal,satr,stop_times,trace_times,proportion=400):
    ''' 信号日起的追踪止损。
            自有信号起至下一个信号间以
                当前值-atr*trace_times的最高者
                买入值-atr*stop_times + (当前值-买入值)的最高者 * proportion / 1000
                
        source:首日估价。这个估价不是买入价，通常是开盘价+最低价/2。不能用收盘价，否则开盘最低到收盘涨停，同样会触发止损，而开盘涨停到收盘跌停，却不会触发
               用开盘价，则只有跌下去的时候会触发。 
        sup:上包线，为high或close
        signal:>0为有信号
        satr:atr线
        stop_times为止损时的atr倍数
        trace_times为跟踪的atr倍数
        proportion为千分位的比例
        按默认参数计算，效果比trace_limit差很多
    '''
    assert len(source) == len(sup) == len(signal) == len(satr)
    rev = np.zeros_like(source)
    if(len(source) == 0):
        return rev
    s_stop = 0
    cur_stop = 0
    cur_trace = 0
    cur_max = 0
    s_src = 0
    for i in xrange(len(source)):
        cur = source[i]
        cur_h = sup[i]
        cur_atr = satr[i]
        if signal[i] > 0:
            s_stop = cur - cur_atr * stop_times/BASE
            cur_stop = s_stop
            s_src = cur_h = cur #高点设为当前点，因为无法判断真正高点是否是在当前点之后出现
            cur_max = cur_h
        elif cur_max < cur_h:   #signal[i]==0
            cur_max = cur_h
        cur_trace = cur_h - cur_atr * trace_times/BASE
        cur_r = s_stop + (cur_max - s_src) * proportion / BASE
        if cur_stop < cur_trace:
            cur_stop = cur_trace
        if cur_stop < cur_r:
            cur_stop = cur_r
        rev[i] = cur_stop
    return rev

def tracemax(source,signal):
    ''' 信号日间的最大值追踪
    '''
    assert len(source) == len(signal)
    rev = np.zeros_like(source)
    cur_max = 0
    for i in xrange(len(source)):
        cur = source[i]
        if signal[i] > 0:
            cur_max = cur
        elif cur_max < cur:
            cur_max = cur
        rev[i] = cur_max
    return rev

def zigzag(source,threshold):#source[i]不能为0. 因为用到了 and . or 选择判断中
    ''' 摆动滤波 Arthur Merrill，求折点(根据折点之前的数据求得转折限，若当日数据突破该限，则转折成立)
        threshold以1/BASE为单位
        注意：这里是否使用当日数据并不重要，如果使用当日数据且其起作用时，必然是新高，所以必然不会破
            但是，从boundary的角度来看，应当不使用当日数据，否则，如果取最低价跌破boundary为卖出信号，
  		    则只要当日创新高且收盘价-最低价超过threshold，就会触发信号
  		    同时，折点本身并没有时效性（最后一折无法计算），所以不是信号，无需遵循指标信号约定
        如果划线(根据折点拉直得到中间点的数据)则需要用到未来数据，但是这里只求折点，不需未来数据
        故该指标名字不需前缀X
        上折点为1，下折点为-1
        返回折点序列和边界序列
    '''
    length = 3 ##两点不成转折，三点才有可能转折,因此数据从第三点开始
    points,boundary = np.zeros_like(source),np.zeros_like(source)
    if(len(source) < length):
        return points,boundary
    factor = BASE + threshold
    d45d,d45u = factor / 2,BASE / 2    #d45d/d45f分别为下限/上限的四舍五入值
    state = 1 if source[1] > source[0] else -1 #1:UP/2:DOWN
    peak = source[1]
    for i in xrange(length-1,len(source)):
        cv = source[i]
        if(state == 1):#上行过程
            limit = (peak * BASE + d45d)/ factor
            if(cv < limit):  #下翻转
                state,peak = -1,cv   #必然是新低
                points[i] = -1
            else:
                if cv > peak:
                    peak = cv 
                points[i] = 0
        else:#下行过程
            limit = (peak * factor + d45u) / BASE
            if(cv > limit): #上翻转
                state,peak = 1,cv
                points[i] = 1
            elif cv < peak:
                peak =  cv
        boundary[i] = limit
    return points,boundary

def wms(tclose,thigh,tlow,length):
    ''' 威廉指标
        可单独使用，同时也被kdj用到
    '''
    assert len(tclose) == len(thigh) and len(tclose) == len(tlow)
    lmax = tmax(thigh,length)
    lmin = tmin(tlow,length)
    rev = np.zeros_like(tclose)
    for i in xrange(len(tclose)):
        cmax,cmin = lmax[i],lmin[i]
        rev[i] = BASE if cmax==cmin else (tclose[i]-cmin) * BASE/(cmax-cmin)
    return rev   

def kdj(tclose,thigh,tlow,rsv=None,length=9,factor=3):
    '''KDJ
        N日RSV=[(Ct-Ln)/(Hn-Ln)] ×100
        今日K值=2/3×昨日K值+1/3×今日RSV
        今日D值=2/3×昨日D值+1/3×今日K值
        J=3D-2K=D+2(D-K)
    '''
    assert len(tclose) == len(thigh) and len(tclose) == len(tlow)
    assert rsv == None or len(rsv) == len(tclose)
    if(rsv == None):
        rsv = wms(tclose,thigh,tlow,length)
    k,d,j = np.zeros_like(tclose),np.zeros_like(tclose),np.zeros_like(tclose)
    d45 = factor/2
    curk,curd = 500,500
    for i in xrange(len(tclose)):
        curk = (rsv[i] + curk*(factor-1) + d45) /factor
        curd = (curk + curd*(factor-1) + d45) /factor
        curj = curd + (factor-1)*(curd-curk)
        k[i],d[i],j[i] = curk,curd,curj
    return k,d,j

def ckdj(tclose,thigh,tlow,rsv=None,length=9,factor=3):
    '''
        国内钱龙等的计算公式,J=3K-2D
    '''
    assert len(tclose) == len(thigh) and len(tclose) == len(tlow)
    assert rsv == None or len(rsv) == len(tclose)
    if(rsv == None):
        rsv = wms(tclose,thigh,tlow,length)
    k,d,j = np.zeros_like(tclose),np.zeros_like(tclose),np.zeros_like(tclose)
    d45 = factor/2
    curk,curd = 500,500
    for i in xrange(len(tclose)):
        curk = (rsv[i] + curk*(factor-1) + d45) /factor
        curd = (curk + curd*(factor-1) + d45) /factor
        curj = curk + (factor-1)*(curk-curd)
        k[i],d[i],j[i] = curk,curd,curj
    return k,d,j

def obv(tclose,tvolume):
    return np.cumsum(trend(tclose) * tvolume)

def obv_old(signal,energy):
    ''' OBV
        obv[n] = obv[n-1] + energy[i]    (signal[i] > signal[i-1])
        obv[n-1] - energy[i]    (signal[i] < signal[i-1])
    计算方式可以通过指标组合得到：
        #accumulate(mul(trend(close),volume))    
        np.cumsum(trend(close) * volume)
    '''
    assert len(signal) == len(energy)
    rev = np.zeros_like(signal)
    sum = 0
    pre = signal[0]
    for i in xrange(1,len(signal)):
        cur = signal[i]
        if(cur > pre):
            sum += energy[i]
        elif(cur < pre):
            sum -= energy[i]
        rev[i] = sum
        pre = cur
    return rev

def roc(source,interval=1):
    assert interval > 0
    rev = np.zeros_like(source)
    if(len(source) < interval + 1): #是第interval+1个才能有值
        return rev
    for i in xrange(interval,len(source)):
        cv,ci = source[i],source[i-interval]
        if(ci == 0):
            rev[i] = 0
        else:
            rev[i] = (cv - ci) * BASE / ci / interval
    return rev

def pvt(signal,energy): 
    ''' PVT
        pvt[n] = pvt[n-1] + energy[n] * (signal[n]-signal[n-1]) /signal[n-1]
    计算方式可以通过指标组合得到(但有四舍五入顺序上的区别，导致两种方法的结果有较大误差)：
        np.cumsum(roc(close) * volume)) 
    '''
    assert len(signal) == len(energy)
    rev = np.zeros_like(signal)
    sum = 0
    pre = signal[0]
    for i in xrange(1,len(signal)):
        cur = signal[i]
        sum += BASE * (cur - pre)*energy[i] / pre   #不用四舍五入，全部舍出。以免复杂
        rev[i] = sum
        pre = cur
    return rev

def rsi(source,length):
    rev = np.zeros_like(source)
    if(len(source) < length+1): #因为引用了前一天的值，所以第一个rsi值必须在length+1那一天[length]才能产生
        return rev
    upsum,downsum = 0,0
    pre = source[0]
    for i in xrange(1,length): #计算upsum,downsum的初值 
        cur = source[i]
        if(cur >= pre):
            upsum += cur - pre
        else:
            downsum += pre - cur
        pre = cur
    for i in xrange(length,len(source)):
        cur = source[i]
        if(cur >= pre):
            upsum += cur - pre
        else:
            downsum += pre - cur
        if(upsum == downsum):
            rev[i] = BASE/2
        else:
            rev[i] = BASE * upsum/(upsum + downsum)
        il1,il = source[i-length+1],source[i-length]
        if(il1 >= il):
            upsum -= il1 - il
        else:
            downsum -= il - il1
        pre = cur
    return rev

def dm(shigh,slow):
    ''' 动向计算
        通达信公式
            HD :=HIGH-REF(HIGH,1);
            LD :=REF(LOW,1)-LOW;
            DMP:=EXPMEMA(IF(HD>0&&HD>LD,HD,0),N);
            DMM:=EXPMEMA(IF(LD>0&&LD>HD,LD,0),N);
            这里取消了N的EXP
    '''
    tpdm = subd(shigh)
    tndm = -subd(slow)
    pdm = np.select([gand(tpdm>0,tpdm>tndm)],[tpdm],default=0)
    ndm = np.select([gand(tndm>0,tndm>tpdm)],[tndm],default=0)
    return pdm,ndm

def di(pdm,ndm,xtr,length=14):
    ''' 方向计算, pdm:正动向, ndm:负动向，xtr:真实波幅，length:平滑系数
        通达信公式
            DMP:=EXPMEMA(IF(HD>0&&HD>LD,HD,0),N);
            DMM:=EXPMEMA(IF(LD>0&&LD>HD,LD,0),N);
            PDI: DMP*100/TR;
            MDI: DMM*100/TR;
    '''
    mxtr = cexpma(xtr,length)
    pdi = cexpma(pdm,length)*10000/mxtr
    ndi = cexpma(ndm,length)*10000/mxtr
    return pdi,ndi

def xadx(pdi,ndi,length=6):
    ''' 动向平均数计算
        通达信公式
            ADX: EXPMEMA(ABS(MDI-PDI)/(MDI+PDI)*100,M);
    '''
    return cexpma(np.abs(pdi-ndi)*10000/(pdi+ndi),length)

def adx(sclose,shigh,slow,n=14,m=6):
    ''' 直接根据sclose,shigh,slow计算adx的快捷函数
        n: 计算di时的平滑天数
        m: 计算adx时的平滑天数
    '''
    pdm,ndm = dm(shigh,slow)
    xtr = tr(sclose,shigh,slow)
    pdi,ndi = di(pdm,ndm,xtr,n)
    return xadx(pdi,ndi,m)

def tr(sclose,shigh,slow):
    ''' 真实波幅
    '''
    sclose = rollx(sclose)
    shl = np.abs(shigh - slow)
    shc = np.abs(shigh - sclose)
    slc = np.abs(slow - sclose)
    return gmax(shl,shc,slc)

def atr(sclose,shigh,slow,length=20):
    return cexpma(tr(sclose,shigh,slow),length)

def atr2(sclose,shigh,slow,length=20):
    return ma(tr(sclose,shigh,slow),length)

def asi(sopen,sclose,shigh,slow):
    '''
        1.A=∣当天最高价-前一天收盘价∣
        B=∣当天最低价-前一天收盘价∣
        C=∣当天最高价-前一天最低价∣
        D=∣前一天收盘价-前一天开盘价∣
        2.比较A、B、C三数值：若A最大，R＝A＋1／2B＋1／4D；若B最大，R＝B＋1／2A十1／4D；若C最大，R=C＋1/4D
        3.  E=当天收盘价-前一天收盘价
            F=当天收盘价-当天开盘价
            G=前一天收盘价-前一天开盘价
        4.X＝E＋1／2F＋G
        5.K=A、B之间的最大值
        6.L＝3；SI=50*X／R*K／L；ASI=累计每日之SI值
    1.ASI指标大部分时机都是和股价走势同步的，投资者仅能从众多股票中寻找少数产生领先突破的个股。若ASI指标领先股价，提早突破前次ASI高点或低点，则次一日之后的股价必然能突破前次高点或低点。
    2.股价由上往下，欲穿越前一波低点的密集支撑区时，于接近低点处，尚未确定股价是否会跌破支撑之际，如果ASI领先股价，提早一步，跌破相对股价的前一波ASI低点，则次一日之后，股价将随后跌破低点支撑区。投资人可以早一步卖出股票，减少不必要的损失。
    3.股价由下往上，欲穿越前一波的高点套牢区时，于接近高点处，尚未确定股价能否顺利穿越之际，如果ASI领先股价，提早一步，通过相对股价的前一波ASI低点，则次一日之后，股价必然能够顺利突破高点套牢区。股民可以把握ASI的领先作用，提前买入股票。
    4.股价走势一波比一波高，而ASI却未相对创新高点形成“顶背离”时，应卖出；股价走势一波比一波低，而ASI却未相对创新低点形成“底背离”时，应买进。
    5.ASI指标和OBV指标同样维持“N”字型的波动，并且也以突破或跌破“N”字型高低点，为观察ASI指标的主要方法。向上爬升的ASI，一旦向下跌破其前一次显著的N型转折点，一律可视为停损卖出的讯号；向下滑落的ASI，一旦向上突破其前一次的N型转折点，一律可视为果断买进的讯号。
    #这些使用很难度量，所以其实asi只能在肉眼使用    
    '''
    a = np.abs(shigh - roll0(sclose))
    b = np.abs(slow - roll0(sclose))
    c = np.abs(shigh - roll0(slow))
    e = subd(sclose)
    f = sclose-sopen
    g = roll0(f)
    d = np.abs(g)
    l = 3
    
    x = e + f/2 + g
    k = np.choose(a>b,[b,a])   #True=1,False=0,因此a>b时True=1
    
    m = np.select([(a>b) & (b>c),(b>c) & (b>a),(c>a) & (c>b)],[a,b,c])
    r = np.select([m==a,m==b,m==c],[a+b/2+d/4,b+a/2+d/4,c+d/4])
    si = 50 * x / r * k / l    
    return si.cumsum()

def uplines(*args):
    ''' args[0]...args[-1]各个序列多头排列，其中args[0]为最快速线
    '''
    trends = [ trend(s)>0 for s in args ]
    sdiff = np.diff(args,axis=0)
    sdiff0 = [ s<0 for s in sdiff]
    strend = gand(*trends)
    return gand(strend,*sdiff0)

def efficient_rate(source,covered=10):
    ''' 效率函数. 来源: smarter trading (略有不同，书中效率值为abs值，而此函数以负表示下降效率)
        根据单一source计算(存在其他方式的效率计算方法，但在此如此计算)
        先计算n日内每日波动幅度amplitude = abs(source[i]-source[i-1])，然后根据n求和为s_amplitude
        然后计算n日总波幅t_amplitude = source[i]-source[i-n]
        当日效率系数 = t_amplitude / s_amplitude
        第covered+1个数据(下标为covered)开始有效，之前的全部置0
        效率值有正有负，为负表明是下降效率
    '''
    assert covered > 0
    if(len(source) <= covered):
        return np.zeros_like(source)
    sdiff = np.abs(subd(source))
    ssum = msum(sdiff,covered)
    sdiffc = subd(source,covered)
    rev = sdiffc * BASE / ssum
    rev[:covered] = 0
    return rev

def ama_maker(covered=10,dfast=2,dslow=30):
    fastest = 2 * BASE / (dfast+1)
    slowest = 2 * BASE / (dslow+1)
    diff = fastest - slowest
    base2 = BASE * BASE
    def ama(source):
        ''' 自适应移动平均线. 来源: smarter trading
            测试数据：  6063,6041,6065,6078,6114,6121,6106,6101,6166,6169,6195,6222,6186,6214,6185
                        0,0,0,0,0,0,0,0,0,0,6173.9,6188.8,6188.4,6192.4,6192.0
        '''
        rev = np.zeros_like(source)
        if(len(source) <= covered):
            return rev
        ers = np.abs(efficient_rate(source,covered))  #使用正的效率值
        smooth = ers * diff/BASE + slowest
        #print ers,mul(smooth,smooth),fastest,slowest
        cbase = BASE
        preama = source[covered-1] * cbase  #初始值为该日原始信号,乘以100是为了提升计算精度
        for i in xrange(covered,len(source)):
            vsm,vse = smooth[i],source[i]
            ama = preama + (vsm *1.0* vsm * (vse*cbase - preama) + base2/2) / base2
            rev[i] = int((ama + cbase/2)/cbase) #对实际结果仍然取整为所需精度
            preama = ama
        return rev
    return ama

def psy(source,length=12):
    ''' 心理线PSY:COUNT(CLOSE>REF(CLOSE,1),N)/N*100
    '''
    s = greater(source,rollx(source))
    rev = (msum(s,length) * BASE + length/2)/ length
    return rev

### emv族及vap族为Richard W. Arms发明的算法,以及改进 
def emv(shigh,slow,sweight):#经典emv算法,sweight即为成交量(权重)
    assert len(shigh) == len(sweight) == len(sweight)
    if(len(shigh)<1):
        return np.array([])
    mid_diff = subd((shigh + slow) / 2,1)
    box = shigh - slow
    swb = np.cast['int64'](sweight) *  BASE
    md_b2 = np.cast['int64'](mid_diff) * BASE * BASE
    ratio = np.where(box>0,swb/box,swb*10)  #box不可能小于0
    rev = np.where(ratio>0,md_b2/ratio,md_b2*10)
    rev[0] = 0
    return np.cast['int32'](rev)

def emv_old(shigh,slow,sweight):#经典emv算法,sweight即为成交量(权重),为迭代算法，而非numpy性质
    assert len(shigh) == len(sweight) == len(sweight)
    rev = np.zeros_like(shigh)
    if(len(shigh)<1):
        return rev
    premid = (shigh[0] + slow[0]) /2
    for i in xrange(1,len(shigh)):   #除0都当作除0.1，即*10
        csh,csl,csw = shigh[i],slow[i],sweight[i]
        mid = (csh + csl) /2
        box = csh - csl
        ratio = box > 0 and csw * BASE / box or csw * BASE * 10 #除数为0当作0.1
        rev[i] = ratio > 0 and (mid-premid)*BASE*BASE / ratio or (mid-premid)*BASE*BASE * 10  #除数为0当作0.1
        #print (mid-premid),box,ratio,rev[i]
        premid = mid
    return rev        

def semv(shigh,slow,sweight,length=13):#标准化后的emv算法,length为均线长度,sweight即为成交量(权重)
    '''
    标准化后的波动难易度
        mid = (max + min)/2
        mid_rate = (mid(n) - mid(n-1)) / mid(n) * BASE
        svolume_rate = svolume(n)/MA(svolume,length) * BASE
        wave_rate = (max-min)/ma(max-min,length) * BASE
        box_rate = svolume_rate / wave_rate
        semv = mid_rate / box_rate    
    '''
    assert len(shigh) == len(sweight) == len(sweight)
    if(len(shigh)<length):
        return np.zeros_like(shigh)
    wma = np.roll(ma(sweight,length),1)
    dma = np.roll(ma(shigh - slow,length),1)
    mid = (shigh + slow)/2
    mid_diff = subd(mid,1)
    mid_rate = np.cast['int64'](mid_diff) * BASE * BASE / mid
    swb = np.cast['int64'](sweight) * BASE
    swr = np.where(wma,swb/wma,swb*10)
    ssb = (shigh-slow)*BASE
    wr = np.where(dma,ssb/dma,ssb*10)   #dma必然大于等于0，等于0时相当于乘10
    rev = np.where(swr>0,mid_rate * wr/swr,mid_rate*wr*10)
    rev[:length] = 0
    return np.cast['int32'](rev)        

def semv_old(shigh,slow,sweight,length=13):#标准化后的emv算法,length为均线长度,sweight即为成交量(权重),迭代算法
    '''
    标准化后的波动难易度
        mid = (max + min)/2
        mid_rate = (mid(n) - mid(n-1)) / mid(n) * BASE
        svolume_rate = svolume(n)/MA(svolume,length) * BASE
        wave_rate = (max-min)/ma(max-min,length) * BASE
        box_rate = svolume_rate / wave_rate
        semv = mid_rate / box_rate    
    未检查是否溢出
    '''
    assert len(shigh) == len(sweight) == len(sweight)
    rev = np.zeros_like(shigh)
    if(len(shigh)<length):
        return rev
    wma = ma(sweight,length)
    dma = ma(shigh - slow,length)
    premid = (shigh[length-1] + slow[length-1]) /2
    for i in xrange(length,len(shigh)):   #除0都当作除0.1，即*10
        csh,csl,csw = shigh[i],slow[i],sweight[i]
        pwm,pdm = wma[i-1],dma[i-1]
        mid = (csh + csl) /2
        mid_rate = (mid-premid) * BASE * BASE / mid
        sweight_rate = pwm > 0 and csw * BASE/pwm or csw * BASE * 10 #除数为0当作0.1
        wave_rate = pdm > 0 and (csh-csl)*BASE/pdm or (csh-csl)*BASE * 10
        rev[i] = sweight_rate > 0 and mid_rate*wave_rate/sweight_rate or mid_rate*wave_rate * 10  #除数为0当作0.1
        #print premid,mid,mid_rate,sweight_rate,wave_rate
        premid = mid
    return rev        

def vap(svolume,sprice,base):
    ''' 成交量调整的价格曲线Volume Adjusted Price Line
        返回经成交量调整的价格序列，以及该序列发生的时间
        原理：
        1	base为成交量单位
        2   依次计算每一日的交易对应的成交量单位数
            每一个单位，在adjustedPrice中添加当日价格，在svolume2Date中添加当日序号
            余数不足一个单位的，按一个单位计算(做多多计区间大小个单位)
        3   对adjustedPrice进行任意操作，最后用transform将相应的成交量坐标映射回date
    这个算法对新股和次新股效果可能较差，因为头几天的成交量实在太大
    '''
    #print len(svolume),len(sprice),base    
    assert len(svolume) == len(sprice) and base > 0
    stimes = np.ones(len(svolume),int)    #默认都是1
    for i in xrange(len(svolume)):
        times = (svolume[i] + base - 1)/base
        stimes[i] = times
    return _fill_price(sprice,stimes)

def vap2(svolume,sprice,base):
    ''' 成交量调整的价格曲线Volume Adjusted Price Line2
        返回经成交量调整的价格序列，以及该序列发生的时间
        原理：(与原VAP略有不同为每日无法整除时余数下移
        1	base为成交量单位
        2   依次计算每一日的交易对应的成交量单位数
            每一个单位，在adjustedPrice中添加当日价格，在svolume2Date中添加当日序号
            余数不足一个单位的，切到下一日
        3   对adjustedPrice进行任意操作，最后用transform将相应的成交量坐标映射回date
    这个算法对新股和次新股效果可能较差，因为头几天的成交量实在太大
    '''
    #print len(svolume),len(sprice)
    assert len(svolume) == len(sprice) and base > 0
    stimes = np.zeros(len(svolume),int)  #默认都是0
    cur,remainder = 0,0
    for i in xrange(len(svolume)):
        cs = svolume[i]
        times = (cs+remainder) / base
        remainder = (cs+remainder) % base
        stimes[i] = times
    return _fill_price(sprice,stimes)

DEFAULT_UNIT = 5000
def vap_pre(svolume,sprice,pre_length,weight=5):   
    ''' 依赖svolume为整数序列，否则导致ma之后0值有非零的base，直接导致后续所有计算出错
        weight为权数，unit单位为pre_length的平均数再除以weight. unit的粒度越细，一致性越好
    '''
    if(len(svolume) < pre_length or pre_length == 0):
        pre_length = len(svolume)
    unit = np.sum(svolume[:pre_length]) / pre_length / weight
    if unit == 0:
        unit = DEFAULT_UNIT
    return vap(svolume,sprice,unit)

def vap2_pre(svolume,sprice,pre_length,weight=5):  
    ''' 依赖svolume为整数序列，否则导致ma之后0值有非零的base，直接导致后续所有计算出错
        weight为权数，unit单位为pre_length的平均数再除以weight. unit的粒度越细，一致性越好
    '''
    if(len(svolume) < pre_length or pre_length == 0):
        pre_length = len(svolume)
    unit = np.sum(svolume[:pre_length]) / pre_length / weight
    if unit == 0:
        unit = DEFAULT_UNIT
    return vap2(svolume,sprice,unit)

def svap(svolume,sprice,sbase):
    ''' 成交量调整的价格曲线Volume Adjusted Price Line
        返回经成交量调整的价格序列，以及该序列发生的时间
        原理：
        1	sbase为成交量单位序列，这个序列只可能在开头处有连续的0，一旦出现非零值，之后就不能再有非零值
            如果sbase为0,则相应的times被计为1(最小情况)
        2   依次计算每一日的交易对应的成交量单位数
            每一个单位，在adjustedPrice中添加当日价格，在svolume2Date中添加当日序号
            余数不足一个单位的，按一个单位计算(做多多计区间大小个单位)
        3   对adjustedPrice进行任意操作，最后用transform将相应的成交量坐标映射回date
    这个算法对新股和次新股效果可能较差，因为头几天的成交量实在太大
    '''
    assert len(svolume) == len(sprice) == len(sbase)
    firsti = _find_first_nonzero_index(sbase)
    if(firsti == -1):   #判断是否是全部是0的状况
        return np.array([]),np.array([])
    stimes = np.ones(len(svolume),int)    #默认全部是1
    for i in xrange(firsti,len(svolume)):
        csv,csb = svolume[i],sbase[i]
        #if csb < 0:
        #    print 'csb<0 :',csb
        times = (csv + csb - 1)/csb if csb else 1   #避免被零除，一旦被零除，因为csv/csb本身是numpy内部类型，会导致生成的结果类型有内存泄漏问题
        stimes[i] = times
    return _fill_price(sprice,stimes)

def svap2(svolume,sprice,sbase):
    ''' 成交量调整的价格曲线Volume Adjusted Price Line2
        返回经成交量调整的价格序列，以及该序列发生的时间
        原理：(与原VAP略有不同为每日无法整除时余数下移
        1	sbase为成交量单位序列，这个序列只可能在开头处有连续的0，一旦出现非零值，之后就不能再有非零值
            如果sbase为0,则相应的times被计为0(最小情况并抛弃余数)
        2   依次计算每一日的交易对应的成交量单位数
            每一个单位，在adjustedPrice中添加当日价格，在svolume2Date中添加当日序号
            余数不足一个单位的，切到下一日
        3   对adjustedPrice进行任意操作，最后用transform将相应的成交量坐标映射回date
    这个算法对新股和次新股效果可能较差，因为头几天的成交量实在太大
    '''
    assert len(svolume) == len(sprice) == len(sbase)
    firsti = _find_first_nonzero_index(sbase)
    if(firsti == -1):   #判断是否是全部是0的状况
        return np.array([]),np.array([])
    stimes = np.zeros(len(svolume),int)    #默认全部是0,因为除不尽的移下
    cur,remainder = 0,0
    for i in xrange(firsti,len(svolume)):
        csv = svolume[i]
        csb = sbase[i]
        if csb: #避免被0除
            times = (csv+remainder) / csb
            remainder = (csv+remainder) % csb
        else:   #必然是csv=csb=0
            times = 0
            assert csv == csb
        stimes[i] = times
    return _fill_price(sprice,stimes)

def svap_ma(svolume,sprice,malength,weight=5):   
    ''' 依赖svolume为整数序列，否则导致ma之后0值有非零的base，直接导致后续所有计算出错
        weight为权数，unit单位ma再除以weight. unit的粒度越细，一致性越好
    '''
    return svap(svolume,sprice,rollx(ma(svolume,malength)/weight))

def svap2_ma(svolume,sprice,malength,weight=5):  
    ''' 依赖svolume为整数序列，否则导致ma之后0值有非零的base，直接导致后续所有计算出错
        weight为权数，unit单位ma再除以weight. unit的粒度越细，一致性越好
    '''
    return svap2(svolume,sprice,rollx(ma(svolume,malength)/weight))

def index2v(signal,v2index,length):
    ''' 变形运算
        以v2index中的value为index，将signal中的相应信号转换为长度为length的序列中
        按照vap族的算法，v2index中的v都是排序的
        signal中的信号在返回值中都变成1
        另有dlex中的transform，区别在于保留signal信号的原值，同时不要求v2index排序
    '''
    assert len(signal) == len(v2index) and max(v2index) < length    #v2index中的value不能大于length,否则越界
    rev = np.zeros(length,int)
    t = v2index.compress(signal)
    rev[t] = 1
    return rev

def _fill_price(sprice,stimes):
    length = sum(stimes)
    #print length,stimes
    rev,v2index = np.zeros(length,int),np.zeros(length,int)
    cur = 0
    for i in xrange(len(stimes)):
        p = sprice[i]
        cst = stimes[i]
        for j in xrange(cur,cur + cst):
            rev[j] = p
            v2index[j] = i
        cur += cst
    return rev,v2index

def _find_first_nonzero_index(slist):
    length = len(slist)
    i = 0
    while(i < length and slist[i] == 0):
        i += 1
    if(i == length):
        return -1
    return i
