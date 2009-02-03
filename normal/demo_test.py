# -*- coding: utf-8 -*-

import unittest
from wolfox.fengine.normal.demo import *

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
    unittest.main()

