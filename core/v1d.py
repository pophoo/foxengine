# -*-coding:utf-8 -*-

#一维向量的计算

import numpy as np

def ma(source,length):    #使用numpy，array更加的惯用法
    """ 计算移动平均线
        @param source 源数组
        @param length 均线跨度
        @return 移动平均序列
    """
    if(len(source) < length):
        return np.zeros(len(source));
    
    rev = np.zeros_like(source); ##预先的0

    pps = length/2 #用于整数四舍五入尾数

    acc = np.add.accumulate(source)
    rev[length-1] = acc[length-1] #第length个元素是第一个非零值

    np.subtract(acc[length:],acc[:len(acc)-length],rev[length:])
    rev += pps  #这种in place方式要快于 sum = (sum + pps) / length
    rev /= length

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
    rev = np.zeros_like(source)
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

