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
    return str('0.1')


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
    :param logfile_type: Type of file to write. Mardown syntax is the default.
        TODO: If other outputs types are desired, they can be converted via pandoc.
    :return: A logger that can be used by other files to write to the log(file)
    """

    log_file = os.path.join(log_pathname, '..', log_filename)
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


def EvalItemSelectString(ItemSelectStr,IndexLength): # Extract index item selection lists from ODYM datafile information
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
    """
    IsValuesRev = []
    CurrentValue = value
    for m in range(0,len(Is)):
        IsValuesRev.append(CurrentValue % Is[len(Is)-m-1])
        CurrentValue = CurrentValue // Is[len(Is)-m-1]
    return IsValuesRev[::-1]

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

