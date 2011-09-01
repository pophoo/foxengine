# -*- coding: utf-8 -*-


'''
2011-01操作指南
#################################
两张合约指南:
简单方式：
    以hbreak2,rebound3分别操作两张,即不能互相平仓
    20点(含20点)损失后不再操作

###############
简化操作(此段已经废弃)
        所有操作都是2张一起开仓，一起平仓
        按照xxx1操作
        每日最大回撤>18点后不再开仓. 如果不到18点，则必然开两张 
        周四建议开一张, 周三随机
##################


#######必须检查
1. 下止损条件单时必须确认成交了几张，止损张数不能大于成交张数，否则条件单无效!!!
2. 下开仓条件单时必须确认开仓张数!!!

操作注意事项:
1. 如果条件开仓单未就绪时发生突破，并且突破后价格回调。此时，不要追求优于系统的开仓价，而应该在原突破处下
   条件开仓单。
    有两个好处，一个是不会出现行情剧烈变化，来不及下止损单的情况
    另一个是突破的成功率其实比较低，出现这种突破后回调情况的，就更低了，值得观望
   但是，有一点必须注意，不要故意不去下条件开仓单!!!
2. 不允许手工平仓单。如果因为特别原因需要先行平仓，则必须以修改条件平仓单触发条件的办法来做,以确保成交
3. 开仓前密切关注XATR是否大于2500
4. 如果大智慧的实时跟踪出信号，但与规则不符，则需要查看文华数据以确认，之前不能下单.
#################################
信号切换规则:
    持仓时出现反向信号，当浮动收益大于25或小于3时或持仓时间大于20分钟时，平仓并开新仓，否则不变
    每日止损大于等于18点不再开仓

开仓和平仓价格的设置:
    1. 如开多目标突破价是3000，则开仓条件单应该是>=3000.2才可以，否则是不对的. 系统中都是叉或超越
    2. 平仓也如是，如果卖出平仓的目标平仓价是3000，则必须是<=2999.8才行
    3. 保本平仓的基准价格是开仓目标价,而不是执行价格.
    4. 这样才能和系统一致

################################
理论依据:
    T1: 日的平均1分钟ATR
    T2: 日波动幅度
    T3: 稳定盈利周期

    T2/T1 > 20 才能挣钱
    T3/T2 > 5. 最小稳定盈利周期定理
    对股指期货来说, 平均下来T2/T1>20是成立的, 最小稳定盈利周期是周. 商品中Cu,Ru可能也适合日内
    对日间交易来说，有些品种T2为年，则稳定盈利周期在5-10年.

筛选品种/状态的方法:
    1. 筛选方法必须与开仓/平仓策略一致
    2. 目前的主策略，筛选方法必然是以开盘价-->最高价/最低价中的大者为波动衡量(可兼顾收盘与开盘的距离)，并以日ATR衡量
       或者 结合最高-最低的幅度 以及 实体占幅度中的比例? 这个可能没啥用
    3. 这个只能用于筛选品种，但不建议作为可行品种过滤交易日的方法

##################################
商品思考:
    多最强，空最弱
    止损，以组合对为单位，设定止损
              

hbreak2系列
    开仓:
        做多: 1. 高点在一分钟内拉高到3分钟前日内高点+3(基准)处. 即如果上一分钟新高了，则该新高不计入内
              2. xatr<2500,xatr30x<10000
              3. 突破点取最高点+3,最低点+28和开盘价+9三个值的最大值
        做空: 1. 低点小于75分钟低点+2处
              2. xatr<2000,xatr30x<10000
              3. 1330前开仓，突破点取基准点和日内高点-35的低者，1330后直接取基准点
              4. 突破点小于开盘-6,或者为日内最低+2
              5. t120<180
    平仓:
        止损为7，保本为8. 30分钟后如果盈利大于10点，则把止损拉到盈利8点或更多处
    工作时段: 
        做多:[1036,1435]
        做空:[945,1459]

    早盘做多:[930,959]
              1. 高点在一分钟内拉高到3分钟前日内高点+3(基准)处. 即如果上一分钟新高了，则该新高不计入内
              2. 3分钟前日内振幅>35, 即如果振幅小于35,则将突破点移动到35+3处

rebound3:
    每天只做第一次
    顶/底均以6分钟计，即13分钟高/低点
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
                5. xatr<2500,xatr30x<10000
    平仓:
        止损为4, 保本为8. 30分钟后如果盈利大于10点，则把止损拉到盈利8点或更多处
    工作时段:
        [1036,1435]

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

##有史以来波幅分布(截止20110310)
>>> [s300,s500,s800,s1000,s1500,s2000]
[19, 57, 68, 33, 30, 8]
<300,300-500,500-800,800-1000,1000-1500,>1500

'''

from wolfox.fengine.ifuture.ibase import *
import wolfox.fengine.ifuture.iftrade as iftrade
import wolfox.fengine.ifuture.utrade as utrade
import wolfox.fengine.ifuture.fcontrol as control
from wolfox.fengine.ifuture.xfuncs import *

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


#主要时间过滤
def nfilter0(sif):
    return gand(
            sif.time > 929,
            sif.time < 1505,
        )

def nfilter2(sif):
    return gand(
            sif.time > 1000,
            sif.time < 1445,
        )

def nfilter3(sif):
    return gand(
            sif.time > 944,
            sif.time < 1445,
        )
    
def mfilter0(sif):
    return gand(
            sif.time > 1031,
            sif.time < 1436,
        )

def mfilter(sif):   
    return gand(
            sif.time > 1035,
            sif.time < 1436,
        )

def mfilter_m(sif):   
    return gand(
            sif.time > 1035,
            sif.time < 1331,
        )

def mfilter_a(sif):   
    return gand(
            sif.time > 1200,
            sif.time < 1436,
        )

def mfilter00(sif):   
    return gand(
            sif.time > 1000,
            sif.time < 1436,
        )

def mfilter01(sif):   
    return gand(
            sif.time > 1014,
            sif.time < 1416,
        )


def mfilter1400(sif):   
    return gand(
            sif.time > 1030,
            sif.time < 1400,
        )

def mfilter1430(sif):   
    return gand(
            sif.time > 1030,
            sif.time < 1430,
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
            gand(sif.time < 935,sif.time>919)
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

def emfilter3(sif):
    return gand(
            sif.time > 929,
            sif.time < 1000,
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

def nx2000X(sif):
    xx = gand(
                sif.xatr < 2000,
                sif.xatr30x < 10000,
                #sif.xatr5x< 4000,
           )
    return rollx(xx)

def nx2500X(sif):
    xx = gand(
                sif.xatr < 2500,
                sif.xatr30x < 10000,
                #sif.xatr5x< 4000,
           )
    return rollx(xx)



def nhhx(sif,vbreak=0):
    thigh = rollx(sif.dhigh+vbreak,1)
    
    ldatr = dnext(sif.atrd,sif.close,sif.i_cofd)
    ldclose = dnext(sif.highd,sif.close,sif.i_cofd)
    vrange = ldatr * 3/5 /XBASE
    #blow = gmin(sif.dlow,ldclose)
    thigh = gmax(thigh,sif.dlow+vrange)
    #thigh = gmax(thigh,blow+vrange)

    signal = gand(
            #cross(rollx(sif.dhigh+30),sif.high)>0
            #sif.high > thigh,
            cross(thigh,sif.high)>0,
            #rollx(sif.dhigh-sif.dlow) > 250,   #150可
            #rollx(sif.dhigh-blow)>200,
            rollx(sif.ma13)  > rollx(sif.ma30),
        )
    return np.select([signal],[gmax(sif.open,thigh)],0)    #避免跳空情况，如果跳空且大于突破点，就以开盘价进入

def nhhy(sif,vbreak=0):
    
    pivot = dnext((sif.highd+sif.lowd+sif.closed)/3,sif.close,sif.i_cofd)
    phigh = dnext(sif.highd,sif.close,sif.i_cofd)
    plow = dnext(sif.lowd,sif.close,sif.i_cofd)
    
    r1 = pivot * 2 - plow
    s1 = pivot * 2 - phigh

    thigh = r1

    signal = gand(
            #cross(rollx(sif.dhigh+30),sif.high)>0
            #sif.high > thigh,
            cross(thigh,sif.high)>0,
            #rollx(sif.dhigh-sif.dlow) > 250,   #150可
            #rollx(sif.dhigh-blow)>200,
            rollx(sif.ma3)  > rollx(sif.ma13),
        )
    return np.select([signal],[gmax(sif.open,thigh)],0)    #避免跳空情况，如果跳空且大于突破点，就以开盘价进入

def nhhk(sif,vbreak=0):
    thigh = rollx(sif.dlow + (sif.dhigh-sif.dlow)*15/30,1)
    
    ldatr = dnext(sif.atrd,sif.close,sif.i_cofd)
    ldclose = dnext(sif.highd,sif.close,sif.i_cofd)
    ldsignal = dnext(sif.closed > sif.opend,sif.close,sif.i_cofd)#,rollx(sif.closed)>rollx(sif.opend)),sif.close,sif.i_cofd)
    #vrange = ldatr * 3/5 /XBASE
    #blow = gmin(sif.dlow,ldclose)
    #thigh = gmax(thigh,sif.dlow+vrange)
    #thigh = gmax(thigh,blow+vrange)

    signal = gand(
            #cross(rollx(sif.dhigh+30),sif.high)>0
            #sif.high > thigh,
            cross(thigh,sif.high)>0,
            #rollx(sif.dhigh-sif.dlow) > 250,   #150可
            #rollx(sif.dhigh-blow)>200,
            #rollx(sif.ma13)  > rollx(sif.ma30),
            ldsignal,
        )
    return np.select([signal],[gmax(sif.open,thigh)],0)    #避免跳空情况，如果跳空且大于突破点，就以开盘价进入

def nhht(sif):
 
    sr = srover2(sif.high,sif.low,sif.time==1514,50,40)
    #sr = srover(sif.high,sif.low,sif.time==1514,150,120)
    isr = np.nonzero(sr>0)
    msr = np.zeros_like(sif.close)
    msr[isr] = rollx(ma(sr[isr],7))
    msr = extend2next(msr)

    thigh = rollx(sif.dhigh+30,1)

    blow = rollx(sif.dlow,1)

    #slimit = gmax(blow + msr)

    #slow = tmin(sif.low,60)
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)

    #thigh = rollx(slow + msr *12/10,3)
    thigh = gmax(thigh,blow+msr*105/100,ldopen+90)

    signal = gand(
            #cross(thigh,sif.high)>0,
            sif.high > thigh,
        )
    return np.select([signal],[gmax(sif.open,thigh)],0)    #避免跳空情况，如果跳空且大于突破点，就以开盘价进入

def mll2t(sif):
 
    sr = srover2(sif.high,sif.low,sif.time==1514,50,40)
    #sr = srover(sif.high,sif.low,sif.time==1514,150,120)
    isr = np.nonzero(sr<0)
    msr = np.zeros_like(sif.close)
    msr[isr] = -rollx(ma(sr[isr],7))
    msr = extend2next(msr)

    slow = tmin(sif.low,80)
    tlow = rollx(slow+10,1)

    bhigh = rollx(sif.dhigh,1)

    tlow = gmin(tlow,bhigh - msr*120/100)

    signal = gand(
            cross(tlow,sif.low)<0,
            #sif.low < tlow,
        )
    return np.select([signal],[gmin(sif.open,tlow)],0)    #避免跳空情况，如果跳空且小于突破点，就以跳空价进入


def nllx(sif,vbreak=-10):
    tlow = rollx(sif.dlow - vbreak,1)
    ldatr = dnext(sif.atrd,sif.close,sif.i_cofd)
    #ldclose = dnext(sif.closed,sif.close,sif.i_cofd)
    
    vrange = ldatr * 2/3 /XBASE

    #dhigh = gmax(sif.dhigh,ldclose)

    tlow = gmin(tlow,sif.dhigh-vrange)
    #tlow = gmin(tlow,dhigh-vrange)

    signal = gand(
            #sif.low < tlow,
            cross(tlow,sif.low)<0,
            #rollx(sif.dhigh-sif.dlow)>360,
            rollx(sif.ma13)  < rollx(sif.ma30),
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
    

break_nhhx = BXFuncA(fstate=gofilter,fsignal=nhhx,fwave=gofilter,ffilter=nfilter0)  ##选择
break_nhhx.name = u'向上突破新高--原始X系统'
break_nllx = SXFuncA(fstate=sdown,fsignal=nllx,fwave=nx2000X,ffilter=nfilter0)  ##选择
break_nllx.name = u'向下突破新低--原始X系统'

break_nhhy = BXFuncA(fstate=gofilter,fsignal=nhhy,fwave=gofilter,ffilter=nfilter0)  ##选择
break_nhhy.name = u'向上突破新高--原始X系统'


break_mhhx = BXFuncA(fstate=gofilter,fsignal=mhhx,fwave=gofilter,ffilter=filter0)  ##选择
break_mhhx.name = u'X分钟向上突破新高--原始X系统'

break_mllx = SXFuncA(fstate=gofilter,fsignal=mllx,fwave=nx2000X,ffilter=filter0)  ##选择
break_mllx.name = u'X分钟向下突破新低--原始X系统'

break_nhhxr = BXFuncA(fstate=gofilter,fsignal=nhhx,fwave=gofilter,ffilter=rmfilter)  ##选择
break_nhhxr.name = u'向上突破新高-原始X系统-前后时段'
break_nllxr = SXFuncA(fstate=gofilter,fsignal=nllx,fwave=nx2000X,ffilter=rmfilter)  ##选择
break_nllxr.name = u'向下突破新低--原始X系统-前后时段'


break_nhhxm = BXFuncA(fstate=gofilter,fsignal=fcustom(nhhx,vbreak=20),fwave=gofilter,ffilter=mfilter)  ##选择
break_nhhxm.name = u'向上突破新高--原始X系统-主要时段'
break_nllxm = SXFuncA(fstate=gofilter,fsignal=fcustom(nllx,vbreak=0),fwave=nx2000X,ffilter=mfilter)  ##选择
break_nllxm.name = u'向下突破新低--原始X系统-主要时段'

break_nhhk = BXFuncA(fstate=gofilter,fsignal=nhhk,fwave=gofilter,ffilter=mfilter)  
break_nhhk.name = u'向上突破新高--原始X系统'
break_nhhk.stop_closer = utrade.atr5_ustop_V7


break_nhhx.stop_closer = utrade.atr5_ustop_TT
break_nllx.stop_closer = utrade.atr5_ustop_TT
break_mhhx.stop_closer = utrade.atr5_ustop_V7
break_mllx.stop_closer = utrade.atr5_ustop_V1
break_nhhxm.stop_closer = utrade.atr5_ustop_V1
break_nllxm.stop_closer = utrade.atr5_ustop_V1

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

#主要时段
break_nxm = [break_nhhxm,break_nllxm]  #120趴下 w=6.4  #6趴下,w=7.1

####以每天前n分钟的高低点为准
def fhx(sif,vbreak=0):
    thigh = np.select([sif.time==1015],[sif.dhigh],0)
    thigh = extend2next(thigh) + vbreak
    signal = gand(
            cross(thigh,sif.high)>0,
            sif.time > 1015,
        )
    msignal = ssum(signal,sif.time==1015)
    signal = gand(signal,
                  msignal < 3,#每天前2次
                  sif.time < 1331,
                )
    return np.select([signal],[gmax(sif.open,thigh)],0)    #避免跳空情况，如果跳空且大于突破点，就以开盘价进入

def flx(sif,vbreak=0):
    tlow = np.select([sif.time==1015],[sif.dlow],0)
    tlow = extend2next(tlow) + vbreak
    signal = gand(cross(tlow,sif.low)<0,
                  sif.time > 1015,
                )
    msignal = ssum(signal,sif.time==1015)
    signal = gand(signal,
                  msignal < 3,#每天前2次
                  sif.time < 1331,
                )
    return np.select([signal],[gmin(sif.open,tlow)],0)    #避免跳空情况，如果跳空且大于突破点，就以开盘价进入

break_fhx = BXFuncA(fstate=gofilter,fsignal=fhx,fwave=gofilter,ffilter=nfilter)  ##选择
break_fhx.name = u'向上突破日初新高'
break_flx = SXFuncA(fstate=gofilter,fsignal=flx,fwave=gofilter,ffilter=nfilter)  ##选择
break_flx.name = u'向下突破日初新低'
break_fhx.stop_closer = utrade.atr5_ustop_V1
break_flx.stop_closer = utrade.atr5_ustop_V1

break_fx = [break_fhx,break_flx]    ##########一个还可以的独立策略. 日亏6点之后不动

def nhh(sif,vbreak=30,vrange=250):  #可以借鉴nhhn的过滤条件,300也不错
    #使用最高点+30, 也就是说必须一下拉开3点
    ldup = dnext(gand(sif.highd>rollx(sif.highd),sif.lowd>rollx(sif.lowd)),sif.close,sif.i_cofd)

    #ldatr = dnext(sif.atrd,sif.close,sif.i_cofd)

    #vrange = sif.close / 1200 * 10

    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)     
    
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)        
    
    ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    thigh = rollx(sif.dhigh+vbreak,3)
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd)

    blow = rollx(sif.dlow,1)
    #blow = rollx(gmin(sif.dlow,ldclose),1)
    #blow = rollx(gmin(sif.dlow,ldhigh),1)
    #thigh = np.select([sif.time<1030,sif.time>=1030],[gmax(thigh,rollx(sif.dlow) + 200),thigh])
    #thigh = gmax(thigh,rollx(sif.dlow,1) + vrange + vbreak)
    #thigh = np.select([gand(sif.time<1330,rollx(sif.dhigh-sif.dlow)<vrange),sif.time>0],[sif.dlow+vrange+vbreak,thigh])    

    slimit = gmax(blow + vrange + vbreak,ldopen+90)
    #slimit = np.select([bnot(ldup)],[slimit],rollx(sif.dhigh))

    thigh = gmax(thigh,slimit)
    signal = gand(
            #cross(rollx(sif.dhigh+30),sif.high)>0
            cross(thigh,sif.high)>0,    #这里在设计实盘的时候要非常小心，本分钟的thigh!=上分钟的thigh
                                        #   好的一点是本分钟的thigh也是能提前计算出来的,所以不算未来数据
            #sif.high  > thigh,
            thigh - sif.dlow < ldopen/33,   #不能涨太多
            #sif.high > thigh,
            rollx(sif.close,3) > thigh * 9966/10000, 
            rollx(sif.xatr) < 2500,
            #rollx(sif.low) > thigh * 9950/10000,
            #rollx(sif.dhigh) > ldlow + 10,     #大于昨日低点
            #rollx(sif.dhigh-sif.dlow,3)>200,
            #thigh - rollx(sif.close,2) < 150,
            #gmax(rollx(sif.dhigh,1),thigh) > ldopen + 80,
            #thigh > ldopen + 60,
            #gor(sif.time>=1330,rollx(sif.dhigh-sif.dlow)>200),
        )
    return np.select([signal],[gmax(sif.open,thigh)],0)    #避免跳空情况，如果跳空且大于突破点，就以跳空价进入
 
