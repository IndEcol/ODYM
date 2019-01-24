# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 16:19:39 2014

"""
import os
import sys
import imp
# Put location of 
sys.path.insert(0,  os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\..')) + '\\modules') # add ODYM module directory to system path
#NOTE: Hidden variable __file__ must be know to script for the directory structure to work.
# Therefore: When first using the model, run the entire script with F5 so that the __file__ variable can be created.

import dynamic_stock_model as dsm # remove and import the class manually if this unit test is run as standalone script
imp.reload(dsm)

import numpy as np
import unittest


###############################################################################
"""My Input for fixed lifetime"""
Time_T_FixedLT = np.arange(0,10)
Inflow_T_FixedLT  = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
lifetime_FixedLT  = {'Type': 'Fixed', 'Mean': np.array([5])}
lifetime_FixedLT0 = {'Type': 'Fixed', 'Mean': np.array([0])}
#lifetime_FixedLT = {'Type': 'Fixed', 'Mean': np.array([5,5,5,5,5,5,5,5,5,5])}
lifetime_NormLT  = {'Type': 'Normal', 'Mean': np.array([5]), 'StdDev': np.array([1.5])}
lifetime_NormLT0 = {'Type': 'Normal', 'Mean': np.array([0]), 'StdDev': np.array([1.5])}
###############################################################################
"""My Output for fixed lifetime"""
Outflow_T_FixedLT = np.array([0, 0, 0, 0, 0, 1, 2, 3, 4, 5])

Outflow_TC_FixedLT = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 4, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 5, 0, 0, 0, 0, 0]])

Stock_T_FixedLT = np.array([1, 3, 6, 10, 15, 20, 25, 30, 35, 40])

StockChange_T_FixedLT = np.array([1, 2, 3, 4, 5, 5, 5, 5, 5, 5])

Stock_TC_FixedLT = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [1, 2, 0, 0, 0, 0, 0, 0, 0, 0],
                             [1, 2, 3, 0, 0, 0, 0, 0, 0, 0],
                             [1, 2, 3, 4, 0, 0, 0, 0, 0, 0],
                             [1, 2, 3, 4, 5, 0, 0, 0, 0, 0],
                             [0, 2, 3, 4, 5, 6, 0, 0, 0, 0],
                             [0, 0, 3, 4, 5, 6, 7, 0, 0, 0],
                             [0, 0, 0, 4, 5, 6, 7, 8, 0, 0],
                             [0, 0, 0, 0, 5, 6, 7, 8, 9, 0],
                             [0, 0, 0, 0, 0, 6, 7, 8, 9, 10]])

Bal = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
"""My Output for normally distributed lifetime"""

Stock_TC_NormLT = np.array([[  9.99570940e-01,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00],
       [  9.96169619e-01,   1.99914188e+00,   0.00000000e+00,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00],
       [  9.77249868e-01,   1.99233924e+00,   2.99871282e+00,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00],
       [  9.08788780e-01,   1.95449974e+00,   2.98850886e+00,
          3.99828376e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00],
       [  7.47507462e-01,   1.81757756e+00,   2.93174960e+00,
          3.98467848e+00,   4.99785470e+00,   0.00000000e+00,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00],
       [  5.00000000e-01,   1.49501492e+00,   2.72636634e+00,
          3.90899947e+00,   4.98084810e+00,   5.99742564e+00,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00],
       [  2.52492538e-01,   1.00000000e+00,   2.24252239e+00,
          3.63515512e+00,   4.88624934e+00,   5.97701772e+00,
          6.99699658e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00],
       [  9.12112197e-02,   5.04985075e-01,   1.50000000e+00,
          2.99002985e+00,   4.54394390e+00,   5.86349921e+00,
          6.97318734e+00,   7.99656752e+00,   0.00000000e+00,
          0.00000000e+00],
       [  2.27501319e-02,   1.82422439e-01,   7.57477613e-01,
          2.00000000e+00,   3.73753731e+00,   5.45273268e+00,
          6.84074908e+00,   7.96935696e+00,   8.99613846e+00,
          0.00000000e+00],
       [  3.83038057e-03,   4.55002639e-02,   2.73633659e-01,
          1.00997015e+00,   2.50000000e+00,   4.48504477e+00,
          6.36152146e+00,   7.81799894e+00,   8.96552657e+00,
          9.99570940e+00]])

Stock_T_NormLT = np.array([  0.99957094,   2.9953115 ,   5.96830193,   9.85008113,
        14.4793678 ,  19.60865447,  24.99043368,  30.46342411,
        35.95916467,  41.45873561])

Outflow_T_NormLT = np.array([  4.29060333e-04,   4.25944090e-03,   2.70095728e-02,
         1.18220793e-01,   3.70713330e-01,   8.70713330e-01,
         1.61822079e+00,   2.52700957e+00,   3.50425944e+00,
         4.50042906e+00])

Outflow_TC_NormLT = np.array([[  4.29060333e-04,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00],
       [  3.40132023e-03,   8.58120666e-04,  -0.00000000e+00,
         -0.00000000e+00,  -0.00000000e+00,  -0.00000000e+00,
         -0.00000000e+00,  -0.00000000e+00,  -0.00000000e+00,
         -0.00000000e+00],
       [  1.89197514e-02,   6.80264047e-03,   1.28718100e-03,
         -0.00000000e+00,  -0.00000000e+00,  -0.00000000e+00,
         -0.00000000e+00,  -0.00000000e+00,  -0.00000000e+00,
         -0.00000000e+00],
       [  6.84610878e-02,   3.78395028e-02,   1.02039607e-02,
          1.71624133e-03,  -0.00000000e+00,  -0.00000000e+00,
         -0.00000000e+00,  -0.00000000e+00,  -0.00000000e+00,
         -0.00000000e+00],
       [  1.61281318e-01,   1.36922176e-01,   5.67592541e-02,
          1.36052809e-02,   2.14530167e-03,  -0.00000000e+00,
         -0.00000000e+00,  -0.00000000e+00,  -0.00000000e+00,
         -0.00000000e+00],
       [  2.47507462e-01,   3.22562636e-01,   2.05383263e-01,
          7.56790055e-02,   1.70066012e-02,   2.57436200e-03,
         -0.00000000e+00,  -0.00000000e+00,  -0.00000000e+00,
         -0.00000000e+00],
       [  2.47507462e-01,   4.95014925e-01,   4.83843953e-01,
          2.73844351e-01,   9.45987569e-02,   2.04079214e-02,
          3.00342233e-03,  -0.00000000e+00,  -0.00000000e+00,
         -0.00000000e+00],
       [  1.61281318e-01,   4.95014925e-01,   7.42522387e-01,
          6.45125271e-01,   3.42305439e-01,   1.13518508e-01,
          2.38092416e-02,   3.43248267e-03,  -0.00000000e+00,
         -0.00000000e+00],
       [  6.84610878e-02,   3.22562636e-01,   7.42522387e-01,
          9.90029850e-01,   8.06406589e-01,   4.10766527e-01,
          1.32438260e-01,   2.72105619e-02,   3.86154300e-03,
         -0.00000000e+00],
       [  1.89197514e-02,   1.36922176e-01,   4.83843953e-01,
          9.90029850e-01,   1.23753731e+00,   9.67687907e-01,
          4.79227614e-01,   1.51358011e-01,   3.06118821e-02,
          4.29060333e-03]])

StockChange_T_NormLT = np.array([ 0.99957094,  1.99574056,  2.97299043,  3.88177921,  4.62928667,
        5.12928667,  5.38177921,  5.47299043,  5.49574056,  5.49957094])

"""My Output for Weibull-distributed lifetime"""

Stock_TC_WeibullLT = np.array([[1, 0,  0,  0,  0,  0,  0, 0, 0,  0],  # computed with Excel and taken from there
                             [0.367879441,	2,	0,	0,	0,	0,	0,	0,	0,	0],
                             [0.100520187,	0.735758882,	3,	0,	0,	0,	0,	0,	0,	0],
                            [0.023820879,	0.201040373,	1.103638324,	4,	0,	0,	0,	0,	0,	0],
                            [0.005102464,	0.047641758,	0.30156056,	1.471517765,5,	0,	0,	0,	0,	0],
                            [0.001009149,	0.010204929,	0.071462637,	0.402080746,1.839397206,	6,	0,	0,	0,	0],
                            [0.000186736,	0.002018297,	0.015307393,	0.095283516,	0.502600933,	2.207276647,	7,	0,	0,	0],
                            [3.26256E-05,	0.000373472,	0.003027446,	0.020409858,	0.119104394,	0.60312112,	2.575156088,	8,	0,	0],
                            [5.41828E-06,	6.52513E-05,	0.000560208,	0.004036594,	0.025512322,	0.142925273,	0.703641306,	2.943035529,	9,	0],
                            [8.59762E-07,	1.08366E-05,	9.78769E-05,	0.000746944,	0.005045743,	0.030614786,	0.166746152,	0.804161493,	3.310914971,	10]])

Stock_T_WeibullLT = np.array([1,2.367879441,3.836279069,5.328499576,6.825822547,8.324154666,9.822673522,11.321225,12.8197819,14.31833966])

Outflow_T_WeibullLT = np.array([0,0.632120559,1.531600372,2.507779493,3.502677029,4.50166788,5.501481144,6.501448519,7.5014431,8.501442241])

Outflow_TC_WeibullLT = np.array([[0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
                                [0.632120559,	0,	0,	0,	0,	0,	0,	0,	0,	0],
                                [0.267359255,	1.264241118,	0,	0,	0,	0,	0,	0,	0,	0],
                                [0.076699308,	0.534718509,	1.896361676,	0,	0,	0,	0,	0,	0,	0],
                                [0.018718414,	0.153398615,	0.802077764,	2.528482235,	0,	0,	0,	0,	0,	0],
                                [0.004093316,	0.037436829,	0.230097923,	1.069437018,	3.160602794,	0,	0,	0,	0,	0],
                                [0.000822413,	0.008186632,	0.056155243,	0.306797231,	1.336796273,	3.792723353,	0,	0,	0,	0],
                                [0.00015411,	0.001644825,	0.012279947,	0.074873658,	0.383496539,	1.604155527,	4.424843912,	0,	0,	0],
                                [2.72074E-05,	0.000308221,	0.002467238,	0.016373263,	0.093592072,	0.460195846,	1.871514782,	5.056964471,	0,	0],
                                [4.55852E-06, 5.44147E-05	,     0.000462331	,     0.00328965,   	0.020466579,	0.112310487,	0.536895154,	2.138874037,	5.689085029,	0]])

StockChange_T_WeibullLT = np.array([1,1.367879441,1.468399628,1.492220507,1.497322971,1.49833212,1.498518856,1.498551481,1.4985569,1.498557759])

lifetime_WeibullLT = {'Type': 'Weibull', 'Shape': np.array([1.2]), 'Scale': np.array([1])}
InitialStock_WB = np.array([0.01, 0.01, 0.08, 0.2,  0.2,  2,  2,  3,  4,  7.50])
Inflow_WB = np.array([11631.1250671964,	1845.6048709861,	2452.0593141014,	1071.0305279511,	198.1868742385,	391.9674590243,	83.9599583940,	29.8447516023,	10.8731273138,	7.5000000000])
# We need 10 digits AFTER the . to get a 9 digits after the . overlap with np.testing.
# The total number of counting digits is higher, because there are up to 5 digits before the .

# For the stock-driven model with initial stock, colculated with Excel
Sc_InitialStock_2_Ref = np.array([[ 3.29968072,  0.        ,  0.        ,  0.        ,  0.        ,
         0.        ,  0.        ,  0.        ,  0.        ],
       [ 3.28845263,  5.1142035 ,  0.        ,  0.        ,  0.        ,
         0.        ,  0.        ,  0.        ,  0.        ],
       [ 3.2259967 ,  5.09680099,  2.0068288 ,  0.        ,  0.        ,
         0.        ,  0.        ,  0.        ,  0.        ],
       [ 3.        ,  5.        ,  2.        ,  4.        ,  0.        ,
         0.        ,  0.        ,  0.        ,  0.        ],
       [ 2.46759471,  4.64972578,  1.962015  ,  3.98638888,  4.93427563,
         0.        ,  0.        ,  0.        ,  0.        ],
       [ 1.65054855,  3.82454624,  1.82456634,  3.91067739,  4.91748538,
         3.8721761 ,  0.        ,  0.        ,  0.        ],
       [ 0.83350238,  2.55819937,  1.50076342,  3.63671549,  4.82409004,
         3.85899993,  2.78772936,  0.        ,  0.        ],
       [ 0.30109709,  1.2918525 ,  1.00384511,  2.9913133 ,  4.48613916,
         3.78570788,  2.77824333,  3.36180162,  0.        ],
       [ 0.07510039,  0.46667297,  0.5069268 ,  2.00085849,  3.68999109,
         3.5205007 ,  2.72547754,  3.35036215,  3.66410986]])

Sc_InitialStock_2_Ref_Sum = np.array([  3.29968072,   8.40265614,  10.32962649,  14.        ,
        18.        ,  20.        ,  20.        ,  20.        ,  20.        ])

Oc_InitialStock_2_Ref = np.array([[  1.41636982e-03,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
       [  1.12280883e-02,   2.19524375e-03,  -0.00000000e+00,
         -0.00000000e+00,  -0.00000000e+00,  -0.00000000e+00,
         -0.00000000e+00,  -0.00000000e+00,  -0.00000000e+00],
       [  6.24559363e-02,   1.74025106e-02,   8.61420234e-04,
         -0.00000000e+00,  -0.00000000e+00,  -0.00000000e+00,
         -0.00000000e+00,  -0.00000000e+00,  -0.00000000e+00],
       [  2.25996698e-01,   9.68009922e-02,   6.82879736e-03,
          1.71697802e-03,  -0.00000000e+00,  -0.00000000e+00,
         -0.00000000e+00,  -0.00000000e+00,  -0.00000000e+00],
       [  5.32405289e-01,   3.50274224e-01,   3.79849998e-02,
          1.36111209e-02,   2.11801070e-03,  -0.00000000e+00,
         -0.00000000e+00,  -0.00000000e+00,  -0.00000000e+00],
       [  8.17046165e-01,   8.25179532e-01,   1.37448656e-01,
          7.57114903e-02,   1.67902556e-02,   1.66211031e-03,
         -0.00000000e+00,  -0.00000000e+00,  -0.00000000e+00],
       [  8.17046165e-01,   1.26634687e+00,   3.23802924e-01,
          2.73961897e-01,   9.33953405e-02,   1.31761643e-02,
          1.19661751e-03,  -0.00000000e+00,  -0.00000000e+00],
       [  5.32405289e-01,   1.26634687e+00,   4.96918311e-01,
          6.45402188e-01,   3.37950879e-01,   7.32920558e-02,
          9.48603036e-03,   1.44303487e-03,  -0.00000000e+00],
       [  2.25996698e-01,   8.25179532e-01,   4.96918311e-01,
          9.90454815e-01,   7.96148072e-01,   2.65207178e-01,
          5.27657861e-02,   1.14394721e-02,   1.57279902e-03]])

I_InitialStock_2_Ref  = np.array([ 3.30109709,  5.11639875,  2.00769022,  4.00171698,  4.93639364,  3.87383821,  2.78892598,  3.36324466,  3.66568266])

""" Test case with fixed lifetime for initial stock"""
Time_T_FixedLT_X = np.arange(1, 9, 1)
lifetime_FixedLT_X = {'Type': 'Fixed', 'Mean': np.array([5])}
InitialStock_X = np.array([0, 0, 0, 7, 5, 4, 3, 2])
Inflow_X = np.array([0, 0, 0, 7, 5, 4, 3, 2])

Time_T_FixedLT_XX = np.arange(1, 11, 1)
lifetime_NormLT_X = {'Type': 'Normal', 'Mean': np.array([5]), 'StdDev': np.array([1.5])}
InitialStock_XX = np.array([0.01, 0.01, 0.08, 0.2,  0.2,  2,  2,  3,  4,  7.50])
Inflow_XX = np.array([ 2.61070664,  0.43955789,  0.87708508,  0.79210262,  0.4,
        2.67555857,  2.20073139,  3.06983925,  4.01538044,  7.50321933])

""" Test case with normally distributed lifetime for initial stock and stock-driven model"""
Time_T_FixedLT_2  = np.arange(1, 10, 1)
lifetime_NormLT_2 = {'Type': 'Normal', 'Mean': np.array([5]), 'StdDev': np.array([1.5])}
InitialStock_2    = np.array([3,5,2,4])
FutureStock_2     = np.array([0,0,0,0,18,20,20,20,20])
ThisSwitchTime    = 5 # First year with future stock curve, start counting from 1.
Inflow_2          = np.array([3.541625588,	5.227890554,2.01531097,4])

###############################################################################
"""Create Dynamic Stock Models and hand over the pre-defined values."""
# For zero lifetime: border case
myDSM0 = dsm.DynamicStockModel(t=Time_T_FixedLT, i=Inflow_T_FixedLT, lt=lifetime_FixedLT0)

# For fixed LT
myDSM = dsm.DynamicStockModel(t=Time_T_FixedLT, i=Inflow_T_FixedLT, lt=lifetime_FixedLT)

myDSM2 = dsm.DynamicStockModel(t=Time_T_FixedLT, s=Stock_T_FixedLT, lt=lifetime_FixedLT)

myDSMx = dsm.DynamicStockModel(t=Time_T_FixedLT_X, lt=lifetime_FixedLT_X)
TestInflow_X = myDSMx.compute_i_from_s(InitialStock=InitialStock_X)

myDSMxy = dsm.DynamicStockModel(t=Time_T_FixedLT_X, i=TestInflow_X, lt=lifetime_FixedLT_X)

# For zero normally distributed lifetime: border case
myDSM0n = dsm.DynamicStockModel(t=Time_T_FixedLT, i=Inflow_T_FixedLT, lt=lifetime_NormLT0)

# For normally distributed Lt
myDSM3 = dsm.DynamicStockModel(t=Time_T_FixedLT, i=Inflow_T_FixedLT, lt=lifetime_NormLT)

myDSM4 = dsm.DynamicStockModel(t=Time_T_FixedLT, s=Stock_T_NormLT, lt=lifetime_NormLT)

myDSMX = dsm.DynamicStockModel(t=Time_T_FixedLT_XX, lt=lifetime_NormLT_X)
TestInflow_XX = myDSMX.compute_i_from_s(InitialStock=InitialStock_XX)

myDSMXY = dsm.DynamicStockModel(t=Time_T_FixedLT_XX, i=TestInflow_XX, lt=lifetime_NormLT_X)

# Test compute_stock_driven_model_initialstock:
TestDSM_IntitialStock = dsm.DynamicStockModel(t=Time_T_FixedLT_2, s=FutureStock_2, lt=lifetime_NormLT_2)
Sc_InitialStock_2,Oc_InitialStock_2,I_InitialStock_2 = TestDSM_IntitialStock.compute_stock_driven_model_initialstock(InitialStock = InitialStock_2, SwitchTime = ThisSwitchTime)
# Compute stock back from inflow
TestDSM_IntitialStock_Verify = dsm.DynamicStockModel(t=Time_T_FixedLT_2, i=I_InitialStock_2, lt=lifetime_NormLT_2)
Sc_Stock_2 = TestDSM_IntitialStock_Verify.compute_s_c_inflow_driven()
Sc_Stock_2_Sum = Sc_Stock_2.sum(axis =1)
Sc_Stock_Sum   = TestDSM_IntitialStock_Verify.compute_stock_total()
Sc_Outflow_t_c = TestDSM_IntitialStock_Verify.compute_o_c_from_s_c()

# For Weibull-distributed Lt
myDSMWB1 = dsm.DynamicStockModel(t=Time_T_FixedLT, i=Inflow_T_FixedLT, lt=lifetime_WeibullLT)

myDSMWB2 = dsm.DynamicStockModel(t=Time_T_FixedLT, s=Stock_T_WeibullLT, lt=lifetime_WeibullLT)

myDSMWB3 = dsm.DynamicStockModel(t=Time_T_FixedLT_XX, lt=lifetime_WeibullLT)
TestInflow_WB = myDSMWB3.compute_i_from_s(InitialStock=InitialStock_XX)

myDSMWB4 = dsm.DynamicStockModel(t=Time_T_FixedLT_XX, i=TestInflow_WB, lt=lifetime_WeibullLT)
# Compute full stock model in correct order
###############################################################################
"""Unit Test Class"""


class KnownResultsTestCase(unittest.TestCase):

    def test_inflow_driven_model_fixedLifetime_0(self):
        """Test Inflow Driven Model with Fixed product lifetime of 0."""
        np.testing.assert_array_equal(myDSM0.compute_s_c_inflow_driven(), np.zeros(Stock_TC_FixedLT.shape))
        np.testing.assert_array_equal(myDSM0.compute_stock_total(), np.zeros((Stock_TC_FixedLT.shape[0])))
        np.testing.assert_array_equal(myDSM0.compute_stock_change(), np.zeros((Stock_TC_FixedLT.shape[0])))
        np.testing.assert_array_equal(myDSM0.compute_outflow_mb(), Inflow_T_FixedLT)
        np.testing.assert_array_equal(myDSM0.check_stock_balance(), Bal.transpose())
    
    
    def test_inflow_driven_model_fixedLifetime(self):
        """Test Inflow Driven Model with Fixed product lifetime."""
        np.testing.assert_array_equal(myDSM.compute_s_c_inflow_driven(), Stock_TC_FixedLT)
        np.testing.assert_array_equal(myDSM.compute_stock_total(),Stock_T_FixedLT)
        np.testing.assert_array_equal(myDSM.compute_o_c_from_s_c(), Outflow_TC_FixedLT)
        np.testing.assert_array_equal(myDSM.compute_outflow_total(), Outflow_T_FixedLT)
        np.testing.assert_array_equal(myDSM.compute_stock_change(), StockChange_T_FixedLT)
        np.testing.assert_array_equal(myDSM.check_stock_balance(), Bal.transpose())

    def test_stock_driven_model_fixedLifetime(self):
        """Test Stock Driven Model with Fixed product lifetime."""
        np.testing.assert_array_equal(myDSM2.compute_stock_driven_model()[0], Stock_TC_FixedLT)
        np.testing.assert_array_equal(myDSM2.compute_stock_driven_model()[1], Outflow_TC_FixedLT)
        np.testing.assert_array_equal(myDSM2.compute_stock_driven_model()[2], Inflow_T_FixedLT)
        np.testing.assert_array_equal(myDSM2.compute_outflow_total(), Outflow_T_FixedLT)
        np.testing.assert_array_equal(myDSM2.compute_stock_change(), StockChange_T_FixedLT)
        np.testing.assert_array_equal(myDSM2.check_stock_balance(), Bal.transpose())
        
    def test_inflow_driven_model_normallyDistrLifetime_0(self):
        """Test Inflow Driven Model with Fixed product lifetime of 0."""
        np.testing.assert_array_equal(myDSM0n.compute_s_c_inflow_driven(), np.zeros(Stock_TC_FixedLT.shape))
        np.testing.assert_array_equal(myDSM0n.compute_stock_total(), np.zeros((Stock_TC_FixedLT.shape[0])))
        np.testing.assert_array_equal(myDSM0n.compute_stock_change(), np.zeros((Stock_TC_FixedLT.shape[0])))
        np.testing.assert_array_equal(myDSM0n.compute_outflow_mb(), Inflow_T_FixedLT)
        np.testing.assert_array_equal(myDSM0n.check_stock_balance(), Bal.transpose())
            
    def test_inflow_driven_model_normallyDistLifetime(self):
        """Test Inflow Driven Model with normally distributed product lifetime."""
        np.testing.assert_array_almost_equal(myDSM3.compute_s_c_inflow_driven(), Stock_TC_NormLT, 8)
        np.testing.assert_array_almost_equal(myDSM3.compute_stock_total(), Stock_T_NormLT, 8)
        np.testing.assert_array_almost_equal(myDSM3.compute_o_c_from_s_c(), Outflow_TC_NormLT, 8)
        np.testing.assert_array_almost_equal(myDSM3.compute_outflow_total(), Outflow_T_NormLT, 8)
        np.testing.assert_array_almost_equal(myDSM3.compute_stock_change(), StockChange_T_NormLT, 8)
        np.testing.assert_array_almost_equal(myDSM3.check_stock_balance(), Bal.transpose(), 12)

    def test_stock_driven_model_normallyDistLifetime(self):
        """Test Stock Driven Model with normally distributed product lifetime."""
        np.testing.assert_array_almost_equal(
            myDSM4.compute_stock_driven_model()[0], Stock_TC_NormLT, 8)
        np.testing.assert_array_almost_equal(
            myDSM4.compute_stock_driven_model()[1], Outflow_TC_NormLT, 8)
        np.testing.assert_array_almost_equal(
            myDSM4.compute_stock_driven_model()[2], Inflow_T_FixedLT, 8)
        np.testing.assert_array_almost_equal(myDSM4.compute_outflow_total(), Outflow_T_NormLT, 8)
        np.testing.assert_array_almost_equal(
            myDSM4.compute_stock_change(), StockChange_T_NormLT, 8)
        np.testing.assert_array_almost_equal(myDSM4.check_stock_balance(), Bal.transpose(), 12)

    def test_inflow_driven_model_WeibullDistLifetime(self):
        """Test Inflow Driven Model with Weibull-distributed product lifetime."""
        np.testing.assert_array_almost_equal(
            myDSMWB1.compute_s_c_inflow_driven(), Stock_TC_WeibullLT, 9)
        np.testing.assert_array_almost_equal(myDSMWB1.compute_stock_total(), Stock_T_WeibullLT, 8)
        np.testing.assert_array_almost_equal(myDSMWB1.compute_o_c_from_s_c(), Outflow_TC_WeibullLT, 9)
        np.testing.assert_array_almost_equal(myDSMWB1.compute_outflow_total(), Outflow_T_WeibullLT, 9)
        np.testing.assert_array_almost_equal(
            myDSMWB1.compute_stock_change(), StockChange_T_WeibullLT, 9)
        np.testing.assert_array_almost_equal(myDSMWB1.check_stock_balance(), Bal.transpose(), 12)

    def test_stock_driven_model_WeibullDistLifetime(self):
        """Test Stock Driven Model with Weibull-distributed product lifetime."""
        np.testing.assert_array_almost_equal(
            myDSMWB1.compute_stock_driven_model()[0], Stock_TC_WeibullLT, 8)
        np.testing.assert_array_almost_equal(
            myDSMWB1.compute_stock_driven_model()[1], Outflow_TC_WeibullLT, 8)
        np.testing.assert_array_almost_equal(
            myDSMWB1.compute_stock_driven_model()[2], Inflow_T_FixedLT, 8)
        np.testing.assert_array_almost_equal(myDSMWB1.compute_outflow_total(), Outflow_T_WeibullLT, 9)
        np.testing.assert_array_almost_equal(
            myDSMWB1.compute_stock_change(), StockChange_T_WeibullLT, 8)
        np.testing.assert_array_almost_equal(myDSMWB1.check_stock_balance(), Bal.transpose(), 12)


    def test_inflow_from_stock_fixedLifetime(self):
        """Test computation of inflow from stock with Fixed product lifetime."""
        np.testing.assert_array_equal(TestInflow_X, Inflow_X)
        np.testing.assert_array_equal(myDSMxy.compute_s_c_inflow_driven()[-1, :], InitialStock_X)

    def test_inflow_from_stock_normallyDistLifetime(self):
        """Test computation of inflow from stock with normally distributed product lifetime."""
        np.testing.assert_array_almost_equal(TestInflow_XX, Inflow_XX, 8)
        np.testing.assert_array_almost_equal(myDSMXY.compute_s_c_inflow_driven()[-1, :], InitialStock_XX, 9)
            
    def test_inflow_from_stock_WeibullDistLifetime(self):
        """Test computation of inflow from stock with Weibull-distributed product lifetime."""
        np.testing.assert_array_almost_equal(TestInflow_WB, Inflow_WB, 9) 
        np.testing.assert_array_almost_equal(myDSMWB4.compute_s_c_inflow_driven()[-1, :], InitialStock_WB, 9)     
        
    def test_compute_stock_driven_model_initialstock(self):
        """Test stock-driven model with initial stock given."""
        np.testing.assert_array_almost_equal(I_InitialStock_2, I_InitialStock_2_Ref, 8) 
        np.testing.assert_array_almost_equal(Sc_InitialStock_2, Sc_InitialStock_2_Ref, 8)
        np.testing.assert_array_almost_equal(Sc_InitialStock_2.sum(axis =1), Sc_InitialStock_2_Ref_Sum, 8)
        np.testing.assert_array_almost_equal(Oc_InitialStock_2, Oc_InitialStock_2_Ref, 8) 

    if __name__ == '__main__':
        unittest.main()

