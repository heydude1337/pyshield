# -*- coding: utf-8 -*-
import numpy as np
from os.path import join
import pyshield as ps

CONFIG = {}

KEY_ERROR = '{0} is not a valid key for setting items'

SKIP_READING_FILES_ON_START = [ps.EXCEL_FILENAME]

_defaults_file = join(ps.__pkg_root__, ps.DEF_CONFIG_FILE)

VALID_CONFIG = tuple(ps.io.read_yaml(_defaults_file).keys())

DEBUG = False

def __str__():
     config_str = 'Pyshield Configuration:'
     config_keys = sorted(CONFIG.keys())
     formatter = '\n {0:<20} {1:<20}'
     for key in config_keys:
         if key in (ps.BARRIERS, ps.SOURCES, ps.POINTS):
             value = str(len(CONFIG[key])) + ' items'
             config_str += formatter.format(key, value)
         elif key in (ps.FLOOR_PLAN,):
             value = 'Size: ' + str(CONFIG[key].shape) 
             config_str += formatter.format(key, value)
         elif key in (ps.BUILDUP,ps.ATTENUATION, ps.ISOTOPES, ps.MATERIALS):
             value = str(tuple(CONFIG[key].keys()))
             config_str += formatter.format(key, value)
                
         else:
             config_str += '\n {0:<20} {1:<20}'.format(key, str(CONFIG[key]) )
     return config_str

def load_defaults():
    """ Load default preferences from disk """
    if len(CONFIG) > 1:
        ps.logger.warning('Overwriting existing settings')
        CONFIG.clear()

    settings = ps.io.read_yaml(join(ps.__pkg_root__, ps.DEF_CONFIG_FILE))

    for key in settings.keys():
        if key not in VALID_CONFIG:
            raise KeyError(KEY_ERROR.format(key))
        else:
            settings[key] = set_setting(key, settings[key])
    return settings

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
    if DEBUG:
        ps.logger.debug('Setting setting %s with value %s', key, str(value))
    if not _is_setting(key):
        raise KeyError(KEY_ERROR.format(key))
    
    if isinstance(value, str):
        if ps.PKG_ROOT_MACRO in value:
            value = value.replace(ps.PKG_ROOT_MACRO, ps.__pkg_root__)

    if ps.io.is_img(value):
        try:
            value = ps.io.read_img(value)
        except FileNotFoundError:
            value = np.zeros((10,10))
    elif ps.io.is_excel(value):
        if key not in SKIP_READING_FILES_ON_START:
            value = ps.io.read_excel(value)
    elif key == ps.CALCULATE:
        # HACK compatibility calculations mus be a list in newer pyshield version
        value = [value] if not isinstance(value, list) else value
    elif key == ps.SHOW:
        value = [] if value == False else value
    else:
        value = ps.io.load_item(value)
    CONFIG[key] = value

def get_setting(key = None, default_value = None):
    """ Get a setting for the pyshield package. """
    if DEBUG:
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

