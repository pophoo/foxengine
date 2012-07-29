# -*- coding:utf-8 -*-

from enthought.traits.api import *
from enthought.traits.ui.api import View,Item,Group,HSplit,VGroup,VGrid,Image,ToolBar,OKButton#,ImageResource
from enthought.traits.ui.api import Label,Heading,EnumEditor,CheckListEditor,TableEditor
from enthought.traits.ui.table_column import ObjectColumn
from enthought.traits.ui.menu import NoButtons

from matplotlib.figure import Figure

from mpl_figure_editor import MPLFigureEditor
from wolfox.fengine.core.base import BaseObject;

OPTIONAL = 0
MUST_NOT = 1
MUST_HAVE = 2



class DataUnit(HasTraits):
    name = Unicode()    #显示的名称
    sname = Str         #sif中的属性名
    value = Int         #值
    display = Trait(OPTIONAL,MUST_NOT,MUST_HAVE)
   

utable_editor = TableEditor(
        columns = [
                ObjectColumn(name='name'),
                ObjectColumn(name='value'),
        ],
        editable = False,
        show_column_labels = False,
    )


class DataUnits(HasTraits):
    data_units = List(Instance(DataUnit))

    def transfer_units(self,sif,xindex):
        for du in self.data_units:
            du.value = sif.__dict__[du.sname][xindex]

    view = View(
      Group(
        Item('data_units',editor = utable_editor),
        show_labels = False,
      ),
      resizable = True,
      width = 200,
      height = 400,
    )

base_infos = DataUnits(data_units=[
        DataUnit(name='xindex',sname='index',value=0,display=MUST_NOT),
        DataUnit(name='xopen',sname='open',value=0,display=MUST_NOT),
        DataUnit(name='xclose',sname='close',value=0,display=MUST_NOT),
        DataUnit(name='xhigh',sname='high',value=0,display=MUST_NOT),
        DataUnit(name='xlow',sname='low',value=0,display=MUST_NOT),
        DataUnit(name='xvol',sname='vol',value=0,display=MUST_NOT),
        DataUnit(name='xholding',sname='holding',value=0,display=MUST_NOT),
        DataUnit(name='xdhigh',sname='dhigh',value=0),
        DataUnit(name='xdlow',sname='dlow',value=0),
        DataUnit(name='xdopen',sname='dopen',value=0),
      ]
    )


index_infos = DataUnits(data_units=[
        DataUnit(name='atr',sname='atr',value=0),
        DataUnit(name='xatr',sname='xatr',value=0),
        DataUnit(name='mxatr',sname='mxatr',value=0),
      ]
    ) 

custom_infos = DataUnits(data_units=[
        DataUnit(name='atr',sname='atr',value=0),
        DataUnit(name='xatr',sname='xatr',value=0),
        DataUnit(name='mxatr',sname='mxatr',value=0),
      ]
    ) 

all_infos = [base_infos,index_infos,custom_infos]

class XInfos(HasTraits):
    pass

class XSetting(HasTraits):   #设定Y轴所用的数据列表,暂时不用
    candidate_items = List(Str) #可选的Y轴数据 
    selected_items = List(Str) # 
    must_have_items = List(Str)
    must_not_items = List(Str)
    name2item = DictStrAny

    speed1 = Int(3,label=u'前进速度')
    speed2 = Int(30,label=u'翻页速度')
    index_from = Int(0,label=u'起始坐标')
    index_width = Int(30,label=u'显示宽度')
    index_cur = Int(0,label=u'当前坐标')
    


    view = View(
            Heading(u'基本状态'),
            Group(
                Item('index_cur'),                
                Item('index_from'),
                Item('index_width'),
                Item('speed1'),
                Item('speed2'),
            ),
            Heading(u'设定显示指标'),
            Group(
                Item("selected_items", style="custom",editor=CheckListEditor(name="object.candidate_items",cols=2, format_str=u"%s")),
                show_labels = False,
            ),
            buttons = [OKButton,]
    )
    
    def generate_candidate(self,infos):
        candidate_items = []
        must_have_items = []
        must_not_items = []
        name2item = {}
        for info in infos:
            for du in info.data_units:
                name2item[du.name] = du
                if du.display == MUST_HAVE:
                    self.must_have_items.append(du.name)
                elif du.display == MUST_NOT:
                    self.must_not_items.append(du.name)
                elif du.display == OPTIONAL:
                    self.candidate_items.append(du.name)


class XControl(HasTraits):
    pre_button = Button(u'<',width=30) #
    next_button = Button(u'>') #
    page_up_button = Button(u'<<') #
    page_down_button = Button(u'>>') #
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
            show_labels = False,
            columns = 2,
        ),
        width=200,
   )


class Nirvana(HasTraits):
    xcontrol = Instance(XControl)
    csetting = Instance(XSetting)
    figure = Instance(Figure) # 控制绘图控件的Figure对象


    view = View(
        HSplit( #
            Item("figure", editor=MPLFigureEditor(), show_label=False,width=0.85),
            Group(
                Item('xcontrol',style='custom',show_label=False),
                Item('csetting',style='custom',show_label=False),
                show_labels = False, # 组中的所有控件都不显示标签
                layout = 'tabbed',
            ),
            show_labels = False # 组中的所有控件都不显示标签
        ),
        resizable=True, 
        height=0.95, 
        width=0.99,
        buttons=[OKButton,]
    )
    
    def _figure_default(self):
        figure = Figure()
        figure.add_axes([0.05, 0.04, 0.9, 0.92])
        return figure

    def _xcontrol_default(self):
        return XControl(figure=self.figure)

    def _csetting_default(self):
        cs = XSetting(figure=self.figure)
        cs.generate_candidate([base_infos,index_infos,custom_infos])
        return cs

