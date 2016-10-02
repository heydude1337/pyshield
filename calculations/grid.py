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


  if grid is None: grid= make_cartesian_grid(step_size = prefs[const.GRIDSIZE])
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



def sum_dose(dose_maps):
  if dose_maps == {}: return None
  total_dose = np.zeros(dose_maps[list(dose_maps.keys())[0]].shape)
  for key, dose_map in dose_maps.items():
    total_dose += dose_map

  return total_dose

def make_cartesian_grid(step_size = 1):
    log.debug('Making grid with step size: ' + str(step_size))
    xmin, xmax = (0, data[const.FLOOR_PLAN].shape[1])
    ymin, ymax = (0, data[const.FLOOR_PLAN].shape[0])

    """ defines a grid within a specified extent (xmin, xmax, ymin, ymax) """
    xi = np.linspace(xmin + 0.5 * step_size, xmax - 0.5 * step_size, round((xmax-xmin)/step_size))
    yi = np.linspace(ymin + 0.5 * step_size, ymax - 0.5 * step_size, round((ymax-ymin)/step_size))

    x,y = np.meshgrid(xi, yi)
    x = x * data[const.SCALE] - data[const.ORIGIN][0]
    y = y * data[const.SCALE] - data[const.ORIGIN][1]
    return (x,y)

def calc_dose_polar(source, r = None, angles = None):
  if const.RMIN in data.keys():
    rmin = data[const.RMIN]
  else:
    log.warning('rmin is not defined setting to 1 cm')
    rmin = 1

  if const.NANGLES in data.keys():
    rmin = data[const.NANGLES]
  else:
    log.warning('number of angles is not defined setting to 360')
    nangles = 360

  r = make_radius(r_min = 100)


  angles = np.linspace(0, 2 * np.pi, nangles, endpoint = False)
  R, Theta = np.meshgrid(r, angles)
  X,Y = (R * np.sin(Theta), R * np.cos(Theta))
  X = X  - data[const.ORIGIN][0]
  Y = Y  - data[const.ORIGIN][1]
  #dose_maps = {}
  #for name, source in sources.items():

  location = source[const.LOCATION]
  grid = (X + location[0], Y+location[1])

  dose_map_p = calc_isotope.calc_dose_source_on_grid(source, grid)

  cgrid = make_cartesian_grid(step_size=prefs[const.GRIDSIZE])
  cgrid = (cgrid[0] - location[0], cgrid[1] - location[1])
  dose_map = polar_to_cart(dose_map_p, 1, rmin, *cgrid )
  return (grid, dose_map_p)

def make_radius(r_min):
  log.debug('Making polar grid ' )
  xmax =  data[const.FLOOR_PLAN].shape[1] * data[const.SCALE]
  ymax =  data[const.FLOOR_PLAN].shape[0] * data[const.SCALE]

  r_max = (xmax ** 2 + ymax ** 2) ** 0.5
  #r = (np.linspace(1, r_max/r_min, num = np.ceil(r_max/r_min)) ** 2) * r_min
  #r = r[r<=r_max]
  return np.linspace(1, np.ceil(r_max/r_min), np.ceil(r_max/r_min)) * r_min
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


# Auxiliary function to map polar data to a cartesian plane
# src: http://stackoverflow.com/questions/2164570/reprojecting-polar-to-cartesian-grid
def polar_to_cart(polar_data, theta_step, range_step, X, Y, order=3):

    from scipy.ndimage.interpolation import map_coordinates as mp

    # "x" and "y" are numpy arrays with the desired cartesian coordinates
    # we make a meshgrid with them
    #X, Y = np.meshgrid(x, y)

    # Now that we have the X and Y coordinates of each point in the output plane
    # we can calculate their corresponding theta and range
    Tc = np.degrees(np.arctan2(Y, X)).ravel()
    Rc = (np.sqrt(X**2 + Y**2)).ravel()

    # Negative angles are corrected
    Tc[Tc < 0] = 360 + Tc[Tc < 0]

    # Using the known theta and range steps, the coordinates are mapped to
    # those of the data grid
    Tc = Tc / theta_step
    Rc = Rc / range_step

    # An array of polar coordinates is created stacking the previous arrays
    coords = np.vstack((Tc, Rc))

    # To avoid holes in the 360º - 0º boundary, the last column of the data
    # copied in the begining
    polar_data = np.vstack((polar_data, polar_data[-1,:]))

    # The data is mapped to the new coordinates
    # Values outside range are substituted with nans
    cart_data = mp(polar_data, coords, order=order, mode='constant', cval=-1)

    # The data is reshaped and returned
    return(cart_data.reshape(X.shape))


