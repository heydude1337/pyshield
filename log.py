# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 00:27:58 2016

@author: msegbers
"""

import logging
from pyshield import  __pkg_root__
from os.path import join

LOG_FILE = 'pyshield.log'
#LOG_ERROR = 'Invalid log level set in config file. Use {0} or {1} as value.'.format(const.LOG_LEVEL_INFO, const.LOG_LEVEL_DEBUG)

## set log level based on setting in config file
#if const.LOG_LEVEL in config.keys():
#  if config[const.LOG_LEVEL] == const.LOG_LEVEL_INFO:    
#    LOG_LEVEL = logging.INFO
#  elif config[const.LOG_LEVEL] == const.LOG_LEVEL_DEBUG:
#    LOG_LEVEL = logging.DEBUG
#  else: 
#    print()
#else:
#  LOG_LEVEL = logging.INFO #default
  
LOG_LEVEL = logging.INFO
  
# create logging object and set format
log=logging.getLogger('pyshield')


formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')

fileHandler = logging.FileHandler(join(__pkg_root__,LOG_FILE), mode = 'w')
fileHandler.setFormatter(formatter)

log.setLevel(LOG_LEVEL)
log.addHandler(fileHandler)
log.propagate = False # prevent logging to console
