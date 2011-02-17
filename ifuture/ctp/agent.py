#-*- coding:utf-8 -*-
'''
Agent的目的是合并行情和交易API到一个类中进行处理
    把行情和交易分开，从技术角度上来看挺好，但从使用者角度看就有些蛋疼了.
    正常都是根据行情决策
'''

import time

import UserApiStruct
from MdApi import MdApi, MdSpi
from TraderApi import TraderApi, TraderSpi  

import logging
logging.basicConfig(filename="ctp_trade.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')


#数据定义中唯一一个enum
THOST_TERT_RESTART  = 0
THOST_TERT_RESUME   = 1
THOST_TERT_QUICK    = 2


inst = [u'IF1102',u'IF1103',u'IF1106']


def make_filename(apart,suffix='txt'):
    return '%s_%s.%s' % (apart,time.strftime('%Y%m%d'),suffix)

class MdSpiDelegate(MdSpi):
    '''
        将行情信息转发到Agent
        并自行处理杂务
    '''
    logger = logging.getLogger('ctp.MdSpiDelegate')    
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
        self.last_map = dict([(id,0) for id in instruments])

    def checkErrorRspInfo(self, info):
        if info.ErrorID !=0:
            logger.error("ErrorID:%s,ErrorMsg:%s" %(info.ErrorID,info.ErrorMsg))
        return info.ErrorID !=0

    def OnRspError(self, info, RequestId, IsLast):
        self.logger.error('requestID:%s,IsLast:%s,info:%s' % (RequestId,IsLast,str(info)))

    def OnFrontDisConnected(self, reason):
        self.logger.info('front disconnected,reason:%s' % (reason,))

    def OnHeartBeatWarning(self, time):
        pass

    def OnFrontConnected(self):
        self.logger.info('front connected')
        self.user_login(self.broker_id, self.investor_id, self.passwd)

    def user_login(self, broker_id, investor_id, passwd):
        req = UserApiStruct.ReqUserLogin(BrokerID=broker_id, UserID=investor_id, Password=passwd)
        self.agent.inc_requestid()
        r=self.api.ReqUserLogin(req, self.agent.get_requestid())

    def OnRspUserLogin(self, userlogin, info, rid, is_last):
        self.logger.info('user login,info:%s,rid:%s,is_last:%s' % (info,rid,is_last))
        if is_last and not self.checkErrorRspInfo(info):
            self.logger.info("get today's trading day:%s" % repr(self.api.GetTradingDay()))
            self.subscribe_market_data(self.instruments)

    def subscribe_market_data(self, instruments):
        self.api.SubscribeMarketData(instruments)

    def OnRtnDepthMarketData(self, depth_market_data):
        #print depth_market_data.BidPrice1,depth_market_data.BidVolume1,depth_market_data.AskPrice1,depth_market_data.AskVolume1,depth_market_data.LastPrice,depth_market_data.Volume,depth_market_data.UpdateTime,depth_market_data.UpdateMillisec,depth_market_data.InstrumentID
        #print 'on data......\n',
        if depth_market_data.InstrumentID not in self.instruments:
            logger.warning(u'收到未订阅的行情:%s' %(depth_market_data.InstrumentID,))
        dp = depth_market_data
        if dp.Volume <= self.last_map[dp.InstrumentID]:
            self.logger.debug(u'行情无变化，inst=%s,time=%s，volume=%s,last_volume=%s' % (dp.InstrumentID,dp.UpdateTime,dp.Volume,self.last_map[dp.InstrumentID]))
            return  #行情未变化
        self.last_map[dp.InstrumentID] = dp.Volume
        self.logger.debug('before loop')
        self.agent.RtnMarketData(depth_market_data)
        self.logger.debug('before write md:')
        ff = open(make_filename(depth_market_data.InstrumentID),'a+')
        ff.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (dp.TradingDay,dp.UpdateTime,dp.UpdateMillisec,dp.OpenInterest,dp.Volume,dp.LastPrice,dp.HighestPrice,dp.LowestPrice,dp.BidPrice1,dp.BidVolume1,dp.AskPrice1,dp.AskVolume1))
        ff.close()
        self.logger.debug('after write md:')


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

    def OnRspQryInstrument(self, pInstrument, pRspInfo, nRequestID, bIsLast):
        #如果合约还要靠查才能确定，直接关机走人
        pass

    def OnRspQryInstrumentMarginRate(self, pInstrumentMarginRate, pRspInfo, nRequestID, bIsLast):
        self.agent.RspQryInstrumentMarginRate(pInstrumentMarginRate,pRspInfo,nRequestID)

    def OnFrontDisconnected(self, nReason):
        #todo:logging
        pass

    def OnRspQryExchange(self, pExchange, pRspInfo, nRequestID, bIsLast):
        #为啥查这个?
        pass

    def OnRspOrderAction(self, pInputOrderAction, pRspInfo, nRequestID, bIsLast):
        pass

    def OnRspQryInvestor(self, pInvestor, pRspInfo, nRequestID, bIsLast):
        '''
请求查询投资者响应'''
        pass

    def OnRspRemoveParkedOrder(self, pRemoveParkedOrder, pRspInfo, nRequestID, bIsLast):
        '''
删除预埋单响应'''
        pass

    def OnRspQrySettlementInfo(self, pSettlementInfo, pRspInfo, nRequestID, bIsLast):
        '''
请求查询投资者结算结果响应'''
        pass

    def OnRspError(self, pRspInfo, nRequestID, bIsLast):
        '''
错误应答'''
        pass

    def OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):
        '''
登录请求响应'''
        pass

    def OnRspParkedOrderAction(self, pParkedOrderAction, pRspInfo, nRequestID, bIsLast):
        '''
预埋撤单录入请求响应'''
        pass

    def OnErrRtnOrderAction(self, pOrderAction, pRspInfo):
        '''
报单操作错误回报'''
        pass

    def OnRtnInstrumentStatus(self, pInstrumentStatus):
        '''
合约交易状态通知'''
        pass

    def OnRspOrderInsert(self, pInputOrder, pRspInfo, nRequestID, bIsLast):
        '''
报单录入请求响应'''
        pass

    def OnRspQryEWarrantOffset(self, pEWarrantOffset, pRspInfo, nRequestID, bIsLast):
        '''
请求查询仓单折抵信息响应'''
        pass

    def OnRspParkedOrderInsert(self, pParkedOrder, pRspInfo, nRequestID, bIsLast):
        '''
预埋单录入请求响应'''
        pass

    def OnRtnTradingNotice(self, pTradingNoticeInfo):
        '''
交易通知'''
        pass

    def OnRspQryInvestorPositionCombineDetail(self, pInvestorPositionCombineDetail, pRspInfo, nRequestID, bIsLast):
        '''
请求查询投资者持仓明细响应'''
        pass

    def OnHeartBeatWarning(self, nTimeLapse):
        '''
心跳超时警告。当长时间未收到报文时，该方法被调用。
@param nTimeLapse 距离上次接收报文的时间'''
        pass

    def OnRspQryTradingCode(self, pTradingCode, pRspInfo, nRequestID, bIsLast):
        '''
请求查询交易编码响应'''
        pass

    def OnRtnErrorConditionalOrder(self, pErrorConditionalOrder):
        '''
提示条件单校验错误'''
        pass

    def OnRspQrySettlementInfoConfirm(self, pSettlementInfoConfirm, pRspInfo, nRequestID, bIsLast):
        '''
请求查询结算信息确认响应'''
        pass

    def OnRtnOrder(self, pOrder):
        '''
报单通知'''
        pass

    def OnRspQryInvestorPosition(self, pInvestorPosition, pRspInfo, nRequestID, bIsLast):
        '''
请求查询投资者持仓响应'''
        pass

    def OnRspUserLogout(self, pUserLogout, pRspInfo, nRequestID, bIsLast):
        '''
登出请求响应'''
        pass

    def OnRspQryInvestorPositionDetail(self, pInvestorPositionDetail, pRspInfo, nRequestID, bIsLast):
        '''
请求查询投资者持仓明细响应'''
        pass

    def OnRspQryParkedOrderAction(self, pParkedOrderAction, pRspInfo, nRequestID, bIsLast):
        '''
请求查询预埋撤单响应'''
        pass

    def OnRspQryBrokerTradingParams(self, pBrokerTradingParams, pRspInfo, nRequestID, bIsLast):
        '''
请求查询经纪公司交易参数响应'''
        pass

    def OnRspQryParkedOrder(self, pParkedOrder, pRspInfo, nRequestID, bIsLast):
        '''
请求查询预埋单响应'''
        pass

    def OnRspQueryBankAccountMoneyByFuture(self, pReqQueryAccount, pRspInfo, nRequestID, bIsLast):
        '''
期货发起查询银行余额应答'''
        pass

    def OnRspQueryMaxOrderVolume(self, pQueryMaxOrderVolume, pRspInfo, nRequestID, bIsLast):
        '''
查询最大报单数量响应'''
        pass

    def OnRtnTrade(self, pTrade):
        '''
成交通知'''
        pass

    def OnErrRtnOrderInsert(self, pInputOrder, pRspInfo):
        '''
报单录入错误回报'''
        pass

    def OnRspQryTradingNotice(self, pTradingNotice, pRspInfo, nRequestID, bIsLast):
        '''
请求查询交易通知响应'''
        pass


    def OnRspQryNotice(self, pNotice, pRspInfo, nRequestID, bIsLast):
        '''
请求查询客户通知响应'''
        pass

    def OnRspQryTradingAccount(self, pTradingAccount, pRspInfo, nRequestID, bIsLast):
        '''
请求查询资金账户响应'''
        pass


    def OnRspSettlementInfoConfirm(self, pSettlementInfoConfirm, pRspInfo, nRequestID, bIsLast):
        '''
投资者结算结果确认响应'''
        pass

    def OnRspQryDepthMarketData(self, pDepthMarketData, pRspInfo, nRequestID, bIsLast):
        '''
请求查询行情响应'''
        pass

    def OnRspRemoveParkedOrderAction(self, pRemoveParkedOrderAction, pRspInfo, nRequestID, bIsLast):
        '''
删除预埋撤单响应'''
        pass

    def OnFrontConnected(self, ):
        '''
当客户端与交易后台建立起通信连接时（还未登录前），该方法被调用。'''
        pass

    def OnRspQryInstrumentCommissionRate(self, pInstrumentCommissionRate, pRspInfo, nRequestID, bIsLast):
        '''
请求查询合约手续费率响应'''
        pass

    def OnRspQryOrder(self, pOrder, pRspInfo, nRequestID, bIsLast):
        '''
请求查询报单响应'''
        pass

    def OnRspQryTrade(self, pTrade, pRspInfo, nRequestID, bIsLast):
        '''
请求查询成交响应'''
        pass


