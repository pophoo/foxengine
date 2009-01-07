# -*- coding: utf-8 -*-

import unittest
from wolfox.fengine.extern import * #准备环境
from wolfox.fengine.core.source import *

class ModuleTest(unittest.TestCase):
    def test_normailize(self):
        #通道测试
        na_null = normalize([])
        a = [(None,None,None,None,None,None,None),(None,None,None,None,None,None,None),(1,1,1,1,1,1,1),(2,2,2,2,2,2,2),(None,None,None,None,None,None,None),(4,4,4,4,4,4,4)]
        na = normalize(a)
        self.assertTrue(True)

    def test_normalize_body(self):
        a = [(1,1,1,1,1,1,1),(2,2,2,2,2,2,2),(None,None,None,None,None,None,None),(4,4,4,4,4,4,4)]
        normalize_body(a,0)
        self.assertEquals((2,2,2,2,2,0,0),a[2])

    def test_normalize_head_normal(self):
        a = [(None,None,None,None,None,None,None),(None,None,None,None,None,None,None),(1,1,1,1,1,1,1),(2,2,2,2,2,2,2),(None,None,None,None,None,None,None),(4,4,4,4,4,4,4)]
        ihead = normalize_head(a)
        self.assertEquals(2,ihead)
        self.assertEquals((1,1,1,1,1,0,0),a[0])
        self.assertEquals((1,1,1,1,1,0,0),a[1])

    def test_normalize_head_zero(self):
        a = [(None,None,None,None,None,None,None),(None,None,None,None,None,None,None),(None,None,None,None,None,None,None)]
        ihead = normalize_head(a)
        self.assertEquals(len(a),ihead)
        self.assertEquals((0,0,0,0,0,0,0),a[0])
        self.assertEquals((0,0,0,0,0,0,0),a[1])
        self.assertEquals((0,0,0,0,0,0,0),a[2])

    def test_normalize_head_border(self):
        a = [(None,None,None,None,None,None,None),(None,None,None,None,None,None,None),(1,1,1,1,1,1,1)]
        ihead = normalize_head(a)
        self.assertEquals(2,ihead)
        self.assertEquals((1,1,1,1,1,0,0),a[0])
        self.assertEquals((1,1,1,1,1,0,0),a[1])

    def test_extract_collect(self):
        a = np.array([(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(13,14)])
        b = np.array([(11,12),(13,14),(15,16),(17,18),(19,110),(111,112),(113,114)])
        c = np.array([a,b])
        rev = extract_collect(c)
        self.assertEquals([[3,4],[13,14]],rev.tolist())
        rev_volume = extract_collect(c,VOLUME)
        self.assertEquals([[13,14],[113,114]],rev_volume.tolist())
        #print rev


class SourceDataTest(unittest.TestCase):    #与源数据相关的测试
    def test_get_ref_dates(self):
        dates = get_ref_dates(0,20090101,rcode=u'SH000001')
        #测试空数据
        dates = get_ref_dates(0,0,rcode=u'SH000001')
        self.assertTrue(True)

    def test_prepare_data(self):
        data = prepare_data(0,20090101,rcode=u'SH000001')
        daga = prepare_data(0,0,rcode=u'SH000001')
        self.assertTrue(True)

    def test_get_codes(self):
        codes = get_codes()
        #测试空数据
        codes = get_codes('NULLXX')
        self.assertFalse(codes)
    
    def test_get_stocks(self):
        codes = get_codes()
        stocks = get_stocks(codes,0,999999999)
        #print [s.transaction for s in stocks.values()]
        #测试空的交易数据
        stocks = get_stocks(codes,0,0)
        self.assertFalse(stocks.values()[0].transaction)
        #测试空数据（没有代码集合）        
        stocks = get_stocks([],0,99999999)
        self.assertFalse(stocks)

    def test_get_catalog_tree(self):
        tree = get_catalog_tree()
        #css = []
        #[css.extend(cs.catalogs) for cs in tree]
        #print [ c.stocks for c in css]
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()

