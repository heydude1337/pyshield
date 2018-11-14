# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 00:27:58 2016

@author: msegbers
"""

import logging
import pyshield as ps
import os
LOG_FILE = 'pyshield.log'
LOG_LEVEL = logging.DEBUG
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def application_logger(app_name='app_name', fname=None,
                       log_level=logging.DEBUG, log_to_console=True):

    """ Create log functionality for an application with app_name """

    logger = logging.getLogger(app_name)
    logger.setLevel(log_level)
    logger.handlers = []
    # create file handler which logs even debug messages
    formatter = logging.Formatter(FORMAT)

    if not fname is None:
        fh = logging.FileHandler(fname)
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    if log_to_console:
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger

def set_log_level(loglevel_str):
    """ change log level for all handlers """
    if loglevel_str == ps.LOG_DEBUG:
        level = logging.DEBUG
    elif loglevel_str == ps.LOG_INFO:
        level = logging.INFO
    elif loglevel_str == ps.LOG_ERROR:
        level = logging.ERROR
    elif type(loglevel_str) not in (str,):
        level = loglevel_str
    else:
        level = LOG_LEVEL
    for handler in logger.handlers:
        handler.setLevel(level)
    logger.setLevel(level)
    
# Keep install location clean
pkg_folder = os.path.normpath(ps.__pkg_root__).lower()
if  pkg_folder in os.path.normpath(os.getcwd()).lower():
    fname = None
else:
    fname = LOG_FILE
    
logger = application_logger(app_name='pyshield',
                           fname=fname,
                           log_level=logging.INFO,
                           log_to_console=True)

if fname is None:
    logger.debug('Log to file is disabled')

