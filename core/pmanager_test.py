# -*- coding: utf-8 -*-

import logging

import unittest
from wolfox.fengine.core.pmanager import *

logger = logging.getLogger('wolfox.fengine.core.pmanager_test')

class ModuleTest(unittest.TestCase):
    pass


class PositionTest(unittest.TestCase):
    def test_init(self):    #通路测试
        p = Position()
        self.assertEquals({},p.holdings)
        self.assertEquals([],p.history)

    def test_clear(self):
        p = Position()
        p.holdings = {'a':1}
        p.history = ['a']
        p.clear()
        self.assertEquals({},p.holdings)
        self.assertEquals([],p.history)

    def test_push(self):
        p = Position()
        trade = Trade(0,20010101,10000,1)
        v = p.push(trade,50,1000000,999999000)
        self.assertEquals(2000,trade.tvolume)
        self.assertEquals(160000,trade.ttax)
        self.assertEquals(-20160000,v)
        self.assertEquals(1,len(p.holdings))        
        #同一个股票的第二次加入.被清零
        trade2 = Trade(0,20010201,10000,1)
        v = p.push(trade2,50,1000000,999999000)
        self.assertEquals(0,trade2.tvolume)
        self.assertEquals(0,trade2.ttax)        
        self.assertEquals(0,v)
        #超过限额
        p.holdings.clear()
        v = p.push(trade,50,1000000,10000000)
        self.assertEquals(900,trade.tvolume)
        self.assertEquals(72000,trade.ttax)
        self.assertEquals(-9072000,v)
        self.assertEquals(trade,p.holdings[trade.tstock][0])
        #交易量取整
        trade3 = Trade(3,20010101,10000,1)
        v = p.push(trade3,150,1000000,999999000)
        self.assertEquals(600,trade3.tvolume)
        self.assertEquals(48000,trade3.ttax)
        self.assertEquals(-6048000,v)
        self.assertEquals(2,len(p.holdings))        
        self.assertEquals(trade3,p.holdings[trade3.tstock][0])
        #交易量小于100,风险过大条件
        self.assertEquals(2,len(p.holdings))        
        trade4 = Trade(4,20010101,10000,1)
        v = p.push(trade4,150,10000,999999000)
        self.assertEquals(0,trade4.tvolume)
        self.assertEquals(0,trade4.ttax)
        self.assertEquals(0,v)
        self.assertEquals(2,len(p.holdings))    #未变化
        #交易量小于100,限额过小条件
        trade5 = Trade(5,20010101,10000,1)
        v = p.push(trade5,150,1000000,99000)
        self.assertEquals(0,trade5.tvolume)
        self.assertEquals(0,trade5.ttax)
        self.assertEquals(0,v)
        self.assertEquals(2,len(p.holdings))    #未变化
        
    def test_pop(self):
        p = Position()
        trade = Trade(0,20010101,10000,1)
        v = p.pop(trade)    #空跳出
        self.assertEquals(0,trade.tvolume)
        self.assertEquals(0,trade.ttax)
        self.assertEquals((0,0),v)
        #测试正常跳出
        p.push(trade,50,1000000,999999000)
        trade2 = Trade(0,20010101,11000,1)        
        v = p.pop(trade2)
        self.assertEquals(-2000,trade2.tvolume)
        self.assertEquals(176000,trade2.ttax)        
        self.assertEquals((21824000, -20160000),v)
        self.assertEquals(0,len(p.holdings))

    def test_pop2(self):    #先行多个同向交易的一次pop
        p = Position()
        #先买入
        trade1 = Trade(0,20010101,10000,1000)
        trade2 = Trade(0,20010101,10000,500)
        p.holdings = {trade1.tstock:[trade1,trade2]}
        trade3 = Trade(0,20010101,10000,-1)
        asell,abuy = p.pop(trade3)
        self.assertEquals(-1500,trade3.tvolume)
        self.assertEquals(14880000,asell)
        self.assertEquals(-15120000,abuy)
        #先卖出
        trade4 = Trade(1,20010101,10000,-1000)
        trade5 = Trade(1,20010101,10000,-500)
        p.holdings = {trade4.tstock:[trade4,trade5]}
        trade6 = Trade(1,20010101,10000,1)
        asell,abuy = p.pop(trade6)
        self.assertEquals(1500,trade6.tvolume)
        self.assertEquals(-15120000,asell)
        self.assertEquals(14880000,abuy)


    def test_sell_first(self):
        #print 'in test sell first'
        p = Position()
        trade1 = Trade(0,20010101,10000,-1)
        trade2 = Trade(0,20010101,10000,1)
        am1 = p.push(trade1,100,1000000,999999000)
        self.assertEquals(9920000,am1)
        asell,abuy = p.pop(trade2)
        self.assertEquals(9920000,abuy)
        self.assertEquals(-10080000,asell)
        self.assertEquals(-160000,abuy + asell)
        #print 'end test sell first'

    def test_cost(self):
        p = Position()
        #初始为0
        self.assertEquals(0,p.cost())
        trade = Trade(0,20010101,10000,1)
        v = p.push(trade,50,1000000,999999000)
        self.assertEquals(20160000,p.cost())
        #同一个的第二次加入.被清零
        trade2 = Trade(0,20010201,10000,1)
        v = p.push(trade2,50,1000000,999999000)
        self.assertEquals(20160000,p.cost()) 
        #换个股票
        trade3 = Trade(2,20010201,10000,1)
        v = p.push(trade3,50,1000000,999999000)
        self.assertEquals(40320000,p.cost()) 
        #pop一个
        p.pop(trade)
        self.assertEquals(20160000,p.cost()) 


