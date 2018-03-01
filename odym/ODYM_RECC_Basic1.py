# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 17:33:01 2017

@authors: spauliuk
"""

"""
File ODYM_RECC_Basic1
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
from tqdm import tqdm


#import re
__version__ = str('0.1')
##################################
#    Section 1)  Initialize      #
##################################
ProjectSpecs_Path_Main = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# NOTE: Hidden variable __file__ must be know to script for the directory structure to work.
# Therefore: When first using the model, run the entire script with F5 so that the __file__ variable can be created.

# add ODYM module directory to system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules')))

### 1.1.) Read main script parameters
#Load project-specific config file
ProjectSpecs_Name_ConFile = 'ODYM_RECC_Config.xlsx'
#ProjectSpecs_Path_ConFile = 'C:/Users/spauliuk/FILES/ARBEIT/PROJECTS/ODYM-RECC/ODYM_RECC_Config.xlsx'
#Model_Configfile = xlrd.open_workbook(os.path.join(ProjectSpecs_Path_Main, ProjectSpecs_Name_ConFile))
Model_Configfile = xlrd.open_workbook(os.path.join(ProjectSpecs_Path_Main, ProjectSpecs_Name_ConFile))
ScriptConfig = {'Model Setting': Model_Configfile.sheet_by_name('Config').cell_value(3,3)}
Model_Configsheet = Model_Configfile.sheet_by_name('Setting_' + ScriptConfig['Model Setting'])
   
#Extract user name from main file
ProjectSpecs_User_Name     = getpass.getuser()

# import packages whose location is now on the system path:    
import ODYM_Classes as msc # import the ODYM class file
imp.reload(msc)
import ODYM_Functions as msf # import the ODYM function file
imp.reload(msf)
import dynamic_stock_model as dsm # import the dynamic stock model library
imp.reload(dsm)

Name_Script        = Model_Configsheet.cell_value(5,3)
if Name_Script != 'ODYM_RECC_Basic1':  # Name of this script must equal the specified name in the Excel config file
    # TODO: This does not work because the logger was not yet initialized
    # log.critical("The name of the current script '%s' does not match to the sript name specfied in the project configuration file '%s'. Exiting the script.",
    #              Name_Script, 'ODYM_RECC_Test1')
    raise AssertionError('Fatal: The name of the current script does not match to the sript name specfied in the project configuration file. Exiting the script.')
# the model will terminate if the name of the script that is run is not identical to the script name specified in the config file.
Name_Scenario            = Model_Configsheet.cell_value(3,3)
StartTime                = datetime.datetime.now()
TimeString               = str(StartTime.year) + '_' + str(StartTime.month) + '_' + str(StartTime.day) + '__' + str(StartTime.hour) + '_' + str(StartTime.minute) + '_' + str(StartTime.second)
DateString               = str(StartTime.year) + '_' + str(StartTime.month) + '_' + str(StartTime.day)
ProjectSpecs_Path_Result = os.path.join(os.path.abspath(os.path.join(ProjectSpecs_Path_Main, '..')), 'Results', Name_Scenario + '_' + TimeString )

### 1.2) Read model control parameters
#Read control and selection parameters into dictionary
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

if not os.path.exists(ProjectSpecs_Path_Result):
    os.makedirs(ProjectSpecs_Path_Result)

### 1.3) Organize model output folder and logger
#Copy Config file into that folder
shutil.copy(os.path.join(ProjectSpecs_Path_Main, ProjectSpecs_Name_ConFile), os.path.join(ProjectSpecs_Path_Result, ProjectSpecs_Name_ConFile))
# Initialize logger    
[Mylog,console_log,file_log] = msf.function_logger(log.DEBUG, Name_Scenario + '_' + TimeString, ProjectSpecs_Path_Result, log.DEBUG) 

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

