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
logger = logging.getLogger('wolfox.fengine.normal.core.funcs_test')

class ModuleTest(unittest.TestCase):    #保持demo的有效性
    
    def test_funcs(self):
        pass

if __name__ == "__main__":
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    unittest.main()

