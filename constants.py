""" List of constants for the pyshield package

    Last Updated 05-02-2016 """

CONFIG_FILE = 'config.yml'
RESOURCE_FILE = 'resources.yml'

#----------Fields that need to be defined in the config file-------------------
GRIDSIZE = 'Gridsize'
PYTHAGORAS = 'Pythagoras'
SCALE = 'Scale'
CLIM_HEATMAP='CLim Heatmap' 
COLORMAP = 'Colormap'
IGNORE_BUILDUP = 'Ignore Buildup'
MULTI_CPU = 'Multiple CPU'

LOG_LEVEL = 'Log level'
LOG_LEVEL_INFO = 'Default'
LOG_LEVEL_DEBUG = 'All'

ISOCONTOURS = 'Isocontours'
#values of isocontours
VALUES= 'Values'
COLORS = 'Colors' 

EXPORT = 'Export'
SHOW = 'Show'
#Values of export/show
SUM_SOURCES = 'Sum sources'
ALL_SOURCES = 'All sources'
SAVE_DISPLAYED = 'Save displayed figures'
FILE_TYPE = 'File type'
DPI = 'DPI'
EXPORT_DIR = 'Export directory'
EXPORT_RAW = 'Export raw'
EXPORT_RAW_FNAME =   'Export raw filename' 
EXPORT_FIG_FNAME = 'Export figures filename'
#data file keys
FILES = 'Files'
#Values of FILES
SOURCES = 'Sources'
SHIELDING = 'Shielding'
ISOTOPES = 'Isotopes'
FLOOR_PLAN = 'Floor plan'
MATERIALS = 'Materials'
XRAY_SHIELDING = 'X-ray_shielding'
BUILDUP = 'Buildup'
#-----------------------------------------------------------------------------

#----------------------Shielding file-----------------------------------------
LOCATION = 'Location [pixels]'
MATERIAL = 'Material [cm]'
#-----------------------------------------------------------------------------
         
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
#
 
#----------------------Sources file-------------------------------------------
ISOTOPE = 'Isotope'
DESINT = 'N desintegrations [year^-1]' 
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



