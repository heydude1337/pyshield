# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 17:24:32 2016

@author: 757021
"""
from pyshield import const
#==============================================================================
#  Help text for command line interface
#==============================================================================
HELP_TEXT = 'help'
DEFAULT = 'default'
DATA_TYPE = 'type'
REQUIRED = 'required'
PREFIX = 'Prefix'
CHOICES = 'choices'

HELP_STRINGS = {
  const.SOURCES:        'Specify a yaml file containing the information of the present sources',
  const.SHIELDING:      'Specify a yaml file containing the information of the present shielding',
  const.FLOOR_PLAN:     'Specify an image file of the floor plan for the calculation',
  const.SCALE:          'Specify the scale of the floorplan in cm/pixel',
  const.ORIGIN:         'Specify the origin in pixels: x,y (no space around the comma)',
  const.EXPORT_DIR:     'Specify a directory to which results (data and images) will be saved',
  const.GRIDSIZE:       'Specify the distance between grid points in pixels',
  const.XY:             'Specify a yaml file with points for which the dos will be calculated',
  const.CLIM_HEATMAP:   'Specify the clim for the heatmap: low,high (notice no space)',
  const.COLORMAP :      'Specify the colormap (any valid matplotlib colormap name)',
  const.SHOW :          'Display the results of grid calculations in a nice figure. Show all sources seperately (all), show the summed dose (sum), or disable showing (none)',
  const.SAVE_IMAGES :   'Save displayed images as PNG',
  const.IMAGE_DPI :     'Specify the DPI for the saved images',
  const.SAVE_DATA :     'Save a (pickle) dump of the data to binary file',
  const.MULTI_CPU :     'Perform calculations on all availabel cpu cores. Disable to debug errors',
  const.PYTHAGORAS :    'When enabled the effective thickness of the barrier is calculated taking into account the angle of intersection.',
  const.ISO_VALUES :    'Isocontours for these dose values will be drawn. Number of values must match number of colors',
  const.ISO_COLORS :    'Colors for the isocontours. Number of colors must match number of values',
  const.DISABLE_BUILDUP :   'When True buildup will be disabled (testing purpuses)',
  const.CALCULATE :     'Perform calculation',
  const.LOG:           'Set log level (info or debug), debug will slow down the calculations considerably'}

# parse comma seperated values to a list (no spaces should be in the string)
# 1.0,2,5,4.5 will be converted to [1.0, 2, 5, 4.5]
str_float_list = lambda s: [float(item) for item in s.replace('"', "").split(',')]
str_list = lambda s: [item for item in s.replace('"', "").split(',')]

COMMAND_LINE_ARGS = {
  const.SOURCES: {
    PREFIX: ('source_file', 'src'),
    HELP_TEXT: HELP_STRINGS[const.SOURCES]},
  const.SHIELDING: {
    PREFIX: ('shielding_file', 's'),
    HELP_TEXT: HELP_STRINGS[const.SHIELDING]},
  const.FLOOR_PLAN: {
    PREFIX: ('floor_plan', 'f'),
    HELP_TEXT: HELP_STRINGS[const.FLOOR_PLAN]},
  const.SCALE: {
    PREFIX: ('scale',),
    DATA_TYPE: float,
    HELP_TEXT: HELP_STRINGS[const.SCALE]},
  const.ORIGIN: {
    PREFIX: ('origin',),
    DATA_TYPE: str_float_list,
    HELP_TEXT: HELP_STRINGS[const.ORIGIN]},
  const.EXPORT_DIR: {
    PREFIX: ('export_dir',),
    HELP_TEXT: HELP_STRINGS[const.EXPORT_DIR]},
  const.GRIDSIZE: {
    PREFIX: ('grid_size',),
    DATA_TYPE: float,
    HELP_TEXT: HELP_STRINGS[const.GRIDSIZE]},
  const.XY: {
    PREFIX: ('xy',),
    DATA_TYPE: str,
    HELP_TEXT: HELP_STRINGS[const.XY]},
  const.CLIM_HEATMAP: {
    PREFIX: ('clim_heatmap',),
    DATA_TYPE: str_float_list,
    HELP_TEXT: HELP_STRINGS[const.CLIM_HEATMAP]},
  const.COLORMAP: {
    PREFIX: ('colormap',),
    HELP_TEXT: HELP_STRINGS[const.COLORMAP]},
  const.SHOW: {
    PREFIX: ('show',),
    CHOICES: ('all', 'sum', 'none'),
    HELP_TEXT: HELP_STRINGS[const.SHOW]},
  const.SAVE_IMAGES: {
    PREFIX: ('save_images',),
    CHOICES: (False, True),
    HELP_TEXT: HELP_STRINGS[const.SAVE_IMAGES]},
  const.IMAGE_DPI: {
    PREFIX: ('image_dpi',),
    DATA_TYPE: int,
    HELP_TEXT: HELP_STRINGS[const.IMAGE_DPI]},
  const.SAVE_DATA: {
    PREFIX: ('dump_file',),
    HELP_TEXT: HELP_STRINGS[const.SAVE_DATA]},
  const.MULTI_CPU: {
    PREFIX: ('multi_cpu',),
    CHOICES: (0, 1),
    DATA_TYPE: int,
    HELP_TEXT: HELP_STRINGS[const.MULTI_CPU]},
  const.PYTHAGORAS: {
    PREFIX: ('pythagoras',),
    CHOICES: (0, 1),
   DATA_TYPE: int,
    HELP_TEXT: HELP_STRINGS[const.PYTHAGORAS]},
  const.ISO_VALUES: {
    PREFIX: ('iso_values',),
    DATA_TYPE: str_float_list,
    HELP_TEXT: HELP_STRINGS[const.ISO_VALUES]},
  const.ISO_COLORS: {
    PREFIX: ('iso_colors',),
    DATA_TYPE: str_list,
    HELP_TEXT: HELP_STRINGS[const.ISO_COLORS]},
  const.DISABLE_BUILDUP: {
    PREFIX: ('disable_buildup',),
    CHOICES: (0, 1),
    DATA_TYPE: int,
    HELP_TEXT: HELP_STRINGS[const.DISABLE_BUILDUP]},
  const.CALCULATE: {
    PREFIX: ('calculate',),
    CHOICES: (0, 1),
    DATA_TYPE: int,
    HELP_TEXT: HELP_STRINGS[const.CALCULATE]},
  const.LOG: {
    PREFIX: ('log',),
    CHOICES: (const.LOG_INFO, const.LOG_DEBUG),
    HELP_TEXT: HELP_STRINGS[const.LOG]}
    }
