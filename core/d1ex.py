# -*-coding:utf-8 -*-

#一维向量的计算
#v1d的补充

import numpy as np
from collections import deque
from wolfox.fengine.core.base import cache,wcache
from wolfox.fengine.core.d1 import BASE,band,gand,gor,nsubd,roll0,rollx,equals,nequals,greater_equals,subd,greater,lesser_equals
from wolfox.fengine.core.utils import fcustom

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

def fma(source,length):    #使用numpy，array更加的惯用法
    """ 计算移动平均线, 返回浮点数
        @param source 源数组
        @param length 均线跨度
        @return 移动平均序列
    """
    if(len(source) < length):
        return np.zeros(len(source),np.float);
    
    rev = np.zeros(len(source),np.float); ##预先的0,不采用zeros_like是为了避免

    acc = np.add.accumulate(source)
    rev[length-1] = acc[length-1] #第length个元素是第一个非零值

    np.subtract(acc[length:],acc[:len(acc)-length],rev[length:])
    rev /= (length*1.0)

    return rev

def fnma(source,length):    #自然ma算法，前length个元素为各自的累积和除以累积元素个数
    """ 计算移动平均线,返回浮点数
        @param source 源数组
        @param length 均线跨度
        @return 移动平均序列
    """
    
    dividen = np.arange(len(source))+1
    dividen[dividen > length] = length

    acc = np.add.accumulate(source)
    rev = nsubd(acc,length)

    rev = rev*1.0/dividen
    return rev


#简单趋势，1表示向上，-1表示向下.
def trend(source,interval=1):
    assert interval >= 0
    return np.sign(subd(source,interval))

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
    rev = np.zeros(len(source),int) #可能产生溢出，所以不能用zeros_like
    if len(source) == 0:
        return rev
    pre_v = source[0]
    cur = 0
    for i in xrange(1,len(source)):
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

#趋势的翻转次数
rturn = lambda sx:sum(gor(gand(rollx(sx)>0,sx<0),gand(rollx(sx)<0,sx>0)))


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
    ''' 信号日低于或下叉。source一般为downlimit,follow为low
        不仅仅给出下叉信号,而且还给出signal日follow是否低于source
        信号日低于，则将屏蔽买入
        下叉则是卖出
    '''
    sd = equals(cross(source,follow),-1)
    indices = (signal > 0)
    sd[indices] = greater_equals(source[indices],follow[indices])
    return sd

def scover(source,covered=1):
    ''' 信号覆盖
        对信号日开始的covered日内进行信号覆盖
        原始序列以>0为有信号
        输出序列以1为有信号
    '''
    ss = greater(source,0)
    mss = msum2(ss,covered)
    #print ss,mss    
    return greater(mss,0)

def cover(source,interval=1): #interval必须大于0
    ''' 信号延伸，length为延伸值，发生日为length,逐日递减(小于0则都为0)，直至另一个发生日.
        初始序列中以!=0认为是有信号
        假定-1位置无信号发生
        新的信号会增强已有信号        
    '''
    rev = np.zeros(len(source),np.int16)    #cover 最大为65536
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
    #print indices
    for i in xrange(0,len(indices)):
        cur = indices[i]
        rev[cur:cur+interval] = source[cur] #越界赋值不会出现异常
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

def extend2diff(source,signal):
    '''
        信号延伸到signal不同的位置
        和derepeatc结合，用于实现一天只取第一个信号
         signal_a = extend2diff(signal_a,sif.date)
         signal_a = derepeatc(signal_a)
    '''
    rev = np.zeros_like(source)
    prev = 0
    pres = 0
    for i in xrange(len(source)):
        cv = source[i]
        cs = signal[i]
        if cv != 0:
            rev[i] = cv
            prev = cv
        elif cs == pres and prev !=0:
            rev[i] = prev
        elif cs != pres:
            prev = 0
        pres = cs
    return rev

