# -*- coding: utf-8 -*-

#完整的运行脚本

from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *

import logging
logger = logging.getLogger('wolfox.fengine.normal.run')    


#1 缩小止损，止损和跟随建议为1600/2400
#2 信号出来后打到55/120均线附近

def prepare_temp_configs(seller,pman=None,dman=None):
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []

    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid= 13,slow=290,rstart=2000,rend=8000))) 	#balance=1012,times= 23
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 29,slow=390,rstart=4500,rend=8000))) 	#balance=1062,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid= 18,slow=245,rstart=2000,rend=7500))) 	#balance=1097,times= 21
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid= 21,slow=250,rstart=7500,rend=8000))) 	#balance=1156,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid= 21,slow=250,rstart=2000,rend=8000))) 	#balance=1043,times= 16
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 21,slow=245,rstart=3000,rend=8000))) 	#balance=1180,times= 23
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 21,slow=385,rstart=1500,rend=8000))) 	#balance=1190,times= 18
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid= 14,slow=320,rstart=7000,rend=10000))) 	#balance=1268,times= 20
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 19,slow=270,rstart=2000,rend=8000))) 	#balance=1301,times= 24
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 23,slow=250,rstart=5000,rend=8000))) 	#balance=1346,times= 13
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 29,slow=270,rstart=7500,rend=8000))) 	#balance=1350,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  3,mid= 31,slow= 95,rstart=8000,rend=9500))) 	#balance=1358,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 23,slow=250,rstart=3500,rend=8000))) 	#balance=1367,times= 17
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid= 21,slow=250,rstart=7000,rend=8500))) 	#balance=1386,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 21,slow=250,rstart=5500,rend=8000))) 	#balance=1428,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid= 85,slow=250,rstart=5000,rend=8000))) 	#balance=1519,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 27,slow=270,rstart=7500,rend=8000))) 	#balance=1544,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 19,slow=250,rstart=7000,rend=8000))) 	#balance=1554,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 23,slow=250,rstart=6500,rend=8000))) 	#balance=1577,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 21,slow=250,rstart=6500,rend=8000))) 	#balance=1577,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 21,slow=270,rstart=7500,rend=8000))) 	#balance=1873,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 27,slow=250,rstart=5000,rend=8000))) 	#balance=1899,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 25,slow=250,rstart=7000,rend=8000))) 	#balance=1937,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 23,slow=250,rstart=7000,rend=8000))) 	#balance=1937,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 21,slow=250,rstart=7000,rend=8000))) 	#balance=1937,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid= 25,slow=250,rstart=6000,rend=8000))) 	#balance=2130,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 27,slow=330,rstart=3000,rend=6000))) 	#balance=2437,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 21,slow=290,rstart=7500,rend=8000))) 	#balance=2518,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 19,slow=245,rstart=7500,rend=8000))) 	#balance=2623,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 27,slow=250,rstart=7500,rend=8000))) 	#balance=3184,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid= 25,slow=250,rstart=7500,rend=8000))) 	#balance=3184,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid= 21,slow=250,rstart=7500,rend=8000))) 	#balance=3184,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 23,slow=270,rstart=7500,rend=8000))) 	#balance=3445,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 11,mid= 19,slow=250,rstart=7500,rend=8000))) 	#balance=4800,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid= 25,slow=250,rstart=7500,rend=8000))) 	#balance=5492,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  9,mid= 93,slow=395,rstart=2500,rend=7500))) 	#balance=6045,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 21,slow=250,rstart=7500,rend=8000))) 	#balance=6826,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 33,mid= 83,slow=280,rstart=  0,rend=6000))) 	#balance=12607,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 11,mid= 74,slow=210,rstart=3000,rend=5500))) 	#balance=12926,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 31,slow=415,rstart=2500,rend=5500))) 	#balance=13274,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 85,slow=165,rstart=5000,rend=5500))) 	#balance=16531,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 18,mid= 66,slow= 20,rstart=3500,rend=5500))) 	#balance=16531,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid= 59,slow=350,rstart=3000,rend=6000))) 	#balance=3291000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid= 91,slow=330,rstart=4500,rend=6000))) 	#balance=4739000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 27,slow=350,rstart=4500,rend=6000))) 	#balance=5850000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 44,mid= 23,slow=250,rstart=7500,rend=8000))) 	#balance=7664000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 43,mid= 67,slow=435,rstart=500,rend=3500))) 	#balance=10923000,times=  1    
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid= 13,slow=290,rstart=2000,rend=8000))) 	#balance=1012,times= 23
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid= 21,slow=250,rstart=2000,rend=8000))) 	#balance=1043,times= 16
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 29,slow=390,rstart=4500,rend=8000))) 	#balance=1062,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid= 18,slow=245,rstart=2000,rend=7500))) 	#balance=1097,times= 21
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid= 21,slow=250,rstart=7500,rend=8000))) 	#balance=1156,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 21,slow=245,rstart=3000,rend=8000))) 	#balance=1180,times= 23
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 21,slow=385,rstart=1500,rend=8000))) 	#balance=1190,times= 18
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid= 14,slow=320,rstart=7000,rend=10000))) 	#balance=1268,times= 20
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 19,slow=270,rstart=2000,rend=8000))) 	#balance=1301,times= 24
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 23,slow=250,rstart=5000,rend=8000))) 	#balance=1346,times= 13
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 29,slow=270,rstart=7500,rend=8000))) 	#balance=1350,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  3,mid= 31,slow= 95,rstart=8000,rend=9500))) 	#balance=1358,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 23,slow=250,rstart=3500,rend=8000))) 	#balance=1367,times= 17
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid= 21,slow=250,rstart=7000,rend=8500))) 	#balance=1386,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 21,slow=250,rstart=5500,rend=8000))) 	#balance=1428,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid= 85,slow=250,rstart=5000,rend=8000))) 	#balance=1519,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 27,slow=270,rstart=7500,rend=8000))) 	#balance=1544,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 19,slow=250,rstart=7000,rend=8000))) 	#balance=1554,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 23,slow=250,rstart=6500,rend=8000))) 	#balance=1577,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 21,slow=250,rstart=6500,rend=8000))) 	#balance=1577,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 21,slow=270,rstart=7500,rend=8000))) 	#balance=1873,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 27,slow=250,rstart=5000,rend=8000))) 	#balance=1899,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 25,slow=250,rstart=7000,rend=8000))) 	#balance=1937,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 23,slow=245,rstart=7000,rend=8000))) 	#balance=1937,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 23,slow=250,rstart=7000,rend=8000))) 	#balance=1937,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 21,slow=250,rstart=7000,rend=8000))) 	#balance=1937,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid= 25,slow=250,rstart=6000,rend=8000))) 	#balance=2130,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 27,slow=330,rstart=3000,rend=6000))) 	#balance=2437,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 21,slow=290,rstart=7500,rend=8000))) 	#balance=2518,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 19,slow=245,rstart=7500,rend=8000))) 	#balance=2623,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 27,slow=250,rstart=7500,rend=8000))) 	#balance=3184,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid= 25,slow=250,rstart=7500,rend=8000))) 	#balance=3184,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid= 21,slow=250,rstart=7500,rend=8000))) 	#balance=3184,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 23,slow=270,rstart=7500,rend=8000))) 	#balance=3445,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 11,mid= 19,slow=250,rstart=7500,rend=8000))) 	#balance=4800,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid= 25,slow=250,rstart=7500,rend=8000))) 	#balance=5492,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  9,mid= 93,slow=395,rstart=2500,rend=7500))) 	#balance=6045,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 21,slow=250,rstart=7500,rend=8000))) 	#balance=6826,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 33,mid= 83,slow=280,rstart=  0,rend=6000))) 	#balance=12607,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 11,mid= 74,slow=210,rstart=3000,rend=5500))) 	#balance=12926,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 31,slow=415,rstart=2500,rend=5500))) 	#balance=13274,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 85,slow=165,rstart=5000,rend=5500))) 	#balance=16531,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 18,mid= 66,slow= 20,rstart=3500,rend=5500))) 	#balance=16531,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid= 59,slow=350,rstart=3000,rend=6000))) 	#balance=3291000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid= 91,slow=330,rstart=4500,rend=6000))) 	#balance=4739000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 27,slow=350,rstart=4500,rend=6000))) 	#balance=5850000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 44,mid= 23,slow=250,rstart=7500,rend=8000))) 	#balance=7664000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 43,mid= 67,slow=435,rstart=500,rend=3500))) 	#balance=10923000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid= 28,slow= 65,rstart=4500,rend=6000))) 	#balance=1041,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid= 64,slow=185,rstart=3000,rend=10000))) 	#balance=2212,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 30,mid= 93,slow=410,rstart=1500,rend=6000))) 	#balance=2832,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 76,slow=410,rstart=3500,rend=8500))) 	#balance=8861,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 27,mid= 42,slow=195,rstart=3500,rend=9500))) 	#balance=1040,times= 15
    configs.append(config(buyer=fcustom(csvama3,fast= 33,mid=  5,slow= 40,rstart=2000,rend=4500))) 	#balance=1047,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid= 30,slow= 70,rstart=4000,rend=8500))) 	#balance=1112,times= 16
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid= 11,slow=145,rstart=7500,rend=8500))) 	#balance=1150,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid= 39,slow=325,rstart=4500,rend=8500))) 	#balance=1241,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=  5,slow= 25,rstart=4500,rend=5500))) 	#balance=1266,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 28,mid= 43,slow=205,rstart=2000,rend=8500))) 	#balance=1349,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast= 31,mid= 37,slow=235,rstart=1500,rend=6000))) 	#balance=1430,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 19,mid= 42,slow=195,rstart=3500,rend=6500))) 	#balance=1663,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid=  9,slow=285,rstart=3500,rend=8500))) 	#balance=1668,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid= 30,slow= 50,rstart=4000,rend=5500))) 	#balance=1704,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 33,mid=  8,slow= 30,rstart=2000,rend=5500))) 	#balance=1770,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 52,slow=170,rstart=500,rend=9000))) 	#balance=1791,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 33,mid=  9,slow= 40,rstart=2500,rend=4500))) 	#balance=1805,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 15,mid=  8,slow=275,rstart=5000,rend=9500))) 	#balance=2323,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast= 15,mid= 11,slow= 65,rstart=1500,rend=8500))) 	#balance=2351,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid=  4,slow=355,rstart=  0,rend=4000))) 	#balance=2952,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 27,mid= 15,slow= 20,rstart=4500,rend=5000))) 	#balance=3578,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 19,mid= 79,slow=300,rstart=4500,rend=7000))) 	#balance=3648,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 19,mid=  5,slow= 15,rstart=2500,rend=5000))) 	#balance=3831,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 11,mid= 79,slow=485,rstart=500,rend=9000))) 	#balance=3901,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 39,mid= 50,slow=275,rstart=3500,rend=4500))) 	#balance=5415,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 44,mid= 70,slow= 60,rstart=7000,rend=8000))) 	#balance=10930,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 15,mid= 23,slow=400,rstart=1500,rend=3000))) 	#balance=4203000,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 28,mid= 15,slow=445,rstart=2500,rend=4000))) 	#balance=4203000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 23,mid= 11,slow=305,rstart=5500,rend=6500))) 	#balance=6087000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 25,slow=420,rstart=4000,rend=8000))) 	#balance=1000,times= 14
    configs.append(config(buyer=fcustom(csvama3,fast= 37,mid= 49,slow=220,rstart=1500,rend=10000))) 	#balance=1000,times= 24
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 91,slow=380,rstart=1500,rend=8000))) 	#balance=1022,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 46,mid= 50,slow=165,rstart=5500,rend=10000))) 	#balance=1040,times= 20
    configs.append(config(buyer=fcustom(csvama3,fast= 47,mid= 82,slow= 90,rstart=5000,rend=9500))) 	#balance=1045,times= 17
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid= 45,slow=185,rstart=1000,rend=9000))) 	#balance=1046,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast= 24,mid= 51,slow=200,rstart=5500,rend=9500))) 	#balance=1081,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid= 51,slow=200,rstart=1000,rend=10000))) 	#balance=1081,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast= 11,mid= 24,slow=405,rstart=  0,rend=8000))) 	#balance=1087,times= 15
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 50,slow=245,rstart=500,rend=9500))) 	#balance=1106,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 23,mid= 46,slow=190,rstart=2000,rend=9500))) 	#balance=1141,times= 13
    configs.append(config(buyer=fcustom(csvama3,fast= 15,mid= 49,slow=190,rstart=1000,rend=9500))) 	#balance=1178,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid= 48,slow=165,rstart=500,rend=10000))) 	#balance=1222,times= 18
    configs.append(config(buyer=fcustom(csvama3,fast= 21,mid= 50,slow= 90,rstart=1500,rend=10000))) 	#balance=1234,times= 30
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid= 84,slow= 90,rstart=4000,rend=10000))) 	#balance=1234,times= 15
    configs.append(config(buyer=fcustom(csvama3,fast= 47,mid= 50,slow=190,rstart=  0,rend=9500))) 	#balance=1276,times= 22
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 25,slow=410,rstart=5500,rend=9000))) 	#balance=1278,times= 15
    configs.append(config(buyer=fcustom(csvama3,fast= 38,mid= 49,slow=190,rstart=1000,rend=9500))) 	#balance=1279,times= 25
    configs.append(config(buyer=fcustom(csvama3,fast= 38,mid= 50,slow=185,rstart=1500,rend=10000))) 	#balance=1298,times= 30
    configs.append(config(buyer=fcustom(csvama3,fast= 37,mid= 59,slow=200,rstart=5500,rend=9500))) 	#balance=1335,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid= 83,slow= 90,rstart=5500,rend=10000))) 	#balance=1338,times= 15
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid= 58,slow=190,rstart=1000,rend=10000))) 	#balance=1357,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast= 47,mid= 83,slow=100,rstart=5500,rend=9500))) 	#balance=1382,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 81,slow=430,rstart=2500,rend=9000))) 	#balance=1391,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast= 48,mid= 49,slow=190,rstart=1500,rend=9500))) 	#balance=1392,times= 15
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid= 17,slow=410,rstart=1500,rend=8000))) 	#balance=1424,times= 15
    configs.append(config(buyer=fcustom(csvama3,fast= 15,mid= 17,slow=420,rstart=5500,rend=7500))) 	#balance=1463,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast= 47,mid= 49,slow=190,rstart=1000,rend=9500))) 	#balance=1471,times= 24
    configs.append(config(buyer=fcustom(csvama3,fast= 47,mid= 49,slow=190,rstart=1500,rend=9500))) 	#balance=1471,times= 24
    configs.append(config(buyer=fcustom(csvama3,fast= 47,mid= 50,slow=190,rstart=6000,rend=9500))) 	#balance=1479,times= 18
    configs.append(config(buyer=fcustom(csvama3,fast= 15,mid= 93,slow=350,rstart=1000,rend=7500))) 	#balance=1489,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 19,mid= 48,slow=170,rstart=  0,rend=10000))) 	#balance=1493,times= 17
    configs.append(config(buyer=fcustom(csvama3,fast= 32,mid= 83,slow=100,rstart=5500,rend=9500))) 	#balance=1509,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast= 11,mid= 92,slow=380,rstart=  0,rend=8000))) 	#balance=1529,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 83,slow=420,rstart=5500,rend=8000))) 	#balance=1538,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid= 82,slow= 90,rstart=5500,rend=10000))) 	#balance=1545,times= 14
    configs.append(config(buyer=fcustom(csvama3,fast= 23,mid= 83,slow= 90,rstart=5500,rend=9500))) 	#balance=1554,times= 15
    configs.append(config(buyer=fcustom(csvama3,fast= 11,mid= 80,slow=410,rstart=1500,rend=9000))) 	#balance=1582,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast= 11,mid= 78,slow=405,rstart=3000,rend=9000))) 	#balance=1621,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast= 21,mid= 81,slow= 90,rstart=5000,rend=10000))) 	#balance=1629,times= 16
    configs.append(config(buyer=fcustom(csvama3,fast= 21,mid= 82,slow= 90,rstart=5500,rend=10000))) 	#balance=1675,times= 13
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid= 27,slow=405,rstart=6000,rend=8000))) 	#balance=1685,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 82,slow=405,rstart=5500,rend=10000))) 	#balance=1685,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 46,mid= 53,slow=190,rstart=5000,rend=10000))) 	#balance=1782,times= 21
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 27,slow=405,rstart=6000,rend=9000))) 	#balance=1884,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid= 49,slow=190,rstart=1000,rend=10000))) 	#balance=1913,times= 14
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid= 24,slow=405,rstart=5500,rend=8000))) 	#balance=1962,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 49,slow=190,rstart=1000,rend=10000))) 	#balance=1990,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast= 48,mid= 51,slow=200,rstart=1500,rend=9500))) 	#balance=2142,times= 19
    configs.append(config(buyer=fcustom(csvama3,fast= 48,mid= 51,slow=200,rstart=1000,rend=9500))) 	#balance=2142,times= 19
    configs.append(config(buyer=fcustom(csvama3,fast= 32,mid= 51,slow=200,rstart=1500,rend=10000))) 	#balance=2155,times= 15
    configs.append(config(buyer=fcustom(csvama3,fast= 47,mid= 51,slow=200,rstart=6500,rend=9500))) 	#balance=2361,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast= 15,mid= 81,slow=380,rstart=1000,rend=5500))) 	#balance=2456,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid= 25,slow=410,rstart=5500,rend=8000))) 	#balance=2706,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 40,mid= 51,slow=200,rstart=7500,rend=9500))) 	#balance=2794,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 21,mid= 82,slow= 85,rstart=5500,rend=10000))) 	#balance=2860,times= 13
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid= 82,slow= 85,rstart=5500,rend=10000))) 	#balance=2978,times= 14
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid= 83,slow=420,rstart=5500,rend=7500))) 	#balance=3697,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid= 83,slow=410,rstart=5500,rend=9500))) 	#balance=3964,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast= 45,mid= 88,slow=295,rstart=5500,rend=7000))) 	#balance=4876,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 93,slow=350,rstart=2000,rend=7000))) 	#balance=10444,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 11,mid= 82,slow=410,rstart=5500,rend=6000))) 	#balance=22734,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 36,slow=425,rstart=6500,rend=8000))) 	#balance=6684000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid=425,slow=830,rstart=  0,rend=9500))) 	#balance=1000,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=215,mid=430,slow=485,rstart=4500,rend=10000))) 	#balance=1000,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=225,slow=1110,rstart=8000,rend=9500))) 	#balance=1006,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid= 84,slow=1140,rstart=2500,rend=9000))) 	#balance=1006,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=255,mid=275,slow=510,rstart=4500,rend=9500))) 	#balance=1008,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid=290,slow=1200,rstart=  0,rend=10000))) 	#balance=1009,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=215,mid=400,slow=1810,rstart=6500,rend=9500))) 	#balance=1013,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=215,slow=790,rstart=2500,rend=9000))) 	#balance=1013,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=100,mid=148,slow=1110,rstart=1000,rend=10000))) 	#balance=1014,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=240,mid=305,slow=510,rstart=3500,rend=10000))) 	#balance=1019,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=455,slow=960,rstart=4500,rend=9000))) 	#balance=1022,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  9,mid=300,slow=950,rstart=  0,rend=9500))) 	#balance=1022,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=455,slow=960,rstart=  0,rend=9000))) 	#balance=1022,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=100,mid=148,slow=1120,rstart=4500,rend=9500))) 	#balance=1028,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid=375,slow=820,rstart=3000,rend=10000))) 	#balance=1028,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=148,slow=1110,rstart=2500,rend=9000))) 	#balance=1038,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=148,slow=1110,rstart=  0,rend=9000))) 	#balance=1038,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=705,slow=790,rstart=2500,rend=8500))) 	#balance=1047,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 42,slow=950,rstart=  0,rend=9500))) 	#balance=1047,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 26,mid=215,slow=1030,rstart=6500,rend=9000))) 	#balance=1050,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=100,mid=225,slow=790,rstart=  0,rend=9000))) 	#balance=1050,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=128,mid=300,slow=950,rstart=1500,rend=10000))) 	#balance=1056,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=255,mid=415,slow=790,rstart=500,rend=9500))) 	#balance=1063,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=480,mid=505,slow=530,rstart=4500,rend=9500))) 	#balance=1066,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid= 84,slow=1120,rstart=  0,rend=9000))) 	#balance=1067,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid= 84,slow=1030,rstart=2500,rend=10000))) 	#balance=1089,times= 18
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid= 84,slow=1030,rstart=  0,rend=10000))) 	#balance=1089,times= 18
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=225,slow=1030,rstart=8000,rend=9000))) 	#balance=1091,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=215,slow=1030,rstart=8000,rend=8500))) 	#balance=1091,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=200,mid=225,slow=1030,rstart=  0,rend=9000))) 	#balance=1091,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 26,mid=215,slow=1030,rstart=7500,rend=9000))) 	#balance=1091,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid= 84,slow=1110,rstart=  0,rend=8500))) 	#balance=1094,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid=215,slow=1030,rstart=7500,rend=9000))) 	#balance=1104,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=295,slow=950,rstart=8500,rend=9500))) 	#balance=1104,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=210,mid=300,slow=530,rstart=4500,rend=9500))) 	#balance=1116,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=210,mid=300,slow=530,rstart=5000,rend=9500))) 	#balance=1116,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=188,slow=1180,rstart=  0,rend=9500))) 	#balance=1116,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=148,slow=1150,rstart=  0,rend=9000))) 	#balance=1117,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=200,mid=385,slow=710,rstart=4500,rend=9500))) 	#balance=1143,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 24,mid=225,slow=1110,rstart=2500,rend=9500))) 	#balance=1146,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid=188,slow=1110,rstart=  0,rend=9000))) 	#balance=1148,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=265,slow=1030,rstart=  0,rend=9500))) 	#balance=1156,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=265,slow=1030,rstart=  0,rend=9500))) 	#balance=1156,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=295,slow=1990,rstart=500,rend=9500))) 	#balance=1164,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=215,slow=1050,rstart=2500,rend=9000))) 	#balance=1175,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=280,slow=800,rstart=1500,rend=10000))) 	#balance=1185,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 88,slow=950,rstart=9000,rend=9500))) 	#balance=1187,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid= 88,slow=950,rstart=2500,rend=10000))) 	#balance=1191,times= 21
    configs.append(config(buyer=fcustom(csvama3,fast=128,mid=136,slow=790,rstart=1000,rend=9500))) 	#balance=1192,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=295,slow=1030,rstart=6500,rend=9000))) 	#balance=1192,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=295,slow=1030,rstart=5500,rend=9000))) 	#balance=1192,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=295,slow=1030,rstart=7500,rend=9000))) 	#balance=1192,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=295,slow=1030,rstart=6000,rend=9000))) 	#balance=1192,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid=385,slow=950,rstart=500,rend=8500))) 	#balance=1194,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 26,mid=215,slow=1110,rstart=2500,rend=9000))) 	#balance=1209,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 24,mid=620,slow=950,rstart=500,rend=8500))) 	#balance=1227,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 42,mid=270,slow=1020,rstart=1500,rend=5500))) 	#balance=1249,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=100,mid=188,slow=1190,rstart=500,rend=10000))) 	#balance=1249,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=120,mid=188,slow=1120,rstart=1500,rend=10000))) 	#balance=1262,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=116,slow=1030,rstart=  0,rend=9500))) 	#balance=1265,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 92,slow=1110,rstart=  0,rend=8500))) 	#balance=1270,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=230,mid=420,slow=720,rstart=3500,rend=10000))) 	#balance=1270,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 78,mid=425,slow=950,rstart=500,rend=9500))) 	#balance=1286,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=345,slow=1030,rstart=8000,rend=9000))) 	#balance=1286,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=350,slow=950,rstart=8500,rend=9500))) 	#balance=1286,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=140,mid=430,slow=790,rstart=500,rend=9500))) 	#balance=1291,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=240,mid=280,slow=485,rstart=3000,rend=9500))) 	#balance=1294,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=100,mid=215,slow=1350,rstart=2500,rend=9500))) 	#balance=1300,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=100,mid=215,slow=1350,rstart=2500,rend=9000))) 	#balance=1300,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=305,slow=950,rstart=4500,rend=9500))) 	#balance=1303,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=295,slow=950,rstart=8500,rend=9500))) 	#balance=1305,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=148,slow=1110,rstart=500,rend=10000))) 	#balance=1317,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid=215,slow=1030,rstart=6500,rend=9000))) 	#balance=1319,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=128,slow=950,rstart=  0,rend=8500))) 	#balance=1320,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid=148,slow=1120,rstart=4500,rend=10000))) 	#balance=1343,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=200,mid=305,slow=950,rstart=  0,rend=9500))) 	#balance=1364,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=200,mid=305,slow=950,rstart=2500,rend=9500))) 	#balance=1364,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid= 84,slow=1030,rstart=  0,rend=8500))) 	#balance=1381,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=215,slow=1350,rstart=  0,rend=10000))) 	#balance=1383,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=180,slow=1350,rstart=2500,rend=9500))) 	#balance=1390,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=180,slow=1350,rstart=2500,rend=9000))) 	#balance=1390,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=188,slow=1350,rstart=  0,rend=9000))) 	#balance=1390,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=215,slow=1030,rstart=500,rend=9500))) 	#balance=1401,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=375,slow=1030,rstart=  0,rend=9500))) 	#balance=1402,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid= 84,slow=1190,rstart=1500,rend=10000))) 	#balance=1414,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=148,slow=1110,rstart=2500,rend=9000))) 	#balance=1420,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=148,slow=1110,rstart=500,rend=9000))) 	#balance=1420,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=108,mid=192,slow=850,rstart=500,rend=9500))) 	#balance=1434,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=215,slow=1350,rstart=2500,rend=9000))) 	#balance=1445,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=215,slow=1350,rstart=  0,rend=9000))) 	#balance=1445,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=120,mid=188,slow=1110,rstart=500,rend=10000))) 	#balance=1455,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=100,mid=148,slow=1110,rstart=  0,rend=9000))) 	#balance=1472,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid=215,slow=1030,rstart=  0,rend=9000))) 	#balance=1476,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=188,slow=1030,rstart=8000,rend=8500))) 	#balance=1493,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid= 92,slow=950,rstart=500,rend=8500))) 	#balance=1493,times= 17
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=188,slow=1030,rstart=8000,rend=8500))) 	#balance=1493,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=295,slow=1030,rstart=2500,rend=9000))) 	#balance=1499,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=295,slow=1030,rstart=  0,rend=9000))) 	#balance=1499,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=345,slow=790,rstart=8000,rend=9500))) 	#balance=1502,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=345,slow=800,rstart=  0,rend=9500))) 	#balance=1512,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=225,slow=1110,rstart=8000,rend=9000))) 	#balance=1522,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 92,slow=1750,rstart=2000,rend=8500))) 	#balance=1546,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=120,mid=184,slow=1120,rstart=1500,rend=10000))) 	#balance=1568,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=345,slow=790,rstart=  0,rend=8500))) 	#balance=1574,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=300,slow=950,rstart=1000,rend=9500))) 	#balance=1582,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 26,mid=200,slow=1120,rstart=1500,rend=9000))) 	#balance=1594,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 42,slow=1110,rstart=2500,rend=9500))) 	#balance=1594,times= 16
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=188,slow=1160,rstart=500,rend=10000))) 	#balance=1597,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=215,mid=335,slow=485,rstart=4500,rend=9500))) 	#balance=1598,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=215,slow=1030,rstart=8000,rend=9500))) 	#balance=1606,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid=215,slow=1030,rstart=5500,rend=9000))) 	#balance=1610,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=210,mid=415,slow=710,rstart=  0,rend=9500))) 	#balance=1632,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=220,mid=350,slow=830,rstart=1000,rend=6500))) 	#balance=1634,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=345,slow=1030,rstart=8000,rend=9500))) 	#balance=1648,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 92,slow=950,rstart=  0,rend=9500))) 	#balance=1680,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 92,slow=950,rstart=500,rend=9500))) 	#balance=1680,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=215,slow=1030,rstart=500,rend=9000))) 	#balance=1721,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=240,mid=305,slow=485,rstart=3000,rend=9500))) 	#balance=1729,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=220,mid=340,slow=540,rstart=  0,rend=9500))) 	#balance=1729,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=240,mid=305,slow=485,rstart=3500,rend=9500))) 	#balance=1729,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=120,mid=168,slow=1120,rstart=  0,rend=9500))) 	#balance=1731,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid= 84,slow=1350,rstart=1500,rend=10000))) 	#balance=1737,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid= 84,slow=1350,rstart=2500,rend=9000))) 	#balance=1737,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  9,mid=188,slow=790,rstart=  0,rend=8500))) 	#balance=1748,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid=215,slow=1030,rstart=  0,rend=9000))) 	#balance=1752,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid=215,slow=1030,rstart=2500,rend=9000))) 	#balance=1752,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=215,slow=1030,rstart=2500,rend=10000))) 	#balance=1758,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=215,slow=1030,rstart=500,rend=10000))) 	#balance=1758,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 84,slow=980,rstart=500,rend=10000))) 	#balance=1779,times= 13
    configs.append(config(buyer=fcustom(csvama3,fast=144,mid=415,slow=700,rstart=4000,rend=9500))) 	#balance=1820,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=200,mid=415,slow=710,rstart=  0,rend=9500))) 	#balance=1824,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=300,slow=950,rstart=500,rend=8500))) 	#balance=1824,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=200,mid=415,slow=710,rstart=  0,rend=8500))) 	#balance=1824,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 78,mid=430,slow=850,rstart=500,rend=9500))) 	#balance=1845,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=335,slow=950,rstart=  0,rend=9500))) 	#balance=1846,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=116,slow=710,rstart=  0,rend=8500))) 	#balance=1852,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=460,slow=790,rstart=1000,rend=9500))) 	#balance=1869,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=265,slow=1030,rstart=  0,rend=8500))) 	#balance=1878,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid= 84,slow=1350,rstart=  0,rend=8500))) 	#balance=1885,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=128,mid=192,slow=1110,rstart=1000,rend=9500))) 	#balance=1890,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=300,slow=950,rstart=500,rend=9000))) 	#balance=1896,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=188,slow=1110,rstart=500,rend=8500))) 	#balance=1908,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  9,mid=495,slow=1350,rstart=  0,rend=9500))) 	#balance=1936,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=100,mid=215,slow=1030,rstart=  0,rend=9000))) 	#balance=1953,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=215,slow=1030,rstart=  0,rend=9000))) 	#balance=1953,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=100,mid=188,slow=1120,rstart=500,rend=9000))) 	#balance=1972,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=270,mid=280,slow=800,rstart=1500,rend=10000))) 	#balance=1983,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=270,mid=280,slow=520,rstart=3500,rend=10000))) 	#balance=1988,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=124,slow=1350,rstart=2500,rend=8500))) 	#balance=1990,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=215,slow=1040,rstart=2500,rend=9000))) 	#balance=1991,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=245,mid=295,slow=1350,rstart=2500,rend=9000))) 	#balance=1992,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=144,mid=184,slow=860,rstart=  0,rend=9500))) 	#balance=2039,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 92,slow=950,rstart=500,rend=8500))) 	#balance=2041,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 92,slow=950,rstart=  0,rend=8500))) 	#balance=2041,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=215,mid=375,slow=485,rstart=2500,rend=9000))) 	#balance=2048,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=305,slow=950,rstart=  0,rend=9500))) 	#balance=2067,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=505,slow=1110,rstart=8000,rend=9500))) 	#balance=2112,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=215,slow=1040,rstart=5500,rend=9000))) 	#balance=2166,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=215,slow=1030,rstart=5500,rend=9000))) 	#balance=2196,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=188,slow=1120,rstart=  0,rend=10000))) 	#balance=2258,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=215,slow=1030,rstart=2500,rend=9000))) 	#balance=2285,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=295,slow=950,rstart=  0,rend=10000))) 	#balance=2376,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=128,mid=300,slow=1110,rstart=1000,rend=9000))) 	#balance=2457,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid= 92,slow=1190,rstart=2500,rend=8500))) 	#balance=2498,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=205,mid=215,slow=1030,rstart=2500,rend=9000))) 	#balance=2507,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=215,slow=1030,rstart=7500,rend=9000))) 	#balance=2588,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=128,mid=188,slow=1120,rstart=  0,rend=10000))) 	#balance=2598,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=215,mid=415,slow=710,rstart=4500,rend=9500))) 	#balance=2614,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=305,slow=950,rstart=  0,rend=8500))) 	#balance=2741,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=305,slow=950,rstart=2500,rend=8500))) 	#balance=2741,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=215,slow=1030,rstart=  0,rend=9500))) 	#balance=2782,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=148,slow=1110,rstart=2500,rend=9000))) 	#balance=2887,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=100,mid=188,slow=1110,rstart=2500,rend=9000))) 	#balance=2939,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=100,mid=188,slow=1110,rstart=500,rend=10000))) 	#balance=3037,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=100,mid=188,slow=1110,rstart=  0,rend=10000))) 	#balance=3037,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=128,mid=705,slow=790,rstart=2500,rend=9500))) 	#balance=3132,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=215,slow=1030,rstart=  0,rend=10000))) 	#balance=3223,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid=148,slow=1110,rstart=4000,rend=8500))) 	#balance=3243,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=148,slow=1110,rstart=4500,rend=8500))) 	#balance=3243,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid=305,slow=950,rstart=  0,rend=9500))) 	#balance=3258,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=215,slow=1030,rstart=5500,rend=10000))) 	#balance=3263,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 92,slow=1120,rstart=2500,rend=9000))) 	#balance=3282,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=225,slow=1030,rstart=2500,rend=9000))) 	#balance=3324,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=480,mid=700,slow=1170,rstart=5000,rend=9000))) 	#balance=3340,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=205,mid=415,slow=710,rstart=6500,rend=9500))) 	#balance=3414,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=108,mid=116,slow=1350,rstart=4500,rend=9500))) 	#balance=3419,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=225,slow=1030,rstart=7500,rend=9000))) 	#balance=3580,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 92,slow=1110,rstart=8000,rend=9500))) 	#balance=3709,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=215,mid=430,slow=485,rstart=2500,rend=9000))) 	#balance=4026,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  9,mid=505,slow=790,rstart=1000,rend=9500))) 	#balance=4079,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=345,slow=1030,rstart=  0,rend=9500))) 	#balance=4420,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=215,slow=1030,rstart=  0,rend=8500))) 	#balance=4631,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=465,slow=485,rstart=  0,rend=9500))) 	#balance=4670,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=188,slow=1350,rstart=2000,rend=8500))) 	#balance=4906,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid= 88,slow=1110,rstart=2500,rend=4500))) 	#balance=4907,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid=148,slow=490,rstart=1500,rend=5500))) 	#balance=5302,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=220,slow=1030,rstart=  0,rend=9000))) 	#balance=5865,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=108,mid=192,slow=1130,rstart=500,rend=9500))) 	#balance=6104,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=255,mid=280,slow=850,rstart=500,rend=9500))) 	#balance=6277,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=100,mid=188,slow=1110,rstart=  0,rend=9500))) 	#balance=7440,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=215,slow=1350,rstart=2500,rend=9000))) 	#balance=7469,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=215,slow=1030,rstart=  0,rend=9000))) 	#balance=7481,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=345,slow=1030,rstart=  0,rend=9000))) 	#balance=8740,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=215,slow=1030,rstart=5500,rend=9000))) 	#balance=10790,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=215,slow=1030,rstart=6500,rend=9000))) 	#balance=10790,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=225,slow=790,rstart=8000,rend=9500))) 	#balance=10930,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=765,slow=1110,rstart=500,rend=7000))) 	#balance=13171,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid=495,slow=860,rstart=5000,rend=6500))) 	#balance=18561,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=188,slow=1110,rstart=8000,rend=9500))) 	#balance=20523,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=156,slow=1110,rstart=  0,rend=9500))) 	#balance=35175,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=270,mid=305,slow=950,rstart=  0,rend=9500))) 	#balance=43486,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=270,mid=305,slow=950,rstart=  0,rend=10000))) 	#balance=43486,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=200,mid=400,slow=500,rstart=4500,rend=9000))) 	#balance=72677,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=385,slow=950,rstart=  0,rend=8500))) 	#balance=108068,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 33,mid= 96,slow=1240,rstart=4500,rend=6000))) 	#balance=3872000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 88,mid=400,slow=1800,rstart=7500,rend=10000))) 	#balance=4082500,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=116,slow=345,rstart=4500,rend=6000))) 	#balance=4991000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=148,slow=1120,rstart=6500,rend=8500))) 	#balance=6684000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=124,mid=148,slow=1150,rstart=3500,rend=8000))) 	#balance=6957500,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=705,slow=1110,rstart=  0,rend=8500))) 	#balance=9550000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=335,slow=630,rstart=4000,rend=8500))) 	#balance=1000,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 39,mid= 45,slow=1910,rstart=4000,rend=9000))) 	#balance=1001,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=172,slow=1130,rstart=4000,rend=10000))) 	#balance=1007,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 26,mid= 92,slow=970,rstart=1500,rend=10000))) 	#balance=1008,times= 18
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 45,slow=640,rstart=4000,rend=9000))) 	#balance=1010,times= 20
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 45,slow=630,rstart=4000,rend=9000))) 	#balance=1010,times= 19
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 92,slow=1060,rstart=2000,rend=10000))) 	#balance=1011,times= 21
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 92,slow=1060,rstart=1500,rend=10000))) 	#balance=1011,times= 21
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 75,slow=720,rstart=4500,rend=5000))) 	#balance=1018,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 75,slow=650,rstart=1500,rend=9000))) 	#balance=1020,times= 19
    configs.append(config(buyer=fcustom(csvama3,fast=155,mid=196,slow=650,rstart=4500,rend=10000))) 	#balance=1032,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=196,slow=495,rstart=5000,rend=10000))) 	#balance=1040,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=196,slow=495,rstart=6000,rend=10000))) 	#balance=1040,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 92,slow=980,rstart=2000,rend=10000))) 	#balance=1044,times= 13
    configs.append(config(buyer=fcustom(csvama3,fast= 28,mid= 75,slow=980,rstart=1500,rend=9500))) 	#balance=1045,times= 29
    configs.append(config(buyer=fcustom(csvama3,fast=116,mid=485,slow=940,rstart=3500,rend=9500))) 	#balance=1045,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 18,mid=196,slow=650,rstart=5000,rend=8500))) 	#balance=1047,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid= 48,slow=960,rstart=1500,rend=8500))) 	#balance=1055,times= 20
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid=305,slow=740,rstart=4000,rend=10000))) 	#balance=1055,times= 13
    configs.append(config(buyer=fcustom(csvama3,fast=120,mid=280,slow=660,rstart=1500,rend=9500))) 	#balance=1059,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid= 48,slow=520,rstart=4000,rend=8500))) 	#balance=1063,times= 21
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid= 75,slow=1130,rstart=4500,rend=10000))) 	#balance=1064,times= 16
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=340,slow=720,rstart=4500,rend=10000))) 	#balance=1064,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  3,mid=235,slow=1010,rstart=2000,rend=9500))) 	#balance=1065,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 39,mid=200,slow=490,rstart=4500,rend=9000))) 	#balance=1069,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 75,slow=1020,rstart=3000,rend=9000))) 	#balance=1084,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast=148,mid=325,slow=1380,rstart=4000,rend=8500))) 	#balance=1091,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=320,slow=1380,rstart=7000,rend=9000))) 	#balance=1091,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=260,slow=630,rstart=1500,rend=9500))) 	#balance=1093,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=215,slow=500,rstart=7000,rend=10000))) 	#balance=1097,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 39,mid= 88,slow=970,rstart=2500,rend=9500))) 	#balance=1098,times= 19
    configs.append(config(buyer=fcustom(csvama3,fast= 26,mid= 72,slow=650,rstart=4000,rend=10000))) 	#balance=1098,times= 25
    configs.append(config(buyer=fcustom(csvama3,fast=  3,mid=172,slow=630,rstart=4000,rend=8500))) 	#balance=1106,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 18,mid= 72,slow=175,rstart=1500,rend=10000))) 	#balance=1109,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid= 78,slow=490,rstart=1500,rend=8500))) 	#balance=1110,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast= 30,mid= 92,slow=980,rstart=2000,rend=10000))) 	#balance=1124,times= 20
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid= 78,slow=980,rstart=4000,rend=8500))) 	#balance=1125,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid=235,slow=650,rstart=7000,rend=10000))) 	#balance=1127,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast= 18,mid=235,slow=650,rstart=7000,rend=10000))) 	#balance=1129,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast= 39,mid= 48,slow=730,rstart=2000,rend=8500))) 	#balance=1135,times= 16
    configs.append(config(buyer=fcustom(csvama3,fast=150,mid=235,slow=660,rstart=2000,rend=8500))) 	#balance=1136,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 75,slow=1130,rstart=7000,rend=10000))) 	#balance=1136,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=240,slow=455,rstart=2000,rend=9000))) 	#balance=1139,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 48,slow=710,rstart=4000,rend=8500))) 	#balance=1139,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast= 39,mid= 48,slow=1160,rstart=4000,rend=8500))) 	#balance=1141,times= 13
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid= 48,slow=760,rstart=1500,rend=8500))) 	#balance=1151,times= 27
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=164,slow=495,rstart=7000,rend=10000))) 	#balance=1158,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=235,slow=730,rstart=4500,rend=9500))) 	#balance=1161,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=120,mid=275,slow=650,rstart=7000,rend=10000))) 	#balance=1161,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=184,slow=650,rstart=4000,rend=10000))) 	#balance=1166,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 30,mid= 92,slow=420,rstart=2000,rend=8500))) 	#balance=1176,times= 15
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=260,slow=650,rstart=7000,rend=10000))) 	#balance=1177,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 78,slow=980,rstart=4500,rend=8500))) 	#balance=1182,times= 17
    configs.append(config(buyer=fcustom(csvama3,fast=150,mid=400,slow=1230,rstart=3000,rend=9000))) 	#balance=1182,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid=164,slow=415,rstart=4000,rend=10000))) 	#balance=1186,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=315,slow=650,rstart=4500,rend=9500))) 	#balance=1208,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid= 48,slow=1120,rstart=1500,rend=8500))) 	#balance=1215,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 48,slow=740,rstart=4000,rend=8500))) 	#balance=1226,times= 17
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid= 42,slow=710,rstart=7000,rend=10000))) 	#balance=1228,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=150,mid=235,slow=495,rstart=2500,rend=10000))) 	#balance=1242,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid=172,slow=490,rstart=4000,rend=8500))) 	#balance=1250,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid=340,slow=650,rstart=7000,rend=10000))) 	#balance=1250,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=340,slow=650,rstart=7000,rend=10000))) 	#balance=1250,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid=340,slow=650,rstart=4000,rend=8500))) 	#balance=1253,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=200,slow=415,rstart=1500,rend=9000))) 	#balance=1256,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid= 72,slow=1020,rstart=1500,rend=10000))) 	#balance=1260,times= 17
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid= 54,slow=630,rstart=7000,rend=8500))) 	#balance=1261,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 48,slow=490,rstart=4500,rend=8500))) 	#balance=1263,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast=124,mid=220,slow=1130,rstart=7000,rend=10000))) 	#balance=1266,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=128,mid=196,slow=1020,rstart=7000,rend=10000))) 	#balance=1273,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid= 75,slow=1130,rstart=1500,rend=10000))) 	#balance=1275,times= 17
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 63,slow=730,rstart=5000,rend=10000))) 	#balance=1283,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=315,slow=650,rstart=7000,rend=10000))) 	#balance=1286,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid=335,slow=630,rstart=7000,rend=10000))) 	#balance=1286,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid=275,slow=500,rstart=6000,rend=9000))) 	#balance=1286,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid=320,slow=580,rstart=4000,rend=9000))) 	#balance=1286,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=335,slow=630,rstart=7000,rend=10000))) 	#balance=1286,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=315,slow=730,rstart=7000,rend=10000))) 	#balance=1286,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=172,slow=495,rstart=4000,rend=10000))) 	#balance=1292,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid=485,slow=1130,rstart=4000,rend=10000))) 	#balance=1300,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=200,slow=1130,rstart=7000,rend=10000))) 	#balance=1302,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid= 78,slow=980,rstart=1500,rend=8500))) 	#balance=1306,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid= 57,slow=730,rstart=7000,rend=10000))) 	#balance=1315,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid=320,slow=660,rstart=4000,rend=10000))) 	#balance=1325,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid=320,slow=650,rstart=6000,rend=9000))) 	#balance=1337,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=200,slow=1110,rstart=4000,rend=9000))) 	#balance=1339,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 48,slow=1440,rstart=4000,rend=8500))) 	#balance=1346,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=128,mid=200,slow=1130,rstart=7000,rend=10000))) 	#balance=1348,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=128,mid=200,slow=1130,rstart=4000,rend=10000))) 	#balance=1348,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=150,mid=260,slow=710,rstart=2000,rend=9000))) 	#balance=1349,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 75,slow=720,rstart=8500,rend=10000))) 	#balance=1359,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 75,slow=1020,rstart=2000,rend=9500))) 	#balance=1360,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast=128,mid=520,slow=800,rstart=4000,rend=10000))) 	#balance=1365,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=124,mid=335,slow=650,rstart=7000,rend=10000))) 	#balance=1373,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=375,mid=655,slow=770,rstart=2000,rend=10000))) 	#balance=1384,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid= 57,slow=730,rstart=7000,rend=9000))) 	#balance=1384,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid= 54,slow=1770,rstart=5000,rend=8500))) 	#balance=1388,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid=320,slow=740,rstart=4000,rend=10000))) 	#balance=1390,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 26,slow=100,rstart=4000,rend=8500))) 	#balance=1390,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=485,slow=630,rstart=4000,rend=8500))) 	#balance=1391,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=148,mid=525,slow=800,rstart=4000,rend=8500))) 	#balance=1398,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=150,mid=335,slow=630,rstart=4000,rend=9500))) 	#balance=1399,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=485,slow=740,rstart=4000,rend=8500))) 	#balance=1401,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=325,slow=640,rstart=4000,rend=8500))) 	#balance=1410,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid=325,slow=640,rstart=4500,rend=8500))) 	#balance=1410,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid=565,slow=1000,rstart=4000,rend=10000))) 	#balance=1416,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=295,slow=630,rstart=7000,rend=10000))) 	#balance=1429,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=335,slow=650,rstart=7000,rend=10000))) 	#balance=1435,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid=335,slow=650,rstart=7000,rend=10000))) 	#balance=1435,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=196,slow=510,rstart=7000,rend=10000))) 	#balance=1446,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=196,slow=510,rstart=5000,rend=10000))) 	#balance=1446,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=150,mid=555,slow=730,rstart=4500,rend=9500))) 	#balance=1448,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 42,mid= 51,slow=1180,rstart=5500,rend=9000))) 	#balance=1458,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=280,slow=700,rstart=4000,rend=9000))) 	#balance=1459,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 78,slow=1020,rstart=1500,rend=8500))) 	#balance=1462,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=325,slow=730,rstart=4500,rend=8500))) 	#balance=1471,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid= 72,slow= 95,rstart=4500,rend=9000))) 	#balance=1504,times= 13
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=335,slow=650,rstart=7000,rend=10000))) 	#balance=1510,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 48,slow=1120,rstart=4500,rend=8500))) 	#balance=1513,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast= 26,mid= 42,slow=730,rstart=5000,rend=9000))) 	#balance=1522,times= 14
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 45,slow= 95,rstart=1500,rend=9000))) 	#balance=1523,times= 19
    configs.append(config(buyer=fcustom(csvama3,fast=150,mid=265,slow=420,rstart=2000,rend=9500))) 	#balance=1526,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 75,slow= 95,rstart=1500,rend=9000))) 	#balance=1531,times= 17
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid= 22,slow=495,rstart=7000,rend=9000))) 	#balance=1554,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 33,slow=630,rstart=4000,rend=8500))) 	#balance=1561,times= 20
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid= 72,slow=980,rstart=1500,rend=5000))) 	#balance=1561,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid=196,slow=980,rstart=7000,rend=8500))) 	#balance=1564,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 48,slow=720,rstart=4000,rend=8500))) 	#balance=1571,times= 15
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 75,slow=1020,rstart=1500,rend=10000))) 	#balance=1576,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=325,slow=520,rstart=4000,rend=8500))) 	#balance=1576,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=400,mid=460,slow=890,rstart=2000,rend=8000))) 	#balance=1577,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid=280,slow=440,rstart=4000,rend=10000))) 	#balance=1581,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid= 78,slow=980,rstart=1500,rend=8500))) 	#balance=1603,times= 13
    configs.append(config(buyer=fcustom(csvama3,fast= 26,mid=315,slow=650,rstart=7000,rend=10000))) 	#balance=1608,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid=168,slow=740,rstart=4000,rend=8500))) 	#balance=1625,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=430,mid=565,slow=630,rstart=500,rend=7000))) 	#balance=1632,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid= 78,slow=500,rstart=4000,rend=8500))) 	#balance=1634,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=164,slow=495,rstart=7000,rend=10000))) 	#balance=1640,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast=140,mid=196,slow=1140,rstart=7500,rend=10000))) 	#balance=1657,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=200,slow=1140,rstart=1500,rend=9500))) 	#balance=1657,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid=645,slow=800,rstart=4000,rend=8500))) 	#balance=1668,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 48,slow=720,rstart=4500,rend=8500))) 	#balance=1689,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=172,slow=495,rstart=7000,rend=10000))) 	#balance=1702,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  3,mid=172,slow=485,rstart=6000,rend=10000))) 	#balance=1702,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=235,slow=730,rstart=4000,rend=10000))) 	#balance=1708,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=235,slow=485,rstart=7000,rend=10000))) 	#balance=1712,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=220,slow=485,rstart=7000,rend=10000))) 	#balance=1712,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 48,slow=740,rstart=1500,rend=8500))) 	#balance=1713,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 42,slow=650,rstart=7000,rend=10000))) 	#balance=1730,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=250,slow=1180,rstart=7500,rend=9000))) 	#balance=1733,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 18,mid= 72,slow=175,rstart=7000,rend=10000))) 	#balance=1737,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 48,slow=1140,rstart=4000,rend=8500))) 	#balance=1745,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 75,slow=840,rstart=1500,rend=8500))) 	#balance=1779,times= 14
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 48,slow=1140,rstart=4000,rend=8500))) 	#balance=1786,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid= 42,slow=1130,rstart=4500,rend=9500))) 	#balance=1788,times= 20
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 78,slow=980,rstart=1500,rend=10000))) 	#balance=1793,times= 13
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 75,slow=1000,rstart=1500,rend=8500))) 	#balance=1795,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=164,slow=630,rstart=7000,rend=10000))) 	#balance=1797,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=164,slow=495,rstart=7000,rend=8500))) 	#balance=1801,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 75,slow=630,rstart=1500,rend=9000))) 	#balance=1829,times= 16
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid=320,slow=660,rstart=4000,rend=9000))) 	#balance=1853,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=124,mid=240,slow=650,rstart=7000,rend=10000))) 	#balance=1867,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid=655,slow=1230,rstart=3500,rend=9000))) 	#balance=1925,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=340,slow=1020,rstart=4000,rend=10000))) 	#balance=2023,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast=150,mid=235,slow=630,rstart=7000,rend=10000))) 	#balance=2024,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 48,slow=740,rstart=4000,rend=8500))) 	#balance=2034,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 42,slow=730,rstart=4500,rend=9500))) 	#balance=2077,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=195,mid=335,slow=1350,rstart=7000,rend=10000))) 	#balance=2087,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=340,slow=650,rstart=7000,rend=10000))) 	#balance=2089,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=148,mid=205,slow=800,rstart=1500,rend=8500))) 	#balance=2095,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=172,slow=630,rstart=4000,rend=10000))) 	#balance=2115,times= 13
    configs.append(config(buyer=fcustom(csvama3,fast=148,mid=196,slow=760,rstart=1500,rend=8500))) 	#balance=2159,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 51,slow=740,rstart=4000,rend=9000))) 	#balance=2190,times= 13
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid=245,slow=980,rstart=1500,rend=8500))) 	#balance=2197,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=395,slow=980,rstart=7000,rend=8000))) 	#balance=2207,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 26,mid= 72,slow= 95,rstart=4500,rend=10000))) 	#balance=2252,times= 13
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=172,slow=1140,rstart=7000,rend=9500))) 	#balance=2309,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 57,slow=1110,rstart=4500,rend=9000))) 	#balance=2334,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=200,mid=435,slow=520,rstart=3500,rend=6000))) 	#balance=2356,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=335,slow=650,rstart=4000,rend=10000))) 	#balance=2375,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=220,slow=650,rstart=7000,rend=10000))) 	#balance=2434,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid= 45,slow=650,rstart=7000,rend=9000))) 	#balance=2437,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=335,slow=630,rstart=7000,rend=10000))) 	#balance=2446,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=340,slow=630,rstart=4000,rend=8500))) 	#balance=2447,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=255,slow=730,rstart=5000,rend=10000))) 	#balance=2508,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 75,slow=440,rstart=1500,rend=10000))) 	#balance=2550,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid=240,slow=740,rstart=7000,rend=9000))) 	#balance=2574,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid= 45,slow=730,rstart=5000,rend=10000))) 	#balance=2591,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=335,slow=630,rstart=4000,rend=9000))) 	#balance=2601,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=335,slow=630,rstart=5000,rend=10000))) 	#balance=2601,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid= 48,slow=720,rstart=4000,rend=8500))) 	#balance=2604,times= 15
    configs.append(config(buyer=fcustom(csvama3,fast=150,mid=235,slow=730,rstart=1500,rend=10000))) 	#balance=2680,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=168,slow=650,rstart=7000,rend=8500))) 	#balance=2694,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid= 45,slow=740,rstart=5000,rend=9000))) 	#balance=2720,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=235,slow=730,rstart=7000,rend=10000))) 	#balance=2823,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=340,slow=630,rstart=4000,rend=9500))) 	#balance=2870,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=340,slow=630,rstart=4000,rend=9000))) 	#balance=2870,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 57,slow=1110,rstart=4000,rend=9000))) 	#balance=2886,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=220,slow=1130,rstart=4000,rend=9000))) 	#balance=2908,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=345,slow=630,rstart=7000,rend=10000))) 	#balance=2929,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=196,slow=1120,rstart=3500,rend=8500))) 	#balance=2939,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=128,mid=196,slow=1110,rstart=4000,rend=9000))) 	#balance=2939,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=340,slow=660,rstart=4000,rend=9500))) 	#balance=2968,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=340,slow=630,rstart=7000,rend=9000))) 	#balance=2998,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=340,slow=630,rstart=7000,rend=10000))) 	#balance=2998,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid= 57,slow=1270,rstart=7000,rend=10000))) 	#balance=3012,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=172,slow=630,rstart=4000,rend=10000))) 	#balance=3026,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast=120,mid=196,slow=1110,rstart=4000,rend=10000))) 	#balance=3037,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=120,mid=240,slow=730,rstart=1500,rend=9000))) 	#balance=3039,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=128,mid=196,slow=1130,rstart=7000,rend=10000))) 	#balance=3075,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 28,mid=360,slow=660,rstart=500,rend=8500))) 	#balance=3122,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 57,slow=1270,rstart=4000,rend=8500))) 	#balance=3217,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 48,slow=720,rstart=4500,rend=8500))) 	#balance=3352,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 33,mid=160,slow=350,rstart=1500,rend=5500))) 	#balance=3365,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=235,slow=730,rstart=7000,rend=10000))) 	#balance=3372,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=340,slow=650,rstart=4000,rend=10000))) 	#balance=3405,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 45,slow=495,rstart=7000,rend=10000))) 	#balance=3414,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=335,slow=630,rstart=7000,rend=10000))) 	#balance=3526,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=335,slow=630,rstart=7000,rend=9000))) 	#balance=3526,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 57,slow=730,rstart=4000,rend=9000))) 	#balance=3560,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=510,slow=720,rstart=3000,rend=9500))) 	#balance=3640,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=172,slow=630,rstart=5000,rend=10000))) 	#balance=4046,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast=144,mid=240,slow=730,rstart=6000,rend=9000))) 	#balance=4162,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid= 45,slow=740,rstart=4000,rend=9000))) 	#balance=4208,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=172,slow=630,rstart=7000,rend=10000))) 	#balance=4355,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=196,slow=495,rstart=2000,rend=10000))) 	#balance=4407,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=196,slow=495,rstart=500,rend=10000))) 	#balance=4407,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=196,slow=495,rstart=2500,rend=10000))) 	#balance=4407,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid=196,slow=495,rstart=4000,rend=10000))) 	#balance=4407,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=196,slow=495,rstart=3000,rend=10000))) 	#balance=4407,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=196,slow=495,rstart=3000,rend=10000))) 	#balance=4407,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=196,slow=495,rstart=4000,rend=10000))) 	#balance=4407,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=196,slow=495,rstart=3500,rend=10000))) 	#balance=4407,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=196,slow=495,rstart=1000,rend=10000))) 	#balance=4407,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid= 42,slow=720,rstart=4500,rend=8500))) 	#balance=4542,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=108,mid=176,slow=500,rstart=500,rend=7000))) 	#balance=4573,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid=196,slow=485,rstart=3000,rend=10000))) 	#balance=4793,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=155,mid=330,slow=540,rstart=3000,rend=9000))) 	#balance=4824,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid=340,slow=660,rstart=4000,rend=10000))) 	#balance=4837,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=120,mid=340,slow=700,rstart=500,rend=9000))) 	#balance=4845,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid=160,slow=590,rstart=3500,rend=5000))) 	#balance=4907,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 80,mid=240,slow=740,rstart=6000,rend=10000))) 	#balance=5274,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=370,mid=660,slow=750,rstart=2000,rend=9000))) 	#balance=5300,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=172,slow=630,rstart=4000,rend=8500))) 	#balance=5325,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid= 42,slow=740,rstart=5000,rend=10000))) 	#balance=5327,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=155,mid=490,slow=540,rstart=5500,rend=9000))) 	#balance=5699,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 18,mid=335,slow=650,rstart=7000,rend=10000))) 	#balance=8031,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=200,slow=485,rstart=3000,rend=10000))) 	#balance=9534,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=205,slow=485,rstart=4000,rend=9500))) 	#balance=9534,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=340,slow=650,rstart=7000,rend=10000))) 	#balance=12220,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 26,mid=335,slow=650,rstart=7000,rend=10000))) 	#balance=12220,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 45,slow=730,rstart=7000,rend=9000))) 	#balance=14338,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 54,mid=750,slow=1230,rstart=500,rend=5500))) 	#balance=15132,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 42,mid= 78,slow=970,rstart=1500,rend=4500))) 	#balance=21750,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid=196,slow=1140,rstart=4000,rend=8500))) 	#balance=35175,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=172,slow=630,rstart=6000,rend=8500))) 	#balance=201151,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=190,mid=196,slow=1910,rstart=4000,rend=10000))) 	#balance=3325000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=120,mid=340,slow=660,rstart=1500,rend=9500))) 	#balance=7492000,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=655,slow=770,rstart=4000,rend=8500))) 	#balance=8748000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=172,slow=630,rstart=7000,rend=8500))) 	#balance=8748000,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=196,slow=485,rstart=1000,rend=10000))) 	#balance=11953000,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=196,slow=495,rstart=6000,rend=10000))) 	#balance=11953000,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=196,slow=495,rstart=4500,rend=9000))) 	#balance=11953000,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid=196,slow=495,rstart=6000,rend=10000))) 	#balance=11953000,times=  5
    
    return configs

