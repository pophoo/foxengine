# -*- coding: utf-8 -*-

#各类函数的快捷方式

import logging
from time import time

from wolfox.fengine.extern import *
from wolfox.fengine.internal import *
from wolfox.fengine.core.d1 import BASE
from wolfox.fengine.core.d1idiom import B0S0,B0S1,B1S0,B1S1,BS_DUMMY
from wolfox.fengine.core.trade import match_trades
from wolfox.fengine.core.base import cache

logger = logging.getLogger('wolfox.fengine.core.shortcut')

@cache
def cached_zeros(n):
    return np.zeros(n,int)

@cache
def cached_ints(n,v=1):
    return np.ones(n,int) * v

def csc_func(stock,buy_signal,threshold=75,**kwargs):   #kwargs目的是吸收无用参数，便于cruiser
    t = stock.transaction
    return d1id.confirmedsellc(buy_signal,t[OPEN],t[CLOSE],t[HIGH],t[LOW],threshold)

def create_evaluator():
    def efunc(trades,**kwargs):         #kwargs目的是吸收无用参数，便于cruiser
        return evaluate(trades)
    return efunc

normal_evaluate = create_evaluator()

def prepare_catalogs(sdata,distance=60):
    ctree = cs.get_catalog_tree(sdata,['DY','HY']) #证监会行业太过细分，不妥
    catalogs = get_all_catalogs(ctree)
    for c in catalogs:  #计算板块指数
        c.transaction = [calc_index(c.stocks)] * 7  #以单一指数冒充所有，避免extract_collect错误
    #print catalogs
    c_posort('c%s' % distance,catalogs,distance=distance)
    d_posort('g%s' % distance,catalogs,distance=distance)
    return ctree,catalogs   

def dlimit(stocks,limit):
    for s in stocks:
        s.transaction[OPEN][s.transaction[OPEN]<limit] = limit
        s.transaction[CLOSE][s.transaction[CLOSE]<limit] = limit
        s.transaction[HIGH][s.transaction[HIGH]<limit] = limit
        s.transaction[LOW][s.transaction[LOW]<limit] = limit
        s.transaction[AVG][s.transaction[AVG]<limit] = limit            

def prepare_all(begin,end,codes=[],icodes=[]):
    print 'start....'
    dates = get_ref_dates(begin,end)
    print 'dates finish....'
    if codes:
        sdata = cs.get_stocks(codes,begin,end,ref_id)
        dlimit(sdata.values(),600)
    else:
        sdata = prepare_data(begin,end)
        dlimit(sdata.values(),600)
        fdata = prepare_data(begin,end,'FUND')
        dlimit(fdata.values(),300)
        sdata.update(fdata)
    print 'sdata finish....'
    if icodes:
        idata = cs.get_stocks(icodes,begin,end,ref_id)
    else:
        idata = prepare_data(begin,end,'INDEX')
    print 'idata finish....'    
    ctree,catalogs = prepare_catalogs(sdata)    
    return dates,sdata,idata,catalogs    

def calc_trades(buyer,seller,sdata,dates,xbegin,cmediator=CNMediator10,**kwargs):
    m = cmediator(buyer,seller)
    name = m.name()
    tradess = m.calc_matched(sdata,dates,xbegin)
    return name,tradess

def batch(configs,sdata,dates,xbegin,**kwargs):
    for config in configs:
        try:
            tbegin = time()            
            buyer = config.buyer
            seller = config.seller
            pman = config.pman
            dman = config.dman
            name,tradess = calc_trades(buyer,seller,sdata,dates,xbegin,**kwargs)
            result,strade = ev.evaluate_all(tradess,pman,dman)
            config.name = name
            #config.mm = rate_mfe_mae(sdata)
            config.result = result
            config.strade = strade
            tend = time()
            logger.debug(u'strade:%s',strade)
            #logger.debug(u'\nMMRatio:%s,mfe:%s,mae:%s,mm_count:%s' % config.mm)
            logger.debug(u'calc finished:%s,耗时:%s',config.name,tend-tbegin)
            print u'calc finished:%s,耗时:%s' % (config.name,tend-tbegin)
        except Exception,inst:
            print 'batch error:',inst
            #import traceback
            #traceback.print_stack()
            logger.exception('batch error:buyer name=%s,seller name=%s',buyer.__name__,seller.__name__)

