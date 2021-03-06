# -*- coding: utf-8 -*-
'''
    使用方法

准备
from wolfox.fengine.ifuture.ifreader import read_ifs

from wolfox.fengine.ifuture.ibase import *
from wolfox.fengine.ifuture.ifreader import *
from wolfox.fengine.ifuture.ifuncs import *
import wolfox.fengine.ifuture.ifuncs as ifuncs
import wolfox.fengine.ifuture.iftrade as iftrade

ifmap = read_ifs()  # fname ==> BaseObject(name='$name',transaction=trans)


###计算
i05 = ifmap['IF1005']
i06 = ifmap['IF1006']
i07 = ifmap['IF1007']
i09 = ifmap['IF1009']
i12 = ifmap['IF1012']

trades = iftrade.itrade(i06,[ifuncs.ipmacd_long],[ifuncs.daystop_long,ifuncs.daystop_short])

trades = iftrade.itrade(i06,[ifuncs.ipmacd_short],[ifuncs.daystop_long,ifuncs.daystop_short,ifuncs.istop_60_100_40])

sum([trade.profit for trade in trades])

for trade in trades:
    print trade.profit,trade.actions[0].date,trade.actions[0].time,trade.actions[0].position,trade.actions[0].price,trade.actions[1].date,trade.actions[1].time,trade.actions[1].position,trade.actions[1].price
 
for trade in trades:print trade.profit,trade.actions[0].date,trade.actions[0].time,trade.actions[0].position,trade.actions[0].price,trade.actions[1].date,trade.actions[1].time,trade.actions[1].position,trade.actions[1].price

trades = iftrade.itrade(i06,[ifuncs.ipmacd_short,ifuncs.ipmacd_long],[ifuncs.daystop_long,ifuncs.daystop_short,ifuncs.atr_stop_2_3])
 
trades = iftrade.itrade(i06,[ifuncs.xhdevi],[ifuncs.daystop_long,ifuncs.daystop_short,ifuncs.atr_stop_2_3])


#除了止损之外，将反向开仓也作为平仓信号无多增益
trades = iftrade.itrade(i06,[ifuncs.ipmacd_short,ifuncs.ipmacd_long,ifuncs.down0,ifuncs.up0,ifuncs.xhdevi,ifuncs.xhdevi2,ifuncs.xldevi,ifuncs.xldevi2],[ifuncs.daystop_long,ifuncs.daystop_short,ifuncs.atr_uxstop_2_3])

'''




from wolfox.fengine.ifuture.ibase import *

DTSORT = lambda x,y: int(((x.date%1000000 * 10000)+x.time) - ((y.date%1000000 * 10000)+y.time)) or -x.xtype+y.xtype #避免溢出, 先平仓再开仓

simple_profit = lambda actions: actions[0].price * actions[0].position + actions[1].price * actions[1].position - TAX

def ocfilter(sif):  #在开盘前30分钟和收盘前5分钟不开仓，头三个交易日不开张
    stime = sif.transaction[ITIME]
    soc = np.ones_like(stime)
    soc = gand(greater(stime,944),lesser(stime,1510))
    soc[:275*3] = 0
    soc[-5:] = 0    #最后交易日收盘在1500，防止溢出(因为买入点通常在下一分钟，那么1500不被屏蔽的话，如果有信号就会溢出)
    
    return soc

def last_filter(sif):  
    stime = sif.transaction[ITIME]
    soc = np.ones_like(stime)
    soc = gand(greater(stime,944),lesser(stime,1510))    
    soc[:275*3] = 0
    return soc

def last_trades(actions,calc_profit=simple_profit,length=10):
    '''
        最后交易
    '''
    state = EMPTY
    trades = []
    #for action in actions:
    #    print 'action:',action.date,action.time,action.position,action.price
    if len(actions)>0:
        trade = BaseObject(actions = actions[-length:])
        trades.append(trade)
    return trades

def last_actions(trades):
    if trades:
        for action in trades[-1].actions:
            xposition = "long" if action.position==LONG else 'short'
            xaction = "open" if action.xtype == XOPEN else 'close'
            print u"name=%s,time=%s:%s,%s:%s,price=%s" % (action.name,action.date,action.time,xaction,xposition,action.price)
            #print 'action:',action.date,action.time,action.position,action.price
    else:
        print u"没有交易"

def last_xactions(sif,tradess,acstrategy=late_strategy):
    xactions = []
    for trades in tradess:
        if trades:
            xactions.extend(trades[0].actions)
    xactions.sort(DTSORT)
    xactions.reverse() 
    for action in xactions:
        xposition = "long" if action.position==LONG else 'short'
        xaction = "open" if action.xtype == XOPEN else 'close'
        print u"name=%s,time=%s:%s,%s:%s,price=%s" % (action.name,action.date,action.time,xaction,xposition,action.price)
            #print 'action:',action.date,action.time,action.position,action.price
    else:
        print u"没有交易"


def simple_trades(actions,calc_profit=simple_profit):  #简单的trades,每个trade只有一次开仓和平仓
    ''' 不支持同时双向开仓
    '''
    state = EMPTY
    trades = []
    for action in actions:
        #print 'action:',action.date,action.time,action.position,action.price
        if state == EMPTY:
            if action.xtype == XOPEN:
                #print 'open:',action.date,action.time,action.position,action.price
                state = action.position
                action.vol = 1
                trade = BaseObject(actions = [action])
            else:   #未持仓时碰到平仓动作,忽略
                pass
        elif action.xtype == XCLOSE and action.position != state:    #平仓且方向相反
            #print 'close:',action.date,action.time,action.position,action.price
            trade.actions.append(action)
            trade.profit = calc_profit(trade.actions)
            trades.append(trade)
            action.vol = 1
            state = EMPTY
        else:   #持仓时碰到同向平仓或碰到新开仓指令,忽略
            pass
    return trades
 
