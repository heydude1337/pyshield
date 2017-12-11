# -*- coding: utf-8 -*-
"""
Visualization tools for showing the results of a pyshield calculation run.

A heatmap is shown on top of the floor plan. Isocontours specified in the
config file are shown as well.

Last Updated 05-02-2016
"""

import numpy as np
import pyshield
import traceback
from matplotlib import pyplot as plt
from os.path import join
from os import makedirs
from datetime import datetime

import pyshield as ps


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
DEFAULT_ALIGNMENT     = 'top left'
FIG_SIZE              = [15, 15]

def sum_dose_maps(dose_maps):
    """ sum a collection of dose maps to obtain the total dose """
    ps.logger.debug('Summing %s dose_maps', len(dose_maps))
    dose_maps = np.stack(dose_maps)
    return np.nansum(dose_maps, axis=0)


def barrier_color(barrier):
    """ Determine color for barrier (lookup in the materials colors dict) """

    colors    = ps.config.get_setting(ps.MATERIAL_COLORS)
    material  = list(barrier[ps.MATERIAL].keys())[0]
    thickness = barrier[ps.MATERIAL][material]

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

    ps.logger.info('Calculate dose at point')
    config = {}

    if not hasattr(pyshield, 'RUN_CONFIGURATION'):
        raise RuntimeError

    config = pyshield.RUN_CONFIGURATION
    config[ps.CALCULATE] = ps.POINTS
    config[ps.POINTS] = {'double click': {ps.LOCATION: point}}

    # run all calculations
    ps.logger.debug('Running with config %s', config)
    result = pyshield.run(**config)
    ps.logger.info('Finished')

    return result

def show_floorplan():
    """ Show shielding barriers on top of floor plan. """
    #get application data
    floor_plan = ps.config.get_setting(ps.FLOOR_PLAN)
    shielding  = ps.config.get_setting(ps.SHIELDING)
    sources    = ps.config.get_setting(ps.SOURCES)
    points     = ps.config.get_setting(ps.POINTS)



    #==========================================================================
    #   Functions to help plotting
    #==========================================================================

    def shielding_descr(name):
        """ Return information about shielding when line is clicked """
        materials = ''

        for material, thickness in shielding[name][ps.MATERIAL].items():
            if materials != '':
                materials += '\n'
            materials += material  + ': ' + str(thickness) + ' cm'


        location = shielding[name][ps.LOCATION]
        return (name, materials, location)

    def source_descr(name):
        """ Return information about source when point is clicked """
        try:
          text = 'Isotope: {isotope} \nEquivalent Activity: {activity}'
          source = sources[name]

          activity = ps.isotope.equivalent_activity(source)
          text = text.format(isotope=source[ps.ISOTOPE],
                             activity='{0} MBq'.format(np.round(activity)))
        except:
          traceback.print_exc()
        return name, text


    def figure_click(event):
        """ Calculate dose at mouse position on double click and display. """
        result = None
        ps.logger.debug('Figure click %s', event)
        if event.dblclick:
            ps.logger.debug('double click')
            ps.logger.debug(str(event))
            try:
                result = calc_dose_at_point((event.xdata, event.ydata))
            except:
                print('Error during point calculation!')
                traceback.print_exc()

            print('{0}'.format(result))
            print('Total Dose: {0}'.format(np.sum(result[ps.DOSE_MSV])))
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
        for material, thickness in barrier[ps.MATERIAL].items():
            density = ps.RESOURCES[ps.MATERIALS][material][ps.DENSITY]
            d += (thickness * density)
        return 30 # d

    def draw_barriers(barriers):
        def draw_barrier(name, barrier):

            ps.logger.debug('start drawing %s', name)
            location = np.array(barrier[ps.LOCATION])

            linewidth = draw_thickness(barrier) * WALL_THICKNESS_SCALE

            color = barrier_color(barrier)



            label = shielding_descr(name)[1]
            _, labels = plt.gca().get_legend_handles_labels()

            if label in labels:
                # if label already in the lagend do nat add
                label = None
            msg = 'Adding %s with thickness %s and color %s'
            ps.logger.debug(msg, label, linewidth, color)

            l = [[location[0], location[2]], [location[1], location[3]]]
            ps.logger.debug('at location %s', l)

            line = plt.plot(*l,
                            color     = color,
                            linestyle = WALL_LINE_STYLE,
                            linewidth = linewidth,
                            picker    = linewidth,
                            label     = label)[0]

            ps.logger.debug(line)
            line.name = name
            # plt.show()
            return line

        lines = []
        for name, barrier in barriers.items():
            line = draw_barrier(name, barrier)
            lines += [line]
        return lines

    def annotate(name, point, alignment = DEFAULT_ALIGNMENT):
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

            plt.annotate(name, xy=point, xytext = offset,
                         textcoords='offset points', ha=ha, va=va,
                         bbox=dict(boxstyle='round,pad=0.5',
                                   fc='yellow',
                                   alpha=0.5),
                         arrowprops=dict(arrowstyle = '->',
                                         connectionstyle='arc3,rad=0'))

    def draw_points(points):

        def draw_point(name, point, alignment = DEFAULT_ALIGNMENT):

            ps.logger.debug('Drawing %s at location %s and alignebt %s', name, point, alignment)



            ps.logger.debug('Plotting point %s', name)
            plot_fcn = lambda xy: plt.plot(*xy,
                                           color  = POINT_COLOR,
                                           marker = POINT_SHAPE,
                                           picker = 5)

            p = plot_fcn(point)

            annotate(name, point, alignment = alignment)

            return p

        points_drawn = []
        for name, point in points.items():
            location = point[ps.LOCATION]
            alignment = point.get(ps.ALIGNMENT, DEFAULT_ALIGNMENT)



            points_drawn += [draw_point(name, location, alignment)]

        return points_drawn

    def draw_sources(sources):
      if sources is None or sources == {}:
        ps.logger.warning('No Sources Defined!')
        sources = {}

      def draw_source(name, source, alignment = DEFAULT_ALIGNMENT):
          ps.logger.debug('Plotting source %s', name)
          plot_fcn = lambda xy: plt.plot(*xy,
                                         color  = SOURCE_COLOR,
                                         marker = SOURCE_SHAPE,
                                         picker = 5)

          location = np.array(source[ps.LOCATION])

          p = plot_fcn(location)[0]
          p.name = name

          alignment = source.get(ps.ALIGNMENT, DEFAULT_ALIGNMENT)
          annotate(name, location, alignment = alignment)
          # plt.show()

          return p

      points = []
      for name, source in sources.items():
          alignment = source.get(ps.ALIGNMENT, DEFAULT_ALIGNMENT)
          p = draw_source(name, source, alignment)
          points += [p]

      return points


    # show floor plan
    fig = plt.figure(figsize = FIG_SIZE)
    plt.imshow(floor_plan, extent = get_extent(floor_plan), origin = 'lower')




    ps.logger.debug(sources.keys())
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
    plt.show(block = False)
    return (fig, legend)


