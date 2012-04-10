# -*- coding: utf8 -*-

'''
    核心交易模块扩展
        针对突破交易和即时止损

'''

from wolfox.fengine.ifuture.utrade import *

###
#打印结果
###
def gen_result(sif,trades):
    extend_s_trade(sif,trades)
    ss = 0
    shigh = 0
    chigh = 0
    for trade in trades:
        ss += trade.profit
        if ss > shigh:
            shigh = ss
            chigh = 0
        else:
            chigh += 1
        trade.chigh = chigh
        print trade.profit,trade.actions[0].date,trade.actions[0].time,trade.actions[0].position,trade.actions[0].price,trade.actions[1].time,trade.actions[1].price,trade.actions[1].index-trade.actions[0].index,trade.orignal.name,trade.chigh


###
###
def extend_s_trade(sif,trades,flost_base = lambda p:p/250):
    '''
        扩展空头交易的信息
    '''
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)         
    for trade in trades:
        ii = trade.actions[0].index #序号
        lbase = flost_base(ldopen[ii])
        trade.move = lbase + trade.profit + 14 #14手续费
        trade.lbase = lbase
        trade.index = ii


def static_classify(sif,trades,afunc):
    '''
        静态归类
    '''
    return sum([afunc(sif,trade) for trade in trades])

def static_analyse(sif,trades):
    '''
        静态分析
    '''
    pass


def day_analyse(sif,trades):
    '''
        分析日交易的情况
        日交易结果来自于 utrade.day_trades
        for trade in trades: print trade.day,trade.twave,trade.tdd,trade.sprofit,trade.profit,trade.rd
    '''
    dd = dnext(nma(sif.waved,5),sif.close,sif.i_cofd)
    for trade in trades:
        #if dd[trade.ii] == 0:
        #    print dd[trade.ii],trade.day
        trade.twave = sif.day2range[trade.day]
        trade.tdd = dd[trade.ii]
        trade.rd = trade.twave * 1.0 / trade.tdd


###
###计算时段的收盘价-开盘价的平均值
###
def calc_ol(sif,oorder,corder):
    oprice = sif.open[sif.iorder==oorder]
    cprice = sif.close[sif.iorder==corder]
    assert len(oprice) == len(cprice),u'开盘序列长度=%s,和收盘序列不一致=%s' % (len(oprice),len(cprice))
    xprice = cprice - oprice
    uxprice = [p for p in xprice if p>0]
    dxprice = [p for p in xprice if p<0]
    return sum(xprice) * 1.0 / len(oprice),sum(uxprice)*1.0/len(uxprice),len(uxprice),sum(dxprice)*1.0/len(dxprice),len(dxprice)


def calc_avg_price(sif,dfrom=0,dend=99999999):
    ''' 计算平均价
    '''
    oaprice = [0] * 271
    caprice = [0] * 271
    for i in range(271):
        oprice = sif.open[gand(sif.iorder==i,sif.date>=dfrom,sif.date<dend)>0]
        cprice = sif.close[gand(sif.iorder==i,sif.date>=dfrom,sif.date<dend)>0]
        oaprice[i] = int(sum(oprice) * 1.0 / len(oprice))
        caprice[i] = int(sum(cprice) * 1.0 / len(cprice))
        #print oaprice[i],caprice[i]
    return oaprice,caprice


def long_time_stoper(sif,sopened,mytime=1454):
    sl = np.select([sif.time==mytime],[1],0)
    return  sl * XSELL

def short_time_stoper(sif,sopened,mytime=1454):
    sl = np.select([sif.time==mytime],[1],0)
    return  sl * XBUY


def long_moving_stoper( #多头移动平仓
        sif,
        sopened,
        flost_base = iftrade.F70,    #flost:买入点数 --> 止损点数
        fmax_drawdown = iftrade.F250, #最大回落比例
        pmax_drawdown = 0.012, #最大回落比例
        tstep = lambda sif,i:40,     #行情顺向滑动单位
        vstep = 20,                  #止损顺向移动单位   
        ):
    '''
    '''
    trans = sif.transaction
    rev = np.zeros_like(sopened)
    isignal = np.nonzero(sopened)[0]
    iclosed = 0    #多头平仓日
    will_losts = []
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)        
    for i in isignal:
        price = sopened[i]
        aprice = abs(price)
        #willlost = flost_base(aprice)
        willlost = flost_base(ldopen[i])    #开盘价的定数
        #willlost = sif.atr15x[i]/XBASE    #效果不佳
        spmax_drawdown = pmax_drawdown * aprice
        sfmax_drawdown = fmax_drawdown(aprice)
        max_drawdown = spmax_drawdown if spmax_drawdown < sfmax_drawdown else sfmax_drawdown
        will_losts.append(willlost)
        mytstep = tstep(sif,i)
        #print u'多头止损'
        if i <= iclosed:
            #print 'long skipped'
            continue
        buy_price = -price
        lost_stop = buy_price - willlost
        cur_high = max(buy_price,sif.close[i])
        win_stop = lost_stop + (cur_high - buy_price)/mytstep * vstep
        #cur_stop = lost_stop if lost_stop > win_stop else win_stop
        cur_stop = win_stop #win_stop必然大于lost_stop
        #print 'wtarget:%s',wtarget
        #print 'stop init:',buy_price,cur_stop,trans[IDATE][i],trans[ITIME][i]
        if trans[ICLOSE][i] < cur_stop:#到达止损
            print '----sell----------:',trans[IDATE][i],trans[ITIME][i],cur_stop,trans[ICLOSE][i],cur_high,lost_stop
            iclosed = i
            rev[i] = cur_stop * XSELL   #设定价格   #两次乘XSELL，把符号整回来
        else:
            #if trans[IDATE][i] == 20110214:
            #print 'begin:',trans[IDATE][i],trans[ITIME][i],buy_price,lost_stop,cur_high,win_stop,cur_stop,trans[ILOW][i]
            for j in range(i+1,len(rev)):
                if trans[IORDER][j] >= 269: #换日
                    iclosed = j
                    break
                if trans[ILOW][j] < cur_stop:
                    iclosed = j
                    rev[j] = (cur_stop if cur_stop < trans[IOPEN][j] else trans[IOPEN][j])* XSELL 
                    break
                nhigh = trans[IHIGH][j]
                if(nhigh > cur_high):
                    cur_high = nhigh
                    win_stop = lost_stop + (cur_high - buy_price)/mytstep * vstep
                    mstop = cur_high - max_drawdown
                    cur_stop = win_stop if win_stop > mstop else mstop
                    
    return rev

