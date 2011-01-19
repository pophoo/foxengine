# -*- coding: utf-8 -*-


'''
2011-01操作指南
#################################
两张合约指南:
    1张主做xxx1a
    另一张做xxx1b, 其中tma属于信号跟随操作
#################################
信号切换规则:
    持仓时出现反向信号，当浮动收益大于25或小于3时或持仓时间大于20分钟时，平仓并开新仓，否则不变
    每日止损大于等于18点不再开仓

开仓和平仓价格的设置:
    1. 如开多目标突破价是3000，则开仓条件单应该是>=3000.2才可以，否则是不对的. 系统中都是叉或超越
    2. 平仓也如是，如果卖出平仓的目标平仓价是3000，则必须是<=2999.8才行
    3. 保本平仓的基准价格是开仓目标价,而不是执行价格.
    4. 这样才能和系统一致

理论依据:
    T1: 日的平均1分钟ATR
    T2: 日波动幅度
    T3: 稳定盈利周期

    T2/T1 > 20 才能挣钱
    T3/T2 > 5. 最小稳定盈利周期定理
    对股指期货来说, 平均下来T2/T1>20是成立的, 最小稳定盈利周期是周. 商品中Cu,Ru可能也适合日内
    对日间交易来说，有些品种T2为年，则稳定盈利周期在5-10年.

hbreak2系列
    开仓:
        做多: 1. 高点在一分钟内拉高到2分钟前日内高点+3处. 即如果上一分钟新高了，则该新高不计入内
              2. 日内高点>昨日低点+1
              3. xatr<2500,xatr5x<4000,xatr30x<10000
              4. 日内振幅>15
        做空: 1. 低点小于75分钟低点+2处
              2. 比前两天的高点中点高2个xatr(或3点). 请注意这个条件，每天早上计算该日的放空点
              3. xatr<2500,xatr5x<4000,xatr30x<10000
              4. 1330前开仓附加条件是:日内振幅>35
              5. t120<180
    平仓:
        止损为6，保本为8. 30分钟后如果盈利大于10点，则把止损拉到盈利8点或更多处
    工作时段: [1036,1435]


xbreak1v系列，连续两次突破后，放宽突破的界限，即延缓突破
    顶/底均以6分钟计，即13分钟高/低点
    开仓:
        做多:   1. 穿越上一显著高点. 
                2. 该显著高点小于当日最高20点, 大于最低点20点, 大于显著低点12点
                3. 底部抬高，或者2分钟底部比5分钟底部高. 
                   ###注意，一定要在出现一个5分钟底或2分钟底之后才下条件单. 如果没有出现底部抬高，失败率比较高
                4. 突破前一分钟高点 > 前2分钟高点
                5. 30分钟内连续两次突破后，放宽突破的界限到显著高点+3点
        做空:   1. 穿越上一显著低点-1点处. 
                2. 该显著低点大于之前的中间价-0.6
                3. 该显著低点低于前两日最高价的平均或者当日开盘价.
                4. xatr<2500,xatr5x<4000,xatr30x<10000
    平仓:
        止损为4, 保本为8. 
    工作时段:
        [1036,1435]

rebound3:
    每天只做第一次
    开仓:
        做多:   跌破前一个低点(非新低)后3分钟内涨回前低+8
                1. 跌破前一个低点(非新低)，但没有穿破该低点-3
                2. 3分钟内高点涨回前低点+8(基准线)
                3. 该基准线大于开盘价或昨日最低价
                4. 振幅大于32点
        做空:   突破前一个高点(非新高)后3分钟内跌回前高-5
                1. 突破前一个高点(非新高)+0.4, 但没有创新高
                2. 3分钟内低点跌回前高-5(基准线)
                3. 该基准线小于开盘价或昨日最高价
                4. 振幅大于32点
                5. xatr<2500,xatr5x<4000,xatr30x<10000
    平仓:
        止损为4, 保本为8. 30分钟后如果盈利大于10点，则把止损拉到盈利8点或更多处
    工作时段:
        [1036,1435]

dbreak系列，每天多空都只取第一次
    开仓:
        做多: 1.当前最高<昨日高点+6(即还未大幅突破过)
              2.开仓点为 high > 昨日最高点
              3.今日高点-今日低点和昨日收盘的低者 > 20点
              4. xatr<2500,xatr5x<4000,xatr30x<10000
        做空: 1.开仓点为 low < 昨日最低-2处
              2.今日高点和昨日收盘的高者-今日低点的低者 > 20点              
              3. xatr<2500,xatr5x<4000,xatr30x<10000
              4. t120<180
    平仓:
        止损为6，保本为8. 30分钟后如果盈利大于10点，则把止损拉到盈利8点或更多处
    工作时段:
        买多:[915,1330]
        做空:[915,1400]

xbreak早盘动作:
    顶/底均以6分钟计，即13分钟高/低点
    开仓:
        做多:   1. 穿越上一显著高点. 
                2. 该显著高点大于当日最低15点
        做空:   无
    平仓:
        止损为4, 保本为8
    工作时段:
        [916,934]

rebound2的早盘动作:
    每天只做第一次
    开仓:
        做多:   无
        做空:   创新高后5分钟内跌回到前高-6处
                1. 基准线: 5分钟之前的高点-6处
                2. 新高突破原高1点
                3. 最低价跌破基准线
                4. 新高在触发的最近5分钟内创出
                5. 振幅大于10点
    平仓:
        止损为8, 保本为8. 15分钟后如果盈利大于10点，则把止损拉到盈利8点或更多处
    工作时段:
        [959,1055]




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

##势的判断
http://www.toujidao.com/viewthread.php?tid=17287
何谓“涨势”？——  
收盘价比昨日最高价高就是涨势。  
高得越离谱表示涨势越强（你可以细分为超强势与一般强势）。  
转化为交易策略就是只考虑买进，不考虑卖出，越强越买。  

何谓“跌势”？——  
收盘价比昨日最低价低就是跌势。  
低得越离谱表示跌势越弱（你可以细分为超弱势与一般弱势）。  
转化为交易策略就是只考虑卖出，不考虑买进，越弱越卖。  
（对不起，为了加深印象，罗嗦一些也无妨，呵呵）  

何谓“盘整势”？——  
收盘价处于昨日最高价与最低价之间就是盘整势。  
盘整的幅度越宽越难以突破，维持的时间也越长。  
转化为交易策略就是不追买、也不追卖，低买高卖就行了。  

'''

from wolfox.fengine.ifuture.ibase import *
import wolfox.fengine.ifuture.iftrade as iftrade
import wolfox.fengine.ifuture.utrade as utrade
import wolfox.fengine.ifuture.fcontrol as control
from wolfox.fengine.ifuture.xfuncs import *


#主要时间过滤
def mfilter0(sif):
    return gand(
            sif.time > 1031,
            sif.time < 1455,
        )

def mfilter(sif):   
    return gand(
            sif.time > 1035,
            sif.time < 1436,
        )

def mfilter1400(sif):   
    return gand(
            sif.time > 1031,
            sif.time < 1400,
        )

def lmfilter(sif):
    return gand(
            sif.time > 1444,
            sif.time < 1510,
        )

