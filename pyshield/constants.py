""" List of constants for the pyshield package

    Last Updated 05-02-2016 """

DEF_CONFIG_FILE =   'default_config.yml'
CONFIG_FILE = 'config.yml'
RESOURCE_FILE =         'resources.yml'

SUM_SOURCES =           'sum_sources'

RUN_CONFIGURATION =     'run_configuration'

#==============================================================================
# Resources
#==============================================================================

MATERIALS =             'Materials'
XRAY_SHIELDING =        'X-ray_shielding'

ISOTOPES =              'Isotopes'
BUILDUP =               'Buildup'
ATTENUATION =           'Attenuation'
#--------------------Materials file--------------------------------------------
DENSITY =               'Density [g/cm^3]'
#-----------------------------------------------------------------------------

#---------------------Isotopes file-------------------------------------------
#values
H10 =                   'h(10) [uSv/h per MBq/m^2]'
#HALFTIME =              'Half time [min]'
LABDA =                 'labda [s^-1]'
ABUNDANCE =             'Abundance'
#-----------------------------------------------------------------------------

#----------------------Buildup and attenuation file---------------------------

ENERGY_keV=             'Energy [keV]'
ENERGY_MeV =            'Energy [MeV]'
MASS_ATTENUATION =      'mu/p [cm^2/g]'
#-----------------------------------------------------------------------------

POLAR =                 'polar'
CARTESIAN =             'cartesian'

LOG_INFO =              'info'
LOG_DEBUG =             'debug'
LOG_ERROR =             'error'

#==============================================================================
# commandline arguments
#==============================================================================

#required options
SOURCES =               'sources'
SHIELDING =             'barriers'
FLOOR_PLAN =            'floor_plan'
POINTS =                'points'
MATERIAL_COLORS =       'material_colors'


SCALE =                 'scale'
ORIGIN =                'origin'
EXPORT_DIR =            'export_dir'


NANGLES =               'number_of_angles'
GRID =                  'grid'
GRIDSIZE =              'grid_size'

PYTHAGORAS =            'pythagoras'

CLIM_HEATMAP=           'clim_heatmap'
COLORMAP =              'colormap'
DISABLE_BUILDUP =       'disable_buildup'
MULTI_CPU =             'multi_cpu'

ISOCONTOUR_LINES =      'isocontour_lines'


SHOW =                  'show'
SAVE_IMAGES =           'save_images'
IMAGE_DPI =             'image_dpi'

CALCULATE =             'calculate'

LOG =                   'log'




#----------------------Sources file-------------------------------------------
ISOTOPE =             'Isotope'
DESINT =              'N desintegrations [year^-1]'
ACTIVITY =            'Activity [MBq]'
DURATION =            'Duration [h]'
ACTIVITY_H =          'Equivalent Activity MBq/h'
DECAY_CORRECTION =    'Decay correction'
TYPE =                'Type'
EXAM =                'Exam'

BODY =                'Body'
HEAD =                'Head'
KVP =                 'kVp'
DLP =                 'Average DLP'
XRAY_SECONDARY =      'X-ray secundary'
NUMBER_OF_EXAMS =     'Number of exams'
#-----------------------------------------------------------------------------

#----------------------Shielding file-----------------------------------------
LOCATION =            'Location [cm]'
MATERIAL =            'Material [cm]'
FLOOR =               'floor'
HEIGHT =              'height'
#-----------------------------------------------------------------------------

#----------------------Points file--------------------------------------------
OCCUPANCY_FACTOR = 'OCCUPANCY_FACTOR'
ALIGNMENT        = 'ALIGNMENT'

#-----------------------------------------------------------------------------


#---------------------- Table Headers-----------------------------------------
SOURCE_NAME =                 'source name'
SOURCE_LOCATION =             'source location_[cm]'
POINT_NAME =                  'point name'
POINT_LOCATION =              'point location [cm]'
TOTAL_SHIELDING =             'Shielding materials'
SOURCE_POINT_DISTANCE =       'Distance in meters'
DOSE_MSV =                    'Dose [mSv]'
DOSE_OCCUPANCY_MSV =          'Dose corrected for occupancy [mSv]'
DOSE_MSV_PER_ENERGY =         'Dose [mSv] per Energy'

#--------------------Result keys-----------------------------------------
DOSE_MAPS = 'dose_maps'
FIGURE    = 'figure'
TABLE     = 'table'
SUM_TABLE = 'sum_table'

POINT_SOURCE = 'point_source'
LINE_SOURCE = 'line_source'
LENGTH = 'lenght'

EXPORT_EXCEL = 'export_excel'
EXCEL_FILENAME_SUMMARY = 'excel_filename_summary'
EXCEL_FILENAME_FULLRESULT = 'excel_filename_fullresult'

#CONSTANTS =  [COLORMAP,
#              FIGURE,
#              SOURCE_NAME,
#              ATTENUATION,
#              FLOOR,
#              DISABLE_BUILDUP,
#              ACTIVITY,
#              MATERIAL,
#              FLOOR_PLAN,
#              SOURCE_POINT_DISTANCE,
#              SUM_TABLE,
#              BODY,
#              KVP,
#              MATERIALS,
#              POINT_NAME,
#              DOSE_MAPS,
#              DENSITY,
#              PYTHAGORAS,
#              SUM_SOURCES,
#              RUN_CONFIGURATION,
#              IMAGE_DPI,
#              DURATION,
#              EXPORT_DIR,
#              LOG_INFO,
#              POINT_LOCATION,
#              ISOCONTOUR_LINES,
#              DEF_PREFERENCE_FILE,
#              HEIGHT,
#              XRAY_SHIELDING,
#              ABUNDANCE,
#              CALCULATE,
#              ALIGNMENT,
#              DLP,
#              DOSE_OCCUPANCY_MSV,
#              MASS_ATTENUATION,
#              SCALE,
#              SHOW,
#              SOURCES,
#              LOG,
#              GRIDSIZE,
#              SHIELDING,
#              ORIGIN,
#              MULTI_CPU,
#              BUILDUP,
#              LOCATION,
#              POINTS,
#              SAVE_IMAGES,
#              NUMBER_OF_EXAMS,
#              ACTIVITY_H,
#              ISOTOPE,
#              TOTAL_SHIELDING,
#              CARTESIAN,
#              DOSE_MSV,
#              XRAY_SECONDARY,
#              CLIM_HEATMAP,
#              LABDA,
#              HEAD,
#              H10,
#              RESOURCE_FILE,
#              SOURCE_LOCATION,
#              ISOTOPES,
#              EXAM,
#              TYPE,
#              GRID,
#              MATERIAL_COLORS,
#              LOG_DEBUG,
#              OCCUPANCY_FACTOR,
#              POLAR,
#              TABLE,
#              DESINT,
#              NANGLES,
#              DECAY_CORRECTION,
#              POINT_SOURCE,
#              LINE_SOURCE,
#              EXPORT_EXCEL,
#              EXCEL_FILENAME_SUMMARY,
#              EXCEL_FILENAME_FULLRESULT]
#
#
#
#
#
#

