def itrade(sif,openers,closers,longfilter=ocfilter,shortfilter=ocfilter,make_trades=simple_trades):
    '''
        所有开仓信号排序交易
        sif: 期指
        openers:opener函数集合
        longfilter/shortfilter:opener过滤器,多空仓必须满足各自过滤器条件才可以发出信号. 比如抑制在0915-0919以及1510-1514开仓等
        closers:closer函数集合
        closer没有过滤器,设置过滤器会导致合约一直开口
    '''
    opens = []  #开仓交易   name:date:time:position:price:vol
    closes = [] #平仓交易
    slongfilter = longfilter(sif)
    sshortfilter = shortfilter(sif)
    if not isinstance(openers,list):   #单个函数
        openers = [openers]
    if not isinstance(closers,list):    #单个函数
        closers = [closers]
    for opener in openers:
        opens.extend(open_position(sif.transaction,opener(sif),slongfilter,sshortfilter))  #开仓必须满足各自sfilter
    opens.sort(DTSORT)
    sopened = np.zeros(len(sif.transaction[IDATE]),int)   #为开仓价格序列,负数为开多仓,正数为开空仓
    for aopen in opens:
        sopened[aopen.index] = aopen.price * aopen.position
    for closer in closers:
        closes.extend(close_position(sif.transaction,closer(sif,sopened)))
    actions = sorted(opens + closes,DTSORT)
    for action in actions:
        action.name = sif.name
    trades = make_trades(actions)   #trade: [open , close] 的序列, 其中前部分都是open,后部分都是close
    return trades

def itrade2(sif,openers,closers,longfilter=ocfilter,shortfilter=ocfilter,make_trades=simple_trades):
    '''
        开平仓信号交易后再排序
        sif: 期指
        openers:opener函数集合
        longfilter/shortfilter:opener过滤器,多空仓必须满足各自过滤器条件才可以发出信号. 比如抑制在0915-0919以及1510-1514开仓等
        closers:closer函数集合
        closer没有过滤器,设置过滤器会导致合约一直开口
    '''
    slongfilter = longfilter(sif)
    sshortfilter = shortfilter(sif)    
    all_trades = []
    if not isinstance(openers,list):   #单个函数
        openers = [openers]
    if not isinstance(closers,list):#单个函数
        closers = [closers]
    for opener in openers:
        if isinstance(opener,tuple):#定义为(opener,closer)对，即有额外的closer
            curcloser = [closer for closer in closers]
            curcloser.append(opener[1])
        else:
            curcloser = closers
        opens = open_position(sif.transaction,opener(sif),slongfilter,sshortfilter)  #开仓必须满足各自sfilter
        sopened = np.zeros(len(sif.transaction[IDATE]),int)   #为开仓价格序列,负数为开多仓,正数为开空仓
        for aopen in opens:
            sopened[aopen.index] = aopen.price * aopen.position
        closes = []
        for closer in closers:
            closes.extend(close_position(sif.transaction,closer(sif,sopened)))
        actions = sorted(opens + closes,DTSORT)
        for action in actions:
            action.name = sif.name
        trades = make_trades(actions)   #trade: [open , close] 的序列, 其中前部分都是open,后部分都是close
        all_trades.extend(trades)
    return filter_trades(all_trades)

def itrade3(sif,openers,bclosers,sclosers,stop_closer,longfilter=ocfilter,shortfilter=ocfilter,make_trades=simple_trades):
    '''
        sif: 期指
        openers:opener函数集合
        closers:无针对性的closer函数集合
        stop_closer: 止损closer函数，只能有一个，通常是atr_uxstop
                      有针对性是指与买入价相关的
                      stop_closer必须处理之前的closers系列发出的卖出信号
        longfilter/shortfilter:opener过滤器,多空仓必须满足各自过滤器条件才可以发出信号. 比如抑制在0915-0919以及1510-1514开仓等
        closer没有过滤器,设置过滤器会导致合约一直开口
    '''
    opens = []  #开仓交易   name:date:time:position:price:vol
    closes = [] #平仓交易
    slongfilter = longfilter(sif)
    sshortfilter = shortfilter(sif)
    if not isinstance(openers,list):   #单个函数
        openers = [openers]
    if not isinstance(bclosers,list):   #单个函数
        bclosers = [bclosers]
    for opener in openers:
        opens.extend(open_position(sif.transaction,opener(sif),slongfilter,sshortfilter))  #开仓必须满足各自sfilter
    opens.sort(DTSORT)
    sopened = np.zeros(len(sif.transaction[IDATE]),int)   #为开仓价格序列,负数为开多仓,正数为开空仓
    for aopen in opens:
        sopened[aopen.index] = aopen.price * aopen.position
    sbclose = np.zeros(len(sif.transaction[IDATE]),int)
    ssclose = np.zeros(len(sif.transaction[IDATE]),int)
    for closer in bclosers:
        #closes.extend(close_position(sif.transaction,closer(sif,sopened)))
        sbclose = gor(sbclose,closer(sif,sopened)) * XBUY
    for closer in sclosers:
        #closes.extend(close_position(sif.transaction,closer(sif,sopened)))
        ssclose = gor(ssclose,closer(sif,sopened)) * XSELL
    closes = close_position(sif.transaction,stop_closer(sif,sopened,sbclose,ssclose))
    actions = sorted(opens + closes,DTSORT)
    for action in actions:
        action.name = sif.name
    trades = make_trades(actions)   #trade: [open , close] 的序列, 其中前部分都是open,后部分都是close
    return trades


