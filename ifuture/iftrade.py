# -*- coding: utf-8 -*-
'''
    核心交易调度模块
'''


from wolfox.fengine.ifuture.ibase import *

DTSORT = lambda x,y: int(((x.date%1000000 * 10000)+x.time) - ((y.date%1000000 * 10000)+y.time)) or -x.xtype+y.xtype #避免溢出, 先平仓再开仓

simple_profit = lambda actions: actions[0].price * actions[0].position + actions[1].price * actions[1].position - TAX

fdirection = fcustom(get_func_attr,attr_name='direction')
fpriority = fcustom(get_func_attr,attr_name='priority')

def normal_profit(actions,max_lost=-120): #最多12点损失
    profit = actions[0].price * actions[0].position + actions[1].price * actions[1].position
    if profit < max_lost:
        profit = max_lost
    profit -= TAX
    return profit

def limit_profit(trades,down_limit):
    #用于时候处理profit
    down_limit -= TAX
    for trade in trades:
        if trade.profit < down_limit:
            trade.profit = down_limit

def delay_filter(sif,signal,delayed=5,limit=60):
    '''
        对signal进行delay处理
        delay值为信号延后发送的周期数
        limit是信号破位的限制
    '''
    sb = signal == XBUY
    ss = signal == XSELL
    smax = tmax(sif.high,delayed)
    smin = tmin(sif.low,delayed)
    psb = (sif.open+sif.high)/2 - limit  #买入止损
    pss = (sif.open+sif.low)/2 + limit  #卖出止损
    sb2 = gand(rollx(sb,delayed),rollx(psb,delayed-1)<smin) #psb在信号的下一周期发生
    ss2 = gand(rollx(ss,delayed),rollx(pss,delayed-1)>smax)
    return np.select([sb2,ss2],[XBUY,XSELL],default=0)

def gothrough_filter(sif,signal,delayed=5,limit=60):
    ''' 直通
    '''
    return signal


def ocfilter(sif,tbegin=944,tend=1510):  #在开盘前30分钟和收盘前5分钟不开仓，头三个交易日不开张
    stime = sif.transaction[ITIME]
    soc = np.ones_like(stime)
    soc = gand(greater(stime,tbegin),lesser(stime,tend))
    soc[:275*3] = 0
    soc[-5:] = 0    #最后交易日收盘在1500，防止溢出(因为买入点通常在下一分钟，那么1500不被屏蔽的话，如果有信号就会溢出)
    
    return soc

ocfilter_c = fcustom(ocfilter,tbegin=930,tend=1455) #商品期货的交易时间为9:00-1500（中间有休息），故filter也修改
ocfilter_null = fcustom(ocfilter,tbegin=0,tend=2401)

def state_filter(sif,prefilter=ocfilter):
    soc = prefilter(sif)
    soc = gand(soc,sif.xstate!=0)
    return soc

def nstate_filter(sif,prefilter=ocfilter):
    soc = prefilter(sif)
    soc = gand(soc,sif.xstate==0)
    return soc


def last_filter(sif,tbegin=930,tend=1510):  
    stime = sif.transaction[ITIME]
    soc = np.ones_like(stime)
    soc = gand(greater(stime,tbegin),lesser(stime,tend))    
    soc[:275*3] = 0
    return soc

last_filter_c = fcustom(last_filter,tbegin=930,tend=1455)
ocfilter_orb = fcustom(ocfilter,tbegin=915,tend=1440) #orb 信号不受影响
ocfilter_k1s = fcustom(ocfilter,tbegin=929,tend=1500) #k1s 信号与隔日无关 


state_oc_filter = fcustom(state_filter,prefilter = ocfilter)
state_last_filter = fcustom(state_filter,prefilter = last_filter)
nstate_oc_filter = fcustom(nstate_filter,prefilter = ocfilter)
nstate_last_filter = fcustom(nstate_filter,prefilter = last_filter)

slast_filter_c = fcustom(state_filter,prefilter=last_filter_c)
nslast_filter_c = fcustom(nstate_filter,prefilter=last_filter_c)

socfilter = state_oc_filter
socfilter_orb = fcustom(state_filter,prefilter=ocfilter_orb) #orb 信号不受影响
socfilter_k1s = fcustom(state_filter,prefilter=ocfilter_k1s) #k1s 信号与隔日无关 

nsocfilter = nstate_oc_filter
nsocfilter_orb = fcustom(nstate_filter,prefilter=ocfilter_orb) #orb 信号不受影响
nsocfilter_k1s = fcustom(nstate_filter,prefilter=ocfilter_k1s) #k1s 信号与隔日无关 

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

def last_trades(actions,calc_profit=normal_profit,length=20):
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

def last_xactions(sif,trades,acstrategy=late_strategy):
    xactions = []
    for trade in trades:
        for action in trade.actions:
            action.functor = trade.functor
            action.trade = trade
            #func_name = str(action.functor)
            #action.fname = func_name[10:func_name.find(' at')]
            action.fname = func_name(action.functor)
        xactions.extend(trade.actions)
    xactions.sort(DTSORT)
    xactions.reverse() 
    for action in xactions:
        xposition = "long" if action.position==LONG else 'short'
        xaction = "open" if action.xtype == XOPEN else 'close'
        print u"name=%s,time=%s:%s,%s:%s,price=%s,priority=%s" % (action.name,action.date,action.time,xaction,xposition,action.price,fpriority(action.functor))
        #print 'action:',action.date,action.time,action.position,action.price

def last_wactions(sif,trades,acstrategy=late_strategy):
    xactions = []
    for trade in trades:
        for action in trade.actions:
            action.functor = trade.functor
            action.trade = trade
            #func_name = str(action.functor)
            #action.fname = func_name[10:func_name.find(' at')]
            action.fname = func_name(action.functor)            
        xactions.extend(trade.actions)
    xactions.sort(DTSORT)
    xactions.reverse() 
    return xactions

def simple_trades(actions,calc_profit=normal_profit):  #简单的trades,每个trade只有一次开仓和平仓
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
                #print u'忽略:',action.date,action.time,action.position,action.price
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
        opens.extend(open_position(sif,opener(sif),slongfilter,sshortfilter))  #开仓必须满足各自sfilter
    opens.sort(DTSORT)
    sopened = np.zeros(len(sif.transaction[IDATE]),int)   #为开仓价格序列,负数为开多仓,正数为开空仓
    for aopen in opens:
        sopened[aopen.index] = aopen.price * aopen.position
    for closer in closers:
        closes.extend(close_position(sif,closer(sif,sopened)))
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
        opens = open_position(sif,opener(sif),slongfilter,sshortfilter)  #开仓必须满足各自sfilter
        sopened = np.zeros(len(sif.transaction[IDATE]),int)   #为开仓价格序列,负数为开多仓,正数为开空仓
        for aopen in opens:
            sopened[aopen.index] = aopen.price * aopen.position
        closes = []
        for closer in closers:
            closes.extend(close_position(sif,closer(sif,sopened)))
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
        opens.extend(open_position(sif,opener(sif),slongfilter,sshortfilter))  #开仓必须满足各自sfilter
    opens.sort(DTSORT)
    sopened = np.zeros(len(sif.transaction[IDATE]),int)   #为开仓价格序列,负数为开多仓,正数为开空仓
    for aopen in opens:
        sopened[aopen.index] = aopen.price * aopen.position
    sbclose = np.zeros(len(sif.transaction[IDATE]),int)
    ssclose = np.zeros(len(sif.transaction[IDATE]),int)
    for closer in bclosers:
        #closes.extend(close_position(sif,closer(sif,sopened)))
        sbclose = gor(sbclose,closer(sif,sopened)) * XBUY
    for closer in sclosers:
        #closes.extend(close_position(sif,closer(sif,sopened)))
        ssclose = gor(ssclose,closer(sif,sopened)) * XSELL
    closes = close_position(sif,stop_closer(sif,sopened,sbclose,ssclose))
    actions = sorted(opens + closes,DTSORT)
    for action in actions:
        action.name = sif.name
    trades = make_trades(actions)   #trade: [open , close] 的序列, 其中前部分都是open,后部分都是close
    return trades