def plot_dose_map(dose_map=None, legend=None):
    """ Plot a heatmap with isocontours on top of the floorplan wiht barriers """

    clim = ps.config.get_setting(ps.CLIM_HEATMAP)
    colormap = ps.config.get_setting(ps.COLORMAP)
    floor_plan = ps.config.get_setting(ps.FLOOR_PLAN)
    isocontour_lines = ps.config.get_setting(ps.ISOCONTOUR_LINES)

    extent=get_extent(floor_plan)

    ps.logger.debug('clims: %s', clim)
    ps.logger.debug('colormap: %s', colormap)

    ps.logger.debug('loading floor_plan')
    fig, legend = show_floorplan()
    ps.logger.debug('floor_plan loaded')


    # show heatmap
    plt.imshow(dose_map,
               extent   = get_extent(floor_plan),
               origin   = 'lower',
               alpha    = 0.5,
               clim     = clim,
               cmap     = plt.get_cmap(colormap))

    # show isocontours
    ps.logger.info('dose_map shape %s', dose_map.shape)

    isocontours = np.array(list(isocontour_lines.keys()))
    isocontour_colors = np.array(list(isocontour_lines.values()))

    isocontour_colors = isocontour_colors[isocontour_colors.argsort()]
    isocontours.sort()

    ps.logger.debug('Isocontours: %s', str(isocontours))
    ps.logger.debug('Isocontour_colors: %s', str(isocontour_colors))

    contour = plt.contour(dose_map, isocontours,
                          colors=isocontour_colors, extent=extent)

    # show isocontour value in line
    plt.clabel(contour, inline=1, fontsize=LABEL_TEXT_SIZE)

    # show legend for isocontours
    legend_labels = [str(value) + ' mSv' for value in isocontours]

    plt.legend(contour.collections, legend_labels, loc=LEGEND_LOCATION)
    if legend is not None:
      plt.gca().add_artist(legend)
    return fig, None


