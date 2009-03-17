# -*- coding: utf-8 -*-

#完整的运行脚本

from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *

import logging
logger = logging.getLogger('wolfox.fengine.normal.run')    


#1 缩小止损，止损和跟随建议为1600/2400
#2 信号出来后打到55/120均线附近

def prepare_temp_configs_0(seller,pman=None,dman=None):
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []

    configs.append(config(buyer=fcustom(csvama2,fast= 13,slow=125,rstart=3000,rend=9000))) 	#balance=1017,times= 47
    configs.append(config(buyer=fcustom(csvama2,fast=  4,slow=275,rstart=  0,rend=9000))) 	#balance=1037,times= 37
    configs.append(config(buyer=fcustom(csvama2,fast= 10,slow=305,rstart=  0,rend=9500))) 	#balance=1077,times= 37
    configs.append(config(buyer=fcustom(csvama2,fast= 34,slow=250,rstart=500,rend=8500))) 	#balance=1101,times= 28
    configs.append(config(buyer=fcustom(csvama2,fast=  1,slow=265,rstart=  0,rend=9000))) 	#balance=1128,times= 24
    configs.append(config(buyer=fcustom(csvama2,fast= 37,slow=115,rstart=3000,rend=9500))) 	#balance=1228,times= 42
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=280,rstart=  0,rend=4500))) 	#balance=1373,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=  1,slow=265,rstart=7000,rend=9500))) 	#balance=1506,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 47,slow=400,rstart=4500,rend=6000))) 	#balance=1557,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 13,slow=275,rstart=2500,rend=6000))) 	#balance=1831,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=250,rstart=500,rend=10000))) 	#balance=1905,times= 39
    configs.append(config(buyer=fcustom(csvama2,fast= 13,slow=125,rstart=  0,rend=1500))) 	#balance=1924,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 34,slow=425,rstart=500,rend=5000))) 	#balance=2208,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 43,slow=  5,rstart=3500,rend=8000))) 	#balance=2856,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 34,slow=280,rstart=3000,rend=4500))) 	#balance=6140,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast=  2,slow=250,rstart=500,rend=4000))) 	#balance=9555,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=  2,slow=250,rstart=8000,rend=8500))) 	#balance=14376,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast=  1,slow=250,rstart=2500,rend=4000))) 	#balance=28344,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=250,rstart=  0,rend=6000))) 	#balance=9103,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=250,rstart=500,rend=4000))) 	#balance=13819,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=275,rstart=1000,rend=10000))) 	#balance=1088,times= 42
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=250,rstart=2500,rend=6000))) 	#balance=15664,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=250,rstart=2500,rend=4000))) 	#balance=57818,times=  4    

    configs.append(config(buyer=fcustom(csvama2,fast= 16,slow=415,rstart=3500,rend=5000))) 	#balance=1023,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow= 20,rstart=2500,rend=4500))) 	#balance=1075,times= 16
    configs.append(config(buyer=fcustom(csvama2,fast= 34,slow=275,rstart=5000,rend=6500))) 	#balance=1910,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=265,rstart=2500,rend=8000))) 	#balance=1006,times= 24
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=455,rstart=6000,rend=9500))) 	#balance=1016,times= 41
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=250,rstart=2000,rend=6000))) 	#balance=1029,times= 24
    configs.append(config(buyer=fcustom(csvama2,fast= 23,slow=380,rstart=3000,rend=6000))) 	#balance=1030,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast=  3,slow=260,rstart=2000,rend=7000))) 	#balance=1046,times= 22
    configs.append(config(buyer=fcustom(csvama2,fast= 10,slow= 60,rstart=5000,rend=8000))) 	#balance=1064,times= 46
    configs.append(config(buyer=fcustom(csvama2,fast= 23,slow=260,rstart=2000,rend=8000))) 	#balance=1069,times= 28
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=250,rstart=3500,rend=5500))) 	#balance=1081,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow= 20,rstart=2500,rend=5500))) 	#balance=1097,times= 21
    configs.append(config(buyer=fcustom(csvama2,fast= 13,slow= 60,rstart=6000,rend=8000))) 	#balance=1104,times= 38
    configs.append(config(buyer=fcustom(csvama2,fast= 22,slow=305,rstart=2500,rend=6000))) 	#balance=1141,times= 16
    configs.append(config(buyer=fcustom(csvama2,fast= 26,slow=280,rstart=5000,rend=8000))) 	#balance=1160,times= 25
    configs.append(config(buyer=fcustom(csvama2,fast= 23,slow=260,rstart=3500,rend=7500))) 	#balance=1225,times= 22
    configs.append(config(buyer=fcustom(csvama2,fast=  8,slow= 20,rstart=2500,rend=5000))) 	#balance=1273,times= 16
    configs.append(config(buyer=fcustom(csvama2,fast= 16,slow= 10,rstart=5500,rend=6500))) 	#balance=1279,times=  1
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow= 45,rstart=7000,rend=7500))) 	#balance=1279,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=395,rstart=3000,rend=5500))) 	#balance=1459,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast=  4,slow= 55,rstart=7000,rend=7500))) 	#balance=1473,times= 15
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=385,rstart=7000,rend=7500))) 	#balance=1682,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=385,rstart=3500,rend=6000))) 	#balance=1699,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 29,slow=385,rstart=3500,rend=6000))) 	#balance=1699,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=395,rstart=3500,rend=5500))) 	#balance=1920,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 10,slow=260,rstart=5000,rend=6000))) 	#balance=2067,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 43,slow=350,rstart=3500,rend=4500))) 	#balance=2584,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=  8,slow=175,rstart=5500,rend=6000))) 	#balance=3404,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=  2,slow= 35,rstart=1000,rend=3000))) 	#balance=6284,times=  1
    configs.append(config(buyer=fcustom(csvama2,fast=  7,slow=240,rstart=5000,rend=7000))) 	#balance=1004,times= 20
    configs.append(config(buyer=fcustom(csvama2,fast= 38,slow=360,rstart=1500,rend=6000))) 	#balance=1006,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast=  1,slow=355,rstart=3000,rend=6000))) 	#balance=1007,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 13,slow=360,rstart=1000,rend=5000))) 	#balance=1012,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=240,rstart=2500,rend=6500))) 	#balance=1024,times= 20
    configs.append(config(buyer=fcustom(csvama2,fast=  4,slow=240,rstart=4500,rend=7000))) 	#balance=1027,times= 23
    configs.append(config(buyer=fcustom(csvama2,fast= 47,slow=200,rstart=2500,rend=6500))) 	#balance=1038,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=225,rstart=4500,rend=6500))) 	#balance=1050,times= 18
    configs.append(config(buyer=fcustom(csvama2,fast=  6,slow=240,rstart=1500,rend=6500))) 	#balance=1050,times= 25
    configs.append(config(buyer=fcustom(csvama2,fast= 13,slow=365,rstart=4500,rend=6500))) 	#balance=1057,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast=  6,slow=240,rstart=3500,rend=7000))) 	#balance=1060,times= 27
    configs.append(config(buyer=fcustom(csvama2,fast=  6,slow= 55,rstart=3000,rend=5000))) 	#balance=1068,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 44,slow=240,rstart=4000,rend=6500))) 	#balance=1080,times= 14
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=200,rstart=4500,rend=6500))) 	#balance=1121,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast= 15,slow=235,rstart=5000,rend=8000))) 	#balance=1147,times= 22
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=235,rstart=3000,rend=6000))) 	#balance=1163,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=240,rstart=3000,rend=6500))) 	#balance=1167,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=200,rstart=4000,rend=6500))) 	#balance=1203,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=240,rstart=5500,rend=7000))) 	#balance=1234,times= 14
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=130,rstart=7000,rend=8500))) 	#balance=1236,times= 15
    configs.append(config(buyer=fcustom(csvama2,fast= 31,slow=240,rstart=4500,rend=7000))) 	#balance=1244,times= 18
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=125,rstart=4500,rend=6500))) 	#balance=1310,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=355,rstart=2000,rend=6000))) 	#balance=1355,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast= 41,slow=240,rstart=3000,rend=6500))) 	#balance=1359,times= 14
    configs.append(config(buyer=fcustom(csvama2,fast= 31,slow=200,rstart=4500,rend=7000))) 	#balance=1373,times= 16
    configs.append(config(buyer=fcustom(csvama2,fast= 38,slow=325,rstart=4500,rend=7000))) 	#balance=1390,times= 16
    configs.append(config(buyer=fcustom(csvama2,fast=  6,slow=235,rstart=4500,rend=6000))) 	#balance=1409,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast= 15,slow=215,rstart=2500,rend=3500))) 	#balance=1441,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 38,slow=475,rstart=4500,rend=7000))) 	#balance=1441,times= 26
    configs.append(config(buyer=fcustom(csvama2,fast= 44,slow=240,rstart=4500,rend=5000))) 	#balance=1466,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 45,slow=240,rstart=4500,rend=5000))) 	#balance=1466,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 38,slow=235,rstart=2000,rend=7000))) 	#balance=1481,times= 19
    configs.append(config(buyer=fcustom(csvama2,fast=  4,slow=355,rstart=4000,rend=6000))) 	#balance=1496,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast=  1,slow=240,rstart=5000,rend=6500))) 	#balance=1568,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=330,rstart=2000,rend=5000))) 	#balance=1621,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=395,rstart=2000,rend=3000))) 	#balance=1627,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 31,slow=325,rstart=4500,rend=7000))) 	#balance=1647,times= 15
    configs.append(config(buyer=fcustom(csvama2,fast=  6,slow=240,rstart=4500,rend=6500))) 	#balance=1650,times= 18
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=240,rstart=4500,rend=6500))) 	#balance=1650,times= 18
    configs.append(config(buyer=fcustom(csvama2,fast=  6,slow=330,rstart=4000,rend=6000))) 	#balance=1793,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 44,slow=355,rstart=2000,rend=6000))) 	#balance=1818,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast=  6,slow=325,rstart=4500,rend=6500))) 	#balance=1953,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=325,rstart=4500,rend=6500))) 	#balance=1953,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast=  4,slow=325,rstart=4500,rend=6500))) 	#balance=1953,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=325,rstart=4500,rend=6500))) 	#balance=1996,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 38,slow=330,rstart=1500,rend=6000))) 	#balance=2097,times= 15
    configs.append(config(buyer=fcustom(csvama2,fast= 37,slow=330,rstart=1500,rend=6000))) 	#balance=2097,times= 15
    configs.append(config(buyer=fcustom(csvama2,fast= 38,slow=330,rstart=2500,rend=5500))) 	#balance=2194,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 37,slow=325,rstart=4500,rend=6500))) 	#balance=2261,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast= 38,slow=330,rstart=4000,rend=6000))) 	#balance=2430,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast= 46,slow=345,rstart=4500,rend=5000))) 	#balance=2563,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=155,rstart=2000,rend=4000))) 	#balance=4203000,times=  1
    configs.append(config(buyer=fcustom(csvama2,fast=  8,slow=170,rstart=5000,rend=7000))) 	#balance=1003,times= 15
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=260,rstart=3000,rend=8000))) 	#balance=1006,times= 27
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=260,rstart=3500,rend=8000))) 	#balance=1006,times= 27
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=250,rstart=4000,rend=6500))) 	#balance=1025,times= 15
    configs.append(config(buyer=fcustom(csvama2,fast= 28,slow=255,rstart=3000,rend=6500))) 	#balance=1026,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast= 44,slow=250,rstart=  0,rend=6500))) 	#balance=1028,times= 17
    configs.append(config(buyer=fcustom(csvama2,fast= 44,slow=250,rstart=1000,rend=6500))) 	#balance=1028,times= 17
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=175,rstart=1000,rend=7500))) 	#balance=1029,times= 24
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=255,rstart=3000,rend=8000))) 	#balance=1030,times= 26
    configs.append(config(buyer=fcustom(csvama2,fast= 44,slow=255,rstart=500,rend=8000))) 	#balance=1033,times= 26
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=170,rstart=5000,rend=7000))) 	#balance=1037,times= 14
    configs.append(config(buyer=fcustom(csvama2,fast=  3,slow= 15,rstart=3000,rend=4500))) 	#balance=1061,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=260,rstart=5000,rend=6500))) 	#balance=1074,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast= 23,slow=100,rstart=3500,rend=8000))) 	#balance=1090,times= 33
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=170,rstart=1000,rend=7500))) 	#balance=1095,times= 19
    configs.append(config(buyer=fcustom(csvama2,fast= 43,slow=260,rstart=5000,rend=8000))) 	#balance=1097,times= 21
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=255,rstart=1000,rend=6500))) 	#balance=1122,times= 17
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=255,rstart=  0,rend=6500))) 	#balance=1122,times= 17
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=170,rstart=5000,rend=7500))) 	#balance=1125,times= 19
    configs.append(config(buyer=fcustom(csvama2,fast= 39,slow=280,rstart=5000,rend=6500))) 	#balance=1133,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 44,slow=270,rstart=5000,rend=8500))) 	#balance=1136,times= 23
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=170,rstart=5000,rend=7000))) 	#balance=1137,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=250,rstart=5000,rend=7500))) 	#balance=1139,times= 17
    configs.append(config(buyer=fcustom(csvama2,fast= 20,slow= 95,rstart=5000,rend=7500))) 	#balance=1170,times= 24
    configs.append(config(buyer=fcustom(csvama2,fast= 20,slow=415,rstart=2000,rend=6000))) 	#balance=1170,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast=  1,slow=210,rstart=5000,rend=7500))) 	#balance=1177,times= 17
    configs.append(config(buyer=fcustom(csvama2,fast= 44,slow=300,rstart=5000,rend=6500))) 	#balance=1189,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=290,rstart=5000,rend=6500))) 	#balance=1189,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast= 44,slow=295,rstart=5000,rend=6500))) 	#balance=1189,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast= 26,slow=300,rstart=5500,rend=7500))) 	#balance=1202,times= 17
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=290,rstart=4000,rend=6500))) 	#balance=1202,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast= 26,slow=255,rstart=3500,rend=7500))) 	#balance=1203,times= 17
    configs.append(config(buyer=fcustom(csvama2,fast= 20,slow=195,rstart=5000,rend=7500))) 	#balance=1211,times= 20
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=175,rstart=1000,rend=8000))) 	#balance=1226,times= 27
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=295,rstart=5000,rend=6500))) 	#balance=1231,times= 14
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=175,rstart=1000,rend=6500))) 	#balance=1240,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=175,rstart=  0,rend=6500))) 	#balance=1240,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=260,rstart=1000,rend=6500))) 	#balance=1241,times= 19
    configs.append(config(buyer=fcustom(csvama2,fast=  7,slow=240,rstart=5000,rend=6500))) 	#balance=1243,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast= 33,slow=250,rstart=5000,rend=7500))) 	#balance=1250,times= 17
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=290,rstart=4000,rend=6500))) 	#balance=1266,times= 15
    configs.append(config(buyer=fcustom(csvama2,fast=  3,slow=385,rstart=4500,rend=5000))) 	#balance=1269,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 28,slow=320,rstart=5000,rend=6500))) 	#balance=1286,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 35,slow=200,rstart=1000,rend=7000))) 	#balance=1325,times= 16
    configs.append(config(buyer=fcustom(csvama2,fast=  8,slow=250,rstart=5000,rend=6500))) 	#balance=1331,times= 15
    configs.append(config(buyer=fcustom(csvama2,fast= 35,slow=200,rstart=1000,rend=6500))) 	#balance=1348,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=290,rstart=  0,rend=6500))) 	#balance=1351,times= 14
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=165,rstart=5000,rend=6500))) 	#balance=1360,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast=  4,slow=175,rstart=5000,rend=6500))) 	#balance=1381,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 44,slow=255,rstart=5000,rend=6500))) 	#balance=1394,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=170,rstart=5000,rend=7500))) 	#balance=1405,times= 14
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=255,rstart=1000,rend=6500))) 	#balance=1408,times= 20
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=255,rstart=500,rend=6500))) 	#balance=1408,times= 20
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=290,rstart=  0,rend=6500))) 	#balance=1424,times= 17
    configs.append(config(buyer=fcustom(csvama2,fast= 39,slow=200,rstart=5000,rend=8000))) 	#balance=1434,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast= 15,slow=200,rstart=5000,rend=6500))) 	#balance=1456,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast=  6,slow=170,rstart=5000,rend=6500))) 	#balance=1464,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=250,rstart=  0,rend=6500))) 	#balance=1472,times= 18
    configs.append(config(buyer=fcustom(csvama2,fast= 46,slow=170,rstart=5000,rend=6500))) 	#balance=1518,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 15,slow=260,rstart=5000,rend=6500))) 	#balance=1529,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast=  8,slow=190,rstart=5000,rend=6500))) 	#balance=1541,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast=  8,slow=170,rstart=5000,rend=6500))) 	#balance=1568,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast=  7,slow=200,rstart=5000,rend=8000))) 	#balance=1575,times= 25
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=210,rstart=5500,rend=7500))) 	#balance=1588,times= 14
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=255,rstart=5000,rend=6500))) 	#balance=1590,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=250,rstart=4000,rend=6500))) 	#balance=1599,times= 15
    configs.append(config(buyer=fcustom(csvama2,fast= 35,slow=255,rstart=4500,rend=7000))) 	#balance=1625,times= 18
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=170,rstart=3000,rend=6500))) 	#balance=1634,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=170,rstart=3000,rend=6500))) 	#balance=1634,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=170,rstart=1000,rend=6500))) 	#balance=1634,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 34,slow=250,rstart=  0,rend=6500))) 	#balance=1647,times= 18
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=250,rstart=5000,rend=6500))) 	#balance=1647,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=280,rstart=5000,rend=6500))) 	#balance=1657,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast=  8,slow=175,rstart=5000,rend=7500))) 	#balance=1657,times= 16
    configs.append(config(buyer=fcustom(csvama2,fast= 44,slow=190,rstart=5000,rend=7500))) 	#balance=1658,times= 14
    configs.append(config(buyer=fcustom(csvama2,fast= 26,slow=250,rstart=5000,rend=6500))) 	#balance=1659,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast=  4,slow=170,rstart=5000,rend=6500))) 	#balance=1681,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast=  8,slow=200,rstart=5000,rend=6500))) 	#balance=1686,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=250,rstart=5000,rend=6500))) 	#balance=1697,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast=  8,slow=175,rstart=5000,rend=8000))) 	#balance=1706,times= 20
    configs.append(config(buyer=fcustom(csvama2,fast= 39,slow=260,rstart=5000,rend=7000))) 	#balance=1721,times= 14
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=255,rstart=5000,rend=6500))) 	#balance=1733,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast=  4,slow=300,rstart=5000,rend=6500))) 	#balance=1758,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 28,slow=170,rstart=5000,rend=6500))) 	#balance=1760,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=170,rstart=3000,rend=6500))) 	#balance=1766,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=170,rstart=1000,rend=6500))) 	#balance=1766,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 26,slow=280,rstart=5000,rend=6500))) 	#balance=1796,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 44,slow=250,rstart=5000,rend=6500))) 	#balance=1840,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=200,rstart=5000,rend=6500))) 	#balance=1891,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 34,slow=250,rstart=4000,rend=6500))) 	#balance=1938,times= 15
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=295,rstart=5000,rend=6500))) 	#balance=1980,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 44,slow=170,rstart=5000,rend=6500))) 	#balance=1993,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=280,rstart=5000,rend=6500))) 	#balance=2068,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast= 39,slow=200,rstart=5000,rend=6500))) 	#balance=2072,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=250,rstart=5000,rend=6500))) 	#balance=2116,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 26,slow=300,rstart=5000,rend=6500))) 	#balance=2117,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=170,rstart=4000,rend=6500))) 	#balance=2127,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=170,rstart=4500,rend=6500))) 	#balance=2127,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast=  4,slow=190,rstart=5000,rend=6500))) 	#balance=2165,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 10,slow=195,rstart=5000,rend=6500))) 	#balance=2165,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast=  8,slow=290,rstart=5000,rend=6500))) 	#balance=2213,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast=  4,slow=255,rstart=5000,rend=6500))) 	#balance=2214,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 43,slow=190,rstart=5000,rend=6500))) 	#balance=2256,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=  7,slow=200,rstart=5000,rend=6500))) 	#balance=2298,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=170,rstart=4500,rend=6500))) 	#balance=2303,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=170,rstart=4000,rend=6500))) 	#balance=2303,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=250,rstart=5000,rend=6500))) 	#balance=2377,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=165,rstart=5000,rend=6500))) 	#balance=2389,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=165,rstart=5000,rend=6500))) 	#balance=2389,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast=  4,slow=200,rstart=5000,rend=6500))) 	#balance=2395,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=255,rstart=5000,rend=6500))) 	#balance=2432,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=190,rstart=5000,rend=6500))) 	#balance=2478,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=190,rstart=5000,rend=6500))) 	#balance=2478,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 44,slow=190,rstart=5000,rend=6500))) 	#balance=2599,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 16,slow=170,rstart=5000,rend=6500))) 	#balance=3077,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast=  8,slow=300,rstart=5000,rend=6500))) 	#balance=3387,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=210,rstart=5000,rend=6500))) 	#balance=3474,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=200,rstart=5000,rend=6500))) 	#balance=4019,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=210,rstart=5000,rend=6500))) 	#balance=4186,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast= 15,slow=170,rstart=5000,rend=6500))) 	#balance=4450,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=170,rstart=5000,rend=6500))) 	#balance=4656,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 13,slow=170,rstart=5000,rend=6500))) 	#balance=4656,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 10,slow=170,rstart=5000,rend=6500))) 	#balance=4656,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=170,rstart=5000,rend=6500))) 	#balance=4656,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=170,rstart=5000,rend=6500))) 	#balance=4703,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 48,slow=385,rstart=2500,rend=4000))) 	#balance=4860,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=290,rstart=4000,rend=4500))) 	#balance=4977000,times=  1
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=400,rstart=5000,rend=5500))) 	#balance=1005,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=320,rstart=2500,rend=6500))) 	#balance=1020,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=205,rstart=5000,rend=6500))) 	#balance=1026,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=320,rstart=4500,rend=7000))) 	#balance=1048,times= 17
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=155,rstart=2500,rend=4500))) 	#balance=1054,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=  8,slow=150,rstart=2500,rend=6000))) 	#balance=1054,times= 19
    configs.append(config(buyer=fcustom(csvama2,fast= 40,slow=365,rstart=  0,rend=6000))) 	#balance=1057,times= 14
    configs.append(config(buyer=fcustom(csvama2,fast= 23,slow=385,rstart=  0,rend=4000))) 	#balance=1064,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=320,rstart=5000,rend=8500))) 	#balance=1079,times= 29
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=225,rstart=3000,rend=8500))) 	#balance=1080,times= 37
    configs.append(config(buyer=fcustom(csvama2,fast= 21,slow=385,rstart=5500,rend=6000))) 	#balance=1084,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast= 31,slow=385,rstart=  0,rend=4000))) 	#balance=1116,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 40,slow=370,rstart=2500,rend=6000))) 	#balance=1134,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast= 13,slow=240,rstart=5000,rend=8500))) 	#balance=1165,times= 29
    configs.append(config(buyer=fcustom(csvama2,fast= 32,slow=290,rstart=2500,rend=6000))) 	#balance=1173,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=225,rstart=3000,rend=6500))) 	#balance=1177,times= 18
    configs.append(config(buyer=fcustom(csvama2,fast= 27,slow=205,rstart=5000,rend=7000))) 	#balance=1192,times= 15
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=225,rstart=3500,rend=6500))) 	#balance=1200,times= 17
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=450,rstart=5000,rend=5500))) 	#balance=1212,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=445,rstart=5000,rend=6500))) 	#balance=1230,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=220,rstart=2500,rend=6500))) 	#balance=1244,times= 21
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=140,rstart=5000,rend=6000))) 	#balance=1283,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 15,slow=230,rstart=5000,rend=8500))) 	#balance=1298,times= 23
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=365,rstart=5000,rend=5500))) 	#balance=1327,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 21,slow=390,rstart=5000,rend=5500))) 	#balance=1327,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 23,slow=315,rstart=2500,rend=6000))) 	#balance=1339,times= 14
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=160,rstart=3000,rend=6500))) 	#balance=1351,times= 14
    configs.append(config(buyer=fcustom(csvama2,fast= 33,slow=400,rstart=1000,rend=6500))) 	#balance=1355,times= 20
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=205,rstart=5000,rend=8500))) 	#balance=1357,times= 24
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=475,rstart=5000,rend=6000))) 	#balance=1365,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 31,slow=315,rstart=2500,rend=6000))) 	#balance=1368,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast= 31,slow=385,rstart=3500,rend=6500))) 	#balance=1399,times= 14
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=205,rstart=7000,rend=8500))) 	#balance=1439,times= 14
    configs.append(config(buyer=fcustom(csvama2,fast= 24,slow=290,rstart=2500,rend=4000))) 	#balance=1441,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=300,rstart=2500,rend=4000))) 	#balance=1441,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 23,slow=390,rstart=2500,rend=4000))) 	#balance=1441,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=365,rstart=5500,rend=6500))) 	#balance=1447,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=160,rstart=4500,rend=8500))) 	#balance=1453,times= 33
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=475,rstart=5000,rend=6500))) 	#balance=1463,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=240,rstart=5000,rend=6500))) 	#balance=1464,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=470,rstart=5000,rend=6000))) 	#balance=1464,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 26,slow=475,rstart=5000,rend=6000))) 	#balance=1464,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 26,slow=460,rstart=5000,rend=6000))) 	#balance=1464,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=460,rstart=5000,rend=6000))) 	#balance=1464,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=445,rstart=5000,rend=6000))) 	#balance=1464,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=440,rstart=5000,rend=6000))) 	#balance=1464,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 33,slow=380,rstart=5000,rend=6500))) 	#balance=1474,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=410,rstart=4500,rend=5500))) 	#balance=1504,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=285,rstart=4500,rend=6000))) 	#balance=1510,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 32,slow=315,rstart=2500,rend=6000))) 	#balance=1510,times= 14
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=365,rstart=5000,rend=6500))) 	#balance=1518,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=300,rstart=5000,rend=6500))) 	#balance=1522,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=205,rstart=5000,rend=7000))) 	#balance=1544,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=225,rstart=3500,rend=7000))) 	#balance=1578,times= 22
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=320,rstart=2500,rend=6000))) 	#balance=1592,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast= 31,slow=305,rstart=3500,rend=6000))) 	#balance=1617,times= 16
    configs.append(config(buyer=fcustom(csvama2,fast= 37,slow=400,rstart=1000,rend=6500))) 	#balance=1646,times= 23
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=400,rstart=5000,rend=6000))) 	#balance=1671,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=160,rstart=2500,rend=6500))) 	#balance=1732,times= 15
    configs.append(config(buyer=fcustom(csvama2,fast= 27,slow=205,rstart=5500,rend=7000))) 	#balance=1747,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=205,rstart=4500,rend=8500))) 	#balance=1750,times= 34
    configs.append(config(buyer=fcustom(csvama2,fast= 37,slow=400,rstart=1000,rend=6000))) 	#balance=1772,times= 20
    configs.append(config(buyer=fcustom(csvama2,fast= 40,slow=370,rstart=5000,rend=6000))) 	#balance=1797,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 32,slow=470,rstart=5000,rend=6000))) 	#balance=1827,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=400,rstart=5000,rend=6500))) 	#balance=1935,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast= 27,slow=205,rstart=5500,rend=6000))) 	#balance=2003,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=475,rstart=5000,rend=6000))) 	#balance=2153,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=320,rstart=5000,rend=6500))) 	#balance=2383,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=285,rstart=5000,rend=6000))) 	#balance=2599,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 13,slow=290,rstart=5000,rend=6000))) 	#balance=2691,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=205,rstart=5000,rend=7000))) 	#balance=2813,times= 16
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=290,rstart=5000,rend=6500))) 	#balance=2837,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=210,rstart=5000,rend=7000))) 	#balance=2930,times= 16
    configs.append(config(buyer=fcustom(csvama2,fast= 27,slow=285,rstart=5000,rend=6000))) 	#balance=3014,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 47,slow=325,rstart=1000,rend=3000))) 	#balance=3349,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 41,slow=360,rstart=500,rend=3000))) 	#balance=3349,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 37,slow=400,rstart=5000,rend=5500))) 	#balance=3517,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=285,rstart=5000,rend=6000))) 	#balance=3733,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=320,rstart=5000,rend=6000))) 	#balance=4667,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=300,rstart=5000,rend=5500))) 	#balance=5771,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=165,rstart=500,rend=3500))) 	#balance=4203000,times=  1
    configs.append(config(buyer=fcustom(csvama2,fast= 39,slow=160,rstart=2500,rend=3500))) 	#balance=4203000,times=  1
    configs.append(config(buyer=fcustom(csvama2,fast= 47,slow=185,rstart=1500,rend=4000))) 	#balance=6073000,times=  1
    configs.append(config(buyer=fcustom(csvama2,fast=116,slow=325,rstart=2000,rend=10000))) 	#balance=1013,times= 54
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=335,rstart=5000,rend=8500))) 	#balance=1014,times= 29
    configs.append(config(buyer=fcustom(csvama2,fast= 33,slow=340,rstart=3500,rend=7500))) 	#balance=1018,times= 21
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=340,rstart=2000,rend=9000))) 	#balance=1041,times= 48
    configs.append(config(buyer=fcustom(csvama2,fast=144,slow=660,rstart=2000,rend=5500))) 	#balance=1051,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=136,slow=310,rstart=500,rend=3500))) 	#balance=1072,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast=  1,slow=340,rstart=3500,rend=6000))) 	#balance=1135,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=108,slow=165,rstart=4500,rend=8500))) 	#balance=1207,times= 32
    configs.append(config(buyer=fcustom(csvama2,fast=  1,slow=570,rstart=5000,rend=8000))) 	#balance=1209,times= 21
    configs.append(config(buyer=fcustom(csvama2,fast=184,slow=445,rstart=  0,rend=7500))) 	#balance=1236,times= 18
    configs.append(config(buyer=fcustom(csvama2,fast=104,slow=320,rstart=500,rend=5500))) 	#balance=1238,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast=132,slow=340,rstart=2000,rend=6000))) 	#balance=1274,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast=144,slow=385,rstart=500,rend=6000))) 	#balance=1298,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=144,slow=325,rstart=2500,rend=6000))) 	#balance=1301,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=112,slow=340,rstart=2000,rend=4000))) 	#balance=1305,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=335,rstart=2500,rend=8000))) 	#balance=1320,times= 31
    configs.append(config(buyer=fcustom(csvama2,fast= 33,slow=660,rstart=3000,rend=8000))) 	#balance=1365,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast=196,slow=490,rstart=1500,rend=4000))) 	#balance=1402,times=  1
    configs.append(config(buyer=fcustom(csvama2,fast=  1,slow=340,rstart=2000,rend=6000))) 	#balance=1422,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 33,slow=680,rstart=3500,rend=7500))) 	#balance=1422,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 33,slow=680,rstart=3000,rend=7500))) 	#balance=1422,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=112,slow=350,rstart=2000,rend=4000))) 	#balance=1431,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast= 26,slow=310,rstart=500,rend=3500))) 	#balance=1441,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=340,rstart=2500,rend=3500))) 	#balance=1441,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 39,slow=260,rstart=500,rend=3500))) 	#balance=1441,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 39,slow=340,rstart=2000,rend=3500))) 	#balance=1441,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast=176,slow=310,rstart=500,rend=7500))) 	#balance=1448,times= 19
    configs.append(config(buyer=fcustom(csvama2,fast=132,slow=305,rstart=  0,rend=4000))) 	#balance=1451,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast=184,slow=205,rstart=1500,rend=5500))) 	#balance=1486,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 87,slow=340,rstart=500,rend=6000))) 	#balance=1567,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast=104,slow=335,rstart=1500,rend=3500))) 	#balance=1604,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 39,slow=660,rstart=6000,rend=9500))) 	#balance=1626,times= 17
    configs.append(config(buyer=fcustom(csvama2,fast= 51,slow=590,rstart=500,rend=4500))) 	#balance=1627,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=132,slow=325,rstart=2000,rend=4000))) 	#balance=1629,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=132,slow=340,rstart=2000,rend=4000))) 	#balance=1629,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 33,slow=660,rstart=6000,rend=9500))) 	#balance=1687,times= 14
    configs.append(config(buyer=fcustom(csvama2,fast=116,slow=330,rstart=3500,rend=5500))) 	#balance=1700,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast=112,slow=340,rstart=2000,rend=5500))) 	#balance=1724,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast=100,slow=285,rstart=2000,rend=3500))) 	#balance=1758,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast=104,slow=320,rstart=500,rend=3500))) 	#balance=1796,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=104,slow=340,rstart=500,rend=3500))) 	#balance=1796,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=108,slow=305,rstart=500,rend=3500))) 	#balance=1796,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=104,slow=310,rstart=500,rend=3500))) 	#balance=1796,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=112,slow=680,rstart=1500,rend=5500))) 	#balance=1847,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=192,slow=225,rstart=1500,rend=5500))) 	#balance=1851,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast=310,slow=430,rstart=3000,rend=5000))) 	#balance=1858,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 72,slow=340,rstart=3500,rend=5500))) 	#balance=1876,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=112,slow=350,rstart=2000,rend=5500))) 	#balance=1896,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 39,slow=340,rstart=2000,rend=5500))) 	#balance=1897,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast=144,slow=260,rstart=  0,rend=6000))) 	#balance=1900,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast=104,slow=320,rstart=2000,rend=6000))) 	#balance=1936,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast=132,slow=285,rstart=  0,rend=6000))) 	#balance=1949,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast=108,slow=260,rstart=  0,rend=6000))) 	#balance=1958,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast=144,slow=340,rstart=2000,rend=6000))) 	#balance=1992,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=660,rstart=6000,rend=8000))) 	#balance=2016,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=112,slow=680,rstart=1500,rend=6000))) 	#balance=2030,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=112,slow=385,rstart=2500,rend=6000))) 	#balance=2074,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast=144,slow=305,rstart=1500,rend=6000))) 	#balance=2096,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=140,slow=310,rstart=1500,rend=5500))) 	#balance=2096,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=144,slow=305,rstart=2500,rend=6000))) 	#balance=2096,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=144,slow=300,rstart=  0,rend=6000))) 	#balance=2096,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=144,slow=305,rstart=500,rend=6000))) 	#balance=2096,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=580,rstart=4500,rend=6000))) 	#balance=2098,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast=  7,slow=660,rstart=6000,rend=9500))) 	#balance=2106,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast=144,slow=435,rstart=2000,rend=6000))) 	#balance=2131,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast=144,slow=305,rstart=500,rend=4000))) 	#balance=2278,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=116,slow=325,rstart=2000,rend=6000))) 	#balance=2700,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast=104,slow=365,rstart=2000,rend=5500))) 	#balance=2435,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=112,slow=345,rstart=2500,rend=6000))) 	#balance=2759,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast=100,slow=365,rstart=2000,rend=6000))) 	#balance=2365,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast=124,slow=305,rstart=500,rend=5500))) 	#balance=2859,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast=192,slow=305,rstart=2000,rend=6000))) 	#balance=2884,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 75,slow=370,rstart=2000,rend=6000))) 	#balance=3073,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=600,rstart=5000,rend=6000))) 	#balance=3095,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=108,slow=365,rstart=1000,rend=6000))) 	#balance=3427,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast=144,slow=340,rstart=2000,rend=5500))) 	#balance=3526,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast= 10,slow=325,rstart=5000,rend=6000))) 	#balance=4667,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=184,slow=305,rstart=4000,rend=5500))) 	#balance=3311000,times=  1
    configs.append(config(buyer=fcustom(csvama2,fast=132,slow=260,rstart=500,rend=3000))) 	#balance=3467000,times=  1
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=320,rstart=1500,rend=3000))) 	#balance=3467000,times=  1
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=320,rstart=3000,rend=8000))) 	#balance=1002,times= 25
    configs.append(config(buyer=fcustom(csvama2,fast=100,slow=215,rstart=3500,rend=6000))) 	#balance=1004,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=165,rstart=500,rend=5500))) 	#balance=1013,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=120,slow=640,rstart=4500,rend=6000))) 	#balance=1013,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=140,rstart=3500,rend=5000))) 	#balance=1021,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=192,slow=485,rstart=2500,rend=8500))) 	#balance=1026,times= 24
    configs.append(config(buyer=fcustom(csvama2,fast= 84,slow=265,rstart=500,rend=6000))) 	#balance=1028,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=185,rstart=2000,rend=8000))) 	#balance=1030,times= 24
    configs.append(config(buyer=fcustom(csvama2,fast=164,slow=550,rstart=4500,rend=6000))) 	#balance=1030,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 26,slow=300,rstart=3500,rend=7500))) 	#balance=1031,times= 28
    configs.append(config(buyer=fcustom(csvama2,fast=188,slow=460,rstart=1000,rend=8500))) 	#balance=1032,times= 28
    configs.append(config(buyer=fcustom(csvama2,fast= 57,slow=680,rstart=4000,rend=10000))) 	#balance=1040,times= 20
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=170,rstart=2000,rend=5000))) 	#balance=1042,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=100,slow=170,rstart=500,rend=5000))) 	#balance=1042,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=112,slow=135,rstart=2000,rend=5000))) 	#balance=1046,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 57,slow=270,rstart=3500,rend=6000))) 	#balance=1054,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast=188,slow=355,rstart=3000,rend=10000))) 	#balance=1055,times= 32
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=495,rstart=500,rend=5000))) 	#balance=1059,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 75,slow=325,rstart=2500,rend=7000))) 	#balance=1061,times= 17
    configs.append(config(buyer=fcustom(csvama2,fast=100,slow=175,rstart=4500,rend=6000))) 	#balance=1064,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=290,rstart=2000,rend=8000))) 	#balance=1066,times= 31
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=210,rstart=2000,rend=8000))) 	#balance=1072,times= 25
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=285,rstart=3000,rend=6000))) 	#balance=1077,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 63,slow=660,rstart=4500,rend=5000))) 	#balance=1080,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 57,slow=660,rstart=3500,rend=5000))) 	#balance=1080,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=  8,slow=175,rstart=4000,rend=10000))) 	#balance=1089,times= 42
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=500,rstart=4500,rend=5000))) 	#balance=1091,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=136,slow=640,rstart=4500,rend=6000))) 	#balance=1091,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 51,slow=260,rstart=2000,rend=5000))) 	#balance=1092,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=265,rstart=3500,rend=6000))) 	#balance=1096,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=270,rstart=2000,rend=8000))) 	#balance=1098,times= 25
    configs.append(config(buyer=fcustom(csvama2,fast=160,slow=500,rstart=3500,rend=6000))) 	#balance=1108,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast=108,slow=175,rstart=4500,rend=6000))) 	#balance=1108,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast=112,slow=325,rstart=500,rend=7500))) 	#balance=1113,times= 21
    configs.append(config(buyer=fcustom(csvama2,fast=140,slow=165,rstart=4500,rend=6000))) 	#balance=1113,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 51,slow=500,rstart=3500,rend=6000))) 	#balance=1124,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast=136,slow=680,rstart=3500,rend=6000))) 	#balance=1128,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=170,rstart=500,rend=6000))) 	#balance=1133,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=265,rstart=3000,rend=6000))) 	#balance=1135,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast=108,slow=185,rstart=3000,rend=7500))) 	#balance=1137,times= 14
    configs.append(config(buyer=fcustom(csvama2,fast=100,slow=130,rstart=2500,rend=5500))) 	#balance=1142,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 45,slow=270,rstart=1000,rend=6000))) 	#balance=1147,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 24,slow=485,rstart=5000,rend=8500))) 	#balance=1147,times= 32
    configs.append(config(buyer=fcustom(csvama2,fast= 51,slow=680,rstart=500,rend=5000))) 	#balance=1165,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=680,rstart=2000,rend=5000))) 	#balance=1165,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=192,slow=325,rstart=2500,rend=8500))) 	#balance=1172,times= 24
    configs.append(config(buyer=fcustom(csvama2,fast= 26,slow=680,rstart=2000,rend=8000))) 	#balance=1174,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=265,rstart=2000,rend=7500))) 	#balance=1180,times= 20
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=500,rstart=3500,rend=5500))) 	#balance=1185,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=290,rstart=2000,rend=6000))) 	#balance=1187,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast=140,slow=175,rstart=2000,rend=6000))) 	#balance=1191,times= 15
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=300,rstart=1000,rend=6000))) 	#balance=1192,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast=192,slow=325,rstart=4500,rend=8500))) 	#balance=1205,times= 23
    configs.append(config(buyer=fcustom(csvama2,fast=192,slow=325,rstart=4000,rend=8500))) 	#balance=1205,times= 23
    configs.append(config(buyer=fcustom(csvama2,fast=184,slow=330,rstart=4000,rend=9000))) 	#balance=1206,times= 22
    configs.append(config(buyer=fcustom(csvama2,fast= 48,slow=305,rstart=3000,rend=5000))) 	#balance=1207,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=108,slow=190,rstart=2000,rend=8000))) 	#balance=1208,times= 25
    configs.append(config(buyer=fcustom(csvama2,fast= 54,slow=285,rstart=500,rend=5500))) 	#balance=1233,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast=212,slow=610,rstart=4500,rend=10000))) 	#balance=1233,times= 27
    configs.append(config(buyer=fcustom(csvama2,fast=160,slow=500,rstart=4500,rend=6000))) 	#balance=1238,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=100,slow=265,rstart=6000,rend=8000))) 	#balance=1239,times= 18
    configs.append(config(buyer=fcustom(csvama2,fast= 93,slow=270,rstart=6000,rend=8000))) 	#balance=1239,times= 21
    configs.append(config(buyer=fcustom(csvama2,fast=140,slow=175,rstart=4500,rend=6000))) 	#balance=1241,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast=108,slow=265,rstart=500,rend=8000))) 	#balance=1250,times= 25
    configs.append(config(buyer=fcustom(csvama2,fast=108,slow=265,rstart=2000,rend=8000))) 	#balance=1250,times= 25
    configs.append(config(buyer=fcustom(csvama2,fast=164,slow=630,rstart=3000,rend=5500))) 	#balance=1252,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 51,slow=260,rstart=3000,rend=7000))) 	#balance=1268,times= 16
    configs.append(config(buyer=fcustom(csvama2,fast= 54,slow=300,rstart=1000,rend=5500))) 	#balance=1270,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=680,rstart=2000,rend=5000))) 	#balance=1271,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=100,slow=175,rstart=2000,rend=6000))) 	#balance=1275,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=175,rstart=500,rend=6000))) 	#balance=1275,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=285,rstart=2000,rend=6000))) 	#balance=1276,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast=108,slow=175,rstart=3500,rend=6000))) 	#balance=1279,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=210,rstart=2000,rend=4500))) 	#balance=1281,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=255,rstart=3500,rend=6000))) 	#balance=1289,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast=136,slow=410,rstart=4000,rend=6000))) 	#balance=1296,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=100,slow=135,rstart=2000,rend=5000))) 	#balance=1299,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast=100,slow=265,rstart=3000,rend=8000))) 	#balance=1303,times= 27
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=265,rstart=3000,rend=8000))) 	#balance=1316,times= 25
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=265,rstart=2000,rend=8000))) 	#balance=1316,times= 25
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=165,rstart=2000,rend=6000))) 	#balance=1333,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast=100,slow=165,rstart=4500,rend=6000))) 	#balance=1333,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=165,rstart=3500,rend=6000))) 	#balance=1333,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=295,rstart=2000,rend=7000))) 	#balance=1336,times= 21
    configs.append(config(buyer=fcustom(csvama2,fast= 63,slow=500,rstart=4500,rend=6000))) 	#balance=1338,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=500,rstart=3500,rend=5000))) 	#balance=1347,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=265,rstart=1000,rend=6000))) 	#balance=1351,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast=172,slow=680,rstart=4500,rend=6000))) 	#balance=1352,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=128,slow=680,rstart=3500,rend=6000))) 	#balance=1354,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=140,slow=185,rstart=3500,rend=6000))) 	#balance=1358,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 39,slow=290,rstart=2000,rend=5000))) 	#balance=1360,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=196,slow=445,rstart=500,rend=7500))) 	#balance=1373,times= 14
    configs.append(config(buyer=fcustom(csvama2,fast= 51,slow=290,rstart=500,rend=5000))) 	#balance=1380,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 57,slow=680,rstart=3500,rend=8000))) 	#balance=1383,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 57,slow=680,rstart=3000,rend=8000))) 	#balance=1383,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast=140,slow=485,rstart=500,rend=5500))) 	#balance=1387,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=270,rstart=500,rend=6000))) 	#balance=1398,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=270,rstart=3500,rend=6000))) 	#balance=1398,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast=100,slow=265,rstart=500,rend=6000))) 	#balance=1411,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast=100,slow=265,rstart=3500,rend=6000))) 	#balance=1411,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 26,slow=660,rstart=3000,rend=8000))) 	#balance=1417,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=510,rstart=5000,rend=6000))) 	#balance=1424,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 57,slow=650,rstart=2000,rend=8000))) 	#balance=1425,times= 17
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=270,rstart=2000,rend=5000))) 	#balance=1427,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 39,slow=445,rstart=2500,rend=3500))) 	#balance=1441,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 63,slow=640,rstart=3500,rend=5500))) 	#balance=1446,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=190,rstart=2000,rend=6000))) 	#balance=1454,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=140,slow=630,rstart=500,rend=5500))) 	#balance=1457,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast=144,slow=175,rstart=3500,rend=6000))) 	#balance=1461,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast=160,slow=500,rstart=4500,rend=5500))) 	#balance=1476,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=290,rstart=2000,rend=6000))) 	#balance=1487,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=285,rstart=2000,rend=6000))) 	#balance=1487,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=290,rstart=3500,rend=6000))) 	#balance=1487,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast=128,slow=500,rstart=3500,rend=5000))) 	#balance=1511,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=144,slow=650,rstart=3500,rend=6000))) 	#balance=1512,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=112,slow=255,rstart=2000,rend=5000))) 	#balance=1517,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=136,slow=680,rstart=4500,rend=6000))) 	#balance=1525,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=290,rstart=4500,rend=6000))) 	#balance=1556,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast=108,slow=165,rstart=2000,rend=6000))) 	#balance=1572,times= 15
    configs.append(config(buyer=fcustom(csvama2,fast= 84,slow=175,rstart=4500,rend=6000))) 	#balance=1596,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=680,rstart=4500,rend=7000))) 	#balance=1597,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 84,slow=175,rstart=2000,rend=6000))) 	#balance=1613,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=660,rstart=3500,rend=5500))) 	#balance=1623,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast= 66,slow=660,rstart=3500,rend=5500))) 	#balance=1623,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=100,slow=175,rstart=4500,rend=5500))) 	#balance=1625,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=108,slow=165,rstart=3000,rend=6000))) 	#balance=1682,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast=144,slow=415,rstart=1500,rend=6000))) 	#balance=1740,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=265,rstart=2000,rend=4000))) 	#balance=1747,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast=108,slow=265,rstart=1000,rend=6000))) 	#balance=1758,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast=108,slow=265,rstart=3000,rend=5000))) 	#balance=1758,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast=108,slow=165,rstart=4500,rend=6000))) 	#balance=1763,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=690,rstart=4000,rend=8000))) 	#balance=1804,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast=112,slow=690,rstart=4500,rend=6000))) 	#balance=1820,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=185,rstart=3500,rend=6000))) 	#balance=1841,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=185,rstart=3000,rend=6000))) 	#balance=1841,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 57,slow=265,rstart=5000,rend=6000))) 	#balance=1855,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 54,slow=300,rstart=5000,rend=5500))) 	#balance=1856,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast=180,slow=300,rstart=2000,rend=7500))) 	#balance=1876,times= 17
    configs.append(config(buyer=fcustom(csvama2,fast=180,slow=680,rstart=3500,rend=6000))) 	#balance=1882,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=128,slow=405,rstart=2500,rend=5500))) 	#balance=1891,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=116,slow=290,rstart=2000,rend=5000))) 	#balance=1914,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=500,rstart=3500,rend=6000))) 	#balance=1928,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=500,rstart=4500,rend=6000))) 	#balance=1934,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=290,rstart=3500,rend=6000))) 	#balance=1946,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 57,slow=660,rstart=500,rend=5000))) 	#balance=1952,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=500,rstart=500,rend=5500))) 	#balance=1955,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast=148,slow=290,rstart=2000,rend=6000))) 	#balance=1955,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=270,rstart=3500,rend=6000))) 	#balance=1964,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 45,slow=425,rstart=5000,rend=6000))) 	#balance=1979,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast=140,slow=285,rstart=3000,rend=6000))) 	#balance=1979,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast=140,slow=290,rstart=2000,rend=6000))) 	#balance=1979,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 57,slow=510,rstart=5000,rend=6000))) 	#balance=1981,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast=140,slow=680,rstart=3500,rend=6000))) 	#balance=2002,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=140,slow=680,rstart=4500,rend=6000))) 	#balance=2002,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=112,slow=165,rstart=4500,rend=5500))) 	#balance=2015,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast=192,slow=340,rstart=2500,rend=8500))) 	#balance=2044,times= 20
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=290,rstart=2000,rend=6000))) 	#balance=2194,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast=108,slow=165,rstart=4500,rend=5000))) 	#balance=2202,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=108,slow=190,rstart=3500,rend=6000))) 	#balance=2223,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=190,rstart=500,rend=6000))) 	#balance=2242,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast= 57,slow=680,rstart=3500,rend=6000))) 	#balance=2273,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=100,slow=185,rstart=3000,rend=6000))) 	#balance=2305,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast=140,slow=265,rstart=3000,rend=6000))) 	#balance=2342,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 51,slow=300,rstart=2000,rend=5000))) 	#balance=2346,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast=100,slow=185,rstart=4500,rend=5500))) 	#balance=2433,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=148,slow=680,rstart=3500,rend=5500))) 	#balance=2451,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=285,rstart=2000,rend=5000))) 	#balance=2467,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast= 45,slow=510,rstart=5000,rend=6000))) 	#balance=2474,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=172,slow=680,rstart=3500,rend=6000))) 	#balance=2516,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=185,rstart=500,rend=8000))) 	#balance=2537,times= 19
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=185,rstart=2000,rend=8000))) 	#balance=2537,times= 19
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=270,rstart=2000,rend=5000))) 	#balance=2550,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=140,slow=265,rstart=4500,rend=6000))) 	#balance=2577,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=425,rstart=4500,rend=6000))) 	#balance=2597,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 57,slow=425,rstart=4500,rend=6000))) 	#balance=2597,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast=140,slow=265,rstart=2000,rend=6000))) 	#balance=2619,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast=100,slow=175,rstart=500,rend=5500))) 	#balance=2633,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=660,rstart=4500,rend=6000))) 	#balance=2653,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 51,slow=255,rstart=500,rend=4000))) 	#balance=2664,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=240,slow=600,rstart=9500,rend=10000))) 	#balance=2678,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast=136,slow=690,rstart=4500,rend=6000))) 	#balance=2684,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=500,rstart=2000,rend=3000))) 	#balance=2701,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 51,slow=300,rstart=2000,rend=4500))) 	#balance=2865,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=144,slow=650,rstart=2000,rend=6000))) 	#balance=2896,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=670,rstart=4500,rend=5500))) 	#balance=3095,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=185,rstart=500,rend=5000))) 	#balance=3187,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast=100,slow=185,rstart=500,rend=5500))) 	#balance=3236,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 45,slow=265,rstart=5000,rend=6000))) 	#balance=3284,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=290,rstart=3500,rend=5000))) 	#balance=3303,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=136,slow=470,rstart=3500,rend=5000))) 	#balance=3334,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=140,slow=265,rstart=2000,rend=5000))) 	#balance=3361,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=680,rstart=4500,rend=6000))) 	#balance=3702,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=680,rstart=3500,rend=6000))) 	#balance=3702,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast= 51,slow=680,rstart=4500,rend=6000))) 	#balance=3796,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 51,slow=660,rstart=500,rend=5500))) 	#balance=3801,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=290,rstart=2000,rend=5000))) 	#balance=3838,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=290,rstart=2000,rend=3000))) 	#balance=4860,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=425,rstart=5000,rend=6000))) 	#balance=4902,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 57,slow=425,rstart=5000,rend=6000))) 	#balance=4902,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=285,rstart=2000,rend=4500))) 	#balance=4914,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 51,slow=290,rstart=2000,rend=4500))) 	#balance=5212,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=116,slow=210,rstart=2000,rend=5000))) 	#balance=5415,times=  1
    configs.append(config(buyer=fcustom(csvama2,fast= 51,slow=290,rstart=3000,rend=4500))) 	#balance=5483,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=500,rstart=500,rend=3000))) 	#balance=7167,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=680,rstart=3500,rend=6000))) 	#balance=9550,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 45,slow=630,rstart=5000,rend=6000))) 	#balance=12676,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=248,slow=395,rstart=1500,rend=3500))) 	#balance=4203000,times=  1
    

    configs.append(config(buyer=fcustom(csvama2,fast=132,slow=1990,rstart=3000,rend=10000))) 	#balance=7014000,times=  1
    configs.append(config(buyer=fcustom(csvama2,fast= 33,slow=1960,rstart=2000,rend=9500))) 	#balance=1137,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=144,slow=1930,rstart=2000,rend=10000))) 	#balance=1436,times=  6



    configs.append(config(buyer=fcustom(csvama2,fast= 26,slow=1420,rstart=3500,rend=9500))) 	#balance=1193,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=104,slow=1420,rstart=4500,rend=9500))) 	#balance=1543,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast=415,slow=1420,rstart=4500,rend=10000))) 	#balance=1706,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=1490,rstart=4000,rend=10000))) 	#balance=2452,times=  2

    configs.append(config(buyer=fcustom(csvama2,fast= 54,slow=1300,rstart=6000,rend=9500))) 	#balance=2497,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=495,slow=1340,rstart=6500,rend=10000))) 	#balance=1522,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast=104,slow=1300,rstart=500,rend=9500))) 	#balance=1246,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=1300,rstart=7500,rend=9500))) 	#balance=9429,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=715,slow=1370,rstart=1500,rend=9500))) 	#balance=1013,times=  1
    configs.append(config(buyer=fcustom(csvama2,fast=112,slow=1300,rstart=6000,rend=9500))) 	#balance=2834,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 39,slow=1300,rstart=500,rend=9000))) 	#balance=3127,times=  5
 
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=1300,rstart=6000,rend=9500))) 	#balance=1325,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 24,slow=1300,rstart=6000,rend=9500))) 	#balance=1322,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 45,slow=1300,rstart=7500,rend=9500))) 	#balance=25312,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=1300,rstart=6500,rend=9500))) 	#balance=5341,times=  6

    configs.append(config(buyer=fcustom(csvama2,fast=144,slow=1300,rstart=6000,rend=9500))) 	#balance=3083,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=272,slow=1300,rstart=6000,rend=9500))) 	#balance=1504,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast=260,slow=1350,rstart=2000,rend=10000))) 	#balance=1653,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=410,slow=1350,rstart=6000,rend=10000))) 	#balance=2434,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=410,slow=1330,rstart=2000,rend=10000))) 	#balance=4367,times=  4



    configs.append(config(buyer=fcustom(csvama2,fast=790,slow=810,rstart=2000,rend=4500))) 	#balance=11976,times=  1
    configs.append(config(buyer=fcustom(csvama2,fast=410,slow=820,rstart=2000,rend=10000))) 	#balance=1021,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 16,slow=810,rstart=6500,rend=10000))) 	#balance=1192,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast=  7,slow=840,rstart=6000,rend=10000))) 	#balance=1567,times= 13
    configs.append(config(buyer=fcustom(csvama2,fast=  8,slow=850,rstart=7000,rend=10000))) 	#balance=1771,times=  7

    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=180,rstart=3500,rend=8000))) 	#balance=2724,times= 20
    configs.append(config(buyer=fcustom(csvama2,fast= 39,slow=180,rstart=1000,rend=8000))) 	#balance=1155,times= 25
    configs.append(config(buyer=fcustom(csvama2,fast=  1,slow=180,rstart=1000,rend=3000))) 	#balance=6603,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast=  4,slow=180,rstart=5000,rend=6500))) 	#balance=1681,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 48,slow=180,rstart=3500,rend=5500))) 	#balance=1563,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 90,slow=180,rstart=500,rend=6000))) 	#balance=1330,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast=136,slow=180,rstart=3500,rend=5000))) 	#balance=3136,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=180,rstart=5000,rend=6500))) 	#balance=2114,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast=108,slow=180,rstart=500,rend=6000))) 	#balance=1734,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast=  7,slow=180,rstart=5000,rend=8000))) 	#balance=1179,times= 24
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=180,rstart=500,rend=5000))) 	#balance=6249,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=180,rstart=500,rend=3000))) 	#balance=8990,times=  2


    configs.append(config(buyer=fcustom(csvama2,fast= 16,slow=670,rstart=3000,rend=6000))) 	#balance=1018,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=124,slow=670,rstart=4500,rend=6000))) 	#balance=1480,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=670,rstart=3000,rend=8000))) 	#balance=1616,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=670,rstart=3500,rend=6000))) 	#balance=1790,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast=615,slow=670,rstart=5000,rend=6000))) 	#balance=4581,times=  1
    configs.append(config(buyer=fcustom(csvama2,fast= 33,slow=670,rstart=5000,rend=6000))) 	#balance=20338,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=670,rstart=5000,rend=6000))) 	#balance=3872000,times=  1
    configs.append(config(buyer=fcustom(csvama2,fast=164,slow=670,rstart=500,rend=5500))) 	#balance=4240,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 66,slow=670,rstart=4500,rend=6000))) 	#balance=4264,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=670,rstart=1000,rend=6000))) 	#balance=6228,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=670,rstart=5000,rend=6000))) 	#balance=13991,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=670,rstart=3500,rend=6000))) 	#balance=3796,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=140,slow=670,rstart=500,rend=6000))) 	#balance=2922,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 57,slow=670,rstart=1000,rend=6000))) 	#balance=8925,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 45,slow=670,rstart=1000,rend=6000))) 	#balance=5203,times=  8

    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=1140,rstart=6500,rend=9500))) 	#balance=1784,times=  9
    configs.append(config(buyer=fcustom(csvama2,fast= 33,slow=1120,rstart=1000,rend=6000))) 	#balance=3872000,times=  1
    configs.append(config(buyer=fcustom(csvama2,fast=635,slow=1110,rstart=1500,rend=7000))) 	#balance=3872000,times=  1
    configs.append(config(buyer=fcustom(csvama2,fast=595,slow=1170,rstart=2000,rend=9000))) 	#balance=9430,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=1140,rstart=6000,rend=10000))) 	#balance=1700,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast=935,slow=1120,rstart=8000,rend=10000))) 	#balance=3325000,times=  1
    configs.append(config(buyer=fcustom(csvama2,fast=116,slow=1130,rstart=2000,rend=7500))) 	#balance=1772,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 63,slow=1140,rstart=6000,rend=9500))) 	#balance=1504,times=  7

    configs.append(config(buyer=fcustom(csvama2,fast=  2,slow=1270,rstart=3000,rend=8000))) 	#balance=1729,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast=315,slow=1290,rstart=4500,rend=9000))) 	#balance=1076,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=1290,rstart=2000,rend=9500))) 	#balance=4513,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=1240,rstart=6000,rend=9500))) 	#balance=4513,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=156,slow=1240,rstart=2500,rend=7000))) 	#balance=2643,times=  1
 
    configs.append(config(buyer=fcustom(csvama2,fast= 28,slow=1280,rstart=6000,rend=9500))) 	#balance=4730,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 57,slow=1240,rstart=7000,rend=9500))) 	#balance=3687,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=585,slow=1220,rstart=6000,rend=9500))) 	#balance=4953,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 26,slow=1240,rstart=6000,rend=9500))) 	#balance=2706,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=1280,rstart=6000,rend=9500))) 	#balance=1954,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast= 26,slow=1240,rstart=4500,rend=10000))) 	#balance=1693,times= 12
    configs.append(config(buyer=fcustom(csvama2,fast= 24,slow=1260,rstart=3500,rend=9500))) 	#balance=1500,times=  8

    configs.append(config(buyer=fcustom(csvama2,fast= 45,slow=1240,rstart=6000,rend=9500))) 	#balance=12421,times=  4

    configs.append(config(buyer=fcustom(csvama2,fast= 39,slow=1240,rstart=5500,rend=9500))) 	#balance=1954,times=  6
    
    configs.append(config(buyer=fcustom(csvama2,fast=280,slow=1240,rstart=6000,rend=9500))) 	#balance=1649,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=440,slow=1680,rstart=4500,rend=9000))) 	#balance=4769,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast=132,slow=1690,rstart=2000,rend=10000))) 	#balance=2594,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=  1,slow=1600,rstart=1000,rend=9500))) 	#balance=3424,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 10,slow=1640,rstart=2000,rend=9500))) 	#balance=2165,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast= 39,slow=1640,rstart=1500,rend=9500))) 	#balance=1166,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=148,slow=1700,rstart=1000,rend=10000))) 	#balance=1896,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=140,slow=1810,rstart=2500,rend=10000))) 	#balance=1235,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=252,slow=1820,rstart=4500,rend=10000))) 	#balance=6263,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=645,slow=1030,rstart=4500,rend=8000))) 	#balance=2982,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 63,slow=920,rstart=2000,rend=10000))) 	#balance=1132,times= 10
    configs.append(config(buyer=fcustom(csvama2,fast=690,slow=980,rstart=5000,rend=9000))) 	#balance=1212,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=980,rstart=7500,rend=9500))) 	#balance=1543,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=315,slow=950,rstart=1500,rend=9000))) 	#balance=1985,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast=435,slow=960,rstart=2500,rend=6000))) 	#balance=4581,times=  1
    configs.append(config(buyer=fcustom(csvama2,fast=300,slow=940,rstart=1000,rend=8500))) 	#balance=2402,times=  2
 

    configs.append(config(buyer=fcustom(csvama2,fast=525,slow=710,rstart=1000,rend=9000))) 	#balance=1288,times= 11
    configs.append(config(buyer=fcustom(csvama2,fast=116,slow=710,rstart=2000,rend=6000))) 	#balance=2229,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=  2,slow=730,rstart=2000,rend=8000))) 	#balance=1189,times=  3

    configs.append(config(buyer=fcustom(csvama2,fast=  7,slow=720,rstart=  0,rend=6000))) 	#balance=1790,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=710,rstart=3000,rend=7500))) 	#balance=1857,times=  5
    
    configs.append(config(buyer=fcustom(csvama2,fast=136,slow=700,rstart=3500,rend=6000))) 	#balance=1431,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=700,rstart=2000,rend=6000))) 	#balance=1516,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=720,rstart=2000,rend=6000))) 	#balance=2144,times=  3
    

    configs.append(config(buyer=fcustom(csvama2,fast= 51,slow=700,rstart=500,rend=5000))) 	#balance=2427,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast= 57,slow=710,rstart=4500,rend=7500))) 	#balance=2042,times=  6
    
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=700,rstart=2000,rend=5000))) 	#balance=2795,times=  3
    
    configs.append(config(buyer=fcustom(csvama2,fast= 24,slow=740,rstart=2000,rend=6000))) 	#balance=5519,times=  3

    configs.append(config(buyer=fcustom(csvama2,fast=685,slow=720,rstart=2000,rend=8000))) 	#balance=3127,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast= 26,slow=740,rstart=1000,rend=7500))) 	#balance=2355,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=164,slow=710,rstart=3000,rend=5500))) 	#balance=3157,times=  3
    configs.append(config(buyer=fcustom(csvama2,fast=172,slow=760,rstart=2000,rend=4000))) 	#balance=4907,times=  1

    configs.append(config(buyer=fcustom(csvama2,fast= 66,slow=720,rstart=2000,rend=8000))) 	#balance=2903,times=  8
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=720,rstart=3500,rend=6000))) 	#balance=3760,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 57,slow=720,rstart=2000,rend=4500))) 	#balance=5667,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=720,rstart=3500,rend=7500))) 	#balance=2278,times=  5

    configs.append(config(buyer=fcustom(csvama2,fast=  3,slow=480,rstart=3500,rend=5000))) 	#balance=1031,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=104,slow=480,rstart=500,rend=5500))) 	#balance=2138,times= 11

    configs.append(config(buyer=fcustom(csvama2,fast= 32,slow=480,rstart=5000,rend=6500))) 	#balance=1648,times= 16
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=480,rstart=5000,rend=6000))) 	#balance=10991,times=  6

    return configs

