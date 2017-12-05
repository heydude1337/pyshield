# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 18:17:39 2016

@author: msegbers
"""

import multiprocessing
import os
from timeit import default_timer as timer
import pandas as pd
from natsort import index_natsorted

import pyshield as ps


#import pyshield.calculations as calc
#import pyshield.visualization as viz
#from pyshield import log, set_log_level


# from pyshield import CONST, is_yaml, read_yaml


# from pyshield.getconfig import get_setting, set_settings

# from pyshield.visualization import show, print_dose_report
# from pyshield.export import export

#from pyshield.calculations.grid import calculate_dose_map_for_source
#from pyshield.calculations.isotope import calc_dose_source_at_location




NCORES = multiprocessing.cpu_count()

def run_with_configuration(config=None, **kwargs):
    """ Call this module to start pyshield. Depending on the settings calculations
    and visualizations will be started.

    By default config.yml in the current folder will be loaded. Optional a valid
    configuration file in yaml format can be specified.

    If no config file is specified, specific settings can be overriden by using
    keyword arguments. e.g. run_with_configuration(calculate=None) will
    disable calculations."""

    if config is None:
        config = ps.CONFIG_FILE

    if os.path.exists(config):
        ps.logger.debug('Loading config file %s', config)
        config = ps.io.read_yaml(config)

    # overwite settings with kwargs
    config.update(kwargs)
    ps.config.set_config(config)

    # change log level based on config file
    ps.log.set_log_level(ps.config.get_setting(ps.LOG))

    # display all parameters in debug
    ps.logger.debug(ps.config.__str__())

    # save original config params
    ps.RUN_CONFIGURATION = ps.config.get_config()

    # map for single core or multiprocessing.pool.map for multi-core
    pool, worker = _get_worker()

    dose_maps = None
    sum_table = None
    table     = None

#    check_calc_settings() # raise value error on incorrect input

    calc_setting = ps.config.get_setting(ps.CALCULATE)

    if ps.GRID in calc_setting:
        # perform grid calculations
        dose_maps = grid_calculations(worker)

    if ps.POINTS in calc_setting:
        # perform dose calculations
        table, sum_table = point_calculations(worker)


    results = {ps.TABLE:     table,
               ps.DOSE_MAPS: dose_maps,
               ps.SUM_TABLE: sum_table}

    # display
    results[ps.FIGURE] = ps.visualization.show(results)

    # print results to console
    if sum_table is not None:
        ps.visualization.print_dose_report(sum_table)

    # necessary for multi core
    if pool is not None:
        pool.close()

    # write results to disk if any
    ps.export.export(results)
    return results



#
#def _check_calc_settings():
#    # Check if calculations are requested and if so check if necessary input
#    # is given by the user. If input is missing (e.g. sources of points file)
#    # raise ValueError. Otherwise return true.
#
#    ps.logger.info('Checking input')
#    calc_setting = ps.config.get_setting(ps.CALCULATE)
#    ps.logger.debug('Calc setting: %s', calc_setting)
#    if not(ps.GRID in calc_setting or ps.POINTS in calc_setting):
#        return True
#
#
#    msg = 'No {0} file specified, file not found or file could' + \
#          ' not read. {0} file: {1}'
#
#
#    if len(ps.config.get_setting(ps.SOURCES)) == 0:
#        ps.logger.error(msg.format('sources', ps.config.get_setting(ps.SOURCES)))
#        raise ValueError
#
#
#    if len(ps.config.get_setting(ps.POINTS)) == 0 and ps.POINTS in calc_setting:
#        ps.logger.error(msg.format('points', ps.config.get_setting(ps.POINTS)))
#        #
#
#        raise ValueError
#        return False
#
#    return True

def dose_table(value_dict = None):
    columns = (ps.SOURCE_NAME, ps.SOURCE_LOCATION, ps.POINT_NAME,
               ps.POINT_LOCATION,ps.DOSE_MSV, ps.ISOTOPE,
               ps.ACTIVITY_H, ps.H10, ps.SOURCE_POINT_DISTANCE,
               ps.TOTAL_SHIELDING, ps.DISABLE_BUILDUP,
               ps.PYTHAGORAS, ps.HEIGHT, ps.DOSE_MSV_PER_ENERGY)

    table = pd.DataFrame(columns = columns)

    if value_dict is not None:
        for key, value in value_dict.items():
            if key not in columns:
                print(key)
                raise KeyError
            table[key] = [value]
    return table



def point_calculator(location):

    table = dose_table()
    height          = ps.config.get_setting(ps.HEIGHT)
    disable_buildup = ps.config.get_setting(ps.DISABLE_BUILDUP)
    pythagoras      = ps.config.get_setting(ps.PYTHAGORAS)
    shielding       = ps.config.get_setting(ps.SHIELDING)
    floor           = ps.config.get_setting(ps.FLOOR)
    sources         = ps.config.get_setting(ps.SOURCES)

    calc_func = ps.calculations.isotope.calc_dose_source_at_location

    for name, source in sources.items():
        result = calc_func(source, location[ps.LOCATION],
                           shielding,
                           disable_buildup = disable_buildup,
                           pythagoras = pythagoras,
                           height = height,
                           return_details = True,
                           floor = floor)

        result[ps.SOURCE_NAME] = name
        row = dose_table(result)

        table = pd.concat((table, row))
    return table


def summary_table(table):
  # generate summary by adding all values by piovote table
  summary = table.pivot_table(values = ps.DOSE_MSV,
                              index = [ps.POINT_NAME, ps.OCCUPANCY_FACTOR],
                              aggfunc = sum)


  #summary = pd.DataFrame(summary).reset_index()

  # get sort order, natsorted gives 0,1,2,3,4,5,6,7,8,8, 10 instead of
  # 0, 1, 10,2, 20 etc.
  #new_index = index_natsorted(summary[ps.POINT_NAME].values)
  new_index = index_natsorted(summary.index)

  # summary = summary.iloc[new_index].reset_index()

  summary = summary.iloc[new_index]
  #summary = summary.to_frame()
  summary.reset_index(inplace = True)

  # add corrected dose for occupancy
  summary[ps.DOSE_OCCUPANCY_MSV] = summary[ps.DOSE_MSV] * \
                                      summary[ps.OCCUPANCY_FACTOR]
  import pickle
  pickle.dump(summary, open('table2.pd', 'wb'))
  return summary


def point_calculations(worker):

    locations       = ps.config.get_setting(ps.POINTS)
    sources         = ps.config.get_setting(ps.SOURCES)

    ps.logger.debug('Locations: {0}'.format(locations))
    ps.logger.debug('Sources: {0}'.format(sources))

    ps.logger.info('\n-----Starting point calculations-----\n')

    # actual calculations
    tables = list(worker(point_calculator, locations.values()))

    # add additional data for each point
    location_names = locations.keys()
    for loc_name, table in zip(location_names, tables):
        table[ps.POINT_NAME] = loc_name
        try:
            table[ps.OCCUPANCY_FACTOR] = locations[loc_name][ps.OCCUPANCY_FACTOR]
        except KeyError:
            table[ps.OCCUPANCY_FACTOR] = 1

    table = pd.concat(tables) # add everything together
    summary = summary_table(table)
    ps.logger.info('\n-----Point calculations finished-----\n')
    return table, summary

def grid_calculations(worker):
    """ Performs calculations for all points on a grid. grid type and grid
      sampling should by specified with the \'grid\', \'grid_size\' and
      \'number_of_angles\' option in run_with configuration.

      Returns:
          dictionary with dose_maps (2D numpy arrays) as values for each
          source name (keys)."""



    def wrapper(source_name, source):
        calc_func = ps.grid.calculate_dose_map_for_source
        ps.logger.info('Calculate: {0}'.format(source_name))
        result = calc_func(source)
        ps.logger.info('{0} Finished!'.format(source_name))
        return result

    sources = ps.config.get_setting(ps.SOURCES)

    ps.logger.info('\n-----Starting grid calculations-----\n')

    snames  = tuple(sources.keys())
    sources = tuple(sources.values())

    start_time = timer()

    # do calculations
    if ps.config.get_setting(ps.MULTI_CPU):
        calc_func = ps.calculations.grid.calc_dose_source_at_location
        results = tuple(worker(calc_func,  sources))
    else:
        results = tuple(worker(wrapper, snames, sources))

    results = dict(zip(snames, [r[0] for r in results]))

    end_time = timer()

    dtime = end_time - start_time
    ps.logger.info('It took {0} to complete the calculation'.format(dtime))

    #format results

    return results

def _get_worker():
    # Return the map function for either single core or multi core
    # calculations based on the \'multi_cpu\' flag in run_with_configuration.

    # Note: Windows cannot perform multi core calculations.

    #    Returns:
    #        map (builtin python map function) or
    #        map (method from the multiprocessing.Pool object) """

    if ps.config.get_setting(ps.MULTI_CPU):
        if not(os.name == 'posix'):
            raise multiprocessing.ProcessError('Not available in Windows')

        pool = multiprocessing.Pool(NCORES)
        worker = pool.map
        ps.logger.info('---MULTI CPU CALCULATIONS STARTED with {0} cpu\'s---\n'.format(NCORES))

    else:
        worker = map
        pool = None
        ps.logger.info('---SINGLE CPU CALCULATIONS STARTED----')
    return pool, worker



