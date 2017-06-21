""" Functions to read resource files (.yml, .xls/.xlsx and images) """

# -*- coding: utf-8 -*-

from os.path import join, splitext
import pandas as pd
import matplotlib.image as mpimg
import numpy as np

from pyshield import __pkg_root__, CONST, log
from pyshield.yaml_wrap import yaml_wrap

VALID_EXTENSIONS = ('.yml', '.yaml', 'xls', 'xlsx',
                    'png', 'jpeg', 'jpg', 'bmp')


RESOURCES = {}

def is_valid_resource_file(file):
  valid = False
  if type(file) not in (str,):
    return valid
  for ext in VALID_EXTENSIONS:
    if type(file) is str and file.endswith(ext):
      valid = True
  return valid



def read_resources():
    """ read resource files and add to pyshield data """
    #resource files are defined in the yml file in the package root
    files = yaml_wrap.read_yaml(join(__pkg_root__, CONST.RESOURCE_FILE))

    # read resource files either yaml or in excel format for buildup
    data = {}

    resource_dir = join(__pkg_root__, 'resources')



    for key, file in files.items():
        full_file = join(resource_dir, file)
        data[key] = read_data_file(full_file)


    RESOURCES.update(data)
    return data

def read_data_file(file):
    """ read file from disk (.yml, .xls/.xlsx and images) """
    if not(is_valid_resource_file(file)):
      print('Cannot read {0}'.format(file))
      raise TypeError

    log.debug('Loading: %s', file)
    ext = splitext(file)[1].lower()

    if ext in ('.yml', '.yaml'):
        log.debug('reading yaml')
        data = yaml_wrap.read_yaml(file)
    elif ext in ('.xls', '.xlsx'):
        log.debug('reading xml')
        data = pd.read_excel(file, sheetname=None)  # read all sheets
    elif ext in ('.png', '.jpeg', '.jpg', '.bmp'):
        log.debug('reading image')
        data = np.flipud(mpimg.imread(file))
    else:
        raise TypeError
    return data

read_resources()




