# -*- coding= utf-8 -*-

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


