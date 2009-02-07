# -*- coding: utf-8 -*-

import numpy as np
import logging
import unittest
from wolfox.fengine.core.mediator import *
from wolfox.fengine.core.base import CommonObject

logger = logging.getLogger('wolfox.fengine.core.mediator_test')

class ModuleTest(unittest.TestCase):
    pass


class MediatorTest(unittest.TestCase):
    def test_init(self):
        fbuy = lambda x:np.array([1,0])
        fsell = lambda x,y:np.array([0,1])
        m = Mediator(fbuy,fsell)
        self.assertTrue(True)

    def test_name(self):
        fbuy = lambda x:np.array([1,0])
        fsell = lambda x,y:np.array([0,1])
        m = Mediator(fbuy,fsell)
        name = m.name()
        logger.debug('mediator name:%s',name)
        self.assertTrue(True)

    def test__calc(self):
        a = np.array([(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(13,14)])
        b = np.array([(11,12),(13,14),(15,16),(17,18),(19,110),(111,112),(113,114)])
        sa = CommonObject(id=3,code='test1',transaction=a)
        sb = CommonObject(id=3,code='test2',transaction=b)
        dates = np.array([1,2])
        sdata = {'sa':sa,'sb':sb}
        fbuy = lambda x:np.array([1,0])
        fsell = lambda x,y:np.array([0,1])
        ftrade = lambda x,y,z,a,c,begin:(1,2)
        m = Mediator(fbuy,fsell)
        m._calc(ftrade,sdata,dates)
        self.assertTrue(True)
        #测试异常包容性
        def fbuy(x): raise Exception('test exception catch')
        me = Mediator(fbuy,fsell)
        me._calc(ftrade,sdata,dates)
        self.assertTrue(True)    

    def test_calc(self):
        a = np.array([(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(13,14)])
        b = np.array([(11,12),(13,14),(15,16),(17,18),(19,110),(111,112),(113,114)])
        sa = CommonObject(id=3,code='test1',transaction=a)
        sb = CommonObject(id=3,code='test2',transaction=b)
        dates = np.array([1,2])
        sdata = {'sa':sa,'sb':sb}
        fbuy = lambda x:np.array([1,0])
        fsell = lambda x,y:np.array([0,1])
        m = Mediator(fbuy,fsell)
        m.calc(sdata,dates)
        self.assertTrue(True)
        
    def test_calc_last(self):
        a = np.array([(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(13,14)])
        b = np.array([(11,12),(13,14),(15,16),(17,18),(19,110),(111,112),(113,114)])
        sa = CommonObject(id=3,code='test1',transaction=a)
        sb = CommonObject(id=3,code='test2',transaction=b)
        dates = np.array([1,2])
        sdata = {'sa':sa,'sb':sb}
        fbuy = lambda x:np.array([1,0])
        fsell = lambda x,y:np.array([0,1])
        m = Mediator(fbuy,fsell)
        m.calc_last(sdata,dates)
        self.assertTrue(True)


if __name__ == "__main__":
    import logging
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    unittest.main()