def short_moving_stoper(
        sif,
        sopened,
        flost_base = iftrade.F70,    #flost:买入点数 --> 止损点数
        fmax_drawdown = iftrade.F250, #最大回落比例
        pmax_drawdown = 0.012, #最大回落比例
        tstep = lambda sif,i:40,     #行情顺向滑动单位
        vstep = 20,                  #止损顺向移动单位   
        ):
    '''
    '''
    trans = sif.transaction
    rev = np.zeros_like(sopened)
    isignal = np.nonzero(sopened)[0]
    iclosed = 0   #空头平仓日
    will_losts = []
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)        
    
    for i in isignal:
        price = sopened[i]
        aprice = abs(price)
        #willlost = flost_base(aprice)
        willlost = flost_base(ldopen[i])    #开盘价的定数
        #willlost = sif.atr15x[i]/XBASE    #效果不佳
        spmax_drawdown = pmax_drawdown * aprice
        sfmax_drawdown = fmax_drawdown(aprice)
        max_drawdown = spmax_drawdown if spmax_drawdown < sfmax_drawdown else sfmax_drawdown
        will_losts.append(willlost)
        mytstep = tstep(sif,i)
        myvstep = vstep
        #mytstep = ldopen[i] / 750
        #myvstep = ldopen[i] / 1500

        #print 'find short stop:',i
        if i<=iclosed:
            #print 'short skipped'
            continue
        sell_price = price
        lost_stop = sell_price + willlost
        cur_low = min(sell_price,trans[ICLOSE][i])
        win_stop = lost_stop - (sell_price - cur_low)/mytstep * myvstep 
        cur_stop = win_stop
        #print trans[IDATE][i],trans[ITIME][i],cur_low,cur_stop
        if trans[ICLOSE][i] > cur_stop:
            #print '----buy----------:',cur_stop,trans[ICLOSE][i],cur_high,lost_stop
            iclosed = i
            rev[i] = cur_stop * XBUY    #两次乘XBUY，把符号整回来
        else:
            for j in range(i+1,len(rev)):
                if trans[IORDER][j] >= 269: #换日
                    iclosed = j
                    break
                if trans[IHIGH][j] > cur_stop:
                    iclosed = j
                    #rev[j] = cur_stop * XBUY
                    rev[j] = (cur_stop if cur_stop > trans[IOPEN][j] else trans[IOPEN][j])* XBUY
                    #print 'buy:',j
                    #print 'buy:',i,price,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j]                        
                    break
                nlow = trans[ILOW][j]
                if(nlow < cur_low):
                    cur_low = nlow
                    win_stop = lost_stop - (sell_price - cur_low)/mytstep * myvstep 
                    mstop = cur_low + max_drawdown
                    cur_stop = win_stop if win_stop < mstop else mstop
                        
    return rev

def calc_points(tstep,vstep,mstep):
    tlist = range(tstep,mstep,-10)
    tlist.extend([mstep]*300)
    stlist = []
    s=0
    for t in tlist:
        stlist.append(s)
        s += t
    prop = vstep * 1.0 / tstep
    svlist = [ int(v*prop+0.5) for v in stlist]
    return stlist,svlist

def calc_points2(tstep,vstep,mstep):
    tlist = [tstep]*300
    stlist = []
    s=0
    for t in tlist:
        stlist.append(s)
        s += t
    prop = vstep * 1.0 / tstep
    svlist = [ int(v*prop+0.5) for v in stlist]
    return stlist,svlist


def find_inext(st,icur,v):
    for i in range(icur,len(st)):
        if st[i] > v:
            break
    return i-1