def sum2diff(source,signal):
    '''
        累加到信号变化处
    '''
    rev = np.zeros(len(source),np.int32)
    ss = 0
    pres = 0
    for i in xrange(len(source)):
        cv = source[i]
        cs = signal[i]
        if cs == pres:
            ss += int(cv)
        else:
            ss = cv
        pres = cs
        rev[i] = ss
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

def distance2(source):
    ''' 信号相对距离，信号日为上一信号日到此距离，次日为1，逐日递增，直至另一个信号日
        初始序列中以非0认为是有信号
    '''
    rev = np.zeros(len(source),int) #可能产生溢出，所以不能用zeros_like
    curdistance = 0 #假设前一天为信号发生，因为计算所的的值肯定小于实际距离
    for i in xrange(len(source)):
        if source[i]:
            rev[i] = curdistance + 1
            curdistance = 0
        else:
            curdistance = curdistance+1
            rev[i] = curdistance
    return rev

def rsum(source,signal):
    ''' 信号日signal之间的相对累积,signal!=0为有信号
        信号日数据为当日值
    '''
    assert len(source) == len(signal)
    rev = np.zeros(len(source),int) #可能产生溢出，所以不能用zeros_like
    sum = 0
    for i in xrange(len(source)):
        sum = source[i] + 0 if signal[i] != 0 else sum+source[i]    #source[i]+0是为了类型转换，将可能的int8转为int32
        rev[i] = sum
    return rev

def rsum2(source,signal):
    ''' 信号日signal之间的相对累积,signal!=0为有信号
        信号日数据是上一日累积值+1/2当日值，并将累积值更新为1/2当日值。即信号日段的值为头尾日值1/2+中间日值
    '''
    assert len(source) == len(signal)
    rev = np.zeros(len(source),int) #可能产生溢出，所以不能用zeros_like
    sum = 0
    for i in xrange(len(source)):
        if signal[i]:
            c = (source[i]+1)/2 #四舍五入
            rev[i] = sum + c
            sum = c
        else:
            sum += source[i]
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

def rsub_old(source,signal):
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

def ssub(source):
    '''
        相邻信号量相减
        约等于rsub(source,source),当第一个元素不等于0时第一个元素不相同
    '''
    isc = np.nonzero(source)
    ssource = nsubd(source[isc])
    rev = np.zeros_like(source)
    if(len(isc[0])>0):
        rev[isc] = ssource
    return rev

def rsub(source,signal):
    ''' 相邻信号日signal的减法(相当于比较) 
        d(n+1) = src(n+1) -  s(n)
        d(0) = src(0)
    '''
    assert len(source) == len(signal)
    if len(source) == 0:
        return source.copy()
    isc = np.nonzero(signal)
    ssource = nsubd(source[isc])
    if(len(ssource)>0): #第一个元素应该减去序列的第一个,因为它没东西减
        ssource[0] -= source[0]
    rev = np.zeros_like(source)
    if(len(isc[0])>0):
        rev[isc] = ssource
    return rev

def rsub2(source,signal,distance=1):
    ''' 相邻信号日signal的减法(相当于比较) 
        d(n+1) = src(n+1) -  s(n)
        d(0) = src(0)
    '''
    assert len(source) == len(signal)
    isc = np.nonzero(signal)
    ssource = nsubd(source[isc],distance)
    if(len(ssource)>0): #前distance元素应该减去序列的第一个,因为它没东西减
        for i in range(distance):
            ssource[i] -= source[0]
    rev = np.zeros_like(source)
    if(len(isc[0])>0):
        #print isc,len(isc)
        rev[isc] = ssource
    return rev

def msum(source,length):   
    """ 计算移动累积,前length-1个置0
        @param source 源序列
        @param length 均线跨度
        @return 移动累积序列
    """
    if(len(source) == 0):
        return source.copy()
    if length == 0:
        length = 1
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
    if length == 0:
        length = 1
    acc = np.add.accumulate(source)
    dacc = np.roll(acc,length)
    dacc[:length]=0
    rev = acc - dacc
    rev[:length-1] = acc[:length-1]
    return rev

