# -*- coding: utf-8 -*-
#因为每个函数都是其它函数的wrapper，只测试通道性

import unittest
from wolfox.fengine.core.d1idiom import *

class ModuleTest(unittest.TestCase):
    def test_down_period(self):
        s = np.array([0,1,2,3,2,0,-1,-5,10,1,2,3,4,5,12,9,10,13])
        self.assertEquals([0,0,0,0,1,2,3,4,0,1,2,3,4,5,0,1,2,0],down_period(s,5).tolist())
        self.assertEquals([0,0,0,0,1,2,3,4,0,1,2,0,0,0,0,1,2,0],down_period(s,2).tolist())
        self.assertEquals([],down_period([]).tolist())

    def test_swingin(self):
        s = swingin(np.array([100,150,180,200,400]),np.array([100,150,180,200,400]),3,500)
        self.assertEquals([1,1,0,1,0],s.tolist())

    def test_swingin1(self):
        s = swingin1(np.array([100,150,180,200,400]),3,500)
        self.assertEquals([1,1,0,1,0],s.tolist())

    def test_up_under(self):
        s = up_under(np.array([100,150,180,200,400,300,200,400]),np.array([100,150,180,200,400,300,500,400]),3,500)
        self.assertEquals([1,0,0,1,0,0,1,1],s.tolist())

    def test_upconfirm(self):
        upconfirm(np.array([1,2,3,4,5]),np.array([2,3,4,5,6]),np.array([4,5,6,7,8]))
        self.assertTrue(True)

    def test_upveto(self):
        upveto(np.array([1,2,3,4,5]),np.array([2,3,4,5,6]),np.array([4,5,6,7,8]),np.array([1,2,3,4,5]))
        self.assertTrue(True)

    def test_sellconfirm(self):
        sellconfirm(np.array([1,2,3,4,5]),np.array([2,3,4,5,6]),np.array([4,5,6,7,8]),np.array([1,2,3,4,5]))
        self.assertTrue(True)

    def test_simplesell(self):
        simplesell(np.array([0,1,0,0,1]),np.array([1,2,3,4,5]),np.array([0,1,2,3,4]),15)
        self.assertTrue(True)

    def test_tsimplesell(self):
        tsimplesell(np.array([0,1,0,0,1]),np.array([1,2,3,4,5]),np.array([0,1,2,3,4]),15)
        self.assertTrue(True)

    def test_confirmedsell(self):
        confirmedsell(np.array([0,1,0,0,1]),np.array([1,2,3,4,5]),np.array([0,1,2,3,4]),np.array([1,2,3,4,5]),np.array([0,1,2,3,4]),np.array([0,1,2,3,4]),15)
        self.assertTrue(True)

    def test_confirmedsellc(self):
        confirmedsellc(np.array([0,1,0,0,1]),np.array([1,2,3,4,5]),np.array([0,1,2,3,4]),np.array([1,2,3,4,5]),np.array([0,1,2,3,4]),15)
        self.assertTrue(True)

    def test_confirmedselll(self):
        confirmedselll(np.array([0,1,0,0,1]),np.array([1,2,3,4,5]),np.array([0,1,2,3,4]),np.array([1,2,3,4,5]),np.array([0,1,2,3,4]),15)
        self.assertTrue(True)

    def test_downup(self):
        downup(np.array([0,1,0,0,1]),np.array([1,2,3,4,5]),15)
        downup(np.array([0,1,0,0,1]),np.array([1,2,3,4,5]),15,5)
        self.assertTrue(True)

    def test_limit_adjuster(self):
        from wolfox.fengine.core.d1idiom import _limit_adjuster_deprecated as _limit_adjuster
        self.assertEquals([],_limit_adjuster(np.array([]),np.array([]),3).tolist())
        css = np.array([1,0,0,1,0,1,0,0])
        cls = np.array([1,1,0,0,0,1,1,1])
        self.assertEquals([0,0,1,0,0,0,0,0],_limit_adjuster(css,cls,3).tolist())
        self.assertEquals([0,0,0,1,0,0,0,0],_limit_adjuster(css,cls,2).tolist())

    def test_limit_adjust_deprecated(self):
        self.assertEquals([],limit_adjust_deprecated(np.array([]),np.array([]),np.array([]),3).tolist())
        css = np.array([1,0,0,1,0,1,0,0])
        cls = np.array([1,1,0,0,0,1,1,1])
        ts0 = np.array([0,0,0,0,0,0,0,0])
        ts1 = np.array([1,1,1,1,1,1,1,1])
        ts2 = np.array([1,1,0,0,1,1,1,1])
        self.assertEquals([0,0,0,0,0,0,0,0],limit_adjust_deprecated(css,cls,ts0).tolist())
        self.assertEquals([0,0,1,0,0,0,0,0],limit_adjust_deprecated(css,cls,ts1).tolist())
        self.assertEquals([0,0,0,1,0,0,0,0],limit_adjust_deprecated(css,cls,ts1,covered=2).tolist())
        self.assertEquals([0,0,0,0,1,0,0,0],limit_adjust_deprecated(css,cls,ts2).tolist())

    def test_limit_adjust(self):
        self.assertEquals([],limit_adjust(np.array([]),np.array([]),np.array([])).tolist())
        css = np.array([1,0,0,1,0,1,0,0])
        cls = np.array([1,1,0,0,0,1,1,1])
        ts0 = np.array([0,0,0,0,0,0,0,0])
        ts1 = np.array([1,1,1,1,1,1,1,1])
        ts2 = np.array([1,1,0,0,1,1,1,1])
        self.assertEquals([0,0,0,0,0,0,0,0],limit_adjust(css,cls,ts0).tolist())
        self.assertEquals([0,0,1,1,0,0,0,0],limit_adjust(css,cls,ts1).tolist())
        self.assertEquals([0,0,0,0,1,0,0,0],limit_adjust(css,cls,ts2).tolist())

    def test_BS_DUMMY(self):
        #空测试
        empty_trans = np.array([(),(),(),(),(),(),()])
        nb,ns = BS_DUMMY(empty_trans,np.array([]),np.array([]))
        self.assertEquals([],nb.tolist())    
        self.assertEquals([],ns.tolist())
        #普通测试
        trans = np.array([(0,0,0,0),(500,550,800,500),(500,550,550,500),(500,550,550,500),(0,0,0,0),(5000,4000,8000,4000),(1000,1000,0,1000)])
        sbuy = np.array([1,0,1,1])
        ssell = np.array([1,0,1,0])
        lb,ls = BS_DUMMY(trans,sbuy,ssell)
        self.assertEquals([1,0,1,1],lb.tolist())
        self.assertEquals([1,0,1,0],ls.tolist())

    def test_B1S1(self):
        #空测试
        empty_trans = np.array([(),(),(),(),(),(),()])
        nb,ns = B1S1(empty_trans,np.array([]),np.array([]))
        self.assertEquals([],nb.tolist())    
        self.assertEquals([],ns.tolist())
        #普通测试
        trans = np.array([(0,0,0,0),(500,550,800,500),(500,550,550,500),(500,550,550,500),(0,0,0,0),(5000,4000,8000,4000),(1000,1000,0,1000)])
        sbuy = np.array([1,0,1,1])
        ssell = np.array([1,0,1,0])
        lb,ls = B1S1(trans,sbuy,ssell)
        self.assertEquals([0,0,0,1],lb.tolist())
        self.assertEquals([0,1,0,0],ls.tolist())

    def test_B1S0(self):
        #空测试
        empty_trans = np.array([(),(),(),(),(),(),()])
        nb,ns = B1S0(empty_trans,np.array([]),np.array([]))
        self.assertEquals([],nb.tolist())    
        self.assertEquals([],ns.tolist())
        #普通测试
        trans = np.array([(0,0,0,0),(500,550,550,500),(500,550,550,500),(500,550,550,500),(0,0,0,0),(5000,4000,8000,4000),(1000,1000,0,1000)])
        sbuy = np.array([1,0,1,1])
        ssell = np.array([1,0,1,0])
        lb,ls = B1S0(trans,sbuy,ssell)
        self.assertEquals([0,0,0,1],lb.tolist()) #第二天涨停，第三天停牌
        self.assertEquals([1,0,0,1],ls.tolist())

    def test_B0S1(self):
        #空测试
        empty_trans = np.array([(),(),(),(),(),(),()])
        nb,ns = B0S1(empty_trans,np.array([]),np.array([]))
        self.assertEquals([],nb.tolist())    
        self.assertEquals([],ns.tolist())
        #普通测试
        trans = np.array([(0,0,0,0),(500,550,550,500),(500,550,550,500),(500,550,550,500),(0,0,0,0),(5000,4000,8000,4000),(1000,1000,0,1000)])
        sbuy = np.array([1,0,1,1])
        ssell = np.array([1,0,1,0])
        lb,ls = B0S1(trans,sbuy,ssell)
        self.assertEquals([1,0,0,1],lb.tolist())
        self.assertEquals([0,1,0,0],ls.tolist()) #最后一天为一线跌停日

    def test_B0S0(self):
        #空测试
        empty_trans = np.array([(),(),(),(),(),(),()])
        nb,ns = B0S0(empty_trans,np.array([]),np.array([]))
        self.assertEquals([],nb.tolist())    
        self.assertEquals([],ns.tolist())
        #普通测试
        trans = np.array([(0,0,0,0),(500,550,550,500),(500,550,550,500),(500,550,550,500),(0,0,0,0),(5000,4000,8000,4000),(1000,1000,0,1000)])
        sbuy = np.array([1,0,1,1])
        ssell = np.array([1,0,1,0])
        lb,ls = B0S0(trans,sbuy,ssell)
        self.assertEquals([1,0,0,1],lb.tolist())
        self.assertEquals([1,0,0,1],ls.tolist())

    def test_bshift(self):
        a = np.array([1,2,3,4])
        self.assertEquals(a.tolist(),B0S0.bshift(a).tolist())
        self.assertEquals(a.tolist(),B0S1.bshift(a).tolist())
        self.assertEquals(rollx(a).tolist(),B1S0.bshift(a).tolist())
        self.assertEquals(rollx(a).tolist(),B1S1.bshift(a).tolist())

    def test_atr_sell_func(self):   #通路测试
        empty_trans = np.array([(),(),(),(),(),(),()])
        atr_sell_func(np.array([]),empty_trans,np.array([]))
        trans = np.array([(0,0,0,0),(500,550,550,500),(500,550,550,500),(500,550,550,500),(0,0,0,0),(5000,4000,8000,4000),(1000,1000,0,1000)])
        satr = np.array([40,50,80,40])
        sbuy = np.array([1,0,1,1])
        s,d = atr_sell_func(sbuy,trans,satr)
        self.assertTrue(True)

    def test_atr_sell_func_old(self):   #通路测试
        empty_trans = np.array([(),(),(),(),(),(),()])
        atr_sell_func_old(np.array([]),empty_trans,np.array([]))
        trans = np.array([(0,0,0,0),(500,550,550,500),(500,550,550,500),(500,550,550,500),(0,0,0,0),(5000,4000,8000,4000),(1000,1000,0,1000)])
        satr = np.array([40,50,80,40])
        sbuy = np.array([1,0,1,1])
        s,d = atr_sell_func_old(sbuy,trans,satr)
        self.assertTrue(True)

    def test_atr_seller(self):
        a = np.array([(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(13,14)])
        sa = CommonObject(id=3,transaction=a,atr=np.array([1,2]))
        bs = np.array([0,1])
        atr_seller(sa,bs)
        #print sa.down_limit
        self.assertEquals(2,len(sa.down_limit))
        #空测试
        a = np.array([(),(),(),(),(),(),()])
        sa = CommonObject(id=3,transaction=a,atr=np.array([]))
        bs = np.array([])
        atr_seller(sa,bs)
        self.assertTrue(True)


    def test_atr_seller_factory(self):  #通路测试
        a = np.array([(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(13,14)])
        sa = CommonObject(id=3,transaction=a,atr=np.array([1,2]))
        bs = np.array([0,1])
        seller1 = atr_seller_factory(1000)
        seller2 = atr_seller_factory(2000)
        seller3 = atr_seller_factory(3000,30)        
        seller1(sa,bs)
        seller2(sa,bs)        
        seller3(sa,bs)
        self.assertTrue(True)

    def test_atr_xseller_factory(self):  #通路测试
        a = np.array([(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(13,14)])
        sa = CommonObject(id=3,transaction=a,atr=np.array([1,2]))
        bs = np.array([0,1])
        seller1 = atr_xseller_factory(1000)
        seller2 = atr_xseller_factory(2000)
        seller3 = atr_xseller_factory(3000,30)        
        ss1=seller1(sa,bs)
        ss2=seller2(sa,bs)        
        ss3=seller3(sa,bs)
        self.assertEquals(1,ss1[-2])
        self.assertEquals(1,ss2[-2])
        self.assertEquals(1,ss3[-2])        
        b=np.array([[],[],[],[],[],[],[]])
        sb = CommonObject(id=4,transaction=b,atr=np.array([]))
        sb1=seller1(sb,np.array([]))
        self.assertTrue(True)

    def test_atr_xseller_factory(self): #测试最后一个为停牌日
        a = np.array([(1,2,2),(3,4,4),(5,6,6),(7,8,8),(9,10,10),(11,12,0),(13,14,0)])
        sa = CommonObject(id=3,transaction=a,atr=np.array([1,2,2]))
        bs = np.array([0,1,0])
        seller1 = atr_xseller_factory(1000)
        ss1=seller1(sa,bs)
        self.assertEquals(0,ss1[-2])
        self.assertEquals(1,ss1[-3])

    def test_seller_wrapper(self):  #通路测试
        a = np.array([(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(13,14)])
        sa = CommonObject(id=3,transaction=a,atr=np.array([1,2]))
        bs = np.array([0,1])
        ##空测试
        seller_a = sellers_wrapper([])
        self.assertEquals([0,0],seller_a(sa,bs).tolist())
        ##有信号测试
        seller1 = atr_xseller_factory(1000)
        seller2 = atr_xseller_factory(2000)
        seller3 = atr_xseller_factory(3000,30)
        seller_b = sellers_wrapper([seller1])
        self.assertEquals([1,0],seller_b(sa,bs).tolist())
        seller_b = sellers_wrapper([seller1,seller2,seller3])
        self.assertEquals([1,0],seller_b(sa,bs).tolist())
        ##无信号测试
        seller4 = lambda stock,signal,**kwargs:np.zeros_like(signal)
        seller_c = sellers_wrapper([seller4])
        self.assertEquals([0,0],seller_c(sa,bs).tolist())
        #彻底的空测试,参数也为空
        b=np.array([[],[],[],[],[],[],[]])
        sb = CommonObject(id=4,transaction=b,atr=np.array([]))
        sb1=seller_a(sb,np.array([]))
        sb2=seller_b(sb,np.array([]))
        self.assertEquals([],sb1.tolist())
        self.assertEquals([],sb2.tolist())        
        self.assertTrue(True)


    def test_vdis(self):    #只测试通路
        na = np.array([])
        a = np.array(np.array([1,2,2]))
        u1,u2,d1,d2 = vdis(na,na,na,na,na)
        self.assertEquals([],u1.tolist())
        u1,u2,d1,d2 = vdis(a,a,a,a,a)
        self.assertTrue(True)

    def test_xc_ru(self):
        na = np.array([])
        a = np.array(np.array([1,2,2]))
        self.assertEquals([],xc_ru(na,na,na,na,na).tolist())
        xc_ru(a,a,a,a,a)
        self.assertTrue(True)

    def test_xc_ru2(self):
        na = np.array([])
        a = np.array(np.array([1,2,2]))
        self.assertEquals([],xc_ru2(na,na,na,na,na).tolist())
        xc_ru2(a,a,a,a,a)
        self.assertTrue(True)

    def test_macd_ru(self):
        na = np.array([])
        a = np.array(np.array([1,2,2]))
        self.assertEquals([],macd_ru(na,na,na,na)[0].tolist())
        macd_ru(a,a,a,a)
        self.assertTrue(True)

    def test_macd_ru2(self):
        na = np.array([])
        a = np.array(np.array([1,2,2]))
        self.assertEquals([],macd_ru2(na,na,na,na)[0].tolist())
        macd_ru2(a,a,a,a)
        self.assertTrue(True)

    def test_macd_ruv(self):
        na = np.array([])
        a = np.array(np.array([1,2,2]))
        self.assertEquals([],macd_ruv(na,na,na,na,na)[0].tolist())
        macd_ruv(a,a,a,a,a)
        self.assertTrue(True)


if __name__ == "__main__":
    import logging
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    unittest.main()
