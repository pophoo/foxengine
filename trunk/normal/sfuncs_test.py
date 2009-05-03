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
        s = BaseObject(code='SH00TEST',transaction=trans,silver=g,g5=g,g20=g,g60=g,g120=g,g250=g,ma10=g,ma20=g,ma60=g,t120=g,above=g,golden=g,thumb=g,svap_ma_67=(g,vi),vap_ma_67=(g,vi))
        s.ref = s   #指向自己
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
    
    def test_gx250(self):
        sbuy = gx250(self.stock)
        self.assertTrue(True)

    def test_xgcs(self):
        sbuy = xgcs(self.stock)
        self.assertTrue(True)

    def test_xgcs0(self):
        sbuy = xgcs0(self.stock)
        self.assertTrue(True)

    def test_gcs(self):
        sbuy = gcs(self.stock)
        self.assertTrue(True)


if __name__ == "__main__":
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    unittest.main()

