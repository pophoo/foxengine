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
        self.predefined = [(1,2,5,3,5,5)]
        #self.sell_func = my_csc_func
        #self.trade_func = fcustom(normal_trade_func,begin=20010601)
        #self.trade_func = fcustom(my_trade_func,begin=20010601)
        self.evaluate_func = normal_evaluate

class Svama3MMCruiser(MM_GeneticCruiser):
    def prepare(self):
        self.args = dict(fast=range(1,49),mid=range(2,100),slow=range(5,260)
                ,sma=range(3,130),ma_standard=range(5,260),extend_days=range(5,36))
        self.buy_func = svama3
        #self.sell_func = csc_func
        self.sell_func = atr_seller
        self.predefined = [(1,2,5,3,5,5),(45,76,85,51,65,5),(45,76,76,51,65,5)]
        #self.sell_func = my_csc_func
        #self.trade_func = fcustom(normal_trade_func,begin=20010601)
        #self.trade_func = fcustom(my_trade_func,begin=20010601)
        self.evaluate_func = normal_evaluate


if __name__ == '__main__':
    logging.basicConfig(filename="custom_cruiser_mm.log",level=logging.DEBUG,format='#%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')

    begin,end = 20010101,20060101
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
    cruiser = Svama3MMCruiser(psize=50,maxstep=50,goal=20000)
    print 'before cruiser,array number:',get_obj_number(np.ndarray),',tuple number:',get_obj_number(tuple),',list number:',get_obj_number(list)
    cruiser.gcruise(sdata,dates,20010601)    
    print 'after cruiesr,array number:',get_obj_number(np.ndarray),',tuple number:',get_obj_number(tuple),',list number:',get_obj_number(list)    
