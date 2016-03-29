# -*- coding: utf-8 -*-
"""
X-ray calculations according to the NCRP 147

Last Updated 05-02-2016
"""


#NCRP 1471 pag 96
KBODY = 3e-4 #cm^-1 
KHEAD = 9e-5 #cm^-1

import numpy as np

from pyshield import const, prefs, data, log
from pyshield.calculations.barrier import sum_shielding_line 
from pyshield.resources import resources


def CTdose_1m(DLP, body_part=const.BODY, N=1):     
  """ Calculate CT dose at 1 meter 
      
      DLP: (Average) Dose Length product per examination
      body_part:  Body or Head
      N: Number of exams """
      
  if body_part == const.BODY:
    k=KBODY
  elif body_part == const.HEAD:
    k=KHEAD
  return 1.2 * k * DLP * N


def archer_attenuation(thickness_cm, alpha, beta, gamma):
  """ Calculate the x-ray attenuation according to the formulas of archer 
  
      alpha, beta, gamma: Material dependend parameters, see NCRP 147 """
      
  x_mm = thickness_cm*10
  attenuation = ((1+beta/alpha)*np.exp(alpha*gamma*x_mm)-beta/alpha)**(-1/gamma)
  
  return attenuation
  
def sum_attenuation(sum_shielding, kVp): 
  """ Calculate the x-ray total attenuaton for the specified shielding. 
  
       sum_shielding: dictonary containing the effective thickness (value) for
                 each material (key) """
    
  attenuation = 1  
  # find attenuation for each material thickness
  for material, thickness_cm in sum_shielding.items():
    # lookup material dependend parameters in the data
    alpha, beta, gamma = resources[const.XRAY_SECONDARY][material][kVp]
    attenuation *= archer_attenuation(thickness_cm, alpha, beta, gamma) 
  return attenuation
  
def calc_dose_source_at_location(source, location, shielding):   
  scale=data[const.SCALE]
  """" Calculates the dose that will be measured in location given a source 
  specified by source and a shielding specified by shielding.
  
  source:     dictonary specifying the source properties
  location:   x, y coordinates for which the dose is calculated
  shielding:  dictonary containing all shielding elements """
  

  
  source_location=source[const.LOCATION]
  kVp = source[const.KVP]  
  DLP = source[const.DLP]
  body_part = source[const.EXAM]
  number_of_exams = source[const.NUMBER_OF_EXAMS]
  
  dose_1m = CTdose_1m(DLP, body_part, N=number_of_exams)
  sum_shielding=sum_shielding_line(source_location, location, shielding)
  attenuation = sum_attenuation(sum_shielding, kVp)
  
  d = np.linalg.norm(np.array(source_location) - (np.array(location))) * scale / 100 # meters
    
  dose = dose_1m / d**2 * attenuation
  
  return dose
  