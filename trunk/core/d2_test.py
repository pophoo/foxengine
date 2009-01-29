# -*- coding: utf-8 -*-

import unittest
from wolfox.fengine.core.base import *
from wolfox.fengine.core.source import extract_collect
from wolfox.fengine.core.d2 import *
from wolfox.fengine.core.d1catalog import CLOSE

class ModuleTest(unittest.TestCase):
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
        na = np.array([[],[],[],[],[],[],[]])
        ns1 = CommonObject(id=5,transaction=na)
        nrev = dispatch_example('test',[ns1,ns1],100)
        self.assertEquals([],ns1.test.tolist())
        self.assertEquals(nrev[0].tolist(),ns1.test.tolist())
        self.assertFalse(nrev[0].tolist())
        #完全的空，测试通路
        nrev2 = dispatch_example('test',[],100)
        self.assertFalse(nrev2)

    def test_dispatch(self):
        f = lambda sdatas,ma=10:sdatas
        df = dispatch(f)
        a = np.array([(1,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(5000,4000,8000,4000),(1000,1000,1000,1000)])
        b = np.array([(2,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,4000,4000),(0,0,2000,1000)])
        s1 = CommonObject(id=3,transaction=a)
        s2 = CommonObject(id=4,transaction=b)
        df('test',[s1,s2],100)
        self.assertEquals(a[CLOSE].tolist(),s1.test.tolist())
        self.assertEquals(b[CLOSE].tolist(),s2.test.tolist())

    def test_cdispatch(self):
        f = lambda sdatas,ma=10:sdatas
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
    
    def test_roll02(self):
        #d1.roll02
        self.assertEquals([1,2,3,4,5],roll02(np.array([1,2,3,4,5]),0).tolist())
        self.assertEquals([0,0,1,2,3],roll02(np.array([1,2,3,4,5]),2).tolist())
        self.assertEquals([0,0,0,0,0],roll02(np.array([1,2,3,4,5]),5).tolist())
        self.assertEquals([0,0,0,0,0],roll02(np.array([1,2,3,4,5]),8).tolist())
        self.assertEquals([3,4,5,0,0],roll02(np.array([1,2,3,4,5]),-2).tolist())        
        self.assertEquals([2,3,4,5,0],roll02(np.array([1,2,3,4,5]),-1).tolist())
        self.assertEquals([0,0,0,0,0],roll02(np.array([1,2,3,4,5]),-6).tolist())        
        #二维
        self.assertEquals([[1,2,3],[4,5,6]],roll02(np.array([(1,2,3),(4,5,6)]),0).tolist())
        self.assertEquals([[0,1,2],[0,4,5]],roll02(np.array([(1,2,3),(4,5,6)]),1).tolist())
        self.assertEquals([[0,0,0],[0,0,0]],roll02(np.array([(1,2,3),(4,5,6)]),4).tolist())
        self.assertEquals([[2,3,0],[5,6,0]],roll02(np.array([(1,2,3),(4,5,6)]),-1).tolist())
        self.assertEquals([[0,0,0],[0,0,0]],roll02(np.array([(1,2,3),(4,5,6)]),-4).tolist())

    def test_rolln2(self):
        #d1.rolln2
        self.assertEquals([1,2,3,4,5],rolln2(np.array([1,2,3,4,5]),0).tolist())
        self.assertEquals([1,1,1,2,3],rolln2(np.array([1,2,3,4,5]),2).tolist())
        self.assertEquals([1,1,1,1,1],rolln2(np.array([1,2,3,4,5]),5).tolist())
        self.assertEquals([1,1,1,1,1],rolln2(np.array([1,2,3,4,5]),8).tolist())
        self.assertEquals([3,4,5,5,5],rolln2(np.array([1,2,3,4,5]),-2).tolist())        
        self.assertEquals([2,3,4,5,5],rolln2(np.array([1,2,3,4,5]),-1).tolist())
        self.assertEquals([5,5,5,5,5],rolln2(np.array([1,2,3,4,5]),-6).tolist())        
        #二维
        self.assertEquals([[1,2,3],[4,5,6]],rolln2(np.array([(1,2,3),(4,5,6)]),0).tolist())
        self.assertEquals([[1,1,2],[4,4,5]],rolln2(np.array([(1,2,3),(4,5,6)]),1).tolist())
        self.assertEquals([[1,1,1],[4,4,4]],rolln2(np.array([(1,2,3),(4,5,6)]),4).tolist())
        self.assertEquals([[2,3,3],[5,6,6]],rolln2(np.array([(1,2,3),(4,5,6)]),-1).tolist())
        self.assertEquals([[3,3,3],[6,6,6]],rolln2(np.array([(1,2,3),(4,5,6)]),-4).tolist())


    def test_nsubd2(self):
        a = np.array([[1,2,3],[4,5,6]])
        self.assertEquals([[1,1,1],[4,1,1]],nsubd2(a).tolist())
        self.assertEquals([[1,2,2],[4,5,2]],nsubd2(a,2).tolist())

    def test_posort(self):
        a = np.array([(5,4,7),(3,2,8),(8,5,3),(4,4,4)])
        sa = posort(a)
        self.assertEquals([[2,1,2],[0,0,3],[3,3,0],[1,2,1]],sa.tolist())

    def test_inverse_posort(self):
        a = np.array([(5,4,7),(3,2,8),(8,5,3),(4,4,4)])
        sa = inverse_posort(a)
        self.assertEquals([[1,2,1],[3,3,0],[0,0,3],[2,1,2]],sa.tolist())

    def test_percent_sort(self):
        a = np.array([(5,4,7),(3,2,8),(8,5,3),(4,4,4)])
        sa = percent_sort(a)
        self.assertEquals([[5000,2500,5000],[0,0,7500],[7500,7500,0],[2500,5000,2500]],sa.tolist())
    
    def test_inverse_percent_sort(self):
        a = np.array([(5,4,7),(3,2,8),(8,5,3),(4,4,4)])
        sa = inverse_percent_sort(a)
        self.assertEquals([[2500,5000,2500],[7500,7500,0],[0,0,7500],[5000,2500,5000]],sa.tolist())

    def test_increase(self):
        a = np.array([(5,4,7),(3,2,8),(8,5,3),(4,4,4)])
        ia = increase(a)
        self.assertEquals([[0,-2000,7500],[0,-3334,30000],[0,-3750,-4000],[0,0,0]],ia.tolist())
        ib = increase(a,2)
        self.assertEquals([[0,0,4000],[0,0,16666],[0,0,-6250],[0,0,0]],ib.tolist())

    def test_nincrease(self):
        a = np.array([(5,4,7),(3,2,8),(8,5,3),(4,4,4)])
        ia = nincrease(a)
        self.assertEquals([[0,-2000,7500],[0,-3334,30000],[0,-3750,-4000],[0,0,0]],ia.tolist())
        ib = nincrease(a,2)
        self.assertEquals([[0,-2000,4000],[0,-3334,16666],[0,-3750,-6250],[0,0,0]],ib.tolist())

    def test_percent(self):
        a = np.array([(5,4,7),(3,2,8),(8,5,3),(4,4,4)])
        ia = percent(a)
        self.assertEquals([[0,8000,17500],[0,6666,40000],[0,6250,6000],[0,10000,10000]],ia.tolist())
        ib = percent(a,2)
        self.assertEquals([[0,0,14000],[0,0,26666],[0,0,3750],[0,0,10000]],ib.tolist())

    def test_npercent(self):
        a = np.array([(5,4,7),(3,2,8),(8,5,3),(4,4,4)])
        ia = npercent(a)
        self.assertEquals([[10000,8000,17500],[10000,6666,40000],[10000,6250,6000],[10000,10000,10000]],ia.tolist())
        ib = npercent(a,2)
        self.assertEquals([[10000,8000,14000],[10000,6666,26666],[10000,6250,3750],[10000,10000,10000]],ib.tolist())

    def test_cmp_percent(self):
        a = np.array([(5,4,7),(3,2,8),(8,5,3),(4,4,4)])
        ia = cmp_percent(a)
        self.assertEquals([[10000,8000,14000],[10000,6666,26666],[10000,6250,3750],[10000,10000,10000]],ia.tolist())

    def test_increase_percent(self):    #不动点
        a = np.array([(5,4,7),(3,2,8),(8,5,3),(4,4,4)])
        ia = percent(a)
        ib = increase(a)+PERCENT_BASE
        ib[:,0] = 0 #第一列也加上了PERCENT_BASE
        self.assertEquals(ib.tolist(),ia.tolist())

    def test_increase_cmp_percent(self):    #不动点2
        a = np.array([(5,4,7),(3,2,8),(8,5,3),(4,4,4)])
        ia = cmp_percent(a)
        ib = increase(a)*1.0/PERCENT_BASE+1
        ibc = np.cast['int'](ib.cumprod(1) * PERCENT_BASE)
        #self.assertEquals(ibc.tolist(),ia.tolist())    #因为有浮点精度损失，在整数转换后不能完全相等
        self.assertEquals(ibc.tolist()[0],ia.tolist()[0])
        #self.assertEquals(ibc.tolist()[1],ia.tolist()[1])   #因为有浮点精度损失，此列有一个数有万分之一的误差
        self.assertEquals(ibc.tolist()[2],ia.tolist()[2])
        self.assertEquals(ibc.tolist()[3],ia.tolist()[3])         
        self.assertTrue(True)

    def test_ma2d(self):
        a= np.array([(1,2,3,4,5,6,7,8,9,0),(0,9,8,7,6,5,4,3,2,1)])
        av = ma2d(a,3)
        self.assertEquals([[0, 0, 2, 3, 4, 5, 6, 7, 8, 6],[0, 0, 6, 8, 7, 6, 5, 4, 3, 2]],av.tolist())

    def test_ma2d_fixure(self):  #ma2的不动点
        a= np.array([(1,2,3,4,5,6,7,8,9,0),(0,9,8,7,6,5,4,3,2,1)])
        av = ma2d(a,3)
        bv = ma2(a,3)
        cv = [r.tolist() for r in ma2a(a,3)]
        self.assertEquals(bv.tolist(),av.tolist())
        self.assertEquals(cv,av.tolist())
        
    def test_nma2d(self):
        a= np.array([(1,2,3,4,5,6,7,8,9,0),(0,9,8,7,6,5,4,3,2,1)])
        av = nma2d(a,3)
        self.assertEquals([[1, 2, 2, 3, 4, 5, 6, 7, 8, 6],[0, 5, 6, 8, 7, 6, 5, 4, 3, 2]],av.tolist())

    def test_nma2d_fixure(self):  #nma2的不动点
        a= np.array([(1,2,3,4,5,6,7,8,9,0),(0,9,8,7,6,5,4,3,2,1)])
        av = nma2d(a,3)
        bv = nma2(a,3)
        self.assertEquals(bv.tolist(),av.tolist())


if __name__ == "__main__":
    unittest.main()

