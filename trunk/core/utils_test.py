# -*- coding: utf-8 -*-

import unittest
from wolfox.fengine.core.base import CommonObject
from wolfox.fengine.core.utils import *

class ModuleTest(unittest.TestCase):
    def test_fcustom(self):
        def x1(a,b):pass
        cx0 = fcustom(x1)   #Æ«º¯ÊýÆ«ÖÃ
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


if __name__ == "__main__":
    unittest.main()
