from os.path import split, join

from pyshield.yaml_wrap.yaml_wrap import read_yaml, write_yaml

from pyshield import constants as const
from pyshield.documentation import __doc__
#__doc__    = pyshield.documentation.__doc__
__author__ = "Marcel Segbers"
__copyright__ = "Copyright 2016, The pyshield Project"
__license__ = "MIT"
__version__ = "0.9"
__maintainer__ = "Marcel Segbers"
__email__ = "m.segbers@erasmusmc.nl"
__status__ = "Beta"
__pkg_root__ = split(__file__)[0]

prefs = read_yaml(join(__pkg_root__, const.DEF_PREFERENCE_FILE))


data = {}       # shielding, sources and scale factor


from pyshield.log import log, set_log_level

from pyshield.resources import resources as resources

from pyshield.resources import read_resource

from pyshield.calculations import *

from pyshield.run  import run_with_configuration

#from pyshield.errors import *