def null_sync_tradess(sif,tradess,acstrategy=late_strategy):
    xtrades = []
    for trades in tradess:
        xtrades.extend(trades)
    return xtrades


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
    cur_trade.orignal = cur_trade.functor   
    extended,filtered,rfiltered,reversed = [],[],[],[]
    close_action = cur_trade.actions[-1]
    #print '#####################first:',close_action.time
    while True:
        #print cur_trade.orignal
        trade = find_first(tradess)
        #print trade
        if trade == None:
            xtrades.append(close_trade(sif,cur_trade,close_action,extended,filtered,rfiltered,reversed))
            break
        #print 'find:date=%s,time=%s,functor=%s' % (trade.actions[0].date,trade.actions[0].time,trade.functor)  
        if DTSORT2(trade.actions[0],close_action)>0:  #时间超过
            #print u'时间超过'
            xtrades.append(close_trade(sif,cur_trade,close_action,extended,filtered,rfiltered,reversed))
            trade.orignal = trade.functor
            cur_trade = trade
            close_action = cur_trade.actions[-1]
            extended,filtered,rfiltered,reversed = [],[],[],[]
            #print cur_trade.orignal
            continue
           
        #print trade.functor,fpriority(trade.functor) ,cur_trade.functor,fpriority(cur_trade.functor)
        if fpriority(trade.functor) <= fpriority(cur_trade.functor):
            #print u'高/平优先级'   #后发的同优先级信号优先
            if trade.direction == cur_trade.direction:  #同向取代关系
                #print u'同向增强,%s|%s:%s被%s增强'%(cur_trade.functor,cur_trade.actions[0].date,cur_trade.actions[0].time,trade.functor)
                close_action = acstrategy(close_action,trade.actions[-1])
                extended.append(cur_trade)
                trade.orignal = cur_trade.orignal
                cur_trade = trade
            else:   #逆向平仓
                #print u'逆向平仓'
                reversed.append(trade)
                xindex = reversed[0].actions[0].index
                cposition = BaseObject(index=xindex,date=sdate[xindex],time=stime[xindex],position=reversed[0].direction,xtype=XCLOSE)    #因为已经抑制了1514开仓,必然不会溢出
                cposition.price = make_price(cposition.position,sopen[xindex],sclose[xindex],shigh[xindex],slow[xindex])
                xtrades.append(close_trade(sif,cur_trade,cposition,extended,filtered,rfiltered,reversed))
                trade.orignal = trade.functor
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


def sync_tradess_pt(sif,tradess,acstrategy=late_strategy):
    '''
        结合优先级和顺势逆势关系
        顺势信号可以逆反优先级小于等于它的逆势信号
        逆势信号不能逆反顺势信号
        低优先级顺势信号不能逆反高优先级顺势信号

    '''
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
    cur_trade.orignal = cur_trade.functor   
    extended,filtered,rfiltered,reversed = [],[],[],[]
    close_action = cur_trade.actions[-1]
    #print '#####################first:',close_action.time
    while True:
        #print cur_trade.orignal
        trade = find_first(tradess)
        if trade == None:
            xtrades.append(close_trade(sif,cur_trade,close_action,extended,filtered,rfiltered,reversed))
            break
        #print 'find:date=%s,time=%s,functor=%s,priority=%s' % (trade.actions[0].date,trade.actions[0].time,trade.functor,fpriority(trade.functor))  
        if DTSORT2(trade.actions[0],close_action)>0:  #时间超过
            #print u'时间超过'
            xtrades.append(close_trade(sif,cur_trade,close_action,extended,filtered,rfiltered,reversed))
            trade.orignal = trade.functor
            cur_trade = trade
            close_action = cur_trade.actions[-1]
            extended,filtered,rfiltered,reversed = [],[],[],[]
            #print cur_trade.orignal
            continue
           
        #print trade.functor,fpriority(trade.functor) ,cur_trade.functor,fpriority(cur_trade.functor)
        if fpriority(trade.functor) <= fpriority(cur_trade.functor) and (trade.actions[0].xfollow >= cur_trade.actions[0].xfollow):    #优先级优先且势优或平. 就是说优先级高但逆势也不能搞顺势，以及顺势低优也不能搞逆势
        #if trade.actions[0].xfollow > cur_trade.actions[0].xfollow or (trade.actions[0].xfollow == cur_trade.actions[0].xfollow and fpriority(trade.functor) <= fpriority(cur_trade.functor)): 
            #print u'顺势搞逆势，或高/平优先级'   #后发的同优先级信号优先
            #print u'xfollow1:%s,xfollow2:%s,time1:%s' % (trade.actions[0].xfollow,cur_trade.actions[0].xfollow,sif.time[trade.actions[0].index])
            if trade.direction == cur_trade.direction:  #同向取代关系
                #print u'同向增强,%s|%s:%s被%s增强'%(cur_trade.functor,cur_trade.actions[0].date,cur_trade.actions[0].time,trade.functor)
                close_action = acstrategy(close_action,trade.actions[-1])
                extended.append(cur_trade)
                trade.orignal = cur_trade.orignal
                cur_trade = trade
            else:   #逆向平仓
                #print u'逆向平仓'
                reversed.append(trade)
                xindex = reversed[0].actions[0].index
                cposition = BaseObject(index=xindex,date=sdate[xindex],time=stime[xindex],position=reversed[0].direction,xtype=XCLOSE)    #因为已经抑制了1514开仓,必然不会溢出
                cposition.price = make_price(cposition.position,sopen[xindex],sclose[xindex],shigh[xindex],slow[xindex])
                xtrades.append(close_trade(sif,cur_trade,cposition,extended,filtered,rfiltered,reversed))
                trade.orignal = trade.functor
                cur_trade = trade
                extended,filtered,rfiltered,reversed = [],[],[],[]
                close_action = cur_trade.actions[-1]                
        else:   #低优先级或逆势对顺势
            #print u'低优先级'
            if trade.direction == cur_trade.direction:  #同向屏蔽
                filtered.append(trade)
            else:   #逆向屏蔽
                rfiltered.append(trade)
    return xtrades

