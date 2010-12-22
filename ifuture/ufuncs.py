# -*- coding: utf-8 -*-


'''
    新高/新低系统
    当出现信号开仓后，如果未平仓前出现第二个信号，则止损要按照这几个信号最宽的一个来放
    L: 0.018手续费

实盘中的几点注意
1. 止损
   a.止损的ATR是根据上一完整周期的5分钟ATR设置的，不是本5分钟的，这一点需要非常注意
   b.当连续创新高或新低时，止损点未必上移或下移，这个取决于ATR5的变化，很可能新高点因为ATR5变大导致
        新计算的止损点不如上一止损点, 从而不移动. 这个必须仔细。

突破法列举:
    1. 当日突破
    2. 突破前一日高点
    3. 突破当日的前一个高点

突破确认类操作
    如果突破当时没用条件单开仓，而突破后价格回落，但未触及止损
    则此时可于突破位-1开条件单，下次突破后再开仓，或者到止损位后撤销条件单
    因为胜率<50%，以条件单续开放式为佳，不建议逆向运转后优势追开

10:30前的操作规则:
    顺t120? 还是r120/60/30?

文华财经的主图指标HHLL： 实际输出是DH和MLL, 即向上以日最高为基准，向下以75分钟最低为基准
参数:
HL:75
LL:75
公式(前半部分是显示K线的):
TMP:=OPEN-CLOSE;
DRAWLINE(TMP>0.00001,HIGH,TMP>0.00001,OPEN,COLORCYAN);
DRAWLINE(TMP>0.00001,LOW,TMP>0.00001,CLOSE,COLORCYAN);
DRAWLINE(TMP<-0.00001,HIGH,TMP<-0.00001,CLOSE,COLORRED);
DRAWLINE(TMP<-0.00001,LOW,TMP<-0.00001,OPEN,COLORRED);
DRAWLINE(ABS(TMP)<0.00001,LOW,ABS(TMP)<0.00001,OPEN,COLORWHITE);
DRAWLINE(ABS(TMP)<0.00001,HIGH,ABS(TMP)<0.00001,OPEN,COLORWHITE);
STICKLINE(TMP>0,OPEN,CLOSE,COLORCYAN,0);
STICKLINE(TMP<=0,OPEN,CLOSE,COLORRED,1);
MHH := REF(HHV(HIGH,HL),1);
MLL : REF(LLV(LOW,LL),1) + 2;
NN:=BARSLAST(DATE<>REF(DATE,1) )+1;
DH: REF(HHV(HIGH,NN),1) + 3;
DL:= REF(LLV(LOW,NN),1);

    #必然存在类似的抄底摸顶策略，但盈损方式不同. 参数取10-120分钟的一种?

todo:
极点转向法
>>> h1 = gand(rollx(sif.high,4) == tmax(sif.high,9))
>>> h11 = rollx(h1,-4)
>>> ih11 = np.where(h11)
>>> sif.time[ih11][-100:]
array([ 928,  952, 1011, 1021, 1047, 1054, 1059, 1100, 1108, 1118, 1128,
       1129, 1307, 1325, 1331, 1355, 1414, 1424, 1438, 1454, 1503, 1509,
        915,  921,  931,  946,  953,  958,  959, 1014, 1023, 1024, 1040,
       1045, 1052, 1057, 1106, 1115, 1124, 1315, 1322, 1330, 1339, 1347,
       1356, 1406, 1421, 1426, 1443, 1444, 1449,  920,  930,  935,  937,
        947,  956, 1008, 1018, 1019, 1025, 1030, 1031, 1039, 1046, 1051,
       1118, 1128, 1313, 1331, 1355, 1400, 1409, 1426, 1441, 1453, 1510,
        914,  928,  945,  948,  957, 1019, 1036, 1042, 1052, 1100, 1105,
       1120, 1126, 1306, 1312, 1321, 1326, 1346, 1355, 1409, 1427, 1438,
       1445])

>>> l1 = gand(rollx(sif.low,4) == tmin(sif.low,9))
>>> l11 = rollx(l1,-4)
>>> il11 = np.where(l11)
>>> sif.time[il11][-100:]
array([1343, 1400, 1411, 1427, 1454, 1507,  931,  945, 1003, 1012, 1013,
       1028, 1036, 1048, 1050, 1105, 1115, 1123, 1301, 1303, 1313, 1343,
       1404, 1405, 1411, 1412, 1420, 1434, 1445, 1458, 1459, 1508,  914,
        929,  940,  942,  943,  950,  951, 1009, 1036, 1046, 1051, 1102,
       1118, 1303, 1313, 1326, 1332, 1344, 1354, 1418, 1424, 1437, 1455,
       1508,  915,  925,  933,  942, 1002, 1007, 1013, 1022, 1035, 1054,
       1104, 1121, 1123, 1303, 1309, 1318, 1326, 1339, 1345, 1359, 1406,
       1419, 1431, 1436, 1448, 1459, 1506, 1514,  920,  940,  951, 1010,
       1029, 1048, 1101, 1111, 1122, 1309, 1342, 1411, 1416, 1425, 1434,
       1444])

当出现极点时，判断本极点与上一同向极点、相反方向的上两个极点以及确认位价格的关系
    如在1444处发现新点(注意，在1448结束确认)，
    此时,先判断与1425处低点的关系，低于前底, 再做下步判断
        再判断与1427/1438的高点的关系, 都小于这两个极点
        然后再判断确认位与上一低点的关系, 确认位>前底
    因此条件不满足，不开仓
    如果条件满足，则在该低点位置(或(最低+收盘)/2)开仓，并将止损设在 前高/前底的低者+1位置
    反向亦然，如1445的高点(在1449结束确认)
        先判断与前一高点的关系，大于1438高点
        再判断与1444,1434低点的关系，大于这两个低点
        最后判断确认位与上一高点的关系，高于这两个高点
    条件都满足，则于该高点(或(高点+收盘)/2处)设定开仓条件单，并将止损设在前高与前底的高者-1出




'''

