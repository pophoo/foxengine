# -*- coding: utf-8 -*-

#完整的起始脚本

from wolfox.fengine.extern import *

#批量设置股票类型属性的语句

#查找上海的股票

def get_codes(type='STOCK',source='SH'):
    pass

def get_stocks(stocks,begin,end):
    quotes = store.get_xquotes2(dj_conn,stocks,begin,end)
    return list2array(quotes)

#将{name:quote_list}转化为{name:[array1,....,array9]}的形式
def list2array():
    pass


