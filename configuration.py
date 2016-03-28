# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 14:56:25 2016

@author: 757021
"""

# -*- coding: utf-8 -*-
from pyshield import log, const, __pkg_root__
from os.path import join, split, isfile
import os
import pickle
from yaml_wrap import yaml_wrap
import Excel.read as import_excel
import matplotlib.image as mpimg
config = {}
data = {}


STATE_FILE = 'config.state'

resource_files = yaml_wrap.read_yaml(join(__pkg_root__, const.RESOURCE_FILE))

for key in resource_files.keys():
  resource_files[key] = join(__pkg_root__, resource_files[key])

MATERIAL_MISSING_WARNING = 'Warning no build up factors defined for {material}!'                       
FILE_MISSING_ERROR = ('Data file missing!, please specify a yml file' + 
                    ' in the config file:\n {config_line}')       
FILE_ERROR = 'Could not open: {file}'
#----------------------Import configuration------------------------------------



def set_file(config_file = None):
    if config_file is None:
      config_file = get_default_config_file()
    dname, fname = split(config_file)
    if dname == '':
        dname = os.getcwd()
    
    config_file = join(dname,fname)    
    state_file = join(__pkg_root__, STATE_FILE)
    pickle.dump(config_file, open(state_file,'wb'))
    update_config()

def update_config():
    state_file = join(__pkg_root__, STATE_FILE)
    if isfile(state_file):
      config_file = pickle.load(open(state_file, 'rb'))
    else:
      config_file = get_default_config_file()
      
    try:
      new_config = _read_config(config_file)
    except:
      log.error('Cannot import config from: ' + config_file)
      try:
         log.info('Importing from the default config instead')
         new_config = _read_config(get_default_config_file())
      except:
          log.error('Cannot import config from the default config file')
          raise
    global config
    config.clear
    config.update(new_config)
    update_data()
    log.debug('New configuration set')

def get_default_config_file():
  return join(__pkg_root__, const.CONFIG_FILE)

def _read_config(config_file = None):
  """Read new configuration options from specified config_file, a dictionary
     is returned with the configuration
  
  config_file: A yaml file containing valid configuration for pyshield"""
  
  # default
  if config_file is None: 
    config_file = get_default_config_file()
    
  log.info('Reading config from: ' + config_file)
  new_config = yaml_wrap.read_yaml(config_file)
  new_config[const.CONFIG_FILE] = config_file
  return new_config
     
def reset():
  set_file()
    

    

#---------------------Import data---------------------------------------------
def read_data(data_files = None):
  """Read data files specified in the pyshield config variable, a dictionary
     is returned with an item for each data file.
     
     data_files: A dictonary containing the files to be read as data."""
      
  # select data files from configuration
    
  if data_files is None:
      data_files = config[const.FILES]
    
  files ={**data_files, **resource_files}    
  
  # read each file type from disk and store in dictionary
  new_data={}
  for key, file in files.items():
    ext=os.path.splitext(file)[1].lower()
    path, dummy = os.path.split(config[const.CONFIG_FILE])
    file = os.path.join(path, file)
    log.info('Loading: ' + file)
    if ext in ('.yml','.yaml'):
      new_data[key]=yaml_wrap.read_yaml(file)
    elif ext in ('.xls', '.xlsx'):
      new_data[key]=import_excel.read_excel_file(file)
    elif ext in ('.png', '.jpeg', '.jpg'):
      new_data[key]=mpimg.imread(file)
    else:
      print(FILE_ERROR.format(file))
      raise
  
  validate(new_data)
  return new_data
    
def update_data(data_files = None):
  """Read data files specified in the pyshield config variable and set the data
     variable, a dictionary is returned with an item for each data file.
     
     data_files: A dictonary containing the files to be read as data."""
  
  #Allow the data variable to be canged by users
  global data

  #Config should be cleared, references to the data variable should not be broken
  data.clear()    
  
  #read and update the data dictionary
  data.update(read_data(data_files))
  
  #Format buildup data if buildup data is specified
  buildup_defined = const.BUILDUP in resource_files.keys() 
  if buildup_defined and not(config[const.IGNORE_BUILDUP]):
    data[const.BUILDUP] = _parse_buildup_data(data[const.BUILDUP]) 



def validate(new_data):   
  """Perform checks a data variable and give meaningful errors and 
     warnings to the user. 
     
     new_data: The data that needs to be validated."""
  
  # Determine if necessary data key was read from disk and present in the data
  # variable
  for key in (const.ISOTOPES, const.SHIELDING, const.MATERIALS, const.SOURCES): 
    file = key.lower() + '.yml'
    error_msg = FILE_MISSING_ERROR.format(config_line = key + ': ' + file)
    assert key in new_data.keys(),  error_msg
    assert new_data[key] is not None, file +  ' Empty or not a valid yml file!'

  for key in new_data[const.MATERIALS].keys():
    if not key in new_data[const.BUILDUP].keys():
      log.warn(MATERIAL_MISSING_WARNING.format(material=key))
      
         
def _parse_buildup_data(buildup_data):
  """First row contains the mean free path and the first column contains the
     energies. Format the buildup_data. """
    
  for material in buildup_data.keys():
    buildup_data[material] = import_excel.parse_sheet_data(
                                buildup_data[material], 
                                row_column_header=0, 
                                column_row_header=0,
                                row_name = const.MFP,
                                column_name = const.ENERGY,
                                data_name = const.BUILDUP_FACTORS)
  return buildup_data