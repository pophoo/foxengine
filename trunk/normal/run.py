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

    #csvama2
    configs.append(config(buyer=fcustom(csvama2,fast= 13,slow=125,rstart=3000,rend=9000))) 	#balance=1017,times= 47
    configs.append(config(buyer=fcustom(csvama2,fast=  4,slow=275,rstart=  0,rend=9000))) 	#balance=1037,times= 37
    configs.append(config(buyer=fcustom(csvama2,fast= 10,slow=305,rstart=  0,rend=9500))) 	#balance=1077,times= 37
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=275,rstart=1000,rend=10000))) 	#balance=1088,times= 42
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
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=250,rstart=  0,rend=6000))) 	#balance=9103,times=  7
    configs.append(config(buyer=fcustom(csvama2,fast=  2,slow=250,rstart=500,rend=4000))) 	#balance=9555,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=250,rstart=500,rend=4000))) 	#balance=13819,times=  5
    configs.append(config(buyer=fcustom(csvama2,fast=  2,slow=250,rstart=8000,rend=8500))) 	#balance=14376,times=  2
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=250,rstart=2500,rend=6000))) 	#balance=15664,times=  6
    configs.append(config(buyer=fcustom(csvama2,fast=  1,slow=250,rstart=2500,rend=4000))) 	#balance=28344,times=  4
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=250,rstart=2500,rend=4000))) 	#balance=57818,times=  4    

    #csvama3
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
    #configs.append(config(buyer=fcustom(cvama3,fast= 33,mid= 84,slow=345,ma_standard=500,extend_days= 27))) 	#balance=1126,times=100 #1025-81-334-245
    #configs.append(config(buyer=fcustom(csvama3,fast= 39,mid= 71,slow=490,ma_standard=120,extend_days=  1))) 	#balance=2262,times=  4    #4103-119-571-7
    #configs.append(config(buyer=fcustom(csvama2,fast= 20,slow=  5,ma_standard=500))) 	#balance=1411,times= 25 #1411-72-285-49 
    return configs

def prepare_configs_A(seller,pman,dman):    #R>=400,winrate>400 or R>=1000,winrate>333
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    
    #候选A winrate>=400且R>=600,times>5 or  R>500且winrate>500
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 83,slow= 20,ma_standard=500,extend_days=  5))) 	#balance=1129,times= 23 #1828-128-425-80 ##
    configs.append(config(buyer=fcustom(svama3,fast= 39,mid= 71,slow=490,ma_standard=120,extend_days=  1))) 	#balance=2262,times=  4    #4103-119-571-7
    configs.append(config(buyer=fcustom(svama3,fast= 39,mid= 71,slow=490,ma_standard=500,extend_days=  1))) 	#balance=4129,times=  3    #4421-168-600-5
    configs.append(config(buyer=fcustom(svama2x,fast=  6,slow=  5,base=240,ma_standard= 10))) 	#balance=6106,times=  5 #2886-153-666-9
    configs.append(config(buyer=fcustom(svama2x,fast= 47,slow=  5,base=168,ma_standard=500))) 	#balance=26391,times=  3 #701-80-400-5
    configs.append(config(buyer=fcustom(vama3,fast= 30,mid= 67,slow= 50,ma_standard=500,extend_days= 31))) 	#balance=1061,times= 80 #1183-84-396-174
    configs.append(config(buyer=fcustom(vama3,fast= 16,mid= 78,slow= 45,ma_standard=500,extend_days= 13))) 	#balance=1062,times= 50 #2424-177-391-161
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 62,slow= 45,ma_standard=500,extend_days=  1))) 	#balance=1096,times=  5 #853-76-470-17
    configs.append(config(buyer=fcustom(vama3,fast= 16,mid= 70,slow= 45,ma_standard=500,extend_days=  9))) 	#balance=1141,times= 63 #1814-127-413-162
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 71,slow= 55,ma_standard=500,extend_days= 25))) 	#balance=1197,times= 68 #1144-95-401-177
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 67,slow= 45,ma_standard=500,extend_days= 27))) 	#balance=1209,times=133 #1746-117-429-342 ##
    configs.append(config(buyer=fcustom(vama3,fast=  9,mid= 68,slow= 45,ma_standard=500,extend_days= 21))) 	#balance=1219,times=108 #1952-123-451-286 ##
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
    #候选A1 winrate>=400且R>=800,times<5
    configs.append(config(buyer=fcustom(svama3,fast= 23,mid= 79,slow= 10,ma_standard=120,extend_days=  1))) 	#balance=2488,times=  2#   #1000-277-1000-1
    configs.append(config(buyer=fcustom(svama2s,fast= 48,slow=500,ma_standard= 67,extend_days= 13))) 	#balance=1162,times=  2 #1843-59-500-2
    configs.append(config(buyer=fcustom(svama2s,fast= 26,slow=430,ma_standard= 67,extend_days=  5))) 	#balance=2503,times=  4 #1000-38-1000-3
    configs.append(config(buyer=fcustom(svama2x,fast= 11,slow=  5,base=198,ma_standard=500))) 	#balance=2672,times=  9 #1428-40-500-4
    configs.append(config(buyer=fcustom(svama2x,fast= 18,slow=  5,base=198,ma_standard= 10))) 	#balance=30309,times=  2 #1800-99-666-3
    configs.append(config(buyer=fcustom(svama2x,fast=  6,slow=  5,base=240,ma_standard=500))) 	#balance=218574,times=  3 #1000-148-1000-4
    configs.append(config(buyer=fcustom(svama2x,fast= 28,slow=  5,base=240,ma_standard= 10))) 	#balance=4312,times=  5 #2328-177-500-4
    configs.append(config(buyer=fcustom(svama2x,fast= 15,slow=  5,base=228,ma_standard=250))) 	#balance=30406,times=  5 #1000-131-1000-2

    return configs

