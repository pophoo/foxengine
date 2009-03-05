# -*- coding: utf-8 -*-

#完整的演示脚本

from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *

import logging
logger = logging.getLogger('wolfox.fengine.normal.run')    


#1 缩小止损，止损和跟随建议为1600/2400
#2 信号出来后打到55/120均线附近

def prepare_configs_A(seller,pman,dman):    #R>=1000
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    
    #svama3
    configs.append(config(buyer=fcustom(svama3,fast=6,mid=42,slow=69,sma=22,ma_standard=227,extend_days=13)))   #mm:(30880, 16830, 545, 4)  [1461,95,650] 20
    configs.append(config(buyer=fcustom(svama3,fast= 28,mid= 93,slow= 76,sma=113,ma_standard=195,extend_days=  5))) 	#balance=2854,times=  9    # [692,54,333] 9
    configs.append(config(buyer=fcustom(svama3,fast= 29,mid= 58,slow= 12,sma= 65,ma_standard=250,extend_days= 13))) 	#balance=98932,times=  2   # [1000,86,1000] 2
    configs.append(config(buyer=fcustom(svama3,fast= 27,mid= 26,slow= 76,sma= 89,ma_standard=190,extend_days=  5))) 	#balance=3885,times= 24    # [2301,122,576] 26
    configs.append(config(buyer=fcustom(svama3,fast= 29,mid= 26,slow=143,sma= 79,ma_standard=175,extend_days= 19))) 	#balance=4901,times= 11      [1227,108,545] 11
    configs.append(config(buyer=fcustom(svama3,fast= 29,mid= 19,slow=144,sma= 95,ma_standard=175,extend_days=  3))) 	#balance=17630,times= 19   #   [1338,137,700] 20 
    configs.append(config(buyer=fcustom(svama3,fast= 10,mid= 94,slow=156,sma= 73,ma_standard=210,extend_days=  5))) 	#balance=8197,times=  6    ##
    configs.append(config(buyer=fcustom(svama3,fast=  2,mid= 90,slow=175,sma= 11,ma_standard=195,extend_days= 13))) 	#balance=8442,times=  2    ##
    configs.append(config(buyer=fcustom(svama3,fast= 42,mid= 25,slow= 76,sma= 97,ma_standard=195,extend_days=  5))) 	#balance=3049,times= 19
    configs.append(config(buyer=fcustom(svama3,fast= 42,mid= 30,slow= 76,sma= 97,ma_standard=195,extend_days= 35))) 	#balance=5359,times=  5    #
    configs.append(config(buyer=fcustom(svama3,fast= 10,mid= 30,slow=204,sma= 97,ma_standard=230,extend_days=  7))) 	#balance=11440,times=  7   ##

    #svama2
    configs.append(config(buyer=fcustom(svama2,fast=  6,slow=171,sma=105,ma_standard=244))) 	#balance=2854,times=  7
    configs.append(config(buyer=fcustom(svama2,fast= 15,slow=  7,sma= 92,ma_standard=232))) #   #balance=69244,times=  2
    configs.append(config(buyer=fcustom(svama2,fast=  3,slow= 60,sma= 54,ma_standard=254))) #	#balance=6066,times=  7
    configs.append(config(buyer=fcustom(svama2,fast=  3,slow= 97,sma=115,ma_standard= 83))) 	#balance=6713,times=  9


    #以下为svama2s
    configs.append(config(buyer=fcustom(svama2s,fast= 14,slow= 56,sma= 85,ma_standard=230,extend_days= 25))) 	#balance=2798,times= 13
    configs.append(config(buyer=fcustom(svama2s,fast= 48,slow=121,sma=111,ma_standard=230,extend_days= 25))) 	#balance=4076,times=  9

    #vama3
    configs.append(config(buyer=fcustom(vama3,fast= 11,mid= 67,slow=218,pre_length=126,ma_standard=235,extend_days= 25))) 	#balance=3774,times=  9

    #vama2
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow= 27,pre_length=151,ma_standard=225))) 	#balance=9395,times= 23
    configs.append(config(buyer=fcustom(vama2,fast=  1,slow= 23,pre_length=151,ma_standard=225))) 	#balance=9613,times= 18
    
    return configs