def sync_tradess_t(sif,tradess,acstrategy=late_strategy):
    '''
        不考虑优先级，只考虑顺逆势的取代关系
        效果并不好
    '''
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
    cur_trade.orignal = cur_trade.functor   
    extended,filtered,rfiltered,reversed = [],[],[],[]
    close_action = cur_trade.actions[-1]
    #print '#####################first:',close_action.time
    while True:
        #print cur_trade.orignal
        trade = find_first(tradess)
        #print trade
        if trade == None:
            xtrades.append(close_trade(sif,cur_trade,close_action,extended,filtered,rfiltered,reversed))
            break
        #print 'find:date=%s,time=%s,functor=%s' % (trade.actions[0].date,trade.actions[0].time,trade.functor)  
        if DTSORT2(trade.actions[0],close_action)>0:  #时间超过
            #print u'时间超过'
            xtrades.append(close_trade(sif,cur_trade,close_action,extended,filtered,rfiltered,reversed))
            trade.orignal = trade.functor
            cur_trade = trade
            close_action = cur_trade.actions[-1]
            extended,filtered,rfiltered,reversed = [],[],[],[]
            #print cur_trade.orignal
            continue
           
        #print trade.functor,fpriority(trade.functor) ,cur_trade.functor,fpriority(cur_trade.functor)
        if trade.actions[0].xfollow >= cur_trade.actions[0].xfollow:    #优先级优先且势优或平. 就是说优先级高但逆势也不能搞顺势，以及顺势低优也不能搞逆势
            #print u'顺势搞逆势，或高/平优先级'   #后发的同优先级信号优先
            if trade.direction == cur_trade.direction:  #同向取代关系
                #print u'同向增强,%s|%s:%s被%s增强'%(cur_trade.functor,cur_trade.actions[0].date,cur_trade.actions[0].time,trade.functor)
                close_action = acstrategy(close_action,trade.actions[-1])
                extended.append(cur_trade)
                trade.orignal = cur_trade.orignal
                cur_trade = trade
            else:   #逆向平仓
                #print u'逆向平仓'
                reversed.append(trade)
                xindex = reversed[0].actions[0].index
                cposition = BaseObject(index=xindex,date=sdate[xindex],time=stime[xindex],position=reversed[0].direction,xtype=XCLOSE)    #因为已经抑制了1514开仓,必然不会溢出
                cposition.price = make_price(cposition.position,sopen[xindex],sclose[xindex],shigh[xindex],slow[xindex])
                xtrades.append(close_trade(sif,cur_trade,cposition,extended,filtered,rfiltered,reversed))
                trade.orignal = trade.functor
                cur_trade = trade
                extended,filtered,rfiltered,reversed = [],[],[],[]
                close_action = cur_trade.actions[-1]                
        else:   #逆势对顺势
            #print u'逆势不能取代顺势'
            if trade.direction == cur_trade.direction:  #同向屏蔽
                filtered.append(trade)
            else:   #逆向屏蔽
                rfiltered.append(trade)
    return xtrades

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
            ,sync_trades=sync_tradess_pt    #汇总各opener得到的交易，计算优先级和平仓。
                                            #对于最后交易序列，用null_sync_tradess
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
    
    openers = [opener for opener in openers if fpriority(opener)<priority_level]

    tradess = []
    for opener in openers:
        if 'filter' not in opener.__dict__: #用于对信号进行过滤,如开盘30分钟内不发出信号等
            myfilter = slongfilter if fdirection(opener) == XBUY else sshortfilter
        else:
            myfilter = opener.filter(sif)
        if 'xfilter' not in opener.__dict__:    #xfilter用于自定义的信号变换,如根据5分钟内的波动决定延迟发送还是吞没
            xfilter = gothrough_filter
        else:
            xfilter = opener.xfilter
        opens = open_position(sif,xfilter(sif,opener(sif)),myfilter,myfilter) #因为opener只返回一个方向的操作,所以两边都用myfilter，但实际上只有相应的一个有效，另一个是虚的
        #opens.sort(DTSORT)
        sopened = np.zeros(len(sif.transaction[IDATE]),int)   #为开仓价格序列,负数为开多仓,正数为开空仓
        for aopen in opens:
            sopened[aopen.index] = aopen.price * aopen.position
        sclose = np.zeros(len(sif.transaction[IDATE]),int)
        if 'closer' in opener.__dict__: #是否有特定的closer,如要将macd下叉也作为多头持仓的平仓条件,则可设置函数,在返回值中添加该下叉信号算法
            if fdirection(opener) == XBUY:
                #print 'buy closer:',opener.closer
                closers = opener.closer(sclosers)
            elif fdirection(opener) == XSELL:
                closers = opener.closer(bclosers)
        else:
            #print 'opener without close fdirection(opener) = %s' % ('XBUY' if fdirection(opener) == XBUY else 'XSELL',)
            closers = sclosers if fdirection(opener) == XBUY else bclosers
        for closer in closers:
            sclose = gor(sclose,closer(sif,sopened)) * (-fdirection(opener))
        ms_closer = stop_closer if 'stop_closer' not in opener.__dict__ else opener.stop_closer
        #closes = close_position(sif,stop_closer(sif,sopened,sclose,sclose)) #因为是单向的，只有一个sclose起作用
        closes = close_position(sif,ms_closer(sif,sopened,sclose,sclose)) #因为是单向的，只有一个sclose起作用        
        actions = sorted(opens + closes,DTSORT)
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

itradez = fcustom(itradex,longfilter = state_oc_filter,shortfilter = state_oc_filter)

def close_trade(sif,cur_trade,close_action,extended,filtered,rfiltered,reversed,calc_profit=normal_profit):
    open_action = extended[0].actions[0] if extended else cur_trade.actions[0]
    trade = BaseObject(actions=[open_action,close_action])
    trade.profit = calc_profit(trade.actions)
    trade.extended = extended
    trade.filtered = filtered
    trade.rfiltered = rfiltered
    trade.reversed = reversed
    trade.functor = cur_trade.functor
    trade.orignal = cur_trade.orignal
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


def open_position(sif,sopener,slongfilter,sshortfilter):
    '''
        sopener中,XBUY表示开多仓,XSELL表示开空仓
    '''
    trans = sif.transaction
    slong = band(equals(sopener,XBUY),slongfilter) * LONG 
    #print slongfilter[-10:],sshortfilter[-10:]
    sshort = band(equals(sopener,XSELL),sshortfilter) * SHORT
    #ss = slong + sshort #多空抵消
    positions = xposition(sif,slong,XOPEN)
    positions.extend(xposition(sif,sshort,XOPEN))
    return positions

def close_position(sif,scloser):
    ''' scloser中, XBUY表示平空(买入),XSELL表示平多(卖出)
    '''
    trans = sif.transaction
    #print scloser[scloser.nonzero()]
    slong = equals(scloser,XBUY) * LONG  #避免直接将scloser中的信号表示与LONG/SHORT隐蔽耦合
    #print slong[slong.nonzero()]
    sshort = equals(scloser,XSELL) * SHORT
    #print sshort[sshort.nonzero()],SHORT
    positions = xposition(sif,slong,XCLOSE)
    positions.extend(xposition(sif,sshort,XCLOSE))
    return positions

def xposition(sif,saction,xtype,defer=1):
    trans = sif.transaction
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
        if xtype == XOPEN:
            position.xfollow = True if (sif.sxtrend[i] == TREND_UP and saction[i] == LONG) or (sif.sxtrend[i] == TREND_DOWN and saction[i] == SHORT) else False
            #print position.xfollow
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
    mdate = 20100401
    for trade in trades:
        tdate = trade.actions[-1].date
        if tdate > datefrom and tdate < dateto: #忽略掉小于开始时间的
            if trade.profit > 0:
                curs = 0
            else:
                curs += trade.profit   #本为负数
                if curs < smax:
                    smax = curs
                    mdate = trade.actions[0].date
            if trade.profit < max1:
                max1 = trade.profit
    return smax,max1,mdate

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

