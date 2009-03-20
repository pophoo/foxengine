# -*- coding: utf-8 -*-

#完整的运行脚本
#采用NMediator,结果发现成功率显然小了(次日上涨的看来挺多，导致止损比预计上移),看来需要加大atr系数 ==>1200比较贴近之前的结果
#不过有个特点，大部分情形，选出交易数越多的方法，稳定性越好

from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *

import logging
logger = logging.getLogger('wolfox.fengine.normal.run')    


#1 缩小止损，止损和跟随建议为1600/2400
#2 信号出来后打到55/120均线附近


def prepare_temp_configs(seller,pman=None,dman=None):
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    configs.append(config(buyer=fcustom(svama3,fast=128,mid=300,slow=1790))) 	#782-54-394-38
    configs.append(config(buyer=fcustom(svama3,fast=116,mid=420,slow=1790))) 	#323-22-421-38
    configs.append(config(buyer=fcustom(svama3,fast= 10,mid=136,slow=365))) 	#43-3-289-107
    configs.append(config(buyer=fcustom(svama3,fast=185,mid=510,slow=1800))) 	#333-27-275-29
    configs.append(config(buyer=fcustom(svama3,fast=185,mid=510,slow=1790))) 	#360-27-290-31
    configs.append(config(buyer=fcustom(svama3,fast=112,mid=490,slow=860))) 	#521-36-265-94
    configs.append(config(buyer=fcustom(svama3,fast=165,mid=300,slow=1750))) 	#13-1-400-25
    configs.append(config(buyer=fcustom(svama3,fast= 18,mid=340,slow=1480))) 	#66-5-280-150
    configs.append(config(buyer=fcustom(svama3,fast= 18,mid=350,slow=1960))) 	#42-3-333-87
    configs.append(config(buyer=fcustom(svama3,fast=160,mid=270,slow=315))) 	#365-30-342-35
    configs.append(config(buyer=fcustom(svama3,fast= 69,mid=295,slow=1510))) 	#0-0-285-70
    configs.append(config(buyer=fcustom(svama3,fast=185,mid=192,slow=1980))) 	#0-0-384-26
    configs.append(config(buyer=fcustom(svama3,fast=116,mid=350,slow=2000))) 	#500-36-320-25
    configs.append(config(buyer=fcustom(svama3,fast=150,mid=350,slow=1990))) 	#289-20-409-22
    configs.append(config(buyer=fcustom(svama3,fast= 22,mid=350,slow=1990))) 	#461-30-386-75
    configs.append(config(buyer=fcustom(svama3,fast=160,mid=510,slow=1790))) 	#494-44-320-25
    configs.append(config(buyer=fcustom(svama3,fast=160,mid=184,slow=1950))) 	#370-30-472-36
    configs.append(config(buyer=fcustom(svama3,fast=160,mid=510,slow=1800))) 	#397-35-269-26
    configs.append(config(buyer=fcustom(svama3,fast=165,mid=184,slow=1950))) 	#316-25-461-39
    configs.append(config(buyer=fcustom(svama3,fast=  1,mid=300,slow=365))) 	#87-7-320-25
    configs.append(config(buyer=fcustom(svama3,fast=160,mid=280,slow=1790))) 	#344-21-421-38
    configs.append(config(buyer=fcustom(svama3,fast=180,mid=300,slow=1810))) 	#194-14-423-26
    configs.append(config(buyer=fcustom(svama3,fast=160,mid=300,slow=1800))) 	#41-3-333-33
    configs.append(config(buyer=fcustom(svama3,fast=160,mid=310,slow=1790))) 	#81-5-343-32
    configs.append(config(buyer=fcustom(svama3,fast=190,mid=350,slow=1790))) 	#473-36-470-17
    configs.append(config(buyer=fcustom(svama2,fast=288,slow=1820))) 	#472-34-308-146
    configs.append(config(buyer=fcustom(svama2,fast= 57,slow=1330))) 	#185-15-350-228
    configs.append(config(buyer=fcustom(svama2,fast=370,slow=1680))) 	#435-34-307-143
    configs.append(config(buyer=fcustom(svama2,fast=  2,slow=1180))) 	#234-19-419-174
    configs.append(config(buyer=fcustom(svama2,fast=365,slow=1670))) 	#734-58-333-144
    configs.append(config(buyer=fcustom(svama2,fast= 14,slow=1210))) 	#493-40-384-226
    configs.append(config(buyer=fcustom(svama2,fast=  7,slow=1170))) 	#506-39-394-233
    configs.append(config(buyer=fcustom(svama2,fast=420,slow=1670))) 	#333-26-333-141
    configs.append(config(buyer=fcustom(svama2,fast=  9,slow=1210))) 	#450-36-371-210
    configs.append(config(buyer=fcustom(svama2,fast= 12,slow=1260))) 	#178-15-391-199
    configs.append(config(buyer=fcustom(svama1,fast= 10,slow=1260))) 	#225-18-380-189
    configs.append(config(buyer=fcustom(svama2,fast=  5,slow=1210))) 	#25-2-338-189
    configs.append(config(buyer=fcustom(svama2,fast=  4,slow=1130))) 	#337-26-427-222
    configs.append(config(buyer=fcustom(svama2,fast= 14,slow=1220))) 	#525-42-378-214
    configs.append(config(buyer=fcustom(svama2,fast= 14,slow=1230))) 	#470-40-390-210
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid= 13,slow=290,rstart=2000,rend=8000))) 	#476-31-36-49
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid= 18,slow=245,rstart=2000,rend=7500))) 	#231-19-309-42
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 21,slow=245,rstart=3000,rend=8000))) 	#0-0-268-41
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 21,slow=385,rstart=1500,rend=8000))) 	#12-1-324-37
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 19,slow=270,rstart=2000,rend=8000))) 	#271-19-358-39
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid= 13,slow=290,rstart=2000,rend=8000))) 	#471-31-306-49
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid= 30,slow= 70,rstart=4000,rend=8500))) 	#205-14-470-34
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid=  4,slow=355,rstart=  0,rend=4000))) 	#1000-15-1000-1
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 25,slow=420,rstart=4000,rend=8000))) 	#402-31-368-19
    configs.append(config(buyer=fcustom(csvama3,fast= 11,mid= 24,slow=405,rstart=  0,rend=8000))) 	#141-11-344-29
    configs.append(config(buyer=fcustom(csvama3,fast= 16,mid= 17,slow=410,rstart=1500,rend=8000))) 	#311-24-307-26
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid= 24,slow=405,rstart=5500,rend=8000))) 	#366-33-416-12
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid= 25,slow=410,rstart=5500,rend=8000))) 	#439-40-500-8
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid=375,slow=820,rstart=3000,rend=10000))) #462-25-411-17
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=265,slow=1030,rstart=  0,rend=9500))) 	#202-19-363-11
    configs.append(config(buyer=fcustom(csvama3,fast= 42,mid=270,slow=1020,rstart=1500,rend=5500))) #391-54-500-4
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=295,slow=950,rstart=8500,rend=9500))) 	#315-24-500-4
    configs.append(config(buyer=fcustom(csvama3,fast= 72,mid= 84,slow=1350,rstart=2500,rend=9000))) #227-23-461-13
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=300,slow=950,rstart=500,rend=8500))) 	#333-18-400-10
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=460,slow=790,rstart=1000,rend=9500))) 	#260-13-500-6
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=265,slow=1030,rstart=  0,rend=8500))) 	##679-53-444-9
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid= 84,slow=1350,rstart=  0,rend=8500))) 	#397-37-500-12
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=215,slow=1030,rstart=  0,rend=9500))) 	#272-24-375-16
    configs.append(config(buyer=fcustom(csvama3,fast=128,mid=705,slow=790,rstart=2500,rend=9500))) 	#961-75-333-3
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 45,slow=640,rstart=4000,rend=9000))) 	#579-40-318-22
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 92,slow=1060,rstart=1500,rend=10000)))#476-41-375-24
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 48,slow=710,rstart=4000,rend=8500))) 	#274-22-222-18
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 75,slow= 95,rstart=1500,rend=9000))) 	#448-35-368-19

    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=172,slow=630,rstart=6000,rend=8500))) 	#400-18-500-4
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=172,slow=630,rstart=7000,rend=8500))) 	#425-37-500-2
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid=220,slow=1130,rstart=4000,rend=9000))) #561-41-266-15
    configs.append(config(buyer=fcustom(csvama3,fast= 69,mid= 84,slow=1140,rstart=2500,rend=9000))) #197-14-357-14
    configs.append(config(buyer=fcustom(csvama3,fast= 39,mid= 48,slow=1160,rstart=4000,rend=8500))) #368-21-428-14
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=148,slow=1110,rstart=500,rend=9000))) 	#466-42-333-21
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid= 21,slow=250,rstart=7000,rend=8500))) 	#424-28-375-16
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 21,slow=250,rstart=7500,rend=8000))) 	#473-18-250-4

    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow= 20,rstart=2500,rend=4500))) 	#647-46-323-71
    configs.append(config(buyer=fcustom(csvama2,fast= 10,slow= 60,rstart=5000,rend=8000))) 	#1196-79-363-77
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow= 20,rstart=2500,rend=5500))) 	#1054-77-344-90
    configs.append(config(buyer=fcustom(csvama2,fast=  8,slow= 20,rstart=2500,rend=5000))) 	#782-54-355-76
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow= 45,rstart=7000,rend=7500))) 	#840-58-300-20
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=130,rstart=7000,rend=8500))) 	#840-58-280-25
    configs.append(config(buyer=fcustom(csvama2,fast= 38,slow=475,rstart=4500,rend=7000))) 	#677-42-352-34
    configs.append(config(buyer=fcustom(csvama2,fast=  3,slow= 15,rstart=3000,rend=4500))) 	#898-71-340-47
    configs.append(config(buyer=fcustom(csvama2,fast= 23,slow=100,rstart=3500,rend=8000))) 	#1297-96-397-73
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=160,rstart=4500,rend=8500))) 	#589-43-352-68
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=160,rstart=2500,rend=6500))) 	#839-73-442-52
    configs.append(config(buyer=fcustom(csvama2,fast= 32,slow=470,rstart=5000,rend=6000))) 	#842-32-384-13
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=475,rstart=5000,rend=6000))) 	#700-28-384-13
    configs.append(config(buyer=fcustom(csvama2,fast= 45,slow=425,rstart=5000,rend=6000))) 	#527-29-416-12
    configs.append(config(buyer=fcustom(csvama2,fast= 57,slow=425,rstart=4500,rend=6000))) 	#1452-77-350-20
    configs.append(config(buyer=fcustom(csvama2,fast= 45,slow=630,rstart=5000,rend=6000))) 	#1447-55-363-11
    configs.append(config(buyer=fcustom(csvama2,fast= 13,slow=125,rstart=3000,rend=9000))) 	#828-63-340-91
    configs.append(config(buyer=fcustom(csvama2,fast= 37,slow=115,rstart=3000,rend=9500))) 	#567-42-323-99
    configs.append(config(buyer=fcustom(csvama2,fast= 20,slow=195,rstart=5000,rend=7500))) 	#753-52-317-41
    configs.append(config(buyer=fcustom(csvama2,fast=  4,slow=190,rstart=5000,rend=6500))) 	#752-73-333-21
    configs.append(config(buyer=fcustom(csvama2,fast= 10,slow=195,rstart=5000,rend=6500))) 	#666-54-333-27
    configs.append(config(buyer=fcustom(csvama2,fast=  4,slow=325,rstart=4500,rend=6500))) 	#803-49-333-21
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=320,rstart=5000,rend=6500))) 	#584-38-263-19
    configs.append(config(buyer=fcustom(csvama2,fast= 51,slow=500,rstart=3500,rend=6000))) 	#830-54-343-32
    configs.append(config(buyer=fcustom(csvama2,fast= 63,slow=500,rstart=4500,rend=6000))) 	#1555-84-350-20
    configs.append(config(buyer=fcustom(csvama2,fast= 99,slow=500,rstart=3500,rend=6000))) 	#500-30-382-34
    configs.append(config(buyer=fcustom(csvama2,fast= 57,slow=510,rstart=5000,rend=6000))) 	#755-34-384-13
    configs.append(config(buyer=fcustom(csvama2,fast= 45,slow=510,rstart=5000,rend=6000))) 	#584-31-384-13
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=210,rstart=5000,rend=7000))) 	#650-52-296-27
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=200,rstart=5000,rend=6500))) 	#938-76-333-27
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=205,rstart=5000,rend=7000))) 	#670-53-333-30
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=205,rstart=4500,rend=8500))) 	#507-35-296-54
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=200,rstart=4500,rend=6500))) 	#617-50-352-34
    configs.append(config(buyer=fcustom(csvama2,fast= 15,slow=215,rstart=2500,rend=5500))) 	#510-50-343-32
    configs.append(config(buyer=fcustom(csvama2,fast=  7,slow=200,rstart=5000,rend=6500))) 	#872-75-391-23
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=210,rstart=5000,rend=6500))) 	#680-64-318-22
    configs.append(config(buyer=fcustom(csvama2,fast= 27,slow=205,rstart=5000,rend=7000))) 	#803-53-285-28
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=210,rstart=5500,rend=7500))) 	#936-59-333-30
    configs.append(config(buyer=fcustom(csvama2,fast= 12,slow=210,rstart=5000,rend=6500))) 	#674-56-260-23
    configs.append(config(buyer=fcustom(csvama2,fast=  8,slow=200,rstart=5000,rend=6500))) 	#759-60-304-23
    configs.append(config(buyer=fcustom(csvama2,fast=  1,slow=210,rstart=5000,rend=7500))) 	#666-54-343-32
    configs.append(config(buyer=fcustom(csvama2,fast= 28,slow=170,rstart=5000,rend=6500))) 	#1000-72-357-14
    configs.append(config(buyer=fcustom(csvama2,fast= 72,slow=340,rstart=3500,rend=5500))) 	#510-25-384-13
    configs.append(config(buyer=fcustom(csvama2,fast= 47,slow=400,rstart=4500,rend=6000))) 	#1409-86-368-19
    configs.append(config(buyer=fcustom(csvama2,fast=  4,slow=180,rstart=5000,rend=6500))) 	#684-65-350-20
    configs.append(config(buyer=fcustom(csvama2,fast=435,slow=960,rstart=2500,rend=6000))) 	#731-49-333-3
    configs.append(config(buyer=fcustom(csvama2,fast= 45,slow=670,rstart=1000,rend=6000))) 	#1542-108-375-16
    configs.append(config(buyer=fcustom(csvama2,fast=645,slow=1030,rstart=4500,rend=8000))) #741-63-181-11
    configs.append(config(buyer=fcustom(csvama2,fast= 63,slow=920,rstart=2000,rend=10000))) #687-44-296-27
    configs.append(config(buyer=fcustom(csvama2,fast=300,slow=940,rstart=1000,rend=8500))) 	#1016-61-227-22
    configs.append(config(buyer=fcustom(csvama2,fast=525,slow=710,rstart=1000,rend=9000))) 	#711-42-217-23
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=710,rstart=3000,rend=7500))) 	#725-58-320-25
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=670,rstart=5000,rend=6000))) 	#778-74-500-4
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=670,rstart=5000,rend=6000))) 	#666-26-285-7
    configs.append(config(buyer=fcustom(csvama2,fast=685,slow=720,rstart=2000,rend=8000))) 	#582-46-307-13
    
    # 储备   
    configs.append(config(buyer=fcustom(csvama2,fast= 34,slow=425,rstart=500,rend=5000))) 	#307-32-392-28
    configs.append(config(buyer=fcustom(csvama2,fast=  5,slow=225,rstart=4500,rend=6500))) 	#487-38-275-29
    configs.append(config(buyer=fcustom(csvama2,fast= 15,slow=235,rstart=5000,rend=8000))) 	#326-32-312-48
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=165,rstart=5000,rend=6500))) 	#292-26-409-22
    configs.append(config(buyer=fcustom(csvama2,fast=  9,slow=450,rstart=5000,rend=5500))) 	#705-24-250-8
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=445,rstart=5000,rend=6500))) 	#283-17-380-21
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=220,rstart=2500,rend=6500))) 	#481-38-312-48
    configs.append(config(buyer=fcustom(csvama2,fast= 15,slow=230,rstart=5000,rend=8500))) 	#376-29-297-47
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=475,rstart=5000,rend=6500))) 	#375-21-391-23
    configs.append(config(buyer=fcustom(csvama2,fast=112,slow=135,rstart=2000,rend=5000))) 	#382-34-333-33
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=495,rstart=500,rend=5000))) 	#292-19-391-23
    configs.append(config(buyer=fcustom(csvama2,fast=164,slow=630,rstart=3000,rend=5500))) 	#397-29-333-21
    configs.append(config(buyer=fcustom(csvama2,fast=108,slow=165,rstart=2000,rend=6000))) 	#267-23-384-39
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=320,rstart=4500,rend=7000))) 	#357-25-390-41
    configs.append(config(buyer=fcustom(csvama2,fast= 47,slow=325,rstart=1000,rend=3000))) 	#217-15-600-5
    configs.append(config(buyer=fcustom(csvama2,fast=132,slow=325,rstart=2000,rend=4000))) 	#390-52-333-9
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=285,rstart=5000,rend=6000))) 	#333-17-333-15
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=290,rstart=2000,rend=6000))) 	#358-24-214-28
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=355,rstart=2000,rend=6000))) 	#395-36-459-37
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=365,rstart=5000,rend=6500))) 	#353-23-347-23
    configs.append(config(buyer=fcustom(csvama2,fast= 51,slow=660,rstart=500,rend=5500))) 	#369-24-454-22
    configs.append(config(buyer=fcustom(csvama2,fast= 42,slow=285,rstart=2000,rend=5000))) 	#360-31-230-26
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=175,rstart=1000,rend=8000))) 	#135-10-294-68
    configs.append(config(buyer=fcustom(csvama2,fast= 54,slow=285,rstart=500,rend=5500))) 	#436-31-324-37
    configs.append(config(buyer=fcustom(csvama2,fast=132,slow=340,rstart=2000,rend=4000))) 	#464-53-375-8
    configs.append(config(buyer=fcustom(csvama2,fast= 39,slow=340,rstart=2000,rend=5500))) 	#436-41-483-31
    configs.append(config(buyer=fcustom(csvama2,fast= 33,slow=400,rstart=1000,rend=6500))) 	#482-41-422-45
    configs.append(config(buyer=fcustom(csvama2,fast=144,slow=415,rstart=1500,rend=6000))) 	#354-22-333-24
    configs.append(config(buyer=fcustom(csvama2,fast=248,slow=395,rstart=1500,rend=3500))) 	#356-46-375-8
    configs.append(config(buyer=fcustom(csvama2,fast= 57,slow=265,rstart=5000,rend=6000))) 	#416-15-250-8
    configs.append(config(buyer=fcustom(csvama2,fast= 23,slow=260,rstart=3500,rend=7500))) 	#171-12-269-52
    configs.append(config(buyer=fcustom(csvama2,fast= 36,slow=250,rstart=  0,rend=6500))) 	#318-22-256-39
    configs.append(config(buyer=fcustom(csvama2,fast= 39,slow=1300,rstart=500,rend=9000))) 	#432-32-555-18
    configs.append(config(buyer=fcustom(csvama2,fast=140,slow=680,rstart=3500,rend=6000))) 	#104-5-454-11
    configs.append(config(buyer=fcustom(csvama2,fast= 39,slow=180,rstart=1000,rend=8000))) 	#27-2-265-64
    configs.append(config(buyer=fcustom(csvama2,fast= 90,slow=180,rstart=500,rend=6000))) 	#155-14-440-25
    configs.append(config(buyer=fcustom(csvama2,fast=  7,slow=180,rstart=5000,rend=8000))) 	#390-30-348-43
    configs.append(config(buyer=fcustom(csvama2,fast=172,slow=760,rstart=2000,rend=4000))) 	#488-42-166-12
    configs.append(config(buyer=fcustom(csvama2,fast= 57,slow=720,rstart=2000,rend=4500))) 	#156-18-571-7
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=720,rstart=3500,rend=7500))) 	#446-29-400-20

    return configs

