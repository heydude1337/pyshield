
import logging
from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
from functools import partial

import pyshield as ps


def dose(isotope = 'I-131',
         barrier = {},
         source_location = (0,0),
         measured_location = {'loc': {ps.LOCATION: (0, 100)}}, **kwargs):

    source = {ps.ACTIVITY_H: 1, ps.LOCATION: (0,0), ps.ISOTOPE: isotope}

    dose_table = ps.run(points = measured_location,
                     barriers     = barrier,
                     sources      = {'source': source},
                     calculate        =  ps.POINTS,
                     scale            = 1,
                     origin           = (100, 100),
                     #area             = [200, 200],
                     log              = logging.ERROR,
                     multi_cpu     = False,
                     show = False,
                     export_excel=False,
                     # disable_buildup = False,
                     #debug = 'info',
                     **kwargs)

    return dose_table[ps.SUM_TABLE][ps.DOSE_MSV][0]


def shielding_factor(isotope = 'Lu-177', material = 'Lead' , thickness = 1, **kwargs):
    if not isinstance(material, (list, tuple)):
        barriers = {material: thickness}
        
    else:
        
        barriers = dict(zip(material, thickness))
    
    barrier = {'barrier' : {ps.MATERIAL: barriers,
                            ps.LOCATION: [-50, 50, 50, 50]}}

    return dose(isotope = isotope, barrier=barrier) / dose(isotope=isotope, **kwargs)

def shielding_thickness(isotope, material, factor = 0.5):
  """ Find half value thickness for isotope and material by optimization """


  opt_func = lambda t: abs(factor - shielding_factor(isotope= isotope,
                                                      material= material,
                                                      thickness = t))
  r = optimize.fmin(opt_func , 0.3, xtol = 1e-3, ftol = 1e-12)
  return r[0]


# 
def hvt(material = 'Lead' , isotope = 'I-131', nhvt=1):
  thickness = shielding_thickness(isotope, material, factor = 0.5**nhvt)
                        
  return thickness

def tvt(material='Lead', isotope = 'I-131'):
    return shielding_thickness(isotope, material, factor = 0.1)

if __name__ == "__main__":
    pass
#      materials = list(ps.RESOURCES[ps.MATERIALS].keys())
#      p=Pool()
#      isotope = 'I-131'
#      hvt_material = partial(hvt, isotope = isotope)
#      thickness = p.map(hvt_material, materials)
#    
#      for t, material in zip(thickness, materials):
#    plt.plot(nhvt, t, label = material)
#    
#      plt.legend()
#      plt.xlabel('Number of half value layers')
#      plt.ylabel('Half value layer thickness [cm]')


#shielding_thickness(isotope = 'I-131', material = 'Robalith 3.7', factor = 0.096)

