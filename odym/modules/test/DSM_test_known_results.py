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
import scipy


###############################################################################
"""My Input for fixed lifetime"""
Time_T_FixedLT = np.arange(0,10)
Time_T_30      = np.arange(0,30)
Inflow_T_FixedLT  = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
lifetime_FixedLT  = {'Type': 'Fixed', 'Mean': np.array([5])}
lifetime_FixedLT0 = {'Type': 'Fixed', 'Mean': np.array([0])}
#lifetime_FixedLT = {'Type': 'Fixed', 'Mean': np.array([5,5,5,5,5,5,5,5,5,5])}
lifetime_NormLT  = {'Type': 'Normal', 'Mean': np.array([5]), 'StdDev': np.array([1.5])}
lifetime_NormLT0 = {'Type': 'Normal', 'Mean': np.array([0]), 'StdDev': np.array([1.5])}
lifetime_NormLT8 = {'Type': 'Normal', 'Mean': np.array([8]), 'StdDev': np.array([3])}
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

Bal    = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
Bal9   = np.zeros((9))
Bal30  = np.zeros((30))
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

Stock_SDM_NegInflow_NormLT    = np.array([0.0,0,1,2,3,5,6,8,8,6,6,6,6,6,8,8,8,9,10,12,9,9,9,9,9,9,9,9.0,9,9])
Stock_SDM_NegInflow_NormLTNeg = np.array([0.0,0,0,0,0,0,0,0,8,6,6,6,6,6,3,3,3,3,4,5,6,7,8,9,9,9,7.1,8,8.0,8])
Stock_SDM_PosInflow_NormLTNeg = np.array([0.0,0,0,0,0,0,0,0,8,8,8,8.2,9,9,8.5,8,7.5,7,6.5,6,5.5,7,8,9,8.8,8.5,8.1,8,8.0,8])

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
Time_T_FixedLT_3  = np.arange(0, 30, 1)
lifetime_NormLT_2 = {'Type': 'Normal', 'Mean': np.array([5]), 'StdDev': np.array([1.5])}
lifetime_NormLT_3 = {'Type': 'LogNormal', 'Mean': np.array([6]), 'StdDev': np.array([3])}
lifetime_NormLT_4 = {'Type': 'Normal', 'Mean': np.array([7]), 'StdDev': np.array([2])}
InitialStock_2    = np.array([3,5,2,4])
InitialStock_8    = np.array([0.5,0.5,0.2,0.4,1,1,1,1])
FutureStock_2     = np.array([0.0,0.0,0.0,0.0,18.0,20,20,20,20.0])
ThisSwitchTime    = 5 # First year with future stock curve, start counting from 1.
Inflow_2          = np.array([3.541625588,	5.227890554,2.01531097,4])

""" Test case with lognormally distributed lifetime for inflow-driven model"""
# NOTE: for dynamic MFA the parameters average lifetime and standard deviation refer to the pdf curve as plotted, 
# whereas in the scipy and Excel functions, the parameters mu and sigma
# refer to the parameters of the underlying normal distribution.
# The parameters need to be converted as follows:
# for single (fixed) lifetime
Time_T_LN  = np.arange(0, 300, 1)
mu    = 20
sg    = 20
LT_LN = np.log(mu / np.sqrt(1 + mu * mu / (sg * sg))) # calculate parameter mu    of underlying normal distribution
SG_LN = np.sqrt(np.log(1 + mu * mu / (sg * sg)))      # calculate parameter sigma of underlying normal distribution
lifetime_LogNorm = {'Type': 'LogNormal', 'Mean': np.array([mu]), 'StdDev': np.array([sg])} # call with ACTUAL mu and sigma of curve,
# dsm makes conversion
SF = scipy.stats.lognorm.sf(x=Time_T_LN, s=SG_LN, loc = 0, scale=np.exp(LT_LN)) # values chosen according to description on
# https://docs.scipy.org/doc/scipy-0.13.0/reference/generated/scipy.stats.lognorm.html
# Same result as EXCEL function "=LOGNORM.VERT(x;LT_LN;SG_LN;TRUE)"
Inflow_LN          = np.zeros((300))
Inflow_LN[0:20]    = np.array([1,2,3,4,5,6,7,8,2,3,5,6,7,1,2,4,5,6,7,3])
LN_Stock_Reference_2060 = 5.8693165260386 # calculated independently with Excel