#####################################################
#     Section 2) Read classifications and data      #
#####################################################
### 2.1) # Read model run config data
Mylog.info('<p><b>Read classification items and define all classifications.</b></p>')
# Note: This part reads the items directly from the Exel master, will be replaced by reading them from version-managed csv file.
Classfile  = xlrd.open_workbook(os.path.join(ProjectSpecs_Path_Main, 'ODYM_Classifications_Master_'  + str(ScriptConfig['Version of master classification']) + '.xlsx'))
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

Mylog.info('<p><b>Read model run control from model config sheet.</b></p>')
PrLix = 0
while True: # search for model flow control entry
    if Model_Configsheet.cell_value(PrLix,1) == 'Model flow control':
        break
    else:
        PrLix += 1
        
PrLix += 2 # start on first data row
while True:
    if Model_Configsheet.cell_value(PrLix,2) != '':
        try:
            ScriptConfig[Model_Configsheet.cell_value(PrLix,2)] = Model_Configsheet.cell_value(PrLix,3)
        except:
            None
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
    
### 2.2) # Define model index table and parameter dictionary
Model_Time_Start = int(min(ModelClassification['Time'].Items))
Model_Time_End   = int(max(ModelClassification['Time'].Items))
Model_Duration   = Model_Time_End - Model_Time_Start

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
Nc = len(IndexTable.Classification[IndexTable.index.get_loc('Cohort')].Items)
Nr = len(IndexTable.Classification[IndexTable.index.get_loc('(Origin)Region')].Items)
NG = len(IndexTable.Classification[IndexTable.set_index('IndexLetter').index.get_loc('g')].Items)
NS = len(IndexTable.Classification[IndexTable.index.get_loc('Scenario')].Items)
#IndexTable.ix['t']['Classification'].Items # get classification content
Mylog.info('<p><b>Read model data and parameters.</b></p>')

ParameterDict = {}
for mo in range(0,len(PL_Names)):
    ParPath = os.path.join(os.path.abspath(os.path.join(ProjectSpecs_Path_Main, '.')), 'ODYM_RECC_Database', PL_Version[mo])
    Mylog.info('<br> Reading parameter ' + PL_Names[mo])
    #MetaData, Values = msf.ReadParameter(ParPath = ParPath,ThisPar = PL_Names[mo], ThisParIx = PL_IndexStructure[mo], IndexMatch = PL_IndexMatch[mo], ThisParLayerSel = PL_IndexLayer[mo], MasterClassification,IndexTable,IndexTable_ClassificationNames,ScriptConfig,Mylog) # Do not change order of parameters handed over to function!
    MetaData, Values = msf.ReadParameter(ParPath,PL_Names[mo],PL_IndexStructure[mo], PL_IndexMatch[mo], PL_IndexLayer[mo], MasterClassification,IndexTable,IndexTable_ClassificationNames,ScriptConfig,Mylog) # Do not change order of parameters handed over to function!
    ParameterDict[PL_Names[mo]] = msc.Parameter(Name = MetaData['Dataset_Name'], ID = MetaData['Dataset_ID'], UUID = MetaData['Dataset_UUID'], P_Res = None, MetaData = MetaData, Indices = PL_IndexStructure[mo], Values=Values, Uncert=None, Unit = MetaData['Dataset_Unit'])


##########################################################
#    Section 3) Initialize dynamic MFA model for RECC    #
##########################################################
Mylog.info('<p><b>Define RECC system and processes.</b></p>')

# Initialize MFA system
RECC_System = msc.MFAsystem(Name='TestSystem',
                            Geogr_Scope='World',
                            Unit='Mt',
                            ProcessList=[],
                            FlowDict={},
                            StockDict={},
                            ParameterDict=ParameterDict,
                            Time_Start=Model_Time_Start,
                            Time_End=Model_Time_End,
                            IndexTable=IndexTable,
                            Elements=IndexTable.loc['Element'].Classification.Items,
                            Graphical=None)
                      
# Check Validity of index tables:
# returns true if dimensions are OK and time index is present and element list is not empty
RECC_System.IndexTableCheck()

# Add processes to system
for m in range(0, len(PrL_Number)):
    RECC_System.ProcessList.append(msc.Process(Name = PrL_Name[m], ID   = PrL_Number[m]))
    
