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
from wolfox.fengine.normal.run import prepare_order

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
        self.args = dict(fast=range(1,49),mid=range(2,100),slow=range(5,501,5)
                ,ma_standard=(10,22,55,67,120,250,500,800)
                ,extend_days=range(1,36,2)
                )
        self.buy_func = lambda stock,fast,mid,slow,ma_standard,extend_days,**kwargs:svama3(stock,fast,mid,slow,ma_standard,extend_days)
        #self.buy_func = lambda stock,fast,mid,slow,sma,ma_standard,extend_days,**kwargs:np.ones_like(stock.transaction[CLOSE])
        #kwargs用于吸收其它函数所需的参数
        #self.sell_func = csc_func
        self.sell_func = atr_seller
        #self.predefined = [dict(fast=1,mid=2,slow=5,sma=3,ma_standard=5,extend_days=5)
        #        ,dict(fast=45,mid=76,slow=85,sma=51,ma_standard=65,extend_days=5)
        #        ,dict(fast=45,mid=76,slow=76,sma=51,ma_standard=65,extend_days=5)
        #        ,dict(fast=15,mid=94,slow=209,sma=24,ma_standard=202,extend_days=30)]
        self.predefined = []
        #self.sell_func = my_csc_func
        #self.trade_func = fcustom(normal_trade_func,begin=20010601)
        #self.trade_func = fcustom(my_trade_func,begin=20010601)
        self.evaluate_func = normal_evaluate

class CSvama3MMCruiser(MM_GeneticCruiser):
    def prepare(self):
        print 'prepare:'
        self.args = dict(fast=range(1,49),mid=range(2,100),slow=range(5,501,5)
                ,rstart=range(0,10001,500)
                ,rend = range(500,10001,500)
                )
        self.buy_func = lambda stock,fast,mid,slow,rstart,rend,**kwargs:csvama3(stock,fast,mid,slow,rstart,rend)
        self.sell_func = atr_seller
        self.predefined = []
        self.evaluate_func = normal_evaluate

class Svama2MMCruiser(MM_GeneticCruiser):
    def prepare(self):
        print 'prepare:'
        self.args = dict(fast=range(1,49),slow=range(5,501,5)
                ,ma_standard=(10,22,55,67,120,250,500,800)
                )
        self.buy_func = lambda stock,fast,slow,ma_standard,**kwargs:svama2(stock,fast,slow,ma_standard)
        #kwargs用于吸收其它函数所需的参数
        self.sell_func = atr_seller
        self.predefined = []
        self.evaluate_func = normal_evaluate

class CSvama2MMCruiser(MM_GeneticCruiser):
    def prepare(self):
        print 'prepare:'
        self.args = dict(fast=range(1,49),slow=range(5,501,5)
                ,rstart=range(0,10001,500)
                ,rend = range(500,10001,500)
                )
        self.buy_func = lambda stock,fast,slow,rstart,rend,**kwargs:csvama2(stock,fast,slow,rstart,rend)
        #kwargs用于吸收其它函数所需的参数
        self.sell_func = atr_seller
        self.predefined = []
        self.evaluate_func = normal_evaluate

class Svama2cMMCruiser(MM_GeneticCruiser):
    def prepare(self):
        print 'prepare:'
        self.args = dict(fast=range(1,49),slow=range(5,501,5)
                ,ma_standard=(10,22,55,67,120,250,500,800)
                )
        self.buy_func = lambda stock,fast,slow,ma_standard,**kwargs:svama2c(stock,fast,slow,ma_standard)
        #kwargs用于吸收其它函数所需的参数
        self.sell_func = atr_seller
        self.predefined = []
        self.evaluate_func = normal_evaluate

class Svama2xMMCruiser(MM_GeneticCruiser):
    def prepare(self):
        print 'prepare:'
        self.args = dict(fast=range(1,49),slow=range(5,501,5)
                ,ma_standard=(10,22,55,67,120,250,500,800)
                ,base=range(8,250,2)
                )
        self.buy_func = lambda stock,fast,slow,base,ma_standard,**kwargs:svama2x(stock,fast,slow,base,ma_standard)
        #kwargs用于吸收其它函数所需的参数
        self.sell_func = atr_seller
        self.predefined = []
        self.evaluate_func = normal_evaluate

class Svama2sMMCruiser(MM_GeneticCruiser):
    def prepare(self):
        print 'prepare:'
        self.args = dict(fast=range(1,49),slow=range(5,501,5)
                ,ma_standard=(10,22,55,67,120,250,500,800)
                ,extend_days=range(1,36,2)
                )
        self.buy_func = lambda stock,fast,slow,ma_standard,extend_days,**kwargs:svama2s(stock,fast,slow,ma_standard,extend_days)
        #kwargs用于吸收其它函数所需的参数
        self.sell_func = atr_seller
        self.predefined = []
        self.evaluate_func = normal_evaluate

class Vama2MMCruiser(MM_GeneticCruiser):
    def prepare(self):
        print 'prepare:'
        self.args = dict(fast=range(1,49),slow=range(5,501,5)
                ,ma_standard=(10,22,55,67,120,250,500,800)
                )
        self.buy_func = lambda stock,fast,slow,ma_standard,**kwargs:vama2(stock,fast,slow,ma_standard)
        #kwargs用于吸收其它函数所需的参数
        self.sell_func = atr_seller
        self.predefined = []
        self.evaluate_func = normal_evaluate

