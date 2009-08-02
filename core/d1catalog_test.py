# -*- coding: utf-8 -*-

import unittest
from wolfox.fengine.core.base import *
from wolfox.fengine.core.d1catalog import *


class ModuleTest(unittest.TestCase):
    def test_calc_weighted_base(self):
        a = np.array([(0,0,0,0),(500,400,800,500),(0,0,0,0),(0,0,0,0),(500,500,500,500),(5000,4000,8000,5000),(1000,1000,1000,1000)])
        b = np.array([(0,0,0,0),(200,200,200,200),(0,0,0,0),(0,0,0,0),(500,500,500,500),(0,0,4000,4000),(0,0,2000,1000)])
        c = np.array([(0,0,0,0),(700,500,500,700),(0,0,0,0),(0,0,0,0),(500,500,500,500),(7000,5000,0,4000),(1000,1000,0,1000)])
        sa = CommonObject(id=0,transaction=a)
        sb = CommonObject(id=1,transaction=b)
        sc = CommonObject(id=2,transaction=c) 
        ss = [sa,sb,sc]
        base = extract_collect(ss,CLOSE)[:,0]
        sbase = base[:,np.newaxis]
        weights = nma2d(extract_collect(ss,VOLUME),30)
        s_weights = weights * RFACTOR / weights.sum(0)
        index = calc_weighted_index(ss,CLOSE,sbase,s_weights)
        self.assertEquals([1000,757,1175,1000],index.tolist())

    def test_calc_indices_base(self):
        a = np.array([(0,0,0,0),(500,400,800,500),(0,0,0,0),(0,0,0,0),(500,500,500,500),(5000,4000,8000,5000),(1000,1000,1000,1000)])
        b = np.array([(0,0,0,0),(200,200,200,200),(0,0,0,0),(0,0,0,0),(500,500,500,500),(0,0,4000,4000),(0,0,2000,1000)])
        c = np.array([(0,0,0,0),(700,500,500,700),(0,0,0,0),(0,0,0,0),(500,500,500,500),(7000,5000,0,4000),(1000,1000,0,1000)])
        sa = CommonObject(id=0,transaction=a)
        sb = CommonObject(id=1,transaction=b)
        sc = CommonObject(id=2,transaction=c) 
        ss = [sa,sb,sc]
        indices = calc_indices_base(ss)
        self.assertEquals([0,0,0,0],indices[OPEN].tolist())
        self.assertEquals([1000,757,1175,1000],indices[CLOSE].tolist())
        self.assertEquals([0,0,0,0],indices[HIGH].tolist())
        self.assertEquals([0,0,0,0],indices[LOW].tolist())
        self.assertEquals([857,857,1347,1364],indices[AVG].tolist())        
        self.assertEquals([12,9,12,13],indices[AMOUNT].tolist())
        self.assertEquals([14,10,8,9],indices[VOLUME].tolist())        

    def test_calc_index_relative(self):
        a = np.array([(0,0,0,0),(500,400,800,500),(0,0,0,0),(0,0,0,0),(0,0,0,0),(5000,4000,8000,5000),(1000,1000,1000,1000)])
        b = np.array([(0,0,0,0),(200,200,200,200),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,4000,4000),(0,0,2000,1000)])
        c = np.array([(0,0,0,0),(700,500,500,700),(0,0,0,0),(0,0,0,0),(0,0,0,0),(7000,5000,0,4000),(1000,1000,0,1000)])
        sa = CommonObject(id=0,transaction=a)
        sb = CommonObject(id=1,transaction=b)
        sc = CommonObject(id=2,transaction=c) 
        ss = [sa,sb,sc]
        index = calc_index_relative(ss)
        self.assertEquals([1000,763,1208,1060],index.tolist())

    def test_calc_indices(self):
        a = np.array([(0,0,0,0),(500,400,800,500),(0,0,0,0),(0,0,0,0),(0,0,0,0),(5000,4000,8000,5000),(1000,1000,1000,1000)])
        b = np.array([(0,0,0,0),(200,200,200,200),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,4000,4000),(0,0,2000,1000)])
        c = np.array([(0,0,0,0),(700,500,500,700),(0,0,0,0),(0,0,0,0),(0,0,0,0),(7000,5000,0,4000),(1000,1000,0,1000)])
        sa = CommonObject(id=0,transaction=a)
        sb = CommonObject(id=1,transaction=b)
        sc = CommonObject(id=2,transaction=c) 
        ss = [sa,sb,sc]
        indices = calc_indices(ss)
        self.assertEquals([0,0,0,0],indices[OPEN].tolist())
        self.assertEquals([1000,763,1208,1060],indices[CLOSE].tolist())
        self.assertEquals([0,0,0,0],indices[HIGH].tolist())
        self.assertEquals([0,0,0,0],indices[LOW].tolist())
        self.assertEquals([250,191,302,265],indices[AVG].tolist())        
        self.assertEquals([12,9,12,13],indices[AMOUNT].tolist())
        self.assertEquals([12,11,9,12],indices[VOLUME].tolist())        

    def test_calc_index_old(self):
        a = np.array([(0,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(5000,4000,8000,4000),(1000,1000,1000,1000)])
        b = np.array([(0,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,4000,4000),(0,0,2000,1000)])
        c = np.array([(0,0,0,0),(700,500,500,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(7000,5000,0,4000),(1000,1000,0,1000)])
        sa = CommonObject(id=0,transaction=a)
        sb = CommonObject(id=1,transaction=b)
        sc = CommonObject(id=2,transaction=c) 
        ss = [sa,sb,sc]
        index = calc_index_old(ss,alen=3)
        self.assertEquals([1000,767,1173,1067],index.tolist())
        index = calc_index_old(ss,alen=2)
        self.assertEquals([1000,767,1204,1067],index.tolist())
        #print index

    def test_avg_price(self):
        a = np.array([(0,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(5000,4000,8000,4000),(1000,1000,1000,1000)])
        b = np.array([(0,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,4000,4000),(0,0,2000,1000)])
        c = np.array([(0,0,0,0),(700,700,300,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(7000,0,3000,4000),(1000,0,1000,1000)])
        sa = CommonObject(id=0,transaction=a)
        sb = CommonObject(id=1,transaction=b)
        sc = CommonObject(id=2,transaction=c) 
        avg = avg_price([sa,sb,sc])
        self.assertEquals([600,400,375,400],avg.tolist())

    def test_calc_amount(self):
        a = np.array([(0,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(5000,4000,8000,4000),(1000,1000,1000,1000)])
        b = np.array([(0,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,4000,4000),(0,0,2000,1000)])
        c = np.array([(0,0,0,0),(700,700,300,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(7000,0,3000,4000),(1000,0,1000,1000)])
        sa = CommonObject(id=0,transaction=a)
        sb = CommonObject(id=1,transaction=b)
        sc = CommonObject(id=2,transaction=c) 
        avg = calc_amount([sa,sb,sc])
        self.assertEquals([12,4,15,12],avg.tolist())

    def test_calc_drate(self):
        a = np.array([(0,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(5000,4000,8000,4000),(1000,1000,1000,1000)])
        b = np.array([(0,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,4000,4000),(0,0,2000,1000)])
        c = np.array([(0,0,0,0),(700,500,500,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(7000,5000,0,4000),(1000,1000,0,1000)])
        d = np.array([(0,0,0,0),(600,600,500,600),(0,0,0,0),(0,0,0,0),(0,0,0,0),(6000,6000,6000,6000),(1000,1000,1000,1000)])        
        sa = CommonObject(id=0,transaction=a)
        sb = CommonObject(id=1,transaction=b)
        sc = CommonObject(id=2,transaction=c) 
        sd = CommonObject(id=3,transaction=d)
        rate = calc_drate([sa,sb,sc,sd],distance=2,wave=4)
        self.assertEquals([[0, 1, 3, 1], [1, 2, 2, 3], [2, 0, 0, 0], [3, 3, 1, 2]],rate.tolist())
        rate = calc_drate([sa,sb,sc,sd])
        self.assertEquals([[0, 25, 75, 0], [25, 50, 25, 75], [50, 0, 50, 25], [75, 75, 0, 50]],rate.tolist())

    def test_catalog_signal(self):
        c1 = CommonObject(id=1,gorder=np.array([0,0,7500,7500]))
        c2 = CommonObject(id=1,gorder=np.array([0,7500,0,7500]))
        c3 = CommonObject(id=1,gorder=np.array([0,7500,0,7500]))
        cata_info = {c1:np.array([1000,1000,1000,8000]),c2:np.array([8000,8000,0,0]),c3:np.array([8000,8000,0,0])}
        self.assertEquals([0,1,0,1],catalog_signal(cata_info,7500,7500).tolist())
        self.assertEquals([0,1,1,1],catalog_signal(cata_info,7500,1000).tolist())        
        self.assertEquals([0,0,0,0],catalog_signal(cata_info,8001,8001).tolist())

    def test_catalog_signal_cs(self):
        c1 = CommonObject(id=1,gorder=np.array([0,0,7500,7500]))
        c2 = CommonObject(id=1,gorder=np.array([0,7500,0,7500]))
        c3 = CommonObject(id=1,gorder=np.array([0,7500,0,7500]))
        cata_info = {c1:np.array([1000,1000,1000,8000]),c2:np.array([8000,8000,0,0]),c3:np.array([8000,8000,0,0])}
        self.assertEquals([0,1,0,1],catalog_signal_cs(cata_info,lambda c,s:band(c.gorder>=7500,s>=7500)).tolist())
        self.assertEquals([0,1,1,1],catalog_signal_cs(cata_info,lambda c,s:band(c.gorder>=7500,s>=1000)).tolist())        
        self.assertEquals([0,0,0,0],catalog_signal_cs(cata_info,lambda c,s:band(c.gorder>=8001,s>=8001)).tolist())

    def test_catalog_signal_c(self):
        c1 = CommonObject(id=1,gorder=np.array([0,0,7500,7500]))
        c2 = CommonObject(id=1,gorder=np.array([0,7500,0,7500]))
        c3 = CommonObject(id=1,gorder=np.array([0,7500,0,7500]))
        cata_info = {c1:np.array([1000,1000,1000,8000]),c2:np.array([8000,8000,0,0]),c3:np.array([8000,8000,0,0])}
        self.assertEquals([0,1,1,1],catalog_signal_c(cata_info,lambda c:c.gorder>=7500).tolist())
        self.assertEquals([0,0,0,0],catalog_signal_c(cata_info,lambda c:c.gorder>=8001).tolist())

    def test_catalog_signal_m(self):
        c1 = CommonObject(id=1,gorder=np.array([0,0,7500,7500]))
        c2 = CommonObject(id=1,gorder=np.array([0,7500,0,7500]))
        c3 = CommonObject(id=1,gorder=np.array([0,7500,0,7500]))
        cata_info = {c1:np.array([1000,1000,1000,8000]),c2:np.array([8000,8000,0,0]),c3:np.array([8000,8000,0,0])}
        self.assertEquals([1,1,1,1],catalog_signal_m(lambda x,y:band(x,y),cata_info,cata_info).tolist())
        cata_info = {c1:np.array([1000,1000,0,8000]),c2:np.array([8000,8000,0,0]),c3:np.array([8000,8000,0,0])}
        self.assertEquals([1,1,0,1],catalog_signal_m(lambda x,y:band(x,y),cata_info,cata_info).tolist())
        cata_info2 = {c1:np.array([0,1000,0,8000]),c2:np.array([8000,8000,0,0]),c3:np.array([8000,8000,0,0])}
        self.assertEquals([1,1,0,1],catalog_signal_m(lambda x,y:band(x,y),cata_info,cata_info2).tolist())
        cata_info2 = {c1:np.array([0,1000,0,8000]),c2:np.array([0,8000,0,0]),c3:np.array([0,8000,0,0])}
        self.assertEquals([0,1,0,1],catalog_signal_m(lambda x,y:band(x,y),cata_info,cata_info2).tolist())
        self.assertEquals([1,1,0,1],catalog_signal_m(lambda x,y:bor(x,y),cata_info,cata_info2).tolist())
        self.assertEquals([1,0,0,0],catalog_signal_m(lambda x,y:x>y,cata_info,cata_info2).tolist())
        self.assertEquals([0,1,1,1],catalog_signal_m(lambda x,y:x==y,cata_info,cata_info2).tolist())


    #deprecated
    def test_calc_index_adjacent(self):
        a = np.array([(0,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(1000,1000,1000,1000)])
        b = np.array([(0,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,2000,1000)])
        c = np.array([(0,0,0,0),(700,700,300,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(1000,0,1000,1000)])
        sa = CommonObject(id=0,transaction=a)
        sb = CommonObject(id=1,transaction=b)
        sc = CommonObject(id=2,transaction=c) 
        ss = [sa,sb,sc]
        index = calc_index_adjacent(ss)
        self.assertEquals([1000, 800, 886, 1132],index.tolist())
    
    #deprecated
    def test_calc_index_base0_and_old(self):
        a = np.array([(0,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(1000,1000,1000,1000)])
        b = np.array([(0,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,2000,1000)])
        c = np.array([(0,0,0,0),(700,700,300,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(1000,0,1000,1000)])
        sa = CommonObject(id=0,transaction=a)
        sb = CommonObject(id=1,transaction=b)
        sc = CommonObject(id=2,transaction=c) 
        ss = [sa,sb,sc]
        index = calc_index_base0(ss)
        self.assertEquals([1000, 800, 1007, 1124],index.tolist())
        #不动点
        index_old = calc_index_base0_old(ss)
        self.assertEquals(index.tolist(),index_old.tolist())
        #print index


if __name__ == "__main__":
    import logging
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    unittest.main()
