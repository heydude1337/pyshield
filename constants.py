""" List of constants for the pyshield package

    Last Updated 05-02-2016 """

DEF_PREFERENCE_FILE =   'default_preferences.yml'
RESOURCE_FILE =         'resources.yml'

SUM_SOURCES =           'sum_sources'
#FILE_TYPE = 'File type'


#==============================================================================
# Resources
#==============================================================================

MATERIALS =             'Materials'
XRAY_SHIELDING =        'X-ray_shielding'

ISOTOPES =              'Isotopes'
BUILDUP =               'Buildup'

#--------------------Materials file--------------------------------------------
DENSITY =               'Density [g/cm^3]'
#-----------------------------------------------------------------------------

#---------------------Isotopes file-------------------------------------------
#values
H10 =                   'h(10) [uSv/h per MBq/m^2]'
HALFTIME =              'Half time [min]'
LABDA =                 'labda [s^-1]'
HALF_VALUE_THICKNESS =  'Half value thickness [cm]'
#-----------------------------------------------------------------------------

#----------------------Buildup file-------------------------------------------
MFP=                    'Mean Free path'
ENERGY=                 'Energy [keV]'
BUILDUP_FACTORS=        'Buildup Factors'
#-----------------------------------------------------------------------------



#==============================================================================
# commandline arguments
#==============================================================================

#required options
SOURCES =               'source_file'
SHIELDING =             'shielding_file'
FLOOR_PLAN =            'floor_plan'
XY =                    'location_receiving_points'

#PREFERENCES = 'preferences'
AREA =                  'area'
SCALE =                 'scale'
ORIGIN =                'origin'
EXPORT_DIR =            'export_dir'
GRID =                  'grid'
POLAR =                 'polar'
RMIN =                  'rmin'
NANGLES =               'number_of_angles'
CARTESIAN =             'cartesian'
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
LOG_INFO =              'info'
LOG_DEBUG =             'debug'
AUDIT =                 'audit'


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
NUMBER_EXAMS =        'Number of exams'
XRAY_SECONDARY =      'X-ray secundary'
NUMBER_OF_EXAMS =     'Number of exams'
#-----------------------------------------------------------------------------

#----------------------Shielding file-----------------------------------------
LOCATION =            'Location [cm]'
LOCATION_PIXELS =     'Location [pixels]'
MATERIAL =            'Material [cm]'
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


























