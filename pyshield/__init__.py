from os.path import split

__pkg_root__ = split(__file__)[0]

from pyshield.constants import *

from pyshield.log import logger
from pyshield.calculations import isotope, grid, barrier, line_intersect
from pyshield.tools import drawing
from pyshield import log, io, config, calculations, tools, visualization, export
from pyshield.execute import run_with_configuration as run


# load resources from disk
io.read_resources()
from pyshield.io import RESOURCES

# load default configuration from disk
config.load_defaults()










