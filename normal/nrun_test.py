# -*- coding: utf-8 -*-

import unittest

import sys
import os
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    print 'prepare ....'
    #准备测试环境
    from django.core.management import setup_environ
    import wolfox.foxit.other_settings.settings_sqlite_test as settings
    setup_environ(settings)

from wolfox.fengine.core.shortcut import *  #因为已经设置了测试环境，所以这里因external导致的环境将不会设置
import wolfox.fengine.normal.nrun as run
from wolfox.fengine.normal.funcs import svama3

import logging
logger = logging.getLogger('wolfox.fengine.normal.run_test')

class ModuleTest(unittest.TestCase):    #保持run的有效性
    def setUp(self):
        from StringIO import StringIO
        self.tmp = sys.stdout
        sys.stdout = StringIO()  #将标准I/O流重定向到buff对象，抑制输出
        self.old_prepare_configs_A1200 = run.prepare_configs_A1200  #保存run.prepare_configs，因为run/run_mm将重写它
        self.old_prepare_configs_A2000 = run.prepare_configs_A2000  #保存run.prepare_configs，因为run/run_mm将重写它
        self.old_prepare_configs_A1 = run.prepare_configs_A1  #保存run.prepare_configs，因为run/run_mm将重写它
        self.old_prepare_configs_A2 = run.prepare_configs_A2 #保存run.prepare_configs，因为run/run_mm将重写它
        self.old_prepare_temp_configs = run.prepare_temp_configs #保存run.prepare_configs，因为run/run_mm将重写它

    def tearDown(self):
        sout = sys.stdout.getvalue()
        logger.debug(u'demo测试控制台输出:%s',sout)
        sys.stdout = self.tmp        #恢复标准I/O流
        #print sout
        run.prepare_configs_A1200 = self.old_prepare_configs_A1200
        run.prepare_configs_A2000 = self.old_prepare_configs_A2000
        run.prepare_configs_A1 = self.old_prepare_configs_A1
        run.prepare_configs_A2 = self.old_prepare_configs_A2        
        run.prepare_temp_configs = self.old_prepare_temp_configs

    def dummy_prepare_configs(self,seller,pman=None,dman=None):
        config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
        configs = []
        configs.append(config(buyer=fcustom(svama3,fast=6,mid=24,slow=49,sma=21,ma_standard=60,extend_days=13)))
        return configs

    def test_prepare_temp_configs(self):
        seller = atr_seller_factory(stop_times=2000,trace_times=3000)
        configs = run.prepare_temp_configs(seller)
        self.assertTrue(len(configs) >= 0)

    def test_prepare_configs_A1200(self):
        pman = AdvancedATRPositionManager()
        dman = DateManager(20010101,20040101)
        seller = atr_seller_factory(stop_times=2000,trace_times=3000)
        configs = run.prepare_configs_A1200(seller,pman,dman)
        self.assertTrue(len(configs) > 0)

    def test_prepare_configs_A2000(self):
        pman = AdvancedATRPositionManager()
        dman = DateManager(20010101,20040101)
        seller = atr_seller_factory(stop_times=2000,trace_times=3000)
        configs = run.prepare_configs_A2000(seller,pman,dman)
        self.assertTrue(len(configs) >=0)

    def test_prepare_configs_A0(self):
        pman = AdvancedATRPositionManager()
        dman = DateManager(20010101,20040101)
        seller = atr_seller_factory(stop_times=2000,trace_times=3000)
        configs = run.prepare_configs_A0(seller,pman,dman)
        self.assertTrue(len(configs) >= 0)

    def test_prepare_configs_A1(self):
        pman = AdvancedATRPositionManager()
        dman = DateManager(20010101,20040101)
        seller = atr_seller_factory(stop_times=2000,trace_times=3000)
        configs = run.prepare_configs_A1(seller,pman,dman)
        self.assertTrue(len(configs) >= 0)

    def test_prepare_configs_A2(self):
        pman = AdvancedATRPositionManager()
        dman = DateManager(20010101,20040101)
        seller = atr_seller_factory(stop_times=2000,trace_times=3000)
        configs = run.prepare_configs_A2(seller,pman,dman)
        self.assertTrue(len(configs) >= 0)

    def test_prepare_order(self):
        begin,end = 20010101,20010701
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        run.prepare_order(sdata.values())
        self.assertTrue(True)

    def test_prepare_common(self):
        begin,end = 20010101,20010701
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        run.prepare_order(sdata.values())        
        run.prepare_common(sdata.values(),idata[ref_id])
        self.assertTrue(True)

    def test_prepare_index(self):
        begin,end = 20010101,20010701
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        run.prepare_index(idata[1])        
        self.assertTrue(True)

    def test_run(self):
        begin,end = 20010101,20010701
        xbegin = 20010401
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        run.prepare_temp_configs = run.prepare_configs_A1200 = run.prepare_configs_A2000 = run.prepare_configs_A1 = run.prepare_configs_A2 = self.dummy_prepare_configs
        run.run_main(dates,sdata,idata,catalogs,begin,end,xbegin)        
        self.assertTrue(True)

    def test_run_last(self):
        begin,end = 20010101,20010701
        xbegin = 20010401
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        run.prepare_temp_configs = run.prepare_configs_A1200 = run.prepare_configs_A2000 = run.prepare_configs_A1 = run.prepare_configs_A2 = self.dummy_prepare_configs
        run.run_last(dates,sdata,idata,catalogs,begin,end,xbegin)        
        self.assertTrue(True)

    def test_run_merge(self):
        begin,end = 20010101,20010701
        xbegin = 20010401
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        run.prepare_temp_configs = run.prepare_configs_A1200 = run.prepare_configs_A2000 = run.prepare_configs_A1 = run.prepare_configs_A2 = self.dummy_prepare_configs
        run.run_merge_main(dates,sdata,idata,catalogs,begin,end,xbegin)        
        self.assertTrue(True)

    def test_catalog_macd(self):
        begin,end = 20010101,20010701
        xbegin = 20010401
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        run.catalog_macd(catalogs)
        self.assertTrue(True)


if __name__ == "__main__":
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    unittest.main()

