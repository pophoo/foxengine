# -*- coding: utf-8 -*-

import unittest

from hreader import *

class IF_PREPARER_Test(unittest.TestCase):
    def test_pd(self):
        xtimes = [1,2,3,4,5,1,2,3,2,1,2,3]
        self.assertEquals([],IF_PREPARER.pd([]))
        self.assertEquals([(5,7),(8,8),(9,11)],IF_PREPARER.pd(xtimes))

    def test_p3(self):
        self.assertEquals([],IF_PREPARER.p3([]))
        self.assertEquals([(4,6),(7,9),(10,12)],IF_PREPARER.p3(range(914,929)))
        self.assertEquals([(4,6),(7,10),(11,13),(14,17),(18,20)],IF_PREPARER.p3(range(914,922)+range(1509,1515)+range(914,922)))        
        self.assertEquals([(0,3),(4,6),(7,9),(10,12)],IF_PREPARER.p3(range(953,960)+range(1000,1008)))
        self.assertEquals([(0,3),(4,6),(7,9),(10,12)],IF_PREPARER.p3(range(953,960)+range(1000,1006)))

    def test_p5(self):
        self.assertEquals([],IF_PREPARER.p5([]))
        self.assertEquals([(6,10)],IF_PREPARER.p5(range(914,929)))
        self.assertEquals([(6,8),(9,13),(14,19)],IF_PREPARER.p5(range(914,922)+range(1509,1515)+range(914,922)))        
        self.assertEquals([(0,6),(7,11)],IF_PREPARER.p5(range(953,960)+range(1000,1008)))
        self.assertEquals([(0,6),(7,11)],IF_PREPARER.p5(range(953,960)+range(1000,1005)))

    def test_p15(self):
        self.assertEquals([],IF_PREPARER.p15([]))
        self.assertEquals([(16,30),(31,45)],IF_PREPARER.p15(range(914,961)))
        self.assertEquals([(16,30),(31,37),(38,53),(54,68)],IF_PREPARER.p15(range(914,946)+range(1509,1515)+range(914,946)))        
        self.assertEquals([(5,19),(20,34)],IF_PREPARER.p15(range(940,960)+range(1000,1018)))
        self.assertEquals([(5,19),(20,34)],IF_PREPARER.p15(range(940,960)+range(1000,1015)))

    def test_p30(self):
        self.assertEquals([],IF_PREPARER.p30([]))
        self.assertEquals([(31,60),(61,90),(91,120)],IF_PREPARER.p30(range(914,960)+range(1000,1060)+range(1100,1120)))
        self.assertEquals([(31,51),(52,82)],IF_PREPARER.p30(range(914,960)+range(1509,1515)+range(914,960))) 
        self.assertEquals([(31,60),(61,90),(91,120)],IF_PREPARER.p30(range(914,960)+range(1000,1060)+range(1100,1115)))


if __name__ == "__main__":
    import logging
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    unittest.main()

