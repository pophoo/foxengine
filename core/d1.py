# -*-coding:utf-8 -*-

#一维向量的计算

import numpy as np

from wolfox.fengine.core.base import cache,wcache

BASE = 1000

band = lambda x,y : np.sign(np.logical_and(x,y))
bor = lambda x,y : np.sign(np.logical_or(x,y))
bnot = lambda x:np.sign(np.logical_not(x))
greater = lambda x,y=0:np.sign(x>y)
greater_equals = lambda x,y=0:np.sign(x>=y)
lesser = lambda x,y=0:np.sign(x<y)
lesser_equals = lambda x,y=0:np.sign(x<=y)
equals = lambda x,y=1:np.sign(x==y)

def gand(*args):
    ''' args[i]等长，返回args同位元素的and序列
        args[i]中非0为信号
    '''
    ss = [ np.sign(s!=0) for s in args]  #每次!=0的出现都作为1
    s = reduce(np.add,ss)
    return np.sign(s == len(ss)) #1出现次数等于ss组数

def gor(*args):
    ''' args[i]等长，返回args同位元素的and序列
        args[i]中非0为信号
    '''
    ss = [ np.sign(s!=0) for s in args]  #每次!=0的出现都作为1
    s = reduce(np.add,ss)
    return np.sign(s > 0) #1出现次数>0

def gmax(*source):
    ''' 返回source各数组中同位元素的最大值组成的数组
    '''
    return np.array(source).max(axis=0)

def gmin(*source):
    ''' 返回source各数组中同位元素的最小值组成的数组
    '''
    return np.array(source).min(axis=0)

def subd(source,distance=1):   #偏移减法,distance必须大于0,返回结果中前distance个元素为0
    pres = np.zeros(distance,int)
    main = source[distance:] - source[:-distance]
    return np.concatenate((pres,main))

def nsubd(source,distance=1):   #自然的偏移减法,distance必须大于0,返回结果中前distance个元素不变
    rs = roll0(source,distance)
    return source - rs

def desync(source,signal):
    ''' 根据signal序列压缩source序列，去除其中signal=0的部分
        也可直接调用source.compress(signal)
    '''
    return source.compress(signal)  #等效于source[np.nonzero(signal)]

def desyncs(source,signal):
    ''' 根据signal序列压缩source序列，去除其中signal=0的部分
        其中source必须是正的信号序列,在返回值中该正信号被标准化为1
        若是source中被去除的部分有信号，则其信号被延递到最接近的下一个未被压缩元素
    '''
    tmp = source.cumsum().compress(signal)
    return np.sign(nsubd(tmp)>0) #这里>0的目的是将np.sign返回的类型约束为int8，因为np.sign对bool返回int8而int返回int32

def sync(source,signal):
    ''' desync的逆函数
        根据source和signal恢复出使desync(xsource,signal)=source的xsource，并且使得xsource中signal为0的位置其值也为0
        必须保证len(source) = sum(signal)或signal中非0值的个数
    '''
    rev = np.zeros(len(signal),source.dtype)
    bsignal = (signal != 0)
    rev[bsignal] = source
    return rev

DEFAULT_SMOOTH_FUNC = lambda *args:args[0] if len(args)==1 else gand(*args) #如果只有一个参数就直接返回
def smooth(signal,*sources,**kwargs):
    ''' 将sources中的各序列按照signal非空压缩后，调用sfunc进行处理，然后将处理结果展开并返回
        一个额外的关键字参数: sfunc
        最简单和典型的用法是
            把source中signal为0位置的信号延续到其后最近的signal为1的位置
            其中source必须是正的信号序列,signal中非0为有信号,在返回值中该正信号被标准化为1
            相当于sync(desyncs(source,signal),signal)
        实际上对于默认的函数来说,相当于sync(desyncs(source,signal),signal)
        这个现在看来没啥用处
    '''
    assert sources
    sfunc = kwargs.get('sfunc',DEFAULT_SMOOTH_FUNC)        #默认参数的另一种方法，避免对位置参数的污染
    rev = np.zeros_like(sources[0]) #这里的不会产生溢出
    bsignal = (signal != 0)
    #连续非空位的累积值如果有变化，则说明第二个位置有信号或者两个非空位之间的空位有信号
    tmp = [greater(nsubd(source.cumsum()[bsignal])) for source in sources]  #这里>0的目的是将np.sign返回的类型约束为int8，因为np.sign对bool返回int8而int返回int32. 而传入的source则可能为int8类型
    #print 'in smooth:tmp=',tmp,',sources:',sources,'bsignal:',bsignal
    #print rev.dtype,tmp.dtype
    rev[bsignal] = sfunc(*tmp)
    return rev

def smooth2(signal,src1,src2):
    ''' 同时处理两个独立source的smooth的快捷方式
    ''' 
    return smooth_simple(signal,src1),smooth(signal,src2)

def smooth_simple(signal,source):   #最早的简单实现,已经废弃
    ''' 把source中signal为0位置的信号延续到其后最近的signal为1的位置
        其中source必须是正的信号序列,signal中非0为有信号,在返回值中该正信号被标准化为1
        相当于sync(desyncs(source,signal),signal)
    '''
    #print 'len of source:',len(source)
    rev = np.zeros_like(source) #这里的不会产生溢出
    bsignal = (signal != 0)
    #连续非空位的累积值如果有变化，则说明第二个位置有信号或者两个非空位之间的空位有信号
    tmp = greater(nsubd(source.cumsum()[bsignal]))  #这里>0的目的是将np.sign返回的类型约束为int8，因为np.sign对bool返回int8而int返回int32. 而传入的source则可能为int8类型
    #print rev.dtype,tmp.dtype
    rev[bsignal] = tmp
    return rev

def roll0(source,shift=1):   #每行数据右移，移动部分补0
    #print len(source),shift
    if len(source) == 0:    #不能用if source，因为np.array不能直接适用逻辑运算
        return np.array([])
    rev = np.roll(source,shift)
    if shift >= 0:
        rev[:shift] = 0
    else:
        slen = len(source)
        begin = slen + shift if slen + shift >=0 else 0
        rev[begin:] = 0
    return rev

def rollx(source,shift=1):   #基本版每行数据移动，移动部分补第一列（右移）的值或最后一列（左移）
    if len(source) == 0:    #不能用not source
        return np.array([])
    rev = np.roll(source,shift)
    if shift > 0:
        rev[:shift] = source[0]
    elif shift < 0:
        slen = len(source)
        begin = slen + shift if slen + shift >=0 else 0
        rev[begin:] = source[-1]
    return rev