def long_moving_stoper3( #多头移动平仓
        sif,
        sopened,
        flost_base = iftrade.F70,    #flost:买入点数 --> 止损点数
        fmax_drawdown = iftrade.F250, #最大回落比例
        pmax_drawdown = 0.012, #最大回落比例
        tstep = 80,     #行情顺向滑动单位--初始
        vstep = 40,                  #止损顺向移动单位--初始   
        mstep = 16,                  #最小移动单位
        ):
    '''
    '''
    trans = sif.transaction
    rev = np.zeros_like(sopened)
    isignal = np.nonzero(sopened)[0]
    iclosed = 0    #多头平仓日
    will_losts = []
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)        
    
    st,sv = calc_points(tstep,vstep,mstep)
    
    for i in isignal:
        price = sopened[i]
        aprice = abs(price)
        #willlost = flost_base(aprice)
        willlost = flost_base(ldopen[i])    #开盘价的定数
        #willlost = sif.atr15x[i]/XBASE    #效果不佳
        spmax_drawdown = pmax_drawdown * aprice
        sfmax_drawdown = fmax_drawdown(aprice)
        max_drawdown = spmax_drawdown if spmax_drawdown < sfmax_drawdown else sfmax_drawdown
        will_losts.append(willlost)
        #mytstep = tstep(sif,i)
        #print u'多头止损'
        if i <= iclosed:
            #print 'long skipped'
            continue
        icur = 0
        buy_price = -price
        lost_stop = buy_price - willlost
        cur_high = max(buy_price,sif.close[i])
        icur = find_inext(st,icur,cur_high - buy_price)
        win_stop = lost_stop + sv[icur]
        #win_stop = lost_stop + (cur_high - buy_price)/mytstep * vstep
        #cur_stop = lost_stop if lost_stop > win_stop else win_stop
        cur_stop = win_stop #win_stop必然大于lost_stop
        #print 'wtarget:%s',wtarget
        #print 'stop init:',buy_price,cur_stop,trans[IDATE][i],trans[ITIME][i]
        if trans[ICLOSE][i] < cur_stop:#到达止损
            print '----sell----------:',trans[IDATE][i],trans[ITIME][i],cur_stop,trans[ICLOSE][i],cur_high,lost_stop
            iclosed = i
            rev[i] = cur_stop * XSELL   #设定价格   #两次乘XSELL，把符号整回来
        else:
            #if trans[IDATE][i] == 20110214:
            #print 'begin:',trans[IDATE][i],trans[ITIME][i],buy_price,lost_stop,cur_high,win_stop,cur_stop,trans[ILOW][i]
            for j in range(i+1,len(rev)):
                if trans[IORDER][j] >= 269: #换日
                    iclosed = j
                    break
                if trans[ILOW][j] < cur_stop:
                    iclosed = j
                    rev[j] = (cur_stop if cur_stop < trans[IOPEN][j] else trans[IOPEN][j])* XSELL 
                    break
                nhigh = trans[IHIGH][j]
                if(nhigh > cur_high):
                    cur_high = nhigh
                    icur = find_inext(st,icur,cur_high - buy_price)
                    win_stop = lost_stop + sv[icur]
                    #win_stop = lost_stop + (cur_high - buy_price)/mytstep * vstep
                    mstop = cur_high - max_drawdown
                    cur_stop = win_stop if win_stop > mstop else mstop
                    
    return rev

def short_moving_stoper4(
        sif,
        sopened,
        flost_base = iftrade.F70,    #flost:买入点数 --> 止损点数
        fzero_base = iftrade.F70,    #平推位
        fmax_drawdown = iftrade.F250, #最大回落比例
        pmax_drawdown = 0.012, #最大回落比例
        tstep = lambda sif,i:40,     #行情顺向滑动单位
        vstep = 20,                  #止损顺向移动单位   
        ):
    '''
    '''
    trans = sif.transaction
    rev = np.zeros_like(sopened)
    isignal = np.nonzero(sopened)[0]
    iclosed = 0   #空头平仓日
    will_losts = []
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)        
    
    for i in isignal:
        price = sopened[i]
        aprice = abs(price)
        #willlost = flost_base(aprice)
        willlost = flost_base(ldopen[i])    #开盘价的定数
        zero_base = fzero_base(ldopen[i])
        #willlost = sif.atr15x[i]/XBASE    #效果不佳
        spmax_drawdown = pmax_drawdown * aprice
        sfmax_drawdown = fmax_drawdown(aprice)
        max_drawdown = spmax_drawdown if spmax_drawdown < sfmax_drawdown else sfmax_drawdown
        will_losts.append(willlost)
        mytstep = tstep(sif,i)
        myvstep = vstep
        #mytstep = ldopen[i] / 750
        #myvstep = ldopen[i] / 1500

        #print 'find short stop:',i
        if i<=iclosed:
            #print 'short skipped'
            continue
        sell_price = price
        zero_price = price - zero_base
        lost_stop = sell_price + willlost
        cur_low = min(sell_price,trans[ICLOSE][i])
        if cur_low < zero_price:
            win_stop = lost_stop - (sell_price - cur_low)/mytstep * myvstep 
            cur_stop = win_stop if win_stop > sell_price else win_stop
        else:
            cur_stop = lost_stop
        #print trans[IDATE][i],trans[ITIME][i],cur_low,cur_stop
        if trans[ICLOSE][i] > cur_stop:
            #print '----buy----------:',cur_stop,trans[ICLOSE][i],cur_high,lost_stop
            iclosed = i
            rev[i] = cur_stop * XBUY    #两次乘XBUY，把符号整回来
        else:
            for j in range(i+1,len(rev)):
                if trans[IORDER][j] >= 269: #换日
                    iclosed = j
                    break
                if trans[IHIGH][j] > cur_stop:
                    iclosed = j
                    #rev[j] = cur_stop * XBUY
                    rev[j] = (cur_stop if cur_stop > trans[IOPEN][j] else trans[IOPEN][j])* XBUY
                    #print 'buy:',j
                    #print 'buy:',i,price,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j]                        
                    break
                nlow = trans[ILOW][j]
                if(nlow < cur_low):
                    if nlow < zero_price:
                        cur_low = nlow
                        win_stop = lost_stop - (sell_price - cur_low)/mytstep * myvstep 
                        mstop = cur_low + max_drawdown
                        cur_stop = win_stop if win_stop < mstop else mstop
                        if cur_stop > sell_price:
                            cur_stop = sell_price
                    else:#不改变止损
                        pass    
    return rev

