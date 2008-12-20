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

    def test_desync(self):
        s = np.array([1,0,0,1,0])
        v = np.array([100,200,300,400,500])
        self.assertEquals([100,400],desync(v,s).tolist())
        s2 = np.array([400,0,0,500,0])
        self.assertEquals([100,400],desync(v,s2).tolist())
        s3 = np.array([400,0,0,-500,0])
        self.assertEquals([100,400],desync(v,s3).tolist())

    def test_right_roll(self):
        self.assertEquals([1,2,3,4,5],right_roll(np.array([1,2,3,4,5]),0).tolist())
        self.assertEquals([0,0,1,2,3],right_roll(np.array([1,2,3,4,5]),2).tolist())
        self.assertEquals([0,0,0,0,0],right_roll(np.array([1,2,3,4,5]),5).tolist())
        self.assertEquals([0,0,0,0,0],right_roll(np.array([1,2,3,4,5]),8).tolist())
        try:
            self.assertEquals([0,0,0,0,0],right_roll(np.array([1,2,3,4,5]),-2).tolist())
        except AssertionError,inst:
            self.assertTrue(True)
            #print type(inst)
        else:
            self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()

