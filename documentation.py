# -*- coding: utf-8 -*-

from collections import OrderedDict
from pyshield import const
LINE_LENGTH = 50
KW_COLUMN_LENGTH = 20

import textwrap 
DOC_STRINGS = \
 ((const.SOURCES,            'Specify a yaml file containing the information of the present sources'),
  (const.SHIELDING,          'Specify a yaml file containing the information of the present shielding'),
  (const.FLOOR_PLAN,         'Specify an image file of the floor plan for the calculation'),
  (const.SCALE,              'Specify the scale of the floorplan in cm/pixel'),
  (const.ORIGIN,             'Specify the origin in pixels: x,y (no space around the comma)'),
  (const.EXPORT_DIR,         'Specify a directory to which results (data and images) will be saved'),
  (const.GRIDSIZE,           'Specify the distance between grid points in pixels'),
  (const.XY,                 'Specify a yaml file with points for which the dos will be calculated'),
  (const.CLIM_HEATMAP,       'Specify the clim for the heatmap: low,high (notice no space)'),
  (const.COLORMAP,           'Specify the colormap (any valid matplotlib colormap name)'),
  (const.SHOW,               'Display the results of grid calculations in a nice figure. Show all sources seperately (all), show the summed dose (sum), or disable showing (none)'),
  (const.MULTI_CPU,          'Perform calculations on all availabel cpu cores. Disable to debug errors'),
  (const.PYTHAGORAS,         'When enabled the effective thickness of the barrier is calculated taking into account the angle of intersection.'),
  (const.ISO_VALUES,         'Isocontours for these dose values will be drawn. Number of values must match number of colors'),
  (const.ISO_COLORS,         'Colors for the isocontours. Number of colors must match number of values'),
  (const.DISABLE_BUILDUP,    'When True buildup will be disabled (testing purpuses)'),
  (const.CALCULATE,          'Perform calculation'),
  (const.LOG,                'Set log level (info or debug), debug will slow down the calculations considerably'))
  
__doc__  = \
"""Pyshield (r) 
written by: M.Segbers
Version:    2.0
Date:       18-10-2016

"""

split_line = '.{1,' + str(LINE_LENGTH - KW_COLUMN_LENGTH) + '}'
single_line = '{0:30} {1}\n'

def nice_split(string):
  words = string.split(' ')
  
  def line(start):
    l = ''
    for index in range(start, len(words)):
      if len(l + ' '  +  words[index]) < LINE_LENGTH:
        l += ' ' + words[index]
      else:
        end = index
        return l, end
    return l[1:], -1
  
  lines = []
  start = 0
  while start >= 0:
    newline, start =line(start)
    lines += [newline]

  return lines
               
                
for kw, description in OrderedDict(DOC_STRINGS).items():
  if len(description) < LINE_LENGTH:
    __doc__+= single_line.format(kw +':', description) 
  else:
    description = nice_split(description)
    __doc__+= single_line.format(kw + ':', description[0])
    for line in description[1:]:
      __doc__ += single_line.format('', line) 
    #print(description)
  __doc__ += '\n'
  
  
  
if __name__ == "__main__":
  print(__doc__)
  pass