def prepare_configs_A(seller,pman,dman):    #R>=400,winrate>400 or R>=1000,winrate>333
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    
    #候选A winrate>=400且R>=600,times>5 or  R>500且winrate>500
    
    configs.append(config(buyer=fcustom(csvama2,fast= 13,slow=125,rstart= 1000,rend=5000))) 	#2268-188-609-41    #9078/988
    configs.append(config(buyer=fcustom(svama3,fast= 39,mid= 71,slow=490,ma_standard=120,extend_days=  1))) 	#balance=2262,times=  4    #4103-119-571-7
    configs.append(config(buyer=fcustom(svama3,fast= 39,mid= 71,slow=490,ma_standard=500,extend_days=  1))) 	#balance=4129,times=  3    #4421-168-600-5
    configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 80,slow=145,ma_standard= 55,extend_days=  1))) 	#balance=1000,times= 11 #986-70-583-12
    configs.append(config(buyer=fcustom(vama3,fast= 20,mid= 55,slow= 95,ma_standard=500,extend_days=  1))) 	#balance=1140,times=  5 #928-65-500-8
    configs.append(config(buyer=fcustom(vama3,fast= 17,mid= 38,slow=125,ma_standard=500,extend_days=  1))) 	#balance=1254,times=  2 #3609-231-400-5
    configs.append(config(buyer=fcustom(vama3,fast= 21,mid= 56,slow=105,ma_standard=500,extend_days=  1))) 	#balance=1276,times=  3 #1410-213-500-6
    configs.append(config(buyer=fcustom(vama3,fast= 18,mid= 57,slow=115,ma_standard=500,extend_days=  1))) 	#balance=1347,times=  4 #3771-264-500-12
    configs.append(config(buyer=fcustom(vama3,fast= 19,mid= 56,slow=105,ma_standard=500,extend_days=  1))) 	#balance=2314,times=  5 #1315-171-571-7
    configs.append(config(buyer=fcustom(vama3,fast= 20,mid= 56,slow=105,ma_standard=500,extend_days=  1))) 	#balance=2416,times=  7 #3494-325-625-8
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 78,slow=125,ma_standard= 55,extend_days=  1))) 	#balance=3214,times=  9 #920-58-500-14
    configs.append(config(buyer=fcustom(svama3,fast=  2,mid= 95,slow=130,ma_standard=120,extend_days=  1))) 	#balance=1244,times= 10    #594-60-444-9
    configs.append(config(buyer=fcustom(svama3,fast=  7,mid= 91,slow=300,ma_standard=500,extend_days=  1))) 	#balance=4343,times=  2#   #555-35-666-3
    configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 54,slow= 85,ma_standard= 55,extend_days=  1))) 	#balance=1006,times= 14 #723-47-413-29
    configs.append(config(buyer=fcustom(vama3,fast= 17,mid= 46,slow= 85,ma_standard= 55,extend_days=  1))) 	#balance=1204,times= 25 #1025-81-535-28
    
    return configs