def short_moving_stoper3(
        sif,
        sopened,
        flost_base = iftrade.F70,    #flost:买入点数 --> 止损点数
        fmax_drawdown = iftrade.F250, #最大回落比例
        pmax_drawdown = 0.012, #最大回落比例
        tstep = 40,     #行情顺向滑动单位--初始
        vstep = 20,                  #止损顺向移动单位--初始   
        mstep = 8,                  #最小移动单位
        ):
    '''
    '''
    trans = sif.transaction
    rev = np.zeros_like(sopened)
    isignal = np.nonzero(sopened)[0]
    iclosed = 0   #空头平仓日
    will_losts = []
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)        
    
    #st,sv = calc_points2(tstep,vstep,mstep)
    st,sv = calc_points(tstep,vstep,mstep)

    for i in isignal:
        price = sopened[i]
        aprice = abs(price)
        #willlost = flost_base(aprice)
        willlost = flost_base(ldopen[i])    #开盘价的定数
        #willlost = sif.atr15x[i]/XBASE    #效果不佳
        spmax_drawdown = pmax_drawdown * aprice
        sfmax_drawdown = fmax_drawdown(aprice)
        max_drawdown = spmax_drawdown if spmax_drawdown < sfmax_drawdown else sfmax_drawdown
        will_losts.append(willlost)

        #print 'find short stop:',i
        if i<=iclosed:
            #print 'short skipped'
            continue
        icur = 0
        sell_price = price
        lost_stop = sell_price + willlost
        cur_low = min(sell_price,trans[ICLOSE][i])
        icur = find_inext(st,icur,sell_price - cur_low)
        win_stop = lost_stop - sv[icur]
        #win_stop = lost_stop - (sell_price - cur_low)/cur_tstep * cur_vstep 
        cur_stop = win_stop
        #print trans[IDATE][i],trans[ITIME][i],cur_low,cur_stop
        if trans[ICLOSE][i] > cur_stop:
            #print '----buy----------:',cur_stop,trans[ICLOSE][i],cur_high,lost_stop
            iclosed = i
            rev[i] = cur_stop * XBUY    #两次乘XBUY，把符号整回来
        else:
            for j in range(i+1,len(rev)):
                if trans[IORDER][j] >= 269: #换日
                    iclosed = j
                    break
                if trans[IHIGH][j] > cur_stop:
                    iclosed = j
                    #rev[j] = cur_stop * XBUY
                    rev[j] = (cur_stop if cur_stop > trans[IOPEN][j] else trans[IOPEN][j])* XBUY
                    #print 'buy:',j
                    #print 'buy:',i,price,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j]                        
                    break
                nlow = trans[ILOW][j]
                if(nlow < cur_low):
                    #if cur_tstep > mstep:
                    #    cur_tstep -= 10
                    #    cur_vstep = cur_tstep * prop
                    cur_low = nlow
                    #win_stop = lost_stop - (sell_price - cur_low)/cur_tstep * cur_vstep #+ ldopen[i]/3000
                    icur = find_inext(st,icur,sell_price - cur_low)
                    win_stop = lost_stop - sv[icur]
                    mstop = cur_low + max_drawdown
                    cur_stop = win_stop if win_stop < mstop else mstop
                        
    return rev

def long_moving_stoper2( #多头移动平仓,一步调整到开仓位
        sif,
        sopened,
        flost_base = iftrade.F70,    #flost:买入点数 --> 止损点数
        fmax_drawdown = iftrade.F250, #最大回落比例
        pmax_drawdown = 0.012, #最大回落比例
        tstep = lambda sif,i:40,     #行情顺向滑动单位
        vstep = 20,                  #止损顺向移动单位   
        fkeeper = iftrade.F120,
        ):
    '''
    '''
    trans = sif.transaction
    rev = np.zeros_like(sopened)
    isignal = np.nonzero(sopened)[0]
    iclosed = 0    #多头平仓日
    will_losts = []
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)        
    for i in isignal:
        price = sopened[i]
        aprice = abs(price)
        #willlost = flost_base(aprice)
        willlost = flost_base(ldopen[i])    #开盘价的定数
        #willlost = sif.atr15x[i]/XBASE    #效果不佳
        mykeeper = fkeeper(ldopen[i])
        pkeeper = aprice + mykeeper     #拉平位置
        spmax_drawdown = pmax_drawdown * aprice
        sfmax_drawdown = fmax_drawdown(aprice)
        max_drawdown = spmax_drawdown if spmax_drawdown < sfmax_drawdown else sfmax_drawdown
        will_losts.append(willlost)
        mytstep = tstep(sif,i)
        #print u'多头止损'
        if i <= iclosed:
            #print 'long skipped'
            continue
        buy_price = -price
        lost_stop = buy_price - willlost
        cur_high = max(buy_price,sif.close[i])
        win_stop = lost_stop + (cur_high - buy_price)/mytstep * vstep
        #cur_stop = lost_stop if lost_stop > win_stop else win_stop
        cur_stop = win_stop #win_stop必然大于lost_stop
        #print 'wtarget:%s',wtarget
        #print 'stop init:',buy_price,cur_stop,trans[IDATE][i],trans[ITIME][i]
        if trans[ICLOSE][i] < cur_stop:#到达止损
            print '----sell----------:',trans[IDATE][i],trans[ITIME][i],cur_stop,trans[ICLOSE][i],cur_high,lost_stop
            iclosed = i
            rev[i] = cur_stop * XSELL   #设定价格   #两次乘XSELL，把符号整回来
        else:
            #if trans[IDATE][i] == 20110214:
            #print 'begin:',trans[IDATE][i],trans[ITIME][i],buy_price,lost_stop,cur_high,win_stop,cur_stop,trans[ILOW][i]
            for j in range(i+1,len(rev)):
                if trans[IORDER][j] >= 269: #换日
                    iclosed = j
                    break
                if trans[ILOW][j] < cur_stop:
                    iclosed = j
                    rev[j] = (cur_stop if cur_stop < trans[IOPEN][j] else trans[IOPEN][j])* XSELL 
                    break
                nhigh = trans[IHIGH][j]
                if(nhigh > cur_high):
                    cur_high = nhigh
                    if nhigh > pkeeper:
                        win_stop = lost_stop + (cur_high - buy_price)/mytstep * vstep
                        if aprice > win_stop:
                            win_stop = aprice
                    else:
                        win_stop = 0    #不能拉平
                    mstop = cur_high - max_drawdown
                    #cur_stop = win_stop if win_stop > mstop else mstop
                    w_stop = win_stop if win_stop > mstop else mstop
                    if w_stop > cur_stop:
                        cur_stop = w_stop
    return rev

