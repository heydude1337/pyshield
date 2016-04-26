# -*- coding: utf-8 -*-
"""
Make a grid and calculate the dose for each source (specified in sources.yml) 
on each point of the grid.

Last Updated 05-02-2016
"""
import numpy as np
from pyshield import const, prefs, data, log
import pyshield.calculations.isotope as calc_isotope
import pyshield.calculations.xray as calc_xray



def calc_dose_grid_source(source, grid = None):
  """ Calculate a dosemap for a given source and shielding on grid.
  
      x:          2D numpy matrix with x-coordinates of the grid
      y:          2D numpy matrix with y-coordinates of the grid
      source:     dictonary specifying the source properties
      shielding:  dictonary containing all shielding elements
    
    """
 

  if grid is None: grid= make_grid(step_size = prefs[const.GRIDSIZE]) 
  shielding = data[const.SHIELDING]
  
  # calculate x-ray (CT) or calculate isotopes
  if source[const.TYPE] == const.ISOTOPE:
    dose_map = calc_isotope.calc_dose_source_on_grid(source, grid)
  elif source[const.TYPE] == const.XRAY_SECONDARY:
    dose_map = np.zeros(grid[0].shape)
    calc_func = calc_xray.calc_dose_source_at_location
    for xi, yi, di in np.nditer((grid[0], grid[1], dose_map), op_flags = ('readwrite',)):
      di[...] = calc_func(source, (xi,yi), shielding)
  else:
    print('Unknown source type: ' + source[const.TYPE])
    raise

  return dose_map
    

def calc_dose_grid_sources(sources, grid = None):
  dose_maps = {}
  if grid is None: grid= make_grid(step = const.GRIDSIZE)  
  
  for key, source in sources.items():
    print('Calculating: ' + key)    
    dose_maps[key] = calc_dose_grid_source(source, grid = grid, name = key)   
  return dose_maps
  
def sum_dose(dose_maps):
  if dose_maps == {}: return None
  total_dose = np.zeros(dose_maps[list(dose_maps.keys())[0]].shape)  
  for key, dose_map in dose_maps.items():
    total_dose += dose_map
  
  return total_dose

def make_grid(step_size = 1):
    log.debug('Making grid with step size: ' + str(step_size))
    xmin, xmax = (0, data[const.FLOOR_PLAN].shape[1]) 
    ymin, ymax = (0, data[const.FLOOR_PLAN].shape[0])
    
    """ defines a grid within a specified extent (xmin, xmax, ymin, ymax) """    
    xi = np.linspace(xmin + 0.5 * step_size, xmax - 0.5 * step_size, round((xmax-xmin)/step_size))
    yi = np.linspace(ymin + 0.5 * step_size, ymax - 0.5 * step_size, round((ymax-ymin)/step_size))
    
    x,y = np.meshgrid(xi, yi)
    x = x * data[const.SCALE] - prefs[const.ORIGIN][0]
    y = y * data[const.SCALE] - prefs[const.ORIGIN][1]
    return (x,y)

#def calc_dose_map(sources, shielding, xmin, xmax, ymin, ymax, step=1):  
#    """ Make a grid and perform calculations over this grid 
#       
#        xmin, xmax:  range of x-coordinates for grid
#        ymin, ymax:  range of y-coordinates for grid
#        step:  gridsize, default 1"""
#    
#
#
#    extent = (xmin, xmax, ymin, ymax)
#    x, y = make_grid(extent = extent, step=step)
#
#   
#    dosemap = calc_dose_grid_sources(x, y, sources, shielding)
#
#    return dosemap
   
    

  