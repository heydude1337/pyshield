# -*- coding: utf-8 -*-
"""
Isotope calculations for pyshield package

Last Updated 05-02-2016
"""

from pyshield import const, prefs, data, log
from pyshield.calculations.barrier import sum_shielding_line
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

  
#def calc_dose_source_on_grid(source, grid):
#  # data
#  shielding = data[const.SHIELDING]
#  isotope   = source[const.ISOTOPE]
#  # c
#  ignore_buildup = prefs[const.DISABLE_BUILDUP]
#  A_eff = equivalent_activity(source)
#  loc =source[const.LOCATION]
#
#
#
#  h10 = resources[const.ISOTOPES][isotope][const.H10]
#
#  grid_size = grid[0].shape
#
#  # distance gird
#  d_meters = np.sqrt((grid[0]-loc[0])**2 + (grid[1] - loc[1])**2) / 100
#
#
#  attenuation = np.zeros(grid_size)
#  buildup = np.zeros(grid_size)
#
#  values = (grid[0], grid[1], attenuation, buildup)
#
#  # iterate over grid
#  for xi, yi, ai, bi in np.nditer(values, op_flags = ('readwrite',)):
#    sum_shielding=sum_shielding_line(loc, (xi, yi), shielding)
#    ai[...] = sum_attenuation(sum_shielding, source)
#
#    if ignore_buildup:
#      bi[...] = 1
#    else:
#      bi[...] = sum_buildup(sum_shielding, source)
#
#  dose_map = A_eff/(d_meters ** 2) * attenuation * buildup * h10 / 1000
#
#  return dose_map
  

  
def calc_dose_source_at_location(source, location, shielding, audit = None):

  """" Calculates the dose that will be measured in location given a source
  specified by source and a shielding specified by shielding

  source:     dictonary specifying the source properties
  location:   x, y coordinates for which the dose is calculated
  shielding:  dictonary containing all shielding elements """


  source_location = source[const.LOCATION]
  isotope         = source[const.ISOTOPE]


  
  A_eff = equivalent_activity(source)
  #h10 = resources[const.ISOTOPES][isotope][const.H10]
  log.debug('Source location: '  + str(source_location))
  log.debug('Grid location: '  + str(location))

  # obtain total shielding between source location and the given location
  sum_shielding=sum_shielding_line(source_location, location, shielding)
  h10 = dose_rate(sum_shielding, isotope)
  d_meters = np.linalg.norm(np.array(source_location) - (np.array(location))) / 100


  # attenuation and buildup
#  attenuation = sum_attenuation(sum_shielding, source)
#  if ignore_buildup:
#    B = 1
#  else:
#    B = sum_buildup(sum_shielding, source)

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
    #audit[const.BUILDUP] =                 [B]
    audit[const.AATTENUATION] =            [attenuation]

  return dose_mSv

def calc_dose_sources_at_locations(sources, locations, shielding, audit = None):
  print(locations)
  dose_mSv = {}
  if prefs[const.AUDIT] and audit is None:
    audit = pd.DataFrame()

  for pname, loc in locations.items():
    di = 0
    log.debug('Calculating point {0}'.format(pname))
    for sname, source in sources.items():
      if prefs[const.AUDIT]:
        audit_entry = pd.DataFrame()
        audit_entry[const.ASOURCE] = [sname]
        audit_entry[const.APOINT] = [pname]
      else:
        audit_entry = None

      log.debug('Calculating source {0} for point {0}'.format(sname, pname))
      di += calc_dose_source_at_location(source, loc,
                                         shielding, 
                                         audit = audit_entry)
      if prefs[const.AUDIT]:
        audit = pd.concat((audit, audit_entry), ignore_index = True)
    dose_mSv[pname] = di

  if  prefs[const.AUDIT]:
    return audit

  return dose_mSv

  
def dose_rate(sum_shielding, isotope):
   
    t = transmission(sum_shielding, isotope)
    energies = resources[const.ISOTOPES][isotope][const.ENERGY_keV]
    abundance = resources[const.ISOTOPES][isotope][const.ABUNDANCE]
    dose_rate = H10(energy_keV=energies, abundance= t * np.array(abundance))
    return dose_rate
    
def transmission(sum_shielding, isotope):
  """calculate the total attenuation for the total amount of shielding
  (calculated by sum_shielding_line)

  sum_shielding: dictonary containing the effective thickness (value) for
                 each material (key)

  source:     dictonary specifying the source properties.

  Note that a source can be shielded in all directions independend of the
  shielding barriers defined.

   """

  energies = np.array(resources[const.ISOTOPES][isotope][const.ENERGY_keV])
  
  ignore_buildup = prefs[const.DISABLE_BUILDUP]
  # attenuation, total is product of the attenuation of each barrier

  #barriers
  t = np.ones(len(energies))
  for material, thickness in sum_shielding.items():
     t *= attenuation(energies, material, thickness)
     if not(ignore_buildup):
       t *= buildup(energies, material, thickness)
     
  

  return t

def sum_buildup(sum_shielding, source):
  """calculate the total buildup for the total amount of shielding
  (calculated by sum_shielding_line)

  sum_shielding: dictonary containing the effective thickness (value) for
                 each material (key)

  source:     dictonary specifying the source properties.

  Note that a source can be shielded in all directions independend of the
  shielding barriers defined.

   """

  b = 1  # default build up is one

  isotope = source[const.ISOTOPE]

  #buildup from shielding barriers
  for material, thickness in sum_shielding.items():
    if material in resources[const.BUILDUP]:
      hvt = resources[const.ISOTOPES][isotope][const.HALF_VALUE_THICKNESS][material]
      mu_lin =1 / np.log(2) * hvt
      n_mfp = thickness / mu_lin
      energy_keV = resources[const.ISOTOPES][isotope][const.ENERGY]
      b *= buildup(material, energy_keV, n_mfp)
    else:
      log.debug(material + ' does not have specified buildup factors.')

  #buildup from shielding around source

  for material, thickness in source[const.MATERIAL].items():
    if material in resources[const.BUILDUP]:
      hvt = resources[const.ISOTOPES][isotope][const.HALF_VALUE_THICKNESS][material]
      mu_lin =1 / np.log(2) * hvt
      n_mfp = thickness / mu_lin
      energy_keV = resources[const.ISOTOPES][isotope][const.ENERGY]
      b *= buildup(material, energy_keV, n_mfp)
    else:
      log.debug(material + ' does not have specified buildup factors.')

  return b

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
  except:
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
 
  return thickness / u_linear(energy_keV, material)

def u_linear(energy_keV, material):
  try:
      table = resources[const.ATTENUATION][material]
  except:
      print(material + ' not in attenuation table!')


  energies = np.array(table[const.ENERGY_MeV])
  
  mu_p = np.array(table[const.MASS_ATTENUATION])
  
  interp_fcn = interp.interp1d(energies, mu_p)
  
  mu_p_i = interp_fcn(energy_keV/1e3)
  
  p = resources[const.MATERIALS][material][const.DENSITY]

  return mu_p_i * p
  
def thickness_nmfp(nmfp, hvt):
  """ Calculates the material thickness

     nmfp: number of mean free paths
     hvt:  half value thickness of the material """

  thickness = hvt/np.log(2) * nmfp
  return thickness



