# -*- coding: utf-8 -*-

import unittest
from wolfox.fengine.core.v1d import * 

class ModuleTest(unittest.TestCase):
    def test_ma(self):
        a= np.array([1,2,3,4,5,6,7,8,9,0])
        av = ma(a,3)
        self.assertEquals([0, 0, 2, 3, 4, 5, 6, 7, 8, 6],av.tolist())

    def testTrend(self):
        a = np.array([1,2,3,2,2,10,2,10,10,4])
        self.assertEquals([0,1,1,-1,0,1,-1,1,0,-1],trend(a).tolist())

    def testSTrend(self):
        source = np.array([10,20,30,30,40,50,40,30,20,20,10,20])
        self.assertEquals([0,1,2,2,3,4,-1,-2,-3,-3,-4,1],strend(source).tolist())

    def testCross(self):
        target = np.array([10,20,30,40,50,40,30,20,10,12,11,12])
        follow = np.array([5,15,35,41,60,50,25,26,8,12,13,12])
        self.assertEquals([0,0,1,0,0,0,-1,1,-1,0,1,0],cross(target,follow).tolist())



if __name__ == "__main__":
    unittest.main()

