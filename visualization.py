# -*- coding: utf-8 -*-
"""
Visualization tools for showing the results of a pyshield calculation run.

A heatmap is shown on top of the floor plan. Isocontours specified in the
config file are shown as well.

Last Updated 05-02-2016
"""

import yaml
import numpy as np
import pickle
import pyshield
import traceback
from matplotlib import pyplot as plt
from os.path import join
from os import makedirs
from datetime import datetime

from pyshield import CONST, get_setting, log
from pyshield.resources import RESOURCES
from pyshield.calculations.isotope import equivalent_activity

# Default Visualisation options
WALL_COLOR            = 'b'
WALL_LINE_STYLE       = '-'
WALL_THICKNESS_SCALE  = 0.1
SOURCE_COLOR          = 'r'
SOURCE_SHAPE          = 'o'
LEGEND_LOCATION       = 4
POINT_COLOR           = 'b'
POINT_SHAPE           = 'o'
LABEL_TEXT_SIZE       = 10


def sum_dose_maps(dose_maps):
    """ sum a collection of dose maps to obtain the total dose """
    log.debug('Summing %s dose_maps', len(dose_maps))

    dose_maps = np.stack(dose_maps)
    return np.nansum(dose_maps, axis=0)


def barrier_color(barrier):
    """ Determine color for barrier (lookup in the materials colors dict) """

    colors    = get_setting(CONST.MATERIAL_COLORS)
    material  = list(barrier[CONST.MATERIAL].keys())[0]
    thickness = barrier[CONST.MATERIAL][material]

    try:
        color = colors[material][thickness]
    except KeyError:
        color = WALL_COLOR

    if type(color) in (tuple, list) and len(color) == 3:
        #rgb color
        color = [c/255 for c in color]

    return color

def calc_dose_at_point(point):
    """ Calculate the dose at a specific point """

    log.info('Calculate dose at point')
    config = {}

    if not hasattr(pyshield, 'RUN_CONFIGURATION'):
        raise RuntimeError

    config = pyshield.RUN_CONFIGURATION
    config[CONST.CALCULATE] = CONST.POINTS
    config[CONST.POINTS] = {'double click': {CONST.LOCATION: point}}

    # run all calculations
    log.debug('Running with config %s', config)
    result = pyshield.run.run_with_configuration(**config)
    log.info('Finished')

    return result

