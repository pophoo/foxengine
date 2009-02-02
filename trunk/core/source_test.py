# -*- coding: utf-8 -*-

import unittest
from wolfox.fengine.extern import * #准备环境
from wolfox.fengine.core.base import *
from wolfox.fengine.core.source import *


class ModuleTest(unittest.TestCase):
    def test_tuple2array(self):
        a = [(None,None,None,None,None,None,None),(None,None,None,None,None,None,None),(1,1,1,1,1,1,1),(2,2,2,2,2,2,2),(None,None,None,None,None,None,None),(4,4,4,4,4,4,4)]
        ta = tuple2array(a)
        self.assertEquals([1,1,1,2,2,4],ta[0].tolist())
        self.assertEquals([1,1,1,2,2,4],ta[4].tolist())        
        self.assertEquals([0,0,1,2,0,4],ta[5].tolist())        
        self.assertEquals([0,0,1,2,0,4],ta[6].tolist())
        tb = tuple2array([])
        self.assertEquals([[],[],[],[],[],[],[]],tb.tolist())

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
        sa = CommonObject(id=3,transaction=a)
        sb = CommonObject(id=3,transaction=b)
        #print a.transaction
        rev = extract_collect([sa,sb])
        self.assertEquals([[3,4],[13,14]],rev.tolist())
        rev_volume = extract_collect([sa,sb],VOLUME)
        self.assertEquals([[13,14],[113,114]],rev_volume.tolist())
        #print rev

    def test_extract_collect1(self):
        a = np.array([(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(13,14)])
        sa = CommonObject(id=3,transaction=a)
        #print a.transaction
        rev = extract_collect1(sa)
        self.assertEquals([3,4],rev.tolist())
        rev_volume = extract_collect1(sa,VOLUME)
        self.assertEquals([13,14],rev_volume.tolist())
        #print rev


class SourceDataTest(unittest.TestCase):    #与源数据相关的测试
    def test_get_ref_dates(self):
        dates = get_ref_dates(0,20090101,rcode=u'SH000001')
        #测试空数据
        dates = get_ref_dates(0,0,rcode=u'SH000001')
        self.assertTrue(True)

    def test_prepare_data(self):
        data = prepare_data(0,20090101,rcode=u'SH000001')
        data = prepare_data(0,0,rcode=u'SH000001')
        self.assertTrue(True)

    def test_get_codes(self):
        codes = get_codes()
        #测试空数据
        codes = get_codes('NULLXX')
        self.assertFalse(codes)
 
    def test_get_codes_startswith(self):
        codes = get_codes_startswith('SH')
        self.assertTrue(codes)
        #测试空数据
        codes = get_codes_startswith('NULLXX')
        self.assertFalse(codes)

    def test_get_stocks(self):
        codes = get_codes()
        stocks = get_stocks(codes,0,999999999)  #测试通路
        self.assertTrue(True)   
        #print [s.transaction for s in stocks.values()]
        #测试空的交易数据
        stocks = get_stocks(codes,0,0)
        self.assertFalse(stocks.values()[0].transaction)
        #测试空数据（没有代码集合）        
        stocks = get_stocks([],0,99999999)
        self.assertFalse(stocks)

    def test_get_catalog_tree(self):
        sdata = prepare_data(0,0,rcode=u'SH000001')        
        tree = get_catalog_tree(sdata)
        css = []
        [css.extend(cs.catalogs) for cs in tree]
        #print [ c.stocks for c in css]
        for c in css:
            self.assertTrue(c.stocks)   #都不是空的
            for s in c.stocks:
                self.assertTrue(isinstance(s,CDO))
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()

