# -*- coding: utf-8 -*-

import unittest
from wolfox.fengine.core.d1ex import * 

class ModuleTest(unittest.TestCase):
    def test_ma(self):
        self.assertEquals([],ma([],3).tolist())
        a= np.array([1,2,3,4,5,6,7,8,9,0])
        av = ma(a,3)
        self.assertEquals([0, 0, 2, 3, 4, 5, 6, 7, 8, 6],av.tolist())

    def test_nma(self):
        self.assertEquals([],nma([],3).tolist())
        a= np.array([1,2,3,4,5,6,7,8,9,0])
        av = nma(a,3)
        self.assertEquals([1, 2, 2, 3, 4, 5, 6, 7, 8, 6],av.tolist())

    def test_fma(self):
        self.assertEquals([],fma([],3).tolist())   
        a= np.array([1,2,3,4,5,6,7,8,9,0])
        av = fma(a,3)
        self.assertEquals([0, 0, 2, 3, 4, 5, 6, 7, 8, 17/3.0],av.tolist())

    def test_fnma(self):
        self.assertEquals([],fnma([],3).tolist())    
        a= np.array([1,2,3,4,5,6,7,8,9,0])
        av = fnma(a,3)
        self.assertEquals([1, 1.5, 2, 3, 4, 5, 6, 7, 8, 17/3.0],av.tolist())

    def test_trend(self):
        a = np.array([1,2,3,2,2,10,2,10,10,4])
        self.assertEquals([0,1,1,-1,0,1,-1,1,0,-1],trend(a).tolist())
        self.assertEquals([0,0,0,0,0,0,0,0,0,0],trend(a,0).tolist())
        self.assertEquals([0,0,1,0,-1,1,0,0,1,-1],trend(a,2).tolist())

    def test_strend(self):
        source = np.array([10,20,30,30,40,50,40,30,20,20,10,20])
        self.assertEquals([0,1,2,2,3,4,-1,-2,-3,-3,-4,1],strend(source).tolist())

    def test_strend2(self):
        source = np.array([10,20,30,30,40,50,40,30,20,20,10,20])
        self.assertEquals([0,1,2,3,4,5,-1,-2,-3,-4,-5,1],strend2(source).tolist())

    def test_rturn(self):
        self.assertEquals(0,rturn(np.array([])))
        self.assertEquals(0,rturn(np.array([0,1,2,3,4,5,6])))
        self.assertEquals(2,rturn(np.array([0,1,2,-1,4,5,6])))
        self.assertEquals(3,rturn(np.array([0,1,2,-1,4,5,-1])))
        self.assertEquals(4,rturn(np.array([0,1,2,-1,4,-2,6])))

    def test_cross(self):
        target = np.array([10,20,30,40,50,40,30,20,10,12,11,12])
        follow = np.array([5,15,35,41,60,50,25,26,8,12,13,12])
        self.assertEquals([0,0,1,0,0,0,-1,1,-1,0,1,0],cross(target,follow).tolist())
        #空测试
        cross(np.array([]),np.array([]))
        self.assertTrue(True)

    def test_under_cross(self):
        target = np.array([10,20,30,40,50,40,30,20,10,12,11,12])
        follow = np.array([5,15,35,41,60,50,25,26,8,12,13,12])
        self.assertEquals([1,1,0,0,0,0,1,0,1,1,0,0],under_cross(np.array([1,1,1,0,0,0,0,0,0,1,1,0]),target,follow).tolist())
        #空测试
        cross(np.array([]),np.array([]))
        self.assertTrue(True)

    def test_scover(self):
        source = np.array([0,0,5,0,-5,0,0,0,0,0,1,0,0,3,0,0,-1,1,2,0,0,0,0,6,0])
        self.assertEquals([],scover(np.array([])).tolist())
        self.assertEquals([],scover(np.array([]),2).tolist())        
        self.assertEquals([0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,1,0,0,0,0,1,0],scover(source,1).tolist())        
        self.assertEquals([0,0,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],scover(source,4).tolist())
       

    def test_cover(self):
        source = np.array([0,0,5,0,-5,0,0,0,0,0,1,0,0,3,0,0,-1,1,2,0,0,0,0,6,0])
        self.assertEquals([0,0,1,0,1,0,0,0,0,0,1,0,0,1,0,0,1,1,1,0,0,0,0,1,0],cover(source,1).tolist())        
        self.assertEquals([0,0,4,3,4,3,2,1,0,0,4,3,2,4,3,2,4,4,4,3,2,1,0,4,3],cover(source,4).tolist())

    def test_repeat(self):
        source = np.array([0,0,5,0,-5,0,0,0,0,0,1,0,0,3,0,0,-1,1,2,0,0,0,0,6,0])
        self.assertEquals([1,1,1,1],repeat(np.array([1,1,1,1]),1).tolist())
        self.assertEquals([0,0,1,0,1,0,0,0,0,0,1,0,0,1,0,0,1,1,1,0,0,0,0,1,0],repeat(source,1).tolist())        
        self.assertEquals([0,0,4,3,2,1,0,0,0,0,4,3,2,1,0,0,4,3,2,1,0,0,0,4,3],repeat(source,4).tolist())

    def test_extend_old(self):
        source = np.array([0,0,5,0,-5,0,0,0,0,0,1,0,0,3,0,0,-1,1,2,0,0,0,0,6,0])
        self.assertEquals([0,0,5,5,-5,-5,-5,-5,0,0,1,1,1,3,3,3,-1,1,2,2,2,2,0,6,6],extend_old(source,4).tolist())
        source2 = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.assertEquals([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],extend_old(source2,4).tolist())

    def test_extend(self):
        source = np.array([0,0,5,0,-5,0,0,0,0,0,1,0,0,3,0,0,-1,1,2,0,0,0,0,6,0])
        self.assertEquals([0,0,5,5,-5,-5,-5,-5,0,0,1,1,1,3,3,3,-1,1,2,2,2,2,0,6,6],extend(source,4).tolist())
        source2 = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.assertEquals([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],extend(source2,4).tolist())
        source2 = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0])
        self.assertEquals([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0],extend(source2,4).tolist())


    def test_extend2reverse(self):
        source = np.array([0,0,5,0,-5,0,0,0,0,0,1,0,0,3,0,0,-1,1,2,0,0,0,0,6,0])
        self.assertEquals([0,0,5,5,-5,-5,-5,-5,-5,-5,1,1,1,1,1,1,-1,1,1,1,1,1,1,1,1],extend2reverse(source).tolist())
        self.assertEquals([],extend2reverse(np.array([])).tolist())

    def test_extend2next(self):
        source = np.array([0,0,5,0,-5,0,0,0,0,0,1,0,0,3,0,0,-1,1,2,0,0,0,0,6,0])
        self.assertEquals([0,0,5,5,-5,-5,-5,-5,-5,-5,1,1,1,3,3,3,-1,1,2,2,2,2,2,6,6],extend2next(source).tolist())
        self.assertEquals([],extend2next(np.array([])).tolist())

    def test_extend2diff(self):
        self.assertEquals([],extend2diff(np.array([]),np.array([])).tolist())                
        source = np.array([0,0,5,0,-5,0,0,0,0,0,1,0,0,3,0,0,-1,1,2,0,0,0,0,6,0])
        signal1 = np.ones_like(source)
        self.assertEquals([0,0,5,5,-5,-5,-5,-5,-5,-5,1,1,1,3,3,3,-1,1,2,2,2,2,2,6,6],extend2diff(source,signal1).tolist())
        signal2 = np.array([0,0,1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4,5,5,5])
        self.assertEquals([0,0,5,5,-5,-5,-5,0,0,0,1,1,0,3,3,3,-1,1,2,2,2,2,0,6,6],extend2diff(source,signal2).tolist())
        signal2 = np.array([0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,3,3,3])
        self.assertEquals([0,0,5,5,-5,-5,-5,-5,-5,-5,1,1,0,3,3,3,-1,1,2,2,2,2,2,6,6],extend2diff(source,signal2).tolist())

    def test_sum2diff(self):
        self.assertEquals([],sum2diff(np.array([]),np.array([])).tolist())                
        source = np.array([0,0,0,1,1,1,2,2,2,3,3,3,-1,-1,-1,4,4,4,5,5,5])
        signal1 = np.ones_like(source)
        self.assertEquals([0,0,0,1,2,3,5,7,9,12,15,18,17,16,15,19,23,27,32,37,42],sum2diff(source,signal1).tolist())
        signal2 = np.array([0,0,0,1,1,1,2,2,2,3,3,3,-1,-1,-1,4,4,4,5,5,5])
        self.assertEquals([0,0,0,1,2,3,2,4,6,3,6,9,-1,-2,-3,4,8,12,5,10,15],sum2diff(source,signal2).tolist())
        signal3 = np.array([0,0,0,0,0,0,0,0,0,1,1,1,3,3,3,3,3,3,3,3,3])
        self.assertEquals([0,0,0,1,2,3,5,7,9,3,6,9,-1,-2,-3,1,5,9,14,19,24],sum2diff(source,signal3).tolist())
        source[0] = 1
        self.assertEquals([1,1,1,2,3,4,6,8,10,13,16,19,18,17,16,20,24,28,33,38,43],sum2diff(source,signal1).tolist())

    def test_sresume(self):
        source = np.array([0,0,5,0,-5,0,0,0,0,0,1,0,0,3,0,0,-1,1,2,0,0,0,0,6,0])
        self.assertEquals([0,0,1,0,1, 0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,1,0],sresume(source,2).tolist())
        self.assertEquals([0,0,0,0,0, 0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,1,0],sresume(source,3).tolist())
        self.assertEquals([0,0,0,0,0, 0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0],sresume(source,5).tolist())
        self.assertEquals([0,0,0,0,0, 0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],sresume(source,6).tolist())
        self.assertEquals([0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],sresume(source,7).tolist())        
        #covered=2
        self.assertEquals([0,0,0,0,0, 0,0,0,0,0,1,1,0,1,1,0,1,1,0,0,0,0,0,1,1],sresume(source,3,2).tolist())
        #测试covered溢出
        self.assertEquals([0,0,0,0,0, 0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1],sresume(source,3,3).tolist())        
        #空测试
        self.assertEquals([],sresume(np.array([])).tolist())
        
    def test_distance(self):
        source = np.array([0,0,5,0,-5,0,0,0,0,0,1,0,0,3,0,0,-1,1,2,0,0,0,0,6,0])
        self.assertEquals([1,2,0,1,0,1,2,3,4,5,0,1,2,0,1,2,0,0,0,1,2,3,4,0,1],distance(source).tolist())
        self.assertEquals([],distance(np.array([])).tolist())

    def test_distance2(self):
        source = np.array([0,0,5,0,-5,0,0,0,0,0,1,0,0,3,0,0,-1,1,2,0,0,0,0,6,0])
        self.assertEquals([1,2,3,1,2,1,2,3,4,5,6,1,2,3,1,2,3,1,1,1,2,3,4,5,1],distance2(source).tolist())
        self.assertEquals([],distance2(np.array([])).tolist())

    def test_rsum(self):
        self.assertEquals([],rsum(np.array([]),np.array([])).tolist())        
        source = np.array([10,20,30,40,50,60])
        signal = np.array([0,0,-1,0,1,0])
        self.assertEquals([10,30,30,70,50,110],rsum(source,signal).tolist())
        signal2 = np.array([1,0,-1,0,1,0])
        self.assertEquals([10,30,30,70,50,110],rsum(source,signal2).tolist())

    def test_rsum2(self):
        self.assertEquals([],rsum2(np.array([]),np.array([])).tolist())        
        source = np.array([10,20,30,40,50,60])
        signal = np.array([0,0,-1,0,1,0])
        self.assertEquals([10,30,45,55,80,85],rsum2(source,signal).tolist())
        signal2 = np.array([1,0,-1,0,1,0])
        self.assertEquals([5,25,40,55,80,85],rsum2(source,signal2).tolist())

    def test_ravg(self):
        self.assertEquals([],ravg(np.array([]),np.array([])).tolist())        
        source = np.array([10,20,30,40,50,60])
        signal = np.array([0,0,-1,0,1,0])
        self.assertEquals([10,15,30,35,50,55],ravg(source,signal).tolist())
        signal2 = np.array([1,0,-1,0,1,0])
        self.assertEquals([10,15,30,35,50,55],ravg(source,signal2).tolist())

    def test_ssub(self):
        self.assertEquals([],ssub(np.array([])).tolist())
        source = np.array([10,20,30,40,50,60])
        self.assertEquals([10,10,10,10,10,10],ssub(source).tolist())
        source = np.array([0,20,0,80,0,60])
        self.assertEquals([0,20,0,60,0,-20],ssub(source).tolist())

    def test_rsub(self):
        self.assertEquals([],rsub(np.array([]),np.array([])).tolist())
        source = np.array([10,20,30,40,50,60])
        signal = np.array([0,0,-1,0,1,0])
        self.assertEquals([0,0,20,0,20,0],rsub(source,signal).tolist())
        signal2 = np.array([1,0,-1,0,1,0])
        self.assertEquals([0,0,20,0,20,0],rsub(source,signal2).tolist())

    def xtest_rsub2(self):
        self.assertEquals([],rsub2(np.array([]),np.array([])).tolist())
        source = np.array([10,20,30,40,50,60])
        signal = np.array([0,0,-1,0,1,0])
        self.assertEquals([0,0,20,0,20,0],rsub2(source,signal).tolist())
        signal2 = np.array([1,0,-1,0,1,0])
        self.assertEquals([0,0,20,0,20,0],rsub2(source,signal2).tolist())
        signal2 = np.array([1,0,-1,0,1,0])
        self.assertEquals([0,0,20,0,40,0],rsub2(source,signal2,2).tolist())

    def test_msum(self):
        self.assertEquals([],msum(np.array([]),2).tolist())
        self.assertEquals([10,20,30,40,50,60,70,80],msum(np.array([10,20,30,40,50,60,70,80]),1).tolist())  #normal,length < len(source)        
        self.assertEquals([10,20,30,40,50,60,70,80],msum(np.array([10,20,30,40,50,60,70,80]),0).tolist())  #normal,length < len(source)
        self.assertEquals([0,0,60,90,120,150,180,210],msum(np.array([10,20,30,40,50,60,70,80]),3).tolist())  #normal,length < len(source)
        self.assertEquals([0,0,0,0,0,0,0,0],msum(np.array([10,20,30,40,50,60,70,80]),10).tolist())   #length > len(source)
        self.assertEquals([0,0,0,0,0,0,0,360],msum(np.array([10,20,30,40,50,60,70,80]),8).tolist())   #length = len(source)

    def test_msum2(self):
        self.assertEquals([],msum2(np.array([]),2).tolist())
        self.assertEquals([10,20,30,40,50,60,70,80],msum2(np.array([10,20,30,40,50,60,70,80]),1).tolist())  #normal,length < len(source)        
        self.assertEquals([10,20,30,40,50,60,70,80],msum2(np.array([10,20,30,40,50,60,70,80]),0).tolist())  #normal,length < len(source)
        self.assertEquals([10,30,60,90,120,150,180,210],msum2(np.array([10,20,30,40,50,60,70,80]),3).tolist())  #normal,length < len(source)
        self.assertEquals([10,30,60,100,150,210,280,360],msum2(np.array([10,20,30,40,50,60,70,80]),10).tolist())   #length > len(source)
        self.assertEquals([10,30,60,100,150,210,280,360],msum2(np.array([10,20,30,40,50,60,70,80]),8).tolist())   #length = len(source)

    def test_kfactor(self):
        self.assertEquals([],kfactor(np.array([])).tolist())
        self.assertEquals([],kfactor(np.array([]),np.array([])).tolist())
        self.assertEquals([0,0,7.250,7.250,7.250,7.250,-20*1.0/3,-20/3.0,-20/3.0],kfactor(np.array([0,1,0,0,0,30,0,0,10])).tolist())
        self.assertEquals([0,0,0,10,10,10,10,10,10],kfactor(np.array([0,1,0,0,0,30,0,0,10]),np.array([0,0,1,0,0,1,0,0,0])).tolist())
        self.assertEquals([0,0,0,0,0,0,0,0,0],kfactor(np.array([0,1,0,0,0,30,0,0,10]),np.array([0,0,1,0,0,0,0,0,0])).tolist())
        self.assertEquals([0,0,0,0,0,0,0,0,0],kfactor(np.array([0,1,0,0,0,30,0,0,10]),np.array([0,0,0,0,0,0,0,0,0])).tolist())

    def test_kx(self):
        self.assertEquals([],kx(np.array([]),10).tolist())
        self.assertEquals([],kx(np.array([]),10,np.array([])).tolist())
        self.assertEquals([0,0,0,0],kx(np.array([0,0,0,0]),3).tolist())        
        self.assertEquals([0,0,10,13,16,19,13,16,19,15,1,2,5],kx(np.array([0,0,10,0,0,0,13,0,0,15,1,2,0]),3).tolist())
        self.assertEquals([0,0,10,13,16,5,1],kx(np.array([0,0,10,0,0,5,1]),3).tolist())
        self.assertEquals([0,0,10,0,0,5,1],kx(np.array([0,0,10,0,0,5,1]),3,np.array([0,0,0,0,0,0,0])).tolist())
        self.assertEquals([0,0,3,6,0,3,6],kx(np.array([0,0,10,0,0,5,1]),3,np.array([0,1,0,0,1,0,0])).tolist())
        self.assertEquals([0,0,3,6,0,3,1],kx(np.array([0,0,10,0,0,5,1]),3,np.array([0,1,0,0,1,0,1])).tolist())        
        self.assertEquals([0,0,3,6,0,5,8],kx(np.array([0,0,10,0,0,5,1]),3,np.array([0,1,0,0,1,1,0])).tolist())
        self.assertEquals([0,0,3.1,3.1+3.1,0,5,5+3.1],kx(np.array([0,0,10,0,0,5,1]),3.1,np.array([0,1,0,0,1,1,0])).tolist())

    def test_kx2(self):
        self.assertEquals([],kx2(np.array([]),np.array([])).tolist())
        self.assertEquals([],kx2(np.array([]),np.array([]),np.array([])).tolist())
        self.assertEquals([],kx2(np.array([]),np.array([10]),np.array([])).tolist())        
        self.assertEquals([0,0,0,0],kx2(np.array([0,0,0,0]),np.array([3,3,3,3])).tolist())        
        self.assertEquals([0,0,10,13,16,19,13,16,19,15,1,2,5],kx2(np.array([0,0,10,0,0,0,13,0,0,15,1,2,0]),np.array([3,3,3,3,3,3,3,3,3,3,3,3,3])).tolist())
        self.assertEquals([0,0,10,13,16,19,13,16,19,15,1,2,5],kx2(np.array([0,0,10,0,0,0,13,0,0,15,1,2,0]),np.array([0,0,3,0,0,0,3,0,0,3,3,3,0])).tolist())        
        self.assertEquals([0,0,10,13,16,19,13,15,17,15,1,2,7],kx2(np.array([0,0,10,0,0,0,13,0,0,15,1,2,0]),np.array([0,0,3,0,0,0,2,0,0,3,4,5,0])).tolist())
        self.assertEquals([0,0,10,13,16,5,1],kx2(np.array([0,0,10,0,0,5,1]),np.array([3,3,3,3,3,3,3])).tolist())
        self.assertEquals([0,0,10,0,0,5,1],kx2(np.array([0,0,10,0,0,5,1]),np.array([0,0,0,0,0,0,0]),np.array([0,0,0,0,0,0,0])).tolist())
        self.assertEquals([0,0,3,6,0,3,6],kx2(np.array([0,0,10,0,0,5,1]),np.array([0,3,0,0,3,0,0]),np.array([0,1,0,0,1,0,0])).tolist())
        self.assertEquals([0,0,0,0,0,3,6],kx2(np.array([0,0,10,0,0,5,1]),np.array([0,0,0,0,3,0,0]),np.array([0,1,0,0,1,0,0])).tolist())        
        self.assertEquals([0,0,3,6,0,3,1],kx2(np.array([0,0,10,0,0,5,1]),np.array([0,3,0,0,3,0,3]),np.array([0,1,0,0,1,0,1])).tolist())        
        self.assertEquals([0,0,3,6,0,5,8],kx2(np.array([0,0,10,0,0,5,1]),np.array([0,3,0,0,3,3,0]),np.array([0,1,0,0,1,1,0])).tolist())
        self.assertEquals([0,0,3.1,3.1+3.1,0,5,5+3.1],kx2(np.array([0,0,10,0,0,5,1]),np.array([0,3.1,0,0,3.1,3.1,0]),np.array([0,1,0,0,1,1,0])).tolist())


    def test_emax(self):
        source = np.array([10,20,30,20,10,0,10,15,10,45,55])
        self.assertEquals([0,1,2,-1,-2,-3,1,2,-1,9,10],emax(source).tolist())
        source2 = np.array([10,5,2,3,5,7,6,15,20,25])
        self.assertEquals([0,-1,-2,1,2,3,-1,5,6,7],emax(source2).tolist())

    def test_emin(self):
        source = np.array([50,40,20,30,40,60,50,35,40,15,10])
        self.assertEquals([0,1,2,-1,-2,-3,1,2,-1,9,10],emin(source).tolist())
        source2 = np.array([10,20,30,20,10,8,10,15,10,7,5])
        self.assertEquals([0,-1,-2,1,2,3,-1,-2,1,7,8],emin(source2).tolist())
        source3 = np.array([10,5,2,3,5,7,6,15,20,25])
        self.assertEquals([0,1,2,-1,-2,-3,1,-1,-2,-3],emin(source3).tolist())

    def test_derepeat(self):
        self.assertEquals([0,3,4,-5,6,0,1,0,23,3,0],derepeat(np.array([0,3,4,-5,6,0,1,0,23,3,0]),0).tolist())
        self.assertEquals([0,3,0,-5,6,0,0,1,0,23,3,0],derepeat(np.array([0,3,0,-5,6,0,0,1,0,23,3,0]),0).tolist())
        self.assertEquals([0,3,4,-5,6,0,1,0,23,3,0],derepeat(np.array([0,3,4,-5,6,0,1,0,23,3,0])).tolist())
        self.assertEquals([0,3,0,-5,0,0,0,1,0,23,0,0],derepeat(np.array([0,3,0,-5,6,0,0,1,0,23,3,0]),2).tolist())
        self.assertEquals([0,3,0,0,6,0,0,1,0,0,3,0],derepeat(np.array([0,3,0,-5,6,0,0,1,0,23,3,0]),3).tolist())

    def test_decover(self):
        self.assertEquals([0,3,4,-5,6,0,1,0,23,3,0],decover(np.array([0,3,4,-5,6,0,1,0,23,3,0]),0).tolist())
        self.assertEquals([0,3,0,-5,6,0,0,1,0,23,3,0],decover(np.array([0,3,0,-5,6,0,0,1,0,23,3,0]),0).tolist())
        self.assertEquals([0,3,0,0,0,0,1,0,23,0,0],decover(np.array([0,3,4,-5,6,0,1,0,23,3,0])).tolist())
        self.assertEquals([0,3,0,0,0,0,0,1,0,0,0,0],decover(np.array([0,3,0,-5,6,0,0,1,0,23,3,0]),2).tolist())

    def test_decover1(self):
        self.assertEquals([0,1,1,1,1,0,1,0,1,1,0],decover1(np.array([0,3,4,-5,6,0,1,0,23,3,0]),0).tolist())
        self.assertEquals([0,1,0,1,1,0,0,1,0,1,1,0],decover1(np.array([0,3,0,-5,6,0,0,1,0,23,3,0]),0).tolist())
        self.assertEquals([0,1,0,0,0,0,1,0,1,0,0],decover1(np.array([0,3,4,-5,6,0,1,0,23,3,0])).tolist())
        self.assertEquals([0,1,0,0,0,0,0,1,0,0,0,0],decover1(np.array([0,3,0,-5,6,0,0,1,0,23,3,0]),2).tolist())

    def test_derepeatc_v(self):
        self.assertEquals([0,3,0,0,0,0,1,0,23,0,0],derepeatc_v(np.array([0,3,4,-5,6,0,1,0,23,3,0])).tolist())
        self.assertEquals([0,3,0,-5,0,0,0,1,0,23,0,0],derepeatc_v(np.array([0,3,0,-5,6,0,0,1,0,23,3,0])).tolist())
        self.assertEquals([0,3,0,0,0,0,1,0,23,0,0],derepeatc_v(np.array([0,3,4,-5,6,0,1,0,23,3,0])).tolist())

    def test_derepeatc(self):
        self.assertEquals([0,1,0,0,0,0,1,0,1,0,0],derepeatc(np.array([0,3,4,-5,6,0,1,0,23,3,0])).tolist())
        self.assertEquals([0,1,0,1,0,0,0,1,0,1,0,0],derepeatc(np.array([0,3,0,-5,6,0,0,1,0,23,3,0])).tolist())
        self.assertEquals([0,1,0,0,0,0,1,0,1,0,0],derepeatc(np.array([0,3,4,-5,6,0,1,0,23,3,0])).tolist())

    def test_sfollow(self):
        source1 = np.array([10,20,0,0,0,0,0,10,0,40,0,0,0,0,0,-40,0])
        source2 = np.array([0,20,0,1,-5,0,0,10,0,0,60,0,0,0,0,0,40])
        self.assertEquals([0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],sfollow(source1,source2).tolist())
        self.assertEquals([0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1],sfollow(source1,source2,2).tolist())
        self.assertEquals([0,1,0,1,1,0,0,1,0,0,1,0,0,0,0,0,1],sfollow(source1,source2,10).tolist())

    def test_syntony(self):
        source1 = np.array([10,0,0,0,-5,10,0,0,10,40, 0,0,0,0,0,40, 0])
        source2 = np.array([0,20,0,1, 5, 0,0,0, 0, 0,60,0,0,0,0, 0,40])
        self.assertEquals([0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],syntony(source1,source2).tolist())
        self.assertEquals([0,1,0,0,1,1,0,0,0,0,1,0,0,0,0,0,1],syntony(source1,source2,2).tolist())
        self.assertEquals([0,1,1,0,1,1,1,0,0,0,1,1,0,0,0,0,1],syntony(source1,source2,3).tolist())
        self.assertEquals([0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],syntony(source1,source2,11).tolist())

    def test_gsyntony(self):
        source1 = np.array([10,0,0,0,-5,10,0,0,10,40, 0,0,0,0,0,40, 0])
        source2 = np.array([0,20,0,1, 5, 0,0,0, 0, 0,60,0,0,0,0, 0,40])
        self.assertEquals([0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],gsyntony(source1,source2,1).tolist())
        self.assertEquals([0,1,0,0,1,1,0,0,0,0,1,0,0,0,0,0,1],gsyntony(source1,source2,2).tolist())
        self.assertEquals([0,1,1,0,1,1,1,0,0,0,1,1,0,0,0,0,1],gsyntony(source1,source2,3).tolist())
        self.assertEquals([0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],gsyntony(source1,source2,11).tolist())
        source3 = np.array([0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,0])
        self.assertEquals([0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1],gsyntony(source1,source2,source3,2).tolist())
        self.assertEquals([0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,1],gsyntony(source1,source2,source3,3).tolist())
        self.assertEquals([0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],gsyntony(source1,source2,source3,10).tolist())
        self.assertEquals([0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],gsyntony(source1,source2,source3,11).tolist())

    def test_consecutive(self):
        source = np.array([0,2,2,2,0,0,1,1,0,0,1,2,2,0,2,0])
        self.assertEquals([0,0,0,0,0,0,1,2,0,0,1,0,0,0,0,0],consecutive(source).tolist())
        self.assertEquals([0,0,0,0,0,0,1,2,0,0,1,0,0,0,0,0],consecutive(source,1).tolist())
        self.assertEquals([0,1,2,3,0,0,0,0,0,0,0,1,2,0,1,0],consecutive(source,2).tolist())

    def test_devi(self):
        self.assertEquals([],devi(np.array([]),np.array([])).tolist())
        s1 = np.array([0,0,0,0,0,0,0,0,0,0,0,0])
        self.assertEquals(s1.tolist(),devi(s1,s1).tolist())
        shigh = np.array([0,13,0,0,0,0,0,15,0,0,0])
        sdiff = np.array([0,13,0,0,0,0,0,10,0,0,0])
        self.assertEquals([0,0,0,0,0,0,0,0,1,1,1],devi(shigh,sdiff).tolist())
        shigh2 = np.array([0,13,0,0,0,0,0,12,0,0,0])
        self.assertEquals([0,0,0,0,0,0,0,0,0,0,0],devi(shigh2,sdiff).tolist())

    def test_hdevi(self):
        self.assertEquals([],hdevi(np.array([]),np.array([]),np.array([])).tolist())
        s1 = np.array([0,0,0,0,0,0,0,0,0,0,0,0])
        self.assertEquals(s1.tolist(),hdevi(s1,s1,s1).tolist())
        shigh = np.array([0,13,0,0,0,0,0,15,0,0,0])
        sdiff = np.array([1,13,0,0,0,0,1,10,0,0,0])
        sdea = np.array([0,15,0,0,0,0,0,12,0,0,0])        
        self.assertEquals([0,0,0,0,0,0,0,1,0,0,0],hdevi(shigh,sdiff,sdea,covered=5).tolist())
        shigh = np.array([0,13,0,0,0,0,0,12,0,0,0]) #双低
        self.assertEquals([0,0,0,0,0,0,0,0,0,0,0],hdevi(shigh,sdiff,sdea,covered=5).tolist())
        shigh = np.array([0,13,0,0,0,0,0,15,0,0,0]) #双高
        sdiff = np.array([1,13,0,0,0,0,1,20,0,0,0])
        sdea = np.array([0,15,0,0,0,0,0,22,0,0,0])        
        self.assertEquals([0,0,0,0,0,0,0,0,0,0,0],hdevi(shigh,sdiff,sdea,covered=5).tolist())

    def test_ldevi(self):
        self.assertEquals([],ldevi(np.array([]),np.array([]),np.array([])).tolist())
        s1 = np.array([0,0,0,0,0,0,0,0,0,0,0,0])
        self.assertEquals(s1.tolist(),ldevi(s1,s1,s1).tolist())
        slow = np.array([15,13,12,10,10,10,10,11,0,0,0])
        sdiff = np.array([3,19,12,8,9,10,12,15,0,0,0])
        sdea = np.array([2,22,0,0,0,0,15,9,0,0,0])        
        self.assertEquals([0,0,0,0,0,0,0,1,0,0,0],ldevi(slow,sdiff,sdea,covered=5).tolist())
        slow = np.array([7,7,7,10,10,10,10,11,0,0,0]) #双高
        self.assertEquals([0,0,0,0,0,0,0,0,0,0,0],ldevi(slow,sdiff,sdea,covered=5).tolist())
        slow = np.array([15,13,12,10,10,10,10,11,0,0,0]) #双低
        sdiff = np.array([3,19,12,8,9,2,12,15,0,0,0])
        sdea = np.array([2,22,0,0,0,0,15,9,0,0,0])        
        self.assertEquals([0,0,0,0,0,0,0,0,0,0,0],ldevi(slow,sdiff,sdea,covered=5).tolist())

    def test_hpeak(self):#测试通路
        self.assertEquals([],hpeak(np.array([]),np.array([]),np.array([])).tolist())

    def test_lpeak(self):#测试通路
        self.assertEquals([],lpeak(np.array([]),np.array([]),np.array([])).tolist())

    def test_hlpeak(self):#测试通路
        self.assertEquals([],hlpeak(np.array([]),np.array([]),np.array([]),np.array([])).tolist())

    def test_zpeak(self):
        self.assertEquals([],zpeak(np.array([])).tolist())
        source = np.array([10,20,30,20,10,5,37,5,3,1,2,1,0,1,0])
        self.assertEquals([0,0,30,0,0,0,37,0,0,0,2,0,0,1,0],zpeak(source).tolist())
        self.assertEquals([0,0,0,0,0,0,37,0,0,0,0,0,0,0,0],zpeak(source,2).tolist())        

    def test_zhpeak(self):  #同zpeak
        self.assertEquals([],zhpeak(np.array([])).tolist())
        source = np.array([10,20,30,20,10,5,37,5,3,1,2,1,0,1,0])
        self.assertEquals([0,0,30,0,0,0,37,0,0,0,2,0,0,1,0],zhpeak(source).tolist())
        self.assertEquals([0,0,0,0,0,0,37,0,0,0,0,0,0,0,0],zhpeak(source,2).tolist())        

    def test_zlpeak(self):  #
        self.assertEquals([],zlpeak(np.array([])).tolist())
        source = np.array([10,20,10,20,10,5,37,15,13,10,12,14])
        self.assertEquals([0,0,10,0,0,5,0,0,0,10,0,0],zlpeak(source).tolist())
        self.assertEquals([0,0,0,0,0,5,0,0,0,0,0,0],zlpeak(source,2).tolist())

    def test_zpeaki(self):
        self.assertEquals([],zpeaki(np.array([]))[0].tolist())
        self.assertEquals([],zpeaki(np.array([]))[1].tolist())        
        source = np.array([10,20,30,20,10,5,37,5,3,1,2,1,0,1,0])
        self.assertEquals([0,0,30,0,0,0,37,0,0,0,2,0,0,1,0],zpeaki(source)[0].tolist())
        self.assertEquals([0,0,3,0,0,0,7,0,0,0,11,0,0,14,0],zpeaki(source)[1].tolist())        
        self.assertEquals([0,0,0,0,0,0,37,0,0,0,0,0,0,0,0],zpeaki(source,2)[0].tolist())        
        self.assertEquals([0,0,0,0,0,0,11,0,0,0,0,0,0,0,0],zpeaki(source,2)[1].tolist())        

    def test_zhpeaki(self):  #同zpeaki
        self.assertEquals([],zhpeaki(np.array([]))[0].tolist())
        self.assertEquals([],zhpeaki(np.array([]))[1].tolist())        
        source = np.array([10,20,30,20,10,5,37,5,3,1,2,1,0,1,0])
        self.assertEquals([0,0,30,0,0,0,37,0,0,0,2,0,0,1,0],zhpeaki(source)[0].tolist())
        self.assertEquals([0,0,3,0,0,0,7,0,0,0,11,0,0,14,0],zhpeaki(source)[1].tolist())        
        self.assertEquals([0,0,0,0,0,0,37,0,0,0,0,0,0,0,0],zhpeaki(source,2)[0].tolist())        
        self.assertEquals([0,0,0,0,0,0,11,0,0,0,0,0,0,0,0],zhpeaki(source,2)[1].tolist())        

    def test_zlpeaki(self):  #
        self.assertEquals([],zlpeaki(np.array([]))[0].tolist())
        self.assertEquals([],zlpeaki(np.array([]))[1].tolist())        
        source = np.array([10,20,10,20,10,5,37,15,13,10,12,14])
        self.assertEquals([0,0,10,0,0,5,0,0,0,10,0,0],zlpeaki(source)[0].tolist())
        self.assertEquals([0,0,3,0,0,6,0,0,0,10,0,0],zlpeaki(source)[1].tolist())        
        self.assertEquals([0,0,0,0,0,5,0,0,0,0,0,0],zlpeaki(source,2)[0].tolist())
        self.assertEquals([0,0,0,0,0,10,0,0,0,0,0,0],zlpeaki(source,2)[1].tolist())        

    def test_swing(self):
        self.assertEquals([0,0,0,0,0],swing(np.array([10,30,25,15,45])).tolist())
        self.assertEquals([0,2000,200,666,2000],swing(np.array([10,30,25,15,45]),2).tolist())
        self.assertEquals([0,2000,2000,1000,2000],swing(np.array([10,30,25,15,45]),3).tolist())

    def test_iswing(self):
        sv,si = iswing(np.array([10,30,25,15,45]))
        self.assertEquals([0,0,0,0,0],sv.tolist())
        self.assertEquals([0,0,0,0,0],si.tolist())        
        #
        sv,si = iswing(np.array([10,30,25,15,45]),2)
        self.assertEquals([0,2000,200,666,2000],sv.tolist())
        self.assertEquals([0,1,-1,-1,1],si.tolist())        
        #
        sv,si = iswing(np.array([10,30,25,15,45]),3)
        self.assertEquals([0,2000,2000,1000,2000],sv.tolist())
        self.assertEquals([0,1,1,-2,1],si.tolist())        

    def test_gswing(self):
        base = np.array([10,10,10,10,10])
        self.assertEquals([0,2000,1000,500,3500],gswing(base,np.array([10,30,5,15,45])).tolist())
        self.assertEquals([0,2000,5000,2000,3500],gswing(base,np.array([10,30,5,15,45]),2).tolist())
        self.assertEquals([0,2000,5000,5000,8000],gswing(base,np.array([10,30,5,15,45]),3).tolist())
        base2 = np.array([20,20,20,20,20])
        self.assertEquals([1000,2000,3000,1000,3500],gswing(base,base2,np.array([10,30,5,15,45])).tolist())
        self.assertEquals([1000,2000,5000,3000,3500],gswing(base,base2,np.array([10,30,5,15,45]),2).tolist())
        self.assertEquals([1000,2000,5000,5000,8000],gswing(base,base2,np.array([10,30,5,15,45]),3).tolist())

    def test_giswing(self):
        base = np.array([10,10,10,10,10])
        #
        sv,si = giswing(base,np.array([10,30,5,15,45]))
        self.assertEquals([0,2000,1000,500,3500],sv.tolist())
        self.assertEquals([0,0,0,0,0],si.tolist())
        #
        sv,si = giswing(base,np.array([10,30,5,15,45]),2)
        self.assertEquals([0,2000,5000,2000,3500],sv.tolist())
        self.assertEquals([0,0,-1,1,0],si.tolist())
        #
        sv,si = giswing(base,np.array([10,30,5,15,45]),3)
        self.assertEquals([0,2000,5000,5000,8000],sv.tolist())
        self.assertEquals([0,0,-1,-1,2],si.tolist())
        #
        base2 = np.array([20,20,20,20,20])
        #
        sv,si = giswing(base,base2,np.array([10,30,5,15,45]))
        self.assertEquals([1000,2000,3000,1000,3500],sv.tolist())
        self.assertEquals([0,0,0,0,0],si.tolist())
        #
        sv,si = giswing(base,base2,np.array([10,30,5,15,45]),2)
        self.assertEquals([1000,2000,5000,3000,3500],sv.tolist())
        self.assertEquals([0,0,-1,1,0],si.tolist())
        #
        sv,si = giswing(base,base2,np.array([10,30,5,15,45]),3)
        self.assertEquals([1000,2000,5000,5000,8000],sv.tolist())
        self.assertEquals([0,0,-1,-1,2],si.tolist())

    def test_swing2(self):
        slow = np.array([10,10,10,10,10,10])
        shigh = np.array([10,30,15,25,45,25])
        self.assertEquals([0,2000,500,1500,3500,1500],swing2(shigh,slow).tolist())
        self.assertEquals([0,2000,2000,1500,3500,3500],swing2(shigh,slow,2).tolist())
        self.assertEquals([0,2000,2000,2000,3500,3500],swing2(shigh,slow,3).tolist())

    def test_iswing2(self):
        slow = np.array([10,10,10,10,10,10])
        shigh = np.array([10,30,15,25,45,25])
        #
        sv,si = iswing2(shigh,slow)
        self.assertEquals([0,2000,500,1500,3500,1500],sv.tolist())
        self.assertEquals([0,0,0,0,0,0],si.tolist())
        #
        sv,si = iswing2(shigh,slow,2)
        self.assertEquals([0,2000,2000,1500,3500,3500],sv.tolist())
        self.assertEquals([0,0,-1,0,0,-1],si.tolist())
        #
        sv,si = iswing2(shigh,slow,3)
        self.assertEquals([0,2000,2000,2000,3500,3500],sv.tolist())
        self.assertEquals([0,0,-1,-2,0,-1],si.tolist())
        
    def test_left_fill(self):
        self.assertEquals([],left_fill([]))
        self.assertEquals([0,0,0,0,0],left_fill(np.array([0,0,0,0,0])).tolist())
        self.assertEquals([1,2,3,4,5],left_fill(np.array([1,2,3,4,5])).tolist())
        self.assertEquals([1,2,3,4,4],left_fill(np.array([1,2,3,4,0])).tolist())
        self.assertEquals([0,2,3,4,5],left_fill(np.array([0,2,3,4,5])).tolist())
        self.assertEquals([0,2,3,4,4],left_fill(np.array([0,2,3,4,0])).tolist())
        self.assertEquals([1,2,2,2,5],left_fill(np.array([1,2,0,0,5])).tolist())
        self.assertEquals([0,2,2,2,5],left_fill(np.array([0,2,0,0,5])).tolist())

    def test_zavg(self):
        self.assertEquals(0,zavg(np.array([])))
        self.assertEquals(25,zavg(np.array([10,20,0,40,30])).tolist())
        self.assertEquals(16,zavg(np.array([10,20,0,40,30,-20])).tolist())

    def test_tmax(self):
        self.assertEquals([7,6,5,4,3,2,1],tmax(np.array([7,6,5,4,3,2,1]),1).tolist())
        self.assertEquals([1,2,3,4,5,6,7],tmax(np.array([1,2,3,4,5,6,7]),2).tolist())
        self.assertEquals([7,7,6,5,4,3,2],tmax(np.array([7,6,5,4,3,2,1]),2).tolist())
        self.assertEquals([7,7,7,7,7,7,7],tmax(np.array([7,6,5,4,3,2,1]),14).tolist())
        self.assertEquals([3,4,5,5,4,7],tmax(np.array([3,4,5,4,4,7]),2).tolist())

    def test_tmin(self):
        self.assertEquals([3,4,5,4,4,7],tmin(np.array([3,4,5,4,4,7]),1).tolist())
        self.assertEquals([1,1,2,3,4,5,6],tmin(np.array([1,2,3,4,5,6,7]),2).tolist())
        self.assertEquals([7,6,5,4,3,2,1],tmin(np.array([7,6,5,4,3,2,1]),2).tolist())
        self.assertEquals([1,1,1,1,1,1,1],tmin(np.array([1,2,3,4,5,6,7]),14).tolist())
        self.assertEquals([3,3,4,4,4,4],tmin(np.array([3,4,5,4,4,7]),2).tolist())

    def test_ti_max(self):
        r,ir = ti_max(np.array([7,6,5,4,3,2,1]),1)
        self.assertEquals([7,6,5,4,3,2,1],r.tolist())
        self.assertEquals([0,1,2,3,4,5,6],ir.tolist())
        #
        r,ir = ti_max(np.array([1,2,3,4,5,6,7]),2)
        self.assertEquals([1,2,3,4,5,6,7],r.tolist())
        self.assertEquals([0,1,2,3,4,5,6],ir.tolist())
        #
        r,ir = ti_max(np.array([7,6,5,4,3,2,1]),2)
        self.assertEquals([7,7,6,5,4,3,2],r.tolist())
        self.assertEquals([0,0,1,2,3,4,5],ir.tolist())
        #
        r,ir = ti_max(np.array([7,6,5,4,3,2,1]),14)
        self.assertEquals([7,7,7,7,7,7,7],r.tolist())
        self.assertEquals([0,0,0,0,0,0,0],ir.tolist())
        #
        #print '---------'
        r,ir = ti_max(np.array([3,4,5,4,4,7]),2)
        self.assertEquals([3,4,5,5,4,7],r.tolist())
        self.assertEquals([0,1,2,2,4,5],ir.tolist())
        #print '+++++++++++'
 
    def test_ti_min(self):
        r,ir = ti_min(np.array([3,4,5,4,4,7]),1)
        self.assertEquals([3,4,5,4,4,7],r.tolist())
        self.assertEquals([0,1,2,3,4,5],ir.tolist())
        #
        r,ir = ti_min(np.array([1,2,3,4,5,6,7]),2)
        self.assertEquals([1,1,2,3,4,5,6],r.tolist())
        self.assertEquals([0,0,1,2,3,4,5],ir.tolist())
        #
        r,ir = ti_min(np.array([7,6,5,4,3,2,1]),2)
        self.assertEquals([7,6,5,4,3,2,1],r.tolist())
        self.assertEquals([0,1,2,3,4,5,6],ir.tolist())
        #
        r,ir = ti_min(np.array([1,2,3,4,5,6,7]),14)
        self.assertEquals([1,1,1,1,1,1,1],r.tolist())
        self.assertEquals([0,0,0,0,0,0,0],ir.tolist())
        #
        r,ir = ti_min(np.array([3,4,5,4,4,7]),2)
        self.assertEquals([3,3,4,4,4,4],r.tolist())
        self.assertEquals([0,0,1,3,4,4],ir.tolist())
        #
        r,ir = ti_min(np.array([5,4,3,4,4,1]),2)
        self.assertEquals([5,4,3,3,4,1],r.tolist())
        self.assertEquals([0,1,2,2,4,5],ir.tolist())

        
    def test_max0(self):
        self.assertEquals([7,7,7,7,7,7,7],max0(np.array([7,6,5,4,3,2,1])).tolist())
        self.assertEquals([1,2,3,4,5,6,7],max0(np.array([1,2,3,4,5,6,7])).tolist())
        self.assertEquals([3,4,5,5,5,7],max0(np.array([3,4,5,4,4,7])).tolist())

    def test_min0(self):
        self.assertEquals([3,3,3,3,3,3],min0(np.array([3,4,5,4,4,7])).tolist())
        self.assertEquals([7,6,5,4,3,2,1],min0(np.array([7,6,5,4,3,2,1])).tolist())
        self.assertEquals([4,4,3,3,1,1],min0(np.array([4,5,3,4,1,7])).tolist())

    def test_amax0(self):
        self.assertEquals([0,0,0,0,0,0,0],amax0(np.array([7,6,5,4,3,2,1])).tolist())
        self.assertEquals([0,1,2,3,4,5,6],amax0(np.array([1,2,3,4,5,6,7])).tolist())
        self.assertEquals([0,1,2,2,2,5],amax0(np.array([3,4,5,4,4,7])).tolist())

    def test_amin0(self):
        self.assertEquals([0,0,0,0,0,0],amin0(np.array([3,4,5,4,4,7])).tolist())
        self.assertEquals([0,1,2,3,4,5,6],amin0(np.array([7,6,5,4,3,2,1])).tolist())
        self.assertEquals([0,0,2,2,4,4],amin0(np.array([4,5,3,4,1,7])).tolist())

    def test_mapping(self):
        self.assertEquals([11,51,41,0,21,0,31],mapping(np.array([11,21,31,41,51]),np.array([0,4,6,2,1]),7).tolist())
        self.assertEquals([11,51,41,0,61,0,31],mapping(np.array([11,21,31,41,51,61]),np.array([0,4,6,2,1,4]),7).tolist())
        self.assertEquals([71,51,41,0,61,0,31],mapping(np.array([0,21,31,41,51,61,71]),np.array([0,4,6,2,1,4,0]),7).tolist())
        try:    
            self.assertEquals([11,51,41,0,21,0,31],mapping(np.array([11,21,31,41,51]),np.array([0,4,6,2,1]),6).tolist())
        except: 
            self.assertTrue(True)
        else:
            self.assertTrue(False)
        #空测试
        self.assertEquals([0,0,0,0,0,0,0],mapping(np.array([]),np.array([]),7).tolist())

    def test_transform(self):
        self.assertEquals([0,0,1,0,1,0,0],transform(np.array([0,1,0,1,0]),np.array([0,4,6,2,1]),7).tolist())
        self.assertEquals([0,1,1,0,0,0,0],transform(np.array([0,1,0,0,1,0]),np.array([0,1,1,1,2,3]),7).tolist())
        self.assertEquals([0,0,0,0,0,0,0],transform(np.array([0,0,0,0,0,0]),np.array([0,1,1,1,2,3]),7).tolist())
        try:    
            self.assertEquals([11,51,41,0,21,0,31],transform(np.array([11,21,31,41,51]),np.array([0,4,6,2,1]),6).tolist())
        except: 
            self.assertTrue(True)
        else:
            self.assertTrue(False)
        #空测试
        self.assertEquals([0,0,0,0,0,0,0],transform(np.array([]),np.array([]),7).tolist())

    def test_limitup1(self):
        self.assertEquals([],limitup1(np.array([])).tolist())
        self.assertEquals([0,1,1,0,1],limitup1(np.array([1000,1100,1210,1000,1099])).tolist())

    def test_limitdown1(self):
        self.assertEquals([],limitdown1(np.array([])).tolist())
        self.assertEquals([0,1,0,1,0],limitdown1(np.array([1000,900,1000,901,1099])).tolist())

    def test_limit1(self):
        self.assertEquals([],limit1(np.array([])).tolist())
        self.assertEquals([0,1,-1,0,1],limit1(np.array([1000,1100,990,1000,1099])).tolist())

    def test_limitup2(self):
        self.assertEquals([],limitup1(np.array([])).tolist())
        self.assertEquals([0,0,1,0,1,1],limitup2(np.array([1000,1100,1210,1000,1099,1101]),np.array([1000,1050,1210,1000,1099,1101])).tolist())

    def test_limitdown2(self):
        self.assertEquals([],limitdown1(np.array([])).tolist())
        self.assertEquals([0,1,0,0,0,1],limitdown2(np.array([1000,900,1000,901,1099,1080]),np.array([1000,900,1000,953,1099,1080])).tolist())

    def test_limit2(self):
        self.assertEquals([],limit2(np.array([]),np.array([])).tolist())
        self.assertEquals([0,1,-1,1,0],limit2(np.array([1000,1100,990,1000,1099]),np.array([1000,1100,990,1000,1080])).tolist())

    def test_cached_zoom_indices(self):
        self.assertEquals([4,9],cached_zoom_indices(10,5,4).tolist())
        self.assertEquals([0,5],cached_zoom_indices(10,5,0).tolist())
        a = cached_zoom_indices(10,5,4)
        b = cached_zoom_indices(10,5,4)
        c = cached_zoom_indices(10,5,1)
        self.assertEquals(id(a),id(b))
        self.assertNotEquals(id(a),id(c))

    def test_pzoom_out(self):
        a = np.arange(10)
        self.assertEquals([4,9],pzoom_out(a,5).tolist())
        self.assertEquals([0,5],pzoom_out(a,5,0).tolist())
        self.assertEquals([3,7],pzoom_out(a,4).tolist())
        self.assertEquals([],pzoom_out(np.array([]),4).tolist())

    def test_vzoom_out(self):
        a = np.arange(10)
        self.assertEquals([10,35],vzoom_out(a,5).tolist())
        self.assertEquals([6,22],vzoom_out(a,4).tolist())
        self.assertEquals([],vzoom_out(np.array([]),4).tolist())

    def test_zoom_in(self):
        zoomed = np.array([1,2])
        self.assertEquals([0,0,1,1,2],zoom_in(zoomed,5,2).tolist())
        self.assertEquals([0,0,0,1,1,1],zoom_in(zoomed,6,3).tolist())
        self.assertRaises(AssertionError,zoom_in,zoomed,6,4)

    def test_supdowns(self):
        na = np.array([])
        na1,na2 = supdowns(na,na,na,na)
        self.assertEquals([],na1.tolist())
        self.assertEquals([],na2.tolist())
        shigh = np.array([1000,1000,1000,1000,1000,1000])
        slow = np.array([800,800,800,800,800,800])
        sopen = np.array([900,900,900,900,900,900])
        sclose = np.array([950,880,900,910,900,880])
        su,sd = supdowns(sopen,sclose,shigh,slow)
        self.assertEquals([1250,900,1000,1050,1000,900],su.tolist())
        self.assertEquals([750,1100,1000,950,1000,1100],sd.tolist())

    def test_supdownc(self):
        na = np.array([])
        na1,na2 = supdownc(na,na,na,na)
        self.assertEquals([],na1.tolist())
        self.assertEquals([],na2.tolist())
        shigh = np.array([1000,1000,1000,1000,1000,1000])
        slow = np.array([800,800,800,800,800,800])
        sopen = np.array([900,900,900,900,900,900])
        sclose = np.array([950,880,900,910,900,880])
        su,sd = supdownc(sopen,sclose,shigh,slow)
        self.assertEquals([1250,900,1100,1050,1000,900],su.tolist())
        self.assertEquals([750,1350,1000,950,1050,1100],sd.tolist())

    def test_supdown(self):
        na = np.array([])
        na1,na2 = supdown(na,na,na,na)
        self.assertEquals([],na1.tolist())
        self.assertEquals([],na2.tolist())
        shigh = np.array([1000,1000,1000,1000,1000,1000])
        slow = np.array([800,800,800,800,800,800])
        sopen = np.array([900,900,900,900,900,900])
        sclose = np.array([950,880,900,910,900,880])
        su,sd = supdown(sopen,sclose,shigh,slow)
        self.assertEquals([250,200,220,210,200,200],su.tolist())
        self.assertEquals([200,270,200,200,210,220],sd.tolist())

    def test_supdown2(self):
        na = np.array([])
        na1,na2 = supdown2(na,na,na,na)
        self.assertEquals([],na1.tolist())
        self.assertEquals([],na2.tolist())
        shigh = np.array([1000,1000,1000,1000,1000,1000])
        slow = np.array([800,800,800,800,800,800])
        sopen = np.array([900,950,880,880,920,930])
        sclose = np.array([950,880,900,910,930,880])
        su,sd = supdown2(sopen,sclose,shigh,slow)
        self.assertEquals([200,130,200,200,220,150],su.tolist())
        self.assertEquals([150,200,180,190,200,200],sd.tolist())

    def test_supdown3(self):
        na = np.array([])
        na1,na2 = supdown3(na,na,na,na)
        self.assertEquals([],na1.tolist())
        self.assertEquals([],na2.tolist())
        shigh = np.array([1000,1000,1000,1000,1000,1000])
        slow = np.array([800,800,800,800,800,800])
        sopen = np.array([900,950,880,880,920,930])
        sclose = np.array([950,880,900,910,930,880])
        su,sd = supdown3(sopen,sclose,shigh,slow)
        self.assertEquals([150,80,100,110,130,80],su.tolist())
        self.assertEquals([50,120,100,90,70,120],sd.tolist())

    def test_range4(self):
        self.assertEquals([],range4(0))
        self.assertEquals([3],range4(4))
        self.assertEquals([3,7],range4(8))        
        self.assertEquals([3,7,11,15,19,23],range4(24))
        x = range4(120)
        y = range4(120)
        self.assertEquals(id(x),id(y))
        self.assertRaises(AssertionError,range4,13)

    def test_range1(self):
        self.assertEquals([],range1(0))
        self.assertEquals([0],range1(4))
        self.assertEquals([0,4],range1(8))        
        self.assertEquals([0,4,8,12,16,20],range1(24))
        x = range1(120)
        y = range1(120)
        self.assertEquals(id(x),id(y))
        self.assertRaises(AssertionError,range1,13)

    def test_range2(self):
        self.assertEquals([],range2(0))
        self.assertEquals([1],range2(4))
        self.assertEquals([1,5],range2(8))        
        self.assertEquals([1,5,9,13,17,21],range2(24))
        x = range2(120)
        y = range2(120)
        self.assertEquals(id(x),id(y))
        self.assertRaises(AssertionError,range2,13)

    def test_range3(self):
        self.assertEquals([],range3(0))
        self.assertEquals([2],range3(4))
        self.assertEquals([2,6],range3(8))        
        self.assertEquals([2,6,10,14,18,22],range3(24))
        x = range3(120)
        y = range3(120)
        self.assertEquals(id(x),id(y))
        self.assertRaises(AssertionError,range3,13)

    def test_nzeros4(self):
        self.assertEquals([],nzeros4(0).tolist())
        self.assertEquals([0,0,0,0],nzeros4(4).tolist())
        self.assertEquals([0,0,0,0,0,0,0,0],nzeros4(8).tolist())
        x = nzeros4(100)
        y = nzeros4(100)
        self.assertEquals(id(x),id(y))
        self.assertRaises(AssertionError,nzeros4,13)
        
    def test_hour2day(self):
        self.assertEquals([],hour2day(np.array([])).tolist())
        self.assertEquals([10],hour2day(np.array([1,2,3,4])).tolist())
        self.assertEquals([10,26],hour2day(np.array([1,2,3,4,5,6,7,8])).tolist())
        self.assertRaises(AssertionError,hour2day,np.array([1,2,3,4,5,6,7,8,9]))

    def test_hour2day4(self):
        self.assertEquals([],hour2day4(np.array([])).tolist())
        self.assertEquals([4],hour2day4(np.array([1,2,3,4])).tolist())
        self.assertEquals([4,8],hour2day4(np.array([1,2,3,4,5,6,7,8])).tolist())
        self.assertRaises(AssertionError,hour2day4,np.array([1,2,3,4,5,6,7,8,9]))

    def test_hour2day1(self):
        self.assertEquals([],hour2day1(np.array([])).tolist())
        self.assertEquals([1],hour2day1(np.array([1,2,3,4])).tolist())
        self.assertEquals([1,5],hour2day1(np.array([1,2,3,4,5,6,7,8])).tolist())
        self.assertRaises(AssertionError,hour2day1,np.array([1,2,3,4,5,6,7,8,9]))

    def test_hour2day2(self):
        self.assertEquals([],hour2day2(np.array([])).tolist())
        self.assertEquals([2],hour2day2(np.array([1,2,3,4])).tolist())
        self.assertEquals([2,6],hour2day2(np.array([1,2,3,4,5,6,7,8])).tolist())
        self.assertRaises(AssertionError,hour2day2,np.array([1,2,3,4,5,6,7,8,9]))

    def test_hour2day3(self):
        self.assertEquals([],hour2day3(np.array([])).tolist())
        self.assertEquals([3],hour2day3(np.array([1,2,3,4])).tolist())
        self.assertEquals([3,7],hour2day3(np.array([1,2,3,4,5,6,7,8])).tolist())
        self.assertRaises(AssertionError,hour2day3,np.array([1,2,3,4,5,6,7,8,9]))


    def test_hour2day_s(self):
        self.assertEquals([],hour2day_s(np.array([]),np.array([])).tolist())
        self.assertEquals([3],hour2day_s(np.array([1,2,3,4]),np.array([0,0,1,0])).tolist())
        self.assertEquals([2,8],hour2day_s(np.array([1,2,3,4,5,6,7,8]),np.array([0,1,0,0,0,0,0,1])).tolist())
        self.assertEquals([2,8],hour2day_s(np.array([1,2,3,4,5,6,7,8]),np.array([0,-3,0,0,0,0,0,5])).tolist())
        self.assertEquals([3,8],hour2day_s(np.array([1,2,3,4,5,6,7,8]),np.array([0,1,0,1,0,0,0,1])).tolist())
        self.assertEquals([3,8],hour2day_s(np.array([1,2,3,4,5,6,7,8]),np.array([0,1,0,4,0,0,0,1])).tolist())
        self.assertRaises(AssertionError,hour2day_s,np.array([1,2,3,4,5,6,7,8,9]),np.array([0,1,2,3,4,5,6,7,8]))

    def test_xfollow(self):
        self.assertEquals([],xfollow(np.array([]),np.array([])).tolist())
        self.assertEquals([1,1,3],xfollow(np.array([1,2,3]),np.array([1,0,1])).tolist())
        self.assertEquals([1,1,3],xfollow(np.array([1,2,3]),np.array([0,0,1])).tolist())
        self.assertEquals([1,2,3],xfollow(np.array([1,2,3]),np.array([1,1,1])).tolist())        
        self.assertRaises(AssertionError,xfollow,np.array([1,2,3,4,5,6,7,8,9]),np.array([1,2,3,4,5,6,7,8]))

    def test_closedayofweek(self):
        self.assertEquals([],closedayofweek(np.array([])).tolist())
        self.assertEquals([1,0,0,0,0,1,0,0,1,1],closedayofweek(np.array([5,1,2,3,4,5,1,2,3,1])).tolist())
        self.assertEquals([1,0,0,0,0,1,0,0,1,1],cofw(np.array([5,1,2,3,4,5,1,2,3,1])).tolist())

    def test_opendayofweek(self):
        self.assertEquals([],opendayofweek(np.array([])).tolist())
        self.assertEquals([1,1,0,0,0,0,1,0,0,1],opendayofweek(np.array([5,1,2,3,4,5,1,2,3,1])).tolist())
        self.assertEquals([1,1,0,0,0,0,1,0,0,1],oofw(np.array([5,1,2,3,4,5,1,2,3,1])).tolist())        



if __name__ == "__main__":
    import logging
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    unittest.main()