from wolfox.fengine.ifuture.ibase import *
import wolfox.fengine.ifuture.iftrade as iftrade
import wolfox.fengine.ifuture.utrade as utrade
import wolfox.fengine.ifuture.fcontrol as control
from wolfox.fengine.ifuture.xfuncs import *


#主要时间过滤
def mfilter0(sif):
    return gand(
            sif.time > 1029,
            sif.time < 1500,
        )

def mfilter(sif):   
    return gand(
            sif.time > 1029,
            sif.time < 1430,
        )

def rfilter(sif):   
    return gand(
            sif.time > 1430,
        )

def afilter(sif):   
    return gand(
            sif.time > 1300,
        )

def mfilter2(sif):   
    return gand(
            sif.time > 1014,
            sif.time < 1445,
        )

def n1300filter(sif):   
    return gand(
            sif.time > 944,
            sif.time < 1300,
        )

def n1330filter(sif):   
    return gand(
            sif.time > 944,
            sif.time < 1330,
        )


def nhh(sif):
    #使用最高点+30, 也就是说必须一下拉开3点
    #ldlow = dnext(sif.lowd/2+sif.closed/2,sif.close,sif.i_cofd)
    ldlow = dnext(sif.lowd,sif.close,sif.i_cofd)
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    thigh = rollx(sif.dhigh+20)
    signal = gand(
            #cross(rollx(sif.dhigh+30),sif.high)>0
            sif.high > thigh,
            rollx(sif.dhigh) > ldlow + 10,     #大于昨日低点
        )
    return np.select([signal],[gmax(sif.low,thigh)],0)    #避免跳空情况，如果跳空且大于突破点，就以最低价进入
    