# Define system variables: Flows.     
RECC_System.FlowDict['F_3_4'] = msc.Flow(Name = 'Final consumption'              , P_Start = 3, P_End = 4, Indices = 't,r,g,S,e', Values=None, Uncert=None, Color = None, ID = None, UUID = None)
RECC_System.FlowDict['F_4_5'] = msc.Flow(Name = 'EoL products'                   , P_Start = 4, P_End = 5, Indices = 't,c,r,g,S,e', Values=None, Uncert=None, Color = None, ID = None, UUID = None)
# Define system variables: Stocks.
RECC_System.StockDict['S_4']  = msc.Stock(Name = 'In-use stock'                  , P_Res = 4, Type = 1, Indices = 't,c,r,g,S,e', Values=None, Uncert=None, ID = None, UUID = None)

RECC_System.Initialize_StockValues() # Assign empty arrays to stocks according to dimensions.
RECC_System.Initialize_FlowValues() # Assign empty arrays to flows according to dimensions.

##########################################################
#    Section 4) Solve dynamic MFA model for RECC         #
##########################################################
Mylog.info('<p><b>Calculate inflows and outflows for use phase.</b></p>')
# THIS IS WHERE WE LEAVE THE FORMAL MODEL STRUCTURE AND DO WHATEVER IS NECESSARY TO SOLVE THE MODEL EQUATIONS.

# 1) Determine total stock from regression model, and apply stock-driven model
TotalStockCurves_S4   = np.zeros((Nt,Nr,NG,NS))    # Stock   by year, region, scenario, and product
#TotalStockCurves_C    = np.zeros((Nt,Nc,Nr,NG,NS)) # Stock   by year, age-cohort, region, scenario, and product
#TotalInflowCurves     = np.zeros((Nt,Nr,NG,NS))    # Inflow  by year, region, scenario, and product
#TotalOutflowCurves    = np.zeros((Nt,Nc,Nr,NG,NS)) # Outflow by year, age-cohort, region, scenario, and product
SF_Array             = np.zeros((Nc,Nc,Nr,NG,NS)) # Stock   by year, age-cohort, region, scenario, and product. PDFs are stored externally because recreating them with scipy.stats is slow.

if ScriptConfig['StockExtrapolation'] == 'Linear': #Apply linear extrapolation from current to future target stock levels
    StockStart          = RECC_System.ParameterDict['Par_HistoricStocks'].Values.sum(axis=1) # NG x NR start value
    Time_Multiplier     = np.arange(0,Nt) / Nt
    TotalStockCurves_S4 = np.einsum('trS,trgS->trgS',RECC_System.ParameterDict['Par_Population'].Values,np.einsum('t,grS->trgS',Time_Multiplier,RECC_System.ParameterDict['Par_SaturationLevelStocks'].Values))
    # plt.plot(TotalStockCurves[:,0,0,0])

# Apply RES 1: Stock sufficiency
TotalStockCurves_S4_ss = np.einsum('trgS,trgS->trgS',1 - np.einsum('gtrS,grS->trgS',RECC_System.ParameterDict['Par_ImplemenationCurves'].Values,RECC_System.ParameterDict['Par_SufficiencyLevelStocks'].Values),TotalStockCurves_S4)

# Apply RES 2: More intense use
TotalStockCurves_S4_ss_IU = np.einsum('trgS,trgS->trgS', 1 / (1 - np.einsum('gtrS,grS->trgS',RECC_System.ParameterDict['Par_ImplemenationCurves'].Values,RECC_System.ParameterDict['Par_IntensityOfUse'].Values)),TotalStockCurves_S4_ss)
    
# Apply RES 3: Product lifetime extension. NOTE: here, the time index t is replaced by the age-cohort index c
# First, replicate lifetimes for the 5 scenarios
RECC_System.ParameterDict['Par_ProductLifetime'].Values = np.einsum('S,grc->grcS',np.ones(NS),RECC_System.ParameterDict['Par_ProductLifetime'].Values)