def mfilterk(sif):
    return gand(
            sif.time >= 1400,
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

def emfilter(sif):
    return gor(
            sif.time < 935,
        )

def emfilter2(sif):
    return gand(
            sif.time >958,
            sif.time < 1056,
        )


def mfilter4(sif):   
    return gand(
            sif.time > 1114,
            sif.time < 1430,
        )


def rmfilter(sif):   
    return gor(
            sif.time <= 1031,
            gand(sif.time >= 1429,sif.time<1510),
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
            sif.time > 1429,
            sif.time < 1445,
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

def filter0(sif):
    return gand(
            sif.time>915,   #避免第一分钟的强烈波动
            sif.time<1510,
        )

def nhhx(sif,vbreak=0):
    thigh = rollx(sif.dhigh+vbreak,1)
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd)
    blow = gmin(sif.dlow,ldclose)
    signal = gand(
            #cross(rollx(sif.dhigh+30),sif.high)>0
            sif.high > thigh,
            rollx(sif.dhigh-sif.dlow) > 200,   #150可
            #rollx(sif.dhigh-blow)>200,
        )
    return np.select([signal],[gmax(sif.open,thigh)],0)    #避免跳空情况，如果跳空且大于突破点，就以开盘价进入

def nllx(sif,vbreak=0):
    tlow = rollx(sif.dlow - vbreak,1)
    signal = gand(
            sif.low < tlow,
            rollx(sif.dhigh-sif.dlow)>360,
        )
    return np.select([signal],[gmin(sif.open,tlow)],0)    #避免跳空情况，如果跳空且大于突破点，就以开盘价进入

def mhhx(sif,length=75,vbreak=0):
    thigh = rollx(tmax(sif.high,length)+vbreak,1)
    signal = gand(
            sif.high > thigh,
            rollx(sif.dhigh-sif.dlow) > 200,   #
        )
    return np.select([signal],[gmax(sif.open,thigh)],0)    #避免跳空情况，如果跳空且大于突破点，就以开盘价进入


def mllx(sif,length=75,vbreak=0):
    #使用最低点
    tlow = rollx(tmin(sif.low,length)-vbreak,1)
    signal = gand(
            sif.low < tlow,
            rollx(sif.dhigh-sif.dlow)>360, 
            sif.time < 1500,
        )
    return np.select([signal],[gmin(sif.open,tlow)],0)    #避免跳空情况，如果跳空且大于突破点，就以最低价进入
    

break_nhhx = BXFuncA(fstate=gofilter,fsignal=nhhx,fwave=gofilter,ffilter=filter0)  ##选择
break_nhhx.name = u'向上突破新高--原始X系统'
break_nllx = SXFuncA(fstate=gofilter,fsignal=nllx,fwave=nx2000X,ffilter=filter0)  ##选择
break_nllx.name = u'向下突破新低--原始X系统'

break_mhhx = BXFuncA(fstate=gofilter,fsignal=mhhx,fwave=gofilter,ffilter=filter0)  ##选择
break_mhhx.name = u'X分钟向上突破新高--原始X系统'

break_mllx = SXFuncA(fstate=gofilter,fsignal=mllx,fwave=nx2000X,ffilter=filter0)  ##选择
break_mllx.name = u'X分钟向下突破新低--原始X系统'

break_nhhxr = BXFuncA(fstate=gofilter,fsignal=nhhx,fwave=gofilter,ffilter=rmfilter)  ##选择
break_nhhxr.name = u'向上突破新高-原始X系统-前后时段'
break_nllxr = SXFuncA(fstate=gofilter,fsignal=nllx,fwave=nx2000X,ffilter=rmfilter)  ##选择
break_nllxr.name = u'向下突破新低--原始X系统-前后时段'


break_nhhx.stop_closer = utrade.atr5_ustop_V1
break_nllx.stop_closer = utrade.atr5_ustop_V1
break_mhhx.stop_closer = utrade.atr5_ustop_V1
break_mllx.stop_closer = utrade.atr5_ustop_V1

break_nhhxr.stop_closer = utrade.atr5_ustop_V1
break_nllxr.stop_closer = utrade.atr5_ustop_V1

#break_nhhx.stop_closer = utrade.atr5_ustop_V1_LK
#break_nllx.stop_closer = utrade.atr5_ustop_V1_LK
#break_mhhx.stop_closer = utrade.atr5_ustop_V1_LK
#break_mllx.stop_closer = utrade.atr5_ustop_V1_LK

break_nx = [break_nhhx,break_nllx]  #120趴下 w=6.4  #6趴下,w=7.1
break_mx = [break_mhhx,break_mllx]  #60趴下,效果很好 w=6.7  #这个参加LK
break_xx = [break_nhhx,break_mllx]  #150趴下 w=6.3
break_xr = [break_nhhxr,break_nllxr]  #150趴下 w=6.3


def nhh(sif,vbreak=30):
    #使用最高点+30, 也就是说必须一下拉开3点
    #ldlow = dnext(sif.lowd/2+sif.closed/2,sif.close,sif.i_cofd)
    ldlow = dnext(sif.lowd,sif.close,sif.i_cofd)
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    thigh = rollx(sif.dhigh+vbreak,2)
    signal = gand(
            #cross(rollx(sif.dhigh+30),sif.high)>0
            sif.high > thigh,
            rollx(sif.dhigh) > ldlow + 10,     #大于昨日低点
            rollx(sif.dhigh-sif.dlow)>150,
            #gor(sif.time>=1330,rollx(sif.dhigh-sif.dlow)>200),
        )
    return np.select([signal],[gmax(sif.low,thigh)],0)    #避免跳空情况，如果跳空且大于突破点，就以跳空价进入
    
def nll2(sif,vbreak=20):
    #使用最低点
    ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)    
    return gand(
            #cross(rollx(sif.dlow-30),sif.low)<0
            sif.low < rollx(sif.dlow+vbreak,3), #比close要小点
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


break_nhh0 = BXFuncA(fstate=gofilter,fsignal=fcustom(nhh,vbreak=0),fwave=nx2500X,ffilter=filter0)  ##选择
break_nhh0.name = u'向上突破新高--原始系统'
    

break_nhh = BXFuncA(fstate=gofilter,fsignal=nhh,fwave=nx2500X,ffilter=nfilter)  ##选择
break_nhh.name = u'向上突破新高'
hbreak_nhh = BXFuncA(fstate=gofilter,fsignal=nhh,fwave=nx2500X,ffilter=mfilter)  ##主要时段
hbreak_nhh.name = u'日内向上突破新高'

hbreak_nhh_k = BXFuncA(fstate=gofilter,fsignal=nhh,fwave=nx2500X,ffilter=mfilterk)  ##主要时段
hbreak_nhh_k.name = u'日内向上突破新高'
hbreak_nhh_k.stop_closer = utrade.atr5_ustop_V


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

sbreak_nll20 = SXFuncA(fstate=gofilter,fsignal=fcustom(nll2,vbreak=0),fwave=nx2500X,ffilter=filter0)    #这个R高，但是次数少
sbreak_nll20.name = u'向下突破--原始系统'


sbreak_nll2 = SXFuncA(fstate=sdown,fsignal=nll2,fwave=nx2500X,ffilter=nfilter)    #这个R高，但是次数少
sbreak_nll2.name = u'向下突破2'
shbreak_nll2 = SXFuncA(fstate=sdown,fsignal=nll2,fwave=nx2500X,ffilter=mfilter)    #

skbreak_nll2 = SXFuncD1(fstate=sdown,fsignal=nll2,fwave=nx2500X,ffilter=kfilter)    #
#skbreak_nll2.stop_closer = utrade.atr5_ustop_V

#sbreak_nlc + sbreak_nlc_break = sbreak_nll2

zbreak0 = [break_nhh0,sbreak_nll20] #这个最好,理念最清晰

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
    tlow = rollx(tmin(sif.low,length)+vbreak,1)
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    #ldmid = dnext((sif.highd+gmin(sif.closed,sif.opend))/2,sif.close,sif.i_cofd)
    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    #opend = dnext(sif.opend,sif.open,sif.i_oofd)            
    #highd = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)            
    #ldmid = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)        
    #ldmid = dnext(sif.highd,sif.close,sif.i_cofd)        
    #ldmid = dnext((sif.highd+sif.closed)/2,sif.close,sif.i_cofd)    
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd) 

    signal = gand(
            #sif.time>1029,
            cross(tlow,sif.low)<0,
            #strend2(sif.low) <= 0,
            #sif.low < tlow,
            #tlow < rollx(sif.dhigh + sif.dlow)/2, #+ sif.dlow
            #tlow < ldhigh-10,  #比昨日最高价低才允许做空
            tlow < ldmid-30,#rollx(sif.xatr)*2/XBASE,  #比前2天高点中点低才允许做空
            #tlow < sif.dmid,
            #tlow < highd,
            #rollx(sif.dhigh - sif.dlow) > 150, 
            gor(sif.time>=1330,rollx(sif.dhigh-sif.dlow)>350),
            sif.time > 915,
        )
    return np.select([signal],[gmin(sif.open,tlow)],0)    #避免跳空情况，如果跳空且小于突破点，就以跳空价进入
    
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

shbreak_mll2_k = SXFuncA(fstate=gofilter,fsignal=mll2,fwave=nx2500X,ffilter=mfilterk)  ##主要时段
shbreak_mll2_k.name = u'日内向下突破新低'
shbreak_mll2_k.stop_closer = utrade.atr5_ustop_X4


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
def bru_old(sif):
    #突破前一日高点
    ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    signal = gand(
            sif.high > ldhigh + 6,
            rollx(sif.dhigh) < ldhigh +60,  #还没拉开过, 如果是915则必然满足
            rollx(sif.sk > sif.sd),
            sif.time < 1330,
            sif.dhigh - sif.dlow > 60,
            #sif.time>914, 
            #sif.time>915,
            #sif.r120>0,
        )
    return np.select([signal],[gmax(sif.open,ldhigh)],0)    #避免跳空情况，如果跳空且大于突破点，就以最低价进入

def bru(sif):
    #突破前一日高点
    ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd)    
    signal = gand(
            sif.high > ldhigh ,
            rollx(sif.dhigh) < ldhigh + 60,  #还没拉开过, 如果是915则必然满足
            rollx(sif.dhigh - gmin(sif.dlow,ldclose)) > 200,
            #rollx(sif.dhigh - sif.dlow) > 200,
            sif.time<1331,
            sif.time>914,
            #rollx(sif.xatr>600),
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

def brd_old(sif):
    ldlow = dnext(sif.lowd,sif.close,sif.i_cofd)
    signal = gand(
            sif.low < ldlow - 30,  
            rollx(sif.sk < sif.sd),
            sif.time < 1430,
            sif.time>914,
            #sif.t120<60,
        )
    return np.select([signal],[gmin(sif.open,ldlow-30)],0)    #避免跳空/skdj后延情况，如果跳空且大于突破点，就以分钟开盘价进入

def brd(sif):
    ldlow = dnext(sif.lowd,sif.close,sif.i_cofd) - 20
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd)        
    signal = gand(
            sif.low < ldlow ,  
            rollx(gmax(sif.dhigh,ldclose) - sif.dlow) > 200,
            #rollx(sif.dhigh - sif.dlow) > 200,
            sif.time < 1401,
            sif.time> 914,
            #sif.t120<60,
        )
    return np.select([signal],[gmin(sif.open,ldlow)],0)    #避免跳空/skdj后延情况，如果跳空且大于突破点，就以分钟开盘价进入

def brdh(sif):
    #最高价低于前日最低价+20，则以收盘价买入
    ldlow = dnext(sif.lowd,sif.close,sif.i_cofd)
    signal = gand(
            sif.high < ldlow +20,   #这个有点无耻,走的不是突破了, 就是说等最高价低于昨日最低+20才在收盘进入
            rollx(sif.dlow) < ldlow -100,    #已经下去过了之后，再穿越. 这个被部分吸收了
            rollx(sif.sk < sif.sd),
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
dbreaks.lastupdate = 20101213

edbreakb = BXFuncD1(fstate=gofilter,fsignal=bru,fwave=nx2500X,ffilter=emfilter)
edbreakb.name = u'早盘突破前日高点'
edbreakb.lastupdate = 20101213
edbreakb.stop_closer = utrade.atr5_ustop_X4

edbreaks = SXFuncD1(fstate=sdown,fsignal=brd,fwave=nx2500X,ffilter=emfilter)
edbreaks.name = u'早盘突破前日低点'
edbreaks.lastupdate = 20101213
edbreaks.stop_closer = utrade.atr5_ustop_X4


dbreak = [dbreakb,dbreaks]#

edbreak = [edbreakb,edbreaks]#

dbreaksh.stop_closer = utrade.atr5_ustop_V

dbreakb2 = BXFuncD1(fstate=gofilter,fsignal=brux,fwave=nx2500X,ffilter=efilter)
dbreakb2.name = u'突破前日高点'
dbreakb2.lastupdate = 20101213
dbreakb2.stop_closer = utrade.atr5_ustop_V1

###Larry Williams###
'''
短线交易秘诀
1. 哎呀交易
   价格跳空高开，当往下杀到昨日最高价时卖出
   价格跳空低开，当往上反弹到昨日最低价时买入
2. 最大振荡幅度. 在上涨的日子中寻找下跌振荡，在下跌日子中寻找上涨振荡
   卖出振荡幅度: 过去3天开盘价-最低价的均值, 应用时必须确认前一天的收盘价>开盘价. 即是自由下跌，而非惯性
   买入振荡幅度: 过去3天最高价-开盘价的均值, 应用时必须确认前一天的收盘价<开盘价
   这些振荡幅度实际上是最大失败振荡幅度，因为最终该日的走势是相反的
   这样，在上涨日计算下跌振荡突破时，最好要求当日收盘价大于5天前收盘价
         在下跌日计算上涨振荡突破时，最好要求当日收盘价小于5天前收盘价
   向上突破系数: 1.8倍，向下2.5倍。自行优化
3. 区间扩张
   以开盘价为基准，前一日振幅为区间RANGE大小.
   买入: 突破上0.4个RANGE (0.8)
   卖出: 突破下2个RANGE   (1.2)
   也可以3天前最高-昨天最低, 以及昨日最高-3天前最低的大者为区间.
'''
##AY交易
def ayu(sif):
    #价格跳空低开，当往上反弹到昨日最低价时开多
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd)
    ldlow = dnext(sif.lowd,sif.close,sif.i_cofd)    
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)    
    bline = ldlow - 30  #感觉缺口有牵引力
    signal = gand(
            ldopen < ldlow,
            cross(bline,sif.high)>0,
            #rollx(sif.dhigh - gmin(sif.dlow,ldclose)) > 200,
            #rollx(sif.dhigh - sif.dlow) > 200,
            sif.time>915,
            #sif.time < 1430,
            #rollx(sif.xatr>600),
        )
    return np.select([signal],[gmax(sif.open,bline)],0)    #避免跳空情况，如果跳空且大于突破点，就以最低价进入

