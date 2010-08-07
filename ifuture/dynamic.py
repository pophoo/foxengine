# -*- coding: utf-8 -*-

import wolfox.fengine.ifuture.ifreader as ifreader


from wolfox.fengine.ifuture.ibase import *
from wolfox.fengine.ifuture.ifreader import *
import wolfox.fengine.ifuture.iftrade as iftrade
import wolfox.fengine.ifuture.ifuncs as ifuncs
import wolfox.fengine.ifuture.tfuncs as tfuncs
from wolfox.fengine.ifuture.ifuncs import *

def xcalc(name,strategy,functor):
    ifmap = ifreader.read1(name,extractor=extract_if_wh)  # fname ==> BaseObject(name='$name',transaction=trans)
    sif = ifmap[name]
    tradesy =  functor(sif,strategy)    
    iftrade.last_actions(tradesy)

calc = fcustom(xcalc,functor=iftrade.ltrade3y)

xcalc = fcustom(xcalc,functor=iftrade.ltrade3y0525_5)
xcalc1 = fcustom(xcalc,functor=iftrade.ltrade3y1_5)
xcalc2 = fcustom(xcalc,functor=iftrade.ltrade3y2_5)
xcalc3 = fcustom(xcalc,functor=iftrade.ltrade3y3_5)
xcalc4 = fcustom(xcalc,functor=iftrade.ltrade3y4_5)
xcalc6 = fcustom(xcalc,functor=iftrade.ltrade3y6_5)



wh_path = u'E:/光大期货Mytrader行情交易系统/'
wh_path2 = u'E:/文华财经Mytrader行情交易系统/'
wh_pattern = wh_path + 'IF*.txt'
wh_pattern2 = wh_path2 + 'IF*.txt'

import glob
import os.path

def find_cur():
    files = glob.glob(wh_pattern)
    files.extend(glob.glob(wh_pattern2))
    ctime = 0
    cfile = None
    for f in files:
        ftime = os.path.getmtime(f)
        #print f,ftime
        #print f,ftime,ctime
        if ftime > ctime:
            ctime = ftime
            cfile = f
    #print cfile
    return cfile

get_if_name = lambda fn:fn[-12:-4]    #仅用于文华财经
get_if_path = lambda fn:fn[:-12]    #仅用于文华财经

def wcalc(strategy,functor):
    fname = find_cur()
    name = get_if_name(fname)
    path = get_if_path(fname)
    #print path,wh_path
    ifmap = ifreader.readp(path,name,extractor=extract_if_wh)  # fname ==> BaseObject(name='$name',transaction=trans)
    sif = ifmap[name]
    tradesy =  functor(sif,strategy)    #xfollow作为平仓信号，且去掉了背离平仓的信号
    iftrade.last_actions(tradesy)

calc = fcustom(wcalc,functor=iftrade.ltrade3y)

wcalc = fcustom(wcalc,functor=iftrade.ltrade3y0525_5)
wcalc1 = fcustom(wcalc,functor=iftrade.ltrade3y1_5)
wcalc2 = fcustom(wcalc,functor=iftrade.ltrade3y2_5)
wcalc3 = fcustom(wcalc,functor=iftrade.ltrade3y3_5)
wcalc4 = fcustom(wcalc,functor=iftrade.ltrade3y4_5)
wcalc6 = fcustom(wcalc,functor=iftrade.ltrade3y6_5)


def wxcalc(strategy,functor):
    fname = find_cur()
    name = get_if_name(fname)
    path = get_if_path(fname)
    #print path,wh_path
    ifmap = ifreader.readp(path,name,extractor=extract_if_wh)  # fname ==> BaseObject(name='$name',transaction=trans)
    sif = ifmap[name]
    print 'last updated--%s:%s' % (sif.transaction[IDATE][-1],sif.transaction[ITIME][-1])
    tradesy =  functor(sif,strategy)    #xfollow作为平仓信号，且去掉了背离平仓的信号
    #print tradesy
    iftrade.last_xactions(sif,tradesy)

wxcalc = fcustom(wxcalc,functor=iftrade.ltrade3x0525)

def whget(strategy,functor,priority=2500):
    fname = find_cur()
    name = get_if_name(fname)
    path = get_if_path(fname)
    #print path,wh_path
    ifmap = ifreader.readp(path,name,extractor=extract_if_wh)  # fname ==> BaseObject(name='$name',transaction=trans)
    sif = ifmap[name]
    print 'last updated--%s:%s' % (sif.transaction[IDATE][-1],sif.transaction[ITIME][-1])
    tradesy =  functor(sif,strategy,priority_level=priority)    #xfollow作为平仓信号，且去掉了背离平仓的信号
    #print tradesy
    xactions = iftrade.last_wactions(sif,tradesy)
    for action in xactions:
        action.price = action.price / 10.0
        calc_stop(sif,action)
    return fname,sif,xactions

def calc_stop(sif,action):
    stop1 = sif.atr5x[action.index]/1250.0
    stop2 = sif.atr[action.index]*1.5/1000
    if stop1 < 3:
        stop1 = 3
    if stop2 < 3:
        stop2 = 3
    if action.position == LONG:
        action.stop1 = action.price - stop1
        action.stop2 = action.price - stop2
        action.stop = min(action.stop1,action.stop2)
    else:
        action.stop1 = action.price + stop1
        action.stop2 = action.price + stop2
        action.stop = max(action.stop1,action.stop2)
    action.stop1 = round(action.stop1,1)    #对空头可能多了0.05个点
    action.stop2 = round(action.stop2,1) 
    action.stop = round(action.stop,1) 
    

#whget = fcustom(whget,functor=iftrade.ltrade3x0525)
#whget = fcustom(whget,functor=iftrade.ltrade3x156)
whget = fcustom(whget,functor=iftrade.ltrade3x0825)
