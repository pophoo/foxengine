# -*- coding: utf-8 -*-

import numpy as np
import logging
import unittest
from wolfox.fengine.core.mediator import *
from wolfox.fengine.core.base import CommonObject,BaseObject

logger = logging.getLogger('wolfox.fengine.core.mediator_test')

class ModuleTest(unittest.TestCase):
    def test_pricers(self):
        s = BaseObject(transaction=np.array([[1],[2],[3],[4],[5],[6],[7]]),down_limit=np.array([8]))
        self.assertEquals([2],cl_pricer[0](s).tolist())
        self.assertEquals([8],cl_pricer[1](s).tolist())
        self.assertEquals([1],ol_pricer[0](s).tolist())
        self.assertEquals([8],ol_pricer[1](s).tolist())
        self.assertEquals([1],oo_pricer[0](s).tolist())
        self.assertEquals([1],oo_pricer[1](s).tolist())
        self.assertEquals([2],co_pricer[0](s).tolist())
        self.assertEquals([1],co_pricer[1](s).tolist())
    
    def test_Mediator10_init(self):
        Mediator10(np.array([1,0,0,1]),np.array([0,0,1,0]))
        self.assertTrue(True)
    
    def test_CMediator10_init(self):
        CMediator10(np.array([1,0,0,1]),np.array([0,0,1,0]))
        self.assertTrue(True)

    def test_OMediator10_init(self):
        OMediator10(np.array([1,0,0,1]),np.array([0,0,1,0]))
        self.assertTrue(True)

    def test_mediator_factory(self):
        mediator1 = mediator_factory()(np.array([1,0,0,1]),np.array([0,0,1,0]))
        mediator2 = mediator_factory(trade_strategy=B1S1,pricer = oo_pricer)(np.array([1,0,0,1]),np.array([0,0,1,0]))
        self.assertTrue(True)


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
        #空测试
        m.calc_matched({},np.array([]))
        self.assertTrue(True)

    def test_calc_matched(self):
        a = np.array([(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(13,14)])
        b = np.array([(11,12),(13,14),(15,16),(17,18),(19,110),(111,112),(113,114)])
        sa = CommonObject(id=3,code='test1',transaction=a)
        sb = CommonObject(id=3,code='test2',transaction=b)
        dates = np.array([1,2])
        sdata = {'sa':sa,'sb':sb}
        fbuy = lambda x:np.array([1,0])
        fsell = lambda x,y:np.array([0,1])
        m = Mediator(fbuy,fsell)
        m.calc_matched(sdata,dates)
        self.assertTrue(True)
        #空测试
        m.calc_matched({},np.array([]))
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
        #空测试
        m.calc_matched({},np.array([]))
        self.assertTrue(True)

    def test_prepare(self):
        a = np.array([(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(13,14)])
        sa = CommonObject(id=3,code='test1',transaction=a)
        fbuy = lambda x:np.array([1,0])
        fsell = lambda x,y:np.array([0,1])
        m = Mediator(fbuy,fsell)
        m.prepare(sa)
        self.assertEquals(2,len(sa.atr))


if __name__ == "__main__":
    import logging
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    unittest.main()