def prepare_temp_configs(seller,pman=None,dman=None):
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []

    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid= 13,slow=290,rstart=2000,rend=8000))) 	#balance=1012,times= 23
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 29,slow=390,rstart=4500,rend=8000))) 	#balance=1062,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid= 18,slow=245,rstart=2000,rend=7500))) 	#balance=1097,times= 21
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 21,slow=245,rstart=3000,rend=8000))) 	#balance=1180,times= 23
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 21,slow=385,rstart=1500,rend=8000))) 	#balance=1190,times= 18
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 19,slow=270,rstart=2000,rend=8000))) 	#balance=1301,times= 24
    configs.append(config(buyer=fcustom(csvama3,fast=  3,mid= 31,slow= 95,rstart=8000,rend=9500))) 	#balance=1358,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 27,slow=270,rstart=7500,rend=8000))) 	#balance=1544,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 21,slow=270,rstart=7500,rend=8000))) 	#balance=1873,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 27,slow=330,rstart=3000,rend=6000))) 	#balance=2437,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 23,slow=270,rstart=7500,rend=8000))) 	#balance=3445,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  9,mid= 93,slow=395,rstart=2500,rend=7500))) 	#balance=6045,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 33,mid= 83,slow=280,rstart=  0,rend=6000))) 	#balance=12607,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 11,mid= 74,slow=210,rstart=3000,rend=5500))) 	#balance=12926,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 85,slow=165,rstart=5000,rend=5500))) 	#balance=16531,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 18,mid= 66,slow= 20,rstart=3500,rend=5500))) 	#balance=16531,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid= 59,slow=350,rstart=3000,rend=6000))) 	#balance=3291000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 27,slow=350,rstart=4500,rend=6000))) 	#balance=5850000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 43,mid= 67,slow=435,rstart=500,rend=3500))) 	#balance=10923000,times=  1    
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid= 13,slow=290,rstart=2000,rend=8000))) 	#balance=1012,times= 23
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 29,slow=390,rstart=4500,rend=8000))) 	#balance=1062,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid= 18,slow=245,rstart=2000,rend=7500))) 	#balance=1097,times= 21
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 21,slow=245,rstart=3000,rend=8000))) 	#balance=1180,times= 23
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 21,slow=385,rstart=1500,rend=8000))) 	#balance=1190,times= 18
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 19,slow=270,rstart=2000,rend=8000))) 	#balance=1301,times= 24
    configs.append(config(buyer=fcustom(csvama3,fast=  3,mid= 31,slow= 95,rstart=8000,rend=9500))) 	#balance=1358,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 27,slow=270,rstart=7500,rend=8000))) 	#balance=1544,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 23,slow=245,rstart=7000,rend=8000))) 	#balance=1937,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 27,slow=330,rstart=3000,rend=6000))) 	#balance=2437,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 23,slow=270,rstart=7500,rend=8000))) 	#balance=3445,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  9,mid= 93,slow=395,rstart=2500,rend=7500))) 	#balance=6045,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 33,mid= 83,slow=280,rstart=  0,rend=6000))) 	#balance=12607,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 11,mid= 74,slow=210,rstart=3000,rend=5500))) 	#balance=12926,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 85,slow=165,rstart=5000,rend=5500))) 	#balance=16531,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 18,mid= 66,slow= 20,rstart=3500,rend=5500))) 	#balance=16531,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 27,slow=350,rstart=4500,rend=6000))) 	#balance=5850000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 43,mid= 67,slow=435,rstart=500,rend=3500))) 	#balance=10923000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid= 28,slow= 65,rstart=4500,rend=6000))) 	#balance=1041,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 30,mid= 93,slow=410,rstart=1500,rend=6000))) 	#balance=2832,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 76,slow=410,rstart=3500,rend=8500))) 	#balance=8861,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 27,mid= 42,slow=195,rstart=3500,rend=9500))) 	#balance=1040,times= 15
    configs.append(config(buyer=fcustom(csvama3,fast= 33,mid=  5,slow= 40,rstart=2000,rend=4500))) 	#balance=1047,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid= 30,slow= 70,rstart=4000,rend=8500))) 	#balance=1112,times= 16
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid= 39,slow=325,rstart=4500,rend=8500))) 	#balance=1241,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=  5,slow= 25,rstart=4500,rend=5500))) 	#balance=1266,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 28,mid= 43,slow=205,rstart=2000,rend=8500))) 	#balance=1349,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast= 19,mid= 42,slow=195,rstart=3500,rend=6500))) 	#balance=1663,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid= 30,slow= 50,rstart=4000,rend=5500))) 	#balance=1704,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 33,mid=  8,slow= 30,rstart=2000,rend=5500))) 	#balance=1770,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 52,slow=170,rstart=500,rend=9000))) 	#balance=1791,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 33,mid=  9,slow= 40,rstart=2500,rend=4500))) 	#balance=1805,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 15,mid= 11,slow= 65,rstart=1500,rend=8500))) 	#balance=2351,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid=  4,slow=355,rstart=  0,rend=4000))) 	#balance=2952,times=  2
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
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid= 45,slow=185,rstart=1000,rend=9000))) 	#balance=1046,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast= 11,mid= 24,slow=405,rstart=  0,rend=8000))) 	#balance=1087,times= 15
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 50,slow=245,rstart=500,rend=9500))) 	#balance=1106,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid= 48,slow=165,rstart=500,rend=10000))) 	#balance=1222,times= 18
    configs.append(config(buyer=fcustom(csvama3,fast= 21,mid= 50,slow= 90,rstart=1500,rend=10000))) 	#balance=1234,times= 30
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 25,slow=410,rstart=5500,rend=9000))) 	#balance=1278,times= 15
    configs.append(config(buyer=fcustom(csvama3,fast= 38,mid= 49,slow=190,rstart=1000,rend=9500))) 	#balance=1279,times= 25
    configs.append(config(buyer=fcustom(csvama3,fast= 38,mid= 50,slow=185,rstart=1500,rend=10000))) 	#balance=1298,times= 30
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 81,slow=430,rstart=2500,rend=9000))) 	#balance=1391,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast= 48,mid= 49,slow=190,rstart=1500,rend=9500))) 	#balance=1392,times= 15
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid= 17,slow=410,rstart=1500,rend=8000))) 	#balance=1424,times= 15
    configs.append(config(buyer=fcustom(csvama3,fast= 15,mid= 17,slow=420,rstart=5500,rend=7500))) 	#balance=1463,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast= 19,mid= 48,slow=170,rstart=  0,rend=10000))) 	#balance=1493,times= 17
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 83,slow=420,rstart=5500,rend=8000))) 	#balance=1538,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 11,mid= 80,slow=410,rstart=1500,rend=9000))) 	#balance=1582,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast= 11,mid= 78,slow=405,rstart=3000,rend=9000))) 	#balance=1621,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid= 27,slow=405,rstart=6000,rend=8000))) 	#balance=1685,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 82,slow=405,rstart=5500,rend=10000))) 	#balance=1685,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 46,mid= 53,slow=190,rstart=5000,rend=10000))) 	#balance=1782,times= 21
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 27,slow=405,rstart=6000,rend=9000))) 	#balance=1884,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid= 49,slow=190,rstart=1000,rend=10000))) 	#balance=1913,times= 14
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid= 24,slow=405,rstart=5500,rend=8000))) 	#balance=1962,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 48,mid= 51,slow=200,rstart=1500,rend=9500))) 	#balance=2142,times= 19
    configs.append(config(buyer=fcustom(csvama3,fast= 48,mid= 51,slow=200,rstart=1000,rend=9500))) 	#balance=2142,times= 19
    configs.append(config(buyer=fcustom(csvama3,fast= 32,mid= 51,slow=200,rstart=1500,rend=10000))) 	#balance=2155,times= 15
    configs.append(config(buyer=fcustom(csvama3,fast= 47,mid= 51,slow=200,rstart=6500,rend=9500))) 	#balance=2361,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast= 15,mid= 81,slow=380,rstart=1000,rend=5500))) 	#balance=2456,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid= 25,slow=410,rstart=5500,rend=8000))) 	#balance=2706,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 40,mid= 51,slow=200,rstart=7500,rend=9500))) 	#balance=2794,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid= 83,slow=420,rstart=5500,rend=7500))) 	#balance=3697,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 45,mid= 88,slow=295,rstart=5500,rend=7000))) 	#balance=4876,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 93,slow=350,rstart=2000,rend=7000))) 	#balance=10444,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 11,mid= 82,slow=410,rstart=5500,rend=6000))) 	#balance=22734,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 36,slow=425,rstart=6500,rend=8000))) 	#balance=6684000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=215,mid=430,slow=485,rstart=4500,rend=10000))) 	#balance=1000,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=215,mid=400,slow=1810,rstart=6500,rend=9500))) 	#balance=1013,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=215,slow=790,rstart=2500,rend=9000))) 	#balance=1013,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=240,mid=305,slow=510,rstart=3500,rend=10000))) 	#balance=1019,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid=375,slow=820,rstart=3000,rend=10000))) 	#balance=1028,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=705,slow=790,rstart=2500,rend=8500))) 	#balance=1047,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 42,slow=950,rstart=  0,rend=9500))) 	#balance=1047,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 26,mid=215,slow=1030,rstart=6500,rend=9000))) 	#balance=1050,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=100,mid=225,slow=790,rstart=  0,rend=9000))) 	#balance=1050,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=480,mid=505,slow=530,rstart=4500,rend=9500))) 	#balance=1066,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid= 84,slow=1030,rstart=2500,rend=10000))) 	#balance=1089,times= 18
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid= 84,slow=1030,rstart=  0,rend=10000))) 	#balance=1089,times= 18
    configs.append(config(buyer=fcustom(csvama3,fast=200,mid=225,slow=1030,rstart=  0,rend=9000))) 	#balance=1091,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 26,mid=215,slow=1030,rstart=7500,rend=9000))) 	#balance=1091,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid=215,slow=1030,rstart=7500,rend=9000))) 	#balance=1104,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=295,slow=950,rstart=8500,rend=9500))) 	#balance=1104,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=210,mid=300,slow=530,rstart=4500,rend=9500))) 	#balance=1116,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=210,mid=300,slow=530,rstart=5000,rend=9500))) 	#balance=1116,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=200,mid=385,slow=710,rstart=4500,rend=9500))) 	#balance=1143,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=265,slow=1030,rstart=  0,rend=9500))) 	#balance=1156,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=265,slow=1030,rstart=  0,rend=9500))) 	#balance=1156,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=215,slow=1050,rstart=2500,rend=9000))) 	#balance=1175,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 88,slow=950,rstart=9000,rend=9500))) 	#balance=1187,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid= 88,slow=950,rstart=2500,rend=10000))) 	#balance=1191,times= 21
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=295,slow=1030,rstart=6500,rend=9000))) 	#balance=1192,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=295,slow=1030,rstart=5500,rend=9000))) 	#balance=1192,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=295,slow=1030,rstart=7500,rend=9000))) 	#balance=1192,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=295,slow=1030,rstart=6000,rend=9000))) 	#balance=1192,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid=385,slow=950,rstart=500,rend=8500))) 	#balance=1194,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 42,mid=270,slow=1020,rstart=1500,rend=5500))) 	#balance=1249,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=116,slow=1030,rstart=  0,rend=9500))) 	#balance=1265,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast=230,mid=420,slow=720,rstart=3500,rend=10000))) 	#balance=1270,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=345,slow=1030,rstart=8000,rend=9000))) 	#balance=1286,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=350,slow=950,rstart=8500,rend=9500))) 	#balance=1286,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=140,mid=430,slow=790,rstart=500,rend=9500))) 	#balance=1291,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=295,slow=950,rstart=8500,rend=9500))) 	#balance=1305,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid=215,slow=1030,rstart=6500,rend=9000))) 	#balance=1319,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=200,mid=305,slow=950,rstart=  0,rend=9500))) 	#balance=1364,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=200,mid=305,slow=950,rstart=2500,rend=9500))) 	#balance=1364,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=180,slow=1350,rstart=2500,rend=9500))) 	#balance=1390,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=180,slow=1350,rstart=2500,rend=9000))) 	#balance=1390,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=188,slow=1350,rstart=  0,rend=9000))) 	#balance=1390,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=375,slow=1030,rstart=  0,rend=9500))) 	#balance=1402,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=108,mid=192,slow=850,rstart=500,rend=9500))) 	#balance=1434,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid=215,slow=1030,rstart=  0,rend=9000))) 	#balance=1476,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=188,slow=1030,rstart=8000,rend=8500))) 	#balance=1493,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid= 92,slow=950,rstart=500,rend=8500))) 	#balance=1493,times= 17
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=188,slow=1030,rstart=8000,rend=8500))) 	#balance=1493,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=295,slow=1030,rstart=2500,rend=9000))) 	#balance=1499,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=295,slow=1030,rstart=  0,rend=9000))) 	#balance=1499,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=345,slow=790,rstart=8000,rend=9500))) 	#balance=1502,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=345,slow=800,rstart=  0,rend=9500))) 	#balance=1512,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=215,mid=335,slow=485,rstart=4500,rend=9500))) 	#balance=1598,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid=215,slow=1030,rstart=5500,rend=9000))) 	#balance=1610,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=210,mid=415,slow=710,rstart=  0,rend=9500))) 	#balance=1632,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=220,mid=350,slow=830,rstart=1000,rend=6500))) 	#balance=1634,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=345,slow=1030,rstart=8000,rend=9500))) 	#balance=1648,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=215,slow=1030,rstart=500,rend=9000))) 	#balance=1721,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=240,mid=305,slow=485,rstart=3000,rend=9500))) 	#balance=1729,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=220,mid=340,slow=540,rstart=  0,rend=9500))) 	#balance=1729,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=240,mid=305,slow=485,rstart=3500,rend=9500))) 	#balance=1729,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid= 84,slow=1350,rstart=1500,rend=10000))) 	#balance=1737,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid= 84,slow=1350,rstart=2500,rend=9000))) 	#balance=1737,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid=215,slow=1030,rstart=  0,rend=9000))) 	#balance=1752,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid=215,slow=1030,rstart=2500,rend=9000))) 	#balance=1752,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=144,mid=415,slow=700,rstart=4000,rend=9500))) 	#balance=1820,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=200,mid=415,slow=710,rstart=  0,rend=9500))) 	#balance=1824,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=300,slow=950,rstart=500,rend=8500))) 	#balance=1824,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=200,mid=415,slow=710,rstart=  0,rend=8500))) 	#balance=1824,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 78,mid=430,slow=850,rstart=500,rend=9500))) 	#balance=1845,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=460,slow=790,rstart=1000,rend=9500))) 	#balance=1869,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=265,slow=1030,rstart=  0,rend=8500))) 	#balance=1878,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid= 84,slow=1350,rstart=  0,rend=8500))) 	#balance=1885,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  9,mid=495,slow=1350,rstart=  0,rend=9500))) 	#balance=1936,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=100,mid=215,slow=1030,rstart=  0,rend=9000))) 	#balance=1953,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=270,mid=280,slow=520,rstart=3500,rend=10000))) 	#balance=1988,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=245,mid=295,slow=1350,rstart=2500,rend=9000))) 	#balance=1992,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=144,mid=184,slow=860,rstart=  0,rend=9500))) 	#balance=2039,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast=215,mid=375,slow=485,rstart=2500,rend=9000))) 	#balance=2048,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=215,slow=1040,rstart=5500,rend=9000))) 	#balance=2166,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=215,slow=1030,rstart=5500,rend=9000))) 	#balance=2196,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=215,slow=1030,rstart=2500,rend=9000))) 	#balance=2285,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=205,mid=215,slow=1030,rstart=2500,rend=9000))) 	#balance=2507,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=215,slow=1030,rstart=7500,rend=9000))) 	#balance=2588,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=215,mid=415,slow=710,rstart=4500,rend=9500))) 	#balance=2614,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=215,slow=1030,rstart=  0,rend=9500))) 	#balance=2782,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=128,mid=705,slow=790,rstart=2500,rend=9500))) 	#balance=3132,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=215,slow=1030,rstart=5500,rend=10000))) 	#balance=3263,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast=205,mid=415,slow=710,rstart=6500,rend=9500))) 	#balance=3414,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=108,mid=116,slow=1350,rstart=4500,rend=9500))) 	#balance=3419,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=215,mid=430,slow=485,rstart=2500,rend=9000))) 	#balance=4026,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=345,slow=1030,rstart=  0,rend=9500))) 	#balance=4420,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=215,slow=1030,rstart=  0,rend=8500))) 	#balance=4631,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=465,slow=485,rstart=  0,rend=9500))) 	#balance=4670,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=188,slow=1350,rstart=2000,rend=8500))) 	#balance=4906,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid=148,slow=490,rstart=1500,rend=5500))) 	#balance=5302,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=220,slow=1030,rstart=  0,rend=9000))) 	#balance=5865,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=215,slow=1030,rstart=5500,rend=9000))) 	#balance=10790,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=215,slow=1030,rstart=6500,rend=9000))) 	#balance=10790,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid=495,slow=860,rstart=5000,rend=6500))) 	#balance=18561,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=200,mid=400,slow=500,rstart=4500,rend=9000))) 	#balance=72677,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 33,mid= 96,slow=1240,rstart=4500,rend=6000))) 	#balance=3872000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 88,mid=400,slow=1800,rstart=7500,rend=10000))) 	#balance=4082500,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=335,slow=630,rstart=4000,rend=8500))) 	#balance=1000,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 39,mid= 45,slow=1910,rstart=4000,rend=9000))) 	#balance=1001,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 45,slow=640,rstart=4000,rend=9000))) 	#balance=1010,times= 20
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 45,slow=630,rstart=4000,rend=9000))) 	#balance=1010,times= 19
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 92,slow=1060,rstart=2000,rend=10000))) 	#balance=1011,times= 21
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 92,slow=1060,rstart=1500,rend=10000))) 	#balance=1011,times= 21
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 75,slow=720,rstart=4500,rend=5000))) 	#balance=1018,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=196,slow=495,rstart=5000,rend=10000))) 	#balance=1040,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=196,slow=495,rstart=6000,rend=10000))) 	#balance=1040,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 92,slow=980,rstart=2000,rend=10000))) 	#balance=1044,times= 13
    configs.append(config(buyer=fcustom(csvama3,fast=116,mid=485,slow=940,rstart=3500,rend=9500))) 	#balance=1045,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid=305,slow=740,rstart=4000,rend=10000))) 	#balance=1055,times= 13
    configs.append(config(buyer=fcustom(csvama3,fast=120,mid=280,slow=660,rstart=1500,rend=9500))) 	#balance=1059,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid= 48,slow=520,rstart=4000,rend=8500))) 	#balance=1063,times= 21
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=340,slow=720,rstart=4500,rend=10000))) 	#balance=1064,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=148,mid=325,slow=1380,rstart=4000,rend=8500))) 	#balance=1091,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=320,slow=1380,rstart=7000,rend=9000))) 	#balance=1091,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=260,slow=630,rstart=1500,rend=9500))) 	#balance=1093,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 18,mid= 72,slow=175,rstart=1500,rend=10000))) 	#balance=1109,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid= 78,slow=490,rstart=1500,rend=8500))) 	#balance=1110,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast= 30,mid= 92,slow=980,rstart=2000,rend=10000))) 	#balance=1124,times= 20
    configs.append(config(buyer=fcustom(csvama3,fast= 18,mid=235,slow=650,rstart=7000,rend=10000))) 	#balance=1129,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 48,slow=710,rstart=4000,rend=8500))) 	#balance=1139,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid= 48,slow=760,rstart=1500,rend=8500))) 	#balance=1151,times= 27
    configs.append(config(buyer=fcustom(csvama3,fast=150,mid=400,slow=1230,rstart=3000,rend=9000))) 	#balance=1182,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=315,slow=650,rstart=4500,rend=9500))) 	#balance=1208,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=150,mid=235,slow=495,rstart=2500,rend=10000))) 	#balance=1242,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid=172,slow=490,rstart=4000,rend=8500))) 	#balance=1250,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=340,slow=650,rstart=7000,rend=10000))) 	#balance=1250,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=200,slow=415,rstart=1500,rend=9000))) 	#balance=1256,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid= 54,slow=630,rstart=7000,rend=8500))) 	#balance=1261,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 48,slow=490,rstart=4500,rend=8500))) 	#balance=1263,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast=128,mid=196,slow=1020,rstart=7000,rend=10000))) 	#balance=1273,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 63,slow=730,rstart=5000,rend=10000))) 	#balance=1283,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=315,slow=650,rstart=7000,rend=10000))) 	#balance=1286,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid=335,slow=630,rstart=7000,rend=10000))) 	#balance=1286,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid=320,slow=580,rstart=4000,rend=9000))) 	#balance=1286,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=335,slow=630,rstart=7000,rend=10000))) 	#balance=1286,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=315,slow=730,rstart=7000,rend=10000))) 	#balance=1286,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=172,slow=495,rstart=4000,rend=10000))) 	#balance=1292,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid= 57,slow=730,rstart=7000,rend=10000))) 	#balance=1315,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid=320,slow=660,rstart=4000,rend=10000))) 	#balance=1325,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 48,slow=1440,rstart=4000,rend=8500))) 	#balance=1346,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=150,mid=260,slow=710,rstart=2000,rend=9000))) 	#balance=1349,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=128,mid=520,slow=800,rstart=4000,rend=10000))) 	#balance=1365,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=124,mid=335,slow=650,rstart=7000,rend=10000))) 	#balance=1373,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=375,mid=655,slow=770,rstart=2000,rend=10000))) 	#balance=1384,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid= 54,slow=1770,rstart=5000,rend=8500))) 	#balance=1388,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 26,slow=100,rstart=4000,rend=8500))) 	#balance=1390,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast=148,mid=525,slow=800,rstart=4000,rend=8500))) 	#balance=1398,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=150,mid=335,slow=630,rstart=4000,rend=9500))) 	#balance=1399,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=485,slow=740,rstart=4000,rend=8500))) 	#balance=1401,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=325,slow=640,rstart=4000,rend=8500))) 	#balance=1410,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid=325,slow=640,rstart=4500,rend=8500))) 	#balance=1410,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=335,slow=650,rstart=7000,rend=10000))) 	#balance=1435,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=150,mid=555,slow=730,rstart=4500,rend=9500))) 	#balance=1448,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 78,slow=1020,rstart=1500,rend=8500))) 	#balance=1462,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid= 72,slow= 95,rstart=4500,rend=9000))) 	#balance=1504,times= 13
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=335,slow=650,rstart=7000,rend=10000))) 	#balance=1510,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 26,mid= 42,slow=730,rstart=5000,rend=9000))) 	#balance=1522,times= 14
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 45,slow= 95,rstart=1500,rend=9000))) 	#balance=1523,times= 19
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 75,slow= 95,rstart=1500,rend=9000))) 	#balance=1531,times= 17
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid= 22,slow=495,rstart=7000,rend=9000))) 	#balance=1554,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 33,slow=630,rstart=4000,rend=8500))) 	#balance=1561,times= 20
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid=196,slow=980,rstart=7000,rend=8500))) 	#balance=1564,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=325,slow=520,rstart=4000,rend=8500))) 	#balance=1576,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=400,mid=460,slow=890,rstart=2000,rend=8000))) 	#balance=1577,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 26,mid=315,slow=650,rstart=7000,rend=10000))) 	#balance=1608,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid= 78,slow=500,rstart=4000,rend=8500))) 	#balance=1634,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 48,slow=720,rstart=4500,rend=8500))) 	#balance=1689,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=172,slow=495,rstart=7000,rend=10000))) 	#balance=1702,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  3,mid=172,slow=485,rstart=6000,rend=10000))) 	#balance=1702,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 48,slow=740,rstart=1500,rend=8500))) 	#balance=1713,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast= 18,mid= 72,slow=175,rstart=7000,rend=10000))) 	#balance=1737,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=164,slow=495,rstart=7000,rend=8500))) 	#balance=1801,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid=655,slow=1230,rstart=3500,rend=9000))) 	#balance=1925,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=340,slow=1020,rstart=4000,rend=10000))) 	#balance=2023,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 48,slow=740,rstart=4000,rend=8500))) 	#balance=2034,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast=195,mid=335,slow=1350,rstart=7000,rend=10000))) 	#balance=2087,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=340,slow=650,rstart=7000,rend=10000))) 	#balance=2089,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=148,mid=205,slow=800,rstart=1500,rend=8500))) 	#balance=2095,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=148,mid=196,slow=760,rstart=1500,rend=8500))) 	#balance=2159,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=395,slow=980,rstart=7000,rend=8000))) 	#balance=2207,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 26,mid= 72,slow= 95,rstart=4500,rend=10000))) 	#balance=2252,times= 13
    configs.append(config(buyer=fcustom(csvama3,fast=200,mid=435,slow=520,rstart=3500,rend=6000))) 	#balance=2356,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=335,slow=630,rstart=7000,rend=10000))) 	#balance=2446,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=340,slow=630,rstart=4000,rend=8500))) 	#balance=2447,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=255,slow=730,rstart=5000,rend=10000))) 	#balance=2508,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=335,slow=630,rstart=4000,rend=9000))) 	#balance=2601,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=335,slow=630,rstart=5000,rend=10000))) 	#balance=2601,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=340,slow=630,rstart=4000,rend=9500))) 	#balance=2870,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=340,slow=630,rstart=4000,rend=9000))) 	#balance=2870,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=345,slow=630,rstart=7000,rend=10000))) 	#balance=2929,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=340,slow=660,rstart=4000,rend=9500))) 	#balance=2968,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=340,slow=630,rstart=7000,rend=9000))) 	#balance=2998,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=340,slow=630,rstart=7000,rend=10000))) 	#balance=2998,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 28,mid=360,slow=660,rstart=500,rend=8500))) 	#balance=3122,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 57,slow=1270,rstart=4000,rend=8500))) 	#balance=3217,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 48,slow=720,rstart=4500,rend=8500))) 	#balance=3352,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast= 33,mid=160,slow=350,rstart=1500,rend=5500))) 	#balance=3365,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=335,slow=630,rstart=7000,rend=10000))) 	#balance=3526,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=335,slow=630,rstart=7000,rend=9000))) 	#balance=3526,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 57,slow=730,rstart=4000,rend=9000))) 	#balance=3560,times= 12
    configs.append(config(buyer=fcustom(csvama3,fast=144,mid=240,slow=730,rstart=6000,rend=9000))) 	#balance=4162,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid= 45,slow=740,rstart=4000,rend=9000))) 	#balance=4208,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=172,slow=630,rstart=7000,rend=10000))) 	#balance=4355,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=108,mid=176,slow=500,rstart=500,rend=7000))) 	#balance=4573,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=155,mid=330,slow=540,rstart=3000,rend=9000))) 	#balance=4824,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid=340,slow=660,rstart=4000,rend=10000))) 	#balance=4837,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=120,mid=340,slow=700,rstart=500,rend=9000))) 	#balance=4845,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 80,mid=240,slow=740,rstart=6000,rend=10000))) 	#balance=5274,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=370,mid=660,slow=750,rstart=2000,rend=9000))) 	#balance=5300,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 18,mid=335,slow=650,rstart=7000,rend=10000))) 	#balance=8031,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=205,slow=485,rstart=4000,rend=9500))) 	#balance=9534,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=340,slow=650,rstart=7000,rend=10000))) 	#balance=12220,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 54,mid=750,slow=1230,rstart=500,rend=5500))) 	#balance=15132,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 42,mid= 78,slow=970,rstart=1500,rend=4500))) 	#balance=21750,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=172,slow=630,rstart=6000,rend=8500))) 	#balance=201151,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=190,mid=196,slow=1910,rstart=4000,rend=10000))) 	#balance=3325000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=120,mid=340,slow=660,rstart=1500,rend=9500))) 	#balance=7492000,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=655,slow=770,rstart=4000,rend=8500))) 	#balance=8748000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=172,slow=630,rstart=7000,rend=8500))) 	#balance=8748000,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=196,slow=495,rstart=4500,rend=9000))) 	#balance=11953000,times=  5


    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=250,slow=1180,rstart=7500,rend=9000))) 	#balance=1733,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=172,slow=1140,rstart=7000,rend=9500))) 	#balance=2309,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=220,slow=1130,rstart=4000,rend=9000))) 	#balance=2908,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=225,slow=1110,rstart=8000,rend=9500))) 	#balance=1006,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid= 84,slow=1140,rstart=2500,rend=9000))) 	#balance=1006,times=  8
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid= 84,slow=1120,rstart=  0,rend=9000))) 	#balance=1067,times=  9
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid= 84,slow=1110,rstart=  0,rend=8500))) 	#balance=1094,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=188,slow=1180,rstart=  0,rend=9500))) 	#balance=1116,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 24,mid=225,slow=1110,rstart=2500,rend=9500))) 	#balance=1146,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 26,mid=215,slow=1110,rstart=2500,rend=9000))) 	#balance=1209,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=100,mid=188,slow=1190,rstart=500,rend=10000))) 	#balance=1249,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 92,slow=1110,rstart=  0,rend=8500))) 	#balance=1270,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=120,mid=188,slow=1110,rstart=500,rend=10000))) 	#balance=1455,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=100,mid=148,slow=1110,rstart=  0,rend=9000))) 	#balance=1472,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=225,slow=1110,rstart=8000,rend=9000))) 	#balance=1522,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=120,mid=184,slow=1120,rstart=1500,rend=10000))) 	#balance=1568,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 26,mid=200,slow=1120,rstart=1500,rend=9000))) 	#balance=1594,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 42,slow=1110,rstart=2500,rend=9500))) 	#balance=1594,times= 16
    configs.append(config(buyer=fcustom(csvama3,fast=128,mid=192,slow=1110,rstart=1000,rend=9500))) 	#balance=1890,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=505,slow=1110,rstart=8000,rend=9500))) 	#balance=2112,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=128,mid=300,slow=1110,rstart=1000,rend=9000))) 	#balance=2457,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid= 92,slow=1190,rstart=2500,rend=8500))) 	#balance=2498,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=128,mid=188,slow=1120,rstart=  0,rend=10000))) 	#balance=2598,times=  6
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 92,slow=1120,rstart=2500,rend=9000))) 	#balance=3282,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=480,mid=700,slow=1170,rstart=5000,rend=9000))) 	#balance=3340,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 92,slow=1110,rstart=8000,rend=9500))) 	#balance=3709,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=108,mid=192,slow=1130,rstart=500,rend=9500))) 	#balance=6104,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=765,slow=1110,rstart=500,rend=7000))) 	#balance=13171,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=188,slow=1110,rstart=8000,rend=9500))) 	#balance=20523,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=156,slow=1110,rstart=  0,rend=9500))) 	#balance=35175,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=705,slow=1110,rstart=  0,rend=8500))) 	#balance=9550000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=172,slow=1130,rstart=4000,rend=10000))) 	#balance=1007,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid= 48,slow=1120,rstart=1500,rend=8500))) 	#balance=1215,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast= 39,mid= 48,slow=1160,rstart=4000,rend=8500))) 	#balance=1141,times= 13
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 48,slow=1140,rstart=4000,rend=8500))) 	#balance=1745,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 48,slow=1140,rstart=4000,rend=8500))) 	#balance=1786,times= 11
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid= 42,slow=1130,rstart=4500,rend=9500))) 	#balance=1788,times= 20
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 48,slow=1120,rstart=4500,rend=8500))) 	#balance=1513,times= 10
    configs.append(config(buyer=fcustom(csvama3,fast=140,mid=196,slow=1140,rstart=7500,rend=10000))) 	#balance=1657,times=  4
 
    configs.append(config(buyer=fcustom(csvama3,fast=120,mid=196,slow=1110,rstart=4000,rend=10000))) 	#balance=3037,times=  5
    configs.append(config(buyer=fcustom(csvama3,fast=128,mid=196,slow=1130,rstart=7000,rend=10000))) 	#balance=3075,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid=196,slow=1140,rstart=4000,rend=8500))) 	#balance=35175,times=  1

    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid=148,slow=1120,rstart=6500,rend=8500))) 	#balance=6684000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 96,mid=148,slow=1110,rstart=  0,rend=9000))) 	#balance=1038,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=148,slow=1110,rstart=500,rend=9000))) 	#balance=1420,times=  7
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid=148,slow=1110,rstart=4000,rend=8500))) 	#balance=3243,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast=124,mid=148,slow=1150,rstart=3500,rend=8000))) 	#balance=6957500,times=  2
 
    configs.append(config(buyer=fcustom(csvama3,fast=132,mid=200,slow=1140,rstart=1500,rend=9500))) 	#balance=1657,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=200,slow=1110,rstart=4000,rend=9000))) 	#balance=1339,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast=128,mid=200,slow=1130,rstart=4000,rend=10000))) 	#balance=1348,times=  5
    

    configs.append(config(buyer=fcustom(csvama3,fast= 44,mid= 23,slow=250,rstart=7500,rend=8000))) 	#balance=7664000,times=  1
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 27,slow=250,rstart=5000,rend=8000))) 	#balance=1899,times= 10

    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 23,slow=250,rstart=6500,rend=8000))) 	#balance=1577,times=  9

    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid= 21,slow=250,rstart=7500,rend=8000))) 	#balance=1156,times=  2
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid= 21,slow=250,rstart=7500,rend=8000))) 	#balance=3184,times=  3

    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid= 21,slow=250,rstart=7000,rend=8500))) 	#balance=1386,times=  9

    
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 21,slow=250,rstart=7500,rend=8000))) 	#balance=6826,times=  4
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid= 25,slow=250,rstart=7500,rend=8000))) 	#balance=3184,times=  3
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid= 25,slow=250,rstart=7500,rend=8000))) 	#balance=5492,times=  5
    
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
    #configs = prepare_temp_configs(seller)
    configs = prepare_temp_configs_0(seller)
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
    logging.basicConfig(filename="run_x4g.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    #测试时间段 [19980101,19990101-20010801],[20000101,20010701-20050901],[20040601,20050801-20071031],[20060601,20071031-20090101]
    #总时间段   [20000101,20010701,20090101]    #一个完整的周期+一个下降段
    #分段测试的要求，段mm > 1000-1500或抑制，总段mm > 2000
    
    begin,xbegin,end = 20000101,20010701,20090101
    #begin,xbegin,end = 19980101,20010701,20090101
    #begin,xbegin,end = 20000101,20010701,20050901
    #begin,xbegin,end = 19980101,19990701,20010801    
    #begin,xbegin,end = 20040601,20050801,20071031
    #begin,xbegin,end = 20060601,20071031,20090101
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

    run_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    #run_merge_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    #run_mm_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    #run_last(dates,sdata,idata,catalogs,begin,end,xbegin,lbegin)

    #近期工作 将svama2x/vama2x改造为syntony

    #prepare_order(sdata.values())
    #prepare_order(catalogs)
    #dummy_catalogs('catalog',catalogs)
    #for c in sdata[816].catalog:
    #    print c.name,c.g20
