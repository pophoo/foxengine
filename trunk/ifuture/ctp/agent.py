#-*- coding:utf-8 -*-
'''
Agent的目的是合并行情和交易API到一个类中进行处理
    把行情和交易分开，从技术角度上来看挺好，但从使用者角度看就有些蛋疼了.
    正常都是根据行情决策

todo:
    1. 打通trade环节
    2. 前期数据的衔接(1分钟,5/30)
    3. 行情数据的整理
    4. trader桩的建立,根据trade桩模拟交易
    5. 中间环境的恢复,如持仓. 
       断点间的撤单--可延后 
    6. 完全模拟交易
    7. 有人值守实盘

    8. 生产环境必须考虑多个行情接入端, 有可能会出现延时情况.

后续工作
    B.1. 合约的自动匹配

##周一提前行动?

##因为流控原因,所有Qry命令都用Command模式?
  不需要,可以忍受1s的延时. 因为行情通过别的来接收  
'''

import time
import logging
import thread

from base import *
from dac import ATR,ATR1,STREND,STREND1,MA,MA1
import hreader

import UserApiStruct as ustruct
import UserApiType as utype
from MdApi import MdApi, MdSpi
from TraderApi import TraderApi, TraderSpi  



#数据定义中唯一一个enum
THOST_TERT_RESTART  = 0
THOST_TERT_RESUME   = 1
THOST_TERT_QUICK    = 2

NFUNC = lambda data:None    #空函数桩

#INSTS = [u'IF1103',u'IF1104']  #必须采用ctp使用的合约名字，内部不做检验
INSTS = [u'IF1103']  #必须采用ctp使用的合约名字，内部不做检验
#建议每跟踪的一个合约都使用一个行情-交易对. 因为行情的接收是阻塞式的,在做处理的时候会延误后面接收的行情
#套利时每一对合约都用一个行情-交易对
#INSTS = [u'IF1102']

#mylock = thread.allocate_lock()


class MdSpiDelegate(MdSpi):
    '''
        将行情信息转发到Agent
        并自行处理杂务
    '''
    logger = logging.getLogger('ctp.MdSpiDelegate')
    
    last_map = {}

    def __init__(self,
            instruments, #合约列表
            broker_id,   #期货公司ID
            investor_id, #投资者ID
            passwd, #口令
            agent,  #实际操作对象
        ):        
        self.instruments = instruments
        self.broker_id =broker_id
        self.investor_id = investor_id
        self.passwd = passwd
        self.agent = agent
        #self.last_map = dict([(id,0) for id in instruments])
        self.last_map.update(dict([(id,0) for id in instruments]))

    def checkErrorRspInfo(self, info):
        if info.ErrorID !=0:
            logger.error(u"ErrorID:%s,ErrorMsg:%s" %(info.ErrorID,info.ErrorMsg))
        return info.ErrorID !=0

    def OnRspError(self, info, RequestId, IsLast):
        self.logger.error(u'requestID:%s,IsLast:%s,info:%s' % (RequestId,IsLast,str(info)))

    def OnFrontDisConnected(self, reason):
        self.logger.info(u'front disconnected,reason:%s' % (reason,))

    def OnHeartBeatWarning(self, time):
        pass

    def OnFrontConnected(self):
        self.logger.info(u'front connected')
        self.user_login(self.broker_id, self.investor_id, self.passwd)

    def user_login(self, broker_id, investor_id, passwd):
        req = ustruct.ReqUserLogin(BrokerID=broker_id, UserID=investor_id, Password=passwd)
        r=self.api.ReqUserLogin(req,self.agent.inc_request_id())

    def OnRspUserLogin(self, userlogin, info, rid, is_last):
        self.logger.info(u'user login,info:%s,rid:%s,is_last:%s' % (info,rid,is_last))
        if is_last and not self.checkErrorRspInfo(info):
            self.logger.info(u"get today's trading day:%s" % repr(self.api.GetTradingDay()))
            self.subscribe_market_data(self.instruments)

    def subscribe_market_data(self, instruments):
        self.api.SubscribeMarketData(instruments)

    def OnRtnDepthMarketData(self, depth_market_data):
        #print depth_market_data.BidPrice1,depth_market_data.BidVolume1,depth_market_data.AskPrice1,depth_market_data.AskVolume1,depth_market_data.LastPrice,depth_market_data.Volume,depth_market_data.UpdateTime,depth_market_data.UpdateMillisec,depth_market_data.InstrumentID
        #print 'on data......\n',
        #with mylock:
        try:
            #mylock.acquire()
            #self.logger.debug(u'获得锁.................,mylock.id=%s' % id(mylock))        
            if depth_market_data.LastPrice > 999999 or depth_market_data.LastPrice < 10:
                logger.warning(u'收到的行情数据有误:%s,LastPrice=:%s' %(depth_market_data.InstrumentID,depth_market_data.LastPrice))
            if depth_market_data.InstrumentID not in self.instruments:
                logger.warning(u'收到未订阅的行情:%s' %(depth_market_data.InstrumentID,))
            #self.logger.debug(u'收到行情:%s,time=%s:%s' %(depth_market_data.InstrumentID,depth_market_data.UpdateTime,depth_market_data.UpdateMillisec))
            dp = depth_market_data
            self.logger.debug(u'收到行情，inst=%s,time=%s，volume=%s,last_volume=%s' % (dp.InstrumentID,dp.UpdateTime,dp.Volume,self.last_map[dp.InstrumentID]))
            if dp.Volume <= self.last_map[dp.InstrumentID]:
                self.logger.debug(u'行情无变化，inst=%s,time=%s，volume=%s,last_volume=%s' % (dp.InstrumentID,dp.UpdateTime,dp.Volume,self.last_map[dp.InstrumentID]))
                return  #行情未变化
            self.last_map[dp.InstrumentID] = dp.Volume
            #mylock.release()   #至此已经去掉重复的数据

            self.logger.debug(u'after modify instrument=%s,lastvolume:%s,curVolume:%s' % (dp.InstrumentID,self.last_map[dp.InstrumentID],dp.Volume))
            #self.logger.debug(u'before loop')
            ctick = self.market_data2tick(depth_market_data)
            self.agent.RtnTick(ctick)
        finally:
            pass
            #mylock.release()   #至此主要工作完成
            #self.logger.debug(u'释放锁.................,mylock.id=%s' % id(mylock))
        

        #self.logger.debug(u'before write md:')
        ff = open(hreader.make_tick_filename(ctick.instrument),'a+')
        #print type(dp.UpdateMillisec),type(dp.OpenInterest),type(dp.Volume),type(dp.BidVolume1)
        #ff.write(u'%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (dp.TradingDay,dp.UpdateTime,dp.UpdateMillisec,dp.OpenInterest,dp.Volume,dp.LastPrice,dp.HighestPrice,dp.LowestPrice,dp.BidPrice1,dp.BidVolume1,dp.AskPrice1,dp.AskVolume1))
        ff.write(u'%(instrument)s,%(date)s,%(min1)s,%(sec)s,%(msec)s,%(holding)s,%(dvolume)s,%(price)s,%(high)s,%(low)s,%(bid_price)s,%(bid_volume)s,%(ask_price)s,%(ask_volume)s\n' % ctick.__dict__)
        ff.close()
        self.logger.debug(u'after write md:')
        #time.sleep(0.3)
        #self.logger.debug(u'after write sleep:')

    def market_data2tick(self,market_data):
        #market_data的格式转换和整理, 交易数据都转换为整数
        rev = BaseObject(instrument = market_data.InstrumentID)
        rev.date = int(market_data.TradingDay)
        rev.min1 = int(market_data.UpdateTime[:2]+market_data.UpdateTime[3:5])
        rev.sec = int(market_data.UpdateTime[-2:])
        rev.msec = int(market_data.UpdateMillisec)
        rev.holding = int(market_data.OpenInterest+0.1)
        rev.dvolume = market_data.Volume
        rev.price = int(market_data.LastPrice*10+0.1)
        rev.high = int(market_data.HighestPrice*10+0.1)
        rev.low = int(market_data.LowestPrice*10+0.1)
        rev.bid_price = int(market_data.BidPrice1*10+0.1)
        rev.bid_volume = market_data.BidVolume1
        rev.ask_price = int(market_data.AskPrice1*10+0.1)
        rev.ask_volume = market_data.AskVolume1
        return rev

