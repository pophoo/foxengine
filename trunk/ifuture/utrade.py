# -*- coding: utf8 -*-

'''
    核心交易模块扩展
        针对突破交易和即时止损

'''

from wolfox.fengine.ifuture.ibase import *
import wolfox.fengine.ifuture.iftrade as iftrade
import wolfox.fengine.ifuture.ifuncs as ifuncs

#同一分钟先开后平, 由make_trades确保已有开仓时不重复. 但已有仓位时同时出现开平信号，则以平仓计
DTSORT2 = lambda x,y: int(((x.date%1000000 * 10000)+x.time) - ((y.date%1000000 * 10000)+y.time)) or x.xtype-y.xtype 

#设定保证
def atr_stop_u(
        sif
        ,sopened
        ,sbclose
        ,ssclose
        ,flost_base = iftrade.FBASE_30    #flost:买入点数 --> 止损点数
        ,fmax_drawdown = iftrade.F100_25 #fdmax:买入点数 --> 最大回落
        ,fmin_drawdown = iftrade.F60_15#fdmin:买入点数 --> 最小回落
        ,fkeeper = iftrade.FKEEP_30 #买入点数-->固定移动止损，移动到价格为止
        ,win_times=300        
        ,ftarget = iftrade.FTARGET #盈利目标,默认是无穷大
        ,tlimit = 10    #约定时间线. 目前没用
        ,wtlimit =  -100   #约定时间线的价格有利变动目标，如果不符合则平仓
        ,natr=1
        ):
    '''
        根据价格突破即时止损,而不是下一个开盘价，返回值为止损价，未考虑滑点
            开仓时刻如果收盘价反向偏离开仓价超过初始止损，则也止损
        sif为实体
        sopened为价格序列，其中负数表示开多仓，正数表示开空仓
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
    satr = iftrade.afm[natr](sif)
    trans = sif.transaction
    rev = np.zeros_like(sopened)
    isignal = np.nonzero(sopened)[0]
    ilong_closed = 0    #多头平仓日
    ishort_closed = 0   #空头平仓日
    will_losts = []
    myssclose = ssclose * XSELL #取符号, 如果是买入平仓，则<0
    mysbclose = sbclose * XBUY #取符号, 如果是卖出平仓，则<0
    #print mysbclose[-300:]
    #print myssclose[np.nonzero(myssclose)]
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
        if price<0: #多头止损
            #print u'多头止损'
            if i <= ilong_closed:
                #print 'long skipped'
                continue
            #print 'find long stop:',i
            #if i < ilong_closed:    #已经开了多头仓，且未平，不再计算
            #    print 'skiped',trans[IDATE][i],trans[ITIME][i],trans[IDATE][ilong_closed],trans[ITIME][ilong_closed]
            #    continue
            buy_price = -price
            lost_stop = buy_price - willlost
            cur_high = max(buy_price,sif.close[i])
            win_stop = cur_high - satr[i] * win_times / XBASE / XBASE
            cur_stop = lost_stop if lost_stop > win_stop else win_stop
            wtarget = buy_price + ftarget(buy_price)
            #print 'wtarget:%s',wtarget
            #print 'stop init:',cur_stop,lost_stop,willlost,min_lost,max_lost
            if myssclose[i] > 0:
                #print 'sell signali:',trans[IDATE][i],trans[ITIME][i],trans[ICLOSE][i]
                pass
            if trans[ICLOSE][i] < cur_stop:#到达止损
                #print '----sell----------:',trans[IDATE][i],trans[ITIME][i],cur_stop,trans[ICLOSE][i],cur_high,lost_stop
                ilong_closed = i
                rev[i] = cur_stop * XSELL   #设定价格
            elif myssclose[i] >0:#或平仓
                ilong_closed = i                
                rev[i] = myssclose[i] * XSELL
            else:
                for j in range(i+1,len(rev)):
                    tv = sif.close[j] - buy_price
                    #print trans[ITIME][j],buy_price,lost_stop,cur_high,win_stop,cur_stop,trans[ILOW][j],satr[j]
                    if trans[ILOW][j] < cur_stop:
                        ilong_closed = j
                        rev[j] = cur_stop * XSELL 
                        #print 'sell in atrstop:'#,i,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j],sif.low[j],cur_stop
                        break
                    elif  myssclose[j] >0:
                        ilong_closed = j
                        rev[j] = myssclose[j] * XSELL 
                        #print 'sell in sclose:'#,i,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j],sif.low[j],cur_stop
                        break
                    elif j==i+tlimit and tv<wtlimit:    #时间到
                        ilong_closed = j
                        rev[j] = trans[ICLOSE][j] * XSELL 
                        #print 'sell in time limit:'#,i,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j],sif.low[j],cur_stop
                        break
                    elif trans[IHIGH][j] > wtarget: #超过目标价
                        ilong_closed = j                        
                        rev[j] = wtarget * XSELL
                        #print 'sell at target:'#,i,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j],sif.low[j],cur_stop
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
            if i<=ishort_closed:
                #print 'short skipped'
                continue
            sell_price = price
            lost_stop = sell_price + willlost
            cur_low = min(sell_price,trans[ICLOSE][i])
            win_stop = cur_low + satr[i] * win_times / XBASE / XBASE
            cur_stop = lost_stop if lost_stop < win_stop else win_stop
            wtarget = sell_price - ftarget(sell_price)
            if trans[ICLOSE][i] > cur_stop:
                #print '----buy----------:',cur_stop,trans[ICLOSE][i],cur_high,lost_stop
                ishort_closed = i
                rev[i] = cur_stop * XBUY
            elif mysbclose[i] >0:
                #print 'buy signali:',trans[IDATE][i],trans[ITIME][i],trans[ICLOSE][i]
                ishort_closed = i
                rev[i] = mysbclose[i] *XBUY
            else:
                for j in range(i+1,len(rev)):
                    tv = sell_price - sif.close[j]
                    #print trans[ITIME][j],sell_price,lost_stop,cur_low,win_stop,cur_stop,trans[IHIGH][j],satr[j]                
                    if trans[IHIGH][j] > cur_stop:
                        ishort_closed = j
                        rev[j] = cur_stop * XBUY
                        #print 'buy:',j
                        #print 'buy:',i,price,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j]                        
                        break
                    elif mysbclose[j] >0:
                        #print 'buy signalj:',trans[IDATE][j],trans[ITIME][j],cur_stop,trans[ICLOSE][j]
                        ishort_closed = j
                        rev[j] = mysbclose[j] * XBUY
                        break
                    elif (j==i+tlimit and tv < wtlimit):#时间到
                        ishort_closed = j
                        rev[j] = trans[ICLOSE] * XBUY   
                        break
                    elif trans[ILOW][j] < wtarget:#
                        ishort_closed = j
                        rev[j] = wtarget * XBUY
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
                        #print nlow,cur_stop,win_stop,satr[j],win_times,drawdown
                        #win_stop = cur_low + satr[j] * win_times / XBASE / XBASE
                        if cur_stop > win_stop:
                            cur_stop = win_stop
                        keep_stop = cur_low + keeper
                        if cur_stop > sell_price and keep_stop < sell_price:
                            cur_stop = sell_price 
                        #if cur_stop > keep_stop:
                        #    cur_stop = keep_stop if keep_stop > sell_price else sell_price
                        
    #print will_losts
    #print rev[np.nonzero(rev)]
    return rev

def sync_tradess_u(sif,tradess,acstrategy=iftrade.late_strategy):
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
    cur_trade = iftrade.find_first(tradess)
    if cur_trade == None:
        return []
    cur_trade.orignal = cur_trade.functor   
    cur_trade.open_action = cur_trade.actions[0]
    extended,filtered,rfiltered,reversed = [],[],[],[]
    close_action = cur_trade.actions[-1]
    #print '#####################first:',close_action.time
    while True:
        #print cur_trade.orignal
        trade = iftrade.find_first(tradess)
        if trade == None:
            xtrades.append(iftrade.close_trade(sif,cur_trade,close_action,extended,filtered,rfiltered,reversed))
            break
        #print 'find:date=%s,time=%s,functor=%s,priority=%s' % (trade.actions[0].date,trade.actions[0].time,trade.functor,fpriority(trade.functor))  
        #if trade.actions[0].xfollow <= 0:
        #    continue
        if DTSORT2(trade.actions[0],close_action)>0:  #时间超过
            #print u'时间超过'
            xtrades.append(iftrade.close_trade(sif,cur_trade,close_action,extended,filtered,rfiltered,reversed))
            trade.orignal = trade.functor
            cur_trade = trade
            close_action = cur_trade.actions[-1]
            extended,filtered,rfiltered,reversed = [],[],[],[]
            #print cur_trade.orignal
            trade.open_action = trade.actions[0]
            continue
           
        if trade.actions[0].index > cur_trade.actions[0].index and iftrade.aprofit(cur_trade.open_action,sclose[trade.actions[0].index]) < 251:   #25点浮动收益后不取代
            if trade.direction == cur_trade.direction:  #同向取代关系
                #print u'同向增强,%s|%s:%s被%s增强'%(cur_trade.functor,cur_trade.actions[0].date,cur_trade.actions[0].time,trade.functor)
                close_action = acstrategy(close_action,trade.actions[-1])
                extended.append(cur_trade)
                trade.orignal = cur_trade.orignal
                trade.open_action = cur_trade.open_action
                cur_trade = trade
            else:   #逆向平仓
                #print u'\n\t逆向平仓:',iftrade.aprofit(cur_trade.open_action,sclose[trade.actions[0].index]),sif.date[cur_trade.open_action.index],sif.time[cur_trade.open_action.index],func_name(cur_trade.orignal),'--',func_name(trade.functor)
                reversed.append(trade)
                xindex = reversed[0].actions[0].index
                cposition = BaseObject(index=xindex,date=sdate[xindex],time=stime[xindex],position=reversed[0].direction,xtype=XCLOSE)    #因为已经抑制了1514开仓,必然不会溢出
                cposition.price = iftrade.make_price(cposition.position,sopen[xindex],sclose[xindex],shigh[xindex],slow[xindex])
                xtrades.append(iftrade.close_trade(sif,cur_trade,cposition,extended,filtered,rfiltered,reversed))
                trade.orignal = trade.functor
                trade.open_action = trade.actions[0]
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


def utrade_x(sif     #期指
            ,openers    #opener函数集合
            ,bclosers   #默认的多平仓函数集合(空头平仓)
            ,sclosers   #默认的空平仓函数集合(多头平仓)
            ,stop_closer    #止损closer函数，只能有一个，通常是atr_uxstop,    
                            #有针对性是指与买入价相关的 stop_closer必须处理之前的closers系列发出的卖出信号
            ,osc_stop_closer = None#震荡止损函数
            ,longfilter=iftrade.ocfilter    #opener过滤器,多空仓必须满足各自过滤器条件才可以发出信号. 
                                    #比如抑制在0915-0919以及1510-1514开仓等
                                    #closer没有过滤器,设置过滤器会导致合约一直开口
            ,shortfilter=iftrade.ocfilter   #opener过滤器,多空仓必须满足各自过滤器条件才可以发出信号. 
            ,make_trades=iftrade.simple_trades  #根据开平仓动作撮合交易的函数。对于最后交易序列，用last_trades
            ,sync_trades=sync_tradess_u    #汇总各opener得到的交易，计算优先级和平仓。
                                            #对于最后交易序列，用null_sync_tradess
            ,acstrategy=iftrade.late_strategy   #增强开仓时的平仓策略。late_strategy是平最晚的那个信号
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
    
    openers = [opener for opener in openers if iftrade.fpriority(opener)<priority_level]

    tradess = []
    for opener in openers:
        #if 'filter' not in opener.__dict__: #用于对信号进行过滤,如开盘30分钟内不发出信号等
        #    myfilter = slongfilter if iftrade.fdirection(opener) == XBUY else sshortfilter
        #else:
        #    myfilter = opener.filter(sif)
        if iftrade.fdirection(opener) == XBUY:
            if 'is_followed' in opener.__dict__ and opener.is_followed == True: #如果设定为follow，则使用默认
                #print 'is_followed x:',longfilter,pstate_oc_filter
                myfilter = slongfilter
            elif 'longfilter' in opener.__dict__:
                #print 'lfilter'
                myfilter = opener.longfilter(sif)
            elif 'filter' in opener.__dict__:
                print 'buy infilter:'
                myfilter = opener.filter(sif)
            else:
                myfilter = slongfilter
        else:#XSELL
            if 'is_followed' in opener.__dict__ and opener.is_followed == True: #如果设定为follow，则使用默认
                #print 'is_followed y:',shortfilter,npstate_oc_filter
                myfilter = sshortfilter
            elif 'shortfilter' in opener.__dict__:
                #print 'sfilter'                
                myfilter = opener.shortfilter(sif)
            elif 'filter' in opener.__dict__:
                print 'sell,infilter:'                
                myfilter = opener.filter(sif)
            else:
                myfilter = sshortfilter
        if 'xfilter' not in opener.__dict__:    #xfilter用于自定义的信号变换,如根据5分钟内的波动决定延迟发送还是吞没
            xfilter = iftrade.gothrough_filter
        else:
            xfilter = opener.xfilter
        opens = uopen_position(sif,xfilter(sif,opener(sif)),myfilter,myfilter) #因为opener只返回一个方向的操作,所以两边都用myfilter，但实际上只有相应的一个有效，另一个是虚的
        #opens.sort(DTSORT)
        sopened = np.zeros(len(sif.transaction[IDATE]),int)   #为开仓价格序列,负数为开多仓,正数为开空仓
        for aopen in opens:
            sopened[aopen.index] = aopen.price * aopen.position
        sclose = np.zeros(len(sif.transaction[IDATE]),int)
        if 'closer' in opener.__dict__: #是否有特定的closer,如要将macd下叉也作为多头持仓的平仓条件,则可设置函数,在返回值中添加该下叉信号算法
            if iftrade.fdirection(opener) == XBUY:
                #print 'buy closer:',opener.closer
                closers = opener.closer(sclosers)
            elif iftrade.fdirection(opener) == XSELL:
                closers = opener.closer(bclosers)
        else:
            #print 'opener without close fdirection(opener) = %s' % ('XBUY' if fdirection(opener) == XBUY else 'XSELL',)
            closers = sclosers if iftrade.fdirection(opener) == XBUY else bclosers
        for closer in closers:
            sclose = gor(sclose,closer(sif,sopened)) * (-iftrade.fdirection(opener))
        if osc_stop_closer == None:
            osc_stop_closer = stop_closer 
        ms_closer = stop_closer if 'stop_closer' not in opener.__dict__ else opener.stop_closer
        
        if 'osc_stop_closer' not in opener.__dict__:
            osc_closer = opener.stop_closer if 'stop_closer' in opener.__dict__ else osc_stop_closer
        else:
            osc_closer = opener.osc_stop_closer

        #closes = uclose_position(sif,stop_closer(sif,sopened,sclose,sclose)) #因为是单向的，只有一个sclose起作用
        
        ms_sclose = ms_closer(sif,sopened,sclose,sclose)
        osc_sclose = osc_closer(sif,sopened,sclose,sclose)
        #sclose的优先级最高. ms_closer是atr类的止损,与osc是竞争关系
        xsclose = np.select([sif.xstate!=0,sif.xstate==0],[ms_sclose,osc_sclose])
        #xsclose = np.select([sclose!=0,sif.xstate!=0,sif.xstate==0],[sclose,ms_sclose,osc_sclose])
        
        xsclose = np.select([sclose!=0],[sclose],default=xsclose)   #不能用gor，gor后-1变1，就没有闭合交易了

        #closes = uclose_position(sif,ms_sclose)
        closes = uclose_position(sif,xsclose)
        #closes = uclose_position(sif,ms_closer(sif,sopened,sclose,sclose)) #因为是单向的，只有一个sclose起作用        


        actions = sorted(opens + closes,iftrade.DTSORT2)
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


def utrade(sif     #期指
            ,openers    #opener函数集合
            ,bclosers   #默认的多平仓函数集合(空头平仓)
            ,sclosers   #默认的空平仓函数集合(多头平仓)
            ,stop_closer    #止损closer函数，只能有一个，通常是atr_uxstop,    
                            #有针对性是指与买入价相关的 stop_closer必须处理之前的closers系列发出的卖出信号
            ,make_trades=iftrade.simple_trades  #根据开平仓动作撮合交易的函数。对于最后交易序列，用last_trades
            ,sync_trades=sync_tradess_u    #汇总各opener得到的交易，计算优先级和平仓。
                                            #对于最后交易序列，用null_sync_tradess
            ,acstrategy=iftrade.late_strategy   #增强开仓时的平仓策略。late_strategy是平最晚的那个信号
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
                name:       名字

    '''
    if not isinstance(openers,list):   #单个函数
        openers = [openers]
    if not isinstance(bclosers,list):   #单个函数
        bclosers = [bclosers]
    if not isinstance(sclosers,list):   #单个函数
        sclosers = [sclosers]
    
    openers = [opener for opener in openers if iftrade.fpriority(opener)<priority_level]

    tradess = []
    for opener in openers:
        opens = uopen_position(sif,opener(sif))
        odir = iftrade.fdirection(opener)
        sopened = np.zeros(len(sif.date),int)   #为开仓价格序列,负数为开多仓,正数为开空仓
        for aopen in opens:
            sopened[aopen.index] = aopen.price * aopen.position
        sclose = np.zeros(len(sif.date),int)
        if 'closer' in opener.__dict__: #是否有特定的closer,如要将macd下叉也作为多头持仓的平仓条件,则可设置函数,在返回值中添加该下叉信号算法
            if odir == XBUY:
                #print 'buy closer:',opener.closer
                closers = opener.closer(sclosers)
            elif odir == XSELL:
                closers = opener.closer(bclosers)
        else:
            #print 'opener without close iftrade.fdirection(opener) = %s' % ('XBUY' if iftrade.fdirection(opener) == XBUY else 'XSELL',)
            closers = sclosers if odir == XBUY else bclosers


        #这里需要u处理
        if odir == XBUY:#卖平
            psclose = np.select([sclose],[np.abs(sclose)],PS_MAX)    #把0转换为最大值
            for closer in closers:#这里默认认为closer返回的数据中只要非0就算是有信号, 而不是区分买平还是卖平
                cur_s = closer(sif,sopened)
                #print closer,cur_s[-300:],XSELL,odir
                cur_ps = np.select([cur_s!=0],[np.abs(cur_s)],PS_MAX)   #把0转换为最大值
                psclose = gmin(psclose,cur_ps)       #卖出选最小
            sclose = np.select([psclose!=PS_MAX],[psclose* (-odir)],0) #将PS_MAX变回0
            #print sclose[np.nonzero(sclose)]
        else:#买平
            psclose = np.abs(sclose)
            for closer in closers:#这里默认认为closer返回的数据中只要非0就算是有信号, 而不是区分买平还是卖平
                psclose = gmax(psclose,np.abs(closer(sif,sopened)))
            sclose = psclose * (-odir)

        ms_closer = stop_closer if 'stop_closer' not in opener.__dict__ else opener.stop_closer
        
        closes = uclose_position(sif,ms_closer(sif,sopened,sclose,sclose)) #因为是单向的，只有一个sclose起作用        

        #print ms_closer(sif,sopened,sclose,sclose)[-300:]
        #print closes[-1].time,closes[-1].date,closes[-2].date,closes[-2].time
        #print opens[-1].time,opens[-1].date,opens[-2].date,opens[-2].time
        #print 'iclose:'
        #for iclose in closes:
        #    print iclose.date,iclose.time
        
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

