""" Functions to read resource files (.yml, .xls/.xlsx and images) """

# -*- coding: utf-8 -*-


from os import path
import pandas as pd
import matplotlib.image as mpimg
import numpy as np
import yaml



import pyshield as ps


def load_item(item):
    """ Load yaml, image or excel or return value as is. """
    if isinstance(item, str):
        if is_yaml(item):
            try:
                item = read_yaml(item)
            except FileNotFoundError:
                item = {}
        if is_img(item):
            item = read_img(item)
        if is_excel(item):
            item = read_excel(item)
    
    if isinstance(item, dict):
        return dict(zip(item.keys(), map(load_item, item.values())))
    else:
        return item
    
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

def read_excel(file):
    return pd.read_excel(file, sheet_name=None)

def read_img(file):
    return np.flipud(mpimg.imread(file))

def read_yaml(file):
    """ 
    Read yaml file and include files that are defined with the INCLUDE tag
    """
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





