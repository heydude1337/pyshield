# -*- coding: utf-8 -*-
"""
Isotope calculations for pyshield package

Last Updated 05-02-2016
"""
import numpy as np
import scipy.interpolate as interp
from pyshield import CONST, log
from pyshield.calculations.barrier import sum_shielding_line, add_barriers
from pyshield.resources import RESOURCES
from pyshield.calculations.dose_rates import H10


def equivalent_activity(source):
    """
    Calculate the equivalent activity in [MBqh]. Activity can be specified
    in two different ways in a source file:

        equivalent activity [MBqh]: Ah

        No calculation needed in this case.

        or:

        activity [MBq]: A
        duration [h]: h
        Number of times per year: n   (default n = 1)
        Decay correction: True        (default = True)

        Equivalent activity in [MBqh] is obtained by integration in this case.

    Args:
        source: dictionary with data for a single source
    Returns:
        eq_activity: equivalent activity in [MBqh] as float

    """

    isotope = source[CONST.ISOTOPE]

    if CONST.ACTIVITY in source.keys() and CONST.DURATION in source.keys():
        # activity and duration specified
        activity_MBq = source[CONST.ACTIVITY]
        duration_h   = source[CONST.DURATION]

        if CONST.NUMBER_OF_EXAMS in source.keys():
            # optional the number of times per year is specified
            times_per_year = source[CONST.NUMBER_OF_EXAMS]
        else:
            source[CONST.NUMBER_OF_EXAMS] = 1
            times_per_year = 1

        if CONST.DECAY_CORRECTION in source.keys():
            # Turn decay correction on or off
            decay_corr = source[CONST.DECAY_CORRECTION]
        else:
            # default correct for decay
            decay_corr = True

        if decay_corr:
            # calculate the number of desintegrations with decau correction
            labda = RESOURCES[CONST.ISOTOPES][isotope][CONST.LABDA]
            log.debug('Isope %s', source[CONST.ISOTOPE])
            log.debug('Activity_MBq  %s', source[CONST.ACTIVITY])
            log.debug('Duration_h %s', source[CONST.DURATION])
            log.debug('Times_per_year %s', source[CONST.NUMBER_OF_EXAMS])
            log.debug('Labda %s', labda)

            ndesintegrations = activity_MBq * 1e6 * times_per_year *\
                               1/labda * (1 - np.exp(-labda*duration_h*3600))
            log.debug('ndesint %s',ndesintegrations)
        else:
            # calculate the number of desintegrations without decay correction
            ndesintegrations = activity_MBq * times_per_year * duration_h * 3600

        eq_activity = ndesintegrations/3600/1E6
        log.debug('Equivalent Activity: %s', eq_activity)
    elif CONST.ACTIVITY_H in source.keys():
        eq_activity = source[CONST.ACTIVITY_H]
    elif CONST.DESINT in source.keys():
        eq_activity = source[CONST.DESINT]/3600/1E6

    return eq_activity


def avg_distance_line_source(L, d):
  return  d*np.sqrt(L**2/(4*d**2) + 1)/2 + d**2*np.asinh(L/(2*d))/L

def dose_rate_line_source(length_meters, distance_meters):
  L = length_meters
  d = distance_meters
  return 2  / (L * d) * np.arctan(L / (2 * d))

def dose_rate_point_source(distance_meters):
  d = distance_meters
  return 1/d**2