def atr_uxstop(sif,sopened
        ,sbclose
        ,ssclose
        ,lost_times=200
        ,win_times=300
        ,max_drawdown=200
        ,min_drawdown=120
        ,min_lost=30
        ,max_lost=60
        ,natr=1):
    '''
        atr止损
        sif为实体
        sopen为价格序列，其中负数表示开多仓，正数表示开空仓
        sbclose是价格无关序列所发出的买入平仓信号集合(平空仓)
        ssclose是价格无关序列所发出的卖出平仓信号集合(平多仓)
        max_drawdown: 从最高点起的最大回落
        min_drawdown: 从最高点起的最小回落
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
    will_losts = []
    for i in isignal:
        price = sopened[i]
        willlost = satr[i] * lost_times / XBASE / XBASE
        #print willlost
        if willlost < min_lost:
            willlost = min_lost
        if willlost > max_lost:
            willlost = max_lost
        will_losts.append(willlost)
        if i < ilong_closed or i<ishort_closed:    #已经开了仓，且未平，不再计算            
            #print 'skiped',trans[IDATE][i],trans[ITIME][i],trans[IDATE][ilong_closed],trans[ITIME][ilong_closed],trans[IDATE][ishort_closed],trans[ITIME][ishort_closed]
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
            #print 'stop init:',cur_stop,lost_stop,willlost,min_lost,max_lost
            if ssclose[i] == XSELL:
                #print 'sell signali:',trans[IDATE][i],trans[ITIME][i],trans[ICLOSE][i]
                pass
            if trans[ICLOSE][i] < cur_stop or ssclose[i] == XSELL:#到达止损或平仓
                #print '----sell----------:',trans[IDATE][i],trans[ITIME][i],cur_stop,trans[ICLOSE][i],cur_high,lost_stop
                ilong_closed = i
                rev[i] = XSELL            
            else:
                for j in range(i+1,len(rev)):
                    if ssclose[j] == XSELL:
                        #print 'sell signalj:',trans[IDATE][j],trans[ITIME][j],cur_stop,trans[ICLOSE][j]
                        pass
                    #print trans[ITIME][j],buy_price,lost_stop,cur_high,win_stop,cur_stop,trans[ILOW][j],satr[j]
                    if trans[ILOW][j] < cur_stop or ssclose[j] == XSELL:    #
                        rev[j] = XSELL
                        #print 'sell:',i,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j],sif.low[j],cur_stop
                        ilong_closed = j
                        break
                    nhigh = trans[IHIGH][j]
                    if(nhigh > cur_high):
                        cur_high = nhigh
                        drawdown = satr[j] * win_times / XBASE / XBASE
                        if drawdown > max_drawdown:
                            drawdown = max_drawdown
                        if drawdown < min_drawdown:
                            drawdown = min_drawdown
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
                #print 'buy signali:',trans[IDATE][i],trans[ITIME][i],trans[ICLOSE][i]
                pass
            if trans[ICLOSE][i] > cur_stop or sbclose[i] == XBUY:
                #print '----buy----------:',cur_stop,trans[ICLOSE][i],cur_high,lost_stop
                ishort_closed = i
                rev[i] = XBUY
            else:
                for j in range(i+1,len(rev)):
                    if sbclose[j] == XBUY:
                        #print 'buy signalj:',trans[IDATE][j],trans[ITIME][j],cur_stop,trans[ICLOSE][j]
                        pass
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
                        if drawdown < min_drawdown:
                            drawdown = min_drawdown
                        win_stop = cur_low + drawdown
                        #print nlow,cur_stop,win_stop,satr[j]
                        #win_stop = cur_low + satr[j] * win_times / XBASE / XBASE
                        if cur_stop > win_stop:
                            cur_stop = win_stop
    #print will_losts
    return rev


def atr_uxstop_t(sif,sopened    
        ,sbclose
        ,ssclose
        ,lost_times=200
        ,win_times=300
        ,max_drawdown=200
        ,min_drawdown=120
        ,min_lost_follow=60
        ,min_lost_against=30
        ,max_lost_follow = 90   #顺势时的止损
        ,max_lost_against = 60   #顺势时的止损
        ,protected_trigger = 300    #保护性止损触发点,300相当于无保护性止损. 即只有最初止损和跟踪止损
        ,protected_v = 0    #保护性止损位
        ,natr=1):
    '''
        考虑到顺势逆势介入时的止损。目前只修改初始止损
        atr止损
        sif为实体
        sopen为价格序列，其中负数表示开多仓，正数表示开空仓
        sbclose是价格无关序列所发出的买入平仓信号集合(平空仓)
        ssclose是价格无关序列所发出的卖出平仓信号集合(平多仓)
        max_drawdown: 从最高点起的最大回落
        min_drawdown: 从最高点起的最小回落
        min_lost_follow: 顺势最小止损
        min_lost_against: 逆势最小止损
        max_lost_follow: 顺势最大止损
        max_lost_against: 逆势最大止损
        只能持有一张合约。即当前合约在未平前会屏蔽掉所有其它开仓
    '''
    #print sbclose[-10:],ssclose[-10:]
    satr = afm[natr](sif)
    trans = sif.transaction
    rev = np.zeros_like(sopened)
    isignal = np.nonzero(sopened)[0]
    ilong_closed = 0    #多头平仓日
    ishort_closed = 0   #空头平仓日
    will_losts = []
    for i in isignal:
        price = sopened[i]
        willlost = satr[i] * lost_times / XBASE / XBASE
        if (sif.sxtrend[i] == TREND_UP and price <0) or (sif.sxtrend[i] == TREND_DOWN and price >0):
            #顺势就是最大止损
            if willlost < min_lost_follow:
                willlost = min_lost_follow
            if willlost > max_lost_follow:
                willlost = max_lost_follow
            #print u'顺势:',sif.sxtrend[i],price
        else:
            #逆势计算
            #print u'逆势:',sif.sxtrend[i],price
            if willlost < min_lost_against:
                willlost = min_lost_against
            if willlost > max_lost_against:
                willlost = max_lost_against
            #print u'逆势,willlost=%s' %(willlost,)
        will_losts.append(willlost)            
        if i < ilong_closed or i<ishort_closed:    #已经开了仓，且未平，不再计算            
            #print 'skiped',trans[IDATE][i],trans[ITIME][i],trans[IDATE][ilong_closed],trans[ITIME][ilong_closed],trans[IDATE][ishort_closed],trans[ITIME][ishort_closed]
            continue
        if price<0: #多头止损
            #print 'find long stop:',i
            #if i < ilong_closed:    #已经开了多头仓，且未平，不再计算
            #    print 'skiped',trans[IDATE][i],trans[ITIME][i],trans[IDATE][ilong_closed],trans[ITIME][ilong_closed]
            #    continue
            buy_price = -price
            lost_stop = buy_price - willlost
            cur_high = max(buy_price,trans[ICLOSE][i])
            drawdown = satr[i] * win_times / XBASE / XBASE
            if drawdown > max_drawdown:
                drawdown = max_drawdown
            if drawdown < min_drawdown:
                drawdown = min_drawdown
            win_stop = cur_high - drawdown
            cur_stop = lost_stop if lost_stop > win_stop else win_stop
            #print 'stop init:',cur_stop,lost_stop,willlost,min_lost,my_max_lost
            if ssclose[i] == XSELL:
                #print 'sell signali:',trans[IDATE][i],trans[ITIME][i],trans[ICLOSE][i]
                pass
            if trans[ICLOSE][i] < cur_stop or ssclose[i] == XSELL:#到达止损或平仓
                #print '----sell----------:',trans[IDATE][i],trans[ITIME][i],cur_stop,trans[ICLOSE][i],cur_high,lost_stop
                ilong_closed = i
                rev[i] = XSELL            
            else:
                for j in range(i+1,len(rev)):
                    if ssclose[j] == XSELL:
                        #print 'sell signalj:',trans[IDATE][j],trans[ITIME][j],cur_stop,trans[ICLOSE][j]
                        pass
                    #print trans[ITIME][j],buy_price,lost_stop,cur_high,win_stop,cur_stop,trans[ILOW][j],satr[j]
                    if trans[ILOW][j] < cur_stop or ssclose[j] == XSELL:    #
                        rev[j] = XSELL
                        #print 'sell:',i,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j],sif.low[j],cur_stop
                        ilong_closed = j
                        break
                    nhigh = trans[IHIGH][j]
                    #计算保护性止损
                    if(nhigh >= buy_price + protected_trigger and cur_stop < buy_price + protected_v):
                        cur_stop = buy_price + protected_v
                    #计算新高止损
                    if(nhigh > cur_high):
                        cur_high = nhigh
                        drawdown = satr[j] * win_times / XBASE / XBASE
                        if drawdown > max_drawdown:
                            drawdown = max_drawdown
                        if drawdown < min_drawdown:
                            drawdown = min_drawdown
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
            drawdown = satr[i] * win_times / XBASE / XBASE
            if drawdown > max_drawdown:
                drawdown = max_drawdown
            if drawdown < min_drawdown:
                drawdown = min_drawdown
            win_stop = cur_low + drawdown
            cur_stop = lost_stop if lost_stop < win_stop else win_stop
            #print u'空头初始止损位: %s, 开仓价位:%s:, 开仓收盘位:%s' % (cur_stop,sell_price,sif.close[i])
            if sbclose[i] == XBUY:
                #print 'buy signali:',trans[IDATE][i],trans[ITIME][i],trans[ICLOSE][i]
                pass
            if trans[ICLOSE][i] > cur_stop or sbclose[i] == XBUY:
                #print '----buy----------:',cur_stop,trans[ICLOSE][i],cur_high,lost_stop
                ishort_closed = i
                rev[i] = XBUY
            else:
                for j in range(i+1,len(rev)):
                    if sbclose[j] == XBUY:
                        #print 'buy signalj:',trans[IDATE][j],trans[ITIME][j],cur_stop,trans[ICLOSE][j]
                        pass
                    #print trans[ITIME][j],sell_price,lost_stop,cur_low,win_stop,cur_stop,trans[IHIGH][j],satr[j]                
                    if trans[IHIGH][j] > cur_stop or sbclose[j] == XBUY:#
                        ishort_closed = j
                        rev[j] = XBUY
                        #print 'buy:',j
                        #print 'buy:',i,price,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j]                        
                        break
                    nlow = trans[ILOW][j]
                    #计算保护性止损
                    if(nlow <= sell_price - protected_trigger and cur_stop > sell_price - protected_v):
                        cur_stop = sell_price - protected_v
                    if(nlow < cur_low):
                        cur_low = nlow
                        drawdown = satr[j] * win_times / XBASE / XBASE
                        if drawdown > max_drawdown:
                            drawdown = max_drawdown
                        if drawdown < min_drawdown:
                            drawdown = min_drawdown
                        win_stop = cur_low + drawdown
                        #print nlow,cur_stop,win_stop,satr[j]
                        #win_stop = cur_low + satr[j] * win_times / XBASE / XBASE
                        if cur_stop > win_stop:
                            cur_stop = win_stop
    #print will_losts
    return rev


#FBASE_30 = lambda bpoint:30 + (bpoint + 5000) / 5000 * 10  #基准3点，以后每上500点加1点. /5000 * 10是为了向.5取整
#F60_15 = lambda bpoint:60 + (bpoint+5000) / 5000 * 10 * 3/2  #基准6点，以后每上500点加1.5点
#F100_25 = lambda bpoint:100 + (bpoint+5000) / 5000 * 10 * 5/2 #基准10点，以后每上500点加2.5点

#FBASE_30 = lambda bpoint:10 + (bpoint+4000) / 4000 * 10  #基准1点，以后每上500点加1点. /5000 * 10是为了向.5取整
#F60_15 = lambda bpoint:30 + (bpoint+4000) / 4000 * 10 * 3/2  #基准3点，以后每上500点加1.5点
#F100_25 = lambda bpoint:90 + (bpoint+4000) / 4000 * 10 * 2 #基准10点，以后每上500点加2.5点

#最简化的方式
FBASE_30 = lambda bpoint: 100 if bpoint < 30000 else 100
F60_15 = lambda bpoint: 150 if bpoint < 30000 else 150
F100_25 = lambda bpoint: 250 if bpoint < 30000 else 250

def atr_uxstop_f(sif,sopened
        ,sbclose
        ,ssclose
        ,flost_base = FBASE_30    #flost:买入点数 --> 止损点数
        ,fmax_drawdown = F100_25 #fdmax:买入点数 --> 最大回落
        ,fmin_drawdown = F60_15#fdmin:买入点数 --> 最小回落
        ,win_times=300        
        ,natr=1):
    '''
        利用函数来确定止损. 实际上为按开仓价格比例止损
        atr止损
        sif为实体
        sopen为价格序列，其中负数表示开多仓，正数表示开空仓
        sbclose是价格无关序列所发出的买入平仓信号集合(平空仓)
        ssclose是价格无关序列所发出的卖出平仓信号集合(平多仓)
        flost_base为初始止损函数
        win_times: 与ATR的乘积，来计算跟踪止损（盈）,如果在[fmin_drawdown(buy_point):fmax_drowdown(buy_point)]之外
            则取端点值
        fmax_drawdown: 确定从最高点起的最大回落点数的函数
        fmin_drawdown: 确定从最高点起的最小回落点数的函数
        只能持有一张合约。即当前合约在未平前会屏蔽掉所有其它开仓
    '''
    #print sbclose[-10:],ssclose[-10:]
    satr = afm[natr](sif)
    trans = sif.transaction
    rev = np.zeros_like(sopened)
    isignal = np.nonzero(sopened)[0]
    ilong_closed = 0    #多头平仓日
    ishort_closed = 0   #空头平仓日
    will_losts = []
    for i in isignal:
        price = sopened[i]
        aprice = abs(price)
        willlost = flost_base(aprice)
        max_drawdown = fmax_drawdown(aprice)
        min_drawdown = fmin_drawdown(aprice)
        #print price,willlost,max_drawdown,min_drawdown
        will_losts.append(willlost)
        if i < ilong_closed or i<ishort_closed:    #已经开了仓，且未平，不再计算            
            #print 'skiped',trans[IDATE][i],trans[ITIME][i],trans[IDATE][ilong_closed],trans[ITIME][ilong_closed],trans[IDATE][ishort_closed],trans[ITIME][ishort_closed]
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
            #print 'stop init:',cur_stop,lost_stop,willlost,min_lost,max_lost
            if ssclose[i] == XSELL:
                #print 'sell signali:',trans[IDATE][i],trans[ITIME][i],trans[ICLOSE][i]
                pass
            if trans[ICLOSE][i] < cur_stop or ssclose[i] == XSELL:#到达止损或平仓
                #print '----sell----------:',trans[IDATE][i],trans[ITIME][i],cur_stop,trans[ICLOSE][i],cur_high,lost_stop
                ilong_closed = i
                rev[i] = XSELL            
            else:
                for j in range(i+1,len(rev)):
                    if ssclose[j] == XSELL:
                        #print 'sell signalj:',trans[IDATE][j],trans[ITIME][j],cur_stop,trans[ICLOSE][j]
                        pass
                    #print trans[ITIME][j],buy_price,lost_stop,cur_high,win_stop,cur_stop,trans[ILOW][j],satr[j]
                    if trans[ILOW][j] < cur_stop or ssclose[j] == XSELL:    #
                        rev[j] = XSELL
                        #print 'sell:',i,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j],sif.low[j],cur_stop
                        ilong_closed = j
                        break
                    nhigh = trans[IHIGH][j]
                    if(nhigh > cur_high):
                        cur_high = nhigh
                        drawdown = satr[j] * win_times / XBASE / XBASE
                        if drawdown > max_drawdown:
                            drawdown = max_drawdown
                        if drawdown < min_drawdown:
                            drawdown = min_drawdown
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
                #print 'buy signali:',trans[IDATE][i],trans[ITIME][i],trans[ICLOSE][i]
                pass
            if trans[ICLOSE][i] > cur_stop or sbclose[i] == XBUY:
                #print '----buy----------:',cur_stop,trans[ICLOSE][i],cur_high,lost_stop
                ishort_closed = i
                rev[i] = XBUY
            else:
                for j in range(i+1,len(rev)):
                    if sbclose[j] == XBUY:
                        #print 'buy signalj:',trans[IDATE][j],trans[ITIME][j],cur_stop,trans[ICLOSE][j]
                        pass
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
                        if drawdown < min_drawdown:
                            drawdown = min_drawdown
                        win_stop = cur_low + drawdown
                        #print nlow,cur_stop,win_stop,satr[j]
                        #win_stop = cur_low + satr[j] * win_times / XBASE / XBASE
                        if cur_stop > win_stop:
                            cur_stop = win_stop
    #print will_losts
    return rev


FKEEP_30 = lambda bpoint: 120   #上升12点后就保证开仓价格
FTARGET = lambda bpoint:10000   #相当于无穷大
#设定保证
def atr_uxstop_k(sif,sopened
        ,sbclose
        ,ssclose
        ,flost_base = FBASE_30    #flost:买入点数 --> 止损点数
        ,fmax_drawdown = F100_25 #fdmax:买入点数 --> 最大回落
        ,fmin_drawdown = F60_15#fdmin:买入点数 --> 最小回落
        ,fkeeper = FKEEP_30 #买入点数-->固定移动止损，移动到价格为止
        ,win_times=300        
        ,ftarget = FTARGET #盈利目标,默认是无穷大
        ,natr=1
        ):
    '''
        利用函数来确定止损. 实际上为按开仓价格比例止损
        atr止损
        sif为实体
        sopen为价格序列，其中负数表示开多仓，正数表示开空仓
        sbclose是价格无关序列所发出的买入平仓信号集合(平空仓)
        ssclose是价格无关序列所发出的卖出平仓信号集合(平多仓)
        flost_base为初始止损函数
        win_times: 与ATR的乘积，来计算跟踪止损（盈）,如果在[fmin_drawdown(buy_point):fmax_drowdown(buy_point)]之外
            则取端点值
        fmax_drawdown: 确定从最高点起的最大回落点数的函数
        fmin_drawdown: 确定从最高点起的最小回落点数的函数
        只能持有一张合约。即当前合约在未平前会屏蔽掉所有其它开仓
    '''
    #print sbclose[-10:],ssclose[-10:]
    satr = afm[natr](sif)
    trans = sif.transaction
    rev = np.zeros_like(sopened)
    isignal = np.nonzero(sopened)[0]
    ilong_closed = 0    #多头平仓日
    ishort_closed = 0   #空头平仓日
    will_losts = []
    #print target
    for i in isignal:
        price = sopened[i]
        aprice = abs(price)
        willlost = flost_base(aprice)
        max_drawdown = fmax_drawdown(aprice)
        min_drawdown = fmin_drawdown(aprice)
        keeper = fkeeper(aprice)
        #print price,willlost,max_drawdown,min_drawdown
        will_losts.append(willlost)
        if i < ilong_closed or i<ishort_closed:    #已经开了仓，且未平，不再计算            
            #print 'skiped',trans[IDATE][i],trans[ITIME][i],trans[IDATE][ilong_closed],trans[ITIME][ilong_closed],trans[IDATE][ishort_closed],trans[ITIME][ishort_closed]
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
            wtarget = buy_price + ftarget(buy_price)
            #print 'wtarget:%s',wtarget
            #print 'stop init:',cur_stop,lost_stop,willlost,min_lost,max_lost
            if ssclose[i] == XSELL:
                #print 'sell signali:',trans[IDATE][i],trans[ITIME][i],trans[ICLOSE][i]
                pass
            if trans[ICLOSE][i] < cur_stop or ssclose[i] == XSELL:#到达止损或平仓
                #print '----sell----------:',trans[IDATE][i],trans[ITIME][i],cur_stop,trans[ICLOSE][i],cur_high,lost_stop
                ilong_closed = i
                rev[i] = XSELL            
            else:
                for j in range(i+1,len(rev)):
                    if ssclose[j] == XSELL:
                        #print 'sell signalj:',trans[IDATE][j],trans[ITIME][j],cur_stop,trans[ICLOSE][j]
                        pass
                    #print trans[ITIME][j],buy_price,lost_stop,cur_high,win_stop,cur_stop,trans[ILOW][j],satr[j]
                    if trans[ILOW][j] < cur_stop or ssclose[j] == XSELL:    #
                        rev[j] = XSELL
                        #print 'sell:',i,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j],sif.low[j],cur_stop
                        ilong_closed = j
                        break
                    if trans[IHIGH][j] > wtarget:
                        rev[j] = XSELL
                        # print 'sell at target:',i,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j],sif.low[j],cur_stop
                        ilong_closed = j                        
                        break
                    nhigh = trans[IHIGH][j]
                    if(nhigh > cur_high):
                        cur_high = nhigh
                        drawdown = satr[j] * win_times / XBASE / XBASE
                        if drawdown > max_drawdown:
                            drawdown = max_drawdown
                        if drawdown < min_drawdown:
                            drawdown = min_drawdown
                        win_stop = cur_high - drawdown
                        #win_stop = cur_high - satr[j] * win_times / XBASE
                        #print nhigh,cur_stop,win_stop,satr[j]
                        if cur_stop < win_stop:
                            cur_stop = win_stop
                        keep_stop = cur_high - keeper
                        if cur_stop < buy_price and keep_stop > buy_price:  #一次跳变
                            cur_stop = buy_price 
                        #if cur_stop < keep_stop:
                        #    cur_stop = keep_stop if keep_stop < buy_price else buy_price
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
            wtarget = sell_price - ftarget(sell_price)
            if sbclose[i] == XBUY:
                #print 'buy signali:',trans[IDATE][i],trans[ITIME][i],trans[ICLOSE][i]
                pass
            if trans[ICLOSE][i] > cur_stop or sbclose[i] == XBUY:
                #print '----buy----------:',cur_stop,trans[ICLOSE][i],cur_high,lost_stop
                ishort_closed = i
                rev[i] = XBUY
            else:
                for j in range(i+1,len(rev)):
                    if sbclose[j] == XBUY:
                        #print 'buy signalj:',trans[IDATE][j],trans[ITIME][j],cur_stop,trans[ICLOSE][j]
                        pass
                    #print trans[ITIME][j],sell_price,lost_stop,cur_low,win_stop,cur_stop,trans[IHIGH][j],satr[j]                
                    if trans[IHIGH][j] > cur_stop or sbclose[j] == XBUY:#
                        ishort_closed = j
                        rev[j] = XBUY
                        #print 'buy:',j
                        #print 'buy:',i,price,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j]                        
                        break
                    if trans[ILOW][j] < wtarget:#
                        ishort_closed = j
                        rev[j] = XBUY
                        #print 'buy at target:',i,price,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j]                        
                        break
                    nlow = trans[ILOW][j]
                    if(nlow < cur_low):
                        cur_low = nlow
                        drawdown = satr[j] * win_times / XBASE / XBASE
                        if drawdown > max_drawdown:
                            drawdown = max_drawdown
                        if drawdown < min_drawdown:
                            drawdown = min_drawdown
                        win_stop = cur_low + drawdown
                        #print nlow,cur_stop,win_stop,satr[j]
                        #win_stop = cur_low + satr[j] * win_times / XBASE / XBASE
                        if cur_stop > win_stop:
                            cur_stop = win_stop
                        keep_stop = cur_low + keeper
                        if cur_stop > sell_price and keep_stop < sell_price:
                            cur_stop = sell_price 
                        #if cur_stop > keep_stop:
                        #    cur_stop = keep_stop if keep_stop > sell_price else sell_price
                        
                            
    #print will_losts
    return rev

def atr_rxstop(sif
        ,sopened
        ,sbclose
        ,ssclose
        ,lost_times=200
        ,win_times=300
        ,max_drawdown=90
        ,min_lost=30
        ,max_lost=70
        ,natr=1):
    '''
        atr止损
        sif为实体
        sopen为价格序列，其中负数表示开多仓，正数表示开空仓
        sbclose是价格无关序列所发出的买入平仓信号集合(平空仓)
        ssclose是价格无关序列所发出的卖出平仓信号集合(平多仓)
        max_drawdown: 从最高点起的最大回落比例，为万分之数
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
        cdrawdown = abs(price * max_drawdown / 10000)
        willlost = satr[i] * lost_times / XBASE / XBASE
        if willlost < min_lost:
            willlost = min_lost
        if willlost > max_lost:
            willlost = max_lost
        if i < ilong_closed or i<ishort_closed:    #已经开了仓，且未平，不再计算            
            #print 'skiped',trans[IDATE][i],trans[ITIME][i],trans[IDATE][ilong_closed],trans[ITIME][ilong_closed],trans[IDATE][ishort_closed],trans[ITIME][ishort_closed]
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
                        #print 'sell signalj:',trans[IDATE][j],trans[ITIME][j],cur_stop,trans[ICLOSE][j]
                        pass
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
                        if drawdown > cdrawdown:
                            drawdown = cdrawdown
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
                #print 'buy signali:',trans[IDATE][i],trans[ITIME][i],trans[ICLOSE][i]
                pass
            if trans[ICLOSE][i] > cur_stop or sbclose[i] == XBUY:
                #print '----buy----------:',cur_stop,trans[ICLOSE][i],cur_high,lost_stop
                ishort_closed = i
                rev[i] = XBUY
            else:
                for j in range(i+1,len(rev)):
                    if sbclose[j] == XBUY:
                        #print 'buy signalj:',trans[IDATE][j],trans[ITIME][j],cur_stop,trans[ICLOSE][j]
                        pass
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
                        if drawdown > cdrawdown:
                            drawdown = cdrawdown
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
atr5_uxstop_2_3 = fcustom(atr_uxstop,lost_times=200,win_times=300,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_25_4 = fcustom(atr_uxstop,lost_times=250,win_times=400,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_25_6 = fcustom(atr_uxstop,lost_times=250,win_times=600,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_2_4 = fcustom(atr_uxstop,lost_times=200,win_times=400,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_3_4 = fcustom(atr_uxstop,lost_times=300,win_times=400,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_15_4 = fcustom(atr_uxstop,lost_times=150,win_times=400,max_drawdown=200,min_lost=30,natr=5)    
atr5_uxstop_1_4 = fcustom(atr_uxstop,lost_times=100,win_times=400,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_05_4 = fcustom(atr_uxstop,lost_times=50,win_times=400,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_1_5 = fcustom(atr_uxstop,lost_times=100,win_times=500,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_05_20 = fcustom(atr_uxstop,lost_times=50,win_times=200,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_05_25 = fcustom(atr_uxstop,lost_times=50,win_times=250,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_03_25 = fcustom(atr_uxstop,lost_times=30,win_times=250,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_06_25 = fcustom(atr_uxstop,lost_times=66,win_times=250,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_07_25 = fcustom(atr_uxstop,lost_times=75,win_times=250,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_08_25 = fcustom(atr_uxstop,lost_times=80,win_times=250,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_15_25 = fcustom(atr_uxstop,lost_times=150,win_times=250,max_drawdown=200,min_lost=30,max_lost=90,natr=5)
atr5_uxstop_12_25 = fcustom(atr_uxstop,lost_times=125,win_times=250,max_drawdown=200,min_lost=30,max_lost=90,natr=5)
atr5_uxstop_20_25 = fcustom(atr_uxstop,lost_times=200,win_times=250,max_drawdown=200,min_lost=30,max_lost=150,natr=5)

atr5_uxstop_08_25_A = fcustom(atr_uxstop,lost_times=80,win_times=250,max_drawdown=200,min_lost=90,max_lost=90,natr=5)
atr5_uxstop_08_25_B = fcustom(atr_uxstop,lost_times=80,win_times=250,max_drawdown=200,min_lost=60,max_lost=60,natr=5)

atr5_uxstop_05_25_A = fcustom(atr_uxstop,lost_times=50,win_times=250,max_drawdown=200,min_lost=30,max_lost=30,natr=5)

atr5_uxstop_T1 = fcustom(atr_uxstop,lost_times=80,win_times=250,max_drawdown=200,min_lost=90,max_lost=90,natr=5)

atr5_uxstop_08_25_C = fcustom(atr_uxstop,lost_times=80,win_times=250,max_drawdown=200,min_drawdown=135,min_lost=90,max_lost=90,natr=5)
atr5_uxstop_08_25_D = fcustom(atr_uxstop,lost_times=80,win_times=250,max_drawdown=200,min_drawdown=200,min_lost=90,max_lost=90,natr=5)

atr5_uxstop_t_08_25 = fcustom(atr_uxstop_t,lost_times=80,win_times=250,max_drawdown=200,natr=5)
atr5_uxstop_t_08_25_A = fcustom(atr_uxstop_t,lost_times=80,win_times=250,max_drawdown=200,min_lost_follow=90,min_lost_against=60,max_lost_follow=90,max_lost_against=60,natr=5) ###??### 不如60到底


###使用固定的90止损
atr5_uxstop_t_08_25_B = fcustom(atr_uxstop_t,lost_times=80,win_times=250,max_drawdown=200,min_lost_follow=90,min_lost_against=90,max_lost_follow=90,max_lost_against=90,natr=5)  #累计收益最大，但R不是. 但胜率提高

atr5_uxstop_t_08_25_B20 = fcustom(atr_uxstop_t,lost_times=80,win_times=250,max_drawdown=200,min_drawdown=150,min_lost_follow=90,min_lost_against=90,max_lost_follow=90,max_lost_against=90,natr=5)  


###使用90-150-250的止损, 9点初始止损，15点最小跟踪止损，25点最大跟踪止损
atr5_uxstop_t_08_25_B2 = fcustom(atr_uxstop_t,lost_times=80,win_times=250,max_drawdown=250,min_drawdown=150,min_lost_follow=90,min_lost_against=90,max_lost_follow=90,max_lost_against=90,natr=5)  
atr5_uxstop_t_08_25_B27 = fcustom(atr_uxstop_t,lost_times=80,win_times=250,max_drawdown=270,min_drawdown=150,min_lost_follow=90,min_lost_against=90,max_lost_follow=90,max_lost_against=90,natr=5)  
atr5_uxstop_t_08_25_B30 = fcustom(atr_uxstop_t,lost_times=80,win_times=250,max_drawdown=300,min_drawdown=150,min_lost_follow=90,min_lost_against=90,max_lost_follow=90,max_lost_against=90,natr=5)  
atr5_uxstop_t_08_25_B26 = fcustom(atr_uxstop_t,lost_times=80,win_times=250,max_drawdown=260,min_drawdown=150,min_lost_follow=90,min_lost_against=90,max_lost_follow=90,max_lost_against=90,natr=5)  


atr5_uxstop_t_08_25_B_10 = fcustom(atr_uxstop_t,lost_times=80,win_times=250,max_drawdown=250,min_drawdown=150,min_lost_follow=100,min_lost_against=100,max_lost_follow=100,max_lost_against=100,natr=5)  


##比例止损
atr5_uxstop_f_A = fcustom(atr_uxstop_f,win_times=250,natr=5)  

atr5_uxstop_k_A = fcustom(atr_uxstop_k,win_times=250,natr=5)

FKEEP_250 = lambda bpoint: 250   #上升25点后就保证开仓价格

FKEEP_200 = lambda bpoint: 200   #上升20点后就保证开仓价格

FKEEP_180 = lambda bpoint: 180   #上升18点后就保证开仓价格

FKEEP_150 = lambda bpoint: 150   #上升15点后就保证开仓价格

FKEEP_135 = lambda bpoint: 135   #上升13.5点后就保证开仓价格

FKEEP_120 = lambda bpoint: 120   #上升12点后就保证开仓价格


atr5_uxstop_k_B = fcustom(atr_uxstop_k,fkeeper=FKEEP_180,win_times=250,natr=5)  

atr5_uxstop_k_250 = fcustom(atr_uxstop_k,fkeeper=FKEEP_250,win_times=250,natr=5)  
atr5_uxstop_k_200 = fcustom(atr_uxstop_k,fkeeper=FKEEP_200,win_times=250,natr=5)  
atr5_uxstop_k_180 = fcustom(atr_uxstop_k,fkeeper=FKEEP_180,win_times=250,natr=5)  
atr5_uxstop_k_150 = fcustom(atr_uxstop_k,fkeeper=FKEEP_150,win_times=250,natr=5)  
atr5_uxstop_k_135 = fcustom(atr_uxstop_k,fkeeper=FKEEP_135,win_times=250,natr=5)  
atr5_uxstop_k_120 = fcustom(atr_uxstop_k,fkeeper=FKEEP_120,win_times=250,natr=5)  

F20 = lambda bpoint:20
F25 = lambda bpoint:25
F30 = lambda bpoint:30
F35 = lambda bpoint:35
F40 = lambda bpoint:40
F45 = lambda bpoint:45
F50 = lambda bpoint:50
F60 = lambda bpoint:60
F70 = lambda bpoint:70
F80 = lambda bpoint:80
F90 = lambda bpoint:90

F100 = lambda bpoint:100
F120 = lambda bpoint:120
F150 = lambda bpoint:150
F180 = lambda bpoint:180

#震荡期止损
atr5_uxstop_k_oscillating = fcustom(atr_uxstop_k
        ,flost_base = F40
        ,fmax_drawdown = F60
        ,fmin_drawdown = F60
        ,fkeeper = F60
        ,win_times=250
        ,natr=5
        )  

atr5_uxstop_kt = fcustom(atr_uxstop_k
        ,flost_base = F40
        ,fmax_drawdown = F60
        ,fmin_drawdown = F60
        ,fkeeper = F60
        ,ftarget = F120
        ,win_times=250
        ,natr=5
        )  


atr5_uxstop_t_08_25_B3 = fcustom(atr_uxstop_t,lost_times=80,win_times=250,max_drawdown=200,min_drawdown=200,min_lost_follow=90,min_lost_against=90,max_lost_follow=90,max_lost_against=90,natr=5)  

atr5_uxstop_t_08_25_C = fcustom(atr_uxstop_t,lost_times=80,win_times=250,max_drawdown=200,min_lost_follow=60,min_lost_against=60,max_lost_follow=60,max_lost_against=60,natr=5)  ####R最大,胜率不是

atr5_uxstop_t_08_25_D = fcustom(atr_uxstop_t,lost_times=80,win_times=250,max_drawdown=200,min_lost_follow=60,min_lost_against=40,max_lost_follow=60,max_lost_against=40,natr=5)

atr5_uxstop_t_08_25_E= fcustom(atr_uxstop_t,lost_times=80,win_times=250,max_drawdown=200,min_lost_follow=80,min_lost_against=60,max_lost_follow=80,max_lost_against=60,natr=5)

atr5_uxstop_t_08_25_F = fcustom(atr_uxstop_t,lost_times=80,win_times=250,max_drawdown=200,min_lost_follow=80,min_lost_against=80,max_lost_follow=80,max_lost_against=80,natr=5)

atr5_uxstop_t_08_25_F2 = fcustom(atr_uxstop_t,lost_times=80,win_times=250,max_drawdown=200,min_lost_follow=85,min_lost_against=85,max_lost_follow=85,max_lost_against=85,natr=5)


atr5_uxstop_t_08_25_G = fcustom(atr_uxstop_t,lost_times=80,win_times=250,max_drawdown=200,min_lost_follow=70,min_lost_against=70,max_lost_follow=70,max_lost_against=70,natr=5)

atr5_uxstop_t_08_25_H = fcustom(atr_uxstop_t,lost_times=80,win_times=250,max_drawdown=200,min_lost_follow=50,min_lost_against=50,max_lost_follow=50,max_lost_against=50,natr=5)

atr5_uxstop_t_08_25_K = fcustom(atr_uxstop_t,lost_times=80,win_times=250,max_drawdown=200,min_lost_follow=100,min_lost_against=100,max_lost_follow=100,max_lost_against=100,natr=5)  #




atr5_uxstop_08_30 = fcustom(atr_uxstop,lost_times=80,win_times=300,max_drawdown=200,min_lost=90,max_lost=90,natr=5)


atr5_uxstop_08_25_6 = fcustom(atr_uxstop,lost_times=80,win_times=250,max_drawdown=200,min_lost=60,natr=5)


atr5_uxstop_05_25_30 = fcustom(atr_uxstop,lost_times=50,win_times=250,max_drawdown=300,min_lost=30,natr=5)
atr5_uxstop_03_25_30 = fcustom(atr_uxstop,lost_times=30,win_times=250,max_drawdown=300,min_lost=30,natr=5)
atr5_uxstop_06_25_30 = fcustom(atr_uxstop,lost_times=66,win_times=250,max_drawdown=300,min_lost=30,natr=5)
atr5_uxstop_07_25_30 = fcustom(atr_uxstop,lost_times=75,win_times=250,max_drawdown=300,min_lost=30,natr=5)
atr5_uxstop_08_25_30 = fcustom(atr_uxstop,lost_times=80,win_times=250,max_drawdown=300,min_lost=30,natr=5)

atr5_uxstop_05_25_25 = fcustom(atr_uxstop,lost_times=50,win_times=250,max_drawdown=250,min_lost=30,natr=5)
atr5_uxstop_03_25_25 = fcustom(atr_uxstop,lost_times=30,win_times=250,max_drawdown=250,min_lost=30,natr=5)
atr5_uxstop_06_25_25 = fcustom(atr_uxstop,lost_times=66,win_times=250,max_drawdown=250,min_lost=30,natr=5)
atr5_uxstop_07_25_25 = fcustom(atr_uxstop,lost_times=75,win_times=250,max_drawdown=250,min_lost=30,natr=5)
atr5_uxstop_08_25_25 = fcustom(atr_uxstop,lost_times=80,win_times=250,max_drawdown=250,min_lost=30,natr=5)


atr5_uxstop_05_3_30 = fcustom(atr_uxstop,lost_times=50,win_times=300,max_drawdown=300,min_lost=30,natr=5)
atr5_uxstop_03_3_30 = fcustom(atr_uxstop,lost_times=30,win_times=300,max_drawdown=300,min_lost=30,natr=5)
atr5_uxstop_06_3_30 = fcustom(atr_uxstop,lost_times=66,win_times=300,max_drawdown=300,min_lost=30,natr=5)
atr5_uxstop_07_3_30 = fcustom(atr_uxstop,lost_times=75,win_times=300,max_drawdown=300,min_lost=30,natr=5)
atr5_uxstop_08_3_30 = fcustom(atr_uxstop,lost_times=80,win_times=300,max_drawdown=300,min_lost=30,natr=5)

atr5_uxstop_05_3_25 = fcustom(atr_uxstop,lost_times=50,win_times=300,max_drawdown=250,min_lost=30,natr=5)
atr5_uxstop_03_3_25 = fcustom(atr_uxstop,lost_times=30,win_times=300,max_drawdown=250,min_lost=30,natr=5)
atr5_uxstop_06_3_25 = fcustom(atr_uxstop,lost_times=66,win_times=300,max_drawdown=250,min_lost=30,natr=5)
atr5_uxstop_07_3_25 = fcustom(atr_uxstop,lost_times=75,win_times=300,max_drawdown=250,min_lost=30,natr=5)
atr5_uxstop_08_3_25 = fcustom(atr_uxstop,lost_times=80,win_times=300,max_drawdown=250,min_lost=30,natr=5)

atr5_rxstop_08_3_83 = fcustom(atr_rxstop,lost_times=80,win_times=300,max_drawdown=83,min_lost=30,natr=5)   #max_drawdown=5/6/100


atr5_uxstop_05_35_30 = fcustom(atr_uxstop,lost_times=50,win_times=350,max_drawdown=300,min_lost=30,natr=5)
atr5_uxstop_03_35_30 = fcustom(atr_uxstop,lost_times=30,win_times=350,max_drawdown=300,min_lost=30,natr=5)
atr5_uxstop_06_35_30 = fcustom(atr_uxstop,lost_times=66,win_times=350,max_drawdown=300,min_lost=30,natr=5)
atr5_uxstop_07_35_30 = fcustom(atr_uxstop,lost_times=75,win_times=350,max_drawdown=300,min_lost=30,natr=5)
atr5_uxstop_08_35_30 = fcustom(atr_uxstop,lost_times=80,win_times=350,max_drawdown=300,min_lost=30,natr=5)

atr5_uxstop_05_3 = fcustom(atr_uxstop,lost_times=50,win_times=300,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_05_15 = fcustom(atr_uxstop,lost_times=50,win_times=150,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_05_10 = fcustom(atr_uxstop,lost_times=50,win_times=100,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_05_05 = fcustom(atr_uxstop,lost_times=50,win_times=50,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_1_6 = fcustom(atr_uxstop,lost_times=100,win_times=600,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_05_6 = fcustom(atr_uxstop,lost_times=50,win_times=600,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_1_25 = fcustom(atr_uxstop,lost_times=100,win_times=250,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_1_15 = fcustom(atr_uxstop,lost_times=100,win_times=150,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_15_15 = fcustom(atr_uxstop,lost_times=150,win_times=150,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_03_15 = fcustom(atr_uxstop,lost_times=30,win_times=150,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_03_10 = fcustom(atr_uxstop,lost_times=30,win_times=100,max_drawdown=200,min_lost=30,natr=5)
atr5_uxstop_03_05 = fcustom(atr_uxstop,lost_times=30,win_times=50,max_drawdown=200,min_lost=30,natr=5)


atr5_uxstop_05_25b = fcustom(atr_uxstop,lost_times=50,win_times=250,max_drawdown=200,min_lost=50,natr=5)
atr5_uxstop_05_25c = fcustom(atr_uxstop,lost_times=50,win_times=250,max_drawdown=200,min_lost=60,natr=5)



