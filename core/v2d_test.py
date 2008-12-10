# -*- coding: utf-8 -*-

import unittest
from wolfox.fengine.core.v2d import * 

class ModuleTest(unittest.TestCase):
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

    def test_ma2d(self):
        a= np.array([(1,2,3,4,5,6,7,8,9,0),(0,9,8,7,6,5,4,3,2,1)])
        av = ma2d(a,3)
        self.assertEquals([[0, 0, 2, 3, 4, 5, 6, 7, 8, 6],[0, 0, 6, 8, 7, 6, 5, 4, 3, 2]],av.tolist())


if __name__ == "__main__":
    unittest.main()