class Agent(object):
    logger = logging.getLogger('ctp.agent')

    def __init__(self):
        self.requestid = 1
        self.strategy_map = {}
        #self.prepare()

    def inc_requestid(self):
        self.requestid += 1

    def get_requestid(self):
        return self.requestid

    def prepare(self):
        '''
            准备数据, 如需要的30分钟数据
        '''
        pass

    def register(self,strategys):
        '''
            策略注册
            strategys是[(合约1,策略1),(合约2,策略2)]的对
                其中一个合约可以对应多个策略，一个策略也可以对应多个合约
        '''
        for ins_id,s in strategys:
            if ins_id not in self.strategy_map:
                self.strategy_map[ins_id] = []
            if s not in self.strategy_map[ins_id]:
                self.strategy_map[ins_id].append(s)

    def RtnMarketData(self,market_data):#行情处理主循环
        pass

def md_main():
    user = MdApi.CreateMdApi("data")
    my_agent = Agent()
    user.RegisterSpi(MdSpiDelegate(instruments=inst, 
                             broker_id="2030",
                             investor_id="0",
                             passwd="8",
                             agent = my_agent,
                             ))
    user.RegisterFront("tcp://asp-sim2-md1.financial-trading-platform.com:26213")
    user.Init()

    while True:
        time.sleep(1)

if __name__=="__main__": main()