def prepare_configs_A1(seller,pman,dman):    #候选A1 winrate>=400且R>=800,times<5
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []

    #候选A1 winrate>=400且R>=800,times<5
    configs.append(config(buyer=fcustom(svama3,fast= 23,mid= 79,slow= 10,ma_standard=120,extend_days=  1))) 	#balance=2488,times=  2#   #1000-277-1000-1
    configs.append(config(buyer=fcustom(svama2s,fast= 48,slow=500,ma_standard= 67,extend_days= 13))) 	#balance=1162,times=  2 #1843-59-500-2
    configs.append(config(buyer=fcustom(svama2s,fast= 26,slow=430,ma_standard= 67,extend_days=  5))) 	#balance=2503,times=  4 #1000-84-1000-1
    configs.append(config(buyer=fcustom(svama2x,fast= 11,slow=  5,base=198,ma_standard=500))) 	#1000-116-1000-1
    configs.append(config(buyer=fcustom(svama2x,fast= 18,slow=  5,base=198,ma_standard= 10))) 	#1800-99-666-3
    configs.append(config(buyer=fcustom(svama2x,fast=  6,slow=  5,base=240,ma_standard=500))) 	#1000-148-1000-4
    configs.append(config(buyer=fcustom(svama2x,fast= 28,slow=  5,base=240,ma_standard= 10))) 	#2328-177-500-4
    configs.append(config(buyer=fcustom(svama2x,fast= 15,slow=  5,base=228,ma_standard=250))) 	#balance=30406,times=  5 #1000-131-1000-2
    configs.append(config(buyer=fcustom(csvama3,fast= 44,mid= 23,slow=250,rstart=7500,rend=8000))) 	#1948-152-500-2 #383/78

    return configs

