# -*- coding: utf-8 -*-

import unittest
from wolfox.fengine.core.cruiser.result2configs import *

import logging
logger = logging.getLogger('wolfox.fengine.core.cruiser.result2configs_test')

from StringIO import StringIO

#svama2_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-02-18 23:04:30,875 DEBUG Mediator:<<lambda>:ma_standard=172,slow=176,fast=22,sma=9:atr_seller:ma_standard=172,slow=176,fast=22,sma=9:make_trade_signal:B1S1>:(1391, 13520, 9718, 7)
                #wolfox.fengine.core.shortcut:log_result:145:2009-02-18 23:04:30,875 DEBUG Mediator:<<lambda>:ma_standard=241,slow=193,fast=22,sma=6:atr_seller:ma_standard=241,slow=193,fast=22,sma=6:make_trade_signal:B1S1>:(1429, 9086, 6358, 4)'''
svama2_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-03-09 03:35:22,062 DEBUG Mediator:<<lambda>:ma_standard=250,slow=128,fast=16:atr_seller:ma_standard=250,slow=128,fast=16:make_trade_signal:B1S1>:(1137, 316847, 278570, 166)
#wolfox.fengine.core.shortcut:log_result:145:2009-03-09 03:35:22,062 DEBUG Mediator:<<lambda>:ma_standard=250,slow=99,fast=32:atr_seller:ma_standard=250,slow=99,fast=32:make_trade_signal:B1S1>:(1144, 323767, 282858, 177)
'''

csvama2_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-03-15 10:38:02,125 DEBUG Mediator:<<lambda>:slow=250,rstart=500,rend=10000,fast=5:atr_seller:slow=250,rstart=500,rend=10000,fast=5:make_trade_signal:B1S1>:(1905, 108785, 57093, 39)
#wolfox.fengine.core.shortcut:log_result:145:2009-03-15 10:38:02,125 DEBUG Mediator:<<lambda>:slow=125,rstart=0,rend=1500,fast=13:atr_seller:slow=125,rstart=0,rend=1500,fast=13:make_trade_signal:B1S1>:(1924, 7382, 3835, 3)
'''

#svama3_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-02-18 14:48:35,125 DEBUG Mediator:<<lambda>:slow=196,sma=48,ma_standard=111,extend_days=6,fast=27,mid=87:atr_seller:slow=196,sma=48,ma_standard=111,extend_days=6,fast=27,mid=87:make_trade_signal:B1S1>:(2008, 28953, 14418, 11)
##wolfox.fengine.core.shortcut:log_result:145:2009-02-18 14:48:35,125 DEBUG Mediator:<<lambda>:slow=16,sma=70,ma_standard=228,extend_days=22,fast=33,mid=6:atr_seller:slow=16,sma=70,ma_standard=228,extend_days=22,fast=33,mid=6:make_trade_signal:B1S1>:(1940, 17272, 8899, 8)'''

svama3_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-03-09 19:11:47,328 DEBUG Mediator:<<lambda>:ma_standard=67,slow=54,extend_days=25,fast=16,mid=9:atr_seller:ma_standard=67,slow=54,extend_days=25,fast=16,mid=9:make_trade_signal:B1S1>:(1213, 291035, 239852, 123)
#wolfox.fengine.core.shortcut:log_result:145:2009-03-09 19:11:47,328 DEBUG Mediator:<<lambda>:ma_standard=250,slow=196,extend_days=23,fast=15,mid=22:atr_seller:ma_standard=250,slow=196,extend_days=23,fast=15,mid=22:make_trade_signal:B1S1>:(1215, 176026, 144823, 82)
'''

csvama3_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-03-15 06:11:56,500 DEBUG Mediator:<<lambda>:slow=290,rstart=2000,mid=13,fast=4,rend=8000:atr_seller:slow=290,rstart=2000,mid=13,fast=4,rend=8000:make_trade_signal:B1S1>:(1012, 59609, 58896, 23)
#wolfox.fengine.core.shortcut:log_result:145:2009-03-15 06:11:56,500 DEBUG Mediator:<<lambda>:slow=250,rstart=2000,mid=21,fast=7,rend=8000:atr_seller:slow=250,rstart=2000,mid=21,fast=7,rend=8000:make_trade_signal:B1S1>:(1043, 39049, 37407, 16)
'''