def nll2(sif):
    #使用最低点
    ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)    
    return gand(
            #cross(rollx(sif.dlow-30),sif.low)<0
            sif.low < rollx(sif.dlow+20,3), #比close要小点
            sif.low < ldhigh,
        )
    
def nx2000X(sif):
    return gand(
                sif.xatr < 2000,
                sif.xatr30x < 10000,
                sif.xatr5x< 4000,
           )

def nx2500X(sif):
    return gand(
                sif.xatr < 2500,
                sif.xatr30x < 10000,
                sif.xatr5x< 4000,
           )

def nlhh(sif):
    #使用最高点+30, 也就是说必须一下拉开3点
    ldlow = dnext(sif.lowd,sif.close,sif.i_cofd)
    return gand(
            #cross(rollx(sif.dhigh+30),sif.high)>0
            cross(sif.ldhigh+50,sif.high)>0,
        )

def cgap(sif):
    #补缺口
    #ldhigh = dnext(sif.closed,sif.close,sif.i_cofd)
    ldhigh = np.select([sif.time==1514],[tmax(sif.high,3)],0)
    ldhigh =extend2next(ldhigh)
            
    lopen = dnext(sif.opend,sif.close,sif.i_oofd)
    return gand(
            #cross(rollx(sif.dhigh+30),sif.high)>0
            lopen > ldhigh,
            cross(sif.ldhigh+20,sif.close)>0,
            sif.time > 919,
        )



break_nhh = BXFuncA(fstate=gofilter,fsignal=nhh,fwave=nx2500X,ffilter=nfilter)  ##选择
break_nhh.name = u'向上突破新高'
hbreak_nhh = BXFuncA(fstate=gofilter,fsignal=nhh,fwave=nx2500X,ffilter=mfilter)  ##主要时段
hbreak_nhh.name = u'日内向上突破新高'

break_nlhh = BXFuncA(fstate=gofilter,fsignal=nlhh,fwave=nx2500X,ffilter=nfilter)  ##选择
hbreak_nlhh = BXFuncA(fstate=gofilter,fsignal=nlhh,fwave=nx2500X,ffilter=efilter2)  ##主要时段

break_cgap = BXFuncF1(fstate=gofilter,fsignal=cgap,fwave=nx2500X,ffilter=e1400filter)  ##选择
hbreak_cgap = BXFuncF1(fstate=gofilter,fsignal=cgap,fwave=nx2500X,ffilter=efilter2)  ##主要时段

def sdown(sif):
    return gand(
            sif.t120 < 80,
            #sif.t120 < -200,    #周期为1个月，末期会不明,有点太投机
        )

def sup(sif):
    return gand(
            sif.t120 < 200, #200均可 这个有点太投机
            #sif.s30>0,
        )

sbreak_nll2 = SXFuncA(fstate=sdown,fsignal=nll2,fwave=nx2500X,ffilter=nfilter)    #这个R高，但是次数少
sbreak_nll2.name = u'向下突破2'
shbreak_nll2 = SXFuncA(fstate=sdown,fsignal=nll2,fwave=nx2500X,ffilter=mfilter)    #

#sbreak_nlc + sbreak_nlc_break = sbreak_nll2


zbreak = [break_nhh,sbreak_nll2] #这个最好,理念最清晰

zhbreak = [hbreak_nhh,shbreak_nll2]

###时间低点突破
def mll2(sif,length=75):
    #使用最低点
    tlow = rollx(tmin(sif.low,length)+20)
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    #ldmid = dnext((sif.highd+gmin(sif.closed,sif.opend))/2,sif.close,sif.i_cofd)
    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    #ldmid = dnext((sif.highd+sif.closed)/2,sif.close,sif.i_cofd)    
    signal = gand(
            #sif.time>1029,
            cross(tlow,sif.low)<0,
            #sif.low < tlow,
            #tlow < rollx(sif.dhigh + sif.dlow)/2, #+ sif.dlow
            #tlow < ldhigh-10,  #比昨日最高价低才允许做空
            tlow < ldmid-sif.xatr*2/XBASE,  #比前2天高点中点低才允许做空            
        )
    return np.select([signal],[gmin(sif.open,tlow)],0)    #避免跳空情况，如果跳空且大于突破点，就以最低价进入
    

