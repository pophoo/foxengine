# -*- coding: utf-8 -*-

"""
遗传算法的辅助函数
"""

import random
from math import log
from bisect import bisect_left as locate

MAX_POPULATION_SIZE = 4096  #最大种群大小
#最小的限制是16，不能更改
RANK_BASE = 10000   #种群适应度的总和(即相当于1),每个1表示万分之一

def accumulate(source):
    sum = 0
    rev = [0] * len(source)
    for i in xrange(0,len(source)):
        sum += source[i]
        rev[i] = sum
    return rev

######crossover(交叉/重组)的控制函数,对应于位串和实值的gene
def random_crossover(parent_genes1,parent_genes2):  #随机交换,#可用于位串和实值
    assert len(parent_genes1) == len(parent_genes2)
    turning_points = random_crosspoints(len(parent_genes1))
    return weave(parent_genes1,parent_genes2,turning_points,exchange)

def uniform_crossover(parent_genes1,parent_genes2):#可用于位串和实值
    '''均匀(一致)交叉,每一位都需要选择. 选择的概率是0.5:0.5(可能0的概率多了0.000...001)'''
    assert len(parent_genes1) == len(parent_genes2)
    genes1,genes2 = parent_genes1[:],parent_genes2[:]   #子代基因默认复制父代
    for i in xrange(len(parent_genes1)):
        if(random.random() > 0.5):  #交叉
            genes1[i],genes2[i] = genes2[i],genes1[i]
    return genes1,genes2

def single_point_crossover(parent_genes1,parent_genes2):#可用于位串和实值
    ''' 两段交换(单点交叉,交叉方式为交换)
        原则上单点交叉可以用参数为1的多点交叉来替换
        但是这里有一个len=2的情形，必然是中点交叉，所以需要一个特殊的处理
    '''
    assert len(parent_genes1) == len(parent_genes2)
    genes1,genes2 = parent_genes1[:],parent_genes2[:]   #子代基因默认复制父代
    if(len(parent_genes1) == 2):#如果只有两个元素，则交叉位必然为1
        turning_points = [1]
    else:
        turning_points = [random.randint(1,len(parent_genes1))]    #cpoint处也交叉,不选0是避免全部交叉，相当于没有交叉
    return weave(parent_genes1,parent_genes2,turning_points,exchange)

def single_point_crossover_g(parent_genes1,parent_genes2):#可用于位串和实值
    ''' 标准两段交换(单点交叉,交叉方式为交换)
        没有特殊情形的单点交叉，可用于bitgroup方式的基因组(bitgroup方式每一个基因组自主交换,因此整体不动或整体互换都有意义)
        相当于multi_points_crossover_factory(1)
    '''
    assert len(parent_genes1) == len(parent_genes2)
    genes1,genes2 = parent_genes1[:],parent_genes2[:]   #子代基因默认复制父代
    turning_points = [random.randint(0,len(parent_genes1))]    #cpoint处也交叉,不选0是避免全部交叉，相当于没有交叉
    return weave(parent_genes1,parent_genes2,turning_points,exchange)

def multi_points_crossover_factory(number=2):  #多点交叉工厂
    def crossover(parent_genes1,parent_genes2):#可用于位串和实值
        '''多段交换(多点交叉,交叉方式为交换)'''
        #print 'number:',number
        assert len(parent_genes1) == len(parent_genes2)
        genes1,genes2 = parent_genes1[:],parent_genes2[:]   #子代基因默认复制父代
        turning_points = [random.randint(0,len(parent_genes1)) for i in xrange(number)]  #交叉点
        turning_points.sort()
        return weave(genes1,genes2,turning_points,exchange)
    return crossover

def discrete_crossover(parent_genes1,parent_genes2):#可用于位串和实值
    '''离散重组，与均匀(一致)交叉的区别是每个子串都可自由选择，不必是交叉(可以两个子串的某个等位基因都来自同一个parent)'''
    assert len(parent_genes1) == len(parent_genes2)
    genes1,genes2 = parent_genes1[:],parent_genes1[:]   #子代基因默认复制parent1
    for i in xrange(len(parent_genes1)):
        if(random.random() > 0.5):  #处理子串1
            genes1[i] = parent_genes2[i]
        if(random.random() > 0.5):  #处理子串2
            genes2[i] = parent_genes2[i]
    return genes1,genes2

