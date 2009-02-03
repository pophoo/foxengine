# -*- coding: utf-8 -*-

import unittest
import wolfox.fengine.core.cruiser.genetichelper as helper
import wolfox.fengine.core.cruiser.genetic

class ModuleTest(unittest.TestCase):
    def testAccumulate(self):
        a = range(0,10)
        self.assertEquals([0,1,3,6,10,15,21,28,36,45],helper.accumulate(a))
    
    def test_random_crossover(self):
        genes1 = [1,2,3,4,5,6]
        genes2 = [10,20,30,40,50,60]
        child1,child2 = helper.random_crossover(genes1,genes2)
        #print child1,child2
        for i in xrange(len(child1)):
            self.assertEquals(set((child1[i],child2[i])),set((genes1[i],genes2[i])))
        genes3 = [100,300]
        self.assertRaises(AssertionError,helper.random_crossover,genes1,genes3)

    def test_uniform_crossover(self):
        genes1 = [1,2,3,4,5,6]
        genes2 = [10,20,30,40,50,60]
        child1,child2 = helper.uniform_crossover(genes1,genes2)
        #print child1,child2
        for i in xrange(len(child1)):
            self.assertEquals(set((child1[i],child2[i])),set((genes1[i],genes2[i])))
        genes3 = [100,300]
        self.assertRaises(AssertionError,helper.uniform_crossover,genes1,genes3)
    
    def test_single_point_crossover(self):
        genes1 = [1,2,3,4,5,6]
        genes2 = [10,20,30,40,50,60]
        child1,child2 = helper.single_point_crossover(genes1,genes2)
        #print child1,child2
        for i in xrange(len(child1)):
            self.assertEquals(set((child1[i],child2[i])),set((genes1[i],genes2[i])))
        genes3 = [100,300]
        self.assertRaises(AssertionError,helper.single_point_crossover,genes1,genes3)
        genes3 = [1,2]
        genes4 = [10,20]
        child3,child4 = helper.single_point_crossover(genes3,genes4)        
        self.assertEquals([1,20],child3)
        self.assertEquals([10,2],child4)
        genes5 = [1]
        genes6 = [0]
        child5,child6 = helper.single_point_crossover(genes5,genes6)
        self.assertTrue(True)   #边界检查

    def test_single_point_crossover_g(self):
        genes1 = [1,2,3,4,5,6]
        genes2 = [10,20,30,40,50,60]
        child1,child2 = helper.single_point_crossover_g(genes1,genes2)
        #print child1,child2
        for i in xrange(len(child1)):
            self.assertEquals(set((child1[i],child2[i])),set((genes1[i],genes2[i])))
        genes3 = [100,300]
        self.assertRaises(AssertionError,helper.single_point_crossover,genes1,genes3)
        genes5 = [1]
        genes6 = [0]
        child5,child6 = helper.single_point_crossover_g(genes5,genes6)
        self.assertTrue(True)   #边界检查

    def test_multi_points_crossover_factory(self):
        genes1 = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        genes2 = [10,20,30,40,50,60,70,80,90,100,110,120,130]
        crossover = helper.multi_points_crossover_factory()
        child1,child2 = crossover(genes1,genes2)
        #print child1,child2
        for i in xrange(len(child1)):
            self.assertEquals(set((child1[i],child2[i])),set((genes1[i],genes2[i])))
        crossover2 = helper.multi_points_crossover_factory(1) #相当于单点交叉
        child1,child2 = crossover2(genes1,genes2)
        #print child1,child2
        for i in xrange(len(child1)):
            self.assertEquals(set((child1[i],child2[i])),set((genes1[i],genes2[i])))
        crossover3 = helper.multi_points_crossover_factory(3)
        child1,child2 = crossover3(genes1,genes2)
        #print child1,child2
        for i in xrange(len(child1)):
            self.assertEquals(set((child1[i],child2[i])),set((genes1[i],genes2[i])))
        genes3 = [100,300]
        self.assertRaises(AssertionError,crossover,genes1,genes3)
        genes3,genes4 = [1],[0]
        crossover(genes3,genes4)
        crossover2(genes3,genes4)
        crossover3(genes3,genes4)
        self.assertTrue(True)   #边界检查
    

    def test_discrete_crossover(self):
        genes1 = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        genes2 = [10,20,30,40,50,60,70,80,90,100,110,120,130]
        child1,child2 = helper.discrete_crossover(genes1,genes2)
        #print child1,child2
        for i in xrange(len(child1)):
            self.assertTrue(child1[i] in (genes1[i],genes2[i]))
            self.assertTrue(child2[i] in (genes1[i],genes2[i]))
        genes3 = [100,300]
        self.assertRaises(AssertionError,helper.discrete_crossover,genes1,genes3)

    def test_middle_crossover(self):
        genes1 = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        genes2 = [10,20,30,40,50,60,70,80,90,100,110,120,130]
        child1,child2 = helper.middle_crossover(genes1,genes2)
        child1,child2 = helper.middle_crossover(genes1,genes2,0.35)
        #print child1,child2
        #不再验证child1,child2的数值
        genes3 = [100,300]
        self.assertRaises(AssertionError,helper.middle_crossover,genes1,genes3)

    def test_middle_sym_crossover(self):
        genes1 = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        genes2 = [10,20,30,40,50,60,70,80,90,100,110,120,130]
        child1,child2 = helper.middle_sym_crossover(genes1,genes2)
        child1,child2 = helper.middle_sym_crossover(genes1,genes2,0.35)
        #print child1,child2
        #不再验证child1,child2的数值
        genes3 = [100,300]
        self.assertRaises(AssertionError,helper.middle_sym_crossover,genes1,genes3)
    
    def test_linear_crossover(self):
        genes1 = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        genes2 = [10,20,30,40,50,60,70,80,90,100,110,120,130]
        child1,child2 = helper.linear_crossover(genes1,genes2)
        child1,child2 = helper.linear_crossover(genes1,genes2,0.35)
        #print child1,child2
        #不再验证child1,child2的数值
        genes3 = [100,300]
        self.assertRaises(AssertionError,helper.linear_crossover,genes1,genes3)
    
    def test_linear_sym_crossover(self):
        genes1 = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        genes2 = [10,20,30,40,50,60,70,80,90,100,110,120,130]
        child1,child2 = helper.linear_sym_crossover(genes1,genes2)
        child1,child2 = helper.linear_sym_crossover(genes1,genes2,0.35)
        #print child1,child2
        #不再验证child1,child2的数值
        genes3 = [100,300]
        self.assertRaises(AssertionError,helper.linear_sym_crossover,genes1,genes3)

    def test_bitgroups_crossover_factory(self):
        icrossover = lambda x,y:(y,x)
        crossover = helper.bitgroups_crossover_factory([1,3,4],icrossover)
        genes1 = [1,1,0,1,0,0,0,1]
        genes2 = [0,1,0,0,0,1,1,0]
        child1,child2 = crossover(genes1,genes2)
        self.assertEquals([0,1,0,0,0,1,1,0],child1)
        self.assertEquals([1,1,0,1,0,0,0,1],child2)
        crossover0 = helper.bitgroups_crossover_factory([1,3,4],icrossover,-0.01)
        child3,child4 = crossover0(genes1,genes2)
        self.assertEquals([1,1,0,1,0,0,0,1],child3)
        self.assertEquals([0,1,0,0,0,1,1,0],child4)

    def test_weave(self):
        genes1 = [1,2,3,4,5,6,7,8,9]
        genes2 = [10,20,30,40,50,60,70,80,90]
        self.assertRaises(AssertionError,helper.weave,genes1,genes2,[3,11],helper.exchange)   #越界
        self.assertEquals(([1,2,3,4,5,6,7,8,9],[10,20,30,40,50,60,70,80,90]),helper.weave(genes1,genes2,[],helper.exchange))
        self.assertEquals(([1,2,3,40,50,60,70,80,90],[10,20,30,4,5,6,7,8,9]),helper.weave(genes1,genes2,[3],helper.exchange))
        self.assertEquals(([10,20,30,4,5,6,7,8,9],[1,2,3,40,50,60,70,80,90]),helper.weave(genes1,genes2,[0,3],helper.exchange))
        self.assertEquals(([1,2,3,40,50,6,7,8,9],[10,20,30,4,5,60,70,80,90]),helper.weave(genes1,genes2,[3,5],helper.exchange))
        self.assertEquals(([1,2,3,40,50,6,7,80,90],[10,20,30,4,5,60,70,8,9]),helper.weave(genes1,genes2,[3,5,7],helper.exchange))
        self.assertEquals(([1,2,3,4,5,6,7,8,9],[10,20,30,40,50,60,70,80,90]),helper.weave(genes1,genes2,[3,3],helper.exchange))
        self.assertEquals(([1,2,3,4,5,60,70,80,90],[10,20,30,40,50,6,7,8,9]),helper.weave(genes1,genes2,[3,3,5],helper.exchange))
        self.assertEquals(([1,2,3,4,5,6,7,8,9],[10,20,30,40,50,60,70,80,90]),helper.weave(genes1,genes2,[3,3,5,5],helper.exchange))
        self.assertEquals(([1,2,3,4,5,60,7,8,9],[10,20,30,40,50,6,70,80,90]),helper.weave(genes1,genes2,[3,3,5,6],helper.exchange))
        self.assertEquals(([1,2,3,40,50,6,7,8,9],[10,20,30,4,5,60,70,80,90]),helper.weave(genes1,genes2,[3,5,9],helper.exchange))
        self.assertEquals(([1,2,3,40,50,60,70,80,90],[10,20,30,4,5,6,7,8,9]),helper.weave(genes1,genes2,[3,9],helper.exchange))
        turning_points = [3,5]  #测试计算前后turning_points没有变化
        self.assertEquals(([1,2,3,40,50,6,7,8,9],[10,20,30,4,5,60,70,80,90]),helper.weave(genes1,genes2,turning_points,helper.exchange))
        self.assertEquals([3,5],turning_points)

    def test_exchange(self):
        genes1,genes2 = [1,2,3,4,5,6,7,8,9],[10,20,30,40,50,60,70,80,90]
        self.assertEquals(([10,20,30,4,5,6,7,8,9],[1,2,3,40,50,60,70,80,90]),helper.exchange(genes1,genes2,0,3))
        genes1,genes2 = [1,2,3,4,5,6,7,8,9],[10,20,30,40,50,60,70,80,90]
        self.assertEquals(([1,2,3,40,50,6,7,8,9],[10,20,30,4,5,60,70,80,90]),helper.exchange(genes1,genes2,3,5))
        genes1,genes2 = [1,2,3,4,5,6,7,8,9],[10,20,30,40,50,60,70,80,90]
        self.assertEquals(([1,2,3,40,50,60,70,80,90],[10,20,30,4,5,6,7,8,9]),helper.exchange(genes1,genes2,3,9))
        genes1,genes2 = [1,2,3,4,5,6,7,8,9],[10,20,30,40,50,60,70,80,90]
        self.assertEquals(([10,20,30,40,50,60,70,80,90],[1,2,3,4,5,6,7,8,9]),helper.exchange(genes1,genes2,0,9))
        genes1,genes2 = [1,2,3,4,5,6,7,8,9],[10,20,30,40,50,60,70,80,90]
        self.assertRaises(AssertionError,helper.exchange,genes1,genes2,3,11)   #越界
        self.assertRaises(AssertionError,helper.exchange,genes1,genes2,-12,3)   #越界
        self.assertRaises(AssertionError,helper.exchange,genes1,genes2,-12,13)   #越界

    def test_random_crosspoints(self):
        tps = helper.random_crosspoints(17)
        self.assertTrue(0 < len(tps) <= 17)
        tps = helper.random_crosspoints(17) #不同的随机
        self.assertTrue(0 < len(tps) <= 17)
        tps = helper.random_crosspoints(17) #不同的随机
        self.assertTrue(0 < len(tps) <= 17)
        tps = helper.random_crosspoints(17) #不同的随机
        self.assertTrue(0 < len(tps) <= 17)
        tps = helper.random_crosspoints(17) #不同的随机
        self.assertTrue(0 < len(tps) <= 17)
        tps = helper.random_crosspoints(17) #不同的随机
        self.assertTrue(0 < len(tps) <= 17)

    def test_linear_rank(self):
        scores = [12,34,56,213,41,31,4,8,87]
        ranks = helper.linear_rank(scores)
        self.assertEquals(len(scores),len(ranks))   

    def test_nonlinear_rank(self):
        scores = xrange(16) #种群大小32位的限制
        ranks = helper.nonlinear_rank(scores)
        self.assertEquals(len(scores),len(ranks))   
    
    def test_simple_rank(self):
        scores = [1,3,5,7,9,11,13,15,2,4,6,8,10,12,14,16]
        ranks = helper._simple_rank(scores,helper._calc_linear_rank)
        self.assertEquals(len(scores),len(ranks))
        self.assertEquals(helper.RANK_BASE,sum(ranks))
        self.assertTrue(ranks[1] < ranks[9] < ranks[2])
        #print ranks
        #带参数
        ranks = helper._simple_rank(scores,helper._calc_linear_rank,1.4)
        self.assertEquals(len(scores),len(ranks))
        self.assertEquals(helper.RANK_BASE,sum(ranks))
        self.assertTrue(ranks[1] < ranks[9] < ranks[2])
        #print ranks
        ranks = helper._simple_rank(scores,helper._calc_nonlinear_rank)
        self.assertEquals(len(scores),len(ranks))
        self.assertEquals(helper.RANK_BASE,sum(ranks))
        self.assertTrue(ranks[1] < ranks[9] < ranks[2])
        #print ranks
        #带参数
        ranks = helper._simple_rank(scores,helper._calc_nonlinear_rank,0.4)
        self.assertEquals(len(scores),len(ranks))
        self.assertEquals(helper.RANK_BASE,sum(ranks))
        self.assertTrue(ranks[1] < ranks[9] < ranks[2])
        #print ranks

    def test_calc_linear_rank(self):
        length = 32
        ranks = helper._calc_linear_rank(length)
        self.assertEquals(length,len(ranks))
        self.assertEquals(helper.RANK_BASE,sum(ranks))
        for rank in ranks:
            self.assertTrue( 0 <= rank < helper.RANK_BASE )
        self.assertEquals(sorted(ranks,lambda x,y : y - x),ranks)
        ranks2 = helper._calc_linear_rank(length)
        self.assertEquals(id(ranks),id(ranks2))
        #带参数,小于默认值
        ranks = helper._calc_linear_rank(length,1.2)
        self.assertEquals(length,len(ranks))
        self.assertEquals(helper.RANK_BASE,sum(ranks))
        #print ranks
        for rank in ranks:
            self.assertTrue( 0 <= rank < helper.RANK_BASE )
        self.assertEquals(sorted(ranks,lambda x,y : y - x),ranks)
        #大于默认值
        ranks = helper._calc_linear_rank(length,1.9)
        self.assertEquals(length,len(ranks))
        self.assertEquals(helper.RANK_BASE,sum(ranks))
        #print ranks
        for rank in ranks:
            self.assertTrue( 0 <= rank < helper.RANK_BASE )
        self.assertEquals(sorted(ranks,lambda x,y : y - x),ranks)

    def test_calc_nonlinear_rank(self):
        length = 40
        ranks = helper._calc_nonlinear_rank(length)
        self.assertEquals(length,len(ranks))
        self.assertEquals(helper.RANK_BASE,sum(ranks))
        for rank in ranks:
            self.assertTrue( 0 <= rank < helper.RANK_BASE )
        self.assertEquals(sorted(ranks,lambda x,y : y - x),ranks)
        ranks2 = helper._calc_nonlinear_rank(length)
        self.assertEquals(id(ranks),id(ranks2))
        #带参数,小于默认值
        ranks = helper._calc_nonlinear_rank(length,0.1)
        self.assertEquals(length,len(ranks))
        self.assertEquals(helper.RANK_BASE,sum(ranks))
        #print ranks
        for rank in ranks:
            self.assertTrue( 0 <= rank < helper.RANK_BASE )
        self.assertEquals(sorted(ranks,lambda x,y : y - x),ranks)
        #大于默认值
        ranks = helper._calc_nonlinear_rank(length,0.3)
        self.assertEquals(length,len(ranks))
        self.assertEquals(helper.RANK_BASE,sum(ranks))
        #print ranks
        for rank in ranks:
            self.assertTrue( 0 <= rank < helper.RANK_BASE )
        self.assertEquals(sorted(ranks,lambda x,y : y - x),ranks)

    def test_roulette(self):
        sums = [4,10,15,23,88,123,451]
        oldr = helper.random.randint
        try:
            helper.random.randint = lambda x,y : 0
            self.assertEquals(0,helper.roulette(sums))
            helper.random.randint = lambda x,y : 4
            self.assertEquals(0,helper.roulette(sums))
            helper.random.randint = lambda x,y : 22
            self.assertEquals(3,helper.roulette(sums))
            helper.random.randint = lambda x,y : 23
            self.assertEquals(3,helper.roulette(sums))
            helper.random.randint = lambda x,y : 451
            self.assertEquals(6,helper.roulette(sums))
        finally:
            helper.random.randint = oldr
 
    def test_distance2i(self):
        seq1 = [1,3,5,7,9]
        seq2 = [4,1,5,8,12]
        self.assertEquals(23,helper.distance2i(seq1,seq2))
        self.assertRaises(AssertionError,helper.distance2i,seq1,[1,3])

    def test_distance2c(self):
        seq1 = ['a','c','e','g','i']
        seq2 = ['d','a','e','h','l']
        self.assertEquals(23,helper.distance2c(seq1,seq2))
        self.assertRaises(AssertionError,helper.distance2c,seq1,['a','c'])

    def test_distance2b(self):
        seq1 = [1,0,0,1,1]
        seq2 = [0,1,0,0,1]
        self.assertEquals(3,helper.distance2b(seq1,seq2))
        self.assertRaises(AssertionError,helper.distance2b,seq1,[1,0])


    def test_distance2(self):
        seq1 = [1,3,5,7,9]
        seq2 = [4,1,5,8,12]
        self.assertEquals(23,helper.distance2(seq1,seq2))
        self.assertRaises(AssertionError,helper.distance2,seq1,[1,3])
        seq1 = ['a','c','e','g','i']
        seq2 = ['d','a','e','h','l']
        self.assertEquals(23,helper.distance2(seq1,seq2))
        self.assertRaises(AssertionError,helper.distance2,seq1,['a','c'])

    def test_cached_distance2(self):
        seq1 = [1,3,5,7,9]
        seq2 = [4,1,5,8,12]
        self.assertEquals(23,helper.cached_distance2(seq1,seq2))
        self.assertRaises(AssertionError,helper.cached_distance2,seq1,[1,3])
        seq1 = ['a','c','e','g','i']
        seq2 = ['d','a','e','h','l']
        self.assertEquals(23,helper.cached_distance2(seq1,seq2))
        self.assertRaises(AssertionError,helper.cached_distance2,seq1,['a','c'])

    def test_find_adjacents(self):
        class TCell(object):pass
        c1,c2,c3,c4 = TCell(),TCell(),TCell(),TCell()
        c1.genes = [10,20]
        c2.genes = [11,21]
        c3.genes = [17,18]
        c4.genes = [12,18]
        adjs = helper.find_adjacents([c1,c2,c3,c4],c1,1)
        self.assertEquals(1,len(adjs))
        self.assertEquals([1],adjs)
        adjs = helper.find_adjacents([c1,c2,c3,c4],c1,2)
        self.assertEquals(2,len(adjs))
        self.assertEquals([1,3],adjs)
        adjs = helper.find_adjacents([c1,c2,c3,c4],c1,3)
        self.assertEquals(3,len(adjs))
        self.assertEquals([1,3,2],adjs)
        adjs = helper.find_adjacents([c1,c2,c3,c4],c1,0)
        self.assertEquals(0,len(adjs))
        self.assertEquals([],adjs)

    def test_find_adjacents_distancer(self):
        class TCell(object):pass
        c1,c2,c3,c4 = TCell(),TCell(),TCell(),TCell()
        c1.genes = [10,20]
        c2.genes = [11,21]
        c3.genes = [17,18]
        c4.genes = [12,18]
        adjs = helper.find_adjacents([c1,c2,c3,c4],c1,1,helper.distance2)
        self.assertEquals(1,len(adjs))
        self.assertEquals([1],adjs)
        adjs = helper.find_adjacents([c1,c2,c3,c4],c1,2,helper.distance2)
        self.assertEquals(2,len(adjs))
        self.assertEquals([1,3],adjs)
        adjs = helper.find_adjacents([c1,c2,c3,c4],c1,3,helper.distance2)
        self.assertEquals(3,len(adjs))
        self.assertEquals([1,3,2],adjs)
        adjs = helper.find_adjacents([c1,c2,c3,c4],c1,0,helper.distance2)
        self.assertEquals(0,len(adjs))
        self.assertEquals([],adjs)

    def test_roulette_wheel_selection_factory(self):
        pls = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        fitness = [1,3,5,7,9,11,13,15,2,4,6,8,10,12,14,16]
        selector = helper.roulette_wheel_selection_factory()
        seeds,gametes = selector(pls,fitness)
        #print seeds,gametes
        self.assertEquals(len(pls),len(seeds))
        self.assertEquals(len(pls),len(gametes))
        for i in xrange(len(seeds)):
            self.assertTrue(seeds[i] in pls)
            self.assertTrue(gametes[i] in pls)
            self.assertTrue(seeds[i] != gametes[i])
        #times=2
        selector2 = helper.roulette_wheel_selection_factory(2)
        seeds,gametes = selector2(pls,fitness)
        #print seeds,gametes
        self.assertEquals(2*len(pls),len(seeds))
        self.assertEquals(2*len(pls),len(gametes))
        for i in xrange(len(seeds)):
            self.assertTrue(seeds[i] in pls)
            self.assertTrue(gametes[i] in pls)
            self.assertTrue(seeds[i] != gametes[i])
        #times非法
        self.assertRaises(AssertionError,helper.roulette_wheel_selection_factory,1.6)

    def test_truncate_selection_factory(self):
        pls = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        fitness = [1,3,5,7,9,11,13,15,2,4,6,8,10,12,14,16]
        selector = helper.truncate_selection_factory()
        seeds,gametes = selector(pls,fitness)
        #print seeds,gametes
        self.assertEquals(len(pls),len(seeds))
        self.assertEquals(len(pls),len(gametes))
        pool = [5,6,7,8,13,14,15,16]
        for i in xrange(len(seeds)):
            self.assertTrue(seeds[i] in pool)
            self.assertTrue(gametes[i] in pool)
            self.assertTrue(seeds[i] != gametes[i])
        #times=2
        selector2 = helper.truncate_selection_factory(times = 2)
        seeds,gametes = selector2(pls,fitness)
        #print seeds,gametes
        self.assertEquals(2*len(pls),len(seeds))
        self.assertEquals(2*len(pls),len(gametes))
        for i in xrange(len(seeds)):
            self.assertTrue(seeds[i] in pool)
            self.assertTrue(gametes[i] in pool)
            self.assertTrue(seeds[i] != gametes[i])
        #times=2
        selector2 = helper.truncate_selection_factory(truncate_rate = 0.6)
        pool1 = pool + [4,12]
        seeds,gametes = selector2(pls,fitness)
        #print seeds,gametes
        self.assertEquals(len(pls),len(seeds))
        self.assertEquals(len(pls),len(gametes))
        for i in xrange(len(seeds)):
            self.assertTrue(seeds[i] in pool1)
            self.assertTrue(gametes[i] in pool1)
            self.assertTrue(seeds[i] != gametes[i])
        #times非法
        self.assertRaises(AssertionError,helper.truncate_selection_factory,times=1.6)

    def test_adjacent_selection_factory_normal(self):#adj = 0.2,times=1,邻集数为2
        for i in range(20):#多次循环以应对random情况
            class TCell(object):pass
            c1,c2,c3,c4,c5,c6,c7,c8 = TCell(),TCell(),TCell(),TCell(),TCell(),TCell(),TCell(),TCell()
            c1.genes,c2.genes,c3.genes,c4.genes,c5.genes,c6.genes,c7.genes,c8.genes = [10],[11],[12],[13],[14],[15],[16],[17]
            pls = [c1,c2,c3,c4,c5,c6,c7,c8]
            fitness = [1,3,5,7,2,4,6,8]
            selector = helper.adjacent_selection_factory()
            seeds,gametes = selector(pls,fitness)
            self.assertEquals(len(pls),len(seeds))
            self.assertEquals(len(pls),len(gametes))
            for i in xrange(len(seeds)):
                self.assertTrue(seeds[i] in pls)
                self.assertTrue(gametes[i] in pls)
                self.assertTrue(seeds[i] != gametes[i])
                #print seeds[i].genes,gametes[i].genes
                if(seeds[i].genes[0] == 10): 
                    self.assertTrue(gametes[i].genes[0] <= seeds[i].genes[0] + 2)  #邻集数为2
                elif(seeds[i].genes[0] == 17):
                    self.assertTrue(gametes[i].genes[0] >= seeds[i].genes[0] - 2)  #邻集数为2
                else:#中间种子的邻集在两边
                    self.assertTrue( seeds[i].genes[0] - 1 <= gametes[i].genes[0] <= seeds[i].genes[0] + 1)  #邻集数为2
 
    def test_adjacent_selection_factory_finder(self):#adj = 0.2,times=1,邻集数为2
        for i in range(20):#多次循环以应对random情况
            class TCell(object):pass
            c1,c2,c3,c4,c5,c6,c7,c8 = TCell(),TCell(),TCell(),TCell(),TCell(),TCell(),TCell(),TCell()
            c1.genes,c2.genes,c3.genes,c4.genes,c5.genes,c6.genes,c7.genes,c8.genes = [10],[11],[12],[13],[14],[15],[16],[17]
            pls = [c1,c2,c3,c4,c5,c6,c7,c8]
            fitness = [1,3,5,7,2,4,6,8]
            selector = helper.adjacent_selection_factory(adj_finder = helper.find_adjacents)
            seeds,gametes = selector(pls,fitness)
            self.assertEquals(len(pls),len(seeds))
            self.assertEquals(len(pls),len(gametes))
            for i in xrange(len(seeds)):
                self.assertTrue(seeds[i] in pls)
                self.assertTrue(gametes[i] in pls)
                self.assertTrue(seeds[i] != gametes[i])
                #print seeds[i].genes,gametes[i].genes
                if(seeds[i].genes[0] == 10): 
                    self.assertTrue(gametes[i].genes[0] <= seeds[i].genes[0] + 2)  #邻集数为2
                elif(seeds[i].genes[0] == 17):
                    self.assertTrue(gametes[i].genes[0] >= seeds[i].genes[0] - 2)  #邻集数为2
                else:#中间种子的邻集在两边
                    self.assertTrue( seeds[i].genes[0] - 1 <= gametes[i].genes[0] <= seeds[i].genes[0] + 1)  #邻集数为2
 
    def test_adjacent_selection_factory_times2(self):#adj = 0.2,times=1,邻集数为2
        for i in range(20):#多次循环以应对random情况
            class TCell(object):pass
            c1,c2,c3,c4,c5,c6,c7,c8 = TCell(),TCell(),TCell(),TCell(),TCell(),TCell(),TCell(),TCell()
            c1.genes,c2.genes,c3.genes,c4.genes,c5.genes,c6.genes,c7.genes,c8.genes = [10],[11],[12],[13],[14],[15],[16],[17]
            pls = [c1,c2,c3,c4,c5,c6,c7,c8]
            fitness = [1,3,5,7,2,4,6,8]
            selector = helper.adjacent_selection_factory(times=2)
            seeds,gametes = selector(pls,fitness)
            self.assertEquals(2*len(pls),len(seeds))
            self.assertEquals(2*len(pls),len(gametes))
            for i in xrange(len(seeds)):
                self.assertTrue(seeds[i] in pls)
                self.assertTrue(gametes[i] in pls)
                self.assertTrue(seeds[i] != gametes[i])
                #print seeds[i].genes,gametes[i].genes
                if(seeds[i].genes[0] == 10): 
                    self.assertTrue(gametes[i].genes[0] <= seeds[i].genes[0] + 2)  #邻集数为2
                elif(seeds[i].genes[0] == 17):
                    self.assertTrue(gametes[i].genes[0] >= seeds[i].genes[0] - 2)  #邻集数为2
                else:#中间种子的邻集在两边
                    self.assertTrue( seeds[i].genes[0] - 1 <= gametes[i].genes[0] <= seeds[i].genes[0] + 1)  #邻集数为2

    def test_adjacent_selection_factory_adj04(self):#adj = 0.5,times=1,邻集数为4
        for i in range(20):#多次循环以应对random情况
            class TCell(object):pass
            c1,c2,c3,c4,c5,c6,c7,c8 = TCell(),TCell(),TCell(),TCell(),TCell(),TCell(),TCell(),TCell()
            c1.genes,c2.genes,c3.genes,c4.genes,c5.genes,c6.genes,c7.genes,c8.genes = [10],[11],[12],[13],[14],[15],[16],[17]
            pls = [c1,c2,c3,c4,c5,c6,c7,c8]
            fitness = [1,3,5,7,2,4,6,8]
            selector = helper.adjacent_selection_factory(adj_factor = 0.5)
            seeds,gametes = selector(pls,fitness)
            self.assertEquals(len(pls),len(seeds))
            self.assertEquals(len(pls),len(gametes))
            for i in xrange(len(seeds)):
                self.assertTrue(seeds[i] in pls)
                self.assertTrue(gametes[i] in pls)
                self.assertTrue(seeds[i] != gametes[i])
                #print seeds[i].genes,gametes[i].genes
                if(seeds[i].genes[0] == 10): 
                    self.assertTrue(gametes[i].genes[0] <= 14)  #邻集数为4
                elif(seeds[i].genes[0] == 11):
                    self.assertTrue(10 <= gametes[i].genes[0] <= 14)  #邻集数为4
                elif(seeds[i].genes[0] == 16):
                    self.assertTrue(13 <= gametes[i].genes[0] <= 17)  #邻集数为4
                elif(seeds[i].genes[0] == 17):
                    self.assertTrue(gametes[i].genes[0] >= seeds[i].genes[0] - 4)  #邻集数为4
                else:#中间种子的邻集在两边
                    self.assertTrue( seeds[i].genes[0] - 2 <= gametes[i].genes[0] <= seeds[i].genes[0] + 2)  #邻集数为4

    def test_calc_bitnumber(self):
        self.assertEquals(8,helper.calc_bitnumber(129))
        self.assertEquals(7,helper.calc_bitnumber(128))
        self.assertEquals(7,helper.calc_bitnumber(127))
        self.assertEquals(16,helper.calc_bitnumber(65536))
        self.assertEquals(17,helper.calc_bitnumber(65537))
        self.assertEquals(16,helper.calc_bitnumber(65535))

    def test_integer_mutation(self):
        oldr = helper.random.randint
        try:
            helper.random.randint = lambda x,y : 0
            self.assertEquals(56,helper.integer_mutation1(57,6))
            self.assertEquals(57,helper.integer_mutation1(56,6))
            helper.random.randint = lambda x,y : 5
            self.assertEquals(25,helper.integer_mutation1(57,6))
            self.assertEquals(57,helper.integer_mutation1(25,6))
            helper.random.randint = lambda x,y : 3
            self.assertEquals(49,helper.integer_mutation1(57,6))
            self.assertEquals(57,helper.integer_mutation1(49,6))
            helper.random.randint = lambda x,y : 0
            self.assertEquals(33,helper.integer_mutation1(32,6))
            self.assertEquals(32,helper.integer_mutation1(33,6))
            helper.random.randint = lambda x,y : 5
        finally:
            helper.random.randint = oldr

    def test_simple_reproducer_factory(self):
        class TCell(object):pass
        cell = TCell()
        acell,bcell = TCell(),TCell()
        cell.mate = lambda other,mrate : (acell,bcell)
        reproducer = helper.simple_reproducer_factory(0.5,0.5)
        self.assertEquals(1,reproducer.times_of_length)
        seeds = [cell,cell,cell,cell]
        gametes = seeds
        children = reproducer(seeds,gametes)
        #print children
        self.assertEquals(len(seeds),len(children))
        for child in children:
            self.assertTrue(child in [cell,acell,bcell])

    def test_simple21_reproducer_factory(self):
        class TCell(object):pass
        cell = TCell()
        acell,bcell = TCell(),TCell()
        cell.mate = lambda other,mrate : (acell,bcell)
        reproducer = helper.simple21_reproducer_factory(0.5,0.5)
        self.assertEquals(1,reproducer.times_of_length)
        seeds = [cell,cell,cell,cell]
        gametes = seeds
        children = reproducer(seeds,gametes)
        #print children
        self.assertEquals(len(seeds),len(children))
        for child in children:
            self.assertTrue(child in [cell,acell])

    def test_bits2int(self):
        self.assertEquals(19,helper.bits2int([1,0,0,1,1]))
        self.assertEquals(25,helper.bits2int([1,1,0,0,1]))

    def test_bits2ints(self):
        self.assertEquals([19,25],helper.bits2ints([5,5],[1,0,0,1,1,1,1,0,0,1]))
        self.assertEquals([2,0,7,9],helper.bits2ints([2,1,3,4],[1,0,0,1,1,1,1,0,0,1]))
        self.assertRaises(AssertionError,helper.bits2ints,[5,5],[1,0,0,1,1,1,1,0,0,1,1])
        self.assertRaises(AssertionError,helper.bits2ints,[5,7],[1,0,0,1,1,1,1,0,0,1])
        self.assertRaises(AssertionError,helper.bits2ints,[5,5],[1])

    def test_int2bits(self):
        self.assertEquals([1,0,0,1,1],helper.int2bits(19,5))
        self.assertEquals([0,0,1,0,0,1,1],helper.int2bits(19,7))
        self.assertRaises(AssertionError,helper.int2bits,19,4)
        self.assertEquals([1,0,0,0,0,0],helper.int2bits(32,6))
        self.assertEquals([0,1,0,0,0,0,0],helper.int2bits(32,7))
        self.assertRaises(AssertionError,helper.int2bits,32,5)

    def test_ints2bits(self):
        self.assertEquals([1,0,0,1,1,1,1,0,0,1],helper.ints2bits([5,5],[19,25]))
        self.assertEquals([1,0,0,1,1,1,1,0,0,1],helper.ints2bits([2,1,3,4],[2,0,7,9]))


if __name__ == "__main__":
    import logging
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')    
    unittest.main()    
