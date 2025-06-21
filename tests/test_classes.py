import odym.classes as msc # import the ODYM class file
import odym.functions as msf # import the ODYM function file
import numpy as np
import pytest
import pandas as pd


@pytest.fixture(scope="module")
def setup_mfa_system():
    """
    Sets up the MFA system for testing. This fixture will be run once
    for all tests in this module.
    """
    # Define results
    MyMFA_Test1_Flowshape1 = (5, 2)
    F_0_1_Values1 = np.array([[1, 1], [0, 0], [2, 2], [1, 1], [4, 4]])
    F_1_2_Values1 = np.array([[1, 1], [1, 1], [32, 32], [1, 1], [4, 4]])
    F_2_1_Values1 = np.array([[0, 0], [1, 1], [30, 30], [0, 0], [0, 0]])
    F_2_0_Values1 = F_0_1_Values1.copy()
    Bal_Test1 = np.zeros((5, 3, 2))

    # Define dynamic MFA model and fill in values
    ModelClassification_Test1 = {}
    ModelClassification_Test1["Unity"] = msc.Classification(
        Name="Unity", Dimension="Unity", Items=[1]
    )
    ModelClassification_Test1["Time"] = msc.Classification(
        Name="Time", Dimension="Time", Items=[2010, 2011, 2012, 2013, 2014]
    )
    ModelClassification_Test1["Element"] = msc.Classification(
        Name="Chem_Elements", Dimension="Element", Items=["All", "Fe"]
    )

    Model_Time_Start = min(ModelClassification_Test1["Time"].Items)
    Model_Time_End = max(ModelClassification_Test1["Time"].Items)

    Model_Aspects = ["Time", "Element", "Unity"]
    IndexTable = pd.DataFrame(
        {
            "Aspect": Model_Aspects,
            "Description": ["Time", "Element", "Unity"],
            "Dimension": ["Time", "Element", "Unity"],
            "Classification": [
                ModelClassification_Test1[Aspect] for Aspect in Model_Aspects
            ],
            "IndexLetter": ["t", "e", "i"],
        }
    )
    IndexTable.set_index("Aspect", inplace=True)

    MyMFA_Test1 = msc.MFAsystem(
        Name="TestSystem",
        Geogr_Scope="World",
        Unit="Mt",
        ProcessList=[],
        FlowDict={},
        StockDict={},
        ParameterDict=None,
        Time_Start=Model_Time_Start,
        Time_End=Model_Time_End,
        IndexTable=IndexTable,
        Elements=IndexTable.loc["Element"].Classification.Items,
    )

    PrL_Name = ["Environment", "Process_1", "Process_2"]
    PrL_Number = [0, 1, 2]
    for m in range(0, len(PrL_Name)):
        MyMFA_Test1.ProcessList.append(msc.Process(Name=PrL_Name[m], ID=PrL_Number[m]))

    MyMFA_Test1.FlowDict["F_0_1"] = msc.Flow(
        Name="Input", P_Start=0, P_End=1, Indices="t,e", Values=None, Uncert=None
    )
    MyMFA_Test1.FlowDict["F_1_2"] = msc.Flow(
        Name="Processed input", P_Start=1, P_End=2, Indices="t,e", Values=None, Uncert=None
    )
    MyMFA_Test1.FlowDict["F_2_1"] = msc.Flow(
        Name="Sent back to 1", P_Start=2, P_End=1, Indices="t,e", Values=None, Uncert=None
    )
    MyMFA_Test1.FlowDict["F_2_0"] = msc.Flow(
        Name="Output", P_Start=2, P_End=0, Indices="t,e", Values=None, Uncert=None
    )

    MyMFA_Test1.Initialize_FlowValues()

    MyMFA_Test1.FlowDict["F_0_1"].Values = F_0_1_Values1
    MyMFA_Test1.FlowDict["F_1_2"].Values = F_1_2_Values1
    MyMFA_Test1.FlowDict["F_2_1"].Values = F_2_1_Values1
    MyMFA_Test1.FlowDict["F_2_0"].Values = F_2_0_Values1

    Bal = MyMFA_Test1.MassBalance()

    return MyMFA_Test1, MyMFA_Test1_Flowshape1, Bal_Test1, Bal


def test_flow_dimensions(setup_mfa_system):
    """
    Tests the dimensions of a flow in the MFA system.
    """
    MyMFA_Test1, MyMFA_Test1_Flowshape1, _, _ = setup_mfa_system
    assert MyMFA_Test1.FlowDict["F_1_2"].Values.shape[0] == MyMFA_Test1_Flowshape1[0]
    assert MyMFA_Test1.FlowDict["F_1_2"].Values.shape[1] == MyMFA_Test1_Flowshape1[1]


def test_mass_balance(setup_mfa_system):
    """
    Tests the mass balance calculation of the MFA system.
    """
    MyMFA_Test1, _, Bal_Test1, Bal = setup_mfa_system
    np.testing.assert_array_equal(Bal, Bal_Test1)