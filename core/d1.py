# -*-coding:utf-8 -*-

#一维向量的计算

import numpy as np

from wolfox.fengine.core.base import wcache

BASE = 1000

band = np.logical_and
bor = np.logical_or

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

def smooth(source,signal):
    ''' 把source中signal为0位置的信号延续到其后最近的signal为1的位置
        其中source必须是正的信号序列,signal中非0为有信号,在返回值中该正信号被标准化为1
        相当于sync(desyncs(source,signal),signal)
    '''
    #print 'len of source:',len(source)
    rev = np.zeros_like(source)
    bsignal = (signal != 0)
    tmp = np.sign(nsubd(source.cumsum()[bsignal]) > 0)  #这里>0的目的是将np.sign返回的类型约束为int8，因为np.sign对bool返回int8而int返回int32. 而传入的source则可能为int8类型
    rev[bsignal] = tmp
    return rev
    #return sync(desyncs(source,signal),signal)

def roll0(source,shift):   #每行数据右移，移动部分补0
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

def rolln(source,shift):   #基本版每行数据移动，移动部分补第一列（右移）的值或最后一列（左移）
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