def ayd(sif):
    #价格跳空低开，当往下到昨日最高价时开空
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd)
    ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)    
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)
    bline = ldhigh - 10
    signal = gand(
            ldopen > ldhigh,
            cross(bline,sif.low)<0,
            #rollx(sif.dhigh - gmin(sif.dlow,ldclose)) > 200,
            #rollx(sif.dhigh - sif.dlow) > 200,
            sif.time>915,
            sif.time <1130,
            #rollx(sif.xatr>600),
        )
    return np.select([signal],[gmin(sif.open,bline)],0)    #避免跳空情况，如果跳空且大于突破点，就以最低价进入


bayu = BXFuncF1(fstate=gofilter,fsignal=ayu,fwave=gofilter,ffilter=gofilter)
bayu.name = u'跳空低开后突破前日低点'
bayu.lastupdate = 20110110
bayu.stop_closer = utrade.atr5_ustop_X1     #样本数太少

sayd = SXFuncF1(fstate=gofilter,fsignal=ayd,fwave=gofilter,ffilter=gofilter)
sayd.name = u'跳空高开后跌破前日高点'
sayd.lastupdate = 20110110
sayd.stop_closer = utrade.atr5_ustop_V1     #样本数太少

ay = [bayu,sayd]    #需要观察到样本数>50

##价格扩张
def erangeu(sif):
    erange = dnext(sif.highd-sif.lowd,sif.close,sif.i_cofd)
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)    
    bline = ldopen + erange / 3
    signal = gand(
            cross(bline,sif.high)>0,
            #rollx(sif.dhigh - gmin(sif.dlow,ldclose)) > 200,
            #rollx(sif.dhigh - sif.dlow) > 200,
            sif.time > 945,
            sif.time < 1400,
            #sif.time < 1430,
            #rollx(sif.xatr>600),
        )
    return np.select([signal],[gmax(sif.open,bline)],0)    #避免跳空情况，如果跳空且大于突破点，就以最低价进入

def erangeu2(sif):
    erange = dnext(gmax(sif.highd-rollx(sif.lowd,3),rollx(sif.highd,3)-rollx(sif.lowd)),sif.close,sif.i_cofd)
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)    
    bline = ldopen + erange / 2
    signal = gand(
            cross(bline,sif.high)>0,
            #rollx(sif.dhigh - gmin(sif.dlow,ldclose)) > 200,
            #rollx(sif.dhigh - sif.dlow) > 200,
            sif.time > 945,
            sif.time < 1400,
            #sif.time < 1430,
            #rollx(sif.xatr>600),
        )
    return np.select([signal],[gmax(sif.open,bline)],0)    #避免跳空情况，如果跳空且大于突破点，就以最低价进入


berangeu = BXFuncD1(fstate=gofilter,fsignal=erangeu,fwave=nx2500X,ffilter=gofilter)
berangeu.name = u'扩张向上'
berangeu.lastupdate = 20110110
berangeu.stop_closer = utrade.atr5_ustop_V1

berangeu2 = BXFuncD1(fstate=gofilter,fsignal=erangeu2,fwave=nx2500X,ffilter=gofilter)
berangeu2.name = u'扩张向上'
berangeu2.lastupdate = 20110110
berangeu2.stop_closer = utrade.atr5_ustop_V1

berange = [berangeu,berangeu2]

def eranged(sif):
    erange = dnext(sif.highd-sif.lowd,sif.close,sif.i_cofd)
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)    
    bline = ldopen - erange
    signal = gand(
            cross(bline,sif.low)<0,
            #rollx(sif.dhigh - gmin(sif.dlow,ldclose)) > 200,
            #rollx(sif.dhigh - sif.dlow) > 200,
            sif.time > 945,
            sif.time < 1400,
            #sif.time < 1430,
            #rollx(sif.xatr>600),
        )
    return np.select([signal],[gmin(sif.open,bline)],0)    #避免跳空情况，如果跳空且大于突破点，就以最低价进入

def eranged2(sif):
    erange = dnext(gmax(sif.highd-rollx(sif.lowd,3),rollx(sif.highd,3)-rollx(sif.lowd)),sif.close,sif.i_cofd)
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)    
    bline = ldopen - erange / 3
    signal = gand(
            cross(bline,sif.low)<0,
            #rollx(sif.dhigh - gmin(sif.dlow,ldclose)) > 200,
            #rollx(sif.dhigh - sif.dlow) > 200,
            sif.time > 945,
            sif.time < 1400,
            #sif.time < 1430,
            #rollx(sif.xatr>600),
        )
    return np.select([signal],[gmin(sif.open,bline)],0)    #避免跳空情况，如果跳空且大于突破点，就以最低价进入


seranged = SXFuncD1(fstate=gofilter,fsignal=eranged,fwave=gofilter,ffilter=gofilter)
seranged.name = u'扩张向下'
seranged.lastupdate = 20110110
seranged.stop_closer = utrade.atr5_ustop_V1

seranged2 = SXFuncD1(fstate=gofilter,fsignal=eranged2,fwave=gofilter,ffilter=gofilter)
seranged2.name = u'扩张向下2'
seranged2.lastupdate = 20110110
seranged2.stop_closer = utrade.atr5_ustop_V1

serange = [seranged,seranged2]

erange = berange + serange      #一组非常好的独立策略

###失败振荡
def ufwave(sif):
    fwave = dnext(ma(sif.highd-sif.opend,3),sif.close,sif.i_cofd)
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)    

    #ldc1 = dnext(sif.closed,sif.close,sif.i_cofd)
    #ldc2 = dnext(rollx(sif.closed,3),sif.close,sif.i_cofd)
    bline = ldopen + fwave * 4/3
    signal = gand(
            cross(bline,sif.high)>0,
            #rollx(sif.dhigh - gmin(sif.dlow,ldclose)) > 200,
            #rollx(sif.dhigh - sif.dlow) > 200,
            sif.time > 944,
            sif.time < 1331,
            #ldc1 < ldc2,
            #sif.time < 1430,
            #rollx(sif.xatr>600),
        )
    return np.select([signal],[gmax(sif.open,bline)],0)    #避免跳空情况，如果跳空且大于突破点，就以最低价进入

def dfwave(sif):
    fwave = dnext(ma(sif.highd-sif.opend,3),sif.close,sif.i_cofd)
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)    

    ldc1 = dnext(sif.closed,sif.close,sif.i_cofd)
    ldc2 = dnext(rollx(sif.closed,3),sif.close,sif.i_cofd)
    bline = ldopen - fwave * 5/3
    signal = gand(
            cross(bline,sif.low)<0,
            #rollx(sif.dhigh - gmin(sif.dlow,ldclose)) > 200,
            #rollx(sif.dhigh - sif.dlow) > 200,
            sif.time > 930,
            sif.time < 1331,
            #ldc1 < ldc2,
            #sif.time < 1430,
            #rollx(sif.xatr>600),
        )
    return np.select([signal],[gmin(sif.open,bline)],0)    #避免跳空情况，如果跳空且大于突破点，就以最低价进入


bfwave = BXFuncD1(fstate=gofilter,fsignal=ufwave,fwave=gofilter,ffilter=gofilter)
bfwave.name = u'振荡突破向上'
bfwave.lastupdate = 20110110
bfwave.stop_closer = utrade.atr5_ustop_V1

sfwave = SXFuncD1(fstate=gofilter,fsignal=dfwave,fwave=gofilter,ffilter=gofilter)
sfwave.name = u'振荡突破向下'
sfwave.lastupdate = 20110110
sfwave.stop_closer = utrade.atr5_ustop_V1

fwave = [bfwave,sfwave]

lwilliams = erange + fwave  #叠加无效果， 单独的以erange为好

for x in lwilliams:
    x.stop_closer = utrade.atr5_ustop_V1    