def uopen_position(sif,sopener):
    '''
        sopener中,XBUY表示开多仓,XSELL表示开空仓
    '''
    pbuy = sopener * XBUY  #取数字, 如果是卖出平仓，则<0    
    psell = sopener * XSELL #取数字, 如果是买入平仓，则<0

    pslong = np.select([pbuy>0],[pbuy*LONG],0)
    psshort = np.select([psell>0],[psell*SHORT],0)    
    positions = uposition(sif,pslong,XOPEN)
    positions.extend(uposition(sif,psshort,XOPEN))
    return positions


def uclose_position(sif,scloser):
    ''' scloser中, XBUY表示平空(买入),XSELL表示平多(卖出)
    '''
    #print 'in uclose position'

    pbuy = scloser * XBUY  #取数字
    psell = scloser * XSELL #取数字

    pslong = np.select([pbuy>0],[pbuy*LONG],0)
    psshort = np.select([psell>0],[psell*SHORT],0)    
    
    positions = uposition(sif,pslong,XCLOSE)
    positions.extend(uposition(sif,psshort,XCLOSE))
    return positions


def uposition(sif,saction,xtype,defer=1):
    '''
        针对saction进行开仓或平仓
        如果与XLONG同向则开多仓     
            与XSHORT同向则开空仓
        如果价格的绝对值==1则按defer在开盘处开仓，否则按指定价即时开仓
    '''
    isignal = saction.nonzero()[0]
    positions = []
    for i in isignal:
        uprice = saction[i] #可能是信号，也可能是信号叠加价格
        direct = np.sign(uprice)    #如果是信号叠加价格，则其方向和信号方向一致
        xindex = i+defer if is_only_position_signal(uprice) else i  #如果是信号则按defer计算，是价格则即时发生
        if xindex >= len(sif.close):   #如果是最后一分钟，则放弃. 这种情况只会出现在动态计算中，且该分钟未走完(走完的话应该出现下一分钟的报价)，所以放弃是正常操作
            continue
        xprice = iftrade.make_price(direct,sif.open[xindex],sif.close[xindex],sif.high[xindex],sif.low[xindex]) if is_only_position_signal(uprice) else np.abs(uprice)
        #print xindex,len(sif.close)
        position = BaseObject(index=xindex,date=sif.date[xindex],time=sif.time[xindex],price=xprice,position=direct,xtype=xtype)    #因为已经抑制了1514开仓,必然不会溢出
        positions.append(position)
        if xtype == XOPEN:
            #顺势、逆势以及不明势
            if saction[i] == LONG:
                if sif.xstate[i] > 0:
                    position.xfollow = 1
                elif sif.xstate[i] < 0:
                    position.xfollow = -1
                else:
                    position.xfollow = 0
            else:
                if sif.xstate[i] < 0:
                    position.xfollow = 1
                elif sif.xstate[i] > 0:
                    position.xfollow = -1
                else:
                    position.xfollow = 0
    return positions

