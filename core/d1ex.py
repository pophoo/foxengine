# -*-coding:utf-8 -*-

#一维向量的计算
#v1d的补充

import numpy as np
from collections import deque
from wolfox.fengine.core.d1 import BASE,band,gand,nsubd,rollx,equals,greater_equals

def ma(source,length):    #使用numpy，array更加的惯用法
    """ 计算移动平均线
        @param source 源数组
        @param length 均线跨度
        @return 移动平均序列
    """
    if(len(source) < length):
        return np.zeros(len(source),int);
    
    rev = np.zeros_like(source); ##预先的0,不采用zeros_like是为了避免

    pps = length/2 #用于整数四舍五入尾数

    acc = np.add.accumulate(source)
    rev[length-1] = acc[length-1] #第length个元素是第一个非零值

    np.subtract(acc[length:],acc[:len(acc)-length],rev[length:])
    rev += pps  #这种in place方式要快于 sum = (sum + pps) / length
    rev /= length

    return rev

def nma(source,length):    #自然ma算法，前length个元素为各自的累积和除以累积元素个数
    """ 计算移动平均线
        @param source 源数组
        @param length 均线跨度
        @return 移动平均序列
    """
    
    dividen = np.arange(len(source)) + 1
    dividen[dividen > length] = length

    pps = dividen/2 #用于整数四舍五入尾数

    acc = np.add.accumulate(source)
    rev = nsubd(acc,length)

    rev += pps  #这种in place方式要快于 sum = (sum + pps) / length
    rev /= dividen
    return rev


#简单趋势，1表示向上，-1表示向下
def trend(source):
    return np.concatenate((np.array([0]),np.sign(np.diff(source))))

def strend(source):
    ''' 简单累积趋势
        若当前趋势为上升或0，trend值为n>0
        则新trend值为：
            n+1 当前值 > pre
            n   当前值 = pre
            -1  当前值 < pre
        若当前趋势为下降，trend值为n(负数)
        则下一trend值为：
            n-1 当前值 < pre
            n   当前值 = pre
            1   当前值 > pre
        0为初始趋势(缺少判断时)
    '''
    rev = np.zeros(len(source),int) #可能产生溢出，所以不能用zeros_like
    if len(source) == 0:
        return rev
    pre_v = source[0]
    cur = 0
    for i in xrange(len(source)):
        cur_v = source[i]
        if cur_v > pre_v:
            cur = cur + 1 if cur >= 0 else 1
        elif cur_v < pre_v:
            cur = cur - 1 if cur < 0 else -1
        else:
            pass
        rev[i] = cur
        pre_v = cur_v
    return rev    

def cross(target,follow):
    ''' 交叉计算:   target: 参照系,follow: 追击者
        状态：  1   Follow上叉Target
                0   无交叉状态 
                -1  Follow下叉

        粘合一次后按趋势发散仍然算叉，即追击--追平--超越也算，但追击--追平--平--....--超越不算
        这里不保证Target在上叉(下叉)时的趋势是向上(向下)的
    '''
    assert len(target) == len(follow)
    if(len(target) == 0):
        return target.copy()
    s = np.sign(follow - target)
    diff = np.diff(s)
    flag_a = (np.abs(diff) == 2)  #直接的叉
    diff_1 = np.roll(diff,1)
    sd = diff + diff_1  
    flag_b = (np.abs(sd) == 2)    #粘合一次的叉，特征为 ...1,1,....或...-1,-1,...
    flag = np.logical_or(flag_a,flag_b)
    signal = np.sign(diff)
    s2 = np.zeros_like(diff)
    np.putmask(s2,flag,signal)
    rev = np.concatenate((np.array([0]),s2))
    return rev

def under_cross(signal,source,follow):
    ''' 信号日低于或下叉
        不仅仅给出下叉信号,而且还给出ssource日follow是否低于source
    '''
    sd = equals(cross(source,follow),-1)
    indices = (signal > 0)
    sd[indices] = greater_equals(source[indices],follow[indices])
    return sd

def cover(source,interval=1): #interval必须大于0
    ''' 信号延伸，length为延伸值，发生日为length,逐日递减(小于0则都为0)，直至另一个发生日.
        初始序列中以>0认为是有信号(以免最普通的用法中需要先过滤掉负值)
        假定-1位置无信号发生
        新的信号会增强已有信号        
    '''
    rev = np.zeros_like(source)
    curcover = 0
    for i in xrange(len(source)):
        curcover = interval if source[i] != 0 else curcover-1
        rev[i] = curcover if curcover > 0 else 0
    return rev