def short_moving_stoper2(
        sif,
        sopened,
        flost_base = iftrade.F70,    #flost:买入点数 --> 止损点数
        fmax_drawdown = iftrade.F250, #最大回落比例
        pmax_drawdown = 0.012, #最大回落比例
        tstep = lambda sif,i:40,     #行情顺向滑动单位
        vstep = 20,                  #止损顺向移动单位   
        fkeeper = iftrade.F120,
        ):
    '''
    '''
    trans = sif.transaction
    rev = np.zeros_like(sopened)
    isignal = np.nonzero(sopened)[0]
    iclosed = 0   #空头平仓日
    will_losts = []
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)        
    
    for i in isignal:
        price = sopened[i]
        aprice = abs(price)
        #willlost = flost_base(aprice)
        willlost = flost_base(ldopen[i])    #开盘价的定数
        #willlost = sif.atr15x[i]/XBASE    #效果不佳
        mykeeper = fkeeper(ldopen[i])
        pkeeper = aprice - mykeeper     #拉平位置
        spmax_drawdown = pmax_drawdown * aprice
        sfmax_drawdown = fmax_drawdown(aprice)
        max_drawdown = spmax_drawdown if spmax_drawdown < sfmax_drawdown else sfmax_drawdown
        will_losts.append(willlost)
        mytstep = tstep(sif,i)

        #print 'find short stop:',i
        if i<=iclosed:
            #print 'short skipped'
            continue
        sell_price = price
        lost_stop = sell_price + willlost
        cur_low = min(sell_price,trans[ICLOSE][i])
        win_stop = lost_stop - (sell_price - cur_low)/mytstep * vstep 
        cur_stop = win_stop
        #print trans[IDATE][i],trans[ITIME][i],cur_low,cur_stop
        if trans[ICLOSE][i] > cur_stop:
            #print '----buy----------:',cur_stop,trans[ICLOSE][i],cur_high,lost_stop
            iclosed = i
            rev[i] = cur_stop * XBUY    #两次乘XBUY，把符号整回来
        else:
            for j in range(i+1,len(rev)):
                if trans[IORDER][j] >= 269: #换日
                    iclosed = j
                    break
                if trans[IHIGH][j] > cur_stop:
                    iclosed = j
                    #rev[j] = cur_stop * XBUY
                    rev[j] = (cur_stop if cur_stop > trans[IOPEN][j] else trans[IOPEN][j])* XBUY
                    #print 'buy:',j
                    #print 'buy:',i,price,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j]                        
                    break
                nlow = trans[ILOW][j]
                if(nlow < cur_low):
                    cur_low = nlow
                    if nlow < pkeeper:
                        win_stop = lost_stop - (sell_price - cur_low)/mytstep * vstep 
                        if aprice < win_stop:
                            win_stop = aprice
                    else:
                        win_stop = 99999999    #不能拉平
                    mstop = cur_low + max_drawdown
                    w_stop = win_stop if win_stop < mstop else mstop
                    if w_stop < cur_stop:
                        cur_stop = w_stop
                        
    return rev


def long_keep_stoper(
        ##这个是不妥的，单独有状态的stoper不能叠加. 因为连续的信号出来之后，前面一个如果一直没有平仓，则后面的被遮蔽了
        sif,
        sopened,
        keep = 250,    #cur_high的1/keep
        ):
    '''
    '''
    #print sbclose[-10:],ssclose[-10:]
    trans = sif.transaction
    rev = np.zeros_like(sopened)
    isignal = np.nonzero(sopened)[0]
    iclosed = 0    #多头平仓日
    for i in isignal:
        price = sopened[i]
        aprice = abs(price)
        if i <= iclosed:
            #print 'long skipped'
            continue
        buy_price = -price
        cur_high = max(buy_price,sif.close[i])
        cur_stop = 0
        #print 'wtarget:%s',wtarget
        #print 'stop init:',cur_stop,lost_stop,willlost,min_lost,max_lost
        if trans[ICLOSE][i] < cur_stop:#到达止损
            #print '----sell----------:',trans[IDATE][i],trans[ITIME][i],cur_stop,trans[ICLOSE][i],cur_high,lost_stop
            iclosed = i
            rev[i] = cur_stop * XSELL   #设定价格
        else:
            for j in range(i+1,len(rev)):
                if trans[ILOW][j] < cur_stop:
                    iclosed = j
                    rev[j] = (cur_stop if cur_stop < trans[IOPEN][j] else trans[IOPEN][j])* XSELL 
                    break
                if trans[IORDER][j] >265:
                    iclosed = j
                    rev[j] = trans[IOPEN][j]
                    break
                nhigh = trans[IHIGH][j]
                if(nhigh > cur_high):
                    cur_high = nhigh
                    cur_stop = buy_price if cur_high - buy_price > cur_high/keep else 0
    #print will_losts
    #print rev[np.nonzero(rev)]
    return rev

def short_keep_stoper(
        ##这个是不妥的，单独有状态的stoper不能叠加. 因为连续的信号出来之后，前面一个如果一直没有平仓，则后面的被遮蔽了
        sif,
        sopened,
        keep = 150,    #cur_low的1/keep
        ):
    '''
    '''
    #print sbclose[-10:],ssclose[-10:]
    trans = sif.transaction
    rev = np.zeros_like(sopened)
    isignal = np.nonzero(sopened)[0]
    iclosed = 0   #空头平仓日
    for i in isignal:
        price = sopened[i]
        aprice = abs(price)
        #print 'find short stop:',i
        if i<=iclosed:
            #print 'short skipped'
            continue
        sell_price = price
        cur_stop = 99999999
        cur_low = min(sell_price,trans[ICLOSE][i])
        if trans[ICLOSE][i] > cur_stop:
            #print '----buy----------:',cur_stop,trans[ICLOSE][i],cur_high,lost_stop
            iclosed = i
            rev[i] = cur_stop * XBUY
        else:
            for j in range(i+1,len(rev)):
                if trans[IHIGH][j] > cur_stop:
                    iclosed = j
                    rev[j] = (cur_stop if cur_stop > trans[IOPEN][j] else trans[IOPEN][j])* XBUY
                    break
                if trans[IORDER][j] ==270:
                    iclosed = j
                    rev[j] = trans[IOPEN][j]
                    break
                nlow = trans[ILOW][j]
                if(nlow < cur_low):
                    cur_low = nlow
                    cur_stop = sell_price if sell_price - cur_low > cur_low/keep else 99999999
    return rev

