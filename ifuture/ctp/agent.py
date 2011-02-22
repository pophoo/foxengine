#-*- coding:utf-8 -*-
'''
Agent的目的是合并行情和交易API到一个类中进行处理
    把行情和交易分开，从技术角度上来看挺好，但从使用者角度看就有些蛋疼了.
    正常都是根据行情决策

'''

import time
import logging

import UserApiStruct
from MdApi import MdApi, MdSpi
from TraderApi import TraderApi, TraderSpi  

from wolfox.fengine.core.base import BaseObject


logging.basicConfig(filename="ctp_trade.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')


#数据定义中唯一一个enum
THOST_TERT_RESTART  = 0
THOST_TERT_RESUME   = 1
THOST_TERT_QUICK    = 2

inst = [u'IF1102',u'IF1103',u'IF1106']  #必须采用ctp使用的合约名字，内部不做检验
#inst = [u'IF1102']


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
        self.agent.inc_request_id()
        r=self.api.ReqUserLogin(req, self.agent.get_request_id())

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
        self.logger.debug(u'收到行情:%s,time=%s:%s' %(depth_market_data.InstrumentID,depth_market_data.UpdateTime,depth_market_data.UpdateMillisec))
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

 
    def isRspSuccess(self,RspInfo):
        return RspInfo == None or RspInfo.ErrorID == 0

    ##交易初始化
    def OnFrontDisconnected(self, nReason):
        #todo:logging
        pass
    
    def OnFrontConnected(self, ):
        '''
            当客户端与交易后台建立起通信连接时（还未登录前），该方法被调用。
        '''
        if bIsLast and self.isRspSuccess(pRspInfo):
            pass
        else:
            #logging
            pass
    

    def OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):
        '''登录请求响应'''
        pass

    def OnRspUserLogout(self, pUserLogout, pRspInfo, nRequestID, bIsLast):
        '''登出请求响应'''
        pass

    def OnRspQrySettlementInfo(self, pSettlementInfo, pRspInfo, nRequestID, bIsLast):
        '''请求查询投资者结算结果响应'''
        pass

    def OnRspQrySettlementInfoConfirm(self, pSettlementInfoConfirm, pRspInfo, nRequestID, bIsLast):
        '''请求查询结算信息确认响应'''
        pass

    def OnRspSettlementInfoConfirm(self, pSettlementInfoConfirm, pRspInfo, nRequestID, bIsLast):
        '''投资者结算结果确认响应'''
        pass

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
        if bIsLast and self.isRspSuccess(pRspInfo):
            agent.rsp_qry_trading_account(pTradingAccount)
        else:
            #logging
            pass

    def OnRspQryInvestorPosition(self, pInvestorPosition, pRspInfo, nRequestID, bIsLast):
        '''请求查询投资者持仓响应'''
        if bIsLast and self.isRspSuccess(pRspInfo):
            agent.rsp_qry_position(pInvestorPosition)
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
            agent.rsp_qry_order(pOrder)
        else:
            #logging
            pass

    def OnRspQryTrade(self, pTrade, pRspInfo, nRequestID, bIsLast):
        '''请求查询成交响应'''
        if bIsLast and self.isRspSuccess(pRspInfo):
            agent.rsp_qry_trade(pTrade)
        else:
            #logging
            pass


    ###交易操作
    def OnRspOrderInsert(self, pInputOrder, pRspInfo, nRequestID, bIsLast):
        '''
            报单未通过参数校验,被CTP拒绝
            正常情况后不应该出现
        '''
        if bIsLast and self.isRspSuccess(pRspInfo):
            agent.rsp_order_insert(pInputOrder.OrderRef,pInputOrder.InstrumentID,pRspInfo.ErrorID,pRspInfo.ErrorMsg)
        else:
            pass
    
    def OnErrRtnOrderInsert(self, pInputOrder, pRspInfo):
        '''
            交易所报单录入错误回报
            正常情况后不应该出现
            这个回报因为没有request_id,所以没办法对应
        '''
        if bIsLast and self.isRspSuccess(pRspInfo):
            agent.err_order_insert(pInputOrder.OrderRef,pInputOrder.InstrumentID,pRspInfo.ErrorID,pRspInfo.ErrorMsg)
        else:
            pass
    
    def OnRtnOrder(self, pOrder):
        ''' 报单通知
            CTP、交易所接受报单
        '''
        if bIsLast and self.isRspSuccess(pRspInfo):
            if pOrder.OrderStatus == 'a':
                #CTP接受，但未发到交易所
                agent.rtn_order_ctp(pOrder)
            else:
                agent.rtn_order_exchange(pOrder)
        else:
            pass

    def OnRtnTrade(self, pTrade):
        '''成交通知'''
        if bIsLast and self.isRspSuccess(pRspInfo):
            agent.rtn_trade(pTrade)
        else:
            pass

    def OnRspOrderAction(self, pInputOrderAction, pRspInfo, nRequestID, bIsLast):
        '''
            ctp撤单校验错误
        '''
        if bIsLast and self.isRspSuccess(pRspInfo):
            agent.rsp_order_action(self,pInputOrderAction.OrderRef,pInputOrderAction.InstrumentID,pRspInfo.ErrorID,pRspInfo.ErrorMsg)
        else:
            pass

    def OnErrRtnOrderAction(self, pOrderAction, pRspInfo):
        ''' 
            交易所撤单操作错误回报
            正常情况后不应该出现
        '''
        if bIsLast and self.isRspSuccess(pRspInfo):
            agent.err_order_action(pOrderAction.OrderRef,pOrderAction.InstrumentID,pRspInfo.ErrorID,pRspInfo.ErrorMsg)
        else:
            pass