def show(results = {}):
    """ Show dose maps, shielding, sources and isocontours as specified in the
    application settings."""


    show_setting = ps.config.get_setting(ps.SHOW).lower()

    if not isinstance(show_setting, (tuple, list)):
        show_setting = [show_setting]

    ps.logger.debug('%s dose_maps loaded for visualization', len(results))
    ps.logger.debug('Showing %s dose_maps', show_setting)

    figures = {}

    if ps.FLOOR_PLAN in show_setting:
        figures[ps.FLOOR_PLAN], _ = show_floorplan()






    dose_maps = results[ps.DOSE_MAPS]
    if len(results) == 0 or dose_maps is None or len(dose_maps) == 0:
        fig, _ = show_floorplan()
        return {ps.FLOOR_PLAN: fig}

    def plot(dose_map, title = ''):
        """ Display a dose map and give figere a title."""
        try:
          ps.logger.info('plotting %s', title)
          figure, _ = plot_dose_map(dose_map)
        except:
          ps.logger.error('failed plotting %s', title)
          traceback.print_exc()
          return None

        figure.canvas.set_window_title(title)
        plt.gca().set_title(title)
        maximize_window()

        return figure

    figures={}
    # show and save all figures it config property is set to show all
    if show_setting == 'all':
        for key, dose_map in results[ps.DOSE_MAPS].items():
            figures[key] = plot(dose_map,  title = key)

    if show_setting in ('all', 'sum'):
        figures['sum'] = plot(sum_dose_maps(dose_maps.values()), title = 'sum')

    return figures

def save(figures = None, dose_maps = None):
    """ Save figures/dose maps to disk. Export dir is defined in application
        settings."""
    export_dir = ps.config.get_setting(ps.EXPORT_DIR)
    save_images = ps.config.get_setting(ps.SAVE_IMAGES)

    makedirs(export_dir, exist_ok=True)

    if save_images:
        for name, figure in figures.items():
            file = join(export_dir, name)
            save_figure(figure, file)


#def maximize_window():
#    """ Maximize the current plot window """
#    backend = plt.get_backend()
#    mng = plt.get_current_fig_manager()
#
#    # Maximization depends on matplotlib backend
#    if backend in ( 'Qt4Agg', 'Qt5Agg'):
#        mng.window.showMaximized()
#    elif backend == 'wxAgg':
#        mng.frame.Maximize(True)
#    elif backend == 'TkAgg':
#        mng.window.state('zoomed')
#    elif backend == 'MacOSX':
#        mng.full_screen_toggle()
#    else:
#        msg = 'Cannot maximize a pyplot figure that uses %s as backend'
#        ps.logger.warn(msg, backend)
#    return


def get_extent(floorplan):
    """ Return boundaries of the image in physical coordinates """

    ps.logger.debug(ps.config.__str__())
    origin = ps.config.get_setting(ps.ORIGIN)
    scale = ps.config.get_setting(ps.SCALE)


    extent_pixels = (0.5 , floorplan.shape[1]-0.5,
                      0.5, floorplan.shape[0]-0.5)
    extent_cm = (extent_pixels[0]*scale - origin[0],
                 extent_pixels[1]*scale - origin[0],
                 extent_pixels[2]*scale - origin[1],
                 extent_pixels[3]*scale - origin[1])

    return extent_cm

def save_figure(fig, source_name):
    """ save specifed figure to disk, file name gets a time stamp appended"""

    fname = ps.config.get_setting(ps.EXPORT_FNAME)
    export_dir = ps.config.get_setting(ps.EXPORT_DIR)
    dpi = ps.config.get_setting(ps.IMAGE_DPI)

    if '{time_stamp}' and '{source_name}' in fname:
        time_stamp = datetime.strftime(datetime.now(), '_%Y%m%d-%H%M%S')
        fname = fname.format(time_stamp = time_stamp,
                             source_name = source_name)
    else:
        ps.logger.error('Invalid filename: ' + fname)

    fname = join(ps.config.get_setting(export_dir, fname))

    ps.logger.debug('Writing: ' + fname)
    fig.savefig(fname, dpi=dpi, bbox_inches='tight')



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