def prepare_configs_B(seller,pman,dman): # 400<=R<1000
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    
    #svama3
    configs.append(config(buyer=fcustom(svama3,fast=  7,mid= 23,slow= 66,sma= 77,ma_standard=195,extend_days= 19))) 	#balance=3092,times= 68      [838,52,455] 102
    configs.append(config(buyer=fcustom(svama3,fast= 17,mid= 26,slow=141,sma= 95,ma_standard=245,extend_days=  3))) 	#balance=3092,times= 13    ##
    configs.append(config(buyer=fcustom(svama3,fast= 37,mid= 67,slow=106,sma= 87,ma_standard=245,extend_days=  9))) 	#balance=6402,times=  4    #
    configs.append(config(buyer=fcustom(svama3,fast= 23,mid= 75,slow=222,sma= 19,ma_standard=180,extend_days= 25))) 	#balance=4287,times=  7    #

    #svama2
    configs.append(config(buyer=fcustom(svama2,fast= 18,slow= 57,sma= 11,ma_standard=245))) 	#balance=2900,times=  4
    configs.append(config(buyer=fcustom(svama2,fast=  4,slow= 91,sma=122,ma_standard= 80))) 	#balance=6461,times= 13
    configs.append(config(buyer=fcustom(svama2,fast= 26,slow= 88,sma= 73,ma_standard=238))) 	#balance=2760,times= 35
    configs.append(config(buyer=fcustom(svama2,fast= 27,slow=175,sma= 85,ma_standard= 72))) 	#balance=5523,times= 36
    configs.append(config(buyer=fcustom(svama2,fast=  2,slow=209,sma= 53,ma_standard=200))) #balance=524165,times=5    
    configs.append(config(buyer=fcustom(svama2,fast=  4,slow=128,sma=120,ma_standard= 80))) 	#balance=4648,times= 12
    configs.append(config(buyer=fcustom(svama2,fast= 14,slow=128,sma=120,ma_standard= 84))) 	#balance=5205,times= 28

    #以下为svama2s
    configs.append(config(buyer=fcustom(svama2s,fast= 13,slow= 79,sma= 41,ma_standard=231,extend_days= 23))) 	#balance=2406,times= 20
    configs.append(config(buyer=fcustom(svama2s,fast= 13,slow= 95,sma= 65,ma_standard=231,extend_days= 23))) 	#balance=2565,times= 10
    configs.append(config(buyer=fcustom(svama2s,fast= 15,slow= 95,sma= 57,ma_standard=232,extend_days= 23))) 	#balance=10557,times= 15

    #vama3
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 36,slow= 44,pre_length=  1,ma_standard=240,extend_days=  5))) 	#balance=7077,times=  4
    configs.append(config(buyer=fcustom(vama3,fast= 11,mid= 28,slow= 99,pre_length= 21,ma_standard=160,extend_days= 29))) 	#balance=2760,times= 54

    #vama2
    configs.append(config(buyer=fcustom(vama2,fast=  8,slow=169,pre_length= 66,ma_standard=235))) 	#balance=4984,times= 18
    configs.append(config(buyer=fcustom(vama2,fast= 23,slow=127,pre_length= 36,ma_standard=190))) 	#balance=3913,times= 25
    configs.append(config(buyer=fcustom(vama2,fast=  6,slow=131,pre_length= 26,ma_standard=235))) 	#balance=4702,times= 16
    
    #ma3
    configs.append(config(buyer=fcustom(ma3,fast= 23,mid= 26,slow=150,ma_standard=240,extend_days= 31))) 	#balance=2857,times=1622

    return configs


