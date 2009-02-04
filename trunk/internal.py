# -*- coding: utf-8 -*-

#fengine内部引用类的集合

import wolfox.fengine.core.source as cs
import wolfox.fengine.core.d1 as d1
import wolfox.fengine.core.d1ex as d1e
import wolfox.fengine.core.d1idiom as d1id
import wolfox.fengine.core.d1indicator as d1in
import wolfox.fengine.core.d1catalog as d1c
import wolfox.fengine.core.d1kline as d1k
import wolfox.fengine.core.d1match as d1m
import wolfox.fengine.core.d2 as d2
import wolfox.fengine.core.trade as trade
import wolfox.fengine.core.utils as utils

from wolfox.fengine.core.utils import fcustom,names,get_null_obj_number,get_obj_number
from wolfox.fengine.core.d1 import band,bor,gand,gor,smooth,smooth2
from wolfox.fengine.core.d1ex import ma,trend,strend,cross,sfollow,syntony,transform
from wolfox.fengine.core.d1indicator import svap_ma
from wolfox.fengine.core.d1idiom import upconfirm,downup,swingin
from wolfox.fengine.core.d2 import dispatch,cdispatch,posort,percent_sort,npercent,percent,nincrease
from wolfox.fengine.core.base import get_all_catalogs
from wolfox.fengine.core.base import OPEN,CLOSE,HIGH,LOW,AVG,AMOUNT,VOLUME
from wolfox.fengine.core.d1catalog import calc_index,catalog_signal
from wolfox.fengine.core.source import get_ref_dates,prepare_data,get_codes,get_codes_startswith
from wolfox.fengine.core.d1match import make_trade_signal
from wolfox.fengine.core.trade import make_trades,last_trade,evaluate