###123/2B
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
         这个算法需要进一步的仔细研究，是不是存在未来数据
         并增强可操作性
    '''

    plen = 4
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
    tp = np.select([lll>rollx(sif.dlow),lll==rollx(sif.dlow)],[gmin(lll+20,xp),xp]) #只有在10:30之前才可能!=low75

    #slx = np.select([lll>sif.dlow,rpll>sif.dlow,rpll2>sif.dlow],[sif.dlow-lll,sif.dlow-rpll,sif.dlow-rpll2],99999999)

    signal = gand(#shh<90,    #不震荡
                #slx < 100,  #发现无必要
                rollx(tmin(sif.low,15)) == rollx(sif.dlow),#15分钟创了新低
                cross(tp,sif.high)>0,
                sif.time>915,   #915会有跳空
                sif.xatr > 1500,
                rollx(sif.high - sif.dlow) > 120,#这个可能用到未来数据
            )
    return np.select([signal],[gmax(sif.open,tp)],0)

def drebound(sif):
    '''
         创新高后以跌破支撑为界
         可扩展至未创新高?
         这个算法需要进一步的仔细研究，是不是存在未来数据
         并增强可操作性
    '''

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

    #lpchh = extend2next(pchh)
    #lpcll = extend2next(pcll)

    #iphh = np.nonzero(phh)
    #rphh = np.zeros_like(phh)
    #rphh[iphh] = rollx(phh[iphh])
    #rphh = extend2next(rphh) +10

    #tp = (lll + rollx(sif.dlow)) / 2#(rpll + lll)/2
    #tp = np.select([lll>sif.dlow,rpll>sif.dlow,rpll==sif.dlow],[(lll+sif.dlow)/2,(rpll+sif.dlow)/2,mlow_last(sif,vlen=10)])
    
    xp = signal_last(sif.dhigh,vlen=30) - 60
    tp = np.select([lhh<rollx(sif.dhigh),lhh==rollx(sif.dhigh)],[gmin(lhh-20,xp),xp])
    #tp = lll

    signal = gand(#shh>0,    #不震荡
                rollx(tmax(sif.high,15)) == rollx(sif.dhigh),
                cross(tp,sif.low)<0,
                sif.time>915,   #915会有跳空
                #strend2(sif.mxatr30x) < 0,
                sif.xatr<1500,
                #sif.dhigh - sif.low > 100,
            )
    return np.select([signal],[gmin(sif.open,tp)],0)

def urebound2(sif):
    '''
         创新高后以跌破支撑为界
         可扩展至未创新高?
         这个算法需要进一步的仔细研究，是不是存在未来数据
         并增强可操作性
    '''

    #tp = signal_last(sif.dlow,vlen=3) + 80
    tp = rollx(sif.dlow,15)+90

    signal = gand(#shh>0,    #不震荡
                rollx(tmin(sif.low,10)) == rollx(sif.dlow),
                sif.dlow < tp - 100,
                sif.dlow > tp - 200, 
                cross(tp,sif.high)>0,
                sif.xatr < 1500,
            )
    return np.select([signal],[gmax(sif.open,tp)],0)


def drebound2(sif):
    '''
         创新高后以跌破支撑为界
    '''

    #tp = signal_last(sif.dhigh,30) - 60
    #bline = np.select([rollx(sif.atr)*6/5/XBASE > 60],[rollx(sif.atr)*6/5/XBASE],60)
    #tp = rollx(sif.dhigh,5)-60
    #tp = rollx(sif.dhigh,5)-rollx(sif.atr) *6/5/XBASE

    bline = 60 #最简单，免去计算, 但不入ATR方式稳定
    tline = 5  #创新高后tline分钟内跌回
    tp = rollx(sif.dhigh,tline)-bline

    signal = gand(#shh>0,    #不震荡
                rollx(tmax(sif.high,tline)) == rollx(sif.dhigh),
                sif.dhigh > tp + bline +10, #突破加1点
                #sif.dhigh < tp + bline +70, #突破加1点
                #sif.dhigh < tp + bline +60, #突破加1点
                #sif.dhigh > tp + 10 + rollx(sif.atr)*6/5/XBASE,
                cross(tp,sif.low)<0,
                rollx(sif.dhigh - sif.dlow)>100,
                #sif.time>1000,   #915会有跳空
                #sif.time < 1046,
                #strend2(sif.mxatr30x) < 0,
                #sif.xatr<1500,
            )
    return np.select([signal],[gmin(sif.open,tp)],0)

def urebound3(sif):
    '''
         跌破前一个低点(非新低)后3分钟内涨回前低+8
    '''

    phh,pll = calc_lh(sif,plen=6)

    sll = extend2next(ssub(pll))
    shh = extend2next(ssub(phh))

    lhh = extend2next(phh)
    lll = extend2next(pll)

    bline = 80 #最简单，免去计算, 但不入ATR方式稳定
    tline = 3  #突破后tline分钟内跌回
    tp = lll + bline#rollx(sif.dhigh,tline)-bline

    ldlow = dnext(sif.lowd,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)        

    signal = gand(
                rollx(tmin(sif.low,tline)) < lll ,
                rollx(tmin(sif.low,tline)) > lll - 30, 
                rollx(tmin(sif.low,tline)) > rollx(sif.dlow),
                cross(tp,sif.high)>0,
                rollx(sif.dhigh-sif.dlow)>320,
                #gor(tp > opend)#,tp>ldmid),
                gor(tp > opend,tp>ldlow),
            )
    return np.select([signal],[gmax(sif.open,tp)],0)


def drebound3(sif):
    '''
         突破前一个高点(非新高)后3分钟内跌回前高-5
    '''

    phh,pll = calc_lh(sif,plen=6)

    sll = extend2next(ssub(pll))
    shh = extend2next(ssub(phh))

    lhh = extend2next(phh)
    lll = extend2next(pll)

    bline = 50 #最简单，免去计算 
    tline = 3  #突破后tline分钟内跌回
    tp = lhh - bline#rollx(sif.dhigh,tline)-bline

    ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)        

    signal = gand(
                rollx(tmax(sif.high,tline)) > lhh + 4,
                rollx(tmax(sif.high,tline)) < rollx(sif.dhigh),    #没创新高
                cross(tp,sif.low)<0,
                rollx(sif.dhigh-sif.dlow)>320,
                gor(tp < opend,tp<ldhigh),  #加了这个以后叠加效果好
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

brebound2 = BXFuncD1(fstate=gofilter,fsignal=urebound2,fwave=gofilter,ffilter=emfilter2)    #样本数太少
brebound2.name = u'向上反弹'
brebound2.lastupdate = 20101225
brebound2.stop_closer = utrade.atr5_ustop_X1

brebound3 = BXFuncD1(fstate=sdown,fsignal=urebound3,fwave=gofilter,ffilter=mfilter)    #样本数太少
brebound3.name = u'向上反弹3'
brebound3.lastupdate = 20110115
brebound3.stop_closer = utrade.atr5_ustop_TV1

srebound2 = SXFuncD1(fstate=gofilter,fsignal=drebound2,fwave=gofilter,ffilter=emfilter2)
srebound2.name = u'向下反弹'
srebound2.lastupdate = 20101225
srebound2.stop_closer = utrade.atr5_ustop_X1

srebound3 = SXFuncD1(fstate=sdown,fsignal=drebound3,fwave=nx2500X,ffilter=mfilter)
srebound3.name = u'向下反弹3'
srebound3.lastupdate = 20110115
srebound3.stop_closer = utrade.atr5_ustop_TV1


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

rebound2 = [srebound2]#,brebound] #brebound2样本数太少，暂时忽略
rebound3 = [srebound3,brebound3] 

###普通形态突破

def uxbreak(sif,tbegin=1030):
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
    tp = np.select([gor(tp<rollx(sif.dhigh)-90,sif.time<945)],[tp],99999999)   #距离突破线比较近的，交给突破    
    #tp = np.select([gor(gand(tp<sif.dhigh-80,rollx(sif.high)<sif.dhigh-30),sif.time<945)],[tp],99999999)   #距离突破线比较近的，交给突破

    #print tp[-140:],sif.high[-140:],lhh[-140:]

    tp2 = lhh + 80  #假动作之后抬升
    tp2 = np.select([gor(tp2<rollx(sif.dhigh)-90,sif.time<945)],[tp2],99999999)   #距离突破线比较近的，交给突破
    #tp2 = np.select([gor(gand(tp2<sif.dhigh-80,rollx(sif.high)<sif.dhigh-30),sif.time<945)],[tp2],99999999)   #距离突破线比较近的，交给突破

    #ldlow = dnext(gmin(sif.lowd,rollx(sif.lowd)),sif.close,sif.i_cofd)
    mhh = rollx(tmax(sif.high,75))
    mll = rollx(tmin(sif.low,75))

    signal = gand(#shh<90,    #不震荡
                gor(lll2 > lll,sll>0),
                #lll2>lll,
                #sll>0,
                cross(tp,sif.high)>0,
                #tp <= rollx(tp),#不是从99999999下来的被上叉
                #rollx(tp)<=tp,
                strend2(sif.high)>0,
                sif.time>915,   #915会有跳空
                tp - sif.dlow > 150,
                #sif.xatr > sif.mxatr,
                #strend2(sif.mxatr)>0,
                sif.xatr > 800,
                #lhh>lll+40,
                #rollx(sif.dhigh - sif.dlow) > 100,  
                mhh-mll>250,
                sif.time > tbegin,  #避免之前信号被重复计算
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
                mhh-mll>250,
            )
    signal = np.select([msignal<3,msignal>=3],[signal,signal2],0)
    ptp = np.select([msignal<3,msignal>=3],[tp,tp2],0)
    return np.select([signal],[gmax(sif.open,ptp)],0)
    #return np.select([signal],[gmax(sif.open,tp)],0)

def euxbreak(sif,tbegin=1030):
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


    tp = lhh 

    signal = gand(
                #gor(lll2 > lll,sll>0),
                cross(tp,sif.high)>0,
                sif.time>915,   #915会有跳空
                tp - sif.dlow > 150,
            )
    return np.select([signal],[gmax(sif.open,tp)],0)

def edxbreak(sif):
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


    tp = lll 

    signal = gand(
                #gor(lll2 > lll,sll>0),
                cross(tp,sif.low)<0,
                sif.time>915,   #915会有跳空
                sif.dhigh - tp > 150,
            )
    return np.select([signal],[gmin(sif.open,tp)],0)


def uxbreak1(sif,tbegin=1030):
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


    tp = lhh 

    tp = np.select([tp<rollx(sif.dhigh-30)],[tp],99999999)   #距离突破线比较近的，交给突破    
    #print tp[-170:]

    tp2 = lhh + 60  #假动作之后抬升
    tp2 = np.select([tp2<rollx(sif.dhigh-30)],[tp2],99999999)   #距离突破线比较近的，交给突破
    #tp2 = np.select([gor(gand(tp2<sif.dhigh-80,rollx(sif.high)<sif.dhigh-30),sif.time<945)],[tp2],99999999)   #距离突破线比较近的，交给突破
    mhh = rollx(tmax(sif.high,75))
    mll = rollx(tmin(sif.low,75))

    signal = gand(#shh<90,    #不震荡
                gor(lll2 > lll,sll>0),
                cross(tp,sif.high)>0,
                #rollx(tp) > tp,#不是从99999999下来的被上叉
                rollx(tp) != 99999999,#剔除, 因为这肯定是突破超过3点后造成的
                rollx(strend2(sif.high))>0,
                #strend2(sif.high)>0,
                sif.time>915,   #915会有跳空
                tp - sif.dlow > 200,
                lhh>lll+80,
                sif.time > tbegin,  #避免之前信号被重复计算
            )

    #msignal = msum(signal,30)
    #signal2 = gand(
    #            gor(lll2 > lll,sll>0),
    #            cross(tp2,sif.high)>0,
    #            tp <= rollx(tp),#不是从99999999下来的被上叉                
    #            sif.time>915,   #915会有跳空
    #            tp2 - sif.dlow > 200,
    #            lhh>lll+80,                
    #        )
    #signal = np.select([msignal<3,msignal>=3],[signal,signal2],0)
    #ptp = np.select([msignal<3,msignal>=3],[tp,tp2],0)
    #return np.select([signal],[gmax(sif.open,ptp)],0)
    return np.select([signal],[gmax(sif.open,tp)],0)

def uxbreak1b(sif,tbegin=1030):
    '''
        向上突破、超过3点后进入
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


    tp = lhh 

    tp = np.select([tp<rollx(sif.dhigh-30)],[tp],99999999)   #距离突破线比较近的，交给突破    
    #print tp[-170:]

    tp2 = lhh + 60  #假动作之后抬升
    tp2 = np.select([tp2<rollx(sif.dhigh-30)],[tp2],99999999)   #距离突破线比较近的，交给突破
    #tp2 = np.select([gor(gand(tp2<sif.dhigh-80,rollx(sif.high)<sif.dhigh-30),sif.time<945)],[tp2],99999999)   #距离突破线比较近的，交给突破
    mhh = rollx(tmax(sif.high,75))
    mll = rollx(tmin(sif.low,75))

    signal = gand(#shh<90,    #不震荡
                gor(lll2 > lll,sll>0),
                cross(tp,sif.high)>0,
                #rollx(tp) >= tp,#不是从99999999下来的被上叉
                rollx(tp) == 99999999,#剔除, 因为这肯定是突破超过3点后造成的
                rollx(strend2(sif.high))>0,
                #strend2(sif.high)>0,
                sif.time>915,   #915会有跳空
                tp - sif.dlow > 200,
                lhh>lll+80,
                sif.time > tbegin,  #避免之前信号被重复计算
            )

    msignal = msum(signal,30)
    signal2 = gand(
                gor(lll2 > lll,sll>0),
                cross(tp2,sif.high)>0,
                tp <= rollx(tp),#不是从99999999下来的被上叉                
                sif.time>915,   #915会有跳空
                tp2 - sif.dlow > 200,
                lhh>lll+80,                
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

    tp = np.select([gor(tp<rollx(sif.dhigh-80),sif.time<945)],[tp],99999999)   #距离突破线比较近的，交给突破
    #tp = gmax(tp,sif.dlow+151)

    tp2 = lhh + 80  #假动作之后抬升
    tp2 = np.select([gor(tp2<rollx(sif.dhigh-80),sif.time<945)],[tp2],99999999)   #距离突破线比较近的，交给突破

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


def dxbreak(sif,tbegin=1030):
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

    tlow = rollx(tmin(sif.low,75))
    #tp = np.select([gor(tp>tlow+60,sif.time<=1031,sif.time>=1430)],[tp],0) #接近低点的给突破
    tp = np.select([gor(tp>tlow+120)],[tp],0) #接近低点的给突破
    #tp = np.select([gand(tp>tlow+60,rollx(sif.low)>tlow+30)],[tp],0) #接近低点的给突破

    tp2 = lll - 50  #假动作之后降低
    tp2 = np.select([tp2>tlow+120],[tp2],0) #接近低点的给突破

    #ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    #ldmid = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)    
    ldmid = dnext(sif.highd,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)        

    mhh = rollx(tmax(sif.high,75))
    mll = rollx(tmin(sif.low,75))

    signal = gand(#sll<0,    #不震荡
                #rollx(sif.sdma)>0,
                #gor(lhh2 < lhh,shh<0),
                cross(tp,sif.low)<0,
                sif.time>915,   #915会有跳空
                #tp >= rollx(tp),    #不是从0起来的被交叉
                #sif.xatr>sif.mxatr,
                #sif.xatr<2500,
                #sif.xatr30x < 10000,
                #sif.xatr5x < 4000,
                #sif.dhigh - sif.low>60,
                gor(tp < ldmid,tp<opend),#-sif.xatr*2/XBASE,  #比前2天高点中点低才允许做空                
                rollx(sif.dhigh - sif.dlow) > 100, 
                sif.time > tbegin,  #避免之前信号被重复计算
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
                gor(tp2 < ldmid,tp2<opend),#-sif.xatr*2/XBASE,  #比前2天高点中点低才允许做空                
                rollx(sif.dhigh - sif.dlow) > 100,  
            )
    signal = np.select([msignal<3,msignal>=3],[signal,signal2],0)
    ptp = np.select([msignal<3,msignal>=3],[tp,tp2],0)
    return np.select([signal],[gmin(sif.open,ptp)],0)
    #return np.select([signal],[gmin(sif.open,tp)],0)

def dxbreak1(sif,tbegin=1030):
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

    
    tp = lll-10
    #tp = lll

    tlow = rollx(sif.dlow)
    #tp = np.select([gor(tp>tlow+60,sif.time<=1031,sif.time>=1430)],[tp],0) #接近低点的给突破
    tp = np.select([gor(tp>tlow+140)],[tp],0) #接近低点的给突破
    #tp = np.select([gand(tp>tlow+60,rollx(sif.low)>tlow+30)],[tp],0) #接近低点的给突破


    #ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    #ldmid = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)    
    #ldmid = dnext(sif.highd,sif.close,sif.i_cofd)    
    ldmid = dnext(sif.highd/2+rollx(sif.highd)/2,sif.close,sif.i_cofd)    
    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)        


    signal = gand(#sll<0,    #不震荡
                #rollx(sif.sdma)>0,
                #gor(lhh2 < lhh,shh<0),
                shh<0,
                cross(tp,sif.low)<0,
                #sif.low < tp,
                sif.time>915,   #915会有跳空
                #tp >= rollx(tp),    #不是从0起来的被交叉
                rollx(tp)>0,   #这个肯定是新低造成的
                #sif.xatr>sif.mxatr,
                #sif.xatr<2500,
                #sif.xatr30x < 10000,
                #sif.xatr5x < 4000,
                #sif.dhigh - sif.low>60,
                #gor(tp < ldmid,tp<opend),#-sif.xatr*2/XBASE,  #比前2天高点中点低才允许做空                
                #rollx(sif.dhigh - sif.dlow) > 100, 
                #rollx(sif.dhigh - sif.dlow) > 200, 
                #rollx(sif.dhigh)- tp >100,
            )
    
    return np.select([signal],[gmin(sif.open,tp)],0)

