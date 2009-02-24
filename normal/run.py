# -*- coding: utf-8 -*-

#完整的演示脚本

from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *

import logging
logger = logging.getLogger('wolfox.fengine.normal.run')    

def run_body(sdata,dates,begin,end):
    
    from time import time
    tbegin = time()

    pman = AdvancedATRPositionManager()
    dman = DateManager(begin,end)
    myMediator=mediator_factory(trade_strategy=B1S1,pricer = oo_pricer)
    seller = atr_seller_factory(stop_times=2000,trace_times=3000)
    #seller = csc_func
    #pman = AdvancedPositionManager()

    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    #configs.append(config(buyer=fcustom(vama3,fast=12,mid=45,slow=100)))    #mm=2030,times=7

    #-34745 4 [('extend_days', 13), ('fast', 6), ('ma_standard', 227), ('mid', 34), ('slow', 69), ('sma', 21)]
    configs.append(config(buyer=fcustom(svama3,fast=6,mid=34,slow=69,sma=21,ma_standard=227,extend_days=13)))
    #<<lambda>:slow=69,sma=22,ma_standard=227,extend_days=13,fast=6,mid=42:atr_seller:slow=69,sma=22,ma_standard=227,extend_days=13,fast=6,mid=42:make_trade_signal:B1S1>:mm:(30880, 16830, 545, 4)
    configs.append(config(buyer=fcustom(svama3,fast=6,mid=42,slow=69,sma=22,ma_standard=227,extend_days=13)))

    #<<lambda>:slow=34,sma=20,ma_standard=48,extend_days=26,fast=8,mid=90:atr_seller:slow=34,sma=20,ma_standard=48,extend_days=26,fast=8,mid=90:make_trade_signal:B1S1>:mm:(3968, 55501, 13985, 17)
    configs.append(config(buyer=fcustom(svama3,fast=8,mid=90,slow=34,sma=20,ma_standard=48,extend_days=26)))


    configs.append(config(buyer=fcustom(svama3,fast=12,mid=42,slow=127)))    #mm=2489,times=5
    configs.append(config(buyer=fcustom(svama3,fast=15,mid=94,slow=209,sma=24,ma_standard=202,extend_days=30)))    

    configs.append(config(buyer=fcustom(svama3,fast=20,mid=64,slow=119)))    #mm=1622,times=4
    configs.append(config(buyer=fcustom(svama3,fast=23,mid=64,slow=120)))   #mm=1611,times=5    #基本同上

    #svama3:slow=193,sma=129,ma_standard=140,mid=78,fast=35,extend_days=19:atr_seller:slow=193,sma=129,ma_standard=140,mid=78,fast=35,extend_days=19:make_trade_signal:B1S1
    configs.append(config(buyer=fcustom(svama3,fast=35,mid=78,slow=193,sma=129,ma_standard=140,extend_days=19)))
    configs.append(config(buyer=fcustom(svama3,fast=35,mid=80,slow=200,sma=120,ma_standard=140,extend_days=20)))
    #<<lambda>:slow=85,sma=53,ma_standard=65,extend_days=5,fast=38,mid=74:atr_seller:slow=85,sma=53,ma_standard=65,extend_days=5,fast=38,mid=74:make_trade_signal:B1S1>:mm:(5241, 99303, 18945, 26)
    #configs.append(config(buyer=fcustom(svama3,fast=38,mid=74,slow=85,sma=53,ma_standard=65,extend_days=5)))   #1801:20010101-20071231 

    #slow=85,sma=54,ma_standard=64,extend_days=5,fast=44,mid=74:atr_seller:slow=85,sma=54,ma_standard=64,extend_days=5,fast=44,mid=74:make_trade_signal:B1S1>:mm:(3894, 118997, 30557, 33)
    configs.append(config(buyer=fcustom(svama3,fast=44,mid=74,slow=85,sma=54,ma_standard=64,extend_days=5)))    #1834:20010101-20071231 

    #新的一批
    #<<lambda>:slow=238,sma=90,ma_standard=126,extend_days=10,fast=28,mid=58:atr_seller:slow=238,sma=90,ma_standard=126,extend_days=10,fast=28,mid=58:make_trade_signal:B1S1>:mm:(9462, 17647, 1865, 5)
    configs.append(config(buyer=fcustom(svama3,fast=28,mid=58,slow=238,sma=90,ma_standard=126,extend_days=10)))
    #<<lambda>:slow=31,sma=59,ma_standard=35,extend_days=18,fast=44,mid=91:atr_seller:slow=31,sma=59,ma_standard=35,extend_days=18,fast=44,mid=91:make_trade_signal:B1S1>:mm:(4448, 26197, 5889, 8)
    configs.append(config(buyer=fcustom(svama3,fast=44,mid=91,slow=31,sma=59,ma_standard=35,extend_days=18)))
    #<<lambda>:slow=161,sma=62,ma_standard=126,extend_days=5,fast=34,mid=50:atr_seller:slow=161,sma=62,ma_standard=126,extend_days=5,fast=34,mid=50:make_trade_signal:B1S1>:mm:(3003, 49892, 16610, 11)
    configs.append(config(buyer=fcustom(svama3,fast=34,mid=50,slow=161,sma=62,ma_standard=126,extend_days=5)))
    #<<lambda>:slow=161,sma=59,ma_standard=129,extend_days=8,fast=40,mid=53:atr_seller:slow=161,sma=59,ma_standard=129,extend_days=8,fast=40,mid=53:make_trade_signal:B1S1>:mm:(5332, 13742, 2577, 6)
    configs.append(config(buyer=fcustom(svama3,fast=40,mid=53,slow=161,sma=59,ma_standard=129,extend_days=8)))
    #<<lambda>:slow=238,sma=59,ma_standard=126,extend_days=5,fast=40,mid=58:atr_seller:slow=238,sma=59,ma_standard=126,extend_days=5,fast=40,mid=58:make_trade_signal:B1S1>:mm:(3127, 17142, 5481, 7)
    configs.append(config(buyer=fcustom(svama3,fast=40,mid=58,slow=238,sma=59,ma_standard=126,extend_days=5)))

    #<<lambda>:slow=64,sma=102,ma_standard=228,extend_days=14,fast=45,mid=6:atr_seller:slow=64,sma=102,ma_standard=228,extend_days=14,fast=45,mid=6:make_trade_signal:B1S1>:(22750, 8486, 373, 4)
    configs.append(config(buyer=fcustom(svama3,fast=45,mid=6,slow=64,sma=102,ma_standard=228,extend_days=14)))
    #<<lambda>:slow=196,sma=46,ma_standard=132,extend_days=22,fast=27,mid=70:atr_seller:slow=196,sma=46,ma_standard=132,extend_days=22,fast=27,mid=70:make_trade_signal:B1S1>:(27508, 35568, 1293, 2)#
    configs.append(config(buyer=fcustom(svama3,fast=27,mid=70,slow=196,sma=46,ma_standard=132,extend_days=22)))
    ##<<lambda>:slow=122,sma=102,ma_standard=228,extend_days=32,fast=47,mid=7:atr_seller:slow=122,sma=102,ma_standard=228,extend_days=32,fast=47,mid=7:make_trade_signal:B1S1>:(98558, 7589, 77, 2)
    configs.append(config(buyer=fcustom(svama3,fast=47,mid=7,slow=122,sma=102,ma_standard=228,extend_days=32)))
    ##<<lambda>:slow=196,sma=46,ma_standard=132,extend_days=7,fast=27,mid=70:atr_seller:slow=196,sma=46,ma_standard=132,extend_days=7,fast=27,mid=70:make_trade_signal:B1S1>:(15764, 40624, 2577, 4)
    configs.append(config(buyer=fcustom(svama3,fast=27,mid=7,slow=196,sma=46,ma_standard=132,extend_days=7)))    
    ##<<lambda>:slow=122,sma=28,ma_standard=239,extend_days=29,fast=11,mid=23:atr_seller:slow=122,sma=28,ma_standard=239,extend_days=29,fast=11,mid=23:make_trade_signal:B1S1>:(7321, 37698, 5149, 11)
    configs.append(config(buyer=fcustom(svama3,fast=11,mid=23,slow=122,sma=28,ma_standard=239,extend_days=29)))    
    #<<lambda>:slow=122,sma=100,ma_standard=239,extend_days=21,fast=45,mid=87:atr_seller:slow=122,sma=100,ma_standard=239,extend_days=21,fast=45,mid=87:make_trade_signal:B1S1>:(3283, 16557, 5042, 7)
    configs.append(config(buyer=fcustom(svama3,fast=45,mid=87,slow=122,sma=100,ma_standard=239,extend_days=21)))
    ##<<lambda>:slow=196,sma=47,ma_standard=128,extend_days=6,fast=44,mid=86:atr_seller:slow=196,sma=47,ma_standard=128,extend_days=6,fast=44,mid=86:make_trade_signal:B1S1>:(5143, 9387, 1825, 2)
    configs.append(config(buyer=fcustom(svama3,fast=44,id=86,slow=196,sma=47,ma_standard=128,extend_days=6)))
    ##<<lambda>:slow=196,sma=111,ma_standard=240,extend_days=26,fast=12,mid=22:atr_seller:slow=196,sma=111,ma_standard=240,extend_days=26,fast=12,mid=22:make_trade_signal:B1S1>:(2979, 15747, 5286, 6)
    configs.append(config(buyer=fcustom(svama3,fast=12,mid=22,slow=196,sma=111,ma_standard=240,extend_days=26)))
    ##<<lambda>:slow=124,sma=28,ma_standard=236,extend_days=29,fast=1,mid=23:atr_seller:slow=124,sma=28,ma_standard=236,extend_days=29,fast=1,mid=23:make_trade_signal:B1S1>:(2830, 32933, 11635, 12)
    configs.append(config(buyer=fcustom(svama3,fast=1,mid=23,slow=124,sma=28,ma_standard=236,extend_days=29)))    
    ##<<lambda>:slow=45,sma=101,ma_standard=225,extend_days=19,fast=1,mid=6:atr_seller:slow=45,sma=101,ma_standard=225,extend_days=19,fast=1,mid=6:make_trade_signal:B1S1>:(2550, 39291, 15407, 18)
    configs.append(config(buyer=fcustom(svama3,fast=1,mid=6,slow=45,sma=101,ma_standard=225,extend_days=19)))    
    #<<lambda>:slow=66,sma=100,ma_standard=207,extend_days=19,fast=11,mid=23:atr_seller:slow=66,sma=100,ma_standard=207,extend_days=19,fast=11,mid=23:make_trade_signal:B1S1>:(2459, 27465, 11167, 12)
    configs.append(config(buyer=fcustom(svama3,fast=11,mid=23,slow=66,sma=100,ma_standard=207,extend_days=19)))    
    ##<<lambda>:slow=250,sma=28,ma_standard=83,extend_days=32,fast=47,mid=23:atr_seller:slow=250,sma=28,ma_standard=83,extend_days=32,fast=47,mid=23:make_trade_signal:B1S1>:(1993, 40470, 20304, 13)
    configs.append(config(buyer=fcustom(svama3,fast=47,mid=23,slow=250,sma=28,ma_standard=83,extend_days=32)))    
    #<<lambda>:slow=196,sma=48,ma_standard=111,extend_days=6,fast=27,mid=87:atr_seller:slow=196,sma=48,ma_standard=111,extend_days=6,fast=27,mid=87:make_trade_signal:B1S1>:(2008, 28953, 14418, 11)
    configs.append(config(buyer=fcustom(svama3,fast=27,mid=87,slow=196,sma=48,ma_standard=111,extend_days=6)))    
    ##<<lambda>:slow=16,sma=70,ma_standard=228,extend_days=22,fast=33,mid=6:atr_seller:slow=16,sma=70,ma_standard=228,extend_days=22,fast=33,mid=6:make_trade_signal:B1S1>:(1940, 17272, 8899, 8)
    configs.append(config(buyer=fcustom(svama3,fast=33,mid=6,slow=16,sma=70,ma_standard=228,extend_days=22)))
    ##<<lambda>:slow=125,sma=45,ma_standard=17,extend_days=8,fast=1,mid=54:atr_seller:slow=125,sma=45,ma_standard=17,extend_days=8,fast=1,mid=54:make_trade_signal:B1S1>:(1854, 131575, 70943, 49)
    configs.append(config(buyer=fcustom(svama3,fast=1,mid=54,slow=125,sma=45,ma_standard=17,extend_days=8)))    
    ##<<lambda>:slow=132,sma=47,ma_standard=20,extend_days=6,fast=28,mid=46:atr_seller:slow=132,sma=47,ma_standard=20,extend_days=6,fast=28,mid=46:make_trade_signal:B1S1>:(1642, 148830, 90637, 61)
    configs.append(config(buyer=fcustom(svama3,fast=28,mid=46,slow=132,sma=47,ma_standard=20,extend_days=6)))    
    #<<lambda>:slow=101,sma=37,ma_standard=55,extend_days=5,fast=24,mid=55:atr_seller:slow=101,sma=37,ma_standard=55,extend_days=5,fast=24,mid=55:make_trade_signal:B1S1>:(1562, 115000, 73590, 45)
    configs.append(config(buyer=fcustom(svama3,fast=24,mid=55,slow=101,sma=37,ma_standard=55,extend_days=5)))    
    ##<<lambda>:slow=68,sma=92,ma_standard=228,extend_days=21,fast=1,mid=7:atr_seller:slow=68,sma=92,ma_standard=228,extend_days=21,fast=1,mid=7:make_trade_signal:B1S1>:(1516, 50833, 33519, 25)
    configs.append(config(buyer=fcustom(svama3,fast=1,mid=7,slow=68,sma=92,ma_standard=228,extend_days=21)))    
    #<<lambda>:slow=61,sma=109,ma_standard=145,extend_days=21,fast=45,mid=6:atr_seller:slow=61,sma=109,ma_standard=145,extend_days=21,fast=45,mid=6:make_trade_signal:B1S1>:(1512, 32844, 21719, 16)
    configs.append(config(buyer=fcustom(svama3,fast=45,mid=6,slow=61,sma=109,ma_standard=145,extend_days=21)))    
    ##<<lambda>:slow=132,sma=36,ma_standard=9,extend_days=8,fast=2,mid=45:atr_seller:slow=132,sma=36,ma_standard=9,extend_days=8,fast=2,mid=45:make_trade_signal:B1S1>:(1374, 123999, 90234, 56)    
    configs.append(config(buyer=fcustom(svama3,fast=2,mid=45,slow=132,sma=36,ma_standard=9,extend_days=8)))

    #以下是svama2
    configs.append(config(buyer=fcustom(svama2,fast= 19,slow=161,sma= 10,ma_standard=241))) 	#balance=2392,times=  7
    configs.append(config(buyer=fcustom(svama2,fast= 43,slow=176,sma= 74,ma_standard=201))) 	#balance=2524,times=  3
    configs.append(config(buyer=fcustom(svama2,fast= 13,slow= 94,sma= 77,ma_standard=242))) 	#balance=2580,times=  7
    configs.append(config(buyer=fcustom(svama2,fast= 13,slow=176,sma= 69,ma_standard=242))) 	#balance=9290,times=  5
    configs.append(config(buyer=fcustom(svama2,fast= 22,slow=166,sma=  3,ma_standard=229))) 	#balance=44708,times=  8
    configs.append(config(buyer=fcustom(svama2,fast= 15,slow=  7,sma= 92,ma_standard=232))) 	#balance=69244,times=  2
    configs.append(config(buyer=fcustom(svama2,fast= 11,slow=114,sma=108,ma_standard=235))) 	#balance=2139,times=  7
    configs.append(config(buyer=fcustom(svama2,fast= 13,slow=238,sma= 78,ma_standard=232))) 	#balance=2253,times=  6
    configs.append(config(buyer=fcustom(svama2,fast=  7,slow=112,sma= 44,ma_standard=231))) 	#balance=2471,times=  7
    configs.append(config(buyer=fcustom(svama2,fast= 14,slow= 99,sma= 46,ma_standard=244))) 	#balance=2661,times=  8
    configs.append(config(buyer=fcustom(svama2,fast= 35,slow=  9,sma= 31,ma_standard=162))) 	#balance=2794,times=  3
    configs.append(config(buyer=fcustom(svama2,fast=  6,slow=171,sma=105,ma_standard=244))) 	#balance=2854,times=  7
    configs.append(config(buyer=fcustom(svama2,fast= 37,slow=112,sma= 46,ma_standard=232))) 	#balance=3039,times=  4
    configs.append(config(buyer=fcustom(svama2,fast= 16,slow=208,sma=104,ma_standard=235))) 	#balance=3441,times=  2
    configs.append(config(buyer=fcustom(svama2,fast= 15,slow=130,sma= 44,ma_standard=231))) 	#balance=3595,times=  6
    configs.append(config(buyer=fcustom(svama2,fast=  7,slow=207,sma= 40,ma_standard=239))) 	#balance=5461,times=  4
    configs.append(config(buyer=fcustom(svama2,fast= 16,slow=207,sma= 31,ma_standard=242))) 	#balance=5607,times=  3
    configs.append(config(buyer=fcustom(svama2,fast=  5,slow=227,sma=114,ma_standard=241))) 	#balance=6963,times=  3
    configs.append(config(buyer=fcustom(svama2,fast= 13,slow=238,sma= 42,ma_standard=232))) 	#balance=7551,times=  3
    configs.append(config(buyer=fcustom(svama2,fast=  8,slow=240,sma= 44,ma_standard=239))) 	#balance=13349,times=  6
    configs.append(config(buyer=fcustom(svama2,fast= 15,slow=112,sma=108,ma_standard=231))) 	#balance=19177,times=  6
    configs.append(config(buyer=fcustom(svama2,fast=  8,slow= 82,sma= 44,ma_standard=231))) 	#balance=60945,times= 12
    configs.append(config(buyer=fcustom(svama2,fast=  8,slow=114,sma= 44,ma_standard=231))) 	#balance=83106,times=  6
    configs.append(config(buyer=fcustom(svama2,fast=  5,slow=192,sma= 86,ma_standard=240))) 	#balance=2021,times=  5
    configs.append(config(buyer=fcustom(svama2,fast=  5,slow= 48,sma=  6,ma_standard=246))) 	#balance=2030,times=  7
    configs.append(config(buyer=fcustom(svama2,fast= 39,slow=219,sma= 52,ma_standard=222))) 	#balance=2068,times=  6
    configs.append(config(buyer=fcustom(svama2,fast= 18,slow= 59,sma= 11,ma_standard=245))) 	#balance=2267,times=  5
    configs.append(config(buyer=fcustom(svama2,fast=  5,slow=165,sma=  6,ma_standard=232))) 	#balance=2361,times=  6
    configs.append(config(buyer=fcustom(svama2,fast=  7,slow= 35,sma= 52,ma_standard=246))) 	#balance=2419,times=  9
    configs.append(config(buyer=fcustom(svama2,fast=  2,slow=187,sma= 93,ma_standard=237))) 	#balance=2424,times=  3
    configs.append(config(buyer=fcustom(svama2,fast= 35,slow= 64,sma= 10,ma_standard=246))) 	#balance=2461,times=  6
    configs.append(config(buyer=fcustom(svama2,fast= 32,slow= 37,sma= 15,ma_standard=232))) 	#balance=2788,times= 16
    configs.append(config(buyer=fcustom(svama2,fast= 18,slow= 57,sma= 11,ma_standard=245))) 	#balance=2900,times=  4
    configs.append(config(buyer=fcustom(svama2,fast=  3,slow=224,sma= 22,ma_standard=246))) 	#balance=2909,times=  4
    configs.append(config(buyer=fcustom(svama2,fast=  5,slow= 29,sma= 54,ma_standard=232))) 	#balance=3023,times= 16
    configs.append(config(buyer=fcustom(svama2,fast=  3,slow= 59,sma= 22,ma_standard=246))) 	#balance=3105,times=  9
    configs.append(config(buyer=fcustom(svama2,fast= 23,slow=178,sma= 18,ma_standard=232))) 	#balance=3167,times=  5
    configs.append(config(buyer=fcustom(svama2,fast=  3,slow= 32,sma= 54,ma_standard=246))) 	#balance=3234,times=  9
    configs.append(config(buyer=fcustom(svama2,fast= 35,slow=165,sma=  6,ma_standard=224))) 	#balance=3378,times=  1
    configs.append(config(buyer=fcustom(svama2,fast=  3,slow= 96,sma= 54,ma_standard=246))) 	#balance=3491,times=  4
    configs.append(config(buyer=fcustom(svama2,fast=  3,slow= 96,sma= 10,ma_standard=254))) 	#balance=3647,times=  5
    configs.append(config(buyer=fcustom(svama2,fast=  3,slow= 60,sma= 54,ma_standard=254))) 	#balance=6066,times=  7
    configs.append(config(buyer=fcustom(svama2,fast=  7,slow= 59,sma= 18,ma_standard=246))) 	#balance=14098,times=  6
    configs.append(config(buyer=fcustom(svama2,fast=  5,slow=160,sma=  6,ma_standard=232))) 	#balance=15205,times=  7
    configs.append(config(buyer=fcustom(svama2,fast=  1,slow= 36,sma= 54,ma_standard=246))) 	#balance=18967,times=  8
    configs.append(config(buyer=fcustom(svama2,fast= 23,slow=178,sma=  8,ma_standard=232))) 	#balance=28719,times=  8
    configs.append(config(buyer=fcustom(svama2,fast=  8,slow= 53,sma=  8,ma_standard=248))) 	#balance=33910,times=  8
    configs.append(config(buyer=fcustom(svama2,fast=  7,slow= 60,sma=  8,ma_standard=246))) 	#balance=47955,times=  9
    configs.append(config(buyer=fcustom(svama2,fast= 35,slow=219,sma= 52,ma_standard=222))) 	#balance=333488,times=  4

    #以下是svama2s
    configs.append(config(buyer=fcustom(svama2s,fast=  2,slow= 87,sma= 66,ma_standard=224,extend_days= 19))) 	#balance=2005,times= 19
    configs.append(config(buyer=fcustom(svama2s,fast=  5,slow= 97,sma= 63,ma_standard=231,extend_days= 23))) 	#balance=2113,times= 17
    configs.append(config(buyer=fcustom(svama2s,fast= 10,slow= 56,sma=129,ma_standard=234,extend_days= 28))) 	#balance=2148,times= 18
    configs.append(config(buyer=fcustom(svama2s,fast= 10,slow=201,sma= 42,ma_standard=231,extend_days=  8))) 	#balance=2196,times= 12
    configs.append(config(buyer=fcustom(svama2s,fast=  6,slow= 82,sma= 48,ma_standard=231,extend_days= 23))) 	#balance=2293,times= 19
    configs.append(config(buyer=fcustom(svama2s,fast=  1,slow=146,sma=127,ma_standard=228,extend_days=  4))) 	#balance=2364,times= 13
    configs.append(config(buyer=fcustom(svama2s,fast=  7,slow=162,sma= 41,ma_standard=232,extend_days= 30))) 	#balance=2381,times= 13
    configs.append(config(buyer=fcustom(svama2s,fast= 20,slow=100,sma= 65,ma_standard=230,extend_days= 19))) 	#balance=2399,times= 14
    configs.append(config(buyer=fcustom(svama2s,fast= 16,slow= 78,sma= 42,ma_standard=232,extend_days= 23))) 	#balance=2402,times= 20
    configs.append(config(buyer=fcustom(svama2s,fast= 16,slow= 78,sma= 42,ma_standard=232,extend_days= 17))) 	#balance=2402,times= 20
    configs.append(config(buyer=fcustom(svama2s,fast= 13,slow= 79,sma= 41,ma_standard=231,extend_days= 23))) 	#balance=2406,times= 20
    configs.append(config(buyer=fcustom(svama2s,fast=  4,slow= 58,sma=128,ma_standard=234,extend_days= 17))) 	#balance=2457,times= 15
    configs.append(config(buyer=fcustom(svama2s,fast=  8,slow= 98,sma= 64,ma_standard=232,extend_days= 27))) 	#balance=2557,times= 19
    configs.append(config(buyer=fcustom(svama2s,fast=  2,slow= 86,sma= 64,ma_standard=224,extend_days= 14))) 	#balance=2562,times= 19
    configs.append(config(buyer=fcustom(svama2s,fast= 13,slow= 95,sma= 65,ma_standard=231,extend_days= 23))) 	#balance=2565,times= 10
    configs.append(config(buyer=fcustom(svama2s,fast=  8,slow=250,sma=106,ma_standard=231,extend_days= 26))) 	#balance=2600,times=  9
    configs.append(config(buyer=fcustom(svama2s,fast=  8,slow= 75,sma= 41,ma_standard=231,extend_days= 24))) 	#balance=2680,times= 19
    configs.append(config(buyer=fcustom(svama2s,fast=  4,slow=100,sma= 63,ma_standard=254,extend_days= 16))) 	#balance=2766,times=  6
    configs.append(config(buyer=fcustom(svama2s,fast= 16,slow= 74,sma= 42,ma_standard=232,extend_days= 17))) 	#balance=2794,times= 18
    configs.append(config(buyer=fcustom(svama2s,fast= 16,slow= 98,sma= 42,ma_standard=232,extend_days= 17))) 	#balance=2887,times=  8
    configs.append(config(buyer=fcustom(svama2s,fast= 16,slow= 75,sma=128,ma_standard=231,extend_days= 35))) 	#balance=2942,times= 18
    configs.append(config(buyer=fcustom(svama2s,fast=  5,slow= 79,sma= 57,ma_standard=231,extend_days= 23))) 	#balance=2943,times= 20
    configs.append(config(buyer=fcustom(svama2s,fast= 15,slow= 34,sma= 41,ma_standard=232,extend_days= 30))) 	#balance=3140,times= 30
    configs.append(config(buyer=fcustom(svama2s,fast= 11,slow=162,sma= 41,ma_standard=232,extend_days= 30))) 	#balance=3230,times= 19
    configs.append(config(buyer=fcustom(svama2s,fast=  1,slow=146,sma=127,ma_standard=226,extend_days=  3))) 	#balance=3262,times=  8
    configs.append(config(buyer=fcustom(svama2s,fast= 31,slow=162,sma= 41,ma_standard=232,extend_days= 29))) 	#balance=3600,times=  6
    configs.append(config(buyer=fcustom(svama2s,fast=  4,slow= 58,sma=106,ma_standard=232,extend_days= 17))) 	#balance=4453,times= 23
    configs.append(config(buyer=fcustom(svama2s,fast=  5,slow= 82,sma= 64,ma_standard=231,extend_days=  7))) 	#balance=4636,times= 16
    configs.append(config(buyer=fcustom(svama2s,fast=  5,slow= 79,sma= 41,ma_standard=231,extend_days= 27))) 	#balance=5146,times= 18
    configs.append(config(buyer=fcustom(svama2s,fast=  8,slow= 98,sma= 40,ma_standard=232,extend_days= 27))) 	#balance=6217,times= 20
    configs.append(config(buyer=fcustom(svama2s,fast= 15,slow=106,sma= 64,ma_standard=232,extend_days= 26))) 	#balance=8173,times= 11
    configs.append(config(buyer=fcustom(svama2s,fast= 15,slow= 95,sma= 57,ma_standard=232,extend_days= 23))) 	#balance=10557,times= 15
    configs.append(config(buyer=fcustom(svama2s,fast= 15,slow=162,sma= 41,ma_standard=232,extend_days= 14))) 	#balance=183626,times= 17
    configs.append(config(buyer=fcustom(svama2s,fast= 15,slow=162,sma= 41,ma_standard=232,extend_days= 22))) 	#balance=183626,times= 17
    configs.append(config(buyer=fcustom(svama2s,fast= 48,slow=249,sma= 31,ma_standard=165,extend_days= 27))) 	#balance=2184,times= 16
    configs.append(config(buyer=fcustom(svama2s,fast= 16,slow= 57,sma=127,ma_standard=230,extend_days=  5))) 	#balance=2333,times= 20
    configs.append(config(buyer=fcustom(svama2s,fast= 16,slow=105,sma=109,ma_standard=230,extend_days= 27))) 	#balance=2391,times= 11
    configs.append(config(buyer=fcustom(svama2s,fast=  8,slow= 71,sma= 15,ma_standard=225,extend_days= 23))) 	#balance=2833,times= 20
    configs.append(config(buyer=fcustom(svama2s,fast=  8,slow=121,sma= 63,ma_standard=230,extend_days= 23))) 	#balance=2953,times= 12
    configs.append(config(buyer=fcustom(svama2s,fast=  3,slow= 26,sma= 45,ma_standard=245,extend_days=  7))) 	#balance=3171,times= 11
    configs.append(config(buyer=fcustom(svama2s,fast= 44,slow=122,sma=129,ma_standard=230,extend_days=  7))) 	#balance=3540,times= 13
    configs.append(config(buyer=fcustom(svama2s,fast= 32,slow=137,sma=109,ma_standard=230,extend_days= 11))) 	#balance=3830,times=  4
    configs.append(config(buyer=fcustom(svama2s,fast=  8,slow=121,sma= 47,ma_standard=230,extend_days= 23))) 	#balance=3901,times= 14
    configs.append(config(buyer=fcustom(svama2s,fast= 48,slow=121,sma=111,ma_standard=230,extend_days= 25))) 	#balance=4076,times=  9
    configs.append(config(buyer=fcustom(svama2s,fast= 13,slow= 57,sma=127,ma_standard=245,extend_days=  7))) 	#balance=4522,times=  7
    configs.append(config(buyer=fcustom(svama2s,fast= 43,slow= 26,sma=129,ma_standard=230,extend_days= 15))) 	#balance=97969,times=  6
    configs.append(config(buyer=fcustom(svama2s,fast= 19,slow=137,sma= 57,ma_standard=230,extend_days= 11))) 	#balance=2081,times= 11
    configs.append(config(buyer=fcustom(svama2s,fast=  8,slow= 74,sma= 31,ma_standard=230,extend_days=  3))) 	#balance=2185,times= 26
    configs.append(config(buyer=fcustom(svama2s,fast= 24,slow=221,sma= 25,ma_standard=230,extend_days=  7))) 	#balance=2291,times= 10
    configs.append(config(buyer=fcustom(svama2s,fast= 35,slow=153,sma= 25,ma_standard=225,extend_days= 23))) 	#balance=2366,times=  6
    configs.append(config(buyer=fcustom(svama2s,fast= 11,slow= 80,sma= 19,ma_standard=230,extend_days=  3))) 	#balance=2400,times= 23
    configs.append(config(buyer=fcustom(svama2s,fast= 35,slow=  9,sma= 25,ma_standard=230,extend_days= 23))) 	#balance=2654,times=  3
    configs.append(config(buyer=fcustom(svama2s,fast= 40,slow= 77,sma= 25,ma_standard=230,extend_days=  3))) 	#balance=2716,times=  6
    configs.append(config(buyer=fcustom(svama2s,fast= 31,slow= 77,sma= 25,ma_standard=240,extend_days=  3))) 	#balance=2819,times=  7
    configs.append(config(buyer=fcustom(svama2s,fast= 39,slow= 10,sma=121,ma_standard=230,extend_days= 23))) 	#balance=2843,times=  5
    configs.append(config(buyer=fcustom(svama2s,fast=  2,slow=167,sma=121,ma_standard=240,extend_days= 29))) 	#balance=2971,times=  5
    configs.append(config(buyer=fcustom(svama2s,fast=  7,slow= 77,sma= 25,ma_standard=240,extend_days=  3))) 	#balance=3553,times= 11
    configs.append(config(buyer=fcustom(svama2s,fast=  5,slow= 77,sma= 29,ma_standard=240,extend_days=  3))) 	#balance=3840,times=  8
    configs.append(config(buyer=fcustom(svama2s,fast= 34,slow= 79,sma=121,ma_standard=230,extend_days= 25))) 	#balance=5007,times=  6
    configs.append(config(buyer=fcustom(svama2s,fast= 48,slow=222,sma= 33,ma_standard=230,extend_days= 19))) 	#balance=6915,times=  3
    configs.append(config(buyer=fcustom(svama2s,fast= 32,slow=222,sma= 65,ma_standard=230,extend_days=  7))) 	#balance=10299,times=  5
    configs.append(config(buyer=fcustom(svama2s,fast= 35,slow=114,sma=121,ma_standard=230,extend_days= 23))) 	#balance=16644,times=  8
    configs.append(config(buyer=fcustom(svama2s,fast= 35,slow=137,sma= 25,ma_standard=225,extend_days= 11))) 	#balance=129906,times=  5
    configs.append(config(buyer=fcustom(svama2s,fast= 34,slow=143,sma= 25,ma_standard=250,extend_days= 25))) 	#balance=530291,times=  3
    configs.append(config(buyer=fcustom(svama2s,fast= 10,slow= 22,sma= 77,ma_standard=230,extend_days= 23))) 	#balance=2100,times= 26
    configs.append(config(buyer=fcustom(svama2s,fast=  8,slow=217,sma= 33,ma_standard=235,extend_days= 11))) 	#balance=2213,times= 11
    configs.append(config(buyer=fcustom(svama2s,fast= 10,slow=166,sma= 61,ma_standard=230,extend_days=  7))) 	#balance=2505,times= 11
    configs.append(config(buyer=fcustom(svama2s,fast= 18,slow=169,sma= 83,ma_standard=235,extend_days= 33))) 	#balance=2515,times= 11
    configs.append(config(buyer=fcustom(svama2s,fast= 14,slow= 56,sma= 85,ma_standard=230,extend_days= 25))) 	#balance=2798,times= 13
    configs.append(config(buyer=fcustom(svama2s,fast= 12,slow=121,sma= 67,ma_standard=225,extend_days=  5))) 	#balance=2880,times= 15
    configs.append(config(buyer=fcustom(svama2s,fast= 28,slow=233,sma= 59,ma_standard=230,extend_days=  9))) 	#balance=3470,times=  8
    configs.append(config(buyer=fcustom(svama2s,fast= 28,slow=170,sma= 61,ma_standard=240,extend_days=  9))) 	#balance=3606,times=  9
    configs.append(config(buyer=fcustom(svama2s,fast= 14,slow=120,sma=109,ma_standard=230,extend_days= 31))) 	#balance=3917,times= 12
    configs.append(config(buyer=fcustom(svama2s,fast= 10,slow=108,sma= 61,ma_standard=230,extend_days= 25))) 	#balance=4545,times= 16
    configs.append(config(buyer=fcustom(svama2s,fast= 12,slow=105,sma= 59,ma_standard=225,extend_days=  9))) 	#balance=5543,times= 13
    configs.append(config(buyer=fcustom(svama2s,fast= 18,slow=233,sma= 77,ma_standard=240,extend_days= 19))) 	#balance=28567,times=  3
    configs.append(config(buyer=fcustom(svama2s,fast= 28,slow=169,sma= 59,ma_standard=230,extend_days= 11))) 	#balance=81130,times=  9
    
    #以下是vama3
    configs.append(config(buyer=fcustom(vama3,fast=  3,mid=  4,slow= 11,pre_length=200,ma_standard=230,extend_days=  2))) 	#balance=2640,times= 17
    configs.append(config(buyer=fcustom(vama3,fast= 11,mid= 80,slow=181,pre_length=  1,ma_standard= 35,extend_days=  2))) 	#balance=2670,times= 13
    configs.append(config(buyer=fcustom(vama3,fast=  3,mid= 51,slow= 67,pre_length= 11,ma_standard=225,extend_days= 19))) 	#balance=2032,times= 10
    configs.append(config(buyer=fcustom(vama3,fast= 42,mid= 11,slow=236,pre_length=116,ma_standard= 50,extend_days= 21))) 	#balance=2383,times= 18
    configs.append(config(buyer=fcustom(vama3,fast= 43,mid= 51,slow=151,pre_length=171,ma_standard=225,extend_days= 15))) 	#balance=2659,times=  4
    configs.append(config(buyer=fcustom(vama3,fast= 44,mid= 51,slow= 67,pre_length= 11,ma_standard=225,extend_days= 19))) 	#balance=3147,times= 15
    configs.append(config(buyer=fcustom(vama3,fast=  9,mid= 51,slow= 67,pre_length= 11,ma_standard=230,extend_days= 23))) 	#balance=4744,times= 12
    configs.append(config(buyer=fcustom(vama3,fast= 13,mid= 51,slow= 67,pre_length= 11,ma_standard=230,extend_days= 27))) 	#balance=6762,times= 11
    configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 51,slow=195,pre_length= 11,ma_standard=230,extend_days= 15))) 	#balance=10887,times=  4
    configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 51,slow= 67,pre_length= 11,ma_standard=230,extend_days= 15))) 	#balance=13094,times=  9
    configs.append(config(buyer=fcustom(vama3,fast= 43,mid= 51,slow=163,pre_length=171,ma_standard=225,extend_days= 15))) 	#balance=34268,times=  3
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 59,slow=195,pre_length=  6,ma_standard=180,extend_days= 21))) 	#balance=3782,times=  3
    configs.append(config(buyer=fcustom(vama3,fast= 44,mid= 92,slow=  5,pre_length=106,ma_standard= 85,extend_days=  9))) 	#balance=4094,times=  3
    configs.append(config(buyer=fcustom(vama3,fast= 14,mid= 59,slow=175,pre_length=161,ma_standard=240,extend_days=  9))) 	#balance=4763,times=  4
    configs.append(config(buyer=fcustom(vama3,fast= 14,mid= 15,slow=175,pre_length=161,ma_standard=225,extend_days=  9))) 	#balance=5453,times=  8
    configs.append(config(buyer=fcustom(vama3,fast=  9,mid= 15,slow=240,pre_length=171,ma_standard=230,extend_days= 15))) 	#balance=6617,times=  4
    configs.append(config(buyer=fcustom(vama3,fast=  5,mid= 15,slow=176,pre_length=176,ma_standard=230,extend_days= 11))) 	#balance=8807,times=  6
    configs.append(config(buyer=fcustom(vama3,fast=  1,mid= 15,slow=176,pre_length=171,ma_standard=230,extend_days= 15))) 	#balance=22063,times=  5
    configs.append(config(buyer=fcustom(vama3,fast= 14,mid= 59,slow=177,pre_length=161,ma_standard=225,extend_days=  5))) 	#balance=545800,times=  2
    configs.append(config(buyer=fcustom(vama3,fast=  9,mid= 15,slow=176,pre_length=171,ma_standard=230,extend_days= 15))) 	#balance=610740,times=  4
    configs.append(config(buyer=fcustom(vama3,fast= 37,mid= 17,slow=119,pre_length=176,ma_standard= 75,extend_days=  7))) 	#balance=2116,times= 13
    configs.append(config(buyer=fcustom(vama3,fast= 37,mid= 17,slow=247,pre_length=176,ma_standard= 25,extend_days=  7))) 	#balance=2926,times= 24
    configs.append(config(buyer=fcustom(vama3,fast= 38,mid= 17,slow=183,pre_length=176,ma_standard= 35,extend_days=  3))) 	#balance=2970,times=  6
    configs.append(config(buyer=fcustom(vama3,fast= 46,mid= 17,slow=247,pre_length=176,ma_standard= 25,extend_days=  3))) 	#balance=3815,times= 10
    configs.append(config(buyer=fcustom(vama3,fast= 37,mid= 17,slow=247,pre_length=176,ma_standard= 25,extend_days=  3))) 	#balance=11902,times= 13
    configs.append(config(buyer=fcustom(vama3,fast= 16,mid= 17,slow=247,pre_length= 16,ma_standard= 25,extend_days=  1))) 	#balance=12576,times=  2
    configs.append(config(buyer=fcustom(vama3,fast= 36,mid=  9,slow=235,pre_length=171,ma_standard= 20,extend_days= 27))) 	#balance=2035,times= 43
    configs.append(config(buyer=fcustom(vama3,fast= 23,mid= 60,slow= 15,pre_length= 51,ma_standard= 65,extend_days=  9))) 	#balance=2242,times=  4
    configs.append(config(buyer=fcustom(vama3,fast= 36,mid=  7,slow=225,pre_length=171,ma_standard= 20,extend_days= 13))) 	#balance=2308,times= 27
    configs.append(config(buyer=fcustom(vama3,fast=  4,mid= 75,slow=237,pre_length= 26,ma_standard=170,extend_days= 11))) 	#balance=2356,times=  3
    configs.append(config(buyer=fcustom(vama3,fast= 23,mid= 28,slow=143,pre_length=171,ma_standard=180,extend_days= 17))) 	#balance=2364,times= 15
    configs.append(config(buyer=fcustom(vama3,fast= 40,mid=  9,slow=219,pre_length= 46,ma_standard=170,extend_days= 31))) 	#balance=2929,times=  2
    configs.append(config(buyer=fcustom(vama3,fast=  7,mid= 60,slow= 14,pre_length=171,ma_standard= 60,extend_days=  9))) 	#balance=3248,times=  7
    configs.append(config(buyer=fcustom(vama3,fast=  7,mid= 52,slow= 13,pre_length= 56,ma_standard= 60,extend_days=  9))) 	#balance=3262,times=  7
    configs.append(config(buyer=fcustom(vama3,fast=  7,mid= 29,slow=144,pre_length=  6,ma_standard=225,extend_days=  9))) 	#balance=3272,times=  6
    configs.append(config(buyer=fcustom(vama3,fast= 31,mid= 28,slow=143,pre_length=171,ma_standard=180,extend_days= 21))) 	#balance=3553,times=  4
    configs.append(config(buyer=fcustom(vama3,fast=  7,mid= 55,slow= 14,pre_length= 46,ma_standard= 60,extend_days=  5))) 	#balance=4730,times=  6
    configs.append(config(buyer=fcustom(vama3,fast= 23,mid= 28,slow=143,pre_length=171,ma_standard=180,extend_days=  9))) 	#balance=5821,times= 10
    configs.append(config(buyer=fcustom(vama3,fast= 23,mid= 92,slow=143,pre_length=176,ma_standard=180,extend_days=  5))) 	#balance=7901,times=  2
    configs.append(config(buyer=fcustom(vama3,fast=  7,mid= 56,slow= 14,pre_length= 51,ma_standard=180,extend_days=  9))) 	#balance=10663,times=  2
    configs.append(config(buyer=fcustom(vama3,fast= 23,mid= 28,slow=143,pre_length=176,ma_standard=180,extend_days=  5))) 	#balance=10940,times=  5
    configs.append(config(buyer=fcustom(vama3,fast=  5,mid= 25,slow=137,pre_length=156,ma_standard=230,extend_days= 11))) 	#balance=13524,times=  3    

    #以下是vama2

    #configs = [config1,config2,config3]
    #configs = [config3]
    #configs = [config1,config2]
    batch(configs,sdata,dates,begin,cmediator=myMediator)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    

    save_configs('atr_ev_svama3.txt',configs,begin,end)