def kfactor(source,signal=None):
    '''
        计算source中相邻信号的k因子
        k因子指值差除以距离
        返回的是浮点数
        这里不设置interval参数，是因为如果interval>1，则有kfactor的交叠问题
            如1-->3,2-->4，则1-->2用13的斜率，而2-4用24斜率，直觉无意义
    '''
    if len(source)==0:
        return np.array([])
    if signal == None:  #对于数值正好为0的情况，需要signal
        signal = source 
    else:
        assert len(source) == len(signal)
    rev = np.zeros(len(source),np.float)
    si = np.nonzero(signal)[0]
    if len(si) == 0:
        return rev
    ss = source[si]
    drev = nsubd(ss) * 1.0 / nsubd(si)
    rev[rollx(si)] = drev
    rev = extend2next(rev)
    #rev[si] = rev[si-1] #起点/转折点斜率为0
    rev = np.select([signal!=0],[rollx(rev)],rev)
    return rev

def kx(source,kfactor,signal=None):
    '''
        根据kfactor对source中的信号划线, kfactor为倍数为BASE的整数
        该线一直划到下一个信号处或终点
        用于拉支撑阻力线
        返回的是浮点数
    '''
    if len(source)==0:
        return np.array([])
    if signal == None:  #对于数值正好为0的情况，需要signal
        signal = source 
    else:
        assert len(source) == len(signal)
    rev = np.select([source!=0],[source*1.0],0)
    si = np.nonzero(signal)[0]
    rev[si] = source[si]
    if len(si) == 0:
        return rev
    pre = si[0]
    for iv in si[1:]:
        prev = rev[pre]
        for irev in xrange(pre+1,iv):
            prev += kfactor
            rev[irev] = prev
        pre = iv
    #尾部
    prev = rev[pre]
    for irev in xrange(pre+1,len(source)):
        prev += kfactor
        rev[irev] = prev        
    return rev

def kx2(source,skfactor,signal=None):
    '''
        根据skfactor对source中的信号划线,skfactor为序列，source中信号以对应的kfactor划线
        该线一直划到下一个信号处
        用于拉支撑阻力线
    '''
    if len(source)==0:
        return np.array([])
    assert len(source) == len(skfactor)
    if signal == None:  #对于数值正好为0的情况，需要signal
        signal = source 
    else:
        assert len(source) == len(signal)
    rev = np.select([source!=0],[source*1.0],0)
    si = np.nonzero(signal)[0]
    rev[si] = source[si]
    if len(si) == 0:
        return rev
    pre = si[0]
    for iv in si[1:]:
        prev = rev[pre]
        kfactor = skfactor[pre]
        for irev in xrange(pre+1,iv):
            prev += kfactor
            rev[irev] = prev
        pre = iv
    #尾部
    prev = rev[pre]
    kfactor = skfactor[pre]
    for irev in xrange(pre+1,len(source)):
        prev += kfactor
        rev[irev] = prev        
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
        如果不忽略，则会导致如果间隔期内持续出现信号，则除了第一个信号之外其余都为0
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

def decover1(source,interval=1):
    ''' 去除间隔期内!=0数值的重复出现，并将信号标准化为1
        新的信号会增强interval. 
        去除效率大于derepeatc
    '''
    nsource = nequals(source,0)
    ms = msum2(nsource,interval+1)  #间隔0为本位和，间隔1位本左邻和
    return gand(equals(ms,1),nsource)

