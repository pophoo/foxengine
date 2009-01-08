# -*- coding= utf-8 -*-

import weakref

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

#from http://wiki.python.org/moin/PythonDecoratorLibrary的memoized,修改成weak reference版本
class cache(object):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.
        只能缓存非原生结果(对int之类的无法weakref it)
    """
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if args in self.cache:
            r = self.cache[args]
            if r():
                return r()
        rev = self.func(*args)
        self.cache[args] = weakref.ref(rev)
        return rev

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__


@cache
def cache_example(i):
    return CommonObject(id=i)

