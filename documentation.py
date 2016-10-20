# -*- coding: utf-8 -*-

from collections import OrderedDict
from pyshield import const
LINE_LENGTH = 50
KW_COLUMN_LENGTH = 20


DOC_STRINGS = \
 ((const.SOURCES,            'Specify a yaml file containing the information of the present sources.'),
  (const.SHIELDING,          'Specify a yaml file containing the information of the present shielding.'),
  (const.FLOOR_PLAN,         'Specify an image file of the floor plan for the calculation.'),
  (const.SCALE,              'Specify the scale of the floorplan in cm/pixel'),
  (const.ORIGIN,             'Specify the origin in pixels: x,y (no space around the comma).'),
  (const.EXPORT_DIR,         'Specify a directory to which results (data and images) will be saved'),
  (const.GRID,               'Specify grid to be \'polar\' or \'cartesian\'. Polar grid sampling provides faster calculations.'),
  (const.GRIDSIZE,           'Specify the sampling distance for the grid. For cartesian girds the distance is equal to the grid_size parameter. For polar grid grids, the grid_size determines the radial diastance between points.'),
  (const.NANGLES,            'Specify the number of angles for polar grid sampling.'),
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
  (const.LOG,                'Set log level (info or debug), debug will slow down the calculations considerably'),
  (const.FLOOR,              'Calculate the dosemap for a floor above or below the source(s) by passing a dict with keys \'{height}\' (specifying the additional height in cm) and \'{materials}\' specifying the additional shielding'.format(materials = const.MATERIALS, height=const.HEIGHT)),
  (const.AREA,               'If the floor_plan option is not used an empty area can be specified (width, height)'))
  
  

TYPES = dict(
  ((const.SOURCES,           'string'),
  (const.SHIELDING,          'string'),
  (const.FLOOR_PLAN,         'string'),
  (const.SCALE,              'float'),
  (const.ORIGIN,             'float, float'),
  (const.EXPORT_DIR,         'string'),
  (const.GRIDSIZE,           'float'),
  (const.NANGLES,            'int'),
  (const.GRID,               'string'),
  (const.XY,                 'string'),
  (const.CLIM_HEATMAP,       'min, max'),
  (const.COLORMAP,           'string'),
  (const.SHOW,               'boolean'),
  (const.MULTI_CPU,          'boolean'),
  (const.PYTHAGORAS,         'boolean'),
  (const.ISO_VALUES,         'list of floats'),
  (const.ISO_COLORS,         'list of colors'),
  (const.DISABLE_BUILDUP,    'boolean'),
  (const.CALCULATE,          'boolean'),
  (const.LOG,                'string'),
  (const.FLOOR,              'dict'),
  (const.AREA,               'list')))

            
                  
                  
__doc__  = \
"""Pyshield (r) 
written by: M.Segbers
Version:    2.0
Date:       18-10-2016

pyshield is a program to calculate dose rates in 2D for facalities that use
radioisotopes. Shielding can be specified using the {shielding} option. 
Sources are specified using the {source} option. The result is a 2D dosemap
that gives the dose for any point on the specified grid. The dosemap can be
displayed on top of a blueprint by using the {floorplan} option. Use the
run_with_configuration function to start the calculations.

Full list of arguments are listed below:\n\n
""".format(shielding = const.SHIELDING,
           source = const.SOURCES,
           floorplan = const.FLOOR_PLAN)
           


doc_line = '{0:30} {1}\n'

def nice_split(string):
  words = string.split(' ')
  
  def line(start):
    l = ''
    for index in range(start, len(words)):
      if len(l + ' '  +  words[index]) < LINE_LENGTH:
        l += ' ' + words[index]
      else:
        end = index
        return l[1:], end
    return l[1:], -1
  
  lines = []
  start = 0
  while start >= 0:
    newline, start =line(start)
    lines += [newline]

  return lines
               
                
for kw, description in OrderedDict(DOC_STRINGS).items():
  default = ' (' + TYPES[kw] + '):'
  if len(description) < LINE_LENGTH:
    __doc__+= doc_line.format(kw + default, description) 
  else:
    description = nice_split(description)
    
    __doc__+= doc_line.format(kw + default, description[0]) 
    for line in description[1:]:
      __doc__ += doc_line.format('', line) 
    #print(description)
  __doc__ += '\n'
  
  
  
if __name__ == "__main__":
  print(__doc__)
  pass