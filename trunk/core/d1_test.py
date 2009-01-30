# -*- coding: utf-8 -*-

import unittest
from wolfox.fengine.core.d1 import * 

class ModuleTest(unittest.TestCase):
    def test_gand(self):
        a = np.array([10,0,-3,0,1])
        b = np.array([3,0,0,-1,1])
        c = np.array([1,0,3,3,-1])
        self.assertEquals([1,0,1,0,1],gand(a).tolist())
        self.assertEquals([1,0,0,0,1],gand(a,b).tolist())
        self.assertEquals([1,0,0,0,1],gand(a,b,c).tolist())
        self.assertEquals([0,0,1,0,1],gand(a,np.array([0,2,3,4,5])).tolist())

    def test_gor(self):
        a = np.array([10,0,-3,0,1])
        b = np.array([3,0,0,-1,0])
        c = np.array([1,0,3,3,-1])
        self.assertEquals([1,0,1,0,1],gand(a).tolist())         
        self.assertEquals([1,0,1,1,1],gor(a,b,c).tolist())
        a2 = np.array([10,0,-3,0,1])
        self.assertEquals([1,1,1,0,1],gor(a2,np.array([0,2,3,0,5])).tolist())

    def test_subd(self):
        a = np.array([1,2,3,4,5])
        self.assertEquals([0,1,1,1,1],subd(a).tolist())
        self.assertEquals([0,0,2,2,2],subd(a,2).tolist())

    def test_nsubd(self):
        a = np.array([1,2,3,4,5])
        self.assertEquals([1,1,1,1,1],nsubd(a).tolist())
        self.assertEquals([1,2,2,2,2],nsubd(a,2).tolist())

    def test_desync(self):
        s = np.array([1,0,0,1,0])
        v = np.array([100,200,300,400,500])
        self.assertEquals([100,400],desync(v,s).tolist())
        s2 = np.array([400,0,0,500,0])
        self.assertEquals([100,400],desync(v,s2).tolist())
        s3 = np.array([400,0,0,-500,0])
        self.assertEquals([100,400],desync(v,s3).tolist())

    def test_desyncs(self):
        #一般用法
        ss = np.array([0,1,0,1,0])
        vv = np.array([1,0,1,1,1])
        self.assertEquals([1,1],desyncs(vv,ss).tolist())
        vv = np.array([0,1,0,1,1])
        self.assertEquals([1,1],desyncs(vv,ss).tolist())
        vv = np.array([0,1,0,0,1])
        self.assertEquals([1,0],desyncs(vv,ss).tolist())
        #特别但是与desync相似的用法
        s = np.array([1,0,0,1,0])
        v = np.array([100,200,300,400,500])
        self.assertEquals([1,1],desyncs(v,s).tolist())
        s2 = np.array([400,0,0,500,0])
        self.assertEquals([1,1],desyncs(v,s2).tolist())
        s3 = np.array([400,0,0,-500,0])
        self.assertEquals([1,1],desyncs(v,s3).tolist())

    def test_sync(self):
        s = np.array([1,0,1,1,0])
        src = np.array([1,0,1])
        self.assertEquals([1,0,0,1,0],sync(src,s).tolist())
        src2 = np.array([0,0,0])
        self.assertEquals([0,0,0,0,0],sync(src2,s).tolist())
        src3 = np.array([1,1,1])
        self.assertEquals([1,0,1,1,0],sync(src3,s).tolist())

    def test_smooth(self):
        ss = np.array([0,1,0,1,0])
        vv = np.array([1,0,1,1,1])
        self.assertEquals([0,1,0,1,0],smooth(vv,ss).tolist())
        vv = np.array([0,1,0,1,1])
        self.assertEquals([0,1,0,1,0],smooth(vv,ss).tolist())
        vv = np.array([0,1,0,0,1])
        self.assertEquals([0,1,0,0,0],smooth(vv,ss).tolist())

    def test_roll0(self):
        #空转
        self.assertEquals([],roll0(np.array([]),0).tolist())
        self.assertEquals([],roll0(np.array([]),2).tolist())        
        #正常情形
        self.assertEquals([1,2,3,4,5],roll0(np.array([1,2,3,4,5]),0).tolist())
        self.assertEquals([0,0,1,2,3],roll0(np.array([1,2,3,4,5]),2).tolist())
        self.assertEquals([0,0,0,0,0],roll0(np.array([1,2,3,4,5]),5).tolist())
        self.assertEquals([0,0,0,0,0],roll0(np.array([1,2,3,4,5]),8).tolist())
        self.assertEquals([3,4,5,0,0],roll0(np.array([1,2,3,4,5]),-2).tolist())        
        self.assertEquals([2,3,4,5,0],roll0(np.array([1,2,3,4,5]),-1).tolist())
        self.assertEquals([0,0,0,0,0],roll0(np.array([1,2,3,4,5]),-6).tolist())

    def test_rolln(self):
        #空转
        self.assertEquals([],rolln(np.array([]),0).tolist())
        self.assertEquals([],rolln(np.array([]),2).tolist())        
        #正常情形
        self.assertEquals([1,2,3,4,5],rolln(np.array([1,2,3,4,5]),0).tolist())
        self.assertEquals([1,1,1,2,3],rolln(np.array([1,2,3,4,5]),2).tolist())
        self.assertEquals([1,1,1,1,1],rolln(np.array([1,2,3,4,5]),5).tolist())
        self.assertEquals([1,1,1,1,1],rolln(np.array([1,2,3,4,5]),8).tolist())
        self.assertEquals([3,4,5,5,5],rolln(np.array([1,2,3,4,5]),-2).tolist())        
        self.assertEquals([2,3,4,5,5],rolln(np.array([1,2,3,4,5]),-1).tolist())
        self.assertEquals([5,5,5,5,5],rolln(np.array([1,2,3,4,5]),-6).tolist())


if __name__ == "__main__":
    unittest.main()

