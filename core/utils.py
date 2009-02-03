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

from wolfox.lib.objgraph import show_most_common_types  #用于显示内存中实例最多的类型及其实例数
#def show_most_common_types(limit=10); Count the names of types with the most instances.Note that the GC does not track simple objects like int or str.
#    Note that classes with the same name but defined in different modules will be lumped together.


import gc
import logging
import win32pdhutil as wu

logger = logging.getLogger('wolfox.fengine.core.utils')

def get_null_obj_number(obj_type):
    i = 0
    for o in gc.get_objects():
        if isinstance(o,obj_type) and not o:
            i+=1
    return i

def get_obj_number(obj_type):
    return sum([ isinstance(o,obj_type) and 1 or 0 for o in gc.get_objects() ])


class memory_guard(object):
    ''' 一个用于检测memory溢出的decorate
        根据http://www.python.org/dev/peps/pep-0318/
        ......
        @decomaker(argA, argB, ...)
        def func(arg1, arg2, ...):
            pass
        
        is equivalent to:
        func = decomaker(argA, argB, ...)(func)

        这个decorate极为耗时，只有在调试时才需要挂上
    '''
    def __init__(self,gtype,criterion = lambda x : True,debug=False):
        ''' gtype为监视的类型
            criterion用于判定该增加类型中的内容
        '''
        self.gtype = gtype
        self.criterion = criterion
        self.debug = debug

    def __call__(self,func):
        self.func = func
        self.__name__ = self.func.__name__
        def new_func(*args,**kwargs):
            mbegin = wu.GetPerformanceAttributes("Memory", "Available Bytes")
            logger.debug('%s memory guard begin: %s',self.__name__,mbegin)
            if self.debug:
                print '%s memory guard begin: %s' % (self.__name__,mbegin)
            pre_objs = self.get_objs()
            rev = self.func(*args,**kwargs)
            cur_objs = self.get_objs()
            diff = [ t for t in seq_diff(cur_objs,pre_objs) if self.criterion(t) ]
            new_func.new_num = new_num = len(diff) 
            logger.debug('%s memory guard end,this run create new objs specified: %s',self.__name__,new_num)
            if self.debug:
                print "new specified %s object number = %s " % (self.gtype,new_num)
                logger.debug('new specified %s objects:%s',self.gtype,diff)
            mend = wu.GetPerformanceAttributes("Memory", "Available Bytes")
            logger.debug('%s memory guard end,this run eat:%s',self.__name__,mbegin-mend)
            return rev
        new_func.parent = self
        new_func.new_num = 0
        return new_func

    def get_objs(self):
        gobjs = [ t for t in gc.get_objects() if isinstance(t,self.gtype)]
        return gobjs

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__


@memory_guard(list,lambda x:x==[1])
def mguard_example():
    return [1]


