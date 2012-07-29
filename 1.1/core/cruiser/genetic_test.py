# -*- coding: utf-8 -*-

import unittest
import wolfox.lib.pmock as pmock
from random import randint,sample
from wolfox.fengine.core.cruiser.genetic import *
import wolfox.fengine.core.cruiser.genetichelper as helper

class ModuleTest(unittest.TestCase):
    def test_rangeround(self):
        self.assertEquals([100,60,0,20,0],rangeround([100,300,40,-40,-60],[120,120,40,60,60]))
        self.assertRaises(AssertionError,rangeround,[100,300,40,-40],[120,120,40,60,60])
    
    def test_init_population_bc(self):
        size = 10
        length = 20
        pls = init_population_bc(BCell,size,length,helper.random_crossover)
        self.assertEquals(size,len(pls))
        for i in xrange(size):
            self.assertTrue(isinstance(pls[i],BCell))
            self.assertEquals(helper.random_crossover,pls[i].crossoverer)
            for j in xrange(length):
                self.assertTrue(pls[i].genes[j] in (0,1))

    def test_init_population_n(self):
        size = 10
        genes_max = [20000,10000]
        pls = init_population_n(NCell,size,genes_max,helper.random_crossover)
        self.assertEquals(size,len(pls))
        for i in xrange(size):
            self.assertTrue(isinstance(pls[i],NCell))
            self.assertEquals(helper.random_crossover,pls[i].crossoverer)
            self.assertTrue(pls[i].genes[0] <= genes_max[0])
            self.assertTrue(pls[i].genes[1] <= genes_max[1])

    def test_init_population_bc_with_geness(self):
        geness = [[1,0,0,1,1],[0,1,1,0,1],[1,0,0,0,0]]
        length = 5
        pls = init_population_bc_with_geness(BCell,geness,helper.random_crossover)
        self.assertEquals(3,len(pls))
        self.assertTrue(isinstance(pls[0],BCell))
        self.assertTrue(isinstance(pls[1],BCell))
        self.assertTrue(isinstance(pls[2],BCell))
        self.assertEquals(helper.random_crossover,pls[0].crossoverer)
        self.assertEquals(helper.random_crossover,pls[1].crossoverer)
        self.assertEquals(helper.random_crossover,pls[2].crossoverer)
        self.assertEquals(geness[0],pls[0].genes)
        self.assertEquals(geness[1],pls[1].genes)
        self.assertEquals(geness[2],pls[2].genes)

    def test_init_population_n_with_geness(self):
        geness = [[100,200],[12345,56789],[1,2]]
        genes_max = [20000,10000]
        pls = init_population_n_with_geness(NCell,geness,genes_max,helper.random_crossover)
        self.assertTrue(isinstance(pls[0],NCell))
        self.assertTrue(isinstance(pls[1],NCell))
        self.assertTrue(isinstance(pls[2],NCell))
        self.assertEquals(helper.random_crossover,pls[0].crossoverer)
        self.assertEquals(helper.random_crossover,pls[1].crossoverer)
        self.assertEquals(helper.random_crossover,pls[2].crossoverer)
        self.assertEquals(geness[0],pls[0].genes)
        self.assertEquals(geness[1],pls[1].genes)
        self.assertEquals(geness[2],pls[2].genes)