class AdvancePositionTest(unittest.TestCase):
    def test_push_one(self):
        p = AdvancedPosition()
        trade = Trade(0,20010101,10000,1)
        p.push(trade,10,1000000,9999999000)
        relative_trades = p.holdings[trade.tstock]
        self.assertEquals(1,len(relative_trades))
        self.assertEquals(trade,relative_trades[0])

    def test_push_multi(self):
        p = AdvancedPosition()
        trade1 = Trade(0,20010101,10000,1)
        trade2 = Trade(0,20010102,10000,1)        
        trade3 = Trade(0,20010103,10000,1)  
        trade4 = Trade(1,20010104,10000,1)  #另一个股票
        p.push(trade1,10,1000000,9999999000)
        p.push(trade2,10,1000000,9999999000)
        p.push(trade3,10,1000000,9999999000)        
        p.push(trade4,10,1000000,9999999000)                
        relative_trades = p.holdings[trade1.tstock]
        self.assertEquals(1,len(relative_trades))   #因为价格没有变化，后续的买入被抛弃
        p.clear()
        trade3.tprice = 10010
        p.push(trade1,10,1000000,9999999000)
        p.push(trade2,10,1000000,9999999000)
        p.push(trade3,10,1000000,9999999000)        
        p.push(trade4,10,1000000,9999999000)                
        relative_trades = p.holdings[trade1.tstock]
        self.assertEquals(2,len(relative_trades))   
        self.assertEquals(trade1,relative_trades[0])
        self.assertEquals(trade3,relative_trades[1])
        self.assertEquals(trade1.tvolume/2,trade3.tvolume)

    def test_push_pop_closed(self):
        p = AdvancedPosition()
        trade1 = Trade(0,20010101,10000,1)
        trade2 = Trade(0,20010101,10000,1)        
        trade3 = Trade(0,20010101,10000,1)  
        trade4 = Trade(1,20010101,10000,1)  #另一个股票
        trade5 = Trade(0,20010101,10000,-1)
        p.push(trade1,10,1000000,9999999000)
        p.push(trade2,10,1000000,9999999000)
        p.push(trade3,10,1000000,9999999000)        
        p.push(trade4,10,1000000,9999999000)                
        p.pop(trade5)
        self.assertTrue(trade1.tstock not in p.holdings)