def dxbreak1b(sif,tbegin=1030):
    '''
        向下突破、回调，再突破
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

    
    tp = lll-10
    #tp = lll

    tlow = rollx(sif.dlow)
    #tp = np.select([gor(tp>tlow+60,sif.time<=1031,sif.time>=1430)],[tp],0) #接近低点的给突破
    tp = np.select([gor(tp>tlow+140)],[tp],0) #接近低点的给突破
    #tp = np.select([gand(tp>tlow+60,rollx(sif.low)>tlow+30)],[tp],0) #接近低点的给突破


    #ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    #ldmid = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)    
    ldmid = dnext(sif.highd,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)        


    signal = gand(#sll<0,    #不震荡
                #rollx(sif.sdma)>0,
                #gor(lhh2 < lhh,shh<0),
                shh<0,
                cross(tp,sif.low)<0,
                #sif.low < tp,
                sif.time>915,   #915会有跳空
                #tp >= rollx(tp),    #不是从0起来的被交叉
                rollx(tp)==0,   #这个肯定是新低造成的
                #sif.xatr>sif.mxatr,
                #sif.xatr<2500,
                #sif.xatr30x < 10000,
                #sif.xatr5x < 4000,
                #sif.dhigh - sif.low>60,
                #gor(tp < ldmid,tp<opend),#-sif.xatr*2/XBASE,  #比前2天高点中点低才允许做空                
                #rollx(sif.dhigh - sif.dlow) > 100, 
                #rollx(sif.dhigh - sif.dlow) > 200, 
                #rollx(sif.dhigh)- tp >100,
            )
    
    return np.select([signal],[gmin(sif.open,tp)],0)

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

def uxbreak1c(sif,tbegin=1030):
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


    tp = lhh 

    tp = np.select([tp<rollx(sif.dhigh-30)],[tp],99999999)   #距离突破线比较近的，交给突破    

    tp2 = lhh + 60  #假动作之后抬升
    tp2 = np.select([tp2<rollx(sif.dhigh-30)],[tp2],99999999)   #距离突破线比较近的，交给突破
    #tp2 = np.select([gor(gand(tp2<sif.dhigh-80,rollx(sif.high)<sif.dhigh-30),sif.time<945)],[tp2],99999999)   #距离突破线比较近的，交给突破
    mhh = rollx(tmax(sif.high,75))
    mll = rollx(tmin(sif.low,75))

    signal = gand(#shh<90,    #不震荡
                gor(lll2 > lll,sll>0), #虽然能有效果滤，但为保持简单性，删除
                #lll2>lll,
                #sll>0,
                cross(tp,sif.high)>0,
                #tp <= rollx(tp),#不是从99999999下来的被上叉
                #rollx(tp)!=99999999,###去掉因为99999999下叉到lll-10引起的穿越. 没必要
                rollx(strend2(sif.high))>0,
                sif.time>915,   #915会有跳空
                tp - sif.dlow > 200,
                lhh>lll+80,
                sif.time > tbegin,  #避免之前信号被重复计算
                #rollx(sif.dhigh - sif.dlow) > 400,
                #rollx(mhh - mll) > 200,
            )

    msignal = msum(signal,30)
    signal2 = gand(
                gor(lll2 > lll,sll>0),
                cross(tp2,sif.high)>0,
                tp <= rollx(tp),#不是从99999999下来的被上叉                
                sif.time>915,   #915会有跳空
                tp2 - sif.dlow > 200,
                lhh>lll+80,                
            )
    signal = np.select([msignal<3,msignal>=3],[signal,signal2],0)
    ptp = np.select([msignal<3,msignal>=3],[tp,tp2],0)
    return np.select([signal],[gmax(sif.open,ptp)],0)
    #return np.select([signal],[gmax(sif.open,tp)],0)


def dxbreak1c(sif,tbegin=1030):
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

    
    tp = lll-10
    #tp = lll

    tlow = rollx(sif.dlow)  #不能计算突破当分钟的
    #tp = np.select([gor(tp>tlow+60,sif.time<=1031,sif.time>=1430)],[tp],0) #接近低点的给突破
    tp = np.select([gor(tp>tlow+120)],[tp],0) #接近低点的给突破
    #tp = np.select([gand(tp>tlow+60,rollx(sif.low)>tlow+30)],[tp],0) #接近低点的给突破


    #ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    #ldmid = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)    
    ldmid = dnext(sif.highd/2+rollx(sif.highd)/2,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)        


    signal = gand(#sll<0,    #不震荡
                #rollx(sif.sdma)>0,
                #gor(lhh2 < lhh,shh<0),
                cross(tp,sif.low)<0,
                #sif.low < tp,
                sif.time>915,   #915会有跳空
                #tp >= rollx(tp),    #不是从0起来的被交叉
                #rollx(tp)!=0,  #去掉因为0上叉到lll-10引起的穿越. 没必要
                #sif.xatr>sif.mxatr,
                #sif.xatr<2500,
                #sif.xatr30x < 10000,
                #sif.xatr5x < 4000,
                #sif.dhigh - sif.low>60,
                gor(tp < ldmid,tp<opend),#-sif.xatr*2/XBASE,  #比前2天高点中点低才允许做空                
                lll < lhh - 60,
                #rollx(sif.dhigh - sif.dlow) > 100, 
                #rollx(sif.dhigh - sif.dlow) > 100, 
                #rollx(sif.dhigh)- tp >100,
            )
    
    return np.select([signal],[gmin(sif.open,tp)],0)

def uxbreak1v(sif,tbegin=1030):
    '''
        向上突破, 接近高点的不作
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


    tp = lhh 

    #tp = np.select([tp<rollx(sif.dhigh-30)],[tp],99999999)   #距离突破线比较近的，交给突破    

    tp2 = lhh + 30  #假动作之后抬升
    #tp2 = np.select([tp2<rollx(sif.dhigh-30)],[tp2],99999999)   #距离突破线比较近的，交给突破
    #tp2 = np.select([gor(gand(tp2<sif.dhigh-80,rollx(sif.high)<sif.dhigh-30),sif.time<945)],[tp2],99999999)   #距离突破线比较近的，交给突破
    mhh = rollx(tmax(sif.high,75))
    mll = rollx(tmin(sif.low,75))
    ldmid = dnext(sif.highd/2+rollx(sif.highd)/2,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)        

    signal = gand(#shh<90,    #不震荡
                gor(lll2 > lll,sll>0), #虽然能有效果滤，但为保持简单性，删除
                #lll2>lll,
                #sll>0,
                cross(tp,sif.high)>0,
                #tp <= rollx(tp),#不是从99999999下来的被上叉
                #rollx(tp)!=99999999,###去掉因为99999999下叉到lll-10引起的穿越. 没必要
                rollx(strend2(sif.high))>0,
                sif.time>915,   #915会有跳空
                tp >= rollx(sif.dlow) + 200,
                tp <= rollx(sif.dhigh) - 200,
                lhh>lll+120,
                sif.time > tbegin,  #避免之前信号被重复计算
                #rollx(sif.dhigh - sif.dlow) > 400,
                #rollx(mhh - mll) > 200,
                #tp > sif.dmid,
                #gor(tp > opend,tp>ldmid),
                #tp>opend,
            )

    msignal = msum(signal,30)
    signal2 = gand(
                gor(lll2 > lll,sll>0),
                cross(tp2,sif.high)>0,
                #tp2 <= rollx(tp2),#不是从99999999下来的被上叉                
                rollx(strend2(sif.high))>0,
                sif.time>915,   #915会有跳空
                tp2 >= rollx(sif.dlow) + 200,
                tp2 <= rollx(sif.dhigh) - 200,
                lhh>lll+120,
                sif.time > tbegin,  #避免之前信号被重复计算
            )
    signal = np.select([msignal<3,msignal>=3],[signal,signal2],0)
    ptp = np.select([msignal<3,msignal>=3],[tp,tp2],0)
    return np.select([signal],[gmax(sif.open,ptp)],0)
    #return np.select([signal],[gmax(sif.open,tp)],0)

