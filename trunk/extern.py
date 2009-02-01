# -*- coding: utf-8 -*-

#django环境准备
try:    #如果已经设置，则不再重新设置。这个是为test准备的
    import os
    os.environ['DJANGO_SETTINGS_MODULE']
    #print os.environ['DJANGO_SETTINGS_MODULE']
except: #未设置settings
    from django.core.management import setup_environ
    import wolfox.foxit.settings as settings
    setup_environ(settings)


import numpy as np
import django.db as dj
from django.db import connection
import wolfox.foxit.dune.store as s
import wolfox.foxit.dune.models as m

store = s.NormalStore()

code2id = store.get_code2id()
id2code = store.get_id2code()

ref_code = 'SH000001'   #上证指数
ref_id = code2id[ref_code]