class PositionManagerTest(unittest.TestCase):
    def test_init(self):
        pm = PositionManager()
        self.assertTrue(pm.position)
    
    def test_assets(self):
        pm = PositionManager()
        self.assertEquals(pm.init_size,pm.assets())
        pm.init_size = 100000
        pm.earning = 1200
        self.assertEquals(101200,pm.assets())

    def test_clear(self):
        pm = PositionManager()
        pm.cash = 100000000
        pm.earning = 20000
        trade1 = Trade(0,20010101,10000,1)        
        pm.position.push(trade1,100,100000,999999000)
        self.assertEquals(1,len(pm.position.holdings))
        pm.clear()
        self.assertEquals(pm.init_size,pm.cash)
        self.assertEquals(0,pm.earning)
        self.assertEquals(0,len(pm.position.holdings))

    def test_cur_limit(self):
        pm = PositionManager()
        self.assertEquals(20000000,pm.cur_limit())
        pm.init_size = 10000
        pm.earning = 2000
        pm.max_proportion = 200
        self.assertEquals(2400,pm.cur_limit())
        #超过cash,被取齐
        pm.cash = 1500
        pm.init_size = 1000
        pm.earning = 20000
        pm.max_proportion = 200
        self.assertEquals(1500,pm.cur_limit())
        
    def test_cur_risk(self):
        pm = PositionManager()
        self.assertEquals(1000000,pm.cur_risk())
        pm.init_size = 10000
        pm.earning = 2000
        pm.risk = 100 
        self.assertEquals(1200,pm.cur_risk())

    def test_income_rate(self):
        pm = PositionManager()
        self.assertEquals(0,pm.income_rate())
        pm.earning = 200000
        self.assertEquals(2,pm.income_rate())
        pm.init_size = 1000000
        self.assertEquals(200,pm.income_rate())

    def test_organize_trades(self):
        pm = PositionManager()
        self.assertEquals([],pm.organize_trades([]))
        trade1 = Trade(0,20010101,10000,1)
        trade2 = Trade(0,20010301,12000,-1)
        trade3 = Trade(0,20010205,10000,1)
        trade4 = Trade(0,20010501,9000,-1)
        trade5 = Trade(1,20010201,10000,1)
        trade6 = Trade(1,20010321,10000,-1)
        named_trade1 = [[trade1,trade2],[trade3,trade4]]
        named_trade2 = trades=[[trade5,trade6]]
        rev = pm.organize_trades([named_trade1,named_trade2])
        self.assertEquals(6,len(rev))
        self.assertEquals([trade1,trade5,trade3,trade2,trade6,trade4],rev) 
        #测试有名的空交易
        named_trade3 = []
        rev = pm.organize_trades([named_trade3])
        self.assertEquals(0,len(rev))

    def test_filter(self):  #只测试通路
        pm = PositionManager()
        #空路径
        self.assertEquals([],pm.filter([]))
        #普通测试
        self.assertEquals([],pm.organize_trades([]))
        trade1 = Trade(0,20010101,10000,1)
        trade2 = Trade(0,20010301,12000,-1)
        trade3 = Trade(0,20010205,10000,1)
        trade4 = Trade(0,20010501,9000,-1)
        trade5 = Trade(1,20010201,10000,1)
        trade6 = Trade(1,20010321,10000,-1)
        parent1 = BaseObject(id=1,evaluation=BaseObject(lostavg=100))
        parent2 = BaseObject(id=2,evaluation=BaseObject(lostavg=100))
        trade1.parent = trade2.parent = trade3.parent = trade4.parent = parent1
        trade5.parent = trade6.parent = parent2
        named_trade1 = [[trade1,trade2],[trade3,trade4]]
        named_trade2 = [[trade5,trade6]]
        mts = pm.filter([named_trade1,named_trade2])
        #self.assertEquals(4,len(mts))

    def test_run(self):
        pm = PositionManager()
        #空路径
        pm.run([])
        self.assertEquals([],pm.position.history)
        #普通测试
        trade1 = Trade(0,20010101,10000,1)
        trade2 = Trade(0,20010301,12000,-1)
        trade3 = Trade(0,20010205,10000,1)
        trade4 = Trade(0,20010501,9000,-1)
        trade5 = Trade(1,20010201,10000,1)
        trade6 = Trade(1,20010321,10000,-1)
        parent = BaseObject(id=1,evaluation=BaseObject(lostavg=100))
        trade1.parent = trade2.parent = trade3.parent = trade4.parent = trade5.parent = trade6.parent = parent
        ptrades = [trade1,trade5,trade3,trade2,trade6,trade4]
        #参数必须已经排序
        pm.run(ptrades)
        #结果过滤掉了trade3<->trade4的一组买卖,因为区间交叉了
        self.assertEquals([[trade1,trade2],[trade5,trade6]],pm.position.history)
        self.assertEquals(101664000,pm.cash)    #毛利2000,税费42*8=336,净利1664
        self.assertEquals(1664000,pm.earning)
        self.assertEquals(pm.earning,pm.cash-pm.init_size)

    def test_run_with_advancedposition(self):
        pm = PositionManager(position=AdvancedPosition)
        #空路径
        pm.run([])
        self.assertEquals([],pm.position.history)
        #普通测试
        trade1 = Trade(0,20010101,10000,1)
        trade2 = Trade(0,20010301,12000,-1)
        trade3 = Trade(0,20010205,10000,1)
        trade4 = Trade(0,20010501,9000,-1)
        trade5 = Trade(1,20010201,10000,1)
        trade6 = Trade(1,20010321,10000,-1)
        parent = BaseObject(id=1,evaluation=BaseObject(lostavg=100))
        trade1.parent = trade2.parent = trade3.parent = trade4.parent = trade5.parent = trade6.parent = parent
        ptrades = [trade1,trade5,trade3,trade2,trade6,trade4]
        #参数必须已经排序
        pm.run(ptrades)
        #过滤掉trade3,因为其买入价没有上升，trade4是无匹配的卖出
        self.assertEquals([[trade1,trade2],[trade5,trade6]],pm.position.history)
        self.assertEquals(101664000,pm.cash)    #毛利2000,税费42*8=336,净利1664
        self.assertEquals(1664000,pm.earning)
        self.assertEquals(pm.earning,pm.cash-pm.init_size)
        #设置trade3价格为上升
        trade3.tprice = 11000
        pm.clear()
        pm.run(ptrades)
        self.assertEquals([[trade1,trade3,trade2],[trade5,trade6]],pm.position.history)
        #print trade1.tvolume,trade3.tvolume,trade1.calc(),trade3.calc(),trade2.tvolume,trade2.calc()
        self.assertEquals(102072000,pm.cash)    #毛利2500,税费(10+5.5+15.5*1.2+20)*8=53.5*8=428,净利2072
        self.assertEquals(2072000,pm.earning)
        self.assertEquals(pm.earning,pm.cash-pm.init_size)

    def test_ev_lost(self):
        trade = BaseObject(parent=BaseObject(evaluation=BaseObject(lostavg=10)))
        self.assertEquals(10,ev_lost(trade))

    def test_atr_lost(self):
        trade = BaseObject(price=10000,atr=200)
        self.assertEquals(20,atr_lost(trade))
        self.assertEquals(40,atr_lost_2(trade))


if __name__ == "__main__":
    import logging
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    unittest.main()