#svama2x_txt = '''#wolfox.fengine.core.shortcut:judge:174:2009-03-05 20:41:57,765 DEBUG Mediator:<<lambda>:slow=154,sma=67,base=152,ma_standard=85,extend_days=5,fast=10:atr_seller:slow=154,sma=67,base=152,ma_standard=85,extend_days=5,fast=10:make_trade_signal:B1S1>:mm:(530, 72242, 136209, 60)
#wolfox.fengine.core.shortcut:judge:174:2009-03-05 20:42:40,046 DEBUG Mediator:<<lambda>:slow=149,sma=47,base=164,ma_standard=55,extend_days=27,fast=6:atr_seller:slow=149,sma=47,base=164,ma_standard=55,extend_days=27,fast=6:make_trade_signal:B1S1>:mm:(421, 65441, 155415, 76)'''

#svama2x_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-03-07 03:56:39,530 DEBUG Mediator:<<lambda>:ma_standard=245,base=62,fast=5,sma=47,slow=181:atr_seller:ma_standard=245,base=62,fast=5,sma=47,slow=181:make_trade_signal:B1S1>:(2324, 105150, 45240, 55)
#wolfox.fengine.core.shortcut:log_result:145:2009-03-07 03:56:39,530 DEBUG Mediator:<<lambda>:ma_standard=255,base=58,fast=5,sma=47,slow=241:atr_seller:ma_standard=255,base=58,fast=5,sma=47,slow=241:make_trade_signal:B1S1>:(2503, 101735, 40630, 51)'''


svama2x_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-03-10 15:16:47,875 DEBUG Mediator:<<lambda>:ma_standard=22,base=226,fast=15,slow=410:atr_seller:ma_standard=22,base=226,fast=15,slow=410:make_trade_signal:B1S1>:(1000, 362985, 362671, 262)
#wolfox.fengine.core.shortcut:log_result:145:2009-03-10 15:16:47,875 DEBUG Mediator:<<lambda>:ma_standard=22,base=196,fast=43,slow=210:atr_seller:ma_standard=22,base=196,fast=43,slow=210:make_trade_signal:B1S1>:(1003, 489505, 488027, 293)
'''

#svama2c_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-03-07 03:49:14,515 DEBUG Mediator:<<lambda>:threshold=5000,ma_standard=45,slow=55,fast=1,sma=115:atr_seller:threshold=5000,ma_standard=45,slow=55,fast=1,sma=115:make_trade_signal:B1S1>:(2097, 206184, 98305, 82)
#wolfox.fengine.core.shortcut:log_result:145:2009-03-07 03:49:14,515 DEBUG Mediator:<<lambda>:threshold=5000,ma_standard=45,slow=183,fast=1,sma=51:atr_seller:threshold=5000,ma_standard=45,slow=183,fast=1,sma=51:make_trade_signal:B1S1>:(2160, 8992, 4162, 4)'''

svama2c_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-03-10 19:14:17,280 DEBUG Mediator:<<lambda>:ma_standard=22,slow=155,fast=41:atr_seller:ma_standard=22,slow=155,fast=41:make_trade_signal:B1S1>:(1018, 1180278, 1158571, 613)
#wolfox.fengine.core.shortcut:log_result:145:2009-03-10 19:14:17,280 DEBUG Mediator:<<lambda>:ma_standard=250,slow=155,fast=41:atr_seller:ma_standard=250,slow=155,fast=41:make_trade_signal:B1S1>:(1036, 873875, 843100, 462)
'''
#svama2s_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-02-22 02:45:57,483 DEBUG Mediator:<<lambda>:ma_standard=230,slow=118,extend_days=7,fast=14,sma=85:atr_seller:ma_standard=230,slow=118,extend_days=7,fast=14,sma=85:make_trade_signal:B1S1>:(2072, 39478, 19047, 18)
#wolfox.fengine.core.shortcut:log_result:145:2009-02-22 02:45:57,500 DEBUG Mediator:<<lambda>:ma_standard=230,slow=22,extend_days=23,fast=10,sma=77:atr_seller:ma_standard=230,slow=22,extend_days=23,fast=10,sma=77:make_trade_signal:B1S1>:(2100, 57464, 27352, 26)'''
svama2s_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-03-10 11:15:18,030 DEBUG Mediator:<<lambda>:ma_standard=250,slow=85,extend_days=25,fast=39:atr_seller:ma_standard=250,slow=85,extend_days=25,fast=39:make_trade_signal:B1S1>:(1171, 22304, 19037, 22)
#wolfox.fengine.core.shortcut:log_result:145:2009-03-10 11:15:18,030 DEBUG Mediator:<<lambda>:ma_standard=67,slow=190,extend_days=25,fast=6:atr_seller:ma_standard=67,slow=190,extend_days=25,fast=6:make_trade_signal:B1S1>:(1273, 179475, 140925, 80)
'''

#vama3_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-02-23 13:18:34,358 DEBUG Mediator:<<lambda>:slow=195,pre_length=6,ma_standard=180,extend_days=21,fast=2,mid=59:atr_seller:slow=195,pre_length=6,ma_standard=180,extend_days=21,fast=2,mid=59:make_trade_signal:B1S1>:(3782, 7561, 1999, 3)
#wolfox.fengine.core.shortcut:log_result:145:2009-02-23 13:18:34,358 DEBUG Mediator:<<lambda>:slow=5,pre_length=106,ma_standard=85,extend_days=9,fast=44,mid=92:atr_seller:slow=5,pre_length=106,ma_standard=85,extend_days=9,fast=44,mid=92:make_trade_signal:B1S1>:(4094, 8386, 2048, 3)'''

