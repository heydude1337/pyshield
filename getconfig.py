# -*- coding: utf-8 -*-

from pyshield import CONST, __pkg_root__, log

from pyshield.yaml_wrap.yaml_wrap import read_yaml
import numpy as np
from os.path import join


SETTINGS = read_yaml(join(__pkg_root__, CONST.DEF_PREFERENCE_FILE))

KEY_ERROR = '{0} is not a valid key for setting items'


SETTING_ITEMS =  (CONST.AREA,
                  CONST.EXPORT_DIR,
                  CONST.RMIN,
                  CONST.NANGLES,
                  CONST.GRID,
                  CONST.GRIDSIZE,
                  CONST.PYTHAGORAS,
                  CONST.CLIM_HEATMAP,
                  CONST.COLORMAP,
                  CONST.DISABLE_BUILDUP,
                  CONST.MULTI_CPU,
                  CONST.ISO_VALUES,
                  CONST.ISO_COLORS,
                  CONST.SHOW,
                  CONST.SAVE_DATA,
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
                  CONST.HEIGHT)

def is_setting(key):
  return key in SETTING_ITEMS


def set_setting(key, value):
  if key not in SETTING_ITEMS:
    print(KEY_ERROR.format(key))
    raise KeyError
  SETTINGS[key] = value


def get_setting(key = None, default_value = None):
  log.debug('Setting {0} requested'.format(key))
  if key is None:
    # return everything
    return SETTINGS

  elif key not in SETTING_ITEMS:
    print(KEY_ERROR.format(key))
    raise KeyError

  # get key or predifined default value



  elif key in SETTINGS.keys():
    return SETTINGS[key]

  elif key == CONST.HEIGHT:
    return 0

  elif default_value is not None:
    SETTINGS[key] = default_value
    return default_value

  elif key in (CONST.SOURCES,
               CONST.SHIELDING,
               CONST.POINTS,
               CONST.MATERIAL_COLORS,
               CONST.FLOOR):
    return {}

  elif key == CONST.SCALE:
    return 1

  elif key == CONST.ORIGIN:
    return (0, 0)

  elif key == CONST.FLOOR_PLAN:
    return np.zeros((10,10))

  else:
    print(KEY_ERROR.format(key))
    raise KeyError