def prepare_configs_A2(seller,pman,dman):    #winrate>=400且R>=600,times>5 or  R>500且winrate>500
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    
    #存在RP问题的参数配置
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 83,slow= 20,ma_standard=500,extend_days=  5))) 	#balance=1129,times= 23 #1746-124-394-76 ##
    configs.append(config(buyer=fcustom(svama2x,fast=  6,slow=  5,base=240,ma_standard= 10))) 	#balance=6106,times=  5 #2603-139-625-8
    configs.append(config(buyer=fcustom(svama2x,fast= 47,slow=  5,base=168,ma_standard=500))) 	#balance=26391,times=  3 #701-80-400-5
    configs.append(config(buyer=fcustom(vama3,fast= 16,mid= 78,slow= 45,ma_standard=500,extend_days= 13))) 	#2493-182-387-155
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 62,slow= 45,ma_standard=500,extend_days=  1))) 	#853-76-470-17
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 71,slow= 55,ma_standard=500,extend_days= 25))) 	#1172-95-377-172
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 67,slow= 45,ma_standard=500,extend_days= 27))) 	#1724-118-418-332 ##
    configs.append(config(buyer=fcustom(vama3,fast=  9,mid= 68,slow= 45,ma_standard=500,extend_days= 21))) 	#1815-118-431-278
    
    return configs

