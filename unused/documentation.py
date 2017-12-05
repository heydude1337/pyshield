# -*- coding: utf-8 -*-

from collections import OrderedDict
from pyshield import CONST
LINE_LENGTH = 50
KW_COLUMN_LENGTH = 20


DOC_STRINGS = \
 ((CONST.SOURCES,            'Specify a yaml file containing the information of the present sources.'),
  (CONST.SHIELDING,          'Specify a yaml file containing the information of the present shielding.'),
  (CONST.FLOOR_PLAN,         'Specify an image file of the floor plan for the calculation.'),
  (CONST.SCALE,              'Specify the scale of the floorplan in cm/pixel'),
  (CONST.ORIGIN,             'Specify the origin in pixels: x,y (no space around the comma).'),
  (CONST.EXPORT_DIR,         'Specify a directory to which results (data and images) will be saved'),
  (CONST.GRID,               'Specify grid to be \'polar\' or \'cartesian\'. Polar grid sampling provides faster calculations.'),
  (CONST.GRIDSIZE,           'Specify the sampling distance for the grid. For cartesian girds the distance is equal to the grid_size parameter. For polar grid grids, the grid_size determines the radial diastance between points.'),
  (CONST.NANGLES,            'Specify the number of angles for polar grid sampling.'),
  (CONST.POINTS,             'Specify a yaml file with points for which the dos will be calculated'),
  (CONST.CLIM_HEATMAP,       'Specify the clim for the heatmap: low,high (notice no space)'),
  (CONST.COLORMAP,           'Specify the colormap (any valid matplotlib colormap name)'),
  (CONST.SHOW,               'Display the results of grid calculations in a nice figure. Show all sources seperately (all), show the summed dose (sum), or disable showing (none)'),
  (CONST.MULTI_CPU,          'Perform calculations on all availabel cpu cores. Disable to debug errors'),
  (CONST.PYTHAGORAS,         'When enabled the effective thickness of the barrier is calculated taking into account the angle of intersection.'),
  (CONST.DISABLE_BUILDUP,    'When True buildup will be disabled (testing purpuses)'),
  (CONST.CALCULATE,          'Perform calculation'),
  (CONST.LOG,                'Set log level (info or debug), debug will slow down the calculations considerably'),
  (CONST.FLOOR,              'Calculate the dosemap for a floor above or below the source(s) by passing a dict with keys \'{height}\' (specifying the additional height in cm) and \'{materials}\' specifying the additional shielding'.format(materials = CONST.MATERIALS, height=CONST.HEIGHT)))




TYPES = dict(
  ((CONST.SOURCES,           'string'),
  (CONST.SHIELDING,          'string'),
  (CONST.FLOOR_PLAN,         'string'),
  (CONST.SCALE,              'float'),
  (CONST.ORIGIN,             'float, float'),
  (CONST.EXPORT_DIR,         'string'),
  (CONST.GRIDSIZE,           'float'),
  (CONST.NANGLES,            'int'),
  (CONST.GRID,               'string'),
  (CONST.POINTS,             'string'),
  (CONST.CLIM_HEATMAP,       'min, max'),
  (CONST.COLORMAP,           'string'),
  (CONST.SHOW,               'boolean'),
  (CONST.MULTI_CPU,          'boolean'),
  (CONST.PYTHAGORAS,         'boolean'),
  (CONST.DISABLE_BUILDUP,    'boolean'),
  (CONST.CALCULATE,          'boolean'),
  (CONST.LOG,                'string'),
  (CONST.FLOOR,              'dict')))




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
""".format(shielding = CONST.SHIELDING,
           source = CONST.SOURCES,
           floorplan = CONST.FLOOR_PLAN)



doc_line = '{0:30} {1}\n'

def nice_split(string, line_length = LINE_LENGTH):
  """ Splits a string to multiple lines """
  words = string.split(' ')

  lines = ['']
  for word in words:
    new_line = lines[-1] + word
    if len(new_line) < line_length:
      # just add word to current line
      lines[-1] = new_line + ' '
    else:
      # create a new line starting with word
      lines += [word]
  return lines


for kw, description in OrderedDict(DOC_STRINGS).items():
  description = nice_split(description)

  type_name = ' (' + TYPES[kw] + '):'

  for line in description:
    if line == description[0]:
      __doc__+= doc_line.format(kw + type_name, line)
    else:
      __doc__ += doc_line.format('', line)





if __name__ == "__main__":
  print(__doc__)
  pass