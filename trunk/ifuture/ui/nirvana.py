# -*- coding:utf-8 -*-

from enthought.traits.api import *
from enthought.traits.ui.api import View,Item,Group,HSplit,VGroup,VGrid
from enthought.traits.ui.api import Heading,EnumEditor,CheckListEditor
from enthought.traits.ui.menu import NoButtons

from matplotlib.figure import Figure

from mpl_figure_editor import MPLFigureEditor

class BaseInfo(HasTraits):
    '''
        基本信息, 不能选择
    '''
    xindex = Int
    xdate = Int
    xmin = Int
    xopen = Int
    xclose = Int
    xhigh = Int
    xlow = Int
    xvol = Int
    xholding = Int
    xdhigh = Int
    xdlow = Int

    def xupdate(self,sif,xindex):
        self.xindex = xindex
        self.xdate = sif.date[xindex]
        self.xmin = sif.time[xindex]
        self.xopen = sif.open[xindex]
        self.xclose = sif.close[xindex]
        self.xhigh = sif.high[xindex]
        self.xlow = sif.low[xindex]
        self.xvol = sif.vol[xindex]
        self.xholding = sif.holding[xindex]
        self.xdhigh = sif.dhigh[xindex]
        sif.xdlow = sif.dlow[xindex]


class IndexInfo(HasTraits):
    atr = Int
    xatr = Int
    mxatr = Int

    def xupdate(self,sif,xindex):
        self.atr = sif.atr[xindex]
        self.xatr = sif.xatr[xindex]
        self.mxatr = sif.mxatr[xindex]

class CustomInfo(HasTraits):
    lbreak_line = Int
    sbreak_line = Int
    lfired = Bool
    sfired = Bool

    def xupdate(self,sif,xindex):
        self.lbreak_line = sif.lbreak_line[xindex]
        self.sbreak_line = sif.sbreak_line[xindex]
        self.lfired = sif.lfired[xindex]
        seflf.sfired = sif.sfired[xindex]


class Setting(HasTraits):   #暂时不需要
    selected_items = List # Y轴所用的数据列表

class XControl(HasTraits):
    pre_button = Button(u'Pre') #
    next_button = Button(u'Next') #
    page_up_button = Button(u'PageUp') #
    page_down_button = Button(u'PageDown') #
    target_date = Int
    go_button = Button(u'Go')
 
    view = View(
        VGrid(
            Item('pre_button'),
            Item('next_button'),
            Item('page_up_button'),
            Item('page_down_button'),
            Item('target_date'),
            Item('go_button'),
            columns = 2,
            show_labels = False # 组中的所有控件都不显示标签
        )
   )


class Nirvana(HasTraits):
    base_info = Instance(BaseInfo)
    index_info = Instance(IndexInfo)
    cinfo = Instance(CustomInfo)
    xcontrol = Instance(XControl)
    figure = Instance(Figure) # 控制绘图控件的Figure对象


    view = View(
        HSplit( # HSplit分为左右两个区域，中间有可调节宽度比例的调节手柄
            Item("figure", editor=MPLFigureEditor(), show_label=False, width=600),
            Group(
               Item('xcontrol',style='custom'),
               show_labels = False # 组中的所有控件都不显示标签
            ),
        ),
        resizable=True, 
        height=0.75, width=0.75,
        buttons=NoButtons,
    )
    
    def _figure_default(self):
        figure = Figure()
        figure.add_axes([0.05, 0.04, 0.9, 0.92])
        return figure

    def _xcontrol_default(self):
        return XControl(figure=self.figure)

