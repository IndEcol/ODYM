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

# 

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


    if __name__ == '__main__':
        unittest.main()
