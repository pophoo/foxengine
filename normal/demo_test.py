# -*- coding: utf-8 -*-

import unittest

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
    def test_demo(self):
        import sys
        from StringIO import StringIO
        tmp = sys.stdout
        sys.stdout = StringIO()  #将标准I/O流重定向到buff对象，抑制输出
        
        begin,end = 20010101,20060101
        dates = get_ref_dates(begin,end)
        sdata = cs.get_stocks(['SH600000'],begin,end,ref_id)
        
        demo(sdata,dates)
        #print 'xxx'
        sys.stdout = tmp        #恢复标准I/O流
        #print 'uuuu'
        self.assertTrue(True)


if __name__ == "__main__":
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    unittest.main()

