# -*-coding:utf-8 -*-

#一维向量的计算

import numpy as np

def ma1(source,length):    #使用numpy，array更加的惯用法
    """ 计算移动平均线
        @param source 源数组
        @param length 均线跨度
        @return 移动平均序列
    """

    if(len(source) < length):
        return np.zeros(len(source));
    
    prezeros = np.zeros_like(source); ##预先的0

    pps = length/2 #用于整数四舍五入尾数

    acc = np.add.accumulate(source)
    prezeros[length-1] = acc[length-1] #第length个元素是第一个非零值

    np.subtract(acc[length:],acc[:len(acc)-length],prezeros[length:])
    prezeros += pps  #这种in place方式要快于 sum = (sum + pps) / length
    prezeros /= length

    return prezeros