class TraderSpiDelegate(TraderSpi):
    '''
        将服务器回应转发到Agent
        并自行处理杂务
    '''
    logger = logging.getLogger('ctp.TraderSpiDelegate')    
    def __init__(self,
            instruments, #合约列表
            broker_id,   #期货公司ID
            investor_id, #投资者ID
            passwd, #口令
            agent,  #实际操作对象
        ):        
        self.instruments = instruments
        self.broker_id =broker_id
        self.investor_id = investor_id
        self.passwd = passwd
        self.agent = agent
        self.agent.set_spi(self)
        self.scur_day = int(time.strftime('%Y%m%d'))
 
    def isRspSuccess(self,RspInfo):
        return RspInfo == None or RspInfo.ErrorID == 0

    ##交易初始化
    def OnFrontConnected(self):
        '''
            当客户端与交易后台建立起通信连接时（还未登录前），该方法被调用。
        '''
        self.logger.info(u'trader front connected')
        self.user_login(self.broker_id, self.investor_id, self.passwd)

    def OnFrontDisconnected(self, nReason):
        self.logger.info(u'trader front disconnected,reason=%s' % (nReason,))

    def user_login(self, broker_id, investor_id, passwd):
        req = ustruct.ReqUserLogin(BrokerID=broker_id, UserID=investor_id, Password=passwd)
        r=self.api.ReqUserLogin(req,self.agent.inc_request_id())

    def OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):
        self.logger.info('trader login')
        self.logger.debug("loggin %s" % str(pRspInfo))
        if not self.isRspSuccess(pRspInfo):
            self.logger.warning(u'trader login failed, errMsg=%s' %(pRspInfo.ErrorMsg,))
            return
        self.agent.login_success(pRspUserLogin.FrontID,pRspUserLogin.SessionID,pRspUserLogin.MaxOrderRef)
        #self.settlementInfoConfirm()
        self.agent.set_trading_day(self.api.GetTradingDay())
        #self.query_settlement_info()
        self.query_settlement_confirm() 

    def OnRspUserLogout(self, pUserLogout, pRspInfo, nRequestID, bIsLast):
        '''登出请求响应'''
        self.logger.info(u'trader logout')

    def resp_common(self,rsp_info,bIsLast,name='默认'):
        #self.logger.debug("resp: %s" % str(rsp_info))
        if not self.isRspSuccess(rsp_info):
            self.logger.info(u"%s失败" % name)
            return -1
        elif bIsLast and self.isRspSuccess(rsp_info):
            self.logger.info(u"%s成功" % name)
            return 1
        else:
            self.logger.info(u"%s结果: 等待数据接收完全..." % name)
            return 0

    def query_settlement_confirm(self):
        '''
            这个基本没用，不如直接确认
            而且需要进一步明确：有史以来第一次确认前查询确认情况还是每天第一次确认查询情况时，返回的响应中
                pSettlementInfoConfirm为空指针. 如果是后者,则建议每日不查询确认情况,或者在generate_struct中对
                CThostFtdcSettlementInfoConfirmField的new_函数进行特殊处理
            CTP写代码的这帮家伙素质太差了，边界条件也不测试，后置断言也不整，空指针乱飞
            2011-3-1 确认每天未确认前查询确认情况时,返回的响应中pSettlementInfoConfirm为空指针
            并且妥善处理空指针之后,仍然有问题,在其中查询结算单无动静
        '''
        req = ustruct.QrySettlementInfoConfirm(BrokerID=self.broker_id,InvestorID=self.investor_id)
        self.api.ReqQrySettlementInfoConfirm(req,self.agent.inc_request_id())

    def query_settlement_info(self):
        #不填日期表示取上一天结算单,并在响应函数中确认
        self.logger.info(u'取上一日结算单信息并确认,BrokerID=%s,investorID=%s' % (self.broker_id,self.investor_id))
        req = ustruct.QrySettlementInfo(BrokerID=self.broker_id,InvestorID=self.investor_id,TradingDay=u'')
        #print req.BrokerID,req.InvestorID,req.TradingDay
        self.api.ReqQrySettlementInfo(req,self.agent.inc_request_id())

    def confirm_settlement_info(self):
        req = ustruct.SettlementInfoConfirm(BrokerID=self.broker_id,InvestorID=self.investor_id)
        self.api.ReqSettlementInfoConfirm(req,self.agent.inc_request_id())

    def OnRspQrySettlementInfo(self, pSettlementInfo, pRspInfo, nRequestID, bIsLast):
        '''请求查询投资者结算信息响应'''
        print u'Rsp 结算单查询'
        if(self.resp_common(pRspInfo,bIsLast,u'结算单查询')>0):
            print u'结算单内容:%s' % pSettlementInfo.Content
            self.logger.info(u'结算单内容:%s' % pSettlementInfo.Content)
            self.confirm_settlement_info()

    def OnRspQrySettlementInfoConfirm(self, pSettlementInfoConfirm, pRspInfo, nRequestID, bIsLast):
        '''请求查询结算信息确认响应'''
        self.logger.debug(u"结算单确认信息查询响应:rspInfo=%s,结算单确认=%s" % (pRspInfo,pSettlementInfoConfirm))
        #self.query_settlement_info()
        if(self.resp_common(pRspInfo,bIsLast,u'结算单确认情况查询')>0):
            if(pSettlementInfoConfirm == None or int(pSettlementInfoConfirm.ConfirmDate) < self.scur_day):
                #其实这个判断是不对的，如果周日对周五的结果进行了确认，那么周一实际上已经不需要再次确认了
                if(pSettlementInfoConfirm != None):
                    self.logger.info(u'最新结算单未确认，需查询后再确认,最后确认时间=%s,scur_day:%s' % (pSettlementInfoConfirm.ConfirmDate,self.scur_day))
                else:
                    self.logger.info(u'结算单确认结果为None')
                time.sleep(1)   #满足1秒一次的查询间隔,避免流控
                self.query_settlement_info()
            else:
                self.logger.info(u'最新结算单已确认，不需再次确认,最后确认时间=%s,scur_day:%s' % (pSettlementInfoConfirm.ConfirmDate,self.scur_day))

    def OnRspSettlementInfoConfirm(self, pSettlementInfoConfirm, pRspInfo, nRequestID, bIsLast):
        '''投资者结算结果确认响应'''
        if(self.resp_common(pRspInfo,bIsLast,u'结算单确认')>0):
            self.logger.info(u'结算单确认时间: %s-%s' %(pSettlementInfoConfirm.ConfirmDate,pSettlementInfoConfirm.ConfirmTime))
        #self.agent.initialize()

    ###交易准备
    def OnRspQryInstrument(self, pInstrument, pRspInfo, nRequestID, bIsLast):
        #如果合约还要靠查才能确定，直接关机走人
        pass

    def OnRspQryInstrumentMarginRate(self, pInstrumentMarginRate, pRspInfo, nRequestID, bIsLast):
        '''
            保证金率回报。返回的必然是绝对值
        '''
        if bIsLast and self.isRspSuccess(pRspInfo):
            agent.rsp_qry_instrument_marginrate(pInstrumentMarginRate)
        else:
            #logging
            pass

    def OnRspQryTradingAccount(self, pTradingAccount, pRspInfo, nRequestID, bIsLast):
        '''
            请求查询资金账户响应
        '''
        print u'查询资金账户响应'
        self.logger.debug(u'资金账户响应:%s' % pTradingAccount)
        if bIsLast and self.isRspSuccess(pRspInfo):
            self.agent.rsp_qry_trading_account(pTradingAccount)
        else:
            #logging
            pass

    def OnRspQryInvestorPosition(self, pInvestorPosition, pRspInfo, nRequestID, bIsLast):
        '''请求查询投资者持仓响应'''
        print u'查询持仓响应',str(pInvestorPosition),str(pRspInfo)
        if bIsLast and self.isRspSuccess(pRspInfo):
            self.agent.rsp_qry_position(pInvestorPosition)
        else:
            #logging
            pass

    def OnRspQryInvestorPositionDetail(self, pInvestorPositionDetail, pRspInfo, nRequestID, bIsLast):
        '''请求查询投资者持仓明细响应'''
        print str(pInvestorPositionDetail)
        if bIsLast and self.isRspSuccess(pRspInfo):
            self.agent.rsp_qry_position_detail(pInvestorPositionDetail)
        else:
            #logging
            pass


    def OnRspError(self, pRspInfo, nRequestID, bIsLast):
        '''错误应答'''
        #logging
        pass

    def OnRspQryOrder(self, pOrder, pRspInfo, nRequestID, bIsLast):
        '''请求查询报单响应'''
        if bIsLast and self.isRspSuccess(pRspInfo):
            self.agent.rsp_qry_order(pOrder)
        else:
            #logging
            pass

    def OnRspQryTrade(self, pTrade, pRspInfo, nRequestID, bIsLast):
        '''请求查询成交响应'''
        if bIsLast and self.isRspSuccess(pRspInfo):
            self.agent.rsp_qry_trade(pTrade)
        else:
            #logging
            pass


    ###交易操作
    def OnRspOrderInsert(self, pInputOrder, pRspInfo, nRequestID, bIsLast):
        '''
            报单未通过参数校验,被CTP拒绝
            正常情况后不应该出现
        '''
        print pRspInfo,nRequestID
        self.logger.warning(u'CTP报单录入错误回报, 正常后不应该出现,rspInfo=%s'%(str(pRspInfo),))
        #self.logger.warning(u'报单校验错误,ErrorID=%s,ErrorMsg=%s,pRspInfo=%s,bIsLast=%s' % (pRspInfo.ErrorID,pRspInfo.ErrorMsg,str(pRspInfo),bIsLast))
        self.agent.rsp_order_insert(pInputOrder.OrderRef,pInputOrder.InstrumentID,pRspInfo.ErrorID,pRspInfo.ErrorMsg)
    
    def OnErrRtnOrderInsert(self, pInputOrder, pRspInfo):
        '''
            交易所报单录入错误回报
            正常情况后不应该出现
            这个回报因为没有request_id,所以没办法对应
        '''
        print u'ERROR Order Insert'
        self.logger.warning(u'交易所报单录入错误回报, 正常后不应该出现,rspInfo=%s'%(str(pRspInfo),))
        self.agent.err_order_insert(pInputOrder.OrderRef,pInputOrder.InstrumentID,pRspInfo.ErrorID,pRspInfo.ErrorMsg)
    
    def OnRtnOrder(self, pOrder):
        ''' 报单通知
            CTP、交易所接受报单
        '''
        self.logger.info(u'报单响应,Order=%s' % str(pOrder))
        if pOrder.OrderStatus == 'a':
            #CTP接受，但未发到交易所
            #print u'CTP接受Order，但未发到交易所, BrokerID=%s,BrokerOrderSeq = %s,TraderID=%s, OrderLocalID=%s' % (pOrder.BrokerID,pOrder.BrokerOrderSeq,pOrder.TraderID,pOrder.OrderLocalID)
            self.logger.info(u'CTP接受Order，但未发到交易所, BrokerID=%s,BrokerOrderSeq = %s,TraderID=%s, OrderLocalID=%s' % (pOrder.BrokerID,pOrder.BrokerOrderSeq,pOrder.TraderID,pOrder.OrderLocalID))
            self.agent.rtn_order_ctp(pOrder)
        else:
            #print u'交易所接受Order,exchangeID=%s,OrderSysID=%s,TraderID=%s, OrderLocalID=%s' % (pOrder.ExchangeID,pOrder.OrderSysID,pOrder.TraderID,pOrder.OrderLocalID)
            self.logger.info(u'交易所接受Order,exchangeID=%s,OrderSysID=%s,TraderID=%s, OrderLocalID=%s' % (pOrder.ExchangeID,pOrder.OrderSysID,pOrder.TraderID,pOrder.OrderLocalID))
            self.agent.rtn_order_exchange(pOrder)

    def OnRtnTrade(self, pTrade):
        '''成交通知'''
        print u'成交通知,BrokerID=%s,BrokerOrderSeq = %s,exchangeID=%s,OrderSysID=%s,TraderID=%s, OrderLocalID=%s' %(pTrade.BrokerID,pTrade.BrokerOrderSeq,pTrade.ExchangeID,pTrade.OrderSysID,pTrade.TraderID,pTrade.OrderLocalID)
        self.logger.info(u'成交回报,Trade=%s' % repr(pTrade))

    def OnRspOrderAction(self, pInputOrderAction, pRspInfo, nRequestID, bIsLast):
        '''
            ctp撤单校验错误
        '''
        self.logger.warning(u'CTP撤单录入错误回报, 正常后不应该出现,rspInfo=%s'%(str(pRspInfo),))
        self.agent.rsp_order_action(pInputOrderAction.OrderRef,pInputOrderAction.InstrumentID,pRspInfo.ErrorID,pRspInfo.ErrorMsg)

    def OnErrRtnOrderAction(self, pOrderAction, pRspInfo):
        ''' 
            交易所撤单操作错误回报
            正常情况后不应该出现
        '''
        self.logger.warning(u'交易所撤单录入错误回报, 可能已经成交,rspInfo=%s'%(str(pRspInfo),))
        self.agent.err_order_action(pOrderAction.OrderRef,pOrderAction.InstrumentID,pRspInfo.ErrorID,pRspInfo.ErrorMsg)