def batch_last(configs,sdata,dates,xbegin,cmediator=CNMediator10,**kwargs):
    ltrades = {}
    for config in configs:
        try:
            tbegin = time()            
            buyer = config.buyer
            seller = config.seller
            m = cmediator(buyer,seller)
            name = m.name()
            trades = m.calc_last(sdata,dates,xbegin)
            if trades:
                ltrades[name] = trades
            tend = time()
            logger.debug(u'calc_last finished:%s,耗时:%s',name,tend-tbegin)
            print u'calc_last finished:%s,耗时:%s' % (name,tend-tbegin)
        except Exception,inst:
            print 'batch_last error:',inst
            #import traceback
            #traceback.print_stack()
            logger.exception('batch_last error:buyer name=%s,seller name=%s',buyer.__name__,seller.__name__)
    return ltrades

def mm_batch(configs,sdata,dates,xbegin):
    for config in configs:
        try:
            tbegin = time()            
            buyer = config.buyer
            seller = config.seller
            pman = config.pman

            myMediator = MM_Mediator(buyer,seller)
            trades = myMediator.calc_matched(sdata,dates,begin=xbegin)
            mm = rate_mfe_mae(sdata)
            logger.debug('%s:mm:%s',myMediator.name(),mm)
            config.mm = mm
            config.name = myMediator.name()
            tend = time()            
            print u'mm_calc finished:%s,耗时:%s,mm=%s' % (config.name,tend-tbegin,mm)
        except Exception,inst:
            print 'mm_batch error:',inst
            #import traceback
            #traceback.print_stack()
            logger.exception('mm_batch error:buyer name=%s,seller name=%s',buyer.__name__,seller.__name__)

def merge(configs,sdata,dates,xbegin,pman,dman,**kwargs):
    merged_trades = []
    for config in configs:
        try:
            tbegin = time()            
            buyer = config.buyer
            seller = config.seller
            name,tradess = calc_trades(buyer,seller,sdata,dates,xbegin,**kwargs)
            merged_trades.extend(tradess)
            tend = time()
            logger.debug(u'merge finished:%s,耗时:%s',name,tend-tbegin)
            print u'merge_calc finished:%s,耗时:%s' % (name,tend-tbegin)            
        except Exception,inst:
            print 'merge error:',inst
            #import traceback
            #traceback.print_stack()
            logger.exception('batch error:buyer name=%s,seller name=%s',buyer.__name__,seller.__name__)
    result,strade = ev.evaluate_all(merged_trades,pman,dman)
    return result,strade

def rate_mfe_mae(sdata):
    sum_mfe,sum_mae = 0,0
    count_mm= 0
    for s in sdata.values():
        #if s.mfe_sum > 0: print s.code
        sum_mfe += s.mfe_sum
        sum_mae += s.mae_sum
        count_mm += s.mm_count
    if sum_mae:
        return (int(sum_mfe * BASE/sum_mae),sum_mfe,sum_mae,count_mm)
    elif sum_mae == sum_mfe:
        return (1,sum_mfe,sum_mae,count_mm)
    else:
        return (BASE * BASE * BASE,sum_mfe,sum_mae,count_mm)    #需要有明显差别

def save_configs(filename,configs,begin,end):
    f = file(filename,'a')
    f.write('\n\n\n------------------------------------------------------------------------------------------------------------')
    f.write('\n\nbegin=%s,end=%s' % (begin,end))
    f.write('\n\n------------------------------------------------------------------------------------------------------------')    
    for config in configs:
        r = config.result
        f.write('\nname:%s\npre_ev:%s\ngev:%s' % (config.name,r.pre_ev,r.g_ev))
        f.write('\nR:%s\nCSHARP:%s\nAVGRANGE:%s\nMAXRANGE:%s\nINRATE:%s' % (r.RPR,r.CSHARP,r.AVGRANGE,r.MAXRANGE,r.income_rate))
        #f.write('\nMMRatio:%s,mfe:%s,mae:%s,mm_count:%s' % config.mm)
        if abs(r.income_rate) > 0:
            f.write('\n%s' % config.strade)
        f.write('\n**************************************************')
    f.close()

