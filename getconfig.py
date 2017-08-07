# -*- coding: utf-8 -*-

from pyshield import CONST, __pkg_root__, log
from pyshield.resources import is_valid_resource_file, read_data_file
from pyshield.yaml_wrap.yaml_wrap import read_yaml, is_yaml
import numpy as np
from os.path import join


SETTINGS = {}

KEY_ERROR = '{0} is not a valid key for setting items'

SKIP_READING_FILES_ON_START = [CONST.EXCEL_FILENAME_FULLRESULT,
                               CONST.EXCEL_FILENAME_SUMMARY]

SETTING_ITEMS =  (CONST.EXPORT_DIR,
                  CONST.NANGLES,
                  CONST.GRID,
                  CONST.GRIDSIZE,
                  CONST.PYTHAGORAS,
                  CONST.CLIM_HEATMAP,
                  CONST.COLORMAP,
                  CONST.DISABLE_BUILDUP,
                  CONST.MULTI_CPU,
                  CONST.ISOCONTOUR_LINES,
                  CONST.SHOW,
                  CONST.SAVE_IMAGES,
                  CONST.IMAGE_DPI,
                  CONST.CALCULATE,
                  CONST.LOG,
                  CONST.FLOOR,
                  CONST.POINTS,
                  CONST.SOURCES,
                  CONST.SHIELDING,
                  CONST.POINTS,
                  CONST.FLOOR_PLAN,
                  CONST.MATERIAL_COLORS,
                  CONST.SCALE,
                  CONST.ORIGIN,
                  CONST.HEIGHT,
                  CONST.EXPORT_EXCEL,
                  CONST.EXCEL_FILENAME_FULLRESULT,
                  CONST.EXCEL_FILENAME_SUMMARY)

def load_default_settings():
  SETTINGS.clear()
  new_settings = read_yaml(join(__pkg_root__, CONST.DEF_PREFERENCE_FILE))

  for setting, value in new_settings.items():
    set_setting(setting, value)
  return

def is_setting(key):
  return key in SETTING_ITEMS

def set_settings(settings):
  for setting, value in settings.items():
    set_setting(setting, value)
  return

def set_setting(key, value):
  if key not in SETTING_ITEMS:
    print(KEY_ERROR.format(key))
    raise KeyError
  if is_valid_resource_file(value) and key not in SKIP_READING_FILES_ON_START:
    try:
      log.debug('Reading: %s', value)
      value = read_data_file(value)
    except (TypeError, FileNotFoundError):
      if key in (CONST.MATERIAL_COLORS, CONST.SOURCES, CONST.SHIELDING, CONST.POINTS):
        msg = '{0} is not a valid value or file for {1}, {1} was set to empty dict.'
        value = {}
        log.debug(msg.format(value, key))
      else:
        msg = '{0} is not a valid value for {1}'
        print(msg.format(value, key))
        raise

  if key == CONST.CALCULATE:
    if not(hasattr(value, '__iter__')):
      value = [value]
  SETTINGS[key] = value


def get_setting(key = None, default_value = None):
  log.debug('Setting {0} requested'.format(key))
  if key is None: # return everything
    return SETTINGS

  elif key not in SETTING_ITEMS:
    print(KEY_ERROR.format(key))
    raise KeyError

  # get key and return set value
  elif key in SETTINGS.keys():
    return SETTINGS[key]

  # key not available return default value
  elif default_value is not None:
    SETTINGS[key] = default_value
    return default_value

  elif key == CONST.FLOOR_PLAN:
    return np.zeros((10,10))

  else:
    print(KEY_ERROR.format(key))
    raise KeyError





