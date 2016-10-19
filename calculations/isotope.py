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
  # amount of activity can be either specified by number of desintegrations
  # or the amount of activity and the duration for which it is present
  # Optional the activity corrected for decay during this duration (default).
  # Decay correction can be turned off
  isotope = source[const.ISOTOPE]

  if const.DESINT in source.keys():
    # number of desintegration specified ACTIVITY and DURATION tags will be ignored
    ndesintegrations = source[const.DESINT]
  elif const.ACTIVITY in source.keys() and const.DURATION in source.keys():
    # activity and duration specified
    activity_bq = source[const.ACTIVITY] * 1e6
    duration_h = source[const.DURATION]
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
      ndesintegrations = activity_bq * times_per_year * (1/labda - np.exp(-labda*duration_h*3600))
    else:
      # calculate the number of desintegrations without decay correction
      ndesintegrations = activity_bq * times_per_year * duration_h * 3600
  elif const.ACTIVITY_H in source.keys():
    ndesintegrations = source[const.ACTIVITY_H] * 3600 * 1E6
  # The equivalent activity is the amount of MBq of the isotope that would be
  # needed to give the amount of desintegrations in one hour without decay corrections


  eq_activity = ndesintegrations/3600/1E6
  return eq_activity

  

  
def calc_dose_source_at_location(source, location, shielding, audit = None):

  """" Calculates the dose that will be measured in location given a source
  specified by source and a shielding specified by shielding

  source:     dictonary specifying the source properties
  location:   x, y coordinates for which the dose is calculated
  shielding:  dictonary containing all shielding elements """


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
  dose_uSv = A_eff * h10 / d_meters**2 #* attenuation * B
  dose_mSv = dose_uSv / 1000

  if prefs[const.AUDIT]:
    audit[const.ALOC_SOURCE] =             [source_location]
    audit[const.ALOC_POINT] =              [location]
    audit[const.DISABLE_BUILDUP] =         prefs[const.DISABLE_BUILDUP]
    audit[const.ISOTOPE] =                 [isotope]
    audit[const.ACTIVITY_H] =              [A_eff]
    audit[const.H10] =                     [h10]
    audit[const.ASHIELDING_MATERIALS_CM] = [str(sum_shielding)]
    audit[const.ADIST_METERS] =            [d_meters]
  
  return dose_mSv


def dose_rate(sum_shielding, isotope):
   
    t         = transmission_sum(sum_shielding, isotope)
    energies  = resources[const.ISOTOPES][isotope][const.ENERGY_keV]
    abundance = resources[const.ISOTOPES][isotope][const.ABUNDANCE]
    dose_rate = H10(energy_keV=energies, abundance= t * np.array(abundance))
    
    return dose_rate
    
def transmission_sum(sum_shielding, isotope):
  """calculate the total attenuation for the total amount of shielding
  (calculated by sum_shielding_line)
  
  sum_shielding: dictonary containing the effective thickness (value) for
                 each material (key)
  
  source:     dictonary specifying the source properties.
  
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
  energies = np.array(resources[const.ISOTOPES][isotope][const.ENERGY_keV])
  
  
  # attenuation, total is product of the attenuation of each barrier

  #barriers
  
  
  t = attenuation(energies, material, thickness)
  log.debug('Attenuation for {0} with thickness {1} and energies {2}: {3}'.format(material, thickness, str(energies), str(t)))
  
  if not(ignore_buildup):
    t *= buildup(energies, material, thickness)
  return t



def attenuation(energy_keV, material, thickness):

  a = np.exp(-u_linear(energy_keV, material) * thickness)

  log.debug('Material: ' + material + ' Thickness: ' + str(thickness) + ' Energy: '+ str(energy_keV))
  log.debug('Calc. attenuation: ' +  str(a))

  return a

def buildup(energy_keV, material, thickness):
  """ Calculate the buildup factor by interpolating the table

      energy_keV: Photon energy in keV
      n_mfp:      Number of mean free paths

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
 
  return thickness * u_linear(energy_keV, material)

def u_linear(energy_keV, material):
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
  
def thickness_nmfp(nmfp, hvt):
  """ Calculates the material thickness

     nmfp: number of mean free paths
     hvt:  half value thickness of the material """

  thickness = hvt/np.log(2) * nmfp
  return thickness