def save_last(filename,dtrades,begin,end,dlast):
    f = file(filename,'a')
    f.write('\n\n\n------------------------------------------------------------------------------------------------------------')
    f.write('\n\nbegin=%s,end=%s,last_date=%s' % (begin,end,dlast))
    f.write('\n\n------------------------------------------------------------------------------------------------------------')    
    for name,trades in dtrades.items():
        f.write('\nname:%s\n' % name)
        for trade in trades:
            if trade.tdate >= dlast:
                f.write('%s\n' % unicode(trade))
        f.write('\n**************************************************')
    f.close()

def save_mm_configs(filename,configs,begin,end):
    f = file(filename,'a')
    f.write('\n\n\n------------------------------------------------------------------------------------------------------------')
    f.write('\n\nbegin=%s,end=%s' % (begin,end))
    f.write('\n\n------------------------------------------------------------------------------------------------------------')    
    for config in configs:
        f.write('\nname:%s\nmm:%s' % (config.name,config.mm))
    f.close()


def save_merged(filename,result,strade,begin,end):
    f = file(filename,'a')
    f.write('\n\n\n------------------------------------------------------------------------------------------------------------')
    f.write('\n\nbegin=%s,end=%s' % (begin,end))
    f.write('\n\n------------------------------------------------------------------------------------------------------------')    
    f.write('\nmerged:\npre_ev:%s\ngev:%s' % (result.pre_ev,result.g_ev))
    f.write('\nR:%s\nCSHARP:%s\nAVGRANGE:%s\nMAXRANGE:%s\nINRATE:%s' % (result.RPR,result.CSHARP,result.AVGRANGE,result.MAXRANGE,result.income_rate))
    f.write('\n%s' % strade)
    f.close()


#以下deprecated,使用Mediator替代
def normal_calc_template_deprecated(sdata,dates,buy_func,sell_func,trade_func):
    trades = []
    for s in sdata.values():
        try:    #捕捉某些异常，如未划入任何板块的股票在计算板块相关信号时会出错
            sbuy = buy_func(s)
            ssell = sell_func(s,sbuy)
            #sbuy,ssell = smooth2(s.transaction[VOLUME],sbuy,ssell) #这个处理被划入bMsN_trade_func中
            trades.extend(trade_func(dates,s,sbuy,ssell))
        except Exception,inst:
            print '%s except : %s' % (s.code,inst)
            logger.warning('%s calc error : %s',s.code,inst)
    return trades

def _trade_func_deprecated(dates,stock,sbuy,ssell,prepare_func,begin=0,taxrate=125,**kwargs):  #kwargs目的是吸收无用参数，便于cruiser
    ''' prepare_func是对sbuy和ssell进行预处理，如买卖都是次日交易则为B1S1 
    '''
    t = stock.transaction
    sbuy,ssell = prepare_func(t,sbuy,ssell)
    ssignal = make_trade_signal(sbuy,ssell)
    return make_trades(stock,ssignal,dates,t[CLOSE],t[CLOSE],begin,taxrate)


dummy_trade_func_deprecated = fcustom(_trade_func_deprecated,prepare_func=BS_DUMMY)  
b1s1_trade_func_deprecated = fcustom(_trade_func_deprecated,prepare_func=B1S1)  
b0s0_trade_func_deprecated = fcustom(_trade_func_deprecated,prepare_func=B0S0)
b0s1_trade_func_deprecated = fcustom(_trade_func_deprecated,prepare_func=B0S1)
b1s0_trade_func_deprecated = fcustom(_trade_func_deprecated,prepare_func=B1S0)
normal_trade_func_deprecated = b1s1_trade_func_deprecated   #一般情形买卖信号都是延后一日发生




