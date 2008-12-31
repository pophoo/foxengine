# -*- coding: utf-8 -*-

#服务于数据读取的工具函数

from wolfox.fengine.extern import *

def get_ref_dates(begin,end):
    rss = store.get_xquotes2(dj.connection,[ref_code],begin,end)   #
    rs = rss.values()[0]
    return np.array([r.tdate for r in rs])

def prepare_data(begin,end,type_code ='STOCK'):
    codes = get_codes(type_code,'SHSE')
    codes.extend(get_codes(type_code,'SZSE'))
    #print codes
    sdata = get_stocks(codes,begin,end)
    return sdata

def get_codes(type_code='STOCK',source='SHSE'):
    ss = m.StockCode.objects.filter(stype=type_code,exchange__code=source)
    return [s.code for s in ss]

def get_stocks(stocks,begin,end):
    rev = {}
    for stock in stocks:
        rev[stock] = tuple2array(store.get_refbased_xquotes(dj.connection,ref_id,code2id[stock],begin,end))
    return rev


####以下是工具类
from wolfox.fengine.core.d1 import OPEN,CLOSE,HIGH,LOW,AVG,AMOUNT,VOLUME
#将{name:quote_list}转化为{name:[array1,....,array7]}的形式
def tuple2array(quotes):
    ''' 返回的是[topens,tcloses,thighs,tlows,tavgs,tamounts,tvolumes]，各元素都是等长数组
    '''
    normalize(quotes)
    rev = np.array(quotes)
    return rev.transpose()
    
#序列的正规化，两个用途:
#   1. 将第一个有效交易日之前的数据都同化为该日数据，但交易量和金额都为0. 如果区间段内没有有效交易日，则都赋值为0
#   2. 将之后的每个无效交易日的数据都同化为前一日的数据
def normalize(quotes):
    ihead = normalize_head(quotes)
    if ihead < len(quotes) - 1: #ihead如果是最后一个，也不需调用normalize_body了
        normalize_body(quotes,ihead)

def normalize_head(quotes):
    for i,v in enumerate(quotes):
        if v[0]:    #这里因为不存在开盘为0的情况，所以不需要v[0] == None,如果根据成交量判断，则因为史上存在某日成交量为0的股票，则必须是v[0] != None
            break
    else:
        for j in xrange(len(quotes)):
            quotes[j] = 0,0,0,0,0,0,0
        return i + 1
    v0,v1,v2,v3,v4 = v[0],v[1],v[2],v[3],v[4]
    for j in xrange(i):
        quotes[j] = v0,v1,v2,v3,v4,0,0
    return i

def normalize_body(quotes,ihead):
    for i in xrange(ihead + 1,len(quotes)):
        if not quotes[i][0]:    #这里因为不存在开盘为0的情况，所以不需要quotes[i][0] == None,则因为史上存在某日成交量为0的股票，则必须是quotes[i][0] != None
            pre = quotes[i-1]
            quotes[i] = pre[0],pre[1],pre[2],pre[3],pre[4],0,0

#从输入的qarrays中抽取指定的分量，并组成集合数组
def extract_collect(qarrays,sector=CLOSE):
    #print "sector:",sector
    ts = [ qa[sector] for qa in qarrays ]
    return np.array(ts)

