# -*- coding: utf-8 -*-
import pyshield as ps
import numpy as np
import pandas as pd
import os

def export_images(results):
    """ Export calculation results to file. """
    export_dir = export_folder()
    
    
    # export images to png
    if ps.FIGURE in results.keys():
        for key, figure in results[ps.FIGURE].items():
            figure.savefig(os.path.join(export_dir, key + '.png'))

def export_folder():
    export_dir = ps.config.get_setting(ps.EXPORT_DIR)
    export_dir = os.path.realpath(export_dir)
    # keep install location clean during testing etc.
    pkg_folder = os.path.normpath(ps.__pkg_root__.lower()).lower()
    if pkg_folder in export_dir.lower():
        raise IOError('Files cannot be exported to pyshield install location')
    
    os.makedirs(export_dir, exist_ok = True)
    return export_dir

def export_excel(results):
    """ Write pandas tables to disk """
    
    export_dir = export_folder()
    
    
    file = os.path.join(export_dir,
                        ps.config.get_setting(ps.EXCEL_FILENAME))
    
    writer = pd.ExcelWriter(file, engine='xlsxwriter')
    
    results[ps.SOURCE_TABLE] = make_source_table()
    
    for key in (ps.SUM_TABLE, ps.TABLE, ps.SOURCE_TABLE):
        if key in results.keys():
            try:
                results[key].to_excel(writer, sheet_name=key)
                ps.logger.debug('%s written to excel', key)
            except:
                msg = 'Cannot write {0} to {1}'
                ps.logger.error(msg.format(key, ps.EXCEL_FILENAME_SUMMARY))
        else:
            ps.logger.debug('{0} not found in results'.format(key))
    writer.save()
    
def make_source_table():
    """ Create pandas table from source file for nice export """
    df = pd.DataFrame()
    sources = ps.config.get_setting('sources')
    for name, source in sources.items():
        df = df.append({'Name': name, **source}, ignore_index=True)
    return df
        
def print_dose_report(result):
    """ Print report table to commandline """
    if not ps.SUM_TABLE in result.keys():
        return
    pandas_table = result[ps.SUM_TABLE]
    style = ps.visualization.item_style({}, item_type=ps.TABLE)
    RED = 31
    #BLACK = 30
    BLUE = 34
    GREEN = 32

    #ANSI CODE for colors
    colors = "\x1b[1;{color}m"
    end_color = "\x1b[0m"

    # tabulated output
    output = '{:<20}' * 4

    # table header
    print(output.format('point name',
                        ps.DOSE_MSV,                        
                        ps.OCCUPANCY_FACTOR,
                        ps.DOSE_OCCUPANCY_MSV))

    # iterate over table and select color based on tresholds
    for row in pandas_table.iterrows():

      index, data = row
      if data[ps.DOSE_OCCUPANCY_MSV] > style[ps.DOSE_LIMIT_RED]:
          color = colors.format(color = RED)
      elif data[ps.DOSE_OCCUPANCY_MSV] > style[ps.DOSE_LIMIT_BLUE]:
          color = colors.format(color = BLUE)
      else:
          color = colors.format(color = GREEN)

      # get values for output
      name = data[ps.POINT_NAME]
      dose = np.round(data[ps.DOSE_MSV], decimals=2)
      corrected_dose = np.round(data[ps.DOSE_OCCUPANCY_MSV], decimals = 2)
      occupancy = data[ps.OCCUPANCY_FACTOR]

      msg =  output.format(name, dose, occupancy, corrected_dose)

      print(color + msg  + end_color)