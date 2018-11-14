# -*- coding: utf-8 -*-
"""
Visualization tools for showing the results of a pyshield calculation run.

A heatmap is shown on top of the floor plan. Isocontours specified in the
config file are shown as well.

Last Updated 05-02-2016
"""
import pyshield as ps
import numpy as np
import pyshield
import yaml
from matplotlib import pyplot as plt
from tkinter import messagebox
import logging

DEBUG = False

def styles():
    # get copy of viz settings so that local changes don't update 
    # global settings
    return ps.config.get_setting(ps.VISUALIZATION, {}).copy()

def format_color(color):
    # Colors can be specified as 8-bit, mpl expects values between 0 and 1
    if type(color) in (tuple, list) and len(color) == 3:
        #rgb color
        color = [c/255 for c in color]
    return color

def item_style(item, item_type=''):
    style = styles()[item_type]
    # override default style for each barrier if keys are specified for that 
    # barrier.
    for key in style.keys():
        if key in item.keys():
            style[key] = item[key]
            
    if ps.COLOR in style.keys():
        style[ps.COLOR] = format_color(style[ps.COLOR])
    return style

def barrier_style(barrier):
    style = item_style(barrier, ps.BARRIER)
    
    # Label is used as legend label for matplotlib
    if ps.LABEL not in style.keys():
        label = '' 
        for material, thickness in barrier[ps.MATERIAL].items():
            if label != '':
                label += '\n'
            
            label += material  + ': ' +  str(thickness) + ' cm'
        style[ps.LABEL] = label        

        
    # Colors may be determined by material type or label
    colors = style.get(ps.COLORS, {})

    # default color
    color = style[ps.COLOR] 
    
    # override with material and thickness specific colors
    materials = barrier[ps.MATERIAL]
    if len(materials) == 1:        
        material = list(materials.keys())[0]
        thickness = list(materials.values())[0]
        thickness_color = colors.get(material, {})
        color = thickness_color.get(thickness, color)
        
    # override with label color
    color = colors.get(ps.LABEL, {}).get(style[ps.LABEL], color) 
        
    # format color 
    if ps.COLOR in style.keys():
        style[ps.COLOR] = format_color(color)
    
    return style

def point_style(point):
    style = item_style(point, ps.POINT)
    style[ps.LABEL] = str(point)
    return style

def source_style(source):
    style = item_style(source, ps.SOURCE)
    style[ps.LABEL] = str(source)
    return style
    

def calc_dose_at_point(point):
    """ Calculate the dose at a specific point """

    ps.logger.info('Calculate dose at point')
    config = {}

    if not hasattr(pyshield, 'RUN_CONFIGURATION'):
        raise RuntimeError

    config = pyshield.RUN_CONFIGURATION
    config[ps.MULTI_CPU] = False
    config[ps.LOG] = logging.ERROR
    config[ps.CALCULATE] = ps.POINTS
    config[ps.POINTS] = {'double click': {ps.LOCATION: point}}
    config[ps.SHOW] = []
    config[ps.EXPORT_EXCEL] = []
    config[ps.EXPORT_IMAGES] = []
    
    # run all calculations
    if DEBUG:
        ps.logger.debug('Running with config %s', config)
    result = pyshield.run(**config)
    ps.logger.info('Finished')

    return result

