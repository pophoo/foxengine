# -*- coding: utf-8 -*-

import wolfox.fengine.ifuture.ifreader as ifreader


from wolfox.fengine.ifuture.ibase import *
from wolfox.fengine.ifuture.ifreader import *
import wolfox.fengine.ifuture.iftrade as iftrade
import wolfox.fengine.ifuture.ifuncs as ifuncs
import wolfox.fengine.ifuture.tfuncs as tfuncs
from wolfox.fengine.ifuture.ifuncs import *

def xcalc(name,strategy,functor):
    ifmap = ifreader.read1(name)  # fname ==> BaseObject(name='$name',transaction=trans)
    sif = ifmap[name]
    tradesy =  functor(sif,strategy)    #xfollow作为平仓信号，且去掉了背离平仓的信号
    iftrade.last_action(tradesy)

calc = fcustom(xcalc,functor=iftrade.ltrade3y)
xcalc1 = fcustom(xcalc,functor=iftrade.ltrade3y1)
xcalc2 = fcustom(xcalc,functor=iftrade.ltrade3y2)
xcalc3 = fcustom(xcalc,functor=iftrade.ltrade3y3)
xcalc4 = fcustom(xcalc,functor=iftrade.ltrade3y4)
xcalc6 = fcustom(xcalc,functor=iftrade.ltrade3y6)
