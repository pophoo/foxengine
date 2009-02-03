# -*- coding: utf-8 -*-

''' 
遗传算法寻优(使用BCell)
'''

import logging
import time
from math import log,ceil
from wolfox.fengine.core.utils import fcustom
from wolfox.fengine.core.cruiser.genetic import *
import wolfox.fengine.core.cruiser.genetichelper as helper
from bisect import bisect_left as locate

logger = logging.getLogger('wolfox.fengine.core.cruiser.geneticcruiser')

#关键评估量map. win/profit为正向收益，用于选择买入点. nwin/nprofit为逆向收益，用于选择卖空点或者判断危险指数
evmap = {'win':lambda ev : ev.winrate,'profit':lambda ev:ev.rateavg,'nwin': lambda ev : -ev.winrate,'nprofit':lambda ev:-ev.rateavg}  

class GeneticCruiser(object):  
    ''' 只接受无关参数的集合，内部采用BCell实现. 
        NCell/NCell2在ngeneticcruiser中实现(非常类似但除了makejudge之外都有微妙差别)
        CCell难以用于这种整数寻优中(可能只适用于小整数范围寻优或者字符代表策略的寻优)
    '''
    def __init__(self,evmode='profit',psize=100,maxstep=100):
        assert evmode in evmap
        self.prepare()   #准备argnames,argpool和template_func
        self.argnames = self.args.keys()
        self.argpool = self.args.values()
        self.bitgroups = [ helper.calc_bitnumber(len(sp)) for sp in self.argpool]
        self.celler = BCell    #这里只能是BCell
        #print self.argnames
        self.extractor = evmap[evmode]
        self.psize = psize
        self.maxstep = maxstep
        #self.crossover = helper.uniform_crossover   #可能被predefined_population用到
        self.crossover = helper.bitgroups_crossover_factory(self.bitgroups,helper.single_point_crossover_g)
        self.reproducer = helper.simple_reproducer_factory(0.85,0.1)
        self.selector = helper.roulette_wheel_selection_factory(self.reproducer.times_of_length)        
        self.ev_result = {}

    def gcruise(self,sdata,dates,tbegin):
        judge = self.makejudge(sdata,dates,tbegin,self.extractor,lambda ev : self.extractor(ev) >= 0)
        nature = Nature(judge,helper.nonlinear_rank,self.selector,self.reproducer,1001)
        population = self.predefined_population()
        population.extend(init_population_bc(self.celler,self.psize - len(population),sum(self.bitgroups),self.crossover))
        #print 'begin loop:',time.time()
        result,loops = nature.run(population,self.maxstep)
        #print 'end loop:',time.time()
        #print len(result),len(population)
        for cell in result:
            #print zip(self.argnames,self.genes2args(cell.genes))
            logger.debug('%s:%s',self.argnames,self.genes2args(cell.genes))

    def genes2args(self,genes):#将基因串转化为参数值
        ints = helper.bits2ints(self.bitgroups,genes)
        #print [len(pool) for pool in self.argpool],ints
        #print len(ints)
        args = []
        for i in xrange(len(ints)):
            curv = ints[i] % len(self.argpool[i])   #对应候选pool中的位置
            #print i,len(self.argpool[i]),ints[i],curv
            args.append(self.argpool[i][curv])
        #print 'ints:%s,args:%s' % (ints,args)
        return args

    def args2genes(self,args):#将参数值转化为基因串
        assert len(args) == len(self.bitgroups)
        genes = []
        for i in xrange(len(args)):
            pos = locate(self.argpool[i],args[i])   #必然可以找到
            #print 'bitgroups[i]/pos',self.bitgroups[i],pos
            genes.extend(helper.int2bits(pos,self.bitgroups[i]))
        return genes

    def makejudge(self,sdata,dates,tbegin,extractor,evthreshold = lambda ev : ev.rateavg >= 0):
        ''' evthreshold:记录详细ev的门限函数
        '''
        #print 'common judge','-' * 40
        @utils.memory_guard(debug=True,gtype=tuple,criterion=lambda t:len(t)==2 and t[0] == 'long_scalars' and not t[1])
        def judge(cell):
            begin = time.time()
            args = self.genes2args(cell.genes)
            self.calc(sdata,dates,tbegin,evthreshold,**dict(zip(self.argnames,args)))
            name,ev = self.calc(sdata,dates,tbegin,evthreshold,**dict(zip(self.argnames,args)))
            if(ev.count > 0):
                pass
                #logger.debug(repr(ev))
            rv = ev.count <=3 and judge.minev or extractor(ev)
            print rv,ev.count,zip(self.argnames,args)
            logger.debug('%s:%s:%s',name,ev.count,unicode(ev))
            #print 'array number:',get_obj_number(np.ndarray),',tuple number:',get_obj_number(tuple),',list number:',get_obj_number(list)
            #show_most_common_types()
            end = time.time()
            print u'judge 耗时',end-begin,begin,end
            return rv
        judge.minev = -1000
        return judge
    
    def predefined_population(self):
        ''' 设置预定义的子种群
            注意，这里的预定义子种群中每个基因组的值都是绝对参数值，需要转换成位置表示的索引值才能对应到genes
            比如 [10,11,21]对应于 (0,20),(10,100),(20,200)的参数范围时，实际的基因值应当是[10,1,1]
        '''
        geness = []
        for arggroup in self.predefined:
            geness.append(self.args2genes(arggroup))
        return init_population_bc_with_geness(self.celler,geness,self.crossover)

    def calc(self,sdata,dates,tbegin,evthreshold,**kwargs):
        buy_func = fcustom(self.buy_func,**kwargs)
        sell_func = fcustom(self.sell_func,**kwargs)
        trade_func = fcustom(self.trade_func,**kwargs)        
        name = names(buy_func,sell_func,trade_func)
        trades = normal_template(sdata,dates,buy_func,sell_func,trade_func)
        ev = self.evaluate_func(trades,**kwargs)  
        if(not evthreshold(ev)):
            ev.matchedtrades,ev.balances = [],[]    #相当于先删除。为保证ev的一致性而都赋为[]。否则str(ev)中的zip(...)会出错
        self.ev_result[name] = ev
        #print 'null list:',get_null_obj_number(list),',null tuple:',get_null_obj_number(tuple)
        return name,ev