def prepare_configs_A1200(seller,pman,dman):    #R>=400,winrate>400 or R>=1000,winrate>333
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    
    #候选A_1200 winrate>=400且R>=800,times>5 or  R>500且winrate>500     如果1200和2000都满足，优先为1200
    configs.append(config(buyer=fcustom(svama3,fast= 39,mid= 71,slow=490,ma_standard=120,extend_days=  1))) #6046-205-500-8 #5522-243-714-7    
    configs.append(config(buyer=fcustom(vama3,fast= 18,mid= 57,slow=115,ma_standard=500,extend_days=  1))) 	#4238-267-500-12    #3726-272-583-12
    configs.append(config(buyer=fcustom(vama3,fast= 20,mid= 56,slow=105,ma_standard=500,extend_days=  1))) 	#3395-275-500-8     #2524-313-625-8
    configs.append(config(buyer=fcustom(vama3,fast= 17,mid= 46,slow= 85,ma_standard= 55,extend_days=  1))) 	#1107-62-500-28     #853-76-535-28
    configs.append(config(buyer=fcustom(csvama2,fast= 11,slow=155,rstart=0,rend=4500))) 	#1597-115-628-35    #1671-127-657-35
    configs.append(config(buyer=fcustom(csvama2,fast=  1,slow=180,rstart=1000,rend=3000))) 	#2091-205-636-11    #1805-195-636-11
    configs.append(config(buyer=fcustom(csvama2,fast= 31,slow=385,rstart=3500,rend=6500))) 	#1037-82-516-31     #1174-74-451-31
    configs.append(config(buyer=fcustom(csvama2,fast= 33,slow=670,rstart=5000,rend=6000))) 	#1529-104-500-6     #1529-104-500-6
    configs.append(config(buyer=fcustom(csvama2,fast=790,slow=810,rstart=2000,rend=4500))) 	#74500-298-857-7    #74500-298-857-7
    configs.append(config(buyer=fcustom(csvama3,fast= 33,mid=  5,slow= 40,rstart=2000,rend=4500))) 	#4978-473-625-8 #3757-496-875-8
    configs.append(config(buyer=fcustom(csvama3,fast= 33,mid=  9,slow= 40,rstart=2500,rend=4500))) 	#3587-287-545-11    #3402-330-636-11
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 45,slow= 95,rstart=1500,rend=9000))) 	#2396-139-576-26    #1873-133-576-26
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 26,slow=100,rstart=4000,rend=8500))) 	#2615-170-521-23    #2617-178-565-23
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=705,slow=1110,rstart=  0,rend=8500))) 	#4784-244-625-8     #6100-305-750-8
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 92,slow=1110,rstart=8000,rend=9500)))	#1178-165-571-7     #1282-168-571-7
    configs.append(config(buyer=fcustom(csvama3,fast= 14,mid= 48,slow=1120,rstart=4500,rend=8500)))	#1948-76-500-10     #1461-91-600-10
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 48,slow=1140,rstart=4000,rend=8500))) #1425-57-538-13     #1193-74-692-13
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 57,slow=1270,rstart=4000,rend=8500))) #2314-125-500-12    #2540-155-600-12
    configs.append(config(buyer=fcustom(csvama3,fast= 10,mid= 54,slow=1770,rstart=5000,rend=8500))) #880-37-500-10      #626-52-600-10
    configs.append(config(buyer=fcustom(svama3,fast=165,mid=340,slow=1790))) 	#1125-81-625-24     #1323-90-625-24
    configs.append(config(buyer=fcustom(svama3,fast=185,mid=260,slow=1800))) 	#830-59-500-32      #638-60-593-32
    configs.append(config(buyer=fcustom(csvama3,fast= 36,mid= 78,slow=500,rstart=4000,rend=8500))) 	##1564-133-500-14   #1287-139-571-14
    configs.append(config(buyer=fcustom(csvama3,fast= 20,mid= 33,slow=630,rstart=4000,rend=8500))) 	##946-71-500-30     #720-67-500-25
    configs.append(config(buyer=fcustom(csvama2,fast= 14,slow=170,rstart=4000,rend=6500))) 	###1545-119-500-34    #1168-118-558-34
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid= 84,slow=1110,rstart=  0,rend=8500))) 	##1792-95-500-20    #1296-83-450-20
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 92,slow=1120,rstart=2500,rend=9000))) ##2058-140-500-12   #1455-115-416-12
    

    return configs


