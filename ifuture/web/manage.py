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
  '/last', 'LastUpdate',
  '/last/(.*)','LastUpdate'
)

application = web.application(urls, globals()).wsgifunc()

class LastUpdate:
    def GET(self,priority=2500):
        try:
            priority = int(priority)    #除默认外，传入的是字符串
        except:
            return u'优先级请输入合法的数字，您输入的是:%s' % priority
        fname,sif,xactions = dynamic.whget(ifuncs.xxx4,priority=priority)
        #return "name=%s,lastupdate=%s:%s" % (fname,sif.transaction[IDATE][-1],sif.transaction[ITIME][-1])
        lasttime = "%s-%s" % (sif.transaction[IDATE][-1],sif.transaction[ITIME][-1])
        #print priority
        return render.last(fname,lasttime,xactions)



if __name__ == "__main__": 
    app = web.application(urls, globals())
    app.run()
