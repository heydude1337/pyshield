# -*- coding: utf-8 -*-
"""
Make a grid and calculate the dose for each source (specified in sources.yml)
on each point of the grid.

Last Updated 05-02-2016
"""
import numpy as np
from scipy.interpolate import griddata

import pyshield as ps

from pyshield.calculations.isotope import calc_dose_source_at_location


def calculate_dose_map_for_source(source):
    """ Calculate a dose map in mSv for a specified source. Dose map is
    calculated on a grid, grid type and size is specified in the application
    configuration (data and prefs) """


    ps.logger.debug('Material:  %s', source.get(ps.MATERIAL, {}))


    barriers = ps.config.get_setting(ps.BARRIERS)

    part_config_items = (ps.FLOOR,
                         ps.HEIGHT,
                         ps.DISABLE_BUILDUP,
                         ps.INTERSECTION_THICKNESS)

    kwargs = dict([(key, ps.config.get_setting(key)) for key in part_config_items])


    if not(isinstance(source[ps.TYPE], (list, tuple))):
       source[ps.TYPE] = [source[ps.TYPE]]

    if not(ps.ISOTOPE in source[ps.TYPE]):
        raise KeyError('Unknown source type: {0}'.format(source[ps.TYPE]))

    calc_dose = lambda loc: calc_dose_source_at_location(source,
                                                         loc,
                                                         barriers,
                                                         **kwargs)
    # obtain grid points for the specified source
    points, grid = grid_points(source)

    # pre allocate memory for dose points
    dose_points = np.zeros(len(points))

    for i, point in enumerate(points):
        dose_points[i] = calc_dose(point)

    # resample dose points to a cartesian grid
    if ps.config.get_setting(ps.GRID) == ps.CARTESIAN:
        # points already on cartesian grid
        dose_map = dose_points.reshape(grid[0].shape)
    if ps.config.get_setting(ps.GRID) == ps.POLAR:
        # interpolate dose_points to rectangular grid
        dose_map = griddata(points, dose_points, grid)

    return (dose_map, points, grid)


def grid_points(source):
    """ Create a grid and list of points based on set preferences """
    grid_type       = ps.config.get_setting(ps.GRID)
    scale           = ps.config.get_setting(ps.SCALE)

    source_location = np.array(source[ps.LOCATION])

    origin          = np.array(ps.config.get_setting(ps.ORIGIN))
    floor_plan      = ps.config.get_setting(ps.FLOOR_PLAN)
    matrix_size     = np.array(floor_plan.shape)
    grid_spacing    = ps.config.get_setting(ps.GRIDSIZE)
    span            = matrix_size[0:2] * scale

    area = ((-origin[0], span[1] - origin[0]),
            (-origin[1], span[0] - origin[1]))

    ps.logger.debug('area: %s', area)
    X, Y = cartesian_grid(area=area, spacing=grid_spacing)

    if grid_type == 'cartesian':
        points = np.stack((X.flatten(), Y.flatten())).T

    elif grid_type == ps.POLAR:
        n_angles = ps.config.get_setting(ps.NANGLES)

        points = polar_points(r_spacing=grid_spacing,
                              n_angles=n_angles,
                              span=span,
                              origin=origin - source_location)

        points[:, 0] += origin[0]
        points[:, 1] += origin[1]

        outside_bounds = np.sum((points[:, 0] < area[0][0],
                                 points[:, 1] < area[1][0],
                                 points[:, 0] > area[0][1],
                                 points[:, 1] > area[1][1]),
                                axis=0) > 0

        points = points[np.logical_not(outside_bounds), :]

    else:
        print('Cannot make grid for: {0}'.format(grid_type))
        raise KeyError
    return (points, (X, Y))

def cartesian_grid(area=((0, 100), (0, 100)), spacing=1):
    """returns a list of points of equally spaced points for a given area """

    xi = np.linspace(area[0][0], area[0][1],
                     np.ceil((area[0][1] - area[0][0]) / spacing))

    yi = np.linspace(area[1][0], area[1][1],
                     np.ceil((area[1][1] - area[1][0]) / spacing))

    X, Y = np.meshgrid(xi, yi)

    return X, Y

def polar_points(r_spacing, n_angles=100, origin=(0, 0), span=(10, 10),
                 grid='quadratic'):


    rmax = (span[0] **2 + span[1]**2) ** 0.5

    if grid.lower() == 'quadratic':
        ri = r_spacing * np.linspace(1, np.ceil(rmax / r_spacing),
                                     np.ceil(rmax/r_spacing)) ** 2
        ri = ri[ri <= rmax]
    else:
        ri = r_spacing * np.linspace(1, np.ceil(rmax/r_spacing),
                                     np.ceil(rmax/r_spacing))

    theta_i = np.linspace(0, 2 * np.pi, n_angles, endpoint=False)

    R, Theta = np.meshgrid(ri, theta_i)

    X, Y = ((R * np.sin(Theta))  - origin[0],
            (R * np.cos(Theta))  - origin[1])

    points = np.stack((X.flatten(), Y.flatten())).T

    return points

def sum_dose_maps(dose_maps):
    """ sum a collection of dose maps to obtain the total dose """
    ps.logger.debug('Summing %s dose_maps', len(dose_maps))
    dose_maps = np.stack(dose_maps)
    return np.nansum(dose_maps, axis=0)


if __name__ == "__main__":
  import matplotlib.pyplot as plt
  points = polar_points(1, n_angles = 45, origin = (0,0), span = (100,100))
  for point in points:
    plt.plot(*point, 'ro')