def day_trades(trades,limit=-200):
    '''
        每日损失到limit之后不再开仓
        在中间即便有盈利，但是如果累计起来仍然为负，则持续计算
    '''
    if len(trades) == 0:
        return []
    cur_trade = trades[0]
    results = [BaseObject(day=cur_trade.actions[-1].date,
                            profit=cur_trade.profit,
                            sprofit = cur_trade.profit,
                            max_drawdown=cur_trade.profit if cur_trade.profit < 0 else 0,
                            ntrade = 1,
                            ontrade = 1,
                        )
                ]
    for trade in trades[1:]:
        tdate = trade.actions[-1].date
        if trade.actions[-1].date ==results[-1].day:
            results[-1].profit += trade.profit
            results[-1].ontrade += 1
            last_drawdown = results[-1].max_drawdown
            if results[-1].sprofit > limit:
            #if last_drawdown > limit:
                results[-1].sprofit += trade.profit
                results[-1].ntrade += 1
            results[-1].max_drawdown += trade.profit
            if results[-1].max_drawdown > 0:
                results[-1].max_drawdown = 0
            elif results[-1].max_drawdown > last_drawdown:
                results[-1].max_drawdown = last_drawdown
        else:
            results.append(BaseObject(day=trade.actions[-1].date,
                        profit=trade.profit,
                        sprofit = trade.profit,                            
                        max_drawdown=trade.profit if trade.profit < 0 else 0,
                        ntrade = 1,
                        ontrade = 1,
                    )
            )
            

    return results


