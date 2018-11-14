# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 18:17:39 2016

@author: msegbers
"""

from pathos import multiprocessing
import os
from timeit import default_timer as timer
import pandas as pd
from natsort import index_natsorted
import matplotlib.pyplot as plt
import pyshield as ps

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
    else:
        #raise FileNotFoundError(config + ' not found in current folder.')
        config = {}

    # overwite settings with kwargs
    config.update(kwargs)
    ps.config.set_config(config)

    # change log level based on config file
    ps.log.set_log_level(ps.config.get_setting(ps.LOG))
    ps.logger.debug('Source file: %s', ps.config.get_setting('sources'))
    ps.logger.info('Working directory: %s', os.getcwd())
    # display all parameters in debug
    ps.logger.info(ps.config.__str__())
    
    # save original config params
    ps.RUN_CONFIGURATION = ps.config.get_config()

    # map for single core or multiprocessing.pool.map for multi-core
    pool, worker = _get_worker()

    result = {} # gather calculation results
    
    calc_setting = ps.config.get_setting(ps.CALCULATE)

    if ps.GRID in calc_setting and ps.config.get_setting(ps.SOURCES):
        ps.logger.debug('Start grid calculations')
        # perform grid calculations
        dose_maps = grid_calculations(worker)
        result[ps.DOSE_MAPS] = dose_maps
    if ps.POINTS in calc_setting and ps.config.get_setting(ps.POINTS):
        ps.logger.debug('Start point calculations')
        # perform dose calculations
        table, sum_table = point_calculations(worker)
        result[ps.TABLE] = table
        result[ps.SUM_TABLE] = sum_table

    # necessary for multi core
    if pool is not None:
        pool.terminate()

    # display
    if ps.config.get_setting(ps.SHOW):
          result[ps.FIGURE] = ps.visualization.show(result)
          if ps.POINTS in ps.config.get_setting(ps.CALCULATE):
              ps.export.print_dose_report(result)
              
    # write results to disk if any
    if ps.config.get_setting(ps.EXPORT_EXCEL):
        ps.export.export_excel(result)
        
    if ps.FIGURE in result.keys() and ps.config.get_setting(ps.EXPORT_IMAGES):
        ps.export.export_images(result)
    
    if ps.COMMAND_LINE and ps.FIGURE in result.keys():
        # Do not exit and go back to cmd line which will close all figs
        plt.show(block=True)
    return result

def point_wrapper(location):
    """
    Calculate dose at a specific location. Dose are calculated per source.
    For each source an entry in a pandas table is created. 
    """ 
    
    # get data from settings
    height                 = ps.config.get_setting(ps.HEIGHT)
    disable_buildup        = ps.config.get_setting(ps.DISABLE_BUILDUP)
    intersection_thickness = ps.config.get_setting(ps.INTERSECTION_THICKNESS)
    barriers               = ps.config.get_setting(ps.BARRIERS)
    floor                  = ps.config.get_setting(ps.FLOOR)
    sources                = ps.config.get_setting(ps.SOURCES)


    calc_func = ps.calculations.isotope.calc_dose_source_at_location
    
    # iterate over all sources
    rows = []
    for name, source in sources.items():
        result = calc_func(source, location[ps.LOCATION],
                           barriers,
                           disable_buildup = disable_buildup,
                           intersection_thickness = intersection_thickness,
                           height = height,
                           return_details = True,
                           floor = floor)

        result[ps.SOURCE_NAME] = name
        #row = dose_table(result)
        rows += [result]
        
    return pd.DataFrame(rows)


def summary_table(table):
  # generate summary by adding all values by piovote table
  summary = table.pivot_table(values = ps.DOSE_MSV,
                              index = [ps.POINT_NAME, ps.OCCUPANCY_FACTOR],
                              aggfunc = sum)

  # get sort order, natsorted gives 0,1,2,3,4,5,6,7,8,8, 10 instead of
  # 0, 1, 10,2, 20 etc.
  new_index = index_natsorted(summary.index)

  # sort table by point name
  summary = summary.iloc[new_index]
  
  summary.reset_index(inplace = True)

  # add corrected dose for occupancy
  summary[ps.DOSE_OCCUPANCY_MSV] = summary[ps.DOSE_MSV] * \
                                   summary[ps.OCCUPANCY_FACTOR]
  
  return summary


def point_calculations(worker):
    """ 
    Calculate doses for all points, use worker to execute calculations.
    """
    
    locations       = ps.config.get_setting(ps.POINTS)
    sources         = ps.config.get_setting(ps.SOURCES)

    ps.logger.debug('Locations: {0}'.format(locations))
    ps.logger.debug('Sources: {0}'.format(sources))

    ps.logger.info('\n-----Starting point calculations-----\n')

    # actual calculations
    tables = list(worker(point_wrapper, locations.values()))

    # add location name and occupance factor to the table for each row
    location_names = locations.keys()
    for loc_name, table in zip(location_names, tables):
        table[ps.POINT_NAME] = loc_name
        try:
            occupancy = locations[loc_name][ps.OCCUPANCY_FACTOR]
        except KeyError: # not defined set to 1 as default
            occupancy = 1
        
        table[ps.OCCUPANCY_FACTOR] = occupancy

    table = pd.concat(tables) # stitch rows together to create single table
    summary = summary_table(table) # use a pivot table to get summarized result
    
    ps.logger.info('\n-----Point calculations finished-----\n')
    
    return table, summary

def grid_wrapper(source_items):
    name, source = source_items
    calc_func = ps.grid.calculate_dose_map_for_source
    ps.logger.info('Calculate: {0}'.format(name))
    result = calc_func(source)
    ps.logger.info('{0} Finished!'.format(name))
    return result

def grid_calculations(worker):
    """ Performs calculations for all points on a grid. grid type and grid
      sampling should by specified with the \'grid\', \'grid_size\' and
      \'number_of_angles\' option in run_with configuration.

      Returns:
          dictionary with dose_maps (2D numpy arrays) as values for each
          source name (keys)."""


    sources = ps.config.get_setting(ps.SOURCES)

    ps.logger.info('\n-----Starting grid calculations-----\n')
    
    start_time = timer()

    # do calculations
    results = tuple(worker(grid_wrapper, sources.items()))
    
    # sort calculations, dose map for each source
    results = dict(zip(sources.keys(), [r[0] for r in results]))

    end_time = timer()
    dtime = end_time - start_time

    ps.logger.info('It took {0} to complete the calculation'.format(dtime))
    
    # sum dose maps 
    summed = ps.calculations.grid.sum_dose_maps(results.values())
    results[ps.SUM_SOURCES] = summed
    
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
            raise RuntimeError('Multi processing not available in Windows')

        pool = multiprocessing.ProcessPool(NCORES)
        worker = pool.map
        msg = '---MULTI CPU CALCULATIONS STARTED with {0} cpu\'s---\n'
        ps.logger.info(msg.format(NCORES))

    else:
        worker = map
        pool = None
        ps.logger.info('---SINGLE CPU CALCULATIONS STARTED----')
    return pool, worker

if __name__ == '__main__':
    run_with_configuration()