def dxbreak1v(sif,tbegin=1030):
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

    
    tp = lll-10
    #tp = lll

    tlow = rollx(sif.dlow)  #不能计算突破当分钟的
    #tp = np.select([gor(tp>tlow+60,sif.time<=1031,sif.time>=1430)],[tp],0) #接近低点的给突破
    #tp = np.select([gor(tp>tlow+120)],[tp],0) #接近低点的给突破
    #tp = np.select([gand(tp>tlow+60,rollx(sif.low)>tlow+30)],[tp],0) #接近低点的给突破


    #ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    #ldmid = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)    
    ldmid = dnext(sif.highd/2+rollx(sif.highd)/2,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)        


    signal = gand(#sll<0,    #不震荡
                #rollx(sif.sdma)>0,
                #gor(lhh2 < lhh,shh<0),
                cross(tp,sif.low)<0,
                #sif.low < tp,
                sif.time>915,   #915会有跳空
                #tp >= rollx(tp),    #不是从0起来的被交叉
                #rollx(tp)!=0,  #去掉因为0上叉到lll-10引起的穿越. 没必要
                #sif.xatr>sif.mxatr,
                #sif.xatr<2500,
                #sif.xatr30x < 10000,
                #sif.xatr5x < 4000,
                #sif.dhigh - sif.low>60,
                gor(tp < ldmid,tp<opend),#-sif.xatr*2/XBASE,  #比前2天高点中点低才允许做空
                #lll < lhh - 60,
                tp > rollx(sif.dmid) - 6,
                #rollx(sif.dhigh-sif.dlow)>200,
                #tp - rollx(sif.dlow) > 200,
                #tp >= rollx(sif.dlow) + 200,
                #rollx(sif.dhigh - sif.dlow) > 100, 
                #rollx(sif.dhigh)- tp >200,
            )
    
    return np.select([signal],[gmin(sif.open,tp)],0)

def dxbreak1d(sif,tbegin=1030):
    '''
        冲高失败后向下突破
    '''

    tp = rollx(sif.dhigh)-120

    ldmid = dnext(sif.highd/2+rollx(sif.highd)/2,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)        

    signal = gand(
                #gor(lhh2 < lhh,shh<0),
                cross(tp,sif.low)<0,
                #sif.low < tp,
                sif.time>915,   #915会有跳空
                rollx(tmax(sif.high,3)) == rollx(sif.dhigh),
            )
    
    return np.select([signal],[gmin(sif.open,tp)],0)

bxbreak = BXFunc(fstate=gofilter,fsignal=uxbreak,fwave=gofilter,ffilter=mfilter3)##e1430filter2)
bxbreak.name = u'向上突破'
bxbreak.lastupdate = 20101231
bxbreak.stop_closer = utrade.atr5_ustop_V1

bxbreak1 = BXFunc(fstate=gofilter,fsignal=uxbreak1,fwave=gofilter,ffilter=mfilter)##e1430filter2)
bxbreak1.name = u'向上突破'
bxbreak1.lastupdate = 20101231
bxbreak1.stop_closer = utrade.atr5_ustop_V1

bxbreak1b = BXFunc(fstate=gofilter,fsignal=uxbreak1b,fwave=gofilter,ffilter=mfilter3)##e1430filter2)
bxbreak1b.name = u'向上突破'
bxbreak1b.lastupdate = 20101231
bxbreak1b.stop_closer = utrade.atr5_ustop_V1

bxbreak1c = BXFunc(fstate=gofilter,fsignal=uxbreak1c,fwave=gofilter,ffilter=mfilter)##e1430filter2)
bxbreak1c.name = u'向上突破c'
bxbreak1c.lastupdate = 20101231
bxbreak1c.stop_closer = utrade.atr5_ustop_V1

bxbreak1v = BXFunc(fstate=gofilter,fsignal=uxbreak1v,fwave=gofilter,ffilter=mfilter)##e1430filter2)
bxbreak1v.name = u'向上突破v'
bxbreak1v.lastupdate = 20101231
bxbreak1v.stop_closer = utrade.atr5_ustop_V1


sxbreak1d = SXFunc(fstate=gofilter,fsignal=dxbreak1d,fwave=gofilter,ffilter=mfilter)##e1430filter2)
sxbreak1d.name = u'向下突破d'
sxbreak1d.lastupdate = 20101231
sxbreak1d.stop_closer = utrade.atr5_ustop_V1


bxbreak1x = BXFunc(fstate=gofilter,fsignal=uxbreak1,fwave=gofilter,ffilter=mfilter3)
bxbreak1x.name = u'向上突破'
bxbreak1x.lastupdate = 20101231
bxbreak1x.stop_closer = utrade.atr5_ustop_V1

bxbreak0 = BXFunc(fstate=gofilter,fsignal=fcustom(uxbreak1,tbegin=0),fwave=gofilter,ffilter=efilter2)##e1430filter2)
bxbreak0.name = u'向上突破0'
bxbreak0.lastupdate = 20101231
bxbreak0.stop_closer = utrade.atr5_ustop_V1


bxbreak2 = BXFunc(fstate=gofilter,fsignal=uxbreak2,fwave=gofilter,ffilter=mfilter3)##e1430filter2)
bxbreak2.name = u'向上突破2'
bxbreak2.lastupdate = 20101231
bxbreak2.stop_closer = utrade.atr5_ustop_X2

bxbreakd = BXFuncF1(fstate=gofilter,fsignal=uxbreak1,fwave=gofilter,ffilter=mfilter3)##e1430filter2)
bxbreakd.name = u'向上突破'
bxbreakd.lastupdate = 20101231
bxbreakd.stop_closer = utrade.atr5_ustop_X2

bxbreak1vd = BXFuncF1(fstate=gofilter,fsignal=uxbreak1v,fwave=gofilter,ffilter=mfilter3)##e1430filter2)
bxbreak1vd.name = u'向上突破'
bxbreak1vd.lastupdate = 20101231
bxbreak1vd.stop_closer = utrade.atr5_ustop_X2

sxbreak = SXFunc(fstate=gofilter,fsignal=dxbreak,fwave=nx2500X,ffilter=mfilter3)##e1430filter2)
sxbreak.name = u'向下突破'
sxbreak.lastupdate = 20101231
sxbreak.stop_closer = utrade.atr5_ustop_V1

sxbreak1 = SXFunc(fstate=gofilter,fsignal=dxbreak1,fwave=nx2500X,ffilter=mfilter)##e1430filter2)
sxbreak1.name = u'向下突破1'
sxbreak1.lastupdate = 20101231
sxbreak1.stop_closer = utrade.atr5_ustop_V1

sxbreak1b = SXFunc(fstate=gofilter,fsignal=dxbreak1b,fwave=nx2500X,ffilter=mfilter3)##e1430filter2)
sxbreak1b.name = u'向下突破1'
sxbreak1b.lastupdate = 20101231
sxbreak1b.stop_closer = utrade.atr5_ustop_V1

sxbreak1c = SXFunc(fstate=gofilter,fsignal=dxbreak1c,fwave=nx2500X,ffilter=mfilter)##e1430filter2)
sxbreak1c.name = u'向下突破1c'
sxbreak1c.lastupdate = 20101231
sxbreak1c.stop_closer = utrade.atr5_ustop_V1

sxbreak1v = SXFunc(fstate=gofilter,fsignal=dxbreak1v,fwave=nx2500X,ffilter=mfilter)
sxbreak1v.name = u'向下突破v'
sxbreak1v.lastupdate = 20101231
sxbreak1v.stop_closer = utrade.atr5_ustop_V1


sxbreak1x = SXFunc(fstate=gofilter,fsignal=dxbreak1,fwave=nx2500X,ffilter=efilter)
sxbreak1x.name = u'向下突破1'
sxbreak1x.lastupdate = 20101231
sxbreak1x.stop_closer = utrade.atr5_ustop_V1

sxbreak2 = SXFunc(fstate=gofilter,fsignal=dxbreak2,fwave=nx2500X,ffilter=mfilter2)##e1430filter2)
sxbreak2.name = u'向下突破'
sxbreak2.lastupdate = 20101231
sxbreak2.stop_closer = utrade.atr5_ustop_X2

sxbreakd = SXFuncF1(fstate=gofilter,fsignal=dxbreak1,fwave=nx2500X,ffilter=mfilter2)##e1430filter2)
sxbreakd.name = u'向下突破'
sxbreakd.lastupdate = 20101231
sxbreakd.stop_closer = utrade.atr5_ustop_V

sxbreak1vd = SXFuncF1(fstate=gofilter,fsignal=dxbreak1v,fwave=nx2500X,ffilter=mfilter2)##e1430filter2)
sxbreak1vd.name = u'向下突破'
sxbreak1vd.lastupdate = 20101231
sxbreak1vd.stop_closer = utrade.atr5_ustop_V

ebxbreak = BXFunc(fstate=gofilter,fsignal=fcustom(uxbreak,tbegin=0),fwave=gofilter,ffilter=emfilter)
ebxbreak.name = u'早盘向上突破'
ebxbreak.lastupdate = 20101231
ebxbreak.stop_closer = utrade.atr5_ustop_X4