def nhhn(sif,vbreak=30):  #不需要删除V
    #使用最高点+30, 也就是说必须一下拉开3点
    #ldlow = dnext(sif.lowd/2+sif.closed/2,sif.close,sif.i_cofd)

    #ldatr = dnext(sif.atrd,sif.close,sif.i_cofd)

    #vrange = sif.close / 1200 * 10

    ldclose = dnext(sif.closed,sif.close,sif.i_cofd)

    vrange = ldclose/125

    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)        
    
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)        
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    thigh = rollx(sif.dhigh+vbreak,3)

    mysdown = gand(sif.low < sif.dhigh-ldclose/75)
    #mysdown = derepeatc(mysdown)
    sss = dsum(mysdown,sif.iday)
    #sss = extend(mysdown,60)

    blow = rollx(sif.dlow,1)
    #thigh = np.select([sif.time<1030,sif.time>=1030],[gmax(thigh,rollx(sif.dlow) + 200),thigh])
    #thigh = gmax(thigh,rollx(sif.dlow,1) + vrange + vbreak)
    #thigh = np.select([gand(sif.time<1330,rollx(sif.dhigh-sif.dlow)<vrange),sif.time>0],[sif.dlow+vrange+vbreak,thigh])    
    thigh = gmax(thigh,blow + vrange + vbreak,ldopen * 1003/1000)
    signal = gand(
            #cross(rollx(sif.dhigh+30),sif.high)>0
            #cross(thigh,sif.high)>0,
            sif.high > thigh,
            rollx(sif.low) > rollx(sif.ma13),
            sss < 1,
            #rollx(sif.dhigh) > ldlow + 10,     #大于昨日低点
            #rollx(sif.dhigh-sif.dlow,3)>200,
            #thigh - rollx(sif.close,2) < 150,
            #gmax(rollx(sif.dhigh,1),thigh) > ldopen + 80,
            #thigh > ldopen + 60,
            #gor(sif.time>=1330,rollx(sif.dhigh-sif.dlow)>200),
        )
    return np.select([signal],[gmax(sif.open,thigh)],0)    #避免跳空情况，如果跳空且大于突破点，就以跳空价进入


def nhh_old(sif,vbreak=30,vrange=250):  #貌似20/30都可以
    #使用最高点+30, 也就是说必须一下拉开3点
    #ldlow = dnext(sif.lowd/2+sif.closed/2,sif.close,sif.i_cofd)

    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)        
    
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)        
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    thigh = rollx(sif.dhigh+vbreak,3)

    #thigh = np.select([sif.time<1030,sif.time>=1030],[gmax(thigh,rollx(sif.dlow) + 200),thigh])
    #thigh = gmax(thigh,rollx(sif.dlow,1) + vrange + vbreak)
    thigh = np.select([gand(sif.time<1330,rollx(sif.dhigh-sif.dlow)<vrange),sif.time>0],[sif.dlow+vrange+vbreak,thigh])    
    signal = gand(
            #cross(rollx(sif.dhigh+30),sif.high)>0
            sif.high > thigh,
            #rollx(sif.dhigh) > ldlow + 10,     #大于昨日低点
            #rollx(sif.dhigh-sif.dlow,3)>200,
            #thigh - rollx(sif.close,2) < 150,
            #gmax(rollx(sif.dhigh,1),thigh) > ldopen + 80,
            thigh > ldopen + 60,
            #gor(sif.time>=1330,rollx(sif.dhigh-sif.dlow)>200),
        )
    return np.select([signal],[gmax(sif.open,thigh)],0)    #避免跳空情况，如果跳空且大于突破点，就以跳空价进入

def nhhz(sif,vbreak=30):  #貌似20/30都可以
    #使用最高点+30, 也就是说必须一下拉开3点
    #ldlow = dnext(sif.lowd/2+sif.closed/2,sif.close,sif.i_cofd)

    #ldatr = dnext(sif.atrd,sif.close,sif.i_cofd)

    #vrange = sif.close / 1200 * 10

    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)        
    
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)        
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd)
    
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    thigh = rollx(sif.dhigh+vbreak,3)

    blow = rollx(sif.dlow,1)
    #blow = gmin(blow,ldclose)
    #thigh = np.select([sif.time<1030,sif.time>=1030],[gmax(thigh,rollx(sif.dlow) + 200),thigh])
    #thigh = gmax(thigh,rollx(sif.dlow,1) + vrange + vbreak)
    #thigh = np.select([gand(sif.time<1330,rollx(sif.dhigh-sif.dlow)<vrange),sif.time>0],[sif.dlow+vrange+vbreak,thigh])    
    
    ldatr = dnext(sif.atrd,sif.close,sif.i_cofd)
    ldclose = dnext(sif.highd,sif.close,sif.i_cofd)
    vrange = ldatr * 3/10 /XBASE
    #vrange = ldatr /XBASE
    vrange = gmin(vrange,ldclose/100)    #vrange不能超过太大
    vopen = ldatr * 1/8 /XBASE

    #vbreak = ldatr * 1/20 /XBASE

    thigh = gmax(thigh,blow + vrange + vbreak,ldopen+vopen)
    signal = gand(
            #cross(rollx(sif.dhigh+30),sif.high)>0
            #sif.high > thigh,
            cross(thigh,sif.high)>0,
            #rollx(sif.dhigh) > ldlow + 10,     #大于昨日低点
            #rollx(sif.dhigh-sif.dlow,3)>200,
            #thigh - rollx(sif.close,2) < 150,
            #gmax(rollx(sif.dhigh,1),thigh) > ldopen + 80,
            #thigh > ldopen + 60,
            #gor(sif.time>=1330,rollx(sif.dhigh-sif.dlow)>200),
            #rollx(sif.ma3) > rollx(sif.ma13),
            rollx(ma(sif.low,3)) > rollx(ma(sif.low,13)),
            rollx(sif.xatr) < 2000,
        )
    #signal = gand(msum(signal,10) > 1,signal)    
    return np.select([signal],[gmax(sif.open,thigh)],0)    #避免跳空情况，如果跳空且大于突破点，就以跳空价进入

def nhhz2(sif,vbreak=30):  #貌似20/30都可以
    #使用最高点+30, 也就是说必须一下拉开3点
    #ldlow = dnext(sif.lowd/2+sif.closed/2,sif.close,sif.i_cofd)

    #ldatr = dnext(sif.atrd,sif.close,sif.i_cofd)

    #vrange = sif.close / 1200 * 10

    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)        
    
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)        
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd)
    
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    thigh = rollx(sif.dhigh+vbreak,3)

    blow = rollx(sif.dlow,1)
    #blow = gmin(blow,ldclose)
    #thigh = np.select([sif.time<1030,sif.time>=1030],[gmax(thigh,rollx(sif.dlow) + 200),thigh])
    #thigh = gmax(thigh,rollx(sif.dlow,1) + vrange + vbreak)
    #thigh = np.select([gand(sif.time<1330,rollx(sif.dhigh-sif.dlow)<vrange),sif.time>0],[sif.dlow+vrange+vbreak,thigh])    
    
    ldatr = dnext(sif.atrd,sif.close,sif.i_cofd)
    ldclose = dnext(sif.highd,sif.close,sif.i_cofd)
    vrange = ldatr * 3/10 /XBASE
    #vrange = ldatr /XBASE
    vrange = gmin(vrange,ldclose/100)    #vrange不能超过太大
    vopen = ldatr * 1/8 /XBASE

    #vbreak = ldatr * 1/20 /XBASE

    #ldrange = np.abs(sif.closed-sif.opend)*1000 / (sif.highd-sif.lowd)
    ldrange = np.abs(sif.closed-sif.opend)*100000 / sif.atrd
    #ldwave = np.abs(sif.closed-sif.opend)*1000 / sif.opend
    ldwave = np.abs(sif.closed-sif.opend)*1000 / sif.atrd

    cldrange = cexpma(cexpma(np.abs(sif.closed-sif.opend)*1000*XBASE / sif.atrd,10),10)
    cldwave = cexpma(np.abs(sif.closed-sif.opend)*1000*XBASE / sif.atrd,10)
    crange = dnext(cldrange,sif.close,sif.i_cofd)
    cwave = dnext(cldwave,sif.close,sif.i_cofd)

    lrange = dnext(ldrange,sif.close,sif.i_cofd)
    lwave = dnext(ma(ldwave,10),sif.close,sif.i_cofd)
    mlrange = dnext(ma(ldrange,10),sif.close,sif.i_cofd)
    ldrange2 = 100000 / (sif.highd-sif.lowd)
    #ldrange2 = sif.atrd / (sif.highd-sif.lowd)
    #ldrange2 = sif.lowd / (sif.highd-sif.lowd)
    #lrange2 = dnext(nma(ldrange2,10),sif.close,sif.i_cofd)
    lrange2 = dnext(nma(ldrange2,10),sif.close,sif.i_cofd)

    ldxatr = dnext(sif.xatrd,sif.close,sif.i_cofd)
    ldmxatr = dnext(sif.mxatrd,sif.close,sif.i_cofd)

    thigh = gmax(thigh,blow + vrange + vbreak,ldopen+vopen)
    signal = gand(
            #cross(rollx(sif.dhigh+30),sif.high)>0
            #sif.high > thigh,
            cross(thigh,sif.high)>0,
            #rollx(sif.dhigh) > ldlow + 10,     #大于昨日低点
            #rollx(sif.dhigh-sif.dlow,3)>200,
            #thigh - rollx(sif.close,2) < 150,
            #gmax(rollx(sif.dhigh,1),thigh) > ldopen + 80,
            #thigh > ldopen + 60,
            #gor(sif.time>=1330,rollx(sif.dhigh-sif.dlow)>200),
            #rollx(sif.ma3) > rollx(sif.ma13),
            rollx(ma(sif.low,3)) > rollx(ma(sif.low,13)),
            rollx(sif.xatr) < 2000,
            lrange2 > 105,#这个最好
            #crange > 450,
            #cwave > 400,
            #lrange>mlrange,
            #lrange > 30,
            #lwave > 12,
            #strend2(ldmxatr)>0,
            #ldxatr > 16000,
        )
    return np.select([signal],[gmax(sif.open,thigh)],0)    #避免跳空情况，如果跳空且大于突破点，就以跳空价进入


def nhhv(sif,vbreak=30):  #貌似20/30都可以
    #使用最高点+30, 也就是说必须一下拉开3点
    #ldlow = dnext(sif.lowd/2+sif.closed/2,sif.close,sif.i_cofd)

    #ldatr = dnext(sif.atrd,sif.close,sif.i_cofd)

    #vrange = sif.close / 1200 * 10

    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)        
    
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)        
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd)
    
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    thigh = rollx(sif.dhigh+vbreak,3)

    blow = ldopen
    #blow = gmin(blow,ldclose)
    #thigh = np.select([sif.time<1030,sif.time>=1030],[gmax(thigh,rollx(sif.dlow) + 200),thigh])
    #thigh = gmax(thigh,rollx(sif.dlow,1) + vrange + vbreak)
    #thigh = np.select([gand(sif.time<1330,rollx(sif.dhigh-sif.dlow)<vrange),sif.time>0],[sif.dlow+vrange+vbreak,thigh])    
    
    ldatr = dnext(sif.atrd,sif.close,sif.i_cofd)
    ldclose = dnext(sif.highd,sif.close,sif.i_cofd)
    vrange = ldatr * 1/3 /XBASE
    #vrange = gmin(vrange,ldclose/133)    #vrange不能超过太大
    vopen = ldatr * 1/8 /XBASE

    #vbreak = ldatr * 1/20 /XBASE

    vwave = dnext(ma(sif.dhigh-sif.dlow,30),sif.close,sif.i_cofd)

    vrange = vwave * 1/2
    vrange = gmin(vrange,ldclose/100)    #vrange不能超过太大

    thigh = gmax(thigh,blow + vrange)
    #thigh = blow + vrange
    signal = gand(
            #cross(rollx(sif.dhigh+30),sif.high)>0
            #sif.high > thigh,
            cross(thigh,sif.high)>0,
            rollx(sif.close,3) > thigh * 9966/10000, 
            #rollx(sif.close,3) > thigh * 9950/10000, 
            #rollx(sif.low) > thigh * 9940/10000,
            #rollx(sif.dhigh) > ldlow + 10,     #大于昨日低点
            #rollx(sif.dhigh-sif.dlow,3)>200,
            #thigh - rollx(sif.close,2) < 150,
            #gmax(rollx(sif.dhigh,1),thigh) > ldopen + 80,
            #thigh > ldopen + 60,
            #gor(sif.time>=1330,rollx(sif.dhigh-sif.dlow)>200),
            rollx(sif.ma5) > rollx(sif.ma13),
            rollx(sif.xatr) < 2000,
            thigh - sif.dlow < ldopen/33,   #不能涨太多
        )
    return np.select([signal],[gmax(sif.open,thigh)],0)    #避免跳空情况，如果跳空且大于突破点，就以跳空价进入


def mhhz(sif,vbreak=36):  #貌似20/30都可以
    #使用最高点+30, 也就是说必须一下拉开3点

    #ldatr = dnext(sif.atrd,sif.close,sif.i_cofd)

    #vrange = sif.close / 1200 * 10

    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)        
    
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)        
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd)
    ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    #thigh = rollx(sif.dhigh+vbreak,3)
    #thigh = rollx(tmax(sif.high,75)+vbreak,20)
    thigh = rollx(tmax(sif.high,90)+vbreak,3)

    blow = rollx(sif.dlow,1)
    #blow = gmin(blow,ldclose)
    #thigh = np.select([sif.time<1030,sif.time>=1030],[gmax(thigh,rollx(sif.dlow) + 200),thigh])
    #thigh = gmax(thigh,rollx(sif.dlow,1) + vrange + vbreak)
    #thigh = np.select([gand(sif.time<1330,rollx(sif.dhigh-sif.dlow)<vrange),sif.time>0],[sif.dlow+vrange+vbreak,thigh])    
    
    ldatr = dnext(sif.atrd,sif.close,sif.i_cofd)
    ldclose = dnext(sif.highd,sif.close,sif.i_cofd)
    vrange = ldatr *3/10 /XBASE
    #vrange = gmin(vrange,ldclose/133)    #vrange不能超过太大
    vopen = ldatr * 1/8 /XBASE
    vrange2 = ldatr *4/10 /XBASE

    #vbreak = ldatr * 1/20 /XBASE

    thigh2 = gmax(thigh,blow + vrange)#,ldopen)#+vopen)
    thigh3 = gmax(thigh,blow + vrange2)#,ldopen)#+vopen)

    thigh = np.select([sif.time<1315,sif.time>=1315],[thigh2,thigh])
    #thigh = thigh2

    signal = gand(
            cross(thigh,sif.high)>0,
            #sif.high > thigh,
            #rollx(sif.dhigh) > ldlow + 10,     #大于昨日低点
            #rollx(sif.dhigh-sif.dlow,3)>200,
            #rollx(thigh) - rollx(sif.close,2) < 150,
            #gmax(rollx(sif.dhigh,1),thigh) > ldopen + 80,
            #thigh > ldopen + 60,
            #gor(sif.time>=1330,rollx(sif.dhigh-sif.dlow)>200),
            rollx(ma(sif.low,3)) > rollx(ma(sif.low,13)),
            rollx(sif.xatr) < 2000,
            sif.sdiff5x > 0,
        )
    return np.select([signal],[gmax(sif.open,thigh)],0)    #避免跳空情况，如果跳空且大于突破点，就以跳空价进入

def nllz(sif,vbreak=20):
    #使用最低点
    tlow = rollx(sif.dlow+vbreak,1)
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    #ldmid = dnext((sif.highd+gmin(sif.closed,sif.opend))/2,sif.close,sif.i_cofd)
    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)            
    #highd = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)            
    #ldmid = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)        
    #ldmid = dnext(sif.highd,sif.close,sif.i_cofd)        
    #ldmid = dnext((sif.highd+sif.closed)/2,sif.close,sif.i_cofd)    
    ldrange = dnext(sif.highd-sif.lowd,sif.close,sif.i_cofd) 
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd) 
    
    ldatr30 = dnext(sif.atr30,sif.close,sif.i_cof30)
    ldatr = dnext(sif.atrd,sif.close,sif.i_cofd)
    
    xatrd = dnext(sif.xatrd,sif.close,sif.i_cofd)

    #bhigh = gmax(ldclose,sif.dhigh)
    bhigh = sif.dhigh

    vrange = ldatr *8/10 / XBASE
    #vrange = np.select([vrange<500],[vrange],500)
    vrange = gmin(vrange,ldclose/66)    #vrange不能超过太大
    vmid = ldatr *1/15/XBASE
    #vmid = 60

    #tlow = gmin(tlow,ldmid-32)
    
    #tlow = np.select([sif.time<1330,sif.time>0],[sif.dhigh-vrange,tlow])    
    tlow = np.select([sif.time<1330,sif.time>=1330],[gmin(bhigh-vrange,tlow),tlow])
    #tlow = gmin(sif.dhigh-vrange,tlow)
    #tlow = np.select([tlow<=rollx(sif.dlow)+vbreak,1],[tlow,gmin(tlow,ldmid-60)])
    #tlow = np.select([tlow>ldmid-60,tlow<=ldmid-60],[rollx(sif.dlow),tlow])
    #tlow = np.select([gand(sif.time<1330,rollx(sif.dhigh-sif.dlow)<vrange+vbreak),sif.time>0],[sif.dhigh-vrange,tlow])
    #tlow = np.select([sif.time<1330,sif.time>0],[gmin(tlow,sif.dhigh-vrange),tlow])
    #tlow = np.select([rollx(sif.dhigh-sif.dlow)<vrange+vbreak,sif.time>0],[sif.dhigh-vrange,tlow])
    #tlow = np.select([gand(sif.time<1330,sif.dhigh-sif.dlow<vrange+vbreak),gand(sif.time<1330,sif.dhigh-sif.dlow>vrange+vbreak),sif.time>1330],[sif.dhigh-vrange,tlow,gmin(sif.dhigh-350,tlow)])
    #tlow = gmin(sif.dhigh-vrange,tlow)
    #tlow = gmin(sif.dhigh-400,tlow)

    

    signal = gand(
            #sif.time>1029,
            cross(tlow,sif.low)<0,
            #strend2(sif.low) <= 0,
            #sif.low < tlow,
            #tlow < rollx(sif.dhigh + sif.dlow)/2, #+ sif.dlow
            #tlow < ldhigh-10,  #比昨日最高价低才允许做空
            #tlow < ldmid-30,#rollx(sif.xatr)*2/XBASE,  #比前2天高点中点低才允许做空
            #gor(tlow < ldmid-30,gand(sif.time>1330,tlow<opend)),#加上1330条件后，有助于减少回撤
            #gor(tlow < ldmid-30,gand(sif.time>1330,tlow==rollx(sif.dlow)+vbreak)),  #1330之后tlow同时创新低时可绕过ldmid-30条件
            tlow < ldmid - vmid,
            #rollx(sif.dhigh - sif.dlow) > vrange, 
            #gor(sif.time>=1330,rollx(sif.dhigh-sif.dlow)>320),
            #rollx(sif.high,2) - tlow < 150,
            sif.time > 915,
            rollx(sif.ma13) < rollx(sif.ma30),
            rollx(sif.xatr)<2500,
            rollx(sif.xatr30x)<10000,
        )
    return np.select([signal],[gmin(sif.open,tlow)],0)    #避免跳空情况，如果跳空且小于突破点，就以跳空价进入

