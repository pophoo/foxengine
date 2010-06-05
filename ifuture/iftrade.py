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
trades = iftrade.itrade(i06,[ifuncs.ipmacd_short,ifuncs.ipmacd_long,ifuncs.down0,ifuncs.up0,ifuncs.xhdevi,ifuncs.xhdevi2,ifuncs.xldevi,ifuncs.xldevi2],[ifuncs.daystop_long,ifuncs.daystop_short,ifuncs.atr_xstop_2_3])

'''




from wolfox.fengine.ifuture.ibase import *

DTSORT = lambda x,y: int(((x.date%1000000 * 10000)+x.time) - ((y.date%1000000 * 10000)+y.time)) #避免溢出

simple_profit = lambda actions: actions[0].price * actions[0].position + actions[1].price * actions[1].position - TAX

def ocfilter(sif):  #在开盘前30分钟和收盘前5分钟不开仓，头三个交易日不开张
    stime = sif.transaction[ITIME]
    soc = gand(greater(stime,959),lesser(stime,1510))
    soc[:275*3] = 0
    return soc

def simple_trades(actions,calc_profit=simple_profit):  #简单的trades,每个trade只有一次开仓和平仓
    ''' 不支持同时双向开仓
    '''
    state = EMPTY
    trades = []
    for action in actions:
        if state == EMPTY:
            if action.xtype == XOPEN:
                state = action.position
                action.vol = 1
                trade = BaseObject(actions = [action])
            else:   #未持仓时碰到平仓动作,忽略
                pass
        elif action.xtype == XCLOSE and action.position != state:    #平仓且方向相反
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

def open_position(trans,sopener,slongfilter,sshortfilter):
    '''
        sopener中,XBUY表示开多仓,XSELL表示开空仓
    '''
    slong = band(equals(sopener,XBUY),slongfilter) * LONG 
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
    smax = 0
    curs = 0
    for trade in trades:
        tdate = trade.actions[-1].date
        if tdate > datefrom and tdate < dateto: #忽略掉小于开始时间的
            if trade.profit > 0:
                curs = 0
            else:
                curs -= trade.profit   #转为正数
                if curs > smax:
                    smax = curs
    return smax;

def max_win(trades,datefrom=20100401,dateto=20200101):
    smax = 0
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
    return smax;

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
