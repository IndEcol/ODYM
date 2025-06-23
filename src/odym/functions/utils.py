import numpy as np


def sort_index(
    mylist, direction
):  # returns index that sorts a list, either ascending or descending
    if direction == "ascending":
        return sorted(range(len(mylist)), key=lambda k: mylist[k])
    elif direction == "descending":
        return sorted(range(len(mylist)), key=lambda k: mylist[k], reverse=True)
    else:
        return None


def GroupingDict2Array(GroupingDict: dict, ElementList: list):
    """
    Tbd.
    """
    NoOfItems = len(GroupingDict.keys())
    GroupingList = []
    for m in GroupingDict.keys():
        GroupingList.append(m)
    ElementContentArray = np.zeros((100, NoOfItems))
    PosCount = 0
    for m in GroupingList:
        for n in GroupingDict[m].keys():
            ElInd = ElementList.index(n)
            ElementContentArray[ElInd, PosCount] = GroupingDict[m][n]
        PosCount += 1
    return GroupingList, ElementContentArray


def ListStringToListNumbers(ListStr: str) -> list[int]:
    """
    Extracts numbers from a string that looks like a list commant in python, and returns them as proper list
    Examples: ListStringToListNumbers('[1,2,3]') yields [1,2,3]
    """
    return [
        int(s)
        for s in ListStr[ListStr.find("[") : ListStr.find("]") + 1]
        .replace("[", ",")
        .replace("]", ",")
        .split(",")
        if s.isdigit()
    ]


def EvalItemSelectString(ItemSelectStr, IndexLength):
    """
    Extract index item selection lists from ODYM datafile information
    """
    if ItemSelectStr == "All" or ItemSelectStr == "ALL" or ItemSelectStr == "all":
        Res = "all"  # Selects all from list
    elif (
        ItemSelectStr.find("except") > -1
    ):  # type 'All except', return full list [0,1,2,5,6,7]
        Res = np.arange(0, IndexLength)
        b = (
            ItemSelectStr[ItemSelectStr.find("[") : ItemSelectStr.find("]") + 1]
            .replace("[", ",")
            .replace("]", ",")
        )
        RemoveList = [int(s) for s in b.split(",") if s.isdigit()]
        Res = np.delete(Res, RemoveList)
        Res = Res.tolist()
    elif ItemSelectStr.find("]") > -1:  # type '[...]', return full list
        Res = ItemSelectStr[ItemSelectStr.find("[") : :]
    elif ItemSelectStr.find(")") > -1:  # type '[..:..)', return range a:b
        Res = ItemSelectStr[ItemSelectStr.find("[") + 1 : -1]
    else:
        Res = "ItemSelectString could not be detected."

    return Res


def MI_Tuple(value, Is):
    """
    Define function for obtaining multiindex tuple from index value
    value: flattened index position, Is: Number of values for each index dimension
    Example: MI_Tuple(10, [3,4,2,6]) returns [0,0,1,4]
    MI_Tuple is the inverse of Tuple_MI.
    """
    IsValuesRev = []
    CurrentValue = value
    for m in range(len(Is)):
        IsValuesRev.append(CurrentValue % Is[len(Is) - m - 1])
        CurrentValue = CurrentValue // Is[len(Is) - m - 1]
    return IsValuesRev[::-1]


def Tuple_MI(Tuple, IdxLength):
    """
    Function to return the absolution position of a multiindex when the index tuple
    and the index hierarchy and size are given.
    Example: Tuple_MI([2,7,3],[100,10,5]) = 138
    Tuple_MI is the inverse of MI_Tuple.
    """
    # First, generate the index position offset values
    A = IdxLength[1:] + IdxLength[:1]  # Shift 1 to left
    A[-1] = 1  # Replace lowest index by 1
    A.reverse()
    IdxPosOffset = np.cumproduct(A).tolist()
    IdxPosOffset.reverse()
    Position = np.sum([a * b for a, b in zip(Tuple, IdxPosOffset)])
    return Position


def ModelIndexPositions_FromData(Positions, RowPos, ColPos):
    """
    This function is needed to read data files into ODYM. It takes the positions of a given data point
    in the parameter file and checks where in the model index structure this data points belongs,
    if it is needed at all.
    """
    TargetPosition = []
    for m in range(0, len(Positions)):
        if m < len(RowPos):
            try:
                TargetPosition.append(Positions[m].index(RowPos[m]))
            except:
                break
        else:
            try:
                TargetPosition.append(Positions[m].index(ColPos[m - len(RowPos)]))
            except:
                break
    return TargetPosition