sbreak_mll2 = SXFuncA(fstate=sdown,fsignal=mll2,fwave=nx2500X,ffilter=nfilter)    #优于nll

#主要时段
shbreak_mll2 = SXFuncA(fstate=sdown,fsignal=mll2,fwave=nx2500X,ffilter=mfilter)    #优于nll
shbreak_mll2.name = u'日内75分钟向下突破'

##下跌采用75分钟的底部+2, 上涨采用日顶部+3(均在10:30-14:30)
hbreak = [shbreak_mll2,break_nhh]  #利润比较好
hbreak2 = [shbreak_mll2,hbreak_nhh]  #这个最大回撤最小      #####################采用此个

##突破前一日高/低点
def bru(sif):
    #突破前一日高点
    ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    signal = gand(
            sif.high > ldhigh,
            rollx(sif.dhigh) < ldhigh +60,  #还没拉开过
            sif.sk > sif.sd,
            sif.time < 1330,
            #sif.r120>0,
        )
    return np.select([signal],[gmax(sif.open,ldhigh)],0)    #避免跳空情况，如果跳空且大于突破点，就以最低价进入


def brux(sif):
    #突破前一日高点
    ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    return gand(
            cross(ldhigh,sif.high+30)>0,
            #sif.sk > sif.sd,
            sif.s1>0,
            sif.time < 1300,
            #sif.r120>0,
        )


def brd(sif):
    ldlow = dnext(sif.lowd,sif.close,sif.i_cofd)
    signal = gand(
            sif.low < ldlow +20,  
            rollx(sif.dlow) < ldlow -100,    #已经下去过了之后，再穿越. 这个被部分吸收了
            sif.sk < sif.sd,
            sif.time < 1430,
            #sif.r120<20,
            sif.t120<60,
        )
    return np.select([signal],[gmin(sif.open,ldlow+20)],0)    #避免跳空情况，如果跳空且大于突破点，就以分钟开盘价进入

def brdh(sif):
    #最高价低于前日最低价+20，则以收盘价买入
    ldlow = dnext(sif.lowd,sif.close,sif.i_cofd)
    signal = gand(
            sif.high < ldlow +20,   #这个有点无耻,走的不是突破了
            rollx(sif.dlow) < ldlow -100,    #已经下去过了之后，再穿越. 这个被部分吸收了
            sif.sk < sif.sd,
            sif.time < 1430,
            #sif.r120<20,
        )
    return np.select([signal],[sif.close],0)    #避免跳空情况，如果跳空且大于突破点，就以分钟开盘价进入
    
#前日突破
dbreakb = BXFuncD1(fstate=gofilter,fsignal=bru,fwave=nx2500X,ffilter=efilter)
dbreakb.name = u'突破前日高点'
dbreakb.lastupdate = 20101213

dbreakbx = BXFuncD1(fstate=gofilter,fsignal=brux,fwave=nx2000X,ffilter=efilter)

dbreaks = SXFuncD1(fstate=gofilter,fsignal=brd,fwave=nx2500X,ffilter=efilter)
dbreaksh = SXFuncD1(fstate=gofilter,fsignal=brdh,fwave=nx2500X,ffilter=efilter)
dbreaks.name = u'突破前日低点'
dbreakb.lastupdate = 20101213
dbreak = [dbreakb,dbreaks]

dbreaksh.stop_closer = utrade.atr5_ustop_V

def dhigh_last(sif):
    drep = crepeat(sif.dhigh)
    dindex = np.nonzero(gand(drep>5,drep>rollx(drep,-1)))  #
    ldhigh = np.zeros_like(sif.dhigh)
    ldhigh[dindex] = sif.dhigh[dindex]
    sif.ldhigh=extend2next(ldhigh)


