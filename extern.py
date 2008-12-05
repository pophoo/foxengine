# -*- coding: utf-8 -*-

#django环境准备
from django.core.management import setup_environ
import wolfox.foxit.settings as settings
setup_environ(settings)

import numpy as n
import django.db as d
import wolfox.foxit.dune.store as s
import wolfox.foxit.dune.models as m

store = s.NormalStore()

code2id = store.get_code2id()
id2code = store.get_id2code()

ref_code = 'SH000001'
ref_id = code2id[ref_code]  #m.StockCode.objects.filter(code=ref_code)[0].id

