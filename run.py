# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 18:17:39 2016

@author: msegbers
"""

import argparse
from pyshield import const, data, prefs, show
from pyshield.resources import read_resource
from pyshield import log, __pkg_root__
from os.path import join
from pyshield.calculations.grid import calc_dose_grid_source, sum_dose

def load_conf(conf):
  data_file_keys = (const.SOURCES, const.SHIELDING, const.FLOOR_PLAN)  
  for key in data_file_keys:   
    conf[key] = read_resource(conf[key])
  return conf
    
def set_conf(conf):
  data_keys = (const.SCALE, const.SOURCES, const.SHIELDING, const.FLOOR_PLAN)
  new_data = dict([(k, v) for k,v in conf.items() if k in data_keys])
  new_prefs = dict([(k, v) for k, v in conf.items() if k not in data_keys])
  
  data.update(new_data)
  prefs.update(new_prefs)
  
def load_def_prefs():
  return read_resource(join(__pkg_root__, const.DEF_PREFERENCE_FILE))

def parse_args():
  def_prefs = load_def_prefs()  
  
  log.debug(def_prefs)
  SOURCES_HELP =   'Specify a yaml file containing the information of the present sources'
  SHIELDING_HELP = 'Specify a yaml file containing the information of the present shielding'
  FLOORPLAN_HELP = 'Specify an image file of the floor plan for the calculation'
  SCALE_HELP =     'Specify the scale of the floorplan in cm/pixel'
  EXPORT_DIR_HELP = 'Specify a directory to which results (data and images) will be saved'
  GRID_SIZE_HELP = 'Specify the distance between grid points in pixels'
  CLIM_HEATMAP_HELP = 'Specify the clim for the heatmap: low,high (notice no space)'
  COLORMAP_HELP = 'Specify the colormap (any valid matplotlib colormap name)'  
  SHOW_HELP = 'Display the results of grid calculations in a nice figure. Show all sources seperately (all), show the summed dose (sum), or disable showing (none)'
  SAVE_IMAGES_HELP = 'Save displayed images as PNG'
  IMAGE_DPI_HELP = 'Specify the DPI for the saved images'
  SAVE_DATA_HELP = 'Save a (pickle) dump of the data to binary file'
  MULTI_CPU_HELP = 'Perform calculations on all availabel cpu cores. Disable to debug errors'
  PYTHA_HELP = 'When enabled the effective thickness of the barrier is calculated taking into account the angle of intersection.'
  ISO_VALUES_HELP = 'Isocontours for these dose values will be drawn. Number of values must match number of colors'
  ISO_COLORS_HELP = 'Colors for the isocontours. Number of colors must match number of values'
  DIS_BUILDUP_HELP = 'When True buildup will be disabled (testing purpuses)'
  
  parser = argparse.ArgumentParser()
  add = parser.add_argument  
  
  # parse comma seperated values to a list (no spaces should be in the string)
  # 1.0,2,5,4.5 will be converted to [1.0, 2, 5, 4.5]
  str_float_list = lambda s: [float(item) for item in s.split(',')]
  str_list = lambda s: [item for item in s.split(',')]
  
  add('--sources','--src', required = True, help = SOURCES_HELP)
  add('--shielding', '--sh', required = True, help= SHIELDING_HELP)
  add('--floorplan', '--f', required = True, help=FLOORPLAN_HELP)
  #add('--preferences', '--p', default = const.DEFAULT, required = False, help='Specify a yaml with with the desired preferences')
  add('--scale', '--sc', required = False, default = def_prefs[const.SCALE], type = float,  help= SCALE_HELP)
  add('--export_dir', '-e', required = False, default = def_prefs[const.EXPORT_DIR], type=str, help = EXPORT_DIR_HELP)
  add('--grid_size', required = False, default = def_prefs[const.GRIDSIZE], type = float, help = GRID_SIZE_HELP)
  add('--clim_heatmap', required=False, default = def_prefs[const.CLIM_HEATMAP], type = str_float_list, help = CLIM_HEATMAP_HELP )
  add('--colormap' , required=False, default = def_prefs[const.COLORMAP], type = str, help = COLORMAP_HELP)
  add('--show', required=False, default = def_prefs[const.SHOW], choices = ['all', 'sum', 'none'], help = SHOW_HELP)
  add('--save_images', required=False, default = def_prefs[const.SAVE_IMAGES], type=bool, help=SAVE_IMAGES_HELP)
  add('--save_data', required=False, default=def_prefs[const.SAVE_DATA], type=bool, help = SAVE_DATA_HELP)
  add('--multi_cpu', required=False, default = def_prefs[const.MULTI_CPU], type=bool, help = MULTI_CPU_HELP)
  add('--pythagoras', required=False, default=def_prefs[const.PYTHAGORAS], type=bool, help = PYTHA_HELP)
  add('--iso_values', required=False, default=def_prefs[const.ISO_VALUES], type=str_float_list, help=ISO_VALUES_HELP)
  add('--iso_colors', required=False, default=def_prefs[const.ISO_COLORS], type=str_list, help=ISO_COLORS_HELP)
  add('--disable_buildup', required=False, default = def_prefs[const.IGNORE_BUILDUP], type=bool, help= DIS_BUILDUP_HELP)
  add('--image_dpi', '--dpi', required=False, default = def_prefs[const.IMAGE_DPI], type=int, help = IMAGE_DPI_HELP)
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
  

if __name__ == '__main__':
  log.info('\n-----Loading settings-----\n')
  conf = parse_args()
  conf = load_conf(conf)
  set_conf(conf)
  log.info('\n-----Starting calculations-----\n')
 
  sources = data[const.SOURCES]
 
 
  dose_maps = single_cpu_calculation(sources)
  dose_maps[const.SUM_SOURCES] = sum_dose(dose_maps)

  log.info('\n-----Starting visualization-----\n')
 
  figs = show(dose_maps)



    
  