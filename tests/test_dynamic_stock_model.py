import odym.dynamic_stock_model as dsm # remove and import the class manually if this unit test is run as standalone script
import numpy as np
import pytest
import scipy

#  Fixtures for Test Data 

@pytest.fixture(scope="module")
def fixed_lifetime_data():
    """Provides test data for fixed lifetime DSMs."""
    Time_T_FixedLT = np.arange(0, 10)
    Inflow_T_FixedLT = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    lifetime_FixedLT = {'Type': 'Fixed', 'Mean': np.array([5])}
    lifetime_FixedLT0 = {'Type': 'Fixed', 'Mean': np.array([0])}

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
    Bal = np.zeros(10)

    # For inflow_from_stock_fixedLifetime
    Time_T_FixedLT_X = np.arange(1, 9, 1)
    lifetime_FixedLT_X = {'Type': 'Fixed', 'Mean': np.array([5])}
    InitialStock_X = np.array([0, 0, 0, 7, 5, 4, 3, 2])
    Inflow_X = np.array([0, 0, 0, 7, 5, 4, 3, 2])

    return {
        "Time_T_FixedLT": Time_T_FixedLT,
        "Inflow_T_FixedLT": Inflow_T_FixedLT,
        "lifetime_FixedLT": lifetime_FixedLT,
        "lifetime_FixedLT0": lifetime_FixedLT0,
        "Outflow_T_FixedLT": Outflow_T_FixedLT,
        "Outflow_TC_FixedLT": Outflow_TC_FixedLT,
        "Stock_T_FixedLT": Stock_T_FixedLT,
        "StockChange_T_FixedLT": StockChange_T_FixedLT,
        "Stock_TC_FixedLT": Stock_TC_FixedLT,
        "Bal": Bal,
        "Time_T_FixedLT_X": Time_T_FixedLT_X,
        "lifetime_FixedLT_X": lifetime_FixedLT_X,
        "InitialStock_X": InitialStock_X,
        "Inflow_X": Inflow_X,
    }


