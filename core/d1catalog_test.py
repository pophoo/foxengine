# -*- coding: utf-8 -*-

import unittest
from wolfox.fengine.core.base import *
from wolfox.fengine.core.d1catalog import *


class ModuleTest(unittest.TestCase):
    def test_calc_index(self):
        a = np.array([(0,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(5000,4000,8000,4000),(1000,1000,1000,1000)])
        b = np.array([(0,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,4000,4000),(0,0,2000,1000)])
        c = np.array([(0,0,0,0),(700,500,500,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(7000,5000,0,4000),(1000,1000,0,1000)])
        sa = CommonObject(id=0,transaction=a)
        sb = CommonObject(id=1,transaction=b)
        sc = CommonObject(id=2,transaction=c) 
        ss = [sa,sb,sc]
        index = calc_index(ss,alen=3)
        self.assertEquals([1000,767,1173,1067],index.tolist())
        index = calc_index(ss,alen=2)
        self.assertEquals([1000,767,1204,1067],index.tolist())
        #print index

    def test_avg_price(self):
        a = np.array([(0,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(5000,4000,8000,4000),(1000,1000,1000,1000)])
        b = np.array([(0,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,4000,4000),(0,0,2000,1000)])
        c = np.array([(0,0,0,0),(700,700,300,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(7000,0,3000,4000),(1000,0,1000,1000)])
        sa = CommonObject(id=0,transaction=a)
        sb = CommonObject(id=1,transaction=b)
        sc = CommonObject(id=2,transaction=c) 
        avg = avg_price([sa,sb,sc])
        self.assertEquals([600,400,375,400],avg.tolist())

    def test_calc_drate(self):
        a = np.array([(0,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(5000,4000,8000,4000),(1000,1000,1000,1000)])
        b = np.array([(0,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,4000,4000),(0,0,2000,1000)])
        c = np.array([(0,0,0,0),(700,500,500,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(7000,5000,0,4000),(1000,1000,0,1000)])
        d = np.array([(0,0,0,0),(600,600,500,600),(0,0,0,0),(0,0,0,0),(0,0,0,0),(6000,6000,6000,6000),(1000,1000,1000,1000)])        
        sa = CommonObject(id=0,transaction=a)
        sb = CommonObject(id=1,transaction=b)
        sc = CommonObject(id=2,transaction=c) 
        sd = CommonObject(id=3,transaction=d)
        rate = calc_drate([sa,sb,sc,sd],distance=2,wave=4)
        self.assertEquals([[0, 1, 3, 1], [1, 2, 2, 3], [2, 0, 0, 0], [3, 3, 1, 2]],rate.tolist())
        rate = calc_drate([sa,sb,sc,sd])
        self.assertEquals([[0, 25, 75, 0], [25, 50, 25, 75], [50, 0, 50, 25], [75, 75, 0, 50]],rate.tolist())

    #deprecated
    def test_calc_index_adjacent(self):
        a = np.array([(0,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(1000,1000,1000,1000)])
        b = np.array([(0,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,2000,1000)])
        c = np.array([(0,0,0,0),(700,700,300,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(1000,0,1000,1000)])
        sa = CommonObject(id=0,transaction=a)
        sb = CommonObject(id=1,transaction=b)
        sc = CommonObject(id=2,transaction=c) 
        ss = [sa,sb,sc]
        index = calc_index_adjacent(ss)
        self.assertEquals([1000, 800, 886, 1132],index.tolist())
    
    #deprecated
    def test_calc_index_base0_and_old(self):
        a = np.array([(0,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(1000,1000,1000,1000)])
        b = np.array([(0,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,2000,1000)])
        c = np.array([(0,0,0,0),(700,700,300,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(1000,0,1000,1000)])
        sa = CommonObject(id=0,transaction=a)
        sb = CommonObject(id=1,transaction=b)
        sc = CommonObject(id=2,transaction=c) 
        ss = [sa,sb,sc]
        index = calc_index_base0(ss)
        self.assertEquals([1000, 800, 1007, 1124],index.tolist())
        #不动点
        index_old = calc_index_base0_old(ss)
        self.assertEquals(index.tolist(),index_old.tolist())
        #print index


if __name__ == "__main__":
    unittest.main()
