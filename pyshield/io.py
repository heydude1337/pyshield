""" Functions to read resource files (.yml, .xls/.xlsx and images) """

# -*- coding: utf-8 -*-


from os import path
import pandas as pd
import matplotlib.image as mpimg
import numpy as np
import yaml



import pyshield as ps

VALID_EXTENSIONS = ('.yml', '.yaml', 'xls', 'xlsx',
                    'png', 'jpeg', 'jpg', 'bmp')


RESOURCES = {}

def _file_ext(file):
    return path.splitext(file)[1].lower()

def is_yaml(file):
    YAML = ('.yml','.yaml')
    return isinstance(file, str) and _file_ext(file) in YAML

def is_img(file):
    IMG = ('.png', '.jpeg', '.jpg', '.bmp')
    return isinstance(file, str) and _file_ext(file) in IMG

def is_excel(file):
    XLS = ('.csv', '.xls', '.xlsx')
    return isinstance(file, str) and _file_ext(file) in XLS

def read_yaml(file):
    if not is_yaml(file):
        raise IOError('File {0} is not a yaml file'.format(file))

    folder = path.dirname(path.abspath(file))

    stream = open(file, 'r')
    yaml_dict = yaml.load(stream)

    if yaml_dict is None: yaml_dict = {}

    # append include files to dict
    files = yaml_dict.pop('INCLUDE', [])

    # read all included files and add items to dict
    for file in files:

        # take care of relative path
        if not(path.isabs(file)):
            file = path.join(folder, file)

        append_dict = read_yaml(file)  # recursive call

        # check if key already existed warn if key will be overwritten
        for key in append_dict.keys():
            if key in yaml_dict.keys():
                ps.logger.warning('Duplicate data found in file' + \
				          '{0} for key {1}'.format(file, key))

        # append data (append_dict keys overwrite yaml_dict keys if duplicates)
        yaml_dict = {**yaml_dict, **append_dict}

    return yaml_dict

def write_yaml(file_name, dict_obj):
    stream = open(file_name, 'w')
    yaml.dump(dict_obj, stream=stream, default_flow_style=False)



def read_resources():
    """ read resource files and add to pyshield data """
    #resource files are defined in the yml file in the package root

    files =  read_yaml(path.join(ps.__pkg_root__, ps.RESOURCE_FILE))

    # read resource files either yaml or in excel format for buildup
    data = {}

    resource_dir = path.join(ps.__pkg_root__, 'resources')

    for key, file in files.items():

        full_file = path.join(resource_dir, file)
        ps.logger.debug('Loading resource {0}'.format(full_file))
        data[key] = load_file(full_file)


    RESOURCES.update(data)

    return data

def load_file(file):
    """ read file from disk (.yml, .xls/.xlsx and images) """
    if not path.exists(file):
        raise FileNotFoundError

    ps.logger.debug('Loading: %s', file)


    if is_yaml(file):
        reader = read_yaml
    elif is_excel(file):
        reader = lambda f: pd.read_excel(f, sheet_name=None)  # read all sheets
    elif is_img(file):
        reader = lambda f: np.flipud(mpimg.imread(f))
    else:
        raise TypeError

    # try:
    data = reader(file)
#    except:
#        raise IOError('Could not read file {0}'.format(file))

    return data