def long_atr_keep_stoper(
        sif,
        sopened,
        akeep = 3.5,    #cur_high的1/keep
        ):
    '''
    '''
    trans = sif.transaction
    rev = np.zeros_like(sopened)
    isignal = np.nonzero(sopened)[0]
    iclosed = 0    #多头平仓日
    for i in isignal:
        price = sopened[i]
        aprice = abs(price)
        vkeep = sif.atr[i] * akeep / XBASE
        if i <= iclosed:
            #print 'long skipped'
            continue
        buy_price = -price
        cur_high = max(buy_price,sif.close[i])
        cur_stop = 0
        #print 'wtarget:%s',wtarget
        #print 'stop init:',cur_stop,lost_stop,willlost,min_lost,max_lost
        if trans[ICLOSE][i] < cur_stop:#到达止损
            #print '----sell----------:',trans[IDATE][i],trans[ITIME][i],cur_stop,trans[ICLOSE][i],cur_high,lost_stop
            iclosed = i
            rev[i] = cur_stop * XSELL   #设定价格
        else:
            for j in range(i+1,len(rev)):
                if trans[ILOW][j] < cur_stop:
                    iclosed = j
                    rev[j] = (cur_stop if cur_stop < trans[IOPEN][j] else trans[IOPEN][j])* XSELL 
                    break
                if trans[IORDER][j] >265:
                    iclosed = j
                    break
                nhigh = trans[IHIGH][j]
                if(nhigh > cur_high):
                    cur_high = nhigh
                    cur_stop = buy_price if cur_high - buy_price > vkeep else 0
    #print will_losts
    #print rev[np.nonzero(rev)]
    return rev

def short_atr_keep_stoper(
        ##这个是不妥的，单独有状态的stoper不能叠加. 因为连续的信号出来之后，前面一个如果一直没有平仓，则后面的被遮蔽了
        sif,
        sopened,
        akeep = 20,    #cur_low的1/keep
        ):
    '''
    '''
    #print sbclose[-10:],ssclose[-10:]
    trans = sif.transaction
    rev = np.zeros_like(sopened)
    isignal = np.nonzero(sopened)[0]
    iclosed = 0   #空头平仓日
    for i in isignal:
        price = sopened[i]
        aprice = abs(price)
        #print 'find short stop:',i
        if i<=iclosed:
            #print 'short skipped'
            continue
        sell_price = price
        cur_stop = 99999999
        cur_low = min(sell_price,trans[ICLOSE][i])
        vkeep = sif.atr[i] * akeep / XBASE
        if trans[ICLOSE][i] > cur_stop:
            #print '----buy----------:',cur_stop,trans[ICLOSE][i],cur_high,lost_stop
            iclosed = i
            rev[i] = cur_stop * XBUY
        else:
            for j in range(i+1,len(rev)):
                if trans[IHIGH][j] > cur_stop:
                    iclosed = j
                    rev[j] = (cur_stop if cur_stop > trans[IOPEN][j] else trans[IOPEN][j])* XBUY
                    break
                if trans[IORDER][j] ==270:
                    iclosed = j
                    break
                nlow = trans[ILOW][j]
                if(nlow < cur_low):
                    cur_low = nlow
                    cur_stop = sell_price if sell_price - cur_low > vkeep else 99999999
    return rev


def long_rapid_stoper(
        sif,
        sopened,
        ltime=1,    #新高后ltime分钟内
        ldown=4,    #回落ldown个atr (3,4)
        ):
    '''
        新高后ltime分钟回落ldown个atr即平仓
    '''
    trans = sif.transaction
    #ldopen = dnext(sif.opend,sif.close,sif.i_oofd)        
    
    #rev = np.zeros_like(sopened)
    lhigh = rollx(tmax(sif.high,ltime))
    bline = lhigh - rollx(sif.atr/XBASE,ltime) * ldown
    signal = gand(cross(bline,sif.low) < 0,
                  lhigh == rollx(sif.dhigh),  
                )
    return np.select([signal],[gmin(sif.open,bline)],0)

def short_rapid_stoper(
        sif,
        sopened,
        ltime=3,    #新高后ltime分钟内
        lup=6,    #上升lup个atr
        ):
    '''
        新低后ltime分钟回升lup个atr即平仓
    '''
    trans = sif.transaction
    #ldopen = dnext(sif.opend,sif.close,sif.i_oofd)        
    
    #rev = np.zeros_like(sopened)
    llow = rollx(tmin(sif.low,ltime))
    bline = llow + rollx(sif.atr/XBASE) * lup
    signal = gand(cross(bline,sif.high) > 0,
                  llow == rollx(sif.dlow),  
                )
    return np.select([signal],[gmax(sif.open,bline)],0)

def long_low_stoper(
        sif,
        sopened,
        lshort = 13,
        llong = 30,    
        ):
    '''
        新低后ltime分钟回升lup个atr即平仓
    '''
    tlow2 = rollx(tmin(sif.low,20),1)
    bline = rollx(tmin(sif.low,lshort))
    signal = gand(cross(bline,sif.low)<0,
                )
    return np.select([signal],[gmin(sif.open,bline)],0)

