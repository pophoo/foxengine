# -*- coding: utf-8 -*-

"""
基本遗传算法:
"""

import random
from math import log
import logging
from wolfox.foxit.base.tutils import linelog
import wolfox.fengine.core.cruiser.genetichelper as helper

logger = logging.getLogger('wolfox.fengine.core.cruiser.genetic')

class Nature(object):
    __slots__ = 'judge','fitness_ranker','selector','reproducer','crossover_rate','mutation_rate','goal','generation','judgecache'
    #目标值打分(按照寻优目标值，针对个体，要求为非负数)、适应度评估(按概率,针对群体，如排序法)
    #选择子(按照概率分布,如轮盘赌等)，根据父代产生子代(包含重组策略)
    #终止目标、当前代数

    def __init__(self,judge,fitness_ranker,selector,reproducer,goal = 99.0):
        self.judge = judge
        self.fitness_ranker = fitness_ranker
        self.selector = selector
        self.reproducer = reproducer
        self.generation = 0
        self.judge = judge
        self.judgecache = {}
        self.goal = goal * 1.0  #转换为浮点数
        
    def run(self,population, n):
        ''' 以population为初始种群，迭代n代或者达到goal
            返回最终的population和迭代次数
        '''
        assert n > 0
        for i in range(n):
            print 'begin loop %s' % i
            logger.debug(u'begin loop %s' % i)
            self.generation = i
            scores = [ self.cached_judge(cell) for cell in population]  #每代按目标值打分
            if(max(scores) >= self.goal):
                #linelog('出现满足要求的解法，迭代终止于第%s代' % i)
                logger.debug(u'出现满足要求的解法，迭代终止于第%s代' % i)
                break
            fitness = self.fitness_ranker(scores)   #确定适应度(以0.0001为单位),总和为10000
            #print scores,fitness
            seeds,gametes = self.selector(population,fitness)    #选出所需数目的候选种子
            population = self.reproducer(seeds,gametes)  #交配
        for k,v in sorted(self.judgecache.items(),cmp=lambda x,y:x[1]-y[1]):  #排序
            logger.debug('%s:%s',k,v)
        return population,i 
 
    def cached_judge(self,cell): #judge缓存
        skey = repr(cell)
        if(skey not in self.judgecache):
            #print 'can not find:',skey
            self.judgecache[skey] = self.judge(cell)
        return self.judgecache[skey]
        
 
class Cell(object):   #整数基因个体
    __slots__ = 'length','crossoverer','genes'
    #length:基因串长度,crossoverer:重组点函数,genes:基因串
    
    def __init__(self,length,crossoverer,genes=None):
        assert not genes or length == len(genes)
        self.length = length
        self.crossoverer = crossoverer
        self.genes = genes
        if(not self.genes): #调用_generate_gene前self.genes必须先行赋值(若条件成立，则其值为None)
            self.genes = [self._generate_gene(i) for i in xrange(length)]

    def __repr__(self):
        return "<genes:%s>" % (repr(self.genes))
        
    def mate(self,other,mutation_rate = 0):  #这种情形必然要交叉
        genes1,genes2 = self.crossoverer(self.genes,other.genes)
        self._intround(genes1)
        self._intround(genes2)
        child1,child2 = self.create_by_genes(genes1),self.create_by_genes(genes2)
        if(random.random() < mutation_rate):
            child1.mutation()
        if(random.random() < mutation_rate):
            child2.mutation()
        return child1,child2

    def mutation(self): #突变
        i = random.randint(0,self.length-1)
        #print 'before mutation,genes[%s]:%s' %(i,self.genes[i])
        self.genes[i] = self.gene_mutation(i)
        #print 'after mutation,genes[%s]:%s' %(i,self.genes[i])

    def _generate_gene(self,index): 
        '''这个方法可能在构建过程中调用，因为用到了self.genes，所以调用方法前self.genes必须已经赋值(其值None也可)'''
        assert index < self.length
        gene = self.random_gene(index)
        while(self.genes and gene == self.genes[index]):
            gene = self.random_gene(index)
        return gene
    
    @staticmethod
    def _intround(genes):
        for i in xrange(len(genes)):
            genes[i] = int(genes[i] + 0.5)
        return genes