def show_floorplan():
    """ Show shielding barriers on top of floor plan. """
    #get application data
    floor_plan = get_setting(CONST.FLOOR_PLAN)
    shielding  = get_setting(CONST.SHIELDING)
    sources    = get_setting(CONST.SOURCES)
    points     = get_setting(CONST.POINTS)



    #==========================================================================
    #   Functions to help plotting
    #==========================================================================

    def shielding_descr(name):
        """ Return information about shielding when line is clicked """
        materials = ''

        for material, thickness in shielding[name][CONST.MATERIAL].items():
            if materials != '':
                materials += '\n'
            materials += material  + ': ' + str(thickness) + ' cm'


        location = shielding[name][CONST.LOCATION]
        return (name, materials, location)

    def source_descr(name):
        """ Return information about source when point is clicked """
        try:
          text = 'Isotope: {isotope} \nEquivalent Activity: {activity}'
          source = sources[name]

          activity = equivalent_activity(source)
          text = text.format(isotope=source[CONST.ISOTOPE],
                             activity='{0} MBq'.format(np.round(activity)))
        except:
          traceback.print_exc()
        return name, text


    def figure_click(event):
        """ Calculate dose at mouse position on double click and display. """
        result = None
        log.debug('Figure click %s', event)
        if event.dblclick:
            log.debug('double click')
            log.debug(str(event))
            try:
                result = calc_dose_at_point((event.xdata, event.ydata))
            except:
                print('Error during point calculation!')
                traceback.print_exc()

            print('{0}'.format(result))
            print('Total Dose: {0}'.format(np.sum(result[CONST.DOSE_MSV])))
            result.to_excel('output.xslx')
        return result

    def object_click(event):
        """Callback for mouse click on object (source or shielding) """

        obj_name = event.artist.name

        if obj_name in shielding.keys():
            # shielding item clicked
            msg = 'Barrier: {0}\nShielding: {1}\nAt location: {2}'
            print(msg.format(*shielding_descr(obj_name)))
        elif obj_name in sources.keys():
            name, text = source_descr(obj_name)
            print('Source: {0}\n{1}'.format(name, text))
        else:
            raise KeyError



        return True

    def draw_thickness(barrier):
        """ Barrier thickness weighted by density """
        d = 0
        for material, thickness in barrier[CONST.MATERIAL].items():
            density = RESOURCES[CONST.MATERIALS][material][CONST.DENSITY]
            d += (thickness * density)
        return 30 # d

    def draw_barriers(barriers):
        def draw_barrier(name, barrier):

            log.debug('start drawing %s', name)
            location = np.array(barrier[CONST.LOCATION])

            linewidth = draw_thickness(barrier) * WALL_THICKNESS_SCALE

            color = barrier_color(barrier)



            label = shielding_descr(name)[1]
            _, labels = plt.gca().get_legend_handles_labels()

            if label in labels:
                # if label already in the lagend do nat add
                label = None
            msg = 'Adding %s with thickness %s and color %s'
            log.debug(msg, label, linewidth, color)

            l = [[location[0], location[2]], [location[1], location[3]]]
            log.debug('at location %s', l)

            line = plt.plot(*l,
                            color     = color,
                            linestyle = WALL_LINE_STYLE,
                            linewidth = linewidth,
                            picker    = linewidth,
                            label     = label)[0]

            log.debug(line)
            line.name = name
            plt.show()
            return line

        lines = []
        for name, barrier in barriers.items():
            line = draw_barrier(name, barrier)
            lines += [line]
        return lines

    def draw_points(points):
        DEFAULT_ALIGNMENT = 'top left'

        def draw_point(name, point, alignment = DEFAULT_ALIGNMENT):

            log.debug('Drawing %s at location %s and alignebt %s', name, point, alignment)

            DELTA = 20
            offset = np.array((0, 0))
            ha = 'center'
            va = 'center'
            if 'left' in alignment:
                offset[0] -= DELTA
                ha = 'right'
            if 'right' in alignment:
                offset[0] += DELTA
                ha = 'left'
            if 'top' in alignment:
                offset[1] += DELTA
                va = 'bottom'
            if 'bottom' in alignment:
                offset[1] -= DELTA
                va = 'top'

            log.debug('Plotting point %s', name)
            plot_fcn = lambda xy: plt.plot(*xy,
                                           color  = POINT_COLOR,
                                           marker = POINT_SHAPE,
                                           picker = 5)
            print(point)
            p = plot_fcn(point)
            plt.annotate(name, xy=point, xytext = offset,
                         textcoords='offset points', ha=ha, va=va,
                         bbox=dict(boxstyle='round,pad=0.5',
                                   fc='yellow',
                                   alpha=0.5),
                         arrowprops=dict(arrowstyle = '->',
                                         connectionstyle='arc3,rad=0'))
            return p

        points_drawn = []
        for name, point in points.items():
            location = point[CONST.LOCATION]
            alignment = point.get(CONST.ALIGNMENT, DEFAULT_ALIGNMENT)



            points_drawn += [draw_point(name, location, alignment)]

        return points_drawn

    def draw_sources(sources):
        def draw_source(name, source):
            log.debug('Plotting source %s', name)
            plot_fcn = lambda xy: plt.plot(*xy,
                                           color  = SOURCE_COLOR,
                                           marker = SOURCE_SHAPE,
                                           picker = 5)

            location = np.array(source[CONST.LOCATION])

            p = plot_fcn(location)[0]
            p.name = name

            plt.show()

            return p

        points = []
        for name, source in sources.items():
            p = draw_source(name, source)
            points += [p]

        return points


    # show floor plan
    fig = plt.figure()
    plt.imshow(floor_plan, extent = get_extent(floor_plan), origin = 'lower')





    draw_barriers(shielding) # plot shielding baririers
    draw_sources(sources)    # plot sources
    draw_points(points)      # points
    # sort and show legend
    box = plt.gca().get_position()
    plt.gca().set_position([box.x0, box.y0, box.width * 0.8, box.height])
    handles, labels = plt.gca().get_legend_handles_labels()

    # sort both labels and handles by labels
    if len(handles) > 0:
        labels, handles = zip(*sorted(zip(labels, handles),
                                      key=lambda t: t[0]))

        legend = plt.gca().legend(handles,
                                  labels, loc='center left',
                                  bbox_to_anchor=(1, 0.5))

    else:
        legend = None

    fig.canvas.mpl_connect('pick_event', object_click)
    fig.canvas.mpl_connect('button_press_event', figure_click)
    maximize_window()
    return (fig, legend)