def repeat(source,interval=1): #interval必须大于0
    ''' 信号延伸，length为延伸值，发生日为length,逐日递减(小于0则都为0)，直至另一个发生日
        初始序列中以>0认为是有信号(以免最普通的用法中需要先过滤掉负值)
        假定-1位置无信号发生
        覆盖期内的新信号无增强作用
    '''
    rev = np.zeros_like(source)
    curcover = -1
    for i in xrange(len(source)):
        if source[i] and curcover <= 0:
            curcover = interval
        rev[i] = curcover if curcover >= 0 else 0
        curcover -= 1
    return rev

def extend_old(source,interval=1):#interval必须大于0
    ''' 信号延伸，length为延伸值，将发生日及其后的length-1日的值赋值为发生日的值
        源序列中所有非0的数值都是信号
        假定-1位置无信号发生，从0开始如果没有新信号，仍然为0
    '''        
    rev = np.zeros_like(source)
    v,curextend = 0,0
    for i in xrange(len(source)):
        cv = source[i]
        if(cv != 0):
            v,curextend = cv,interval
        else:
            curextend -= 1
        rev[i] = v if curextend > 0 else 0
    return rev

def extend(source,interval=1):#interval必须大于0
    if len(source) == 0:
        return np.array([])
    rev = np.zeros_like(source)
    indices = np.where(source != 0)[0]
    cur=0
    #print indices
    for i in xrange(0,len(indices)):
        index = indices[i]
        rev[cur:cur+interval] = source[cur]
        cur = index
    rev[cur:] = source[cur]
    return rev


def extend2next(source):
    ''' 信号延伸，一直延伸到下一个信号
        >0  正信号
        =0  无信号
        <0  负信号
    '''
    rev = np.zeros_like(source)
    cur = 0
    for i in xrange(len(source)):
        cv = source[i]
        if cv != 0:
            cur = cv
        rev[i] = cur
    return rev

def sresume(source,length=5,covered=1):
    ''' 连续>=length个零随后covered个非零日
    '''
    rev = np.zeros_like(source)
    nzeros = np.where(source != 0)[0]
    sdiff = nsubd(nzeros)
    indice = nzeros[sdiff>=length]
    if len(indice) > 0:
        rlen = len(rev)
        for i in range(covered):
            cur_indice = indice + i
            cur_indice[cur_indice>=rlen] = rlen-1   #防止溢出
            rev[cur_indice] = 1
    return rev

def extend2reverse(source):
    ''' 信号延伸，一直延伸到反向信号
        >0  正信号
        =0  无信号
        <0  负信号
    '''
    rev = np.zeros_like(source)
    cur = 0
    for i in xrange(len(source)):
        cv = source[i]
        #if cv != 0 and cv * cur <= 0:
        if cv != 0 and (( cv > 0 and cur <=0) or (cv<0 and cur >=0)):   #效率上可能高一些?
           cur = cv
        rev[i] = cur
    return rev

def distance(source):
    ''' 信号相对距离，信号日为0，逐日递增，直至另一个信号日
        初始序列中以非0认为是有信号
    '''
    rev = np.zeros(len(source),int) #可能产生溢出，所以不能用zeros_like
    curdistance = 0 #假设前一天为信号发生，因为计算所的的值肯定小于实际距离
    for i in xrange(len(source)):
        curdistance = curdistance+1 if source[i] == 0 else 0 
        rev[i] = curdistance
    return rev

def rsum(source,signal):
    ''' 信号日signal之间的相对累积,signal!=0为有信号'''
    assert len(source) == len(signal)
    rev = np.zeros(len(source),int) #可能产生溢出，所以不能用zeros_like
    sum = 0
    for i in xrange(len(source)):
        if(signal[i] != 0):
            sum = source[i] + 0 #将可能的int8转换为int32,避免溢出
        else:
            sum += source[i] #不能采用 ?? and 0 or ?+1的方式，因为and 0是False常量
        rev[i] = sum
    return rev

def ravg(source,signal):
    ''' 信号日signal之间的相对均值,signal!=0为有信号'''
    assert len(source) == len(signal)
    rev = np.zeros_like(source) #这里不会溢出
    n,sum = 0,0
    for i in xrange(len(source)):
        if(signal[i] != 0):
            sum = source[i] + 0 #将可能的int8转换为int32,避免溢出
            n = 1
        else:
            sum += source[i] #不能采用 ?? and 0 or ?+1的方式，因为and 0是False常量
            n += 1
        rev[i] = (sum + n/2) / n
    return rev