class NatureTest(unittest.TestCase):
    def test_init(self):
        judge = lambda cell : 100
        reproducer = helper.simple_reproducer_factory(0.8,0.001)
        nature = Nature(judge,helper.nonlinear_rank,helper.roulette_wheel_selection_factory(reproducer.times_of_length),reproducer)
        nature = Nature(judge,helper.nonlinear_rank,helper.roulette_wheel_selection_factory(reproducer.times_of_length),reproducer,101)

    def test_cached_judge(self):
        class TCell(object):pass
        cell = TCell()
        proxy = pmock.Mock()
        proxy.expects(pmock.once()).judge(pmock.eq(cell)).will(pmock.return_value(88))
        reproducer = helper.simple_reproducer_factory(0.8,0.001)
        nature = Nature(proxy.judge,helper.nonlinear_rank,helper.roulette_wheel_selection_factory(reproducer.times_of_length),reproducer)
        nature.cached_judge(cell)
        nature.cached_judge(cell)
        nature.cached_judge(cell)
        proxy.verify()
        
    def test_run_loopout(self): #未找到最优解,完成所有迭代
        class TCell(object):pass
        cell = TCell()
        pls = [cell,cell]
        proxy = pmock.Mock()
        proxy.stubs().method('judge').will(pmock.return_value(88))
        proxy.stubs().method('fitness_ranker').will(pmock.return_value([50,50]))
        proxy.stubs().method('selector').will(pmock.return_value(([cell,cell],[cell,cell])))
        reproducer = lambda seeds,gametes : pls
        reproducer.times_of_length = 1
        nature = Nature(proxy.judge,proxy.fitness_ranker,proxy.selector,reproducer)
        times = 20
        rpls,laststep = nature.run(pls,20)
        self.assertEquals(times-1,laststep)
        self.assertEquals(pls,rpls)

    def test_run_0(self): #迭代次数非法
        pls = []
        fn = lambda x : x   #桩基
        nature = Nature(fn,fn,fn,fn)
        self.assertRaises(AssertionError,nature.run,pls,0)

    def test_run_1(self): #第一次就找到最优解
        class TCell(object):pass
        cell = TCell()
        pls = [cell,cell]
        proxy = pmock.Mock()
        proxy.stubs().method('judge').will(pmock.return_value(100))
        proxy.stubs().method('fitness_ranker').will(pmock.return_value([50,50]))
        proxy.stubs().method('selector').will(pmock.return_value(([cell,cell],[cell,cell])))
        reproducer = lambda seeds,gametes : pls
        reproducer.times_of_length = 1
        nature = Nature(proxy.judge,proxy.fitness_ranker,proxy.selector,reproducer)
        times = 20
        rpls,laststep = nature.run(pls,20)
        proxy.verify()
        self.assertEquals(0,laststep)
        self.assertEquals(pls,rpls)

    def test_run_2(self):   #第二代找到最优解
        #print 'begin run2'
        class TCell(object):pass
        cell,cell2 = TCell(),TCell()
        pls = [cell,cell]
        pls2 = [cell2,cell2]
        proxy = pmock.Mock()
        proxy.expects(pmock.once()).judge(pmock.eq(cell)).will(pmock.return_value(88))
        proxy.expects(pmock.once()).judge(pmock.eq(cell2)).will(pmock.return_value(100))
        proxy.stubs().method('fitness_ranker').will(pmock.return_value([50,50]))
        proxy.stubs().method('selector').will(pmock.return_value(([cell,cell],[cell,cell])))
        reproducer = lambda seeds,gametes : pls2
        reproducer.times_of_length = 1
        nature = Nature(proxy.judge,proxy.fitness_ranker,proxy.selector,reproducer)
        times = 20
        rpls,laststep = nature.run(pls,20)
        proxy.verify()
        self.assertEquals(1,laststep)
        self.assertEquals(pls2,rpls)
        #print 'end run2'

class CellTest(unittest.TestCase):
    def test_init(self):
        Cell.random_gene = lambda self,i : i
        cell = Cell(10,helper.single_point_crossover)
        self.assertEquals(range(10),cell.genes)
        cell2 = Cell(10,helper.single_point_crossover,range(10))
        self.assertEquals(range(10),cell2.genes)
        self.assertRaises(AssertionError,Cell,10,helper.single_point_crossover,range(5))

    def test_repr(self):
        Cell.random_gene = lambda self,i : i
        cell = Cell(3,helper.single_point_crossover)
        self.assertEquals('<genes:[0, 1, 2]>',repr(cell))

    def test_intround(self):
        self.assertEquals([1,2,3,4,5],Cell._intround([1,2,2.6,4.2,4.5]))

    def test_generate_gene(self):
        Cell.random_gene = lambda self,i : randint(0,9)
        cell = Cell(10,helper.single_point_crossover)
        self.assertRaises(AssertionError,cell._generate_gene,10)
        for i in xrange(20):
            self.assertTrue(cell.genes[5] != cell._generate_gene(5))

    def test_mutation(self):
        Cell.random_gene = lambda obj,i : randint(0,9)
        Cell.gene_mutation = lambda obj,i : obj._generate_gene(i)
        cell = Cell(10,helper.single_point_crossover)
        oldrandint = helper.random.randint
        helper.random.randint = lambda x,y : 5
        try:
            oldv = cell.genes[5]
            for i in xrange(20):
                cell.genes[5] = oldv
                cell.mutation()
                self.assertTrue(oldv != cell.genes[5])
        finally:
            helper.random.randint = oldrandint

    def test_mate(self):
        Cell.random_gene = lambda obj,i : randint(0,9)
        Cell.gene_mutation = lambda obj,i : obj._generate_gene(i)
        Cell.create_by_genes = lambda obj,genes : Cell(obj.length,obj.crossoverer,genes)
        crossoverer = lambda x,y : (y,x)    #直接互换
        cella = Cell(10,crossoverer)
        cellb = Cell(10,crossoverer)
        for i in xrange(20):
            child1,child2 = cella.mate(cellb)
            self.assertEquals(cella.genes,child2.genes)
            self.assertEquals(cellb.genes,child1.genes)
            child1,child2 = cella.mate(cellb,1.01)  #必然变异
            self.assertEquals(cella.genes,child2.genes)
            self.assertEquals(cellb.genes,child1.genes)


