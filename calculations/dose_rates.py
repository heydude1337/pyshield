#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 11:35:41 2016

@author: Marcel
"""
import numpy as np



def H10(energy_keV, abundance = 1, add = True):
  """
  Calculates the h10 in uSv/h per MBq/m^2 for given photon energy or 
  multiple energies.
  Args:
    energy_keV: photon energy(ies) 
    abundance:  abundance for each photon energy
    add:        sum dose rates for all energies (default = True)
  Returns:
    dose rate in uSv/h per MBq/m^2
  """
  # convert tuple and list to numpy
  energy_keV = np.array(energy_keV)
  abundance = np.array(abundance)
  energies_keV  = [20,      30,     40,     50,     60,     70,     
                   80,     100,    200,    300,    1000]
  Hp10_ka       = [0.644,   1.155,  1.529,  1.778,  1.921,  1.921,  
                   1.916,  1.832,  1.483,  1.342,  1.167]
  
  ratio = np.interp(energy_keV, energies_keV, Hp10_ka)
  
  h10 = ratio * kerma_air_rate(energy_keV, abundance, add = False)
  
  if add:
      h10 = np.sum(h10)
  return h10
  
def kerma_air_rate(energy_keV, abundance=1, add = True):
  """
  Calculates the air kerma in uGy/h per MBq/m^2 for given photon energy or 
  multiple energies.
  Args:
    energy_keV: photon energy(ies) 
    abundance:  abundance for each photon energy
    add:        sum dose rates for all energies (default = True)
  Returns:
    kerma in uGy/h per MBq/m^2
  """
  # air kerma : dKair/dt = A/(4*pi*l^2) * uk/p * E
  energy_keV = np.array(energy_keV)
  abundance = np.array(abundance)
  # kerma rate at 1m for 1 Bq (A=1, l=1)
  eV_per_Joule = 1.60217662e-19
  
  energy_J = eV_per_Joule * energy_keV * 1000
  
  energy_transfer_coeff = linear_energy_transfer_coeff_air(energy_keV) 
  
  energy_transfer_coeff *= 3600 * 1e12 #s^-1 --> h^-1 Gy--> uGy Bq --> MBq
  
  kerma = abundance * energy_transfer_coeff * energy_J / (4 * np.pi) #uGy/h per MBq/m^2
  
  if add:
      kerma = np.sum(kerma)
  return kerma
  

  
def linear_energy_transfer_coeff_air(energy_keV): 
  """ 
  Calculates the linear energy transfer coefficients by interpolation.
  Source data is obtained from the NIST XCOM database.
  
  Args:
    energy_keV: photon energy(ies) in keV
  Returns:
    linear energy tranfer rate(s)
  """
  
  energy_keV = np.array(energy_keV)
  # source data
  Energy_MeV =  [  1.00000000e-03,   1.50000000e-03,   2.00000000e-03,
                   3.00000000e-03,   3.20000000e-03,   3.20000000e-03,
                   4.00000000e-03,   5.00000000e-03,   6.00000000e-03,
                   8.00000000e-03,   1.00000000e-02,   1.50000000e-02,
                   2.00000000e-02,   3.00000000e-02,   4.00000000e-02,
                   5.00000000e-02,   6.00000000e-02,   8.00000000e-02,
                   1.00000000e-01,   1.50000000e-01,   2.00000000e-01,
                   3.00000000e-01,   4.00000000e-01,   5.00000000e-01,
                   6.00000000e-01,   8.00000000e-01,   1.00000000e+00,
                   1.25000000e+00,   1.50000000e+00,   2.00000000e+00,
                   3.00000000e+00,   4.00000000e+00,   5.00000000e+00,
                   6.00000000e+00,   8.00000000e+00,   1.00000000e+01,
                   1.50000000e+01,   2.00000000e+01]
  
                   
  u_en_p = [  3.60000000e+03,   1.19000000e+03,   5.26000000e+02,
              1.61000000e+02,   1.33000000e+02,   1.46000000e+02,
              7.64000000e+01,   3.93000000e+01,   2.27000000e+01,
              9.45000000e+00,   4.74000000e+00,   1.33000000e+00,
              5.39000000e-01,   1.54000000e-01,   6.83000000e-02,
              4.10000000e-02,   3.04000000e-02,   2.41000000e-02,
              2.33000000e-02,   2.50000000e-02,   2.67000000e-02,
              2.87000000e-02,   2.95000000e-02,   2.97000000e-02,
              2.95000000e-02,   2.88000000e-02,   2.79000000e-02,
              2.67000000e-02,   2.55000000e-02,   2.35000000e-02,
              2.06000000e-02,   1.87000000e-02,   1.74000000e-02,
              1.65000000e-02,   1.53000000e-02,   1.45000000e-02,
              1.35000000e-02,   1.31000000e-02]                 
  coeff = np.interp(energy_keV/1e3, Energy_MeV, u_en_p) # Units cm^2 per g
  coeff /= 10 # cm^2/g --> m^2/g
  return coeff

if __name__ == "__main__":
    #http://cdn.intechopen.com/pdfs-wm/32834.pdf
    from pyshield import const
    from pyshield import resources
    isotopes = resources[const.ISOTOPES]
    
    h10_I131 = H10(isotopes['I-131'][const.ENERGY_keV], isotopes['I-131'][const.ABUNDANCE])
    
    print(str(h10_I131/isotopes['I-131'][const.H10] * 100) + '% ' 'accurate for I-131')
    
    h10_Lu177 = H10(isotopes['Lu-177'][const.ENERGY_keV], isotopes['Lu-177'][const.ABUNDANCE])
    
    print(str(h10_Lu177/isotopes['Lu-177'][const.H10] * 100) + '% ' 'accurate for Lu-177')
    
    