# -*- coding: utf-8 -*-

import wolfox.fengine.ifuture.ifreader as ifreader


from wolfox.fengine.ifuture.ibase import *
from wolfox.fengine.ifuture.ifreader import *
import wolfox.fengine.ifuture.iftrade as iftrade
import wolfox.fengine.ifuture.ifuncs as ifuncs
import wolfox.fengine.ifuture.tfuncs as tfuncs
from wolfox.fengine.ifuture.ifuncs import *

def calc(name):

    ifmap = ifreader.read1(name)  # fname ==> BaseObject(name='$name',transaction=trans)
    sif = ifmap[name]

    xfollow = [ifuncs.ipmacd_short_1,ifuncs.ipmacd_short_2,ifuncs.ipmacd_short_3,ifuncs.ma3x10_short,ifuncs.down01,ifuncs.dmacd_short5,ifuncs.ipmacdx_short,ifuncs.ipmacd_short5,ifuncs.ma30_short,ifuncs.ma60_short]

    #逆势品种
    d22 = fcustom(ifuncs.dmacd_short2,rolled=2)
    #xagainst = [ifuncs.ipmacd_long_devi1,ifuncs.dmacd_long,ifuncs.dmacd_short2,d22,ifuncs.down30]
    xagainst = [ifuncs.dmacd_short2,d22,ifuncs.down30,ifuncs.up05] #dmacd_long被dms取代

    #xagainst = [ifuncs.dmacd_short2,d22,ifuncs.down30]

    #中间品种 dms基本被吸收，但在long_f和dms之间，选择dms
    xmiddle = [ifuncs.ipmacd_longt,ifuncs.ipmacd_long5,ifuncs.xldevi2,ifuncs.dms,ifuncs.ipmacd_long_1,ifuncs.up0,ifuncs.dmacd_long5,ifuncs.ma60_long,ifuncs.ipmacd_long_devi1]

    xnormal = [ifuncs.ipmacd_short_4,ifuncs.ipmacd_short_5]

    tradesy =  iftrade.ltrade3y(sif,xfollow+xagainst+xmiddle+xnormal)    #xfollow作为平仓信号，且去掉了背离平仓的信号

    iftrade.last_action(tradesy)
    