def run_main(dates,sdata,idata,catalogs,begin,end):
    d_posort('g5',sdata.values(),distance=5)        
    d_posort('g20',sdata.values(),distance=20)    
    d_posort('g120',sdata.values(),distance=120)     
    d_posort('g250',sdata.values(),distance=250)     
    run_body(sdata,dates,begin,end)

def run_mm_main(dates,sdata,idata,catalogs,begin,end):
    d_posort('g5',sdata.values(),distance=5)        
    d_posort('g20',sdata.values(),distance=20)    
    d_posort('g120',sdata.values(),distance=120)     
    d_posort('g250',sdata.values(),distance=250)     
    run_mm_body(sdata,dates,begin,end)

def run_mm_body(sdata,dates,begin,end):
    from time import time
    tbegin = time()

    kvs = dict(fast=15,mid=94,slow=209,sma=24,ma_standard=202,extend_days=30)
    seller = fcustom(atr_seller,**kvs) #atr_seller_factory(stop_times=1500)

    myMediator=MM_Mediator(fcustom(svama3,**kvs),seller)
    trades = myMediator.calc_matched(sdata,dates,begin=tbegin)
    ev = normal_evaluate(trades,**kvs)  
    mm = rate_mfe_mae(sdata)
    logger.debug('%s:mm:%s:%s:%s',myMediator.name(),mm,ev.count,unicode(ev))
    
    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    

    #save_configs('atr_ev_mm_test.txt',configs,begin,end)


if __name__ == '__main__':
    logging.basicConfig(filename="run.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    begin,end = 20010701,20080101
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
    tend = time()
    print u'数据准备耗时: %s' % (tend-tbegin)    
    import psyco
    psyco.full()

    run_main(dates,sdata,idata,catalogs,begin,end)
    #run_mm_main(dates,sdata,idata,catalogs,begin,end)