vama3_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-03-11 04:02:45,092 DEBUG Mediator:<<lambda>:ma_standard=500,slow=55,extend_days=1,fast=32,mid=79:atr_seller:ma_standard=500,slow=55,extend_days=1,fast=32,mid=79:make_trade_signal:B1S1>:(3550000, 7100, 2, 2)
#wolfox.fengine.core.shortcut:log_result:145:2009-03-11 04:02:45,092 DEBUG Mediator:<<lambda>:ma_standard=800,slow=410,extend_days=1,fast=48,mid=81:atr_seller:ma_standard=800,slow=410,extend_days=1,fast=48,mid=81:make_trade_signal:B1S1>:(3764000, 3764, 1, 1)
'''

vama2_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-02-24 20:56:11,937 DEBUG Mediator:<<lambda>:pre_length=31,ma_standard=250,slow=18,fast=1:atr_seller:pre_length=31,ma_standard=250,slow=18,fast=1:make_trade_signal:B1S1>:(2050, 8385, 4089, 4)
#wolfox.fengine.core.shortcut:log_result:145:2009-02-24 20:56:11,937 DEBUG Mediator:<<lambda>:pre_length=1,ma_standard=245,slow=38,fast=8:atr_seller:pre_length=1,ma_standard=245,slow=38,fast=8:make_trade_signal:B1S1>:(2102, 23633, 11241, 8)'''

vama2_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-03-11 06:03:25,765 DEBUG Mediator:<<lambda>:ma_standard=55,slow=5,fast=38:atr_seller:ma_standard=55,slow=5,fast=38:make_trade_signal:B1S1>:(1305, 78672, 60264, 44)
#wolfox.fengine.core.shortcut:log_result:145:2009-03-11 06:03:25,765 DEBUG Mediator:<<lambda>:ma_standard=500,slow=20,fast=35:atr_seller:ma_standard=500,slow=20,fast=35:make_trade_signal:B1S1>:(1412, 203081, 143809, 87)
'''

vama2x_txt='''#wolfox.fengine.core.shortcut:log_result:145:2009-03-11 08:18:58,046 DEBUG Mediator:<<lambda>:ma_standard=250,base=182,fast=43,slow=20:atr_seller:ma_standard=250,base=182,fast=43,slow=20:make_trade_signal:B1S1>:(8040, 33788, 4202, 5)
#wolfox.fengine.core.shortcut:log_result:145:2009-03-11 08:18:58,046 DEBUG Mediator:<<lambda>:ma_standard=10,base=182,fast=43,slow=15:atr_seller:ma_standard=10,base=182,fast=43,slow=15:make_trade_signal:B1S1>:(12074000, 12074, 1, 2)
'''

#vama2x_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-03-08 05:13:31,489 DEBUG Mediator:<<lambda>:pre_length=91,ma_standard=250,base=148,fast=18,slow=175:atr_seller:pre_length=91,ma_standard=250,base=148,fast=18,slow=175:make_trade_signal:B1S1>:(3033, 129088, 42558, 58)
#wolfox.fengine.core.shortcut:log_result:145:2009-03-08 05:13:31,489 DEBUG Mediator:<<lambda>:pre_length=91,ma_standard=250,base=140,fast=18,slow=105:atr_seller:pre_length=91,ma_standard=250,base=140,fast=18,slow=105:make_trade_signal:B1S1>:(3165, 102432, 32359, 48)'''