def prepare_configs_A2000(seller,pman,dman):    #R>=400,winrate>400 or R>=1000,winrate>333
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    
    #候选A_2000 winrate>=400且R>=800,times>5 or  R>500且winrate>500
    configs.append(config(buyer=fcustom(csvama2,fast= 13,slow=125,rstart= 1000,rend=5000))) 	#975-80-418-43  #1292-115-500-42
    configs.append(config(buyer=fcustom(svama3,fast= 39,mid= 71,slow=490,ma_standard=500,extend_days=  1))) #4243-157-400-5 #3772-166-600-5
    configs.append(config(buyer=fcustom(csvama2,fast= 25,slow=140,rstart=5000,rend=6000))) 	#2150-129-400-15    #1975-158-600-15
    configs.append(config(buyer=fcustom(csvama2,fast=184,slow=305,rstart=4000,rend=5500))) 	#-108   #2716-144-666-9
    configs.append(config(buyer=fcustom(csvama2,fast=128,slow=405,rstart=2500,rend=5500))) 	#208-14-473-19      #1558-106-684-19
    configs.append(config(buyer=fcustom(csvama2,fast= 30,slow=475,rstart=5000,rend=6000))) 	#340-17-400-15      #1000-48-533-15
    configs.append(config(buyer=fcustom(csvama2,fast= 48,slow=385,rstart=2500,rend=4000))) 	#1039-109-400-10    #1504-179-500-10
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 25,slow=410,rstart=5500,rend=9000))) 	#691-47-461-13      #891-74-538-13
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 63,slow=730,rstart=5000,rend=10000))) #168-126-545-11     #1107-113-545-11
    configs.append(config(buyer=fcustom(csvama3,fast=  2,mid=215,slow=1050,rstart=2500,rend=9000))) #750-69-357-14  #897-88-500-14
    configs.append(config(buyer=fcustom(csvama2,fast= 60,slow=720,rstart=3500,rend=6000))) 	#345-19-307-13      ##1256-98-538-13
    configs.append(config(buyer=fcustom(csvama2,fast=635,slow=1110,rstart=1500,rend=7000))) #2406-142-300-10    ##6545-288-500-10
    configs.append(config(buyer=fcustom(csvama3,fast=  7,mid= 30,slow= 50,rstart=4000,rend=5500))) 	#4071-285-461-13    ##4054-300-538-13
    configs.append(config(buyer=fcustom(csvama3,fast= 22,mid=325,slow=640,rstart=4000,rend=8500))) 	#729-62-500-6       ##1901-289-833-6
    configs.append(config(buyer=fcustom(csvama3,fast=  8,mid= 57,slow=730,rstart=4000,rend=9000))) 	#1521-108-333-9     ##2056-220-555-9
    configs.append(config(buyer=fcustom(csvama3,fast=  5,mid= 45,slow=740,rstart=4000,rend=9000))) 	#959-71-357-14      ##1761-148-500-14
    configs.append(config(buyer=fcustom(csvama3,fast=  6,mid= 48,slow=740,rstart=4000,rend=8500))) 	#2604-211-454-11    ##3756-293-545-11
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=345,slow=1030,rstart=  0,rend=9500))) 	#2648-143-300-10    ##2981-164-500-10
    
    return configs

