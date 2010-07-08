# -*- coding: utf-8 -*-

import wolfox.fengine.ifuture.ifreader as ifreader


from wolfox.fengine.ifuture.ibase import *
from wolfox.fengine.ifuture.ifreader import *
import wolfox.fengine.ifuture.iftrade as iftrade
import wolfox.fengine.ifuture.ifuncs as ifuncs
import wolfox.fengine.ifuture.tfuncs as tfuncs
from wolfox.fengine.ifuture.ifuncs import *

def calc(name,strategy):

    ifmap = ifreader.read1(name)  # fname ==> BaseObject(name='$name',transaction=trans)
    sif = ifmap[name]

    tradesy =  iftrade.ltrade3y(sif,strategy)    #xfollow作为平仓信号，且去掉了背离平仓的信号

    iftrade.last_action(tradesy)
    
