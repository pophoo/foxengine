# -*- coding: utf-8 -*-

import web
from wolfox.fengine.ifuture.ibase import *
import wolfox.fengine.ifuture.dynamic as dynamic
import wolfox.fengine.ifuture.ifuncs as ifuncs

#必须写绝对路径名，否则在apache中相对路径的起始是site-packages/web
render = web.template.render('D:/work/applications/gcode/wolfox/fengine/ifuture/web')


urls = (
  '/last', 'LastUpdate'
)

application = web.application(urls, globals()).wsgifunc()

class LastUpdate:
    def GET(self):
        fname,sif,xactions = dynamic.whget(ifuncs.xxx)
        #return "name=%s,lastupdate=%s:%s" % (fname,sif.transaction[IDATE][-1],sif.transaction[ITIME][-1])
        lasttime = "%s-%s" % (sif.transaction[IDATE][-1],sif.transaction[ITIME][-1])
        return render.last(fname,lasttime,xactions)


if __name__ == "__main__": 
    app = web.application(urls, globals())
    app.run()
