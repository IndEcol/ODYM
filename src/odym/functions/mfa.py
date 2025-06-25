import numpy as np


def TableWithFlowsToShares(Table: np.ndarray, axis: int) -> np.ndarray:
    """
    Given a 2D-table with flow values that sum up to a total,
    either along the columns (= across rows, axis =0) or along the rows (=across the columns, axis =1).
    The function then converts the flows into shares (between 0 and 1), that each element has in the column sum (axis =0)
    or the row sum (axis =1).
    Only makes sense if all table entries have the same sign, that is not checked by the function.
    """
    Shares = np.zeros(Table.shape)
    if axis == 0:  # shares along columns
        colsum = Table.sum(axis=0)
        Divisor = np.einsum("b,a->ab", colsum, np.ones(Table.shape[0]))
    if axis == 1:  # shares along rows
        rowsum = Table.sum(axis=1)
        Divisor = np.einsum("a,b->ab", rowsum, np.ones(Table.shape[1]))
    Divided = np.divide(1, Divisor, out=np.zeros_like(Divisor), where=Divisor != 0)
    Shares = Table * Divided
    return Shares


def DetermineElementComposition_All_Oth(me: np.ndarray) -> np.ndarray:
    """
    Given an array of flows of materials (rows) broken down into chem. elements (columns),
    where the first element is "all" and the last element is "other",
    the function determines the share of each element in the material, and fills nonexistent rows with a 1 for all and other, resp.
    """
    result = np.zeros(me.shape)
    Shares = TableWithFlowsToShares(me[:, 1::], 1)
    SharesSum = Shares.sum(axis=1)
    result[:, 0] = 1
    result[:, 1::] = Shares.copy()
    for m in range(0, me.shape[0]):
        if SharesSum[m] == 0:
            result[m, -1] = 1
    return result
