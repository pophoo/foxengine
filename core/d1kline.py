# -*-coding:utf-8 -*-

#一维向量K线相关指标的计算

import numpy as np
from wolfox.fengine.core.d1indicator import ma,BASE

#未知都用'u'表示

def ksign(sfirst,tlast):   
    ''' 阴阳计算 a 阳 b 阴 c平 
        返回字符串
    '''
    assert len(sfirst) == len(tlast)
    strlist = ['u'] * len(sfirst)
    for i in xrange(len(sfirst)):
        ct,cs = tlast[i],sfirst[i]
        strlist[i] = ct > cs and 'a' or (ct < cs and 'b') or 'c'
    return ''.join(strlist)

def ksize(sfirst,tlast,tsmall=3,tmiddle=12,tbig=35):
    ''' 实体/影线计算
            tlast-sfirst/sfirst >= tbig/1000 为大'a', 
            tmiddle/1000-tbig/1000为中'b', 
            tsmall/1000-tmiddle/1000为小'c'，
            <tsmall/1000 可忽略'd'
    '''
    assert len(sfirst) == len(tlast)
    strlist = ['u'] * len(sfirst)
    for i in xrange(len(sfirst)):
        ct,cs = tlast[i],sfirst[i]        
        s = abs(cs - ct)*BASE/cs
        if(s >= tbig):
            strlist[i] = 'a'
        elif(s >= tmiddle):
            strlist[i] = 'b'
        elif(s >= tsmall):
            strlist[i] = 'c'
        else:
            strlist[i] = 'd'
    return ''.join(strlist)


def ksized(sfirst,tlast,length=5,tbig=2000,tmiddle=600,tsmall=200):
    ''' 实体/影线计算
        动态算法 sfirst[i]-tlast[i]/ma(sfirst-tlast)[i-1] >= tbig/1000 为大'a', 
                 tmiddle/1000-tbig/1000为中'b', 
                 tsmall/1000-tmiddle/1000为小'c'，
                 <tsmall/1000 可忽略'd'
            未知u (第一个线形)
    '''
    assert len(sfirst) == len(tlast)
    strlist = ['u'] * len(sfirst)
    if(len(sfirst) < length+1): #实际上没有这个判断也能正常运作
        return ''.join(strlist)
    sma = ma(np.abs(sfirst-tlast),length)
    for i in xrange(length,len(sfirst)):
        ct,cs = tlast[i],sfirst[i]        
        s = (sma[i-1] ==0) and tbig+1 or abs((cs - ct)*BASE/sma[i-1])     #分母为0算大阳
        if(s >= tbig):
            strlist[i] = 'a'
        elif(s >= tmiddle):
            strlist[i] = 'b'
        elif(s >= tsmall):
            strlist[i] = 'c'
        else:
            strlist[i] = 'd'
    return ''.join(strlist)

def kscmp(first1,first2,follow1,follow2,tbig=4000,tmiddle=2000,tsmall=500):
    ''' 线型比较
        abs((follow2-follow1)/(first2-first1)) >= tbig/1000 为大'a', 
        tmiddle/1000-tbig/1000为中'b', 
        tsmall/1000-tmiddle/1000为小'c'，
        <tsmall/1000 可忽略'd'
        比如: kscmp(OPEN,CLOSE,HIGH,LOW)为比较影线
            而kscmp(OPEN,CLOSE,HIGH,tmax(OPEN,CLOSE))为比较下影线
    '''
    assert len(first1) == len(first2) == len(follow1) == len(follow2)
    strlist = ['u'] * len(first1)
    for i in xrange(len(first1)):
        cft1,cft2,cfw1,cfw2 = first1[i],first2[i],follow1[i],follow2[i]
        s = (cft1-cft2 == 0) and tbig + 1 or abs((cfw2-cfw1)*BASE/(cft2-cft1))
        #print first1[i],first2[i],follow1[i],follow2[i],s
        if(s >= tbig):
            strlist[i] = 'a'
        elif(s >= tmiddle):
            strlist[i] = 'b'
        elif(s >= tsmall):
            strlist[i] = 'c'
        else:
            strlist[i] = 'd'
    return ''.join(strlist)    

def krelation(target1,target2,follow1=None,follow2=None,interval=1):
    ''' 组线交叉
        各分为六类:(*为参照线)
 *  *   A   B   C   D   E   F   G   H   I   J
 *      |
 *          |   |   |
 *  |       |   |   |    
 *  |       |   |   |   |   |   |
 *  |           |   |       |   |
 *  |           |   |       |   |   |   |
 *  |               |           |       |
 *                  |           |       |   
 *                                          |

    一共10种，其中中间部分的比较为上半段，下半段
        另未知为'u'
    krelation(OPEN,CLOSE,HIGH,LOW,0) 可以用作当日的比较,但比较粗糙
    '''
    if not follow1: #默认等于target1
        follow1 = target1
    if not follow2: #默认等于target1
        follow2 = target2
    assert len(target1) == len(target2) and len(target1) == len(follow1) and len(follow1) == len(follow2)
    strlist = ['u'] * len(target1)
    if(len(target1) < interval+1): #实际上没有这个判断也能正常运作
        return ''.join(strlist)
    for i in xrange(interval,len(target1)):
        ct1,ct2,cf1,cf2 = target1[i-interval],target2[i-interval],follow1[i],follow2[i]
        tmax,tmin = max(ct1,ct2),min(ct1,ct2)
        fmax,fmin = max(cf1,cf2),min(cf1,cf2)
        tmid = (tmax + tmin + 1)/2
        #print tmax,tmin,tmid,fmax,fmin
        if(fmin > tmax):
            strlist[i] = 'a'
        elif(fmax > tmax and fmin > tmid):
            strlist[i] = 'b'
        elif(fmax > tmax and fmin > tmin):
            strlist[i] = 'c'
        elif(fmax > tmax):
            strlist[i] = 'd'
        elif(fmin > tmid):
            strlist[i] = 'e'
        elif(fmax > tmid and fmin > tmin):
            strlist[i] = 'f'
        elif(fmax > tmid):
            strlist[i] = 'g'
        elif(fmin > tmin):
            strlist[i] = 'h'
        elif(fmax > tmin):
            strlist[i] = 'i'
        else:
            strlist[i] = 'j'
    return ''.join(strlist)

def kmatch(target,reobj):
    ''' 模式匹配
        target为字符串,对找到的每一个匹配子串，最末一个字符匹配位置为匹配发生位置，置为1. 其余为0
    '''
    assert isinstance(target,str)
    rev = np.zeros(len(target),int)
    start = 0
    while(start < len(target)):
        f = reobj.search(target,start)
        if(f):
            start = f.end()
            rev[start-1] = 1
        else:
            break
    return rev

