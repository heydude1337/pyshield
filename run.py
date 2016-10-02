# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 18:17:39 2016

@author: msegbers
"""

import argparse
import pyshield
from pyshield import data, prefs, const
import pyshield.command_line as cmdl
from pyshield.visualization import show, show_floorplan
from pyshield.resources import read_resource
from pyshield import log, __pkg_root__, set_log_level
from os.path import join
from pyshield.calculations.grid import calc_dose_grid_source, sum_dose, calc_dose_polar
from pyshield.calculations.isotope import calc_dose_sources_at_locations

import multiprocessing
import os
from timeit import default_timer as timer

NCORES = multiprocessing.cpu_count()

def read_prefs(prefs):
  log.debug(prefs.keys())
  data_file_keys = (const.SOURCES, const.SHIELDING, const.FLOOR_PLAN, const.XY)
  for key in data_file_keys:
    try:
      log.debug('Reading {0}'.format(key))
      prefs[key] = read_resource(prefs[key])
    except:
      log.exception('No valid or no input for {0}'.format(key))
      prefs[key] = {}

#  if const.SHIELDING not in prefs.keys():
#    log.warning('No shielding file found')
#    prefs[const.SHIELDING] = {}
#  if const.SOURCES not in prefs.keys():
#    log.warning('Ńo sources file found')
#    prefs[const.SOURCES] = {}
#  if prefs[const.XY] not in prefs.keys():
#    log.warning('No points file found')
#    prefs[const.XY] = {}

  return prefs

def set_prefs(conf):
  data_keys = (const.XY, const.SCALE, const.ORIGIN,
               const.SOURCES, const.SHIELDING, const.FLOOR_PLAN)

  new_data = dict([(k, v) for k,v in conf.items() if k in data_keys])
  new_prefs = dict([(k, v) for k, v in conf.items() if k not in data_keys])

  data.update(new_data)
  prefs.update(new_prefs)

def load_def_prefs():
  return read_resource(join(__pkg_root__, const.DEF_PREFERENCE_FILE))

def parse_args():
  parser = argparse.ArgumentParser()

  prefix = {}

  for name, arg in cmdl.COMMAND_LINE_ARGS.items():
    prefix[name] = arg.pop(cmdl.PREFIX, None)
    prefix[name] = ['--' + p for p in prefix[name]]

  for name, arg in cmdl.COMMAND_LINE_ARGS.items():
    parser.add_argument(*prefix[name], **arg)
  return vars(parser.parse_args())


def run(**kwargs):
  # load default settings
  log_str = 'Running with options: '
  for key, value in kwargs.items():
    log_str += '\n{0}: {1}'.format(key, value)
  log.debug(log_str)
  prefs = load_def_prefs()

  # update settings
  for key, value in kwargs.items():
    prefs[key] = value

  # read yaml files from disk and set pyshield prefs accasible to whole package
  set_prefs(read_prefs(prefs))
  set_log_level(prefs[const.LOG])

  # do point calculations, grid calculations or just display based on settings
  if prefs[const.CALCULATE] and prefs[const.XY] != {}:
    dose = point_calculations()
  elif prefs[const.CALCULATE] and prefs[const.GRID] is not None:
    dose = grid_calculations()

  else:
    #return (pyshield.data, pyshield.prefs)
    show_floorplan()
    dose = 0
  return dose


def point_calculations():
  log.info('\n-----Starting point calculations-----\n')

  locations = data[const.XY]
  sources= data[const.SOURCES]

  shielding = data[const.SHIELDING]

  worker = get_worker()

  dose = worker(calc_dose_sources_at_locations,
                sources.values(),
                locations,
                shielding)

  log.info('\n-----Point calculations finished-----\n')
  return dose

def get_worker():
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
  return worker

def grid_calculations():
  sources = data[const.SOURCES]

  #if prefs[const.CALCULATE] and prefs[const.GRIDSIZE] is not None:

  log.info('\n-----Starting grid calculations-----\n')

  if prefs[const.GRID] == const.CARTESIAN:
    calc_func = calc_dose_grid_source
  elif prefs[const.GRID] == const.POLAR:
    calc_func = calc_dose_polar

  worker = get_worker()

  # do calculations
  start_time = timer()
  dose_maps = tuple(worker(calc_func, tuple(sources.values())))
  end_time = timer()

  log.info('It took {0} to complete the calculation'.format(end_time - start_time))

  #format results
  dose_maps = dict(zip(tuple(sources.keys()), dose_maps))
  # sum over all dose_maps
  #dose_maps[const.SUM_SOURCES] = sum_dose(dose_maps)

  log.info('\n-----Starting gird visualization-----\n')
  #figs = show(dose_maps)

  return dose_maps


  return data




if __name__ == '__main__':
  # start from commandlune with commandline arguments
  log.info('\n-----Commandline start-----\n')
  prefs = parse_args()
  set_log_level(prefs[const.LOG])
  run(**prefs)




#



