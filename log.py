# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 00:27:58 2016

@author: msegbers
"""

import logging
from pyshield import  __pkg_root__
from os.path import join

LOG_FILE = 'pyshield.log'
LOG_TO_FILE = True
LOG_TO_STDOUT = True
LOG_LEVEL = logging.DEBUG

# create logging object and set format
log=logging.getLogger('pyshield')
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')

#create file handler
fileHandler = logging.FileHandler(join(__pkg_root__,LOG_FILE), mode = 'w')
fileHandler.setFormatter(formatter)
#create handler for text logging to console
stdoutHandler = logging.StreamHandler()
stdoutHandler.setFormatter(formatter)


# add handlers

if LOG_TO_FILE: log.setLevel(LOG_LEVEL)
if LOG_TO_STDOUT: log.addHandler(fileHandler)


log.propagate = False # prevent logging to console
