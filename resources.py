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

def is_valid_resource_file(file):
  valid = False
  for ext in VALID_EXTENSIONS:
    if type(file) is str and file.endswith(ext):
      valid = True
  return valid

def read_resources(files=None):
    """ read file as resource and add to pyshield data """
    # read resource files either yaml or in excel format for buildup
    data = {}
    resource_dir = join(__pkg_root__, 'resources')

    files = dict([(key, join(resource_dir, file)) for key, file in files.items()])

    for key, file in files.items():
        data[key] = read_resource(file)
    return data

def read_resource(file):
    """ read file from disk (.yml, .xls/.xlsx and images) """
    if not(is_valid_resource_file(file)):
      print('Cannot read {0}'.format(file))
      raise(TypeError)

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

#resource files are defined in the yml file in the package root
RESOURCE_FILES = yaml_wrap.read_yaml(join(__pkg_root__, CONST.RESOURCE_FILE))
RESOURCES = read_resources(RESOURCE_FILES)