def derepeatc_v(source):
    ''' 去除!=0数值的连续出现(只剩下第一个)
        c是consecutive的意思
        保持原来的值不变
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

def derepeatc(source):
    ''' 去除!=0数值的连续出现(只剩下第一个),正规化为1
        c是consecutive的意思
    '''
    t = subd(nequals(source,0))
    return equals(t,1)

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

def devi(shigh,sdiff,regr=96):
    '''
        背离，是指shigh新高头部形成时，sdiff没有创相应周期的新高
        shigh:高点序列
        sdiff:macd的diff序列
        regr:回撤比例
    '''
    xhigh = tmax(shigh,7)
    xhighl = xhigh * regr/100
    xhighA = gand(shigh < xhighl,rollx(shigh,6)<xhigh)
    xhigh60 =tmax(shigh,60)
    xdiff7 = tmax(sdiff,7)
    xdiff60 = tmax(sdiff,60)
    xdev = gand(xhighA,xhigh == xhigh60,xdiff7<xdiff60)
    return xdev

def hdevi(shigh,ref_quick,ref_slow,sbase=None,covered=20,distance=1):
    '''
        顶背离
        ref_quick,ref_slow(sdiff,ref_slow)用于确认顶底
        sbase是比较线,即顶底确认后的比较
        distance表示与前面第几个顶背离
        这个算法根据macd下叉来确认顶，可能更好？
    '''
    if sbase == None:
        sbase = ref_quick
    sc = gand(cross(ref_slow,ref_quick)<0)
    xhigh = tmax(shigh,covered)
    dhigh = tmax(sbase,covered)
    dxhigh = rsub2(xhigh,sc,distance)
    ddhigh = rsub2(dhigh,sc,distance)
    signal = gand(dxhigh>0,ddhigh<0)
    return signal

def ldevi(slow,ref_quick,ref_slow,sbase=None,covered=20,distance=1):
    '''
        底背离
        ref_quick,ref_slow用于确认顶底
        sbase是比较线,即顶底确认后的比较
        distance表示与前面第几个底背离
        这个算法根据macd下叉来确认底，可能更好？
    '''
    if sbase == None:
        sbase = ref_quick
    sc = gand(cross(ref_slow,ref_quick)>0)
    xlow = tmin(slow,covered)
    dlow = tmin(sbase,covered)
    #print sc,xlow.tolist(),dlow.tolist()
    dxlow = rsub2(xlow,sc,distance)
    ddlow = rsub2(dlow,sc,distance)
    #print dxlow,ddlow
    signal = gand(dxlow<0,ddlow>0)
    return signal

def hpeak(shigh,ref_quick,ref_slow,covered=10):
    '''
        寻找最近高点
        ref_quick,ref_slow(skdj/k,skdj/d)用于确认顶底
        用一分钟skdj的时候，比较快捷，所以covered默认为10
    '''
    sc = gand(cross(ref_slow,ref_quick)<0)
    xhigh = tmax(shigh,covered)
    return np.select([sc],[xhigh],0)

def lpeak(slow,ref_quick,ref_slow,covered=10):
    '''
        寻找最近低点
        ref_quick,ref_slow(skdj/k,skdj/d)用于确认顶底
        用一分钟skdj的时候，比较快捷，所以covered默认为10
    '''
    sc = gand(cross(ref_slow,ref_quick)>0)
    xlow = tmin(slow,covered)
    return np.select([sc],[xlow],0)

def hlpeak(shigh,slow,ref_quick,ref_slow,covered=10):
    '''
        寻找最近高/低点,其中低点以负数表示
        ref_quick,ref_slow(skdj/k,skdj/d)用于确认顶底
        用一分钟skdj的时候，比较快捷，所以covered默认为10
    '''
    sc = cross(ref_slow,ref_quick)
    xhigh = tmax(shigh,covered)    
    xlow = tmin(slow,covered)
    return np.select([sc==-1,sc==1],[xhigh,-xlow],0)

fhigh = lambda sx:gand(sx>rollx(sx),sx>=rollx(sx,-1))   #连续同高，以第一个高点为准
flow = lambda sx:gand(sx<rollx(sx),sx<=rollx(sx,-1))    #连续同低，以第一个低点为准

def zpeak(source,order=1,fpeak=fhigh):
    '''
        寻找n阶高/低点, 含未来数据，只能用于划线
        order默认为1,小于1当作1
    '''
    tsx1 = fpeak(source)
    sx1 = np.select([tsx1!=0],[source],0)
    if order <= 1:
        return sx1
    icursx = np.nonzero(tsx1)[0]
    for i in xrange(1,order):
        sxx = source[icursx]
        tsxx = fpeak(sxx)
        icursx = icursx[np.nonzero(tsxx)[0]]
    osx = np.zeros_like(source)
    osx[icursx] = source[icursx]
    return osx
        
zhpeak = fcustom(zpeak,fpeak=fhigh)
zlpeak = fcustom(zpeak,fpeak=flow)

def zpeaki(source,order=1,fpeak=fhigh):
    '''
        寻找n阶高/低点
        返回值为高点数据序列，以及该高点最大跨度的坐标(即计算该高/低点所需用到的最远的未来数据的坐标)
        order默认为1,小于1当作1
        返回值中第一个是高/低点非0,其余为0的序列 sh
                第二个是该高低点的最远未来数据的坐标序列 si
                其中 sh[np.nonzero(sh)]为高点序列, si[np.nonzero(sh)]为坐标序列,sif.time[si[np.nonzero(sh)]]为坐标的影响时间序列
    '''
    tsx1 = fpeak(source)
    sx1 = np.select([tsx1!=0],[source],0)
    icovered = rollx(np.arange(len(source)),-1)
    if order <= 1:
        return sx1,np.select([tsx1],[icovered],0)
    icursx = np.nonzero(tsx1)[0]
    for i in xrange(1,order):   #必然进入循环
        sxx = source[icursx]
        tsxx = fpeak(sxx)
        icovered[icursx] = rollx(icovered[icursx],-1)   #当前高/低点的计算范围,即之前顶点的范围左转一位(排除掉不是顶点的)
        icursx = icursx[np.nonzero(tsxx)[0]]
    osx = np.zeros_like(source)
    osx[icursx] = source[icursx]
    iz = np.zeros_like(source)
    iz[icursx] = icovered[icursx]   #去掉icovered之中不必要的那些数字
    return osx,iz

zhpeaki = fcustom(zpeaki,fpeak=fhigh)
zlpeaki = fcustom(zpeaki,fpeak=flow)


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
    s = np.sum(source)
    cz = len(np.where(source==0)[0])
    cnz = len(source) - cz
    if(cnz == 0):
        return 0
    return (s+cnz/2)/cnz

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

@cache
def cached_zoom_indices(n,times,pos):
    ''' 缓存同长度zoomout的indices,用在同一次遍历中 '''
    return np.arange(pos,n,times)

def pzoom_out(source,times=5,pos=-1):
    ''' 价格系列缩小，以pos日为准
        pos为-1或者[0:times)
        一般而言pos日即为最后日(times-1)
        但若需要开收盘,则pos日为第一日0
    '''
    pos = pos if pos >= 0 else times-1
    indices = cached_zoom_indices(len(source),times,pos)
    return source.take(indices)

def vzoom_out(source,times=5):
    ''' 量系列缩小,以当期累积为准'''
    indices = cached_zoom_indices(len(source),times,times-1)
    srev = msum(source,times)
    return srev.take(indices)

def zoom_in(zoomed,src_length,times=5):
    ''' zoom_out的逆. 通用于p/v类型
        src_length为放回后的长度
        必须保证 src_length >= len(zoomed)*times
        并且所有指标后移times位
        因为当期指标只有在本期末才能计算得到,所以其覆盖为下期
    '''
    assert src_length >= len(zoomed)*times
    rev = zoomed.repeat(times)
    outed = src_length - len(zoomed)*times
    #print rev,np.zeros(outed,int)    
    if outed > 0:
        rev = np.concatenate((rev,np.zeros(outed,int)))
    return roll0(rev,times)

def supdowns(sopen,sclose,shigh,slow):
    ''' 计算每日的上升力和下降力,简版，不考虑前一日情况
        物理含义: 能确定的必然经历的上升段,是从开盘到高点,以及从最低到收盘
                  下降段,是从开盘到低点,和从最高到收盘
        上升力：
            high-open+close-low
        下降力:
            open-low+high-close
        单位:
            high - low
    '''
    if len(sopen) == 0:
        return np.array([],int),np.array([],int)
    sc1 = rollx(sclose)
    su = shigh - sopen + sclose - slow
    sd = sopen - slow + shigh - sclose
    sb = shigh - slow
    return su*BASE/sb,sd*BASE/sb,

def supdownc(sopen,sclose,shigh,slow):
    ''' 计算每日的上升力和下降力,考虑前一日的情况
        基本上升力：
            high-open+close-low
        基本下降力:
            open-low+high-close
        基本单位:
            high - low
        若open>=close(-1):
            上升力 = 基本上升力 + open - close(-1)
        else:
            下降力 = 基本下降力 - open + close(-1)
        若low>close(-1):
            单位 = 基本单位 + low - close(-1)
        若high<close(-1):
            单位 = 基本单位 + close(-1) - high
    '''
    if len(sopen) == 0:
        return np.array([],int),np.array([],int)
    sc1 = rollx(sclose)
    sc1[0] = sopen[0]   #哨兵，便于处理
    ou = shigh - sopen + sclose - slow
    od = sopen - slow + shigh - sclose
    ob = shigh - slow
    su = np.where(sopen>=sc1,ou+sopen-sc1,ou)
    sd = np.where(sopen<sc1,od-sopen+sc1,od)
    sb1 = np.where(slow>sc1,ob+slow-sc1,ob)
    sb = np.where(shigh<sc1,sb1+sc1-shigh,sb1)
    return su*BASE/sb,sd*BASE/sb,

def supdown(sopen,sclose,shigh,slow):
    ''' 计算每日的上升行程和下降行程
        以前一日收盘和今日开盘指向的方向为运行方向
        则若指向下方,运行轨迹为 开盘-->最低-->最高-->收盘
          若指向上方,运行轨迹为 开盘-->最高-->最低-->收盘
          平开,则顺着昨天的指向收盘的方向，亦即昨日的开盘方向（每日收盘方向等于开盘方向）
        但这个方式有个问题，按理说 跳高开盘高走，应当是买力强劲，而低开高走则相对弱势
                但在本方式的Volume的分配上，反而是后者的比例高。
    '''
    if len(sopen) == 0:
        return np.array([],int),np.array([],int)
    sc1 = rollx(sclose)
    sc1[0] = sopen[0]   #前一日收盘价视同首日开盘价
    u_hlc = shigh-sc1+sclose-slow
    u_lhc = shigh - slow
    d_hlc = shigh - slow
    d_lhc = sc1-slow+shigh-sclose
    direct = np.sign(sopen-sc1) #1为向上，-1为向下，0为平
    direct[0] = 1
    direct = extend2next(direct)    #把0都给填充掉，即用昨日指向收盘的方向作为今日的方向
    u = np.select([direct>0,direct<0],[u_hlc,u_lhc])
    d = np.select([direct>0,direct<0],[d_hlc,d_lhc])
    return u,d


def supdown2(sopen,sclose,shigh,slow):
    ''' 计算每日的上升行程和下降行程
        以距离开盘价距离近的方向为运行方向
        则若最低近,运行轨迹为 开盘-->最低-->最高-->收盘
          若最高近,运行轨迹为 开盘-->最高-->最低-->收盘
          平开往低走
          另，如果开盘大于昨日收盘，则上升段 +　开盘－昨收盘
            　小于昨日收盘，则下降段　+ 昨收盘 - 开盘
    '''
    if len(sopen) == 0:
        return np.array([],int),np.array([],int)
    sc1 = rollx(sclose)
    sc1[0] = sopen[0]   #前一日收盘价视同首日开盘价
    u_hlc = shigh-sopen+sclose-slow
    u_lhc = shigh - slow
    d_hlc = shigh - slow
    d_lhc = sopen-slow+shigh-sclose
    ou = np.where(sopen > sc1)
    od = np.where(sopen < sc1)
    doc = sopen-sc1
    u_hlc[ou] = u_hlc[ou] + doc[ou]
    u_lhc[ou] = u_lhc[ou] + doc[ou]
    d_hlc[od] = d_hlc[od] - doc[od] #doc[od]<0
    d_lhc[od] = d_lhc[od] - doc[od] #doc[od]<0
    is_up = shigh-sopen < sopen-slow #True为向上，False为向下
    u = np.select([is_up],[u_hlc],default=u_lhc)
    d = np.select([is_up],[d_hlc],default=d_lhc)
    return u,d


def supdown3(sopen,sclose,shigh,slow):
    ''' 计算每日的上升行程和下降行程
        以最高价-收盘价为卖方能力，收盘价-最低价位买方能力
        最简单的方式
    '''
    if len(sopen) == 0:
        return np.array([],int),np.array([],int)
    cup = sclose-slow
    cdown = shigh - sclose
    return cup,cdown
    
@cache 
def range4(length):
    assert length % 4 == 0
    return range(3,length,4)

@cache 
def range1(length):
    assert length % 4 == 0
    return range(0,length,4)

@cache 
def range2(length):
    assert length % 4 == 0
    return range(1,length,4)

@cache 
def range3(length):
    assert length % 4 == 0
    return range(2,length,4)

@cache
def nzeros4(length):
    assert length % 4 == 0
    return np.zeros(length,np.int8)

def hour2day(source):
    ms = msum2(source,4)
    return ms.take(range4(len(source)))

def hour2day4(source):#第四位直接转换
    return source.take(range4(len(source)))    

def hour2day1(source):#第1位直接转换
    return source.take(range1(len(source)))    

def hour2day2(source):#第2位直接转换
    return source.take(range2(len(source)))    

def hour2day3(source):#第2位直接转换
    return source.take(range3(len(source)))    


def hour2day_s(source,signals):  
    #根据signals选中相应的source，并在合并中以此source值为准
    #!=0相当于有信号
    #用于根据60分钟叉信号选出相应的价格
    ss = nequals(signals,0)
    ss1 = ss.choose(nzeros4(len(source)),source)
    return hour2day(ss1)/hour2day(ss)   #避免出现多个的情况

def xfollow(source,ref):
    #根据ref中为0的数据，将source中对应位置的数据改为其最左边那个ref不为0的数
    #通常ref为成交量，用于信号的成交量延递，比如涨停信号
    #就地更改
    assert len(source) == len(ref)
    for i in xrange(1,len(source)):
        if ref[i] == 0:
            source[i] = source[i-1]
    return source

def closedayofweek(weekdays): #周收盘日
    #特别特殊的情形下会不正确,如某周一交易日后，下一个交易日正好是下周二,则该周一不会被识别为周收盘日
    #另，最后一个交易日也被识别为周收盘日
    return greater(greater_equals(weekdays-rollx(weekdays,-1)) + equals(weekdays,5))

def opendayofweek(weekdays):    #周开盘日
    #特定情形下会不正确,如某周一交易日后，下一个交易日正好是下周二,则该周二不会被识别为周开盘日. 好在错误对称。
    #另，第一个交易日也被识别为周开盘日
    return greater(lesser_equals(weekdays-rollx(weekdays)) + equals(weekdays,1)) 

cofw = closedayofweek
oofw = opendayofweek