def dmax_drawdown(dtrades,datefrom=20100401,dateto=20200101):
    '''
        按日计算
        dtrades为每日的交易汇总
    '''
    smax = 0    #最大连续回撤
    max1 = 0    #最大单日回撤
    curs = 0
    mdate = 20100401
    for trade in dtrades:
        tdate = trade.day
        if tdate > datefrom and tdate < dateto: #忽略掉小于开始时间的
            curs += trade.sprofit   #本为负数
            if curs > 0:
                curs = 0
            elif curs < smax:
                smax = curs
                mdate = tdate
            if trade.sprofit < max1:
                max1 = trade.sprofit
    return smax,max1,mdate


atr5_ustop_V = fcustom(atr_stop_u,
                fkeeper=iftrade.F80,
                win_times=250,
                natr=5,
                flost_base=iftrade.F60,
                fmax_drawdown=iftrade.F333
            )      #

#V1的回报类似(减少10%)，单次止损小,回撤收窄.R大
atr5_ustop_V1 = fcustom(atr_stop_u
        ,fkeeper=iftrade.F80
        ,win_times=250
        ,natr=5
        ,flost_base=iftrade.F40 #止损太窄不好操作，很可能还没设止损单就已经破了
        ,fmax_drawdown=iftrade.F333)      #120-60