def rsub(source,signal):
    ''' 相邻信号日signal的减法(相当于比较) 
        d(n+1) = src(n+1) -  s(n)
        d(0) = src(0)
    '''
    assert len(source) == len(signal)
    if len(source) == 0:
        return source.copy()
    rev = np.zeros_like(source) #原则上不会溢出,若source的类型是int8时,数字将在+/-5之间
    pre = source[0] 
    for i in xrange(len(source)):
        if(signal[i] != 0):
            cv = source[i]
            rev[i] = cv - pre
            pre = cv
    return rev

def msum(source,length):   
    """ 计算移动累积,前length-1个置0
        @param source 源序列
        @param length 均线跨度
        @return 移动累积序列
    """
    if(len(source) == 0):
        return source.copy()
    acc = np.add.accumulate(source)
    dacc = np.roll(acc,length)
    dacc[:length]=0
    rev = acc - dacc
    rev[:length-1] = 0
    return rev

def msum2(source,length):   
    """ 计算移动累积,前length-1个置为0至当前位置的累积
        @param source 源序列
        @param length 均线跨度
        @return 移动累积序列
    """
    if(len(source) == 0):
        return source.copy()
    acc = np.add.accumulate(source)
    dacc = np.roll(acc,length)
    dacc[:length]=0
    rev = acc - dacc
    rev[:length-1] = acc[:length-1]
    return rev

def l_emaxmin(source,functor):
    ''' 近似新高/新低覆盖，因为两层循环内多次用到索引操作，所以用list来计算，用np.array效率会极低
        以最远的小于当前点的高/低点的覆盖范围(界限为该高/低点对应的低/高点)为起始点
        而实际上，该点和前一高点之间还存在比当前点更低的连续点，这部分被忽略
        所以结果实际上是从某个低点开始的总长度(当前点不计入内)
    '''
    rev = [0] * len(source)
    if(len(source) < 2):
        return rev
    rev[1] = functor(source[1],source[0]) and 1 or -1
    for i in xrange(2,len(source)): #rev[0]=0,rev[1]必须预先设置(因为pre>0作为终止条件)
        pre = i-1
        while(functor(source[i],source[pre]) and pre > 0):
            if(rev[pre] > 0):#继续正向
                rev[i] = i - pre + rev[pre]
                pre = i - rev[i] + rev[i-rev[i]] # i-rev[i]是上一底的为位置，rev[i-rev[i]]是上一底到上一顶的距离
            else:#由逆(或source[0])转正
                rev[i] = 1
                pre = i - (1-rev[pre]) #找到上一高的位置
        else: #第一次检测进入
            if(not functor(source[i],source[i-1])):
                rev[i] = rev[i-1] > 0 and -1 or rev[i-1]-1 #翻转或继续逆向行驶
    return rev

from operator import gt,lt
def emax(source):
    return np.array(l_emaxmin(source.tolist(),gt))

def emin(source):
    return np.array(l_emaxmin(source.tolist(),lt))

def derepeat(source,interval=1):
    ''' 去除间隔期内!=0数值的重复出现，间隔期内新信号被忽略其增强作用
    '''
    rev = np.zeros_like(source)
    cover = 0
    for i in xrange(len(source)):
        cv = source[i]
        if cv and cover <=0:
            rev[i] = cv
            cover = interval
        cover -= 1
    return rev

def decover(source,interval=1):
    ''' 去除间隔期内!=0数值的重复出现，新的信号会增强interval
        去除效率大于derepeatc
    '''
    rev = np.zeros_like(source)
    cover = 0
    for i in xrange(len(source)):
        cv = source[i]
        if(cv != 0):
            if(cover <= 0):
                rev[i] = cv
            cover = interval
        else:
            cover -= 1
    return rev

def derepeatc(source):
    ''' 去除!=0数值的连续出现(只剩下第一个)
        c是consecutive的意思
    '''
    rev = np.zeros_like(source)
    state = 0   #有信号状态
    for i in xrange(len(source)):
        cv = source[i]
        if(cv != 0):
            if(state == 0):
                rev[i] = cv
                state = 1
        else:
            state = 0
    return rev