def itradex(sif     #期指
            ,openers    #opener函数集合
            ,bclosers   #默认的多平仓函数集合(空头平仓)
            ,sclosers   #默认的空平仓函数集合(多头平仓)
            ,stop_closer    #止损closer函数，只能有一个，通常是atr_uxstop,    
                            #有针对性是指与买入价相关的 stop_closer必须处理之前的closers系列发出的卖出信号
            ,longfilter=ocfilter    #opener过滤器,多空仓必须满足各自过滤器条件才可以发出信号. 
                                    #比如抑制在0915-0919以及1510-1514开仓等
                                    #closer没有过滤器,设置过滤器会导致合约一直开口
            ,shortfilter=ocfilter   #opener过滤器,多空仓必须满足各自过滤器条件才可以发出信号. 
            ,make_trades=simple_trades  #根据开平仓动作撮合交易的函数。对于最后交易序列，用last_trades
            ,collect_trades=sync_tradess    #汇总各opener得到的交易，计算优先级和平仓。
                                            #对于最后交易序列，用last_xactions
            ,acstrategy=late_strategy   #增强开仓时的平仓策略。late_strategy是平最晚的那个信号
            ,priority_level=2500    #筛选opener的优先级, 忽略数字大于此的开仓
        ):
    '''
        本函数针对每个opener计算出各自的闭合交易
        然后集中处理这些闭合交易，根据优先级来确认交易的持续性
            最终得到从开仓到平仓的单个交易的集合
            其中单个交易的要素有：
                开仓价格、时间、交易量
                平仓价格、时间、交易量
                当前主方法名(持有合约的方法)
                filtered: 开仓后被过滤掉的同向低优先级方法名及其信号价格和时间
                rfiltered:开仓后被过滤掉的反向低优先级方法名及其信号价格和时间
                extended: 曾经起效，但因优先级低而被取代的同向方法名及其信号价格和时间. 第一个价格即是开仓价格
                reversed: 逆转持仓的方法及其信号价格和时间
                          如优先级高的中止本次持仓的方法。通常导致反向开仓。  
            要求每个方法的属性有：
                direction:  多/空方向 XBUY/XSELL
                priority:   优先级, 数字越低越高
                            如果不存在，默认为0
                closer:     平仓方法
                            签名为 closer(closers):closers
                                根据传入的closers，返回处理后的，这样，可以取代默认的，也可以在默认之后附加
                            如果不存在，就使用默认的
                stop_closer 止损方法[单个], 如果存在，就取代默认的                                
                filter:     符合filter签名的filter
                name:       名字

    '''
    slongfilter = longfilter(sif)
    sshortfilter = shortfilter(sif)
    snull = np.zeros_like(sif.close)
    if not isinstance(openers,list):   #单个函数
        openers = [openers]
    if not isinstance(bclosers,list):   #单个函数
        bclosers = [bclosers]
    if not isinstance(sclosers,list):   #单个函数
        sclosers = [sclosers]
    
    openers = [opener for opener in openers if opener.priority<priority_level]

    tradess = []
    for opener in openers:
        if 'filter' not in opener.__dict__:
            myfilter = slongfilter if opener.direction == XBUY else sshortfilter
        else:
            myfilter = opener.filter(sif)
        opens = open_position(sif.transaction,opener(sif),myfilter,myfilter) #因为opener只返回一个方向的操作,所以两边都用myfilter，但实际上只有相应的一个有效，另一个是虚的
        #opens.sort(DTSORT)
        sopened = np.zeros(len(sif.transaction[IDATE]),int)   #为开仓价格序列,负数为开多仓,正数为开空仓
        for aopen in opens:
            sopened[aopen.index] = aopen.price * aopen.position
        sclose = np.zeros(len(sif.transaction[IDATE]),int)
        if 'closer' in opener.__dict__:
            if opener.direction == XBUY:
                closers = opener.closer(sclosers)
            elif opener.direction == XSELL:
                closers = opener.closer(bclosers)
        else:
            #print 'opener without close opener.direction = %s' % ('XBUY' if opener.direction == XBUY else 'XSELL',)
            closers = sclosers if opener.direction == XBUY else bclosers
        for closer in closers:
            sclose = gor(sclose,closer(sif,sopened)) * (-opener.direction)
        closes = close_position(sif.transaction,stop_closer(sif,sopened,sclose,sclose)) #因为是单向的，只有一个sclose起作用
        actions = sorted(opens + closes,DTSORT)
        for action in actions:
            action.name = sif.name
        trades = make_trades(actions)   #trade: [open , close] 的序列, 其中前部分都是open,后部分都是close
        for trade in trades:
            trade.functor = opener
            trade.direction = trade.actions[0].position   #LONG/SHORT
        tradess.append(trades)
    #return null_sync_tradess(tradess)
    return collect_trades(sif,tradess,acstrategy)


def null_sync_tradess(tradess):
    xtrades = []
    for trades in tradess:
        xtrades.extend(trades)
    return xtrades

##平仓比较函数中，第一个参数的优先级低于第二个
def early_strategy(action1,action2):#多选时的平仓策略，最早平仓
    return action1 if action1.date<action2.date else action2

def late_strategy(action1,action2):#多选时的平仓策略，最晚平仓. 从止损的角度来看比较兼顾
    return action1 if action1.date>=action2.date else action2

def min_strategy(action1,action2):#多选时的平仓策略，最窄平仓.取得是最高的平仓价，有预读的可能性
    if action1.position == LONG:#多平仓，即买入平仓的，以低者为窄
        return action1 if action1.price < action2.price else action2
    else:#空平仓，即卖出平多仓的，平仓位应越来越高
        return action1 if action1.price > action2.price else action2

def max_strategy(action1,action2):#多选时的平仓策略，最宽平仓. 取得都是最低的平仓价，不合理
    if action1.position == LONG:#多平仓，即买入平仓的，以高者为宽
        return action1 if action1.price > action2.price else action2
    else:#空平仓，即卖出平多仓的，平仓位应越来越低
        return action1 if action1.price < action2.price else action2

def a1_strategy(action1,action2):#始终选择第1次的平仓位,从止损来看最合理
    return action1

def a2_strategy(action1,action2):#始终选择第2次的平仓位
    ##a2的问题是可能会抬高臀位，比如本来2700买入，2720出现新的高优先级信号，那么按之前的方法，其止损在2700左右，而新的情况导致止损到了2715左右，
    return action2



DTSORT2 = lambda x,y: int(((x.date%1000000 * 10000)+x.time) - ((y.date%1000000 * 10000)+y.time))
def sync_tradess(sif,tradess,acstrategy=late_strategy):
    trans = sif.transaction
    sdate = trans[IDATE]
    stime = trans[ITIME]
    sopen = trans[IOPEN]
    sclose = trans[ICLOSE]
    shigh = trans[IHIGH]
    slow = trans[ILOW]    
    
    xtrades = []
    finished =False
    cur_trade = find_first(tradess)
    if cur_trade == None:
        return []
    extended,filtered,rfiltered,reversed = [],[],[],[]
    close_action = cur_trade.actions[-1]
    print '#####################first:',close_action.time
    while True:
        trade = find_first(tradess)
        if trade == None:
            xtrades.append(close_trade(sif,cur_trade,close_action,extended,filtered,rfiltered,reversed))
            break
        print 'find:date=%s,time=%s,functor=%s' % (trade.actions[0].date,trade.actions[0].time,trade.functor)  
        if DTSORT2(trade.actions[0],close_action)>0:  #时间超过
            #print u'时间超过'
            xtrades.append(close_trade(sif,cur_trade,close_action,extended,filtered,rfiltered,reversed))
            cur_trade = trade
            close_action = cur_trade.actions[-1]
            extended,filtered,rfiltered,reversed = [],[],[],[]
            continue
           
        #print trade.functor,trade.functor.priority ,cur_trade.functor,cur_trade.functor.priority
        if trade.functor.priority < cur_trade.functor.priority:
            #print u'高优先级'
            if trade.direction == cur_trade.direction:  #同向取代关系
                print u'同向增强,%s|%s:%s被%s增强'%(cur_trade.functor,cur_trade.actions[0].date,cur_trade.actions[0].time,trade.functor)
                close_action = acstrategy(close_action,trade.actions[-1])
                extended.append(cur_trade)
                cur_trade = trade
            else:   #逆向平仓
                print u'逆向平仓'
                reversed.append(trade)
                xindex = reversed[0].actions[0].index
                cposition = BaseObject(index=xindex,date=sdate[xindex],time=stime[xindex],position=reversed[0].direction,xtype=XCLOSE)    #因为已经抑制了1514开仓,必然不会溢出
                cposition.price = make_price(cposition.position,sopen[xindex],sclose[xindex],shigh[xindex],slow[xindex])
                xtrades.append(close_trade(sif,cur_trade,cposition,extended,filtered,rfiltered,reversed))
                cur_trade = trade
                extended,filtered,rfiltered,reversed = [],[],[],[]
                close_action = cur_trade.actions[-1]                
        else:   #低优先级
            #print u'低优先级'
            if trade.direction == cur_trade.direction:  #同向屏蔽
                filtered.append(trade)
            else:   #逆向屏蔽
                rfiltered.append(trade)
    return xtrades

