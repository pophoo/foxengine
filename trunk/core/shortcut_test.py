# -*- coding: utf-8 -*-

import sys
import unittest
from wolfox.fengine.core.base import CommonObject
from wolfox.fengine.core.shortcut import *

class ModuleTest(unittest.TestCase):    #只测试通道
    def setUp(self):
        from StringIO import StringIO
        self.tmp = sys.stdout
        sys.stdout = StringIO()  #将标准I/O流重定向到buff对象，抑制输出

    def tearDown(self):
        sout = sys.stdout.getvalue()
        logger.debug(u'测试输出:%s',sout)
        sys.stdout = self.tmp        #恢复标准I/O流
        #print sout    

    def test_normal_calc_template(self):
        a = np.array([(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(13,14)])
        b = np.array([(11,12),(13,14),(15,16),(17,18),(19,110),(111,112),(113,114)])
        sa = CommonObject(id=3,code='test1',transaction=a)
        sb = CommonObject(id=3,code='test2',transaction=b)
        dates = np.array([1,2])
        sdata = {'sa':sa,'sb':sb}
        fbuy = lambda x:np.array([1,0])
        fsell = lambda x,y:np.array([0,1])
        ftrade = lambda x,y,z,a:(1,2)
        normal_calc_template(sdata,dates,fbuy,fsell,ftrade)
        self.assertTrue(True)
        #测试异常包容性
        def fbuy(x): raise Exception
        normal_calc_template(sdata,dates,fbuy,fsell,ftrade)
        self.assertTrue(True)

    def test_csc_func(self):
        a = np.array([(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(13,14)])
        sa = CommonObject(id=3,transaction=a)
        bs = np.array([0,1])
        csc_func(sa,bs)
        self.assertTrue(True)
        #空测试
        a = np.array([(),(),(),(),(),(),()])
        sa = CommonObject(id=3,transaction=a)
        bs = np.array([])
        csc_func(sa,bs)
        self.assertTrue(True)

    def test_trade_func(self):
        from wolfox.fengine.core.shortcut import _trade_func
        a = np.array([(1,2,1),(3,4,3),(5,6,5),(7,8,7),(9,10,4),(11,12,3),(13,14,5)])      
        sa = CommonObject(id=3,code='TEST',transaction=a)        
        dates = np.array([1,2,3])
        sb = np.array([0,1,0])
        ss = np.array([0,0,1])
        _trade_func(dates,sa,sb,ss,prepare_func=B0S0)
        self.assertTrue(True)
        #空测试
        a = np.array([(),(),(),(),(),(),()])        
        sa = CommonObject(id=3,code='TEST',transaction=a)        
        dates = np.array([])
        sb = np.array([])
        ss = np.array([])
        _trade_func(dates,sa,sb,ss,prepare_func=B0S0)
        self.assertTrue(True)
 
    def test_normal_trade_func(self):   #只测试通路
        a = np.array([(1,2,1),(3,4,3),(5,6,5),(7,8,7),(9,10,4),(11,12,3),(13,14,5)])      
        sa = CommonObject(id=3,code='TEST',transaction=a)        
        dates = np.array([1,2,3])
        sb = np.array([0,1,0])
        ss = np.array([0,0,1])
        normal_trade_func(dates,sa,sb,ss)
        self.assertTrue(True)

    def test_trade_funcs(self):   #测试全部bMsN_trade_func,只测试通路
        a = np.array([(1,2,1),(3,4,3),(5,6,5),(7,8,7),(9,10,4),(11,12,3),(13,14,5)])      
        sa = CommonObject(id=3,code='TEST',transaction=a)
        dates = np.array([1,2,3])
        sb = np.array([0,1,0])
        ss = np.array([0,0,1])
        dummy_trade_func(dates,sa,sb,ss)
        b0s0_trade_func(dates,sa,sb,ss)
        b0s1_trade_func(dates,sa,sb,ss)
        b1s0_trade_func(dates,sa,sb,ss)
        b1s1_trade_func(dates,sa,sb,ss)
        self.assertTrue(True)

    def test_ppsort(self):
        a = np.array([(5,4,7),(3,2,8),(8,5,3),(4,4,4)])
        sa = ppsort(a)
        self.assertTrue(True)
        #空测试
        a = np.array([(),(),(),(),(),(),()])        
        sa = ppsort(a)
        self.assertTrue(True)

    def test_create_evaluator(self): #只测试通路
        evf = create_evaluator()
        evf([])
        self.assertTrue(True)
        

if __name__ == "__main__":
    import logging
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    unittest.main()
