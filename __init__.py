from os.path import split

from pyshield.yaml_wrap.yaml_wrap import read_yaml, write_yaml

from pyshield import constants as CONST

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


from pyshield.log import log, set_log_level

from pyshield.getconfig import get_setting, set_setting, is_setting

from pyshield.resources import RESOURCES

from pyshield.resources import read_resource

from pyshield.calculations import *

from pyshield.run  import run_with_configuration

#from pyshield.errors import *









