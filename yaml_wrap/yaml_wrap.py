# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 11:00:43 2016

@author: 757021
"""
import os.path
import yaml
import logging as log


FILE_EXTENSIONS = ('.yml','.yaml')

def is_yaml(file_name):
  ext=os.path.splitext(file_name)[1].lower()
  if ext in FILE_EXTENSIONS:
    isyml=True
  else:
    isyml=False
  return isyml
      
def read_yaml(file_name):

  stream = open(file_name, 'r')
  yaml_dict = yaml.load(stream)
  
  if yaml_dict is None: yaml_dict = {}
  
  # append include files to dict
  if 'INCLUDE' in yaml_dict.keys():
    
    files = yaml_dict['INCLUDE']
    
    # remove include tag
    yaml_dict = dict([(k, v) for k, v in yaml_dict.items() if k != 'INCLUDE'])
    
    # read all included files and add items to dict
    for file in files:
      append_dict = read_yaml(file)  # recursive call
    # check if key already existed warn if key will be overwritten      
      for key in append_dict.keys():
        if key in yaml_dict.keys():
          log.warning('Duplicate data found in file' + \
                      '{0} for key {1}'.format(file, key))
      # append data (append_dict keys overwrite yaml_dict keys if duplicates)
      yaml_dict = {**yaml_dict, **append_dict}
      
  return yaml_dict

def write_yaml(file_name, dict_obj):
  stream = open(file_name, 'w')
  yaml.dump(dict_obj, stream=stream, default_flow_style=False)
  
#a=import_afscherming(FILE)
#isotopen=read_yaml('isotopen.yml')