def close_trade(sif,cur_trade,close_action,extended,filtered,rfiltered,reversed,calc_profit=simple_profit):
    open_action = extended[0].actions[0] if extended else cur_trade.actions[0]
    trade = BaseObject(actions=[open_action,close_action])
    trade.profit = calc_profit(trade.actions)
    trade.extended = extended
    trade.filtered = filtered
    trade.rfiltered = rfiltered
    trade.reversed = reversed
    trade.functor = cur_trade.functor
    trade.trade = cur_trade
    return trade


def find_first(tradess):
    curdt = BaseObject(date=999999,time=9999)
    cur_trades = None
    ftrade = None
    for trades in tradess:
        if trades and DTSORT2(curdt,trades[0].actions[0])>0:
            curdt = BaseObject(date=trades[0].actions[0].date,time=trades[0].actions[0].time)
            cur_trades = trades
    if cur_trades:
        ftrade = cur_trades[0]
        del cur_trades[0]
        #print 'find:date=%s,time=%s' % (ftrade.actions[0].date,ftrade.actions[0].time)
    return ftrade
            


action_dtime = lambda action: action.date%1000000 * 10000 + action.time
def filter_trades(trades):
    '''
        去掉交易时间交叉的纪录
    '''
    sorter = lambda x,y:int(action_dtime(x.actions[0]) - action_dtime(y.actions[0]))
    trades.sort(sorter)
    revs = []
    closed_dtime = 0
    for trade in trades:
        dtime = action_dtime(trade.actions[0])
        if dtime > closed_dtime:
            revs.append(trade)
            closed_dtime = action_dtime(trade.actions[-1])
        else:
            #print 'skip action:',trade.actions[0].date,trade.actions[0].time
            pass
    return revs


def open_position(trans,sopener,slongfilter,sshortfilter):
    '''
        sopener中,XBUY表示开多仓,XSELL表示开空仓
    '''
    slong = band(equals(sopener,XBUY),slongfilter) * LONG 
    #print slongfilter[-10:],sshortfilter[-10:]
    sshort = band(equals(sopener,XSELL),sshortfilter) * SHORT
    #ss = slong + sshort #多空抵消
    positions = xposition(trans,slong,XOPEN)
    positions.extend(xposition(trans,sshort,XOPEN))
    return positions

def close_position(trans,scloser):
    ''' scloser中, XBUY表示平空(买入),XSELL表示平多(卖出)
    '''
    #print scloser[scloser.nonzero()]
    slong = equals(scloser,XBUY) * LONG  #避免直接将scloser中的信号表示与LONG/SHORT隐蔽耦合
    #print slong[slong.nonzero()]
    sshort = equals(scloser,XSELL) * SHORT
    #print sshort[sshort.nonzero()],SHORT
    positions = xposition(trans,slong,XCLOSE)
    positions.extend(xposition(trans,sshort,XCLOSE))
    return positions

def xposition(trans,saction,xtype,defer=1):
    sdate = trans[IDATE]
    stime = trans[ITIME]
    sopen = trans[IOPEN]
    sclose = trans[ICLOSE]
    shigh = trans[IHIGH]
    slow = trans[ILOW]    
    isignal = saction.nonzero()[0]
    positions = []
    for i in isignal:
        xindex = i + defer  #defer后动作，一般为下一分钟
        if xindex >= len(sclose):   #如果是最后一分钟，则放弃. 这种情况只会出现在动态计算中，且该分钟未走完(走完的话应该出现下一分钟的报价)，所以放弃是正常操作
            continue
        #print xindex,trans[ITIME][xindex]
        direct = saction[i]
        position = BaseObject(index=xindex,date=sdate[xindex],time=stime[xindex],position=direct,xtype=xtype)    #因为已经抑制了1514开仓,必然不会溢出
        position.price = make_price(direct,sopen[xindex],sclose[xindex],shigh[xindex],slow[xindex])
        positions.append(position)
    return positions


def make_price(position,open,close,high,low):
    #return open
    if position == LONG:
        return (open+high)/2
        #return open + (high - open) / 2
        #return high
    else:
        return (open+low)/2
        #return open - (open - low) / 2
        #return low
 

def snet(trades,netfrom=0,datefrom=20100401,dateto=20200101):
    s = netfrom
    ss = [BaseObject(date=datefrom,net=netfrom)]
    for trade in trades:
        tdate = trade.actions[-1].date
        if tdate > datefrom and tdate < dateto: #忽略掉小于开始时间的
            s += trade.profit
            snew = BaseObject(date=tdate,net=s)
            ss.append(snew)
    return ss

def max_drawdown(trades,datefrom=20100401,dateto=20200101):
    smax = 0    #最大连续回撤
    max1 = 0    #最大单笔回撤
    curs = 0
    for trade in trades:
        tdate = trade.actions[-1].date
        if tdate > datefrom and tdate < dateto: #忽略掉小于开始时间的
            if trade.profit > 0:
                curs = 0
            else:
                curs += trade.profit   #本为负数
                if curs < smax:
                    smax = curs
            if trade.profit < max1:
                max1 = trade.profit
    return smax,max1;

def max_win(trades,datefrom=20100401,dateto=20200101):
    smax = 0    #最大连续盈利
    max1 = 0    #最大单笔盈利 
    curs = 0
    for trade in trades:
        tdate = trade.actions[-1].date
        if tdate > datefrom and tdate < dateto: #忽略掉小于开始时间的
            if trade.profit > 0:
                curs += trade.profit
                if curs > smax:
                    smax = curs
            else:
                curs = 0
            if trade.profit > max1:
                max1 = trade.profit
    return smax,max1;

