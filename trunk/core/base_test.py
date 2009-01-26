# -*- coding= utf-8 -*-

import unittest
from wolfox.fengine.core.base import * 

class CacheTest(unittest.TestCase):
    def test_wcache(self):
        f = lambda id : CommonObject(id = id)
        cf = wcache(f)
        a = cf(1)
        b = cf(1)
        c = cf(2)
        self.assertEquals(a,b)
        self.assertNotEquals(a,c)
        del a,b #测试弱引用
        #print cf.cache.keys()
        self.assertFalse(cf.cache[(1,)]())
        a = cf([])      #测试不可hash的key，except通道

    def test_cache(self):
        f = lambda id : id + 10
        cf = cache(f)
        a = cf(1)
        b = cf(1)
        c = cf(2)
        fl = lambda l : l[0]    #不可hash的key，except通道
        cfl = cache(fl)
        a = cfl([10])
        fl2 = lambda l1,l2 : l1[0]
        cfl2 = cache(fl2)
        a = cfl2([10],[])

    def test_AbstractCache(self):   #测试通路,逻辑由具体类测试
        ac = AbstractCache(lambda x:x)
        ac.clear()
        self.assertRaises(TypeError,str,ac) #因为内含的函数没有定义__doc__,导致str(ac)返回None，引发TypeError
        self.assertRaises(NotImplementedError,ac)   #调用抽象方法__call__

    def test_CacheManager(self):
        cache_manager.caches.clear()    #清除caches中的列表
        ac1 = AbstractCache(lambda x:x)
        ac2 = AbstractCache(lambda x:x)
        self.assertEquals(2,len(cache_manager.caches))
        ac1.cache['1'] = 2
        ac2.cache['2'] = 1
        self.assertTrue('1' in ac1.cache)
        self.assertTrue('2' in ac2.cache)
        cache_manager.clear()
        self.assertTrue('1' not in ac1.cache)
        self.assertTrue('2' not in ac2.cache)



class ModuleTest(unittest.TestCase):
    def testCommonObject(self): #通路测试
        co1 = CommonObject(1)
        co2 = CommonObject(1,xx=12)
        self.assertTrue(True)

    def testCatalogSubject(self):   #通路测试
        c1 = Catalog(1,'test',[1,2,3])
        c2 = Catalog(1,'test',[6,7,8])
        cs1 = CatalogSubject(1,'test',[c1,c2])
        self.assertTrue(True)

    def testCatalog(self):  #通路测试
        c1 = Catalog(1,'test',[1,2,3])
        self.assertTrue(True)    

    def test_get_all_catalogs(self):
        c1 = Catalog(1,'test',[1,2,3])
        c2 = Catalog(1,'test',[6,7,8])
        cs1 = CatalogSubject(1,'test',[c1,c2])
        c3 = Catalog(1,'test',[1,2,3])
        c4 = Catalog(1,'test',[6,7,8])
        cs2 = CatalogSubject(1,'test',[c3,c4])
        self.assertEquals([c1,c2,c3,c4],get_all_catalogs([cs1,cs2]))
        self.assertEquals([c3,c4,c1,c2],get_all_catalogs([cs2,cs1]))

    def test_trans(self):
        self.assertEquals((),trans([]))
        self.assertEquals((),trans({}))
        self.assertEquals(1,trans(1))

    def test_generate_key(self):
        self.assertEquals((),generate_key())
        self.assertEquals((1,2),generate_key(1,2))
        self.assertEquals((1,2,('xx',3)),generate_key(1,2,xx=3))
        self.assertEquals((1,(2,),('xx',3)),generate_key(1,[2,],xx=3))
        self.assertEquals((1,(2,),(('k',1),),('xx',3)),generate_key(1,[2,],{'k':1},xx=3))
        self.assertEquals((1,(2,),(('k',1),),('xx',3)),generate_key(1,(2,),{'k':1},xx=3))
        self.assertEquals((1,(2,),(('k',1),('b',2)),('yy',4),('xx',3)),generate_key(1,(2,),{'k':1,'b':2},xx=3,yy=4))        
        self.assertRaises(TypeError,generate_key,[[],[]],(2,),{'k':1},xx=3) #[[],[]]不能够被转换成可hash的对象


if __name__ == "__main__":
    unittest.main()