def sfollow(source1,source2,covered=1):
    ''' 简单追踪共振
        在source1发出信号covered范围内source2是否发出共振信号
        covered < 1 视同1,即为同一天
        两个序列都是!=0为有信号，但都建议>0表示有信号
    '''
    assert len(source1) == len(source2)
    #rev = np.zeros_like(source1)
    extended = extend(source1,covered) if covered>1 else source1
    rev = band(extended,source2)
    #for i in xrange(len(source1)):
    #    if(extended[i] and source2[i]):
    #        rev[i] = 1
    return rev

def syntony(source1,source2,covered = 1):
    ''' 简单共振
        >0为有信号
        source1,source2信号不论先后，在covered天中同时出现，则以匹配日(后个信号出现的那一天)为信号发出日
        covered =1 为同一天发出信号,<1视同为1
        要求source1/source2的元素在本序列内部都是同号的(但source1,source2可以不同号)
        注意：source1,source2非0为有信号
        注意2:  bor(sfollow(x,y,n),sfollow(y,x,n)) != syntony(x,y,n)
                因为sfollow类型的只有在follow的当日发出信号，而syntony在信号发出的n-diff(diff等于follow和源的时间差)天内都有信号
    '''
    s1 = msum2(source1,covered)
    s2 = msum2(source2,covered)
    return np.sign(np.logical_and(s1,s2))   #将True/False转为显式的0/1

def _iargsparse(idefault,*args):  
    ''' 对n-1个序列+一个整数的参数数组进行解析，返回序列和整数值    '''
    if(isinstance(args[-1],int)):
        ivalue = args[-1]
        seqs = args[:-1]
    else:
        ivalue = idefault
        seqs = args
    return seqs,ivalue

def gsyntony(*args):
    ''' 简单共振的多参数版本
        为保持接口的一致性，如果args[-1]为整数，则为covered参数，否则covered=1. 其余的args都是序列 
        args中的序列信号不论先后，在covered天中同时出现，则以匹配日(后个信号出现的那一天)为信号发出日
        covered =1 为同一天发出信号,<1视同为1
        要求args的元素在本序列内部都是同号的(但args之间可以不同号)
        注意：args各序列非零为有信号
    '''
    assert len(args) >= 2
    sources,covered = _iargsparse(1,*args)
    ss = [msum2(s,covered) for s in sources]
    return gand(*ss)

def consecutive(source,value=1):
    ''' 计算序列source中value的连续出现次数
    '''
    rev = np.zeros(len(source),int)
    cur = 0
    for i in xrange(len(source)):
        if(source[i] == value):
            cur += 1
            rev[i] = cur
        else:
            cur = 0
            #rev[i]默认值就是0
    return rev

def swing(source,covered=1):    #波动幅度
    return swing2(source,source,covered)

def swing2(shigh,slow,covered=1):   #已知高低序列的波动幅度
    vmax = tmax(shigh,covered)
    vmin = tmin(slow,covered)
    vdiff = vmax - vmin
    return vdiff*BASE/vmin

def iswing(source,covered=1):   #计算序列的波动幅度，以及高低点离当前点的远近差(正数表示高点近,负数表示低点近)
    return iswing2(source,source,covered)

def iswing2(shigh,slow,covered=1):   #计算高低序列的波动幅度，以及高低点离当前点的远近差(正数表示高点近[即曾经上升],负数表示低点近[即曾经下降])
    vmax,imax = ti_max(shigh,covered)
    vmin,imin = ti_min(slow,covered)
    vdiff = vmax - vmin
    return vdiff*BASE/vmin,imax-imin

def gswing(*args):  #多参数波动幅度，最后一个参数可以为covered值，默认为1
    sources,covered = _iargsparse(1,*args)
    d2 = np.array(sources)
    vmax = tmax(np.max(d2,0),covered)
    vmin = tmin(np.min(d2,0),covered)
    vdiff = vmax - vmin
    return vdiff*BASE/vmin

def giswing(*args):  #多参数波动幅度以及高低点离当前点的远近差，最后一个参数可以为covered值，默认为1
    sources,covered = _iargsparse(1,*args)
    d2 = np.array(sources)
    vmax,imax = ti_max(np.max(d2,0),covered)
    vmin,imin = ti_min(np.min(d2,0),covered)
    #print vmax,imax
    #print vmin,imin
    vdiff = vmax - vmin
    return vdiff*BASE/vmin,imax-imin