def avg_wl(trades,datefrom=20100401,dateto=20200101):
    wsum,wtime = 0,0
    lsum,ltime = 0,0
    for trade in trades:
        tdate = trade.actions[-1].date
        if tdate > datefrom and tdate < dateto: #忽略掉小于开始时间的
            if trade.profit > 0:
                wsum += trade.profit
                wtime += 1
            else:
                lsum += trade.profit
                ltime +=1
    return wsum,wtime,lsum,ltime
    

def R(trades,datefrom=20100401,dateto=20200101):
    wsum,wtime,lsum,ltime = avg_wl(trades,datefrom,dateto)
    if lsum == 0 or ltime == 0:
        return XBASE
    xavg = (wsum + lsum) * XBASE / (wtime+ltime)
    lavg = lsum * XBASE / ltime
    return xavg * XBASE / abs(lavg)


def RR(trades,datefrom=20100401,dateto=20200101):
    '''
        R的计算的调整
        比如一个算法交易80次，成功40次，失败40次，总收益1000，总损失400，则R = 10/(400/40) = 1
            而另一个算法交易100次，成功40次，失败60次，总收益900，总损失500，则R=9/(500/60) = 1.08
            但是显然是第一个算法好。第二个算法只不过多出20次较小的损失而已
            而且在实际操作中结果也是第一个好。
        如果用RR，
        则第一个算法: RR = 1000/400 * 40 * 40 /(80*80) = 5/8 = 0.625
            第二个算法: RR = 900/500 * 40 * 60 /(100*100) = .24*18 = .432
    '''
    wsum,wtime,lsum,ltime = avg_wl(trades,datefrom,dateto)
    if lsum == 0 or ltime == 0:
        return XBASE
    return (wsum+lsum)*XBASE/abs(lsum) * wtime * ltime /(wtime+ltime)/(wtime+ltime)

def psum(trades,datefrom=0,dateto=99999999):
    '''
        [x,y)区间
    '''
    return sum([trade.profit for trade in trades if trade.actions[0].date>=datefrom and trade.actions[0].date<dateto])

afm = {1:lambda sif:sif.atr
        ,5:lambda sif:sif.atr5x
        ,15:lambda sif:sif.atr15x
        ,30:lambda sif:sif.atr30x
        ,270:lambda sif:sif.atrdx
    }

def atr_uxstop(sif,sopened,sbclose,ssclose,lost_times=200,win_times=300,max_drawdown=200,min_lost=30,max_lost=70,natr=1):
    '''
        atr止损
        sif为实体
        sopen为价格序列，其中负数表示开多仓，正数表示开空仓
        sbclose是价格无关序列所发出的买入平仓信号集合(平空仓)
        ssclose是价格无关序列所发出的卖出平仓信号集合(平多仓)
        max_drawdown: 从最高点起的最大回落
        min_lost: 最小止损
        max_lost: 最大止损
        只能持有一张合约。即当前合约在未平前会屏蔽掉所有其它开仓
    '''
    #print sbclose[-10:],ssclose[-10:]
    satr = afm[natr](sif)
    trans = sif.transaction
    rev = np.zeros_like(sopened)
    isignal = np.nonzero(sopened)[0]
    ilong_closed = 0    #多头平仓日
    ishort_closed = 0   #空头平仓日
    for i in isignal:
        price = sopened[i]
        willlost = satr[i] * lost_times / XBASE / XBASE
        if willlost < min_lost:
            willlost = min_lost
        if willlost > max_lost:
            willlost = max_lost
        if i < ilong_closed or i<ishort_closed:    #已经开了仓，且未平，不再计算            
            print 'skiped',trans[IDATE][i],trans[ITIME][i],trans[IDATE][ilong_closed],trans[ITIME][ilong_closed],trans[IDATE][ishort_closed],trans[ITIME][ishort_closed]
            continue
        if price<0: #多头止损
            #print 'find long stop:',i
            #if i < ilong_closed:    #已经开了多头仓，且未平，不再计算
            #    print 'skiped',trans[IDATE][i],trans[ITIME][i],trans[IDATE][ilong_closed],trans[ITIME][ilong_closed]
            #    continue
            buy_price = -price
            lost_stop = buy_price - willlost
            cur_high = max(buy_price,trans[ICLOSE][i])
            win_stop = cur_high - satr[i] * win_times / XBASE / XBASE
            cur_stop = lost_stop if lost_stop > win_stop else win_stop
            if ssclose[i] == XSELL:
                print 'sell signali:',trans[IDATE][i],trans[ITIME][i],trans[ICLOSE][i]
            if trans[ICLOSE][i] < cur_stop or ssclose[i] == XSELL:#到达止损或平仓
                #print '----sell----------:',trans[IDATE][i],trans[ITIME][i],cur_stop,trans[ICLOSE][i],cur_high,lost_stop
                ilong_closed = i
                rev[i] = XSELL            
            else:
                for j in range(i+1,len(rev)):
                    if ssclose[j] == XSELL:
                        print 'sell signalj:',trans[IDATE][j],trans[ITIME][j],cur_stop,trans[ICLOSE][j]
                    #print trans[ITIME][j],buy_price,lost_stop,cur_high,win_stop,cur_stop,trans[ILOW][j],satr[j]
                    if trans[ILOW][j] < cur_stop or ssclose[j] == XSELL:    #
                        rev[j] = XSELL
                        #print 'sell:',i,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j]
                        ilong_closed = j
                        break
                    nhigh = trans[IHIGH][j]
                    if(nhigh > cur_high):
                        cur_high = nhigh
                        drawdown = satr[j] * win_times / XBASE / XBASE
                        if drawdown > max_drawdown:
                            drawdown = max_drawdown
                        win_stop = cur_high - drawdown
                        #win_stop = cur_high - satr[j] * win_times / XBASE
                        #print nhigh,cur_stop,win_stop,satr[j]
                        if cur_stop < win_stop:
                            cur_stop = win_stop
        else:   #空头止损
            #print 'find short stop:',i
            #if i < ishort_closed:    #已经开了空头仓，且未平，不再计算
            #    print 'skiped',trans[IDATE][i],trans[ITIME][i],trans[IDATE][ishort_closed],trans[ITIME][ishort_closed]
            #    continue
            sell_price = price
            lost_stop = sell_price + willlost
            cur_low = min(sell_price,trans[ICLOSE][i])
            win_stop = cur_low + satr[i] * win_times / XBASE / XBASE
            cur_stop = lost_stop if lost_stop < win_stop else win_stop
            if sbclose[i] == XBUY:
                print 'buy signali:',trans[IDATE][i],trans[ITIME][i],trans[ICLOSE][i]
            if trans[ICLOSE][i] > cur_stop or sbclose[i] == XBUY:
                #print '----buy----------:',cur_stop,trans[ICLOSE][i],cur_high,lost_stop
                ishort_closed = i
                rev[i] = XBUY
            else:
                for j in range(i+1,len(rev)):
                    if sbclose[j] == XBUY:
                        print 'buy signalj:',trans[IDATE][j],trans[ITIME][j],cur_stop,trans[ICLOSE][j]
                    #print trans[ITIME][j],sell_price,lost_stop,cur_low,win_stop,cur_stop,trans[IHIGH][j],satr[j]                
                    if trans[IHIGH][j] > cur_stop or sbclose[j] == XBUY:#
                        ishort_closed = j
                        rev[j] = XBUY
                        #print 'buy:',j
                        #print 'buy:',i,price,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j]                        
                        break
                    nlow = trans[ILOW][j]
                    if(nlow < cur_low):
                        cur_low = nlow
                        drawdown = satr[j] * win_times / XBASE / XBASE
                        if drawdown > max_drawdown:
                            drawdown = max_drawdown
                        win_stop = cur_low + drawdown
                        #print nlow,cur_stop,win_stop,satr[j]
                        #win_stop = cur_low + satr[j] * win_times / XBASE / XBASE
                        if cur_stop > win_stop:
                            cur_stop = win_stop
    return rev