def prepare_configs(seller,pman,dman):
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    '''
    #svama3
    configs.append(config(buyer=fcustom(svama3,fast=6,mid=42,slow=69,sma=22,ma_standard=227,extend_days=13)))   #mm:(30880, 16830, 545, 4)  [1461,95,650] 20
    configs.append(config(buyer=fcustom(svama3,fast=6,mid=34,slow=69,sma=21,ma_standard=227,extend_days=13)))   #mm:[3239,230,551] 49
    configs.append(config(buyer=fcustom(svama3,fast= 28,mid= 93,slow= 76,sma=113,ma_standard=195,extend_days=  5))) 	#balance=2854,times=  9    # [692,54,333] 9
    configs.append(config(buyer=fcustom(svama3,fast= 29,mid= 58,slow= 12,sma= 65,ma_standard=250,extend_days= 13))) 	#balance=98932,times=  2   # [1000,86,1000] 2
    configs.append(config(buyer=fcustom(svama3,fast= 27,mid= 26,slow= 76,sma= 89,ma_standard=190,extend_days=  5))) 	#balance=3885,times= 24    # [2301,122,576] 26
    configs.append(config(buyer=fcustom(svama3,fast=  7,mid= 23,slow= 66,sma= 77,ma_standard=195,extend_days= 19))) 	#balance=3092,times= 68      [838,52,455] 102
    configs.append(config(buyer=fcustom(svama3,fast= 29,mid= 26,slow=143,sma= 79,ma_standard=175,extend_days= 19))) 	#balance=4901,times= 11      [1227,108,545] 11
    configs.append(config(buyer=fcustom(svama3,fast= 29,mid= 19,slow=144,sma= 95,ma_standard=175,extend_days=  3))) 	#balance=17630,times= 19   #   [1338,137,700] 20 
    configs.append(config(buyer=fcustom(svama3,fast= 17,mid= 26,slow=141,sma= 95,ma_standard=245,extend_days=  3))) 	#balance=3092,times= 13    ##
    configs.append(config(buyer=fcustom(svama3,fast= 10,mid= 94,slow=156,sma= 73,ma_standard=210,extend_days=  5))) 	#balance=8197,times=  6    ##
    configs.append(config(buyer=fcustom(svama3,fast=  2,mid= 90,slow=175,sma= 11,ma_standard=195,extend_days= 13))) 	#balance=8442,times=  2    ##
    configs.append(config(buyer=fcustom(svama3,fast= 37,mid= 67,slow=106,sma= 87,ma_standard=245,extend_days=  9))) 	#balance=6402,times=  4    #
    configs.append(config(buyer=fcustom(svama3,fast= 42,mid= 25,slow= 76,sma= 97,ma_standard=195,extend_days=  5))) 	#balance=3049,times= 19
    configs.append(config(buyer=fcustom(svama3,fast= 42,mid= 30,slow= 76,sma= 97,ma_standard=195,extend_days= 35))) 	#balance=5359,times=  5    #
    configs.append(config(buyer=fcustom(svama3,fast= 39,mid= 57,slow=196,sma=101,ma_standard=180,extend_days= 17))) 	#balance=7971,times= 18
    configs.append(config(buyer=fcustom(svama3,fast=  2,mid= 19,slow=233,sma= 81,ma_standard=245,extend_days= 15))) 	#balance=3648,times= 42
    configs.append(config(buyer=fcustom(svama3,fast= 10,mid= 30,slow=204,sma= 97,ma_standard=230,extend_days=  7))) 	#balance=11440,times=  7   ##
    configs.append(config(buyer=fcustom(svama3,fast= 27,mid= 62,slow= 49,sma= 73,ma_standard=205,extend_days= 31))) 	#balance=3872,times= 16
    configs.append(config(buyer=fcustom(svama3,fast= 23,mid= 75,slow=222,sma= 19,ma_standard=180,extend_days= 25))) 	#balance=4287,times=  7    #
    #svama2
    configs.append(config(buyer=fcustom(svama2,fast=  6,slow=171,sma=105,ma_standard=244))) 	#balance=2854,times=  7
    configs.append(config(buyer=fcustom(svama2,fast= 15,slow=  7,sma= 92,ma_standard=232))) #   #balance=69244,times=  2
    configs.append(config(buyer=fcustom(svama2,fast= 18,slow= 57,sma= 11,ma_standard=245))) 	#balance=2900,times=  4
    configs.append(config(buyer=fcustom(svama2,fast=  8,slow= 66,sma=114,ma_standard= 92))) 	#balance=3082,times= 33
    configs.append(config(buyer=fcustom(svama2,fast=  3,slow= 60,sma= 54,ma_standard=254))) #	#balance=6066,times=  7
    configs.append(config(buyer=fcustom(svama2,fast=  4,slow= 91,sma=122,ma_standard= 80))) 	#balance=6461,times= 13
    configs.append(config(buyer=fcustom(svama2,fast=  3,slow= 97,sma=115,ma_standard= 83))) 	#balance=6713,times=  9
    configs.append(config(buyer=fcustom(svama2,fast= 26,slow= 88,sma= 73,ma_standard=238))) 	#balance=2760,times= 35
    configs.append(config(buyer=fcustom(svama2,fast= 27,slow=175,sma= 85,ma_standard= 72))) 	#balance=5523,times= 36
    configs.append(config(buyer=fcustom(svama2,fast=  8,slow=164,sma=122,ma_standard= 78))) 	#balance=2727,times= 28
    configs.append(config(buyer=fcustom(svama2,fast=  5,slow=166,sma= 53,ma_standard= 79))) 	#balance=3572,times= 15
    configs.append(config(buyer=fcustom(svama2,fast=  8,slow=196,sma= 46,ma_standard=214))) 	#balance=11796,times= 15
    configs.append(config(buyer=fcustom(svama2,fast=  2,slow=209,sma= 53,ma_standard=200))) #balance=524165,times=5    
    configs.append(config(buyer=fcustom(svama2,fast=  4,slow=128,sma=120,ma_standard= 80))) 	#balance=4648,times= 12
    configs.append(config(buyer=fcustom(svama2,fast= 14,slow=128,sma=120,ma_standard= 84))) 	#balance=5205,times= 28
    configs.append(config(buyer=fcustom(svama2,fast= 37,slow=112,sma= 46,ma_standard=232))) 	#balance=3039,times=  4

    #以下为svama2s
    configs.append(config(buyer=fcustom(svama2s,fast= 13,slow= 79,sma= 41,ma_standard=231,extend_days= 23))) 	#balance=2406,times= 20
    configs.append(config(buyer=fcustom(svama2s,fast= 13,slow= 95,sma= 65,ma_standard=231,extend_days= 23))) 	#balance=2565,times= 10
    configs.append(config(buyer=fcustom(svama2s,fast= 14,slow= 56,sma= 85,ma_standard=230,extend_days= 25))) 	#balance=2798,times= 13
    configs.append(config(buyer=fcustom(svama2s,fast=  3,slow= 56,sma= 75,ma_standard=130,extend_days= 19))) 	#balance=2687,times= 43
    configs.append(config(buyer=fcustom(svama2s,fast=  7,slow=155,sma=121,ma_standard=105,extend_days= 17))) 	#balance=7728,times= 34
    configs.append(config(buyer=fcustom(svama2s,fast= 48,slow=121,sma=111,ma_standard=230,extend_days= 25))) 	#balance=4076,times=  9
    configs.append(config(buyer=fcustom(svama2s,fast= 15,slow= 95,sma= 57,ma_standard=232,extend_days= 23))) 	#balance=10557,times= 15

    #vama3
    configs.append(config(buyer=fcustom(vama3,fast=  3,mid= 51,slow= 67,pre_length= 11,ma_standard=225,extend_days= 19))) 	#balance=2032,times= 10
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 36,slow= 44,pre_length=  1,ma_standard=240,extend_days=  5))) 	#balance=7077,times=  4
    configs.append(config(buyer=fcustom(vama3,fast= 15,mid= 73,slow= 31,pre_length= 46,ma_standard=135,extend_days=  5))) 	#balance=6570,times=  4 #
    configs.append(config(buyer=fcustom(vama3,fast= 20,mid= 73,slow= 35,pre_length=101,ma_standard=135,extend_days= 21))) 	#balance=124860,times=  5   #
    configs.append(config(buyer=fcustom(vama3,fast= 15,mid= 76,slow=211,pre_length= 36,ma_standard=200,extend_days= 23))) 	#balance=17956,times=  6    #
    configs.append(config(buyer=fcustom(vama3,fast= 11,mid= 67,slow=218,pre_length=126,ma_standard=235,extend_days= 25))) 	#balance=3774,times=  9
    configs.append(config(buyer=fcustom(vama3,fast= 11,mid= 39,slow=254,pre_length=151,ma_standard=255,extend_days= 33))) 	#balance=3471,times= 22
    configs.append(config(buyer=fcustom(vama3,fast= 13,mid= 20,slow= 81,pre_length=111,ma_standard=255,extend_days= 17))) 	#balance=3245,times= 64
    configs.append(config(buyer=fcustom(vama3,fast= 11,mid= 28,slow= 99,pre_length= 21,ma_standard=160,extend_days= 29))) 	#balance=2760,times= 54

    #vama2
    configs.append(config(buyer=fcustom(vama2,fast=  6,slow=152,pre_length= 71,ma_standard=225))) 	#balance=4537,times=  7
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow=151,pre_length=151,ma_standard=235))) 	#balance=885500,times=  3##
    configs.append(config(buyer=fcustom(vama2,fast=  6,slow=161,pre_length= 66,ma_standard=255))) 	#balance=4347,times= 13
    configs.append(config(buyer=fcustom(vama2,fast=  8,slow=169,pre_length= 66,ma_standard=235))) 	#balance=4984,times= 18
    configs.append(config(buyer=fcustom(vama2,fast= 24,slow=152,pre_length=  1,ma_standard=225))) 	#balance=6746,times=  7
    configs.append(config(buyer=fcustom(vama2,fast=  1,slow=208,pre_length= 46,ma_standard=250))) 	#balance=517134,times=  4
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow=234,pre_length= 46,ma_standard=250))) 	#balance=89137,times=  4
    configs.append(config(buyer=fcustom(vama2,fast=  8,slow=228,pre_length= 61,ma_standard=255))) 	#balance=11032,times= 10
    configs.append(config(buyer=fcustom(vama2,fast= 16,slow=193,pre_length= 76,ma_standard= 35))) 	#balance=3300,times= 24
    configs.append(config(buyer=fcustom(vama2,fast= 42,slow=219,pre_length=196,ma_standard=175))) 	#balance=5216,times= 22
    configs.append(config(buyer=fcustom(vama2,fast=  1,slow=100,pre_length=151,ma_standard=210))) 	#balance=18190,times=  3##
    configs.append(config(buyer=fcustom(vama2,fast=  4,slow= 42,pre_length= 26,ma_standard=250))) 	#balance=277724,times=  5#
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow= 58,pre_length=  6,ma_standard=245))) 	#balance=31915,times=  4
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow= 67,pre_length= 46,ma_standard=245))) 	#balance=21599,times=  7
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow= 27,pre_length=151,ma_standard=225))) 	#balance=9395,times= 23
    configs.append(config(buyer=fcustom(vama2,fast=  1,slow= 23,pre_length=151,ma_standard=225))) 	#balance=9613,times= 18
    configs.append(config(buyer=fcustom(vama2,fast= 23,slow=127,pre_length= 36,ma_standard=190))) 	#balance=3913,times= 25
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow=136,pre_length=141,ma_standard=225))) 	#balance=51614,times=  4#
    configs.append(config(buyer=fcustom(vama2,fast=  6,slow=131,pre_length= 26,ma_standard=235))) 	#balance=4702,times= 16
    configs.append(config(buyer=fcustom(vama2,fast=  4,slow= 89,pre_length= 21,ma_standard=230))) 	#balance=4130,times= 16
    #ma3
    configs.append(config(buyer=fcustom(ma3,fast= 23,mid= 26,slow=150,ma_standard=240,extend_days= 31))) 	#balance=2857,times=1622
    '''

    #svama2x
    configs.append(config(buyer=fcustom(svama2x,base=55,fast=  6,slow=171,sma=105,ma_standard=244))) 	#balance=2854,times=  7
    configs.append(config(buyer=fcustom(svama2x,base=55,fast= 15,slow=  7,sma= 92,ma_standard=232))) #   #balance=69244,times=  2
    configs.append(config(buyer=fcustom(svama2x,base=55,fast= 18,slow= 57,sma= 11,ma_standard=245))) 	#balance=2900,times=  4
    configs.append(config(buyer=fcustom(svama2x,base=55,fast=  8,slow= 66,sma=114,ma_standard= 92))) 	#balance=3082,times= 33
    configs.append(config(buyer=fcustom(svama2x,base=55,fast=  3,slow= 60,sma= 54,ma_standard=254))) #	#balance=6066,times=  7
    configs.append(config(buyer=fcustom(svama2x,base=55,fast=  4,slow= 91,sma=122,ma_standard= 80))) 	#balance=6461,times= 13
    configs.append(config(buyer=fcustom(svama2x,base=55,fast=  3,slow= 97,sma=115,ma_standard= 83))) 	#balance=6713,times=  9
    configs.append(config(buyer=fcustom(svama2x,base=55,fast= 26,slow= 88,sma= 73,ma_standard=238))) 	#balance=2760,times= 35
    configs.append(config(buyer=fcustom(svama2x,base=55,fast= 27,slow=175,sma= 85,ma_standard= 72))) 	#balance=5523,times= 36
    configs.append(config(buyer=fcustom(svama2x,base=55,fast=  8,slow=164,sma=122,ma_standard= 78))) 	#balance=2727,times= 28
    configs.append(config(buyer=fcustom(svama2x,base=55,fast=  5,slow=166,sma= 53,ma_standard= 79))) 	#balance=3572,times= 15
    configs.append(config(buyer=fcustom(svama2x,base=55,fast=  8,slow=196,sma= 46,ma_standard=214))) 	#balance=11796,times= 15
    configs.append(config(buyer=fcustom(svama2x,base=55,fast=  2,slow=209,sma= 53,ma_standard=200))) #balance=524165,times=5    
    configs.append(config(buyer=fcustom(svama2x,base=55,fast=  4,slow=128,sma=120,ma_standard= 80))) 	#balance=4648,times= 12
    configs.append(config(buyer=fcustom(svama2x,base=55,fast= 14,slow=128,sma=120,ma_standard= 84))) 	#balance=5205,times= 28
    configs.append(config(buyer=fcustom(svama2x,base=55,fast= 37,slow=112,sma= 46,ma_standard=232))) 	#balance=3039,times=  4
    
    return configs

