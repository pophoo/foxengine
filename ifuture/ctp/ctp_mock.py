# -*- coding: utf-8 -*-

'''
对CTP进行mock，目的有二：
    1. 为agent提供桩机，便于agent功能的开发和测试
    2. 结合实时行情，测试策略的实时信号
    3. 结合历史ticks行情，对策略进行确认测试

为真实起见，在mock中采用Command模式
桩机控制: (数据播放循环)
    数据播放
    触发Agent数据准备
    触发Agent策略执行
    触发API桩机-->Command
    控制器触发SPI 
    ...   
'''


class TraderMock(object):
    pass

class UserMock(object):
    pass

class MockManager(object):
    pass
