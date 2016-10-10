#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 11:35:41 2016

@author: Marcel
"""
import numpy as np



def H10(energy_keV, abundace =1):
  energies_keV = [20, 30, 40, 50, 60, 70, 80, 100, 200, 300, 1000]
  Hp10_ka = [0.644, 1.155, 1.529, 1.778, 1.921, 1.921, 1.916, 1.832, 1.483, 1.342, 1.167]
  ratio = np.interp(energy_keV, energies_keV, Hp10_ka)
  return ratio * kerma_air_rate(energy_keV) * 1e12 * 3600 #Bq --> MBq Sv --> uSv and seconds --> hours
  
def kerma_air_rate(energy_keV, abundance=1):
  # air kerma : dKair/dt = A/(4*pi*l^2) * uk/p * E
  
  # kerma rate at 1m for 1 Bq (A=1, l=1)
  eV_per_Joule = 1.60217662e-19
  energy_J = eV_per_Joule * energy_keV * 1000
  return abundance * linear_energy_transfer_coeff_air(energy_keV) * energy_J / (4 * np.pi)
  

  
def linear_energy_transfer_coeff_air(energy_keV):
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

  return np.interp(energy_keV/1e3, Energy_MeV, u_en_p)