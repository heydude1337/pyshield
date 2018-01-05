# -*- coding: utf-8 -*-
import pyshield as ps
import numpy as np
import os

def export(results):
    """ Export calculation results to file. """
    # export folder, create if not exists
    export_dir = ps.config.get_setting(ps.EXPORT_DIR)
    os.makedirs(export_dir, exist_ok = True)

    def export_table(table, file_name):
        # Write pandas table to disk
        if table is not None:
            table.to_excel(os.path.join(export_dir, file_name))


    # export tables to excel
    if ps.config.get_setting(ps.EXPORT_EXCEL):

        export_table(results[ps.SUM_TABLE],
                     ps.config.get_setting(ps.EXCEL_FILENAME_SUMMARY))


        export_table(results[ps.TABLE],
                     ps.config.get_setting(ps.EXCEL_FILENAME_FULLRESULT))

    # export images to png
    if ps.config.get_setting(ps.EXPORT_IMAGES):
        for key, figure in results[ps.FIGURE].items():
            figure.savefig(os.path.join(export_dir, key + '.png'))

    # print results to console
    if ps.SUM_TABLE in ps.config.get_setting(ps.SHOW):
        if results[ps.SUM_TABLE] is not None:
            ps.export.print_dose_report(results[ps.SUM_TABLE])


def print_dose_report(pandas_table):
    RED = 31
    #BLACK = 30
    BLUE = 34
    GREEN = 32

    #ANSI CODE for colors
    colors = "\x1b[1;{color}m"
    end_color = "\x1b[0m"



    # tabulated output
    output = '{:<15}' * 4

    # table header
    print(output.format('point name',
                        ps.DOSE_MSV,
                        ps.DOSE_OCCUPANCY_MSV,
                        ps.OCCUPANCY_FACTOR))

    # iterate over table and select color based on tresholds
    for row in pandas_table.iterrows():

      index, data = row
      if data[ps.DOSE_OCCUPANCY_MSV] > 0.3:
          color = colors.format(color = RED)
      elif data[ps.DOSE_OCCUPANCY_MSV] > 0.1:
          color = colors.format(color = BLUE)
      else:
          color = colors.format(color = GREEN)

      # get values for output
      name = data[ps.POINT_NAME]
      dose = np.round(data[ps.DOSE_MSV], decimals=2)
      corrected_dose = np.round(data[ps.DOSE_OCCUPANCY_MSV], decimals = 2)
      occupancy = data[ps.OCCUPANCY_FACTOR]

      msg =  output.format(name, dose, corrected_dose, occupancy)

      print(color + msg  + end_color)