def prepare_order(sdata):
    d_posort('g5',sdata,distance=5)        
    d_posort('g20',sdata,distance=20)    
    d_posort('g120',sdata,distance=120)     
    d_posort('g250',sdata,distance=250)     

def run_body(sdata,dates,begin,end,xbegin):
    
    from time import time
    tbegin = time()

    pman = AdvancedATRPositionManager()
    dman = DateManager(begin,end)
    myMediator=mediator_factory(trade_strategy=B1S1,pricer = oo_pricer)
    #seller = atr_seller_factory(stop_times=2000,trace_times=3000)
    #seller = atr_seller_factory(stop_times=1500,trace_times=3000)
    #seller = atr_seller_factory(stop_times=1000,trace_times=3000)
    seller = atr_seller_factory(stop_times=600,trace_times=3000)
    #seller = csc_func
    #seller = fcustom(csc_func,threshold=100)

    configs = prepare_configs(seller,pman,dman)
    batch(configs,sdata,dates,xbegin,cmediator=myMediator)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    

    save_configs('atr_ev.txt',configs,xbegin,end)

def run_merge_body(sdata,dates,begin,end,xbegin):
    
    from time import time
    tbegin = time()

    pman = AdvancedATRPositionManager()
    dman = DateManager(begin,end)
    myMediator=mediator_factory(trade_strategy=B1S1,pricer = oo_pricer)
    seller = atr_seller_factory(stop_times=2000,trace_times=3000)
    #seller = csc_func

    configs = prepare_configs(seller,pman,dman)
    result,strade = merge(configs,sdata,dates,xbegin,pman,dman,cmediator=myMediator)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    
    save_merged('atr_merged.txt',result,strade,xbegin,end)

