# -*- coding: utf-8 -*-

'''
    建立能量模型的尝试
    1. 表示关系
       s = 价格变化, 以点为单位
       t = 时间，以分为单位
       f = 成交量，以张为单位, 分为Fup,Fdown((以下简写为Fu/Fd))
           每分钟成交量= Fu + Fd
           合力 dF = Fu - Fd  
       m = 持仓量，以张为单位
    2. 基本公式
       以当前级别的line为依据，判断处于上升还是下降途中
            并且前一高/低点为s的起点
       平均速度: v = s/t
       加速度: Fup - Fdown = ma ==> a = (Fu-Fd)/m
       动能: E = mvv/2
       动能差:  dE = E(n) - E(n-1)  #要考虑到正功和负功
            另：dE = dFs = (Fu-Fd)*s
    3. 推导
       Fu - Fd = dE / s
       Fu + Fd = svol
       ==>  Fu = (dE/s +svol)/2
            Fd = (svol - dE/s)/2
       这里可能少个系数,来平衡dE和svol的级差

    或者:
        s = v(0)t + att/2
        a = 2(s - v(0)t)/tt
        dF = ma = 2m(s-v(0)t)/(tt)

    合并:
        E系列:
            dFE = dE/s * m
        V系列:
            dFV = 2m(s-v0t)/(tt) * k
        l = m/k = dFE / dFV

'''
