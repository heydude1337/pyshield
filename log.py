# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 00:27:58 2016

@author: msegbers
"""

import logging
from pyshield import  __pkg_root__, const
from os.path import join

LOG_FILE = 'pyshield.log'
LOG_TO_FILE = True
LOG_TO_STDOUT = True
LOG_LEVEL = logging.INFO


log =logging.getLogger('pyshield')

def add_handlers(log):
        
   
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
    
    #create file handler
    fileHandler = logging.FileHandler(join(__pkg_root__,LOG_FILE), mode = 'w')
    fileHandler.setFormatter(formatter)
    
    #create handler for text logging to console
    stdoutHandler = logging.StreamHandler()
    stdoutHandler.setFormatter(formatter)
    
    
    # add handlers
    if LOG_TO_STDOUT:
      log.addHandler(stdoutHandler)
    if LOG_TO_FILE:
      log.addHandler(fileHandler)
      
    
    log.setLevel(LOG_LEVEL)
  

    log.propagate = False # prevent logging to console
    
    return log
    
    
def set_log_level(loglevel_str):
  if loglevel_str == const.LOG_DEBUG:
    log.setLevel(logging.DEBUG)
  elif loglevel_str == const.LOG_INFO:
    log.setLevel(logging.INFO)


if log.handlers == []:
  add_handlers(log)
        

