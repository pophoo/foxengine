# -*- coding: utf-8 -*-

import unittest

import numpy as np
from wolfox.fengine.core.future import * 

class ModuleTest(unittest.TestCase):
    def test_mm_ratio(self):
        shigh = np.array([200,250,200,400])
        slow = np.array([100,200,100,200])
        sclose = np.array([150,220,180,300])
        amfe,amae = mm_ratio(sclose,shigh,slow,2,1)
        self.assertEquals([700,800,0,0],amfe.tolist())
        self.assertEquals([-300,400,0,0],amae.tolist())        
        #self.assertEquals([100,100,120,250],atr(sclose,shigh,slow,1).tolist())
        


if __name__ == "__main__":
    import logging
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    unittest.main()

