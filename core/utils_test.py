# -*- coding: utf-8 -*-

import unittest
from wolfox.fengine.core.base import CommonObject
from wolfox.fengine.core.utils import *

class ModuleTest(unittest.TestCase):
    def test_fcustom(self):
        def x1(a,b):pass
        cx0 = fcustom(x1)   #偏函数偏置
        self.assertEquals('x1:',cx0.__name__)
        cx1 = fcustom(x1,a=2)
        self.assertEquals('x1:a=2',cx1.__name__)
        cx2 = fcustom(x1,b=2)
        self.assertEquals('x1:b=2',cx2.__name__)
        def y(a,b,c=3):pass
        cy1 = fcustom(y,a=2)
        self.assertEquals('y:a=2',cy1.__name__)

    def test_names(self):
        self.assertEquals((),names())
        a,b = CommonObject(id=1),CommonObject(id=2)
        a.__name__,b.__name__ = 'af','bf'
        self.assertEquals(('af','bf'),names(a,b))

    def test_seq_diff(self):
        self.assertEquals([],seq_diff([],[]))
        self.assertEquals([],seq_diff([],[1,2]))
        self.assertEquals([1,2],seq_diff([1,2],[]))
        self.assertEquals([1,2],seq_diff([1,1,2,2],[]))        
        self.assertEquals([1],seq_diff([1,1,2],[2]))

    def test_get_null_obj_number(self):
        n = get_null_obj_number(list)
        a = []
        n1 = get_null_obj_number(list)
        self.assertEquals(n1,n+1)

    def test_get_obj_number(self):
        n = get_obj_number(list)
        a = []
        n1 = get_obj_number(list)
        self.assertEquals(n1,n+1)
    
    def xtest_memory_guard(self):   #虚拟内存被禁后失效?
        inner_func = lambda : []
        ig = memory_guard(list)(inner_func)
        ig()
        self.assertTrue(ig.new_num > 1)
        ig2 = memory_guard(list,lambda t : not t)(inner_func)
        ig2()
        self.assertEquals(1,ig2.new_num)

    def xtest_mguard_example(self): #虚拟内存被禁后失效?
        mg = mguard_example
        mg()
        self.assertEquals(1,mg.new_num)

    def xtest_mguard_example_debug(self):  #虚拟内存被禁后失效?
        #测试debug分支的语法正确性
        import sys
        from StringIO import StringIO
        tmp = sys.stdout
        sys.stdout = StringIO()  #将标准I/O流重定向到buff对象，抑制输出
        ##测试
        inner_func = lambda : []
        ig = memory_guard(list,debug=True)(inner_func)
        ig()
        #print 'xxx'
        sys.stdout = tmp        #恢复标准I/O流
        #print 'uuuu'
        self.assertTrue(True)

if __name__ == "__main__":
    import logging
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    unittest.main()
