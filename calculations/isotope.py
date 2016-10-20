# -*- coding: utf-8 -*-
"""
Isotope calculations for pyshield package

Last Updated 05-02-2016
"""

from pyshield import const, prefs, data, log
from pyshield.calculations.barrier import sum_shielding_line, add_barriers
from pyshield.resources import resources
import numpy as np
import scipy.interpolate as interp
import pandas as pd
from pyshield.calculations.dose_rates import H10

#import pickle
def equivalent_activity(source):
  """ 
  Calculate the equivalent activity in [MBqh]. Activity can be specified
  in two different ways in a source file:
     
      equivalent activity [MBqh]: Ah
      
      No calculation needed in this case.
      
      or:
    
      activity [MBq]: A
      duration [h]: h
      Number of times per year: n   (default n =1)
      Decay correction: True        (default = True)
      
      Equivalent activity in [MBqh] is obtained by integration in this case.
      
  Args:
      source: dictionary with data for a single source
  Returns:
      eq_activity: equivalent activity in [MBqh] as float
      
  """
      
  isotope = source[const.ISOTOPE]

  if const.ACTIVITY in source.keys() and const.DURATION in source.keys():
    # activity and duration specified
    activity_bq = source[const.ACTIVITY] * 1e6
    duration_h  = source[const.DURATION]

    if const.TIMES_PER_YEAR in source.keys():
      # optional the number of times per year is specified
      times_per_year = source[const.TIMES_PER_YEAR]
    else:
      times_per_year = 1

    if const.DECAY_CORRECTION in source.keys():
      # Turn decay correction on or off
      decay_corr = source[const.DECAY_CORRECTION]
    else:
      # default correct for decay
      decay_corr = True

    if decay_corr:
      # calculate the number of desintegrations with decau correction
      labda = resources[const.ISOTOPES][isotope][const.LABDA]
      ndesintegrations = activity_bq * times_per_year \
                         * (1/labda - np.exp(-labda*duration_h*3600))
    else:
      # calculate the number of desintegrations without decay correction
      ndesintegrations = activity_bq * times_per_year * duration_h * 3600
      eq_activity = ndesintegrations/3600/1E6
  elif const.ACTIVITY_H in source.keys():
    eq_activity = source[const.ACTIVITY_H]

  
  return eq_activity

  

  
def calc_dose_source_at_location(source, location, shielding, table = None):

  """" Calculates the dose that will be measured in location given a source
  specified by source and a shielding specified by shielding.
 
  Args:
    
      source:     dictonary specifying the source properties
      location:   x, y coordinates for which the dose is calculated
      shielding:  dictonary containing all shielding elements.
   
   Returns:
       dose_mSv: the total summed dose for the source at the specified 
                 location and defined shielding."""

  
  source_location = source[const.LOCATION]
  isotope         = source[const.ISOTOPE]
  
  if const.FLOOR in prefs.keys() and const.HEIGHT in prefs[const.FLOOR].keys():
    height = prefs[const.FLOOR][const.HEIGHT]
  else:
    height = 0
  
  A_eff = equivalent_activity(source)
  #h10 = resources[const.ISOTOPES][isotope][const.H10]
  log.debug('Source location: '  + str(source_location))
  log.debug('Grid location: '  + str(location))
  log.debug('Height: '  + str(height))
  # obtain total shielding between source location and the given location
  
  sum_shielding=sum_shielding_line(source_location, location, shielding)
  
  #include shielding from source
  sum_shielding = add_barriers(sum_shielding, source[const.MATERIAL])
  
  log.debug('Shielding: ' + str(sum_shielding))
  
  h10 = dose_rate(sum_shielding, isotope)
  
  d_cm = np.linalg.norm(np.array(source_location) - (np.array(location))) 
  
  d_meters = ((d_cm**2+height**2) ** 0.5) / 100
  
  
  # calculate the dose for the location
  dose_uSv = A_eff * h10 / (d_meters**2)
  dose_mSv = dose_uSv / 1000
  log.debug('height: {0} | h10: {1} | dose_uSv: {2}'\
            .format(height, h10, dose_uSv))
  # add calculations details to a table if one was passed to this function
  if table is not None:
    table[const.ALOC_SOURCE] =             [source_location]
    table[const.ALOC_POINT] =              [location]
    table[const.DISABLE_BUILDUP] =         prefs[const.DISABLE_BUILDUP]
    table[const.ISOTOPE] =                 [isotope]
    table[const.ACTIVITY_H] =              [A_eff]
    table[const.H10] =                     [h10]
    table[const.ASHIELDING_MATERIALS_CM] = [str(sum_shielding)]
    table[const.ADIST_METERS] =            [d_meters]
  
  return dose_mSv


