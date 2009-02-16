# -*- coding: utf-8 -*-

'''
    geneticcruiser的应用
'''

import logging
import time as stime
from wolfox.fengine.core.utils import fcustom
from wolfox.fengine.core.cruiser.geneticcruiser import *
from wolfox.fengine.normal.funcs import *
from wolfox.fengine.core.shortcut import *

logger = logging.getLogger('wolfox.fengine.core.cruiser.customcruiser')

class Svama3Cruiser(GeneticCruiser):
    def prepare(self):
        self.args = dict(fast=range(1,49),mid=range(2,100),slow=range(5,260)
                ,sma=range(3,130),ma_standard=range(5,260),extend_days=range(5,36))
        self.buy_func = svama3
        #self.sell_func = csc_func
        self.sell_func = atr_seller
        self.predefined = [dict(fast=1,mid=2,slow=5,sma=3,ma_standard=5,extend_days=5)]
        #self.sell_func = my_csc_func
        #self.trade_func = fcustom(normal_trade_func,begin=20010601)
        #self.trade_func = fcustom(my_trade_func,begin=20010601)
        self.evaluate_func = normal_evaluate

class Svama3MMCruiser(MM_GeneticCruiser):
    def prepare(self):
        print 'prepare:'
        self.args = dict(fast=range(1,49),mid=range(2,100),slow=range(5,260)
                ,sma=range(3,130),ma_standard=range(5,260),extend_days=range(5,36))
        self.buy_func = svama3
        #self.sell_func = csc_func
        self.sell_func = atr_seller
        #self.predefined = [dict(fast=1,mid=2,slow=5,sma=3,ma_standard=5,extend_days=5)
        #        ,dict(fast=45,mid=76,slow=85,sma=51,ma_standard=65,extend_days=5)
        #        ,dict(fast=45,mid=76,slow=76,sma=51,ma_standard=65,extend_days=5)]
        self.predefined = [dict(fast=15,mid=94,slow=209,sma=24,ma_standard=202,extend_days=30)] * 16
        #self.sell_func = my_csc_func
        #self.trade_func = fcustom(normal_trade_func,begin=20010601)
        #self.trade_func = fcustom(my_trade_func,begin=20010601)
        self.evaluate_func = normal_evaluate


if __name__ == '__main__':
    logging.basicConfig(filename="custom_cruiser_mm.log",level=logging.DEBUG,format='#%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')

    begin,end = 20010701,20060101
    dates,sdata,idata,catalogs = prepare_all(begin,end,[],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH601988','SH600050'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH601988'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600050'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH601398'],[ref_code])        
    #dates,sdata,idata,catalogs = prepare_all(begin,end,get_codes(),[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,get_codes(source='SZSE'),[ref_code])
    import psyco
    psyco.full()

    d_posort('g5',sdata.values(),distance=5)        
    d_posort('g20',sdata.values(),distance=20)    
    d_posort('g120',sdata.values(),distance=120)     
    d_posort('g250',sdata.values(),distance=250)     
    #cruiser = Svama3MMCruiser(psize=100,maxstep=40,goal=20000)
    cruiser = Svama3MMCruiser(psize=16,maxstep=1,goal=20000)
    print 'before cruiser,array number:',get_obj_number(np.ndarray),',tuple number:',get_obj_number(tuple),',list number:',get_obj_number(list)
    cruiser.gcruise(sdata,dates,20010701)    
    print 'after cruiesr,array number:',get_obj_number(np.ndarray),',tuple number:',get_obj_number(tuple),',list number:',get_obj_number(list)    