def u123(sif):
    #向上123

    plen = 4
    alen = 2*plen+1

    chh = gand(rollx(sif.high,plen) == tmax(sif.high,alen))
    cll = gand(rollx(sif.low,plen) == tmin(sif.low,alen))
    
    phh = np.select([chh],[rollx(sif.high,plen)],0)
    pll = np.select([cll],[rollx(sif.low,plen)],0)


    #pchh = np.select([chh],[sif.close],0)
    #pcll = np.select([cll],[sif.close],0)

    shh = extend2next(ssub(phh))
    sll = extend2next(ssub(pll))

    lhh = extend2next(phh)
    lll = extend2next(pll)

    #lpchh = extend2next(pchh)
    #lpcll = extend2next(pcll)

    rlhh = rollx(lhh+50)    #连续上去，没出现新的极点

    signal = gand(shh>0,
                sll>0,
                tmin(sif.low,4)>lll,
                cross(rlhh,sif.high)>0,
                strend2(sif.ma120)>0,
                sif.sdma>0,
            )
    return np.select([signal],[rlhh],0)

def d123(sif):
    #向下123

    plen = 4
    alen = 2*plen+1


    chh = gand(rollx(sif.high,plen) == tmax(sif.high,alen))
    cll = gand(rollx(sif.low,plen) == tmin(sif.low,alen))
    
    phh = np.select([chh],[rollx(sif.high,plen)],0)
    pll = np.select([cll],[rollx(sif.low,plen)],0)


    #pchh = np.select([chh],[sif.close],0)
    #pcll = np.select([cll],[sif.close],0)

    shh = extend2next(ssub(phh))
    sll = extend2next(ssub(pll))

    lhh = extend2next(phh)
    lll = extend2next(pll)

    #lpchh = extend2next(pchh)
    #lpcll = extend2next(pcll)

    rlll = rollx(lll-80)

    signal = gand(shh<0,
                sll<0,
                tmax(sif.high,4)<lhh,
                cross(rlll,sif.close)<0,
            )
    return np.select([signal],[sif.close],0)

def d123a(sif):
    #向下123

    plen = 4
    alen = 2*plen+1

    chh = gand(sif.high == tmax(sif.high,alen))
    cll = gand(rollx(sif.low,plen) == tmin(sif.low,alen))
    
    phh = np.select([chh],[sif.high],0)
    pll = np.select([cll],[rollx(sif.low,plen)],0)

    shh = extend2next(ssub(phh))
    sll = extend2next(ssub(pll)) #如果最低点连续，则因为相减为0，相当于只有一个最低点

    lhh = extend2next(phh)
    lll = extend2next(pll)

    rlll = rollx(lll)

    signal = gand(shh<0,
                #sll<0,
                #tmax(sif.high,4)<lhh,
                cross(rlll,sif.low)<0,
            )
    return np.select([signal],[rlll],0)

def u123a(sif):
    #向上123

    plen = 4
    alen = 2*plen+1

    chh = gand(rollx(sif.high,plen) == tmax(sif.high,alen))
    cll = gand(rollx(sif.low,plen) == tmin(sif.low,alen))
    
    phh = np.select([chh],[rollx(sif.high,plen)],0)
    pll = np.select([cll],[rollx(sif.low,plen)],0)

    shh = extend2next(ssub(phh))
    sll = extend2next(ssub(pll))

    lhh = extend2next(phh)
    lll = extend2next(pll)

    signal = gand(#shh>0,
                sll>0,
                tmin(sif.low,4)>lll,
                #cross(rollx(lll),sif.low)>0,
                sif.low > rollx(lll),
            )
    return np.select([signal],[sif.close],0)


b123 = BXFunc(fstate=gofilter,fsignal=u123,fwave=nx2500X,ffilter=n1430filter)
b123.name = u'向上123'
b123.lastupdate = 20101222
b123.stop_closer = utrade.atr5_ustop_V

