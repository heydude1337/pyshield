# -*- coding: utf-8 -*-
from hvt import shielding_factor, shielding_thickness

lead_thickness = [3, 4, 5, 6]

isotope = 'I-131'

factor =[]

for t in lead_thickness:
  factor += [shielding_factor(isotope=isotope, material='Lead' , thickness = t)]


materials = ['Concrete', 'Robalith 3.5', 'Brick']

thickness = {}
thickness['lead'] = lead_thickness

for material in materials:
  t = []
  for f in factor:
    print('{0} for {1}'.format(material, f))
    t += [shielding_thickness(material = material , isotope = 'I-131', factor = f)]

  thickness[material] = t

thickness['Factor'] = factor
