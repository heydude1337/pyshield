

import matplotlib.pyplot as plt
import yaml
import numpy as np

import pyshield as ps

default_shielding = {'Lead': 0.2}


def wall(name = 'wall', shielding = default_shielding, fig = None, npoints = 2):
    if shielding is None:
        shielding = {'Lead': 1}

    if fig is None:
        fig = plt.gcf()

    points = fig.ginput(npoints)
    points = np.round(points)


    walls = {}

    for i in range(0, len(points)-1):
      wall = {}
      loc = list(points[i]) + list(points[i+1])
      wall[ps.LOCATION] = [float(np.round(li)) for li in loc]
      wall[ps.MATERIAL] = shielding.copy()
      walls[name + str(i)] = wall

    print(yaml.dump(walls, default_flow_style = False))

    return walls


def point(name = 'point', fig = None, npoints = 1,
          occupancy_factor = 1, alignment = 'top left'):

    p=np.round(plt.ginput(npoints))
    points = {}
    for i, pi in enumerate(p):
      pname = name + str(i + 1)
      points[pname] = {ps.LOCATION:          [float(pi[0]), float(pi[1])],
                       ps.OCCUPANCY_FACTOR:  occupancy_factor,
                       ps.ALIGNMENT:          alignment}

    print(yaml.dump(points))
    return points# -*- coding: utf-8 -*-

