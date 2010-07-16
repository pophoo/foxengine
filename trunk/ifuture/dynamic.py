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
    tradesy =  functor(sif,strategy)    #xfollow作为平仓信号，且去掉了背离平仓的信号
    iftrade.last_action(tradesy)

calc = fcustom(xcalc,functor=iftrade.ltrade3y)

xcalc = fcustom(xcalc,functor=iftrade.ltrade3y0525_5)
xcalc1 = fcustom(xcalc,functor=iftrade.ltrade3y1_5)
xcalc2 = fcustom(xcalc,functor=iftrade.ltrade3y2_5)
xcalc3 = fcustom(xcalc,functor=iftrade.ltrade3y3_5)
xcalc4 = fcustom(xcalc,functor=iftrade.ltrade3y4_5)
xcalc6 = fcustom(xcalc,functor=iftrade.ltrade3y6_5)

