# -*- coding: utf-8 -*-

import os.path
import web
from wolfox.fengine.ifuture.ibase import *
import wolfox.fengine.ifuture.dynamic as dynamic
import wolfox.fengine.ifuture.ifuncs as ifuncs

#必须写绝对路径名，否则在apache中相对路径的起始是site-packages/web
path_name = os.path.dirname(__file__)
#path_name = 'D:/work/applications/gcode/wolfox/fengine/ifuture/web'
render = web.template.render(path_name)


urls = (
  '/last', 'LastUpdate'
)

application = web.application(urls, globals()).wsgifunc()

class LastUpdate:
    def GET(self):
        fname,sif,xactions = dynamic.whget(ifuncs.xxx)
        #return "name=%s,lastupdate=%s:%s" % (fname,sif.transaction[IDATE][-1],sif.transaction[ITIME][-1])
        lasttime = "%s-%s" % (sif.transaction[IDATE][-1],sif.transaction[ITIME][-1])
        for action in xactions:
            stop1 = sif.atr5x[action.index]/2000.0
            stop2 = sif.atr[action.index]*1.5/1000
            if stop1 < 3:
                stop1 = 3
            if stop2 < 3:
                stop2 = 3
            if action.position == LONG:
                action.stop1 = action.price - stop1
                action.stop2 = action.price - stop2
                action.stop = min(action.stop1,action.stop2)
            else:
                action.stop1 = action.price + stop1
                action.stop2 = action.price + stop2
                action.stop = max(action.stop1,action.stop2)
            action.stop1 = round(action.stop1,1)    #对空头可能多了0.05个点
            action.stop2 = round(action.stop2,1) 
            action.stop = round(action.stop,1) 
        return render.last(fname,lasttime,xactions)


if __name__ == "__main__": 
    app = web.application(urls, globals())
    app.run()