def prepare_configs_B(seller,pman,dman):    #R>=500,winrate<400
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    #候选C R>800,或R>500且winrate>400
    configs.append(config(buyer=fcustom(vama3,fast= 29,mid= 78,slow= 65,ma_standard=500,extend_days= 29))) 	#1315-100-325-270
    configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 81,slow= 65,ma_standard=500,extend_days= 29))) 	#1259-97-348-264
    configs.append(config(buyer=fcustom(vama3,fast= 31,mid= 91,slow= 65,ma_standard=500,extend_days= 25))) 	#1027-76-365-205
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 59,slow= 50,ma_standard=500,extend_days= 27))) 	#1250-90-361-501
    configs.append(config(buyer=fcustom(vama3,fast= 17,mid= 69,slow= 65,ma_standard=500,extend_days= 31))) 	#1040-78-312-432
    configs.append(config(buyer=fcustom(vama3,fast= 11,mid=  8,slow= 65,ma_standard=500,extend_days= 27))) 	#750-60-346-124
    configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 72,slow= 45,ma_standard=500,extend_days= 25))) 	#1257-88-298-134
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 80,slow= 45,ma_standard=500,extend_days= 29))) 	#2289-158-262-80
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 79,slow= 55,ma_standard=500,extend_days=  1))) 	#7714-270-333-3
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 79,slow= 45,ma_standard=500,extend_days= 17))) 	#928-65-288-90
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 69,slow= 45,ma_standard=500,extend_days= 23))) 	#1089-68-304-115
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 91,slow= 50,ma_standard=500,extend_days= 27))) 	#1000-74-350-248
    configs.append(config(buyer=fcustom(vama3,fast=  4,mid= 78,slow= 60,ma_standard=500,extend_days= 27))) 	#1065-81-325-393
    configs.append(config(buyer=fcustom(vama3,fast= 31,mid= 68,slow= 65,ma_standard=500,extend_days= 29))) 	#949-75-326-315
    configs.append(config(buyer=fcustom(vama3,fast=  8,mid= 78,slow= 45,ma_standard=500,extend_days= 29))) 	#2138-154-369-222
    configs.append(config(buyer=fcustom(vama3,fast= 17,mid= 56,slow= 45,ma_standard=500,extend_days= 13))) 	#1426-97-354-237
    configs.append(config(buyer=fcustom(vama3,fast= 29,mid= 78,slow= 45,ma_standard=500,extend_days= 29))) 	#2109-154-284-95
    configs.append(config(buyer=fcustom(vama3,fast= 17,mid= 55,slow= 50,ma_standard=500,extend_days= 27))) 	#910-61-345-385
    configs.append(config(buyer=fcustom(vama3,fast= 18,mid= 91,slow= 50,ma_standard=500,extend_days= 27))) 	#1200-90-368-160
    configs.append(config(buyer=fcustom(svama3,fast= 17,mid= 95,slow=130,ma_standard= 10,extend_days=  1))) 	#962-76-333-15
    configs.append(config(buyer=fcustom(svama3,fast= 17,mid= 95,slow=130,ma_standard=120,extend_days=  1))) 	#1036-85-357-14
    configs.append(config(buyer=fcustom(svama2,fast= 20,slow=  5,ma_standard=500))) 	#1411-72-285-49
    configs.append(config(buyer=fcustom(svama2c,fast= 32,slow=  5,ma_standard= 22))) 	#1285-72-307-13
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 83,slow= 15,ma_standard=500,extend_days= 13))) 	#1394-99-272-66
    configs.append(config(buyer=fcustom(vama3,fast= 24,mid= 55,slow=105,ma_standard= 55,extend_days=  1))) 	#1333-100-333-15
    configs.append(config(buyer=fcustom(vama3,fast= 33,mid= 84,slow=345,ma_standard=500,extend_days= 27))) 	#936-74-323-241
    configs.append(config(buyer=fcustom(vama3,fast=  1,mid= 78,slow=365,ma_standard=500,extend_days= 29))) 	#1025-80-317-173
    configs.append(config(buyer=fcustom(vama3,fast=  4,mid= 88,slow=425,ma_standard=500,extend_days= 33))) 	#1146-102-303-158
    configs.append(config(buyer=fcustom(vama3,fast= 27,mid= 60,slow=335,ma_standard=500,extend_days= 17))) 	#1012-80-313-217
    configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 68,slow=465,ma_standard=500,extend_days= 21))) 	#800-60-275-156
    configs.append(config(buyer=fcustom(vama3,fast= 16,mid= 78,slow=445,ma_standard=500,extend_days= 21))) 	#932-83-339-115
    configs.append(config(buyer=fcustom(vama3,fast= 33,mid= 72,slow=445,ma_standard=500,extend_days= 17))) 	#1213-91-258-155
    configs.append(config(buyer=fcustom(vama3,fast=  8,mid= 78,slow=445,ma_standard=500,extend_days= 21))) 	#897-79-289-107
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 78,slow=450,ma_standard=500,extend_days= 17))) 	#883-68-284-130
    configs.append(config(buyer=fcustom(vama3,fast=  1,mid= 69,slow=465,ma_standard=500,extend_days= 31))) 	#759-60-278-201
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 78,slow=445,ma_standard=500,extend_days= 29))) 	#1024-85-277-144
    configs.append(config(buyer=fcustom(vama2,fast= 29,slow=  5,ma_standard=250))) 	#954-63-264-34
    configs.append(config(buyer=fcustom(vama2,fast= 35,slow= 20,ma_standard=500))) 	#1064-83-325-172
    configs.append(config(buyer=fcustom(vama2,fast= 35,slow= 15,ma_standard=500))) 	#845-60-285-77
    configs.append(config(buyer=fcustom(vama2x,fast= 25,slow=  5,base=214,ma_standard=120))) 	#1622-86-250-4
    configs.append(config(buyer=fcustom(svama2x,fast= 31,slow= 10,base=170,ma_standard=120))) 	#253-16-428-7
    configs.append(config(buyer=fcustom(csvama2,fast= 37,slow=115,rstart=3000,rend=8000))) 	#1202-95-367-68

    return configs