def nll2(sif,vbreak=-10,vrange=350):
    #使用最低点
    tlow = rollx(sif.dlow+vbreak,1)
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)    
    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)        
    tlow = np.select([gand(sif.time<1330,rollx(sif.dhigh-sif.dlow)<vrange+vbreak),sif.time>0],[sif.dhigh-vrange,tlow])    
    #tlow = np.select([sif.time<1330,sif.time>0],[sif.dhigh-vrange,tlow])
    #tlow = gmin(tlow,sif.dhigh-vrange+vbreak)
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)            
    tlow = gmin(tlow,ldopen-150)
    signal = gand(
            #cross(rollx(sif.dlow-30),sif.low)<0
            #sif.low < rollx(sif.dlow+vbreak,3), #比close要小点
            #sif.low < ldhigh,
            cross(tlow,sif.low)<0,
            #sif.low < tlow,
            #tlow < ldmid-60,#rollx(sif.xatr)*2/XBASE,  #比前2天高点中点低才允许做空
            #tlow < ldopen - 100,
            #gor(sif.time>=1330,rollx(sif.dhigh-sif.dlow)>350),
        )
    return np.select([signal],[gmin(sif.open,tlow)],0)    #避免跳空情况，如果跳空且小于突破点，就以跳空价进入
    
 
def nll2_old(sif,vbreak=20):
    #使用最低点
    tlow = rollx(sif.dlow+vbreak,1)
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)    
    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)        
    return gand(
            #cross(rollx(sif.dlow-30),sif.low)<0
            #sif.low < rollx(sif.dlow+vbreak,3), #比close要小点
            #sif.low < ldhigh,
            cross(tlow,sif.low)<0,
            tlow < ldmid-30,#rollx(sif.xatr)*2/XBASE,  #比前2天高点中点低才允许做空
            gor(sif.time>=1330,rollx(sif.dhigh-sif.dlow)>350),
        )

def nll3(sif,vbreak=20):
    #使用最低点
    tlow = rollx(tmin(sif.low,75)/2 + sif.dlow/2 +vbreak,2)
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)    
    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)        
    return gand(
            #cross(rollx(sif.dlow-30),sif.low)<0
            #sif.low < rollx(sif.dlow+vbreak,3), #比close要小点
            #sif.low < ldhigh,
            cross(tlow,sif.low)<0,
            tlow < ldmid-30,#rollx(sif.xatr)*2/XBASE,  #比前2天高点中点低才允许做空
            gor(sif.time>=1330,rollx(sif.dhigh-sif.dlow)>350),
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


break_nhh0 = BXFuncA(fstate=gofilter,fsignal=fcustom(nhh,vbreak=0),fwave=nx2500X,ffilter=filter0)  ##选择
break_nhh0.name = u'向上突破新高--原始系统'
    

break_nhh = BXFuncA(fstate=gofilter,fsignal=nhh,fwave=nx2500X,ffilter=nfilter)  ##选择
break_nhh.name = u'向上突破新高'

hbreak_nhh = BXFuncA(fstate=gofilter,fsignal=nhh,fwave=gofilter,ffilter=mfilter)  ##主要时段
#hbreak_nhh = BXFuncA(fstate=gofilter,fsignal=nhh,fwave=nx2500X,ffilter=nfilter2)  ##主要时段
hbreak_nhh.name = u'日内向上突破新高'

hbreak_nhhn = BXFuncA(fstate=gofilter,fsignal=nhhn,fwave=nx2500X,ffilter=mfilter)  ##主要时段
hbreak_nhhn.name = u'日内向上突破新高n'


hbreak_nhhz = BXFuncA(fstate=gofilter,fsignal=nhhz,fwave=gofilter,ffilter=mfilter)  ##主要时段
#hbreak_nhhz = BXFuncA(fstate=gofilter,fsignal=nhhz,fwave=gofilter,ffilter=efilter)  ##主要时段
hbreak_nhhz.name = u'日内向上突破新高'

hbreak_nhhz2 = BXFuncA(fstate=gofilter,fsignal=nhhz2,fwave=gofilter,ffilter=mfilter)  ##主要时段
hbreak_nhhz2.name = u'日内向上突破新高'

hbreak_nhht = BXFuncA(fstate=gofilter,fsignal=nhht,fwave=gofilter,ffilter=nfilter3)  ##主要时段
#hbreak_nhht = BXFuncA(fstate=gofilter,fsignal=nhht,fwave=gofilter,ffilter=efilter)  ##主要时段
hbreak_nhht.name = u'日内向上突破新高'

shbreak_nllz = SXFuncA(fstate=sdown,fsignal=nllz,fwave=gofilter,ffilter=mfilter2)    #优于nll
shbreak_nllz.name = u'日内7向下突破新低z'


hbreak_nhhv = BXFuncA(fstate=gofilter,fsignal=nhhv,fwave=gofilter,ffilter=mfilter)  ##主要时段
hbreak_nhhv.name = u'日内向上突破新高'


hbreak_mhhz = BXFuncA(fstate=gofilter,fsignal=mhhz,fwave=gofilter,ffilter=mfilter)  ##主要时段
hbreak_mhhz.name = u'日内向上突破分钟新高'


hbreak_nhh_e = BXFuncF1(fstate=gofilter,fsignal=fcustom(nhh,vrange=350),fwave=gofilter,ffilter=emfilter3)  ##主要时段
hbreak_nhh_e.name = u'日内向上突破新高e'

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


sbreak_nll20 = SXFuncA(fstate=gofilter,fsignal=fcustom(nll2,vbreak=0),fwave=nx2500X,ffilter=filter0)    #这个R高，但是次数少
sbreak_nll20.name = u'向下突破--原始系统'

sbreak_nll2 = SXFuncA(fstate=sdown,fsignal=nll2,fwave=nx2500X,ffilter=mfilter2)    #这个R高，不错
sbreak_nll2.name = u'向下突破2'

shbreak_nll2 = SXFuncA(fstate=sdown,fsignal=nll2,fwave=nx2500X,ffilter=nfilter)    #

skbreak_nll2 = SXFuncD1(fstate=sdown,fsignal=nll2,fwave=nx2500X,ffilter=kfilter)    #
#skbreak_nll2.stop_closer = utrade.atr5_ustop_V

#sbreak_nlc + sbreak_nlc_break = sbreak_nll2

zbreak0 = [break_nhh0,sbreak_nll20] #这个最好,理念最清晰

zbreak = [break_nhh,sbreak_nll2] #这个最好,理念最清晰

zhbreak = [hbreak_nhh,shbreak_nll2]     #也是一个不错的主方法   ##############

zhbreak2 = [break_nhhx,shbreak_nll2]     #也是一个不错的主方法   ##############


###
def mhh2(sif,length=20):
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
#def mll2(sif,length=80,vbreak=10,vrange=350):
def mll2(sif,length=80,vbreak=10,vrange=270,vrange2=200):    
    '''
        280去掉时间放松
        与350加时间放松效果类似
        vrange2为tlimit后的约束
    '''
    #使用最低点
    tlow = rollx(tmin(sif.low,length)+vbreak,1)
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    #ldmid = dnext((sif.highd+gmin(sif.closed,sif.opend))/2,sif.close,sif.i_cofd)
    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    

    #ldlow = dnext(gmin(sif.closed,sif.opend),sif.close,sif.i_cofd) - 0 
    ldlow = dnext(sif.lowd,sif.close,sif.i_cofd) 
    lddown = dnext(gand(sif.highd < rollx(sif.highd),sif.lowd<rollx(sif.lowd)),sif.close,sif.i_cofd)


    opend = dnext(sif.opend,sif.open,sif.i_oofd)            
    #highd = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)            
    #ldmid = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)        
    #ldmid = dnext(sif.highd,sif.close,sif.i_cofd)        
    #ldmid = dnext((sif.highd+sif.closed)/2,sif.close,sif.i_cofd)    
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd) 
    
    ldatr = dnext(sif.atr30,sif.close,sif.i_cof30)
    #vrange = ldatr *2 / XBASE
    #vrange2 = 0

    #tlow = gmin(tlow,ldmid-32)
    
    #mytime = 1315

    tlimit = 1325   #不如所有时间都作幅度要求
    #tlimit = 1325
    
    vhigh = sif.dhigh
    #vhigh = gmax((ldclose-sif.dhigh)/2+sif.dhigh,sif.dhigh)
    #vhigh = gmax(ldclose,sif.dhigh)
    #vhigh = gmax(ldlow,sif.dhigh)
    drange = rollx(vhigh - sif.dlow)
    #drange = rollx(sif.dhigh - sif.dlow)

    #tlow = np.select([sif.time<1330,sif.time>0],[sif.dhigh-vrange,tlow])
    #slimit = np.select([sif.time<1325,sif.time>=1325],[sif.dhigh-vrange,sif.dhigh-250])
    #slimit = np.select([sif.time<tlimit,sif.time>=tlimit],[sif.dhigh-vrange,tlow])

    #slimit = np.select([gor(sif.time>=tlimit,drange >= vrange),sif.time<tlimit],[tlow,sif.dhigh-vrange])   #时间大于tlimit或振幅大于vrange,则以现有分钟均线为准

    #slimit = np.select([gand(sif.time<tlimit,drange<vrange)],[sif.dhigh-vrange],tlow)   #时间大于tlimit或振幅大于vrange,则以现有分钟均线为准
    
    #slimit = np.select([gand(sif.time<tlimit,drange<vrange)],[vhigh-vrange],tlow)   #时间大于tlimit或振幅大于vrange,则以现有分钟均线为准
    #这个有问题，当价格处于vrange和vrange2之间时，有问题
    slimit = np.select([gand(sif.time<tlimit,drange<vrange),gand(sif.time>tlimit,drange<vrange)],[vhigh-vrange,vhigh-vrange2],tlow)   #时间大于tlimit或振幅大于vrange,则以现有分钟均线为准

    #slimit = np.select([sif.time<1325,sif.time>=1325],[sif.dhigh-vrange,gmax(sif.dhigh-250,ldlow)])
    #slimit = gmax(slimit,ldlow)
    #slimit = np.select([lddown],[sif.dhigh-250],slimit)
    #tlow = np.select([sif.time<1325,sif.time>=1325],[gmin(sif.dhigh-vrange,tlow),gmin(tlow,sif.dhigh-250)])
    tlow = gmin(slimit,tlow,ldmid-60)
    #tlow = np.select([sif.time<1325,sif.time>=1325],[gmin(sif.dhigh-vrange,tlow),tlow])
    #tlow = np.select([sif.time<mytime,sif.time>=mytime],[gmin(sif.dhigh-vrange,tlow),gmin(sif.dhigh-vrange2,tlow)])
    #tlow = np.select([sif.time<1330,sif.time>=1330],[gmin(sif.dhigh-vrange,tlow),tlow])
    #tlow = np.select([tlow<=rollx(sif.dlow)+vbreak,1],[tlow,gmin(tlow,ldmid-60)])
    #tlow = np.select([tlow>ldmid-60,tlow<=ldmid-60],[rollx(sif.dlow),tlow])
    #tlow = np.select([gand(sif.time<1330,rollx(sif.dhigh-sif.dlow)<vrange+vbreak),sif.time>0],[sif.dhigh-vrange,tlow])
    #tlow = np.select([sif.time<1330,sif.time>0],[gmin(tlow,sif.dhigh-vrange),tlow])
    #tlow = np.select([rollx(sif.dhigh-sif.dlow)<vrange+vbreak,sif.time>0],[sif.dhigh-vrange,tlow])
    #tlow = np.select([gand(sif.time<1330,sif.dhigh-sif.dlow<vrange+vbreak),gand(sif.time<1330,sif.dhigh-sif.dlow>vrange+vbreak),sif.time>1330],[sif.dhigh-vrange,tlow,gmin(sif.dhigh-350,tlow)])
    #tlow = gmin(sif.dhigh-vrange,tlow)
    #tlow = gmin(sif.dhigh-400,tlow)

    #tlow = np.select([gand(tlow>ldmid-60,tlow>rollx(sif.dlow)+vbreak),gor(tlow<=ldmid-60,tlow==rollx(sif.dlow)+vbreak)],[ldmid-60,tlow])

    signal = gand(
            cross(tlow,sif.low)<0,
            #rollx(sif.close) < tlow + 50,
            rollx(sif.close) < tlow * 10015/10000,
            #rollx(sif.close,3) < tlow * 10050/10000,
            #rollx(sif.high) < tlow * 10025/10000,
            #sif.low < tlow,
            gor(tlow<ldmid-60),#,tlow==rollx(sif.dlow)+vbreak),
            #sif.time > 915,
            rollx(sif.ma13) < rollx(sif.ma30),
            #rollx(sif.ma7) < rollx(sif.ma20),
            #sif.dhigh - sif.low > 150,
            #sif.dhigh - tlow > 120,
            #sif.time < 1325,
            #tlow > sif.dhigh - 350,
            sif.dhigh - tlow < opend/33,   #不能跌太多
        )
    return np.select([signal],[gmin(sif.open,tlow)],0)    #避免跳空情况，如果跳空且小于突破点，就以跳空价进入.
 
def rll(sif,length=80,vbreak=10,vrange=270):    
    #使用最低点
    tlow = rollx(tmin(sif.low,length)+vbreak,1)
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    #ldmid = dnext((sif.highd+gmin(sif.closed,sif.opend))/2,sif.close,sif.i_cofd)
    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    

    #ldlow = dnext(gmin(sif.closed,sif.opend),sif.close,sif.i_cofd) - 0 
    ldlow = dnext(sif.lowd,sif.close,sif.i_cofd) 
    lddown = dnext(gand(sif.highd < rollx(sif.highd),sif.lowd<rollx(sif.lowd)),sif.close,sif.i_cofd)


    opend = dnext(sif.opend,sif.open,sif.i_oofd)            
    #highd = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)            
    #ldmid = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)        
    #ldmid = dnext(sif.highd,sif.close,sif.i_cofd)        
    #ldmid = dnext((sif.highd+sif.closed)/2,sif.close,sif.i_cofd)    
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd) 
    
    ldatr = dnext(sif.atr30,sif.close,sif.i_cof30)
    #vrange = ldatr *2 / XBASE
    #vrange2 = 0

    #tlow = gmin(tlow,ldmid-32)
    
    #mytime = 1315

    tlimit = 1525   #不如所有时间都作幅度要求
    #tlimit = 1325
    
    vhigh = sif.dhigh
    #vhigh = gmax((ldclose-sif.dhigh)/2+sif.dhigh,sif.dhigh)
    #vhigh = gmax(ldclose,sif.dhigh)
    #vhigh = gmax(ldlow,sif.dhigh)
    drange = rollx(vhigh - sif.dlow)
    #drange = rollx(sif.dhigh - sif.dlow)

    #tlow = np.select([sif.time<1330,sif.time>0],[sif.dhigh-vrange,tlow])
    #slimit = np.select([sif.time<1325,sif.time>=1325],[sif.dhigh-vrange,sif.dhigh-250])
    #slimit = np.select([sif.time<tlimit,sif.time>=tlimit],[sif.dhigh-vrange,tlow])

    #slimit = np.select([gor(sif.time>=tlimit,drange >= vrange),sif.time<tlimit],[tlow,sif.dhigh-vrange])   #时间大于tlimit或振幅大于vrange,则以现有分钟均线为准

    #slimit = np.select([gand(sif.time<tlimit,drange<vrange)],[sif.dhigh-vrange],tlow)   #时间大于tlimit或振幅大于vrange,则以现有分钟均线为准
    #slimit = np.select([gand(sif.time<tlimit,drange<vrange)],[vhigh-vrange],tlow)   #时间大于tlimit或振幅大于vrange,则以现有分钟均线为准

    #slimit = np.select([sif.time<1325,sif.time>=1325],[sif.dhigh-vrange,gmax(sif.dhigh-250,ldlow)])
    #slimit = gmax(slimit,ldlow)
    #slimit = np.select([lddown],[sif.dhigh-250],slimit)
    #tlow = np.select([sif.time<1325,sif.time>=1325],[gmin(sif.dhigh-vrange,tlow),gmin(tlow,sif.dhigh-250)])
    #tlow = gmin(slimit,tlow,ldmid-60)
    #tlow = gmin(vhigh-vrange,tlow)
    #tlow = np.select([sif.time<1325,sif.time>=1325],[gmin(sif.dhigh-vrange,tlow),tlow])
    #tlow = np.select([sif.time<mytime,sif.time>=mytime],[gmin(sif.dhigh-vrange,tlow),gmin(sif.dhigh-vrange2,tlow)])
    #tlow = np.select([sif.time<1330,sif.time>=1330],[gmin(sif.dhigh-vrange,tlow),tlow])
    #tlow = np.select([tlow<=rollx(sif.dlow)+vbreak,1],[tlow,gmin(tlow,ldmid-60)])
    #tlow = np.select([tlow>ldmid-60,tlow<=ldmid-60],[rollx(sif.dlow),tlow])
    #tlow = np.select([gand(sif.time<1330,rollx(sif.dhigh-sif.dlow)<vrange+vbreak),sif.time>0],[sif.dhigh-vrange,tlow])
    #tlow = np.select([sif.time<1330,sif.time>0],[gmin(tlow,sif.dhigh-vrange),tlow])
    #tlow = np.select([rollx(sif.dhigh-sif.dlow)<vrange+vbreak,sif.time>0],[sif.dhigh-vrange,tlow])
    #tlow = np.select([gand(sif.time<1330,sif.dhigh-sif.dlow<vrange+vbreak),gand(sif.time<1330,sif.dhigh-sif.dlow>vrange+vbreak),sif.time>1330],[sif.dhigh-vrange,tlow,gmin(sif.dhigh-350,tlow)])
    #tlow = gmin(sif.dhigh-vrange,tlow)
    #tlow = gmin(sif.dhigh-400,tlow)

    #tlow = np.select([gand(tlow>ldmid-60,tlow>rollx(sif.dlow)+vbreak),gor(tlow<=ldmid-60,tlow==rollx(sif.dlow)+vbreak)],[ldmid-60,tlow])

    signal = gand(
            cross(tlow,sif.low)<0,
            #rollx(sif.close) < tlow + 50,
            #rollx(sif.close) < tlow * 10015/10000,
            #rollx(sif.close,3) < tlow * 10050/10000,
            #rollx(sif.high) < tlow * 10025/10000,
            #sif.low < tlow,
            #gor(tlow<ldmid-60),#,tlow==rollx(sif.dlow)+vbreak),
            #sif.time > 915,
            rollx(sif.ma13) > rollx(sif.ma30),
            #rollx(sif.ma7) > rollx(sif.ma20),
            #sif.dhigh - sif.low > 150,
            #sif.dhigh - tlow > 120,
            #sif.time < 1325,
            #tlow > sif.dhigh - 350,
        )
    return np.select([signal],[gmin(sif.open,tlow)],0)    #避免跳空情况，如果跳空且小于突破点，就以跳空价进入


