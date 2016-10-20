# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 00:27:58 2016

@author: msegbers
"""

import logging
from pyshield import  __pkg_root__, const
from os.path import join
from ImageTools.app_logger import application_logger
LOG_FILE = 'pyshield.log'
#LOG_TO_FILE = True
#LOG_TO_STDOUT = True
#LOG_LEVEL = logging.DEBUG

LOG_LEVEL = logging.DEBUG
#log =logging.getLogger('pyshield')
log = application_logger('pyshield',
                         fname = LOG_FILE,
                         log_level = logging.INFO,
                         log_to_console = True)
#def add_handlers(log):
#
#
#    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
#
#    #create file handler
#    fileHandler = logging.FileHandler(join(__pkg_root__,LOG_FILE), mode = 'w')
#    fileHandler.setFormatter(formatter)
#
#    #create handler for text logging to console
#    stdoutHandler = logging.StreamHandler()
#    stdoutHandler.setFormatter(formatter)
#
#
#    # add handlers
#    if LOG_TO_STDOUT:
#      log.addHandler(stdoutHandler)
#    if LOG_TO_FILE:
#      log.addHandler(fileHandler)
#
#
#    log.setLevel(LOG_LEVEL)
#
#
#    log.propagate = False # prevent logging to console
#
#    return log
#
#
def set_log_level(loglevel_str):
  if loglevel_str == const.LOG_DEBUG:
    level = logging.DEBUG
  elif loglevel_str == const.LOG_INFO:
    level = logging.INFO
  elif type(loglevel_str) not in (str,):
    level = loglevel_str
  else:
    level = LOG_LEVEL
  for handler in log.handlers:
    handler.setLevel(level)
  log.setLevel(level)
#
#
#if log.handlers == []:
#  add_handlers(log)