def plot_dose_map(dose_map=None, legend=None):
    """ Plot a heatmap with isocontours on top of the floorplan wiht barriers """

    clim = get_setting(CONST.CLIM_HEATMAP)
    colormap = get_setting(CONST.COLORMAP)
    floor_plan = get_setting(CONST.FLOOR_PLAN)
    iso_contour_values = get_setting(CONST.ISO_VALUES)
    colors = get_setting(CONST.ISO_COLORS)
    extent=get_extent(floor_plan)

    log.debug('clims: %s', clim)
    log.debug('colormap: %s', colormap)

    log.debug('loading floor_plan')
    fig, legend = show_floorplan()
    log.debug('floor_plan loaded')


    # show heatmap
    plt.imshow(dose_map,
               extent   = get_extent(floor_plan),
               origin   = 'lower',
               alpha    = 0.5,
               clim     = clim,
               cmap     = plt.get_cmap(colormap))

    # show isocontours
    log.info('dose_map %s', dose_map.shape)

    contour = plt.contour(dose_map, iso_contour_values,
                          colors= colors, extent=extent)

    # show isocontour value in line
    plt.clabel(contour, inline=1, fontsize=LABEL_TEXT_SIZE)

    # show legend for isocontours
    legend_labels = [str(value) + ' mSv' for value in iso_contour_values]

    plt.legend(contour.collections, legend_labels, loc=LEGEND_LOCATION)
    plt.gca().add_artist(legend)
    return fig, None


def show(results = {}):
    """ Show dose maps, shielding, sources and isocontours as specified in the
    application settings."""

    show_setting = get_setting(CONST.SHOW).lower()
    log.debug('%s dosem_maps loaded for visualization', len(results))
    log.debug('Showing %s dose_maps', show_setting)

    if show_setting not in ('all', 'sum'):
      return None

    if len(results) == 0 or results[CONST.DOSE_MAPS] is None:
        fig, _ = show_floorplan()
        return {CONST.FLOOR_PLAN: fig}

    def plot(dose_map, title = ''):
        """ Display a dose map and give figere a title."""
        try:
          log.info('plotting %s', title)
          figure, _ = plot_dose_map(dose_map)
        except:
          log.error('failed plotting %s', title)
          traceback.print_exc()
          return None

        figure.canvas.set_window_title(title)
        plt.gca().set_title(title)
        maximize_window()

        return figure

    figures={}
    # show and save all figures it config property is set to show all
    if show_setting == 'all':
        for key, dose_map in results[CONST.DOSE_MAPS].items():
            print(key)
            figures[key] = plot(dose_map,  title = key)

    if show_setting in ('all', 'sum'):
        #points = np.concatenate([result[0] for result in results.values()])
        figures['sum'] = plot(sum_dose_maps(results[CONST.DOSE_MAPS].values()),
                                            title = 'sum')

    return figures

def save(figures = None, dose_maps = None):
    """ Save figures/dose maps to disk. Export dir is defined in application
        settings."""
    export_dir = get_setting(CONST.EXPORT_DIR)
    save_images = get_setting(CONST.SAVE_IMAGES)
    export_data = get_setting(CONST.SAVE_DATA)
    export_file_name = get_setting(CONST.EXPORT_FNAME)
    makedirs(export_dir, exist_ok=True)

    if save_images:
        for name, figure in figures.items():
            save_figure(figure, name.lower())


    if dose_maps is not None and export_data:
        if '{time_stamp}' in export_file_name:
            time_stamp = datetime.strftime(datetime.now(), '_%Y%m%d-%H%M%S')
            export_file_name = export_file_name.format(time_stamp = time_stamp)

        export_file_name = join(export_dir, export_file_name)

        log.debug('Pickle dumping data: ' + export_file_name)
        pickle.dump(dose_maps, open(export_file_name, 'wb'))
        log.debug('results dumped to file: ' + export_file_name)