""" Test case with folded normally distributed lifetime for inflow-driven model"""
Time_T_FN  = np.arange(0, 100, 1)
mu    = 20
sg    = 20
lifetime_FoldNorm = {'Type': 'FoldedNormal', 'Mean': np.array([mu]), 'StdDev': np.array([sg])} # call with mu and sigma of curve BEFORE folding,
# dsm makes conversion
Inflow_FN          = np.zeros((100))
Inflow_FN[0:20]    = np.array([1,2,3,4,5,6,7,8,2,3,5,6,7,1,2,4,5,6,7,3])
FN_Stock_Reference_2060 = 6.5004904790008300000
 # calculated independently with Excel

# Inflow for quick declines in stock, with negative entries, no correction of negative inflows
InflowNeg_NoCorr = np.array([0,0,1.003845108798,1.009876170898,1.022946871294,2.052181974193,1.098597211758,2.178632487261,0.2864589383765,
-1.57838035116,0.5823071731028,0.7368688072826,0.8609818446092,0.9303172472582,2.940380920226,0.8868056550348,0.8077321288789,1.74261978268,
1.72284735601,2.770808172213,-2.13996861954,0.9927014953087,1.118058099656,1.211591711403,1.256322506739,1.248773108954,1.197964611415,
1.122904133751,1.047910488113,0.9952110047915])
InflowNeg_WithCorr = np.array([0,0,1.003845108797608,1.009876170898179,1.022946871293978,2.052181974192771,1.09859721175781,2.178632487260613,
0.2864589383765391,0,0.468909567774503,0.600148064601485,0.7138380402455925,0.7922474677487478,2.832866490884595,0.8262270093751778,0.7986846781384966,
1.775290769026188,1.776531605001062,2.822224969997677,0,0.82099326892646,0.9183009967181216,1.007417665416504,1.076751857993922,1.119633273700667,
1.134233884697729,1.123750382153023,1.096483322433279,1.064262457376682])

StockChange_WithCorr = np.array([0,0,1,1,1,2,1,2,0,-2,0,0,0,0,2,0,0,1,1,2,-3,0,0,0,0,0,0,0,0,0])

InitialStockInflowNegNoCorrect = np.array([0.7929476381216127,0.6688896434012339,0.2377146834690121,0.4401462789619187,1.050188897357724,
1.023279749316858,1.00991262429366,1.003845108797608,2.734512232505172,-1.576179715364555,0.5270786116039677,0.6253099746885178,
0.7133245646541703,0.7808737550728377,-2.193761739572536,0.8006372758619281,0.7486059179704083,0.6628542885032971,1.562532671694373,
1.463347346524538,1.385763022717013,1.346937342733784,1.360199865992007,1.431582763055532,0.5522778871344547,0.7074660291917115,
-1.038359636072531,1.901306859994554,1.088965343251684,1.121312374405391])

InitialStockInflowNoNegCorrect = np.array([0.7929476381216127,0.6688896434012339,0.2377146834690121,0.4401462789619187,1.050188897357724,
1.023279749316858,1.00991262429366,1.003845108797608,2.734512232505172,0.431510502230662,0.5391407358051091,0.8522203972396362,
1.568386852314742,0.8767713133566062,0.4696866483782957,0.5372828546582809,0.5715642400086977,0.571388710240865,0.5417776639498378,
0.4910906219746665,0.4275448257791661,2.365060643030991,1.802882915501588,1.755204649624293,0.5284632857607936,0.4360513595181573,
0.3800804006621792,0.755755759275017,0.9453763220611762,1.024955581556197])

InitialStockInflowNegCorrect = np.array([0.7929476381216127,0.6688896434012339,0.2377146834690121,0.4401462789619187,
1.050188897357724,1.023279749316858,1.00991262429366,1.003845108797608,2.734512232505172,0,0.4252614122673855,0.5118790151618888,
0.5969693316522457,0.6739530024236163,0,0.4358419187951329,0.4372674850950349,0.4227905939406414,1.401739961117737,1.38013886282689,
1.370084205085089,1.381499862452395,1.422069169849336,1.495945462462685,0.5985535082458745,0.7251533575497293,0,1.756743048425328,
0.9375744022016721,0.984738434681199])