def middle_crossover(parent_genes1,parent_genes2,d=0.25):#只用于实值
    ''' 中间重组 子个体 = 父个体1 + a*(父个体2-父个体1)
        a是处于[-d,1+d]上的随机数，通常d取0.25
        每个子代的每个基因都有独立的a值
    '''
    assert len(parent_genes1) == len(parent_genes2)
    genes1,genes2 = [],[]
    random2range = lambda rm,dd = d : -dd + rm * ( 1 + 2 * dd)  
    for i in xrange(len(parent_genes1)):
        a1 = random2range(random.random())
        a2 = random2range(random.random())
        genes1.append(parent_genes1[i] + a1 * (parent_genes2[i]-parent_genes1[i]))
        genes2.append(parent_genes1[i] + a2 * (parent_genes2[i]-parent_genes1[i]))
    #print genes1,genes2
    return genes1,genes2
        
def middle_sym_crossover(parent_genes1,parent_genes2,d=0.25):#只用于实值
    ''' 对称中间重组 
        子个体1 = 父个体1 + a*(父个体2-父个体1)
        子个体2 = 父个体2 + a*(父个体1-父个体2)
        a是处于[-d,1+d]上的随机数，通常d取0.25
        两个子代的每对等位基因共享一个独立的a值
    '''
    assert len(parent_genes1) == len(parent_genes2)
    genes1,genes2 = [],[]
    random2range = lambda rm,dd = d : -dd + rm * ( 1 + 2 * dd)  
    for i in xrange(len(parent_genes1)):
        a = random2range(random.random())
        genes1.append(parent_genes1[i] + a * (parent_genes2[i]-parent_genes1[i]))
        genes2.append(parent_genes2[i] + a * (parent_genes1[i]-parent_genes2[i]))
    return genes1,genes2


def linear_crossover(parent_genes1,parent_genes2,d=0.25):#只用于实值
    ''' 线性重组 子个体 = 父个体1 + a*(父个体2-父个体1)
        a是处于[-d,1+d]上的随机数，通常d取0.25
        每个子代共享一个独立的a值
    '''
    assert len(parent_genes1) == len(parent_genes2)
    genes1,genes2 = [],[]
    random2range = lambda rm,dd = d : -dd + rm * ( 1 + 2 * dd)  
    a1 = random2range(random.random())
    a2 = random2range(random.random())
    for i in xrange(len(parent_genes1)):
        genes1.append(parent_genes1[i] + a1 * (parent_genes2[i]-parent_genes1[i]))
        genes2.append(parent_genes1[i] + a2 * (parent_genes2[i]-parent_genes1[i]))
    return genes1,genes2

def linear_sym_crossover(parent_genes1,parent_genes2,d=0.25):#只用于实值
    ''' 对称线性重组 
        子个体1 = 父个体1 + a*(父个体2-父个体1)
        子个体2 = 父个体2 + a*(父个体1-父个体2)
        a是处于[-d,1+d]上的随机数，通常d取0.25
        所有子代共享a值
    '''
    assert len(parent_genes1) == len(parent_genes2)
    genes1,genes2 = [],[]
    random2range = lambda rm,dd = d : -dd + rm * ( 1 + 2 * dd)  
    a = random2range(random.random())
    for i in xrange(len(parent_genes1)):
        genes1.append(parent_genes1[i] + a * (parent_genes2[i]-parent_genes1[i]))
        genes2.append(parent_genes2[i] + a * (parent_genes1[i]-parent_genes2[i]))
    return genes1,genes2

def bitgroups_crossover_factory(bitgroups,icrossover=single_point_crossover,icrossover_rate=1.01):
    ''' 位串基因组交叉函数
        bitgroups为位串组的size列表，分别表示多少个连续位组成一组以表示一个数字
        icrossover为位串组的交叉方法
        icrossoverrate为外部决定crossover之后，内部各基因组的crossover概率. 
            icrossover > 1表示只要进入这个函数，每个定位基因必然以icrossover方式交叉
        如果icrossover = uniform_crossover,且icrossover_rate>1.0，则相当于直接使用uniform_crossover
    '''
    def crossover(parent_genes1,parent_genes2):
        assert len(parent_genes1) == len(parent_genes2) == sum(bitgroups)
        cur = 0
        genes1,genes2 = [],[]
        for limit in bitgroups:
            if(random.random() < icrossover_rate):
                cgenes1,cgenes2 = icrossover(parent_genes1[cur:cur+limit],parent_genes2[cur:cur+limit])
                genes1.extend(cgenes1)
                genes2.extend(cgenes2)
            else:
                genes1.extend(parent_genes1[cur:cur+limit])
                genes2.extend(parent_genes2[cur:cur+limit])
            cur += limit
        #print 'parents:',parent_genes1,parent_genes2
        #print 'children:',genes1,genes2
        return genes1,genes2
    return crossover