###时间低点突破
def mll2n(sif,length=80,vbreak=10,vrange=350):#创新低后弹起16点后60分钟内不能开空
    #使用最低点
    tlow = rollx(tmin(sif.low,length)+vbreak,1)
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    #ldmid = dnext((sif.highd+gmin(sif.closed,sif.opend))/2,sif.close,sif.i_cofd)
    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)            

    #highd = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)            
    #ldmid = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)        
    #ldmid = dnext(sif.highd,sif.close,sif.i_cofd)        
    #ldmid = dnext((sif.highd+sif.closed)/2,sif.close,sif.i_cofd)    
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd) 
    
    ldatr = dnext(sif.atr30,sif.close,sif.i_cof30)
    
    vrange = ldclose / 80

    #vrange = ldatr *2 / XBASE
    #vrange2 = 0

    #tlow = gmin(tlow,ldmid-32)
    
    #mytime = 1315

    #tlow = np.select([sif.time<1330,sif.time>0],[sif.dhigh-vrange,tlow])    
    tlow = np.select([sif.time<1315,sif.time>=1315],[gmin(sif.dhigh-vrange,tlow),tlow])
    #tlow = gmin(sif.dhigh-vrange,tlow)
    #tlow = np.select([sif.time<mytime,sif.time>=mytime],[gmin(sif.dhigh-vrange,tlow),gmin(sif.dhigh-vrange2,tlow)])
    #tlow = np.select([sif.time<1330,sif.time>=1330],[gmin(sif.dhigh-vrange,tlow),tlow])
    #tlow = np.select([tlow<=rollx(sif.dlow)+vbreak,1],[tlow,gmin(tlow,ldmid-60)])
    #tlow = np.select([tlow>ldmid-60,tlow<=ldmid-60],[rollx(sif.dlow),tlow])
    #tlow = np.select([gand(sif.time<1330,rollx(sif.dhigh-sif.dlow)<vrange+vbreak),sif.time>0],[sif.dhigh-vrange,tlow])
    #tlow = np.select([sif.time<1330,sif.time>0],[gmin(tlow,sif.dhigh-vrange),tlow])
    #tlow = np.select([rollx(sif.dhigh-sif.dlow)<vrange+vbreak,sif.time>0],[sif.dhigh-vrange,tlow])
    #tlow = np.select([gand(sif.time<1330,sif.dhigh-sif.dlow<vrange+vbreak),gand(sif.time<1330,sif.dhigh-sif.dlow>vrange+vbreak),sif.time>1330],[sif.dhigh-vrange,tlow,gmin(sif.dhigh-350,tlow)])
    #tlow = gmin(sif.dhigh-vrange,tlow)
    #tlow = gmin(sif.dhigh-400,tlow)

    #tlow = np.select([gand(tlow>ldmid-60,tlow>rollx(sif.dlow)+vbreak),gor(tlow<=ldmid-60,tlow==rollx(sif.dlow)+vbreak)],[ldmid-60,tlow])

    #mysup = gand(sif.high > opend + 90)
    #mysup = gand(sif.high > sif.dlow + 160)
    mysup = gand(sif.high > sif.dlow + sif.dlow/ 12000* 80)
    #mysup = derepeatc(mysup)
    mysup = decover1(mysup,30)
    #mysup = gand(sif.high > sif.dlow + sif.atr5x *2.5/XBASE)
    #mysup = gand(sif.high > sif.dlow +ldclose/200)#160)
    #mysup = gand(sif.high > sif.dlow  * 1005/1000)#+160)
    sss = dsum(mysup,sif.iday)
    
    #sss = extend(mysup,60)

    signal = gand(
            #cross(tlow,sif.low)<0,
            sif.low < tlow,
            #gor(tlow<ldmid-60),#,tlow==rollx(sif.dlow)+vbreak),
            gor(tlow<ldmid-120),#,tlow==rollx(sif.dlow)+vbreak),
            #sif.time > 915,
            #rollx(sif.ma13) < rollx(sif.ma30),
            rollx(sif.high) < rollx(sif.ma20),
            sss < 1,
            #sif.dhigh - sif.low > 150,
        )
    return np.select([signal],[gmin(sif.open,tlow)],0)    #避免跳空情况，如果跳空且小于突破点，就以跳空价进入

###时间低点突破
def mll2r(sif,length=80,vbreak=10,vrange=250):
    #使用最低点
    #tlow = rollx(tmin(sif.low,length)+vbreak,1)
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    #ldmid = dnext((sif.highd+gmin(sif.closed,sif.opend))/2,sif.close,sif.i_cofd)
    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)            
    #highd = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)            
    #ldmid = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)        
    #ldmid = dnext(sif.highd,sif.close,sif.i_cofd)        
    #ldmid = dnext((sif.highd+sif.closed)/2,sif.close,sif.i_cofd)    
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd) 
    
    ldatr = dnext(sif.atr30,sif.close,sif.i_cof30)
    #vrange = ldatr *2 / XBASE
    #vrange2 = 0

    #tlow = gmin(tlow,ldmid-32)
    
    #mytime = 1315

    #vrange = ldatr *5/3/ XBASE
    vrange = 400
    #vrange = gmin(vrange,ldclose/66)    #vrange不能超过太大

    #tlow = np.select([sif.time<1330,sif.time>0],[sif.dhigh-vrange,tlow])    
    #tlow = np.select([sif.time<1315,sif.time>=1315],[gmin(sif.dhigh-vrange,tlow),tlow])
    tlow = sif.dhigh-vrange
    #tlow = np.select([sif.time<mytime,sif.time>=mytime],[gmin(sif.dhigh-vrange,tlow),gmin(sif.dhigh-vrange2,tlow)])
    #tlow = np.select([sif.time<1330,sif.time>=1330],[gmin(sif.dhigh-vrange,tlow),tlow])
    #tlow = np.select([tlow<=rollx(sif.dlow)+vbreak,1],[tlow,gmin(tlow,ldmid-60)])
    #tlow = np.select([tlow>ldmid-60,tlow<=ldmid-60],[rollx(sif.dlow),tlow])
    #tlow = np.select([gand(sif.time<1330,rollx(sif.dhigh-sif.dlow)<vrange+vbreak),sif.time>0],[sif.dhigh-vrange,tlow])
    #tlow = np.select([sif.time<1330,sif.time>0],[gmin(tlow,sif.dhigh-vrange),tlow])
    #tlow = np.select([rollx(sif.dhigh-sif.dlow)<vrange+vbreak,sif.time>0],[sif.dhigh-vrange,tlow])
    #tlow = np.select([gand(sif.time<1330,sif.dhigh-sif.dlow<vrange+vbreak),gand(sif.time<1330,sif.dhigh-sif.dlow>vrange+vbreak),sif.time>1330],[sif.dhigh-vrange,tlow,gmin(sif.dhigh-350,tlow)])
    #tlow = gmin(sif.dhigh-vrange,tlow)
    #tlow = gmin(sif.dhigh-400,tlow)

    #tlow = np.select([gand(tlow>ldmid-60,tlow>rollx(sif.dlow)+vbreak),gor(tlow<=ldmid-60,tlow==rollx(sif.dlow)+vbreak)],[ldmid-60,tlow])

    #mysup = gand(sif.high > opend + 90)
    mysup = gand(sif.high > sif.dlow+160)
    #sss = dsum(mysup,sif.iday)
    sss = extend(mysup,60)

    signal = gand(
            cross(tlow,sif.low)<0,
            #sif.low < tlow,
            gor(tlow<ldmid-90),#,tlow==rollx(sif.dlow)+vbreak),
            #sif.time > 915,
            #rollx(sif.ma13) < rollx(sif.ma30),
            sss < 1,
            #sif.dhigh - sif.low > 150,
        )
    return np.select([signal],[gmin(sif.open,tlow)],0)    #避免跳空情况，如果跳空且小于突破点，就以跳空价进入

def mll2z(sif,length=80,vbreak=20):
    #使用最低点
    tlow = rollx(tmin(sif.low,length)+vbreak,1)
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    #ldmid = dnext((sif.highd+gmin(sif.closed,sif.opend))/2,sif.close,sif.i_cofd)
    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)            
    #highd = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)            
    #ldmid = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)        
    #ldmid = dnext(sif.highd,sif.close,sif.i_cofd)        
    #ldmid = dnext((sif.highd+sif.closed)/2,sif.close,sif.i_cofd)    
    ldrange = dnext(sif.highd-sif.lowd,sif.close,sif.i_cofd) 
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd) 
    
    ldatr30 = dnext(sif.atr30,sif.close,sif.i_cof30)
    ldatr = dnext(sif.atrd,sif.close,sif.i_cofd)
    
    xatrd = dnext(sif.xatrd,sif.close,sif.i_cofd)

    #bhigh = gmax(ldclose,sif.dhigh)
    bhigh = sif.dhigh

    vrange = ldatr *2/3 / XBASE
    #vrange = ldatr *1/2 / XBASE
    #vrange = ldatr / XBASE
    #vrange2 = ldatr /2/ XBASE

    #vrange = np.select([vrange<500],[vrange],500)
    vrange = gmin(vrange,ldclose/66)    #vrange不能超过太大
    vmid = ldatr *1/8/XBASE
    #vmid = 60

    #tlow = gmin(tlow,ldmid-32)
    
    #tlow = np.select([sif.time<1330,sif.time>0],[sif.dhigh-vrange,tlow])    
    #tlow = np.select([sif.time<1330,sif.time>=1330],[gmin(bhigh-vrange,tlow),tlow])
    tlow = np.select([sif.time<1325,sif.time>=1325],[gmin(bhigh-vrange,tlow),tlow])    
    #tlow = gmin(sif.dhigh-vrange,tlow)
    
    #mysup = gand(sif.high > sif.dlow+ldatr/2/XBASE)
    mysup = gand(sif.high > sif.dlow+ldatr/2/XBASE)
    #sss = dsum(mysup,sif.iday)
    sss = extend(mysup,60)

    signal = gand(
            cross(tlow,sif.low)<0,
            #sif.low < tlow,
            gor(tlow<ldmid-vmid,tlow==rollx(sif.dlow)+vbreak),
            #tlow<ldmid-vmid,
            #tlow < ldmid-vmid,
            sif.time > 915,
            #rollx(sif.ma13) < rollx(sif.ma30),
            rollx(ma(sif.high,13)) < rollx(ma(sif.high,30)),
            rollx(sif.xatr)<2000,
            rollx(sif.xatr30x)<10000,
            #sss < 1,
            #sif.dhigh - tlow > 120,  
        )
    #signal = gand(msum(signal,10) > 1,signal)
    
    return np.select([signal],[gmin(sif.open,tlow)],0)    #避免跳空情况，如果跳空且小于突破点，就以跳空价进入


def mll2v(sif,length=80,vbreak=10):
    #使用最低点
    tlow = rollx(tmin(sif.low,length)+vbreak,1)
    #print tlow[-270:]
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    #ldmid = dnext((sif.highd+gmin(sif.closed,sif.opend))/2,sif.close,sif.i_cofd)
    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)            
    #highd = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)            
    #ldmid = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)        
    #ldmid = dnext(sif.highd,sif.close,sif.i_cofd)        
    #ldmid = dnext((sif.highd+sif.closed)/2,sif.close,sif.i_cofd)    
    ldrange = dnext(sif.highd-sif.lowd,sif.close,sif.i_cofd) 
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd) 
    
    ldatr30 = dnext(sif.atr30,sif.close,sif.i_cof30)
    ldatr = dnext(sif.atrd,sif.close,sif.i_cofd)
    
    xatrd = dnext(sif.xatrd,sif.close,sif.i_cofd)/100
    #bhigh = gmax(ldclose,sif.dhigh)
    bhigh = sif.dhigh

    #vwave = dnext(ma(sif.dhigh-sif.dlow,30),sif.close,sif.i_cofd)
    vwave = dnext(ma(sif.highd-sif.lowd,3),sif.close,sif.i_cofd)

    #vwave = xatrd
    #print vwave[-270:]
    #vrange = vwave * 5/2
    #vrange = vwave * 4/3
    #vrange2 = vwave * 2/3

    vrange = vwave * 2/3
    vrange2 = vwave * 1/2

    #vrange = vwave * 5/3
    #vrange2 = vwave * 4/3

    #print vrange[-270:],vrange2[-270:]

    #vrange = np.select([vrange<500],[vrange],500)
    #vrange = gmin(vrange,ldclose/66)    #vrange不能超过太大
    #vrange = gmin(vrange,opend/66)    #vrange不能超过太大
    #vrange2 = gmin(vrange2,opend/66)    #vrange不能超过太大
    #vrange = gmin(vrange,opend/30)    #vrange不能超过太大
    #vrange2 = gmin(vrange2,opend/30)    #vrange不能超过太大
    #vrange = opend/66
    #vmid = ldatr *1/8/XBASE
    vmid = 60
    #vmid = (opend +250)/ 500

    #tlow = gmin(tlow,ldmid-32)
    
    drange = rollx(sif.dhigh - sif.dlow)

    tlimit = 1325
    #tlimit = 1400
    #tlow = np.select([sif.time<1330,sif.time>0],[sif.dhigh-vrange,tlow])    
    #tlow = np.select([sif.time<1330,sif.time>=1330],[gmin(bhigh-vrange,tlow),tlow])
    
    #tlow = np.select([sif.time<tlimit,sif.time>=tlimit],[gmin(bhigh-vrange,tlow),tlow])    
    #tlow = np.select([gand(sif.time<tlimit,drange<vrange)],[gmin(bhigh-vrange,tlow)],tlow)  #时间大于tlimit或振幅大于vrange,则以现有分钟均线为准
    tlow = np.select([gand(sif.time<tlimit,drange<vrange),gand(sif.time>tlimit,drange<vrange2)],[gmin(bhigh-vrange,tlow),gmin(bhigh-vrange2,tlow)],tlow)   #时间大于tlimit或振幅大于vrange,则以现有分钟均线为准

    #print vwave[-30:],tlow[-30:]
    #print (bhigh-vrange)[-270:]
    #print tlow[-270:]

    #tlow = gmin(bhigh-vrange,tlow)
    #tlow = gmin(sif.dhigh-vrange,tlow)
    
    #mysup = gand(sif.high > sif.dlow+ldatr/2/XBASE)
    #mysup = gand(sif.high > sif.dlow+ldatr/2/XBASE)
    #sss = dsum(mysup,sif.iday)
    #sss = extend(mysup,60)

    signal = gand(
            cross(tlow,sif.low)<0,
            #sif.low < tlow,
            #gor(tlow<ldmid-vmid,tlow==rollx(sif.dlow)+vbreak),
            tlow < ldmid - vmid,
            rollx(sif.close,3) < tlow * 10050/10000,
            #rollx(sif.close,1) < tlow * 10030/10000,
            #rollx(sif.high) < tlow * 10030/10000,
            #tlow<ldmid-vmid,
            #tlow < ldmid-vmid,
            sif.time > 915,
            #rollx(sif.ma13) < rollx(sif.ma30),
            rollx(ma(sif.high,13)) < rollx(ma(sif.high,30)),
            rollx(sif.xatr)<2000,
            rollx(sif.xatr30x)<10000,
            #sss < 1,
            sif.dhigh - tlow < opend/33,   #不能跌太多
            #sif.dhigh - tlow > 120,  
        )
    #signal = gand(msum(signal,10) > 1,signal)
    
    return np.select([signal],[gmin(sif.open,tlow)],0)    #避免跳空情况，如果跳空且小于突破点，就以跳空价进入

def mll2z0(sif,length=80,vbreak=20):
    #使用最低点, 第二次突破
    tlow = rollx(tmin(sif.low,length)+vbreak,1)
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    #ldmid = dnext((sif.highd+gmin(sif.closed,sif.opend))/2,sif.close,sif.i_cofd)
    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)            
    #highd = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)            
    #ldmid = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)        
    #ldmid = dnext(sif.highd,sif.close,sif.i_cofd)        
    #ldmid = dnext((sif.highd+sif.closed)/2,sif.close,sif.i_cofd)    
    ldrange = dnext(sif.highd-sif.lowd,sif.close,sif.i_cofd) 
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd) 
    
    ldatr30 = dnext(sif.atr30,sif.close,sif.i_cof30)
    ldatr = dnext(sif.atrd,sif.close,sif.i_cofd)
    
    xatrd = dnext(sif.xatrd,sif.close,sif.i_cofd)

    #bhigh = gmax(ldclose,sif.dhigh)
    bhigh = sif.dhigh

    vrange = ldatr *2/3 / XBASE
    #vrange = ldatr / XBASE
    #vrange2 = ldatr /2/ XBASE

    #vrange = np.select([vrange<500],[vrange],500)
    vrange = gmin(vrange,ldclose/66)    #vrange不能超过太大
    vmid = ldatr *1/8/XBASE
    #vmid = 60

    #tlow = gmin(tlow,ldmid-32)
    
    #tlow = np.select([sif.time<1330,sif.time>0],[sif.dhigh-vrange,tlow])    
    tlow = np.select([sif.time<1330,sif.time>=1330],[gmin(bhigh-vrange,tlow),tlow])
    #tlow = gmin(sif.dhigh-vrange,tlow)
    

    signal = gand(
            cross(tlow,sif.low)<0,
            #sif.low < tlow,
            gor(tlow<ldmid-vmid,tlow==rollx(sif.dlow)+vbreak),
            #tlow<ldmid-vmid,
            #tlow < ldmid-vmid,
            sif.time > 915,
            #rollx(sif.ma13) < rollx(sif.ma30),
            rollx(ma(sif.high,13)) < rollx(ma(sif.high,30)),
            rollx(sif.xatr)<2000,
            rollx(sif.xatr30x)<10000,
        )
    signal = gand(msum(signal,10) > 1,signal)

    return np.select([signal],[gmin(sif.open,tlow)],0)    #避免跳空情况，如果跳空且小于突破点，就以跳空价进入


