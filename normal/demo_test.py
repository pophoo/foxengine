# -*- coding: utf-8 -*-

import unittest

import sys
import os
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    #准备测试环境
    from django.core.management import setup_environ
    import wolfox.foxit.other_settings.settings_sqlite_test as settings
    setup_environ(settings)


from wolfox.fengine.normal.demo import *

import logging
logger = logging.getLogger('wolfox.fengine.normal.core.raw_test')

class ModuleTest(unittest.TestCase):    #保持demo的有效性
    def setUp(self):
        from StringIO import StringIO
        self.tmp = sys.stdout
        sys.stdout = StringIO()  #将标准I/O流重定向到buff对象，抑制输出

    def tearDown(self):
        sout = sys.stdout.getvalue()
        logger.debug(u'demo测试控制台输出:%s',sout)
        sys.stdout = self.tmp        #恢复标准I/O流
        #print sout
    
    def test_demo(self):
        begin,end = 20010101,20060101
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        d_posort('g5',sdata.values(),distance=5)        
        d_posort('g20',sdata.values(),distance=20)    
        d_posort('g120',sdata.values(),distance=120)     
        d_posort('g250',sdata.values(),distance=250)            
        demo(sdata,dates,begin,end)        
        self.assertTrue(True)


if __name__ == "__main__":
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    unittest.main()

