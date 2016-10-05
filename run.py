# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 18:17:39 2016

@author: msegbers
"""

import argparse
from pyshield import data, prefs, const
import pyshield.command_line as cmdl
from pyshield.visualization import show, show_floorplan
from pyshield.resources import read_resource
from pyshield import log, __pkg_root__, set_log_level
from os.path import join
from pyshield.calculations.grid import calculate_dose_map_for_source
from pyshield.calculations.isotope import calc_dose_sources_at_locations
import numpy as np
import multiprocessing
import os
from timeit import default_timer as timer

NCORES = multiprocessing.cpu_count()


def run_with_configuration(**kwargs):
  # update settings
  for key, value in kwargs.items():
    if key in (const.ORIGIN, const.SCALE):
        data[key] = value
    else:
        prefs[key] = value

  log_str = 'Running with configuration: '
  pref_keys = sorted(prefs.keys())
  for key in pref_keys:
    log_str += '\n{0}:\t\t\t\t\t {1}'.format(key, prefs[key])
  log.info(log_str)

  # read yaml files from disk and set pyshield prefs accasible to whole package
  data_keys = (const.SOURCES, const.SHIELDING, const.FLOOR_PLAN, const.XY)
  for key in data_keys:
    try:
      if key in prefs.keys():
          data[key] = read_resource(prefs[key])
      else:
        # empty image with size area if no image is defined
        if key == const.FLOOR_PLAN:
          if const.AREA in prefs.keys():              
              data[key] = np.zeros(const.AREA)
              prefs[const.SCALE] = 1 
    except:
      data[key] = {}
      print('Cannot read file for {0} data'.format(key))
   
  set_log_level(prefs[const.LOG])

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
  log.info('\n-----Starting point calculations-----\n')

  locations = data[const.XY]
  log.debug('Locations: {0}'.format(locations))

  sources= data[const.SOURCES]

  shielding = data[const.SHIELDING]


  calc_func = lambda sources: calc_dose_sources_at_locations(sources,
                                                             locations,
                                                             shielding)
  
  result = calc_func(sources)
  
  # calculate dose for each source seperately excel like
  if prefs[const.AUDIT]:
    result[const.DOSE_MSV] = result[const.AATTENUATION] * \
                             result[const.BUILDUP] *      \
                             result[const.ACTIVITY_H] *   \
                             result[const.H10]/1000 /     \
                             (result[const.ADIST_METERS]**2)
  log.info('\n-----Point calculations finished-----\n')
  return result

def grid_calculations():
  
  sources = data[const.SOURCES]


  log.info('\n-----Starting grid calculations-----\n')


  worker = get_worker()

  # do calculations
  start_time = timer()
  snames  = tuple(sources.keys())
  sources = tuple(sources.values())


  results = tuple(worker(calculate_dose_map_for_source, sources))

  end_time = timer()

  log.info('It took {0} to complete the calculation'.format(end_time - start_time))

  #format results
  results = dict(zip(snames, results))

  log.info('\n-----Starting gird visualization-----\n')
 

  return results

def get_worker():
  # select single core or multi core processing
  if prefs[const.MULTI_CPU]:
    if not(os.name == 'posix'):
      print('Cannot use multi processing on non posix os (Windows)')
      raise multiprocessing.ProcessError

    pool = multiprocessing.Pool(NCORES)
    worker = pool.map
    log.info('---MULTI CPU CALCULATIONS STARTED with {0} cpu\'s---\n'.format(NCORES))
    log.info('Multi core calculations')
  else:
    worker = map
    log.info('Single core calculations')
  return worker
  
  
def parse_args():
  parser = argparse.ArgumentParser()

  prefix = {}

  for name, arg in cmdl.COMMAND_LINE_ARGS.items():
    prefix[name] = arg.pop(cmdl.PREFIX, None)
    prefix[name] = ['--' + p for p in prefix[name]]

  for name, arg in cmdl.COMMAND_LINE_ARGS.items():
    parser.add_argument(*prefix[name], **arg)
  return vars(parser.parse_args())


if __name__ == '__main__':
  # start from commandlune with commandline arguments
  log.info('\n-----Commandline start-----\n')
  #prefs = parse_args()
  set_log_level(prefs[const.LOG])
  #run(**prefs)




#



