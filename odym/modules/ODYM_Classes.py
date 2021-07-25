# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 17:29:41 2017

@author: spauliuk
"""

"""
File ODYM_Classes
Check https://github.com/IndEcol/ODYM for latest version.

Contains class definitions for ODYM

standard abbreviation: msc (material-system-classes)

dependencies:
    numpy >= 1.9
    scipy >= 0.14

Repository for this class, documentation, and tutorials: https://github.com/IndEcol/ODYM

"""
import os
import logging
import numpy as np
import pandas as pd
import xlrd, xlwt

####################################
#      Define classes for ODYM  #
####################################

def __version__():
    return str('1.0') # version number of this file


class Obj(object):
    """
    Class with the object definition for a data object (system, process, flow, ...) in ODYM
    """
    def __init__(self, Name=None, ID=None, UUID=None):
        """ Basic initialisation of Obj."""
        self.Name            = Name # object name
        self.ID              = ID   # object ID
        self.UUID            = UUID # object UUID
        self.Aspects         = {'Time': 'Model time','Cohort': 'Age-cohort','OriginProcess':'Process where flow originates','DestinationProcess':'Destination process of flow','OriginRegion': 'Region where flow originates from','DestinationRegion': 'Region where flow is bound to', 'Good': 'Process, good, or commodity', 'Material': 'Material: ore, alloy, scrap type, ...','Element': 'Chemical element' } # Define the aspects of the system variables
        self.Dimensions      = {'Time': 'Time', 'Process':'Process', 'Region': 'Region', 'Good': 'Process, good, or commodity', 'Material': 'Material: ore, alloy, scrap type, ...','Element': 'Chemical element' } # Define the dimensions of the system variables


        
class Classification(Obj):
  
    """
    Class for aspect classification
    """
    
    def __init__(self, Name = None, ID = None, UUID = None, Dimension = None, Items = None, IDs = None, AdditionalProporties = {}):
        """ Basic initialisation of an item list for alloys, materials, etc."""
        Obj.__init__(self, Name = Name, ID = ID, UUID = UUID) # Hand over parameters to parent class init
        self.Dimension         = Dimension # Dimension of classification: Time, Region, process, material, goods, ...
        self.Items             = Items # list with names of items
        self.IDs               = IDs # list with IDs of items
        self.AdditionalProps   = AdditionalProporties # Like population for regions, element composition for alloys, ...
        
        
class MFAsystem(Obj):

    """
    Class with the definition and methods for a system in ODYM
    """
    
    def __init__(self, Name, Time_Start, Time_End, Geogr_Scope, Unit, IndexTable, Elements, ProcessList = [], FlowDict = {}, StockDict = {}, ParameterDict = {}, Graphical = None, ID = None, UUID = None, ):
        """ Initialisation of MFAsystem."""
        Obj.__init__(self, Name = Name, ID = ID, UUID = UUID) # Hand over parameters to parent class init
        
        self.Time_Start      = Time_Start # start time of model (year: int)
        self.Time_End        = Time_End # end time of model (year: int)
        self.Geogr_Scope     = Geogr_Scope   # geographical boundary (string)
        self.Elements        = Elements # list of chemical elements considered, indicated by atomic numbers
        self.Unit            = Unit    # flow and stock base unit, without 'per yr'
        
        self.ProcessList     = ProcessList # list of processes, processes are referred to by their number
        self.FlowDict        = FlowDict # Dictionary of flows, are indexed by tuples of process they are attached to (p1,p2)
        self.StockDict       = StockDict # Dictionary of stocks, are indexed by process they are located at (p)
        self.ParameterDict   = ParameterDict # Dictionary of of parameters: lifetime, yield rates, etc.
        self.IndexTable      = IndexTable # Dictionary of abbreviations for aspect-classification tuples 
        
        self.Graphical       = Graphical # Dictionary of graphical properties (size in pixel, background color, etc.)

    @property
    def Time_V(self):
        """ Array of all model years"""
        return np.arange(self.Time_Start,self.Time_End +1,1)
        
    @property
    def Time_L(self):
        """ List of all model years"""
        return np.arange(self.Time_Start,self.Time_End +1,1).tolist()
        
    def IndexTableCheck(self):
        """ Check whether chosen classifications fit to dimensions of index table."""
        for indx in self.IndexTable.index:
            if self.IndexTable.loc[indx]['Dimension']  != self.IndexTable.loc[indx]['Classification'].Dimension:
                raise ValueError('Dimension mismatch. Dimension of classifiation needs to fit to dimension of flow or parameter index. Found a mismatch for the following index: {foo}. Check your index table definition!'.format(foo = indx))
        if 'Time' not in self.IndexTable.index:
            raise ValueError(' "Time" aspect must be present in IndexTable. Please check your index table definition!')            
        if 'Element' not in self.IndexTable.index:
            raise ValueError(' "Element" aspect must be present in IndexTable. Please check your index table definition!')                            
        if len(self.IndexTable.loc['Element'].Classification.Items) == 0:
            raise ValueError('Need at least one element in element list, please check your classification definition!')
        if len(self.IndexTable.loc['Time'].Classification.Items) == 0:
            raise ValueError('Need at least one element in Time list, please check your classification definition!')

        return True
           
    def Initialize_FlowValues(self):
        """ This method will construct empty numpy arrays (zeros) for all flows where the value is None and wheree the indices are given."""
        for key in self.FlowDict:
            if self.FlowDict[key].Values is None:
                self.FlowDict[key].Values = np.zeros(tuple([len(self.IndexTable.set_index('IndexLetter').loc[x]['Classification'].Items) for x in self.FlowDict[key].Indices.split(',')]))   
#        Raw code, for development        
#        Indices = 't,Ro,a,e'
#        IndList = Indices.split(',')
#        Dimensions = [len(IndexTable.ix[x]['Classification'].Items) for x in IndList]
#        Values = np.zeros(tuple(Dimensions))       

    def Initialize_StockValues(self):
        """ This method will construct empty numpy arrays (zeros) for all stocks where the value is None and wheree the indices are given."""
        for key in self.StockDict:
            if self.StockDict[key].Values is None:
                self.StockDict[key].Values = np.zeros(tuple([len(self.IndexTable.set_index('IndexLetter').loc[x]['Classification'].Items) for x in self.StockDict[key].Indices.split(',')]))   

    def Initialize_ParameterValues(self):
        """ This method will construct empty numpy arrays (zeros) for all parameters where the value is None and wheree the indices are given."""
        for key in self.ParameterDict:
            if self.ParameterDict[key].Values is None:
                self.ParameterDict[key].Values = np.zeros(tuple([len(self.IndexTable.set_index('IndexLetter').loc[x]['Classification'].Items) for x in self.ParameterDict[key].Indices.split(',')]))                   
                
    def Consistency_Check(self):
        """ Method that check a readily defined system for consistency of dimensions, Value setting, etc. See detailed comments."""                
        
        # 1) Check dimension consistency in index table:
        A = self.IndexTableCheck()
        
        # 2) Check whether all process indices that the flows refer to are in the process list:
        for key in self.FlowDict:
            if self.FlowDict[key].P_Start > len(self.ProcessList) -1:
                raise ValueError('Start process of flow {foo} not present. Check your flow definition!'.format(foo = key))
            if self.FlowDict[key].P_End > len(self.ProcessList) -1:
                raise ValueError('End process of flow {foo} not present. Check your flow definition!'.format(foo = key))                
        
        # 3) Check whethe all flow valua arrays match with the index structure:
        for key in self.FlowDict:
            if tuple([len(self.IndexTable.set_index('IndexLetter').loc[x]['Classification'].Items) for x in self.FlowDict[key].Indices.split(',')]) != self.FlowDict[key].Values.shape:
                raise ValueError('Dimension mismatch. Dimension of flow value array does not fit to flow indices for flow {foo}. Check your flow and flow value definition!'.format(foo = key))
                
        return A, True, True
        
    def Flow_Sum_By_Element(self,FlowKey):
        """ 
        Reduce flow values to a Time x Elements matrix and return as t x e array.
        We take the indices of each flow, e.g., 't,O,D,G,m,e', strip off the ',' to get 'tODGme', 
        add a '->' and the index letters for time and element (here, t and e), 
        and call the Einstein sum function np.einsum with the string 'tODGme->te', 
        and apply it to the flow values. 
        """
        return np.einsum(self.FlowDict[FlowKey].Indices.replace(',','') + '->'+ self.IndexTable.loc['Time'].IndexLetter + self.IndexTable.loc['Element'].IndexLetter ,self.FlowDict[FlowKey].Values) 
    
    def Stock_Sum_By_Element(self,StockKey):
        """ 
        Reduce stock values to a Time x Elements matrix and return as t x e array.
        We take the indices of each stock, e.g., 't,c,G,m,e', strip off the ',' to get 'tcGme', 
        add a '->' and the index letters for time and element (here, t and e), 
        and call the Einstein sum function np.einsum with the string 'tcGme->te', 
        and apply it to the stock values. 
        """
        return np.einsum(self.StockDict[StockKey].Indices.replace(',','') + '->'+ self.IndexTable.loc['Time'].IndexLetter + self.IndexTable.loc['Element'].IndexLetter ,self.StockDict[StockKey].Values) 
                 
    def MassBalance(self, Element = None):
        """ 
        Determines mass balance of MFAsystem
        We take the indices of each flow, e.g., 't,O,D,G,m,e', strip off the ',' to get 'tODGme', 
        add a '->' and the index letters for time and element (here, t and e), 
        and call the Einstein sum function np.einsum with the string 'tODGme->te', 
        and apply it to the flow values. 
        Sum to t and e is subtracted from process where flow is leaving from and added to destination process.
        """
        Bal = np.zeros((len(self.Time_L),len(self.ProcessList),len(self.Elements))) # Balance array: years x process x element: 
        #process position 0 is the balance for the system boundary, the other positions are for the processes, 
        #element position 0 is the balance for the entire mass, the other are for the balance of the individual elements
        
        for key in self.FlowDict: # Add all flows to mass balance
            Bal[:,self.FlowDict[key].P_Start,:] -= self.Flow_Sum_By_Element(key) # Flow leaving a process
            Bal[:,self.FlowDict[key].P_End,:]   += self.Flow_Sum_By_Element(key) # Flow entering a process
            
        for key in self.StockDict: # Add all stock changes to the mass balance
            if  self.StockDict[key].Type == 1:
                Bal[:,self.StockDict[key].P_Res,:] -= self.Stock_Sum_By_Element(key) # 1: net stock change or addition to stock
            elif self.StockDict[key].Type == 2:
                Bal[:,self.StockDict[key].P_Res,:] += self.Stock_Sum_By_Element(key) # 2: removal/release from stock
            
        #add stock changes to process with number 0 ('system boundary, environment of system')
        for key in self.StockDict:
            if  self.StockDict[key].Type == 1:
                Bal[:,0,:] += self.Stock_Sum_By_Element(key) # 1: net stock change or addition to stock
            elif self.StockDict[key].Type == 2:
                Bal[:,0,:] -= self.Stock_Sum_By_Element(key) # 2: removal/release from stock
            
        return Bal
    
    def Check_If_All_Chem_Elements_Are_present(self,FlowKey,AllElementsIndex):
        """
        This method is applicable to systems where the chemical element list contains both 0 ('all' chemical elements) and individual elements.
        It checks whether the sum of the system variable of the other elements equals the entry for element 0.
        This means that the breakdown of the system variable into individual elements has the same mass as the total for all elements.
        AllElementsindex is the position of the element 0 in the element list, typically, it is also 0.
        """
        txe = self.Flow_Sum_By_Element(FlowKey)
        txe_0 = txe[:,AllElementsIndex]
        txe_o = np.delete(txe,AllElementsIndex,axis=1).sum(axis=1)
        if np.allclose(txe_0,txe_o):
            Check = True
        else:
            Check = False
        return Check, txe_0, txe_o  # Check flag, time series for element 'all', time series for all 'other' elements.
        
    def SankeyExport(self,Year, Path, Element): # Export data for given year in excel format for the D3.js Circular Sankey method
        """ Exports MFAsystem to xls Template for the Circular Sankey method."""
        
        TimeIndex = Year - self.Time_Start
        
        myfont = xlwt.Font()
        myfont.bold = True
        mystyle = xlwt.XFStyle()
        mystyle.font = myfont
        
        Result_workbook  = xlwt.Workbook(encoding = 'ascii') 
        Result_worksheet = Result_workbook.add_sheet('Nodes') 
        Result_worksheet.write(0, 0, label = 'Name', style = mystyle)
        Result_worksheet.write(0, 1, label = 'Color', style = mystyle)
        Result_worksheet.write(0, 2, label = 'Orientation', style = mystyle)
        Result_worksheet.write(0, 3, label = 'Width', style = mystyle)
        Result_worksheet.write(0, 4, label = 'Height', style = mystyle)
        Result_worksheet.write(0, 5, label = 'x_position', style = mystyle)
        Result_worksheet.write(0, 6, label = 'y_position', style = mystyle)
        
        for m in range(0,len(self.ProcessList)): 
            if self.ProcessList[m].Graphical is None:
                raise ValueError('Graphical properties of process number {foo} are not set. No export to Sankey possible, as position of process on canvas etc. needs is not specified.'.format(foo = m))
            Result_worksheet.write(m +1, 0, label = self.ProcessList[m].Graphical['Name'])
            Result_worksheet.write(m +1, 1, label = self.ProcessList[m].Graphical['Color'])
            Result_worksheet.write(m +1, 2, label = self.ProcessList[m].Graphical['Angle'])
            Result_worksheet.write(m +1, 3, label = self.ProcessList[m].Graphical['Width'])
            Result_worksheet.write(m +1, 4, label = self.ProcessList[m].Graphical['Height'])
            Result_worksheet.write(m +1, 5, label = self.ProcessList[m].Graphical['xPos'])
            Result_worksheet.write(m +1, 6, label = self.ProcessList[m].Graphical['yPos'])
            
        Result_worksheet = Result_workbook.add_sheet('Flows') 
        Result_worksheet.write(0, 0, label = 'StartNode', style = mystyle)
        Result_worksheet.write(0, 1, label = 'EndNode', style = mystyle)
        Result_worksheet.write(0, 2, label = 'Value', style = mystyle)
        Result_worksheet.write(0, 3, label = 'Color', style = mystyle)
        
        for key in self.FlowDict:
            Result_worksheet.write(m +1, 0, label = self.FlowDict[key].P_Start)
            Result_worksheet.write(m +1, 1, label = self.FlowDict[key].P_End)
            Result_worksheet.write(m +1, 2, label = float(self.Flow_Sum_By_Element(key)[TimeIndex,Element]))
            Result_worksheet.write(m +1, 3, label = self.FlowDict[key].Color)
            
        Result_workbook.save(Path + self.Name + '_' + str(TimeIndex) + '_' + str(Element) + '_Sankey.xls')  
        
        
class Process(Obj):

    """
    Class with the definition and methods for a process in ODYM
    """
    
    def __init__(self, Name = None, ID = None, UUID = None, Bipartite = None, Graphical = None, Extensions = None, Parameters = None):
        """ Basic initialisation of a process."""
        Obj.__init__(self, Name = Name, ID = ID, UUID = UUID) # Hand over parameters to parent class init        
        self.Bipartite = Bipartite   # For bipartite system graphs, a string with value 't' or 'd' for transformation and distribution process indicates which group the process belongs to.
        self.Extensions= Extensions  # Dictionary of     
        self.Graphical = Graphical   # # Dictionary of graphical properties: xPos = None, yPos = None, Orientation = None, Color=None, Width = None, Height=None, 
        
    def add_extension(self,Time = None, Name = None, Value=None, Unit = None, Uncert=None): # Extensions flows that are not part of the system-wide mass balance!
        if self.Extensions is None:
            self.Extensions = []
        self.Extensions.append(Flow(P_Start = self.ID, P_End = None, Time = Time, Name = Name, Unit = Unit, Value = Value, Uncert = Uncert))
      
    def add_parameter(self,Name = None):
        if self.Parameters is None:
            self.Parameters = []
        self.Parameters.append(Parameter(Value = None))
            
class Flow(Obj): # Flow needs to at least have dimension time x element

    """
    Class with the definition and methods for a flow in ODYM
    """
    
    def __init__(self, Name = None, ID = None, UUID = None, P_Start = None, P_End = None, Indices = None, Values=None, Uncert=None, Unit = None, Color = None):
        """ Basic initialisation of a flow."""
        Obj.__init__(self, Name = Name, ID = ID, UUID = UUID) # Hand over parameters to parent class init
        self.P_Start     = P_Start # id of start process of flow (id: int)
        self.P_End       = P_End   # id of end process of flow (id: int)
        self.Indices     = Indices # String with indices as defined in IndexTable, separated by ,: 't,c,p,s,e'
        
        self.Values      = Values   # flow values, np.array, multidimensional, unit is system-wide unit
        self.Uncert      = Uncert  # uncertainty of value in %
        self.Unit        = Unit    # Unit string
        
        self.Color       = Color   # color as string 'R,G,B', where each of R, G, B has a value of 0...255



class Stock(Obj): # Flow needs to at least have dimension time x element

    """
    Class with the definition and methods for a stock in ODYM
    """
    
    def __init__(self, Name = None, ID = None, UUID = None, P_Res = None, Indices = None, Type = None, Values=None, Uncert=None, Unit = None, Color = None):
        """ Basic initialisation of a stock."""
        Obj.__init__(self, Name = Name, ID = ID, UUID = UUID) # Hand over parameters to parent class init
        self.P_Res       = P_Res   # id of process where stock resides (id: int)
        self.Indices     = Indices # String with indices as defined in IndexTable, separated by ,: 't,c,p,s,e'
        self.Type        = Type  # Type is an int value, indicating: 0: stock, 1: (net) stock change or addition to stock, 2: removal from stock
        
        self.Values      = Values  # flow values, np.array, multidimensional, unit is system-wide unit
        self.Uncert      = Uncert  # uncertainty of value in %
        self.Unit        = Unit    # Unit string

        self.Color       = Color   # color as string 'R,G,B', where each of R, G, B has a value of 0...255


class Parameter(Obj):
  
    """
    Class with the definition and methods for parameters
    """
    
    def __init__(self, Name = None, ID = None, UUID = None, P_Res = None, MetaData = None, Indices = None, Values=None, Uncert=None, Unit = None):
        """ Basic initialisation of a parameter."""
        Obj.__init__(self, Name = Name, ID = ID, UUID = UUID) # Hand over parameters to parent class init
        self.P_Res       = P_Res   # id of process to which parameter is assigned (id: int)
        self.Indices     = Indices # String with indices as defined in IndexTable, separated by ,: 't,c,p,s,e'
        self.MetaData    = MetaData # Dictionary with additional metadata
        
        self.Values      = Values   # parameter values, np.array, multidimensional, unit is Unit
        self.Uncert      = Uncert  # uncertainty of value in %
        self.Unit        = Unit   # Unit of parameter values

  
       



        
#   
#
#    