def left_fill(source,empty=0):#使用左值补全源序列中为empty的点.直接操作源序列.
    pre = 0
    for i in xrange(len(source)):
        cv = source[i]
        if(cv):
            pre = cv
        else:
            source[i] = pre
    return source

def zavg(source):#求所有非零值的平均数
    sum,count = 0,0
    for v in source:
        if(v != 0):
            sum += v
            count +=1
    if(count == 0):
        return 0
    return (sum+count/2)/count

def tmaxmin(source,covered,functor,gfunctor,limit): #最近len个数据的max值
    tm = limit
    rev = np.zeros_like(source)
    length = len(source)
    prelen = length > covered and covered or length
    for i in range(prelen):
        tm = functor(tm,source[i])
        rev[i] = tm
    buffer = deque([v for v in source[:prelen]])   #优化方法，避免vquit=source[i-covered]的方式，对nbarray的直接索引有严重的性能问题
    for i in range(prelen,length):
        v = source[i]
        buffer.append(v)
        vquit=buffer.popleft()
        tm = functor(tm,v)
        if tm == vquit and v != tm: #退出的正好是最大值,计算前covered-1个元素的最大值, pre=source[i-1]
            tm = gfunctor(source[i-covered+1:i+1])
        rev[i] = tm
    return rev

def tmax(source,covered): #最近len个数据的max值
    ''' 等同于
        tmaxmin(source,covered,max,np.max,-99999999)
        是其展开版本
    '''
    tm = -99999999
    rev = np.zeros_like(source)
    length = len(source)
    prelen = length > covered and covered or length
    for i in range(prelen):
        v = source[i]
        if tm < v:
            tm = v
        rev[i] = tm
    buffer = deque([v for v in source[:prelen]])   #优化方法，避免vquit=source[i-covered]的方式，对nbarray的直接索引有严重的性能问题
    for i in range(prelen,length):
        v = source[i]
        buffer.append(v)
        vquit=buffer.popleft()
        if tm < v:
            tm = v
        if tm == vquit and v != tm: #退出的正好是最大值,计算前covered-1个元素的最大值, pre=source[i-1]
            tm = np.max(source[i-covered+1:i+1])
        rev[i] = tm
    return rev

def tmin(source,covered): #最近len个数据的max值
    ''' 等同于
        tmaxmin(source,covered,min,np.min,99999999)
        是其展开版本
    '''
    tm = 99999999
    rev = np.zeros_like(source)
    length = len(source)
    prelen = length > covered and covered or length
    for i in range(prelen):
        v = source[i]
        if tm > v:
            tm = v
        rev[i] = tm
    buffer = deque([v for v in source[:prelen]])   #优化方法，避免vquit=source[i-covered]的方式，对nbarray的直接索引有严重的性能问题
    for i in range(prelen,length):
        v = source[i]
        buffer.append(v)
        vquit=buffer.popleft()
        if tm > v:
            tm = v
        if tm == vquit and v != tm: #退出的正好是最大值,计算前covered-1个元素的最大值, pre=source[i-1]
            tm = np.min(source[i-covered+1:i+1])
        rev[i] = tm
    return rev

def ti_max(source,covered): #最近len个数据的max值及这些max值的坐标
    tm = -99999999
    im = 0
    rev = np.zeros_like(source)
    irev = np.zeros_like(source)
    length = len(source)
    prelen = length > covered and covered or length
    for i in range(prelen):
        v = source[i]
        if tm <= v: #以最近的那个最大值位置为准
            tm = v
            im = i
        rev[i] = tm
        irev[i] = im
    buffer = deque([v for v in source[:prelen]])   #优化方法，避免vquit=source[i-covered]的方式，对nbarray的直接索引有严重的性能问题
    for i in range(prelen,length):
        v = source[i]
        buffer.append(v)
        vquit=buffer.popleft()
        if tm <= v:  #以最近的那个最大值位置为准
            #print tm,v
            tm = v
            im = i
        if tm == vquit and v != tm: #退出的正好是最大值,计算前covered-1个元素的最大值, pre=source[i-1]
            tm = np.max(source[i-covered+1:i+1])
            im = i - np.argmax(source[i:i-covered:-1])  #计算离当前点最近的那个最大值,故必须倒序求位置,然后再反过来
            #print 'quit:',tm,im
        rev[i] = tm
        irev[i] = im
    return rev,irev

