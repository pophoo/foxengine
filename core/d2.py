# -*-coding:utf-8 -*-

#二维向量的计算

import numpy as np
PERCENT_BASE = 10000

from wolfox.fengine.core.base import OPEN,CLOSE,HIGH,LOW,AVG,AMOUNT,VOLUME
import wolfox.fengine.core.d1 as d1
from wolfox.fengine.core.source import extract_collect


def assign(stocks,name,obj):
    for s in stocks:
        s.__dict__[name] = obj

class dispatch(object):
    """ 将(name,stocks,*args,**kwargs)形式的调用结果(array形式)dispatch到stock中相应name的属性中
        要求被修饰函数的签名为(stocks,*args,**kwargs)
    """
    def __init__(self, func):
        self.func = func
    
    def __call__(self,name,stocks,*args,**kwargs):
        sector = kwargs.get('sector',CLOSE)        #默认参数的另一种方法，避免对内部func位置参数的污染(否则为了向func提供参数，必须先明确提供sector参数，或者使用关键字方式指定func的参数，而不能使用位置方式[会被优先当作sector])
        sdatas = extract_collect(stocks,sector)
        datas = self.func(sdatas,*args,**kwargs)
        #print datas
        for s,data in zip(stocks,datas):
            s.__dict__[name] = data
        return datas

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__


class cdispatch(object):
    """ 将(name,catalogs,*args,**kwargs)形式的调用结果(array形式)dispatch到stock中相应name属性表示的dict中，dict[catalog_id] = v
        要求被修饰函数的签名为(stocks,*args,**kwargs)
        #需要一个准集成测试
    """
    def __init__(self, func):
        self.func = func
    
    def __call__(self,name,catalogs,*args,**kwargs):
        sector = kwargs.get('sector',CLOSE)        #默认参数的另一种方法，避免对内部func位置参数的污染(否则为了向func提供参数，必须先明确提供sector参数，或者使用关键字方式指定func的参数，而不能使用位置方式[会被优先当作sector])
        for c in catalogs:
            self._dispatch(name,c,sector,*args,**kwargs)

    def _dispatch(self,name,catalog,sector=CLOSE,*args,**kwargs):
        sdatas = extract_collect(catalog.stocks,sector)
        datas = self.func(sdatas,*args,**kwargs)
        #print datas
        for s,data in zip(catalog.stocks,datas):
            s.__dict__.setdefault(name,{})[catalog] = data  #这样，这个dict的item就是(catalog,data)
        return datas

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

@dispatch
def dispatch_example(sdatas,ma=10):
    try:
        return sdatas
    except Exception,inst: #没有交易数据
        #print np.array([[] for s in stocks]).tolist()
        return np.array([[] for s in stocks])


def roll02(source,shift):   #每行数据右移，移动部分补0. 二维版本(兼容一维)
    if source.ndim == 1:
        return d1.roll0(source,shift)
    assert source.ndim == 2
    if len(source[0]) == 0:
        return source.copy()
    rev = np.roll(source,shift,axis=1)
    if shift >= 0:
        rev[:,:shift] = 0
    else:
        rlen = source.shape[1]
        begin = rlen + shift if rlen + shift >=0 else 0
        rev[:,begin:] = 0
    return rev

def rollx2(source,shift):   #每行数据右移，移动部分补第一列. 二维版本(兼容一维)
    if source.ndim == 1:
        return d1.rollx(source,shift)
    assert source.ndim == 2
    if len(source[0]) == 0:
        return source.copy()
    rev = np.roll(source,shift,axis=1)
    if shift > 0:
        rev[:,:shift] = source[:,0][:,np.newaxis]   #化行为列,source[:,0]返回的是行，[:,np.newaxis]后变为二维
    elif shift < 0:
        rlen = source.shape[1]
        begin = rlen + shift if rlen + shift >=0 else 0
        rev[:,begin:] = source[:,-1][:,np.newaxis]  #化行为列
    return rev


def nsubd2(source,distance=1):   #自然的偏移减法,distance必须大于0,返回结果中前distance个元素不变
    if source.ndim == 1:
        return d1.nsubd(source)
    rs = roll02(source,distance)
    return source - rs

def posort(v):   
    ''' 对二维数组的每一列进行位置排序
        返回的每个元素都表示它所对应的源元素在所在列的排序序号
    '''
    return v.argsort(0).argsort(0)

