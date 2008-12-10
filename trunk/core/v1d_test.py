# -*- coding: utf-8 -*-

import unittest
from wolfox.fengine.core.v1d import * 

class ModuleTest(unittest.TestCase):
    def test_ma1(self):
        a= np.array([1,2,3,4,5,6,7,8,9,0])
        av = ma1(a,3)
        self.assertEquals(True,np.all(np.array([0, 0, 2, 3, 4, 5, 6, 7, 8, 6])==av))


if __name__ == "__main__":
    unittest.main()