class BCell(Cell):#基因为二进制串
    def __init__(self,length,crossoverer,genes=None):
        super(BCell,self).__init__(length,crossoverer,genes)

    def random_gene(self,index):
        return  random.randint(0,1)

    def gene_mutation(self,index):
        return [1,0][self.genes[index]]

    def create_by_genes(self,genes):
        cell = BCell(self.length,self.crossoverer,genes)
        return cell


class CCell(Cell):#基因为字符串
    pool = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def __init__(self,length,crossoverer,genes=None):
        super(CCell,self).__init__(length,crossoverer,genes)

    def random_gene(self,index):
        return  random.choice(self.pool)

    def gene_mutation(self,index):
        return self._generate_gene(index)

    def create_by_genes(self,genes):
        cell = CCell(self.length,self.crossoverer,genes)
        return cell


def rangeround(genes,genes_max):
    assert len(genes) == len(genes_max)
    for i in xrange(len(genes)):
        genes[i] = genes[i] % genes_max[i]
    return genes

class NCell(Cell):#整数基因
    __slots__ = 'genes_max'  #genes_max:单个基因的最大值

    def __init__(self,genes_max,crossoverer,genes=None):
        self.genes_max = genes_max    #必须先设置，因为后面要用到
        super(NCell,self).__init__(len(genes_max),crossoverer,genes)

    def random_gene(self,index):
        return  random.randint(0,self.genes_max[index])

    def gene_mutation(self,index):   #可以采取一些比较复杂的算法，如公式2.61,这里简单处理
        return self._generate_gene(index)

    def create_by_genes(self,genes):
        rangeround(genes,self.genes_max)
        cell = NCell(self.genes_max,self.crossoverer,genes)
        return cell


class NCell2(Cell): #NCell的变化版本，变异时只变化一位
    __slots__ = 'genes_max','genes_bits'  #genes_max:单个基因的最大值,genes_bits:单个基因的最大位数
    ''' 基因值到真实参数值的变换，因为余数与变异的原因，需要在外部使用者确定，通常采用 基因值/genes_max最近的质数 % genes_max
        这里不保存每个gene的max值
    '''

    def __init__(self,genes_max,crossoverer,genes=None):
        self.genes_max = genes_max
        self.genes_bits = self.calc_bits(genes_max)    #必须先设置，因为后面要用到
        super(NCell2,self).__init__(len(genes_max),crossoverer,genes)

    def random_gene(self,index):
        return  random.randint(0,self.genes_max[index])

    def gene_mutation(self,index):   #1位变异算法,不能超过当前最大值(好像存在概率问题??对于uplimit和1<<bitnumber-1之间的数字?又好像没有??)
        uplimit = self.genes_max[index]
        curv = self.genes[index]
        nextv = curv
        while(nextv > uplimit or nextv == curv): 
            nextv = helper.integer_mutation1(self.genes[index],self.genes_bits[index])
            #print curv,self.genes_bits[index],uplimit,nextv
        return nextv
               
    def create_by_genes(self,genes):
        rangeround(genes,self.genes_max)
        cell = NCell2(self.genes_max,self.crossoverer,genes)
        return cell

    @staticmethod
    def calc_bits(genes_max):
        bits = []
        for uplimit in genes_max:
            bits.append(helper.calc_bitnumber(uplimit))
        return bits


def init_population_bc(initializer,size,length,crossover):
    population = []
    for i in xrange(size):
        population.append(initializer(length,crossover))
    return population

def init_population_bc_with_geness(initializer,geness,crossover):
    assert len(geness) > 0
    length = len(geness[0])
    population = []
    for genes in geness:
        population.append(initializer(length,crossover,genes))
    return population

def init_population_n(initializer,size,genes_max,crossover):
    population = []
    for i in xrange(size):
        population.append(initializer(genes_max,crossover))
    return population

def init_population_n_with_geness(initializer,geness,genes_max,crossover):
    assert len(geness) > 0
    population = []
    for genes in geness:
        population.append(initializer(genes_max,crossover,genes))
    return population