###重组/交叉模板函数###
def weave(parent_genes1,parent_genes2,turning_points,weave_functor): 
    ''' 重组子,根据两个父基因组和交叉转折点(turning_points，交叉状态的反转点)，以及交叉状态下的操作函数weave_functor
        生成子代基因
    '''
    assert len(parent_genes1) == len(parent_genes2)
    if(len(turning_points) == 0):
        return parent_genes1,parent_genes2
    assert turning_points[-1] <= len(parent_genes2)
    genes1,genes2 = parent_genes1[:],parent_genes2[:]   #子代基因默认复制父代
    ttps = turning_points + [len(parent_genes1)]    #哨兵点,必要时启动最后一段的交叉
    #print ttps
    pre = 0
    cross_flag = False
    for tp in ttps:
        if(cross_flag):
            weave_functor(genes1,genes2,pre,tp)
        cross_flag = not cross_flag
        pre = tp
    return genes1,genes2

#具体的重组/交叉函数
def exchange(genes1,genes2,begin,end): #等位交换交叉子,交叉从[begin,end)的等位基因
    assert len(genes1) == len(genes2)
    assert 0 <= begin  <= end <= len(genes1)
    for index in xrange(begin,end):
        genes1[index],genes2[index] = genes2[index],genes1[index]
    return genes1,genes2

###其它的重组/交叉辅助函数
def random_crosspoints(gene_length):
    ''' 随机多点交叉
        计算各个部分的重组转折点
        从0到第一个转折点的部分为第一部分，依次为第二、三、四....
        每个奇数部分不交叉(0表示)，偶数部分交叉(1表示)
    '''
    lastpart = random.randint(1,gene_length)    #lastpart不能为0，否则将不会进入循环
    turning_points = []
    curpoint = 0
    while(curpoint < lastpart):
        part = random.randint(0,gene_length - curpoint)
        curpoint += part
        turning_points.append(curpoint)
    return turning_points

######适应度
###适应度计算
def linear_rank(scores):
    return _simple_rank(scores,_calc_linear_rank)

def nonlinear_rank(scores):
    return _simple_rank(scores,_calc_nonlinear_rank)

def intround(fv):
    return int(fv + 0.5)

_indices = xrange(MAX_POPULATION_SIZE)
def _simple_rank(scores,rank_functor,*args):
    pairs = zip(scores,_indices)
    pairs.sort()    #排序
    pairs.reverse() #倒序，分值最高的在最前面
    ranks = rank_functor(len(scores),*args)
    orders = zip([second for first,second in pairs],ranks)
    orders.sort()
    return [second for first,second in orders]

###适应度数值缓存
cached_linear_ranks = {}
cached_nonlinear_ranks = {}
#线性适应度计算
def _calc_linear_rank(length,first_times = 1.8): 
    ''' 根据<遗传算法--理论、应用与软件实现p29,公式2.50
        返回的列表中每个元素都是以0.0001为单位的整数，表示概率
        这个算法对length没有要求
        但是 1 < first_times < 2 (<1变为倒序，>2会在最后部分出现负数)
    '''
    ranks_key = '%s_%s' % (length,first_times)
    if(ranks_key in cached_linear_ranks):
        return cached_linear_ranks[ranks_key]
    ns = 2 * first_times - 2.0
    d1 = 1.0/length
    d2 = 1.0/(length-1)
    #print ns,d1,d2
    ranks = []
    for i in xrange(0,length):
        #print RANK_BASE * d1 * (first_times - ns*i*d2)
        ranks.append(intround(RANK_BASE * d1 * (first_times - ns*i*d2)))
    #print ranks,sum(ranks)
    epsl = RANK_BASE - sum(ranks)
    ranks[0] += epsl    #差额加到第一个
    cached_linear_ranks[ranks_key] = ranks
    return ranks