def calc_dose_source_at_location(source, location, shielding,
                                 height = 0, disable_buildup = False,
                                 pythagoras = True, return_details = False,
                                 floor = {}):

    """" Calculates the dose that will be measured in location given a source
    specified by source and a shielding specified by shielding.

    Args:

        source:     dictonary specifying the source properties
        location:   x, y coordinates for which the dose is calculated
        shielding:  dictonary containing all shielding elements.

     Returns:
         dose_mSv: the total summed dose for the source at the specified
                   location and defined shielding."""

    source_location = np.array(source[CONST.LOCATION])
    isotope         = source[CONST.ISOTOPE]



    A_eff = equivalent_activity(source)

    log.debug('Source location: %s', source_location)
    log.debug('Grid location: %s', location)
    log.debug('Height: %s', height)

    # obtain total shielding between source location and the given location
    sum_shielding=sum_shielding_line(source_location, location,
                                     shielding, pythagoras)

    #include shielding from source
    sum_shielding = {**sum_shielding, **source.get(CONST.MATERIAL,{})}
    sum_shielding = add_barriers(sum_shielding, floor)

    h10 = dose_rate(sum_shielding, isotope, disable_buildup)



    d_meters = np.linalg.norm(np.array(source_location) -
                              np.array(location)) / 100


    if CONST.LINE_SOURCE in source.get(CONST.TYPE, [None]):
      if height > 0:
        print('Cannot use height > 0 for line sources')
        raise NotImplementedError

      rel_strength = dose_rate_line_source(source.get(CONST.LENGTH), d_meters)

    else:
      #print(source.get(CONST.TYPE, CONST.POINT_SOURCE))
      rel_strength = dose_rate_point_source(d_meters + height / 100)


    # calculate the dose for the location
    dose_mSv = A_eff * h10 * rel_strength / 1000

    log.debug('height: %s | h10: %s | dose_mSv: %s', height, h10, dose_mSv)
    # add calculations details to a table if one was passed to this function
    if return_details:
        details = {}
        #disable_buidup = get_setting(CONST.DISABLE_BUILDUP)

        details[CONST.SOURCE_LOCATION]          = source_location
        details[CONST.POINT_LOCATION]           = location
        details[CONST.DISABLE_BUILDUP]          = disable_buildup
        details[CONST.ISOTOPE]                  = isotope
        details[CONST.ACTIVITY_H]               = A_eff
        details[CONST.H10]                      = h10
        details[CONST.TOTAL_SHIELDING]          = str(sum_shielding)
        details[CONST.SOURCE_POINT_DISTANCE]    = d_meters
        details['Dose [mSv] per Energy']        = dose_mSv
        details[CONST.DOSE_MSV]                 = np.sum(dose_mSv)
        details[CONST.PYTHAGORAS]               = pythagoras
        details[CONST.HEIGHT]                   = height

        return details

    return np.sum(dose_mSv)

def dose_rate(sum_shielding, isotope, disable_buildup = False):
    """
    Calculate the dose rate for a specified isotope behind shielding
    behind shielding barriers. The dose_rate is calculated for 1MBq

    Args:
        sum_shielding:  dict with shielding elements
        isotope:        isotope name (string)
    """

    t         = transmission_sum(sum_shielding, isotope, disable_buildup)
    energies  = RESOURCES[CONST.ISOTOPES][isotope][CONST.ENERGY_keV]
    abundance = RESOURCES[CONST.ISOTOPES][isotope][CONST.ABUNDANCE]

    log.debug(isotope)
    log.debug('t: %s', t)
    log.debug('energies: %s', energies)
    log.debug('abundance: %s', abundance)

    rate = H10(energy_keV=energies, abundance=t * np.array(abundance))

    return rate

def transmission_sum(sum_shielding, isotope, disable_buildup = False):
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
    #ignore_buildup = get_setting(CONST.DISABLE_BUILDUP)
    energies = np.array(RESOURCES[CONST.ISOTOPES][isotope][CONST.ENERGY_keV])
    t = np.ones(len(energies))
    for material, thickness in sum_shielding.items():
        log.debug('transmission through %s cm %s', thickness, material)
        t *= transmission(isotope, material, thickness, disable_buildup)
    return t

def transmission(isotope, material, thickness, disable_buildup=False):
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

    energies = np.array(RESOURCES[CONST.ISOTOPES][isotope][CONST.ENERGY_keV])


    # attenuation, total is product of the attenuation of each barrier

    #barriers


    t = attenuation(energies, material, thickness)
    msg = 'Attenuation for %s with thickness %s and energies %s: %s'
    log.debug(msg, material, thickness, energies, t)

    if not disable_buildup:
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

    msg = 'Material: %s Thickness: %s Energy: %s Attenuation %s'
    log.debug(msg, material, thickness, energy_keV, attenuation)
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
        table = RESOURCES[CONST.BUILDUP][material]
    except NameError:
        print(material + ' not in buildup table!')
        raise NameError


    if thickness == 0:
        return 1

    n_mfp       = np.array(table.index)
    energies    = np.array(table.columns)
    factors     = np.array(table)
    energy_MeV  = energy_keV/1000
    n_mfp_i     = number_mean_free_path(energy_keV, material, thickness)
    interp_func = interp.interp2d(energies, n_mfp, factors, kind='linear')
    factor      = interp_func(energy_MeV, n_mfp_i)[0]

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
        table = RESOURCES[CONST.ATTENUATION][material]
    except NameError:
        print(material + ' not in attenuation table!')
        raise NameError

    energies = np.array(table[CONST.ENERGY_MeV])

    mu_p = np.array(table[CONST.MASS_ATTENUATION])

    interp_fcn = interp.interp1d(energies, mu_p)

    mu_p_i = interp_fcn(energy_keV / 1e3)

    p = RESOURCES[CONST.MATERIALS][material][CONST.DENSITY]

    return mu_p_i * p
