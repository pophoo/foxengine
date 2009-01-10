# -*-coding:utf-8 -*-

#一维向量的计算

import numpy as np

BASE = 1000

OPEN,CLOSE,HIGH,LOW,AVG,AMOUNT,VOLUME = range(0,7)  #要做数组的下标，必须从0开始

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

def roll0(source,shift):   #每行数据右移，移动部分补0
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
