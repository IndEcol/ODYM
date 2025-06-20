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

import ODYM_Classes as msc # import the ODYMM class file
import ODYM_Functions as msf # import the ODYM function file
import numpy as np
import unittest
import pandas as pd


###############################################################################
# Test 1) A simple MFA system with 5 years and 1 chemical element
###############################################################################
# Define results

# For TableWithFlowsToShares(Table,axis):

TSA = np.array([[1, 2, 1, 2, 4, 1],
                [1, 3, 0, 2, 4, 3],
                [0, 3, 4, 3, 1, 0],
                [1, 4, 3, 2, 1, 0]])

TSB = np.array([[0.333333,0.166667,0.125,0.222222,0.4,0.25],
[0.333333,0.25,0,0.222222,0.4,0.75],
[0,0.25,0.5,0.333333,0.1,0],
[0.333333,0.333333,0.375,0.222222,0.1,0]])

TSC = np.array([[0.0909091,0.181818,0.0909091,0.181818,0.363636,0.0909091],
[0.0769231,0.230769,0,0.153846,0.307692,0.230769],
[0,0.272727,0.363636,0.272727,0.0909091,0],
[0.0909091,0.363636,0.272727,0.181818,0.0909091,0]])

B = msf.TableWithFlowsToShares(TSA,axis=0)
C = msf.TableWithFlowsToShares(TSA,axis=1)

TSAx = np.array([[1, 2, 1, 0, 4, 1],
                 [1, 3, 0, 0, 4, 3],
                 [0, 3, 4, 0, 1, 0],
                 [1, 4, 3, 0, 1, 0]])

Bx = msf.TableWithFlowsToShares(TSAx,axis=0)
Cx = msf.TableWithFlowsToShares(TSAx,axis=1)

TSBx = np.array([[0.3333333333333333,0.1666666666666667,0.125,0,0.4,0.25],
[0.3333333333333333,0.25,0,0,0.4,0.75],
[0,0.25,0.5,0,0.1,0],
[0.3333333333333333,0.3333333333333333,0.375,0,0.1,0]])

TSCx = np.array([[0.1111111111111111,0.2222222222222222,0.1111111111111111,0,0.4444444444444444,0.1111111111111111],
[0.09090909090909091,0.2727272727272727,0,0,0.3636363636363636,0.2727272727272727],
[0,0.375,0.5,0,0.125,0],
[0.1111111111111111,0.4444444444444444,0.3333333333333333,0,0.1111111111111111,0]])

TSAy = np.array([[1, 2, 1, 2, 4, 1],
                 [1, 3, 0, 2, 4, 3],
                 [0, 3, 4, 3, 1, 0],
                 [0, 0, 0, 0, 0, 0]])

By = msf.TableWithFlowsToShares(TSAy,axis=0)
Cy = msf.TableWithFlowsToShares(TSAy,axis=1)

TSAzref = np.array([[0.5,0.25,0.2,0.2857142857142857,0.4444444444444444,0.25],
[0.5,0.375,0,0.2857142857142857,0.4444444444444444,0.75],
[0,0.375,0.8,0.4285714285714285,0.1111111111111111,0],
[0,0,0,0,0,0]])

TSBzref = np.array([[0.090909090909090911614143238,0.18181818181818182322828648,0.090909090909090911614143238,0.18181818181818182322828648,0.36363636363636364645657295,0.090909090909090911614143238],
[0.076923076923076927347011633,0.2307692307692307820410349,0,0.15384615384615385469402327,0.30769230769230770938804653,0.2307692307692307820410349],
[0,0.2727272727272727070868541,0.36363636363636364645657295,0.2727272727272727070868541,0.090909090909090911614143238,0],
[0,0,0,0,0,0]])

TSAz = np.zeros((4,6))
Bz = msf.TableWithFlowsToShares(TSAz,axis=0)
Cz = msf.TableWithFlowsToShares(TSAz,axis=1)


ELCTest1 = np.array([[3.59212,0,0,0.00922665,3.58289,0,0,0],
[0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0],
[0.173689,0,0.1719,0,0,0.00178926,0,0],
[0.0574175,0,0,0,0,0.0574175,0,0],
[0,0,0,0,0,0,0,0]])

ELCTest1res = np.array([[1,0,0,0.002568583066476976,0.9974314169335231,0,0,0],
[1,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,1],
[1,0,0.9896984994927148,0,0,0.01030150050728525,0,0],
[1,0,0,0,0,1,0,0],
[1,0,0,0,0,0,0,1]])

#A= msf.DetermineElementComposition_All_Oth(ELCTest1)


###############################################################################
# Tests
###############################################################################

class KnownResultsTestCase(unittest.TestCase):

    # For MyMFA_Test1:
    def test_ListStringToListNumbers(self):
        """Test the list string to list of numbers function."""
        np.testing.assert_array_equal(msf.ListStringToListNumbers('[1,2,3]'),[1,2,3])
           
    def test_MI_Tuple(self):
        """Test the MI_Tuple function."""
        np.testing.assert_array_equal(msf.MI_Tuple(10, [3,4,2,6]),[0,0,1,4])

    def test_TableWithFlowsToShares(self):
        """Test the TableWithFlowsToShares function."""
        np.testing.assert_array_almost_equal(msf.TableWithFlowsToShares(TSA,axis=0),TSB,6)
        np.testing.assert_array_almost_equal(msf.TableWithFlowsToShares(TSA,axis=1),TSC,6)
        np.testing.assert_array_almost_equal(msf.TableWithFlowsToShares(TSAx,axis=0),TSBx,16)
        np.testing.assert_array_almost_equal(msf.TableWithFlowsToShares(TSAx,axis=1),TSCx,16)
        np.testing.assert_array_almost_equal(msf.TableWithFlowsToShares(TSAy,axis=0),TSAzref,16)
        np.testing.assert_array_almost_equal(msf.TableWithFlowsToShares(TSAy,axis=1),TSBzref,26)
        np.testing.assert_array_equal(msf.TableWithFlowsToShares(TSAz,axis=0),np.zeros((4,6)))
        np.testing.assert_array_equal(msf.TableWithFlowsToShares(TSAz,axis=1),np.zeros((4,6)))
    
    def test_DetermineElementComposition_All_Oth(self):
        """Test the DetermineElementComposition_All_Oth function."""
        np.testing.assert_array_almost_equal(msf.DetermineElementComposition_All_Oth(ELCTest1),ELCTest1res,16)
        
    
    if __name__ == '__main__':
        unittest.main()
