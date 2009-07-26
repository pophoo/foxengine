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


import wolfox.fengine.core.cruiser.customcruiser as ccruiser
from wolfox.fengine.core.shortcut import *

logger = logging.getLogger('wolfox.fengine.core.cruiser.customcruiser_test')

class ModuleTest(unittest.TestCase):    #通过性测试,纳入测试的目的是保持geneticcruiser的有效性
    def test_ma2s_cruiser(self):
        begin,end = 20010101,20010201
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        ccruiser.prepare_next(sdata,idata,catalogs)
        cruiser = ccruiser.Ma2sCruiser(psize=20,maxstep=1,goal=20000)
        cruiser.gcruise(sdata,dates,20010601)    
    
    def test_tsvama2_cruiser(self):
        begin,end = 20010101,20010201
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        ccruiser.prepare_next(sdata,idata,catalogs)
        cruiser = ccruiser.TSvama2Cruiser(psize=20,maxstep=1,goal=20000)
        cruiser.gcruise(sdata,dates,20010601)    

    def test_tsvama2sb_cruiser(self):
        begin,end = 20010101,20010201
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        ccruiser.prepare_next(sdata,idata,catalogs)
        cruiser = ccruiser.TSvama2sbCruiser(psize=20,maxstep=1,goal=20000)
        cruiser.gcruise(sdata,dates,20010601)    

    def test_emv1_cruiser(self):
        begin,end = 20010101,20010201
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        ccruiser.prepare_next(sdata,idata,catalogs)
        cruiser = ccruiser.Emv1Cruiser(psize=20,maxstep=1,goal=20000)
        cruiser.gcruise(sdata,dates,20010601)    
    
    def test_emv2_cruiser(self):
        begin,end = 20010101,20010201
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        ccruiser.prepare_next(sdata,idata,catalogs)
        cruiser = ccruiser.Emv2Cruiser(psize=20,maxstep=1,goal=20000)
        cruiser.gcruise(sdata,dates,20010601)    

    def test_tsvama4_cruiser(self):
        begin,end = 20010101,20010201
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        ccruiser.prepare_next(sdata,idata,catalogs)
        cruiser = ccruiser.TSvama4Cruiser(psize=20,maxstep=1,goal=20000)
        cruiser.gcruise(sdata,dates,20010601)    
 
    def test_tsvama3_cruiser(self):
        begin,end = 20010101,20010201
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        ccruiser.prepare_next(sdata,idata,catalogs)
        cruiser = ccruiser.TSvama3Cruiser(psize=20,maxstep=1,goal=20000)
        cruiser.gcruise(sdata,dates,20010601)    

    def test_tsvama3b_cruiser(self):
        begin,end = 20010101,20010201
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        ccruiser.prepare_next(sdata,idata,catalogs)
        cruiser = ccruiser.TSvama3bCruiser(psize=20,maxstep=1,goal=20000)
        cruiser.gcruise(sdata,dates,20010601)    

    def test_svama3_cruiser(self):
        begin,end = 20010101,20010201
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        ccruiser.prepare_next(sdata,idata,catalogs)
        d_posort('g5',sdata.values(),distance=5)        
        d_posort('g20',sdata.values(),distance=20)    
        d_posort('g120',sdata.values(),distance=120)     
        d_posort('g250',sdata.values(),distance=250)     
        cruiser = ccruiser.Svama3Cruiser(psize=20,maxstep=1,goal=20000)
        cruiser.gcruise(sdata,dates,20010601)    

    def test_svama3_mm_cruiser(self):
        begin,end = 20010101,20010201
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        ccruiser.prepare_next(sdata,idata,catalogs)
        d_posort('g5',sdata.values(),distance=5)        
        d_posort('g20',sdata.values(),distance=20)    
        d_posort('g120',sdata.values(),distance=120)     
        d_posort('g250',sdata.values(),distance=250)     
        cruiser = ccruiser.Svama3MMCruiser(psize=20,maxstep=1,goal=20000)
        cruiser.gcruise(sdata,dates,20010601)    
    
    def test_svama3b_mm_cruiser(self):
        begin,end = 20010101,20010201
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        ccruiser.prepare_next(sdata,idata,catalogs)
        d_posort('g5',sdata.values(),distance=5)        
        d_posort('g20',sdata.values(),distance=20)    
        d_posort('g120',sdata.values(),distance=120)     
        d_posort('g250',sdata.values(),distance=250)     
        cruiser = ccruiser.Svama3bMMCruiser(psize=20,maxstep=1,goal=20000)
        cruiser.gcruise(sdata,dates,20010601)    

    def test_svama2_mm_cruiser(self):
        begin,end = 20010101,20010201
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        ccruiser.prepare_next(sdata,idata,catalogs)
        d_posort('g5',sdata.values(),distance=5)        
        d_posort('g20',sdata.values(),distance=20)    
        d_posort('g120',sdata.values(),distance=120)     
        d_posort('g250',sdata.values(),distance=250)     
        cruiser = ccruiser.Svama2MMCruiser(psize=20,maxstep=1,goal=20000)
        cruiser.gcruise(sdata,dates,20010601)    

    def test_svama2b_mm_cruiser(self):
        begin,end = 20010101,20010201
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        ccruiser.prepare_next(sdata,idata,catalogs)
        d_posort('g5',sdata.values(),distance=5)        
        d_posort('g20',sdata.values(),distance=20)    
        d_posort('g120',sdata.values(),distance=120)     
        d_posort('g250',sdata.values(),distance=250)     
        cruiser = ccruiser.Svama2bMMCruiser(psize=20,maxstep=1,goal=20000)
        cruiser.gcruise(sdata,dates,20010601)    

    def test_csvama3_mm_cruiser(self):
        begin,end = 20010101,20010201
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        ccruiser.prepare_next(sdata,idata,catalogs)
        d_posort('g5',sdata.values(),distance=5)        
        d_posort('g20',sdata.values(),distance=20)    
        d_posort('g120',sdata.values(),distance=120)     
        d_posort('g250',sdata.values(),distance=250)     
        cruiser = ccruiser.CSvama3MMCruiser(psize=20,maxstep=1,goal=20000)
        cruiser.gcruise(sdata,dates,20010601)    

    def test_csvama2_mm_cruiser(self):
        begin,end = 20010101,20010201
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        ccruiser.prepare_next(sdata,idata,catalogs)
        d_posort('g5',sdata.values(),distance=5)        
        d_posort('g20',sdata.values(),distance=20)    
        d_posort('g120',sdata.values(),distance=120)     
        d_posort('g250',sdata.values(),distance=250)     
        cruiser = ccruiser.CSvama2MMCruiser(psize=20,maxstep=1,goal=20000)
        cruiser.gcruise(sdata,dates,20010601)    


    def test_svama2x_mm_cruiser(self):
        begin,end = 20010101,20010201
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        ccruiser.prepare_next(sdata,idata,catalogs)
        d_posort('g5',sdata.values(),distance=5)        
        d_posort('g20',sdata.values(),distance=20)    
        d_posort('g120',sdata.values(),distance=120)     
        d_posort('g250',sdata.values(),distance=250)     
        cruiser = ccruiser.Svama2xMMCruiser(psize=20,maxstep=1,goal=20000)
        cruiser.gcruise(sdata,dates,20010601)    

    def test_svama2s_mm_cruiser(self):
        begin,end = 20010101,20010201
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        ccruiser.prepare_next(sdata,idata,catalogs)
        d_posort('g5',sdata.values(),distance=5)        
        d_posort('g20',sdata.values(),distance=20)    
        d_posort('g120',sdata.values(),distance=120)     
        d_posort('g250',sdata.values(),distance=250)     
        cruiser = ccruiser.Svama2sMMCruiser(psize=20,maxstep=1,goal=20000)
        cruiser.gcruise(sdata,dates,20010601)    

    def test_Vama2_mm_cruiser(self):
        begin,end = 20010101,20010201
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        ccruiser.prepare_next(sdata,idata,catalogs)
        d_posort('g5',sdata.values(),distance=5)        
        d_posort('g20',sdata.values(),distance=20)    
        d_posort('g120',sdata.values(),distance=120)     
        d_posort('g250',sdata.values(),distance=250)     
        cruiser = ccruiser.Vama2MMCruiser(psize=20,maxstep=1,goal=20000)
        cruiser.gcruise(sdata,dates,20010601)    

    def test_Vama3_mm_cruiser(self):
        begin,end = 20010101,20010201
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        ccruiser.prepare_next(sdata,idata,catalogs)
        d_posort('g5',sdata.values(),distance=5)        
        d_posort('g20',sdata.values(),distance=20)    
        d_posort('g120',sdata.values(),distance=120)     
        d_posort('g250',sdata.values(),distance=250)     
        cruiser = ccruiser.Vama3MMCruiser(psize=20,maxstep=1,goal=20000)
        cruiser.gcruise(sdata,dates,20010601)    

    def test_Ma3_mm_cruiser(self):
        begin,end = 20010101,20010201
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        ccruiser.prepare_next(sdata,idata,catalogs)
        d_posort('g5',sdata.values(),distance=5)        
        d_posort('g20',sdata.values(),distance=20)    
        d_posort('g120',sdata.values(),distance=120)     
        d_posort('g250',sdata.values(),distance=250)     
        cruiser = ccruiser.Ma3MMCruiser(psize=20,maxstep=1,goal=20000)
        cruiser.gcruise(sdata,dates,20010601)    


if __name__ == "__main__":
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    unittest.main()    
