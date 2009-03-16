# -*- coding: utf-8 -*-

import sys
import time as stime
import unittest
import logging

import os
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    #准备测试环境
    from django.core.management import setup_environ
    import wolfox.foxit.other_settings.settings_sqlite_test as settings
    setup_environ(settings)


import wolfox.fengine.core.cruiser.geneticcruiser as gcruiser
from wolfox.fengine.core.shortcut import *

logger = logging.getLogger('wolfox.fengine.core.cruiser.geneticcruiser_test')

class ModuleTest(unittest.TestCase):    #通过性测试,纳入测试的目的是保持geneticcruiser的有效性
    def setUp(self):
        from StringIO import StringIO
        self.tmp = sys.stdout
        sys.stdout = StringIO()  #将标准I/O流重定向到buff对象，抑制输出

    def tearDown(self):
        sout = sys.stdout.getvalue()
        logger.debug(u'geneticcruiser测试控制台输出:%s',sout)
        sys.stdout = self.tmp        #恢复标准I/O流
        print sout
    
    def test_args2genes_genes2args(self): #不动点测试
        cruiser = ExampleGeneticCruiser(psize=16,maxstep=1)
        genes = cruiser.args2genes(dict(fast=32,slow=81))
        args = cruiser.genes2args(genes)
        self.assertEquals([32,81],args)

    def test_log_result_mm(self):
        cruiser = ExampleMMGeneticCruiser(psize=16,maxstep=1)
        cruiser.ev_result['test1'] = (10,11,11,11)
        cruiser.ev_result['test2'] = (11,10,10,10)
        cruiser.log_result()
        self.assertTrue(True)
        cruiser.ev_result['test3'] = 11
        self.assertRaises(ValueError,cruiser.log_result)

    def test_geneticcruiser(self):
        begin,end = 20010101,20010201
        dates = get_ref_dates(begin,end)
        codes = get_codes_startswith('SH600000')
        sdata = cs.get_stocks(codes,begin,end,ref_id)
        #idata = prepare_data(begin,end,'INDEX')

        from time import time
        d_posort('gorder',sdata.values(),distance=60)
        tbegin = time()
        cruiser = ExampleGeneticCruiser(psize=16,maxstep=1)
        cruiser.gcruise(sdata,dates,20010201)
        
        tend = time()
        print u'耗时: %s' % (tend-tbegin)
        logger.debug(u'耗时: %s' % (tend-tbegin))    

    def test_geneticcruiser_filtered(self):
        begin,end = 20010101,20010201
        dates = get_ref_dates(begin,end)
        codes = get_codes_startswith('SH600000')
        sdata = cs.get_stocks(codes,begin,end,ref_id)
        #idata = prepare_data(begin,end,'INDEX')

        from time import time
        d_posort('gorder',sdata.values(),distance=60)
        tbegin = time()
        cruiser = FilteredGeneticCruiser(psize=16,maxstep=1)
        cruiser.gcruise(sdata,dates,20010201)
        
        tend = time()
        print u'耗时: %s' % (tend-tbegin)
        logger.debug(u'耗时: %s' % (tend-tbegin))    


    def test_mm_geneticcruiser(self):
        begin,end = 20010101,20010201
        dates = get_ref_dates(begin,end)
        codes = get_codes_startswith('SH600000')
        sdata = cs.get_stocks(codes,begin,end,ref_id)
        #idata = prepare_data(begin,end,'INDEX')

        from time import time
        d_posort('gorder',sdata.values(),distance=60)
        tbegin = time()
        cruiser = ExampleMMGeneticCruiser(psize=16,maxstep=1)
        cruiser.gcruise(sdata,dates,20010201)
        
        tend = time()
        print u'耗时: %s' % (tend-tbegin)
        logger.debug(u'耗时: %s' % (tend-tbegin))    

    def test_mm_geneticcruiser(self):
        begin,end = 20010101,20010201
        dates = get_ref_dates(begin,end)
        codes = get_codes_startswith('SH600000')
        sdata = cs.get_stocks(codes,begin,end,ref_id)
        #idata = prepare_data(begin,end,'INDEX')

        from time import time
        d_posort('gorder',sdata.values(),distance=60)
        tbegin = time()
        cruiser = FilteredMMGeneticCruiser(psize=16,maxstep=1)
        cruiser.gcruise(sdata,dates,20010201)
        
        tend = time()
        print u'耗时: %s' % (tend-tbegin)
        logger.debug(u'耗时: %s' % (tend-tbegin))    

class ExampleGeneticCruiser(gcruiser.GeneticCruiser):
    def prepare(self):
        self.args = {'fast':range(2,49),'slow':range(5,129)}
        self.predefined = [dict(fast=12,slow=55),dict(fast=20,slow=120)]
        self.buy_func = buy_func_demo
        self.sell_func = my_csc_func
        #self.trade_func = fcustom(my_trade_func,begin=20010601)
        self.evaluate_func = normal_evaluate

class FilteredGeneticCruiser(gcruiser.GeneticCruiser):
    def prepare(self):
        self.args = {'fast':range(2,49),'slow':range(5,129)}
        self.predefined = [dict(fast=12,slow=55),dict(fast=20,slow=120)]
        self.buy_func = buy_func_demo
        self.sell_func = my_csc_func
        #self.trade_func = fcustom(my_trade_func,begin=20010601)
        self.evaluate_func = normal_evaluate

    def filtered(self,**kwargs):
        return True

class ExampleMMGeneticCruiser(gcruiser.MM_GeneticCruiser):
    def prepare(self):
        self.args = {'fast':range(2,49),'slow':range(5,129)}
        self.predefined = [dict(fast=12,slow=55),dict(fast=20,slow=120)]
        self.buy_func = buy_func_demo
        self.sell_func = my_csc_func    #无用
        #self.trade_func = fcustom(my_trade_func,begin=20010601)
        self.evaluate_func = normal_evaluate

class FilteredMMGeneticCruiser(gcruiser.MM_GeneticCruiser):
    def prepare(self):
        self.args = {'fast':range(2,49),'slow':range(5,129)}
        self.predefined = [dict(fast=12,slow=55),dict(fast=20,slow=120)]
        self.buy_func = buy_func_demo
        self.sell_func = my_csc_func    #无用
        #self.trade_func = fcustom(my_trade_func,begin=20010601)
        self.evaluate_func = normal_evaluate
    
    def filtered(self,**kwargs):
        return True

def buy_func_demo(stock,fast,slow,extend_days = 20,**kwargs):
    logger.debug('calc: %s ' % stock.code)
    t = stock.transaction
    rev = np.ones_like(t[CLOSE])
    rev = [1 if i/3==0 else 0 for i in xrange(len(t[CLOSE]))]
    return np.array(rev)


#两个空桩基
def my_csc_func(stock,buy_signal,threshold=75,**kwargs):   #kwargs目的是吸收无用参数，便于cruiser
    return np.roll(buy_signal,1)

def my_trade_func(dates,stock,sbuy,ssell,begin=0,taxrate=125,**kwargs):  #kwargs目的是吸收无用参数，便于cruiser
    return []



if __name__ == "__main__":
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    unittest.main()    