class Agent(object):
    logger = logging.getLogger('ctp.agent')

    def __init__(self,trader,cuser,instruments):
        '''
            trader为交易对象
        '''
        self.trader = trader
        self.cuser = cuser
        self.instruments = instruments
        self.request_id = 1
        self.data_funcs = []  #计算函数集合. 如计算各类指标, 顺序关系非常重要
                              #每一类函数由一对函数组成，.sfunc计算序列用，.func1为动态计算用，只计算当前值
                              #接口为(data), 从data的属性中取数据,并计算另外一些属性
                              #顺序关系非常重要，否则可能会紊乱
        self.strategy_map = {}
        ###交易数据, instrument==>tdata的映射
        #其中tdata.m1/m3/m5/m15/m30/d1为不同周期的数据
        #   tdata.cur_min是当前分钟的行情，包括开盘,最高,最低,当前价格,持仓,累计成交量
        #   tdata.cur_day是当日的行情，包括开盘,最高,最低,当前价格,持仓,累计成交量, 其中最高/最低有两类，一者是tick的当前价集合得到的，一者是tick中的最高/最低价得到的
        self.data = {}    #为合约号==>合约数据的dict
        ###
        self.lastupdate = 0
        self.holding = []   #(合约、策略族、基准价、基准时间、request_id、持仓量、止损价、止损函数)
        self.transited_orders = []    #发出后等待回报的指令, 回报后到holding
        self.queued_orders = []     #因为保证金原因等待发出的指令(合约、策略族、基准价、基准时间(到秒))
        self.front_id = None
        self.session_id = None
        self.order_ref = 1
        self.trading_day = 20110101
        self.scur_day = int(time.strftime('%Y%m%d'))
        #当前资金/持仓
        self.account = 0
        self.position = []


        self.register_data_funcs(
                BaseObject(sfunc=NFUNC,func1=hreader.time_period_switch),    #时间切换函数
                BaseObject(sfunc=ATR,func1=ATR1),
                BaseObject(sfunc=MA,func1=MA1),
                BaseObject(sfunc=STREND,func1=STREND1),
            )

        self.prepare_data_env()

    def set_spi(self,spi):
        self.spi = spi

    def inc_request_id(self):
        self.request_id += 1
        return self.request_id

    def inc_order_ref(self):
        self.order_ref += 1
        return self.order_ref

    def set_trading_day(self,trading_day):
        self.trading_day = trading_day

    def get_trading_day(self):
        return self.trading_day

    def login_success(self,frontID,sessionID,max_order_ref):
        self.front_id = frontID
        self.session_id = sessionID
        self.order_ref = int(max_order_ref)

    def initialize(self):
        '''
            初始化，如保证金率，账户资金等
        '''
        pass

    def prepare_data_env(self):
        '''
            准备数据环境, 如需要的30分钟数据
        '''
        self.data.update(hreader.prepare_data(self.instruments))
        for dinst in self.data.values():
            for dfo in self.data_funcs:
                dfo.sfunc(dinst)
            

    def register_strategy(self,strategys):
        '''
            策略注册. 简单版本，都按照100%用完合约分额计算. 这样，合约的某个策略集合持仓时，其它策略集合就不能再开仓
            strategys是[(合约1,策略集1),(合约2,策略集2)]的对
                其中一个合约可以对应多个策略，一个策略也可以对应多个合约
        '''
        for ins_id,s in strategys:
            if ins_id not in self.strategy_map:
                self.strategy_map[ins_id] = []
            if s not in self.strategy_map[ins_id]:
                self.strategy_map[ins_id].append((s,100)) 

    def cregister_strategy(self,strategys):
        '''
            策略注册，复杂版本
            strategys是[(合约1,策略集合1,手数占比),(合约2,策略集合2,手数占比)]的集合
                其中一个合约可以对应多个策略集合
            策略集合:
                (策略,策略,策略)    其中这些策略可以相互平仓
            手数占比:
                0-100, 表示在该合约允许持仓数中的占比, 百分之一，并取整
        '''
        for ins_id,s,proportion in strategys:
            if ins_id not in self.strategy_map:
                self.strategy_map[ins_id] = []
            self.strategy_map[ins_id].append((s,proportion))    #重复的话就会引发多次下单

    
    def register_data_funcs(self,*funcss):
        for funcs in funcss:
            self.data_funcs.append(funcs)

    ##内务处理
    def fetch_trading_account(self):
        #获取资金帐户
        print u'获取资金帐户..'
        req = ustruct.QryTradingAccount(BrokerID=self.cuser.broker_id, InvestorID=self.cuser.investor_id)
        r=self.trader.ReqQryTradingAccount(req,self.inc_request_id())
        print u'查询资金账户, 函数发出返回值:%s' % r

    def fetch_investor_position(self,instrument_id):
        #获取合约的当前持仓
        print u'获取合约%s的当前持仓..' % (instrument_id,)
        req = ustruct.QryInvestorPosition(BrokerID=self.cuser.broker_id, InvestorID=self.cuser.investor_id,InstrumentID=instrument_id)
        r=self.trader.ReqQryInvestorPosition(req,self.inc_request_id())
        print u'查询持仓, 函数发出返回值:%s' % r
    
    def fetch_investor_position_detail(self,instrument_id):
        #获取合约的当前持仓明细
        print u'获取合约%s的当前持仓..' % (instrument_id,)
        req = ustruct.QryInvestorPositionDetail(BrokerID=self.cuser.broker_id, InvestorID=self.cuser.investor_id,InstrumentID=instrument_id)
        r=self.trader.ReqQryInvestorPositionDetail(req,self.inc_request_id())
        print u'查询持仓, 函数发出返回值:%s' % r

    ##交易处理
    def RtnTick(self,ctick):#行情处理主循环
        print u'in my lock, close长度:%s,ma_5长度:%s\n' %(len(self.data[ctick.instrument].sclose),len(self.data[ctick.instrument].ma_5))
        inst = ctick.instrument
        self.prepare_tick(ctick)
        #先平仓
        close_positions = self.check_close_signal()
        self.make_trade(close_positions)
        #再开仓.
        open_signals = self.check_signal()
        open_positions = self.calc_position(open_signals)
        self.make_trade(open_positions)
        #撤单, 撤销3分钟内未成交的以及等待发出队列中30秒内未发出的单子
        self.cancel_orders()
        #检查待发出单
        self.check_queued()
        ##扫尾
        self.finalize()
        print u'after my lock, close长度:%s,ma_5长度:%s\n' %(len(self.data[ctick.instrument].sclose),len(self.data[ctick.instrument].ma_5))
        
    def prepare_tick(self,ctick):
        '''
            准备计算, 包括分钟数据、指标的计算
        '''
        inst = ctick.instrument
        if inst not in self.data:
            logger.info(u'接收到未订阅的合约数据:%s' % (inst,))
        dinst = self.data[inst]
        if(self.prepare_base(dinst,ctick)):  #如果切分分钟则返回>0
            for func in self.data_funcs:    #动态计算
                func.func1(dinst)

    def prepare_base(self,dinst,ctick):
        '''
            返回值标示是否是分钟的切换
            这里没有处理15:00:00的问题
        '''
        rev = False #默认不切换
        if ctick.min1 != dinst.cur_min.vtime or ctick.date != dinst.cur_min.vdate:#时间切换
            rev = True
            #print ctick.min1,dinst.cur_min.vtime,ctick.date,dinst.cur_min.vdate
            if (len(dinst.stime)>0 and (ctick.date > dinst.sdate[-1] or ctick.min1 > dinst.stime[-1])) or len(dinst.stime)==0:#已有分钟与已保存的有差别
                #这里把00秒归入到新的分钟里面
                if (hreader.is_if(ctick.instrument) and ctick.min1 == 1515 and ctick.sec==0) or (not hreader.is_if(ctick.instrument) and ctick.min1 == 1500 and ctick.sec==0): #最后一秒钟算1514/1500的
                    print u'最后一秒钟....'
                    dinst.cur_min.vclose = ctick.price
                    if ctick.price > dinst.cur_min.vhigh:
                        dinst.cur_min.vhigh = ctick.price
                    if ctick.price < dinst.cur_min.vlow:
                        dinst.cur_min.vlow = ctick.price
                    dinst.cur_min.vholding = ctick.holding
                    dinst.cur_min.vvolume += (ctick.dvolume - dinst.cur_day.vvolume)
                if dinst.cur_min.vdate != 0:    #不是史上第一个
                    print u'正常保存分钟数据.......'
                    dinst.sdate.append(dinst.cur_min.vdate)
                    dinst.stime.append(dinst.cur_min.vtime)
                    dinst.sopen.append(dinst.cur_min.vopen)
                    dinst.sclose.append(dinst.cur_min.vclose)
                    dinst.shigh.append(dinst.cur_min.vhigh)
                    dinst.slow.append(dinst.cur_min.vlow)
                    dinst.sholding.append(dinst.cur_min.vholding)
                    dinst.svolume.append(dinst.cur_min.vvolume)
                    ##需要save下
                    hreader.save1(dinst.name,dinst.cur_min)
                else:#是史上第一个，之前的cur_min是默认值
                    print u'不保存分钟数据,date=%s' % (dinst.cur_min.vdate)
                    rev = False
            dinst.cur_min.vdate = ctick.date
            dinst.cur_min.vtime = ctick.min1
            dinst.cur_min.vopen = ctick.price
            dinst.cur_min.vclose = ctick.price
            dinst.cur_min.vhigh = ctick.price
            dinst.cur_min.vlow = ctick.price
            dinst.cur_min.vholding = ctick.holding
            dinst.cur_min.vvolume = ctick.dvolume - dinst.cur_day.vvolume if ctick.date == dinst.cur_day.vdate else ctick.dvolume
        else:#当分钟的处理
            dinst.cur_min.vclose = ctick.price
            if ctick.price > dinst.cur_min.vhigh:
                dinst.cur_min.vhigh = ctick.price
            if ctick.price < dinst.cur_min.vlow:
                dinst.cur_min.vlow = ctick.price
            dinst.cur_min.vholding = ctick.holding
            dinst.cur_min.vvolume += (ctick.dvolume - dinst.cur_day.vvolume)
        ##日的处理
        if ctick.date != dinst.cur_day.vdate:
            dinst.cur_day.vdate = ctick.date
            dinst.cur_day.vopen = ctick.price
            dinst.cur_day.vhigh = ctick.price
            dinst.cur_day.vlow = ctick.price
        else:
            if ctick.price > dinst.cur_day.vhigh:
                dinst.cur_day.vhigh = ctick.price   #根据当前价比较得到的最大/最小
            if ctick.price < dinst.cur_day.vlow:
                dinst.cur_day.vlow = ctick.price
        dinst.cur_day.vholding = ctick.holding
        dinst.cur_day.vvolume = ctick.dvolume
        dinst.cur_day.vhighd = ctick.high   #服务器传过来的最大/最小
        dinst.cur_day.vlowd = ctick.low
        dinst.cur_day.vclose = ctick.price
        return rev
        
    def check_close_signal(self):
        '''
            检查平仓信号
        '''
        return []

    def check_signal(self):
        '''
            检查信号并发出指令
            信号包括开仓信号、平仓信号
        '''
        return []

    def cancel_orders(self):
        pass

    def check_queued(self):
        pass

    def calc_position(self,signals):
        '''
            根据信号集合来确定仓位
            signal的结构为(合约号、开/平、策略集id、开平比例)
        '''
        return []

    def make_trade(self,positions):
        '''
            根据仓位指令进行交易
            position的结构为(合约号、开/平、策略集id、开平手数)
            必须处理同时发出开平仓指令时保证金不足引起的问题，此时，应该放入到队列中, 并在每次平仓后检查这个队列中是否满足保证金
                这类指令必须在指定时间内(如30秒)实现，否则废弃
        '''
        pass

    def open_position(self,order):
        ''' 
            发出下单指令
        '''
        req = ustruct.InputOrder(
                InstrumentID = order.instrument,
                Direction = order.direction,
                OrderRef = str(order.order_ref),
                LimitPrice = order.price,
                VolumeTotalOriginal = order.volume,
                OrderPriceType = utype.THOST_FTDC_OPT_LimitPrice,
                
                BrokerID = self.cuser.broker_id,
                InvestorID = self.cuser.investor_id,
                CombOffsetFlag = utype.THOST_FTDC_OF_Open,         #开仓 5位字符,但是只用到第0位
                CombHedgeFlag = utype.THOST_FTDC_HF_Speculation,   #投机 5位字符,但是只用到第0位

                VolumeCondition = utype.THOST_FTDC_VC_AV,
                MinVolume = 1,
                ForceCloseReason = utype.THOST_FTDC_FCC_NotForceClose,
                IsAutoSuspend = 1,
                UserForceClose = 0,
                TimeCondition = utype.THOST_FTDC_TC_GFD,
            )
        r = self.trader.ReqOrderInsert(req,self.inc_request_id())


    def close_position(self,order,CombOffsetFlag = utype.THOST_FTDC_OF_CloseToday):
        ''' 
            发出平仓指令. 默认平今仓
        '''
        req = ustruct.InputOrder(
                InstrumentID = order.instrument,
                Direction = order.direction,
                OrderRef = str(order.order_ref),
                LimitPrice = order.price,
                VolumeTotalOriginal = order.volume,
                CombOffsetFlag = CombOffsetFlag,
                OrderPriceType = utype.THOST_FTDC_OPT_LimitPrice,
                
                BrokerID = self.cuser.broker_id,
                InvestorID = self.cuser.investor_id,
                CombHedgeFlag = utype.THOST_FTDC_HF_Speculation,   #投机 5位字符,但是只用到第0位

                VolumeCondition = utype.THOST_FTDC_VC_AV,
                MinVolume = 1,
                ForceCloseReason = utype.THOST_FTDC_FCC_NotForceClose,
                IsAutoSuspend = 1,
                UserForceClose = 0,
                TimeCondition = utype.THOST_FTDC_TC_GFD,
            )
        r = self.trader.ReqOrderInsert(req,self.inc_request_id())

    def cancel_order(self,order):
        '''
            发出撤单指令
        '''
        req = ustruct.InputOrderAction(
                InstrumentID = order.instrument,
                OrderRef = str(order.order_ref),
                
                BrokerID = self.cuser.broker_id,
                InvestorID = self.cuser.investor_id,
                FrontID = self.front_id,
                SessionID = self.session_id,
                ActionFlag = utype.THOST_FTDC_AF_Delete,
                #OrderActionRef = self.inc_order_ref()  #没用
            )
        r = self.trader.ReqOrderAction(req,self.inc_request_id())


    def finalize(self):
        #记录分钟数据??
        pass

    def resume(self):
        '''
            恢复环境
            对每一个合约:
                1. 获得必要的历史数据
                2. 获得当日分钟数据, 并计算相关指标
                3. 获得当日持仓，并初始化止损. 
        '''
        pass


    ###交易

    ###回应
    def rtn_order_ctp(self,sorder):
        '''
            ctp接受下单/撤单回报
        '''
        pass    #可以忽略

    def rtn_order_exchange(self,sorder):
        '''
            交易所接受下单/撤单回报
        '''
        #需要记录
        pass

    def rsp_order_insert(self,order_ref,instrument_id,error_id,error_msg):
        '''
            CTP下单错误回报
        '''
        pass    #可以忽略

    def err_order_insert(self,order_ref,instrument_id,error_id,error_msg):
        '''
            交易所下单错误回报
        '''
        pass    #可以忽略

    def rtn_trade(self,strade):
        '''
            成交回报
        '''
        pass    #需要记录

    def rsp_order_action(self,order_ref,instrument_id,error_id,error_msg):
        '''
            CTP撤单错误回报
        '''
        pass    #可以忽略
    
    def err_order_action(self,order_ref,instrument_id,error_id,error_msg):
        '''
            交易所撤单错误回报
        '''
        pass    #可能撤单已经成交
    
    
    def rsp_qry_instrument_marginrate(self):
        '''
            查询保证金率回报
        '''
        pass

    def rsp_qry_instrument(self):
        pass

    def rsp_qry_trading_account(self,account):
        '''
            查询资金帐户回报
        '''
        pass

    def rsp_qry_position(self,position):
        '''
            查询持仓回报, 得到持仓的一多一空
        '''
        pass

    def rsp_qry_position_detail(self,position_detail):
        '''
            查询持仓明细回报, 得到每一次成交的持仓,其中若已经平仓,则持量为0,平仓量>=1
        '''
        pass


    def rsp_qry_order(self,sorder):
        '''
            查询报单
        '''
        pass    #可以忽略

    def rsp_qry_trade(self,strade):
        '''
            查询成交
        '''
        pass    #可以忽略

