# -*-   coding: utf-8 -*-
"""
Created on Fri 2 11:50:40 2016

@author: M. Segbers
"""

import numpy as np
import math

from pyshield.calculations.line_intersect import intersect_line, angle_between_lines
from pyshield import get_setting



from pyshield import CONST, log

def sum_shielding_line(source_location, location, shielding, pythagoras = True):
    """ Calculates the amount of shielding between two points source_location
        and location. Shielding is a dictopnary. If pythagoras is True the
        total effective thickness is calculated by taking the angle of
        intersection into account. Returns a dictionary:

        {MATERIAL1: THICKNESS1, MATERIAL2: THICKNESS2,...}

        Thickness is the total (summed) thickness of the material between
        source_location and location
        """
    # Line between the source location and the specified location
    L0 = np.array((source_location, location))
    # list of points with intersections
    points = []

    # total amount of shielding between location and   source location
    shielding_line = {}

    #iterate over shielding all defined barriers,
    for name, barrier in shielding.items():
        log.debug('Intersection %s?', name)
        location = np.array(barrier[CONST.LOCATION])


        #line for barrier
        L1 = np.array((location[0:2], location[2:4]))

        #check for intersection
        p = intersect_line(L0, L1)


        # None: no intersection
        # NaN: parellel lines, no intersection
        # if p already in points list disregard this intersection.
        # example line ((0,0),(1,0)) and line ((0,0),(0,1)) if there is an
        # intersection at (0,0) with another then only one should count. i.e.
        # the point list should contain unique points


        if not(None in p) and not(np.NaN in p) and not p in points:
            points.append(p) # valid intersection at point p
            log.debug('Intersection at: ' + str(p))

            # calculate the angle of intersection or assume 90 degrees
            if pythagoras:
                theta = angle_between_lines(L0, L1)
            else:
                theta = 0.5 * math.pi

            # Add thickness and material to the sum of the total shielding
            # shielding is summed for each material seperately
            for material, thickness in barrier[CONST.MATERIAL].items():
                # check if material already was found if not so add
                # material as key
                if not material in shielding_line.keys():
                    shielding_line[material] = 0

                # add effective thickness for material
                eff_thickness =  thickness / math.sin(theta)
                shielding_line[material] += eff_thickness
                log.debug('Eff. Thickness of barrier: %s', eff_thickness)

    return shielding_line



def add_barriers(barrier1, barrier2):
    """ Function to add two barrier dictionaries. If material is present in
    both, the combined thickness is set """

    barrier = barrier1.copy()
    for material in barrier.keys():
        if material in barrier2.keys():
            barrier[material] += barrier2[material]
    for material in barrier2.keys():
        if material not in barrier.keys():
            barrier[material] = barrier2[material]
    return barrier


def add_floor():
  """ Add shielding to the source to simulate the shielding of the
      ceiling or floor """
  sources         = get_setting(CONST.SOURCES)
  floor_shielding = get_setting(CONST.FLOOR)[CONST.MATERIAL]


  for source in sources.values():
     source_shielding = source.get(CONST.MATERIAL, {})
     source[CONST.MATERIAL] = add_barriers(source_shielding, floor_shielding)







