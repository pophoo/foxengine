# -*- coding: utf-8 -*-

import unittest

from random import randint
import numpy as np

from wolfox.fengine.core.base import BaseObject
from wolfox.fengine.normal.funcs import *

import logging
logger = logging.getLogger('wolfox.fengine.normal.funcs_test')

class ModuleTest(unittest.TestCase):    #通路测试
    def setUp(self):
        #prepare data
        sopen = np.array([randint(10000,15000) for i in range(2000)])
        sclose = np.array([randint(10000,15000) for i in range(2000)])
        svolume = np.array([randint(1000,15000) for i in range(2000)])
        shigh = np.max(np.array([sopen,sclose]),axis=0)
        slow = np.max(np.array([sopen,sclose]),axis=0)
        savg = sopen + sclose / 2
        samount = svolume * sopen /1000
        trans = [sopen,sclose,svolume,shigh,savg,samount,svolume]
        g5 = np.array([randint(0,10000) for i in range(2000)])
        g20 = np.array([randint(0,10000) for i in range(2000)])
        g60 = np.array([randint(0,10000) for i in range(2000)])
        g120 = np.array([randint(0,10000) for i in range(2000)])
        g250 = np.array([randint(0,10000) for i in range(2000)])        
        s = BaseObject(code='SH00TEST',transaction=trans,g5=g5,g20=g20,g60=g60,g120=g120,g250=g250)
        s.catalog = {s:g5}
        self.stock = s

    def test_ma3(self):
        sbuy = ma3(self.stock,5,20,120)
        self.assertTrue(True)

    def test_svama2(self):
        sbuy = svama2(self.stock,5,20)
        self.assertTrue(True)

    def test_svama2s(self):
        sbuy = svama2s(self.stock,5,20)
        self.assertTrue(True)

    def test_svama3(self):
        sbuy = svama3(self.stock,5,20,120)
        self.assertTrue(True)
    
    def test_vama2(self):
        sbuy = vama2(self.stock,5,20)
        self.assertTrue(True)
    
    def test_vama3(self):
        sbuy = vama3(self.stock,5,20,120)
        self.assertTrue(True)

    def test_svama3_x(self):
        sbuy = svama3_x(self.stock,5,20,120)
        self.assertTrue(True)

if __name__ == "__main__":
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    unittest.main()