def mll2z2(sif,length=80,vbreak=20):
    '''
        用实体大小的倒数做过滤
    '''
    #使用最低点
    tlow = rollx(tmin(sif.low,length)+vbreak,1)
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    #ldmid = dnext((sif.highd+gmin(sif.closed,sif.opend))/2,sif.close,sif.i_cofd)
    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)            
    #highd = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)            
    #ldmid = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)        
    #ldmid = dnext(sif.highd,sif.close,sif.i_cofd)        
    #ldmid = dnext((sif.highd+sif.closed)/2,sif.close,sif.i_cofd)    
    ldrange = dnext(sif.highd-sif.lowd,sif.close,sif.i_cofd) 
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd) 
    
    ldatr30 = dnext(sif.atr30,sif.close,sif.i_cof30)
    ldatr = dnext(sif.atrd,sif.close,sif.i_cofd)
    
    xatrd = dnext(sif.xatrd,sif.close,sif.i_cofd)

    #bhigh = gmax(ldclose,sif.dhigh)
    bhigh = sif.dhigh

    vrange = ldatr *2/3 / XBASE
    #vrange = ldatr / XBASE
    #vrange2 = ldatr /2/ XBASE

    #vrange = np.select([vrange<500],[vrange],500)
    vrange = gmin(vrange,ldclose/66)    #vrange不能超过太大
    vmid = ldatr *1/8/XBASE
    #vmid = 60

    #tlow = gmin(tlow,ldmid-32)
    
    #tlow = np.select([sif.time<1330,sif.time>0],[sif.dhigh-vrange,tlow])    
    tlow = np.select([sif.time<1330,sif.time>=1330],[gmin(bhigh-vrange,tlow),tlow])
    #tlow = gmin(sif.dhigh-vrange,tlow)
    
    ldrange2 = 100000 / (sif.highd-sif.lowd)
    lrange2 = dnext(nma(ldrange2,10),sif.close,sif.i_cofd)

    signal = gand(
            cross(tlow,sif.low)<0,
            #sif.low < tlow,
            gor(tlow<ldmid-vmid,tlow==rollx(sif.dlow)+vbreak),
            #tlow < ldmid-vmid,
            sif.time > 915,
            #rollx(sif.ma13) < rollx(sif.ma30),
            rollx(ma(sif.high,13)) < rollx(ma(sif.high,30)),
            rollx(sif.xatr)<2000,
            rollx(sif.xatr30x)<10000,
            lrange2 > 90,
        )
    return np.select([signal],[gmin(sif.open,tlow)],0)    #避免跳空情况，如果跳空且小于突破点，就以跳空价进入


def mll2e(sif,length=75,vbreak=20,vrange=350):
    #使用最低点
    #ldmid = dnext((sif.highd+gmin(sif.closed,sif.opend))/2,sif.close,sif.i_cofd)
    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)            
    #highd = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)            
    #ldmid = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)        
    #ldmid = dnext(sif.highd,sif.close,sif.i_cofd)        
    #ldmid = dnext((sif.highd+sif.closed)/2,sif.close,sif.i_cofd)    
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd) 


    #tlow = gmin(tlow,ldmid-32)
    
    #tlow = np.select([sif.time<1330,sif.time>0],[sif.dhigh-vrange,tlow])    
    #tlow = np.select([sif.time<1330,sif.time>=1330],[gmin(sif.dhigh-vrange,tlow),tlow])
    tlow = sif.dhigh-vrange
    #tlow = np.select([sif.time<1330,sif.time>0],[gmin(tlow,sif.dhigh-vrange),tlow])
    #tlow = np.select([sif.dhigh-sif.dlow<vrange+vbreak,sif.time>0],[sif.dhigh-vrange,tlow])
    #tlow = np.select([gand(sif.time<1330,sif.dhigh-sif.dlow<vrange+vbreak),gand(sif.time<1330,sif.dhigh-sif.dlow>vrange+vbreak),sif.time>1330],[sif.dhigh-vrange,tlow,gmin(sif.dhigh-350,tlow)])
    #tlow = gmin(sif.dhigh-vrange,tlow)
    #tlow = gmin(sif.dhigh-400,tlow)

    signal = gand(
            #sif.time>1029,
            cross(tlow,sif.low)<0,
            sif.time < 1330,
            #rollx(sif.dhigh - sif.dlow) < vrange+vbreak,
            #strend2(sif.low) <= 0,
            #sif.low < tlow,
            #tlow < rollx(sif.dhigh + sif.dlow)/2, #+ sif.dlow
            #tlow < ldhigh-10,  #比昨日最高价低才允许做空
            #tlow < ldmid-30,#rollx(sif.xatr)*2/XBASE,  #比前2天高点中点低才允许做空
            #gor(tlow < ldmid-30,gand(sif.time>1330,tlow<opend)),#加上1330条件后，有助于减少回撤
            #gor(tlow < ldmid-30,gand(sif.time>1330,tlow==rollx(sif.dlow)+vbreak)),  #1330之后tlow同时创新低时可绕过ldmid-30条件
            gor(tlow<ldmid-60,tlow==rollx(sif.dlow)+vbreak),
            #tlow < sif.dmid,
            #rollx(sif.dhigh - sif.dlow) > vrange, 
            #gor(sif.time>=1330,rollx(sif.dhigh-sif.dlow)>320),
            rollx(sif.close,2) - tlow < 150,
            sif.time > 915,
        )
    return np.select([signal],[gmin(sif.open,tlow)],0)    #避免跳空情况，如果跳空且小于突破点，就以跳空价进入


def mll2w(sif,length=75,vbreak=20,vrange=350):
    #使用最低点
    tlow = rollx(tmin(sif.low,length)+vbreak,1)
    #ldhigh = dnext(sif.highd,sif.close,sif.i_cofd)
    #ldmid = dnext((sif.highd+gmin(sif.closed,sif.opend))/2,sif.close,sif.i_cofd)
    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)            
    #highd = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)            
    #ldmid = dnext(gmax(sif.highd,rollx(sif.highd)),sif.close,sif.i_cofd)        
    #ldmid = dnext(sif.highd,sif.close,sif.i_cofd)        
    #ldmid = dnext((sif.highd+sif.closed)/2,sif.close,sif.i_cofd)    
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd) 


    #tlow = gmin(tlow,ldmid-32)
    
    #tlow = np.select([sif.time<1330,sif.time>0],[sif.dhigh-vrange,tlow])    
    #tlow = np.select([sif.time<1330,sif.time>=1330],[gmin(sif.dhigh-vrange,tlow),tlow])
    #tlow = np.select([gand(sif.time<1330,sif.dhigh-sif.dlow<vrange+vbreak),sif.time>0],[sif.dhigh-vrange,tlow])
    #tlow = np.select([sif.time<1330,sif.time>0],[gmin(tlow,sif.dhigh-vrange),tlow])
    #tlow = np.select([sif.dhigh-sif.dlow<vrange+vbreak,sif.time>0],[sif.dhigh-vrange,tlow])
    #tlow = np.select([gand(sif.time<1330,sif.dhigh-sif.dlow<vrange+vbreak),gand(sif.time<1330,sif.dhigh-sif.dlow>vrange+vbreak),sif.time>1330],[sif.dhigh-vrange,tlow,gmin(sif.dhigh-350,tlow)])
    #tlow = gmin(sif.dhigh-vrange,tlow)
    #tlow = gmin(sif.dhigh-400,tlow)

    signal = gand(
            #sif.time>1029,
            cross(tlow,sif.low)<0,
            sif.time >= 1330,
            #gor(sif.time >= 1330),rollx(sif.dhigh-sif.dlow) >= vrange+vbreak),
            gor(tlow<ldmid-60,tlow==rollx(sif.dlow)+vbreak),
            #tlow < sif.dmid,
            #rollx(sif.dhigh - sif.dlow) > vrange, 
            #gor(sif.time>=1330,rollx(sif.dhigh-sif.dlow)>320),
            rollx(sif.close,2) - tlow < 150,
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


def mfilterx(sif):
    return gand(sif.time > 1015,sif.time<1326)

#主要时段
#shbreak_mll2 = SXFuncA(fstate=sdown,fsignal=mll2,fwave=nx2000X,ffilter=mfilter2)    #优于nll
#shbreak_mll2 = SXFuncA(fstate=gofilter,fsignal=mll2,fwave=nx2000X,ffilter=mfilter2)    #优于nll
shbreak_mll2 = SXFuncA(fstate=gofilter,fsignal=mll2,fwave=nx2000X,ffilter=nfilter2)    #1000-1445

#shbreak_mll2 = SXFuncA(fstate=gofilter,fsignal=mll2,fwave=gofilter,ffilter=nfilter2)    #1000-1445

#shbreak_mll2 = SXFuncA(fstate=sdown,fsignal=mll2,fwave=nx2000X,ffilter=efilter)    #优于nll
shbreak_mll2.name = u'日内75分钟向下突破'

shbreak_mll2n = SXFuncA(fstate=gofilter,fsignal=mll2n,fwave=nx2000X,ffilter=mfilter2)    #优于nll
#shbreak_mll2n = SXFuncA(fstate=sdown,fsignal=mll2n,fwave=gofilter,ffilter=efilter)    #优于nll
shbreak_mll2n.name = u'日内75分钟向下突破n'

shbreak_mll2r = SXFuncA(fstate=gofilter,fsignal=mll2r,fwave=nx2000X,ffilter=mfilter2)    #优于nll
#shbreak_mll2r = SXFuncA(fstate=sdown,fsignal=mll2r,fwave=gofilter,ffilter=efilter)    #优于nll
shbreak_mll2r.name = u'日内75分钟向下突破n'

#shbreak_mll2z = SXFuncA(fstate=sdown,fsignal=mll2z,fwave=gofilter,ffilter=nfilter3)    #优于nll
shbreak_mll2z = SXFuncA(fstate=gofilter,fsignal=mll2z,fwave=gofilter,ffilter=nfilter3)    #优于nll
#shbreak_mll2z = SXFuncA(fstate=sdown,fsignal=mll2z,fwave=gofilter,ffilter=efilter)    #优于nll
shbreak_mll2z.name = u'日内75分钟向下突破z'

shbreak_mll2z2 = SXFuncA(fstate=sdown,fsignal=mll2z2,fwave=gofilter,ffilter=nfilter3)    #优于nll
shbreak_mll2z2.name = u'日内75分钟向下突破z2'

shbreak_mll2v = SXFuncA(fstate=gofilter,fsignal=mll2v,fwave=gofilter,ffilter=nfilter3)    #优于nll
#shbreak_mll2v = SXFuncA(fstate=gofilter,fsignal=mll2v,fwave=gofilter,ffilter=nfilter3)    #优于nll
#shbreak_mll2v = SXFuncA(fstate=sdown,fsignal=mll2v,fwave=gofilter,ffilter=efilter)    #优于nll
shbreak_mll2v.name = u'日内75分钟向下突破v'

shbreak_mll2t = SXFuncA(fstate=gofilter,fsignal=mll2t,fwave=gofilter,ffilter=nfilter3)    #优于nll
#shbreak_mll2t = SXFuncA(fstate=sdown,fsignal=mll2t,fwave=gofilter,ffilter=efilter)    #优于nll
shbreak_mll2t.name = u'日内75分钟向下突破t'

shbreak_mll2_e = SXFuncA(fstate=gofilter,fsignal=fcustom(mll2,vrange=250),fwave=gofilter,ffilter=emfilter3)    #貌似无用
shbreak_mll2_e.name = u'日内75分钟向下突破e'    

shbreak_mll2m = SXFuncA(fstate=sdown,fsignal=mll2,fwave=nx2000X,ffilter=mfilterx)    #优于nll
shbreak_mll2m.stop_closer = utrade.atr5_ustop_T

shbreak_mll2_k = SXFuncA(fstate=gofilter,fsignal=mll2,fwave=nx2500X,ffilter=mfilterk)  ##主要时段
shbreak_mll2_k.name = u'日内向下突破新低'
shbreak_mll2_k.stop_closer = utrade.atr5_ustop_X4

shbreak_mll2e = SXFuncD1(fstate=sdown,fsignal=mll2e,fwave=nx2000X,ffilter=mfilter2)    #优于nll
shbreak_mll2e.name = u'日内75分钟向下突破e'

shbreak_mll2w = SXFuncA(fstate=sdown,fsignal=mll2w,fwave=nx2000X,ffilter=mfilter2)    #优于nll
shbreak_mll2w.name = u'日内75分钟向下突破w'

shbreak_mll_30 = SXFuncA(fstate=sdown,fsignal=fcustom(mll2,length=30),fwave=nx2000X,ffilter=nfilter)    #优于nll
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


hbreak2t = [hbreak_nhht,shbreak_mll2t]  #没啥用

##下跌采用75分钟的底部+2, 上涨采用日顶部+3(均在10:30-14:30)
hbreak = [shbreak_mll2,break_nhh]  #利润比较好
#hbreak2 = [shbreak_mll2,hbreak_nhh,hbreak_nhh_e]  #这个最大回撤最小      #####################采用此个
hbreak2 = [shbreak_mll2,hbreak_nhh]#,hbreak_nhh_e]  #这个最大回撤最小      #####################采用此个

hbreak2v = [shbreak_mll2v,hbreak_nhhv]#,hbreak_nhh_e]  #这个去除了对特定过滤幅度值的依赖, 次数减少18%,收益增加2%;


hbreak3 = [hbreak_nhh,shbreak_mll2]#,hbreak_nhh_e]#

d1_hbreak = [dhbreak_nhh,dshbreak_mll2]

break2z = [shbreak_nllz,hbreak_nhhz]

hbreak2n = [shbreak_mll2n,hbreak_nhhn]  #建议采用这个,效率很高


hbreak2z = [shbreak_mll2z,hbreak_nhhz]  #超过12点后趴下

hbreak2z2 = [shbreak_mll2z2,hbreak_nhhz2]  #超过12点后趴下

hbreak_rll = BXFuncA(fstate=gofilter,fsignal=rll,fwave=nx2000X,ffilter=nfilter)    
hbreak_rll.name = u''
hbreak_rll.stop_closer = utrade.vstop_8_42

###单边
def _srise(sif,n1=5,n2=19):
    mh = gmax(tmax(sif.high,n1),rollx(sif.close,n1))
    ml = gmin(tmin(sif.low,n1),rollx(sif.close,n1))
    th = gand(  #向上单边
            sif.high > rollx(mh),
            sif.low < rollx(ml,n1),
        )
    tl = gand(  #向下单边
            sif.high > rollx(mh,-n1),
            sif.low < rollx(ml),
        )

    hn1 = np.zeros_like(sif.high)
    hn1[np.where(tl)] = tmax(sif.high[np.where(tl)],n2)
    exhn1 = extend2next(hn1)

    thl = np.select([th,tl],[1,-1],default=0)

    exthl = extend2next(thl)  #最近的一次单边信号
    tdis = distance(thl)    #当前日距信号日的距离

    tl_high = np.select([tl],[sif.high],default=0)
    
    signal = gand(
                exthl == 1,
                tdis > n1,#因为n1是偷看期   
                #sif.close > rollx(tmax(tl_high,n2),n1),
                sif.close > exhn1,
            )
    return signal
srise = BXFuncA(fstate=gofilter,fsignal=_srise,fwave=gofilter,ffilter=mfilter3)
srise.name = u'向上单边突破'
srise.stop_closer = utrade.atr5_ustop_TU

def _srise2(sif,n1=5,n2=1):
    mh = gmax(tmax(sif.high,n1),rollx(sif.close,n1))
    ml = gmin(tmin(sif.low,n1),rollx(sif.close,n1))
    th = gand(  #向上单边
            sif.high > rollx(mh),
            sif.low < rollx(ml,n1),
        )
    tl = gand(  #向下单边
            sif.high > rollx(mh,-n1),
            sif.low < rollx(ml),
        )

    hn1 = np.zeros_like(sif.high)
    hn1[np.where(tl)] = tmax(sif.high[np.where(tl)],n2)
    exhn1 = extend2next(hn1)

    thl = np.select([th,tl],[1,-1],default=0)

    exthl = extend2next(thl)  #最近的一次单边信号
    tdis = distance(thl)    #当前日距信号日的距离

    tl_high = np.select([tl],[sif.high],default=0)

    chl = np.zeros_like(sif.close)
    c = 0
    for i in range(len(thl)):
        if thl[i] == 1:
            c += 1
        elif thl[i] == -1:
            c = 0
        chl[i] = c

    print max(chl)

    signal = gand(
                tdis > n1,#因为n1是偷看期   
                chl > n2,
            )
    return signal
srise2 = BXFuncA(fstate=gofilter,fsignal=_srise2,fwave=gofilter,ffilter=mfilter3)
srise2.name = u'向上单边突破2'
srise2.stop_closer = utrade.atr5_ustop_TA

def _sdown2(sif,n1=5,n2=25):
    mh = gmax(tmax(sif.high,n1),rollx(sif.close,n1))
    ml = gmin(tmin(sif.low,n1),rollx(sif.close,n1))
    th = gand(  #向上单边
            sif.high > rollx(mh),
            sif.low < rollx(ml,n1),
        )
    tl = gand(  #向下单边
            sif.high > rollx(mh,-n1),
            sif.low < rollx(ml),
        )

    hn1 = np.zeros_like(sif.high)
    hn1[np.where(tl)] = tmax(sif.high[np.where(tl)],n2)
    exhn1 = extend2next(hn1)

    thl = np.select([th,tl],[1,-1],default=0)

    exthl = extend2next(thl)  #最近的一次单边信号
    tdis = distance(thl)    #当前日距信号日的距离

    tl_high = np.select([tl],[sif.high],default=0)

    chl = np.zeros_like(sif.close)
    c = 0
    for i in range(len(thl)):
        if thl[i] == -1:
            c += 1
        elif thl[i] == 1:
            c = 0
        chl[i] = c

    signal = gand(
                tdis > n1,#因为n1是偷看期   
                chl > n2,
            )
    return signal
sdown2 = SXFuncA(fstate=gofilter,fsignal=_sdown2,fwave=gofilter,ffilter=mfilter)
sdown2.name = u'向上单边突破2'
sdown2.stop_closer = utrade.atr5_ustop_TV


###中间价突破
def lmx(sif,length=30):#最低价突破中间价,收盘模型
    twave = sif.atr/XBASE*5/2
    #twave = np.select([twave>150],[150],twave)

    tmid =  tmin(sif.low,length)/2 + tmax(sif.high,length)/2 + twave

    signal = gand(
            cross(tmid,sif.low)>0,
            #sif.low > tmid,
            sif.time > 915,
            sif.low > sif.dlow + 300,
            sif.close > sif.dmid,
        )
    return signal    #下一分钟介入
bmx = BXFuncA(fstate=gofilter,fsignal=lmx,fwave=nx2500X,ffilter=mfilter)
bmx.name = u'中间价向上突破'
bmx.stop_closer = utrade.atr5_ustop_V1

def hmx(sif,length=30):#最高价突破中间价,收盘模型
    twave = sif.atr/XBASE*2
    #twave = np.select([twave<50],[50],twave)
    
    tmid =  tmin(sif.low,length)/2 + tmax(sif.high,length)/2 - twave
    signal = gand(
            cross(tmid,sif.high)<0,
            #sif.high < tmid,
            sif.time > 915,
            sif.dhigh-sif.dlow>360,
            sif.dhigh > sif.high + 300,
        )
    return signal    #下一分钟介入
smx = SXFuncA(fstate=sdown,fsignal=hmx,fwave=nx2000X,ffilter=mfilter)
smx.name = u'中间价向下突破'
smx.stop_closer = utrade.atr5_ustop_V1

mxx = [bmx,smx] #又一个独立策略 ############

####改成n分钟高于/低于

def lmx1(sif,length=30):#最低价突破中间价,收盘模型
    twave = sif.atr/XBASE*5/2
    #twave = np.select([twave>150],[150],twave)

    tmid =  tmin(sif.low,length)/2 + tmax(sif.high,length)/2 + twave

    signal = gand(
            sif.low > tmid,
            sif.time > 915,
            sif.low > rollx(sif.dlow) + 300,
            sif.close > rollx(sif.dmid),
        )
    signal = msum(signal,2) == 2
    signal = derepeatc(signal)
    return signal    #下一分钟介入
bmx1 = BXFuncA(fstate=gofilter,fsignal=lmx1,fwave=nx2500X,ffilter=mfilter)
bmx1.name = u'中间价向上突破1'
bmx1.stop_closer = utrade.atr5_ustop_V

def hmx1(sif,length=30):#最高价突破中间价,收盘模型
    twave = sif.atr/XBASE*2
    #twave = np.select([twave<50],[50],twave)
    
    tmid =  tmin(sif.low,length)/2 + tmax(sif.high,length)/2 - twave
    signal = gand(
            sif.high < tmid,
            sif.time > 915,
            rollx(sif.dhigh-sif.dlow)>360,
            sif.dhigh > sif.high + 300,
        )
    signal = msum(signal,4) == 4
    signal = derepeatc(signal)
    return signal    #下一分钟介入
smx1 = SXFuncA(fstate=sdown,fsignal=hmx1,fwave=nx2000X,ffilter=mfilter)
smx1.name = u'中间价向下突破1'
smx1.stop_closer = utrade.atr5_ustop_V

mxx1 = [bmx1,smx1]  #一个有点意思的独立策略, 不错,########


def lmx2(sif,length=30):#最高价突破中间价(5周期前),突破模型
    twave = sif.atr/XBASE*5/2
    #twave = np.select([twave>150],[150],twave)

    tmid =  tmin(sif.low,length)/2 + tmax(sif.high,length)/2 + twave

    bline = rollx(tmid,5)

    signal = gand(
            cross(bline,sif.high)>0,
            #sif.low > tmid,
            sif.time > 915,
            rollx(sif.low) > sif.dlow + 300,
            rollx(sif.close) > sif.dmid,
        )
    return np.select([signal>0],[gmax(sif.open,bline)],0)
bmx2 = BXFuncA(fstate=gofilter,fsignal=lmx2,fwave=nx2500X,ffilter=mfilter)
bmx2.name = u'中间价向上突破2'
bmx2.stop_closer = utrade.atr5_ustop_V1

def hmx2(sif,length=30):#最低价突破中间价(3周期前),突破模型
    twave = sif.atr/XBASE*2
    #twave = np.select([twave<50],[50],twave)
    
    tmid =  tmin(sif.low,length)/2 + tmax(sif.high,length)/2 - twave

    bline = rollx(tmid,5)

    signal = gand(
            cross(bline,sif.low)<0,
            #sif.high < tmid,
            sif.time > 915,
            sif.dhigh-sif.dlow>360,
            sif.dhigh > rollx(sif.high) + 300,
        )
    return np.select([signal>0],[gmin(sif.open,bline)],0)
smx2 = SXFuncA(fstate=sdown,fsignal=hmx2,fwave=nx2000X,ffilter=mfilter)
smx2.name = u'中间价向下突破2'
smx2.stop_closer = utrade.atr5_ustop_V1

mxx2 = [bmx2,smx2]  #突破模型，也还可以，不如收盘模型，但能确保成交

####ema通道突破
def uema(sif,length=20):#
    twave = sif.atr/XBASE * 6/2
    #twave = np.select([twave>150],[150],twave)

    tmid = cexpma(sif.high,length)

    tbreak = tmid + twave

    bline = rollx(tbreak,1)

    cmid = cross(rollx(tmid),sif.low)>0
    mcmid = msum(cmid,2)

    signal = gand(
            cross(bline,sif.high)>0,
            #mcmid > 0,
            sif.time > 915,
            #rollx(sif.low) > sif.dlow + 150,
        )
    return np.select([signal>0],[gmax(sif.open,bline)],0)
bema = BXFuncA(fstate=gofilter,fsignal=uema,fwave=nx2500X,ffilter=nfilter)
bema.name = u'ema通道向上突破'
bema.stop_closer = utrade.atr5_ustop_V

def dema(sif,length=30):#
    twave = sif.atr/XBASE*2
    #twave = np.select([twave<50],[50],twave)
    
    tmid =  tmin(sif.low,length)/2 + tmax(sif.high,length)/2 - twave
    signal = gand(
            cross(tmid,sif.high)<0,
            #sif.high < tmid,
            sif.time > 915,
            sif.dhigh-sif.dlow>360,
            sif.dhigh > rollx(sif.high) + 300,
        )
    return signal    #下一分钟介入
sema = SXFuncA(fstate=sdown,fsignal=dema,fwave=nx2000X,ffilter=mfilter)
sema.name = u'ema通道向下突破'
sema.stop_closer = utrade.atr5_ustop_V1

ema = [bema,sema]

###中间通道突破
def _bxchannel(sif,length=20):#
    twave = sif.atr/XBASE * 3
    #twave = np.select([twave>150],[150],twave)

    tmid = (tmax(sif.high,length) + tmin(sif.low,length))/2

    tbreak = tmid + twave

    bline = rollx(tbreak,1)

    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd) + 30

    bline = gmax(ldopen,bline)

    signal = gand(
            cross(bline,sif.high)>0,
            #bline > gmax(ldopen,sif.dmid) ,
            sif.time > 915,
            sif.dhigh > sif.dlow + 300,
        )
    return np.select([signal>0],[gmax(sif.open,bline)],0)

