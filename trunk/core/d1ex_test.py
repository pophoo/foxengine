# -*- coding: utf-8 -*-

import unittest
from wolfox.fengine.core.d1ex import * 

class ModuleTest(unittest.TestCase):
    def test_ma(self):
        a= np.array([1,2,3,4,5,6,7,8,9,0])
        av = ma(a,3)
        self.assertEquals([0, 0, 2, 3, 4, 5, 6, 7, 8, 6],av.tolist())

    def test_nma(self):
        a= np.array([1,2,3,4,5,6,7,8,9,0])
        av = nma(a,3)
        self.assertEquals([1, 2, 2, 3, 4, 5, 6, 7, 8, 6],av.tolist())

    def test_trend(self):
        a = np.array([1,2,3,2,2,10,2,10,10,4])
        self.assertEquals([0,1,1,-1,0,1,-1,1,0,-1],trend(a).tolist())

    def test_strend(self):
        source = np.array([10,20,30,30,40,50,40,30,20,20,10,20])
        self.assertEquals([0,1,2,2,3,4,-1,-2,-3,-3,-4,1],strend(source).tolist())

    def test_cross(self):
        target = np.array([10,20,30,40,50,40,30,20,10,12,11,12])
        follow = np.array([5,15,35,41,60,50,25,26,8,12,13,12])
        self.assertEquals([0,0,1,0,0,0,-1,1,-1,0,1,0],cross(target,follow).tolist())
        #空测试
        cross(np.array([]),np.array([]))
        self.assertTrue(True)

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

    def test_extend2reverse(self):
        source = np.array([0,0,5,0,-5,0,0,0,0,0,1,0,0,3,0,0,-1,1,2,0,0,0,0,6,0])
        self.assertEquals([0,0,5,5,-5,-5,-5,-5,-5,-5,1,1,1,1,1,1,-1,1,1,1,1,1,1,1,1],extend2reverse(source).tolist())
        self.assertEquals([],extend2reverse(np.array([])).tolist())

    def test_extend2next(self):
        source = np.array([0,0,5,0,-5,0,0,0,0,0,1,0,0,3,0,0,-1,1,2,0,0,0,0,6,0])
        self.assertEquals([0,0,5,5,-5,-5,-5,-5,-5,-5,1,1,1,3,3,3,-1,1,2,2,2,2,2,6,6],extend2next(source).tolist())
        self.assertEquals([],extend2next(np.array([])).tolist())

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

    def test_rsum(self):
        self.assertEquals([],rsum(np.array([]),np.array([])).tolist())        
        source = np.array([10,20,30,40,50,60])
        signal = np.array([0,0,-1,0,1,0])
        self.assertEquals([10,30,30,70,50,110],rsum(source,signal).tolist())
        signal2 = np.array([1,0,-1,0,1,0])
        self.assertEquals([10,30,30,70,50,110],rsum(source,signal2).tolist())

    def test_ravg(self):
        self.assertEquals([],ravg(np.array([]),np.array([])).tolist())        
        source = np.array([10,20,30,40,50,60])
        signal = np.array([0,0,-1,0,1,0])
        self.assertEquals([10,15,30,35,50,55],ravg(source,signal).tolist())
        signal2 = np.array([1,0,-1,0,1,0])
        self.assertEquals([10,15,30,35,50,55],ravg(source,signal2).tolist())

    def test_rsub(self):
        self.assertEquals([],rsub(np.array([]),np.array([])).tolist())
        source = np.array([10,20,30,40,50,60])
        signal = np.array([0,0,-1,0,1,0])
        self.assertEquals([0,0,20,0,20,0],rsub(source,signal).tolist())
        signal2 = np.array([1,0,-1,0,1,0])
        self.assertEquals([0,0,20,0,20,0],rsub(source,signal2).tolist())

    def test_msum(self):
        self.assertEquals([],msum(np.array([]),2).tolist())
        self.assertEquals([0,0,60,90,120,150,180,210],msum(np.array([10,20,30,40,50,60,70,80]),3).tolist())  #normal,length < len(source)
        self.assertEquals([0,0,0,0,0,0,0,0],msum(np.array([10,20,30,40,50,60,70,80]),10).tolist())   #length > len(source)
        self.assertEquals([0,0,0,0,0,0,0,360],msum(np.array([10,20,30,40,50,60,70,80]),8).tolist())   #length = len(source)

    def test_msum2(self):
        self.assertEquals([],msum2(np.array([]),2).tolist())
        self.assertEquals([10,30,60,90,120,150,180,210],msum2(np.array([10,20,30,40,50,60,70,80]),3).tolist())  #normal,length < len(source)
        self.assertEquals([10,30,60,100,150,210,280,360],msum2(np.array([10,20,30,40,50,60,70,80]),10).tolist())   #length > len(source)
        self.assertEquals([10,30,60,100,150,210,280,360],msum2(np.array([10,20,30,40,50,60,70,80]),8).tolist())   #length = len(source)

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

    def test_derepeatc(self):
        self.assertEquals([0,3,0,0,0,0,1,0,23,0,0],derepeatc(np.array([0,3,4,-5,6,0,1,0,23,3,0])).tolist())
        self.assertEquals([0,3,0,-5,0,0,0,1,0,23,0,0],derepeatc(np.array([0,3,0,-5,6,0,0,1,0,23,3,0])).tolist())
        self.assertEquals([0,3,0,0,0,0,1,0,23,0,0],derepeatc(np.array([0,3,4,-5,6,0,1,0,23,3,0])).tolist())

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

    def test_transform(self):
        self.assertEquals([11,51,41,0,21,0,31],transform(np.array([11,21,31,41,51]),np.array([0,4,6,2,1]),7).tolist())
        self.assertEquals([11,51,41,0,61,0,31],transform(np.array([11,21,31,41,51,61]),np.array([0,4,6,2,1,4]),7).tolist())
        self.assertEquals([71,51,41,0,61,0,31],transform(np.array([0,21,31,41,51,61,71]),np.array([0,4,6,2,1,4,0]),7).tolist())
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


if __name__ == "__main__":
    import logging
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    unittest.main()