def run_mm_body(sdata,dates,begin,end,xbegin):
    from time import time
    tbegin = time()

    #kvs = dict(fast=15,mid=94,slow=209,sma=24,ma_standard=202,extend_days=30)
    #seller = fcustom(atr_seller,**kvs) #atr_seller_factory(stop_times=1500)
    seller = atr_seller_factory()
    myMediator=MM_Mediator
    configs = prepare_configs(seller,None,None)
    
    mm_batch(configs,sdata,dates,xbegin)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    

    save_mm_configs('mm_ev.txt',configs,xbegin,end)
    #save_configs('atr_ev_mm_test.txt',configs,begin,end)

def run_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata.values())
    prepare_order(catalogs)
    dummy_catalogs('catalog',catalogs)
    run_body(sdata,dates,begin,end,xbegin)

def run_merge_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata.values())
    prepare_order(catalogs)    
    run_merge_body(sdata,dates,begin,end,xbegin)

def run_mm_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata.values())
    prepare_order(catalogs)    
    run_mm_body(sdata,dates,begin,end,xbegin)

def run_last(dates,sdata,idata,catalogs,begin,end,xbegin,lbegin=0):
    prepare_order(sdata.values())
    prepare_order(catalogs)    
    from time import time
    tbegin = time()

    pman = None
    dman = None
    myMediator=mediator_factory(trade_strategy=B1S1,pricer = oo_pricer)
    #seller = atr_seller_factory(stop_times=2000,trace_times=3000)
    seller = atr_seller_factory(stop_times=600,trace_times=3000)
    #seller = csc_func
    if lbegin == 0:
        lbegin = end - 5

    configs_a = prepare_configs_A(seller,pman,dman)
    dtrades_a = batch_last(configs_a,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_a.txt',dtrades_a,xbegin,end,lbegin)

    configs_b = prepare_configs_B(seller,pman,dman)
    dtrades_b = batch_last(configs_b,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_b.txt',dtrades_b,xbegin,end,lbegin)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    


if __name__ == '__main__':
    logging.basicConfig(filename="run_x4a.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    #测试时间段 [19980101,19990101-20010801],[20000101,20010701-20050901],[20040601,20050801-20071031],[20060601,20071031-20090101]
    #总时间段   [20000101,20010701,20090101]    #一个完整的周期+一个下降段
    #分段测试的要求，段mm > 1000-1500或抑制，总段mm > 2000
    
    begin,xbegin,end = 20000101,20010701,20090101
    #begin,xbegin,end = 19980101,19990701,20010801    
    #begin,xbegin,end = 20040601,20050801,20071031
    #begin,xbegin,end = 20060601,20071031,20090101
    #begin,xbegin,end = 19980101,19990101,20090101
    #begin,xbegin,end,lbegin = 20070101,20080601,20090327,20080601
    from time import time
    tbegin = time()
    
    dates,sdata,idata,catalogs = prepare_all(begin,end,[],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH601988','SH600050'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH601988'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH601398'],[ref_code])        
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SZ000630'],[ref_code])        
    #dates,sdata,idata,catalogs = prepare_all(begin,end,get_codes(),[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,get_codes(source='SZSE'),[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SZ000792'],[ref_code])            
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600888'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SZ000020'],[ref_code])
    tend = time()
    print u'数据准备耗时: %s' % (tend-tbegin)    
    import psyco
    psyco.full()

    run_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    #run_merge_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    #run_mm_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    run_last(dates,sdata,idata,catalogs,begin,end,xbegin,lbegin)

    #prepare_order(sdata.values())
    #prepare_order(catalogs)
    #dummy_catalogs('catalog',catalogs)
    #for c in sdata[816].catalog:
    #    print c.name,c.g20