def prepare_configs_A1(seller,pman,dman):   
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []

    #候选A1 winrate>=400且R>=800,times<5    #atr=1200
    configs.append(config(buyer=fcustom(svama3,fast= 23,mid= 79,slow= 10,ma_standard=120,extend_days=  1))) 	#1000-277-1000-1 #1000-277-1000-1
    configs.append(config(buyer=fcustom(svama2s,fast= 48,slow=500,ma_standard= 67,extend_days= 13))) 	#2739-63-500-2  #905-48-500-2
    configs.append(config(buyer=fcustom(svama2s,fast= 26,slow=430,ma_standard= 67,extend_days=  5))) 	#1000-57-1000-3 #1000-56-1000-3
    configs.append(config(buyer=fcustom(svama2x,fast= 11,slow=  5,base=198,ma_standard=500))) 	#1000-116-1000-1    #1000-116-1000-1
    configs.append(config(buyer=fcustom(svama2x,fast= 18,slow=  5,base=198,ma_standard= 10))) 	#2127-117-666-3     #1000-187-1000-3
    configs.append(config(buyer=fcustom(svama2x,fast=  6,slow=  5,base=240,ma_standard=500))) 	#1000-148-1000-4    #1000-148-1000-1
    configs.append(config(buyer=fcustom(svama2x,fast= 28,slow=  5,base=240,ma_standard= 10))) 	#1394-159-500-4     #2124-174-500-4
    configs.append(config(buyer=fcustom(svama2x,fast= 15,slow=  5,base=228,ma_standard=250))) 	#1000-131-1000-2    #1000-131-1000-2
    configs.append(config(buyer=fcustom(csvama3,fast= 44,mid= 23,slow=250,rstart=7500,rend=8000))) 	#95000-190-500-2 #1948-152-500-2
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=765,slow=1110,rstart=500,rend=7000))) 	#1000-407-1000-2    #1000-407-1000-2
    configs.append(config(buyer=fcustom(csvama3,fast=  4,mid=655,slow=770,rstart=4000,rend=8500))) 	#1000-162-1000-1    #1000-162-1000-1
    configs.append(config(buyer=fcustom(csvama3,fast=195,mid=335,slow=1350,rstart=7000,rend=10000)))    #3790-235-500-2 #1000-311-1000-2
    configs.append(config(buyer=fcustom(csvama3,fast= 12,mid= 85,slow=165,rstart=5000,rend=5500))) 	#1000-1776-1000-1   #1000-1776-1000-1
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid= 76,slow=410,rstart=3500,rend=8500))) 	#1433-86-500-2  #788-71-500-2
    configs.append(config(buyer=fcustom(csvama3,fast= 11,mid= 82,slow=410,rstart=5500,rend=6000))) 	#1000-137-1000-1    #1000-137-1000-1
    configs.append(config(buyer=fcustom(csvama3,fast=  1,mid=350,slow=950,rstart=8500,rend=9500))) 	#4724-104-500-2     #584-62-500-2

    return configs

