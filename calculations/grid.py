# -*- coding: utf-8 -*-
"""
Make a grid and calculate the dose for each source (specified in sources.yml)
on each point of the grid.

Last Updated 05-02-2016
"""
import numpy as np
from pyshield import const, prefs, data, log
from pyshield.calculations.isotope import calc_dose_source_at_location
#import pyshield.calculations.xray as calc_xray
from scipy.interpolate import griddata
from pyshield.calculations.barrier import add_barriers



def calculate_dose_map_for_source(source):
    if const.FLOOR in prefs.keys() and const.MATERIAL in prefs[const.FLOOR].keys():
      floor = prefs[const.FLOOR]

      source[const.MATERIAL] = add_barriers(floor[const.MATERIAL], 
                                            source[const.MATERIAL])
  
  
    
    log.debug('Material:  ' + str(source[const.MATERIAL]))
  
    shielding = data[const.SHIELDING]
    if source[const.TYPE] == const.ISOTOPE:
        calc_dose = lambda p: calc_dose_source_at_location(source, p,
                                                           shielding)
    else:
        print('Unknown source type: {0}'.format(source[const.TYPE]))
        raise KeyError

    points, grid = grid_points(source)
    dose_points = np.zeros(len(points))
    for i, point in enumerate(points):
        dose_points[i] = calc_dose(point)

    if prefs[const.GRID] == const.CARTESIAN:
        
        dose_map = dose_points.reshape(grid[0].shape)

    if prefs[const.GRID] == const.POLAR:
        # interpolate dose_points to rectangular grid
        dose_map = griddata(points, dose_points, grid)

    return (dose_map, points, grid)


def grid_points(source):
    """ Create a grid and list of points based on set preferences """
    source_location = np.array(source[const.LOCATION])
    grid_type       = prefs[const.GRID]
    scale           = data[const.SCALE]

    origin          = np.array(data[const.ORIGIN])
    matrix_size     = np.array(data[const.FLOOR_PLAN].shape)
    grid_spacing    = prefs[const.GRIDSIZE]
    span            = matrix_size[0:2] * scale

    area = ((-origin[0], span[1] - origin[0]),
            (-origin[1], span[0] - origin[1]))

    
    X, Y = cartesian_grid(area = area,
                          spacing = grid_spacing)

    if grid_type == 'cartesian':
      points = np.stack((X.flatten(), Y.flatten())).T

    elif grid_type == const.POLAR:
        n_angles    = prefs[const.NANGLES]

        points = polar_points(r_spacing = grid_spacing,
                              n_angles = n_angles,
                              span = span,
                              origin = origin - source_location)
        
        points[:,0] += origin[0]
        points[:,1] += origin[1]
        
        outside_bounds = np.sum((points[:,0] < area[0][0],
                                 points[:,1] < area[1][0],
                                 points[:,0] > area[0][1],
                                 points[:,1] > area[1][1]),
                                axis = 0) > 0

        points = points[np.logical_not(outside_bounds), :]
                    
    else:
        print('Cannot make grid for: {0}'.format(grid_type))
        raise KeyError
    return (points, (X,Y))

def cartesian_grid(area = ((0, 100),(0, 100)), spacing = 1):
   """returns a list of points of equally spaced points for a given area """

   xi = np.linspace(area[0][0], area[0][1],
                     np.ceil((area[0][1] - area[0][0]) / spacing))

   yi = np.linspace(area[1][0], area[1][1],
                     np.ceil((area[1][1] - area[1][0]) / spacing))

   X, Y = np.meshgrid(xi, yi)

   return X, Y

def polar_points(r_spacing, n_angles = 100, origin = (0, 0), span = (10, 10),
                 grid = 'quadratic' ):


    rmax = (span[0] **2 + span[1]**2) ** 0.5

    if grid.lower() == 'quadratic':
        ri = r_spacing * np.linspace(1, np.ceil(rmax / r_spacing),
                                     np.ceil(rmax/r_spacing)) ** 2
        ri = ri[ri<=rmax]
    else:
        ri = r_spacing * np.linspace(1, np.ceil(rmax/r_spacing),
                                     np.ceil(rmax/r_spacing))

    theta_i = np.linspace(0, 2 * np.pi, n_angles, endpoint = False)

    R, Theta = np.meshgrid(ri, theta_i)

    X, Y = ((R * np.sin(Theta))  - origin[0],
            (R * np.cos(Theta))  - origin[1])

    points = np.stack((X.flatten(), Y.flatten())).T

    

    return points

#
