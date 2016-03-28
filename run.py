# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 14:05:47 2016

@author: 757021
"""

import pyshield
from pyshield import data, const, config, log
from pyshield.calculations.grid import calc_dose_grid_source, sum_dose
import sys
import timeit


from multiprocessing import Pool, cpu_count

def single_cpu_calculation(sources):
  log.info('Single CPU Calculation')
  
  for key, source in sources.items():
    log.info('Calculating: ' + key)
    dose_maps[key] = calc_dose_grid_source(source)
    log.info(key + 'finished calculation.')
    print(key + 'finished calculation.')
  return dose_maps


def multi_cpu_calculation(sources, pool):
  log.info('Multiple CPU Calculation')
  
  results = {}
  for key, source in sources.items():
    #c#allback = lambda : callback(key)
    results[key] = pool.apply_async(calc_dose_grid_source, args=(source,))
    log.debug('Queueing calculation for: ' + key)
  
  dose_maps = {}   
  # gather results
  keys = list(results.keys())
  while len(results) > 0:
    for key in keys:
      if key in results.keys() and results[key].ready():
        log.debug('getting result for ' + key)
        dose_maps[key] = results.pop(key).get()
        log.info('Calculation finished: '  + key)   
        print('Calculation finished: '  + key)

  pool.close()
  pool.join()
  
  return dose_maps
          
  
if __name__ == '__main__':
  if len(sys.argv) == 2:
    pyshield.config_and_data.set_file(sys.argv[1])
  elif len(sys.arg) > 2:
    print('python run.py or python run.py config.yml')

  log.info('\n-----Starting calculations-----\n')
  
  
  sources = data[const.SOURCES]
  dose_maps = {}
  
  start = timeit.default_timer()  
  
  if const.MULTI_CPU in config.keys() and config[const.MULTI_CPU]:
    log.info('Multi CPU Calculation')
    pool = Pool(cpu_count())
    dose_maps = multi_cpu_calculation(sources, pool)
  else:
    dose_maps = single_cpu_calculation(sources)
    
  dose_maps[const.SUM_SOURCES] = sum_dose(dose_maps)  
  stop = timeit.default_timer()
  
  log.info("Calculation time: "  + str(round(stop-start)))
  log.info('\n-----Calculations finished-------\n')
  
  figs = pyshield.show(dose_maps)
  pyshield.save(figs, dose_maps)
  