@pytest.fixture(scope="module")
def normal_lifetime_data():
    """Provides test data for normally distributed lifetime DSMs."""
    Time_T_FixedLT = np.arange(0, 10)
    Inflow_T_FixedLT = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    lifetime_NormLT = {'Type': 'Normal', 'Mean': np.array([5]), 'StdDev': np.array([1.5])}
    lifetime_NormLT0 = {'Type': 'Normal', 'Mean': np.array([0]), 'StdDev': np.array([1.5])}
    lifetime_NormLT8 = {'Type': 'Normal', 'Mean': np.array([8]), 'StdDev': np.array([3])}
    
    Stock_TC_NormLT = np.array([[9.99570940e-01, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
                                 [9.96169619e-01, 1.99914188e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
                                 [9.77249868e-01, 1.99233924e+00, 2.99871282e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
                                 [9.08788780e-01, 1.95449974e+00, 2.98850886e+00, 3.99828376e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
                                 [7.47507462e-01, 1.81757756e+00, 2.93174960e+00, 3.98467848e+00, 4.99785470e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
                                 [5.00000000e-01, 1.49501492e+00, 2.72636634e+00, 3.90899947e+00, 4.98084810e+00, 5.99742564e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
                                 [2.52492538e-01, 1.00000000e+00, 2.24252239e+00, 3.63515512e+00, 4.88624934e+00, 5.97701772e+00, 6.99699658e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
                                 [9.12112197e-02, 5.04985075e-01, 1.50000000e+00, 2.99002985e+00, 4.54394390e+00, 5.86349921e+00, 6.97318734e+00, 7.99656752e+00, 0.00000000e+00, 0.00000000e+00],
                                 [2.27501319e-02, 1.82422439e-01, 7.57477613e-01, 2.00000000e+00, 3.73753731e+00, 5.45273268e+00, 6.84074908e+00, 7.96935696e+00, 8.99613846e+00, 0.00000000e+00],
                                 [3.83038057e-03, 4.55002639e-02, 2.73633659e-01, 1.00997015e+00, 2.50000000e+00, 4.48504477e+00, 6.36152146e+00, 7.81799894e+00, 8.96552657e+00, 9.99570940e+00]])
    Stock_T_NormLT = np.array([0.99957094, 2.9953115, 5.96830193, 9.85008113, 14.4793678, 19.60865447, 24.99043368, 30.46342411, 35.95916467, 41.45873561])
    Outflow_T_NormLT = np.array([4.29060333e-04, 4.25944090e-03, 2.70095728e-02, 1.18220793e-01, 3.70713330e-01, 8.70713330e-01, 1.61822079e+00, 2.52700957e+00, 3.50425944e+00, 4.50042906e+00])
    Outflow_TC_NormLT = np.array([[4.29060333e-04, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
                                   [3.40132023e-03, 8.58120666e-04, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00],
                                   [1.89197514e-02, 6.80264047e-03, 1.28718100e-03, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00],
                                   [6.84610878e-02, 3.78395028e-02, 1.02039607e-02, 1.71624133e-03, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00],
                                   [1.61281318e-01, 1.36922176e-01, 5.67592541e-02, 1.36052809e-02, 2.14530167e-03, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00],
                                   [2.47507462e-01, 3.22562636e-01, 2.05383263e-01, 7.56790055e-02, 1.70066012e-02, 2.57436200e-03, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00],
                                   [2.47507462e-01, 4.95014925e-01, 4.83843953e-01, 2.73844351e-01, 9.45987569e-02, 2.04079214e-02, 3.00342233e-03, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00],
                                   [1.61281318e-01, 4.95014925e-01, 7.42522387e-01, 6.45125271e-01, 3.42305439e-01, 1.13518508e-01, 2.38092416e-02, 3.43248267e-03, -0.00000000e+00, -0.00000000e+00],
                                   [6.84610878e-02, 3.22562636e-01, 7.42522387e-01, 9.90029850e-01, 8.06406589e-01, 4.10766527e-01, 1.32438260e-01, 2.72105619e-02, 3.86154300e-03, -0.00000000e+00],
                                   [1.89197514e-02, 1.36922176e-01, 4.83843953e-01, 9.90029850e-01, 1.23753731e+00, 9.67687907e-01, 4.79227614e-01, 1.51358011e-01, 3.06118821e-02, 4.29060333e-03]])
    StockChange_T_NormLT = np.array([0.99957094, 1.99574056, 2.97299043, 3.88177921, 4.62928667, 5.12928667, 5.38177921, 5.47299043, 5.49574056, 5.49957094])
    
    Bal = np.zeros(10)
    Bal30 = np.zeros(30)
    Time_T_30 = np.arange(0, 30)

    # Inflow/Stock for negative inflow tests
    Stock_SDM_NegInflow_NormLT = np.array([0.0,0,1,2,3,5,6,8,8,6,6,6,6,6,8,8,8,9,10,12,9,9,9,9,9,9,9,9.0,9,9])
    Stock_SDM_NegInflow_NormLTNeg = np.array([0.0,0,0,0,0,0,0,0,8,6,6,6,6,6,3,3,3,3,4,5,6,7,8,9,9,9,7.1,8,8.0,8])
    Stock_SDM_PosInflow_NormLTNeg = np.array([0.0,0,0,0,0,0,0,0,8,8,8,8.2,9,9,8.5,8,7.5,7,6.5,6,5.5,7,8,9,8.8,8.5,8.1,8,8.0,8])

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

    # For inflow_from_stock_normallyDistLifetime
    Time_T_FixedLT_XX = np.arange(1, 11, 1)
    lifetime_NormLT_X = {'Type': 'Normal', 'Mean': np.array([5]), 'StdDev': np.array([1.5])}
    InitialStock_XX = np.array([0.01, 0.01, 0.08, 0.2, 0.2, 2, 2, 3, 4, 7.50])
    Inflow_XX = np.array([2.61070664, 0.43955789, 0.87708508, 0.79210262, 0.4,
                          2.67555857, 2.20073139, 3.06983925, 4.01538044, 7.50321933])

    # For stock-driven model with initial stock
    Time_T_FixedLT_2 = np.arange(1, 10, 1)
    lifetime_NormLT_2 = {'Type': 'Normal', 'Mean': np.array([5]), 'StdDev': np.array([1.5])}
    lifetime_NormLT_4 = {'Type': 'Normal', 'Mean': np.array([7]), 'StdDev': np.array([2])} # for type split normal LT
    InitialStock_2 = np.array([3, 5, 2, 4])
    InitialStock_8 = np.array([0.5, 0.5, 0.2, 0.4, 1, 1, 1, 1])
    FutureStock_2 = np.array([0.0, 0.0, 0.0, 0.0, 18.0, 20, 20, 20, 20.0])
    ThisSwitchTime = 5 # First year with future stock curve, start counting from 1.
    
    Sc_InitialStock_2_Ref = np.array([[ 3.29968072,  0.        ,  0.        ,  0.        ,  0.        ,
                                         0.        ,  0.        ,  0.        ,  0.        ],
                                      [ 3.28845263,  5.1142035 ,  0.        ,  0.        ,  0.        ,
                                         0.        ,  0.        ,  0.        ,  0.        ],
                                      [ 3.2259967 ,  5.09680099,  2.0068288 ,  0.        ,  0.        ,
                                         0.        ,  0.        ,  0.        ,  0.        ],
                                      [ 3.00000000,  5.00000000,  2.00000000,  4.00000000,  0.        ,
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

    Sc_InitialStock_2_Ref_Sum = np.array([3.29968072, 8.40265614, 10.32962649, 14.00000000,
                                          18.00000000, 20.00000000, 20.00000000, 20.00000000, 20.00000000])

    Oc_InitialStock_2_Ref = np.array([[1.41636982e-03, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
                                      [1.12280883e-02, 2.19524375e-03, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00],
                                      [6.24559363e-02, 1.74025106e-02, 8.61420234e-04, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00],
                                      [2.25996698e-01, 9.68009922e-02, 6.82879736e-03, 1.71697802e-03, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00],
                                      [5.32405289e-01, 3.50274224e-01, 3.79849998e-02, 1.36111209e-02, 2.11801070e-03, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00],
                                      [8.17046165e-01, 8.25179532e-01, 1.37448656e-01, 7.57114903e-02, 1.67902556e-02, 1.66211031e-03, -0.00000000e+00, -0.00000000e+00, -0.00000000e+00],
                                      [8.17046165e-01, 1.26634687e+00, 3.23802924e-01, 2.73961897e-01, 9.33953405e-02, 1.31761643e-02, 1.19661751e-03, -0.00000000e+00, -0.00000000e+00],
                                      [5.32405289e-01, 1.26634687e+00, 4.96918311e-01, 6.45402188e-01, 3.37950879e-01, 7.32920558e-02, 9.48603036e-03, 1.44303487e-03, -0.00000000e+00],
                                      [2.25996698e-01, 8.25179532e-01, 4.96918311e-01, 9.90454815e-01, 7.96148072e-01, 2.65207178e-01, 5.27657861e-02, 1.14394721e-02, 1.57279902e-03]])

    I_InitialStock_2_Ref = np.array([3.30109709, 5.11639875, 2.00769022, 4.00171698, 4.93639364, 3.87383821, 2.78892598, 3.36324466, 3.66568266])
    Bal9 = np.zeros(9)

    return {
        "Time_T_FixedLT": Time_T_FixedLT,
        "Inflow_T_FixedLT": Inflow_T_FixedLT,
        "lifetime_NormLT": lifetime_NormLT,
        "lifetime_NormLT0": lifetime_NormLT0,
        "lifetime_NormLT8": lifetime_NormLT8,
        "Stock_TC_NormLT": Stock_TC_NormLT,
        "Stock_T_NormLT": Stock_T_NormLT,
        "Outflow_T_NormLT": Outflow_T_NormLT,
        "Outflow_TC_NormLT": Outflow_TC_NormLT,
        "StockChange_T_NormLT": StockChange_T_NormLT,
        "Bal": Bal, # for 10 periods
        "Bal30": Bal30, # for 30 periods
        "Time_T_30": Time_T_30,
        "Stock_SDM_NegInflow_NormLT": Stock_SDM_NegInflow_NormLT,
        "Stock_SDM_NegInflow_NormLTNeg": Stock_SDM_NegInflow_NormLTNeg,
        "Stock_SDM_PosInflow_NormLTNeg": Stock_SDM_PosInflow_NormLTNeg,
        "InflowNeg_NoCorr": InflowNeg_NoCorr,
        "InflowNeg_WithCorr": InflowNeg_WithCorr,
        "StockChange_WithCorr": StockChange_WithCorr,
        "InitialStockInflowNegNoCorr": InitialStockInflowNegNoCorrect,
        "InitialStockInflowNoNegCorr": InitialStockInflowNoNegCorrect,
        "InitialStockInflowNegCorr": InitialStockInflowNegCorrect,
        "Time_T_FixedLT_XX": Time_T_FixedLT_XX,
        "lifetime_NormLT_X": lifetime_NormLT_X,
        "InitialStock_XX": InitialStock_XX,
        "Inflow_XX": Inflow_XX,
        "Time_T_FixedLT_2": Time_T_FixedLT_2,
        "lifetime_NormLT_2": lifetime_NormLT_2,
        "lifetime_NormLT_4": lifetime_NormLT_4,
        "InitialStock_2": InitialStock_2,
        "InitialStock_8": InitialStock_8,
        "FutureStock_2": FutureStock_2,
        "ThisSwitchTime": ThisSwitchTime,
        "Sc_InitialStock_2_Ref": Sc_InitialStock_2_Ref,
        "Sc_InitialStock_2_Ref_Sum": Sc_InitialStock_2_Ref_Sum,
        "Oc_InitialStock_2_Ref": Oc_InitialStock_2_Ref,
        "I_InitialStock_2_Ref": I_InitialStock_2_Ref,
        "Bal9": Bal9, # for 9 periods
    }


@pytest.fixture(scope="module")
def weibull_lifetime_data():
    """Provides test data for Weibull distributed lifetime DSMs."""
    Time_T_FixedLT = np.arange(0, 10) # reused
    Inflow_T_FixedLT = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) # reused

    Stock_TC_WeibullLT = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0.367879441, 2, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0.100520187, 0.735758882, 3, 0, 0, 0, 0, 0, 0, 0],
                                 [0.023820879, 0.201040373, 1.103638324, 4, 0, 0, 0, 0, 0, 0],
                                 [0.005102464, 0.047641758, 0.30156056, 1.471517765, 5, 0, 0, 0, 0, 0],
                                 [0.001009149, 0.010204929, 0.071462637, 0.402080746, 1.839397206, 6, 0, 0, 0, 0],
                                 [0.000186736, 0.002018297, 0.015307393, 0.095283516, 0.502600933, 2.207276647, 7, 0, 0, 0],
                                 [3.26256E-05, 0.000373472, 0.003027446, 0.020409858, 0.119104394, 0.60312112, 2.575156088, 8, 0, 0],
                                 [5.41828E-06, 6.52513E-05, 0.000560208, 0.004036594, 0.025512322, 0.142925273, 0.703641306, 2.943035529, 9, 0],
                                 [8.59762E-07, 1.08366E-05, 9.78769E-05, 0.000746944, 0.005045743, 0.030614786, 0.166746152, 0.804161493, 3.310914971, 10]])
    Stock_T_WeibullLT = np.array([1, 2.367879441, 3.836279069, 5.328499576, 6.825822547, 8.324154666, 9.822673522, 11.321225, 12.8197819, 14.31833966])
    Outflow_T_WeibullLT = np.array([0, 0.632120559, 1.531600372, 2.507779493, 3.502677029, 4.50166788, 5.501481144, 6.501448519, 7.5014431, 8.501442241])
    Outflow_TC_WeibullLT = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0.632120559, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0.267359255, 1.264241118, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0.076699308, 0.534718509, 1.896361676, 0, 0, 0, 0, 0, 0, 0],
                                     [0.018718414, 0.153398615, 0.802077764, 2.528482235, 0, 0, 0, 0, 0, 0],
                                     [0.004093316, 0.037436829, 0.230097923, 1.069437018, 3.160602794, 0, 0, 0, 0, 0],
                                     [0.000822413, 0.008186632, 0.056155243, 0.306797231, 1.336796273, 3.792723353, 0, 0, 0, 0],
                                     [0.00015411, 0.001644825, 0.012279947, 0.074873658, 0.383496539, 1.604155527, 4.424843912, 0, 0, 0],
                                     [2.72074E-05, 0.000308221, 0.002467238, 0.016373263, 0.093592072, 0.460195846, 1.871514782, 5.056964471, 0, 0],
                                     [4.55852E-06, 5.44147E-05, 0.000462331, 0.00328965, 0.020466579, 0.112310487, 0.536895154, 2.138874037, 5.689085029, 0]])
    StockChange_T_WeibullLT = np.array([1, 1.367879441, 1.468399628, 1.492220507, 1.497322971, 1.49833212, 1.498518856, 1.498551481, 1.4985569, 1.498557759])
    
    lifetime_WeibullLT = {'Type': 'Weibull', 'Shape': np.array([1.2]), 'Scale': np.array([1])}
    InitialStock_WB = np.array([0.01, 0.01, 0.08, 0.2, 0.2, 2, 2, 3, 4, 7.50])
    Inflow_WB = np.array([11631.1250671964, 1845.6048709861, 2452.0593141014, 1071.0305279511, 198.1868742385, 391.9674590243, 83.9599583940, 29.8447516023, 10.8731273138, 7.5000000000])

    Bal = np.zeros(10)

    return {
        "Time_T_FixedLT": Time_T_FixedLT,
        "Inflow_T_FixedLT": Inflow_T_FixedLT,
        "Stock_TC_WeibullLT": Stock_TC_WeibullLT,
        "Stock_T_WeibullLT": Stock_T_WeibullLT,
        "Outflow_T_WeibullLT": Outflow_T_WeibullLT,
        "Outflow_TC_WeibullLT": Outflow_TC_WeibullLT,
        "StockChange_T_WeibullLT": StockChange_T_WeibullLT,
        "lifetime_WeibullLT": lifetime_WeibullLT,
        "InitialStock_WB": InitialStock_WB,
        "Inflow_WB": Inflow_WB,
        "Bal": Bal,
        "Time_T_FixedLT_XX": np.arange(1, 11, 1)
    }


@pytest.fixture(scope="module")
def lognormal_lifetime_data():
    """Provides test data for lognormally distributed lifetime DSMs."""
    Time_T_LN = np.arange(0, 300, 1)
    mu_dist = 20
    sg_dist = 20
    # Calculations from original code:
    # LT_LN = np.log(mu_dist / np.sqrt(1 + mu_dist * mu_dist / (sg_dist * sg_dist)))
    # SG_LN = np.sqrt(np.log(1 + mu_dist * mu_dist / (sg_dist * sg_dist)))
    lifetime_LogNorm = {'Type': 'LogNormal', 'Mean': np.array([mu_dist]), 'StdDev': np.array([sg_dist])}
    
    Inflow_LN = np.zeros(300)
    Inflow_LN[0:20] = np.array([1, 2, 3, 4, 5, 6, 7, 8, 2, 3, 5, 6, 7, 1, 2, 4, 5, 6, 7, 3])
    LN_Stock_Reference_2060 = 5.8693165260386

    return {
        "Time_T_LN": Time_T_LN,
        "lifetime_LogNorm": lifetime_LogNorm,
        "Inflow_LN": Inflow_LN,
        "LN_Stock_Reference_2060": LN_Stock_Reference_2060
    }


@pytest.fixture(scope="module")
def folded_normal_lifetime_data():
    """Provides test data for folded normally distributed lifetime DSMs."""
    Time_T_FN = np.arange(0, 100, 1)
    mu_dist = 20
    sg_dist = 20
    lifetime_FoldNorm = {'Type': 'FoldedNormal', 'Mean': np.array([mu_dist]), 'StdDev': np.array([sg_dist])}
    
    Inflow_FN = np.zeros(100)
    Inflow_FN[0:20] = np.array([1, 2, 3, 4, 5, 6, 7, 8, 2, 3, 5, 6, 7, 1, 2, 4, 5, 6, 7, 3])
    FN_Stock_Reference_2060 = 6.5004904790008300000

    return {
        "Time_T_FN": Time_T_FN,
        "lifetime_FoldNorm": lifetime_FoldNorm,
        "Inflow_FN": Inflow_FN,
        "FN_Stock_Reference_2060": FN_Stock_Reference_2060
    }

@pytest.fixture(scope="module")
def type_split_data():
    """Provides test data for type split DSMs."""
    FutureStock1 = np.array([2.8,3,3.5,4,5,5])
    FutureStock1a = np.array([0,0,0,2.8,3,3.5,4,5,5]) # Longer array for more time steps
    FutureStock2 = np.array([2.8,3,3.5,2.2,2.3,2.5])
    FutureStock2a = np.array([0,0,0,2.8,3,3.5,2.2,2.3,2.5]) # Longer array
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
                                       [0.1138340956232945,1.024506860965],
                                       [0.6134536124575378,0.6134536124575378],
                                       [1.459402923878064,0.3648507309695161],
                                       [0.5136958913485281,0.5136958913485281]])

    TypeSplitInitialStockInflowCorrect1StockCheck = np.array([[0,0],[0,0],[0.5,1],
                                                              [0.3908625698550751,0.7817251397101502],
                                                              [0.2957996369747763,0.5915992739495526],
                                                              [0.2324798530180466,0.4649597060360933],
                                                              [0.1882452627129519,0.3764905254259038],
                                                              [0.1559267249296865,0.311853449859373],
                                                              [0.1314683082705697,0.2629366165411394]])
    TypeSplitInitialStockInflowCorrect2StockCheck = np.array([[0,0],[0,0],[0.5,1],
                                                              [0.3908625698550751,0.7817251397101502],
                                                              [0.2957996369747763,0.5915992739495526],
                                                              [0.2324798530180466,0.4649597060360933],
                                                              [0.1882452627129519,0.3764905254259038],
                                                              [0.1559267249296865,0.311853449859373],
                                                              [0.1314683082705697,0.2629366165411394]])
    TypeSplitInitialStockInflowCorrect3StockCheck = np.array([[0,0],[0,0],[0.5,1],
                                                              [0.3908625698550751,0.7817251397101502],
                                                              [0.2957996369747763,0.5915992739495526],
                                                              [0.2324798530180466,0.4649597060360933],
                                                              [0.1493421286476113,0.2986842572952226],
                                                              [0.123702603074578,0.247405206149156],
                                                              [0.1042988106254021,0.2085976212508043]])
    
    return {
        "FutureStock1": FutureStock1, "FutureStock1a": FutureStock1a,
        "FutureStock2": FutureStock2, "FutureStock2a": FutureStock2a,
        "InitialStock1": InitialStock1, "InitialStock2": InitialStock2,
        "TypeSplit1": TypeSplit1, "TypeSplit1a": TypeSplit1a, "TypeSplit2a": TypeSplit2a,
        "TypeSplitStockCheckType1": TypeSplitStockCheckType1,
        "TypeSplitStockCheckType2": TypeSplitStockCheckType2,
        "TypeSplitInflowCheckType": TypeSplitInflowCheckType,
        "TypeSplitInitialStockInflowCorrect1StockCheck": TypeSplitInitialStockInflowCorrect1StockCheck,
        "TypeSplitInitialStockInflowCorrect2StockCheck": TypeSplitInitialStockInflowCorrect2StockCheck,
        "TypeSplitInitialStockInflowCorrect3StockCheck": TypeSplitInitialStockInflowCorrect3StockCheck,
    }


@pytest.fixture(scope="module")
def dsm_instances(fixed_lifetime_data, normal_lifetime_data, weibull_lifetime_data, lognormal_lifetime_data, folded_normal_lifetime_data, type_split_data):
    """Initializes and returns all DynamicStockModel instances."""
    data_f = fixed_lifetime_data
    data_n = normal_lifetime_data
    data_w = weibull_lifetime_data
    data_l = lognormal_lifetime_data
    data_fn = folded_normal_lifetime_data
    data_ts = type_split_data

    dsms = {}

    # For zero lifetime: border case
    dsms["myDSM0"] = dsm.DynamicStockModel(t=data_f["Time_T_FixedLT"], i=data_f["Inflow_T_FixedLT"], lt=data_f["lifetime_FixedLT0"])

    # For fixed LT
    dsms["myDSM"] = dsm.DynamicStockModel(t=data_f["Time_T_FixedLT"], i=data_f["Inflow_T_FixedLT"], lt=data_f["lifetime_FixedLT"])
    dsms["myDSM2"] = dsm.DynamicStockModel(t=data_f["Time_T_FixedLT"], s=data_f["Stock_T_FixedLT"], lt=data_f["lifetime_FixedLT"])

    dsms["myDSMx"] = dsm.DynamicStockModel(t=data_f["Time_T_FixedLT_X"], lt=data_f["lifetime_FixedLT_X"])
    TestInflow_X = dsms["myDSMx"].compute_i_from_s(InitialStock=data_f["InitialStock_X"])
    dsms["myDSMxy"] = dsm.DynamicStockModel(t=data_f["Time_T_FixedLT_X"], i=TestInflow_X, lt=data_f["lifetime_FixedLT_X"])
    dsms["TestInflow_X"] = TestInflow_X

    # For zero normally distributed lifetime: border case
    dsms["myDSM0n"] = dsm.DynamicStockModel(t=data_n["Time_T_FixedLT"], i=data_n["Inflow_T_FixedLT"], lt=data_n["lifetime_NormLT0"])

    # For normally distributed Lt
    dsms["myDSM3"] = dsm.DynamicStockModel(t=data_n["Time_T_FixedLT"], i=data_n["Inflow_T_FixedLT"], lt=data_n["lifetime_NormLT"])
    dsms["myDSM4"] = dsm.DynamicStockModel(t=data_n["Time_T_FixedLT"], s=data_n["Stock_T_NormLT"], lt=data_n["lifetime_NormLT"])
    dsms["myDSM4a"] = dsm.DynamicStockModel(t=data_n["Time_T_FixedLT"], s=data_n["Stock_T_NormLT"], lt=data_n["lifetime_NormLT"])

    dsms["myDSMX"] = dsm.DynamicStockModel(t=data_n["Time_T_FixedLT_XX"], lt=data_n["lifetime_NormLT_X"])
    TestInflow_XX = dsms["myDSMX"].compute_i_from_s(InitialStock=data_n["InitialStock_XX"])
    dsms["myDSMXY"] = dsm.DynamicStockModel(t=data_n["Time_T_FixedLT_XX"], i=TestInflow_XX, lt=data_n["lifetime_NormLT_X"])
    dsms["TestInflow_XX"] = TestInflow_XX

    # For negative inflow correction 
    dsms["myDSM_ICF"] = dsm.DynamicStockModel(t=data_n["Time_T_30"], s=data_n["Stock_SDM_NegInflow_NormLT"], lt=data_n["lifetime_NormLT8"])
    dsms["myDSM_ICT"] = dsm.DynamicStockModel(t=data_n["Time_T_30"], s=data_n["Stock_SDM_NegInflow_NormLT"], lt=data_n["lifetime_NormLT8"])

    # For negative inflow correction with initial stock
    dsms["myDSM_ICFIS"] = dsm.DynamicStockModel(t=data_n["Time_T_30"], s=data_n["Stock_SDM_NegInflow_NormLTNeg"].copy(), lt=data_n["lifetime_NormLT8"])
    dsms["myDSM_ICTIST"] = dsm.DynamicStockModel(t=data_n["Time_T_30"], s=data_n["Stock_SDM_PosInflow_NormLTNeg"].copy(), lt=data_n["lifetime_NormLT8"])
    dsms["myDSM_ICTIS"] = dsm.DynamicStockModel(t=data_n["Time_T_30"], s=data_n["Stock_SDM_NegInflow_NormLTNeg"].copy(), lt=data_n["lifetime_NormLT8"])

    # Test compute_stock_driven_model_initialstock
    dsms["TestDSM_IntitialStock"] = dsm.DynamicStockModel(t=data_n["Time_T_FixedLT_2"], s=data_n["FutureStock_2"], lt=data_n["lifetime_NormLT_2"])
    Sc_InitialStock_2, Oc_InitialStock_2, I_InitialStock_2 = dsms["TestDSM_IntitialStock"].compute_stock_driven_model_initialstock(InitialStock=data_n["InitialStock_2"], SwitchTime=data_n["ThisSwitchTime"])
    dsms["Sc_InitialStock_2"] = Sc_InitialStock_2
    dsms["Oc_InitialStock_2"] = Oc_InitialStock_2
    dsms["I_InitialStock_2"] = I_InitialStock_2

    # Test stock-driven model with initialstock and type split (lognormal lifetime)
    lifetime_LogNorm_TS = {'Type': 'LogNormal', 'Mean': np.array([6]), 'StdDev': np.array([3])} # Defined locally as it wasn't in main fixtures
    dsms["TestDSM_IntitialStockTypeSplit"] = dsm.DynamicStockModel(t=data_n["Time_T_FixedLT_2"], s=data_ts["FutureStock1"], lt=lifetime_LogNorm_TS)
    dsms["SFArrayCombined_TS"] = dsms["TestDSM_IntitialStockTypeSplit"].compute_sf().copy()

    dsms["TestDSM_IntitialStockTypeSplit1"] = dsm.DynamicStockModel(t=data_n["Time_T_FixedLT_2"], s=data_ts["FutureStock1a"].copy(), lt=lifetime_LogNorm_TS)
    dsms["SFArrayCombined_TS1"] = dsms["TestDSM_IntitialStockTypeSplit1"].compute_sf().copy()

    dsms["TestDSM_IntitialStockTypeSplit2"] = dsm.DynamicStockModel(t=data_n["Time_T_FixedLT_2"], s=data_ts["FutureStock2a"].copy(), lt=lifetime_LogNorm_TS)
    dsms["SFArrayCombined_TS2"] = dsms["TestDSM_IntitialStockTypeSplit2"].compute_sf().copy()

    dsms["TestDSM_IntitialStockTypeSplit3"] = dsm.DynamicStockModel(t=data_n["Time_T_FixedLT_2"], s=data_ts["FutureStock2a"].copy(), lt=lifetime_LogNorm_TS)
    dsms["SFArrayCombined_TS3"] = dsms["TestDSM_IntitialStockTypeSplit3"].compute_sf().copy()

    # Test stock-driven model with initialstock and type split and NegativeInflowCorrect, normal lifetime
    dsms["TestDSM_IntitialStockTypeSplit1a"] = dsm.DynamicStockModel(t=data_n["Time_T_30"], s=data_n["Stock_SDM_PosInflow_NormLTNeg"].copy(), lt=data_n["lifetime_NormLT_4"])
    dsms["SFArrayCombineda_TS1a"] = dsms["TestDSM_IntitialStockTypeSplit1a"].compute_sf().copy()

    dsms["TestDSM_IntitialStockTypeSplit2a"] = dsm.DynamicStockModel(t=data_n["Time_T_30"], s=data_n["Stock_SDM_NegInflow_NormLTNeg"].copy(), lt=data_n["lifetime_NormLT_4"])
    dsms["SFArrayCombineda_TS2a"] = dsms["TestDSM_IntitialStockTypeSplit2a"].compute_sf().copy()

    dsms["TestDSM_IntitialStockTypeSplit3a"] = dsm.DynamicStockModel(t=data_n["Time_T_30"], s=data_n["Stock_SDM_NegInflow_NormLTNeg"].copy(), lt=data_n["lifetime_NormLT_4"])
    dsms["SFArrayCombineda_TS3a"] = dsms["TestDSM_IntitialStockTypeSplit3a"].compute_sf().copy()

    # Compute stock back from inflow
    dsms["TestDSM_IntitialStock_Verify"] = dsm.DynamicStockModel(t=data_n["Time_T_FixedLT_2"], i=I_InitialStock_2, lt=data_n["lifetime_NormLT_2"])

    # For Weibull-distributed Lt
    dsms["myDSMWB1"] = dsm.DynamicStockModel(t=data_w["Time_T_FixedLT"], i=data_w["Inflow_T_FixedLT"], lt=data_w["lifetime_WeibullLT"])
    dsms["myDSMWB2"] = dsm.DynamicStockModel(t=data_w["Time_T_FixedLT"], s=data_w["Stock_T_WeibullLT"], lt=data_w["lifetime_WeibullLT"])
    
    dsms["myDSMWB3"] = dsm.DynamicStockModel(t=data_w["Time_T_FixedLT_XX"], lt=data_w["lifetime_WeibullLT"])
    TestInflow_WB = dsms["myDSMWB3"].compute_i_from_s(InitialStock=data_w["InitialStock_WB"])
    dsms["myDSMWB4"] = dsm.DynamicStockModel(t=data_w["Time_T_FixedLT_XX"], i=TestInflow_WB, lt=data_w["lifetime_WeibullLT"])
    dsms["TestInflow_WB"] = TestInflow_WB

    # Test lognormal lifetime dist.
    dsms["myDSM_LN"] = dsm.DynamicStockModel(t=data_l["Time_T_LN"], i=data_l["Inflow_LN"], lt=data_l["lifetime_LogNorm"])

    # Test folded normal lifetime dist.
    dsms["myDSM_FN"] = dsm.DynamicStockModel(t=data_fn["Time_T_FN"], i=data_fn["Inflow_FN"], lt=data_fn["lifetime_FoldNorm"])

    # Test that outflow computed with pdf from compute_outflow_pdf() yields same result as the one calculated directly from the sf via compute_s_c_inflow_driven() and compute_o_c_from_s_c()
    lt_pdf = {'Type': 'Normal', 'Mean': np.array([8]), 'StdDev': np.array([3])}
    ifl_pdf = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5])
    dsms["DSM_pdf"] = dsm.DynamicStockModel(t=np.arange(0, 25, 1), i=ifl_pdf, lt=lt_pdf)
    dsms["ifl_pdf"] = ifl_pdf

    return dsms


#  Test Functions 


## Fixed Lifetime Model Tests

def test_inflow_driven_model_fixedLifetime_0(dsm_instances, fixed_lifetime_data):
    """Test Inflow Driven Model with Fixed product lifetime of 0."""
    myDSM0 = dsm_instances["myDSM0"]
    data_f = fixed_lifetime_data
    assert np.allclose(myDSM0.compute_s_c_inflow_driven(), np.zeros(data_f["Stock_TC_FixedLT"].shape))
    assert np.allclose(myDSM0.compute_stock_total(), np.zeros(data_f["Stock_TC_FixedLT"].shape[0]))
    assert np.allclose(myDSM0.compute_stock_change(), np.zeros(data_f["Stock_TC_FixedLT"].shape[0]))
    assert np.allclose(myDSM0.compute_outflow_mb(), data_f["Inflow_T_FixedLT"])
    assert np.allclose(myDSM0.check_stock_balance(), data_f["Bal"])

def test_inflow_driven_model_fixedLifetime(dsm_instances, fixed_lifetime_data):
    """Test Inflow Driven Model with Fixed product lifetime."""
    myDSM = dsm_instances["myDSM"]
    data_f = fixed_lifetime_data
    assert np.allclose(myDSM.compute_s_c_inflow_driven(), data_f["Stock_TC_FixedLT"])
    assert np.allclose(myDSM.compute_stock_total(), data_f["Stock_T_FixedLT"])
    assert np.allclose(myDSM.compute_o_c_from_s_c(), data_f["Outflow_TC_FixedLT"])
    assert np.allclose(myDSM.compute_outflow_total(), data_f["Outflow_T_FixedLT"])
    assert np.allclose(myDSM.compute_stock_change(), data_f["StockChange_T_FixedLT"])
    assert np.allclose(myDSM.check_stock_balance(), data_f["Bal"])

def test_stock_driven_model_fixedLifetime(dsm_instances, fixed_lifetime_data):
    """Test Stock Driven Model with Fixed product lifetime."""
    myDSM2 = dsm_instances["myDSM2"]
    data_f = fixed_lifetime_data
    stock_c, outflow_c, inflow = myDSM2.compute_stock_driven_model()
    assert np.allclose(stock_c, data_f["Stock_TC_FixedLT"])
    assert np.allclose(outflow_c, data_f["Outflow_TC_FixedLT"])
    assert np.allclose(inflow, data_f["Inflow_T_FixedLT"])
    assert np.allclose(myDSM2.compute_outflow_total(), data_f["Outflow_T_FixedLT"])
    assert np.allclose(myDSM2.compute_stock_change(), data_f["StockChange_T_FixedLT"])
    assert np.allclose(myDSM2.check_stock_balance(), data_f["Bal"])


## Normally Distributed Lifetime Model Tests

def test_inflow_driven_model_normallyDistrLifetime_0(dsm_instances, normal_lifetime_data):
    """Test Inflow Driven Model with Normally distributed product lifetime with Mean 0."""
    myDSM0n = dsm_instances["myDSM0n"]
    data_n = normal_lifetime_data
    assert np.allclose(myDSM0n.compute_s_c_inflow_driven(), np.zeros(data_n["Stock_TC_NormLT"].shape))
    assert np.allclose(myDSM0n.compute_stock_total(), np.zeros(data_n["Stock_TC_NormLT"].shape[0]))
    assert np.allclose(myDSM0n.compute_stock_change(), np.zeros(data_n["Stock_TC_NormLT"].shape[0]))
    assert np.allclose(myDSM0n.compute_outflow_mb(), data_n["Inflow_T_FixedLT"])
    assert np.allclose(myDSM0n.check_stock_balance(), data_n["Bal"])

def test_inflow_driven_model_normallyDistLifetime(dsm_instances, normal_lifetime_data):
    """Test Inflow Driven Model with normally distributed product lifetime."""
    myDSM3 = dsm_instances["myDSM3"]
    data_n = normal_lifetime_data
    assert np.allclose(myDSM3.compute_s_c_inflow_driven(), data_n["Stock_TC_NormLT"], atol=1e-8)
    assert np.allclose(myDSM3.compute_stock_total(), data_n["Stock_T_NormLT"], atol=1e-8)
    assert np.allclose(myDSM3.compute_o_c_from_s_c(), data_n["Outflow_TC_NormLT"], atol=1e-8)
    assert np.allclose(myDSM3.compute_outflow_total(), data_n["Outflow_T_NormLT"], atol=1e-8)
    assert np.allclose(myDSM3.compute_stock_change(), data_n["StockChange_T_NormLT"], atol=1e-8)
    assert np.allclose(myDSM3.check_stock_balance(), data_n["Bal"], atol=1e-12)

def test_stock_driven_model_normallyDistLifetime(dsm_instances, normal_lifetime_data):
    """Test Stock Driven Model with normally distributed product lifetime."""
    myDSM4 = dsm_instances["myDSM4"]
    data_n = normal_lifetime_data
    stock_c, outflow_c, inflow = myDSM4.compute_stock_driven_model()
    assert np.allclose(stock_c, data_n["Stock_TC_NormLT"], atol=1e-8)
    assert np.allclose(outflow_c, data_n["Outflow_TC_NormLT"], atol=1e-8)
    assert np.allclose(inflow, data_n["Inflow_T_FixedLT"], atol=1e-8)
    assert np.allclose(myDSM4.compute_outflow_total(), data_n["Outflow_T_NormLT"], atol=1e-8)
    assert np.allclose(myDSM4.compute_stock_change(), data_n["StockChange_T_NormLT"], atol=1e-8)
    assert np.allclose(myDSM4.check_stock_balance(), data_n["Bal"], atol=1e-12)

def test_stock_driven_model_normallyDistLifetime_NegInflowFlagTrue(dsm_instances, normal_lifetime_data):
    """Test Stock Driven Model with normally distributed product lifetime.
    Set the NegativeInflowCorrect flag as True but use a test case without negative inflows."""
    myDSM4a = dsm_instances["myDSM4a"]
    data_n = normal_lifetime_data
    stock_c, outflow_c, inflow = myDSM4a.compute_stock_driven_model(NegativeInflowCorrect=True)
    assert np.allclose(stock_c, data_n["Stock_TC_NormLT"], atol=1e-8)
    assert np.allclose(outflow_c, data_n["Outflow_TC_NormLT"], atol=1e-8)
    assert np.allclose(inflow, data_n["Inflow_T_FixedLT"], atol=1e-8)
    assert np.allclose(myDSM4a.compute_outflow_total(), data_n["Outflow_T_NormLT"], atol=1e-8)
    assert np.allclose(myDSM4a.compute_stock_change(), data_n["StockChange_T_NormLT"], atol=1e-8)
    assert np.allclose(myDSM4a.check_stock_balance(), data_n["Bal"], atol=1e-12)

def test_stock_driven_model_normallyDistLifetime_NegInflow(dsm_instances, normal_lifetime_data):
    """Test Stock Driven Model with normally distributed product lifetime, with negative inflow."""
    myDSM_ICF = dsm_instances["myDSM_ICF"]
    myDSM_ICT = dsm_instances["myDSM_ICT"]
    data_n = normal_lifetime_data
    _, _, I1 = myDSM_ICF.compute_stock_driven_model(NegativeInflowCorrect=False)
    _, _, I2 = myDSM_ICT.compute_stock_driven_model(NegativeInflowCorrect=True)
    assert np.allclose(I1, data_n["InflowNeg_NoCorr"], atol=1e-12)
    assert np.allclose(I2, data_n["InflowNeg_WithCorr"], atol=1e-12)
    assert np.allclose(myDSM_ICT.compute_stock_change(), data_n["StockChange_WithCorr"], atol=1e-12)
    assert np.allclose(myDSM_ICT.check_stock_balance(), data_n["Bal30"], atol=1e-12)

def test_stock_driven_model_Initialstock_NegInflow(dsm_instances, normal_lifetime_data):
    """Test Stock Driven Model with normally distributed product lifetime, initial stock, with negative inflow and no negative inflow correction."""
    myDSM_ICFIS = dsm_instances["myDSM_ICFIS"]
    data_n = normal_lifetime_data
    _, _, I1IS = myDSM_ICFIS.compute_stock_driven_model_initialstock(InitialStock=data_n["InitialStock_8"], SwitchTime=9, NegativeInflowCorrect=False)
    assert np.allclose(myDSM_ICFIS.check_stock_balance(), data_n["Bal30"], atol=1e-12)
    assert np.allclose(I1IS, data_n["InitialStockInflowNegNoCorr"], atol=1e-12)

def test_stock_driven_model_Initialstock_NegInflowNotUsed(dsm_instances, normal_lifetime_data):
    """Test Stock Driven Model with normally distributed product lifetime, initial stock, with no negative inflow and no negative inflow correction."""
    myDSM_ICTIST = dsm_instances["myDSM_ICTIST"]
    data_n = normal_lifetime_data
    _, _, I3IS = myDSM_ICTIST.compute_stock_driven_model_initialstock(InitialStock=data_n["InitialStock_8"], SwitchTime=9, NegativeInflowCorrect=False)
    assert np.allclose(myDSM_ICTIST.check_stock_balance(), data_n["Bal30"], atol=1e-12)
    assert np.allclose(I3IS, data_n["InitialStockInflowNoNegCorr"], atol=1e-12)

def test_stock_driven_model_Initialstock_NegInflowFixed(dsm_instances, normal_lifetime_data):
    """Test Stock Driven Model with normally distributed product lifetime, initial stock, with negative inflow and negative inflow correction."""
    myDSM_ICTIS = dsm_instances["myDSM_ICTIS"]
    data_n = normal_lifetime_data
    _, _, I2IS = myDSM_ICTIS.compute_stock_driven_model_initialstock(InitialStock=data_n["InitialStock_8"], SwitchTime=9, NegativeInflowCorrect=True)
    assert np.allclose(myDSM_ICTIS.check_stock_balance(), data_n["Bal30"], atol=1e-12)
    assert np.allclose(I2IS, data_n["InitialStockInflowNegCorrect"], atol=1e-12)


## Type Split Model Tests

def test_stock_driven_model_Initialstock_NegInflow_TypeSplit_NotUsed(dsm_instances, normal_lifetime_data, type_split_data):
    """Test Stock Driven Model with lognormally distributed product lifetime, initial stock, typesplit, with negative inflow correction but no negative inflow occurring."""
    TestDSM_IntitialStockTypeSplit1 = dsm_instances["TestDSM_IntitialStockTypeSplit1"]
    SFArrayCombined = dsm_instances["SFArrayCombined_TS1"]
    data_n = normal_lifetime_data
    data_ts = type_split_data
    SC_IS_TS1, _, _, _ = TestDSM_IntitialStockTypeSplit1.compute_stock_driven_model_initialstock_typesplit_negativeinflowcorrect(
        SwitchTime=3, InitialStock=data_ts["InitialStock1"], SFArrayCombined=np.einsum('tc,g->tcg', SFArrayCombined, np.ones(2)),
        TypeSplit=data_ts["TypeSplit1a"], NegativeInflowCorrect=True
    )
    assert np.allclose(TestDSM_IntitialStockTypeSplit1.check_stock_balance(), data_n["Bal9"], atol=1e-12)
    assert np.allclose(SC_IS_TS1[:, 2, :], data_ts["TypeSplitInitialStockInflowCorrect1StockCheck"], atol=1e-12)

def test_stock_driven_model_Initialstock_NegInflow_TypeSplit_NoCorr(dsm_instances, normal_lifetime_data, type_split_data):
    """Test Stock Driven Model with lognormally distributed product lifetime, initial stock, typesplit, with negative inflow correction of but negative inflow occurring."""
    TestDSM_IntitialStockTypeSplit2 = dsm_instances["TestDSM_IntitialStockTypeSplit2"]
    SFArrayCombined = dsm_instances["SFArrayCombined_TS2"]
    data_n = normal_lifetime_data
    data_ts = type_split_data
    SC_IS_TS2, _, _, _ = TestDSM_IntitialStockTypeSplit2.compute_stock_driven_model_initialstock_typesplit_negativeinflowcorrect(
        SwitchTime=3, InitialStock=data_ts["InitialStock1"], SFArrayCombined=np.einsum('tc,g->tcg', SFArrayCombined, np.ones(2)),
        TypeSplit=data_ts["TypeSplit1a"], NegativeInflowCorrect=False
    )
    assert np.allclose(TestDSM_IntitialStockTypeSplit2.check_stock_balance(), data_n["Bal9"], atol=1e-12)
    assert np.allclose(SC_IS_TS2[:, 2, :], data_ts["TypeSplitInitialStockInflowCorrect2StockCheck"], atol=1e-12)

def test_stock_driven_model_Initialstock_NegInflow_TypeSplit_Corr(dsm_instances, normal_lifetime_data, type_split_data):
    """Test Stock Driven Model with lognormally distributed product lifetime, initial stock, typesplit, with negative inflow correction on and negative inflow occurring and corrected."""
    TestDSM_IntitialStockTypeSplit3 = dsm_instances["TestDSM_IntitialStockTypeSplit3"]
    SFArrayCombined = dsm_instances["SFArrayCombined_TS3"]
    data_n = normal_lifetime_data
    data_ts = type_split_data
    SC_IS_TS3, _, _, _ = TestDSM_IntitialStockTypeSplit3.compute_stock_driven_model_initialstock_typesplit_negativeinflowcorrect(
        SwitchTime=3, InitialStock=data_ts["InitialStock1"], SFArrayCombined=np.einsum('tc,g->tcg', SFArrayCombined, np.ones(2)),
        TypeSplit=data_ts["TypeSplit1a"], NegativeInflowCorrect=True
    )
    assert np.allclose(TestDSM_IntitialStockTypeSplit3.check_stock_balance(), data_n["Bal9"], atol=1e-12)
    assert np.allclose(SC_IS_TS3[:, 2, :], data_ts["TypeSplitInitialStockInflowCorrect3StockCheck"], atol=1e-12)

def test_stock_driven_model_Initialstock_NegInflow_TypeSplit_NotUsed_NormalLT(dsm_instances, normal_lifetime_data, type_split_data):
    """Test Stock Driven Model with normally distributed product lifetime, initial stock, typesplit, with negative inflow correction but no negative inflow occurring."""
    TestDSM_IntitialStockTypeSplit1a = dsm_instances["TestDSM_IntitialStockTypeSplit1a"]
    SFArrayCombineda = dsm_instances["SFArrayCombineda_TS1a"]
    data_n = normal_lifetime_data
    data_ts = type_split_data
    _, _, _, _ = TestDSM_IntitialStockTypeSplit1a.compute_stock_driven_model_initialstock_typesplit_negativeinflowcorrect(
        SwitchTime=8, InitialStock=data_ts["InitialStock2"], SFArrayCombined=np.einsum('tc,g->tcg', SFArrayCombineda, np.ones(2)),
        TypeSplit=data_ts["TypeSplit2a"], NegativeInflowCorrect=True
    )
    assert np.allclose(TestDSM_IntitialStockTypeSplit1a.check_stock_balance(), data_n["Bal30"], atol=1e-12)

def test_stock_driven_model_Initialstock_NegInflow_TypeSplit_NoCorr_NormalLT(dsm_instances, normal_lifetime_data, type_split_data):
    """Test Stock Driven Model with normally distributed product lifetime, initial stock, typesplit, with negative inflow correction of but negative inflow occurring."""
    TestDSM_IntitialStockTypeSplit2a = dsm_instances["TestDSM_IntitialStockTypeSplit2a"]
    SFArrayCombineda = dsm_instances["SFArrayCombineda_TS2a"]
    data_n = normal_lifetime_data
    data_ts = type_split_data
    _, _, _, _ = TestDSM_IntitialStockTypeSplit2a.compute_stock_driven_model_initialstock_typesplit_negativeinflowcorrect(
        SwitchTime=8, InitialStock=data_ts["InitialStock2"], SFArrayCombined=np.einsum('tc,g->tcg', SFArrayCombineda, np.ones(2)),
        TypeSplit=data_ts["TypeSplit2a"], NegativeInflowCorrect=False
    )
    assert np.allclose(TestDSM_IntitialStockTypeSplit2a.check_stock_balance(), data_n["Bal30"], atol=1e-12)

def test_stock_driven_model_Initialstock_NegInflow_TypeSplit_Corr_NormalLT(dsm_instances, normal_lifetime_data, type_split_data):
    """Test Stock Driven Model with normally distributed product lifetime, initial stock, typesplit, with negative inflow correction on and negative inflow occurring and corrected."""
    TestDSM_IntitialStockTypeSplit3a = dsm_instances["TestDSM_IntitialStockTypeSplit3a"]
    SFArrayCombineda = dsm_instances["SFArrayCombineda_TS3a"]
    data_n = normal_lifetime_data
    data_ts = type_split_data
    _, _, _, _ = TestDSM_IntitialStockTypeSplit3a.compute_stock_driven_model_initialstock_typesplit_negativeinflowcorrect(
        SwitchTime=8, InitialStock=data_ts["InitialStock2"], SFArrayCombined=np.einsum('tc,g->tcg', SFArrayCombineda, np.ones(2)),
        TypeSplit=data_ts["TypeSplit2a"], NegativeInflowCorrect=True
    )
    assert np.allclose(TestDSM_IntitialStockTypeSplit3a.check_stock_balance(), data_n["Bal30"], atol=1e-12)

def test_stock_driven_model_Initialstock_TypeSplit(dsm_instances, normal_lifetime_data, type_split_data):
    """Test Stock Driven Model with lognormally distributed product lifetime, initial stock, and type split."""
    TestDSM_IntitialStockTypeSplit = dsm_instances["TestDSM_IntitialStockTypeSplit"]
    SFArrayCombined = dsm_instances["SFArrayCombined_TS"]
    data_n = normal_lifetime_data
    data_ts = type_split_data
    # check_stock_balance for this particular setup has a non-zero first element in the original.
    # The original test checked [1::] which implies the first element is expected to be different.
    assert np.allclose(TestDSM_IntitialStockTypeSplit.check_stock_balance()[1:], np.zeros(5), atol=1e-12)
    SC_IS_TS, _, I_IS_TS = TestDSM_IntitialStockTypeSplit.compute_stock_driven_model_initialstock_typesplit(
        FutureStock=data_ts["FutureStock1"], InitialStock=data_ts["InitialStock1"],
        SFArrayCombined=np.einsum('tc,g->tcg', SFArrayCombined, np.ones(2)), TypeSplit=data_ts["TypeSplit1"]
    )
    assert np.allclose(SC_IS_TS[4, :, 0], data_ts["TypeSplitStockCheckType1"], atol=1e-12)
    assert np.allclose(SC_IS_TS[4, :, 1], data_ts["TypeSplitStockCheckType2"], atol=1e-12)
    assert np.allclose(I_IS_TS, data_ts["TypeSplitInflowCheckType"], atol=1e-12)


## Weibull Distributed Lifetime Model Tests

def test_inflow_driven_model_WeibullDistLifetime(dsm_instances, weibull_lifetime_data, fixed_lifetime_data):
    """Test Inflow Driven Model with Weibull-distributed product lifetime."""
    myDSMWB1 = dsm_instances["myDSMWB1"]
    data_w = weibull_lifetime_data
    data_f = fixed_lifetime_data # For Bal (zeros array)
    assert np.allclose(myDSMWB1.compute_s_c_inflow_driven(), data_w["Stock_TC_WeibullLT"], atol=1e-9)
    assert np.allclose(myDSMWB1.compute_stock_total(), data_w["Stock_T_WeibullLT"], atol=1e-8)
    assert np.allclose(myDSMWB1.compute_o_c_from_s_c(), data_w["Outflow_TC_WeibullLT"], atol=1e-9)
    assert np.allclose(myDSMWB1.compute_outflow_total(), data_w["Outflow_T_WeibullLT"], atol=1e-9)
    assert np.allclose(myDSMWB1.compute_stock_change(), data_w["StockChange_T_WeibullLT"], atol=1e-9)
    assert np.allclose(myDSMWB1.check_stock_balance(), data_f["Bal"], atol=1e-12)

def test_stock_driven_model_WeibullDistLifetime(dsm_instances, weibull_lifetime_data, fixed_lifetime_data):
    """Test Stock Driven Model with Weibull-distributed product lifetime."""
    myDSMWB1 = dsm_instances["myDSMWB1"] # Reused myDSMWB1 for stock-driven comparison as in original
    data_w = weibull_lifetime_data
    data_f = fixed_lifetime_data # For Bal (zeros array)
    stock_c, outflow_c, inflow = myDSMWB1.compute_stock_driven_model()
    assert np.allclose(stock_c, data_w["Stock_TC_WeibullLT"], atol=1e-8)
    assert np.allclose(outflow_c, data_w["Outflow_TC_WeibullLT"], atol=1e-8)
    assert np.allclose(inflow, data_w["Inflow_T_FixedLT"], atol=1e-8)
    assert np.allclose(myDSMWB1.compute_outflow_total(), data_w["Outflow_T_WeibullLT"], atol=1e-9)
    assert np.allclose(myDSMWB1.compute_stock_change(), data_w["StockChange_T_WeibullLT"], atol=1e-8)
    assert np.allclose(myDSMWB1.check_stock_balance(), data_f["Bal"], atol=1e-12)


## Inflow from Stock Computations Tests

def test_inflow_from_stock_fixedLifetime(dsm_instances, fixed_lifetime_data):
    """Test computation of inflow from stock with Fixed product lifetime."""
    myDSMxy = dsm_instances["myDSMxy"]
    TestInflow_X = dsm_instances["TestInflow_X"]
    data_f = fixed_lifetime_data
    assert np.allclose(TestInflow_X, data_f["Inflow_X"])
    assert np.allclose(myDSMxy.compute_s_c_inflow_driven()[-1, :], data_f["InitialStock_X"])

def test_inflow_from_stock_normallyDistLifetime(dsm_instances, normal_lifetime_data):
    """Test computation of inflow from stock with normally distributed product lifetime."""
    myDSMXY = dsm_instances["myDSMXY"]
    TestInflow_XX = dsm_instances["TestInflow_XX"]
    data_n = normal_lifetime_data
    assert np.allclose(TestInflow_XX, data_n["Inflow_XX"], atol=1e-8)
    assert np.allclose(myDSMXY.compute_s_c_inflow_driven()[-1, :], data_n["InitialStock_XX"], atol=1e-9)

def test_inflow_from_stock_WeibullDistLifetime(dsm_instances, weibull_lifetime_data):
    """Test computation of inflow from stock with Weibull-distributed product lifetime."""
    myDSMWB4 = dsm_instances["myDSMWB4"]
    TestInflow_WB = dsm_instances["TestInflow_WB"]
    data_w = weibull_lifetime_data
    assert np.allclose(TestInflow_WB, data_w["Inflow_WB"], atol=1e-6)
    assert np.allclose(myDSMWB4.compute_s_c_inflow_driven()[-1, :], data_w["InitialStock_WB"], atol=1e-8)

def test_compute_stock_driven_model_initialstock(dsm_instances, normal_lifetime_data):
    """Test stock-driven model with initial stock given."""
    data_n = normal_lifetime_data
    Sc_InitialStock_2 = dsm_instances["Sc_InitialStock_2"]
    Oc_InitialStock_2 = dsm_instances["Oc_InitialStock_2"]
    I_InitialStock_2 = dsm_instances["I_InitialStock_2"]

    assert np.allclose(I_InitialStock_2, data_n["I_InitialStock_2_Ref"], atol=1e-8)
    assert np.allclose(Sc_InitialStock_2, data_n["Sc_InitialStock_2_Ref"], atol=1e-8)
    assert np.allclose(Sc_InitialStock_2.sum(axis=1), data_n["Sc_InitialStock_2_Ref_Sum"], atol=1e-8)
    assert np.allclose(Oc_InitialStock_2, data_n["Oc_InitialStock_2_Ref"], atol=1e-8)


## Specific Lifetime Distribution Tests

def test_stock_from_inflow_LogNormalDistLifetime(dsm_instances, lognormal_lifetime_data):
    """Test computation of stock from inflow for lognormally distributed product lifetime."""
    myDSM_LN = dsm_instances["myDSM_LN"]
    data_l = lognormal_lifetime_data
    LN_Stock = myDSM_LN.compute_s_c_inflow_driven()
    LN_Stock_60 = LN_Stock.sum(axis=1)
    assert np.allclose(LN_Stock_60[60], data_l["LN_Stock_Reference_2060"], atol=1e-9)

def test_stock_from_inflow_FoldedNormalDistLifetime(dsm_instances, folded_normal_lifetime_data):
    """Test computation of stock from inflow for folded normally distributed product lifetime."""
    myDSM_FN = dsm_instances["myDSM_FN"]
    data_fn = folded_normal_lifetime_data
    FN_Stock = myDSM_FN.compute_s_c_inflow_driven()
    FN_Stock_60 = FN_Stock.sum(axis=1)
    assert np.allclose(FN_Stock_60[60], data_fn["FN_Stock_Reference_2060"], atol=1e-12)


## Outflow PDF Computation Test

def test_compute_outflow_pdf(dsm_instances):
    """Test whether outflow computed with pdf from compute_outflow_pdf yields same result as the one calculated directly from the sf via compute_s_c_inflow_driven() and compute_o_c_from_s_c()."""
    DSM_pdf = dsm_instances["DSM_pdf"]
    ifl_pdf = dsm_instances["ifl_pdf"]
    PDF_pdf = DSM_pdf.compute_outflow_pdf()
    SC_pdf = DSM_pdf.compute_s_c_inflow_driven()
    OC_pdf = DSM_pdf.compute_o_c_from_s_c()
    OC_alt = np.einsum('c,tc->tc', np.array(ifl_pdf), PDF_pdf)
    Bal_pdf = (np.abs(OC_pdf - OC_alt)).sum()

    assert np.allclose(OC_pdf, OC_alt, atol=1e-14)
    assert np.allclose(Bal_pdf, 0, atol=1e-12)