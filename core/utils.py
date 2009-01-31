# -*- coding: utf-8 -*-

#工具函数

from functools import partial

def fcustom(func,**kwargs):
    ''' 根据kwargs设置func的偏函数,并将此偏函数的名字设定为源函数名+所固定的关键字参数名
    '''
    pf = partial(func,**kwargs)
    #pf.name = pf.func.func_name
    pf.paras = ','.join(['%s=%s' % item for item in pf.keywords.items()])
    pf.__name__ = '%s:%s' % (func.__name__,pf.paras)
    return pf

def names(*args):
    ''' 返回传入的args中各元素__name__值组成的元组
    '''
    return tuple([f.__name__ for f in args])