atr5_ustop_V2 = fcustom(atr_stop_u
        ,fkeeper=iftrade.F80
        ,win_times=250
        ,natr=5
        ,flost_base=iftrade.F30 #止损太窄不好操作，很可能还没设止损单就已经破了
        ,fmax_drawdown=iftrade.F333)      #120-60

atr5_ustop_X = fcustom(atr_stop_u
        ,fkeeper=iftrade.F150
        ,win_times=250
        ,natr=5
        ,flost_base=iftrade.F60 #止损太窄不好操作，很可能还没设止损单就已经破了
        ,fmax_drawdown=iftrade.F333)      #120-60

atr5_ustop_X1 = fcustom(atr_stop_u
        ,fkeeper=iftrade.F150
        ,win_times=250
        ,natr=5
        ,flost_base=iftrade.F90 #止损太窄不好操作，很可能还没设止损单就已经破了
        ,fmax_drawdown=iftrade.F333
        )      #120-60

atr5_ustop_X2 = fcustom(atr_stop_u
        ,fkeeper=lambda x: 60#
        ,win_times=250
        ,natr=5
        ,flost_base=iftrade.F30 #止损太窄不好操作，很可能还没设止损单就已经破了
        ,fmax_drawdown=iftrade.F333)      #120-60

atr5_ustop_X3 = fcustom(atr_stop_u
        ,fkeeper=lambda x: 100#效果和X2差不多,哲学上选择这个。倡导较长持仓
        ,win_times=250
        ,natr=5
        ,flost_base=iftrade.F30 #止损太窄不好操作，很可能还没设止损单就已经破了
        ,fmax_drawdown=iftrade.F333)      #120-60