# Parameters for stock-driven model with initial stock:
FutureStock1  = np.array([2.8,3,3.5,4,5,5])
FutureStock1a = np.array([0,0,0,2.8,3,3.5,4,5,5])
FutureStock2  = np.array([2.8,3,3.5,2.2,2.3,2.5])
FutureStock2a = np.array([0,0,0,2.8,3,3.5,2.2,2.3,2.5])
InitialStock1 = np.array([[0.4,0.2,0.5,0,0,0,0,0,0],[0.1,0.5,1.0,0,0,0,0,0,0]]).transpose()
InitialStock2 = np.array([[0.4,0.2,0.5,0.1,0.25,0.3,0.1,0.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0.1,0.5,1.0,0.7,0.2,0.3,0.45,0.2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]).transpose()
TypeSplit1    = np.array([[0.5,0.5,0.1,0.5,0.8,0.5],[0.5,0.5,0.9,0.5,0.2,0.5]]).transpose()
TypeSplit1a   = np.array([[0,0,0,0.5,0.5,0.1,0.5,0.8,0.5],[0,0,0,0.5,0.5,0.9,0.5,0.2,0.5]]).transpose()
TypeSplit2a   = np.array([[0,0,0,0,0,0,0,0,0.5,0.5,0.1,0.5,0.8,0.5,0.5,0.1,0.5,0.8,0.5,0.5,0.1,0.5,0.8,0.5,0.5,0.1,0.5,0.8,0.5,0.33],
                          [0,0,0,0,0,0,0,0,0.5,0.5,0.9,0.5,0.2,0.5,0.5,0.9,0.5,0.2,0.5,0.5,0.9,0.5,0.2,0.5,0.5,0.9,0.5,0.2,0.5,0.67]]).transpose()

TypeSplitStockCheckType1=np.array([0.1520464589202331,0.06727086112098983,0.1559267249296865,0.1326551318262058,0.1923019570573063,
                                   0.06734416832144496,0.4795521109040651,1.459402923878064,0])

TypeSplitStockCheckType2=np.array([0.03801161473005826,0.1681771528024746,0.311853449859373,0.1326551318262058,0.1923019570573063,
                                   0.6060975148930047,0.4795521109040651,0.3648507309695161,0])

TypeSplitInflowCheckType=np.array([[0.6761333517696461,0.1690333379424115],
[0.2558444008518857,0.6396110021297141],
[0.5,1],
[0.3523465342883199,0.3523465342883199],
[0.4135884347844512,0.4135884347844512],
[0.1138340956232945,1.02450686060965],
[0.6134536124575378,0.6134536124575378],
[1.459402923878064,0.3648507309695161],
[0.5136958913485281,0.5136958913485281]])

TypeSplitInitialStockInflowCorrect1StockCheck = np.array([[0,0],
[0,0],
[0.5,1],
[0.3908625698550751,0.7817251397101502],
[0.2957996369747763,0.5915992739495526],
[0.2324798530180466,0.4649597060360933],
[0.1882452627129519,0.3764905254259038],
[0.1559267249296865,0.311853449859373],
[0.1314683082705697,0.2629366165411394]])

TypeSplitInitialStockInflowCorrect2StockCheck = np.array([[0,0],
[0,0],
[0.5,1],
[0.3908625698550751,0.7817251397101502],
[0.2957996369747763,0.5915992739495526],
[0.2324798530180466,0.4649597060360933],
[0.1882452627129519,0.3764905254259038],
[0.1559267249296865,0.311853449859373],
[0.1314683082705697,0.2629366165411394]])

TypeSplitInitialStockInflowCorrect3StockCheck = np.array([[0,0],
[0,0],
[0.5,1],
[0.3908625698550751,0.7817251397101502],
[0.2957996369747763,0.5915992739495526],
[0.2324798530180466,0.4649597060360933],
[0.1493421286476113,0.2986842572952226],
[0.123702603074578,0.247405206149156],
[0.1042988106254021,0.2085976212508043]])

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
myDSM4a= dsm.DynamicStockModel(t=Time_T_FixedLT, s=Stock_T_NormLT, lt=lifetime_NormLT)

myDSMX = dsm.DynamicStockModel(t=Time_T_FixedLT_XX, lt=lifetime_NormLT_X)
TestInflow_XX = myDSMX.compute_i_from_s(InitialStock=InitialStock_XX)

myDSMXY = dsm.DynamicStockModel(t=Time_T_FixedLT_XX, i=TestInflow_XX, lt=lifetime_NormLT_X)

#For negatative inflow correction 
myDSM_ICF = dsm.DynamicStockModel(t=Time_T_30, s=Stock_SDM_NegInflow_NormLT, lt=lifetime_NormLT8)
[SC1,OC1,I1] = myDSM_ICF.compute_stock_driven_model(NegativeInflowCorrect = False)
myDSM_ICT = dsm.DynamicStockModel(t=Time_T_30, s=Stock_SDM_NegInflow_NormLT, lt=lifetime_NormLT8)
[SC2,OC2,I2] = myDSM_ICT.compute_stock_driven_model(NegativeInflowCorrect = True)
OT2 = myDSM_ICT.compute_outflow_total()
SCh2= myDSM_ICT.compute_stock_change()
Bal2= myDSM_ICT.check_stock_balance()

#For negatative inflow correction with initial stock
#a) Neg inflow, Correction Flag is False:
myDSM_ICFIS = dsm.DynamicStockModel(t=Time_T_30, s=Stock_SDM_NegInflow_NormLTNeg.copy(), lt=lifetime_NormLT8)
[SC1IS,OC1IS,I1IS] = myDSM_ICFIS.compute_stock_driven_model_initialstock(InitialStock = InitialStock_8, SwitchTime = 9, NegativeInflowCorrect = False)
OT1IS = myDSM_ICFIS.compute_outflow_total()
SCh1IS= myDSM_ICFIS.compute_stock_change()
Bal1IS= myDSM_ICFIS.check_stock_balance()
#b) No neg. inflow, correction flag is True:
myDSM_ICTIST = dsm.DynamicStockModel(t=Time_T_30, s=Stock_SDM_PosInflow_NormLTNeg.copy(), lt=lifetime_NormLT8)
[SC3IS,OC3IS,I3IS] = myDSM_ICTIST.compute_stock_driven_model_initialstock(InitialStock = InitialStock_8, SwitchTime = 9, NegativeInflowCorrect = True)
OT3IS = myDSM_ICTIST.compute_outflow_total()
SCh3IS= myDSM_ICTIST.compute_stock_change()
Bal3IS= myDSM_ICTIST.check_stock_balance()
#c) Neg. inflow: Correction flag is True and neg. inflow occurs.
myDSM_ICTIS = dsm.DynamicStockModel(t=Time_T_30, s=Stock_SDM_NegInflow_NormLTNeg.copy(), lt=lifetime_NormLT8)
[SC2IS,OC2IS,I2IS] = myDSM_ICTIS.compute_stock_driven_model_initialstock(InitialStock = InitialStock_8, SwitchTime = 9, NegativeInflowCorrect = True)
OT2IS = myDSM_ICTIS.compute_outflow_total()
SCh2IS= myDSM_ICTIS.compute_stock_change()
Bal2IS= myDSM_ICTIS.check_stock_balance()

# Test compute_stock_driven_model_initialstock:
TestDSM_IntitialStock = dsm.DynamicStockModel(t=Time_T_FixedLT_2, s=FutureStock_2, lt=lifetime_NormLT_2)
Sc_InitialStock_2,Oc_InitialStock_2,I_InitialStock_2 = TestDSM_IntitialStock.compute_stock_driven_model_initialstock(InitialStock = InitialStock_2, SwitchTime = ThisSwitchTime)
OT3 = TestDSM_IntitialStock.compute_outflow_total()
#TestDSM_IntitialStock.compute_stock_total()
SCh3= TestDSM_IntitialStock.compute_stock_change()
Bal3= TestDSM_IntitialStock.check_stock_balance()

# Test stock-driven model with initialstock and type split
TestDSM_IntitialStockTypeSplit = dsm.DynamicStockModel(t=Time_T_FixedLT_2, s=FutureStock1, lt=lifetime_NormLT_3)
SFArrayCombined                = TestDSM_IntitialStockTypeSplit.compute_sf().copy()
[SC_IS_TS,OC_IS_TS,I_IS_TS]    = TestDSM_IntitialStockTypeSplit.compute_stock_driven_model_initialstock_typesplit(FutureStock=FutureStock1,InitialStock=InitialStock1,SFArrayCombined=np.einsum('tc,g->tcg',SFArrayCombined,np.ones(2)),TypeSplit=TypeSplit1)
OT_IS_TS  = TestDSM_IntitialStockTypeSplit.compute_outflow_total()
SCh_IS_TS = TestDSM_IntitialStockTypeSplit.compute_stock_change()
Bal_IS_TS = TestDSM_IntitialStockTypeSplit.check_stock_balance()

# Test stock-driven model with initialstock and type split and NegativeInflowCorrect, lognormal lifetime
# 1) NegativeInflowCorrect on but does not occur
TestDSM_IntitialStockTypeSplit1       = dsm.DynamicStockModel(t=Time_T_FixedLT_2, s=FutureStock1a.copy(), lt=lifetime_NormLT_3) 
SFArrayCombined                       = TestDSM_IntitialStockTypeSplit1.compute_sf().copy()
[SC_IS_TS1,OC_IS_TS1,I_IS_TS1,Flags1] = TestDSM_IntitialStockTypeSplit1.compute_stock_driven_model_initialstock_typesplit_negativeinflowcorrect(SwitchTime=3,InitialStock=InitialStock1,SFArrayCombined=np.einsum('tc,g->tcg',SFArrayCombined,np.ones(2)),TypeSplit=TypeSplit1a,NegativeInflowCorrect=True)
OT_IS_TS1                             = TestDSM_IntitialStockTypeSplit1.compute_outflow_total()
SCh_IS_TS1                            = TestDSM_IntitialStockTypeSplit1.compute_stock_change()
Bal_IS_TS1                            = TestDSM_IntitialStockTypeSplit1.check_stock_balance()

# 2) NegativeInflowCorrect on but is not fixed
TestDSM_IntitialStockTypeSplit2       = dsm.DynamicStockModel(t=Time_T_FixedLT_2, s=FutureStock2a.copy(), lt=lifetime_NormLT_3) 
SFArrayCombined                       = TestDSM_IntitialStockTypeSplit2.compute_sf().copy()
[SC_IS_TS2,OC_IS_TS2,I_IS_TS2,Flags2] = TestDSM_IntitialStockTypeSplit2.compute_stock_driven_model_initialstock_typesplit_negativeinflowcorrect(SwitchTime=3,InitialStock=InitialStock1,SFArrayCombined=np.einsum('tc,g->tcg',SFArrayCombined,np.ones(2)),TypeSplit=TypeSplit1a,NegativeInflowCorrect=False)
OT_IS_TS2                             = TestDSM_IntitialStockTypeSplit2.compute_outflow_total()
SCh_IS_TS2                            = TestDSM_IntitialStockTypeSplit2.compute_stock_change()
Bal_IS_TS2                            = TestDSM_IntitialStockTypeSplit2.check_stock_balance()

# 3) NegativeInflowCorrect on and fixed
TestDSM_IntitialStockTypeSplit3       = dsm.DynamicStockModel(t=Time_T_FixedLT_2, s=FutureStock2a.copy(), lt=lifetime_NormLT_3) 
SFArrayCombined                       = TestDSM_IntitialStockTypeSplit3.compute_sf().copy()
[SC_IS_TS3,OC_IS_TS3,I_IS_TS3,Flags3] = TestDSM_IntitialStockTypeSplit3.compute_stock_driven_model_initialstock_typesplit_negativeinflowcorrect(SwitchTime=3,InitialStock=InitialStock1,SFArrayCombined=np.einsum('tc,g->tcg',SFArrayCombined,np.ones(2)),TypeSplit=TypeSplit1a,NegativeInflowCorrect=True)
OT_IS_TS3                             = TestDSM_IntitialStockTypeSplit3.compute_outflow_total()
SCh_IS_TS3                            = TestDSM_IntitialStockTypeSplit3.compute_stock_change()
Bal_IS_TS3                            = TestDSM_IntitialStockTypeSplit3.check_stock_balance()

# Test stock-driven model with initialstock and type split and NegativeInflowCorrect, normal lifetime
# 1) NegativeInflowCorrect on but does not occur
TestDSM_IntitialStockTypeSplit1a          = dsm.DynamicStockModel(t=Time_T_FixedLT_3, s=Stock_SDM_PosInflow_NormLTNeg.copy(), lt=lifetime_NormLT_4) 
SFArrayCombineda                          = TestDSM_IntitialStockTypeSplit1a.compute_sf().copy()
[SC_IS_TS1a,OC_IS_TS1a,I_IS_TS1a,Flags1a] = TestDSM_IntitialStockTypeSplit1a.compute_stock_driven_model_initialstock_typesplit_negativeinflowcorrect(SwitchTime=8,InitialStock=InitialStock2,SFArrayCombined=np.einsum('tc,g->tcg',SFArrayCombineda,np.ones(2)),TypeSplit=TypeSplit2a,NegativeInflowCorrect=True)
OT_IS_TS1a                                = TestDSM_IntitialStockTypeSplit1a.compute_outflow_total()
SCh_IS_TS1a                               = TestDSM_IntitialStockTypeSplit1a.compute_stock_change()
Bal_IS_TS1a                               = TestDSM_IntitialStockTypeSplit1a.check_stock_balance()

# 2) NegativeInflowCorrect on but is not fixed
TestDSM_IntitialStockTypeSplit2a          = dsm.DynamicStockModel(t=Time_T_FixedLT_3, s=Stock_SDM_NegInflow_NormLTNeg.copy(), lt=lifetime_NormLT_4) 
SFArrayCombineda                          = TestDSM_IntitialStockTypeSplit2a.compute_sf().copy()
[SC_IS_TS2a,OC_IS_TS2a,I_IS_TS2a,Flags2a] = TestDSM_IntitialStockTypeSplit2a.compute_stock_driven_model_initialstock_typesplit_negativeinflowcorrect(SwitchTime=8,InitialStock=InitialStock2,SFArrayCombined=np.einsum('tc,g->tcg',SFArrayCombineda,np.ones(2)),TypeSplit=TypeSplit2a,NegativeInflowCorrect=False)
OT_IS_TS2a                                = TestDSM_IntitialStockTypeSplit2a.compute_outflow_total()
SCh_IS_TS2a                               = TestDSM_IntitialStockTypeSplit2a.compute_stock_change()
Bal_IS_TS2a                               = TestDSM_IntitialStockTypeSplit2a.check_stock_balance()

# 3) NegativeInflowCorrect on and fixed
TestDSM_IntitialStockTypeSplit3a          = dsm.DynamicStockModel(t=Time_T_FixedLT_3, s=Stock_SDM_NegInflow_NormLTNeg.copy(), lt=lifetime_NormLT_4) 
SFArrayCombineda                          = TestDSM_IntitialStockTypeSplit3a.compute_sf().copy()
[SC_IS_TS3a,OC_IS_TS3a,I_IS_TS3a,Flags3a] = TestDSM_IntitialStockTypeSplit3a.compute_stock_driven_model_initialstock_typesplit_negativeinflowcorrect(SwitchTime=8,InitialStock=InitialStock2,SFArrayCombined=np.einsum('tc,g->tcg',SFArrayCombineda,np.ones(2)),TypeSplit=TypeSplit2a,NegativeInflowCorrect=True)
OT_IS_TS3a                                = TestDSM_IntitialStockTypeSplit3a.compute_outflow_total()
SCh_IS_TS3a                               = TestDSM_IntitialStockTypeSplit3a.compute_stock_change()
Bal_IS_TS3a                               = TestDSM_IntitialStockTypeSplit3a.check_stock_balance()

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

# Test lognormal lifetime dist.
myDSM_LN = dsm.DynamicStockModel(t=Time_T_LN, i=Inflow_LN, lt=lifetime_LogNorm)
LN_Stock = myDSM_LN.compute_s_c_inflow_driven()
LN_Stock_60 = LN_Stock.sum(axis =1)

# Test folded normal lifetime dist.
myDSM_FN = dsm.DynamicStockModel(t=Time_T_FN, i=Inflow_FN, lt=lifetime_FoldNorm)
FN_Stock = myDSM_FN.compute_s_c_inflow_driven()
FN_Stock_60 = FN_Stock.sum(axis =1)


# Test that ouflow computed with pdf from compute_outflow_pdf() yields same result as the one calculated directly from the sf via compute_s_c_inflow_driven() and compute_o_c_from_s_c()
lt_pdf   = {'Type': 'Normal', 'Mean': np.array([8]), 'StdDev': np.array([3])}
ifl_pdf  = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5]

