import numpy as np


def ExcelSheetFill(
    Workbook,
    Sheetname,
    values,
    topcornerlabel=None,
    rowlabels=None,
    collabels=None,
    Style=None,
    rowselect=None,
    colselect=None,
):
    Sheet = Workbook.add_sheet(Sheetname)
    if topcornerlabel is not None:
        if Style is not None:
            Sheet.write(
                0, 0, label=topcornerlabel, style=Style
            )  # write top corner label
        else:
            Sheet.write(0, 0, label=topcornerlabel)  # write top corner label
    if (
        rowselect is None
    ):  # assign row select if not present (includes all rows in that case)
        rowselect = np.ones((values.shape[0]))
    if (
        colselect is None
    ):  # assign col select if not present (includes all columns in that case)
        colselect = np.ones((values.shape[1]))
    if rowlabels is not None:  # write row labels
        rowindexcount = 0
        for m in range(0, len(rowlabels)):
            if rowselect[m] == 1:  # True if True or 1
                if Style is None:
                    Sheet.write(rowindexcount + 1, 0, label=rowlabels[m])
                else:
                    Sheet.write(rowindexcount + 1, 0, label=rowlabels[m], style=Style)
                rowindexcount += 1
    if collabels is not None:  # write column labels
        colindexcount = 0
        for m in range(0, len(collabels)):
            if colselect[m] == 1:  # True if True or 1
                if Style is None:
                    Sheet.write(0, colindexcount + 1, label=collabels[m])
                else:
                    Sheet.write(0, colindexcount + 1, label=collabels[m], style=Style)
                colindexcount += 1
    # write values:
    rowindexcount = 0
    for m in range(0, values.shape[0]):  # for all rows
        if rowselect[m] == 1:
            colindexcount = 0
            for n in range(0, values.shape[1]):  # for all columns
                if colselect[n] == 1:
                    Sheet.write(
                        rowindexcount + 1, colindexcount + 1, label=values[m, n]
                    )
                    colindexcount += 1
            rowindexcount += 1


def ExcelExportAdd_tAB(
    Sheet,
    Data,
    rowoffset,
    coloffset,
    IName,
    UName,
    RName,
    FName,
    REName,
    ALabels,
    BLabels,
):
    """
    This function exports a 3D array with aspects time, A, and B to a given excel sheet.
    Same as xlsxExportAdd_tAB but this function is for xls files with xlrd.
    The t dimension is exported in one row, the A and B dimensions as several rows.
    Each row starts with IName (indicator), UName (unit), RName (region),
    FName (figure where data are used), REName (Resource efficiency scenario),
    and then come the values for the dimensions A and B and from coloffset onwards, the time dimension.
    Function is meant to be used multiple times, so a rowoffset is given, incremented, and returned for the next run.
    """
    for m in range(0, len(ALabels)):
        for n in range(0, len(BLabels)):
            Sheet.write(rowoffset, 0, label=IName)
            Sheet.write(rowoffset, 1, label=UName)
            Sheet.write(rowoffset, 2, label=RName)
            Sheet.write(rowoffset, 3, label=FName)
            Sheet.write(rowoffset, 4, label=REName)
            Sheet.write(rowoffset, 5, label=ALabels[m])
            Sheet.write(rowoffset, 6, label=BLabels[n])
            for t in range(0, Data.shape[0]):
                Sheet.write(rowoffset, coloffset + t, label=Data[t, m, n])
            rowoffset += 1

    return rowoffset


def xlsxExportAdd_tAB(
    Sheet,
    Data,
    rowoffset,
    coloffset,
    IName,
    UName,
    RName,
    FName,
    REName,
    ALabels,
    BLabels,
):
    """
    This function exports a 3D array with aspects time, A, and B to a given excel sheet.
    Same as ExcelExportAdd_tAB but this function is for xlsx files with openpyxl.
    The t dimension is exported in one row, the A and B dimensions as several rows.
    Each row starts with IName (indicator), UName (unit), RName (region),
    FName (figure where data are used), REName (Resource efficiency scenario),
    and then come the values for the dimensions A and B and from coloffset onwards, the time dimension.
    Function is meant to be used multiple times, so a rowoffset is given, incremented, and returned for the next run.
    """
    for m in range(0, len(ALabels)):
        for n in range(0, len(BLabels)):
            Sheet.cell(row=rowoffset, column=1).value = IName
            Sheet.cell(row=rowoffset, column=2).value = UName
            Sheet.cell(row=rowoffset, column=3).value = RName
            Sheet.cell(row=rowoffset, column=4).value = FName
            Sheet.cell(row=rowoffset, column=5).value = REName
            Sheet.cell(row=rowoffset, column=6).value = ALabels[m]
            Sheet.cell(row=rowoffset, column=7).value = BLabels[n]
            for t in range(0, Data.shape[0]):
                Sheet.cell(row=rowoffset, column=coloffset + t + 1).value = Data[
                    t, m, n
                ]
            rowoffset += 1

    return rowoffset
