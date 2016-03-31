# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 11:00:43 2016

@author: 757021
"""
import os.path
import yaml

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
  return yaml_dict

def write_yaml(file_name, dict_obj):
  stream = open(file_name, 'w')
  yaml.dump(dict_obj, stream=stream, default_flow_style=False)
  
#a=import_afscherming(FILE)
#isotopen=read_yaml('isotopen.yml')