# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 18:17:39 2016

@author: msegbers
"""

import pyshield
from pyshield import CONST
from pyshield.getconfig import get_setting, set_setting, is_setting
from pyshield.resources import is_valid_resource_file, read_resource
from pyshield.calculations.barrier import add_floor
#import pyshield.command_line as cmdl
from pyshield.visualization import show, show_floorplan

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

def run_with_configuration(**kwargs):
  """ See pyshield doc """

  # update package settings
  for key, value in kwargs.items():
    if not is_setting(key):
      print('{0} is not a valid setting for pyshield projects'.format(key))
      raise KeyError

    if type(value) in [str]:
      if is_valid_resource_file(value):
        value = read_resource(value)

    set_setting(key, value)
    set_log_level(get_setting(CONST.LOG))


  log_str = 'Running with configuration: '
  pref_keys = sorted(get_setting().keys())
  for key in pref_keys:
    log_str += '\n {0:<20} {1:<20}'.format(key, str(get_setting(key)))
  log.info(log_str)


  pyshield.RUN_CONFIGURATION = get_setting()

  #add_floor()


  pool, worker = get_worker()
  # do point calculations and/or grid calculations

  calc_setting = get_setting(CONST.CALCULATE)
  if not hasattr(calc_setting, '__iter__'):
    calc_setting = (calc_setting,)


  dose_maps = None
  sum_table = None
  table = None

  if CONST.GRID in calc_setting:
    dose_maps = grid_calculations(worker)
  if CONST.POINTS in calc_setting:
    table, sum_table = point_calculations(worker)

  result = {CONST.TABLE:     table,
            CONST.DOSE_MAPS: dose_maps,
            CONST.SUM_TABLE: sum_table}

  result[CONST.FIGURE] = show(result)



  if pool is not None:
    pool.close()

  make_report('report.pdf', result[CONST.SUM_TABLE], result[CONST.FIGURE])

  return result


def dose_table(value_dict = None):
  columns = (CONST.ASOURCE, CONST.ALOC_SOURCE, CONST.APOINT, CONST.ALOC_POINT,
             CONST.DOSE_MSV, CONST.ISOTOPE, CONST.ACTIVITY_H, CONST.H10, CONST.ADIST_METERS,
             CONST.ASHIELDING_MATERIALS_CM, CONST.DISABLE_BUILDUP,
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
      result[CONST.ASOURCE] = name
      row = dose_table(result)
      #print(row)
      table = pd.concat((table, row))
    return table


def summary_table(table):
  # generate summary by adding all values by piovote table
  summary = table.pivot_table(values = CONST.DOSE_MSV,
                              index = [CONST.APOINT, CONST.OCCUPANCY_FACTOR],
                              aggfunc = sum)


  summary = pd.DataFrame(summary).reset_index()

  # get sort order, natsorted gives 0,1,2,3,4,5,6,7,8,8, 10 instead of
  # 0, 1, 10,2, 20 etc.
  new_index = index_natsorted(summary[CONST.APOINT].values)

  summary = summary.iloc[new_index].reset_index()
  # add corrected dose for occupancy
  summary[CONST.DOSE_OCCUPANCY_MSV] = summary[CONST.DOSE_MSV] * \
                                      summary[CONST.OCCUPANCY_FACTOR]

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
    table[CONST.APOINT] = loc_name
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
run_with_configuration.__doc__ = pyshield.__doc__





#



