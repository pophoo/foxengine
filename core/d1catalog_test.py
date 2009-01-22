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

    def test_dispatch_example(self):
        a = np.array([(1,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(5000,4000,8000,4000),(1000,1000,1000,1000)])
        b = np.array([(2,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,4000,4000),(0,0,2000,1000)])
        s1 = CommonObject(id=3,transaction=a)
        s2 = CommonObject(id=4,transaction=b)
        rev = dispatch_example('test',[s1,s2],100)
        self.assertEquals(a[CLOSE].tolist(),s1.test.tolist())
        self.assertEquals(b[CLOSE].tolist(),s2.test.tolist())
        self.assertEquals(rev[0].tolist(),s1.test.tolist())
        self.assertEquals(rev[1].tolist(),s2.test.tolist())        
        #测试空数据
        na = np.array([])
        ns1 = CommonObject(id=5,transaction=na)
        nrev = dispatch_example('test',[ns1,ns1],100)
        self.assertEquals([],ns1.test.tolist())
        self.assertEquals(nrev[0].tolist(),ns1.test.tolist())
        self.assertFalse(nrev[0].tolist())
        #完全的空，测试通路
        nrev2 = dispatch_example('test',[],100)
        self.assertFalse(nrev2)

    def test_dispatch(self):
        f = lambda stocks,ma=10:extract_collect(stocks)
        df = dispatch(f)
        a = np.array([(1,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(5000,4000,8000,4000),(1000,1000,1000,1000)])
        b = np.array([(2,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,4000,4000),(0,0,2000,1000)])
        s1 = CommonObject(id=3,transaction=a)
        s2 = CommonObject(id=4,transaction=b)
        df('test',[s1,s2],100)
        self.assertEquals(a[CLOSE].tolist(),s1.test.tolist())
        self.assertEquals(b[CLOSE].tolist(),s2.test.tolist())

    def test_cdispatch(self):
        f = lambda stocks,ma=10:extract_collect(stocks)
        #f = lambda stocks,ma=10:(np.array([1,2,3,4]),np.array([5,6,7,8]))
        df = cdispatch(f)
        a = np.array([(1,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(5000,4000,8000,4000),(1000,1000,1000,1000)])
        b = np.array([(2,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,4000,4000),(0,0,2000,1000)])
        s1 = CommonObject(id=3,transaction=a)
        s2 = CommonObject(id=4,transaction=b)
        catalog = CommonObject(id=15,stocks=[s1,s2])
        df('test',[catalog],100)
        #print s1.test[catalog]
        self.assertEquals([500,400,800,400],s1.test[catalog].tolist())
        self.assertEquals([200,200,200,400],s2.test[catalog].tolist())
        c = np.array([(1,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(5000,4000,8000,4000),(1000,1000,1000,1000)])
        d = np.array([(2,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,4000,4000),(0,0,2000,1000)])
        s3 = CommonObject(id=4,transaction=c)
        s4 = CommonObject(id=5,transaction=d)
        catalog2 = CommonObject(id=16,stocks=[s3,s4])
        df('test2',[catalog,catalog2],100)        
        self.assertEquals([500,400,800,400],s1.test2[catalog].tolist())
        self.assertEquals([200,200,200,400],s2.test2[catalog].tolist())
        self.assertEquals([500,400,800,400],s3.test2[catalog2].tolist())
        self.assertEquals([200,200,200,400],s4.test2[catalog2].tolist())
        #测试空数据
        na = np.array([[],[],[],[],[],[],[]])
        ns1 = CommonObject(id=51,transaction=na)
        ns2 = CommonObject(id=52,transaction=na)        
        catalog3 = CommonObject(id=16,stocks=[ns1,ns2])
        catalog4 = CommonObject(id=17,stocks=[ns1,ns2])        
        df('test2',[catalog3,catalog4],100)
        self.assertEquals([],ns1.test2[catalog3].tolist())
        #完全的空，测试通路
        nrev2 = df('test3',[],100)
        self.assertFalse(nrev2)

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
