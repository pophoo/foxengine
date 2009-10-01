# -*- coding: utf-8 -*-

#django环境准备
import os
if 'DJANGO_SETTINGS_MODULE' not in os.environ: #如果已经设置，则不再重新设置。这个是为test准备的
    #未设置settings
    from django.core.management import setup_environ
    import wolfox.foxit.settings as settings
    setup_environ(settings)
    os.environ['wolfox.db'] = settings.sqlite_db_name        

import numpy as np
import django.db as dj
import wolfox.foxit.dune.store as s
import wolfox.foxit.dune.models as m

store = s.NormalStore()

code2id = store.get_code2id()
id2code = store.get_id2code()

ref_code = 'SH000001'   #上证指数
ref_id = code2id[ref_code]

def get_dj_connection():
    return dj.connection

def get_src_connection():
    if not get_src_connection.connection:
        import sqlite3
        get_src_connection.connection = sqlite3.connect(os.environ['wolfox.db'])
    return get_src_connection.connection

get_src_connection.connection = None

get_connection = get_src_connection
