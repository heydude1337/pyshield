# -*- coding: utf-8 -*-
from pyshield.calculations.grid import grid_points
from pyshield import const
import numpy as np
from pyshield.calculations.isotope import sum_attenuation, sum_buildup, attenuation


def project3D(dose_maps, sources, floor_barrier, distance):
  dose_maps3D = {}
  for sname, source in sources.items():
    print(sname)
    source_location = source[const.LOCATION]
    p, grid = grid_points(source)
    
    Rxy = ((grid[0] - source_location[0])**2 + \
            (grid[1] - source_location[1])**2) ** 0.5
           
    Rxyz = (Rxy **2 + distance ** 2) ** 0.5
           
    eff_thickness = np.ones(Rxyz.shape)
    theta = np.arcsin(distance / Rxyz)
    eff_thickness /= np.sin(theta)
    
    a = np.ones(eff_thickness.shape)
    for material, thickness in floor_barrier.items():
      a *= attenuation(material, eff_thickness, source[const.ISOTOPE])
    
    dose_map    = dose_maps[sname][2]
    dose_map3D  = np.copy(dose_map)
    dose_map3D /= (Rxyz/Rxy) **2  
    dose_map3D *= a
    dose_maps3D[sname] = dose_map3D
  return dose_maps3D