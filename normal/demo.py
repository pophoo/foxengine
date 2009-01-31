# -*- coding: utf-8 -*-

#完整的起始脚本

from wolfox.fengine.core.shortcut import *

def buy_func_demo1(stock):
    t = stock.transaction
    g = stock.gtest >= 7500
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


if __name__ == '__main__':
    begin,end = 20010101,20030101
    dates = get_ref_dates(begin,end)
    sdata = prepare_data(begin,end)
    idata = prepare_data(begin,end,'INDEX')
    ctree = cs.get_catalog_tree(sdata)
    catalogs = get_all_catalogs(ctree)

    c_posort('test',catalogs,distance=10)
    d_posort('gtest',sdata.values(),distance=60)

    #template(sdata,dates,buy_func_demo1,csc_func,trade_func)
    demo2 = fcustom(buy_func_demo2,fast=4,mid=20,slow=75)
    trades,name = normal_template(sdata,dates,demo2,csc_func,normal_trade_func)
    evs = evaluate(trades)

    print name #,unicode(evs)
    print evs.header()