def short_high_stoper(
        sif,
        sopened,
        hshort = 13,
        hlong = 30,    
        ):
    '''
        新低后ltime分钟回升lup个atr即平仓
    '''
    bline = rollx(tmax(sif.high,hshort))
    signal = gand(cross(bline,sif.high)>0,
                )
    return np.select([signal],[gmax(sif.open,bline)],0)

def long_peak_stoper(
        sif,
        sopened,
        xdiff = 30,    
        ):
    '''
        日内新高前xdiff平多仓
    '''
    bline = rollx(sif.dhigh-xdiff,10)
    signal = gand(sif.high > bline,sif.high,
                  rollx(sif.dhigh-sif.dlow,10) > 150,   #如果振幅太小，则不动
                )
    return np.select([signal],[gmin(sif.open,bline)],0)

def short_peak_stoper(
        sif,
        sopened,
        xdiff = 30,
        ):
    '''
        日内新低前xdiff平空仓
    '''
    bline = rollx(sif.dlow+xdiff) 
    signal = gand(cross(bline,sif.low)<0,
                )
    return np.select([signal],[gmax(sif.open,bline)],0)

def utrade2x(sif     #
            ,openers    #opener函数集合
            ,bclosers   #默认的多平仓函数集合(空头平仓)
            ,sclosers   #默认的空平仓函数集合(多头平仓)
            ,make_trades=iftrade.simple_trades  #根据开平仓动作撮合交易的函数。对于最后交易序列，用last_trades
            ,sync_trades=sync_tradess_u    #汇总各opener得到的交易，计算优先级和平仓。
                                            #对于最后交易序列，用null_sync_tradess
            ,acstrategy=iftrade.late_strategy   #增强开仓时的平仓策略。late_strategy是平最晚的那个信号
        ):
    '''
        本函数针对每个opener计算出各自的闭合交易
        要求每个方法的属性有：
                direction:  多/空方向 XBUY/XSELL
                stop_closer 止损方法(单个或多个), 如果存在，就加入到closer中去
                name:       名字

    '''
    if not isinstance(openers,list):   #单个函数
        openers = [openers]
    if not isinstance(bclosers,list):   #单个函数
        bclosers = [bclosers]
    if not isinstance(sclosers,list):   #单个函数
        sclosers = [sclosers]
    
    tradess = []
    for opener in openers:
        opens = uopen_position(sif,opener(sif))
        odir = iftrade.fdirection(opener)
        sopened = np.zeros(len(sif.date),int)   #为开仓价格序列,负数为开多仓,正数为开空仓
        for aopen in opens:
            sopened[aopen.index] = aopen.price * aopen.position
        if 'closer' in opener.__dict__: #是否有特定的closer,如要将macd下叉也作为多头持仓的平仓条件,则可设置函数,在返回值中添加该下叉信号算法
            if odir == XBUY:
                #print 'buy closer:',opener.closer
                closers = opener.closer(sclosers)[:]    #复制
            elif odir == XSELL:
                closers = opener.closer(bclosers)[:]
        else:
            #print 'opener without close iftrade.fdirection(opener) = %s' % ('XBUY' if iftrade.fdirection(opener) == XBUY else 'XSELL',)
            closers = sclosers[:] if odir == XBUY else bclosers[:]

        if 'stop_closer' in opener.__dict__:
            if isinstance(opener.stop_closer,list) or isinstance(opener.stop_closer,tuple):
                closers.extend(opener.stop_closer)
            else:
                closers.append(opener.stop_closer)


        #这里需要u处理
        ''' 1. 0为无信号
            2. 1或-1为 下一分钟平仓信号
            3. 其它数值为当分钟平仓信号
               当分钟平仓的，以价格最高的为准。因为必然该信号最早发出
            4. 当分钟平仓信号优先于下一分钟平仓信号
        '''
        psclose = np.zeros_like(sif.date) #np.select([sclose],[np.abs(sclose)],PS_MAX)    #把0转换为最大值
        for closer in closers:#这里默认认为closer返回的数据中只要非0就算是有信号, 而不是区分买平还是卖平
            #print func_name(closer)
            cur_s = np.abs(closer(sif,sopened))
            psclose = gmax(psclose,cur_s)       #实际平仓价 > 平仓信号 > 0
        sclose = psclose * (-odir)

        closes = uclose_position(sif,sclose) #因为是单向的，只有一个sclose起作用        

        actions = sorted(opens + closes,iftrade.DTSORT2) #必须确保先开后平, 但如果已经开了，则只有平仓
        #print len(opens+closes),len(actions)
        for action in actions:
            action.name = sif.name
            #print action.name,action.date,action.time,action.position,action.price
        trades = make_trades(actions)   #trade: [open , close] 的序列, 其中前部分都是open,后部分都是close
        for trade in trades:
            trade.functor = opener
            trade.direction = trade.actions[0].position   #LONG/SHORT
            #print trade.actions[0].date,trade.actions[0].time,trade.direction
        tradess.append(trades)
    return sync_trades(sif,tradess,acstrategy)

#########
# 震荡平仓
#########
lw_4_21 = fcustom(long_moving_stoper,
                flost_base = iftrade.F40, 
                fmax_drawdown = iftrade.F60, 
                pmax_drawdown = 0.003, 
                tstep = lambda sif,i:20,     
                vstep = 10,                  
            )

sw_4_21 = fcustom(short_moving_stoper,
                flost_base = iftrade.F40, 
                fmax_drawdown = iftrade.F60, 
                pmax_drawdown = 0.003, 
                tstep = lambda sif,i:20,     
                vstep = 10,                  
            )

lp_3 = fcustom(long_peak_stoper,
               xdiff = 30
            )

sp_3 = fcustom(short_peak_stoper,
               xdiff = 30
            )


########
# 趋势平仓
########

