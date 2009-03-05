# -*- coding: utf-8 -*-

import unittest
from wolfox.fengine.core.cruiser.result2configs import *

import logging
logger = logging.getLogger('wolfox.fengine.core.cruiser.result2configs_test')

from StringIO import StringIO

svama2_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-02-18 23:04:30,875 DEBUG Mediator:<<lambda>:ma_standard=172,slow=176,fast=22,sma=9:atr_seller:ma_standard=172,slow=176,fast=22,sma=9:make_trade_signal:B1S1>:(1391, 13520, 9718, 7)
                #wolfox.fengine.core.shortcut:log_result:145:2009-02-18 23:04:30,875 DEBUG Mediator:<<lambda>:ma_standard=241,slow=193,fast=22,sma=6:atr_seller:ma_standard=241,slow=193,fast=22,sma=6:make_trade_signal:B1S1>:(1429, 9086, 6358, 4)
'''
svama3_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-02-18 14:48:35,125 DEBUG Mediator:<<lambda>:slow=196,sma=48,ma_standard=111,extend_days=6,fast=27,mid=87:atr_seller:slow=196,sma=48,ma_standard=111,extend_days=6,fast=27,mid=87:make_trade_signal:B1S1>:(2008, 28953, 14418, 11)
##wolfox.fengine.core.shortcut:log_result:145:2009-02-18 14:48:35,125 DEBUG Mediator:<<lambda>:slow=16,sma=70,ma_standard=228,extend_days=22,fast=33,mid=6:atr_seller:slow=16,sma=70,ma_standard=228,extend_days=22,fast=33,mid=6:make_trade_signal:B1S1>:(1940, 17272, 8899, 8)
'''
svama2x_txt = '''#wolfox.fengine.core.shortcut:judge:174:2009-03-05 20:41:57,765 DEBUG Mediator:<<lambda>:slow=154,sma=67,base=152,ma_standard=85,extend_days=5,fast=10:atr_seller:slow=154,sma=67,base=152,ma_standard=85,extend_days=5,fast=10:make_trade_signal:B1S1>:mm:(530, 72242, 136209, 60)
#wolfox.fengine.core.shortcut:judge:174:2009-03-05 20:42:40,046 DEBUG Mediator:<<lambda>:slow=149,sma=47,base=164,ma_standard=55,extend_days=27,fast=6:atr_seller:slow=149,sma=47,base=164,ma_standard=55,extend_days=27,fast=6:make_trade_signal:B1S1>:mm:(421, 65441, 155415, 76)
'''

svama2s_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-02-22 02:45:57,483 DEBUG Mediator:<<lambda>:ma_standard=230,slow=118,extend_days=7,fast=14,sma=85:atr_seller:ma_standard=230,slow=118,extend_days=7,fast=14,sma=85:make_trade_signal:B1S1>:(2072, 39478, 19047, 18)
#wolfox.fengine.core.shortcut:log_result:145:2009-02-22 02:45:57,500 DEBUG Mediator:<<lambda>:ma_standard=230,slow=22,extend_days=23,fast=10,sma=77:atr_seller:ma_standard=230,slow=22,extend_days=23,fast=10,sma=77:make_trade_signal:B1S1>:(2100, 57464, 27352, 26)
'''

vama3_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-02-23 13:18:34,358 DEBUG Mediator:<<lambda>:slow=195,pre_length=6,ma_standard=180,extend_days=21,fast=2,mid=59:atr_seller:slow=195,pre_length=6,ma_standard=180,extend_days=21,fast=2,mid=59:make_trade_signal:B1S1>:(3782, 7561, 1999, 3)
#wolfox.fengine.core.shortcut:log_result:145:2009-02-23 13:18:34,358 DEBUG Mediator:<<lambda>:slow=5,pre_length=106,ma_standard=85,extend_days=9,fast=44,mid=92:atr_seller:slow=5,pre_length=106,ma_standard=85,extend_days=9,fast=44,mid=92:make_trade_signal:B1S1>:(4094, 8386, 2048, 3)
'''

vama2_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-02-24 20:56:11,937 DEBUG Mediator:<<lambda>:pre_length=31,ma_standard=250,slow=18,fast=1:atr_seller:pre_length=31,ma_standard=250,slow=18,fast=1:make_trade_signal:B1S1>:(2050, 8385, 4089, 4)
#wolfox.fengine.core.shortcut:log_result:145:2009-02-24 20:56:11,937 DEBUG Mediator:<<lambda>:pre_length=1,ma_standard=245,slow=38,fast=8:atr_seller:pre_length=1,ma_standard=245,slow=38,fast=8:make_trade_signal:B1S1>:(2102, 23633, 11241, 8)
'''
vama2x_txt = '''#wolfox.fengine.core.shortcut:judge:174:2009-03-05 21:50:22,187 DEBUG Mediator:<<lambda>:slow=81,base=50,pre_length=146,ma_standard=65,extend_days=25,fast=16:atr_seller:slow=81,base=50,pre_length=146,ma_standard=65,extend_days=25,fast=16:make_trade_signal:B1S1>:mm:(423, 550130, 1299040, 458)
#wolfox.fengine.core.shortcut:judge:174:2009-03-05 21:51:03,858 DEBUG Mediator:<<lambda>:slow=232,base=58,pre_length=86,ma_standard=160,extend_days=19,fast=24:atr_seller:slow=232,base=58,pre_length=86,ma_standard=160,extend_days=19,fast=24:make_trade_signal:B1S1>:mm:(559, 124328, 222183, 99)
'''

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
