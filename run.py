# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 18:17:39 2016

@author: msegbers
"""

import argparse
import pyshield
from pyshield import data, prefs, const
from pyshield.command_line import *
from pyshield.visualization import show, show_floorplan
from pyshield.resources import read_resource
from pyshield import log, __pkg_root__, set_log_level
from os.path import join
from pyshield.calculations.grid import calc_dose_grid_source, sum_dose

from pyshield.calculations.isotope import calc_dose_sources_at_locations


def load_conf(conf):
  data_file_keys = (const.SOURCES, const.SHIELDING, const.FLOOR_PLAN, const.XY)
  for key in data_file_keys:
    if key in conf.keys() and conf[key] is not None:
      try:
        conf[key] = read_resource(conf[key])
      except:
        print(pyshield.WARN_MISSING.format(missing = key))
        raise
  return conf

def set_conf(conf):
  data_keys = (const.XY, const.SCALE, const.ORIGIN, const.SOURCES, const.SHIELDING, const.FLOOR_PLAN)
  new_data = dict([(k, v) for k,v in conf.items() if k in data_keys])
  new_prefs = dict([(k, v) for k, v in conf.items() if k not in data_keys])

  data.update(new_data)
  prefs.update(new_prefs)

def load_def_prefs():
  return read_resource(join(__pkg_root__, const.DEF_PREFERENCE_FILE))

def parse_args():
  def_prefs = load_def_prefs()
  log.debug(def_prefs)
  parser = argparse.ArgumentParser()

  prefix = {}
  for name, arg in COMMAND_LINE_ARGS.items():
    prefix[name] = arg.pop(PREFIX, None)
    prefix[name] = ['--' + p for p in prefix[name]]

    if name in def_prefs.keys():
      arg[DEFAULT] = def_prefs[name]
    else:
      arg[DEFAULT] = None

  for name, arg in COMMAND_LINE_ARGS.items():
    parser.add_argument(*prefix[name], **arg)
  return vars(parser.parse_args())

def single_cpu_calculation(sources):
  log.info('Single CPU Calculation')
  dose_maps = {}
  for key, source in sources.items():
    log.info('Calculating: ' + key)
    dose_maps[key] = calc_dose_grid_source(source)
    log.info(key + 'finished calculation.')
    print(key + 'finished calculation.')
  return dose_maps

def run(conf = None, **kwargs):
  if conf is None:
    conf = load_def_prefs()

  for key, value in kwargs.items():
    conf[key] = value
  conf = load_conf(conf)
  set_conf(conf)

  set_log_level(conf[const.LOG])
  if conf[const.CALCULATE] and conf[const.XY] is not None:
    log.info('\n-----Starting point calculations-----\n')
    locations = data[const.XY]
    sources= data[const.SOURCES]

    shielding = data[const.SHIELDING]
    dose = calc_dose_sources_at_locations(sources, locations, shielding)

    log.info('\n-----Point calculations finished-----\n')
    return dose

  if conf[const.CALCULATE] and conf[const.GRIDSIZE] is not None:
    log.info('\n-----Starting gird calculations-----\n')
    sources = data[const.SOURCES]
    print(sources.keys())
    dose_maps = single_cpu_calculation(sources)
    dose_maps[const.SUM_SOURCES] = sum_dose(dose_maps)
    log.info('\n-----Starting gird visualization-----\n')
    figs = show(dose_maps)
    return [conf, data, dose_maps]
  else:
    #return (pyshield.data, pyshield.prefs)
    show_floorplan()
  return data




if __name__ == '__main__':
  log.info('\n-----Loading settings-----\n')
  conf = parse_args()

  set_log_level(conf[const.LOG])
  conf = load_conf(conf)
  set_conf(conf)




#



