# -*- coding: utf-8 -*-
import pyshield as ps
import os
def export(results):
  # export folder, create if not exists

  export_dir = ps.config.get_setting(ps.EXPORT_DIR)
  os.makedirs(export_dir, exist_ok = True)
  # check if export is requested
  if ps.config.get_setting(ps.EXPORT_EXCEL):
    if ps.POINTS in ps.config.get_setting(ps.CALCULATE):
      sum_file_name = ps.config.get_setting(ps.EXCEL_FILENAME_SUMMARY)
      full_file_name = ps.config.get_setting(ps.EXCEL_FILENAME_FULLRESULT)
      if results[ps.SUM_TABLE] is not None:
        results[ps.SUM_TABLE].to_excel(os.path.join(export_dir, sum_file_name))
        results[ps.TABLE].to_excel(os.path.join(export_dir, full_file_name))

  for key, figure in results[ps.FIGURE].items():


      figure.savefig(os.path.join(export_dir, key + '.png'))