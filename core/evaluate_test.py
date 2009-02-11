# -*- coding: utf-8 -*-

import unittest
from wolfox.fengine.base.common import Quote,Trade,Evaluation
from wolfox.fengine.core.pmanager import AdvancedPositionManager,DateManager
from wolfox.fengine.core.base import BaseObject
from wolfox.fengine.core.evaluate import *

class ModuleTest(unittest.TestCase):
    def test_evaluate(self):    #只测试通路
        evaluate([])
        self.assertTrue(True)
    
    def test_DEFAULT_EVALUATE_FILTER(self):
        #空测试
        self.assertEquals([],DEFAULT_EVALUATE_FILTER([]))        
        #正常测试
        mnt1 = [1,2,3]
        mnt2 = [10,20,30]
        filtered = DEFAULT_EVALUATE_FILTER([mnt1,mnt2])
        self.assertEquals([1,2,3,10,20,30],filtered)

    def test_gevaluate(self):
        trade1 = Trade(1,20050101,1000,1)
        trade2 = Trade(1,20050101,1100,-1)
        trade3 = Trade(2,20050501,1000,1)
        trade4 = Trade(2,20050501,1100,-1)
        #trade5 = Trade(3,20050501,1100,1)        
        nt1 = BaseObject(name='test1',evaluation=Evaluation([]),trades=[[trade1,trade2]])
        nt2 = BaseObject(name='test1',evaluation=Evaluation([]),trades=[[trade3,trade4]])
        #nt3 = BaseObject(name='test1',evaluation=Evaluation([]),trades=[trade5])
        ev = gevaluate([nt1,nt2])
        self.assertEquals([[trade1,trade2],[trade3,trade4]],ev.matchedtrades)
        self.assertEquals(nt1,trade1.parent)
        self.assertEquals(nt1,trade2.parent)
        self.assertEquals(nt2,trade3.parent)
        self.assertEquals(nt2,trade4.parent)

    def test_evaluate_all(self):    #只测试通路
        trade1 = Trade(1,20050101,1000,1)
        trade2 = Trade(1,20050101,1100,-1)
        pman = AdvancedPositionManager()
        dm = DateManager(20050101,20050401)        
        rev,srev = evaluate_all([[trade1,trade2]],pman,dm)
        self.assertTrue(rev)
        self.assertTrue(srev)
        self.assertTrue(rev.pre_ev)
        self.assertTrue(rev.g_ev)
        

if __name__ == "__main__":
    import logging
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    unittest.main()
