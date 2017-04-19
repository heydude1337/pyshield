# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 17:24:32 2016

@author: 757021
"""
from pyshield import CONST
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
  CONST.SOURCES:        'Specify a yaml file containing the information of the present sources',
  CONST.SHIELDING:      'Specify a yaml file containing the information of the present shielding',
  CONST.FLOOR_PLAN:     'Specify an image file of the floor plan for the calculation',
  CONST.SCALE:          'Specify the scale of the floorplan in cm/pixel',
  CONST.ORIGIN:         'Specify the origin in pixels: x,y (no space around the comma)',
  CONST.EXPORT_DIR:     'Specify a directory to which results (data and images) will be saved',
  CONST.GRIDSIZE:       'Specify the distance between grid points in pixels',
  CONST.POINTS:         'Specify a yaml file with points for which the dos will be calculated',
  CONST.CLIM_HEATMAP:   'Specify the clim for the heatmap: low,high (notice no space)',
  CONST.COLORMAP :      'Specify the colormap (any valid matplotlib colormap name)',
  CONST.SHOW :          'Display the results of grid calculations in a nice figure. Show all sources seperately (all), show the summed dose (sum), or disable showing (none)',
  CONST.SAVE_IMAGES :   'Save displayed images as PNG',
  CONST.IMAGE_DPI :     'Specify the DPI for the saved images',
  CONST.SAVE_DATA :     'Save a (pickle) dump of the data to binary file',
  CONST.MULTI_CPU :     'Perform calculations on all availabel cpu cores. Disable to debug errors',
  CONST.PYTHAGORAS :    'When enabled the effective thickness of the barrier is calculated taking into account the angle of intersection.',
  CONST.ISO_VALUES :    'Isocontours for these dose values will be drawn. Number of values must match number of colors',
  CONST.ISO_COLORS :    'Colors for the isocontours. Number of colors must match number of values',
  CONST.DISABLE_BUILDUP :   'When True buildup will be disabled (testing purpuses)',
  CONST.CALCULATE :     'Perform calculation',
  CONST.LOG:           'Set log level (info or debug), debug will slow down the calculations considerably'}

# parse comma seperated values to a list (no spaces should be in the string)
# 1.0,2,5,4.5 will be converted to [1.0, 2, 5, 4.5]
str_float_list = lambda s: [float(item) for item in s.replace('"', "").split(',')]
str_list = lambda s: [item for item in s.replace('"', "").split(',')]

DATA_TYPES = {
   CONST.SCALE:             float,
   CONST.ORIGIN:            str_float_list,
   CONST.GRIDSIZE:          float,
   CONST.CLIM_HEATMAP:      str_float_list,
   CONST.COLORMAP :         str_list,
   CONST.SAVE_IMAGES :      int,
   CONST.IMAGE_DPI :        int,
   CONST.MULTI_CPU :        int,
   CONST.PYTHAGORAS :       int,
   CONST.ISO_VALUES :       str_float_list,
   CONST.ISO_COLORS :       str_list,
   CONST.DISABLE_BUILDUP :  int}


SHORT_PREFIX = {CONST.SOURCES:    'src',
                CONST.SHIELDING:  's',
                CONST.FLOOR_PLAN: 'f',
                CONST.POINTS:     'p'}

CHOICE_ITEMS = {CONST.SHOW: ('all', 'sum', 'none'),
                CONST.SAVE_IMAGES: (0,1),

                CONST.MULTI_CPU: (0,1),
                CONST.PYTHAGORAS: (0,1),
                CONST.DISABLE_BUILDUP: (0, 1),
                CONST.CALCULATE: (CONST.POINTS, CONST.GRID),
                CONST.LOG: (CONST.LOG_INFO, CONST.LOG_DEBUG)}

COMMAND_LINE_ARGS = {}
for key, help_text in HELP_STRINGS.items():
  entry = {HELP_TEXT: help_text}
  if key in DATA_TYPES.keys():
    entry[DATA_TYPE] = DATA_TYPES[key]
  if key in CHOICE_ITEMS:
    entry[CHOICES] = CHOICE_ITEMS[key]
  if key in SHORT_PREFIX.keys():
    entry[PREFIX] = (key, SHORT_PREFIX[key])
  else:
    entry[PREFIX] = (key,)

  COMMAND_LINE_ARGS[key] = entry

#COMMAND_LINE_ARGS = {
#
#
#
#
#  CONST.DISABLE_BUILDUP: {
#    PREFIX: ('disable_buildup',),
#    CHOICES: (0, 1),
#    DATA_TYPE: int,
#    HELP_TEXT: HELP_STRINGS[CONST.DISABLE_BUILDUP]},
#  CONST.CALCULATE: {
#    PREFIX: ('calculate',),
#    CHOICES: (0, 1),
#    DATA_TYPE: int,
#    HELP_TEXT: HELP_STRINGS[CONST.CALCULATE]},
#  CONST.LOG: {
#    PREFIX: ('log',),
#    CHOICES: (CONST.LOG_INFO, CONST.LOG_DEBUG),
#    HELP_TEXT: HELP_STRINGS[CONST.LOG]}
#    }