def prepare_configs_C(seller,pman,dman): # 0<=R<500 且winrate<400  R/avg income/win rate #只做储备
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []

    configs.append(config(buyer=fcustom(ma3,fast= 23,mid= 26,slow=150,ma_standard=240,extend_days= 31))) 	#480/25/296
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

    configs = prepare_temp_configs(seller,pman,dman)
    #configs = prepare_configs_A(seller,pman,dman)
    #configs = prepare_configs_B(seller,pman,dman)
    #configs.extend(prepare_configs_A1(seller,pman,dman))
    #configs.extend(prepare_configs_A2(seller,pman,dman))    
    #configs.extend(prepare_configs_B(seller,pman,dman))
    batch(configs,sdata,dates,xbegin,cmediator=myMediator)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    

    save_configs('atr_ev_n.txt',configs,xbegin,end)

def run_merge_body(sdata,dates,begin,end,xbegin):
    
    from time import time
    tbegin = time()

    pman = AdvancedATRPositionManager()
    dman = DateManager(begin,end)
    myMediator=mediator_factory(trade_strategy=B1S1,pricer = oo_pricer)
    seller = atr_seller_factory(stop_times=600,trace_times=3000) 
    #seller = csc_func

    configs = prepare_configs_A(seller,pman,dman)
    #configs.extend(prepare_configs_B(seller,pman,dman))
    
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
    configs = prepare_temp_configs(seller)
    #configs = prepare_configs_A(seller,None,None)
    #configs.extend(prepare_configs_B(seller,None,None))
    
    mm_batch(configs,sdata,dates,xbegin)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    

    save_mm_configs('mm_ev_c.txt',configs,xbegin,end)
    #save_configs('atr_ev_mm_test.txt',configs,begin,end)

