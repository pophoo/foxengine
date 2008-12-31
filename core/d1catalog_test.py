# -*- coding: utf-8 -*-

import unittest
from wolfox.fengine.core.d1catalog import *

class ModuleTest(unittest.TestCase):
    def test_calc_index_adjacent(self):
        a = np.array([(0,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(1000,1000,1000,1000)])
        b = np.array([(0,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,2000,1000)])
        c = np.array([(0,0,0,0),(700,700,300,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(1000,0,1000,1000)])
        qa = np.array([a,b,c])
        index,orders = calc_index_adjacent(qa)
        self.assertEquals([1000, 800, 886, 1132],index.tolist())
    
    def test_calc_index_base0(self):
        a = np.array([(0,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(1000,1000,1000,1000)])
        b = np.array([(0,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,2000,1000)])
        c = np.array([(0,0,0,0),(700,700,300,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(1000,0,1000,1000)])
        qa = np.array([a,b,c])
        index,orders = calc_index_base0(qa)
        self.assertEquals([1000, 800, 1007, 1124],index.tolist())
        #不动点
        index_old,orders_old = calc_index_base0_old(qa)
        self.assertEquals(index.tolist(),index_old.tolist())
        #print index

    def test_calc_index(self):
        a = np.array([(0,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(5000,4000,8000,4000),(1000,1000,1000,1000)])
        b = np.array([(0,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,4000,4000),(0,0,2000,1000)])
        c = np.array([(0,0,0,0),(700,500,500,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(7000,5000,0,4000),(1000,1000,0,1000)])
        qa = np.array([a,b,c])
        index,orders = calc_index(qa,alen=3)
        self.assertEquals([1000,767,1173,1067],index.tolist())
        index,orders = calc_index(qa,alen=2)
        self.assertEquals([1000,767,1204,1067],index.tolist())
        #print index

    def test_avg_price(self):
        a = np.array([(0,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(5000,4000,8000,4000),(1000,1000,1000,1000)])
        b = np.array([(0,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,4000,4000),(0,0,2000,1000)])
        c = np.array([(0,0,0,0),(700,700,300,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(7000,0,3000,4000),(1000,0,1000,1000)])
        qa = np.array([a,b,c])
        avg = avg_price(qa)
        self.assertEquals([600,400,375,400],avg.tolist())


if __name__ == "__main__":
    unittest.main()