from wolfox.fengine.core.shortcut import *
def buy_func_demo3(stock,fast,slow,extend_days = 20,**kwargs):
    #print stock.code
    logger.debug('calc: %s ' % stock.code)
    t = stock.transaction
    g = stock.gorder >= 8500    
    maslow = ma(t[CLOSE],55)
    ma120 = ma(t[CLOSE],120)
    svap,v2i = svap_ma(t[VOLUME],t[CLOSE],22)
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = trend(ma_svapfast) > 0
    trend_ma_svapslow = trend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))
    trend_ma120 = trend(ma120) > 0
    sconfirm = upconfirm(t[OPEN],t[CLOSE],t[HIGH])
    down_up = downup(maslow,t[CLOSE],10,3)
    confirm_up = band(down_up,sconfirm)
    confirmed_signal = syntony(msvap,confirm_up,15)
    smmroc = swingin(t[HIGH],t[LOW],45,800)
    return gand(confirmed_signal,trend_ma120,smmroc)

class ExampleGeneticCruiser(GeneticCruiser):
    def prepare(self):
        self.args = {'fast':range(2,49),'slow':range(5,129)}
        self.predefined = [(12,55),(20,120)]
        self.buy_func = buy_func_demo3
        self.sell_func = csc_func
        #self.sell_func = my_csc_func
        self.trade_func = fcustom(normal_trade_func,begin=20010601)
        #self.trade_func = fcustom(my_trade_func,begin=20010601)
        self.evaluate_func = normal_evaluate


if __name__ == '__main__':
    logging.basicConfig(filename="genetic_cruiser.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')

    begin,end = 20010101,20060101
    print 'start....'
    dates = get_ref_dates(begin,end)
    print 'dates finish....'
    #sdata = prepare_data(begin,end)
    #sdata = cs.get_stocks(['SH600503'],begin,end,ref_id)
    #sdata = cs.get_stocks(['SH600503','SH600000','SZ000001'],begin,end,ref_id)
    #print sdata[442].transaction[CLOSE]
    codes = get_codes_startswith('SH600000')
    sdata = cs.get_stocks(codes,begin,end,ref_id)
    print 'sdata finish....'    
    #idata = prepare_data(begin,end,'INDEX')
    print 'idata finish....'    

    from time import time
    tbegin = time()

    d_posort('gorder',sdata.values(),distance=60)
    #trade_func = fcustom(normal_trade_func,begin=20010601)  #交易初始时间
    cruiser = ExampleGeneticCruiser(psize=20,maxstep=2)
    cruiser.gcruise(sdata,dates,20010601)
    print 'array number:',get_obj_number(np.ndarray),',tuple number:',get_obj_number(tuple),',list number:',get_obj_number(list)
    tend = time()
    print u'耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    
    
    '''
    evs = cruiser.ev_result.items()
    evs.sort(key=lambda x:x[1],reverse=True)
    for name,ev in evs:
        #print name,unicode(ev)
        pass
    '''