lm_stoper_10_42_old = fcustom(long_moving_stoper,
                flost_base = iftrade.F100, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                tstep = lambda sif,i:40,     
                vstep = 20,                  
            )

lm_stoper_18_43 = fcustom(long_moving_stoper,
                flost_base = lambda p:p/133, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                tstep = lambda sif,i:40,     
                vstep = 30,                  
            )


lm_stoper_10_42 = fcustom(long_moving_stoper,
                flost_base = lambda p:p/250, 
                fmax_drawdown = iftrade.F360, 
                #fmax_drawdown = lambda x:900, 
                pmax_drawdown = 0.011, 
                #pmax_drawdown = 0.1, #即不起作用
                tstep = lambda sif,i:80,     
                vstep = 40,                  
            )

lm_stoper_10_42b = fcustom(long_moving_stoper2,
                flost_base = lambda p:p/300, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                tstep = lambda sif,i:40,     
                vstep = 20,                  
                fkeeper = lambda p:p/160,
            )

lm_stoper_10_21 = fcustom(long_moving_stoper,
                flost_base = lambda p:p/250, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                tstep = lambda sif,i:20,     
                vstep = 10,                  
            )

lm_stoper_10_21b = fcustom(long_moving_stoper,
                flost_base = lambda p:p/250, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.015, 
                tstep = lambda sif,i:20,     
                vstep = 10,                  
            )


lm_stoper_8_21 = fcustom(long_moving_stoper,
                flost_base = lambda p:p/300, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                tstep = lambda sif,i:20,     
                vstep = 10,                  
            )

lm_stoper_8_42 = fcustom(long_moving_stoper,
                flost_base = lambda p:p/300, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                tstep = lambda sif,i:40,     
                vstep = 20,                  
            )


lm_stoper_6_21 = fcustom(long_moving_stoper,
                flost_base = lambda p:p/400, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                tstep = lambda sif,i:20,     
                vstep = 12,                  
            )

lm_stoper_5_21 = fcustom(long_moving_stoper,
                flost_base = lambda p:p/666, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                tstep = lambda sif,i:20,     
                vstep = 10,                  
            )

sm_stoper_10_42_old = fcustom(short_moving_stoper,
                flost_base = iftrade.F100, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                tstep = lambda sif,i:40,     
                vstep = 20,                  
            )

sm_stoper_18_42 = fcustom(short_moving_stoper,
                flost_base = lambda p:p/180, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                tstep = lambda sif,i:40,     
                vstep = 30,                  
            )

sm_stoper_10_42b = fcustom(short_moving_stoper2,
                flost_base = lambda p:p/250, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                tstep = lambda sif,i:40,     
                vstep = 20,                  
                fkeeper = lambda p:p/125,
            )

sm_stoper_10_42d = fcustom(short_moving_stoper4,
                flost_base = lambda p:p/333, 
                fzero_base = lambda p:p/300, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                tstep = lambda sif,i:160,     
                vstep = 80,                  
            )

sm_stoper_10_42 = fcustom(short_moving_stoper,
                flost_base = lambda p:p/250, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                tstep = lambda sif,i:40,     
                vstep = 20,                  
            )

sm_stoper_10_42_2 = fcustom(short_moving_stoper,
                flost_base = lambda p:p/300, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                tstep = lambda sif,i:60,     
                vstep = 30,                  
            )


sm_stoper_10_21 = fcustom(short_moving_stoper,
                flost_base = lambda p:p/250, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                tstep = lambda sif,i:20,     
                vstep = 10,                  
            )

sm_stoper_8_42 = fcustom(short_moving_stoper,
                flost_base = lambda p:p/300, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                tstep = lambda sif,i:40,     
                vstep = 20,                  
            )

sm_stoper_8_21 = fcustom(short_moving_stoper,
                flost_base = lambda p:p/300, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                tstep = lambda sif,i:20,     
                vstep = 10,                  
            )

sm_stoper_6_21 = fcustom(short_moving_stoper,
                flost_base = lambda p:p/400, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                tstep = lambda sif,i:20,     
                vstep = 12,                  
            )

sm_stoper_5_21 = fcustom(short_moving_stoper,
                flost_base = lambda p:p/666, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                tstep = lambda sif,i:20,     
                vstep = 10,                  
            )

ystop_10_42 = fcustom(atr_stop_y,
                flost_base = iftrade.F100, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                tstep = lambda sif,i:40,     
                vstep = 20,                  
            )

lm_stoper_10_42c = fcustom(long_moving_stoper3,
                flost_base = lambda p:p/250, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                #tstep = 40,     
                #vstep = 20,                  
            )

sm_stoper_10_42c = fcustom(short_moving_stoper3,
                flost_base = lambda p:p/250, 
                fmax_drawdown = iftrade.F360, 
                pmax_drawdown = 0.011, 
                #tstep = 40,     
                #vstep = 20,                  
            )


#utrade2_n = fcustom(utrade2x,bclosers=[atr_stop_y,fcustom(last_stop_short2,ttrace=250,tend=266,vbegin=0.020)],sclosers=[atr_stop_y,fcustom(last_stop_long2,ttrace=240,tend=266,vbegin=0.020)])
utrade2_n = fcustom(utrade2x,bclosers=[fcustom(last_stop_short2,ttrace=250,tend=266,vbegin=0.020),short_rapid_stoper],sclosers=[fcustom(last_stop_long2,ttrace=240,tend=266,vbegin=0.020),long_rapid_stoper]) #收效甚微
#utrade2_n = fcustom(utrade2x,bclosers=[fcustom(last_stop_short2,ttrace=250,tend=266,vbegin=0.020)],sclosers=[fcustom(last_stop_long2,ttrace=240,tend=266,vbegin=0.020)])

#utrade2_n = fcustom(utrade2x,bclosers=[],sclosers=[])
