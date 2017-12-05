# -*- coding: utf-8 -*-
import pyshield as ps

def export(results):
  if ps.config.get_setting(ps.EXPORT_EXCEL):
    if ps.POINTS in ps.config.get_setting(ps.CALCULATE):
      sum_file_name = ps.config.get_setting(ps.EXCEL_FILENAME_SUMMARY)
      full_file_name = ps.config.get_setting(ps.EXCEL_FILENAME_FULLRESULT)
      if results[ps.SUM_TABLE] is not None:
        results[ps.SUM_TABLE].to_excel(sum_file_name)
        results[ps.TABLE].to_excel(full_file_name)