def _bxchannel2(sif,length=20):#
    twave = sif.atr/XBASE * 3
    #twave = np.select([twave>150],[150],twave)

    tmid = (tmax(sif.high,length) + tmin(sif.low,length))/2

    tbreak = tmid + twave


    bline = rollx(tbreak,1)
 
    treverse = tmid - twave
 
    breverse = rollx(treverse,1)

    sreverse = gand(
                sif.low < breverse,
            )
    
    sreverse = derepeatc(sreverse)

    mreverse = msum(sreverse,60)

    sfollow = gand(
                sif.high > bline,
            )

    sfollow = derepeatc(sfollow)

    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd) + 30

    bline = gmax(ldopen,bline)

    signal = gand(
            cross(bline,sif.high)>0,
            #bline > gmax(ldopen,sif.dmid) ,
            sif.time > 915,
            sif.dhigh > sif.dlow + 300,
            mreverse < 1,
            rollx(sif.xatr) < 1600,
            sif.xatr30x < 10000,
        )
    return np.select([signal>0],[gmax(sif.open,bline)],0)

bxchannel = BXFuncA(fstate=sdown,fsignal=_bxchannel,fwave=nx2000X,ffilter=nfilter2)
bxchannel.name = u'中间通道向上突破'
bxchannel.stop_closer = utrade.atr5_ustop_V7

bxchannel2 = BXFuncA(fstate=gofilter,fsignal=_bxchannel2,fwave=gofilter,ffilter=mfilter)
bxchannel2.name = u'中间通道向上突破2'
bxchannel2.stop_closer = utrade.atr5_ustop_V


def _sxchannel(sif,length=20):#
    twave = sif.atr/XBASE * 7/2

    tmid = (tmax(sif.high,length) + tmin(sif.low,length))/2

    tbreak = tmid - twave

    bline = rollx(tbreak,1)
    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    

    signal = gand(
            cross(bline,sif.low)<0,
            #mcmid > 0,
            sif.time > 915,
            sif.dhigh > sif.dlow + 300,
            bline < ldmid - 30,
        )
    return np.select([signal>0],[gmin(sif.open,bline)],0)
sxchannel = SXFuncA(fstate=sdown,fsignal=_sxchannel,fwave=nx2000X,ffilter=nfilter2)
sxchannel.name = u'中间通道向下突破'
sxchannel.stop_closer = utrade.atr5_ustop_V7

def _sxchannel2(sif,length=20):#
    twave = sif.atr/XBASE * 7/2

    tmid = (tmax(sif.high,length) + tmin(sif.low,length))/2

    tbreak = tmid - twave

    bline = rollx(tbreak,1)
    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    
    
    treverse = tmid + twave
 
    breverse = rollx(treverse,1)

    sreverse = gand(
                sif.high > breverse,
            )
    
    sreverse = derepeatc(sreverse)

    mreverse = msum(sreverse,60)

    signal = gand(
            cross(bline,sif.low)<0,
            #mcmid > 0,
            sif.time > 915,
            sif.dhigh > sif.dlow + 300,
            bline < ldmid - 30,
            mreverse < 1,
        )
    
    

    return np.select([signal>0],[gmin(sif.open,bline)],0)
sxchannel2 = SXFuncA(fstate=sdown,fsignal=_sxchannel2,fwave=nx2000X,ffilter=nfilter2)
sxchannel2.name = u'中间通道向下突破'
sxchannel2.stop_closer = utrade.atr5_ustop_V7


xchannel = [bxchannel,sxchannel]    #####一对非常好的备用策略


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
            sif.time>915,
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
    ldlow = dnext(sif.lowd,sif.close,sif.i_cofd) - 30
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd)        
    signal = gand(
            sif.low < ldlow ,  
            rollx(gmax(sif.dhigh,ldclose) - sif.dlow) > 200,
            #rollx(sif.dhigh - sif.dlow) > 200,
            sif.time < 1331,
            sif.time> 915,
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

dbreaks = SXFuncD1(fstate=sdown,fsignal=brd,fwave=nx2000X,ffilter=nfilter)
dbreaksh = SXFuncD1(fstate=gofilter,fsignal=brdh,fwave=nx2500X,ffilter=efilter)
dbreaks.name = u'突破前日低点'
dbreaks.lastupdate = 20101213
dbreaks.stop_closer = utrade.atr5_ustop_TA


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

'''
dbreak暂时停用
dbreak系列，每天多空都只取第一次
    开仓:
        做多: 1.当前最高<昨日高点+6(即还未大幅突破过)
              2.开仓点为 high > 昨日最高点
              3.今日高点-今日低点和昨日收盘的低者 > 20点
              4. xatr<2500,xatr30x<10000
        做空: 1.开仓点为 low < 昨日最低-2处
              2.今日高点和昨日收盘的高者-今日低点的低者 > 20点              
              3. xatr<2500,xatr30x<10000
              4. t120<180
    平仓:
        止损为6，保本为8. 30分钟后如果盈利大于10点，则把止损拉到盈利8点或更多处
    工作时段:
        买多:[D2,1330] #第二分钟开始
        做空:[D2,1400] #第二分钟开始

'''

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
            sif.time > 944,
            sif.time < 1445,
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
            sif.time > 944,
            sif.time < 1445,
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
            sif.time > 944,
            sif.time < 1445,
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

erange1 = [berangeu,seranged2]

###失败振荡
def _ugsv(sif):
    d_wave = np.select([sif.closed < sif.opend],[sif.highd-sif.opend],[0])
    id_gsv = np.where(d_wave>0)
    d_gsv = np.zeros_like(sif.closed)
    d_gsv[id_gsv] = ma(d_wave[id_gsv],22)
    d_gsv = extend2next(d_gsv)

    gsv = dnext(d_gsv,sif.close,sif.i_cofd)
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)    

    bline = ldopen + gsv * 5/2
    signal = gand(
            cross(bline,sif.high)>0,
            #rollx(sif.dhigh - gmin(sif.dlow,ldclose)) > 200,
            #rollx(sif.dhigh - sif.dlow) > 200,
            sif.time > 1014,
            sif.time < 1416,
            #ldc1 < ldc2,
            #sif.time < 1430,
            #rollx(sif.xatr>600),
        )
    return np.select([signal],[gmax(sif.open,bline)],0)    #避免跳空情况，如果跳空且大于突破点，就以最低价进入

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

ugsv = BXFunc(fstate=gofilter,fsignal=_ugsv,fwave=gofilter,ffilter=gofilter)
ugsv.name = u'gsv振荡突破向上'
ugsv.lastupdate = 20110110
ugsv.stop_closer = utrade.atr5_ustop_V1


sfwave = SXFuncD1(fstate=gofilter,fsignal=dfwave,fwave=gofilter,ffilter=gofilter)
sfwave.name = u'振荡突破向下'
sfwave.lastupdate = 20110110
sfwave.stop_closer = utrade.atr5_ustop_V1

fwave = [bfwave,sfwave]

lwilliams = erange #+ fwave  #叠加反效果， 单独的以erange为好. 稳定性达到0.37

for x in lwilliams:
    x.stop_closer = utrade.atr5_ustop_T9

#erange以每日一次失败为限

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

def mfilterx(sif):
    return gand(sif.time > 1015,sif.time<1435)

srebound3m = SXFuncD1(fstate=sdown,fsignal=drebound3,fwave=nx2500X,ffilter=mfilterx)
srebound3m.name = u'向下反弹3m'
srebound3m.lastupdate = 20110115
srebound3m.stop_closer = utrade.atr5_ustop_TV1


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

'''
rebound2的早盘动作:#暂时停止. 次数比较少
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
'''

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

def uxbreak1u(sif):
    '''
        向上突破, 震荡模型
    '''
    phh,pll = calc_lh(sif,plen=6)

    sll = extend2next(ssub(pll))
    shh = extend2next(ssub(phh))

    lhh = extend2next(phh)
    lll = extend2next(pll)

    tp = lhh 

    ldmid = dnext(sif.highd/2+rollx(sif.highd)/2,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)        

    signal = gand(
                cross(tp,sif.high)>0,
                rollx(strend2(sif.high))>0,
                sif.time>915,   #915会有跳空
                tp >= rollx(sif.dlow) + 150,
                lhh>lll+120,
            )

    return np.select([signal],[gmax(sif.open,tp)],0)

def dxbreak1u(sif):
    '''
        向下突破,震荡模型
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

    tp = lll+20

    ldmid = dnext(sif.highd/2+rollx(sif.highd)/2,sif.close,sif.i_cofd)    
    opend = dnext(sif.opend,sif.open,sif.i_oofd)        

    signal = gand(
                cross(tp,sif.low)<0,
                rollx(sif.s30)<0,
                rollx(sif.sdiff30x)<0,
                rollx(sif.diff1)<0,
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

bxbreak1u = BXFunc(fstate=gofilter,fsignal=uxbreak1u,fwave=gofilter,ffilter=mfilter2a)
bxbreak1u.name = u'向上突破v'
bxbreak1u.lastupdate = 20110124
bxbreak1u.stop_closer = utrade.atr5_ustop_63

sxbreak1u = SXFunc(fstate=sdown,fsignal=dxbreak1u,fwave=gofilter,ffilter=mfilter2a)
sxbreak1u.name = u'向下突破v'
sxbreak1u.lastupdate = 20110124
sxbreak1u.stop_closer = utrade.atr5_ustop_63

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

xbreak1u = [bxbreak1u,sxbreak1u]    #目前唯一的震荡模型.    ###########################


'''
这个方法正在衰退中，在2011-1中没有捕捉到任何大波动，而且回撤还很大. 需要进一步观察
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
                4. xatr<2500,xatr30x<10000
    平仓:
        止损为4, 保本为8. 
    工作时段:
        [1036,1435]


xbreak1v系列，连续两次突破后，放宽突破的界限，即延缓突破
    顶/底均以6分钟计，即13分钟高/低点
    开仓:
        做多:   1. 穿越上一显著高点. 
                2. 该显著高点小于当日最高20点, 大于最低点20点, 大于显著低点12点
                3. 底部抬高，或者2分钟底部比5分钟底部高. 
                   ###注意，一定要在出现一个5分钟底或2分钟底之后才下条件单. 如果没有出现底部抬高，失败率比较高
                4. 突破前一分钟高点 > 前2分钟高点
                5. 30分钟内连续两次突破后，放宽突破的界限到显著高点+3点
        做空:   暂时观望
    平仓:
        止损为4, 保本为8. 
    工作时段:
        [1036,1435]


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

'''

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
        如果30分钟内已经有失败尝试，则拉高step点
    '''

    #distance = sif.xatr30x * 600/100/ XBASE
    bline1 = sif.dlow + distance

    rbline = rollx(tmin(sif.low,75),1)
    
    t1 = gand(sif.time > 1030,
              cross(bline1,sif.high)>0,
              #bline1 > rbline,
        )
    ms1 = msum(t1,30)

    bline2 = sif.dhigh + distance + 60
    bline = bline1
    bline = np.select([ms1<3,ms1>=3],[bline1,bline2])

    ldlow = dnext(sif.lowd/2+rollx(sif.lowd)/2,sif.close,sif.i_cofd)
    signal1 = gand(
                sif.high > bline,
                bline > rollx(sif.dmid),   #这一条保证了很多. 至少拉开之后，不会被触发
                #bline > rbline,
                #rollx(sif.close) > rollx(sif.close,11),
                rollx(sif.high) > rollx(ma(sif.high,10)),
                #rollx(sif.high) > rollx(sif.high,11),
                rollx(sif.low) > rollx(sif.ma5),
                #sif.dlow > ldlow , 
            )
    return np.select([signal1>0],[gmax(sif.open,bline)],0)

def rbreaks(sif,distance=400):
    '''
        幅度从最高跨越distance点时开仓
    '''
    bline1 = sif.dhigh - distance

    t1 = gand(
              cross(bline1,sif.low)<0,
              #bline1 < rbline,
        )

    ms1 = msum(t1,30)

    bline2 = sif.dhigh - distance - 90

    bline = bline1
    bline = np.select([ms1<3,ms1>=3],[bline1,bline2])

    signal1 = gand(
                sif.low < bline,
                #bline < rbline,
                sif.t120 < 180,
                rollx(sif.low) < rollx(sif.low,31),  
                #rollx(sif.low) < rollx(ma(sif.low,31)),
                rollx(sif.high) < rollx(sif.ma13),
            )
    return np.select([signal1>0],[gmin(sif.open,bline)],0)

def rbreakb2(sif,distance=250):
    '''
        幅度从最低跨越distance点时开仓
        如果30分钟内已经有失败尝试，则拉高step点
    '''

    ldatr = dnext(sif.atrd,sif.close,sif.i_cofd)

    ldclose = dnext(sif.closed,sif.close,sif.i_cofd)
    #distance = ldclose / 80 - ldatr/XBASE/100
    distance = ldclose / 80

    
    bline1 = sif.dlow + distance

    rbline = rollx(tmin(sif.low,75),1)
    
    t1 = gand(sif.time > 1030,
              cross(bline1,sif.high)>0,
              #bline1 > rbline,
        )
    ms1 = msum(t1,30)

    bline2 = sif.dhigh + distance + 60
    bline = bline1
    bline = np.select([ms1<3,ms1>=3],[bline1,bline2])

    ldlow = dnext(sif.lowd/2+rollx(sif.lowd)/2,sif.close,sif.i_cofd)

    #mysdown = gand(sif.low < sif.dhigh-400)
    mysdown = gand(sif.low < sif.dhigh - ldclose/75) 
    #mysdown = derepeatc(mysdown)
    #sss = dsum(mysdown,sif.iday)
    sss = extend(mysdown,80)
    
    signal1 = gand(
                sif.high > bline,
                bline > rollx(sif.dmid),   #这一条保证了很多. 至少拉开之后，不会被触发
                #bline > rbline,
                #rollx(sif.close) > rollx(sif.close,11),
                rollx(sif.high) > rollx(ma(sif.high,10)),
                #rollx(sif.high) > rollx(sif.high,11),
                rollx(sif.low) > rollx(sif.ma5),
                #sif.dlow > ldlow , 
                sss<1,
            )
    return np.select([signal1>0],[gmax(sif.open,bline)],0)

