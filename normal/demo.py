# -*- coding: utf-8 -*-

#完整的起始脚本

from wolfox.fengine.core.shortcut import *

import logging
logger = logging.getLogger('wolfox.fengine.normal.demo')    

def buy_func_demo1(stock):
    t = stock.transaction
    g = stock.gorder >= 7500
    cma_5 = d1e.ma(t[CLOSE],5)
    cma_22 = d1e.ma(t[CLOSE],22)
    cma_long = d1e.ma(t[CLOSE],60)
    c_5_22 = d1e.cross(cma_22,cma_5) > 0
    c_trend_22 = d1e.strend(cma_22) > 0
    c_trend_5 = d1e.strend(cma_5) > 0
    c_trend_long = d1e.strend(cma_long) > 0    
    #signal = gand(c_5_22,c_trend_22,c_trend_5)
    sbuy = gand(g,c_5_22,c_trend_22,c_trend_5,c_trend_long)
    return sbuy

def buy_func_demo2(stock,fast,mid,slow,extend_days = 10):
    logger.debug('calc: %s ' % stock.code)    
    t = stock.transaction
    ma_fast = ma(t[CLOSE],fast)
    ma_mid = ma(t[CLOSE],mid)
    ma_slow = ma(t[CLOSE],slow)
    trend_fast = trend(ma_fast) > 0
    trend_mid = trend(ma_mid) > 0    
    trend_slow = trend(ma_slow) > 0
    cross_fast_mid = band(cross(ma_mid,ma_fast),trend_fast)
    cross_fast_slow = band(cross(ma_slow,ma_fast),trend_fast)
    cross_mid_slow = band(cross(ma_slow,ma_mid),trend_mid)
    cross_fm_fs = sfollow(cross_fast_mid,cross_fast_slow,extend_days)
    confirm_cross = sfollow(cross_fm_fs,cross_mid_slow,extend_days)
    trend_standard = trend(ma(t[CLOSE],55)) > 0
    return band(trend_standard,confirm_cross)

def buy_func_demo3(stock,fast,slow,extend_days = 20):
    #print stock.code
    logger.debug('calc: %s ' % stock.code)
    t = stock.transaction
    g = stock.gorder >= 8500    
    signal_s = catalog_signal(stock.c60,8500,8500)  #kao.存在没有c60也就是不归属任何catalog的stock，直接异常
    #print stock.code,max(stock.gorder)
    svap,v2i = svap_ma(t[VOLUME],t[CLOSE],22)
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = trend(ma_svapfast) > 0
    trend_ma_svapslow = trend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))
    maslow = ma(t[CLOSE],55)
    ma120 = ma(t[CLOSE],120)
    trend_ma120 = trend(ma120) > 0
    sconfirm = upconfirm(t[OPEN],t[CLOSE],t[HIGH])
    down_up = downup(maslow,t[CLOSE],10,3)
    confirm_up = band(down_up,sconfirm)
    confirmed_signal = syntony(msvap,confirm_up,15)
    smmroc = swingin(t[HIGH],t[LOW],45,800)
    #return gand(confirmed_signal,trend_ma120,smmroc)
    return gand(g,confirmed_signal,trend_ma120,signal_s)

def demo(sdata,dates,idata=None):
    ctree = cs.get_catalog_tree(sdata,['DY','ZHY'])
    print ctree
    for s in ctree:
        print s.name
        for c in s.catalogs:
            print c.name
    catalogs = get_all_catalogs(ctree)
    print 'catalog number:',len(catalogs)
    #print [ str(c.name) for c in catalogs]

    for c in catalogs:
        print c.name
        for st in c.stocks:
            print st.code
    from time import time
    tbegin = time()

    for c in catalogs:  #计算板块指数
        c.transaction = [calc_index(c.stocks)] * 7  #以单一指数冒充所有，避免extract_collect错误
    
    c_posort('c60',catalogs,distance=60)
    d_posort('gorder',sdata.values(),distance=60)
    d_posort('gorder',catalogs,distance=60)

    #x20=[ band(k.gorder >= 7500,v >= 7500) for k,v in sdata[20].c60.items()]    #板块全局>7500并且在板块内的排序>7500
    #gor(*x20)   #是否存在某个板块序>7500并且块内排序>7500
    #svs = sdata.values()
    #print dir(svs[0])
    #print svs[0].c60
    #template(sdata,dates,buy_func_demo1,csc_func,trade_func)
    demo2 = fcustom(buy_func_demo2,fast=4,mid=20,slow=75)
    #name =  names(demo2,csc_func,normal_trade_func)    
    #trades = normal_calc_template(sdata,dates,demo2,csc_func,normal_trade_func)
    #evs = normal_evaluate(trades)

    demo3 = fcustom(buy_func_demo3,fast=5,slow=98)
    
    trade_func = fcustom(normal_trade_func,begin=20010601)  #交易起始交易时间

    name =  names(demo3,csc_func,trade_func)
    trades = normal_calc_template(sdata,dates,demo3,csc_func,trade_func)    
    tend = time()
    print u'耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    
    evs2 = normal_evaluate(trades)
    print evs2.header()

if __name__ == '__main__':
    logging.basicConfig(filename="demo.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    begin,end = 20010101,20060101
    print 'start....'
    dates = get_ref_dates(begin,end)
    print 'dates finish....'
    #sdata = prepare_data(begin,end)
    #sdata = cs.get_stocks(['SH600503'],begin,end,ref_id)
    #sdata = cs.get_stocks(['SZ000655'],begin,end,ref_id)
    #print sdata[442].transaction[CLOSE]
    #sdata = cs.get_stocks(['SH600000'],begin,end,ref_id)
    codes = get_codes_startswith('SH600')
    sdata = cs.get_stocks(codes,begin,end,ref_id)    
    print 'sdata finish....'    
    #idata = prepare_data(begin,end,'INDEX')
    print 'idata finish....'    
    
    demo(sdata,dates)