def dose_rate(sum_shielding, isotope):
    """ 
    Calculate the dose rate for a specified isotope behind shielding 
    behind shielding barriers. The dose_rate is calculated for 1MBq 
    
    Args:
        sum_shielding:  dict with shielding elements
        isotope:        isotope name (string)
    """
    
    
    t         = transmission_sum(sum_shielding, isotope)
    energies  = resources[const.ISOTOPES][isotope][const.ENERGY_keV]
    abundance = resources[const.ISOTOPES][isotope][const.ABUNDANCE]
    dose_rate = H10(energy_keV=energies, abundance= t * np.array(abundance))
    
    return dose_rate
    
def transmission_sum(sum_shielding, isotope):
  """calculate the total attenuation for the total amount of shielding
  (calculated by sum_shielding_line). Buildup is taken into account unless
  disabled in the pyshield options.
  
  Args:
      sum_shielding: dictonary containing the effective thickness (value) for
                     each material (key)
  
      source:     dictonary specifying the source properties.
  
  Returns:
      t:  the total transmission throught the shielding elements in 
          sum_shielding.
          
  Note that a source can be shielded in all directions independend of the
  shielding barriers defined.
  
   """
  ignore_buildup = prefs[const.DISABLE_BUILDUP]
  energies = np.array(resources[const.ISOTOPES][isotope][const.ENERGY_keV])
  t = np.ones(len(energies))
  for material, thickness in sum_shielding.items():
    t *= transmission(isotope, material, thickness, ignore_buildup)
  return t
   
def transmission(isotope, material, thickness, ignore_buildup = False):
  """ Transmission through a material with thickness. Buildup is taken
      into account unless disabled.
      Args:
          isotope: name of the isotope
          material: name of the material
          thickness: thickness of the material
          ignore_buildup: if True buildup factor is 1.
      Returns:
          t: transmission factor (float)
  """
  
  energies = np.array(resources[const.ISOTOPES][isotope][const.ENERGY_keV])
  
  
  # attenuation, total is product of the attenuation of each barrier

  #barriers
  
  
  t = attenuation(energies, material, thickness)
  log.debug('Attenuation for {0} with thickness {1} and energies {2}: {3}'.format(material, thickness, str(energies), str(t)))
  
  if not(ignore_buildup):
    t *= buildup(energies, material, thickness)
  return t



def attenuation(energy_keV, material, thickness):
  """ 
  Attenuation for a given energy through a matrial with thickness. 
  Args:
      energy_keV: the energy of  the photon in keV
      material: name of the material
      thickness: thickness of the material
  Returns:
      a:  attenation factor (float)
  """
  a = np.exp(-u_linear(energy_keV, material) * thickness)

  log.debug('Material: ' + material + ' Thickness: ' + str(thickness) + ' Energy: '+ str(energy_keV))
  log.debug('Calc. attenuation: ' +  str(a))

  return a

def buildup(energy_keV, material, thickness):
  """ 
  Buildup for a given energy through a matrial with thickness. 
  Args:
      energy_keV: the energy of  the photon in keV
      material: name of the material
      thickness: thickness of the material
  Returns:
      b:  buildup factor (float)
  """

  try:
      table = resources[const.BUILDUP][material]
  except NameError:
      print(material + ' not in buildup table!')
      raise NameError

      
  if thickness == 0: return 1

  n_mfp       = np.array(table.index)
  energies    = np.array(table.columns)
  factors     = np.array(table)
  energy_MeV  = energy_keV/1000
  n_mfp_i     = number_mean_free_path(energy_keV, material, thickness)
  interp_func= interp.interp2d(energies, n_mfp,  factors, kind = 'linear')
  factor = interp_func(energy_MeV, n_mfp_i)[0]

  log.debug('Buildup factor:  ' + str(factor))
  log.debug('Material: '        + str(material))
  log.debug('Thickness: '       + str(thickness))
  log.debug('Energy: '          + str(energy_MeV))

  return factor



def number_mean_free_path(energy_keV, material, thickness):
  """"
  Args:
    energy_keV: the energy of  the photon in keV
    material: name of the material
    thickness: thickness of the material
  Retuns:
    number of mean free paths for a given photon enery, material and 
    material thicknesss
  """
  
  return thickness * u_linear(energy_keV, material)

def u_linear(energy_keV, material):
  """
  Args:
    energy_keV: the energy of  the photon in keV
    material: name of the material
  Returns:
    Linear attenuation coefficient in [cm^-1]
  Raises:
    NameError if material is not defined in the pyshield recources    
  """
  
  try:
      table = resources[const.ATTENUATION][material]
  except NameError:
      print(material + ' not in attenuation table!')
      raise NameError

  energies = np.array(table[const.ENERGY_MeV])
  
  mu_p = np.array(table[const.MASS_ATTENUATION])
  
  interp_fcn = interp.interp1d(energies, mu_p)
  
  mu_p_i = interp_fcn(energy_keV / 1e3)
  
  p = resources[const.MATERIALS][material][const.DENSITY]

  return mu_p_i * p
  



