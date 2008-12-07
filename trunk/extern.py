# -*- coding: utf-8 -*-

#django环境准备
from django.core.management import setup_environ
import wolfox.foxit.settings as settings
setup_environ(settings)

import numpy as np
import django.db as dj
import wolfox.foxit.dune.store as s
import wolfox.foxit.dune.models as m

store = s.NormalStore()

code2id = store.get_code2id()
id2code = store.get_id2code()

ref_code = 'SH000001'   #上证指数
ref_id = code2id[ref_code]