esxbreak = SXFunc(fstate=gofilter,fsignal=fcustom(dxbreak1,tbegin=0),fwave=nx2500X,ffilter=emfilter)##e1430filter2)
esxbreak.name = u'早盘向下突破'
esxbreak.lastupdate = 20101231
esxbreak.stop_closer = utrade.atr5_ustop_X4

ebxbreak2 = BXFunc(fstate=gofilter,fsignal=euxbreak,fwave=gofilter,ffilter=emfilter)
ebxbreak2.name = u'早盘向上突破2'
ebxbreak2.lastupdate = 20101231
ebxbreak2.stop_closer = utrade.atr5_ustop_X4

esxbreak2 = SXFunc(fstate=gofilter,fsignal=edxbreak,fwave=nx2500X,ffilter=emfilter)##e1430filter2)
esxbreak2.name = u'早盘向下突破2'
esxbreak2.lastupdate = 20101231
esxbreak2.stop_closer = utrade.atr5_ustop_X4

xbreak = [bxbreak,sxbreak] #sxbreak1取代sxbreak
xbreak1 = [bxbreak1,sxbreak1] #sxbreak1取代sxbreak
xbreak1b = [bxbreak1b,sxbreak1b] #突破回调系统

xbreak1c = [bxbreak1c,sxbreak1c] #结合起来的系统，好好研究下, 体会下回调开仓
xbreak1v = [bxbreak1v,sxbreak1v] #


xbreakx = xbreak1 + xbreak1b    #一个不错的独立方法

xbreak2 = [bxbreak2,sxbreak2]
d1_xbreak = [bxbreakd,sxbreakd]
d1_xbreak1v = [bxbreak1vd,sxbreak1vd]
exbreak = [ebxbreak,esxbreak]

exbreak2 = [ebxbreak2]

#####阻力反向
def dxpeak(sif,tbegin=1030):
    '''
        向上到前顶后放空
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


    tp = lhh + 10
    tp2 = tp + 60

    ldmid = dnext(sif.highd/2+rollx(sif.highd)/2,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)        
    ldlow = dnext(sif.lowd,sif.close,sif.i_cofd)        

    signal = gand(
                #cross(tp,sif.high)>0,
                sif.high > tp,
                sif.high < tp2,
                sif.time>915,   #915会有跳空
                tp < opend,
                tp < ldlow,
                tp < sif.dhigh - 200,
                rollx(sif.dhigh-sif.dlow)>250,
            )

    return signal#np.select([signal],[tp],0)

sxpeak = SXFunc(fstate=gofilter,fsignal=dxpeak,fwave=nx2500X,ffilter=mfilter)
sxpeak.name = u'阻力放空'
sxpeak.lastupdate = 20110114
sxpeak.stop_closer = utrade.atr5_ustop_V1


##幅度突破rbreak
def rbreakb(sif,distance=250):
    '''
        幅度从最低跨越distance点时开仓
    '''
    bline = sif.dlow + distance
    signal = gand(
                sif.high > bline,
                bline > sif.dmid,
                rollx(sif.high) > rollx(sif.high,11),
            )
    return np.select([signal>0],[gmax(sif.open,bline)],0)

def rbreaks(sif,distance=400):
    '''
        幅度从最高跨越distance点时开仓
    '''
    bline = sif.dhigh - distance
    signal = gand(
                sif.low < bline,
                sif.t120 < 180,
                rollx(sif.low) < rollx(sif.low,31),  
            )
    return np.select([signal>0],[gmin(sif.open,bline)],0)

def rmbreakb(sif,distance=250):
    '''
        幅度从最低跨越distance点时开仓
    '''
    bline = rollx(tmin(sif.low,75)) + distance
    signal = gand(
                sif.high > bline,
                bline > sif.dmid,
                #bline > rollx(tmin(sif.low,75) + tmax(sif.high,75))/2,
                #sif.high > rollx(tmax(sif.high,20)), 
                rollx(sif.high) > rollx(sif.high,11),                
            )
    return np.select([signal>0],[gmax(sif.open,bline)],0)

def rmbreaks(sif,distance=400):
    '''
        幅度从最高跨越distance点时开仓
    '''
    bline = rollx(tmax(sif.high,75)) - distance
    signal = gand(
                sif.low < bline,
                sif.t120 < 180,
                #sif.low < rollx(tmin(sif.low,20)),                
                rollx(sif.low) < rollx(sif.low,31),  
            )
    return np.select([signal>0],[gmin(sif.open,bline)],0)


brbreak = BXFunc(fstate=gofilter,fsignal=rbreakb,fwave=gofilter,ffilter=mfilter1400)
brbreak.name = u'幅度向上突破25'
brbreak.lastupdate = 20110106
brbreak.stop_closer = utrade.atr5_ustop_X4

srbreak = SXFunc(fstate=gofilter,fsignal=rbreaks,fwave=nx2500X,ffilter=mfilter1400)
srbreak.name = u'幅度向下突破40'
srbreak.lastupdate = 20110106
srbreak.stop_closer = utrade.atr5_ustop_X4

lbrbreak = BXFuncD1(fstate=gofilter,fsignal=rbreakb,fwave=gofilter,ffilter=lmfilter)
lbrbreak.name = u'尾盘幅度向上突破25'
lbrbreak.lastupdate = 20110106
lbrbreak.stop_closer = utrade.atr5_ustop_X4

lsrbreak = SXFuncD1(fstate=gofilter,fsignal=rbreaks,fwave=nx2500X,ffilter=lmfilter)
lsrbreak.name = u'尾盘幅度向下突破40'
lsrbreak.lastupdate = 20110106
lsrbreak.stop_closer = utrade.atr5_ustop_X4

bmrbreak = BXFunc(fstate=gofilter,fsignal=rmbreakb,fwave=gofilter,ffilter=mfilter1400)
bmrbreak.name = u'幅度向上突破25'
bmrbreak.lastupdate = 20110106
bmrbreak.stop_closer = utrade.atr5_ustop_X4

smrbreak = SXFunc(fstate=gofilter,fsignal=rmbreaks,fwave=nx2500X,ffilter=mfilter1400)
smrbreak.name = u'幅度向下突破40'
smrbreak.lastupdate = 20110106
smrbreak.stop_closer = utrade.atr5_ustop_X4

lbmrbreak = BXFunc(fstate=gofilter,fsignal=rmbreakb,fwave=gofilter,ffilter=lmfilter)
lbmrbreak.name = u'幅度向上突破25'
lbmrbreak.lastupdate = 20110106
lbmrbreak.stop_closer = utrade.atr5_ustop_X4

lsmrbreak = SXFunc(fstate=gofilter,fsignal=rmbreaks,fwave=nx2500X,ffilter=lmfilter)
lsmrbreak.name = u'幅度向下突破40'
lsmrbreak.lastupdate = 20110106
lsmrbreak.stop_closer = utrade.atr5_ustop_X4


rbreak = [brbreak,srbreak]  #这是一个很好的备选主方案, 无遗漏系统
lrbreak = [lbrbreak,lsrbreak]  #

rbreak_all = rbreak + [lsrbreak] + [shbreak_mll2_k]#时段

mrbreak = [bmrbreak,smrbreak]  #也是一个很好的备选主方案. 回撤较小. 感觉有点抓到本质了. 有遗漏
lmrbreak = [lbmrbreak,lsmrbreak]  #也是一个很好的备选主方案. 回撤较小. 感觉有点抓到本质了. 有遗漏
mrbreak_all = mrbreak + lmrbreak

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
                rollx(tmin(sif.low,4)) > lll-20,
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
                rollx(tmax(sif.high,4)) < lhh - 20,
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

###7操作系统

##做多在9/11/12/13/46/53/57, 正向运动, 11综合最好
def ux7(sif):   #
    signal = gand(
            gor(sif.time%100 == 11),#,sif.time%100 == 37,sif.time%100 == 57),
            sif.low > rollx(sif.low,1),
            sif.high > rollx(sif.high,1),         
            sif.close > rollx(sif.close,1),
          )
    
    return signal
bx7 = BXFunc(fstate=gofilter,fsignal=ux7,fwave=gofilter,ffilter=nfilter)
bx7.name = u'7系统向上'
bx7.lastupdate = 20110111
bx7.stop_closer = utrade.atr5_ustop_V1

#31肯定卡到某些周期交易者的气门了，空头占优时他们动作之后被趋势反动
#逢31就放空,1393点,439次，143点. 这个止损是8点
#无条件放空: 止损到4点，8点报本，768点, 275次, 最大回撤74点. 每天亏到3点就收工
######反向放空(止损4保本8)，即该分钟收盘/最高/最低都大于上分钟，则423点，129次，最大回撤44点. 打酱油系统
############如果设定每天最多亏6点，就是438点,126次,44点回撤
def dx7(sif):   #
    signal = gand(
            gor(sif.time%100 == 31),#,sif.time%100 == 37,sif.time%100 == 57),
            sif.low > rollx(sif.low,1),
            #sif.high > rollx(sif.high,1),#下跌判断不需要高点增高
            sif.close > rollx(sif.close,1),                        
            sif.close > sif.open,
          )
    
    return signal
sx7 = SXFunc(fstate=gofilter,fsignal=dx7,fwave=gofilter,ffilter=nfilter)
sx7.name = u'7系统向下'
sx7.lastupdate = 20110111
sx7.stop_closer = utrade.atr5_ustop_V1

x7 = [bx7,sx7]  #合成之后，879点,290次,80点回撤. 止损4保本8
                #如果改成止损6保本8,并且每天亏上12点后收工，则变成993/267,回撤68
                #去掉dx7中的高点条件后，变成1232/339, 回撤66, 不需要每天的连亏设置
                #这个系统需要观察2个月

#振幅  盈利日数 盈利累计  亏损日数   亏损累计
#0-30     4      32.4         13     -113.6
#30-50    18     152.5        21     -222.8
#50-100   34     884.1        45     -363.2
#100-150  13     586.2        10     -60.4
#>150     4      341.6        3      -4.0
##按月的盈利分布也不错

##指标系统
###macd
def muc(sif):
    signal = gand(
            cross(sif.dea1,sif.diff1)>0,
            sif.s30 < 0,
            sif.close < sif.dlow + 150,
          )
    return signal
smuc = SXFuncD1(fstate=sdown,fsignal=muc,fwave=nx2500X,ffilter=mfilter)
smuc.name = u'macd上叉放空'
smuc.lastupdate = 20110116
smuc.stop_closer = utrade.atr5_ustop_V1

def mdc(sif):
    signal = gand(
            cross(sif.dea1,sif.diff1)<0,
            sif.s30 > 0,
            sif.close >sif.dlow + 200,
            sif.high < sif.dhigh,
          )
    return signal
bmdc = BXFuncD1(fstate=sdown,fsignal=mdc,fwave=nx2500X,ffilter=mfilter)
bmdc.name = u'macd下叉做多'
bmdc.lastupdate = 20110116
bmdc.stop_closer = utrade.atr5_ustop_V1

def muc0(sif):
    signal = gand(
            cross(cached_zeros(len(sif.close)),sif.diff1)>0,
            sif.s30 < 0,
            sif.close < sif.dlow + 150,
          )
    return signal
smuc0 = SXFuncD1(fstate=sdown,fsignal=muc0,fwave=nx2500X,ffilter=mfilter)
smuc0.name = u'macd上叉0放空'
smuc0.lastupdate = 20110116
smuc0.stop_closer = utrade.atr5_ustop_V1

def mdc0(sif):
    signal = gand(
            cross(cached_zeros(len(sif.close)),sif.diff1)>0,
            sif.s30 > 0,
            sif.close >sif.dlow + 200,
            sif.high < sif.dhigh,
          )
    return signal
bmdc0 = BXFuncD1(fstate=sdown,fsignal=mdc0,fwave=nx2500X,ffilter=mfilter)
bmdc0.name = u'macd上叉做多'
bmdc0.lastupdate = 20110116
bmdc0.stop_closer = utrade.atr5_ustop_V1

mc = [bmdc,smuc,smuc0,bmdc0]    #一种简单的基于macd的系统

###rsi
def ruc(sif):
    signal = gand(
            cross(sif.rsi19,sif.rsi7)<0,
            sif.s30 < 0,
            sif.close < sif.dlow + 150,
          )
    return signal
sruc = SXFuncD1(fstate=sdown,fsignal=ruc,fwave=nx2500X,ffilter=mfilter)
sruc.name = u'rsi上叉放空'
sruc.lastupdate = 20110116
sruc.stop_closer = utrade.atr5_ustop_V1

def rdc(sif):
    signal = gand(
            cross(sif.rsi19,sif.rsi7)<0,
            sif.s30 > 0,
            sif.close >sif.dlow + 200,
            sif.high < sif.dhigh,
          )
    return signal
brdc = BXFuncD1(fstate=sdown,fsignal=rdc,fwave=nx2500X,ffilter=mfilter)
brdc.name = u'rsi下叉做多'
brdc.lastupdate = 20110116
brdc.stop_closer = utrade.atr5_ustop_V1

rc = [sruc,brdc]    #不如macd系统

###xud
def xudd(sif):
    mxc = xc0c(sif.open10,sif.close10,sif.high10,sif.low10,13) < 0
    signal = np.zeros_like(sif.close)
    signal[sif.i_cof10] = mxc
    
    signal = gand(signal,
            sif.s30 > 0,
            sif.close < sif.dhigh - 150,
           )
    return signal
sxudd = SXFunc(fstate=sdown,fsignal=xudd,fwave=nx2500X,ffilter=mfilter)
sxudd.name = u'xud放空'
sxudd.lastupdate = 20110116
sxudd.stop_closer = utrade.atr5_ustop_V1
 
###ma
def uma(sif):
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd)
    signal = gand(cross(sif.ma5,sif.low)>0,
            strend2(sif.low)>0,
            strend2(sif.ma5)>0,
            sif.s30 > 0,
            sif.close > sif.dlow + 500,
            #sif.dhigh-sif.dlow > 500,
            sif.ma5 > sif.ma13,
            sif.ma30 > sif.ma270,
           )
    return signal
buma = BXFunc(fstate=sdown,fsignal=uma,fwave=nx2500X,ffilter=mfilter)
buma.name = u'最低价穿越ma5'
buma.lastupdate = 20110116
buma.stop_closer = utrade.atr5_ustop_V1

def dma(sif):
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd)
    signal = gand(cross(sif.ma5,sif.high)<0,
            strend2(sif.ma5)<0,
            #sif.s30 < 0,
            sif.close < gmax(sif.dhigh,ldclose) - 400,
            #sif.dhigh-sif.dlow > 300,
            #sif.close < sif.dhigh - 400,
            sif.ma5 < sif.ma13,
            sif.ma13 < sif.ma30,
           )
    return signal
sdma = SXFunc(fstate=sdown,fsignal=dma,fwave=nx2500X,ffilter=mfilter)
sdma.name = u'最高价穿越ma5'
sdma.lastupdate = 20110116
sdma.stop_closer = utrade.atr5_ustop_V1

tma = [buma,sdma]   #这个系统更加强,是个不错的主策略, 简单

####添加老系统
wxxx = [xds,xdds3,k5_d3b,xuub,K1_DDD1,K1_UUX,K1_RU,Z5_P2,xmacd3s,xup01,ua_fa,FA_15_120,K1_DVB,K1_DDUU,K1_DVBR]

#wxxx_s = [xds,xdds3,k5_d3b,K1_DDD1,Z5_P2,xmacd3s,FA_15_120]
#wxxx_b = [xuub,K1_UUX,K1_RU,xup01,ua_fa,K1_DDUU]
#wxxx_b2 = [K1_DVB,K1_DVBR]

wxxx_s = [xds,k5_d3b,Z5_P2,xmacd3s]#,FA_15_120] #xdds4很有意思
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

#xxx1 = xbreak1c + hbreak2 + dbreak + exbreak2 + rebound2#+ d1_rebound #+ amm #+ break123c  #此方法每日亏损20点之后趴下装死比较妥当
#xxx1 = xbreak1c + hbreak2 + dbreak + exbreak2 + rebound2#此方法每日亏损20点之后趴下装死比较妥当
xxx1 = hbreak2 + xbreak1v + rebound3 +dbreak + exbreak2 + rebound2    #此方法每日亏损18点(775)或12点(75)之后趴下装死比较妥当. 关键是保持一致性

xxx1a = hbreak2 + xbreak1v + dbreak #一个独立的策略
xxx1b = tma + rebound3 + rebound2 + exbreak2#一个不错的候补策略. 和hbreak2+xbreak1v不协调


dxxx = d1_xbreak1v + d1_hbreak + dbreak #+ d1_rebound#+break123c# #+ rebound  #此方法每日亏损12点之后趴下装死比较妥当

#xxx2 = xxx +wxfs #+ wxxx
xxx2 = xxx1 + tma

xamm = amm + hbreak2 + rebound    #这是一个非常好的独立策略, 作为候选, 每日亏损9(7+1+1)点之后趴下装死.

rxxx = rbreak_all + edbreak + exbreak #+ rebound #一个很牛的独立策略, 亏损12点后趴下
mrxxx = mrbreak + edbreak +exbreak #+ rebound #一个很牛的独立策略，类似于上

rxxx2 = rbreak + break_xr + xbreak1b #xbreak1b:突破回调系统

xxx3 = dbreak+ xbreak1c + exbreak2 + xbreak1 + rebound2 #也还可以

#xxx2 = rxxx

#####
# 主策略采用xxx1, 被选策略为dxxx和xamm
#####

'''
计算每日亏损以及截断的统计办法
>>> tradesy =  utrade.utrade_n(i00,ufuncs.dxxx)
>>> sum([trade.profit for trade in tradesy])
35655
>>> len(tradesy)
481
>>> 35655/481.
74.126819126819129
>>> iftrade.max_drawdown(tradesy)    #最大连续回撤和单笔回撤
(-612, -70, 20100604)
>>> pdays =utrade.day_trades(tradesy,-200)  #每日最大亏损20点,之后不再开仓
>>> sum([p.ntrade for p in pdays])
475
>>> sum([p.sprofit for p in pdays])
34766
>>> 34766/475.
73.191578947368427
>>> utrade.dmax_drawdown(pdays)
(-518, -220, 20100813)
>>> pdays =utrade.day_trades(tradesy,-150)  #每日最大亏损15点,之后不再开仓
.....
>>> mds = utrade.day_trades(tradesy,-1000)    #日交易汇总
>>> for md in mds: print md.day,md.sprofit,i00.day2range[md.day]
20100416 176 748
20100419 1982 2296
......
>>> xmds = [md for md in mds if md.profit<0 and i00.day2range[md.day]>600]  #振幅大于60点但未盈利日
>>> for md in xmds: print md.day,md.sprofit,i00.day2range[md.day]
...
20100420 -70 688
20100510 -70 606
......
>>> pds = utrade.pd(i00,mds)    #求利润分布
>>> for pd in pds:print pd.end,pd.wins,pd.pwins,pd.losts,pd.plosts
...
300 0 0 6 -320
500 10 856 28 -1987
1000 48 12483 32 -3223
1500 21 12626 2 -220
10000 8 9583 0 0
>>> pds = utrade.pd(i00,mds,[300,500,800,1000,1500,5000])    #求利润分布
>>> for pd in pds:print pd.end,pd.wins,pd.pwins,pd.losts,pd.plosts
...
300 0 0 6 -320
500 10 856 28 -1987
800 27 4897 23 -2445
1000 21 7586 9 -778
1500 21 12626 2 -220
5000 8 9583 0 0

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

