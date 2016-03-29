# -*- coding: utf-8 -*-
"""
Created on Fri 2 11:50:40 2016

@author: M. Segbers
"""

from pyshield.calculations.line_intersect import intersect_line, angle_between_lines
import numpy as np
import math

from pyshield import const, prefs, data, log

def sum_shielding_line(source_location, location, shielding):
    """ Calculates the amount of shielding between two points source_location en location
        shielding is a dictopnary. If pythagoras is True the total effective thickness 
        is calculated by taking the angle of intersection into account. Returns a 
        dictionary:

        {MATERIAL1: THICKNESS1, MATERIAL2: THICKNESS2,...}
        
        Thickness is the total (summed) thickness of the material between source_location 
        and location        
        """
    # Line between the source location and the specified location
    L0 = np.array((source_location, location))    
    points = []  
    shielding_line={} 
    
    #iterate over shielding items, each item has a thickness, material and
    #location key specyfiying a line element
    for key, item in shielding.items(): 
        log.debug('Intersection? ' + key)
        location = item[const.LOCATION]
        
        #simple line element
        L1=np.array((location[0:2], location[2:4]))
        
        #check for intersection
        p = intersect_line(L0,L1)

        #None: no intersection, NaN: parellel lines, no intersection
        # if p already in points list disregard this intersection.
        #example line ((0,0),(1,0)) and line ((0,0),(0,1)) if there is an 
        #intersection at (0,0) with L0 then only one should count. i.e. the 
        #specifield shielding elements may not overlap!
        if not(None in p) and not(np.NaN in p) and not p in points:        
          points.append(p)
          log.debug('Intersection at: ' + str(p))
          # calculate the angle of intersection or assume 90 degrees
          if prefs[const.PYTHAGORAS]:
            theta = angle_between_lines(L0,L1)    
          else:
            theta = 0.5 * math.pi

          # Add thickness and material to the sum of the total shielding
          # shielding is summed for each material seperately
          for material, thickness in item[const.MATERIAL].items():
            #check if material already was found if not so add material as key            
            if not material in shielding_line.keys():
              shielding_line[material] = 0
            
            # add effective thickness for material
            eff_thickness =  thickness  / math.sin(theta)
            shielding_line[material]+= eff_thickness
            log.debug('Eff. Thickness of barrier: ' + str(eff_thickness))
  
    return shielding_line



  
  

    
    
    
    
    
    
    
    
  