atr_uxstop_15_45 = fcustom(atr_uxstop,lost_times=150,win_times=450,max_drawdown=200,min_lost=30)  
atr_uxstop_15_5 = fcustom(atr_uxstop,lost_times=150,win_times=500,max_drawdown=200,min_lost=30)
atr_uxstop_15_6 = fcustom(atr_uxstop,lost_times=150,win_times=600,max_drawdown=200,min_lost=30)   #
atr_uxstop_15_A = fcustom(atr_uxstop,lost_times=150,win_times=1000,max_drawdown=200,min_lost=30)
atr_uxstop_15_15 = fcustom(atr_uxstop,lost_times=150,win_times=150,max_drawdown=200,min_lost=30)  
atr_uxstop_2_2 = fcustom(atr_uxstop,lost_times=200,win_times=200,max_drawdown=200,min_lost=30)  
atr_uxstop_15_2 = fcustom(atr_uxstop,lost_times=150,win_times=200,max_drawdown=200,min_lost=30)  
atr_uxstop_2_6 = fcustom(atr_uxstop,lost_times=200,win_times=600,max_drawdown=200,min_lost=30)   
atr_uxstop_3_6 = fcustom(atr_uxstop,lost_times=300,win_times=600,max_drawdown=200,min_lost=30)   
atr_uxstop_4_6 = fcustom(atr_uxstop,lost_times=400,win_times=600,max_drawdown=200,min_lost=30)   

atr_uxstop_6_6 = fcustom(atr_uxstop,lost_times=600,win_times=600,max_drawdown=200,min_lost=30)   



atr_uxstop_15_6_45 = fcustom(atr_uxstop,lost_times=150,win_times=600,max_drawdown=200,min_lost=45)   #


atr_uxstop_1_2 = fcustom(atr_uxstop,lost_times=100,win_times=200,max_drawdown=200,min_lost=30)
atr_uxstop_15_25 = fcustom(atr_uxstop,lost_times=150,win_times=250,max_drawdown=200,min_lost=30)
atr_uxstop_2_3 = fcustom(atr_uxstop,lost_times=200,win_times=300,max_drawdown=200,min_lost=30)
atr_uxstop_25_4 = fcustom(atr_uxstop,lost_times=250,win_times=400,max_drawdown=200,min_lost=30)
atr_uxstop_25_6 = fcustom(atr_uxstop,lost_times=250,win_times=600,max_drawdown=200,min_lost=30)
atr_uxstop_2_4 = fcustom(atr_uxstop,lost_times=200,win_times=400,max_drawdown=200,min_lost=30)
atr_uxstop_3_4 = fcustom(atr_uxstop,lost_times=300,win_times=400,max_drawdown=200,min_lost=30)
atr_uxstop_15_4 = fcustom(atr_uxstop,lost_times=150,win_times=400,max_drawdown=200,min_lost=30)    
atr_uxstop_1_4 = fcustom(atr_uxstop,lost_times=100,win_times=400,max_drawdown=200,min_lost=30)
atr_uxstop_05_4 = fcustom(atr_uxstop,lost_times=50,win_times=400,max_drawdown=200,min_lost=30)
atr_uxstop_1_5 = fcustom(atr_uxstop,lost_times=100,win_times=500,max_drawdown=200,min_lost=30)
atr_uxstop_05_2 = fcustom(atr_uxstop,lost_times=50,win_times=200,max_drawdown=200,min_lost=30)
atr_uxstop_05_15 = fcustom(atr_uxstop,lost_times=50,win_times=150,max_drawdown=200,min_lost=30)
atr_uxstop_05_1 = fcustom(atr_uxstop,lost_times=50,win_times=100,max_drawdown=200,min_lost=30)
atr_uxstop_1_6 = fcustom(atr_uxstop,lost_times=100,win_times=600,max_drawdown=200,min_lost=30)

import wolfox.fengine.ifuture.ifuncs as ifuncs

itrade3u = fcustom(itrade3,stop_closer=atr_uxstop_15_6,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])

#平仓：买入后macd马上下叉，则卖出;卖出后macd马上上叉，也平仓；另持多仓时出现新的买入点，但macd即刻下叉，则将持仓卖出,反之亦然
#diff5<0,diff30<0的顶背离作为平多仓条件，把特定底背离当作平空仓条件

itrade3x = fcustom(itrade3,stop_closer=atr_uxstop_15_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1,ifuncs.ipmacd_long_devi1],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])

#itrade3y = fcustom(itrade3,stop_closer=atr_uxstop_15_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=[ifuncs.daystop_long,ifuncs.ipmacd_short,ifuncs.down01,ifuncs.dmacd_short5,ifuncs.ipmacdx_short,ifuncs.ipmacd_short5,ifuncs.ma30_short,ifuncs.ma60_short,ifuncs.xmacd_stop_long1])

#sycloser = [ifuncs.daystop_long,ifuncs.ipmacd_short_1,ifuncs.ipmacd_short_2,ifuncs.ipmacd_short_3,ifuncs.ma3x10_short,ifuncs.down01,ifuncs.dmacd_short5,ifuncs.ipmacdx_short,ifuncs.ipmacd_short5,ifuncs.ma30_short,ifuncs.ma60_short,ifuncs.xmacd_stop_long1]

sycloser = [ifuncs.daystop_long]