#d_posort = dispatch(posort)
#c_posort = cdispatch(posort)

def inverse_posort(v):
    ''' 对二维数组的每一列进行位置排序
        返回的每个元素都表示它所对应的源元素在所在列的逆排序序号
    '''
    return (v.shape[0] - 1) - v.argsort(0).argsort(0)

iposort = inverse_posort

#d_inverse_posort = dispatch(inverse_posort)
#c_inverse_posort = cdispatch(inverse_posort)



def percent_sort(v,sfunc=posort):
    ''' 对二维数组的每一列进行位置排序
        返回的每个元素都表示它所对应的源元素在所在列的百分序
        即有万分之多少的数小于它
    '''
    rev = sfunc(v)
    rev *= PERCENT_BASE
    rev /= rev.shape[0]
    return rev

#d_percent_sort = dispatch(percent_sort)
#c_percent_sort = cdispatch(percent_sort)

def inverse_percent_sort(v):
    ''' 对二维数组的每一列进行位置排序
        返回的每个元素都表示它所对应的源元素在所在列的百分序
        即有万分之多少的数大于它
    '''
    return percent_sort(v,inverse_posort)

ipercent_sort = inverse_percent_sort

#d_inverse_percent_sort = dispatch(inverse_percent_sort)
#c_inverse_percent_sort = cdispatch(inverse_percent_sort)

def increase(v,distance=1):
    ''' 计算二维数组每列的distance增量(以万分数表示)
        返回的前distance列都为0
    '''
    assert v.ndim == 2
    if len(v[0]) == 0:
        return v.copy()
    r1 = np.roll(v,distance,1)
    rev = (v-r1)*PERCENT_BASE/r1
    rev[:,:distance] = 0
    return rev

def nincrease(v,distance=1):
    ''' 计算二维数组每列的distance增量(以万分数表示)
        返回的前distance列都是针对第一列的增量
    '''
    r1 = rollx2(v,distance)
    rev = (v-r1)*PERCENT_BASE/r1
    return rev

def percent(v,distance=1):
    ''' 计算二维数组每列的distance比例(以万分数表示，当前列是目标列的%)
        返回的前distance列都为0
        相当于increase+1，最大的差异是percent都大于0，而increase为[-1,..)，全零者(increase=0)被置于中间。percent相对于标准化了，全零者(percent=0)被置于底部
        故percent更适合        
    '''
    assert v.ndim == 2
    if len(v[0]) == 0:
        return v.copy()
    r1 = np.roll(v,distance,1)
    rev = v*PERCENT_BASE/r1
    rev[:,:distance] = 0
    return rev

def npercent(v,distance=1):
    ''' 计算二维数组每列的distance比例(以万分数表示，当前列是目标列的%)
        相当于nincrease+1
        相对于nincrease，最大的差异是npercent都大于0，而nincrease为[-1,..)，全零者(nincrease=0)被置于中间。npercent相对于标准化了，全零者(npercent)被置于底部
        故npercent更适合
    '''
    r1 = rollx2(v,distance)
    rev = v*PERCENT_BASE/r1
    return rev

def cmp_percent(v,pos=0):
    ''' 计算二维数组每列的相对于第pos列的比例(以万分数表示，当前列是目标列的%)
    '''
    assert v.ndim == 2
    if len(v[0]) == 0:
        return v.copy()
    d = v[:,pos]
    d_column = d[:,np.newaxis]    #化行为列，便于除法
    return (v * PERCENT_BASE)/ d_column


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

def nma2d(source,length):
    ''' 计算二维数组每行的native ma 
    '''
    dividen = np.arange(source.shape[-1]) + 1
    dividen[dividen > length] = length

    pps = dividen/2 #用于整数四舍五入尾数

    acc = np.cumsum(source,1)
    rev = nsubd2(acc,length) 

    rev += pps  #这种in place方式要快于 sum = (sum + pps) / length
    rev /= dividen

    return rev

from wolfox.fengine.core.d1ex import ma,nma
def ma2(v2,length): #利用一维数组的ma算法
    row_number = v2.shape[0]
    rev = np.zeros_like(v2)
    for i in xrange(row_number):
        rev[i] = ma(v2[i],length)
    return rev

def nma2(v2,length): #利用一维数组的ma算法
    row_number = v2.shape[0]
    rev = np.zeros_like(v2)
    for i in xrange(row_number):
        rev[i] = nma(v2[i],length)
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

