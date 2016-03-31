""" List of constants for the pyshield package

    Last Updated 05-02-2016 """

DEF_PREFERENCE_FILE = 'default_preferences.yml'
RESOURCE_FILE = 'resources.yml'

SUM_SOURCES = 'sum_sources'
#FILE_TYPE = 'File type'


#==============================================================================
# Resources
#==============================================================================

MATERIALS = 'Materials'
XRAY_SHIELDING = 'X-ray_shielding'

ISOTOPES = 'Isotopes'
BUILDUP = 'Buildup'

#--------------------Materials file--------------------------------------------
DENSITY = 'Density [g/cm^3]' 
#-----------------------------------------------------------------------------

#---------------------Isotopes file-------------------------------------------
#values
H10 = 'h(10) [uSv/h per MBq/m^2]'
HALFTIME = 'Half time [min]'
LABDA = 'labda [s^-1]'
HALF_VALUE_THICKNESS = 'Half value thickness [cm]'      
#----------------------------------------------------------------------------- 

#----------------------Buildup file-------------------------------------------
MFP='Mean Free path'
ENERGY='Energy [keV]'
BUILDUP_FACTORS='Buildup Factors'
#-----------------------------------------------------------------------------
 


#==============================================================================
# commandline arguments
#==============================================================================

#required options
SOURCES = 'sources'
SHIELDING = 'shielding'
FLOOR_PLAN = 'floorplan'

#PREFERENCES = 'preferences'
SCALE = 'scale'
EXPORT_DIR = 'export_dir'
GRIDSIZE = 'grid_size'
PYTHAGORAS = 'pythagoras'

CLIM_HEATMAP='clim_heatmap' 
COLORMAP = 'colormap'
IGNORE_BUILDUP = 'disable_buildup'
MULTI_CPU = 'multiple_cpu'

ISO_VALUES='iso_values'
ISO_COLORS='iso_colors'

SHOW = 'show'
SAVE_DATA = 'save_data'
SAVE_IMAGES = 'save_images'
IMAGE_DPI = 'image_dpi'

CALCULATE = 'calculate'

#ISOCONTOURS = 'socontours'
#values of isocontours
#VALUES= 'Values'
#COLORS = 'Colors' 



#Values of export/show

#ALL_SOURCES = 'All sources'
#SAVE = 'Save displayed figures'
#
##DPI = 'DPI'
#
#
#
#EXPORT_RAW_FNAME =   'Pickle File' 
#EXPORT_FIG_FNAME = 'Image File'
##data file keys
#FILES = 'Files'
#Values of FILES

#----------------------Sources file-------------------------------------------
ISOTOPE = 'Isotope'
DESINT = 'N desintegrations [year^-1]' 
ACTIVITY = 'Activity [MBq]'
DURATION = 'Duration [h]'
TIMES_PER_YEAR = 'Number of times per year'
DECAY_CORRECTION = 'Decay correction'
TYPE = 'Type'
EXAM = 'Exam'

BODY = 'Body'
HEAD = 'Head'
KVP = 'kVp'
DLP = 'Average DLP'
NUMBER_EXAMS = 'Number of exams'
XRAY_SECONDARY = 'X-ray secundary'
NUMBER_OF_EXAMS = 'Number of exams'
#-----------------------------------------------------------------------------

#----------------------Shielding file-----------------------------------------
LOCATION = 'Location [pixels]'
MATERIAL = 'Material [cm]'
#-----------------------------------------------------------------------------
       






  