class Agent(object):
    logger = logging.getLogger('ctp.agent')

    def __init__(self,trader):
        '''
            trader为交易对象
        '''
        self.trader = trader
        self.request_id = 1
        self.base_funcs = []  #基本函数集合. 如合成分钟数据,30,日数据等.  需处理动态数据. 
                              # 接口为(data,dyndata), 把dyndata添加到data的相应属性中去
                              #顺序关系非常重要
        self.data_funcs = []  #计算函数集合. 如计算各类指标, 顺序关系非常重要
                              # 接口为(data), 从data的属性中取数据,并计算另外一些属性
                              #顺序关系非常重要，否则可能会紊乱
        self.strategy_map = {}
        self.data = {}    #为合约号==>合约数据的dict
        self.lastupdate = 0
        self.holding = []   #(合约、策略族、基准价、基准时间、request_id、持仓量、止损价、止损函数)
        self.transited_orders = []    #发出后等待回报的指令, 回报后到holding
        self.queued_orders = []     #因为保证金原因等待发出的指令(合约、策略族、基准价、基准时间(到秒))
        #self.prepare()

    def inc_request_id(self):
        self.request_id += 1

    def get_request_id(self):
        return self.request_id

    def prepare(self):
        '''
            准备数据, 如需要的30分钟数据
        '''
        pass

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

    def register_base_funcs(self,funcs):
        self.base_funcs.update(funcs)
    
    def register_data_funcs(self,funcs):
        self.data_funcs.update(funcs)

    def RtnMarketData(self,market_data):#行情处理主循环
        inst = market_data.InstrumentID
        self.prepare(market_data)
        #先平仓
        close_positions = self.check_close_signal()
        self.make_trade(close_positions)
        #再开仓.
        open_signals = self.check_signal()
        open_positions = self.make_position(open_signals)
        self.make_trade(open_positions)
        #撤单, 撤销3分钟内未成交的以及等待发出队列中30秒内未发出的单子
        self.cancel()
        #检查待发出单
        self.check_queued()
        ##扫尾
        self.finalize()
        
    def prepare(self,dyndata):
        '''
            准备计算, 包括分钟数据、指标的计算
        '''
        for func in self.base_funcs:
            func(self.data,dyndata)
        for func in self.data_funcs:
            func(self.data)

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

    def make_position(self,signals):
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

    def rtn_order_ctp(self,sorder):
        '''
            ctp接受下单/撤单回报
        '''
        pass

    def rtn_order_exchange(self,sorder):
        '''
            交易所接受下单/撤单回报
        '''
        pass

    def rsp_order_insert(self,order_ref,instrument_id,error_id,error_msg):
        '''
            CTP下单错误回报
        '''
        pass

    def err_order_insert(self,order_ref,instrument_id,error_id,error_msg):
        '''
            交易所下单错误回报
        '''
        pass

    def rtn_trade(self,strade):
        '''
            成交回报
        '''
        pass

    def rsp_order_action(self):
        '''
            CTP撤单错误回报
        '''
        pass
    
    def err_order_action(self,order_ref,instrument_id,error_id,error_msg):
        '''
            交易所撤单错误回报
        '''
        pass
    
    
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
            查询持仓回报
        '''
        pass

    def rsp_qry_order(self,sorder):
        '''
            查询报单
        '''
        pass

    def rsp_qry_trade(self,strade):
        '''
            查询成交
        '''
        pass


def user_main():
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

def trade_main():
    trader = TraderApi.CreateTraderApi("trader")
    trader.RegisterSpi(TraderSpiDelegate(instruments=inst, 
                             broker_id="2030",
                             investor_id="0",
                             passwd="8",
                             agent = my_agent,
                       ))


if __name__=="__main__":
    main()
