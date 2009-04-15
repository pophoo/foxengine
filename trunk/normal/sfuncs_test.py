# -*- coding: utf-8 -*-

import unittest

from random import randint
import numpy as np

from wolfox.fengine.core.base import BaseObject
from wolfox.fengine.normal.sfuncs import *

import logging
logger = logging.getLogger('wolfox.fengine.normal.funcs_test')

class ModuleTest(unittest.TestCase):    #通路测试
    def setUp(self):
        #prepare data
        sopen = sclose = svolume = shigh = slow = savg = samount = np.array([randint(10000,15000) for i in range(2000)])
        trans = [sopen,sclose,svolume,shigh,savg,samount,svolume]
        vi = np.array([i for i in range(2000)])
        g = np.array([randint(0,10000) for i in range(2000)])
        s = BaseObject(code='SH00TEST',transaction=trans,g5=g,g20=g,g60=g,g120=g,g250=g,ma10=g,ma20=g,ma60=g,t120=g,above=g,golden=g,thumb=g,svap_ma_67=(g,vi),vap_ma_67=(g,vi))
        s.silver = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=6600)
        s.catalog = {s:g}
        s.c60 = {s:g}
        self.stock = s

    def test_tsvama2(self):
        sbuy = tsvama2(self.stock,5,20)
        self.assertTrue(True)

    def test_pmacd(self):
        sbuy = pmacd(self.stock)
        self.assertTrue(True)

    def test_nhigh(self):
        sbuy = nhigh(self.stock)
        self.assertTrue(True)
    
    def test_xma60(self):
        sbuy = xma60(self.stock)
        self.assertTrue(True)

    def test_wvad(self):
        sbuy = wvad(self.stock)
        self.assertTrue(True)

    def test_temv(self):
        sbuy = temv(self.stock)
        self.assertTrue(True)

    def test_vmacd_ma4(self):
        sbuy = vmacd_ma4(self.stock)
        self.assertTrue(True)

    def test_ma4(self):
        sbuy = ma4(self.stock)
        self.assertTrue(True)

    def test_vmacd(self):
        sbuy = vmacd(self.stock)
        self.assertTrue(True)

    def test_gx60(self):
        sbuy = gx60(self.stock)
        self.assertTrue(True)
    
    def test_gx120(self):
        sbuy = gx120(self.stock)
        self.assertTrue(True)


if __name__ == "__main__":
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    unittest.main()

