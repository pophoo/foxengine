# -*- coding: utf-8 -*-

''' 所有未来相关函数
'''

from wolfox.fengine.core.d1indicator import atr
from wolfox.fengine.core.d1ex import tmax,tmin
from wolfox.fengine.core.d1 import rollx,BASE

def mm_ratio(sclose,shigh,slow,length=1,atr_length=1):
    ''' 计算标准化的最大有利变动(MFE)/最大不利变动(MAE)
        即以当日为基准，计算length内AMFE=(最大值-当日值)/atr和(当日值-最小值)/atr
        用于优势率e_ratio的计算：
            所有信号的CMFE之和/所有信号的CMAE之和 (信号次数被约掉)
            应当用这种方式，而不是单独计算CMFE/CMAE然后求平均
            比如一次是2/1,另一次是1/2，如果单独求比例然后平均，则e_ratio=(2+0.5)/2=1.25
                而先求平均再除,则是 (2+1)/(1+2) = 1
                显然后者是正常情形
        这是一个future函数, 正因为有左移的原因,所以最后length的数据是失准的,需要处理掉,失灭为准
    '''
    m_atr = atr(sclose,shigh,slow,atr_length)
    #print m_atr
    m_max = rollx(tmax(sclose,length),-length)  #未来数据左移
    m_min = rollx(tmin(sclose,length),-length)  #未来数据左移
    #print m_min,tmin(sclose,length)
    amfe = (m_max - sclose) * BASE / m_atr      #可能出现m_max[i] < sclose[i]的情况，如当日之后的length内sclose一直下行
    amae = (sclose - m_min) * BASE / m_atr      #可能出现m_min[i] > sclose[i]的情况，如当日之后的length内sclose一直上行
    amfe[-length:] = amae[-length:] = 0
    return amfe,amae

def decline(source,length=1):
    ''' 计算length内最大衰落期和衰落幅度
    '''
    rsource = source[::-1]
    xmin = min0(rsource)[::-1]  #求逆序的顺序最小值
    smax = source - xmin    #当前值和后续的最小值的差，即衰落幅度
    max_range = np.max(smax)
    max_period = 0
    return max_range,max_period
