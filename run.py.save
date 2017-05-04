# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 18:17:39 2016

@author: msegbers
"""

import pyshield
from pyshield import data, prefs, const
import pyshield.command_line as cmdl
from pyshield.visualization import show, show_floorplan
from pyshield.resources import read_resource
from pyshield import log, set_log_level
from pyshield.calculations.grid import calculate_dose_map_for_source
from pyshield.calculations.isotope import calc_dose_source_at_location
from pyshield.calculations.barrier import add_barriers
import numpy as np
import multiprocessing
import os
from timeit import default_timer as timer
import pandas as pd

NCORES = multiprocessing.cpu_count()

def run_with_configuration(**kwargs):
  """ See pyshield doc """ 
  
  # update package settings
  for key, value in kwargs.items():
    if key in (const.ORIGIN, const.SCALE):
        data[key] = value
    else:
        prefs[key] = value
  
  set_log_level(prefs[const.LOG])
  
  # log all settings to the pyshield logger
  log_str = 'Running with configuration: '
  pref_keys = sorted(prefs.keys())
  for key in pref_keys:
    log_str += '\n {0:<20} {1:<20}'.format(key, str(prefs[key]))
  log.info(log_str)

  # read yaml files from disk 
  data_keys = (const.SOURCES, const.SHIELDING, const.FLOOR_PLAN, const.XY, const.MATERIAL_COLORS)
  for key in data_keys:
    if key not in prefs.keys():
      data[key] = {}
      log.debug('No input was supplied for {0}'.format(key))
    else:
      try:
        data[key] = read_resource(prefs[key])
      except TypeError:       
        if key == const.XY and type(prefs[const.XY]) in (tuple, list):
          points = {}
          for i, p in enumerate(prefs[const.XY]):
            points['point ' + str(i)] = p
          data[const.XY] = points
        elif key==const.XY and type(prefs[const.XY]) is dict:
          data[const.XY] = prefs[const.XY]
        
        elif key == const.SOURCES:
          if key in prefs.keys() and type(prefs[const.SOURCES]) is dict:
            log.debug('Sources loaded as dict')
            data[const.SOURCES] = prefs[const.SOURCES]
        elif key == const.SHIELDING:
          if key in prefs.keys() and type(prefs[const.SHIELDING]) is dict:
            data[const.SHIELDING] = prefs[const.SHIELDING]
        else:
          data[key] = {}
          log.info('Cannot read file for {0} data'.format(key))
  
  data['run configuration'] = kwargs.copy()
  
  # make empty image with size area if no image is defined       
  if const.FLOOR_PLAN not in data.keys():
    data[const.FLOOR_PLAN] = np.zeros(prefs[const.AREA])
    log.debug('Empty area with size: {0}'.format(data[const.FLOOR_PLAN].shape))
    if const.SCALE not in prefs.keys():
      prefs[const.SCALE] = 1

  # set shielding empty if no file was defined
  if const.SHIELDING not in data.keys():
    data[const.SHIELDING] = {}
    log.debug('Empyt shielding set because no file was specified')

  # set empty shielding around source if it was not specified
  for source in data[const.SOURCES].values():
    if const.MATERIAL not in source.keys():
      source[const.MATERIAL] ={}
  
  # do point calculations, grid calculations or just display based on settings
  if prefs[const.CALCULATE] == const.GRID:
    result = grid_calculations()
    show(result)
  elif prefs[const.CALCULATE] == const.XY:
    result = point_calculations()
  else:
    #return (pyshield.data, pyshield.prefs)
    show_floorplan()
    result = None
  
  return result

def point_calculations():
  """ Performs calculation for a given set of points defined by the
      \'points\' option in run_with_configuration function. Returns a pandas
      Dataframe that contains information for each point and for each source."""
  
  log.info('\n-----Starting point calculations-----\n')

  locations = data[const.XY]
  log.debug('Locations: {0}'.format(locations))

  sources= data[const.SOURCES]

  shielding = data[const.SHIELDING]

  calc_func = lambda src, loc, table: \
              calc_dose_source_at_location(src, loc, shielding, table = table)
  
  excel_table = pd.DataFrame()
  dosemSv = {}
  for sname, source in sources.items():
    if const.FLOOR in prefs.keys():
      source[const.MATERIAL] = add_barriers(source[const.MATERIAL], 
                                            prefs[const.FLOOR][const.MATERIAL])
    dosemSv[sname] = 0
    

    for lname, location in locations.items():
        excel_row = pd.DataFrame()
        excel_row[const.ASOURCE] = [sname]
        excel_row[const.APOINT]  = [lname]
        dose = calc_func(source, location, excel_row)        
        excel_row['Dose [mSv]'] = dose 
        excel_table = pd.concat((excel_table, excel_row), ignore_index= True)
 
  
  log.info('\n-----Point calculations finished-----\n')
  return excel_table


  
  
def grid_calculations():
  """ Performs calculations for all points on a grid. grid type and grid
      sampling should by specified with the \'grid\', \'grid_size\' and
      \'number_of_angles\' option in run_with configuration.
      
      Returns:
          dictionary with dose_maps (2D numpy arrays) as values for each
          source name (keys)."""
  def wrapper(source_name, source):
    log.info('Calculate: {0}'.format(source_name))
    result = calculate_dose_map_for_source(source)       
    log.info('{0} Finished!'.format(source_name))
    return result

  sources = data[const.SOURCES]


  log.info('\n-----Starting grid calculations-----\n')

  # get single cpu or multi cpu worker
  worker = get_worker()

  snames  = tuple(sources.keys())
  sources = tuple(sources.values())
  
  start_time = timer()
  
  # do calculations
  if prefs[const.MULTI_CPU]:
    results = tuple(worker(calculate_dose_map_for_source,  sources))
  else:    
    results = tuple(worker(wrapper, snames, sources))

  end_time = timer()

  log.info('It took {0} to complete the calculation'.format(end_time - start_time))

  #format results
  results = dict(zip(snames, [r[0] for r in results]))
  
  log.info('\n-----Starting gird visualization-----\n')
  show(results = results)
  
 
  return results

def get_worker():
  """ Return the map function for either single core or multi core 
      calculations based on the \'multi_cpu\' flag in run_with_configuration.
      
      Note: Windows cannot perform multi core calculations.
      
        Returns:
            map (builtin python map function) or
            map (method from the multiprocessing.Pool object) """
      
  # select single core or multi core processing
 
    
  
  if prefs[const.MULTI_CPU]:
    if not(os.name == 'posix'):
      print('Cannot use multi processing on non posix os (Windows)')
      raise multiprocessing.ProcessError

    pool = multiprocessing.Pool(NCORES)
    worker = pool.map
    log.info('---MULTI CPU CALCULATIONS STARTED with {0} cpu\'s---\n'.format(NCORES))
    
  else:
    worker = map
    log.info('Single core calculations')
  return worker

# copy pyshield documentation to run with configuration  
run_with_configuration.__doc__ = pyshield.__doc__





#