def rbreaks2(sif,distance=400):
    '''
        幅度从最高跨越distance点时开仓
    '''
    ldatr = dnext(sif.atrd,sif.close,sif.i_cofd)

    ldclose = dnext(sif.closed,sif.close,sif.i_cofd)
    #distance = ldclose / 1000 * 1000/ 75 
    distance = ldclose / 75 
    #distance = sif.atr30x * 3 / XBASE

    bline1 = sif.dhigh - distance

    t1 = gand(
              cross(bline1,sif.low)<0,
              #bline1 < rbline,
        )

    ms1 = msum(t1,30)

    bline2 = sif.dhigh - distance - 90

    bline = bline1
    #bline = np.select([ms1<3,ms1>=3],[bline1,bline2])

    #ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)        

    #mysup = gand(sif.high > sif.dlow+160)
    mysup = gand(sif.high > sif.dlow + sif.dlow/ 12000* 80)
    
    #sss = dsum(mysup,sif.iday)
    sss = extend(mysup,60)

    signal1 = gand(
                sif.low < bline,
                rollx(sif.high) < rollx(sif.ma13),
                sss<1,
            )
    return np.select([signal1>0],[gmin(sif.open,bline)],0)

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


brbreak = BXFunc(fstate=gofilter,fsignal=rbreakb,fwave=nx2000X,ffilter=mfilter1400)
brbreak.name = u'幅度向上突破25'
brbreak.lastupdate = 20110106
brbreak.stop_closer = utrade.atr5_ustop_V1

srbreak = SXFunc(fstate=gofilter,fsignal=rbreaks,fwave=nx2000X,ffilter=mfilter1430)
srbreak.name = u'幅度向下突破40'
srbreak.lastupdate = 20110106
srbreak.stop_closer = utrade.atr5_ustop_V1

brbreak2 = BXFunc(fstate=gofilter,fsignal=rbreakb2,fwave=nx2000X,ffilter=mfilter1400)
brbreak2.name = u'幅度向上突破25'
brbreak2.lastupdate = 20110106
brbreak2.stop_closer = utrade.atr5_ustop_V1


srbreak2 = SXFunc(fstate=gofilter,fsignal=rbreaks2,fwave=nx2000X,ffilter=nfilter3)
srbreak2.name = u'幅度向下突破40'
srbreak2.lastupdate = 20110106
srbreak2.stop_closer = utrade.atr5_ustop_V1


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

rbreak2 = [brbreak2,srbreak2]  #这是一个很好的备选主方案, 无遗漏系统.远远优于rbreak

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

amm = [bamm,samm]   #单独可以作为主策略. 201101开始退化

amm1 = [bamm1,samm1]    #每天10:31之后根据开盘价，当前价和中点关系开仓. 并用到缩量. 单独非常有效，叠加无效

amm2 = [bamm2,samm2]    #每天11:01定时开仓，方向根据最近30分钟运行方向. 其中samm2很强

amm3 = [bamm3,samm3]    #单个也可作为备用主策略. 201001开始退化

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
sk5a.stop_closer = utrade.vstop_10_42

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
                rollx(sif.high5) < rollx(sif.high5,2),
                rollx(sif.high5,2) < rollx(sif.high5,3),
                strend2(ma(sif.low5,5))<0,
              )

    delay = 5
    bline = dnext_cover(sif.low5,sif.close,sif.i_cof5,3)
    signal1 = gand(
            cross(bline,sif.low)<0,
           )

    signal2 = dnext_cover(signal5,sif.close,sif.i_cof5,delay)
    
    signal = gand(signal1,
                signal2,
            )
    return np.select([signal],[gmin(sif.open,bline)],0)


sk15d = SXFunc(fstate=gofilter,fsignal=k5rd,fwave=gofilter,ffilter=nfilter2)
sk15d.name = u'k5向上突破'
sk15d.lastupdate = 20101224
sk15d.stop_closer = utrade.vstop_10_42

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
def muc(sif):   #macd下降途中上叉放空
    signal = gand(
            cross(sif.dea1,sif.diff1)>0,
            sif.s15 < 0,
            sif.diff1 < 0,
            rollx(sif.high) < rollx(sif.dlow) + 120,
            rollx(strend2(sif.ma13))<0,
            rollx(strend2(sif.ma60))<0,
            rollx(strend2(sif.ma120))<0,
          )
    return signal
smuc = SXFuncA(fstate=sdown,fsignal=muc,fwave=nx2000X,ffilter=mfilter2)
smuc.name = u'下降趋势中macd上叉放空'
smuc.lastupdate = 20110116
smuc.stop_closer = utrade.atr5_ustop_TV

def mdc(sif):   #上升过程中下叉开多
    signal = gand(
            cross(sif.dea1,sif.diff1)<0,
            sif.s30 > 0,
            sif.diff1 > 0,
            rollx(strend2(sif.ma13))>0,
            rollx(strend2(sif.ma60))>0,
            rollx(strend2(sif.ma120))>0,
          )
    return signal
bmdc = BXFuncA(fstate=sdown,fsignal=mdc,fwave=nx2500X,ffilter=mfilter2)
bmdc.name = u'上升趋势中macd下叉做多'
bmdc.lastupdate = 20110116
bmdc.stop_closer = utrade.atr5_ustop_T

mc = [smuc,bmdc]

def muc0(sif):
    signal = gand(
            cross(cached_zeros(len(sif.close)),sif.diff1)<0,
            sif.s15 < 0,
            rollx(sif.high) < rollx(sif.dlow) + 150,
            rollx(strend2(sif.ma13))<0,
            rollx(strend2(sif.ma60))<0,
            rollx(strend2(sif.ma120))<0,
          )
    return signal
smuc0 = SXFuncA(fstate=sdown,fsignal=muc0,fwave=nx2500X,ffilter=mfilter)
smuc0.name = u'macd上叉0放空'
smuc0.lastupdate = 20110116
smuc0.stop_closer = utrade.atr5_ustop_TV

def mdc0(sif):
    signal = gand(
            cross(cached_zeros(len(sif.close)),sif.diff1)>0,
            sif.s30 > 0,
            sif.sdiff5x>=0,
          )
    return signal
bmdc0 = BXFuncA(fstate=gofilter,fsignal=mdc0,fwave=nx2500X,ffilter=mfilter)
bmdc0.name = u'macd上叉做多'
bmdc0.lastupdate = 20110116
bmdc0.stop_closer = utrade.atr5_ustop_TV

mc = [bmdc,smuc,smuc0,bmdc0]    #一种简单的基于macd的系统

###rsi
def ruc(sif):
    signal = gand(
            cross(sif.rsi19,sif.rsi7)<0,
            sif.s30 < 0,
            rollx(strend2(sif.ma120))<0,
          )
    return signal
sruc = SXFuncA(fstate=sdown,fsignal=ruc,fwave=nx2500X,ffilter=mfilter)
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
brdc.stop_closer = utrade.atr5_ustop_TV

rc = [sruc,brdc]    #不如macd系统

def rsi_long_x2(sif,sopened=None,rshort=7,rlong=19):
    '''
        比较妥当的是 7/19和13/41参数,其中前者明显优于后者
    '''

    #signal = cross(sif.dea1,sif.diff1)>0
    rshort = 7
    rlong = 19
    rsia = rsi2(sif.close,rshort)   #7,19/13,41
    rsib = rsi2(sif.close,rlong)
    signal = cross(rsib,rsia)>0    

    signal = gand(signal
              ,sif.rm_trend>0
              ,sif.ltrend>0               
              ,sif.ms>0
              ,sif.ma3>sif.ma13  
              ,sif.ma7> sif.ma30              
              ,sif.s30>0
            )

    return signal
brsi2 = BXFuncA(fstate=gofilter,fsignal=rsi_long_x2,fwave=gofilter,ffilter=nfilter2)
brsi2.name = u'rsi上叉做多'
brsi2.lastupdate = 20110311
brsi2.stop_closer = utrade.atr5_ustop_TT

###min5
def _umin5(sif):
    exp1 = cexpma(sif.close5,3)
    exp2 = cexpma(sif.close5,54)    #日周期
    signal5 = gand(
                cross(exp2,exp1)>0,
                sif.diff5x >= 0,
                strend2(sif.diff5x-sif.dea5x)>0,
                #sif.diff5x-sif.dea5x>0,
            )
    signal = np.zeros_like(sif.close)
    signal[sif.i_cof5] = signal5
    signal = gand(
                signal,
                strend2(sif.ma270)>0,
                #strend2(sif.ma13-sif.ma30)>0,
                #sif.close < sif.dhigh - 150,
           )
    return signal
umin5 = BXFunc(fstate=gofilter,fsignal=_umin5,fwave=gofilter,ffilter=mfilter)
umin5.name = u'min5做多'
umin5.lastupdate = 20110612
umin5.stop_closer = utrade.atr5_ustop_TV

def _dmin5(sif):
    exp1 = cexpma(sif.close5,3)
    exp2 = cexpma(sif.close5,54)    #日周期
    signal5 = gand(
                cross(exp2,exp1)<0,
                #sif.diff5x <= 0,
            )
    signal = np.zeros_like(sif.close)
    signal[sif.i_cof5] = signal5
    signal = gand(
                signal,
                strend2(sif.ma30)<0,
                #sif.close < sif.dhigh - 150,
           )
    return signal
dmin5 = SXFunc(fstate=gofilter,fsignal=_dmin5,fwave=gofilter,ffilter=mfilter)
dmin5.name = u'min5做空'
dmin5.lastupdate = 20110612
dmin5.stop_closer = utrade.atr5_ustop_TA

#发散
def _ufs(sif):
    signal = gand(
            sif.ma5 > sif.ma13,
            sif.ma13 > sif.ma30,
            sif.ma30 > sif.ma120,
            strend2(sif.ma30)>0,
            strend2(sif.ma120)>0,
            strend2(sif.ma270)>0,
            strend2(sif.ma3-sif.ma13)>0,
            strend2(sif.ma13-sif.ma120)>0,
           )
    return signal
ufs = BXFunc(fstate=gofilter,fsignal=_ufs,fwave=gofilter,ffilter=mfilter)
ufs.name = u'min5做多'
ufs.lastupdate = 20110612
ufs.stop_closer = utrade.atr5_ustop_TU


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
#sxudd.stop_closer = utrade.atr5_ustop_V1
sxudd.stop_closer = utrade.vstop_10_42
 
def xud_short_2(sif,sopened=None):
    '''
    '''
    mxc = xc0c(sif.open10,sif.close10,sif.high10,sif.low10,13) < 0

    signal = np.zeros_like(sif.close)
    signal[sif.i_cof10] = mxc

    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    

    signal = gand(signal,
            sif.xatr30x<6600,
            #sif.s5<0,
            sif.s30>0,
            strend2(sif.ma270)>0,
            #strend2(sif.ma13)<0,
            sif.ma13 < sif.ma30,
            sif.dhigh - sif.dlow < (sif.dlow + 500)/66,#500,
           )

    return signal * xud_short_2.direction
xud_short_2.direction = XSELL
xud_short_2.priority = 2400
xud_short_2.stop_closer = utrade.vstop_10_42        
#xud_short_2.stop_closer = utrade.atr5_ustop_TV

def _xud_short(sif,sopened=None):
    '''
    '''
    #mxc = xc0c(sif.open10,sif.close10,sif.high10,sif.low10,13) < 0
    #signal = np.zeros_like(sif.close)
    #signal[sif.i_cof10] = mxc

    mxc0 = xc0c(sif.open10,sif.close10,sif.high10,sif.low10,13) < 0

    signal = dnext_cover(mxc0,sif.close,sif.i_cof10,2)


    ldmid = dnext((sif.highd+rollx(sif.highd))/2,sif.close,sif.i_cofd)    

    signal = gand(signal,
            sif.xatr30x<6600,
            #sif.s5<0,
            sif.s30>0,
            strend2(sif.ma270)>0,
            #strend2(sif.ma13)<0,
            sif.ma13 < sif.ma30,
            sif.dhigh - sif.dlow < sif.dlow/66,#500,
           )

    return signal
xud_short = SXFunc(fstate=gofilter,fsignal=_xud_short,fwave=gofilter,ffilter=efilter2)
xud_short.name = u'xud放空'
xud_short.lastupdate = 20110804
#xud_short.stop_closer = utrade.atr5_ustop_V1
#xud_short.stop_closer = utrade.atr5_ustop_TV
xud_short.stop_closer = utrade.vstop_10_42      #一个很好的候选


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
buma = BXFunc(fstate=sdown,fsignal=uma,fwave=nx2000X,ffilter=mfilter00)
buma.name = u'最低价穿越ma5'
buma.lastupdate = 20110116
buma.stop_closer = utrade.atr5_ustop_V1

def dma(sif):
    #ldclose = dnext(sif.closed,sif.close,sif.i_cofd)
    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)        
    bline = gmin(rollx(sif.dma),ldopen-60)#,(sif.dhigh+sif.dlow)/2)
    signal = gand(
            #cross(sif.ma5,sif.high)<0,
            cross(bline,sif.low)<0,
            #rollx(sif.sdma) < 0,
            #strend2(sif.ma5)<0,
            #sif.s30 < 0,
            #sif.close < gmax(sif.dhigh,ldclose) - 400,
            #sif.close < sif.dhigh - 400,
            #sif.ma5 < sif.ma13,
            #sif.ma13 < sif.ma30,
           )
    return np.select([signal],[gmin(sif.open,bline)],0) 

sdma = SXFunc(fstate=sdown,fsignal=dma,fwave=nx2000X,ffilter=efilter)
sdma.name = u'最高价穿越ma5'
sdma.lastupdate = 20110116
#sdma.stop_closer = utrade.atr5_ustop_V1
sdma.stop_closer = utrade.vstop_10_42

tma = [buma,sdma]   #这个系统更加强,是个不错的主策略, 简单. 稳定性=0.36
'''
tma系列. ma与5分钟均线的关系    #####
    开仓:
        做多: 1.开仓点为最低价大于1分钟线的5周期均线，次分钟开盘开仓
              2.要求均线和最低价都比上一分钟高
              3.s30>0. 即30分钟macd的3周期线的趋势向上
              4. 该分钟收盘价 > 最低价 + 50点
              5. 1分钟的5周期均线>13周期均线，30周期均线>270周期均线
              6. xatr<2000,xatr30x<10000
              7. t120<180
        做空: 1.开仓点为最高价小于1分钟线的5周期均线，次分钟开盘开仓
              2.要求均线比上一分钟低
              3. 该分钟收盘价 < 当日最高和昨日收盘中高者 - 40点
              5. 1分钟的5周期均线<13周期均线，13周期均线<30周期均线
              6. xatr<2000,xatr30x<10000
              7. t120<180
    平仓:
        止损为4，保本为8. 
    工作时段:
        买多:[1001,1435]
        做空:[1001,1435]

'''

###ma2
def uma2(sif):
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd)
    bline = sif.ma30
    signal = gand(
            rollx(sif.close,4) <= rollx(bline,4),
            rollx(sif.close,3) > rollx(bline,3),
            rollx(sif.close,2) > rollx(bline,2),
            rollx(sif.close) > rollx(bline),
            sif.close > bline,
            strend2(bline)>0,
            sif.ma30 > sif.ma135,
            strend2(sif.ma270)>0,
           )
    return signal
buma2 = BXFuncD2(fstate=sdown,fsignal=uma2,fwave=nx2000X,ffilter=mfilter)
buma2.name = u'向上穿越ma且站住3分钟'
buma2.lastupdate = 20110203
buma2.stop_closer = utrade.atr5_ustop_V1

def dma2(sif):
    ldclose = dnext(sif.closed,sif.close,sif.i_cofd)
    bline = sif.ma30
    signal = gand(
            rollx(sif.close,3) >= rollx(bline,3),
            rollx(sif.close,2) < rollx(bline,2),
            rollx(sif.close) < rollx(bline),
            sif.close < bline,
            strend2(bline)<0,
            sif.ma30 < sif.ma135,
            sif.ma7 < sif.ma30,
            sif.s15<0,
           )
    return signal
sdma2 = SXFuncD2(fstate=sdown,fsignal=dma2,fwave=nx2000X,ffilter=mfilter)
sdma2.name = u'向下穿越ma且站住3分钟'
sdma2.lastupdate = 20110203
sdma2.stop_closer = utrade.atr5_ustop_V1

tma2 = [buma2,sdma2]    #另一个还可以的ma策略,12点后趴下


####添加老系统
wxxx = [xds,xdds3,k5_d3b,xuub,K1_DDD1,K1_UUX,K1_RU,Z5_P2,xmacd3s,xup01,ua_fa,FA_15_120,K1_DVB,K1_DDUU,K1_DVBR]

wok = [xds,xdds3]

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

##老系统的重新实现,都是分钟收盘后出信号
def _k3d3(sif): #k3d3的实现
    xfilter = gand(
                sif.s30 < 0,
                sif.t120 < 0,
                sif.r60 < 0,
                sif.r13<0,
            )
    xsignal3 = gand(
                sif.close3 < sif.open3,
                rollx(sif.close3) < rollx(sif.open3),
                rollx(sif.high3)<rollx(sif.high3,2),
                sif.diff3x < sif.dea3x,
                sif.low3 == tmin(sif.low3,3),            
            )
    xsignal = dnext_cover(xsignal3,sif.close,sif.i_cof3,1)
    xwave = gand(
             sif.mxatr > rollx(sif.mxatr,270),  #xatr在放大中,这个条件在单个很有用，合并时被处理掉             
             sif.mxadtr > sif.mxautr,
        )
    signal = gand(xfilter,xsignal,xwave)
    return signal

k3d3 = SXFuncA(fstate=gofilter,fsignal=_k3d3,fwave=gofilter,ffilter=mfilter2)    #这个单个效益好，叠加无作用
k3d3.name = u'k3d3'
k3d3.stop_closer = utrade.atr5_ustop_TA

def _ydds2(sif): #xdds2的实现
    xfilter = gand(
                sif.sdiff30x<0,
                sif.s30<0,
                sif.s3<0,
                sif.r120<0,
                sif.r13<0,
            )
    xsignal = gand(
                sif.close < rollx(tmin(sif.low,120))+60,
                rollx(sif.close,1) < rollx(sif.close,2),
            )
    xwave = gand(
                sif.xatr<2000,
            )
    signal = gand(xfilter,xsignal,xwave)
    return signal

