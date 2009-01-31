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
        self.assertEquals([-1,-2,4,3,4,3,2,1,0,-1,4,3,2,4,3,2,4,4,4,3,2,1,0,4,3],cover(source,4).tolist())

    def test_extend(self):
        source = np.array([0,0,5,0,-5,0,0,0,0,0,1,0,0,3,0,0,-1,1,2,0,0,0,0,6,0])
        self.assertEquals([0,0,5,5,-5,-5,-5,-5,0,0,1,1,1,3,3,3,-1,1,2,2,2,2,0,6,6],extend(source,4).tolist())

    def test_distance(self):
        source = np.array([0,0,5,0,-5,0,0,0,0,0,1,0,0,3,0,0,-1,1,2,0,0,0,0,6,0])
        self.assertEquals([1,2,0,1,0,1,2,3,4,5,0,1,2,0,1,2,0,0,0,1,2,3,4,0,1],distance(source).tolist())

    def test_rsum(self):
        source = np.array([10,20,30,40,50,60])
        signal = np.array([0,0,-1,0,1,0])
        self.assertEquals([10,30,30,70,50,110],rsum(source,signal).tolist())
        signal2 = np.array([1,0,-1,0,1,0])
        self.assertEquals([10,30,30,70,50,110],rsum(source,signal2).tolist())

    def test_ravg(self):
        source = np.array([10,20,30,40,50,60])
        signal = np.array([0,0,-1,0,1,0])
        self.assertEquals([10,15,30,35,50,55],ravg(source,signal).tolist())
        signal2 = np.array([1,0,-1,0,1,0])
        self.assertEquals([10,15,30,35,50,55],ravg(source,signal2).tolist())

    def test_rsub(self):
        source = np.array([10,20,30,40,50,60])
        signal = np.array([0,0,-1,0,1,0])
        self.assertEquals([0,0,30,0,20,0],rsub(source,signal).tolist())
        signal2 = np.array([1,0,-1,0,1,0])
        self.assertEquals([10,0,20,0,20,0],rsub(source,signal2).tolist())

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
        self.assertEquals([0,3,0,0,0,0,1,0,23,0,0],derepeat(np.array([0,3,4,-5,6,0,1,0,23,3,0])).tolist())
        self.assertEquals([0,3,0,0,0,0,0,1,0,0,0,0],derepeat(np.array([0,3,0,-5,6,0,0,1,0,23,3,0]),2).tolist())

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

    def test_gswing(self):
        base = np.array([10,10,10,10,10])
        self.assertEquals([0,2000,1000,500,3500],gswing(base,np.array([10,30,5,15,45])).tolist())
        self.assertEquals([0,2000,5000,2000,3500],gswing(base,np.array([10,30,5,15,45]),2).tolist())
        self.assertEquals([0,2000,5000,5000,8000],gswing(base,np.array([10,30,5,15,45]),3).tolist())
        base2 = np.array([20,20,20,20,20])
        self.assertEquals([1000,2000,3000,1000,3500],gswing(base,base2,np.array([10,30,5,15,45])).tolist())
        self.assertEquals([1000,2000,5000,3000,3500],gswing(base,base2,np.array([10,30,5,15,45]),2).tolist())
        self.assertEquals([1000,2000,5000,5000,8000],gswing(base,base2,np.array([10,30,5,15,45]),3).tolist())

    def test_swing2(self):
        slow = np.array([10,10,10,10,10,10])
        shigh = np.array([10,30,15,25,45,25])
        self.assertEquals([0,2000,500,1500,3500,1500],swing2(shigh,slow).tolist())
        self.assertEquals([0,2000,2000,1500,3500,3500],swing2(shigh,slow,2).tolist())
        self.assertEquals([0,2000,2000,2000,3500,3500],swing2(shigh,slow,3).tolist())

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


if __name__ == "__main__":
    unittest.main()

