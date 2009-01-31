# -*- coding: utf-8 -*-

import unittest
from wolfox.fengine.core.base import CommonObject
from wolfox.fengine.core.shortcut import *

class ModuleTest(unittest.TestCase):    #∂º «Õ®¬∑≤‚ ‘
    def test_normal_template(self):
        a = np.array([(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(13,14)])
        b = np.array([(11,12),(13,14),(15,16),(17,18),(19,110),(111,112),(113,114)])
        sa = CommonObject(id=3,transaction=a)
        sb = CommonObject(id=3,transaction=b)
        dates = np.array([1,2])
        sdata = {'sa':sa,'sb':sb}
        fbuy = lambda x:np.array([1,0])
        fsell = lambda x,y:np.array([0,1])
        ftrade = lambda x,y,z,a:(1,2)
        normal_template(sdata,dates,fbuy,fsell,ftrade)

    def test_csc_func(self):
        a = np.array([(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(13,14)])
        sa = CommonObject(id=3,transaction=a)
        bs = np.array([0,1])
        csc_func(sa,bs)
        self.assertTrue(True)
        #ø’≤‚ ‘
        a = np.array([(),(),(),(),(),(),()])
        sa = CommonObject(id=3,transaction=a)
        bs = np.array([])
        csc_func(sa,bs)
        self.assertTrue(True)


    def test_normal_trade_func(self):
        a = np.array([(1,2,1),(3,4,3),(5,6,5),(7,8,7),(9,10,4),(11,12,3),(13,14,5)])      
        sa = CommonObject(id=3,transaction=a)        
        dates = np.array([1,2,3])
        sb = np.array([0,1,0])
        ss = np.array([0,0,1])
        normal_trade_func(dates,sa,sb,ss)
        self.assertTrue(True)
        #ø’≤‚ ‘
        a = np.array([(),(),(),(),(),(),()])        
        sa = CommonObject(id=3,transaction=a)        
        dates = np.array([])
        sb = np.array([])
        ss = np.array([])
        normal_trade_func(dates,sa,sb,ss)
        self.assertTrue(True)
        
    def test_ppsort(self):
        a = np.array([(5,4,7),(3,2,8),(8,5,3),(4,4,4)])
        sa = ppsort(a)
        self.assertTrue(True)
        #ø’≤‚ ‘
        a = np.array([(),(),(),(),(),(),()])        
        sa = ppsort(a)
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