def prepare_configs_A2(seller,pman,dman):    
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    
    #A2 存在RP问题的参数配置    atr=1200
    configs.append(config(buyer=fcustom(svama2x,fast=  6,slow=  5,base=240,ma_standard= 10))) 	#2360-118-555-9     #1160-101-555-9
    configs.append(config(buyer=fcustom(vama3,fast= 32,mid= 62,slow= 45,ma_standard=500,extend_days=  1))) 	#884-84-500-16      #629-73-500-16
    
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
    myMediator=nmediator_factory(trade_strategy=B1S1,pricer = oo_pricer)
    seller1200 = atr_seller_factory(stop_times=1200,trace_times=3000)
    seller2000 = atr_seller_factory(stop_times=2000,trace_times=3000)    
    #seller = csc_func
    #seller = fcustom(csc_func,threshold=100)

    #configs = prepare_temp_configs(seller,pman,dman)
    #configs = prepare_configs_A1200(seller1200,pman,dman)
    ##configs = prepare_configs_A2000(seller2000,pman,dman)    
    #configs.extend(prepare_configs_A1(seller1200,pman,dman))
    #configs.extend(prepare_configs_A2(seller1200,pman,dman))    
    batch(configs,sdata,dates,xbegin,cmediator=myMediator)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    

    save_configs('atr_ev_nm_1200.txt',configs,xbegin,end)
    #save_configs('atr_ev_nm_2000.txt',configs,xbegin,end)    

