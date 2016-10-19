# -*- coding: utf-8 -*-
from pyshield.calculations.grid import grid_points
from pyshield.calculations.isotope import transmission_sum
from pyshield import const, resources
import numpy as np


def d

def project3D(dose_maps, sources, floor_barrier, distance):
  dose_maps3D = {}
 
  for sname, source in sources.items():
    isotope = source[const.ISOTOPE]
    print(sname)
    source_location = source[const.LOCATION]
    p, grid = grid_points(source)
    
    Rxy = ((grid[0] - source_location[0])**2 + \
            (grid[1] - source_location[1])**2) ** 0.5
           
    Rxyz = (Rxy **2 + distance ** 2) ** 0.5
           
    
    T = transmission_sum(floor_barrier, isotope)
    


    
    
    dose_map    = dose_maps[sname][2]
    dose_map3D  = np.copy(dose_map)
    dose_map3D *= ((Rxy/Rxyz) **2)
    dose_map3D *= np.max(T)
    dose_maps3D[sname] = ((Rxy/Rxyz)**2, T, dose_map3D)
   
  return dose_maps3D

  

  
  