class Vama2xMMCruiser(MM_GeneticCruiser):
    def prepare(self):
        print 'prepare:'
        self.args = dict(fast=range(1,49),slow=range(5,501,5)
                ,ma_standard=(10,22,55,67,120,250,500,800) 
                ,base=range(8,250,2)#,extend_days=range(0,36)
                )
        self.buy_func = lambda stock,fast,slow,base,ma_standard,**kwargs:vama2x(stock,fast,slow,base,ma_standard)
        #kwargs用于吸收其它函数所需的参数
        self.sell_func = atr_seller
        self.predefined = []
        self.evaluate_func = normal_evaluate

class Vama3MMCruiser(MM_GeneticCruiser):
    def prepare(self):
        print 'prepare:'
        self.args = dict(fast=range(1,49),mid=range(2,100),slow=range(5,501,5)
                ,ma_standard=(10,22,55,67,120,250,500,800)
                ,extend_days=range(1,36,2)
                )
        self.buy_func = lambda stock,fast,mid,slow,ma_standard,extend_days,**kwargs:vama3(stock,fast,mid,slow,ma_standard,extend_days)
        #kwargs用于吸收其它函数所需的参数
        self.sell_func = atr_seller
        self.predefined = []
        self.evaluate_func = normal_evaluate

class Ma3MMCruiser(MM_GeneticCruiser):
    def prepare(self):
        print 'prepare:'
        self.args = dict(fast=range(1,49),mid=range(2,100),slow=range(5,260)
                ,ma_standard=range(5,260,5)
                ,extend_days=range(1,36,2)
                )
        self.buy_func = lambda stock,fast,mid,slow,ma_standard,extend_days,**kwargs:ma3(stock,fast,mid,slow,ma_standard,extend_days)
        #kwargs用于吸收其它函数所需的参数
        self.sell_func = atr_seller
        self.predefined = []
        self.evaluate_func = normal_evaluate


if __name__ == '__main__':
    logging.basicConfig(filename="custom_cruiser_mm_1.log",level=logging.DEBUG,format='#%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')

    begin,end = 20000101,20050901
    tbegin = 20010801
    
    dates,sdata,idata,catalogs = prepare_all(begin,end,[],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH601988','SH600050'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH601988'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600050'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH601398'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SZ000630'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,get_codes(),[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,get_codes(source='SZSE'),[ref_code])
    import psyco
    psyco.full()

    prepare_order(sdata.values())
    prepare_order(catalogs)
    dummy_catalogs('catalog',catalogs)
    
    #cruiser = Svama3MMCruiser(psize=16,maxstep=1,goal=0)
    #cruiser = Svama3MMCruiser(psize=100,maxstep=50,goal=2000000)    #goal不能太小
    #cruiser = Svama2MMCruiser(psize=100,maxstep=50,goal=2000000)
    #cruiser = Svama2sMMCruiser(psize=100,maxstep=50,goal=200000000)
    #cruiser = Svama2xMMCruiser(psize=100,maxstep=50,goal=20000000)
    #cruiser = Svama2cMMCruiser(psize=100,maxstep=50,goal=20000000)
    #cruiser = Vama3MMCruiser(psize=100,maxstep=50,goal=200000000)
    #cruiser = Vama2MMCruiser(psize=100,maxstep=50,goal=20000000)
    #cruiser = Ma3MMCruiser(psize=100,maxstep=50,goal=200000000)
    #cruiser = Vama2xMMCruiser(psize=100,maxstep=50,goal=20000000)
    print 'before cruiser,array number:',get_obj_number(np.ndarray),',tuple number:',get_obj_number(tuple),',list number:',get_obj_number(list)
    
    logger.debug('*****************csvama3 begin**********************')
    cruiser = CSvama3MMCruiser(psize=100,maxstep=50,goal=200000000)    #goal不能太小
    cruiser.gcruise(sdata,dates,tbegin)
    logger.debug('*****************csvama2 begin********************')
    cruiser = CSvama2MMCruiser(psize=100,maxstep=50,goal=200000000)
    cruiser.gcruise(sdata,dates,tbegin)
    #logger.debug('*****************svama2s begin*******************')    
    #cruiser = Svama2sMMCruiser(psize=100,maxstep=50,goal=200000000)
    #cruiser.gcruise(sdata,dates,tbegin)
    #logger.debug('*****************svama2x begin*******************')    
    #cruiser = Svama2xMMCruiser(psize=100,maxstep=50,goal=20000000)
    #cruiser.gcruise(sdata,dates,tbegin)
    #logger.debug('*****************svama2c begin*******************')    
    #cruiser = Svama2cMMCruiser(psize=100,maxstep=50,goal=20000000)
    #cruiser.gcruise(sdata,dates,tbegin)
    #logger.debug('*****************vama3 begin*********************')    
    #cruiser = Vama3MMCruiser(psize=100,maxstep=50,goal=200000000)
    #cruiser.gcruise(sdata,dates,tbegin)
    #logger.debug('*****************vama2 begin*********************')    
    #cruiser = Vama2MMCruiser(psize=100,maxstep=50,goal=20000000)
    #cruiser.gcruise(sdata,dates,tbegin)
    #logger.debug('*****************vama2x begin********************')
    #cruiser = Vama2xMMCruiser(psize=100,maxstep=50,goal=20000000)
    #cruiser.gcruise(sdata,dates,tbegin)

    print 'after cruiesr,array number:',get_obj_number(np.ndarray),',tuple number:',get_obj_number(tuple),',list number:',get_obj_number(list)    