s123 = SXFunc(fstate=gofilter,fsignal=d123,fwave=nx2500X,ffilter=nfilter)
s123.name = u'向下123'
s123.lastupdate = 20101222
s123.stop_closer = utrade.atr5_ustop_V

s123a = SXFunc(fstate=gofilter,fsignal=d123a,fwave=nx2500X,ffilter=nfilter)
s123a.name = u'向下123'
s123a.lastupdate = 20101222
s123a.stop_closer = utrade.atr5_ustop_V

b123a = BXFuncD1(fstate=gofilter,fsignal=u123a,fwave=nx2500X,ffilter=nfilter)
b123a.name = u'向上123a'
b123a.lastupdate = 20101222
b123a.stop_closer = utrade.atr5_ustop_V

break123 = [b123,s123]  #整体上缺乏合成性


####添加老系统
wxxx = [xds,xdds3,k5_d3b,xuub,K1_DDD1,K1_UUX,K1_RU,Z5_P2,xmacd3s,xup01,ua_fa,FA_15_120,K1_DVB,K1_DDUU,K1_DVBR]

#wxxx_s = [xds,xdds3,k5_d3b,K1_DDD1,Z5_P2,xmacd3s,FA_15_120]
#wxxx_b = [xuub,K1_UUX,K1_RU,xup01,ua_fa,K1_DDUU]
#wxxx_b2 = [K1_DVB,K1_DVBR]

wxxx_s = [xds,k5_d3b,Z5_P2,xmacd3s,FA_15_120]
wxxx_b = [xuub,xup01,K1_DDUU,K1_RU,ua_fa]
wxxx_b2 = [K1_DVB,K1_DVBR]


#wxss = CSFuncF1(u'向下投机组合',*wxxx_s)
#wxbs = CBFuncF1(u'向上投机组合',*wxxx_b)
#wxb2s = CBFuncF1(u'向上投机组合2',*wxxx_b2)

ctest = CFunc(u'CTEST',xuub)

wxss = CFunc(u'向下投机组合',*wxxx_s)
wxbs = CFunc(u'向上投机组合',*wxxx_b)
wxb2s = CFunc(u'向上投机组合2',*wxxx_b2)

wxfs = [wxss,wxbs,wxb2s]

#xxx = zbreak

xxx = hbreak2 + dbreak + break123

#txfs = [xds,k5_d3b,xuub,K1_DDD1,K1_UUX,K1_RU,Z5_P2,xmacd3s,xup01,ua_fa,FA_15_120,K1_DVB,K1_DDUU,K1_DVBR]
txfs = [xds,xuub,K1_RU,xup01,FA_15_120,K1_DVBR,Z5_P2,k5_d3b,xmacd3s,ua_fa,K1_DVB]   #剔除xdds3,K1_UUX,K1_DDD1
#K1_DDUU样本数太少，要观察

txxx = hbreak2 + txfs

xxx2 = xxx +wxfs #+ wxxx

'''
各组合及其分子的累计收益，发现4/6/8加成收益不大，7/12负收益，5/9/10/11加成收益10%以上
xxx2        hbreak2     wxfa
12:156      100         416
11:6370     3588        4010
10:4364     2238        3954
9:1481      502         1218
8:1444      504         1316
7:2070      1634        2414
6:3184      2542        3050
5:7174      4750        6552
4:3936      2191        3932

'''


for x in xxx2+wxxx:
    #x.stop_closer = iftrade.atr5_uxstop_kF #60/120       
    #x.stop_closer = iftrade.atr5_uxstop_kQ #10/120       
    #x.stop_closer = iftrade.atr5_uxstop_kV #60/120/333
    x.stop_closer = utrade.atr5_ustop_V
    #x.stop_closer = utrade.atr5_ustop_W1
    x.cstoper = iftrade.F60  #初始止损,目前只在动态显示时用
    if 'lastupdate' not in x.__dict__:
        x.lastupdate = 20101209
    