# Second, change lifetime of future age-cohorts according to lifetime extension parameter
# This is equation 10 of the paper:
RECC_System.ParameterDict['Par_ProductLifetime'].Values[:,:,Nc - Model_Duration - 1::,:] = np.einsum('crgS,grcS->grcS',1 + np.einsum('gcrS,grS->crgS',RECC_System.ParameterDict['Par_ImplemenationCurves'].Values,RECC_System.ParameterDict['Par_LifeTimeExtension'].Values),RECC_System.ParameterDict['Par_ProductLifetime'].Values[:,:,Nc -Model_Duration -1::,:])

# Replicate lifetime values for region 0 and year 2017 from test dataset:
RECC_System.ParameterDict['Par_ProductLifetime'].Values = np.einsum('G,abc->Gabc',RECC_System.ParameterDict['Par_ProductLifetime'].Values[:,0,167,0],np.ones((Nr,Nc,NS)))

# Build pdf array from lifetime distribution: Probability of discard
for r in tqdm(range(0, Nr), unit='region'):
    for G in range(0, NG):
        for S in range(0, NS):
            lt = {'Type': 'Normal',
                  'Mean': RECC_System.ParameterDict['Par_ProductLifetime'].Values[G, r, :, S],
                  'StdDev': 0.3 * RECC_System.ParameterDict['Par_ProductLifetime'].Values[G, r, :, S]}
            SF_Array[:, :, r, G, S] = dsm.DynamicStockModel(t=np.arange(0, Nc, 1), lt=lt).compute_sf().copy()
            # AA = dsm.DynamicStockModel(t = np.arange(0,Nc,1), lt = {'Type': 'Normal', 'Mean': RECC_System.ParameterDict['Par_ProductLifetime'].Values[G,r,:,S], 'StdDev': 0.3 * RECC_System.ParameterDict['Par_ProductLifetime'].Values[G,r,:,S] })

# Apply stock-driven model with historic stock as initial stock
for r in tqdm(range(0, Nr), unit='region'):
    for G in range(0,NG):
        for S in range(0,NS):
            lt = {'Type': 'Normal',
                  'Mean': RECC_System.ParameterDict['Par_ProductLifetime'].Values[G, r, :, S],
                  'StdDev': 0.3 * RECC_System.ParameterDict['Par_ProductLifetime'].Values[G, r, :, S]}
            DSM_IntitialStock = dsm.DynamicStockModel(t=np.arange(0, Nc, 1),
                                                      s=np.concatenate((np.zeros((Nc - Model_Duration - 1)),
                                                                        TotalStockCurves_S4_ss_IU[:, r, G, S]),
                                                                       axis=0),
                                                      lt=lt,
                                                      sf=SF_Array[:, :, r, G, S])
            Var_S, Var_O, Var_I = \
                DSM_IntitialStock.compute_stock_driven_model_initialstock(InitialStock=RECC_System.ParameterDict['Par_HistoricStocks'].Values[G, 0: Nc - Model_Duration - 1, r],
                                                                          SwitchTime=Nc - Model_Duration - 1)              
            # Assign result to MFA system
            RECC_System.StockDict['S_4'].Values[:, Nc - Model_Duration - 1::, r, G, S, 0] = \
                Var_S[Nc - Model_Duration - 1::, Nc - Model_Duration - 1::]
            RECC_System.FlowDict['F_3_4'].Values[:, r, G, S, 0] = \
                Var_I[Nc - Model_Duration - 1::]
            RECC_System.FlowDict['F_4_5'].Values[:, Nc - Model_Duration - 1::, r, G, S, 0] = \
                Var_O[Nc - Model_Duration - 1::, Nc - Model_Duration - 1::]

# Clean up
del TotalStockCurves_S4
del TotalStockCurves_S4_ss
del TotalStockCurves_S4_ss_IU

