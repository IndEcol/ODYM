import odym.classes as msc
import odym.functions as msf
import numpy as np
import pytest


@pytest.fixture(scope="module")
def setup_table_data():
    """
    Fixture to define and return the test data for TableWithFlowsToShares.
    """
    TSA = np.array([[1, 2, 1, 2, 4, 1],
                    [1, 3, 0, 2, 4, 3],
                    [0, 3, 4, 3, 1, 0],
                    [1, 4, 3, 2, 1, 0]])

    TSB = np.array([[0.333333, 0.166667, 0.125, 0.222222, 0.4, 0.25],
                    [0.333333, 0.25, 0, 0.222222, 0.4, 0.75],
                    [0, 0.25, 0.5, 0.333333, 0.1, 0],
                    [0.333333, 0.333333, 0.375, 0.222222, 0.1, 0]])

    TSC = np.array([[0.0909091, 0.181818, 0.0909091, 0.181818, 0.363636, 0.0909091],
                    [0.0769231, 0.230769, 0, 0.153846, 0.307692, 0.230769],
                    [0, 0.272727, 0.363636, 0.272727, 0.0909091, 0],
                    [0.0909091, 0.363636, 0.272727, 0.181818, 0.0909091, 0]])

    TSAx = np.array([[1, 2, 1, 0, 4, 1],
                     [1, 3, 0, 0, 4, 3],
                     [0, 3, 4, 0, 1, 0],
                     [1, 4, 3, 0, 1, 0]])

    TSBx = np.array([[0.3333333333333333, 0.1666666666666667, 0.125, 0, 0.4, 0.25],
                     [0.3333333333333333, 0.25, 0, 0, 0.4, 0.75],
                     [0, 0.25, 0.5, 0, 0.1, 0],
                     [0.3333333333333333, 0.3333333333333333, 0.375, 0, 0.1, 0]])

    TSCx = np.array([[0.1111111111111111, 0.2222222222222222, 0.1111111111111111, 0, 0.4444444444444444, 0.1111111111111111],
                     [0.09090909090909091, 0.2727272727272727, 0, 0, 0.3636363636363636, 0.2727272727272727],
                     [0, 0.375, 0.5, 0, 0.125, 0],
                     [0.1111111111111111, 0.4444444444444444, 0.3333333333333333, 0, 0.1111111111111111, 0]])

    TSAy = np.array([[1, 2, 1, 2, 4, 1],
                     [1, 3, 0, 2, 4, 3],
                     [0, 3, 4, 3, 1, 0],
                     [0, 0, 0, 0, 0, 0]])

    # Note: These values might need adjustment if the original code's floating-point precision
    # was causing issues with exact comparisons. pytest.approx is often better for this.
    TSAzref = np.array([[0.5, 0.25, 0.2, 0.2857142857142857, 0.4444444444444444, 0.25],
                        [0.5, 0.375, 0, 0.2857142857142857, 0.4444444444444444, 0.75],
                        [0, 0.375, 0.8, 0.4285714285714285, 0.1111111111111111, 0],
                        [0, 0, 0, 0, 0, 0]])

    TSBzref = np.array([[0.09090909090909091, 0.18181818181818182, 0.09090909090909091, 0.18181818181818182, 0.36363636363636365, 0.09090909090909091],
                        [0.07692307692307693, 0.23076923076923078, 0, 0.15384615384615385, 0.3076923076923077, 0.23076923076923078],
                        [0, 0.2727272727272727, 0.36363636363636365, 0.2727272727272727, 0.09090909090909091, 0],
                        [0, 0, 0, 0, 0, 0]])

    TSAz = np.zeros((4, 6))

    return {
        "TSA": TSA, "TSB": TSB, "TSC": TSC,
        "TSAx": TSAx, "TSBx": TSBx, "TSCx": TSCx,
        "TSAy": TSAy, "TSAzref": TSAzref, "TSBzref": TSBzref,
        "TSAz": TSAz
    }


@pytest.fixture(scope="module")
def setup_element_composition_data():
    """
    Fixture to define and return the test data for DetermineElementComposition_All_Oth.
    """
    ELCTest1 = np.array([[3.59212, 0, 0, 0.00922665, 3.58289, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0.173689, 0, 0.1719, 0, 0, 0.00178926, 0, 0],
                         [0.0574175, 0, 0, 0, 0, 0.0574175, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0]])

    ELCTest1res = np.array([[1, 0, 0, 0.002568583066476976, 0.9974314169335231, 0, 0, 0],
                            [1, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0, 0, 0, 0, 0, 1],
                            [1, 0, 0.9896984994927148, 0, 0, 0.01030150050728525, 0, 0],
                            [1, 0, 0, 0, 0, 1, 0, 0],
                            [1, 0, 0, 0, 0, 0, 0, 1]])
    return {"ELCTest1": ELCTest1, "ELCTest1res": ELCTest1res}


def test_ListStringToListNumbers():
    """Test the ListStringToListNumbers function."""
    np.testing.assert_array_equal(msf.ListStringToListNumbers('[1,2,3]'), [1, 2, 3])


def test_MI_Tuple():
    """Test the MI_Tuple function."""
    np.testing.assert_array_equal(msf.MI_Tuple(10, [3, 4, 2, 6]), [0, 0, 1, 4])


def test_TableWithFlowsToShares_axis0(setup_table_data):
    """Test the TableWithFlowsToShares function with axis=0."""
    data = setup_table_data
    np.testing.assert_array_almost_equal(msf.TableWithFlowsToShares(data["TSA"], axis=0), data["TSB"], decimal=6)
    np.testing.assert_array_almost_equal(msf.TableWithFlowsToShares(data["TSAx"], axis=0), data["TSBx"], decimal=16)
    np.testing.assert_array_almost_equal(msf.TableWithFlowsToShares(data["TSAy"], axis=0), data["TSAzref"], decimal=16)
    np.testing.assert_array_equal(msf.TableWithFlowsToShares(data["TSAz"], axis=0), np.zeros((4, 6)))


def test_TableWithFlowsToShares_axis1(setup_table_data):
    """Test the TableWithFlowsToShares function with axis=1."""
    data = setup_table_data
    np.testing.assert_array_almost_equal(msf.TableWithFlowsToShares(data["TSA"], axis=1), data["TSC"], decimal=6)
    np.testing.assert_array_almost_equal(msf.TableWithFlowsToShares(data["TSAx"], axis=1), data["TSCx"], decimal=16)
    np.testing.assert_array_almost_equal(msf.TableWithFlowsToShares(data["TSAy"], axis=1), data["TSBzref"], decimal=26)
    np.testing.assert_array_equal(msf.TableWithFlowsToShares(data["TSAz"], axis=1), np.zeros((4, 6)))


def test_DetermineElementComposition_All_Oth(setup_element_composition_data):
    """Test the DetermineElementComposition_All_Oth function."""
    data = setup_element_composition_data
    np.testing.assert_array_almost_equal(msf.DetermineElementComposition_All_Oth(data["ELCTest1"]), data["ELCTest1res"], decimal=16)
