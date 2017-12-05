# -*- coding: utf-8 -*
import numpy as np
from hvt import shielding_factor, shielding_thickness


reference_material = 'Lead'  # shielding material for which thickness is defined
reference_thickness = np.array(range(0, 50))[1:]/10

materials = ['Concrete', 'Robalith 3.5', 'Robalith 3.7',  'Brick', 'Lead']
isotope = 'I-131'   # isotope

factor =[]

for t in reference_thickness:
  factor += [shielding_factor(isotope=isotope, \
                              material=reference_material , thickness = t)]

materials.remove(reference_material)

thickness = {}
thickness[reference_material] = reference_thickness

for material in materials:
  t = []
  for f in factor:
    print('{0} for {1}'.format(material, f))
    t += [shielding_thickness(material = material , isotope = isotope, factor = f)]

  thickness[material] = t

thickness['Factor'] = factor
