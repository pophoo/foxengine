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
        self.assertFalse(cf.cache[((1,),())]())
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


if __name__ == "__main__":
    unittest.main()


