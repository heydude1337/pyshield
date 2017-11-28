from os.path import split
from pyshield.yaml_io import is_yaml, read_yaml


from pyshield import constants as CONST

#from pyshield.documentation import __doc__

#__doc__    = pyshield.documentation.__doc__
__author__ = "Marcel Segbers"
__copyright__ = "Copyright 2016, The pyshield Project"
__license__ = "MIT"
__version__ = "0.9"
__maintainer__ = "Marcel Segbers"
__email__ = "heydude1337@gmail.com"
__status__ = "Beta"
__pkg_root__ = split(__file__)[0]


from pyshield.log import log, set_log_level

from pyshield.getconfig import get_setting, set_setting, is_setting
from pyshield.getconfig import load_default_settings
load_default_settings()


from pyshield.resources import read_resources, RESOURCES


from pyshield.resources import read_data_file

from pyshield.calculations import *

from pyshield.main  import run_with_configuration as run

from pyshield.Tools.drawing import point, wall



#from pyshield.errors import *









