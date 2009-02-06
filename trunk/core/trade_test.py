# -*- coding: utf-8 -*-

import unittest
from wolfox.common.tcommon import Quote,Trade
from wolfox.fengine.core.trade import *

class ModuleTest(unittest.TestCase):
    def test_buy_first(self):
        self.assertEquals(1,buy_first(-1))
        self.assertEquals(0,buy_first(1))
        self.assertEquals(0,buy_first(0))

    def test_sell_first(self):
        self.assertEquals(1,sell_first(1))
        self.assertEquals(0,sell_first(-1))
        self.assertEquals(0,sell_first(0))

    def test_double_first(self):
        self.assertEquals(0,double_first(-1))
        self.assertEquals(0,double_first(1))
        self.assertEquals(0,double_first(0))

    def test_last_trade(self): #begin=0
        tdate = np.array([20050101,20050102,20050103,20050104,20050105,20050106,20050107,20050108,20050109,20050110])
        tbuy = np.array([101,102,103,104,105,106,107,108,109,110])
        tsell = np.array([1101,1102,1103,1104,1105,1106,1107,1108,1109,1110])        
        signal0 = np.array([0,0,0,0,0,0,0,0,0,0])
        trade = last_trade(1,signal0,tdate,tbuy,tsell)
        self.assertEquals([],trade)
        signal1 = np.array([0,0,1,-1,0,1,0,-1,1,0])
        trades = last_trade(1,signal1,tdate,tbuy,tsell)
        self.assertEquals(1,len(trades))
        self.assertEquals(20050109,trades[0].tdate)
        self.assertEquals(109,trades[0].tprice)
        self.assertEquals(1000,trades[0].tvolume)

    def test_last_trade_with_begin(self):
        tdate = np.array([20050101,20050102,20050103,20050104,20050105,20050106,20050107,20050108,20050109,20050110])
        tbuy = np.array([101,102,103,104,105,106,107,108,109,110])
        tsell = np.array([1101,1102,1103,1104,1105,1106,1107,1108,1109,1110])        
        signal1 = np.array([0,0,1,-1,0,1,0,-1,1,0])
        trades = last_trade(1,signal1,tdate,tbuy,tsell,begin=20050101)
        self.assertEquals(1,len(trades))
        self.assertEquals(20050109,trades[0].tdate)
        self.assertEquals(109,trades[0].tprice)
        self.assertEquals(1000,trades[0].tvolume)
        trades = last_trade(1,signal1,tdate,tbuy,tsell,begin=20050201)
        self.assertEquals(0,len(trades))
        trades = last_trade(1,signal1,tdate,tbuy,tsell,begin=20050103)
        self.assertEquals(1,len(trades))
        self.assertEquals(20050109,trades[0].tdate)
        self.assertEquals(109,trades[0].tprice)
        self.assertEquals(1000,trades[0].tvolume)
        trades = last_trade(1,signal1,tdate,tbuy,tsell,begin=20050104)
        self.assertEquals(0,len(trades))    #全部已经平仓，无未平仓，以卖出开始
        trades = last_trade(1,signal1,tdate,tbuy,tsell,begin=20050105)
        self.assertEquals(1,len(trades))
        self.assertEquals(20050109,trades[0].tdate)
        self.assertEquals(109,trades[0].tprice)
        self.assertEquals(1000,trades[0].tvolume)
        signal1 = np.array([0,0,1,-1,0,1,0,-1,-1,0])
        trades = last_trade(1,signal1,tdate,tbuy,tsell,begin=20050101)
        self.assertEquals(1,len(trades))
        self.assertEquals(20050109,trades[0].tdate)
        self.assertEquals(1109,trades[0].tprice)
        self.assertEquals(-1000,trades[0].tvolume)


    def test_make_trades(self): #begin=0
        tdate = np.array([20050101,20050102,20050103,20050104,20050105,20050106,20050107,20050108,20050109,20050110])
        tbuy = np.array([101,102,103,104,105,106,107,108,109,110])
        tsell = np.array([1101,1102,1103,1104,1105,1106,1107,1108,1109,1110])        
        signal0 = np.array([0,0,0,0,0,0,0,0,0,0])
        trades = make_trades(1,signal0,tdate,tbuy,tsell)
        self.assertEquals([],trades)
        signal1 = np.array([0,0,1,-1,0,1,0,-1,1,0])
        trades = make_trades(1,signal1,tdate,tbuy,tsell)
        self.assertEquals(4,len(trades))

    def test_make_trades_with_begin(self):
        tdate = np.array([20050101,20050102,20050103,20050104,20050105,20050106,20050107,20050108,20050109,20050110])
        tbuy = np.array([101,102,103,104,105,106,107,108,109,110])
        tsell = np.array([1101,1102,1103,1104,1105,1106,1107,1108,1109,1110])        
        signal1 = np.array([0,0,1,-1,0,1,0,-1,1,0])
        trades = make_trades(1,signal1,tdate,tbuy,tsell,begin=20050101)
        self.assertEquals(4,len(trades))
        trades = make_trades(1,signal1,tdate,tbuy,tsell,begin=20050201)
        self.assertEquals(0,len(trades))
        trades = make_trades(1,signal1,tdate,tbuy,tsell,begin=20050103)
        self.assertEquals(4,len(trades))
        trades = make_trades(1,signal1,tdate,tbuy,tsell,begin=20050104)
        self.assertEquals(2,len(trades))    #舍弃20050104的第一个卖出信号
        trades = make_trades(1,signal1,tdate,tbuy,tsell,begin=20050105)
        self.assertEquals(2,len(trades))
        #特殊情况,去除第一个买入信号后，卖出信号也应该抛弃掉，即序列仍然相当于空信号
        signal2 = np.array([0,0,1,0,0,-1,0,0,0,0])
        trades = make_trades(1,signal2,tdate,tbuy,tsell,begin=20050104)
        self.assertEquals(0,len(trades))

    def test_match_trades_successive(self):#连续
        trade1 = Trade(1,20050101,1000,1)
        trade2 = Trade(1,20050101,1100,1)
        trade3 = Trade(1,20050101,800,-1)
        trade4 = Trade(1,20050101,1200,-1)
        trades = [trade1,trade2,trade3,trade4]
        mts = match_trades(trades)
        self.assertEquals(1,len(mts))
        self.assertEquals([trade1,trade2,trade3,trade4],mts[0])

    def test_match_trades_left(self):#包含未闭合交易
        trade1 = Trade(1,20050101,1000,1)
        trade2 = Trade(1,20050101,1100,1)
        trade3 = Trade(1,20050101,800,-1)
        trade4 = Trade(1,20050101,1200,-1)
        trade5= Trade(1,20050101,1200,1)
        trades = [trade1,trade2,trade3,trade4,trade5]
        mts = match_trades(trades)
        self.assertEquals(1,len(mts))
        self.assertEquals([trade1,trade2,trade3,trade4],mts[0])

    def test_match_trades_multi(self):#包含未闭合交易
        trade1 = Trade(1,20050101,1000,1)
        trade2 = Trade(2,20050101,1100,1)
        trade3 = Trade(1,20050101,800,-1)
        trade4 = Trade(2,20050101,1200,-1)
        trade5= Trade(1,20050101,1200,1)
        trade6= Trade(2,20050101,1300,-1)
        trades = [trade1,trade2,trade3,trade4,trade5,trade6]
        mts = match_trades(trades)
        self.assertEquals(2,len(mts))
        self.assertEquals([trade1,trade3],mts[0])
        self.assertEquals([trade2,trade4],mts[1])

    def test_evaluate(self):    #只测试通路
        evaluate([])
        self.assertTrue(True)
    
    def test_DEFAULT_EVALUATE_FILTER(self):
        mnt1 = BaseObject(trades = [1,2,3])
        mnt2 = BaseObject(trades = [10,20,30])
        filtered = DEFAULT_EVALUATE_FILTER([mnt1,mnt2])
        self.assertEquals([1,2,3,10,20,30],filtered)

    def test_gevaluate(self):
        trade1 = Trade(1,20050101,1000,1)
        trade2 = Trade(1,20050101,1100,-1)
        trade3 = Trade(2,20050501,1000,1)
        trade4 = Trade(2,20050501,1100,-1)
        nt1 = BaseObject(name='test1',evaluation=Evaluation([]),trades=[trade1,trade2])
        nt2 = BaseObject(name='test1',evaluation=Evaluation([]),trades=[trade3,trade4])
        ev = gevaluate([nt1,nt2])
        self.assertEquals([[trade1,trade2],[trade3,trade4]],ev.matchedtrades)


if __name__ == "__main__":
    import logging
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    unittest.main()