class BCellTest(unittest.TestCase):
    def test_init(self):
        bcell1 = BCell(19,helper.single_point_crossover)
        bcell2 = BCell(19,helper.single_point_crossover,range(19))

    def test_random_gene(self):
        bcell = BCell(19,helper.single_point_crossover)
        for i in xrange(24):
            self.assertTrue(bcell.random_gene(1) in (0,1))

    def test_gene_mutation(self):
        bcell = BCell(19,helper.single_point_crossover)
        for i in xrange(24):
            self.assertTrue(bcell.gene_mutation(1) != None)
            self.assertTrue(bcell.gene_mutation(1) != bcell.genes[1])

    def test_create_by_genes(self):
        bcell = BCell(19,helper.single_point_crossover)
        bcell2 = bcell.create_by_genes(bcell.genes)
        self.assertEquals(bcell.genes,bcell2.genes)
        bcell3 = bcell.create_by_genes(range(3,22))
        self.assertEquals(range(3,22),bcell3.genes)


class CCellTest(unittest.TestCase):
    def test_init(self):
        ccell1 = CCell(19,helper.single_point_crossover)
        ccell2 = CCell(19,helper.single_point_crossover,sample(CCell.pool,19))

    def test_random_gene(self):
        ccell = CCell(19,helper.single_point_crossover)
        for i in xrange(24):
            self.assertTrue(ccell.random_gene(1) in CCell.pool)

    def test_gene_mutation(self):
        ccell = CCell(19,helper.single_point_crossover)
        for i in xrange(24):
            self.assertTrue(ccell.gene_mutation(1) != None)
            self.assertTrue(ccell.gene_mutation(1) != ccell.genes[1])

    def test_create_by_genes(self):
        ccell = CCell(19,helper.single_point_crossover)
        ccell2 = ccell.create_by_genes(ccell.genes)
        self.assertEquals(ccell.genes,ccell2.genes)
        genes = sample(CCell.pool,19)
        ccell3 = ccell.create_by_genes(genes)
        self.assertEquals(genes,ccell3.genes)


class NCellTest(unittest.TestCase):
    def test_init(self):
        ncell1 = NCell([100,200,300,400],helper.single_point_crossover)
        ncell2 = NCell([100,200,300,400],helper.single_point_crossover,[1,2,3,4])

    def test_random_gene(self):
        ncell = NCell([10,12,30,40],helper.single_point_crossover)
        for i in xrange(24):
            self.assertTrue(ncell.random_gene(1) <= 12)

    def test_gene_mutation(self):
        ncell = NCell([10,12,30,40],helper.single_point_crossover)
        for i in xrange(24):
            self.assertTrue(ncell.gene_mutation(1) != None)
            self.assertTrue(ncell.gene_mutation(1) != ncell.genes[1])

    def test_create_by_genes(self):
        ncell = NCell([10,12,30,40],helper.single_point_crossover)
        ncell2 = ncell.create_by_genes(ncell.genes)
        self.assertEquals(ncell.genes,ncell2.genes)
        ncell3 = ncell.create_by_genes([31,8,32,17])
        self.assertEquals([1,8,2,17],ncell3.genes)


class NCell2Test(unittest.TestCase):
    def test_init(self):
        ncell1 = NCell2([100,200,300,400],helper.single_point_crossover)
        ncell2 = NCell2([100,200,300,400],helper.single_point_crossover,[1,2,3,4])

    def test_random_gene(self):
        ncell = NCell2([10,12,30,40],helper.single_point_crossover)
        for i in xrange(24):
            self.assertTrue(ncell.random_gene(1) <= 12)
    
    def test_gene_mutation(self):
        ncell = NCell2([10,12,30,40],helper.single_point_crossover)
        for i in xrange(24):
            self.assertTrue(ncell.gene_mutation(1) != None)
            self.assertTrue(ncell.gene_mutation(1) != ncell.genes[1])

    def test_create_by_genes(self):
        ncell = NCell2([10,12,30,40],helper.single_point_crossover)
        ncell2 = ncell.create_by_genes(ncell.genes)
        self.assertEquals(ncell.genes,ncell2.genes)
        ncell3 = ncell.create_by_genes([31,8,32,17])
        self.assertEquals([1,8,2,17],ncell3.genes)

    def test_calc_bits(self):
        self.assertEquals([],NCell2.calc_bits([]))
        self.assertEquals([4,4,5,6],NCell2.calc_bits([15,16,17,33]))


if __name__ == "__main__":
    import logging
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')    
    unittest.main()    
