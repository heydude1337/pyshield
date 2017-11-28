# -*- coding: utf-8 -*-
from pyshield import get_setting, CONST

def export(results):
  if get_setting(CONST.EXPORT_EXCEL):
    if CONST.POINTS in get_setting(CONST.CALCULATE):
      sum_file_name = get_setting(CONST.EXCEL_FILENAME_SUMMARY)
      full_file_name = get_setting(CONST.EXCEL_FILENAME_FULLRESULT)
      if results[CONST.SUM_TABLE] is not None:
        results[CONST.SUM_TABLE].to_excel(sum_file_name)
        results[CONST.TABLE].to_excel(full_file_name)