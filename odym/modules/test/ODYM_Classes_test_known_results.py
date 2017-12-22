# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 16:19:39 2014

@authors: Stefan Pauliuk, Uni Freiburg, Germany
"""
import os
import sys
# Put location of 
sys.path.insert(0,  os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\..')) + '\\modules') # add ODYM module directory to system path
#NOTE: Hidden variable __file__ must be know to script for the directory structure to work.
# Therefore: When first using the model, run the entire script with F5 so that the __file__ variable can be created.

import ODYM_Classes as msc # import the ODYM class file
import ODYM_Functions as msf # import the ODYM function file
import numpy as np
import unittest
import pandas as pd


###############################################################################
# Test 1) A simple MFA system with 5 years and 1 chemical element
###############################################################################
# Define results
MyMFA_Test1_Flowshape1 = (5,2) # shape of a flow in system defined below.
F_0_1_Values1          = np.array([[1,1],[0,0],[2,2],[1,1],[4,4]]) # Define some arbitrary inflow data for each year and element
F_1_2_Values1          = np.array([[1,1],[1,1],[32,32],[1,1],[4,4]]) # 
F_2_1_Values1          = np.array([[0,0],[1,1],[30,30],[0,0],[0,0]]) # Define flow back to process 1, make sure mass balance holds.
F_2_0_Values1          = F_0_1_Values1.copy()  # outflow equals inflow as no stocks are present
Bal_Test1              = np.zeros((5,3,2))

# Define dynamic MFA model and fill in values
"""Create Dynamic MFA Models and hand over the pre-defined values."""
# Define a basic classification with 5 years, 1 element, and unity. 'Time' and 'Element' must be present!
ModelClassification_Test1 = {} 
ModelClassification_Test1['Unity']    = msc.Classification(Name = 'Unity',         Dimension = 'Unity',   Items = [1])
ModelClassification_Test1['Time']     = msc.Classification(Name = 'Time',          Dimension = 'Time',    Items = [2010,2011,2012,2013,2014])
ModelClassification_Test1['Element'] = msc.Classification(Name = 'Chem_Elements', Dimension = 'Element', Items = ['All','Fe'])

#extract start and end year
Model_Time_Start = min(ModelClassification_Test1['Time'].Items)
Model_Time_End   = max(ModelClassification_Test1['Time'].Items)

#Define model aspects in right order
Model_Aspects = ['Time','Element','Unity'] # aspects of the model to be considered. Must be the same as the items of the ModelClassification_Test1 dictionary
# Define a simple index table with the three aspects time, element, and unity, using the modelclassification above.
IndexTable = pd.DataFrame({'Aspect'        : Model_Aspects, # 'Time' and 'Element' must be present!
                           'Description'   : ['Time','Element','Unity'],
                           'Dimension'     : ['Time','Element','Unity'], # must be the same as 'Dimenstion' in the classification above
                           'Classification': [ModelClassification_Test1[Aspect] for Aspect in Model_Aspects],
                           'IndexLetter'   : ['t','e','i']}) # Unique one letter (upper or lower case) indices to be used later for calculations. t for time, e for element

IndexTable.set_index('Aspect', inplace = True) # Default indexing of IndexTable, other indices are produced on the fly

# Initialize MFA system
MyMFA_Test1 = msc.MFAsystem(Name = 'TestSystem', 
                      Geogr_Scope = 'World', 
                      Unit = 'Mt', 
                      ProcessList = [], 
                      FlowDict = {}, 
                      StockDict = {},
                      ParameterDict = None, 
                      Time_Start = Model_Time_Start, 
                      Time_End = Model_Time_End, 
                      IndexTable = IndexTable, 
                      Elements = IndexTable.ix['Element'].Classification.Items) 
                      
# Add 2 processes to system
PrL_Name   = ['Environment','Process_1','Process_2']
PrL_Number = [0,1,2]
for m in range(0, len(PrL_Name)):
    MyMFA_Test1.ProcessList.append(msc.Process(Name = PrL_Name[m], ID   = PrL_Number[m]))
    
# Define 4 flows by symbol and names
MyMFA_Test1.FlowDict['F_0_1'] = msc.Flow(Name = 'Input'             , P_Start = 0, P_End = 1, Indices = 't,e', Values=None, Uncert=None)
MyMFA_Test1.FlowDict['F_1_2'] = msc.Flow(Name = 'Processed input'   , P_Start = 1, P_End = 2, Indices = 't,e', Values=None, Uncert=None)
MyMFA_Test1.FlowDict['F_2_1'] = msc.Flow(Name = 'Sent back to 1'    , P_Start = 2, P_End = 1, Indices = 't,e', Values=None, Uncert=None)
MyMFA_Test1.FlowDict['F_2_0'] = msc.Flow(Name = 'Output'            , P_Start = 2, P_End = 0, Indices = 't,e', Values=None, Uncert=None)

MyMFA_Test1.Initialize_FlowValues() # Assign empty arrays to flows according to dimensions specified above

# Assign values to flows, manually: This prodecure mimicks the calculation of results by solving the model equations
MyMFA_Test1.FlowDict['F_0_1'].Values = F_0_1_Values1
MyMFA_Test1.FlowDict['F_1_2'].Values = F_1_2_Values1
MyMFA_Test1.FlowDict['F_2_1'].Values = F_2_1_Values1
MyMFA_Test1.FlowDict['F_2_0'].Values = F_2_0_Values1

Bal = MyMFA_Test1.MassBalance() # Determine Mass Balance    

###############################################################################
# Tests
###############################################################################

class KnownResultsTestCase(unittest.TestCase):

    # For MyMFA_Test1:
    def test_Dimensions_MyMFA_Test1(self):
        """Test Inflow Driven Model with Fixed product lifetime."""
        np.testing.assert_array_equal(MyMFA_Test1.FlowDict['F_1_2'].Values.shape[0],MyMFA_Test1_Flowshape1[0])
        np.testing.assert_array_equal(MyMFA_Test1.FlowDict['F_1_2'].Values.shape[1],MyMFA_Test1_Flowshape1[1])
        np.testing.assert_array_equal(MyMFA_Test1.MassBalance(),Bal_Test1)
           



    if __name__ == '__main__':
        unittest.main()