#非线性适应度计算
def _calc_nonlinear_rank(length,first=0.2):
    ''' 根据<遗传算法--理论、应用与软件实现p30,公式2.51
        返回的列表中每个元素都是以0.0001为单位的整数，表示概率
        要求length>=16. (否则计算误差很难忽略)
        first为排序第一的元素的概率，默认为0.2，并且 0 < first < 1 (因为有epsl的调整，所以first只要>0就可以.为0则第一元素为10000，不合法)
    '''
    assert length >= 16 #如果length太小，这个算法是有问题的
    ranks_key = '%s_%s' % (length,first)
    if(ranks_key in cached_nonlinear_ranks):
        return cached_nonlinear_ranks[ranks_key]
    factor = 1-first
    ranks = [intround(first * RANK_BASE)]
    cur = first
    for i in xrange(1,length):
        cur = cur * factor
        ranks.append(intround(cur * RANK_BASE))
    epsl = RANK_BASE - sum(ranks)
    ranks[0] += epsl    #差额加到第一个
    cached_nonlinear_ranks[ranks_key] = ranks
    return ranks

######选择算法,所有的选择算法都返回2个长度为种群长度*2的序列,第一个序列为随机序列，第二个序列为前者的配对序列(当第一序列元素需要配对的时候)
###这样，就能处理局部选择法
#轮盘选择
def roulette(sums):
    v = random.randint(0,sums[-1])
    return locate(sums,v)

#序列距离
bits = [0,1]
dcache = {}

def cached_distance2(seq1,seq2):
    skey = repr(seq1) + repr(seq2)
    if(skey not in dcache):
        #print 'new distance'
        dcache[skey] = distance2(seq1,seq2)
    else:
        #print 'cached distance'
        pass
    return dcache[skey]

def distance2(seq1,seq2):   #求两个序列的距离
    assert len(seq1) > 0
    if(isinstance(seq1[0],int)):
        if(seq1[0] not in bits or seq1[-1] not in bits or seq2[0] not in bits or seq2[1] not in bits):
            #先作简单判断，避免下面一个判断的耗时操作
            return distance2i(seq1,seq2)
        elif(set(seq1).issubset([0,1])):#略去对set(seq2)的判断
            return distance2b(seq1,seq2)
        else:#仍然是整数序列
            return distance2i(seq1,seq2)
    elif(isinstance(seq1[0],str)):
        return distance2c(seq1,seq2)
    else:
        assert False

def distance2c(seq1,seq2):#求两个字符序列的距离
    assert len(seq1) == len(seq2)
    sum = 0
    for i in xrange(len(seq1)):
        sd = ord(seq1[i]) - ord(seq2[i])
        sum += sd * sd
    return sum

def distance2i(seq1,seq2):   #求两个实数序列的距离
    assert len(seq1) == len(seq2)
    sum = 0
    for i in xrange(len(seq1)):
        sum += (seq1[i] - seq2[i]) * (seq1[i] - seq2[i])
    return sum

def distance2b(seq1,seq2):   #求两个位序列的相差位数
    assert len(seq1) == len(seq2)
    sum = 0
    for i in xrange(len(seq1)):
        sum += seq1[i] - seq2[i] > 0 and seq1[i] - seq2[i] or seq2[i] - seq1[i]
    return sum

##查找邻集
#整数邻集
def find_adjacents(population,seed,adj_number,distancer = cached_distance2):
    ''' population为种群序列,seed为选中的个体,adj_number为该索引中需要选出的最近距离的邻居数
        返回找到的邻集的索引
    '''
    assert adj_number < len(population)
    distance2s = [distancer(seed.genes,unit.genes) for unit in population]
    pairs = zip(distance2s,_indices)
    pairs.sort()
    return [index for distance,index in pairs[1:adj_number+1]]

#轮盘赌选择算法
def roulette_wheel_selection_factory(times=1):
    assert isinstance(times,int)
    def roulette_wheel_selection(population,fitness):
        assert len(fitness) > 0
        length = times * len(fitness)
        sums = accumulate(fitness)    #天然排序
        seeds = []
        gametes = []    #配偶子
        for i in xrange(0,length):
            seed = population[roulette(sums)]
            gamete = population[roulette(sums)]
            while(gamete == seed):
                gamete = population[roulette(sums)]
            seeds.append(seed)            
            gametes.append(gamete)
        return seeds,gametes
    return roulette_wheel_selection