import config as c 

def make_user(my_agent,hq_user,name='data'):
    user = MdApi.CreateMdApi(name)
    user.RegisterSpi(MdSpiDelegate(instruments=my_agent.instruments, 
                             broker_id=hq_user.broker_id,
                             investor_id= hq_user.investor_id,
                             passwd= hq_user.passwd,
                             agent = my_agent,
                    ))
    user.RegisterFront(hq_user.port)
    
    #user.RegisterFront(c.GD_USER.port)
    #user.RegisterFront(c.GD_USER_3.port)    
    #user.RegisterFront(c.GD_USER_2.port)        
    #user.RegisterFront(c.GD_USER_4.port)            
    user.Init()
    

def user_main():
    logging.basicConfig(filename="ctp_user_agent.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    cuser0 = c.SQ_USER
    cuser1 = c.GD_USER
    cuser2 = c.GD_USER_3
    cuser_wt1= c.GD_USER_2  #网通
    cuser_wt2= c.GD_USER_4  #网通

    my_agent = Agent(None,None,INSTS)

    make_user(my_agent,cuser1,'data1')
    #make_user(my_agent,cuser2,'data2')    
    #make_user(my_agent,cuser_wt1,'data_wt1')
    #make_user(my_agent,cuser_wt2,'data_wt2')    
    
    #make_user(my_agent,cuser0,'data')
    #make_user(my_agent,cuser0,'data')
    #make_user(my_agent,cuser0,'data')
    #make_user(my_agent,cuser0,'data')
    #make_user(my_agent,cuser0,'data')
    #make_user(my_agent,cuser0,'data')

    #while True:
    #    time.sleep(1)

def trade_test_main():
    '''
import agent
trader,myagent = agent.trade_test_main()
#开仓

##释放连接
trader.RegisterSpi(None)
    '''
    logging.basicConfig(filename="ctp_trade.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    trader = TraderApi.CreateTraderApi("trader")
    #cuser = c.SQ_TRADER1
    cuser = c.SQ_TRADER2
    my_agent = Agent(trader,cuser,INSTS)
    myspi = TraderSpiDelegate(instruments=INSTS, 
                             broker_id=cuser.broker_id,
                             investor_id= cuser.investor_id,
                             passwd= cuser.passwd,
                             agent = my_agent,
                       )
    trader.RegisterSpi(myspi)
    trader.SubscribePublicTopic(THOST_TERT_QUICK)
    trader.SubscribePrivateTopic(THOST_TERT_QUICK)
    trader.RegisterFront(cuser.port)
    trader.Init()
    return trader,my_agent
    
'''
#测试
import agent
trader,myagent = agent.trade_test_main()

myagent.spi.OnRspOrderInsert(agent.BaseObject(OrderRef='12',InstrumentID='IF1103'),agent.BaseObject(ErrorID=1,ErrorMsg='test'),1,1)
myagent.spi.OnErrRtnOrderInsert(agent.BaseObject(OrderRef='12',InstrumentID='IF1103'),agent.BaseObject(ErrorID=1,ErrorMsg='test'))
myagent.spi.OnRspOrderAction(agent.BaseObject(OrderRef='12',InstrumentID='IF1103'),agent.BaseObject(ErrorID=1,ErrorMsg='test'),1,1)
myagent.spi.OnErrRtnOrderAction(agent.BaseObject(OrderRef='12',InstrumentID='IF1103'),agent.BaseObject(ErrorID=1,ErrorMsg='test'))

#资金和持仓
myagent.fetch_trading_account()
myagent.fetch_investor_position(u'IF1103')
myagent.fetch_investor_position_detail(u'IF1103')

#测试报单
morder = agent.BaseObject(instrument='IF1103',direction='0',order_ref=myagent.inc_order_ref(),price=3280,volume=1)
myagent.open_position(morder)
morder = agent.BaseObject(instrument='IF1103',direction='0',order_ref=myagent.inc_order_ref(),price=3280,volume=20)

#平仓
corder = agent.BaseObject(instrument='IF1103',direction='1',order_ref=myagent.inc_order_ref(),price=3220,volume=1)
myagent.close_position(corder)

#测试撤单
import agent
trader,myagent = agent.trade_test_main()

cref = myagent.inc_order_ref()
morder = agent.BaseObject(instrument='IF1103',direction='0',order_ref=cref,price=3180,volume=1)
myagent.open_position(morder)

rorder = agent.BaseObject(instrument='IF1103',order_ref=cref)
myagent.cancel_order(rorder)


'''


if __name__=="__main__":
    main()
