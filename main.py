# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 18:17:39 2016

@author: msegbers
"""

import pyshield
from pyshield import CONST
from pyshield.getconfig import get_setting, set_settings, is_setting
from pyshield.resources import is_valid_resource_file, read_data_file
from pyshield.yaml_wrap.yaml_wrap import is_yaml, read_yaml
from pyshield.visualization import show, print_dose_report
from pyshield.export import export
from pyshield import log, set_log_level
from pyshield.calculations.grid import calculate_dose_map_for_source
from pyshield.calculations.isotope import calc_dose_source_at_location

import multiprocessing
import os
from timeit import default_timer as timer
import pandas as pd
from pyshield.report import make_report
from natsort import index_natsorted


NCORES = multiprocessing.cpu_count()

def run_with_configuration(settings=None, **kwargs):


  if is_yaml(settings):
    settings = read_yaml(settings)
    log.info('Config file found and read.')

  elif settings is None:
     try:
       settings = read_yaml('config.yml')
       log.info('File config.yml found and read.')
     except FileNotFoundError:
       settings = kwargs
       pass

  else:
    print('Argument settings be a yml file!')
    raise TypeError

  set_settings(settings)

  # keyword arguments override settings
  set_settings(kwargs)

  set_log_level(get_setting(CONST.LOG))

  display_user_settings() # print settings to stdout in debug mode

  pyshield.RUN_CONFIGURATION = get_setting()  # save original config params

  pool, worker = get_worker()  # map or pool.map

  dose_maps = None
  sum_table = None
  table     = None

  check_calc_settings() # raise value error on incorrect input

  calc_setting = get_setting(CONST.CALCULATE)

  if CONST.GRID in calc_setting:
    # perform grid calculations
    dose_maps = grid_calculations(worker)
  if CONST.POINTS in calc_setting:
    # perform dose calculations
    table, sum_table = point_calculations(worker)


  results = {CONST.TABLE:     table,
             CONST.DOSE_MAPS: dose_maps,
             CONST.SUM_TABLE: sum_table}

  results[CONST.FIGURE] = show(results) # display

  if sum_table is not None:
    print_dose_report(sum_table)

  if pool is not None:
    pool.close()

  export(results) # write results to disk

  return results

def display_user_settings():
    log_str = 'Running with configuration: '
    pref_keys = sorted(get_setting().keys())
    for key in pref_keys:
      log_str += '\n {0:<20} {1:<20}'.format(key, str(get_setting(key)))

    log.debug(log_str)


def check_calc_settings():
  """ Check if calculations are requested and if so check if necessary input
      is given by the user. If input is missing (e.g. sources of points file)
      raise ValueError. Otherwise return true """

  log.info('Checking input')
  calc_setting = get_setting(CONST.CALCULATE)
  log.debug('Calc setting: %s', calc_setting)
  if not(CONST.GRID in calc_setting or CONST.POINTS in calc_setting):

    return True


  msg = 'No {0} file specified, file not found or file could' + \
        ' not read. {0} file: {1}'


  if len(get_setting(CONST.SOURCES)) == 0:
    log.error(msg.format('sources', get_setting(CONST.SOURCES)))
    raise ValueError
    return False

  if len(get_setting(CONST.POINTS)) == 0 and CONST.POINTS in calc_setting:
    log.error(msg.format('points', get_setting(CONST.POINTS)))
    raise ValueError
    return False

  return True

def dose_table(value_dict = None):
  columns = (CONST.SOURCE_NAME, CONST.SOURCE_LOCATION, CONST.POINT_NAME, CONST.POINT_LOCATION,
             CONST.DOSE_MSV, CONST.ISOTOPE, CONST.ACTIVITY_H, CONST.H10, CONST.SOURCE_POINT_DISTANCE,
             CONST.TOTAL_SHIELDING, CONST.DISABLE_BUILDUP,
             CONST.PYTHAGORAS, CONST.HEIGHT, 'Dose [mSv] per Energy')

  table = pd.DataFrame(columns = columns)

  if value_dict is not None:
    for key, value in value_dict.items():
      if key not in columns:
        print(key)
        raise KeyError

      table[key] = [value]
  return table



def func(location):
    table = dose_table()
    height          = get_setting(CONST.HEIGHT)
    disable_buildup = get_setting(CONST.DISABLE_BUILDUP)
    pythagoras      = get_setting(CONST.PYTHAGORAS)
    shielding       = get_setting(CONST.SHIELDING)
    floor           = get_setting(CONST.FLOOR)
    sources         = get_setting(CONST.SOURCES)


    for name, source in sources.items():
      result = calc_dose_source_at_location(source, location[CONST.LOCATION],
                                            shielding,
                                            disable_buildup = disable_buildup,
                                            pythagoras = pythagoras,
                                            height = height,
                                            return_details = True,
                                            floor = floor)

      result[CONST.SOURCE_NAME] = name
      row = dose_table(result)

      table = pd.concat((table, row))
    return table


def summary_table(table):
  # generate summary by adding all values by piovote table
  summary = table.pivot_table(values = CONST.DOSE_MSV,
                              index = [CONST.POINT_NAME, CONST.OCCUPANCY_FACTOR],
                              aggfunc = sum)


  #summary = pd.DataFrame(summary).reset_index()

  # get sort order, natsorted gives 0,1,2,3,4,5,6,7,8,8, 10 instead of
  # 0, 1, 10,2, 20 etc.
  #new_index = index_natsorted(summary[CONST.POINT_NAME].values)
  new_index = index_natsorted(summary.index)

  # summary = summary.iloc[new_index].reset_index()

  summary = summary.iloc[new_index]
  summary = summary.to_frame()
  summary.reset_index(inplace = True)

  # add corrected dose for occupancy
  summary[CONST.DOSE_OCCUPANCY_MSV] = summary[CONST.DOSE_MSV] * \
                                      summary[CONST.OCCUPANCY_FACTOR]
  import pickle
  pickle.dump(summary, open('table2.pd', 'wb'))
  return summary


def point_calculations(worker):
  locations       = get_setting(CONST.POINTS)
  sources         = get_setting(CONST.SOURCES)

  log.debug('Locations: {0}'.format(locations))
  log.debug('Sources: {0}'.format(sources))

  log.info('\n-----Starting point calculations-----\n')

  tables = list(worker(func, locations.values()))  # actual calculations

  # add additional data for each point
  location_names = locations.keys()
  for loc_name, table in zip(location_names, tables):
    table[CONST.POINT_NAME] = loc_name
    try:
      table[CONST.OCCUPANCY_FACTOR] = locations[loc_name][CONST.OCCUPANCY_FACTOR]
    except KeyError:
      table[CONST.OCCUPANCY_FACTOR] = 1

  table = pd.concat(tables) # add everything together
  summary = summary_table(table)
  log.info('\n-----Point calculations finished-----\n')



  return table, summary





def grid_calculations(worker):
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

  sources = get_setting(CONST.SOURCES)


  log.info('\n-----Starting grid calculations-----\n')



  snames  = tuple(sources.keys())
  sources = tuple(sources.values())

  start_time = timer()

  # do calculations
  if get_setting(CONST.MULTI_CPU):
    results = tuple(worker(calculate_dose_map_for_source,  sources))
  else:
    results = tuple(worker(wrapper, snames, sources))

  results = dict(zip(snames, [r[0] for r in results]))

  end_time = timer()

  dtime = end_time - start_time
  log.info('It took {0} to complete the calculation'.format(dtime))

  #format results

  return results

def get_worker():
  """ Return the map function for either single core or multi core
      calculations based on the \'multi_cpu\' flag in run_with_configuration.

      Note: Windows cannot perform multi core calculations.

        Returns:
            map (builtin python map function) or
            map (method from the multiprocessing.Pool object) """

  # select single core or multi core processing



  if get_setting(CONST.MULTI_CPU):
    if not(os.name == 'posix'):
      print('Cannot use multi processing on non posix os (Windows)')
      raise multiprocessing.ProcessError

    pool = multiprocessing.Pool(NCORES)
    worker = pool.map
    log.info('---MULTI CPU CALCULATIONS STARTED with {0} cpu\'s---\n'.format(NCORES))

  else:
    worker = map
    pool = None
    log.info('Single core calculations')
  return pool, worker

# copy pyshield documentation to run with configuration
#run_with_configuration.__doc__ = pyshield.__doc__





#