#动态止损，去掉daystop_long
#sycloser_d = [ifuncs.ipmacd_short_1,ifuncs.ipmacd_short_2,ifuncs.ipmacd_short_3,ifuncs.ma3x10_short,ifuncs.down01,ifuncs.dmacd_short5,ifuncs.ipmacdx_short,ifuncs.ipmacd_short5,ifuncs.ma30_short,ifuncs.ma60_short]

sycloser_d = []

#sycloser_k = [ifuncs.daystop_long,ifuncs.ipmacd_short_1,ifuncs.ipmacd_short_2,ifuncs.ipmacd_short_3,ifuncs.ma3x10_short,ifuncs.down01,ifuncs.dmacd_short5,ifuncs.ipmacdx_short,ifuncs.ipmacd_short5,ifuncs.ma30_short,ifuncs.ma60_short]

sycloser_k = sycloser

#sycloser_kd = [ifuncs.ipmacd_short_1,ifuncs.ipmacd_short_2,ifuncs.ipmacd_short_3,ifuncs.ma3x10_short,ifuncs.down01,ifuncs.dmacd_short5,ifuncs.ipmacdx_short,ifuncs.ipmacd_short5,ifuncs.ma30_short,ifuncs.ma60_short]

sycloser_kd = []


lycloser = [r for r in sycloser]
del lycloser[0] #去掉daystop_long

itrade3y = fcustom(itrade3,stop_closer=atr_uxstop_15_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)


ltrade3y = fcustom(itrade3,stop_closer=atr_uxstop_15_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=last_trades,longfilter=last_filter,shortfilter=last_filter)



#空头不把macd即刻反叉作为平仓条件
itrade3yk = fcustom(itrade3,stop_closer=atr_uxstop_15_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser_k)

itrade3x1 = fcustom(itrade3,stop_closer=atr_uxstop_1_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1,ifuncs.ipmacd_long_devi1],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])

itrade3y1 = fcustom(itrade3,stop_closer=atr_uxstop_1_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y2 = fcustom(itrade3,stop_closer=atr_uxstop_2_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y3 = fcustom(itrade3,stop_closer=atr_uxstop_3_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y4 = fcustom(itrade3,stop_closer=atr_uxstop_4_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)
itrade3y6 = fcustom(itrade3,stop_closer=atr_uxstop_6_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)


ltrade3y1 = fcustom(itrade3,stop_closer=atr_uxstop_1_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=last_trades,longfilter=last_filter,shortfilter=last_filter)
ltrade3y2 = fcustom(itrade3,stop_closer=atr_uxstop_2_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=last_trades,longfilter=last_filter,shortfilter=last_filter)
ltrade3y3 = fcustom(itrade3,stop_closer=atr_uxstop_3_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=last_trades,longfilter=last_filter,shortfilter=last_filter)
ltrade3y4 = fcustom(itrade3,stop_closer=atr_uxstop_4_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=last_trades,longfilter=last_filter,shortfilter=last_filter)
ltrade3y6 = fcustom(itrade3,stop_closer=atr_uxstop_6_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=last_trades,longfilter=last_filter,shortfilter=last_filter)



itrade3x45 = fcustom(itrade3,stop_closer=atr_uxstop_15_6_45,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1,ifuncs.ipmacd_long_devi1],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])


itrade1525 = fcustom(itrade3,stop_closer=atr_uxstop_15_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])

itrade256 = fcustom(itrade3,stop_closer=atr_uxstop_15_6,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])



#空头不把即刻反叉作为平仓选项
itrade3xk = fcustom(itrade3,stop_closer=atr_uxstop_15_6,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])


import wolfox.fengine.ifuture.tfuncs as tfuncs

#itrade3xkx = fcustom(itrade3,stop_closer=atr_uxstop_15_6,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1,tfuncs.xdevi_stop_long12])




