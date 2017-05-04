""" List of constants for the pyshield package

    Last Updated 05-02-2016 """

DEF_PREFERENCE_FILE =   'default_preferences.yml'
RESOURCE_FILE =         'resources.yml'

SUM_SOURCES =           'sum_sources'

RUN_CONFIGURATION = 'run_configuration'

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
HALF_VALUE_THICKNESS =  'Half value thickness [cm]'
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

#==============================================================================
# commandline arguments
#==============================================================================

#required options
SOURCES =               'source_file'
SHIELDING =             'shielding_file'
FLOOR_PLAN =            'floor_plan'
POINTS =                'dose_points_file'
MATERIAL_COLORS =       'material colors'

#PREFERENCES = 'preferences'
AREA =                  'area'
SCALE =                 'scale'
ORIGIN =                'origin'
EXPORT_DIR =            'export_dir'

RMIN =                  'rmin'
NANGLES =               'number_of_angles'

GRID =                  'grid'
GRIDSIZE =              'grid_size'

PYTHAGORAS =            'pythagoras'

CLIM_HEATMAP=           'clim_heatmap'
COLORMAP =              'colormap'
DISABLE_BUILDUP =       'disable_buildup'
MULTI_CPU =             'multiple_cpu'

ISO_VALUES=             'iso_values'
ISO_COLORS=             'iso_colors'

SHOW =                  'show'
SAVE_DATA =             'save_data'
SAVE_IMAGES =           'save_images'
IMAGE_DPI =             'image_dpi'

CALCULATE =             'calculate'

LOG =                   'log'

AUDIT =                 'audit'
EXPORT_FNAME =          'dose_map'


#----------------------Sources file-------------------------------------------
ISOTOPE =             'Isotope'
DESINT =              'N desintegrations [year^-1]'
ACTIVITY =            'Activity [MBq]'
DURATION =            'Duration [h]'
TIMES_PER_YEAR =      'Number of times per year'
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
LOCATION_PIXELS =     'Location [pixels]'
MATERIAL =            'Material [cm]'
COLOR =               'Color'
FLOOR =               'floor'
HEIGHT =              'height'
#-----------------------------------------------------------------------------

#----------------------Points file--------------------------------------------
OCCUPANCY_FACTOR = 'OCCUPANCY_FACTOR'
ALIGNMENT        = 'ALIGNMENT'

#-----------------------------------------------------------------------------


#----------------------Audit keys  -------------------------------------------
ASOURCE =                 'source name'
ALOC_SOURCE =             'source location [cm]'
APOINT =                  'point name'
ALOC_POINT =              'point location [cm]'
ASHIELDING_MATERIALS_CM = 'Shielding materials'
ADIST_METERS =            'Distance in meters'
ASCALE =                  'Scale Factor in cm/pixel'
AATTENUATION =            'Total attenuation'
DOSE_MSV =                'Dose [mSv]'
DOSE_OCCUPANCY_MSV =      'Dose corrected for occupancy [mSv]'


#--------------------Result keys-----------------------------------------
DOSE_MAPS = 'dose_maps'
FIGURE    = 'figure'
TABLE     = 'table'
SUM_TABLE = 'sum_table'


CONST = (DEF_PREFERENCE_FILE,
         RESOURCE_FILE,
         SUM_SOURCES,
         MATERIALS,
         XRAY_SHIELDING,
         ISOTOPES,
         BUILDUP,
         ATTENUATION,
         DENSITY,
         H10,
         LABDA,
         HALF_VALUE_THICKNESS,
         ABUNDANCE,
         ENERGY_keV,
         ENERGY_MeV,
         MASS_ATTENUATION,
         GRID,
         POLAR,
         LOG_INFO,
         LOG_DEBUG,
         # source file
         ISOTOPE,
         DESINT,
         ACTIVITY,
         DURATION,
         TIMES_PER_YEAR,
         ACTIVITY_H,
         DECAY_CORRECTION,
         TYPE,
         EXAM,
         BODY,
         HEAD,
         KVP,
         DLP,
         XRAY_SECONDARY,
         NUMBER_OF_EXAMS,
         # shielding file
         LOCATION,
         MATERIAL,
         COLOR,
         FLOOR,
         HEIGHT,
         #audit
         ASOURCE,
         ALOC_SOURCE,
         APOINT,
         ALOC_POINT,
         ASHIELDING_MATERIALS_CM,
         ADIST_METERS,
         ASCALE,
         AATTENUATION,
         DOSE_MSV,
         # points file
         OCCUPANCY_FACTOR,
         POINTS,
         DOSE_OCCUPANCY_MSV)
























