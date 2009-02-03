# -*- coding: utf-8 -*-

#服务于数据读取的工具函数

import logging

from wolfox.fengine.extern import *
from wolfox.fengine.core.base import CommonObject as CDO,CatalogSubject as CSO,Catalog as CO,cache,wcache

logger = logging.getLogger('wolfox.fengine.core.source')

def get_ref_dates(begin,end,rcode=ref_code):
    rss = store.get_xquotes2(dj.connection,[rcode],begin,end)   #
    if not rss:
        return np.array([])
    rs = rss.values()[0]
    return np.array([r.tdate for r in rs])

#@cache  #不能用wcache,无法weakref dict
def prepare_data(begin,end,type_code ='STOCK',rcode=ref_code):
    rid = code2id[rcode]
    codes = get_codes(type_code,'SHSE')
    codes.extend(get_codes(type_code,'SZSE'))
    #print 'codes:',tuple(codes)
    sdata = get_stocks(codes,begin,end,rid=rid)
    #print sdata
    return sdata

@wcache
def get_codes(type_code='STOCK',source='SHSE'):
    ss = m.StockCode.objects.filter(stype=type_code,exchange__code=source)
    return [s.code for s in ss]

@wcache
def get_codes_startswith(cond):
    ss = m.StockCode.objects.filter(code__startswith=cond)
    return [s.code for s in ss]

def get_stocks(codes,begin,end,rid=ref_id): 
    #print 'codes:',codes
    rev = {}
    for code in codes:
        sid = code2id[code]
        logger.debug('loading stock:%s' % code)
        #print code
        vo = CDO(id=sid,code=code)
        vo.transaction = tuple2array(store.get_refbased_xquotes(dj.connection,ref_id,sid,begin,end))
        #t:transaction,d:data,g:global,c:catalog?
        rev[sid] = vo
    return rev

def get_catalog_tree(sdata,subjects=None):
    ''' sdata是 id ==> stock 的dict
        subjects为板块类别列表
    '''
    if subjects:    #如果设置了subjects，则只取这些
        ss = m.CatalogSubject.objects.filter(code__in = subjects)
    else:
        ss = m.CatalogSubject.objects.all()
    return _build_catalog_tree(ss,sdata)

def _build_catalog_tree(css,sdata):
    #只保留有stock的catalog和catalogsubject
    rev = []
    for s in css:
        #cos = [CO(c.id,name=c.name,stocks=[ sdata[sc.id] for sc in c.stocks.all() if sc.id in sdata]) for c in s.catalogs.all()]
        cos = []
        for c in s.catalogs.all():
            for sc in c.stocks.all():
                if sc.id in sdata:
                    stocks = [sdata[sc.id]]
                    cos.append(CO(c.id,name=c.name,stocks=stocks))


        #这里需要确保sdata[sc.id]!=null，否则会刨出异常。这个条件貌似必然成立，如果数据库完整性能被保证
        cos = [ co for co in cos if co.stocks ]
        if cos:
            cso = CSO(s.code,name=s.name,catalogs=cos)
            rev.append(cso)
    return rev



####以下是工具类
from wolfox.fengine.core.base import OPEN,CLOSE,HIGH,LOW,AVG,AMOUNT,VOLUME
#将{name:quote_list}转化为{name:[array1,....,array7]}的形式
def tuple2array(quotes):
    ''' 返回的是数组[topens,tcloses,thighs,tlows,tavgs,tamounts,tvolumes]，各元素都是等长数组
    '''
    if not quotes:  #[]时需要满足语义
        return np.array([[],[],[],[],[],[],[]])
    normalize(quotes)
    rev = np.array(quotes)
    return rev.transpose()
    
#序列的正规化，两个用途:
#   1. 将第一个有效交易日之前的数据都同化为该日数据，但交易量和金额都为0. 如果区间段内没有有效交易日，则都赋值为0
#   2. 将之后的每个无效交易日的数据都同化为前一日的数据
def normalize(quotes):
    if not quotes:
        return quotes
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

#从输入stock的qarrays中抽取指定的分量，并组成集合数组。这是一个耗时的操作，故设置弱引用cache
#@wcache
def extract_collect(stocks,sector=CLOSE):
    #print "sector:",sector
    return np.array([s.transaction[sector] for s in stocks])

def extract_collect1(stock,sector=CLOSE):
    #print "sector:",sector
    return stock.transaction[sector]