ma3_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-02-25 02:41:09,203 DEBUG Mediator:<<lambda>:ma_standard=195,slow=103,extend_days=31,fast=36,mid=43:atr_seller:ma_standard=195,slow=103,extend_days=31,fast=36,mid=43:make_trade_signal:B1S1>:(3256, 3244448, 996354, 782)
#wolfox.fengine.core.shortcut:log_result:145:2009-02-25 02:41:09,203 DEBUG Mediator:<<lambda>:ma_standard=185,slow=103,extend_days=31,fast=38,mid=43:atr_seller:ma_standard=185,slow=103,extend_days=31,fast=38,mid=43:make_trade_signal:B1S1>:(2855, 3182238, 1114287, 818)
'''

file_input,file_output = 'test_result2configs_input','test_result2configs_output'

class ModuleTest(unittest.TestCase):
    def test_lines2configs(self):
        rf = StringIO(svama2_txt)
        wf = StringIO()
        lines2configs('svama2',rf,wf)
        result = wf.getvalue()
        rows = result.split('\n')
        self.assertEquals(3,len(rows))

    def test_transform(self):
        line = '''#wolfox.fengine.core.shortcut:log_result:145:2009-02-18 23:04:30,875 DEBUG Mediator:<<lambda>:ma_standard=172,slow=176,fast=22,sma=9:atr_seller:ma_standard=172,slow=176,fast=22,sma=9:make_trade_signal:B1S1>:(1391, 13520, 9718, 7)'''
        pattern = re.compile(r'''ma_standard=(?P<ma_standard>\d+),slow=(?P<slow>\d+),fast=(?P<fast>\d+),sma=(?P<sma>\d+)''')
        groups = ['fast','slow','sma','ma_standard']
        self.assertEquals('fast= 22,slow=176,sma=  9,ma_standard=172',transform(line,pattern,groups))

    def test_results2configs(self): #只测试通路
        rfile = open(file_input,'w+')
        rfile.write(svama2_txt)
        rfile.close()
        result2configs('svama2',file_input,file_output)
        self.assertRaises(KeyError,result2configs,'key not exists',file_input,file_output)
        import os
        os.remove(file_input)
        os.remove(file_output)

    def test_svama2(self):
        rf = StringIO(svama2_txt)
        wf = StringIO()
        lines2configs('svama2',rf,wf)
        result = wf.getvalue()
        rows = result.split('\n')
        self.assertEquals(3,len(rows))

    def test_csvama2(self):
        rf = StringIO(csvama2_txt)
        wf = StringIO()
        lines2configs('csvama2',rf,wf)
        result = wf.getvalue()
        rows = result.split('\n')
        self.assertEquals(3,len(rows))

    def test_svama2c(self):
        rf = StringIO(svama2c_txt)
        wf = StringIO()
        lines2configs('svama2c',rf,wf)
        result = wf.getvalue()
        rows = result.split('\n')
        self.assertEquals(3,len(rows))

    def test_svama2x(self):
        rf = StringIO(svama2x_txt)
        wf = StringIO()
        lines2configs('svama2x',rf,wf)
        result = wf.getvalue()
        rows = result.split('\n')
        self.assertEquals(3,len(rows))

    def test_svama3(self):
        rf = StringIO(svama3_txt)
        wf = StringIO()
        lines2configs('svama3',rf,wf)
        result = wf.getvalue()
        rows = result.split('\n')
        self.assertEquals(3,len(rows))

    def test_csvama3(self):
        rf = StringIO(csvama3_txt)
        wf = StringIO()
        lines2configs('csvama3',rf,wf)
        result = wf.getvalue()
        rows = result.split('\n')
        self.assertEquals(3,len(rows))

    def test_svama2s(self):
        rf = StringIO(svama2s_txt)
        wf = StringIO()
        lines2configs('svama2s',rf,wf)
        result = wf.getvalue()
        rows = result.split('\n')
        self.assertEquals(3,len(rows))

    def test_vama3(self):
        rf = StringIO(vama3_txt)
        wf = StringIO()
        lines2configs('vama3',rf,wf)
        result = wf.getvalue()
        rows = result.split('\n')
        self.assertEquals(3,len(rows))

    def test_vama2(self):
        rf = StringIO(vama2_txt)
        wf = StringIO()
        lines2configs('vama2',rf,wf)
        result = wf.getvalue()
        rows = result.split('\n')
        self.assertEquals(3,len(rows))

    def test_vama2x(self):
        rf = StringIO(vama2x_txt)
        wf = StringIO()
        lines2configs('vama2x',rf,wf)
        result = wf.getvalue()
        rows = result.split('\n')
        self.assertEquals(3,len(rows))

    def test_ma3(self):
        rf = StringIO(ma3_txt)
        wf = StringIO()
        lines2configs('ma3',rf,wf)
        result = wf.getvalue()
        rows = result.split('\n')
        self.assertEquals(3,len(rows))


if __name__ == "__main__":
    import logging
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='#%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')    
    unittest.main()    