DSM_pdf = dsm.DynamicStockModel(t=np.arange(0, 25, 1),i=ifl_pdf, lt=lt_pdf)
SF_pdf  = DSM_pdf.compute_sf()
PDF_pdf = DSM_pdf.compute_outflow_pdf()
SC_pdf  = DSM_pdf.compute_s_c_inflow_driven()
OC_pdf  = DSM_pdf.compute_o_c_from_s_c()
OC_alt  = np.einsum('c,tc->tc',np.array(ifl_pdf),PDF_pdf)
Bal_pdf = (np.abs(OC_pdf-OC_alt)).sum()
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
        
    def test_stock_driven_model_normallyDistLifetime_NegInflowFlagTrue(self):
        """Test Stock Driven Model with normally distributed product lifetime.
        Set the NegativeInflowCorrect flag as True but use a test case without negative inflows."""
        np.testing.assert_array_almost_equal(
            myDSM4a.compute_stock_driven_model(NegativeInflowCorrect = True)[0], Stock_TC_NormLT, 8)
        np.testing.assert_array_almost_equal(
            myDSM4a.compute_stock_driven_model(NegativeInflowCorrect = True)[1], Outflow_TC_NormLT, 8)
        np.testing.assert_array_almost_equal(
            myDSM4a.compute_stock_driven_model(NegativeInflowCorrect = True)[2], Inflow_T_FixedLT, 8)
        np.testing.assert_array_almost_equal(myDSM4a.compute_outflow_total(), Outflow_T_NormLT, 8)
        np.testing.assert_array_almost_equal(
            myDSM4a.compute_stock_change(), StockChange_T_NormLT, 8)
        np.testing.assert_array_almost_equal(myDSM4a.check_stock_balance(), Bal.transpose(), 12)        
        
    def test_stock_driven_model_normallyDistLifetime_NegInflow(self):
        """Test Stock Driven Model with normally distributed product lifetime, with negative inflow."""
        np.testing.assert_array_almost_equal(
            myDSM_ICF.compute_stock_driven_model(NegativeInflowCorrect = False)[2], InflowNeg_NoCorr, 12)
        np.testing.assert_array_almost_equal(
            myDSM_ICT.compute_stock_driven_model(NegativeInflowCorrect = True)[2], InflowNeg_WithCorr, 12)
        np.testing.assert_array_almost_equal(
            myDSM_ICT.compute_stock_change(), StockChange_WithCorr, 12)
        np.testing.assert_array_almost_equal(myDSM_ICT.check_stock_balance(), Bal30.transpose(), 12)   
        
    def test_stock_driven_model_Initialstock_NegInflow(self):
        """Test Stock Driven Model with normally distributed product lifetime, initial stock, with negative inflow and no negative inflow correction."""
        np.testing.assert_array_almost_equal(myDSM_ICFIS.check_stock_balance(), Bal30.transpose(), 12) 
        np.testing.assert_array_almost_equal(myDSM_ICFIS.compute_stock_driven_model_initialstock(InitialStock = InitialStock_8, SwitchTime = 9, NegativeInflowCorrect = False)[2], InitialStockInflowNegNoCorrect, 12) 
        
    def test_stock_driven_model_Initialstock_NegInflowNotUsed(self):
        """Test Stock Driven Model with normally distributed product lifetime, initial stock, with no negative inflow and no negative inflow correction."""
        np.testing.assert_array_almost_equal(myDSM_ICTIST.check_stock_balance(), Bal30.transpose(), 12) 
        np.testing.assert_array_almost_equal(myDSM_ICTIST.compute_stock_driven_model_initialstock(InitialStock = InitialStock_8, SwitchTime = 9, NegativeInflowCorrect = False)[2], InitialStockInflowNoNegCorrect, 12) 

    def test_stock_driven_model_Initialstock_NegInflowFixed(self):
        """Test Stock Driven Model with normally distributed product lifetime, initial stock, with negative inflow and negative inflow correction."""
        np.testing.assert_array_almost_equal(myDSM_ICTIS.check_stock_balance(), Bal30.transpose(), 12) 
        np.testing.assert_array_almost_equal(myDSM_ICTIS.compute_stock_driven_model_initialstock(InitialStock = InitialStock_8, SwitchTime = 9, NegativeInflowCorrect = True)[2], InitialStockInflowNegCorrect, 12) 

    def test_stock_driven_model_Initialstock_NegInflow_TypeSplit_NotUsed(self):
        """Test Stock Driven Model with lognormally distributed product lifetime, initial stock, typesplit, with negative inflow correction but no negative inflow occurring."""
        np.testing.assert_array_almost_equal(TestDSM_IntitialStockTypeSplit1.check_stock_balance(), Bal9.transpose(), 12) 
        np.testing.assert_array_almost_equal(TestDSM_IntitialStockTypeSplit1.compute_stock_driven_model_initialstock_typesplit_negativeinflowcorrect(SwitchTime=3,InitialStock=InitialStock1,SFArrayCombined=np.einsum('tc,g->tcg',SFArrayCombined,np.ones(2)),TypeSplit=TypeSplit1a,NegativeInflowCorrect=True)[0][:,2,:], TypeSplitInitialStockInflowCorrect1StockCheck, 12) 
     
    def test_stock_driven_model_Initialstock_NegInflow_TypeSplit_NoCorr(self):
        """Test Stock Driven Model with lognormally distributed product lifetime, initial stock, typesplit, with negative inflow correction of but negative inflow occurring."""
        np.testing.assert_array_almost_equal(TestDSM_IntitialStockTypeSplit2.check_stock_balance(), Bal9.transpose(), 12) 
        np.testing.assert_array_almost_equal(TestDSM_IntitialStockTypeSplit2.compute_stock_driven_model_initialstock_typesplit_negativeinflowcorrect(SwitchTime=3,InitialStock=InitialStock1,SFArrayCombined=np.einsum('tc,g->tcg',SFArrayCombined,np.ones(2)),TypeSplit=TypeSplit1a,NegativeInflowCorrect=False)[0][:,2,:], TypeSplitInitialStockInflowCorrect2StockCheck, 12) 
        
    def test_stock_driven_model_Initialstock_NegInflow_TypeSplit_Corr(self):
        """Test Stock Driven Model with lognormally distributed product lifetime, initial stock, typesplit, with negative inflow correction on and negative inflow occurring and corrected."""
        np.testing.assert_array_almost_equal(TestDSM_IntitialStockTypeSplit3.check_stock_balance(), Bal9.transpose(), 12) 
        np.testing.assert_array_almost_equal(TestDSM_IntitialStockTypeSplit3.compute_stock_driven_model_initialstock_typesplit_negativeinflowcorrect(SwitchTime=3,InitialStock=InitialStock1,SFArrayCombined=np.einsum('tc,g->tcg',SFArrayCombined,np.ones(2)),TypeSplit=TypeSplit1a,NegativeInflowCorrect=True)[0][:,2,:], TypeSplitInitialStockInflowCorrect3StockCheck, 12) 

    def test_stock_driven_model_Initialstock_NegInflow_TypeSplit_NotUsed_NormalLT(self):
        """Test Stock Driven Model with normally distributed product lifetime, initial stock, typesplit, with negative inflow correction but no negative inflow occurring."""
        np.testing.assert_array_almost_equal(TestDSM_IntitialStockTypeSplit1a.check_stock_balance(), Bal30.transpose(), 12) 
     
    def test_stock_driven_model_Initialstock_NegInflow_TypeSplit_NoCorr_NormalLT(self):
        """Test Stock Driven Model with normally distributed product lifetime, initial stock, typesplit, with negative inflow correction of but negative inflow occurring."""
        np.testing.assert_array_almost_equal(TestDSM_IntitialStockTypeSplit2a.check_stock_balance(), Bal30.transpose(), 12) 
        
    def test_stock_driven_model_Initialstock_NegInflow_TypeSplit_Corr_NormalLT(self):
        """Test Stock Driven Model with normally distributed product lifetime, initial stock, typesplit, with negative inflow correction on and negative inflow occurring and corrected."""
        np.testing.assert_array_almost_equal(TestDSM_IntitialStockTypeSplit3a.check_stock_balance(), Bal30.transpose(), 12) 

    def test_stock_driven_model_Initialstock_TypeSplit(self):
        """Test Stock Driven Model with lognormally distributed product lifetime, initial stock, and type split."""
        np.testing.assert_array_almost_equal(TestDSM_IntitialStockTypeSplit.check_stock_balance()[1::], np.zeros((5)), 12) 
        np.testing.assert_array_almost_equal(TestDSM_IntitialStockTypeSplit.compute_stock_driven_model_initialstock_typesplit(FutureStock=FutureStock1,InitialStock=InitialStock1,SFArrayCombined=np.einsum('tc,g->tcg',SFArrayCombined,np.ones(2)),TypeSplit=TypeSplit1)[0][4,:,0], TypeSplitStockCheckType1, 12) 
        np.testing.assert_array_almost_equal(TestDSM_IntitialStockTypeSplit.compute_stock_driven_model_initialstock_typesplit(FutureStock=FutureStock1,InitialStock=InitialStock1,SFArrayCombined=np.einsum('tc,g->tcg',SFArrayCombined,np.ones(2)),TypeSplit=TypeSplit1)[0][4,:,1], TypeSplitStockCheckType2, 12) 
        np.testing.assert_array_almost_equal(TestDSM_IntitialStockTypeSplit.compute_stock_driven_model_initialstock_typesplit(FutureStock=FutureStock1,InitialStock=InitialStock1,SFArrayCombined=np.einsum('tc,g->tcg',SFArrayCombined,np.ones(2)),TypeSplit=TypeSplit1)[2],        TypeSplitInflowCheckType, 12) 

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
        np.testing.assert_array_almost_equal(TestInflow_WB, Inflow_WB, 6) 
        np.testing.assert_array_almost_equal(myDSMWB4.compute_s_c_inflow_driven()[-1, :], InitialStock_WB, 8)     
        
    def test_compute_stock_driven_model_initialstock(self):
        """Test stock-driven model with initial stock given."""
        np.testing.assert_array_almost_equal(I_InitialStock_2, I_InitialStock_2_Ref, 8) 
        np.testing.assert_array_almost_equal(Sc_InitialStock_2, Sc_InitialStock_2_Ref, 8)
        np.testing.assert_array_almost_equal(Sc_InitialStock_2.sum(axis =1), Sc_InitialStock_2_Ref_Sum, 8)
        np.testing.assert_array_almost_equal(Oc_InitialStock_2, Oc_InitialStock_2_Ref, 8) 

    def test_stock_from_inflow_LogNormalDistLifetime(self):
        """Test computation of stock from inflow for lognormally distributed product lifetime."""
        np.testing.assert_array_almost_equal(LN_Stock_Reference_2060, LN_Stock_60[60], 9) 

    def test_stock_from_inflow_FoldedNormalDistLifetime(self):
        """Test computation of stock from inflow for folded normally distributed product lifetime."""
        np.testing.assert_array_almost_equal(FN_Stock_Reference_2060, FN_Stock_60[60], 12) 

    def test_compute_outflow_pdf(self):
        """Test wether outflow by cohort is the same if computed with pdf from compute_outflow_pdf vs. the standard routines."""
        np.testing.assert_array_almost_equal(OC_pdf, OC_alt, 14) 
        np.testing.assert_array_almost_equal(Bal_pdf, 0, 12) 


    if __name__ == '__main__':
        unittest.main()