atr5_ustop_X4 = fcustom(atr_stop_u
        ,fkeeper=lambda x: 60#
        ,win_times=250
        ,natr=5
        ,flost_base=iftrade.F40 #止损太窄不好操作，很可能还没设止损单就已经破了
        ,fmax_drawdown=iftrade.F333)      #120-60


atr5_ustop_W1 = fcustom(atr_stop_u,fkeeper=iftrade.F120,win_times=250,natr=5,flost_base=iftrade.F60,fmax_drawdown=iftrade.F333)      #120-60
atr5_ustop_V3 = fcustom(atr_stop_u,fkeeper=iftrade.F90,win_times=250,natr=5,flost_base=iftrade.F80,fmax_drawdown=iftrade.F333)      #120-60

atr5_ustop_5 = fcustom(atr_stop_u
                ,fkeeper=iftrade.F50
                ,win_times=250
                ,natr=5
                ,flost_base=iftrade.F30
                ,fmax_drawdown=iftrade.F180
                ,fmin_drawdown=iftrade.F100                
                #,ftarget = iftrade.F180
            )

atr5_ustop_6 = fcustom(atr_stop_u
                ,fkeeper=iftrade.F80
                ,win_times=250
                ,natr=5
                ,flost_base=iftrade.F60
                ,fmax_drawdown=iftrade.F120
                ,fmin_drawdown=iftrade.F80
                #,ftarget = iftrade.F180
            )