def show_floorplan(points = {}, sources = {}):
    """ Show shielding barriers on top of floor plan. """
    #get application data
    floor_plan = ps.config.get_setting(ps.FLOOR_PLAN)
    barriers  = ps.config.get_setting(ps.BARRIERS)

    #==========================================================================
    #   Functions to help plotting
    #==========================================================================

    def figure_click(event):
        """ Calculate dose at mouse position on double click and display. """
        result = None
        if DEBUG:
            ps.logger.debug('Figure click %s', event)
        dose = None
        if event.dblclick:
            if DEBUG:
                ps.logger.debug('double click')
                ps.logger.debug(str(event))
       
            result = calc_dose_at_point((event.xdata, event.ydata))
           
            dose = result[ps.SUM_TABLE][ps.DOSE_MSV][0]
            messagebox.showinfo(title='caclulation',
                                message='Total Dose: {0}'.format(dose))

        return dose

    def object_click(event):
        """Callback for mouse click on object (source or shielding) """

        name = event.artist.name

        if name in barriers.keys():
            title = ps.BARRIER
            item = barriers[name]
        elif name in sources.keys():
            title = ps.SOURCE
            item = sources[name]
        elif name in points.keys():
            title = ps.POINT
            item = points[name]
        else:
            if DEBUG:
                ps.logger.debug('Unknown name %s', name)
            item = None
        if item:
            item[ps.NAME] = name # add name to output window
            messagebox.showinfo(title=title,
                                message=yaml.dump(item))
            
        return True


    def draw_barriers(barriers):
        def draw_barrier(name, barrier):
            style = barrier_style(barrier)
            style[ps.NAME] = name
            if DEBUG:
                ps.logger.debug('start drawing %s', name)
            
            location = np.array(barrier[ps.LOCATION])
            
            _, labels = plt.gca().get_legend_handles_labels()

            if style[ps.LABEL] in labels:
                # if label already in the lagend do nat add
                label = None
            else:
                label = style[ps.LABEL]
                
            if DEBUG:
                msg = 'Adding %s with style %s'
                ps.logger.debug(msg, name, str(style))

            l = [[location[0], location[2]], [location[1], location[3]]]
            
            
            if DEBUG:
                ps.logger.debug('at location %s', l)
            
            line = plt.plot(*l,
                            color     = style[ps.COLOR],
                            linestyle = style[ps.LINE_STYLE],
                            linewidth = style[ps.LINE_WIDTH],
                            picker    = style[ps.LINE_WIDTH],
                            label     = label)[0]

            
            line.name = name
            return line

        lines = []
        for name, barrier in barriers.items():
            line = draw_barrier(name, barrier)
            lines += [line]
        return lines

    def annotate(item, style={}):            
        DELTA = 20
        offset = np.array((0, 0))
        ha = 'center'
        va = 'center'
        if 'left' in style[ps.ALIGNMENT]:
            offset[0] -= DELTA
            ha = 'right'
        if 'right' in style[ps.ALIGNMENT]:
            offset[0] += DELTA
            ha = 'left'
        if 'top' in style[ps.ALIGNMENT]:
            offset[1] += DELTA
            va = 'bottom'
        if 'bottom' in style[ps.ALIGNMENT]:
            offset[1] -= DELTA
            va = 'top'
            
        plt.annotate(style[ps.NAME], xy=item[ps.LOCATION], xytext = offset,
                     textcoords='offset points', ha=ha, va=va,
                     bbox=dict(boxstyle='round,pad=0.5',
                               fc='yellow',
                               alpha=0.5),
                     arrowprops=dict(arrowstyle = '->',
                                     connectionstyle='arc3,rad=0'))
    
    def draw_point(name, point, style):
            style[ps.NAME] = name
            if DEBUG:
                ps.logger.debug('Drawing %s with value %s', name, str(point))
                ps.logger.debug('Plotting point %s', name)
            
            plot_fcn = lambda xy: plt.plot(*xy,
                                           color  = style[ps.COLOR],
                                           marker = style[ps.MARKER],
                                           picker = 5)

            p = plot_fcn(point[ps.LOCATION])
            p[0].name = name
            annotate(point, style=style)

            return p
        
    
    def _draw_points(points, item_type=ps.POINT):
        points_drawn = []
        if item_type == ps.POINT:
            styler = lambda point: point_style(point)
        elif item_type == ps.SOURCE:
            styler = lambda point: source_style(point)
        
        for name, point in points.items():
            style = styler(point)
            if DEBUG:
                ps.logger.debug('Plotting %s at %s with style %s', name, 
                                str(point), str(style))
            points_drawn += [draw_point(name, point, style)]
            
        return points_drawn

    def draw_points(points):
        if DEBUG:
            ps.logger.debug('Drawing %s points', str(len(points)))
        return _draw_points(points, item_type=ps.POINT)
    
    def draw_sources(points):
        if DEBUG:
            ps.logger.debug('Drawing %s sources', str(len(sources)))
        return _draw_points(points, item_type=ps.SOURCE)

    # show floor plan
    fig = plt.figure(figsize = styles()[ps.FIGURE][ps.FIG_SIZE])
    plt.imshow(floor_plan, extent = get_extent(floor_plan), origin = 'lower')

    if barriers:
        draw_barriers(barriers) # plot shielding baririers
    if sources:
        draw_sources(sources)    # plot sources
    if points:
        draw_points(points)      # points
    
    
    # sort and show legend
    box = plt.gca().get_position()
    plt.gca().set_position([box.x0, box.y0, box.width * 0.8, box.height])
    handles, labels = plt.gca().get_legend_handles_labels()

    # sort both labels and handles by labels
    if len(handles) > 0:
        labels, handles = zip(*sorted(zip(labels, handles),
                                      key=lambda t: t[0]))

        plt.gca().legend(handles, labels,
                         loc='center left',
                         bbox_to_anchor=(1, 0.5))

    fig.canvas.mpl_connect('pick_event', object_click)
    fig.canvas.mpl_connect('button_press_event', figure_click)
    return fig