for x in rxxx:
    x.stop_closer = utrade.atr5_ustop_X4


###第一序列
bxbreak.stop_closer = utrade.atr5_ustop_V1
sxbreak.stop_closer = utrade.atr5_ustop_V1
bxbreak1.stop_closer = utrade.atr5_ustop_V1
sxbreak1.stop_closer = utrade.atr5_ustop_V1
bxbreak1c.stop_closer = utrade.atr5_ustop_V1
sxbreak1c.stop_closer = utrade.atr5_ustop_V1

bxbreak1v.stop_closer = utrade.atr5_ustop_V1
sxbreak1v.stop_closer = utrade.atr5_ustop_V1

ebxbreak2.stop_closer = utrade.atr5_ustop_V1

shbreak_mll2.stop_closer = utrade.atr5_ustop_T
hbreak_nhh.stop_closer = utrade.atr5_ustop_T

dbreakb.stop_closer = utrade.atr5_ustop_T
dbreaks.stop_closer = utrade.atr5_ustop_T

brebound3.stop_closer = utrade.atr5_ustop_TV1
srebound3.stop_closer = utrade.atr5_ustop_TV1


#########候补序列
bxbreakd.stop_closer = utrade.atr5_ustop_V
sxbreakd.stop_closer = utrade.atr5_ustop_V

dhbreak_nhh.stop_closer = utrade.atr5_ustop_V
dshbreak_mll2.stop_closer = utrade.atr5_ustop_V

brebound2.stop_closer = utrade.atr5_ustop_T1
srebound2.stop_closer = utrade.atr5_ustop_T1

####AMM系列
bamm.stop_closer = utrade.atr5_ustop_V1
samm.stop_closer = utrade.atr5_ustop_V1

####ma系列
sdma.stop_closer = utrade.atr5_ustop_V1
buma.stop_closer = utrade.atr5_ustop_V1



#b123b.stop_closer = utrade.atr5_ustop_X2

#for x in dxxx:#
#    x.stop_closer = utrade.atr5_ustop_V