def run_merge_body(sdata,dates,begin,end,xbegin):
    
    from time import time
    tbegin = time()

    pman = AdvancedATRPositionManager()
    dman = DateManager(begin,end)
    myMediator=mediator_factory(trade_strategy=B1S1,pricer = oo_pricer)
    seller1200 = atr_seller_factory(stop_times=1200,trace_times=3000) 
    #seller = csc_func

    configs1200 = prepare_configs_A1200(seller1200,pman,dman)
    configs1200.extend(prepare_configs_A1(seller1200,pman,dman))
    configs1200.extend(prepare_configs_A2(seller1200,pman,dman))
    
    result1200,strade1200 = merge(configs1200,sdata,dates,xbegin,pman,dman,cmediator=myMediator)

    save_merged('atr_merged_1200.txt',result1200,strade1200,xbegin,end)

    seller2000 = atr_seller_factory(stop_times=2000,trace_times=3000) 
    configs2000 = prepare_configs_A2000(seller2000,pman,dman)
    result2000,strade2000 = merge(configs2000,sdata,dates,xbegin,pman,dman,cmediator=myMediator)
    save_merged('atr_merged_2000.txt',result2000,strade2000,xbegin,end)
    
    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    

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
    seller1200 = atr_seller_factory(stop_times=1200,trace_times=3000)
    seller2000 = atr_seller_factory(stop_times=2000,trace_times=3000)    
    #seller = csc_func
    if lbegin == 0:
        lbegin = end - 5

    configs_a = prepare_configs_A1200(seller1200,pman,dman)
    dtrades_a = batch_last(configs_a,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_a1200.txt',dtrades_a,xbegin,end,lbegin)

    configs_a = prepare_configs_A2000(seller2000,pman,dman)
    dtrades_a = batch_last(configs_a,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_a2000.txt',dtrades_a,xbegin,end,lbegin)

    configs_a1 = prepare_configs_A1(seller1200,pman,dman)
    dtrades_a1 = batch_last(configs_a1,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_a1.txt',dtrades_a1,xbegin,end,lbegin)

    configs_a2 = prepare_configs_A2(seller1200,pman,dman)
    dtrades_a2 = batch_last(configs_a2,sdata,dates,xbegin,cmediator=myMediator)
    save_last('atr_last_a2.txt',dtrades_a2,xbegin,end,lbegin)

    #configs_t = prepare_temp_configs(seller1200,pman,dman)
    #dtrades_t = batch_last(configs_t,sdata,dates,xbegin,cmediator=myMediator)
    #save_last('atr_last_t.txt',dtrades_t,xbegin,end,lbegin)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    


if __name__ == '__main__':
    logging.basicConfig(filename="run_x4n_1000.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
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
    #begin,xbegin,end,lbegin = 20070101,20080601,20090327,20090201
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


