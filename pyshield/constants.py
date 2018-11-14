""" List of constants for the pyshield package

    Last Updated 13-11-2018 """

#==============================================================================
# General
#==============================================================================

DEF_CONFIG_FILE =               'default_config.yml'
CONFIG_FILE =                   'config.yml'
RUN_CONFIGURATION =             'run_configuration'
PKG_ROOT_MACRO =                '$pyshield_folder$'
COMMAND_LINE =                  False #  true if pyshield is run from cmd
#==============================================================================
# Physics and calculation
#==============================================================================

#--------------------Materials file--------------------------------------------
# KEY
MATERIALS =                     'materials'
# ITEMS
DENSITY =                       'Density [g/cm^3]'
#-----------------------------------------------------------------------------

#---------------------Isotopes file-------------------------------------------
# KEYS
ISOTOPES =                      'isotopes'
#items
H10 =                           'h(10) [uSv/h per MBq/m^2]' # not used (!)
LABDA =                         'labda [s^-1]'
ABUNDANCE =                     'Abundance'

#----------------------Buildup and attenuation file---------------------------
# KEYS
BUILDUP =                       'buildup'
ATTENUATION =                   'attenuation'
# ITEMS
ENERGY_keV=                     'Energy [keV]'
ENERGY_MeV =                    'Energy [MeV]'
MASS_ATTENUATION =              'mu/p [cm^2/g]'

#--------------------Calculation Settings--------------------------------------
CALCULATE =                     'calculate'
POLAR =                         'polar'
CARTESIAN =                     'cartesian'
NANGLES =                       'number_of_angles'
GRID =                          'grid'
GRIDSIZE =                      'grid_size'
INTERSECTION_THICKNESS =        'intersection_thickness'
DISABLE_BUILDUP =               'disable_buildup'
MULTI_CPU =                     'multi_cpu'


#--------------------Logging---------------------------------------------------
# KEY
LOG =                           'log'
# VALUES
LOG_INFO =                      'info'
LOG_DEBUG =                     'debug'
LOG_ERROR =                     'error'


#==============================================================================
# Definitions
#==============================================================================

#----------------------Barriers------------------------------------------------
# KEY
BARRIERS =                      'barriers'
# ITEMS
LOCATION =                      'Location [cm]'
MATERIAL =                      'Material [cm]'
FLOOR =                         'floor'
HEIGHT =                        'height'
LABEL =                         'Label'

#----------------------Points--------------------------------------------------
# KEY
POINTS =                        'points'
# ITEMS
OCCUPANCY_FACTOR =              'OCCUPANCY_FACTOR'
ALIGNMENT =                     'ALIGNMENT'

#------------------------Floorplan---------------------------------------------
# KEYS
FLOOR_PLAN =                    'floor_plan'
SCALE =                         'scale'
ORIGIN =                        'origin'

#----------------------Sources-------------------------------------------------
# KEY
SOURCES =                       'sources'
# ITEMS
DESINT =                        'N desintegrations [year^-1]'
ACTIVITY =                      'Activity [MBq]'
DURATION =                      'Duration [h]'
ACTIVITY_H =                    'Equivalent Activity MBq/h'
DECAY_CORRECTION =              'Decay correction'

NUMBER_OF_EXAMS =               'Number of exams'
LENGTH =                        'lenght'

# SUBKEY
TYPE =                          'Type'
# ITEMS
POINT_SOURCE =                  'point_source'
LINE_SOURCE =                   'line_source'
ISOTOPE =                       'Isotope'


#==============================================================================
# Export, results and display
#==============================================================================

#-----------------------Results------------------------------------------------

DOSE_MAPS =                     'dose_maps'
FIGURE    =                     'figure'
TABLE     =                     'table'
SUM_TABLE =                     'sum_table'
TABLE     =                     'table'
SOURCE_TABLE =                  'source_table'

#--------------------Visualization---------------------------------------------
# KEY
SHOW =                          'show'
VISUALIZATION =                 'visualization'
# SUB KEY
FIGURE =                        'figure'
FIG_SIZE =                      'fig_size'
LEGEND_LOCATION =               'legend_location'
# SUBKEYS
BARRIER =                       'barrier'
POINT =                         'point'
SOURCE=                         'source'
# ITEMS
COLOR =                         'color'
COLORS =                        'colors'
LINE_STYLE =                    'line_style'
LINE_WIDTH =                    'line_width'
SOURCE =                        'source'
MARKER =                        'marker'
ALIGNMENT =                     'alignment'
NAME =                          'name'
# SUBKEY
DOSE_MAP =                      'dose_map'
# ITEMS
CLIM =                          'clim'
COLOR_MAP =                     'color_map'
LINES =                         'lines'
FONT_SIZE =                     'font_size'
#----------------------------Export Settings-----------------------------------
EXPORT_EXCEL =                  'export_excel'
EXPORT_IMAGES =                 'export_images'
EXCEL_FILENAME =                'excel_filename'
SUM_SOURCES =                   'sum_sources'
ALL_SOURCES =                   'all_sources'
EXPORT_DIR =                    'export_dir'
IMAGE_DPI =                     'image_dpi'
DOSE_LIMIT_BLUE   =             'dose_limit_blue'
DOSE_LIMIT_RED =                'dose_limit_red'

#---------------------- Table Headers------------------------------------------
SOURCE_NAME =                   'source name'
SOURCE_LOCATION =               'source location_[cm]'
POINT_NAME =                    'point name'
POINT_LOCATION =                'point location [cm]'
TOTAL_SHIELDING =               'Shielding materials'
SOURCE_POINT_DISTANCE =         'Distance in meters'
DOSE_MSV =                      'Dose [mSv]'
DOSE_OCCUPANCY_MSV =            'Dose corrected for occupancy [mSv]'
DOSE_MSV_PER_ENERGY =           'Dose [mSv] per Energy'