# -*- coding: utf-8 -*-
import numpy as np
from os.path import join

import pyshield as ps




CONFIG = {}

KEY_ERROR = '{0} is not a valid key for setting items'

SKIP_READING_FILES_ON_START = [ps.EXCEL_FILENAME_FULLRESULT,
                               ps.EXCEL_FILENAME_SUMMARY]

VALID_CONFIG =  (ps.EXPORT_DIR,
                 ps.NANGLES,
                 ps.GRID,
                 ps.GRIDSIZE,
                 ps.PYTHAGORAS,
                 ps.CLIM_HEATMAP,
                 ps.COLORMAP,
                 ps.DISABLE_BUILDUP,
                 ps.MULTI_CPU,
                 ps.ISOCONTOUR_LINES,
                 ps.SHOW,
                 ps.SAVE_IMAGES,
                 ps.IMAGE_DPI,
                 ps.CALCULATE,
                 ps.LOG,
                 ps.FLOOR,
                 ps.POINTS,
                 ps.SOURCES,
                 ps.SHIELDING,
                 ps.POINTS,
                 ps.FLOOR_PLAN,
                 ps.MATERIAL_COLORS,
                 ps.SCALE,
                 ps.ORIGIN,
                 ps.HEIGHT,
                 ps.EXPORT_EXCEL,
                 ps.EXCEL_FILENAME_FULLRESULT,
                 ps.EXCEL_FILENAME_SUMMARY,
                 ps.EXPORT_IMAGES)


def __str__():
     config_str = 'Pyshield Configuration:'
     config_keys = sorted(CONFIG.keys())
     for key in config_keys:
        config_str += '\n {0:<20} {1:<20}'.format(key, str(CONFIG[key]))
     return config_str




def load_defaults():
    """ Load default preferences from disk """
    if len(CONFIG) > 1:
        ps.logger.warning('Overwriting existing settings')
        CONFIG.clear()

    settings = ps.io.read_yaml(join(ps.__pkg_root__, ps.DEF_CONFIG_FILE))

    for setting, value in settings.items():
        set_setting(setting, value)
    return

def _is_setting(key):
    # return true if it is a valid setting for pyshield
    return key in VALID_CONFIG

def set_config(config):
    """ Set settings for pyshield, settings must be a dictionary. Existing settings
    will be overwritten. """
    for setting, value in config.items():
        # loop trough setting and set each individual setting
        set_setting(setting, value)
    return

def get_config():
    return CONFIG


def set_setting(key, value):
    """ Set a setting for the pyshield package. """
    ps.logger.debug('Setting setting %s with value %s', key, str(value))
    if not _is_setting(key):
        raise KeyError(KEY_ERROR.format(key))

    if not isinstance(value, str):
        CONFIG[key] = value
    elif ps.io.is_yaml(value):
        try:
            value = ps.io.read_yaml(value)
        except FileNotFoundError:
            ps.logger.debug('File not found: %s', value)
            value = {}
        CONFIG[key] = value
    elif ps.io.is_img(value):
        try:
            CONFIG[key] = ps.io.load_file(value)
        except FileNotFoundError:
            value = np.zeros((10,10))
    elif key == ps.CALCULATE:
        # HACK compatibility calculations mus be a list in newer pyshield version
        CONFIG[key] = [value]

    else:
        CONFIG[key] = value

def get_setting(key = None, default_value = None):
    """ Get a setting for the pyshield package. """

    ps.logger.debug('Setting {%s requested', key)

    if not _is_setting(key) and key is not None:
        raise KeyError(KEY_ERROR.format(key))

    elif key is None: # return everything
        return_value = CONFIG

    else:
        return_value = CONFIG.get(key, default_value)

    if key == ps.FLOOR_PLAN and return_value is None:
        # HACK default value for floor_plan, must be numpy
        return_value = np.zeros((10,10))
    if key == ps.CALCULATE and return_value is None:
        # HACK compatibility calculations mus be a list in newer pyshield version
        return_value = []
    return return_value

