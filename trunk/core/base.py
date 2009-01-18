# -*- coding= utf-8 -*-

import weakref
import numpy as np

from wolfox.common.tcommon import *
#直接从wolfox.common.tcommon导入

class CommonObject(object):
    def __init__(self,id,**kwargs):
        self.id = id
        self.__dict__.update(kwargs)


class CatalogSubject(CommonObject):
    def __init__(self,id,name,catalogs):
        super(CatalogSubject,self).__init__(id,name=name,catalogs=catalogs)


class Catalog(CommonObject):
    def __init__(self,id,name,stocks):
        super(Catalog,self).__init__(id,name=name,stocks=stocks)

def trans(t):
    if isinstance(t,dict):
        return tuple(t.items())
    elif isinstance(t,list):
        return tuple(t)
    return t

def generate_key(*args,**kwargs):
    ''' 将第一层可转换成tuple的list,dict对象转换成tuple以生成key
        但对于[[],[]]这样的位置参数，还是会抛出TypeError
    '''
    try:
        #print 'args:',args,',kwargs:',kwargs.items()
        key1 = args + tuple(kwargs.items()) #即tuple(kwargs.keys),keys的tuple
        hash(key1)
        return key1
    except TypeError:
        key2 = tuple((trans(t) for t in args)) + tuple(kwargs.items())
        #print 'key2:',key2
        hash(key2)
        return key2

class CacheManager(object):
    def __init__(self):
        self.caches = set([])

    def register(self,cache):
        self.caches.add(cache)
    
    def clear(self):    #清除已注册各cache的内容,而不是清除这个caches列表(即不是unregister all)
        for cache in self.caches:
            cache.clear()

cache_manager = CacheManager()

class AbstractCache(object):
    def __init__(self,func):
        self.func = func
        self.cache = {}
        cache_manager.register(self)

    def __call__(self):
        raise NotImplementedError,u'该函数为抽象函数，需要由子类实现'

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

    def clear(self):
        self.cache.clear()


#from http://wiki.python.org/moin/PythonDecoratorLibrary的memoized,修改成weak reference版本
class cache(AbstractCache):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.
        只能缓存非原生结果(对int之类的无法weakref it)
    """
   
    def __call__(self, *args,**kwargs):
        try:    #对不可hash的Key类型设防
            key = generate_key(*args,**kwargs)            
            if key in self.cache:
                return self.cache[key]
            rev = self.func(*args,**kwargs)
            self.cache[key] = rev
        except TypeError,inst:
            #print 'in type error',str(inst)
            return self.func(*args,**kwargs)
        return rev


@cache
def cache_example(i):
    return i+10

class wcache(AbstractCache):
    """weakref cache
    Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.
        只能缓存非原生结果(对int之类的无法weakref it)
    """

    def __call__(self, *args,**kwargs):
        try:    #对不可hash的Key类型设防
            key = generate_key(*args,**kwargs)
            #print key
            if key in self.cache:
                #print 'find key:',key
                r = self.cache[key]
                if r() != None: #只能如此，否则如果直接用 if r():，当r()是np.array类型时，会报ValueError,The truth value of an array with more than one element is ambiguous.Use a.any() or a.all()
                    return r()
            rev = self.func(*args,**kwargs)
            self.cache[key] = weakref.ref(rev)
        except TypeError,inst:
            #print 'type error',args,kwargs,key #对dict无法进行weak reference
            #import traceback
            #traceback.print_exc()
            return self.func(*args,**kwargs)
        return rev

@wcache
def cache_example(i):
    return CommonObject(id=i)

