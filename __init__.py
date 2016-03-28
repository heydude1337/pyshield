"""
  pyshield is an advanced program to calculate the (lead) shielding of a 
  nuclear medicine facility. Shielding barriers can be specified in the 
  shielding.yml file. Configuration options are specified in the config.yml
  file. Radioactive source should be specified in the sources.yml file. 
  A floorplan image can be privided as floor_plan.png.
  
  In the resources directory the following files are found:
  isotopes.yml:         Isotope data (half life, half value thickness etc.)
  materials.yml:        Materials data (density, composition etc.)
  buildup.xlsx:         Buidup factors for each material
  archer_secondary.yml: Constants for CT calculation based on NCRP 147 
  
  
  use pyshield.run() to start the calculations
  
  Matplotlib figures will be shown that show dose isocontour and a heatmap of
  the total (annual) dose on top of the floor_plan.
  
  Last Updated 05-02-2016
  
  """
  

from os.path import split 
__author__ = "Marcel Segbers"
__copyright__ = "Copyright 2016, The pyshield Project"
__license__ = "MIT"
__version__ = "0.9"
__maintainer__ = "Marcel Segbers"
__email__ = "m.segbers@erasmusmc.nl"
__status__ = "Beta"
__pkg_root__ = split(__file__)[0]


from pyshield import constants as const
from pyshield.log import log
from pyshield.config_and_data import config, data, update_config, set_file

from os.path import join, split
from pyshield.visualization import show, save, show_floorplan



update_config()