atr5_ustop_61 = fcustom(atr_stop_u
                ,fkeeper=iftrade.F80
                ,win_times=250
                ,natr=5
                ,flost_base=iftrade.F40
                ,fmax_drawdown=iftrade.F120
                ,fmin_drawdown=iftrade.F80
                #,ftarget = iftrade.F180
            )

atr5_ustop_62 = fcustom(atr_stop_u
                ,fkeeper=iftrade.F80
                ,win_times=250
                ,natr=5
                ,flost_base=iftrade.F30
                ,fmax_drawdown=iftrade.F120
                ,fmin_drawdown=iftrade.F80
                #,ftarget = iftrade.F180
            )

atr5_ustop_j = fcustom(atr_stop_u
                ,fkeeper=iftrade.F50
                ,win_times=250
                ,natr=5
                ,flost_base=iftrade.F30
                ,fmax_drawdown=iftrade.F80
                ,fmin_drawdown=iftrade.F80                
                #,ftarget = iftrade.F180
            )      #120-60


utrade_n = fcustom(utrade,stop_closer=atr5_ustop_V,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long])
utrade_d = fcustom(utrade,stop_closer=atr5_ustop_V,bclosers=[ifuncs.xdaystop_short],sclosers=[ifuncs.xdaystop_long],make_trades=iftrade.last_trades,sync_trades=iftrade.null_sync_tradess)

