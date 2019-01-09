# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 17:33:00 2017

@author: spauliuk
"""

"""
File ODYM_Functions
Check https://github.com/IndEcol/ODYM for latest version.

Contains class definitions for ODYM

standard abbreviation: msf (material-system-functions)

dependencies:
    numpy >= 1.9
    scipy >= 0.14

Repository for this class, documentation, and tutorials: https://github.com/IndEcol/ODYM

"""

import os
import logging
import numpy as np
import pandas as pd
import xlrd
import pypandoc

####################################
#      Define functions            #
####################################


def __version__():  # return version of this file
    return str('1.0')



def function_logger(log_filename, log_pathname, file_level=logging.DEBUG, console_level=logging.WARNING):
    """
    This is the logging routine of the model. It returns alogger that can be used by other functions to write to the
    log(file).

    :param file_level: Verbosity level for the logger's output file. This can be log.WARNING (default),
        log.INFO, log.DEBUG
    :param log_filename: The filename for the logfile.
    :param log_pathname: The pathname for the logfile.
    :param console_level: Verbosity level for the logger's output file.
    out
    :param logfile_type: Type of file to write. Markdown syntax is the default.
        TODO: If other outputs types are desired, they can be converted via pandoc.
    :return: A logger that can be used by other files to write to the log(file)
    """

    log_file = os.path.join(log_pathname, log_filename)
    # logging.basicConfig(format='%(levelname)s (%(filename)s <%(funcName)s>): %(message)s',
    #                     filename=log_file,
    #                     level=logging.INFO)
    logger = logging.getLogger()
    logger.handlers = []  # required if you don't want to exit the shell
    logger.setLevel(file_level)

    # The logger for console output
    console_log = logging.StreamHandler() #StreamHandler logs to console
    console_log.setLevel(console_level)
    # console_log_format = logging.Formatter('%(message)s')
    console_log_format = logging.Formatter('%(levelname)s (%(filename)s <%(funcName)s>): %(message)s')
    console_log.setFormatter(console_log_format)
    logger.addHandler(console_log)

    # The logger for log file output
    file_log = logging.FileHandler(log_file, mode='w', encoding=None, delay=False)
    file_log.setLevel(file_level)
    file_log_format = logging.Formatter('%(message)s\n')
    file_log.setFormatter(file_log_format)
    logger.addHandler(file_log)

    return logger,  console_log, file_log



def ensure_dir(f): # Checks whether a given directory f exists, and creates it if not
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)     
        
        
        
def sort_index(mylist,direction): # returns index that sorts a list, either ascending or descending
    if direction == 'ascending':
        return sorted(range(len(mylist)), key=lambda k: mylist[k])       
    elif direction == 'descending':
        return sorted(range(len(mylist)), key=lambda k: mylist[k], reverse=True)
    else:
        return None



def GroupingDict2Array(GroupingDict, ElementList):
    '''
    Tbd.
    '''
    NoOfItems = len(GroupingDict.keys())
    GroupingList = []
    for m in GroupingDict.keys():
        GroupingList.append(m)
    ElementContentArray = np.zeros((100,NoOfItems))
    PosCount = 0
    for m in GroupingList:
        for n in GroupingDict[m].keys():
            ElInd = ElementList.index(n)
            ElementContentArray[ElInd,PosCount] = GroupingDict[m][n]
        PosCount += 1
    return GroupingList, ElementContentArray



def ListStringToListNumbers(ListStr):
    """
    Extracts numbers from a string that looks like a list commant in python, and returns them as proper list
    Examples: ListStringToListNumbers('[1,2,3]') yields [1,2,3]
    """
    return [int(s) for s in ListStr[ListStr.find('['):ListStr.find(']')+1].replace('[',',').replace(']',',').split(',') if s.isdigit()]



def EvalItemSelectString(ItemSelectStr,IndexLength): 
    '''
    Extract index item selection lists from ODYM datafile information
    '''
    if ItemSelectStr == 'All' or ItemSelectStr == 'ALL' or ItemSelectStr == 'all':
        Res = 'all' # Selects all from list
    elif ItemSelectStr.find('except') > -1: # type 'All except', return full list [0,1,2,5,6,7]
        Res = np.arange(0,IndexLength)
        b = ItemSelectStr[ItemSelectStr.find('['):ItemSelectStr.find(']')+1].replace('[',',').replace(']',',')
        RemoveList = [int(s) for s in b.split(',') if s.isdigit()]   
        Res = np.delete(Res,RemoveList)      
        Res = Res.tolist() 
    elif ItemSelectStr.find(']') > -1: # type '[...]', return full list
        Res = ItemSelectStr[ItemSelectStr.find('[')::]
    elif ItemSelectStr.find(')') > -1: # type '[..:..)', return range a:b
        Res = ItemSelectStr[ItemSelectStr.find('[')+1:-1]
    else:
        Res = 'ItemSelectString could not be detected.'
    
    return Res



def MI_Tuple(value, Is): 
    """
    Define function for obtaining multiindex tuple from index value
    value: flattened index position, Is: Number of values for each index dimension
    Example: MI_Tuple(10, [3,4,2,6]) returns [0,0,1,4]
    MI_Tuple is the inverse of Tuple_MI.    
    """
    IsValuesRev = []
    CurrentValue = value
    for m in range(0,len(Is)):
        IsValuesRev.append(CurrentValue % Is[len(Is)-m-1])
        CurrentValue = CurrentValue // Is[len(Is)-m-1]
    return IsValuesRev[::-1]



def Tuple_MI(Tuple, IdxLength): 
    """
    Function to return the absolution position of a multiindex when the index tuple
    and the index hierarchy and size are given.
    Example: Tuple_MI([2,7,3],[100,10,5]) = 138
    Tuple_MI is the inverse of MI_Tuple.
    """
    # First, generate the index position offset values
    A =  IdxLength[1:] +  IdxLength[:1] # Shift 1 to left
    A[-1] = 1 # Replace lowest index by 1
    A.reverse()
    IdxPosOffset = np.cumproduct(A).tolist()
    IdxPosOffset.reverse()
    Position = np.sum([a*b for a,b in zip(Tuple,IdxPosOffset)])
    return Position



def ModelIndexPositions_FromData(Positions,RowPos,ColPos):
    """
    This function is needed to read data files into ODYM. It takes the positions of a given data point 
    in the parameter file and checks where in the model index structure this data points belongs, 
    if it is needed at all.
    """
    TargetPosition = []
    for m in range(0,len(Positions)):
        if m < len(RowPos):
            try:
                TargetPosition.append(Positions[m].index(RowPos[m]))
            except:
                break
        else:
            try:
                TargetPosition.append(Positions[m].index(ColPos[m-len(RowPos)]))
            except:
                break
    return TargetPosition



def ReadParameter(ParPath, ThisPar, ThisParIx, IndexMatch, ThisParLayerSel, MasterClassification,
                  IndexTable, IndexTable_ClassificationNames, ScriptConfig, Mylog):
    """
    This function reads a model parameter from the corresponding parameter file
    """
    Parfile   = xlrd.open_workbook(ParPath + '.xlsx')
    ParHeader = Parfile.sheet_by_name('Cover')
    
    IM = eval(IndexMatch) # List that matches model aspects to parameter indices
    
    ri = 1 # row index
    MetaData = {}
    while True: # read cover sheet info
        ThisItem = ParHeader.cell_value(ri,0)
        if ThisItem != 'Dataset_RecordType':
            MetaData[ThisItem] = ParHeader.cell_value(ri,1)
            ri += 1
        else:
            break # terminate while loop when all meta information is read.
            # Now we are in the row of Dataset_RecordType
    
    # Check whether parameter file uses same classification:
    if 'ODYM_Classifications_Master_' + \
            ScriptConfig['Version of master classification'] != MetaData['Dataset_Classification_version_number']:
        Mylog.critical('CLASSIFICATION FILE FATAL ERROR: Classification file of parameter ' + ThisPar +
                       ' is not identical to the classification master file used for the current model run.')
        
    if ParHeader.cell_value(ri,1) == 'List':
        IList = []
        IListMeaning = []
        ci = 1 # column index
        while True:
            if ParHeader.cell_value(ri +1,ci) != '':
                IList.append(ParHeader.cell_value(ri +1,ci))
                IListMeaning.append(ParHeader.cell_value(ri +2,ci))
                ci += 1
            else:
                break
        # Re-Order indices to fit model aspect order:
        IList = [IList[i] for i in IM]
        IListMeaning = [IListMeaning[i] for i in IM]
            
        ValueList = []
        VIComment = []
        ci = 1 # column index
        while True:
            if ParHeader.cell_value(ri +4,ci) != '':
                ValueList.append(ParHeader.cell_value(ri +3,ci))
                VIComment.append(ParHeader.cell_value(ri +4,ci))
                ci += 1
            else:
                break
        
        # Check whether all indices are present in the index table of the model  
        if set(IList).issubset(set(IndexTable_ClassificationNames)) is False:
            Mylog.error('CLASSIFICATION ERROR: Index list of data file for parameter ' + ThisPar +
                        ' contains indices that are not part of the current model run.')
    
        # Check how well items match between model and data, select items to import
        IndexSizesM  = [] # List of dimension size for model
        for m in range(0,len(ThisParIx)):
            ThisDim = ThisParIx[m]
            # Check whether index is present in parameter file:
            ThisDimClassificationName  = IndexTable.set_index('IndexLetter').ix[ThisDim].Classification.Name
            if ThisDimClassificationName != IList[m]:
                Mylog.error('CLASSIFICATION ERROR: Classification ' + ThisDimClassificationName + ' for aspect ' +
                            ThisDim + ' of parameter ' + ThisPar +
                            ' must be identical to the specified classification of the corresponding parameter dimension, which is ' + IList[m])
                break  # Stop parsing parameter, will cause model to halt
            
            IndexSizesM.append(IndexTable.set_index('IndexLetter').ix[ThisDim]['IndexSize'])

        # Read parameter values into array:
        Values = np.zeros((IndexSizesM))
        ValIns = np.zeros((IndexSizesM)) # Array to check how many values are actually loaded
        ValuesSheet = Parfile.sheet_by_name('Values_Master')
        ColOffset = len(IList)
        RowOffset = 1 # fixed for this format, different quantification layers (value, error, etc.) will be read later
        cx        = 0
        while True:
            try:
                CV = ValuesSheet.cell_value(cx + RowOffset, ColOffset)
            except:
                break
            TargetPosition = []
            for mx in range(0,len(IList)): # mx iterates over the aspects of the parameter 
                CurrentItem = ValuesSheet.cell_value(cx + RowOffset, IM[mx])
                try:
                    TargetPosition.append(IndexTable.set_index('IndexLetter').ix[ThisParIx[mx]].Classification.Items.index(CurrentItem))
                except:
                    break # Current parameter value is not needed for model, outside scope for a certain aspect. 
            if len(TargetPosition) == len(ThisParIx):
                Values[tuple(TargetPosition)] = CV
                ValIns[tuple(TargetPosition)] = 1
            cx += 1
            
        Mylog.info('A total of ' + str(cx+1) + ' values was read from file for parameter ' + ThisPar + '.')
        Mylog.info(str(ValIns.sum()) + ' of ' + str(np.prod(IndexSizesM)) + ' values for parameter ' + ThisPar + ' were assigned.')
         
        
        
    ### Table version ###
    if ParHeader.cell_value(ri,1) == 'Table': # have 3 while loops, one for row indices, one for column indices, one for value layers
       
        RIList        = []
        RISize        = []
        RIListMeaning = []
        ci = 1 # column index
        while True:
            if ParHeader.cell_value(ri +1,ci) != '':
                RIList.append(ParHeader.cell_value(ri +1,ci))
                RISize.append(int(ParHeader.cell_value(ri +2,1)))
                RIListMeaning.append(ParHeader.cell_value(ri +3,ci))
                ci += 1
            else:
                break
        RISize = RISize[0]      
            
        CIList        = []
        CISize        = []
        CIListMeaning = []
        ci = 1 # column index
        while True:
            if ParHeader.cell_value(ri +4,ci) != '':
                CIList.append(ParHeader.cell_value(ri +4,ci))
                CISize.append(int(ParHeader.cell_value(ri +5,1)))
                CIListMeaning.append(ParHeader.cell_value(ri +6,ci))
                ci += 1
            else:
                break
        CISize = CISize[0]
        
        # Re-Order indices to fit model aspect order:
        ComIList        = RIList        + CIList    
        ComIList        = [ComIList[i] for i in IM]                
            
        ValueList = []
        VIComment = []
        ci = 1 # column index
        while True:
            if ParHeader.cell_value(ri +7,ci) != '':
                ValueList.append(ParHeader.cell_value(ri +7,ci))
                VIComment.append(ParHeader.cell_value(ri +8,ci))
                ci += 1
            else:
                break
        
        # Check whether all indices are present in the index table of the model  
        if set(RIList).issubset(set(IndexTable_ClassificationNames)) is False:
            Mylog.error('CLASSIFICATION ERROR: Row index list of data file for parameter ' + ThisPar + ' contains indices that are not part of the current model run.')
        if set(CIList).issubset(set(IndexTable_ClassificationNames)) is False:
            Mylog.error('CLASSIFICATION ERROR: Column index list of data file for parameter ' + ThisPar + ' contains indices that are not part of the current model run.')
            
        # Determine index letters for RIList and CIList
        RIIndexLetter = []
        for m in range(0,len(RIList)):
            RIIndexLetter.append(ThisParIx[IM.index(m)])    
        CIIndexLetter = []
        for m in range(0,len(CIList)):
            CIIndexLetter.append(ThisParIx[IM.index(m+len(RIList))])    
        
        # Check how well items match between model and data, select items to import
        IndexSizesM  = [] # List of dimension size for model
        for m in range(0,len(ThisParIx)):
            ThisDim = ThisParIx[m]
            ThisDimClassificationName  = IndexTable.set_index('IndexLetter').ix[ThisDim].Classification.Name
            if ThisDimClassificationName != ComIList[m]:
                Mylog.error('CLASSIFICATION ERROR: Classification ' + ThisDimClassificationName + ' for aspect ' +
                            ThisDim + ' of parameter ' + ThisPar +
                            ' must be identical to the specified classification of the corresponding parameter dimension, which is ' +
                            ComIList[m])
                break  # Stop parsing parameter, will cause model to halt
                
            IndexSizesM.append(IndexTable.set_index('IndexLetter').ix[ThisDim]['IndexSize'])
        
        # Read parameter values into array:
        Values = np.zeros((IndexSizesM))
        ValIns = np.zeros((IndexSizesM)) # Array to check how many values are actually loaded
        ValuesSheet = Parfile.sheet_by_name(ValueList[ThisParLayerSel[0]])
        ColOffset = len(RIList)
        RowOffset = len(CIList)
        RowNos    = RISize   
        ColNos    = CISize
        
        TargetPos_R = []
        for m in range(0,RowNos):
            TP_RD = []
            for mc in range(0,len(RIList)):
                try:
                    CurrentItem = int(ValuesSheet.cell_value(m + RowOffset, mc))
                except:
                    CurrentItem = ValuesSheet.cell_value(m + RowOffset, mc)
                try:
                    IX   = ThisParIx.find(RIIndexLetter[mc])
                    TPIX = IndexTable.set_index('IndexLetter').ix[RIIndexLetter[mc]].Classification.Items.index(CurrentItem)
                    TP_RD.append((IX,TPIX))
                except:
                    TP_RD.append(None)
                    break
            TargetPos_R.append(TP_RD)           

        TargetPos_C = []                
        for n in range(0,ColNos):
            TP_CD = []
            for mc in range(0,len(CIList)):
                try:
                    CurrentItem = int(ValuesSheet.cell_value(mc, n + ColOffset))
                except:
                    CurrentItem = ValuesSheet.cell_value(mc, n + ColOffset)
                try:
                    IX = ThisParIx.find(CIIndexLetter[mc])
                    TPIX = IndexTable.set_index('IndexLetter').ix[CIIndexLetter[mc]].Classification.Items.index(CurrentItem)
                    TP_CD.append((IX,TPIX))
                except:
                    TP_CD.append(None)
                    break  
            TargetPos_C.append(TP_CD)
        
        for m in range(0,RowNos):
            for n in range(0,ColNos):
                TargetPosition = [0 for i in range(0,len(ComIList))]
                try:
                    for i in range(0,len(RIList)):
                        TargetPosition[TargetPos_R[m][i][0]] = TargetPos_R[m][i][1] 
                    for i in range(0,len(CIList)):
                        TargetPosition[TargetPos_C[n][i][0]] = TargetPos_C[n][i][1] 
                except:
                    TargetPosition = [0]
                if len(TargetPosition) == len(ComIList):
                    Values[tuple(TargetPosition)] = ValuesSheet.cell_value(m + RowOffset, n + ColOffset)
                    ValIns[tuple(TargetPosition)] = 1
                    
        Mylog.info(str(ValIns.sum()) + ' of ' + str(np.prod(IndexSizesM)) + ' values for parameter ' + ThisPar +
                   ' were assigned.')
       
    return MetaData, Values



def ReadParameterV2(ParPath, ThisPar, ThisParIx, IndexMatch, ThisParLayerSel, MasterClassification,
                    IndexTable, IndexTable_ClassificationNames, ScriptConfig, Mylog, ParseUncertainty):
    """
    This function reads a model parameter from the corresponding parameter file
    """
    Parfile   = xlrd.open_workbook(ParPath + '.xlsx')
    ParHeader = Parfile.sheet_by_name('Cover')
    
    IM = eval(IndexMatch) # List that matches model aspects to parameter indices
    
    ri = 1 # row index
    MetaData = {}
    while True: # read cover sheet info
        ThisItem = ParHeader.cell_value(ri,0)
        if (ThisItem != '[Empty on purpose]' and ThisItem != 'Dataset_RecordType'):
            MetaData[ThisItem] = ParHeader.cell_value(ri,1)
            if ThisItem == 'Dataset_Unit':
                if ParHeader.cell_value(ri,1) == 'GLOBAL':
                    MetaData['Unit_Global']         = ParHeader.cell_value(ri,2)
                    MetaData['Unit_Global_Comment'] = ParHeader.cell_value(ri,3) 
            if ThisItem == 'Dataset_Uncertainty':
                # if LIST is specified, nothing happens here.
                if ParHeader.cell_value(ri,1) == 'GLOBAL':
                    MetaData['Dataset_Uncertainty_Global'] = ParHeader.cell_value(ri,2)
                if ParHeader.cell_value(ri,1) == 'TABLE':
                    MetaData['Dataset_Uncertainty_Sheet']  = ParHeader.cell_value(ri,2)                    
            if ThisItem == 'Dataset_Comment':
                if ParHeader.cell_value(ri,1) == 'GLOBAL':
                    MetaData['Dataset_Comment_Global']     = ParHeader.cell_value(ri,2)                    
            ri += 1
        else:
            break # terminate while loop when all meta information is read.
            # Now we are in the row of Dataset_RecordType
    
    # Check whether parameter file uses same classification:
    if  ScriptConfig['Version of master classification'] != MetaData['Dataset_Classification_version_number']:
        Mylog.critical('CLASSIFICATION FILE FATAL ERROR: Classification file of parameter ' + ThisPar +
                       ' is not identical to the classification master file used for the current model run.')
        
    # Continue parsing until line 'Dataset_RecordType' is found:
    while True:
        ThisItem = ParHeader.cell_value(ri,0)
        if ThisItem == 'Dataset_RecordType':  
            break
        else:
            ri += 1
        
    ### List version ###        
    if ParHeader.cell_value(ri,1) == 'LIST':
        IList = []
        IListMeaning = []
        RI_Start = ri + 2
        while True:
            if ParHeader.cell_value(RI_Start,0) != '':
                IList.append(ParHeader.cell_value(RI_Start,0))
                IListMeaning.append(ParHeader.cell_value(RI_Start,1))
                RI_Start += 1
            else:
                break
        # Re-Order indices to fit model aspect order:
        IList = [IList[i] for i in IM]
        IListMeaning = [IListMeaning[i] for i in IM]
            
        ValueList = []
        VIComment = []
        RI_Start = ri + 2
        while True:
            if ParHeader.cell_value(RI_Start,2) != '':
                ValueList.append(ParHeader.cell_value(RI_Start,2))
                VIComment.append(ParHeader.cell_value(RI_Start,3))
                RI_Start += 1
            else:
                break
        
        # Check whether all indices are present in the index table of the model  
        if set(IList).issubset(set(IndexTable_ClassificationNames)) is False:
            Mylog.error('CLASSIFICATION ERROR: Index list of data file for parameter ' + ThisPar +
                        ' contains indices that are not part of the current model run.')
    
        # Check how well items match between model and data, select items to import
        IndexSizesM  = [] # List of dimension size for model
        for m in range(0,len(ThisParIx)):
            ThisDim = ThisParIx[m]
            # Check whether index is present in parameter file:
            ThisDimClassificationName  = IndexTable.set_index('IndexLetter').ix[ThisDim].Classification.Name
            if ThisDimClassificationName != IList[m]:
                Mylog.error('CLASSIFICATION ERROR: Classification ' + ThisDimClassificationName + ' for aspect ' +
                            ThisDim + ' of parameter ' + ThisPar +
                            ' must be identical to the specified classification of the corresponding parameter dimension, which is ' + IList[m])
                break  # Stop parsing parameter, will cause model to halt
            
            IndexSizesM.append(IndexTable.set_index('IndexLetter').ix[ThisDim]['IndexSize'])

        # Read parameter values into array, uncertainty into list:
        Values      = np.zeros((IndexSizesM)) # Array for parameter values
        Uncertainty = [None] * np.product(IndexSizesM) # parameter value uncertainties  
        ValIns      = np.zeros((IndexSizesM)) # Array to check how many values are actually loaded
        ValuesSheet = Parfile.sheet_by_name('Values_Master')
        ColOffset = len(IList)
        RowOffset = 1 # fixed for this format, different quantification layers (value, error, etc.) will be read later
        cx        = 0
        while True:
            try:
                CV = ValuesSheet.cell_value(cx + RowOffset, ColOffset)
            except:
                break
            TargetPosition = []
            for mx in range(0,len(IList)): # mx iterates over the aspects of the parameter 
                CurrentItem = ValuesSheet.cell_value(cx + RowOffset, IM[mx])
                try:
                    TargetPosition.append(IndexTable.set_index('IndexLetter').ix[ThisParIx[mx]].Classification.Items.index(CurrentItem))
                except:
                    break # Current parameter value is not needed for model, outside scope for a certain aspect. 
            if len(TargetPosition) == len(ThisParIx):
                Values[tuple(TargetPosition)] = CV
                ValIns[tuple(TargetPosition)] = 1
                Uncertainty[Tuple_MI(TargetPosition, IndexSizesM)] = ValuesSheet.cell_value(cx + RowOffset, ColOffset + 3)
            cx += 1
            
        Mylog.info('A total of ' + str(cx) + ' values was read from file for parameter ' + ThisPar + '.')
        Mylog.info(str(ValIns.sum()) + ' of ' + str(np.prod(IndexSizesM)) + ' values for parameter ' + ThisPar + ' were assigned.')
         
        
        
    ### Table version ###
    if ParHeader.cell_value(ri,1) == 'TABLE': # have 3 while loops, one for row indices, one for column indices, one for value layers
        ColNos =  int(ParHeader.cell_value(ri,5)) # Number of columns in dataset
        RowNos =  int(ParHeader.cell_value(ri,3)) # Number of rows in dataset
        
        RI = ri + 2 # row where indices start
        RIList        = []
        RIListMeaning = []
        while True:
            if ParHeader.cell_value(RI,0) != '':
                RIList.append(ParHeader.cell_value(RI,0))
                RIListMeaning.append(ParHeader.cell_value(RI,1))
                RI += 1
            else:
                break

        RI = ri + 2 # row where indices start    
        CIList        = []
        CIListMeaning = []
        while True:
            if ParHeader.cell_value(RI,2) != '':
                CIList.append(ParHeader.cell_value(RI,2))
                CIListMeaning.append(ParHeader.cell_value(RI,3))
                RI += 1
            else:
                break
        
        # Re-Order indices to fit model aspect order:
        ComIList        = RIList        + CIList    # List of all indices, both rows and columns
        ComIList        = [ComIList[i] for i in IM]                
            
        RI = ri + 2 # row where indices start  
        ValueList = []
        VIComment = []
        while True:
            if ParHeader.cell_value(RI,4) != '':
                ValueList.append(ParHeader.cell_value(RI,4))
                VIComment.append(ParHeader.cell_value(RI,5))
                RI += 1
            else:
                break
        
        # Check whether all indices are present in the index table of the model  
        if set(RIList).issubset(set(IndexTable_ClassificationNames)) is False:
            Mylog.error('CLASSIFICATION ERROR: Row index list of data file for parameter ' + ThisPar + ' contains indices that are not part of the current model run.')
        if set(CIList).issubset(set(IndexTable_ClassificationNames)) is False:
            Mylog.error('CLASSIFICATION ERROR: Column index list of data file for parameter ' + ThisPar + ' contains indices that are not part of the current model run.')
            
        # Determine index letters for RIList and CIList
        RIIndexLetter = []
        for m in range(0,len(RIList)):
            RIIndexLetter.append(ThisParIx[IM.index(m)])    
        CIIndexLetter = []
        for m in range(0,len(CIList)):
            CIIndexLetter.append(ThisParIx[IM.index(m+len(RIList))])    
        
        # Check how well items match between model and data, select items to import
        IndexSizesM  = [] # List of dimension size for model
        for m in range(0,len(ThisParIx)):
            ThisDim = ThisParIx[m]
            ThisDimClassificationName  = IndexTable.set_index('IndexLetter').ix[ThisDim].Classification.Name
            if ThisDimClassificationName != ComIList[m]:
                Mylog.error('CLASSIFICATION ERROR: Classification ' + ThisDimClassificationName + ' for aspect ' +
                            ThisDim + ' of parameter ' + ThisPar +
                            ' must be identical to the specified classification of the corresponding parameter dimension, which is ' +
                            ComIList[m])
                break  # Stop parsing parameter, will cause model to halt
                
            IndexSizesM.append(IndexTable.set_index('IndexLetter').ix[ThisDim]['IndexSize'])
        
        # Read parameter values into array:
        Values      = np.zeros((IndexSizesM)) # Array for parameter values
        Uncertainty = [None] * np.product(IndexSizesM) # parameter value uncertainties  
        ValIns      = np.zeros((IndexSizesM)) # Array to check how many values are actually loaded, contains 0 or 1.
        ValuesSheet = Parfile.sheet_by_name(ValueList[ThisParLayerSel[0]])
        if 'Dataset_Uncertainty_Sheet' in MetaData:
            UncertSheet = Parfile.sheet_by_name(MetaData['Dataset_Uncertainty_Sheet'])
        ColOffset   = len(RIList)
        RowOffset   = len(CIList)
        cx          = 0
        
        TargetPos_R = [] # Determine all row target positions in data array
        for m in range(0,RowNos):
            TP_RD = []
            for mc in range(0,len(RIList)):
                try:
                    CurrentItem = int(ValuesSheet.cell_value(m + RowOffset, mc)) # in case items come as int, e.g., years
                except:
                    CurrentItem = ValuesSheet.cell_value(m + RowOffset, mc)
                try:
                    IX   = ThisParIx.find(RIIndexLetter[mc])
                    TPIX = IndexTable.set_index('IndexLetter').ix[RIIndexLetter[mc]].Classification.Items.index(CurrentItem)
                    TP_RD.append((IX,TPIX))
                except:
                    TP_RD.append(None)
                    break
            TargetPos_R.append(TP_RD)         
                

        TargetPos_C = [] # Determine all col target positions in data array  
        for n in range(0,ColNos):
            TP_CD = []
            for mc in range(0,len(CIList)):
                try:
                    CurrentItem = int(ValuesSheet.cell_value(mc, n + ColOffset))
                except:
                    CurrentItem = ValuesSheet.cell_value(mc, n + ColOffset)
                try:
                    IX = ThisParIx.find(CIIndexLetter[mc])
                    TPIX = IndexTable.set_index('IndexLetter').ix[CIIndexLetter[mc]].Classification.Items.index(CurrentItem)
                    TP_CD.append((IX,TPIX))
                except:
                    TP_CD.append(None)
                    break  
            TargetPos_C.append(TP_CD)
        
        for m in range(0,RowNos): # Read values from excel template
            for n in range(0,ColNos):
                TargetPosition = [0 for i in range(0,len(ComIList))]
                try:
                    for i in range(0,len(RIList)):
                        TargetPosition[TargetPos_R[m][i][0]] = TargetPos_R[m][i][1] 
                    for i in range(0,len(CIList)):
                        TargetPosition[TargetPos_C[n][i][0]] = TargetPos_C[n][i][1] 
                except:
                    TargetPosition = [0]
                if len(TargetPosition) == len(ComIList): # Read value if TargetPosition Tuple has same length as indexList
                    Values[tuple(TargetPosition)] = ValuesSheet.cell_value(m + RowOffset, n + ColOffset)
                    ValIns[tuple(TargetPosition)] = 1
                    # Add uncertainty
                    if 'Dataset_Uncertainty_Global' in MetaData:
                        Uncertainty[Tuple_MI(TargetPosition, IndexSizesM)] = MetaData['Dataset_Uncertainty_Global']
                    if 'Dataset_Uncertainty_Sheet' in MetaData:
                        Uncertainty[Tuple_MI(TargetPosition, IndexSizesM)] = UncertSheet.cell_value(m + RowOffset, n + ColOffset)
                cx += 1

        Mylog.info('A total of ' + str(cx) + ' values was read from file for parameter ' + ThisPar + '.')                    
        Mylog.info(str(ValIns.sum()) + ' of ' + str(np.prod(IndexSizesM)) + ' values for parameter ' + ThisPar +
                   ' were assigned.')
    if ParseUncertainty == True:
        return MetaData, Values, Uncertainty
    else:
        return MetaData, Values

def compute_stock_driven_model_initialstock_typesplit(FutureStock,InitialStock,SFArrayCombined,TypeSplit, NegativeInflowCorrect = False):
    """ 
    With given total future stock and lifetime distribution, the method builds the stock by cohort and the inflow.
    The age structure of the initial stock is given for each technology, and a type split of total inflow into different technology types is given as well.
    
    SPECIFICATION: Stocks are always measured AT THE END of the discrete time interval.
    
    Indices:
      t: time: Entire time frame: from earliest age-cohort to latest model year.
      c: age-cohort: same as time.
      T: Switch time: DEFINED as first year where historic stock is NOT present, = last year where historic stock is present +1.
      g: product type
    
    Data:
      FutureStock[t],           total future stock at end of each year, starting at T
      InitialStock[c,g],        0...T-1;0...T-1, stock at the end of T-1, by age-cohort c and product type g
      SFArrayCombined[t,c,g],   Survival function of age-cohort c at end of year t for product type g
      Typesplit[t,g],           splits total inflow into product types for future years 
      NegativeInflowCorrect     BOOL, retains items in stock if their leaving would lead to negative inflows. 
        
    The extra parameter InitialStock is a vector that contains the age structure of the stock at time t0, and it covers as many historic cohorts as there are elements in it.
    In the year SwitchTime the model switches from the historic stock to the stock-driven approach.
    Only future years, i.e., years after SwitchTime, are computed and returned.
    The InitialStock is a vector of the age-cohort composition of the stock at SwitchTime, with length SwitchTime.
    The parameter TypeSplit splits the total inflow into Ng types. """
    
    SwitchTime = SFArrayCombined.shape[0] - FutureStock.shape[0]
    Ntt        = SFArrayCombined.shape[0] # Total no of years
    Nt0        = FutureStock.shape[0]     # No of future years
    Ng         = SFArrayCombined.shape[2] # No of product groups
    
    s_cg = np.zeros((Nt0,Ntt,Ng)) # stock year, cohort and product
    o_cg = np.zeros((Nt0,Ntt,Ng)) # outflow by year, cohort and product
    i_g  = np.zeros((Ntt,Ng))     # inflow by product
    
    # Construct historic inflows
    for c in range(0,SwitchTime): # for all historic age-cohorts til SwitchTime - 1:
        for g in range(0,Ng):
            if SFArrayCombined[SwitchTime-1,c,g] != 0:
             i_g[c,g] = InitialStock[c,g] / SFArrayCombined[SwitchTime-1,c,g]
             
             # if InitialStock is 0, historic inflow also remains 0, 
             # as it has no impact on future anymore.
             
             # If survival function is 0 but initial stock is not, the data are inconsisent and need to be revised.
             # For example, a safety-relevant device with 5 years fixed lifetime but a 10 year old device is present.
             # Such items will be ignored and break the mass balance.

    # year-by-year computation, starting from SwitchTime
    for t in range(SwitchTime, Ntt):  # for all years t, starting at SwitchTime
        # 1) Compute stock at the end of the year:
        s_cg[t - SwitchTime,:,:] = np.einsum('cg,cg->cg',i_g,SFArrayCombined[t,:,:])
        # 2) Compute outflow during year t from previous age-cohorts:
        if t == SwitchTime:
            o_cg[t -SwitchTime,:,:] = InitialStock - s_cg[t -SwitchTime,:,:]
        else:
            o_cg[t -SwitchTime,:,:] = s_cg[t -SwitchTime -1,:,:] - s_cg[t -SwitchTime,:,:] # outflow table is filled row-wise, for each year t.
        # 3) Determine total inflow from mass balance:
        i0 = FutureStock[t -SwitchTime] - s_cg[t - SwitchTime,:,:].sum()
        # 3a) Correct remaining stock in cases where inflow would be negative:
#        if NegativeInflowCorrect is True:
#            if self.i[m] < 0: # if stock-driven model yield negative inflow
#                Delta = -1 * self.i[m].copy() # Delta > 0!
#                self.i[m] = 0 # Set inflow to 0 and distribute mass balance gap onto remaining cohorts:
#                if self.o_c[m,:].sum() != 0:
#                    Delta_c = Delta * self.o_c[m, :] / self.o_c[m,:].sum() # Distribute gap proportionally to outflow
#                else:
#                    Delta_c = 0
#                self.o_c[m, :] = self.o_c[m, :] - Delta_c # reduce outflow by Delta_c
#                self.s_c[m, :] = self.s_c[m, :] + Delta_c # augment stock by Delta_c
#                # NOTE: This method is only of of many plausible methods of reducing the outflow to keep stock levels high.
#                # It may lead to implausible results, and, if Delta > sum(self.o_c[m,:]), also to negative outflows.
#                # In such situations it is much better to change the lifetime assumption than using the NegativeInflowCorrect option.
        # 4) Add new inflow to stock and determine future decay of new age-cohort
        i_g[t,:] = TypeSplit[t -SwitchTime,:] * i0
        for g in range(0,Ng): # Correct for share of inflow leaving during first year.
            if SFArrayCombined[t,t,g] != 0: # Else, inflow leaves within the same year and stock modelling is useless
                i_g[t,g] = i_g[t,g] / SFArrayCombined[t,t,g] # allow for outflow during first year by rescaling with 1/SF[t,t,g]
            s_cg[t -SwitchTime,t,g]  = i_g[t,g] * SFArrayCombined[t,t,g]
            o_cg[t -SwitchTime,t,g]  = i_g[t,g] * (1 - SFArrayCombined[t,t,g])
        
    return s_cg, o_cg, i_g


def ExcelSheetFill(Workbook, Sheetname, values, topcornerlabel=None,
                   rowlabels=None, collabels=None, Style=None,
                   rowselect=None, colselect=None):
    Sheet = Workbook.add_sheet(Sheetname)
    if topcornerlabel is not None:
        if Style is not None:
            Sheet.write(0,0,label = topcornerlabel, style = Style)  # write top corner label
        else:
            Sheet.write(0,0,label = topcornerlabel)  # write top corner label
    if rowselect is None: # assign row select if not present (includes all rows in that case)
        rowselect = np.ones((values.shape[0]))
    if colselect is None: # assign col select if not present (includes all columns in that case)
        colselect = np.ones((values.shape[1]))        
    if rowlabels is not None: # write row labels
         rowindexcount = 0
         for m in range(0,len(rowlabels)):
             if rowselect[m] == 1: # True if True or 1
                 if Style is None:
                     Sheet.write(rowindexcount +1, 0, label = rowlabels[m])
                 else:
                     Sheet.write(rowindexcount +1, 0, label = rowlabels[m], style = Style)
                 rowindexcount += 1
    if collabels is not None: # write column labels
         colindexcount = 0
         for m in range(0,len(collabels)):
             if colselect[m] == 1: # True if True or 1
                 if Style is None:
                     Sheet.write(0, colindexcount +1, label = collabels[m])
                 else:
                     Sheet.write(0, colindexcount +1, label = collabels[m], style = Style)
                 colindexcount += 1   
    # write values:
    rowindexcount = 0
    for m in range(0,values.shape[0]): # for all rows
        if rowselect[m] == 1:
            colindexcount = 0
            for n in range(0,values.shape[1]): # for all columns
                if colselect[n] == 1:
                    Sheet.write(rowindexcount +1, colindexcount + 1, label=values[m, n])
                    colindexcount += 1
            rowindexcount += 1
                       
            

def convert_log(file, file_format='html'):
    """
    Converts the log file to a given file format

    :param file: The filename and path
    :param file_format: The desired format
    """
    output_filename = os.path.splitext(file)[0] + '.' + file_format
    output = pypandoc.convert_file(file, file_format, outputfile=output_filename)
    assert output == ""

# The End

