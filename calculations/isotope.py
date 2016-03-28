# -*- coding: utf-8 -*-
"""
Isotope calculations for pyshield package

Last Updated 05-02-2016
"""

from pyshield import data, const, config, log
from pyshield.calculations.barrier import sum_shielding_line
import numpy as np
import scipy.interpolate as interp
import pickle
def equivalent_activity(ndesintegrations, isotope):
  """Calculates the activity in MBq that will have ndesintegraties of desintegrations
  in one hour.
  
  ndesintegrations:  number of desintegrations
  isotope: Isotope name (should be in the isotopes.yml file)
  """
    
  #labda = data[const.ISOTOPES][isotope][const.LABDA]
  
  # number of desintegrations per Bq in one hour     
  #N_Bq = 1/labda * (1-np.exp(-labda*60*60)) 
 
 
  return ndesintegrations/3600/1E6

def calc_dose_source_on_grid(source, grid):
  # data
  shielding = data[const.SHIELDING]
  isotope   = source[const.ISOTOPE]
  # c
  ignore_buildup = config[const.IGNORE_BUILDUP]  
  A_eff = equivalent_activity(source[const.DESINT], isotope)  
  loc =source[const.LOCATION]
  
  scale = config[const.SCALE]

  h10 = data[const.ISOTOPES][isotope][const.H10]
  
  grid_size = grid[0].shape
  
  distance_r = np.sqrt((grid[0]-loc[0])**2 + (grid[1] - loc[1])**2) * scale / 100
  attenuation = np.zeros(grid_size)
  buildup = np.zeros(grid_size)

  values = (grid[0], grid[1], attenuation, buildup)  
  
  for xi, yi, ai, bi in np.nditer(values, op_flags = ('readwrite',)):
    sum_shielding=sum_shielding_line(loc, (xi, yi), shielding) 
    ai[...] = sum_attenuation(sum_shielding, source)
    
    if ignore_buildup:
      bi[...] = 1
    else:
      bi[...] = sum_buildup(sum_shielding, source)
    
  results = {'distance_r': distance_r,
             'attenuation': attenuation,
             'buildup': buildup,
             'activity': A_eff}
  pickle.dump(results, open('temp.dat', 'wb'))
  dose_map = A_eff/(distance_r ** 2) * attenuation * buildup * h10 / 1000
  return dose_map
  
def calc_dose_source_at_location(source, location, shielding):   
  """" Calculates the dose that will be measured in location given a source 
  specified by source and a shielding specified by shielding 
  
  source:     dictonary specifying the source properties
  location:   x, y coordinates for which the dose is calculated
  shielding:  dictonary containing all shielding elements """
  
  source_location=source[const.LOCATION]
  isotope = source[const.ISOTOPE]
  scale = config[const.SCALE]
  ignore_buildup = config[const.IGNORE_BUILDUP]
  A_eff = equivalent_activity(source[const.DESINT], isotope)
  h10 = data[const.ISOTOPES][isotope][const.H10]
  log.debug('Source location: '  + str(source_location))
  log.debug('Grid location: '  + str(location))
  # obtain total shielding between source location and the given location
  sum_shielding=sum_shielding_line(source_location, location, shielding) 
 
  d = np.linalg.norm(np.array(source_location) - (np.array(location))) / 100 * scale
  
  # attenuation and buildup
  attenuation = sum_attenuation(sum_shielding, source)
  if ignore_buildup:
    B = 1
  else:
    B = sum_buildup(sum_shielding, source)

  # calculate the dose for the location
  dose_uSv = A_eff * h10 / d**2 * attenuation * B
  dose_mSv = dose_uSv / 1000
  
  return dose_mSv
  
def sum_attenuation(sum_shielding, source):
  """calculate the total attenuation for the total amount of shielding 
  (calculated by sum_shielding_line) 
  
  sum_shielding: dictonary containing the effective thickness (value) for
                 each material (key)
  
  source:     dictonary specifying the source properties.

  Note that a source can be shielded in all directions independend of the
  shielding barriers defined.              
  
   """
  
  
  isotope = source[const.ISOTOPE]
  
  # attenuation, total is product of the attenuation of each barrier
  
  #barriers
  a = 1    
  for material, thickness in sum_shielding.items():        
    a *= attenuation(material, thickness, isotope)

  # add the shielding thickness around the source
  for material, thickness in source[const.MATERIAL].items():
    a *= attenuation(material, thickness, isotope)
    
  return a
  
