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

def seq_diff(source,target):   
    ''' 对source和follow两个seq求diff，因为序列可能包含不可hash的元素，所以不能直接转换为set
        返回为diff元素的列表
    '''
    ds = dict([ (id(s),s) for s in source])
    dt = dict([ (id(t),t) for t in target])
    diff = set(ds) - set(dt)
    return [ ds[d] for d in diff]

import gc
def get_null_obj_number(obj_type):
    i = 0
    for o in gc.get_objects():
        if isinstance(o,obj_type) and not o:
            i+=1
    return i

def get_obj_number(obj_type):
    return sum([ isinstance(o,obj_type) and 1 or 0 for o in gc.get_objects() ])

