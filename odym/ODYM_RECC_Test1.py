# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 17:33:01 2017

@authors: spauliuk
"""

"""
File ODYM_RECC_Test1
Check https://github.com/IndEcol/ODYM for latest version.

Contains the model instructions for the resource efficiency climate change project developed using ODYM: ODYM-RECC

dependencies:
    numpy >= 1.9
    scipy >= 0.14

"""
# Import required libraries:
import os  
import sys
import logging as log
import xlrd, xlwt
import numpy as np
import time
import datetime
import scipy.io
import scipy
import pandas as pd
import shutil   
import uuid
import matplotlib.pyplot as plt   
import imp
import getpass
from copy import deepcopy


#import re
__version__ = str('0.1')
#######################
#     Initialize      #
#######################
ProjectSpecs_Path_Main = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# NOTE: Hidden variable __file__ must be know to script for the directory structure to work.
# Therefore: When first using the model, run the entire script with F5 so that the __file__ variable can be created.

#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules'))) # add ODYM module directory to system path

# Load project-specific config file
ProjectSpecs_Name_ConFile = 'ODYM_RECC_Config.xlsx'
Model_Configfile = xlrd.open_workbook(os.path.join(ProjectSpecs_Path_Main, ProjectSpecs_Name_ConFile))
ScriptConfig = {'Model Setting': Model_Configfile.sheet_by_name('Config').cell_value(3,3)}
Model_Configsheet = Model_Configfile.sheet_by_name('Setting_' + ScriptConfig['Model Setting'])
   
#Extract user name from main file
ProjectSpecs_User_Name     = getpass.getuser()

# import packages whose location is now on the system path:    
import ODYM_Classes as msc  # import the ODYM class file
imp.reload(msc)
import ODYM_Functions as msf  # import the ODYM function file
imp.reload(msf)
import dynamic_stock_model as dsm  # import the dynamic stock model library
imp.reload(dsm)


Name_Script = Model_Configsheet.cell_value(5, 3)
if Name_Script != 'ODYM_RECC_Test1':  # Name of this script must equal the specified name in the Excel config file
    # TODO: This does not work because the logger was not yet initialized
    # log.critical("The name of the current script '%s' does not match to the sript name specfied in the project configuration file '%s'. Exiting the script.",
    #              Name_Script, 'ODYM_RECC_Test1')
    raise AssertionError('Fatal: The name of the current script does not match to the sript name specfied in the project configuration file. Exiting the script.')
# the model will terminate if the name of the script that is run is not identical to the script name specified in the config file.
Name_Scenario      = Model_Configsheet.cell_value(3,3)
StartTime          = datetime.datetime.now()
TimeString         = str(StartTime.year) + '_' + str(StartTime.month) + '_' + str(StartTime.day) + '__' + str(StartTime.hour) + '_' + str(StartTime.minute) + '_' + str(StartTime.second)
DateString         = str(StartTime.year) + '_' + str(StartTime.month) + '_' + str(StartTime.day)
Path_Result        = ProjectSpecs_Path_Main + 'Results' + '\\' + Name_Scenario + '_' + TimeString + '\\'

# Read control and selection parameters into dictionary
SCix = 0
# search for script config list entry
while Model_Configsheet.cell_value(SCix, 1) != 'General Info':
    SCix += 1
        
SCix += 2  # start on first data row
while len(Model_Configsheet.cell_value(SCix, 3)) > 0:
    ScriptConfig[Model_Configsheet.cell_value(SCix, 2)] = Model_Configsheet.cell_value(SCix,3)
    SCix += 1

SCix = 0
# search for script config list entry
while Model_Configsheet.cell_value(SCix, 1) != 'Software version selection':
    SCix += 1
        
SCix += 2 # start on first data row
while len(Model_Configsheet.cell_value(SCix, 3)) > 0:
    ScriptConfig[Model_Configsheet.cell_value(SCix, 2)] = Model_Configsheet.cell_value(SCix,3)
    SCix += 1

ScriptConfig['Current_UUID'] = str(uuid.uuid4())

# Create scenario folder
msf.ensure_dir(Path_Result)
#
# Copy Config file into that folder
shutil.copy(ProjectSpecs_Path_Main + ProjectSpecs_Name_ConFile, Path_Result + ProjectSpecs_Name_ConFile)
# Initialize logger
[Mylog,console_log,file_log] = msf.function_logger(logging.DEBUG, Name_Scenario + '_' + TimeString, Path_Result, logging.DEBUG) 

# log header and general information
Mylog.info('<html>\n<head>\n</head>\n<body bgcolor="#ffffff">\n<br>')
Mylog.info('<font "size=+5"><center><b>Script: ' + Name_Script + '.py</b></center></font>')
Mylog.info('<font "size=+5"><center><b>Model script version: ' + __version__ + '</b></center></font>')
Mylog.info('<font "size=+5"><center><b>Model functions version: ' + msf.__version__() + '</b></center></font>')
Mylog.info('<font "size=+5"><center><b>Model classes version: ' + msc.__version__() + '</b></center></font>')
Mylog.info('<font "size=+4"> <b>Current User: ' + ProjectSpecs_User_Name + '.</b></font><br>')
Mylog.info('<font "size=+4"> <b>Current Path: ' + ProjectSpecs_Path_Main + '.</b></font><br>')
Mylog.info('<font "size=+4"> <b>Current Scenario: ' + Name_Scenario + '.</b></font><br>')
Mylog.info(ScriptConfig['Description'])
Mylog.info('Unique ID of scenario run: <b>' + ScriptConfig['Current_UUID'] + '</b>')

Time_Start = time.time()
Mylog.info('<font "size=+4"> <b>Start of simulation: ' + time.asctime() + '.</b></font><br>')

##########################################
#     Read classifications and data      #
##########################################

Mylog.info('<p><b>Read classification items and define all classifications.</b></p>')
# Note: This part reads the items directly from the Exel master, will be replaced by reading them from version-managed csv file.
Classfile  = xlrd.open_workbook(ProjectSpecs_Path_Main + 'ODYM_Classifications_Master_'  + str(ScriptConfig['Version of master classification']) + '.xlsx')
Classsheet = Classfile.sheet_by_name('MAIN_Table')
ci = 1 # column index to start with
MasterClassification = {} # Dict of master classifications
while True:
    TheseItems = []
    ri = 10 # row index to start with    
    try: 
        ThisName = Classsheet.cell_value(0,ci)
        ThisDim  = Classsheet.cell_value(1,ci)
        ThisID   = Classsheet.cell_value(3,ci)
        ThisUUID = Classsheet.cell_value(4,ci)
        TheseItems.append(Classsheet.cell_value(ri,ci)) # read the first classification item
    except:
        Mylog.info('<p><b>End of file or formatting error while reading the classification file in column '+ str(ci) +'.</b></p>')
        break
    while True:
        ri +=1
        try:
            ThisItem = Classsheet.cell_value(ri,ci)
        except:
            break
        if ThisItem is not '':
            TheseItems.append(ThisItem)
    MasterClassification[ThisName] = msc.Classification(Name = ThisName, Dimension = ThisDim, ID = ThisID, UUID = ThisUUID, Items = TheseItems)
    ci +=1 

Mylog.info('<p><b>Read index table from model config sheet.</b></p>')
ITix = 0
while True: # search for index table entry
    if Model_Configsheet.cell_value(ITix,1) == 'Index Table':
        break
    else:
        ITix += 1
        
IT_Aspects        = []
IT_Description    = []
IT_Dimension      = []
IT_Classification = []
IT_Selector       = []
IT_IndexLetter    = []
ITix += 2 # start on first data row
while True:
    if len(Model_Configsheet.cell_value(ITix,2)) > 0:
        IT_Aspects.append(Model_Configsheet.cell_value(ITix,2))
        IT_Description.append(Model_Configsheet.cell_value(ITix,3))
        IT_Dimension.append(Model_Configsheet.cell_value(ITix,4))
        IT_Classification.append(Model_Configsheet.cell_value(ITix,5))
        IT_Selector.append(Model_Configsheet.cell_value(ITix,6))
        IT_IndexLetter.append(Model_Configsheet.cell_value(ITix,7))        
        ITix += 1
    else:
        break

Mylog.info('<p><b>Read parameter list from model config sheet.</b></p>')
PLix = 0
while True: # search for parameter list entry
    if Model_Configsheet.cell_value(PLix,1) == 'Model Parameters':
        break
    else:
        PLix += 1
        
PL_Names          = []
PL_Description    = []
PL_Version        = []
PL_IndexStructure = []
PL_IndexMatch     = []
PL_IndexLayer     = []
PLix += 2 # start on first data row
while True:
    if len(Model_Configsheet.cell_value(PLix,2)) > 0:
        PL_Names.append(Model_Configsheet.cell_value(PLix,2))
        PL_Description.append(Model_Configsheet.cell_value(PLix,3))
        PL_Version.append(Model_Configsheet.cell_value(PLix,4))
        PL_IndexStructure.append(Model_Configsheet.cell_value(PLix,5))
        PL_IndexMatch.append(Model_Configsheet.cell_value(PLix,6))
        PL_IndexLayer.append(msf.ListStringToListNumbers(Model_Configsheet.cell_value(PLix,7))) # strip numbers out of list string
        PLix += 1
    else:
        break
    
Mylog.info('<p><b>Read process list from model config sheet.</b></p>')
PrLix = 0
while True: # search for process list entry
    if Model_Configsheet.cell_value(PrLix,1) == 'Process Group List':
        break
    else:
        PrLix += 1
        
PrL_Number         = []
PrL_Name           = []
PrL_Code           = []
PrL_Type           = []
PrLix += 2 # start on first data row
while True:
    if Model_Configsheet.cell_value(PrLix,2) != '':
        try:
            PrL_Number.append(int(Model_Configsheet.cell_value(PrLix,2)))
        except:
            PrL_Number.append(Model_Configsheet.cell_value(PrLix,2))
        PrL_Name.append(Model_Configsheet.cell_value(PrLix,3))
        PrL_Code.append(Model_Configsheet.cell_value(PrLix,4))
        PrL_Type.append(Model_Configsheet.cell_value(PrLix,5))
        PrLix += 1
    else:
        break    

Mylog.info('<p><b>Read model output control from model config sheet.</b></p>')
None

Mylog.info('<p><b>Define model classifications and select items for model classifications according to information provided by config file.</b></p>')
ModelClassification  = {} # Dict of model classifications
for m in range(0,len(IT_Aspects)):
    ModelClassification[IT_Aspects[m]] = deepcopy(MasterClassification[IT_Classification[m]])
    EvalString = msf.EvalItemSelectString(IT_Selector[m],len(ModelClassification[IT_Aspects[m]].Items))
    if EvalString.find(':') > -1: # range of items is taken
        RangeStart = int(EvalString[0:EvalString.find(':')])
        RangeStop  = int(EvalString[EvalString.find(':')+1::])
        ModelClassification[IT_Aspects[m]].Items = ModelClassification[IT_Aspects[m]].Items[RangeStart:RangeStop]           
    elif EvalString.find('[') > -1: # selected items are taken
        ModelClassification[IT_Aspects[m]].Items = [ModelClassification[IT_Aspects[m]].Items[i] for i in eval(EvalString)]
    elif EvalString == 'all':
        None
    else:
        Mylog.info('ITEM SELECT ERROR for aspect ' + IT_Aspects[m] + ' were found in datafile.</br>')
        break
    
Model_Time_Start = min(ModelClassification['Time'].Items)
Model_Time_End   = max(ModelClassification['Time'].Items)

Mylog.info('<p><b> Define index table dataframe.</b></p>')
IndexTable = pd.DataFrame({'Aspect'        : IT_Aspects, # 'Time' and 'Element' must be present!
                           'Description'   : IT_Description,
                           'Dimension'     : IT_Dimension,
                           'Classification': [ModelClassification[Aspect] for Aspect in IT_Aspects],
                           'IndexLetter'   : IT_IndexLetter}) # Unique one letter (upper or lower case) indices to be used later for calculations.

IndexTable.set_index('Aspect', inplace = True) # Default indexing of IndexTable, other indices are produced on the fly

# Add indexSize to IndexTable:
IndexTable['IndexSize'] = pd.Series([len(IndexTable.Classification[i].Items) for i in range(0,len(IndexTable.IndexLetter))], index=IndexTable.index)

IndexTable_ClassificationNames = [IndexTable.Classification[i].Name for i in range(0,len(IndexTable.IndexLetter))] # list of the classifications used for each indexletter

#Define shortcuts for the most important index sizes:
Nt = len(IndexTable.Classification[IndexTable.index.get_loc('Time')].Items)
Nr = len(IndexTable.Classification[IndexTable.index.get_loc('(Origin)Region')].Items)
NG = len(IndexTable.Classification[IndexTable.set_index('IndexLetter').index.get_loc('G')].Items)
#IndexTable.ix['t']['Classification'].Items # get classification content
Mylog.info('<p><b>Read model data and parameters.</b></p>')

ParameterDict = {}
for mo in range(0,len(PL_Names)):
    ParPath = ProjectSpecs_Path_Main + 'ODYM_RECC_Database\\' + PL_Version[mo]    
    Mylog.info('<br> Reading parameter ' + PL_Names[mo])
    #MetaData, Values = msf.ReadParameter(ParPath = ParPath,ThisPar = PL_Names[mo], ThisParIx = PL_IndexStructure[mo], IndexMatch = PL_IndexMatch[mo], ThisParLayerSel = PL_IndexLayer[mo], MasterClassification,IndexTable,IndexTable_ClassificationNames,ScriptConfig,Mylog) # Do not change order of parameters handed over to function!
    MetaData, Values = msf.ReadParameter(ParPath,PL_Names[mo],PL_IndexStructure[mo], PL_IndexMatch[mo], PL_IndexLayer[mo], MasterClassification,IndexTable,IndexTable_ClassificationNames,ScriptConfig,Mylog) # Do not change order of parameters handed over to function!
    ParameterDict[PL_Names[mo]] = msc.Parameter(Name = MetaData['Dataset_Name'], ID = MetaData['Dataset_ID'], UUID = MetaData['Dataset_UUID'], P_Res = None, MetaData = MetaData, Indices = PL_IndexStructure[mo], Values=Values, Uncert=None, Unit = MetaData['Dataset_Unit'])


###############################################
#    Initialize dynamic MFA model example 1   #
###############################################

Mylog.info('<p><b>Define system and processes.</b></p>')

MyMFA = msc.MFAsystem(Name = 'TestSystem', 
                      Geogr_Scope = 'World', 
                      Unit = 'Mt', 
                      ProcessList = [], 
                      FlowDict = {}, 
                      StockDict = {},
                      ParameterDict = ParameterDict, 
                      Time_Start = Model_Time_Start, 
                      Time_End = Model_Time_End, 
                      IndexTable = IndexTable, 
                      Elements = IndexTable.ix['Element'].Classification.Items, 
                      Graphical = None) # Initialize MFA system
                      
# Check Validity of index tables:
MyMFA.IndexTableCheck() # returns true if dimensions are OK and time index is present and element list is not empty

# Add processes to system
for m in range(0, len(PrL_Number)):
    MyMFA.ProcessList.append(msc.Process(Name = PrL_Name[m], ID   = PrL_Number[m]))

# Define flows by symbol and names, can also be imported from Excel
MyMFA.FlowDict['F_1_2'] = msc.Flow(Name = 'Steel production'       , P_Start = 1, P_End = 2, Indices = 't,r,a,e', Values=None, Uncert=None, Color = None, ID = None, UUID = None)
MyMFA.FlowDict['F_2_3'] = msc.Flow(Name = 'Steel use'              , P_Start = 2, P_End = 3, Indices = 't,r,s,e', Values=None, Uncert=None, Color = None, ID = None, UUID = None)
MyMFA.FlowDict['F_2_0'] = msc.Flow(Name = 'Steel loss'             , P_Start = 2, P_End = 0, Indices = 't,c,r,a,e', Values=None, Uncert=None, Color = None, ID = None, UUID = None)
MyMFA.FlowDict['F_1_4'] = msc.Flow(Name = 'Fabrication Scrap'      , P_Start = 1, P_End = 4, Indices = 't,c,r,D,s,e', Values=None, Uncert=None, Color = None, ID = None, UUID = None)
MyMFA.FlowDict['F_4_0'] = msc.Flow(Name = 'Landfills'              , P_Start = 4, P_End = 0, Indices = 't,e', Values=None, Uncert=None, Color = None, ID = None, UUID = None)

MyMFA.Initialize_FlowValues() # Assign empty arrays to flows according to dimensions.

# Assign values to flows, manually:
MyMFA.FlowDict['F_1_2'].Values[0,0,:,0] = 5
MyMFA.FlowDict['F_2_3'].Values[0,0,:,4] = 2

# Define stocks 
MyMFA.StockDict['S_2']   = msc.Stock(Name = 'Steel stock in use'              , P_Res = 2, Type = 0, Indices = 't,c,G,a,e', Values=None, Uncert=None, ID = None, UUID = None)
MyMFA.StockDict['DS_2']  = msc.Stock(Name = 'Change of Steel stock in use'    , P_Res = 2, Type = 1, Indices = 't,G,a,e', Values=None, Uncert=None, ID = None, UUID = None)

MyMFA.Initialize_StockValues() # Assign empty arrays to stocks according to dimensions.

# Assign values to stocks, manually:
MyMFA.StockDict['DS_2'].Values[0,0,:,0] = 5

MyMFA.Consistency_Check() # Check whether flow value arrays match their indices, etc.

Bal = MyMFA.MassBalance() # Determine Mass Balance

# Save mass balance to Excel
myfont = xlwt.Font()
myfont.bold = True
mystyle = xlwt.XFStyle()
mystyle.font = myfont
Result_workbook  = xlwt.Workbook(encoding = 'ascii') 
for m in range(0,len(MyMFA.IndexTable.set_index('IndexLetter').ix['e'].Classification.Items)):
    ThisEl = MyMFA.IndexTable.set_index('IndexLetter').ix['e'].Classification.Items[m]
    msf.ExcelSheetFill(Result_workbook,'MassBalance_Example_' + ThisEl, Bal[:,:,m], topcornerlabel = 'Mass balance for ' + ThisEl + ', in ' + MyMFA.Unit, rowlabels = MyMFA.IndexTable.set_index('IndexLetter').ix['t'].Classification.Items, collabels = PrL_Name, Style = mystyle, rowselect = None, colselect = None)
Result_workbook.save(Path_Result + 'MassBalance_Example.xls') 

# delete system
del MyMFA

#####################################################
#    Example 2: Perform model calculations          #
#####################################################
Mylog.info('<p><b>Define new system and processes.</b></p>')

MyMFA2 = msc.MFAsystem(Name = 'TestSystem', 
                      Geogr_Scope = 'World', 
                      Unit = 'Mt', 
                      ProcessList = [], 
                      FlowDict = {}, 
                      StockDict = {},
                      ParameterDict = ParameterDict, 
                      Time_Start = Model_Time_Start, 
                      Time_End = Model_Time_End, 
                      IndexTable = IndexTable, 
                      Elements = IndexTable.ix['Element'].Classification.Items, 
                      Graphical = None) # Initialize MFA system
                      
# Check Validity of index tables:
MyMFA2.IndexTableCheck() # returns true if dimensions are OK and time index is present and element list is not empty

# Add processes to system
for m in range(0, len(PrL_Number)):
    MyMFA2.ProcessList.append(msc.Process(Name = PrL_Name[m], ID   = PrL_Number[m]))
    
# Define system variables: Flows.     
MyMFA2.FlowDict['F_3_4'] = msc.Flow(Name = 'Final consumption'              , P_Start = 3, P_End = 4, Indices = 't,r,G,a,e', Values=None, Uncert=None, Color = None, ID = None, UUID = None)
MyMFA2.FlowDict['F_4_5'] = msc.Flow(Name = 'EoL products'                   , P_Start = 4, P_End = 5, Indices = 't,r,G,a,e', Values=None, Uncert=None, Color = None, ID = None, UUID = None)
# Define system variables: Stocks.
MyMFA2.StockDict['S_4']  = msc.Stock(Name = 'In-use stock'                  , P_Res = 4, Type = 1, Indices = 't,c,r,G,a,e', Values=None, Uncert=None, ID = None, UUID = None)

MyMFA2.Initialize_StockValues() # Assign empty arrays to stocks according to dimensions.
MyMFA2.Initialize_FlowValues() # Assign empty arrays to flows according to dimensions.

Mylog.info('<p><b>Perform sample model calculation.</b></p>') 
# THIS IS WHERE WE LEAVE THE FORMAL MODEL STRUCTURE AND DO WHATEVER IS NECESSARY TO SOLVE THE MODEL EQUATIONS.

# 1) Determine total stock from regression model, and apply stock-driven model
TotalStockCurves   = np.zeros((Nt,Nr,NG))    # Stock   by year, age-cohort, region, and product
TotalStockCurves_C = np.zeros((Nt,Nt,Nr,NG)) # Stock   by year, age-cohort, region, and product
TotalInflowCurves  = np.zeros((Nt,Nr,NG))    # Inflow  by year, region, and product
TotalOutflowCurves = np.zeros((Nt,Nt,Nr,NG)) # Outflow by year, age-cohort, region, and product
PDF_Array          = np.zeros((Nt,Nt,NG)) # Stock   by year, age-cohort, and product. PDFs are stored externally because recreating them with scipy.stats is very slow.
LT_Estimate = MyMFA2.ParameterDict['Par_ProductLifetime'].Values[:,0,17] # Take existing nonzero values.
for r in range(0,Nr): # Apply simple linear growth model
    #print(r) # Print region index to display progress.
    for G in range(0,NG):
        if r == 0:
            TotalStockCurves[:,r,G] = np.arange(0,Nt) * MyMFA2.ParameterDict['Par_SaturationLevelStocks'].Values[G,r,0] / Nt # forSSP1, linear growth model
            DSM_StockDriven = dsm.DynamicStockModel(t = np.arange(0,Nt,1), s = TotalStockCurves[:,r,G], lt = {'Type': 'Normal', 'Mean': [LT_Estimate[G]], 'StdDev': [0.3 * LT_Estimate[G]] })    
            TotalStockCurves_C[:,:,r,G], TotalOutflowCurves[:,:,r,G], TotalInflowCurves[:,r,G], ExitFlag = DSM_StockDriven.compute_stock_driven_model()
            PDF_Array[:,:,G] = DSM_StockDriven.pdf.copy()
        else:
            TotalStockCurves[:,r,G] = np.arange(0,Nt) * MyMFA2.ParameterDict['Par_SaturationLevelStocks'].Values[G,r,0] / Nt # forSSP1, linear growth model
            DSM_StockDriven = dsm.DynamicStockModel(t = np.arange(0,Nt,1), s = TotalStockCurves[:,r,G], lt = {'Type': 'Normal', 'Mean': [LT_Estimate[G]], 'StdDev': [0.3 * LT_Estimate[G]] }, pdf = PDF_Array[:,:,G])    
            TotalStockCurves_C[:,:,r,G], TotalOutflowCurves[:,:,r,G], TotalInflowCurves[:,r,G], ExitFlag = DSM_StockDriven.compute_stock_driven_model()
            
# 2) Apply material composition of products and element composition of materials to determine the elemement-by-material flows and stocks:
TotalStockCurves_C_a            = np.einsum('tcrG,Ga->tcrGa',   TotalStockCurves_C,  MyMFA2.ParameterDict['Par_MaterialContentProducts'].Values) # Stock by material
MyMFA2.StockDict['S_4'].Values  = np.einsum('tcrGa,ae->tcrGae', TotalStockCurves_C_a,MyMFA2.ParameterDict['Par_ElementContentMaterials'].Values) # Stock by element
del TotalStockCurves_C_a  

TotalInflowCurves_a             = np.einsum('trG,Ga->trGa',   TotalInflowCurves,   MyMFA2.ParameterDict['Par_MaterialContentProducts'].Values) # Inflow by material
MyMFA2.FlowDict['F_3_4'].Values = np.einsum('trGa,ae->trGae', TotalInflowCurves_a ,MyMFA2.ParameterDict['Par_ElementContentMaterials'].Values) # Inflow by element
del TotalInflowCurves_a

TotalOutflowCurves_a            = np.einsum('trG,Ga->trGa',   np.einsum('tcrG->trG',TotalOutflowCurves),   MyMFA2.ParameterDict['Par_MaterialContentProducts'].Values) # Inflow by material
MyMFA2.FlowDict['F_4_5'].Values = np.einsum('trGa,ae->trGae', TotalOutflowCurves_a ,MyMFA2.ParameterDict['Par_ElementContentMaterials'].Values) # Inflow by element
del TotalOutflowCurves_a

MyMFA2.Consistency_Check() # Check whether flow value arrays match their indices, etc.

Bal = MyMFA2.MassBalance() # Determine Mass Balance

##########################################
#   Evaluate results, save, and close    #
##########################################

# CREATE PLOTS and include them in log file
Mylog.info('<p>Plot results. </p>')
Figurecounter = 1

# 1) Pie plot of element composition of stocks
labels  = ModelClassification['Element'].Items[1::]
sizes   = np.einsum('abcde->e',MyMFA2.StockDict['S_4'].Values[-1,:,:,:,:,1::]) # All elements except 'All' for last model year.
explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()
fig_name = 'TestFig.png'
fig1.savefig(Path_Result + fig_name, dpi = 500) 
# include figure in logfile:
Mylog.info('<center><img src="'+ fig_name +'" width="857" height="600" alt="' + fig_name + '"></center>')
Mylog.info('<font "size=+3"><center><b><i>Figure '+ str(Figurecounter) + ': ' + fig_name + '.</i></b></center></font><br>')
Figurecounter += 1 
#
# 2) Export in Sankey format for Sankey app. Not working yet! Will be implemented once model code is stable.
# MyMFA.SankeyExport(Year = 2017,Path = Path_Result, Element = 0) # Export in Sankey format for D3.js Circular Sankey, 

# 3) Export to Excel
myfont = xlwt.Font()
myfont.bold = True
mystyle = xlwt.XFStyle()
mystyle.font = myfont
Result_workbook  = xlwt.Workbook(encoding = 'ascii') # Export element stock by region
msf.ExcelSheetFill(Result_workbook,'ElementComposition', np.einsum('abcde->be',MyMFA2.StockDict['S_4'].Values[-1,:,:,:,:,:]), topcornerlabel = 'Total in-use stock of elements, by region, in ' + MyMFA2.Unit, rowlabels = MyMFA2.IndexTable.set_index('IndexLetter').ix['r'].Classification.Items, collabels = MyMFA2.IndexTable.set_index('IndexLetter').ix['e'].Classification.Items, Style = mystyle, rowselect = None, colselect = None)
Result_workbook.save(Path_Result + 'ElementCompositionExample.xls') 

# 4) Export as .mat file
Mylog.info('Saving stock data to Matlab.<br>')
Filestring_Matlab_out      = Path_Result + 'StockData.mat' 
scipy.io.savemat(Filestring_Matlab_out, mdict={'Stock':np.einsum('abcdef->acdef',MyMFA2.StockDict['S_4'].Values)})

# Model run is finished. Wrap up.                         
Mylog.info('<br> Script is finished. Terminating logging process and closing all log files.<br>')
Time_End = time.time()
Time_Duration = Time_End - Time_Start
Mylog.info('<font "size=+4"> <b>End of simulation: ' + time.asctime() + '.</b></font><br>')
Mylog.info('<font "size=+4"> <b>Duration of simulation: %.1f seconds.</b></font><br>' % Time_Duration)
logging.shutdown()
# remove all handlers from logger
root = logging.getLogger()
root.handlers = [] # required if you don't want to exit the shell



#
#
# The End