def plot_dose_map(dose_map=None, legend=None, title = ''):
    """ Plot a heatmap with isocontours on top of the floorplan wiht barriers """
    
    floor_plan = ps.config.get_setting(ps.FLOOR_PLAN)
    extent=get_extent(floor_plan)
    
    style = styles()[ps.DOSE_MAP]

    fig = show_floorplan()

    # show heatmap
    plt.imshow(dose_map,
               extent   = get_extent(floor_plan),
               origin   = 'lower',
               alpha    = 0.5,
               clim     = style[ps.CLIM],
               cmap     = style[ps.COLOR_MAP])

    # show isocontours
    ps.logger.info('dose_map shape %s', dose_map.shape)

    isocontours = np.array(list(style[ps.LINES].keys()))
    isocontour_colors = np.array(list(style[ps.LINES].values()))

    isocontour_colors = isocontour_colors[isocontour_colors.argsort()]
    isocontours.sort()
    if DEBUG:
        ps.logger.debug('Isocontours: %s', str(isocontours))
        ps.logger.debug('Isocontour_colors: %s', str(isocontour_colors))

    contour = plt.contour(dose_map, isocontours,
                          colors=isocontour_colors, extent=extent)

    # show isocontour value in line
    plt.clabel(contour, inline=1, fontsize=style[ps.FONT_SIZE])

    # show legend for isocontours
    legend_labels = [str(value) + ' mSv' for value in isocontours]

    legend_loc = styles()[ps.FIGURE][ps.LEGEND_LOCATION]
    plt.legend(contour.collections, legend_labels, loc=legend_loc)
    
    if legend is not None:
      plt.gca().add_artist(legend)

    plt.title(title)
    fig.canvas.set_window_title(title)
    
    
    
    return fig


def show(results = {}):
    """ Show dose maps, shielding, sources and isocontours as specified in the
    application settings."""

    # obtain the setting from config.yml
    show_setting = ps.config.get_setting(ps.SHOW)

    # make list for non lists
    if not isinstance(show_setting, (tuple, list)):
        show_setting = [show_setting]
    
    if DEBUG:
        ps.logger.debug('%s dose_maps loaded for visualization', len(results))
        ps.logger.debug('Showing %s', show_setting)

    figures = {}

    if ps.FLOOR_PLAN in show_setting:
        figures[ps.FLOOR_PLAN] = show_floorplan()
    if ps.SOURCES in show_setting:
        sources = ps.config.get_setting(ps.SOURCES)
        figures[ps.SOURCES] = show_floorplan(sources=sources)
    if ps.POINTS in show_setting:
        points = ps.config.get_setting(ps.POINTS)
        figures[ps.POINTS] = show_floorplan(points=points)
   
    if ps.SUM_SOURCES in show_setting or ps.ALL_SOURCES in show_setting:
        try:
            dose_maps = results[ps.DOSE_MAPS]
        except (TypeError, KeyError):
            dose_maps = None
            ps.logger.error('No dose maps found in results')

        if ps.SUM_SOURCES in show_setting and dose_maps:
            summed_dose_map = results[ps.DOSE_MAPS][ps.SUM_SOURCES]
            figures[ps.SUM_SOURCES] = plot_dose_map(summed_dose_map,
                   title = ps.SUM_SOURCES)

        if ps.ALL_SOURCES in show_setting and dose_maps:
            for source, dose_map in dose_maps.items():
                ps.logger.info('plotting %s', source)
                figures[source] = plot_dose_map(dose_map, title = source)

    return figures


def get_extent(floorplan):
    """ Return boundaries of the image in physical coordinates """

    origin = ps.config.get_setting(ps.ORIGIN)
    scale = ps.config.get_setting(ps.SCALE)


    extent_pixels = (0.5 , floorplan.shape[1]-0.5,
                      0.5, floorplan.shape[0]-0.5)
    extent_cm = (extent_pixels[0]*scale - origin[0],
                 extent_pixels[1]*scale - origin[0],
                 extent_pixels[2]*scale - origin[1],
                 extent_pixels[3]*scale - origin[1])

    return extent_cm








