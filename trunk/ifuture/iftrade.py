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

def simple_trades(actions,calc_profit=simple_profit):  #简单的trades,每个trade只有一次开仓和平仓
    ''' 不支持同时双向开仓
    '''
    state = EMPTY
    trades = []
    for action in actions:
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

def atr_uxstop(sif,sopened,sbclose,ssclose,lost_times=200,win_times=300,max_drawdown=200,min_lost=30):
    '''
        atr止损
        sif为实体
        sopen为价格序列，其中负数表示开多仓，正数表示开空仓
        sbclose是价格无关序列所发出的买入平仓信号集合(平空仓)
        ssclose是价格无关序列所发出的卖出平仓信号集合(平多仓)
        只能持有一张合约。即当前合约在未平前会屏蔽掉所有其它开仓
    '''
    #print sbclose[-10:],ssclose[-10:]
    trans = sif.transaction
    rev = np.zeros_like(sopened)
    isignal = np.nonzero(sopened)[0]
    ilong_closed = 0    #多头平仓日
    ishort_closed = 0   #空头平仓日
    for i in isignal:
        price = sopened[i]
        willlost = sif.atr[i] * lost_times / XBASE
        if willlost < min_lost:
            willlost = min_lost
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
            win_stop = cur_high - sif.atr[i] * win_times / XBASE
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
                    #print trans[ITIME][j],buy_price,lost_stop,cur_high,win_stop,cur_stop,trans[ILOW][j],sif.atr[j]
                    if trans[ILOW][j] < cur_stop or ssclose[j] == XSELL:    #
                        rev[j] = XSELL
                        #print 'sell:',i,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j]
                        ilong_closed = j
                        break
                    nhigh = trans[IHIGH][j]
                    if(nhigh > cur_high):
                        cur_high = nhigh
                        drawdown = sif.atr[j] * win_times / XBASE
                        if drawdown > max_drawdown:
                            drawdown = max_drawdown
                        win_stop = cur_high - drawdown
                        #win_stop = cur_high - sif.atr[j] * win_times / XBASE
                        #print nhigh,cur_stop,win_stop,sif.atr[j]
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
            win_stop = cur_low + sif.atr[i] * win_times / XBASE 
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
                    #print trans[ITIME][j],sell_price,lost_stop,cur_low,win_stop,cur_stop,trans[IHIGH][j],sif.atr[j]                
                    if trans[IHIGH][j] > cur_stop or sbclose[j] == XBUY:#
                        ishort_closed = j
                        rev[j] = XBUY
                        #print 'buy:',j
                        #print 'buy:',i,price,trans[IDATE][i],trans[ITIME][i],trans[IDATE][j],trans[ITIME][j]                        
                        break
                    nlow = trans[ILOW][j]
                    if(nlow < cur_low):
                        cur_low = nlow
                        drawdown = sif.atr[j] * win_times / XBASE
                        if drawdown > max_drawdown:
                            drawdown = max_drawdown
                        win_stop = cur_low + drawdown
                        #print nlow,cur_stop,win_stop,sif.atr[j]
                        #win_stop = cur_low + sif.atr[j] * win_times / XBASE
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

itrade3y = fcustom(itrade3,stop_closer=atr_uxstop_15_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=[ifuncs.daystop_long,ifuncs.ipmacd_short,ifuncs.down01,ifuncs.dmacd_short5,ifuncs.ipmacdx_short,ifuncs.ipmacd_short5,ifuncs.ma30_short,ifuncs.xmacd_stop_long1])

itrade3x1 = fcustom(itrade3,stop_closer=atr_uxstop_1_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1,ifuncs.ipmacd_long_devi1],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])

itrade3y1 = fcustom(itrade3,stop_closer=atr_uxstop_1_6,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1],sclosers=[ifuncs.daystop_long,ifuncs.ipmacd_short,ifuncs.down01,ifuncs.dmacd_short5,ifuncs.ipmacdx_short,ifuncs.ipmacd_short5,ifuncs.ma30_short,ifuncs.xmacd_stop_long1])


itrade3x45 = fcustom(itrade3,stop_closer=atr_uxstop_15_6_45,bclosers=[ifuncs.daystop_short,ifuncs.xmacd_stop_short1,ifuncs.ipmacd_long_devi1],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])


itrade1525 = fcustom(itrade3,stop_closer=atr_uxstop_15_25,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])

itrade256 = fcustom(itrade3,stop_closer=atr_uxstop_15_6,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])



#空头不把即刻反叉作为平仓选项
itrade3xk = fcustom(itrade3,stop_closer=atr_uxstop_15_6,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1])


import wolfox.fengine.ifuture.tfuncs as tfuncs

#itrade3xkx = fcustom(itrade3,stop_closer=atr_uxstop_15_6,bclosers=[ifuncs.daystop_short],sclosers=[ifuncs.daystop_long,ifuncs.xmacd_stop_long1,ifuncs.xdevi_stop_long1,tfuncs.xdevi_stop_long12])