def ti_min(source,covered): #最近len个数据的min值及这些min值的坐标
    tm = 99999999
    im = 0
    rev = np.zeros_like(source)
    irev = np.zeros_like(source)
    length = len(source)
    prelen = length > covered and covered or length
    for i in range(prelen):
        v = source[i]
        if tm >= v: #以最近的那个最小值位置为准
            tm = v
            im = i
        rev[i] = tm
        irev[i] = im
    buffer = deque([v for v in source[:prelen]])   #优化方法，避免vquit=source[i-covered]的方式，对nbarray的直接索引有严重的性能问题
    for i in range(prelen,length):
        v = source[i]
        buffer.append(v)
        vquit=buffer.popleft()
        if tm >= v: #以最近的那个最小值位置为准
            tm = v
            im = i
        if tm == vquit and v != tm: #退出的正好是最大值,计算前covered-1个元素的最大值, pre=source[i-1]
            tm = np.min(source[i-covered+1:i+1])
            im = i - np.argmin(source[i:i-covered:-1])  #计算离当前点最近的那个最小值,故必须倒序求位置,然后再反过来            
        rev[i] = tm
        irev[i] = im
    return rev,irev

def maxmin0(source,functor,limit):    #全周期顺序maxmin计算,即返回值每个元素都是从起始到它这个位置的最大/最小值
    rev = np.zeros_like(source)
    cur = limit
    for i in range(len(source)):
        cur = functor(cur,source[i])
        rev[i] = cur
    return rev

def amaxmin0(source,functor,limit):    #全周期顺序maxmin位置计算,即返回值每个元素都是从起始到它这个位置的最大/最小值的索引
    rev = np.zeros_like(source)
    pre = limit
    index = 0
    for i in range(len(source)):
        cur = functor(pre,source[i])
        if cur != pre:
            index = i
            pre = cur
        rev[i] = index
    return rev

def max0(source):
    return maxmin0(source,max,-99999999)

def min0(source):
    return maxmin0(source,min,99999999)

def amax0(source):
    return amaxmin0(source,max,-99999999)

def amin0(source):
    return amaxmin0(source,min,99999999)


def mapping(signal,v2index,length):
    ''' 映射运算
        以v2index中的value为index，将signal中的相应信号转换为长度为length的序列中
        后面的数值覆盖前面的. 因此不能将此用于vap/svap系列的逆运算，因为可能会导致同日的后面的0覆盖前面的信号
    '''
    assert len(signal) == len(v2index)
    assert len(v2index) == 0 or np.max(v2index) < length    #v2index中的value不能大于length,否则越界
    rev = np.zeros(length,int)
    for i in xrange(len(signal)):
        rev[v2index[i]] = signal[i]
    return rev

def transform(signal,v2index,length):
    ''' 变形运算
        以v2index中的value为index，将signal中的相应信号转换为长度为length的序列中
        信号量均转换为1
    '''
    assert len(signal) == len(v2index)
    assert len(v2index) == 0 or np.max(v2index) < length    #v2index中的value不能大于length,否则越界
    rev = np.zeros(length,int)
    ss = v2index[signal!=0]
    if len(ss) > 0:
        rev[ss] = 1
    return rev

LIMIT_BASE = 10000
def limitup1(source,limit=990):   #涨停板,以万分之表示
    pre = rollx(source,1)
    return np.sign(source * LIMIT_BASE / pre >= limit + LIMIT_BASE)

def limitdown1(source,limit=-990):  #跌停板,以万分之表示
    pre = rollx(source,1)
    return np.sign(source * LIMIT_BASE / pre <= limit+LIMIT_BASE)

def limit1(source,uplimit=990,downlimit=-990):  #涨跌停板,返回值以1表示涨停,-1表示跌停
    tu = limitup1(source,uplimit)
    td = limitdown1(source,downlimit)
    return tu - td     

def limitup2(high,low,limit=990):   #一字涨停,以万分之表示,不再依赖limit,认为上涨一线就是停
    #return band(high-low==0,limitup1(high,limit))
    pre = rollx(high,1)
    return band(high-low==0,pre<high)

def limitdown2(high,low,limit=-990):   #一字跌停,以万分之表示
    pre = rollx(high,1)
    return band(high-low==0,pre>high)

def limit2(high,low,uplimit=990,downlimit=-990):  #涨跌停板,返回值以1表示一字涨停,-1表示一字跌停
    tu = limitup2(high,low,uplimit)
    td = limitdown2(high,low,downlimit)
    return tu - td     

