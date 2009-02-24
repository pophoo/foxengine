# -*- coding: utf-8 -*-

import re
from wolfox.fengine.core.base import BaseObject

import logging
logger = logging.getLogger('wolfox.fengine.core.cruiser.result2configs_test')

mm_pattern = r'\(-?(?P<balance>\d+), -?\d+, -?\d+, (?P<times>\d+)\)'
mm_groups = ['balance','times']

svama2_pattern = r'ma_standard=(?P<ma_standard>\d+),slow=(?P<slow>\d+),fast=(?P<fast>\d+),sma=(?P<sma>\d+)'
svama2_groups = ['fast','slow','sma','ma_standard']
svama3_pattern = r'slow=(?P<slow>\d+),sma=(?P<sma>\d+),ma_standard=(?P<ma_standard>\d+),extend_days=(?P<extend_days>\d+),fast=(?P<fast>\d+),mid=(?P<mid>\d+)'
svama3_groups = ['fast','mid','slow','sma','ma_standard','extend_days']
svama2s_pattern = r'ma_standard=(?P<ma_standard>\d+),slow=(?P<slow>\d+),extend_days=(?P<extend_days>\d+),fast=(?P<fast>\d+),sma=(?P<sma>\d+)'
svama2s_groups = ['fast','slow','sma','ma_standard','extend_days']
vama3_pattern = r'slow=(?P<slow>\d+),pre_length=(?P<pre_length>\d+),ma_standard=(?P<ma_standard>\d+),extend_days=(?P<extend_days>\d+),fast=(?P<fast>\d+),mid=(?P<mid>\d+)'
vama3_groups = ['fast','mid','slow','pre_length','ma_standard','extend_days']
vama2_pattern = r'slow=(?P<slow>\d+),pre_length=(?P<pre_length>\d+),ma_standard=(?P<ma_standard>\d+),fast=(?P<fast>\d+)'
vama2_groups = ['fast','slow','pre_length','ma_standard']
ma3_pattern = r'slow=(?P<slow>\d+),ma_standard=(?P<ma_standard>\d+),extend_days=(?P<extend_days>\d+),fast=(?P<fast>\d+),mid=(?P<mid>\d+)'
ma3_groups = ['fast','mid','slow','ma_standard','extend_days']


pmappings = {'svama2':BaseObject(pattern=svama2_pattern,groups=svama2_groups),
        'svama3':BaseObject(pattern=svama3_pattern,groups=svama3_groups),
        'svama2s':BaseObject(pattern=svama2s_pattern,groups=svama2s_groups),
        'vama3':BaseObject(pattern=vama3_pattern,groups=vama3_groups),
        }


def result2configs(name,file_from,file_to):
    if name not in pmappings:
        raise KeyError('%s not in pmappings' % name)
    rf = open(file_from,'r')
    wf = open(file_to,'w+')
    try:
        lines2configs(name,rf,wf)
    finally:
        rf.close()
        wf.close()


def lines2configs(name,rf,wf):
    pattern = re.compile(pmappings[name].pattern)
    groups = pmappings[name].groups
    cmm_pattern = re.compile(mm_pattern)
    for line in rf:
        if not line.rstrip():   #滤掉空行
            continue
        s_mm = transform(line,cmm_pattern,mm_groups)
        s_key = transform(line,pattern,groups)
        if s_key:
            oline = 'configs.append(config(buyer=fcustom(%s,%s))) #%s\n' % (name,s_key,s_mm)
            #print oline
            wf.write(oline)
        
def transform(line,pattern,groups):
    x = re.search(pattern,line)
    #print pattern,line
    lss = []
    for grp in groups:
        lss.append('%s=%s' % (grp,x.group(grp)))
    ss = ','.join(lss)
    return ss



