# -*-coding:utf-8 -*-

#二维向量的计算

import numpy as np

def posort(v):   
    ''' 对二维数组的每一列进行位置排序
        返回的每个元素都表示它所对应的源元素在所在列的排序序号
    '''
    return v.argsort(0).argsort(0)

def inverse_posort(v):
    ''' 对二维数组的每一列进行位置排序
        返回的每个元素都表示它所对应的源元素在所在列的逆排序序号
    '''
    return (v.shape[0] - 1) - v.argsort(0).argsort(0)

def percent_sort(v,sfunc=posort):
    ''' 对二维数组的每一列进行位置排序
        返回的每个元素都表示它所对应的源元素在所在列的百分序
    '''
    rev = sfunc(v)
    rev *= 10000
    rev /= rev.shape[0]
    return rev

def inverse_percent_sort(v):
    return percent_sort(v,inverse_posort)

def increase(v,distance=1):
    ''' 计算二维数组每列的distance增量(以万分数表示)
        返回的前distance列都为0
    '''
    r1 = np.roll(v,distance,1)
    rev = (v-r1)*10000/r1
    rev[:,:distance] = 0
    return rev

def ma2d(source,length):
    ''' 计算二维数组每行的ma 
    '''
    if(source.shape[1] < length):
        return np.zeros_like(source);
    
    prezeros = np.zeros_like(source); ##预先的0

    pps = length/2 #用于整数四舍五入尾数

    acc = np.cumsum(source,1)
    prezeros[:,length-1] = acc[:,length-1] #第length个元素是第一个非零值

    np.subtract(acc[:,length:],acc[:,:acc.shape[1]-length],prezeros[:,length:])
    prezeros += pps  #这种in place方式要快于 sum = (sum + pps) / length
    prezeros /= length
    
    return prezeros

from wolfox.fengine.core.v1d import ma
def ma2(v2,length): #利用一维数组的ma算法
    row_number = v2.shape[0]
    rev = np.zeros_like(v2)
    for i in xrange(row_number):
        rev[i] = ma(v2[i],length)
    return rev

def ma2a(v2,length):    #v2是array的list
    row_number = len(v2)
    rev = [0] * row_number
    for i in xrange(row_number):
        rev[i] = ma(v2[i],length)
    return rev

def __bench_ma():
    from time import time

    length = 4000
    times = 50
    a=np.arange(8000000)
    a.shape=2000,4000

    b=time()
    for i in xrange(times):
        s = [ r for r in a]
    e=time()
    print e-b

    b=time()
    for i in xrange(10):
        sa = np.array(s)
    e=time()
    print e-b


    b=time()
    for i in xrange(times):
        ma2(a,3)
    e=time()
    print e-b

    b=time()
    for i in xrange(times):
        ma2d(a,3)
    e=time()
    print e-b

    b=time()
    for i in xrange(times):
        ma2a(s,3)
    e=time()
    print e-b
    

if __name__ == '__main__':
    import psyco
    psyco.full()
    __bench_ma()
    #一般情况，大概二维向量ma的方式比逐行ma快一倍
    #在pysco.full()下面，提升不大，差别在10%以内。内存耗用ma2a最小