def prepare_configs_B(seller,pman,dman):    #R>=500,winrate<400
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
#候选B R>800,或R>500且winrate>400
    configs.append(config(buyer=fcustom(vama3,fast= 29,mid= 78,slow= 65,ma_standard=500,extend_days= 29))) 	#balance=1213,times=105 #1368-104-346-277
    configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 81,slow= 65,ma_standard=500,extend_days= 29))) 	#balance=1222,times=103 #1280-96-346-274
    configs.append(config(buyer=fcustom(vama3,fast= 31,mid= 91,slow= 65,ma_standard=500,extend_days= 25))) 	#balance=1298,times= 69 #1098-78-367-207
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 59,slow= 50,ma_standard=500,extend_days= 27))) 	#balance=1246,times=240 #1246-91-361-517
    configs.append(config(buyer=fcustom(vama3,fast= 17,mid= 69,slow= 65,ma_standard=500,extend_days= 31))) 	#balance=1032,times=214 #1213-91-347-460
    configs.append(config(buyer=fcustom(vama3,fast= 11,mid=  8,slow= 65,ma_standard=500,extend_days= 27))) 	#balance=1047,times= 77 #768-63-365-123
    configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 72,slow= 45,ma_standard=500,extend_days= 25))) 	#balance=1322,times= 64 #1214-85-333-144
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 79,slow= 45,ma_standard=500,extend_days= 17))) 	#balance=1325,times= 29 #1000-69-311-93
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 69,slow= 45,ma_standard=500,extend_days= 23))) 	#balance=1347,times= 43 #1089-73-350-117
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 80,slow= 45,ma_standard=500,extend_days= 29))) 	#balance=1416,times= 23 #2343-157-289-83
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 91,slow= 50,ma_standard=500,extend_days= 27))) 	#balance=1234,times= 79 #1000-74-363-253
    configs.append(config(buyer=fcustom(vama3,fast=  4,mid= 78,slow= 60,ma_standard=500,extend_days= 27))) 	#balance=1114,times=139 #1131-86-345-400
    configs.append(config(buyer=fcustom(vama3,fast= 31,mid= 68,slow= 65,ma_standard=500,extend_days= 29))) 	#balance=1000,times=176 #1076-84-359-331
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 79,slow= 55,ma_standard=500,extend_days=  1))) 	#balance=3550000,times=  2 #7714-270-333-3
    configs.append(config(buyer=fcustom(vama3,fast=  8,mid= 78,slow= 45,ma_standard=500,extend_days= 29))) 	#balance=1068,times= 81 #2362-163-385-231
    configs.append(config(buyer=fcustom(vama3,fast= 17,mid= 56,slow= 45,ma_standard=500,extend_days= 13))) 	#balance=1093,times=133 #1432-96-361-249
    configs.append(config(buyer=fcustom(vama3,fast= 29,mid= 78,slow= 45,ma_standard=500,extend_days= 29))) 	#balance=1039,times= 34 #2095-153-303-99
    configs.append(config(buyer=fcustom(vama3,fast= 17,mid= 55,slow= 50,ma_standard=500,extend_days= 27))) 	#balance=1143,times=214 #939-62-352-400 
    configs.append(config(buyer=fcustom(vama3,fast= 18,mid= 91,slow= 50,ma_standard=500,extend_days= 27))) 	#balance=1053,times= 45 #1229-91-381-165
    configs.append(config(buyer=fcustom(svama3,fast= 17,mid= 95,slow=130,ma_standard= 10,extend_days=  1))) 	#balance=2366,times= 11    #962-76-333-15
    configs.append(config(buyer=fcustom(svama3,fast= 17,mid= 95,slow=130,ma_standard=120,extend_days=  1))) 	#balance=2641,times= 10    #1036-85-357-14
    configs.append(config(buyer=fcustom(svama2,fast= 20,slow=  5,ma_standard=500))) 	#balance=1411,times= 25 #1411-72-285-49
    configs.append(config(buyer=fcustom(svama2c,fast= 32,slow=  5,ma_standard= 22))) 	#balance=3295,times= 13 #1096-68-307-13
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 83,slow= 15,ma_standard=500,extend_days= 13))) 	#balance=1988,times= 16 #1588-108-304-69
    configs.append(config(buyer=fcustom(vama3,fast= 24,mid= 55,slow=105,ma_standard= 55,extend_days=  1))) 	#balance=1181,times= 11 #1157-88-312-16
    configs.append(config(buyer=fcustom(vama3,fast= 33,mid= 84,slow=345,ma_standard=500,extend_days= 27))) 	#balance=1126,times=100 #1025-81-334-245
    configs.append(config(buyer=fcustom(vama3,fast=  1,mid= 78,slow=365,ma_standard=500,extend_days= 29))) 	#balance=1014,times= 75 #1038-80-322-180
    configs.append(config(buyer=fcustom(vama3,fast=  4,mid= 88,slow=425,ma_standard=500,extend_days= 33))) 	#balance=1016,times= 67 #1215-107-327-165
    configs.append(config(buyer=fcustom(vama3,fast= 27,mid= 60,slow=335,ma_standard=500,extend_days= 17))) 	#balance=1016,times=107 #1102-86-328-222
    configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 68,slow=465,ma_standard=500,extend_days= 21))) 	#balance=1177,times= 67 #878-65-307-169
    configs.append(config(buyer=fcustom(vama3,fast= 16,mid= 78,slow=445,ma_standard=500,extend_days= 21))) 	#balance=1247,times= 43 #920-81-344-119
    configs.append(config(buyer=fcustom(vama3,fast= 33,mid= 72,slow=445,ma_standard=500,extend_days= 17))) 	#balance=1358,times= 64 #1263-96-284-165
    configs.append(config(buyer=fcustom(vama3,fast=  8,mid= 78,slow=445,ma_standard=500,extend_days= 21))) 	#balance=1437,times= 38 #965-84-309-113
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 78,slow=450,ma_standard=500,extend_days= 17))) 	#balance=1453,times= 52 #1000-77-318-138
    configs.append(config(buyer=fcustom(vama3,fast=  1,mid= 69,slow=465,ma_standard=500,extend_days= 31))) 	#balance=1532,times= 93 #810-64-308-211
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 78,slow=445,ma_standard=500,extend_days= 29))) 	#balance=1586,times= 46 #1036-86-289-152
    configs.append(config(buyer=fcustom(vama2,fast= 29,slow=  5,ma_standard=250))) 	#balance=1093,times= 27 #891-61-264-34
    configs.append(config(buyer=fcustom(vama2,fast= 35,slow= 20,ma_standard=500))) 	#balance=1412,times= 87 #1090-84-331-172
    configs.append(config(buyer=fcustom(vama2,fast= 35,slow= 15,ma_standard=500))) 	#balance=1426,times= 41 #847-61-307-78
    configs.append(config(buyer=fcustom(vama2x,fast= 25,slow=  5,base=214,ma_standard=120))) 	#balance=3795,times=  8 #806-50-200-5
    configs.append(config(buyer=fcustom(svama2x,fast= 31,slow= 10,base=170,ma_standard=120))) 	#balance=1400,times= 10 #253-16-428-7

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
    #configs.extend(prepare_configs_B(seller,pman,dman))
    batch(configs,sdata,dates,xbegin,cmediator=myMediator)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    

    save_configs('atr_ev_t.txt',configs,xbegin,end)

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

    #configs_a = prepare_configs_A(seller,pman,dman)
    #dtrades_a = batch_last(configs_a,sdata,dates,xbegin,cmediator=myMediator)
    #save_last('atr_last_a.txt',dtrades_a,xbegin,end,lbegin)


    #configs_b = prepare_configs_B(seller,pman,dman)
    #dtrades_b = batch_last(configs_b,sdata,dates,xbegin,cmediator=myMediator)
    #save_last('atr_last_b.txt',dtrades_b,xbegin,end,lbegin)

    configs_t = prepare_temp_configs(seller,pman,dman)
    dtrades_t = batch_last(configs_t,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_t.txt',dtrades_t,xbegin,end,lbegin)

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
    #begin,xbegin,end,lbegin = 20060101,20070901,20090327,20081101
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
