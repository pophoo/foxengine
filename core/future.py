# -*- coding: utf-8 -*-

''' 所有未来相关函数
    未来函数通常用于事后评估和统计，如计算夏普指数等
'''

import logging

import numpy as np
from wolfox.fengine.core.d1indicator import atr
from wolfox.fengine.core.d1ex import tmax,tmin,tmaxmin,min0,amin0,derepeatc,distance,rsub
from wolfox.fengine.core.d1 import BASE,bor,equals,rollx,roll0

logger = logging.getLogger("wolfox.fengine.core.future")

def mm_ratio(sclose,shigh,slow,satr,covered=1):
    ''' 计算标准化的最大有利变动(MFE)/最大不利变动(MAE)
        即以当日为基准，计算covered内AMFE=(最大值-当日值)/atr和(当日值-最小值)/atr
        用于优势率e_ratio的计算：
            所有信号的CMFE之和/所有信号的CMAE之和 (信号次数被约掉)
            应当用这种方式，而不是单独计算CMFE/CMAE然后求平均
            比如一次是2/1,另一次是1/2，如果单独求比例然后平均，则e_ratio=(2+0.5)/2=1.25
                而先求平均再除,则是 (2+1)/(1+2) = 1
                显然后者是正常情形
        这是一个future函数, 正因为有左移的原因,所以最后covered的数据是失准的,需要处理掉,失灭为准
    '''
    m_max = rollx(tmax(sclose,covered),-covered)  #未来数据左移
    m_min = rollx(tmin(sclose,covered),-covered)  #未来数据左移
    #print m_min,tmin(sclose,covered)
    amfe = (m_max - sclose) * BASE / satr      #可能出现m_max[i] < sclose[i]的情况，如当日之后的covered内sclose一直下行
    amae = (sclose - m_min) * BASE / satr      #可能出现m_min[i] > sclose[i]的情况，如当日之后的covered内sclose一直上行
    amfe[-covered:] = amae[-covered:] = 0
    #print amfe.tolist(),amae.tolist()
    return amfe,amae

def mm_sum(sbuy,smfe,smae):
    ''' 根据sbuy和smfe,smae值计算sbuy信号日的mfe,mae之和
    '''
    indices = sbuy > 0
    sum_smfe = np.sum(smfe[indices])
    sum_smae = np.sum(smae[indices])
    return int(sum_smfe),int(sum_smae)

def mm_sum_smooth(sbuy,smfe,smae,smooth=1):
    ''' 根据sbuy和smfe,smae值计算sbuy信号日的mfe,mae之和
    '''
    indices = sbuy > 0
    sum_smfe =  _sum_smooth_mfe(smfe[indices],smooth)
    sum_smae =  _sum_smooth_mae(smae[indices])
    return int(sum_smfe),int(sum_smae)

def _sum_smooth_mfe(smfe,smooth=1):
    ''' smooth是需要平滑掉的max数,平滑方式是用smooth个平均值取代头smooth个最大值
    '''
    ssmfe = np.sort(smfe)
    #print ssmfe
    if smooth > len(ssmfe):
        smooth = len(ssmfe)
    avg_mfe = int(np.average(ssmfe) + 0.5)
    #print avg_mfe,smooth,len(indices)
    sum_smfe =  np.sum(ssmfe[:-smooth]) + smooth * avg_mfe    
    return sum_smfe

def _sum_smooth_mae(smae):
    ''' 对于mae，所有<0的数都平滑成1  '''
    smae[smae < 0]  = 1
    sum_smae = np.sum(smae)
    return sum_smae

def decline(source):
    ''' 计算最大衰落幅度和相应衰弱期(未必是最大衰落期)
    '''
    rsource = source[::-1]
    xmin = min0(rsource)[::-1]  #求逆序的顺序最小值
    amin = len(source)-1-amin0(rsource)[::-1]  #逆序求最小值位置号后转换成顺序值
    smax = source - xmin    #当前值和后续的最小值的差，即衰落幅度
    max_range = np.max(smax)
    max_index = np.where(smax==max_range)[-1][0]  #最后一个为准，符合直观. np.where返回数组的元素是索引号数组，所以需[0]
    min_index = amin[max_index]
    max_period = min_index - max_index  #以交易日为单位的衰落期
    return int(max_range),int(max_period)   #返回值非数组时，必须转换为标准int

def decline_ranges(source,covered=22):    
    ''' 求以covered为顶/底点辐射半径所得到的高低点确定的衰落幅度
        covered默认为辐射半径为月
        返回衰落幅度数组
    '''
    peaks = xpeak_points(source,covered)
    prange = rsub(source,peaks)
    min_peaks = (peaks == -1)   #做选择下标必须是bool类型
    max_ranges = -prange[min_peaks]  #这里的值都是cur_min-pre_max，故此需要取反.
    return max_ranges

def decline_periods(source,covered=22):
    ''' 求以covered为顶/底点辐射半径所得到的高低点确定的衰落期
        covered默认为辐射半径为月
        返回衰落期数组
    '''
    peaks = xpeak_points(source,covered)
    periods = roll0(distance(peaks),1)    #distance计数信号日为0，因此右移一日。右移后距离是信号日起的距离-1
    min_peaks = (peaks == -1) 
    max_periods = periods[min_peaks] + 1 #
    return max_periods

def xmaxmin_points(source,extends,functor,gfunctor,limit):
    ''' 计算最高或最低点,extends为作用范围. 返回值中前extends和后extends位都置0
    '''
    covered = extends * 2 + 1 #最大点必然大于之前的extends个元素和之后的extends个元素
    if(len(source) < covered):
        return np.zeros_like(source)
    peak_values = tmaxmin(source,covered,functor,gfunctor,limit)
    xpeak_values = rollx(peak_values,-extends)
    cores = equals(source,xpeak_values)
    ncores = derepeatc(cores)
    ncores[:extends] = ncores[-extends:] = 0
    return ncores

def xmax_points(source,extends):
    return xmaxmin_points(source,extends,max,np.max,-99999999)

def xmin_points(source,extends):
    return xmaxmin_points(source,extends,min,np.min,99999999)

def xpeak_points_2(shigh,slow,extends):   #高点序列的顶点和底点序列的底点
    ''' 顶点必然不会是底点, 1表示顶点，-1表示底点，0表示中间点. 高低点同时出现，按中间点算
        非常微妙的情况下，也能够处理正确(符合直觉和逻辑)
        self.assertEquals([0,1,-1,1,-1,0],xpeak_points([1,7,6,6,2,8],1))  #[2]的6被计为底点,而[3]的6被计为顶点
        但这类情况当extends为相对大度量时绝对不会在正常情况下出现
        理论上会出现高点和底点同时在一个位置的情形，此时默认为高点.(实际上当extends相对较大时极其少见)
    '''
    return xmax_points(shigh,extends) - xmin_points(slow,extends)

def xpeak_points(source,extends):   #单一序列的顶/底点
    ''' 顶点必然不会是底点, 1表示顶点，-1表示底点，0表示中间点. 高低点同时出现，按中间点算
        非常微妙的情况下，也能够处理正确(符合直觉和逻辑)
        self.assertEquals([0,1,-1,1,-1,0],xpeak_points([1,7,6,6,2,8],1))  #[2]的6被计为底点,而[3]的6被计为顶点
        但这类情况当extends为相对大度量时绝对不会在正常情况下出现
    '''
    return xpeak_points_2(source,source,extends)

