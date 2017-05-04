import pyshield
from pyshield import CONST
from pyshield import  run_with_configuration as run
import logging
from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
from functools import partial

def dose(isotope = 'I-131',
         barrier = {},
         source_location = (0,0),
         measured_location = {'loc': {CONST.LOCATION: (0, 100)}}):

    source = {CONST.ACTIVITY_H: 1, CONST.LOCATION: (0,0), CONST.ISOTOPE: isotope}

    dose_table = run(dose_points_file = measured_location,
                     shielding_file   = barrier,
                     source_file      = {'source': source},
                     calculate        =  CONST.POINTS,
                     scale            = 1,
                     origin           = (100, 100),
                     area             = [200, 200],
                     log              = logging.ERROR,
                     multiple_cpu     = False,
                     disable_buildup  =  False)

    return dose_table[CONST.SUM_TABLE][CONST.DOSE_MSV][0]


def shielding_factor(isotope = 'Lu-177', material = 'Lead' , thickness = 1):
  barrier = {'barrier' : {CONST.MATERIAL: {material: thickness},
                          CONST.LOCATION: [-50, 50, 50, 50]}}

  return dose(isotope = isotope, barrier=barrier) / dose(isotope=isotope)

def shielding_thickness(isotope, material, factor = 0.5):
  """ Find half value thickness for isotope and material by optimization """


  opt_func = lambda t: abs(factor - shielding_factor(isotope= isotope,
                                                      material= material,
                                                      thickness = t))
  r = optimize.fmin(opt_func , 0.3, xtol = 1e-3, ftol = 1e-12)
  return r[0]


nhvt = np.arange(0.1, 20, step = 0.5)
def hvt(material = 'Lead' , isotope = 'I-131'):

  thickness = np.array([shielding_thickness(isotope, material, factor = 0.5**ni)\
                        / ni for ni in nhvt])
  return thickness

if __name__ == "__main__":
  materials = list(pyshield.RESOURCES[CONST.MATERIALS].keys())
  p=Pool()
  isotope = 'I-131'
  hvt_material = partial(hvt, isotope = isotope)
  thickness = p.map(hvt_material, materials)

  for t, material in zip(thickness, materials):
    plt.plot(nhvt, t, label = material)

  plt.legend()
  plt.xlabel('Number of half value layers')
  plt.ylabel('Half value layer thickness [cm]')


#shielding_thickness(isotope = 'I-131', material = 'Robalith 3.7', factor = 0.096)