####5分钟atr5
atr5_uxstop_15_45 = fcustom(atr_uxstop,lost_times=150,win_times=450,max_drawdown=200,min_lost=30,natr=5)  
atr5_uxstop_15_5 = fcustom(atr_uxstop,lost_times=150,win_times=500,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_15_6 = fcustom(atr_uxstop,lost_times=150,win_times=600,max_drawdown=200,min_lost=30,natr=5)   #
atr5_uxstop_15_A = fcustom(atr_uxstop,lost_times=150,win_times=1000,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_15_15 = fcustom(atr_uxstop,lost_times=150,win_times=150,max_drawdown=200,min_lost=30,natr=5)  
atr5_uxstop_2_2 = fcustom(atr_uxstop,lost_times=200,win_times=200,max_drawdown=200,min_lost=30,natr=5)  
atr5_uxstop_15_2 = fcustom(atr_uxstop,lost_times=150,win_times=200,max_drawdown=200,min_lost=30,natr=5)  
atr5_uxstop_2_6 = fcustom(atr_uxstop,lost_times=200,win_times=600,max_drawdown=200,min_lost=30,natr=5)   
atr5_uxstop_3_6 = fcustom(atr_uxstop,lost_times=300,win_times=600,max_drawdown=200,min_lost=30,natr=5)   
atr5_uxstop_4_6 = fcustom(atr_uxstop,lost_times=400,win_times=600,max_drawdown=200,min_lost=30,natr=5)   

atr5_uxstop_6_6 = fcustom(atr_uxstop,lost_times=600,win_times=600,max_drawdown=200,min_lost=30,natr=5)   



atr5_uxstop_15_6_45 = fcustom(atr_uxstop,lost_times=150,win_times=600,max_drawdown=200,min_lost=45,natr=5)   #


atr5_uxstop_1_2 = fcustom(atr_uxstop,lost_times=100,win_times=200,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_15_25 = fcustom(atr_uxstop,lost_times=150,win_times=250,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_2_3 = fcustom(atr_uxstop,lost_times=200,win_times=300,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_25_4 = fcustom(atr_uxstop,lost_times=250,win_times=400,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_25_6 = fcustom(atr_uxstop,lost_times=250,win_times=600,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_2_4 = fcustom(atr_uxstop,lost_times=200,win_times=400,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_3_4 = fcustom(atr_uxstop,lost_times=300,win_times=400,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_15_4 = fcustom(atr_uxstop,lost_times=150,win_times=400,max_drawdown=200,min_lost=30,natr=5)    
atr5_uxstop_1_4 = fcustom(atr_uxstop,lost_times=100,win_times=400,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_05_4 = fcustom(atr_uxstop,lost_times=50,win_times=400,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_1_5 = fcustom(atr_uxstop,lost_times=100,win_times=500,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_05_2 = fcustom(atr_uxstop,lost_times=50,win_times=200,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_05_25 = fcustom(atr_uxstop,lost_times=50,win_times=250,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_05_3 = fcustom(atr_uxstop,lost_times=50,win_times=300,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_05_15 = fcustom(atr_uxstop,lost_times=50,win_times=150,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_05_1 = fcustom(atr_uxstop,lost_times=50,win_times=100,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_05_05 = fcustom(atr_uxstop,lost_times=50,win_times=50,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_1_6 = fcustom(atr_uxstop,lost_times=100,win_times=600,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_05_6 = fcustom(atr_uxstop,lost_times=50,win_times=600,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_1_25 = fcustom(atr_uxstop,lost_times=100,win_times=250,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_1_15 = fcustom(atr_uxstop,lost_times=100,win_times=150,max_drawdown=200,min_lost=30,natr=5)


atr5_uxstop_05_25b = fcustom(atr_uxstop,lost_times=50,win_times=250,max_drawdown=200,min_lost=50,natr=5)
atr5_uxstop_05_25c = fcustom(atr_uxstop,lost_times=50,win_times=250,max_drawdown=200,min_lost=60,natr=5)


itrade3y_5 = fcustom(itrade3,stop_closer=atr5_uxstop_15_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)


ltrade3y_5 = fcustom(itrade3,stop_closer=atr5_uxstop_15_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=last_trades,longfilter=last_filter,shortfilter=last_filter)



#空头不把macd即刻反叉作为平仓条件
itrade3yk_5 = fcustom(itrade3,stop_closer=atr5_uxstop_15_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser_k)

itrade3x1_5 = fcustom(itrade3,stop_closer=atr5_uxstop_1_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1,ifuncs.ipmacd_long_devi1],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])

itrade3y05_5 = fcustom(itrade3,stop_closer=atr5_uxstop_05_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y05_15 = fcustom(itrade3,stop_closer=atr5_uxstop_05_15,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y05_1 = fcustom(itrade3,stop_closer=atr5_uxstop_05_1,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)
itrade3y05_05 = fcustom(itrade3,stop_closer=atr5_uxstop_05_05,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)


itrade3y05_2 = fcustom(itrade3,stop_closer=atr5_uxstop_05_2,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y05_25 = fcustom(itrade3,stop_closer=atr5_uxstop_05_25,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser) ###最好的搭配

itrade3y05_25b = fcustom(itrade3,stop_closer=atr5_uxstop_05_25b,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser) ###最好的搭配

itrade3y05_25c = fcustom(itrade3,stop_closer=atr5_uxstop_05_25c,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser) ###最好的搭配

itrade3y05_3 = fcustom(itrade3,stop_closer=atr5_uxstop_05_3,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)
itrade3y05_4 = fcustom(itrade3,stop_closer=atr5_uxstop_05_4,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y1_2 = fcustom(itrade3,stop_closer=atr5_uxstop_1_2,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)
itrade3y1_15 = fcustom(itrade3,stop_closer=atr5_uxstop_1_15,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y1_25 = fcustom(itrade3,stop_closer=atr5_uxstop_1_25,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)


itrade3y1_5 = fcustom(itrade3,stop_closer=atr5_uxstop_1_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y2_5 = fcustom(itrade3,stop_closer=atr5_uxstop_2_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y3_5 = fcustom(itrade3,stop_closer=atr5_uxstop_3_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)

itrade3y4_5 = fcustom(itrade3,stop_closer=atr5_uxstop_4_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)
itrade3y6_5 = fcustom(itrade3,stop_closer=atr5_uxstop_6_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=sycloser)


ltrade3y1_5 = fcustom(itrade3,stop_closer=atr5_uxstop_1_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=last_trades,longfilter=last_filter,shortfilter=last_filter)
ltrade3y2_5 = fcustom(itrade3,stop_closer=atr5_uxstop_2_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=last_trades,longfilter=last_filter,shortfilter=last_filter)
ltrade3y3_5 = fcustom(itrade3,stop_closer=atr5_uxstop_3_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=last_trades,longfilter=last_filter,shortfilter=last_filter)
ltrade3y4_5 = fcustom(itrade3,stop_closer=atr5_uxstop_4_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=last_trades,longfilter=last_filter,shortfilter=last_filter)
ltrade3y6_5 = fcustom(itrade3,stop_closer=atr5_uxstop_6_6,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=last_trades,longfilter=last_filter,shortfilter=last_filter)

ltrade3y0525_5 = fcustom(itrade3,stop_closer=atr5_uxstop_05_25,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=last_trades,longfilter=last_filter,shortfilter=last_filter)

ltrade3y0520_5 = fcustom(itrade3,stop_closer=atr5_uxstop_05_2,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=last_trades,longfilter=last_filter,shortfilter=last_filter)

ltrade3y0515_5 = fcustom(itrade3,stop_closer=atr5_uxstop_05_15,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=last_trades,longfilter=last_filter,shortfilter=last_filter)

ltrade3y0530_5 = fcustom(itrade3,stop_closer=atr5_uxstop_05_3,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=last_trades,longfilter=last_filter,shortfilter=last_filter)

ltrade3y1025_5 = fcustom(itrade3,stop_closer=atr5_uxstop_1_25,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=last_trades,longfilter=last_filter,shortfilter=last_filter)

ltrade3y1525_5 = fcustom(itrade3,stop_closer=atr5_uxstop_15_25,bclosers=[ifuncs.xmacd_stop_short1],sclosers=sycloser_d,make_trades=last_trades,longfilter=last_filter,shortfilter=last_filter)


itrade3x45_5 = fcustom(itrade3,stop_closer=atr5_uxstop_15_6_45,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1,ifuncs.ipmacd_long_devi1],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])


itrade1525_5 = fcustom(itrade3,stop_closer=atr5_uxstop_15_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])

itrade256_5 = fcustom(itrade3,stop_closer=atr5_uxstop_15_6,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])



#空头不把即刻反叉作为平仓选项
itrade3xk_5 = fcustom(itrade3,stop_closer=atr5_uxstop_15_6,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])


itradex_y = fcustom(itradex,stop_closer=atr_uxstop_15_6,bclosers=[ifuncs.daystop_short],sclosers=sycloser)
itradex5_y = fcustom(itradex,stop_closer=atr5_uxstop_05_25,bclosers=[ifuncs.daystop_short],sclosers=sycloser)

#相比较物
itrade3yx = fcustom(itrade3,stop_closer=atr_uxstop_15_6,bclosers=[ifuncs.daystop_short],sclosers=sycloser)


