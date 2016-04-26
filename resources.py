# -*- coding: utf-8 -*-
import pyshield
from pyshield import __pkg_root__, const, log, excel_import
from pyshield.yaml_wrap import yaml_wrap
import os
from os.path import join, splitext


import matplotlib.image as mpimg
import numpy as np

def read_resources(files = None):    
  # read resource files either yaml or in excel format for buildup
  data={}
  resource_dir = join(__pkg_root__ ,'resources')
  
  files = dict([(key,join(resource_dir,file)) for key, file in files.items()])
  
  for key, file in files.items():
    data[key] = read_resource(file)
    
  if const.BUILDUP in data.keys():
    data[const.BUILDUP] = format_buildup_data(data[const.BUILDUP])
  
  return data

def read_resource(file):
  log.debug('Loading: '  + file)
  ext = splitext(file)[1].lower()
  log.info('wdir=' + os.getcwd())
  log.info('Loading resource: ' + file)
  if ext in ('.yml','.yaml'):
    data=yaml_wrap.read_yaml(file)
  elif ext in ('.xls', '.xlsx'):
    data=excel_import.read_excel_file(file)
  elif ext in ('.png', '.jpeg', '.jpg'):
    data=np.flipud(mpimg.imread(file))
  else:
    print(pyshield.ERR_FILE.format(file=file))
    raise
  return data
 

def format_buildup_data(data):
  for material in data.keys():
    data[material] = excel_import.parse_sheet_data(
                                data[material], 
                                row_column_header=0, 
                                column_row_header=0,
                                row_name = const.MFP,
                                column_name = const.ENERGY,
                                data_name = const.BUILDUP_FACTORS)
  return data
  
#resource files are defined in the yml file in the package root
resource_files = yaml_wrap.read_yaml(join(__pkg_root__, const.RESOURCE_FILE))  
resources = read_resources(resource_files)