def maximize_window():
    """ Maximize the current plot window """
    backend = plt.get_backend()
    mng = plt.get_current_fig_manager()

    # Maximization depends on matplotlib backend
    if backend in ( 'Qt4Agg', 'Qt5Agg'):
        mng.window.showMaximized()
    elif backend == 'wxAgg':
        mng.frame.Maximize(True)
    elif backend == 'TkAgg':
        mng.window.state('zoomed')
    elif backend == 'MacOSX':
        mng.full_screen_toggle()
    else:
        msg = 'Cannot maximize a pyplot figure that uses %s as backend'
        log.warn(msg, backend)
    return


def get_extent(floorplan):
    """ Return boundaries of the image in physical coordinates """

    origin = get_setting(CONST.ORIGIN)
    scale = get_setting(CONST.SCALE)


    extent_pixels = (0.5 , floorplan.shape[1]-0.5,
                      0.5, floorplan.shape[0]-0.5)
    extent_cm = (extent_pixels[0]*scale - origin[0],
                 extent_pixels[1]*scale - origin[0],
                 extent_pixels[2]*scale - origin[1],
                 extent_pixels[3]*scale - origin[1])

    return extent_cm

def save_figure(fig, source_name):
    """ save specifed figure to disk, file name gets a time stamp appended"""

    fname = get_setting(CONST.EXPORT_FNAME)
    export_dir = get_setting(CONST.EXPORT_DIR)
    dpi = get_setting(CONST.IMAGE_DPI)

    if '{time_stamp}' and '{source_name}' in fname:
        time_stamp = datetime.strftime(datetime.now(), '_%Y%m%d-%H%M%S')
        fname = fname.format(time_stamp = time_stamp,
                             source_name = source_name)
    else:
        log.error('Invalid filename: ' + fname)

    fname = join(get_setting(export_dir, fname))

    log.debug('Writing: ' + fname)
    fig.savefig(fname, dpi=dpi, bbox_inches='tight')

def cursor(name = '', shielding = None, fig = None, npoints = 2):
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
      wall[CONST.LOCATION] = [float(np.round(li)) for li in loc]
      wall[CONST.MATERIAL] = shielding.copy()
      walls[name + str(i)] = wall

    print(yaml.dump(walls, default_flow_style = False))

    return walls


def point(name = '', fig = None, npoints = 1,
          occupancy_factor = 1, alignment = 'top left'):

    p=np.round(plt.ginput(npoints))
    points = {}
    for i, pi in enumerate(p):
      pname = name + str(i + 1)
      points[pname] = {CONST.LOCATION:          [float(pi[0]), float(pi[1])],
                       CONST.OCCUPANCY_FACTOR:  occupancy_factor,
                       CONST.ALIGNMENT:          alignment}

    print(yaml.dump(points))
    return points

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
                      CONST.DOSE_MSV,
                      CONST.DOSE_OCCUPANCY_MSV,
                      CONST.OCCUPANCY_FACTOR))

  # iterate over table and select color based on tresholds
  for row in pandas_table.iterrows():

    index, data = row
    if data[CONST.DOSE_OCCUPANCY_MSV] > 0.3:
      color = colors.format(color = RED)
    elif data[CONST.DOSE_OCCUPANCY_MSV] > 0.1:
      color = colors.format(color = BLUE)
    else:
      color = colors.format(color = GREEN)

    # get values for output
    name = index
    dose = np.round(data[CONST.DOSE_MSV], decimals=2)
    corrected_dose = np.round(data[CONST.DOSE_OCCUPANCY_MSV], decimals = 2)
    occupancy = data[CONST.OCCUPANCY_FACTOR]

    msg =  output.format(name, dose, corrected_dose, occupancy)

    print(color + msg  + end_color)