def sum_buildup(sum_shielding, source):
  """calculate the total buildup for the total amount of shielding 
  (calculated by sum_shielding_line) 
  
  sum_shielding: dictonary containing the effective thickness (value) for
                 each material (key)
  
  source:     dictonary specifying the source properties.

  Note that a source can be shielded in all directions independend of the
  shielding barriers defined.              
  
   """
  
  b = 1
  
  isotope = source[const.ISOTOPE]
  
  #buildup from shielding barriers
  for material, thickness in sum_shielding.items():
    if material in data[const.BUILDUP]:
      hvt = data[const.ISOTOPES][isotope][const.HALF_VALUE_THICKNESS][material]
      mu_lin =1 / np.log(2) * hvt
      n_mfp = thickness / mu_lin
      energy_keV = data[const.ISOTOPES][isotope][const.ENERGY]
      b *= buildup(material, energy_keV, n_mfp)
  
  #buildup from shielding around source
  for material in source[const.MATERIAL].items():
    if material in data[const.BUILDUP]:
      hvt = data[const.ISOTOPES][isotope][const.HALF_VALUE_THICKNESS][material]
      mu_lin =1 / np.log(2) * hvt
      n_mfp = thickness / mu_lin
      energy_keV = data[const.ISOTOPES][isotope][const.ENERGY]
      b *= buildup(material, energy_keV, n_mfp)
      
    
  return b
    
def attenuation(material, thickness, isotope):
  HVT = data[const.ISOTOPES][isotope][const.HALF_VALUE_THICKNESS][material] 
  n_HVT = thickness/HVT
  a = 0.5**n_HVT
  log.debug('Material: ' + material + ' Thickness: ' + str(thickness) + ' Isotope: '+ isotope)
  log.debug('Calc. attenuation: ' +  str(a))
  return a

def buildup(material, energy_keV, n_mfp_i):
  """ Calculate the buildup factor by interpolating the table 
      
      energy_keV: Photon energy in keV      
      n_mfp:      Number of mean free paths
      
  """
  
  #retrun 0 for 0 thickness
  #if not(isinstance(n_mfp_i, np.ndarray)):
    #n_mfp_i = np.array(n_mfp_i)
    
  #if all(n_mfp_i == 0): return np.zeros(n_mfp_i.shape)
  if n_mfp_i ==0: return 0
    
#  if material == 'Robaliet':
#    factor = 3.5
#  else:
  n_mfp = data[const.BUILDUP][material][const.MFP]
  energies = data[const.BUILDUP][material][const.ENERGY]
  factors = data[const.BUILDUP][material][const.BUILDUP_FACTORS]
  energy_meV = energy_keV/1000  
#  if energies.size == 1:
#     interp_func=interp.interp1d(n_mfp, factors)
#     factor =interp_func(n_mfp_i)
#  else: 
  interp_func= interp.interp2d(n_mfp,energies,  factors, kind = 'linear')
  factor = interp_func(n_mfp_i, energy_meV)
  
      
  
  log.debug('Buildup factor:  ' + str(factor))
  log.debug('MFP: '  + str(n_mfp_i))
  log.debug('Energy: ' + str(energy_meV))
  

  return np.squeeze(factor)


    
def number_mean_free_path(thickness, hvt):
  """ Calculates the number of mean free paths 
  
      thickness: material thickness in cm
      hvt:       Half value thickness for that material"""
  
  
  mu_lin = np.log(2)/hvt
  N = thickness * mu_lin
  return N
  
def thickness_nmfp(nmfp, hvt):
  """ Calculates the material thickness 

     nmfp: number of mean free paths
     hvt:  half value thickness of the material """
     
  thickness = hvt/np.log(2) * nmfp
  return thickness
  
  
 
       