ydds2 = SXFuncA(fstate=gofilter,fsignal=_ydds2,fwave=gofilter,ffilter=mfilter3)    #这个单个效益巨好
ydds2.name = u'ydds2'
ydds2.stop_closer = utrade.atr5_ustop_TA
ydds2.stop_closer = utrade.vstop_8_42

def _ydds3(sif): #xdds3的实现
    xfilter = gand(
                sif.s30 < 0,
                sif.s5<0,
                sif.t120 < 0,
                sif.r60 < 0,
                strend2(sif.ma60)<0,
            )
    xsignal = gand(
                rollx(sif.close,1) < rollx(sif.close,2),
                sif.close < rollx(sif.close),
                sif.low < rollx(sif.low,2),
                sif.high < rollx(sif.high,2),
            )
    xwave = gand(
             #sif.mxadtr30x > sif.mxautr30x,
             #sif.xatr30x < sif.mxatr30x,
             #sif.xatr<3600,
             #sif.xatr30x<12000,
             sif.mxatr > rollx(sif.mxatr,270),  #xatr在放大中,这个条件在单个很有用，合并时被处理掉             
             sif.mxadtr > sif.mxautr,
        )
    signal = gand(xfilter,xsignal,xwave)
    return signal

ydds3 = SXFuncA(fstate=gofilter,fsignal=_ydds3,fwave=gofilter,ffilter=mfilter)    #这个单个效益巨好
ydds3.name = u'ydds3'
ydds3.stop_closer = utrade.atr5_ustop_TA
#ydds3.stop_closer = utrade.atr5_ustop_V15

def _ydds4(sif): #xdds4的实现
    xfilter = gand(
                sif.s15< 0,
                sif.s5<0,
                sif.s1<0,
                strend2(sif.ma13 - sif.ma30)<0, #差距扩大中
                sif.r60 < 0,
                sif.t120<0,
            )
    xsignal = gand(
                #rollx(sif.close,1) < rollx(sif.close,2),
                sif.close < rollx(sif.close),
                rollx(sif.close)<rollx(sif.open),
            )
    xwave = gand(
                sif.xatr30x < 10000,
            )
    signal = gand(xfilter,xsignal,xwave)
    return signal

ydds4 = SXFuncA(fstate=gofilter,fsignal=_ydds4,fwave=gofilter,ffilter=mfilter3)    #这个单个效益巨好
ydds4.name = u'ydds4'
ydds4.stop_closer = utrade.atr5_ustop_TA

def _yds(sif): #xds的实现
    xfilter = gand(
                sif.r120<0,
                sif.s3<0,
                sif.r60<0,
        )
    xsignal = gand(
                sif.close < sif.open,
                sif.close < rollx(tmin(sif.low,30)),
                tmax(sif.high,10) > tmax(sif.high,30) - 30
            )
    xwave = gand(
                sif.xatr > sif.mxatr,
                strend2(sif.mxatr30x)<0,
                sif.xatr30x < sif.mxatr30x,
            )
    signal = gand(xfilter,xsignal,xwave)
    return signal

yds = SXFuncA(fstate=gofilter,fsignal=_yds,fwave=gofilter,ffilter=mfilter3)    
yds.name = u'yds'
yds.stop_closer = utrade.atr5_ustop_TA

##最好的空头组合
#best_s = [yds,ydds3]
best_s = [ydds3]

#best_s = [yds,ydds3,shbreak_mll2n]

##其它尝试
def _id_up(sif,sopened=None):
    '''
        内移日次日向上
    '''

 
    sday = gand(sif.highd<rollx(sif.highd),sif.lowd>rollx(sif.lowd))
    #print [(d,s) for d,s in zip(sif.day,sday) if s!=0]

    highd = np.select([sday],[sif.highd+sif.atrd/XBASE/10],default=0)

    #print zip(sif.day,highd,sif.atrd,sif.highd)

    chighd = dnext_cover(highd,sif.close,sif.i_cofd,260) 

    signal = gand(
                cross(chighd,sif.high)>0,
            )

    return signal
id_up = BXFuncA(fstate=gofilter,fsignal=_id_up,fwave=gofilter,ffilter=nfilter2)
id_up.name = u'id_up'
id_up.stop_closer = utrade.atr5_ustop_TV

def _id_down(sif,sopened=None):
    '''
        内移日次日向下
    '''

 
    sday = gand(sif.highd<rollx(sif.highd),sif.lowd>rollx(sif.lowd))
    #print [(d,s) for d,s in zip(sif.day,sday) if s!=0]

    lowd = np.select([sday],[sif.lowd-sif.atrd/XBASE/3],default=0)

    #print zip(sif.day,highd,sif.atrd,sif.highd)

    clowd = dnext_cover(lowd,sif.close,sif.i_cofd,260) 

    signal = gand(
                cross(clowd,sif.low)<0,
            )

    return signal
id_down = SXFuncF1(fstate=gofilter,fsignal=_id_down,fwave=gofilter,ffilter=nfilter2)
id_down.name = u'id_up'
id_down.stop_closer = utrade.atr5_ustop_TV

idx = [id_up,id_down]   #效果足够,次数还不够

##AD
def _ad_up(sif,sopened=None):
    '''
        AD指标
    '''

    sad = (sif.close+sif.close-sif.high-sif.low)*1.0 / (sif.high-sif.low) * sif.vol
    ssad = np.select([sif.high>sif.low],[sad],0)    #被0除则为0

    #lad = msum(ssad,270)
    #lad = ssad.cumsum()
    lad = dsum(ssad,sif.iday)
    mlad2 = ma(lad,45)
    mlad1 = ma(lad,3)

    signal = gand(
                cross(mlad2,mlad1)>0,
                sif.s15>0,
                sif.sdiff5x>sif.sdea5x,
                sif.xatr < 2000,
                sif.diff1>0,
                strend2(sif.ma30)>0,
                sif.r120>1,
            )

    return signal
ad_up = BXFuncA(fstate=gofilter,fsignal=_ad_up,fwave=gofilter,ffilter=mfilter)
ad_up.name = u'id_up'
ad_up.stop_closer = utrade.atr5_ustop_TV

def _ad_down(sif,sopened=None):
    '''
        AD指标
    '''

 
    sad = (sif.close+sif.close-sif.high-sif.low)*1.0 / (sif.high-sif.low) * sif.vol
    ssad = np.select([sif.high>sif.low],[sad],0)    #被0除则为0

    #lad = msum(ssad,270)
    #lad = ssad.cumsum()
    lad = dsum(ssad,sif.iday)
    mlad2 = ma(lad,75)
    mlad1 = ma(lad,1)

    signal = gand(
                cross(mlad2,mlad1)<0,
                sif.s1<0,
                sif.s5<0,
                sif.xatr30x < sif.mxatr30x,
                sif.ma3 < sif.ma13,
            )


    return signal
ad_down = SXFuncA(fstate=gofilter,fsignal=_ad_down,fwave=gofilter,ffilter=nfilter2)
ad_down.name = u'id_down'
ad_down.stop_closer = utrade.atr5_ustop_TV

ad = [ad_up,ad_down]   #合成无增益

##三重滤网
def _tri_up(sif,sopened=None):
    '''
        三重滤网
    '''

    bline = rollx(tmax(sif.high,30),1)

    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)        

    bfilter = gand(
                sif.sdiff10x>sif.sdea10x,#第二重a
                sif.sdiff10x > 0,#第二重b
                sif.dhigh - sif.dlow > 180,
                sif.high > ldopen, 
                sif.r120>0, #第一重
            )

    signal = gand(
                cross(bline,sif.high)>0,#第三重
                rollx(bfilter),
            )

    return np.select([signal],[gmax(sif.open,bline)],0)    #避免跳空情况，如果跳空且大于突破点，就以跳空价进入

tri_up = BXFuncA(fstate=gofilter,fsignal=_tri_up,fwave=gofilter,ffilter=mfilter3)
tri_up.name = u'tri_up'
tri_up.stop_closer = utrade.atr5_ustop_V15

def _tri_down(sif,sopened=None):
    '''
        三重滤网, 向下找不到合适的
    '''

    bline = rollx(tmin(sif.low,45),1)

    ldopen = dnext(sif.opend,sif.close,sif.i_oofd)        

    bfilter = gand(
                sif.sdiff10x < sif.sdea10x,
                sif.dhigh - sif.dlow > 360,
                sif.r60<0,
                strend2(sif.ma30)<0,
            )

    signal = gand(
                cross(bline,sif.low)<0,
                rollx(bfilter),
            )

    return np.select([signal],[gmin(sif.open,bline)],0)    #避免跳空情况，如果跳空且大于突破点，就以跳空价进入

tri_down = SXFuncA(fstate=gofilter,fsignal=_tri_down,fwave=gofilter,ffilter=mfilter)
tri_down.name = u'tri_down'
tri_down.stop_closer = utrade.atr5_ustop_V25

xtri = [tri_up,tri_down]        #一个非常好的候选策略

best_b = [tri_up]

txxx = hbreak2 + txfs

#xxx1 = xbreak1c + hbreak2 + dbreak + exbreak2 + rebound2#+ d1_rebound #+ amm #+ break123c  #此方法每日亏损20点之后趴下装死比较妥当
#xxx1 = xbreak1c + hbreak2 + dbreak + exbreak2 + rebound2#此方法每日亏损20点之后趴下装死比较妥当
#xxx1 = hbreak2 + xbreak1v + rebound3 +dbreak + exbreak2 + rebound2    #此方法每日亏损18点(775)或12点(75)之后趴下装死比较妥当. 关键是保持一致性

#xxx1a = hbreak2 +  dbreak + rebound3 + rebound2#一个独立的策略
xxx1a = hbreak2 #hbreak2 + rebound3 + rebound2#一个独立的策略, 暂时删除dbreak, 增加的收益不够
xxx1a2 = xxx1a + [hbreak_nhh_e]
xxx1b = tma  # 一个不错的候补策略. 和hbreak2+xbreak1v不协调
xxx1c = exbreak2 + xbreak1v #2011-1正在衰退
xxx1d = [bxbreak1v] + rbreak

xxx1 = xxx1a #+ xxx1d    #做空已经足够，补足做多

xxx = d1_xbreak1v + d1_hbreak + dbreak #+ d1_rebound#+break123c# #+ rebound  #此方法每日亏损12点之后趴下装死比较妥当

#xxx2 = xxx +wxfs #+ wxxx
xxx2 = xxx1 

xamm = amm + hbreak2 + rebound    #这是一个非常好的独立策略, 作为候选, 每日亏损9(7+1+1)点之后趴下装死.

rxxx = rbreak_all + edbreak + exbreak #+ rebound #一个很牛的独立策略, 亏损12点后趴下
mrxxx = mrbreak + edbreak +exbreak #+ rebound #一个很牛的独立策略，类似于上

rxxx2 = rbreak + break_xr + xbreak1b #xbreak1b:突破回调系统

xxx3 = dbreak+ xbreak1c + exbreak2 + xbreak1 + rebound2 #也还可以

_xmax = hbreak2n +best_s + best_b #目前的最大

_ymax = hbreak2 + best_s + best_b #目前最稳定


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

>>> pds = utrade.pd2(i00,mds)    #求标准波幅-利润分布
>>> for pd in pds:print pd.end,pd.wins,pd.pwins,pd.losts,pd.plosts
...
0.6 6 338 21 -1593
1 23 4183 42 -3838
1.5 25 8074 9 -366
4 37 22777 0 0
>>> pds = utrade.pd2(i00,mds,[0.4,0.7,1,1.5,4])    #求标准波幅-利润分布
>>> for pd in pds:print pd.end,pd.wins,pd.pwins,pd.losts,pd.plosts
0.4 2 44 3 -254
0.7 8 824 32 -2642
1 19 3653 28 -2535
1.5 25 8074 9 -366
4 37 22777 0 0
##表明波幅<atrd时，总体是在制造润滑, 利润完全来自于波幅/atrd>1的部分
'''



for x in xxx2:
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
#shbreak_mll2.stop_closer = utrade.atr5_ustop_T
#hbreak_nhh.stop_closer = utrade.atr5_ustop_T

#hbreakn是最好的

#shbreak_mll2.stop_closer = utrade.atr5_ustop_TV #_TV

#shbreak_mll2.stop_closer = utrade.atr5_ustop_V25 #这个也不错

#shbreak_mll2.stop_closer = utrade.atr5_ustop_V7

shbreak_mll2.stop_closer = utrade.vstop_10_42


#shbreak_mll2.stop_closer = utrade.vstop_7_42
#shbreak_mll2.stop_closer = utrade.atr5_ustop_V10


#shbreak_mll2.stop_closer = utrade.atr5_ustop_V712

#hbreak_nhh.stop_closer = utrade.atr5_ustop_TA

#hbreak_nhh.stop_closer = utrade.atr5_ustop_V25

#hbreak_nhh.stop_closer = utrade.atr5_ustop_V7

hbreak_nhh.stop_closer = utrade.vstop_10_42


#hbreak_nhh.stop_closer = utrade.vstop_7_42

#hbreak_nhh.stop_closer = utrade.atr5_ustop_V10

#hbreak_nhh.stop_closer = utrade.atr5_ustop_V7

shbreak_mll2n.stop_closer = utrade.atr5_ustop_TV    #最好的
hbreak_nhhn.stop_closer = utrade.atr5_ustop_TA      #最好的

#hbreak_nhhn.stop_closer = utrade.vstop_10_42
#shbreak_mll2n.stop_closer = utrade.vstop_10_42


hbreak_mhhz.stop_closer = utrade.atr5_ustop_TU  #最好的

hbreak_nhhz.stop_closer = utrade.atr5_ustop_TV
shbreak_mll2z.stop_closer = utrade.atr5_ustop_TU
#shbreak_mll2z.stop_closer = utrade.vstop_10_42
#hbreak_nhhz.stop_closer = utrade.vstop_10_42
#hbreak_nhhz.stop_closer = utrade.vstop_10_42
#shbreak_mll2z.stop_closer = utrade.vstop_10_42
hbreak_nhht.stop_closer = utrade.vstop_10_42
shbreak_mll2t.stop_closer = utrade.vstop_10_42

#shbreak_mll2v.stop_closer = utrade.atr5_ustop_TU
shbreak_mll2v.stop_closer = utrade.vstop_10_42
#shbreak_mll2v.stop_closer = utrade.vstop_5_42
#shbreak_mll2v.stop_closer = utrade.atr5_ustop_V7

#hbreak_nhhv.stop_closer = utrade.atr5_ustop_TA
hbreak_nhhv.stop_closer = utrade.vstop_10_42
#hbreak_nhhv.stop_closer = utrade.vstop_5_42
#hbreak_nhhv.stop_closer = utrade.atr5_ustop_V7


#shbreak_mll2z.stop_closer = utrade.atr5_ustop_TA

shbreak_mll2r.stop_closer = utrade.atr5_ustop_TV

srbreak2.stop_closer = utrade.atr5_ustop_TA
brbreak2.stop_closer = utrade.atr5_ustop_TV

hbreak_nhhz2.stop_closer = utrade.atr5_ustop_TV
shbreak_mll2z2.stop_closer = utrade.atr5_ustop_TU

#bx7.stop_closer = utrade.atr5_ustop_T
#sx7.stop_closer = utrade.atr5_ustop_T


#shbreak_mll2z.stop_closer = utrade.step_stop_7
#hbreak_nhhz.stop_closer = utrade.step_stop_7
#shbreak_mll2.stop_closer = utrade.step_stop_7
#hbreak_nhh.stop_closer = utrade.step_stop_7



shbreak_mll2e.stop_closer = utrade.atr5_ustop_T
shbreak_mll2w.stop_closer = utrade.atr5_ustop_T

hbreak_nhh_e.stop_closer = utrade.atr5_ustop_T

break_nhh.stop_closer = utrade.atr5_ustop_T
shbreak_nll2.stop_closer = utrade.atr5_ustop_T

sbreak_nll20.stop_closer = utrade.atr5_ustop_TA
sbreak_nll2.stop_closer = utrade.atr5_ustop_TA


break_nhhx.stop_closer = utrade.atr5_ustop_TB
break_nllx.stop_closer = utrade.atr5_ustop_TB

#break_nhhx.stop_closer = utrade.step_stop_7
#break_nllx.stop_closer = utrade.step_stop_7


break_nhhxm.stop_closer = utrade.atr5_ustop_V1
break_nllxm.stop_closer = utrade.atr5_ustop_V1  #注意，这个是V1,即5个点的止损


bmx.stop_closer = utrade.atr5_ustop_V1
smx.stop_closer = utrade.atr5_ustop_V1

dbreakb.stop_closer = utrade.atr5_ustop_T
dbreaks.stop_closer = utrade.atr5_ustop_T

brebound3.stop_closer = utrade.atr5_ustop_TV1
srebound3.stop_closer = utrade.atr5_ustop_TV1


#########候补序列
bxbreak.stop_closer = utrade.atr5_ustop_V1
sxbreak.stop_closer = utrade.atr5_ustop_V1
bxbreak1.stop_closer = utrade.atr5_ustop_V1
sxbreak1.stop_closer = utrade.atr5_ustop_V1
bxbreak1c.stop_closer = utrade.atr5_ustop_V1
sxbreak1c.stop_closer = utrade.atr5_ustop_V1

#bxbreak1v.stop_closer = utrade.atr5_ustop_V1
bxbreak1v.stop_closer = utrade.atr5_ustop_63
sxbreak1v.stop_closer = utrade.atr5_ustop_V1

ebxbreak2.stop_closer = utrade.atr5_ustop_V1

bxbreakd.stop_closer = utrade.atr5_ustop_V
sxbreakd.stop_closer = utrade.atr5_ustop_V

dhbreak_nhh.stop_closer = utrade.atr5_ustop_V
dshbreak_mll2.stop_closer = utrade.atr5_ustop_V

brebound2.stop_closer = utrade.atr5_ustop_T1
srebound2.stop_closer = utrade.atr5_ustop_T1


brbreak.stop_closer = utrade.atr5_ustop_V1
srbreak.stop_closer = utrade.atr5_ustop_VY

####AMM系列
bamm.stop_closer = utrade.atr5_ustop_V1
samm.stop_closer = utrade.atr5_ustop_V1

####ma系列
sdma.stop_closer = utrade.atr5_ustop_V1
buma.stop_closer = utrade.atr5_ustop_V1

sdma.stop_closer = utrade.vstop_10_42
buma.stop_closer = utrade.vstop_10_42
####震荡模型
bxbreak1u.stop_closer = utrade.atr5_ustop_63
sxbreak1u.stop_closer = utrade.atr5_ustop_63

##其它
for tx in wxxx:
    tx.stop_closer = utrade.atr5_ustop_TV
    tx.stop_closer = utrade.vstop_10_42

#b123b.stop_closer = utrade.atr5_ustop_X2

#for x in dxxx:#
#    x.stop_closer = utrade.atr5_ustop_V

for tx in x1164:
    tx.stop_closer = utrade.atr5_ustop_V7
    tx.stop_closer = utrade.vstop_10_42
    
