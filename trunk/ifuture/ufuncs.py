# -*- coding: utf-8 -*-


'''
2011-01操作指南
#################################
信号切换规则:
    持仓时出现反向信号，当浮动收益大于25或小于3时，平仓并开新仓，否则不变

xbreak系列，连续两次突破后，放宽突破的界限，即延缓突破
    顶/底均以6分钟计，即13分钟高/低点
    开仓:
        做多:   1. 突破上一高点+0.6点处.
                2. 距底部>15点
                3. xatr>800
                4. 底部抬高，或者2分钟底部比5分钟底部高
                5. 30分钟连续第三次突破时，从0.6点抬高到8个点
                6. 9.45之后，如果开仓点HPEAK5接近日内高点8个点内，则不动作
                   注意，连续突破时，HPEAK5并不直接跟上，此时是否突破，看的是上一个顶点
        做空:   1. 突破上一低点+0.2点处
                2. 30分钟连续第三次突破时，从+0.2点放低到-5个点        
                3. 突破基准线低于前日高点或今天开盘
                4. 如果开仓点LPEAK5接近日内低点10个点内，则不动作
                5. xatr<2500,xatr5x<4000,xatr30x<10000

    平仓:
        止损为4, 保本为8
    工作时段:
        [916,934]+[1032,1429]

hbreak2系列
    开仓:
        做多: 1. 高点在一分钟内拉高到日内高点+3处
              2. 日内高点>昨日低点+1
              3. xatr<2500,xatr5x<4000,xatr30x<10000
        做空: 1. 低点小于75分钟低点+2处
              2. 比前两天的高点中点高2个xatr(或3点)
              3. xatr<2500,xatr5x<4000,xatr30x<10000
    平仓:
        止损为6，保本为8
    工作时段: [1032,1429]

dbreak系列，只取第一次
    开仓:
        做多: 1.当前最高<昨日高点+6
              2.sk>sd
              3.开仓点为 high > 昨日最高处
              4. xatr<2500,xatr5x<4000,xatr30x<10000
        做空: 1.最低<昨日低点 -10
              2.sk<sd
              3.开仓点为 low > 昨日最低+2处
              4. xatr<2500,xatr5x<4000,xatr30x<10000
    平仓:
        止损为6，保本为8
    工作时段:
        买多:[915,1329]
        做空:[915,1429]

    

###############################
突破系统
    当出现信号开仓后，如果未平仓前出现第二个信号，则止损要按照这几个信号最宽的一个来放
    L: 0.018手续费

实盘中的几点注意
1. 止损
   a.止损的ATR是根据上一完整周期的5分钟ATR设置的，不是本5分钟的，这一点需要非常注意
   b.当连续创新高或新低时，止损点未必上移或下移，这个取决于ATR5的变化，很可能新高点因为ATR5变大导致
        新计算的止损点不如上一止损点, 从而不移动. 这个必须仔细。
   c.止损价位必须根据文华软件中的柱线的高低价来设定，而不是汇总中的日最高/最低价，目的是与系统保持一致
   d.如果还来不及移动止损，就被打穿新止损位，而老止损位未被打穿，那就按现价出掉。也可于新止损处收窄1-2个点重新设定
2. 开仓时的保护性止损设置
   开仓当分钟，止损先设为4, 下分钟之后改为3 
3. 收盘规则
   以15:00开盘价为基准，做空放宽到+5，做多放宽到-5，如果触及止损，则以止损为计
   15:10之后，收窄到15:10开盘价+3/-3


系统测试时的注意点
1. 为什么两个好的策略，叠加起来的效果比较差，有时比单个还差 
   因为好策略的盈利交易，因为其持仓时间通常较长，所以覆盖的可能性比较高，而亏损交易因为持仓较短，所以通常不互相覆盖
   从而导致叠加时盈利互相覆盖亏损各自独立，引起集成效果差


突破法列举:
    1. 当日突破
    2. 突破前一日高点
    3. 突破当日的前一个高点

突破确认类操作
    如果突破当时没用条件单开仓，而突破后价格回落，但未触及止损
    则此时可于突破位-1开条件单，下次突破后再开仓，或者到止损位后撤销条件单
    因为胜率<50%，以条件单续开放式为佳，不建议逆向运转后优势追开


##前期高点的处理
对于连续高点，如果后一个高点只是比前一个高点低2个点以内，则仍按前一个高点算

##测试高点后突破前面一个低点/或者先形成一个低点，然后突破它
##测试低点后突破前面一个高点/或者先形成一个高点，然后突破它
##注意在时间和空间上保持一定距离，尤其是空间上

发现一个诡异现象
    10/15/30整的时间，多数有暴涨暴跌动作发生
    可以根据之前2分钟的动量来判断. 如果方向一致且第-1分钟的收盘方向与运动方向一致(即便阴阳线不一致，
            比如下跌后拉回也算是上升方向). 则同方向开仓
        如果是孕线，判断第-1分钟方向和与-1收盘价与-3分钟的方向

        -1分钟方向判断: 收盘价与最高价和最低价的关系，如果最高-收盘>收盘-最低, 则为向下，反之为向上
    开仓在-1分钟收盘,止损价-3
    如果进入突破区间，则跟随突破规则止损

10:30前的操作规则:
    顺t120? 还是r120/60/30?

AMM的操作方法
    1. 围绕开盘价1-10个点，以2个点左右为多
    2. 10.00后开仓
    3. 第一次开仓观察当前价与前一日实体的关系，在中部以下则开空，以上则开多


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
            sif.time > 1031,
            sif.time < 1430,
        )

def mfilter2(sif):   
    return gand(
            sif.time > 1014,
            sif.time < 1445,
        )

def mfilter2a(sif):   
    return gand(
            sif.time > 1031,
            sif.time < 1445,
        )

def mfilter1a(sif):   
    return gand(
            sif.time > 1001,
            sif.time < 1331,
        )

def mfilter3(sif):   
    return gor(
            gand(
                sif.time > 1031,
                sif.time < 1430,
            ),
            sif.time < 935,
        )

def mfilter4(sif):   
    return gand(
            sif.time > 1114,
            sif.time < 1430,
        )


def rmfilter(sif):   
    return gor(
            sif.time < 1029,
        )


def kfilter(sif):
    return gand(
            sif.time > 929,
            sif.time < 1000,
        )

def ekfilter(sif):
    return gand(
            sif.time > 914,
            sif.time < 945,
        )

def ekfilter2(sif):
    return gor(
            gand(sif.time>929,sif.time < 1000),
            gand(sif.time>1130,sif.time<1330),
        )

def ekfilter3(sif):
    return gand(
            sif.time > 914,
            sif.time < 920,
        )


def rfilter(sif):   
    return gand(
            sif.time > 1430,
        )

def afilter(sif):   
    return gand(
            sif.time > 1300,
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


def nhh(sif,vbreak=30):
    #使用最高点+20, 也就是说必须一下拉开3点
    #ldlow = dnext(sif.lowd/2+sif.closed/2,sif.close,sif.i_cofd)
    ldlow = dnext(sif.lowd,sif.close,sif.i_cofd)
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    thigh = rollx(sif.dhigh+vbreak)
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
    xx = gand(
                sif.xatr < 2000,
                sif.xatr30x < 10000,
                sif.xatr5x< 4000,
           )
    return rollx(xx)

def nx2500X(sif):
    xx = gand(
                sif.xatr < 2500,
                sif.xatr30x < 10000,
                sif.xatr5x< 4000,
           )
    return rollx(xx)

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

dhbreak_nhh = BXFuncD1(fstate=gofilter,fsignal=nhh,fwave=nx2500X,ffilter=mfilter4)  ##主要时段
dhbreak_nhh.name = u'日内向上突破新高'
dhbreak_nhh.stop_closer = utrade.atr5_ustop_V

break_nlhh = BXFuncA(fstate=gofilter,fsignal=nlhh,fwave=nx2500X,ffilter=nfilter)  ##选择
hbreak_nlhh = BXFuncA(fstate=gofilter,fsignal=nlhh,fwave=nx2500X,ffilter=efilter2)  ##主要时段

break_cgap = BXFuncF1(fstate=gofilter,fsignal=cgap,fwave=nx2500X,ffilter=e1400filter)  ##选择
hbreak_cgap = BXFuncF1(fstate=gofilter,fsignal=cgap,fwave=nx2500X,ffilter=efilter2)  ##主要时段

def sdown(sif):
    return gand(
            sif.t120 < 180,
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

skbreak_nll2 = SXFuncD1(fstate=sdown,fsignal=nll2,fwave=nx2500X,ffilter=kfilter)    #
#skbreak_nll2.stop_closer = utrade.atr5_ustop_V

#sbreak_nlc + sbreak_nlc_break = sbreak_nll2


zbreak = [break_nhh,sbreak_nll2] #这个最好,理念最清晰

zhbreak = [hbreak_nhh,shbreak_nll2]

###
def mhh2(sif,length=20):
    #使用最低点
    thigh = rollx(tmax(sif.high,length))
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    #ldmid = dnext((sif.highd+gmin(sif.closed,sif.opend))/2,sif.close,sif.i_cofd)
    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    #ldmid = dnext((sif.highd+sif.closed)/2,sif.close,sif.i_cofd)    
    signal = gand(
            #sif.time>1029,
            cross(thigh,sif.high)<0,
            #sif.low < tlow,
            #tlow < rollx(sif.dhigh + sif.dlow)/2, #+ sif.dlow
            #tlow < ldhigh-10,  #比昨日最高价低才允许做空
            #thigh > ldmid+sif.xatr*2/XBASE,  #比前2天高点中点低才允许做空            
        )
    return np.select([signal],[gmin(sif.open,thigh)],0)    #避免跳空情况，如果跳空且大于突破点，就以最低价进入


###时间低点突破
def mll2(sif,length=75,vbreak=20):
    #使用最低点
    tlow = gmin(rollx(tmin(sif.low,length)+vbreak))
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    #ldmid = dnext((sif.highd+gmin(sif.closed,sif.opend))/2,sif.close,sif.i_cofd)
    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)            
    #ldmid = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)        
    #ldmid = dnext(sif.highd,sif.close,sif.i_cofd)        
    #ldmid = dnext((sif.highd+sif.closed)/2,sif.close,sif.i_cofd)    
    signal = gand(
            #sif.time>1029,
            cross(tlow,sif.low)<0,
            #sif.low < tlow,
            #tlow < rollx(sif.dhigh + sif.dlow)/2, #+ sif.dlow
            #tlow < ldhigh-10,  #比昨日最高价低才允许做空
            tlow < ldmid-30,#rollx(sif.xatr)*2/XBASE,  #比前2天高点中点低才允许做空
        )
    return np.select([signal],[gmin(sif.open,tlow)],0)    #避免跳空情况，如果跳空且大于突破点，就以最低价进入
    
def mll3(sif,length=75):
    #使用最低点
    tlow = gmin(rollx(tmin(sif.low,length)+20))
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    #ldmid = dnext((sif.highd+gmin(sif.closed,sif.opend))/2,sif.close,sif.i_cofd)
    ldlow = dnext(sif.lowd,sif.close,sif.i_cofd)    
    #ldmid = dnext((sif.highd+sif.closed)/2,sif.close,sif.i_cofd)    
    signal = gand(
            #sif.time>1029,
            cross(tlow,sif.low)<0,
            #sif.low < tlow,
            #tlow < rollx(sif.dhigh + sif.dlow)/2, #+ sif.dlow
            #tlow < ldhigh-10,  #比昨日最高价低才允许做空
            tlow < ldlow,
        )
    return np.select([signal],[gmin(sif.open,tlow)],0)    #避免跳空情况，如果跳空且大于突破点，就以最低价进入


sbreak_mll2 = SXFuncA(fstate=sdown,fsignal=mll2,fwave=nx2500X,ffilter=nfilter)    #优于nll
bbreak_mhh2 = BXFuncA(fstate=gofilter,fsignal=mhh2,fwave=nx2500X,ffilter=nfilter)    #优于nll

#主要时段
shbreak_mll2 = SXFuncA(fstate=sdown,fsignal=mll2,fwave=nx2500X,ffilter=mfilter)    #优于nll
shbreak_mll2.name = u'日内75分钟向下突破'

shbreak_mll_30 = SXFuncD1(fstate=sdown,fsignal=fcustom(mll2,length=30),fwave=nx2000X,ffilter=kfilter)    #优于nll
shbreak_mll_30.name = u'日内30分钟向下突破'
shbreak_mll_30.stop_closer = utrade.atr5_ustop_V

shbreak_mll3 = SXFuncA(fstate=sdown,fsignal=mll3,fwave=nx2500X,ffilter=ekfilter)    #优于nll
shbreak_mll3.name = u'日内75分钟向下突破3'
shbreak_mll3.stop_closer = utrade.atr5_ustop_V


dshbreak_mll2 = SXFuncD1(fstate=sdown,fsignal=mll2,fwave=nx2500X,ffilter=mfilter4)    #优于nll
dshbreak_mll2.name = u'日内75分钟向下突破d'
dshbreak_mll2.stop_closer = utrade.atr5_ustop_V

##moontage
mhbreak_mll2 = SXFuncA(fstate=gofilter,fsignal=fcustom(mll2,length=75,vbreak=0),fwave=nx2500X,ffilter=mfilter)    #优于nll
mhbreak_nhh = BXFuncA(fstate=gofilter,fsignal=fcustom(nhh,vbreak=30),fwave=nx2500X,ffilter=mfilter)    #优于nll
mhbreak_mll2.stop_closer = utrade.atr5_ustop_V
mhbreak_nhh.stop_closer = utrade.atr5_ustop_V
mhbreak = [mhbreak_mll2,mhbreak_nhh]


##下跌采用75分钟的底部+2, 上涨采用日顶部+3(均在10:30-14:30)
hbreak = [shbreak_mll2,break_nhh]  #利润比较好
hbreak2 = [shbreak_mll2,hbreak_nhh]  #这个最大回撤最小      #####################采用此个

d1_hbreak = [dhbreak_nhh,dshbreak_mll2]

##突破前一日高/低点
def bru(sif):
    #突破前一日高点
    ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    signal = gand(
            sif.high > ldhigh,
            rollx(sif.dhigh) < ldhigh +60,  #还没拉开过, 如果是915则必然满足
            sif.sk > sif.sd,
            sif.time < 1330,
            #sif.time>915,
            #sif.r120>0,
        )
    return np.select([signal],[gmax(sif.open,ldhigh)],0)    #避免跳空情况，如果跳空且大于突破点，就以最低价进入

def bru2(sif):
    #突破前一日高点
    ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    signal = gand(
            sif.high > ldhigh,
            rollx(sif.dhigh) < ldhigh +60,  #还没拉开过, 如果是915则必然满足
            sif.sk > sif.sd,
            sif.time < 1330,
            #sif.time>915,
            #sif.r120>0,
        )
    return np.select([signal],[gmax(sif.open,ldhigh)],0)    #避免跳空情况，如果跳空且大于突破点，就以最低价进入


def brux(sif):
    #突破前一日高点
    ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    tp = ldhigh - 20
    signal =  gand(
            cross(tp,sif.low)>0,
            #sif.sk > sif.sd,
            #sif.s1>0,
            sif.time < 1330,
            sif.time > 1000,
            #sif.r120>0,
        )
    #return np.select([signal],[gmax(sif.open,tp)],0)
    return signal


def brd(sif):
    ldlow = dnext(sif.lowd,sif.close,sif.i_cofd)
    signal = gand(
            sif.low < ldlow +20,  
            rollx(sif.dlow) < ldlow-100,    #已经下去过了之后，再穿越. 这个被部分吸收了
            sif.sk < sif.sd,
            sif.time < 1430,
            #sif.time>915,
            #sif.t120<60,
        )
    return np.select([signal],[gmin(sif.open,ldlow+20)],0)    #避免跳空/skdj后延情况，如果跳空且大于突破点，就以分钟开盘价进入

def brdh(sif):
    #最高价低于前日最低价+20，则以收盘价买入
    ldlow = dnext(sif.lowd,sif.close,sif.i_cofd)
    signal = gand(
            sif.high < ldlow +20,   #这个有点无耻,走的不是突破了, 就是说等最高价低于昨日最低+20才在收盘进入
            rollx(sif.dlow) < ldlow -100,    #已经下去过了之后，再穿越. 这个被部分吸收了
            sif.sk < sif.sd,
            sif.time < 1430,
            #sif.r120<20,
        )
    return np.select([signal],[sif.close],0)    
    
#前日突破
dbreakb = BXFuncD1(fstate=gofilter,fsignal=bru,fwave=nx2500X,ffilter=efilter)
dbreakb.name = u'突破前日高点'
dbreakb.lastupdate = 20101213

dbreakbx = BXFuncD1(fstate=gofilter,fsignal=brux,fwave=nx2000X,ffilter=efilter)

dbreaks = SXFuncD1(fstate=sdown,fsignal=brd,fwave=nx2500X,ffilter=efilter)
dbreaksh = SXFuncD1(fstate=gofilter,fsignal=brdh,fwave=nx2500X,ffilter=efilter)
dbreaks.name = u'突破前日低点'
dbreakb.lastupdate = 20101213
dbreak = [dbreakb,dbreaks]#
dbreaksh.stop_closer = utrade.atr5_ustop_V

dbreakb2 = BXFuncD1(fstate=gofilter,fsignal=brux,fwave=nx2500X,ffilter=efilter)
dbreakb2.name = u'突破前日高点'
dbreakb2.lastupdate = 20101213
dbreakb2.stop_closer = utrade.atr5_ustop_V1


def u123(sif):
    #向上123

    plen = 5
    alen = 2*plen+1

    chh = gand(rollx(sif.high,plen) == tmax(sif.high,alen))
    cll = gand(rollx(sif.low,plen) == tmin(sif.low,alen))
    
    phh = np.select([chh],[rollx(sif.high,plen)],0)
    pll = np.select([cll],[rollx(sif.low,plen)],0)

    pphh = extend2next(phh)
    ppll = extend2next(pll)

    #pchh = np.select([chh],[sif.close],0)
    #pcll = np.select([cll],[sif.close],0)

    shh = extend2next(ssub(phh))
    sll = extend2next(ssub(pll))

    lhh = extend2next(phh)
    lll = extend2next(pll)

    #lpchh = extend2next(pchh)
    #lpcll = extend2next(pcll)

    rlhh = rollx(lhh+50)    #连续上去，没出现新的极点

    signal = gand(shh>-10,
                sll>0,#上次允许是微弱失败尝试
                tmin(rollx(sif.low),4)>lll,
                #pphh - ppll < 120,                
                cross(rlhh,sif.high)>0,
                rollx(sif.sdma)>0,
                #sif.high > rollx(tmax(sif.high,20)),
                #rollx(strend2(sif.ma120))>0,
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


    pchh = np.select([chh],[sif.low],0)
    pcll = np.select([cll],[sif.high],0)

    shh = extend2next(ssub(phh))
    sll = extend2next(ssub(pll))

    pphh = extend2next(phh)
    ppll = extend2next(pll)

    lhh = extend2next(phh)
    lll = extend2next(pll)

    lpchh = extend2next(pchh)
    lpcll = extend2next(pcll)

    rlll = rollx(lll)
    rhhh = rollx(lhh)

    signal = gand(shh<0,
                sll<10, #上次允许是微弱失败尝试
                #rollx(pphh - ppll) < 120,
                #tmax(rollx(sif.high),5)<lhh,    #前1分钟没有创新高
                cross(rlll,sif.low)<0,
                rollx(sif.r30)<0,
            )
    return np.select([signal],[rlll],0)

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

def u123b(sif):
    #向上123后，退回到前高,突破后买入,这个合并效果好

    plen = 6
    alen = 2*plen+1

    chh = gand(rollx(sif.high,plen) == tmax(sif.high,alen))
    cll = gand(rollx(sif.low,plen) == tmin(sif.low,alen))
    
    phh = np.select([chh],[rollx(sif.high,plen)],0)
    pll = np.select([cll],[rollx(sif.low,plen)],0)

    pphh = extend2next(phh)
    ppll = extend2next(pll)

    #pchh = np.select([chh],[sif.close],0)
    #pcll = np.select([cll],[sif.close],0)

    shh = extend2next(ssub(phh))
    sll = extend2next(ssub(pll))

    lhh = extend2next(phh)
    lll = extend2next(pll)

    #lpchh = extend2next(pchh)
    #lpcll = extend2next(pcll)

    rlhh = rollx(lhh)    #连续上去，没出现新的极点

    iphh = np.nonzero(phh)
    rphh = np.zeros_like(phh)
    rphh[iphh] = rollx(phh[iphh])
    rphh = extend2next(rphh) +10

    tp = gmin(rphh,lhh+10)

    signal = gand(#shh>0,
                sll>=0,#
                cross(tp,sif.high)>0,
                #rollx(sif.sdma)>0,
                strend2(rollx(sif.ma10))>0,
                rollx(sif.ma10)>rollx(sif.ma30),
                rollx(sif.ma5)>rollx(sif.ma13),
                strend2(sif.mxatr30x)>0,
            )
    return np.select([signal],[tp],0)

def d123b(sif):
    #向下123后，退回到前低上，突破后开空,这个合并效果好

    plen = 6
    alen = 2*plen+1

    chh = gand(rollx(sif.high,plen) == tmax(sif.high,alen))
    cll = gand(rollx(sif.low,plen) == tmin(sif.low,alen))
    
    phh = np.select([chh],[rollx(sif.high,plen)],0)
    pll = np.select([cll],[rollx(sif.low,plen)],0)

    pphh = extend2next(phh)
    ppll = extend2next(pll)

    #pchh = np.select([chh],[sif.close],0)
    #pcll = np.select([cll],[sif.close],0)

    shh = extend2next(ssub(phh))
    sll = extend2next(ssub(pll))

    lhh = extend2next(phh)
    lll = extend2next(pll)

    #lpchh = extend2next(pchh)
    #lpcll = extend2next(pcll)

    rlhh = rollx(lhh)    #连续上去，没出现新的极点

    iphh = np.nonzero(phh)
    rphh = np.zeros_like(phh)
    rphh[iphh] = rollx(phh[iphh])
    rphh = extend2next(rphh) +10

    #print rphh[-100:]
    ipll = np.nonzero(pll)
    rpll = np.zeros_like(pll)
    rpll[ipll] = rollx(pll[ipll])
    rpll = extend2next(rpll) + 20


    tp = gmin(rpll,lll+20)#,rollx(tmin(sif.low,60))+20)

    signal = gand(#shh<20,
                cross(tp,sif.low)<0,
                #strend2(sif.mxatr30x)<0,
                #sif.low > sif.dlow + 150,
            )
    return np.select([signal],[tp])

def u2b(sif):
    #向上2b，是中期逆势

    plen = 3
    alen = 2*plen+1

    chh = gand(rollx(sif.high,plen) == tmax(sif.high,alen))
    cll = gand(rollx(sif.low,plen) == tmin(sif.low,alen))
    
    phh = np.select([chh],[rollx(sif.high,plen)],0)
    pll = np.select([cll],[rollx(sif.low,plen)],0)

    pphh = extend2next(phh)
    ppll = extend2next(pll)

    #pchh = np.select([chh],[sif.close],0)
    #pcll = np.select([cll],[sif.close],0)

    shh = extend2next(ssub(phh))
    sll = extend2next(ssub(pll))

    lhh = extend2next(phh)
    lll = extend2next(pll)

    #lpchh = extend2next(pchh)
    #lpcll = extend2next(pcll)

    rlhh = rollx(lhh)    #连续上去，没出现新的极点

    iphh = np.nonzero(phh)
    rphh = np.zeros_like(phh)
    rphh[iphh] = rollx(phh[iphh])
    rphh = extend2next(rphh) 

    tp = gmin(rphh,lhh)
    ldlow = dnext(sif.lowd,sif.close,sif.i_cofd)

    signal = gand(#shh>0,
                sll<0,#
                sll>-80,
                cross(tp,sif.high)>0,
                rollx(sif.sdma)>0,
                sif.xatr30x < sif.mxatr30x,
                #rollx(strend2(sif.ma120))<0,
                sif.r7<0,
            )
    return np.select([signal],[gmax(tp,sif.open)],0)

def d2b(sif):
    #向下2b

    plen = 3
    alen = 2*plen+1

    chh = gand(rollx(sif.high,plen) == tmax(sif.high,alen))
    cll = gand(rollx(sif.low,plen) == tmin(sif.low,alen))
    
    phh = np.select([chh],[rollx(sif.high,plen)],0)
    pll = np.select([cll],[rollx(sif.low,plen)],0)

    pphh = extend2next(phh)
    ppll = extend2next(pll)

    #pchh = np.select([chh],[sif.close],0)
    #pcll = np.select([cll],[sif.close],0)

    shh = extend2next(ssub(phh))
    sll = extend2next(ssub(pll))

    lhh = extend2next(phh)
    lll = extend2next(pll)

    #lpchh = extend2next(pchh)
    #lpcll = extend2next(pcll)

    rlhh = rollx(lhh)    #连续上去，没出现新的极点

    ipll = np.nonzero(pll)
    rpll = np.zeros_like(pll)
    rpll[ipll] = rollx(pll[ipll])
    rpll = extend2next(rpll)

    rpll2 = np.zeros_like(pll)
    rpll2[ipll] = rollx(pll[ipll],2)
    rpll2 = extend2next(rpll2) 
    tp = gmin(rpll,lll)

    signal = gand(#sll>0,
                shh>0,#
                shh<20,
                cross(tp,sif.low)<0,
                strend2(sif.mxatr30x)<0,
            )
    return np.select([signal],[gmin(tp,sif.open)],0)


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

b123b = BXFunc(fstate=gofilter,fsignal=u123b,fwave=nx2500X,ffilter=e1430filter2)
b123b.name = u'向上123b'
b123b.lastupdate = 20101222
b123b.stop_closer = utrade.atr5_ustop_V

s123b = SXFunc(fstate=sdown,fsignal=d123b,fwave=nx2500X,ffilter=mfilter)
s123b.name = u'向下123b'
s123b.lastupdate = 20101222
s123b.stop_closer = utrade.atr5_ustop_V

b2b = BXFunc(fstate=gofilter,fsignal=u2b,fwave=nx2500X,ffilter=ekfilter2)##e1430filter2)
b2b.name = u'向上2b'
b2b.lastupdate = 20101222
b2b.stop_closer = utrade.atr5_ustop_V

s2b = SXFunc(fstate=sdown,fsignal=d2b,fwave=nx2500X,ffilter=ekfilter)
s2b.name = u'向下2b'
s2b.lastupdate = 20101222
s2b.stop_closer = utrade.atr5_ustop_V

break123 = [b123,s123]  #整体上缺乏合成性

break123b = [b123b,s123b]  #b123b集成性比较好,s123b不好

break123c = [b123b,b2b,s2b]  #集成性可能比较好
break123c = [b123b]#,s2b,b2b]  #集成性可能比较好, b2b样本太少. b123b作为突破后收盘模型，较难操作，因有惯性

####反弹类
def urebound(sif):
    '''
         创新低后,以冲破支撑为界
         可演变为未创新低的情况
    '''

    plen = 5
    alen = 2*plen+1

    chh = gand(rollx(sif.high,plen) == tmax(sif.high,alen))
    cll = gand(rollx(sif.low,plen) == tmin(sif.low,alen))
    
    phh = np.select([chh],[rollx(sif.high,plen)],0)
    pll = np.select([cll],[rollx(sif.low,plen)],0)

    lhh = extend2next(phh)
    lll = extend2next(pll)

    #lpchh = extend2next(pchh)
    #lpcll = extend2next(pcll)

    #ipll = np.nonzero(pll)
    #rpll = np.zeros_like(pll)
    #rpll[ipll] = rollx(pll[ipll])
    #rpll = extend2next(rpll)

    #rpll2 = np.zeros_like(pll)
    #rpll2[ipll] = rollx(pll[ipll],2)
    #rpll2 = extend2next(rpll2)


    #tp = (lll + rollx(sif.dlow)) / 2#(rpll + lll)/2
    #tp = np.select([lll>sif.dlow,rpll>sif.dlow,rpll==sif.dlow],[(lll+sif.dlow)/2,(rpll+sif.dlow)/2,mlow_last(sif,vlen=10)])
    
    #xp1 = signal_last(tmin(sif.low,75),vlen=10)+20
    #xp2 = signal_last(sif.dlow,vlen=10)+20
    #xp = np.select([sif.time<1030,sif.time>=1030],[xp2,xp1])
    #xp = xp1    #
    xp = signal_last(tmin(sif.low,75),vlen=10)+20
    tp = np.select([lll>sif.dlow,lll==sif.dlow],[gmin(lll+20,xp),xp]) #只有在10:30之前才可能!=low75

    #slx = np.select([lll>sif.dlow,rpll>sif.dlow,rpll2>sif.dlow],[sif.dlow-lll,sif.dlow-rpll,sif.dlow-rpll2],99999999)

    signal = gand(#shh<90,    #不震荡
                #slx < 100,  #发现无必要
                tmin(sif.low,15) == rollx(sif.dlow),#tmin(sif.low,90),当分钟没创新低
                cross(tp,sif.high)>0,
                sif.time>915,   #915会有跳空
                sif.xatr > 1500,
                sif.high - sif.dlow > 100,#这个可能用到未来数据
            )
    return np.select([signal],[gmax(sif.open,tp)],0)

def drebound(sif):
    '''
         创新高后以跌破支撑为界
         可扩展至未创新高?
    '''

    plen = 5
    alen = 2*plen+1

    chh = gand(rollx(sif.high,plen) == tmax(sif.high,alen))
    cll = gand(rollx(sif.low,plen) == tmin(sif.low,alen))
    
    phh = np.select([chh],[rollx(sif.high,plen)],0)
    pll = np.select([cll],[rollx(sif.low,plen)],0)


    shh = extend2next(ssub(phh))
    sll = extend2next(ssub(pll))

    lhh = extend2next(phh)
    lll = extend2next(pll)

    #lpchh = extend2next(pchh)
    #lpcll = extend2next(pcll)

    #iphh = np.nonzero(phh)
    #rphh = np.zeros_like(phh)
    #rphh[iphh] = rollx(phh[iphh])
    #rphh = extend2next(rphh) +10

    #tp = (lll + rollx(sif.dlow)) / 2#(rpll + lll)/2
    #tp = np.select([lll>sif.dlow,rpll>sif.dlow,rpll==sif.dlow],[(lll+sif.dlow)/2,(rpll+sif.dlow)/2,mlow_last(sif,vlen=10)])
    
    xp = signal_last(sif.dhigh,vlen=30) - 20
    tp = np.select([lhh<sif.dhigh,lhh==sif.dhigh],[gmin(lhh-20,xp),xp])
    #tp = lll

    signal = gand(#shh>0,    #不震荡
                tmax(sif.high,15) == rollx(sif.dhigh),
                cross(tp,sif.low)<0,
                sif.time>915,   #915会有跳空
                #strend2(sif.mxatr30x) < 0,
                sif.xatr<1800,
                #sif.dhigh - sif.low > 100,
            )
    return np.select([signal],[gmin(sif.open,tp)],0)

def calc_lh(sif,plen=5):
    alen = 2*plen+1

    chh = gand(rollx(sif.high,plen) == tmax(sif.high,alen))
    cll = gand(rollx(sif.low,plen) == tmin(sif.low,alen))
    
    phh = np.select([chh>0],[rollx(sif.high,plen)],0)
    pll = np.select([cll>0],[rollx(sif.low,plen)],0)

    return phh,pll    



brebound = BXFunc(fstate=gofilter,fsignal=urebound,fwave=gofilter,ffilter=e1430filter)##e1430filter2)
brebound.name = u'向上反弹'
brebound.lastupdate = 20101225
brebound.stop_closer = utrade.atr5_ustop_6

srebound = SXFunc(fstate=gofilter,fsignal=drebound,fwave=gofilter,ffilter=mfilter2)##e1430filter2)
srebound.name = u'向下反弹'
srebound.lastupdate = 20101225
srebound.stop_closer = utrade.atr5_ustop_6


dbrebound = BXFuncD1(fstate=gofilter,fsignal=urebound,fwave=gofilter,ffilter=e1430filter)##e1430filter2)
dbrebound.name = u'向上反弹'
dbrebound.lastupdate = 20101225
dbrebound.stop_closer = utrade.atr5_ustop_6

dsrebound = SXFuncD1(fstate=gofilter,fsignal=drebound,fwave=gofilter,ffilter=mfilter2)##e1430filter2)
dsrebound.name = u'向下反弹'
dsrebound.lastupdate = 20101225
dsrebound.stop_closer = utrade.atr5_ustop_6

rebound = [brebound,srebound]

d1_rebound = [dbrebound,dsrebound]

###普通形态突破
def uxbreak(sif):
    '''
        向上突破
    '''

    phh,pll = calc_lh(sif,plen=6)
    phh2,pll2 = calc_lh(sif,plen=2)

    sll = extend2next(ssub(pll))
    shh = extend2next(ssub(phh))

    lhh = extend2next(phh)
    lll = extend2next(pll)
    lll2 = extend2next(pll2)
    lhh2 = extend2next(phh2)

    ihh = np.nonzero(phh)
    ill = np.nonzero(pll)

    iihh = np.zeros_like(phh)
    iill = np.zeros_like(pll)
    iihh[ihh] = ihh
    iill[ill] = ill
    iihh = extend2next(iihh)
    iill = extend2next(iill)


    #lpchh = extend2next(pchh)
    #lpcll = extend2next(pcll)

    #ipll = np.nonzero(pll)
    #rpll = np.zeros_like(pll)
    #rpll[ipll] = rollx(pll[ipll])
    #rpll = extend2next(rpll)

    #rpll2 = np.zeros_like(pll)
    #rpll2[ipll] = rollx(pll[ipll],2)
    #rpll2 = extend2next(rpll2)


    #tp = (lll + rollx(sif.dlow)) / 2#(rpll + lll)/2
    #tp = np.select([lll>sif.dlow,rpll>sif.dlow,rpll==sif.dlow],[(lll+sif.dlow)/2,(rpll+sif.dlow)/2,mlow_last(sif,vlen=10)])
    
    #xp1 = signal_last(tmin(sif.low,75),vlen=10)+20
    #xp2 = signal_last(sif.dlow,vlen=10)+20
    #xp = np.select([sif.time<1030,sif.time>=1030],[xp2,xp1])
    #xp = xp1    #

    tp = lhh + 6

    #slx = np.select([lll>sif.dlow,rpll>sif.dlow,rpll2>sif.dlow],[sif.dlow-lll,sif.dlow-rpll,sif.dlow-rpll2],99999999)

    #tp = np.select([gor(tp<sif.dhigh-80,sif.time<945)],[tp],99999999)   #距离突破线比较近的，交给突破
    tp = np.select([gor(tp<rollx(sif.dhigh)-80,sif.time<945)],[tp],99999999)   #距离突破线比较近的，交给突破    
    #tp = np.select([gor(gand(tp<sif.dhigh-80,rollx(sif.high)<sif.dhigh-30),sif.time<945)],[tp],99999999)   #距离突破线比较近的，交给突破

    #print tp[-140:],sif.high[-140:],lhh[-140:]

    tp2 = lhh + 80  #假动作之后抬升
    tp2 = np.select([gor(tp2<rollx(sif.dhigh)-80,sif.time<945)],[tp2],99999999)   #距离突破线比较近的，交给突破
    #tp2 = np.select([gor(gand(tp2<sif.dhigh-80,rollx(sif.high)<sif.dhigh-30),sif.time<945)],[tp2],99999999)   #距离突破线比较近的，交给突破

    #ldlow = dnext(gmin(sif.lowd,rollx(sif.lowd)),sif.close,sif.i_cofd)

    signal = gand(#shh<90,    #不震荡
                gor(lll2 > lll,sll>0),
                #lll2>lll,
                #sll>0,
                cross(tp,sif.high)>0,
                tp <= rollx(tp),#不是从99999999下来的被上叉
                strend2(sif.high)>0,
                sif.time>915,   #915会有跳空
                tp - sif.dlow > 150,
                #sif.xatr > sif.mxatr,
                #strend2(sif.mxatr)>0,
                sif.xatr > 800,
                #lhh>lll+40,
              )

    msignal = msum(signal,30)
    signal2 = gand(
                gor(lll2 > lll,sll>0),
                #lll2>lll,
                #sll>0,
                cross(tp2,sif.high)>0,
                tp <= rollx(tp),#不是从99999999下来的被上叉                
                sif.time>915,   #915会有跳空
                tp2 - sif.dlow > 150,
                #sif.xatr > sif.mxatr,
                #strend2(sif.mxatr)>0,
                sif.xatr > 800,
                #lhh>lll+40,
            )
    signal = np.select([msignal<3,msignal>=3],[signal,signal2],0)
    ptp = np.select([msignal<3,msignal>=3],[tp,tp2],0)
    return np.select([signal],[gmax(sif.open,ptp)],0)
    #return np.select([signal],[gmax(sif.open,tp)],0)

def uxbreak2(sif):
    '''
        向上突破
        添加
        rollx(sif.xatr > sif.mxatr),
    '''

    phh,pll = calc_lh(sif,plen=5)
    phh2,pll2 = calc_lh(sif,plen=2)

    sll = extend2next(ssub(pll))
    shh = extend2next(ssub(phh))

    lhh = extend2next(phh)
    lll = extend2next(pll)
    lll2 = extend2next(pll2)

    ihh = np.nonzero(phh)
    ill = np.nonzero(pll)

    iihh = np.zeros_like(phh)
    iill = np.zeros_like(pll)
    iihh[ihh] = ihh
    iill[ill] = ill
    iihh = extend2next(iihh)
    iill = extend2next(iill)


    #lpchh = extend2next(pchh)
    #lpcll = extend2next(pcll)

    #ipll = np.nonzero(pll)
    #rpll = np.zeros_like(pll)
    #rpll[ipll] = rollx(pll[ipll])
    #rpll = extend2next(rpll)

    #rpll2 = np.zeros_like(pll)
    #rpll2[ipll] = rollx(pll[ipll],2)
    #rpll2 = extend2next(rpll2)


    #tp = (lll + rollx(sif.dlow)) / 2#(rpll + lll)/2
    #tp = np.select([lll>sif.dlow,rpll>sif.dlow,rpll==sif.dlow],[(lll+sif.dlow)/2,(rpll+sif.dlow)/2,mlow_last(sif,vlen=10)])
    
    #xp1 = signal_last(tmin(sif.low,75),vlen=10)+20
    #xp2 = signal_last(sif.dlow,vlen=10)+20
    #xp = np.select([sif.time<1030,sif.time>=1030],[xp2,xp1])
    #xp = xp1    #

    tp = lhh + 6

    #slx = np.select([lll>sif.dlow,rpll>sif.dlow,rpll2>sif.dlow],[sif.dlow-lll,sif.dlow-rpll,sif.dlow-rpll2],99999999)

    tp = np.select([gor(tp<sif.dhigh-80,sif.time<945)],[tp],99999999)   #距离突破线比较近的，交给突破
    #tp = gmax(tp,sif.dlow+151)

    tp2 = lhh + 80  #假动作之后抬升
    tp2 = np.select([gor(tp2<sif.dhigh-80,sif.time<945)],[tp2],99999999)   #距离突破线比较近的，交给突破

    signal = gand(#shh<90,    #不震荡
                #gor(lll2 > lll,sll>0),
                #lll2>lll,
                #sll>0,
                cross(tp,sif.high)>0,
                sif.time>915,   #915会有跳空
                tp - sif.dlow > 150,
                rollx(sif.xatr > sif.mxatr),
                #strend2(sif.mxatr)>0,
                #sif.xatr > 800,
                #lhh>lll+40,
                )

    return np.select([signal],[gmax(sif.open,tp)],0)


def dxbreak(sif):
    '''
        向下突破
    '''

    phh,pll = calc_lh(sif,plen=6)
    phh2,pll2 = calc_lh(sif,plen=2)

    sll = extend2next(ssub(pll))
    shh = extend2next(ssub(phh))

    lhh = extend2next(phh)
    lll = extend2next(pll)
    lll2 = extend2next(pll2)
    lhh2 = extend2next(phh2)

    ihh = np.nonzero(phh)
    ill = np.nonzero(pll)

    iihh = np.zeros_like(phh)
    iill = np.zeros_like(pll)
    iihh[ihh] = ihh
    iill[ill] = ill
    iihh = extend2next(iihh)
    iill = extend2next(iill)

    
    tp = lll+2
    #tp = lll

    tlow = gmin(rollx(tmin(sif.low,75)+20))
    #tp = np.select([gor(tp>tlow+60,sif.time<=1031,sif.time>=1430)],[tp],0) #接近低点的给突破
    tp = np.select([gor(tp>tlow+80)],[tp],0) #接近低点的给突破
    #tp = np.select([gand(tp>tlow+60,rollx(sif.low)>tlow+30)],[tp],0) #接近低点的给突破

    tp2 = lll - 50  #假动作之后降低
    tp2 = np.select([tp2>tlow+80],[tp2],0) #接近低点的给突破

    #ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    #ldmid = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)    
    ldmid = dnext(sif.highd,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)        

    signal = gand(#sll<0,    #不震荡
                #rollx(sif.sdma)>0,
                #gor(lhh2 < lhh,shh<0),
                cross(tp,sif.low)<0,
                sif.time>915,   #915会有跳空
                tp >= rollx(tp),    #不是从0起来的被交叉
                #sif.xatr>sif.mxatr,
                #sif.xatr<2500,
                #sif.xatr30x < 10000,
                #sif.xatr5x < 4000,
                #sif.dhigh - sif.low>60,
                gor(tp < ldmid,tp<opend),#-sif.xatr*2/XBASE,  #比前2天高点中点低才允许做空                
            )
    
    msignal = msum(signal,15)
    signal2 = gand(#sll<0,    #不震荡
                #rollx(sif.sdma)>0,
                #gor(lhh2 < lhh,shh<0),
                cross(tp2,sif.low)<0,
                sif.time>915,   #915会有跳空
                tp >= rollx(tp),    #不是从0起来的被交叉                
                #sif.xatr<2500,
                #sif.xatr30x < 10000,
                #sif.xatr5x < 4000,
                #sif.dhigh - sif.low>60,
                gor(tp < ldmid,tp<opend),#-sif.xatr*2/XBASE,  #比前2天高点中点低才允许做空                
            )
    signal = np.select([msignal<3,msignal>=3],[signal,signal2],0)
    ptp = np.select([msignal<3,msignal>=3],[tp,tp2],0)
    return np.select([signal],[gmin(sif.open,ptp)],0)
    #return np.select([signal],[gmin(sif.open,tp)],0)

def dxbreak2(sif):
    '''
        向下突破
        添加
        rollx(sif.xatr > sif.mxatr),
    '''

    phh,pll = calc_lh(sif,plen=5)
    phh2,pll2 = calc_lh(sif,plen=2)

    sll = extend2next(ssub(pll))
    shh = extend2next(ssub(phh))

    lhh = extend2next(phh)
    lll = extend2next(pll)
    lll2 = extend2next(pll2)
    lhh2 = extend2next(phh2)

    ihh = np.nonzero(phh)
    ill = np.nonzero(pll)

    iihh = np.zeros_like(phh)
    iill = np.zeros_like(pll)
    iihh[ihh] = ihh
    iill[ill] = ill
    iihh = extend2next(iihh)
    iill = extend2next(iill)

    
    tp = lll+2
    #tp = lll

    tlow = gmin(rollx(tmin(sif.low,75)+20))
    tp = np.select([tp>tlow+60],[tp],0) #接近低点的给突破

    signal = gand(#sll<0,    #不震荡
                #rollx(sif.sdma)>0,
                #gor(lhh2 < lhh,shh<0),
                cross(tp,sif.low)<0,
                sif.time>915,   #915会有跳空
                rollx(sif.xatr > sif.mxatr),
                #sif.xatr<2500,
                #sif.xatr30x < 10000,
                #sif.xatr5x < 4000,
                #sif.dhigh - sif.low>60,
            )
    
    return np.select([signal],[gmin(sif.open,tp)],0)


bxbreak = BXFunc(fstate=gofilter,fsignal=uxbreak,fwave=gofilter,ffilter=mfilter3)##e1430filter2)
bxbreak.name = u'向上突破'
bxbreak.lastupdate = 20101231
bxbreak.stop_closer = utrade.atr5_ustop_V1

bxbreak2 = BXFunc(fstate=gofilter,fsignal=uxbreak2,fwave=gofilter,ffilter=mfilter3)##e1430filter2)
bxbreak2.name = u'向上突破2'
bxbreak2.lastupdate = 20101231
bxbreak2.stop_closer = utrade.atr5_ustop_X2

bxbreakd = BXFuncF1(fstate=gofilter,fsignal=uxbreak,fwave=gofilter,ffilter=mfilter3)##e1430filter2)
bxbreakd.name = u'向上突破'
bxbreakd.lastupdate = 20101231
bxbreakd.stop_closer = utrade.atr5_ustop_X2


sxbreak = SXFunc(fstate=gofilter,fsignal=dxbreak,fwave=nx2500X,ffilter=mfilter3)##e1430filter2)
sxbreak.name = u'向下突破'
sxbreak.lastupdate = 20101231
sxbreak.stop_closer = utrade.atr5_ustop_V1

sxbreak2 = SXFunc(fstate=gofilter,fsignal=dxbreak2,fwave=nx2500X,ffilter=mfilter2)##e1430filter2)
sxbreak2.name = u'向下突破'
sxbreak2.lastupdate = 20101231
sxbreak2.stop_closer = utrade.atr5_ustop_X2

sxbreakd = SXFuncF1(fstate=gofilter,fsignal=dxbreak,fwave=nx2500X,ffilter=mfilter2)##e1430filter2)
sxbreakd.name = u'向下突破'
sxbreakd.lastupdate = 20101231
sxbreakd.stop_closer = utrade.atr5_ustop_V

xbreak = [bxbreak,sxbreak]
xbreak2 = [bxbreak2,sxbreak2]
d1_xbreak = [bxbreakd,sxbreakd]

##仿AMM算法
def uamm(sif):
    '''
        仿AMM的回归
    '''

    phh,pll = calc_lh(sif,plen=5)
    phh2,pll2 = calc_lh(sif,plen=2)

    sll = extend2next(ssub(pll))
    shh = extend2next(ssub(phh))

    lhh = extend2next(phh)
    lll = extend2next(pll)
    lll2 = extend2next(pll2)

    ihh = np.nonzero(phh)
    ill = np.nonzero(pll)

    iihh = np.zeros_like(phh)
    iill = np.zeros_like(pll)
    iihh[ihh] = ihh
    iill[ill] = ill
    iihh = extend2next(iihh)
    iill = extend2next(iill)


    #lpchh = extend2next(pchh)
    #lpcll = extend2next(pcll)

    #ipll = np.nonzero(pll)
    #rpll = np.zeros_like(pll)
    #rpll[ipll] = rollx(pll[ipll])
    #rpll = extend2next(rpll)

    #rpll2 = np.zeros_like(pll)
    #rpll2[ipll] = rollx(pll[ipll],2)
    #rpll2 = extend2next(rpll2)


    #tp = (lll + rollx(sif.dlow)) / 2#(rpll + lll)/2
    #tp = np.select([lll>sif.dlow,rpll>sif.dlow,rpll==sif.dlow],[(lll+sif.dlow)/2,(rpll+sif.dlow)/2,mlow_last(sif,vlen=10)])
    
    #xp1 = signal_last(tmin(sif.low,75),vlen=10)+20
    #xp2 = signal_last(sif.dlow,vlen=10)+20
    #xp = np.select([sif.time<1030,sif.time>=1030],[xp2,xp1])
    #xp = xp1    #

    tp = lhh - 80

    #slx = np.select([lll>sif.dlow,rpll>sif.dlow,rpll2>sif.dlow],[sif.dlow-lll,sif.dlow-rpll,sif.dlow-rpll2],99999999)

    tp = np.select([gor(tp<sif.dhigh-80,sif.time<945)],[tp],99999999)   #距离突破线比较近的，交给突破
    #tp = gmax(tp,sif.dlow+151)

    signal = gand(#shh<90,    #不震荡
                gor(lll2 > lll,sll>0),
                #lll2>lll,
                #sll>0,
                cross(tp,sif.high)>0,
                tp >= rollx(tp),
                sif.time>915,   #915会有跳空
                tp - sif.dlow > 150,
                tmin(sif.low,4) > lll-20,
                #sif.xatr > sif.mxatr,
                #strend2(sif.mxatr)>0,
                #sif.xatr > 800,
                #sif.xatr > sif.mxatr,
                #rollx(sif.xatr > sif.mxatr *0.95),
                rollx(sif.xatr > sif.mxatr - 60),
                #lhh>lll+40,
                )

    return np.select([signal],[gmax(sif.open,tp)],0)

def damm(sif):
    '''
        向下突破
    '''

    phh,pll = calc_lh(sif,plen=5)
    phh2,pll2 = calc_lh(sif,plen=2)

    sll = extend2next(ssub(pll))
    shh = extend2next(ssub(phh))

    lhh = extend2next(phh)
    lll = extend2next(pll)
    lll2 = extend2next(pll2)
    lhh2 = extend2next(phh2)

    ihh = np.nonzero(phh)
    ill = np.nonzero(pll)

    iihh = np.zeros_like(phh)
    iill = np.zeros_like(pll)
    iihh[ihh] = ihh
    iill[ill] = ill
    iihh = extend2next(iihh)
    iill = extend2next(iill)

    
    tp = lll+60
    #tp = lll

    tlow = gmin(rollx(tmin(sif.low,75)+20))
    #print tp[-440:-400],tlow[-440:-400]
    tp = np.select([tp>tlow+60],[tp],0) #接近低点的给突破

    signal = gand(#sll<0,    #不震荡
                #rollx(sif.sdma)>0,
                #gor(lhh2 < lhh,shh<0),
                cross(tp,sif.low)<0,
                tp <= rollx(tp),    #排除tp从0-->实际数字的跳变，即因为tlow的下降，使得原来为0的tp变成某个大数，
                                    #   从而被动变成下叉
                sif.time>915,   #915会有跳空
                #sif.xatr<2500,
                
                rollx(sif.xatr > sif.mxatr - 60), 
                tmax(sif.high,4) < lhh - 20,
                #sif.dhigh - tp > 100,
                #sif.dhigh-rollx(sif.high)>100,
                #rollx(sif.low) != tlow-20,
                
                #sif.xatr30x < 10000,
                #sif.xatr5x < 4000,
                #sif.dhigh - sif.low>60,
            )
    
    return np.select([signal],[gmin(sif.open,tp)],0)

def uamm1(sif):
    ssignal = gand(sif.close < sif.open,
                sif.close <  sif.dmid,#(sif.dhigh + sif.dlow*2)/3,#sif.dmid,
                sif.close < sif.dlow + 120,
                sif.time > 1031,    #1030和1031差异很大. 感觉1030是突变点? 如果没有成功变盘，则重新发向时进入
                                    #以1030-1035的运行方向开仓a
                sif.xatr < sif.mxatr,
                strend2(sif.mxatr)<0,

            )
    sms = dsum(ssignal,sif.iday)
    signal = gand(sif.close > sif.open,
                sif.close> (sif.dhigh*2 + sif.dlow)/3,#sif.dmid,
                sif.close > sif.dhigh - 120,
                sif.time > 1031,    #1030和1031差异很大. 感觉1030是突变点? 如果没有成功变盘，则重新发向时进入
                                    #以1030-1035的运行方向开仓
                sms < 1,
                sif.xatr < sif.mxatr,
                strend2(sif.mxatr)<0,
            )
    return np.select([signal],[sif.close],0)

def uamm2(sif):
    signal = gand(sif.close > rollx(sif.close,30)  ,
                sif.time == 1101,
            )
    return np.select([signal],[sif.close],0)

def damm1(sif):
    bsignal = gand(sif.close > sif.open,
                sif.close> (sif.dhigh*2 + sif.dlow)/3,#sif.dmid,
                sif.close > sif.dhigh - 120,
                sif.time > 1031,    #1030和1031差异很大. 感觉1030是突变点? 如果没有成功变盘，则重新发向时进入
                                    #以1030-1035的运行方向开仓
                sif.xatr < sif.mxatr,
                strend2(sif.mxatr)<0,
            )
    sms = dsum(bsignal,sif.iday)
    signal = gand(sif.close < sif.open,
                sif.close <  sif.dmid,#(sif.dhigh + sif.dlow*2)/3,#sif.dmid,
                sif.close < sif.dlow + 120,
                sif.time > 1031,    #1030和1031差异很大. 感觉1030是突变点? 如果没有成功变盘，则重新发向时进入
                                    #以1030-1035的运行方向开仓a
                sif.xatr < sif.mxatr,
                strend2(sif.mxatr)<0,
                sms<1,
            )
    return np.select([signal],[sif.close],0)

def damm2(sif):
    signal = gand(sif.close < rollx(sif.close,30)  ,
                sif.time == 1101,
            )
    return np.select([signal],[sif.close],0)


def damm3(sif):

    '''
        向下突破
    '''

    phh,pll = calc_lh(sif,plen=5)
    phh2,pll2 = calc_lh(sif,plen=2)

    sll = extend2next(ssub(pll))
    shh = extend2next(ssub(phh))

    lhh = extend2next(phh)
    lll = extend2next(pll)
    lll2 = extend2next(pll2)
    lhh2 = extend2next(phh2)

    ihh = np.nonzero(phh)
    ill = np.nonzero(pll)

    iihh = np.zeros_like(phh)
    iill = np.zeros_like(pll)
    iihh[ihh] = ihh
    iill[ill] = ill
    iihh = extend2next(iihh)
    iill = extend2next(iill)

    
    tp = lll+60

    signal = gand(#sll<0,    #不震荡
                #sif.sdma<0,
                #gor(lhh2 < lhh,shh<0),
                sif.time>1031,   #915会有跳空
                sif.xatr < sif.mxatr, 
                strend2(sif.mxatr)<0,
                tmax(sif.high,4) < lhh - 80,
                sif.dhigh - sif.high > 100,
                sif.close < (tmax(sif.high,30)+tmin(sif.low,30))/2,
                #sif.low < tp,
                #sif.xatr30x < 10000,
                #sif.xatr5x < 4000,
                #sif.dhigh - sif.low>60,
            )
    return signal


def uamm3(sif):

    '''
        向上突破
    '''

    phh,pll = calc_lh(sif,plen=5)
    phh2,pll2 = calc_lh(sif,plen=2)

    sll = extend2next(ssub(pll))
    shh = extend2next(ssub(phh))

    lhh = extend2next(phh)
    lll = extend2next(pll)
    lll2 = extend2next(pll2)
    lhh2 = extend2next(phh2)

    ihh = np.nonzero(phh)
    ill = np.nonzero(pll)

    iihh = np.zeros_like(phh)
    iill = np.zeros_like(pll)
    iihh[ihh] = ihh
    iill[ill] = ill
    iihh = extend2next(iihh)
    iill = extend2next(iill)

    
    tp = lhh-120
    #tp = lll


    signal = gand(#sll<0,    #不震荡
                #rollx(sif.sdma)>0,
                #gor(lhh2 < lhh,shh<0),
                sif.time>1030,   #915会有跳空
                sif.xatr < sif.mxatr, 
                tmin(sif.low,4) > lll + 120,
                tmax(sif.high,4) > lhh - 30,
                tmax(sif.high,4) < lhh + 10,
                #sif.close > tp,
                #sif.close < (tmax(sif.high,30)+tmin(sif.low,30))/2,
                #sif.low < tp,
                #sif.xatr30x < 10000,
                #sif.xatr5x < 4000,
                #sif.dhigh - sif.low>60,
            )
    return signal


def uamm4(sif):

    '''
        向上回归
    '''

    phh,pll = calc_lh(sif,plen=5)
    phh2,pll2 = calc_lh(sif,plen=2)

    sll = extend2next(ssub(pll))
    shh = extend2next(ssub(phh))

    lhh = extend2next(phh)
    lll = extend2next(pll)
    lll2 = extend2next(pll2)
    lhh2 = extend2next(phh2)

    ihh = np.nonzero(phh)
    ill = np.nonzero(pll)

    iihh = np.zeros_like(phh)
    iill = np.zeros_like(pll)
    iihh[ihh] = ihh
    iill[ill] = ill
    iihh = extend2next(iihh)
    iill = extend2next(iill)

    
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd)
    ldopen = dnext(sif.opend,sif.open,sif.i_oofd)    
    ldmid = (ldclose + ldopen)/2
    ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)

    xsignal = gand(
                cross(sif.mxatr,sif.xatr)>0,
                strend2(sif.xatr)>0,
            )

    bline = np.select([xsignal],[sif.high+30],0)
    bline = extend(bline,15)
    bline = np.select([bline>0],[bline],99999999)

    signal = gand(
                cross(bline,sif.high),
            )
    return np.select([signal],[gmax(sif.open,bline)],0)


bamm = BXFunc(fstate=gofilter,fsignal=uamm,fwave=gofilter,ffilter=mfilter1a)##e1430filter2)
bamm.name = u'AMM向上突破'
bamm.lastupdate = 20101231
bamm.stop_closer = utrade.atr5_ustop_V

bamm1 = BXFuncD1(fstate=gofilter,fsignal=uamm1,fwave=gofilter,ffilter=gofilter)##e1430filter2)
bamm1.name = u'AMM向上突破'
bamm1.lastupdate = 20101231
bamm1.stop_closer = utrade.atr5_ustop_V1

bamm2 = BXFuncD1(fstate=gofilter,fsignal=uamm2,fwave=gofilter,ffilter=gofilter)##e1430filter2)
bamm2.name = u'AMM向上突破'
bamm2.lastupdate = 20101231
bamm2.stop_closer = utrade.atr5_ustop_X2

bamm3 = BXFuncD1(fstate=gofilter,fsignal=uamm3,fwave=gofilter,ffilter=gofilter)##e1430filter2)
bamm3.name = u'AMM向上突破3'
bamm3.lastupdate = 20101231
bamm3.stop_closer = utrade.atr5_ustop_V

bamm4 = BXFunc(fstate=gofilter,fsignal=uamm4,fwave=gofilter,ffilter=mfilter)##e1430filter2)
bamm4.name = u'AMM向上突破4'
bamm4.lastupdate = 20101231
bamm4.stop_closer = utrade.atr5_ustop_V1


samm = SXFunc(fstate=gofilter,fsignal=damm,fwave=nx2500X,ffilter=mfilter1a)##e1430filter2)
samm.name = u'AMM向下突破'
samm.lastupdate = 20101231
samm.stop_closer = utrade.atr5_ustop_V

samm1 = SXFuncD1(fstate=gofilter,fsignal=damm1,fwave=gofilter,ffilter=gofilter)##e1430filter2)
samm1.name = u'AMM向下突破1'
samm1.lastupdate = 20101231
samm1.stop_closer = utrade.atr5_ustop_V1

###samm3单个极好
samm3 = SXFuncD1(fstate=gofilter,fsignal=damm3,fwave=gofilter,ffilter=gofilter)##e1430filter2)
samm3.name = u'AMM向下突破3'
samm3.lastupdate = 20101231
samm3.stop_closer = utrade.atr5_ustop_V



samm2 = SXFuncD1(fstate=gofilter,fsignal=damm2,fwave=gofilter,ffilter=gofilter)##e1430filter2)
samm2.name = u'AMM向上突破'
samm2.lastupdate = 20101231
samm2.stop_closer = utrade.atr5_ustop_X2

amm = [bamm,samm]   #单独可以作为主策略

amm1 = [bamm1,samm1]    #每天10:31之后根据开盘价，当前价和中点关系开仓. 并用到缩量. 单独非常有效，叠加无效

amm2 = [bamm2,samm2]    #每天11:01定时开仓，方向根据最近30分钟运行方向. 其中samm2很强

amm3 = [bamm3,samm3]    #单个也可作为备用主策略

ammx = amm + amm1   #这个方法可以，模拟AMM. 累计收益不错. 工作稳定. 可以作为主模型

ammy = amm + amm3  #不如amm3

###顶底突破
def bbreak1(sif):
    '''
        低点突破
        1. 高点后突破前一个显著低点
        2. 高点后形成一个低点然后突破
        存在时间要求
    '''

    plen = 5
    alen = 2*plen+1

    chh = gand(rollx(sif.high,plen) == tmax(sif.high,alen))
    cll = gand(rollx(sif.low,plen) == tmin(sif.low,alen))
    
    phh = np.select([chh],[rollx(sif.high,plen)],0)
    pll = np.select([cll],[rollx(sif.low,plen)],0)

    lhh = extend2next(phh)
    lll = extend2next(pll)

    #lpchh = extend2next(pchh)
    #lpcll = extend2next(pcll)

    #ipll = np.nonzero(pll)
    #rpll = np.zeros_like(pll)
    #rpll[ipll] = rollx(pll[ipll])
    #rpll = extend2next(rpll)

    #rpll2 = np.zeros_like(pll)
    #rpll2[ipll] = rollx(pll[ipll],2)
    #rpll2 = extend2next(rpll2)


    #tp = (lll + rollx(sif.dlow)) / 2#(rpll + lll)/2
    #tp = np.select([lll>sif.dlow,rpll>sif.dlow,rpll==sif.dlow],[(lll+sif.dlow)/2,(rpll+sif.dlow)/2,mlow_last(sif,vlen=10)])
    
    #xp1 = signal_last(tmin(sif.low,75),vlen=10)+20
    #xp2 = signal_last(sif.dlow,vlen=10)+20
    #xp = np.select([sif.time<1030,sif.time>=1030],[xp2,xp1])
    #xp = xp1    #
    xp = signal_last(tmin(sif.low,75),vlen=10)+20
    tp = np.select([lll>sif.dlow,lll==sif.dlow],[gmin(lll+20,xp),xp]) #只有在10:30之前才可能!=low75

    #slx = np.select([lll>sif.dlow,rpll>sif.dlow,rpll2>sif.dlow],[sif.dlow-lll,sif.dlow-rpll,sif.dlow-rpll2],99999999)

    signal = gand(#shh<90,    #不震荡
                #slx < 100,  #发现无必要
                tmin(sif.low,15) == rollx(sif.dlow),#tmin(sif.low,90),当分钟没创新低
                cross(tp,sif.high)>0,
                sif.time>915,   #915会有跳空
                sif.xatr > 1500,
                sif.high - sif.dlow > 100,
            )
    return np.select([signal],[gmax(sif.open,tp)],0)

def pbreak1(sif):
    '''
        高点突破
        1. 低点后突破前一个显著高点
        2. 低点后形成一个高点然后突破
        
    '''

    plen = 5
    alen = 2*plen+1

    chh = gand(rollx(sif.high,plen) == tmax(sif.high,alen))
    cll = gand(rollx(sif.low,plen) == tmin(sif.low,alen))
    
    phh = np.select([chh],[rollx(sif.high,plen)],0)
    pll = np.select([cll],[rollx(sif.low,plen)],0)


    shh = extend2next(ssub(phh))
    sll = extend2next(ssub(pll))

    lhh = extend2next(phh)
    lll = extend2next(pll)

    #lpchh = extend2next(pchh)
    #lpcll = extend2next(pcll)

    #iphh = np.nonzero(phh)
    #rphh = np.zeros_like(phh)
    #rphh[iphh] = rollx(phh[iphh])
    #rphh = extend2next(rphh) +10

    #tp = (lll + rollx(sif.dlow)) / 2#(rpll + lll)/2
    #tp = np.select([lll>sif.dlow,rpll>sif.dlow,rpll==sif.dlow],[(lll+sif.dlow)/2,(rpll+sif.dlow)/2,mlow_last(sif,vlen=10)])
    
    xp = signal_last(sif.dhigh,vlen=30) - 20
    tp = np.select([lhh<sif.dhigh,lhh==sif.dhigh],[gmin(lhh-20,xp),xp])
    #tp = lll

    signal = gand(#shh>0,    #不震荡
                tmax(sif.high,15) == rollx(sif.dhigh),
                cross(tp,sif.low)<0,
                sif.time>915,   #915会有跳空
                #strend2(sif.mxatr30x) < 0,
                sif.xatr<1800,
                #sif.dhigh - sif.low > 100,
            )
    return np.select([signal],[gmin(sif.open,tp)],0)


###不同周期突破系统
def k15d(sif):
    bline = dnext_cover(sif.low15-60,sif.close,sif.i_cof15,6)
    signal = gand(
            cross(bline,sif.low)<0,
            #(sif.time%100) % 15 !=0,#不是卡在15分钟末，因为这个是low的切换点，不能作为cross依据
           )
    
    return np.select([signal],[gmin(sif.open,bline)],0)

sk15a = SXFunc(fstate=sdown,fsignal=k15d,fwave=nx2500X,ffilter=mfilter)
sk15a.name = u'15分钟周期向下突破'
sk15a.lastupdate = 20101224
sk15a.stop_closer = utrade.atr5_ustop_V


def k5d(sif):   #集成效果不佳,但可以作为主单元
    bline = dnext_cover(sif.low5-10,sif.close,sif.i_cof5,4)
    signal = gand(
            cross(bline,sif.low)<0,
            tmax(sif.high,15) < tmax(sif.high,90)-100,            
            (sif.time%100) % 5 !=0,#不是卡在5分钟头，因为这个是low的切换点，不能作为cross依据
           )
    
    return np.select([signal],[gmin(sif.open,bline)],0)

sk5a = SXFunc(fstate=sdown,fsignal=k5d,fwave=nx2500X,ffilter=mfilter)
sk5a.name = u'k5向下突破'
sk5a.lastupdate = 20101224
sk5a.stop_closer = utrade.atr5_ustop_V

def k5u(sif):   #
    bline = hdnext_cover(sif.high5+30,sif.close,sif.i_cof5,4)
    signal = gand(
            cross(bline,sif.high)>0,
            tmin(sif.low,30) > tmin(sif.low,75)+90,
            (sif.time%100) % 5 !=0,#不是卡在5分钟头，因为这个是high的切换点，不能作为cross依据
            #sif.xatr > sif.mxatr,
           )
    
    return np.select([signal],[gmax(sif.open,bline)],0)

bk5a = BXFunc(fstate=gofilter,fsignal=k5u,fwave=gofilter,ffilter=e1400filter2)
bk5a.name = u'k5向上突破'
bk5a.lastupdate = 20101224
bk5a.stop_closer = utrade.atr5_ustop_V

zk5 = [sk5a,bk5a]   #单独效果尚可，合并不好

def k5ru(sif):
    
    signal5 = gand(
                rollx(sif.low5) == tmin(sif.low5,10),
                #sif.low5 < rollx(sif.low5)
                sif.close5 > rollx(sif.high5)+50,
              )

    delay = 1

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof5] = signal5
    #signal = dnext_cover(signal5,sif.close,sif.i_cof5,delay)
 
    signal = gand(signal,
                sif.xatr30x < 12000,
            )


    return signal

bk15a = BXFunc(fstate=gofilter,fsignal=k5ru,fwave=gofilter,ffilter=mfilter)
bk15a.name = u'k5向上突破'
bk15a.lastupdate = 20101224
bk15a.stop_closer = utrade.atr5_ustop_V


def k5rd(sif):
    
    signal5 = gand(
                rollx(sif.high5) == tmax(sif.high5,6),
                #sif.low5 < rollx(sif.low5)
                sif.close5 < rollx(sif.low5),
              )


    signal = np.zeros_like(sif.close)
    signal[sif.i_cof5] = signal5
    #signal = dnext_cover(signal5,sif.close,sif.i_cof5,delay)
 

    return signal

sk15d = SXFunc(fstate=gofilter,fsignal=k5rd,fwave=gofilter,ffilter=nfilter)
sk15d.name = u'k5向上突破'
sk15d.lastupdate = 20101224
sk15d.stop_closer = utrade.atr5_ustop_V

def k5rd2(sif):
    
    signal5 = gand(sif.high5 == tmax(sif.high5,3),sif.high5 < tmax(sif.high5,30),)

    bline = sif.low5#tmin(sif.low5,2)

    bline = dnext_cover(np.select([signal5>0],[bline],0),sif.close,sif.i_cof5,4)    

    signal = gand(cross(bline,sif.low)<0,
              #sif.xatr30x < sif.mxatr30x,
              strend2(sif.mxatr30x)<0,
              sif.xatr<1500,
              #sif.time != 915,
            )

    return np.select([signal>0],[gmin(sif.open,bline)],0)
sk5d2 = SXFuncD1(fstate=gofilter,fsignal=k5rd2,fwave=gofilter,ffilter=ekfilter)
sk5d2.name = u'5分钟周期向下突破2'
sk5d2.lastupdate = 20101227
sk5d2.stop_closer = utrade.atr5_ustop_V

ebreak = [sk15a]#,sk5d2] #sk5d2样本太少<40


###5/10/15/30/60分钟投机系统, 按分钟分解,难以找到好策略. 


def jxd5(sif):   #
    xmod =  sif.time % 100 % 10
    signal = gand(
            gor(xmod == 9),#9,gand(xmod>=0,xmod<=2)),
            #strend2(sif.mxatr30x)<0,
            #strend2(sif.mxatr)>0,            
            #sif.low < rollx(sif.low,30),
            #tmax(sif.high,5)<tmax(sif.high,30),
            sif.low < rollx(sif.low)-10,
            sif.low > rollx(tmin(sif.low,75))+20,
            sif.close < sif.open,
            rollx(sif.close) < rollx(sif.open),
            sif.xatr<2500,
          )
    
    return np.select([signal],[sif.close],0)

sjxd5 = SXFunc(fstate=sdown,fsignal=jxd5,fwave=gofilter,ffilter=mfilter)
sjxd5.name = u'5分钟向下投机'
sjxd5.lastupdate = 20101224
#sjxd5.stop_closer = utrade.atr5_ustop_V #可用于主方法
sjxd5.stop_closer = utrade.atr5_ustop_j #可用于主方法

def jxu5(sif):   #
    xmod =  sif.time % 100 % 10
    signal = gand(
            gor(xmod == 4),#9,gand(xmod>=0,xmod<=2)),
            strend2(sif.mxatr)<0,            
            sif.xatr > sif.mxatr,
            sif.open > rollx(sif.close,30),
            sif.close > rollx(sif.close),
            sif.low > rollx(sif.low),            
            sif.xatr>800,
          )
    
    return np.select([signal],[sif.close],0)

bjxu5 = BXFunc(fstate=gofilter,fsignal=jxu5,fwave=gofilter,ffilter=mfilter)
bjxu5.name = u'5分钟向上投机'
bjxu5.lastupdate = 20101224
#bjxu5.stop_closer = utrade.atr5_ustop_V #可用于主方法
bjxu5.stop_closer = utrade.atr5_ustop_j #可用于主方法



####添加老系统
wxxx = [xds,xdds3,k5_d3b,xuub,K1_DDD1,K1_UUX,K1_RU,Z5_P2,xmacd3s,xup01,ua_fa,FA_15_120,K1_DVB,K1_DDUU,K1_DVBR]

#wxxx_s = [xds,xdds3,k5_d3b,K1_DDD1,Z5_P2,xmacd3s,FA_15_120]
#wxxx_b = [xuub,K1_UUX,K1_RU,xup01,ua_fa,K1_DDUU]
#wxxx_b2 = [K1_DVB,K1_DVBR]

wxxx_s = [xds,k5_d3b,Z5_P2,xmacd3s]#,FA_15_120]
wxxx_b = [xuub,xup01,K1_RU,ua_fa]   #,K1_DDUU
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

xxx = hbreak2 + rebound  + ebreak + break123c + dbreak

#txfs = [xds,k5_d3b,xuub,K1_DDD1,K1_UUX,K1_RU,Z5_P2,xmacd3s,xup01,ua_fa,FA_15_120,K1_DVB,K1_DDUU,K1_DVBR]
txfs = [xds,xuub,K1_RU,xup01,FA_15_120,K1_DVBR,Z5_P2,k5_d3b,xmacd3s,ua_fa,K1_DVB]   #剔除xdds3,K1_UUX,K1_DDD1
#K1_DDUU样本数太少，要观察

txxx = hbreak2 + txfs

xxx1 = xbreak + hbreak2 + dbreak #+ d1_rebound #+ amm #+ break123c  #此方法每日亏损20点之后趴下装死比较妥当

dxxx = d1_xbreak + d1_hbreak + dbreak #+ d1_rebound#+break123c# #+ rebound  #此方法每日亏损12点之后趴下装死比较妥当

#xxx2 = xxx +wxfs #+ wxxx
xxx2 = xxx1

xamm = amm + hbreak2    #这是一个非常好的独立策略, 作为候选, 每日亏损15点之后趴下装死

'''
计算每日亏损以及截断的统计办法
>>> tradesy =  utrade.utrade_n(i00,ufuncs.dxxx)
>>> sum([p.ntrade for p in pdays])
709
>>> sum([trade.profit for trade in tradesy])
35655
>>> len(tradesy)
481
>>> 35655/481.
74.126819126819129
>>> iftrade.max_drawdown(tradesy)    #最大连续回撤和单笔回撤
(-612, -70, 20100604)
>>> pdays =utrade.day_trades(tradesy,-200)
>>> sum([p.ntrade for p in pdays])
475
>>> sum([p.sprofit for p in pdays])
34766
>>> 34766/475.
73.191578947368427
>>> utrade.dmax_drawdown(pdays)
(-518, -220, 20100813)
>>> pdays =utrade.day_trades(tradesy,-150)
.....
'''


for x in xxx2+wxxx:
    #x.stop_closer = iftrade.atr5_uxstop_kF #60/120       
    #x.stop_closer = iftrade.atr5_uxstop_kQ #10/120       
    #x.stop_closer = iftrade.atr5_uxstop_kV #60/120/333
    x.stop_closer = utrade.atr5_ustop_V
    #x.stop_closer = utrade.atr5_ustop_5       #非常平稳
    #x.stop_closer = utrade.atr5_ustop_W1
    x.cstoper = iftrade.F60  #初始止损,目前只在动态显示时用
    if 'lastupdate' not in x.__dict__:
        x.lastupdate = 20101209

for x in rebound + d1_rebound:#反弹止损收窄
    x.stop_closer = utrade.atr5_ustop_6


###第一序列
bxbreak.stop_closer = utrade.atr5_ustop_V1
sxbreak.stop_closer = utrade.atr5_ustop_V1

shbreak_mll2.stop_closer = utrade.atr5_ustop_V
hbreak_nhh.stop_closer = utrade.atr5_ustop_V

dbreaks.stop_closer = utrade.atr5_ustop_V
dbreakb.stop_closer = utrade.atr5_ustop_V

#########候补序列
bxbreakd.stop_closer = utrade.atr5_ustop_V
sxbreakd.stop_closer = utrade.atr5_ustop_V

dhbreak_nhh.stop_closer = utrade.atr5_ustop_V
dshbreak_mll2.stop_closer = utrade.atr5_ustop_V

####AMM系列
bamm.stop_closer = utrade.atr5_ustop_V1
samm.stop_closer = utrade.atr5_ustop_V1


#b123b.stop_closer = utrade.atr5_ustop_X2

#for x in dxxx:#
#    x.stop_closer = utrade.atr5_ustop_V

