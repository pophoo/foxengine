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

svama2s_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-02-22 02:45:57,483 DEBUG Mediator:<<lambda>:ma_standard=230,slow=118,extend_days=7,fast=14,sma=85:atr_seller:ma_standard=230,slow=118,extend_days=7,fast=14,sma=85:make_trade_signal:B1S1>:(2072, 39478, 19047, 18)
#wolfox.fengine.core.shortcut:log_result:145:2009-02-22 02:45:57,500 DEBUG Mediator:<<lambda>:ma_standard=230,slow=22,extend_days=23,fast=10,sma=77:atr_seller:ma_standard=230,slow=22,extend_days=23,fast=10,sma=77:make_trade_signal:B1S1>:(2100, 57464, 27352, 26)
'''

vama3_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-02-23 13:18:34,358 DEBUG Mediator:<<lambda>:slow=195,pre_length=6,ma_standard=180,extend_days=21,fast=2,mid=59:atr_seller:slow=195,pre_length=6,ma_standard=180,extend_days=21,fast=2,mid=59:make_trade_signal:B1S1>:(3782, 7561, 1999, 3)
#wolfox.fengine.core.shortcut:log_result:145:2009-02-23 13:18:34,358 DEBUG Mediator:<<lambda>:slow=5,pre_length=106,ma_standard=85,extend_days=9,fast=44,mid=92:atr_seller:slow=5,pre_length=106,ma_standard=85,extend_days=9,fast=44,mid=92:make_trade_signal:B1S1>:(4094, 8386, 2048, 3)
'''

vama2_txt = '''#wolfox.fengine.core.shortcut:log_result:145:2009-02-24 20:56:11,937 DEBUG Mediator:<<lambda>:pre_length=31,ma_standard=250,slow=18,fast=1:atr_seller:pre_length=31,ma_standard=250,slow=18,fast=1:make_trade_signal:B1S1>:(2050, 8385, 4089, 4)
#wolfox.fengine.core.shortcut:log_result:145:2009-02-24 20:56:11,937 DEBUG Mediator:<<lambda>:pre_length=1,ma_standard=245,slow=38,fast=8:atr_seller:pre_length=1,ma_standard=245,slow=38,fast=8:make_trade_signal:B1S1>:(2102, 23633, 11241, 8)
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



if __name__ == "__main__":
    import logging
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='#%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')    
    unittest.main()    
