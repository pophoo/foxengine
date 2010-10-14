# -*- coding: utf-8 -*-

'''
#速度
sma_n = ma_n-rollx(ma_n)  n分钟的平均速度
ama_n = sma_n - rollx(sma_n) n分钟的加速度


    参数优化方法的结果
'''

from wolfox.fengine.ifuture.ibase import *
from wolfox.fengine.ifuture.iftrade import *

##第一类方法，直接参数优化后，不需要其它条件


##第二类方法，添加一般条件

#macd
def macd1x(sif,ifast=17,islow=33,idiff=25):
    ''' 
        17-65-13
        9-49-7  #
        5-41-13 #
        29-153-19   #
        17-33-25
        57-257-13   #
        45-265-19
        57-105-13   #
        49-121-13
        37-129-19   #
        33-257-7    #
        33-177-7    #
        48-137-13   #
        57-161/153-7    ##
        21-250-13
        45-129-13   #
        5-233-7 #?#

                
    '''
    diff,dea = cmacd(sif.close * 10,ifast=ifast,islow=islow,idiff=idiff)
    signal = gand(cross(dea,diff)>0,strend2(diff)>0)
    signal = gand(signal
                #,sif.s30>0
                ,sif.smacd15x > 0
                ,sif.smacd5x < 0
                #,strend2(sif.ma30)>0
                #,sif.xatr<sif.mxatr
                #,strend2(sif.mxatr30x)<0
                )
    return signal
macd1x.direction = XBUY
macd1x.priority = 1500

msb_a = fcustom(macd1x,ifast=17,islow=65,idiff=13)





