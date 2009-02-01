# -*- coding: utf-8 -*-

#完整的起始脚本

from wolfox.fengine.core.shortcut import *

logger = None

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
    logger.debug(stock.code)
    t = stock.transaction
    g = stock.gorder >= 7500    
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
    return gand(confirmed_signal,trend_ma120)

if __name__ == '__main__':
    import logging
    logging.basicConfig(filename="demo.log",level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger('wolfox.fengine.normal.demo')    
    begin,end = 20010101,20030101
    print 'start....'
    dates = get_ref_dates(begin,end)
    print 'dates finish....'
    sdata = prepare_data(begin,end)
    #sdata = cs.get_stocks(['SH600503'],begin,end,ref_id)
    #print sdata[442].transaction[CLOSE]
    print 'sdata finish....'    
    idata = prepare_data(begin,end,'INDEX')
    print 'idata finish....'    
    ctree = cs.get_catalog_tree(sdata)
    catalogs = get_all_catalogs(ctree)

    #c_posort('test',catalogs,distance=10)
    d_posort('gorder',sdata.values(),distance=60)
    #template(sdata,dates,buy_func_demo1,csc_func,trade_func)
    #demo2 = fcustom(buy_func_demo2,fast=4,mid=20,slow=75)
    #trades,name = normal_template(sdata,dates,demo2,csc_func,normal_trade_func)
    #evs = evaluate(trades)

    demo3 = fcustom(buy_func_demo3,fast=5,slow=98)
    trades,name = normal_template(sdata,dates,demo3,csc_func,normal_trade_func)
    evs2 = evaluate(trades)
    print evs2.header()