# Compute obsolete stock formation
F_4_5_Obs = np.einsum('trgS,trgS->trgS',np.einsum('trgS,grS->trgS',1 - np.einsum('gtrS,grS->trgS',RECC_System.ParameterDict['Par_ImplemenationCurves'].Values,RECC_System.ParameterDict['Par_ObsoleteStockReduction'].Values),RECC_System.ParameterDict['Par_ObsoleteStockFormation'].Values),RECC_System.FlowDict['F_4_5'].Values[:,:,:,:,:,0].sum(axis=1))
# Compute inflow to waste management industries
F_4_5_WM  = RECC_System.FlowDict['F_4_5'].Values[:,:,:,:,:,0].sum(axis=1) - F_4_5_Obs


RECC_System.Consistency_Check() # Check whether flow value arrays match their indices, etc.

# Determine Mass Balance
Bal = RECC_System.MassBalance()

#####################################################
#   Section 5) Evaluate results, save, and close    #
#####################################################

### 5.1.) CREATE PLOTS and include them in log file
Mylog.info('<p>Plot results. </p>')
Figurecounter = 1

# 1) Pie plot of element composition of stocks
labels  = ModelClassification['Element'].Items[0::]
sizes   = np.einsum('abcde->e',RECC_System.StockDict['S_4'].Values[-1,:,:,:,:,0::]) # All elements except 'All' for last model year.
explode = (0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()
fig_name = 'TestFig.png'
fig1.savefig(os.path.join(ProjectSpecs_Path_Result, fig_name), dpi = 500) 
# include figure in logfile:
Mylog.info('<center><img src="'+ fig_name +'" width="857" height="600" alt="' + fig_name + '"></center>')
Mylog.info('<font "size=+3"><center><b><i>Figure '+ str(Figurecounter) + ': ' + fig_name + '.</i></b></center></font><br>')
Figurecounter += 1 
#

### 5.2) Export in Sankey format for Sankey app [http://www.visualisation.industrialecology.uni-freiburg.de/]. Not working yet! Will be implemented once model code is stable.
# MyMFA.SankeyExport(Year = 2017,Path = Path_Result, Element = 0) # Export in Sankey format for D3.js Circular Sankey, 

### 5.3) Export to Excel
myfont = xlwt.Font()
myfont.bold = True
mystyle = xlwt.XFStyle()
mystyle.font = myfont
Result_workbook  = xlwt.Workbook(encoding = 'ascii') # Export element stock by region
msf.ExcelSheetFill(Result_workbook,'ElementComposition', np.einsum('tcrge->re',RECC_System.StockDict['S_4'].Values[:,:,:,:,0,:]), topcornerlabel = 'Total in-use stock of elements, by region, in ' + RECC_System.Unit, rowlabels = RECC_System.IndexTable.set_index('IndexLetter').loc['r'].Classification.Items, collabels = RECC_System.IndexTable.set_index('IndexLetter').loc['e'].Classification.Items, Style = mystyle, rowselect = None, colselect = None)
Result_workbook.save(os.path.join(ProjectSpecs_Path_Result,'ElementCompositionExample.xls'))

### 5.4) Export as .mat file
Mylog.info('Saving stock data to Matlab.<br>')
Filestring_Matlab_out      = os.path.join(ProjectSpecs_Path_Result, 'StockData.mat')
scipy.io.savemat(Filestring_Matlab_out, mdict={'Stock':np.einsum('tcrgSe->trgS',RECC_System.StockDict['S_4'].Values)})

### 5.5) Model run is finished. Wrap up.                         
Mylog.info('<br> Script is finished. Terminating logging process and closing all log files.<br>')
Time_End = time.time()
Time_Duration = Time_End - Time_Start
Mylog.info('<font "size=+4"> <b>End of simulation: ' + time.asctime() + '.</b></font><br>')
Mylog.info('<font "size=+4"> <b>Duration of simulation: %.1f seconds.</b></font><br>' % Time_Duration)
log.shutdown()
# remove all handlers from logger
root = log.getLogger()
root.handlers = [] # required if you don't want to exit the shell
print('done.')


#
#
# The End.