def run_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata.values())
    prepare_order(catalogs)
    dummy_catalogs('catalog',catalogs)
    run_body(sdata,dates,begin,end,xbegin)

def run_merge_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata.values())
    prepare_order(catalogs)    
    dummy_catalogs('catalog',catalogs)
    run_merge_body(sdata,dates,begin,end,xbegin)

def run_mm_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata.values())
    prepare_order(catalogs)    
    dummy_catalogs('catalog',catalogs)
    run_mm_body(sdata,dates,begin,end,xbegin)

def run_last(dates,sdata,idata,catalogs,begin,end,xbegin,lbegin=0):
    prepare_order(sdata.values())
    prepare_order(catalogs)    
    dummy_catalogs('catalog',catalogs)
    from time import time
    tbegin = time()

    pman = None
    dman = None
    myMediator=mediator_factory(trade_strategy=B0S0,pricer = oo_pricer)
    #seller = atr_seller_factory(stop_times=2000,trace_times=3000)
    seller = atr_seller_factory(stop_times=600,trace_times=3000)
    #seller = csc_func
    if lbegin == 0:
        lbegin = end - 5

    configs_a = prepare_configs_A(seller,pman,dman)
    dtrades_a = batch_last(configs_a,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_a.txt',dtrades_a,xbegin,end,lbegin)

    configs_a1 = prepare_configs_A1(seller,pman,dman)
    dtrades_a1 = batch_last(configs_a1,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_a1.txt',dtrades_a1,xbegin,end,lbegin)

    configs_a2 = prepare_configs_A2(seller,pman,dman)
    dtrades_a2 = batch_last(configs_a2,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_a2.txt',dtrades_a2,xbegin,end,lbegin)

    configs_b = prepare_configs_B(seller,pman,dman)
    dtrades_b = batch_last(configs_b,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_b.txt',dtrades_b,xbegin,end,lbegin)

    #configs_t = prepare_temp_configs(seller,pman,dman)
    #dtrades_t = batch_last(configs_t,sdata,dates,xbegin,cmediator=myMediator)
    #save_last('atr_last_t.txt',dtrades_t,xbegin,end,lbegin)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    


if __name__ == '__main__':
    logging.basicConfig(filename="run_x4f.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    #测试时间段 [19980101,19990101-20010801],[20000101,20010701-20050901],[20040601,20050801-20071031],[20060601,20071031-20090101]
    #总时间段   [20000101,20010701,20090101]    #一个完整的周期+一个下降段
    #分段测试的要求，段mm > 1000-1500或抑制，总段mm > 2000
    
    #begin,xbegin,end = 20000101,20010701,20090101
    #begin,xbegin,end = 19980101,20010701,20090101
    #begin,xbegin,end = 20000101,20010701,20050901
    #begin,xbegin,end = 19980101,19990701,20010801    
    #begin,xbegin,end = 20040601,20050801,20071031
    begin,xbegin,end = 20060601,20071031,20090101
    #begin,xbegin,end = 19980101,19990101,20090101
    #begin,xbegin,end,lbegin = 20070101,20080601,20090327,20081101
    #begin,xbegin,end,lbegin = 20060101,20070901,20090327,20090201
    #begin,xbegin,end = 20080701,20090101,20090301
    #begin,xbegin,end = 20080701,20090101,20090301
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
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600002'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600766'],[ref_code])
    tend = time()
    print u'数据准备耗时: %s' % (tend-tbegin)    
    import psyco
    psyco.full()

    #run_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    #run_merge_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    run_mm_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    #run_last(dates,sdata,idata,catalogs,begin,end,xbegin,lbegin)

    #近期工作 将svama2x/vama2x改造为syntony

    #prepare_order(sdata.values())
    #prepare_order(catalogs)
    #dummy_catalogs('catalog',catalogs)
    #for c in sdata[816].catalog:
    #    print c.name,c.g20
