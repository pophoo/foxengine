# -*-coding:utf-8 -*-

#一维向量的计算
#v1d的补充

import numpy as np
BASE = 1000

def cover(source,interval=1): #interval必须大于0
    ''' 信号延伸，length为延伸值，发生日为length,逐日递减，直至另一个发生日
        初始序列中以>0认为是有信号(以免最普通的用法中需要先过滤掉负值)
        假定-1位置无信号发生
    '''
    rev = np.zeros_like(source)
    curcover = 0
    for i in xrange(len(source)):
        curcover = source[i] != 0 and interval or curcover-1
        rev[i] = curcover
    return rev

def extend(source,interval=1):#interval必须大于0
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
        rev[i] = curextend > 0 and v or 0
    return rev

def distance(source):
    ''' 信号相对距离，信号日为0，逐日递增，直至另一个信号日
        初始序列中以非0认为是有信号
    '''
    rev = np.zeros_like(source)
    curdistance = 0 #假设前一天为信号发生，因为计算所的的值肯定小于实际距离
    for i in xrange(len(source)):
        curdistance = source[i] == 0 and curdistance+1 or 0 #不能采用 ?? and 0 or ?+1的方式，因为and 0是False常量
        rev[i] = curdistance
    return rev


def rsum(source,signal):
    ''' 信号日signal之间的相对累积,signal!=0为有信号'''
    assert len(source) == len(signal)
    rev = np.zeros_like(source)
    sum = 0
    for i in xrange(len(source)):
        if(signal[i] != 0):
            sum = source[i]
        else:
            sum += source[i] #不能采用 ?? and 0 or ?+1的方式，因为and 0是False常量
        rev[i] = sum
    return rev

def ravg(source,signal):
    ''' 信号日signal之间的相对均值,signal!=0为有信号'''
    assert len(source) == len(signal)
    rev = np.zeros_like(source)
    n,sum = 0,0
    for i in xrange(len(source)):
        if(signal[i] != 0):
            sum = source[i]
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
    rev = np.zeros_like(source)
    pre = 0
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
        @return 移动平均序列
    """
    acc = np.add.accumulate(source)
    dacc = np.roll(acc,length)
    rev = acc - dacc
    rev[:length] = 0
    return rev

def msum2(source,length):   
    """ 计算移动累积,前length-1个置为0-当前位置的累积
        @param source 源序列
        @param length 均线跨度
        @return 移动平均序列
    """
    acc = np.add.accumulate(source)
    dacc = np.roll(acc,length)
    rev = acc - dacc
    rev[:length] = acc[:length]
    return rev


def l_emaxmin(source,functor):
    ''' 近似新高/新低覆盖，因为两层循环内多次用到索引操作，所以用list来计算，用np.array效率会极低
        以最远的小于当前点的高/低点的覆盖范围(界限为该高/低点对应的低/高点)为起始点
        而实际上，该点和前一高点之间还存在比当前点更低的连续点，这部分被忽略
        所以结果实际上是从某个低点开始的总长度(当前点不计入内)
    '''
    rev = numbers(len(source))
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
    '''去除间隔期内!=0数值的重复出现
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
    rev = np.zeros_like(source)
    extended = covered>1 and extend(source1,covered) or source1
    for i in xrange(len(source1)):
        if(extended[i] != 0 and source2[i] != 0):
            rev[i] = 1
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
    ss = [ np.sign(msum2(s,covered)) for s in sources]  #每次出现都作为1
    s = reduce(np.add,ss]
    return np.sign(s == len(ss)) #1出现次数等于ss组数

def consecutive(source,value=1):
    ''' 计算序列source中value的连续出现次数
    '''
    rev = np.zeros_like(source)
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
    vmax = tmax(source,covered)
    vmin = tmin(source,covered)
    vdiff = vmax-vmin
    return vdiff*BASE/vmin

def swing2(shigh,slow,covered=1):   #已知高低序列的波动幅度
    vmax = tmax(shigh,covered)
    vmin = tmin(slow,covered)
    vdiff = vmax - vmin
    return vdiff*BASE/vmin

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
    rev = zeros_like(source)
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

def tmax(source,covered):
    return tmaxmin(source,covered,max,np.max,-99999999)

def tmin(source,covered):
    return tmaxmin(source,covered,min,np.min,99999999)