#截断选择法
def truncate_selection_factory(times=1,truncate_rate=0.5):
    assert isinstance(times,int)
    def truncate_selection(population,fitness):
        assert len(fitness) > 0
        length = times * len(fitness)
        pairs = zip(fitness,population)
        pairs.sort()
        pairs.reverse()
        snumber = int(len(pairs) * truncate_rate + 0.5)
        pool = [ cell for fit,cell in pairs][:snumber]
        seeds = []
        gametes = []    #配偶子
        for i in xrange(length):
            seed = random.choice(pool)
            gamete = random.choice(pool)
            while(gamete == seed):
                gamete = random.choice(pool)
            seeds.append(seed)
            gametes.append(gamete)
        return seeds,gametes
    return truncate_selection

#最近邻集选择法工厂 类似于p31中的线性邻集，但扩散效率恒定
#这个方法计算开销很大，每一代必须做种群大小次数的distance sort.
def adjacent_selection_factory(times=1,adj_factor = 0.2,adj_finder = find_adjacents):
    def adjacent_selection(population,fitness):    #adjnumber邻接因子,为种群数的一个百分比
        ''' 对于从fitness中找到的每个随机点，其gemete从距离最近的len(fitness) * adj_factor个元素中随机选择'''
        length = times * len(fitness)
        adj_number = intround(len(fitness) * adj_factor)
        #print adj_number,len(population),len(fitness),len(fitness) * adj_factor
        sums = accumulate(fitness)    #天然排序
        seeds = []
        gametes = []    #配偶子
        for i in xrange(0,length):
            seed = population[roulette(sums)]
            seeds.append(seed)
            candidates = find_adjacents(population,seed,adj_number)
            gametes.append(population[candidates[random.randint(0,adj_number-1)]])
        return seeds,gametes
    return adjacent_selection

######变异算法
#整数的二进制表示位数计算
def calc_bitnumber(uplimit):
    return int(log(uplimit,2)+0.99999)

#整数的一位变异
def integer_mutation1(value,bitnumber):
    ''' bitnumber为该整数的上限所占的二进制位数'''
    bit = random.randint(0,bitnumber-1)
    xorv = 1 << bit
    return value ^ xorv
    
######繁殖控制算法
#简单繁殖算法工厂. crossover_rate决定是否交叉，若不交叉则直接复制
def simple_reproducer_factory(crossover_rate,mutation_rate): 
    def reproducer(seeds,gametes):
        #print seeds
        assert len(seeds) == len(gametes)
        children = []
        cur = 0
        while(len(children) < len(seeds)):
            if(random.random() < crossover_rate):
                children.extend(list(seeds[cur].mate(gametes[cur],mutation_rate)))
                cur += 1
            else:
                children.extend([seeds[cur],gametes[cur]])
        assert len(children) == len(seeds)
        #print 'children size: %s' % len(children)
        return children
    reproducer.times_of_length = 1
    return reproducer

#2生1. crossover_rate决定是否交叉，若不交叉则直接复制
def simple21_reproducer_factory(crossover_rate,mutation_rate): 
    def reproducer(seeds,gametes):
        #print seeds
        assert len(seeds) == len(gametes)
        children = []
        cur = 0
        while(len(children) < len(seeds)):
            if(random.random() < crossover_rate):
                child1,child2 = seeds[cur].mate(gametes[cur],mutation_rate)
                children.append(child1) #取第一个子代
                cur += 1
            else:
                children.append(seeds[cur])
        assert len(children) == len(seeds)
        #print 'children size: %s' % len(children)
        return children
    reproducer.times_of_length = 1
    return reproducer

######其它辅助函数
def bits2int(bits): #将bits列表转换为相应的int值,其中高位在前，如[1,0,0,1,1] ==> 19
    value = 0
    length = len(bits)
    for i in xrange(length):
        value += pow(2,length - i - 1) * bits[i]
    return value

#将bits转换为ints,isizes为每个整数占的位数,如[4,6,4,2]等,bits为位串
def bits2ints(isizes,bits):
    assert sum(isizes) == len(bits)
    cur = 0
    ints = []
    for s in isizes:
        ints.append(bits2int(bits[cur:cur+s]))
        cur += s
    return ints

def int2bits(iv,bitnumber):
    bs = []
    while(iv > 0):
        bs.insert(0,iv & 1)
        iv >>= 1
    assert len(bs) <= bitnumber
    bs[0:0] = [0] * (bitnumber - len(bs))
    return bs
        
def ints2bits(isizes,ints):
    assert len(ints) == len(isizes)
    bs = []
    for i in xrange(len(ints)):
        bs.extend(int2bits(ints[i],isizes[i]))
    return bs

