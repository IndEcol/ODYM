from odym.classes.classification import Classification
from odym.functions.utils import ListStringToListNumbers


def ParseModelControl(Model_Configsheet, ScriptConfig):
    """Parse the RECC and ODYM model control parameters from the ODYM config sheet."""
    SCix = 1
    # search for script config list entry
    while Model_Configsheet.cell(SCix, 2).value != "General Info":
        SCix += 1

    SCix += 2  # start on first data row
    while Model_Configsheet.cell(SCix, 4).value is not None:
        ScriptConfig[Model_Configsheet.cell(SCix, 3).value] = Model_Configsheet.cell(
            SCix, 4
        ).value
        SCix += 1

    SCix = 1
    # search for script config list entry
    while Model_Configsheet.cell(SCix, 2).value != "Software version selection":
        SCix += 1

    SCix += 2  # start on first data row
    while Model_Configsheet.cell(SCix, 4).value is not None:
        ScriptConfig[Model_Configsheet.cell(SCix, 3).value] = Model_Configsheet.cell(
            SCix, 4
        ).value
        SCix += 1

    return ScriptConfig


def ParseClassificationFile_Main(Classsheet, Mylog):
    """Parse the ODYM classification file, format version"""
    ci = 2  # column index to start with
    MasterClassification = {}  # Dict of master classifications
    while Classsheet.cell(1, ci).value is not None:
        TheseItems = []
        ri = 11  # row index to start with
        ThisName = Classsheet.cell(1, ci).value
        ThisDim = Classsheet.cell(2, ci).value
        ThisID = Classsheet.cell(4, ci).value
        ThisUUID = Classsheet.cell(5, ci).value
        while Classsheet.cell(ri, ci).value is not None:
            TheseItems.append(
                Classsheet.cell(ri, ci).value
            )  # read the classification items
            ri += 1
        MasterClassification[ThisName] = Classification(
            Name=ThisName, Dimension=ThisDim, ID=ThisID, UUID=ThisUUID, Items=TheseItems
        )
        ci += 1

    return MasterClassification


def ParseConfigFile(Model_Configsheet, ScriptConfig, Mylog):
    """
    Standard routine to parse the ODYM model config file.
    """
    ITix = 0

    # search for index table entry
    while True:
        if Model_Configsheet.cell(ITix + 1, 2).value == "Index Table":
            break
        else:
            ITix += 1

    IT_Aspects = []
    IT_Description = []
    IT_Dimension = []
    IT_Classification = []
    IT_Selector = []
    IT_IndexLetter = []
    ITix += 2  # start on first data row
    while Model_Configsheet.cell(ITix + 1, 3).value is not None:
        IT_Aspects.append(Model_Configsheet.cell(ITix + 1, 3).value)
        IT_Description.append(Model_Configsheet.cell(ITix + 1, 4).value)
        IT_Dimension.append(Model_Configsheet.cell(ITix + 1, 5).value)
        IT_Classification.append(Model_Configsheet.cell(ITix + 1, 6).value)
        IT_Selector.append(Model_Configsheet.cell(ITix + 1, 7).value)
        IT_IndexLetter.append(Model_Configsheet.cell(ITix + 1, 8).value)
        ITix += 1

    Mylog.info("Read parameter list from model config sheet.")
    PLix = 0
    while True:  # search for parameter list entry
        if Model_Configsheet.cell(PLix + 1, 2).value == "Model Parameters":
            break
        else:
            PLix += 1

    PL_Names = []
    PL_Description = []
    PL_Version = []
    PL_IndexStructure = []
    PL_IndexMatch = []
    PL_IndexLayer = []
    PL_SubFolder = []
    PL_ProxyCode = []
    PL_ProcMethod = []
    PL_UpdateOverwrite = (
        []
    )  # 2308 add choice to read new par data or use data from dat file

    PLix += 2  # start on first data row
    while Model_Configsheet.cell(PLix + 1, 3).value is not None:
        PL_Names.append(Model_Configsheet.cell(PLix + 1, 3).value)
        PL_Description.append(Model_Configsheet.cell(PLix + 1, 4).value)
        PL_Version.append(Model_Configsheet.cell(PLix + 1, 5).value)
        PL_IndexStructure.append(Model_Configsheet.cell(PLix + 1, 6).value)
        PL_IndexMatch.append(Model_Configsheet.cell(PLix + 1, 7).value)
        PL_IndexLayer.append(
            ListStringToListNumbers(Model_Configsheet.cell(PLix + 1, 8).value)
        )  # strip numbers out of list string
        PL_SubFolder.append(Model_Configsheet.cell(PLix + 1, 12).value)
        PL_ProxyCode.append(Model_Configsheet.cell(PLix + 1, 13).value)
        PL_ProcMethod.append(Model_Configsheet.cell(PLix + 1, 14).value)
        PL_UpdateOverwrite.append(
            Model_Configsheet.cell(PLix + 1, 15).value
        )  # 2308 add choice to read new par data or use data from dat file
        PLix += 1

    Mylog.info("Read process list from model config sheet.")
    PrLix = 1

    # search for process list entry
    while Model_Configsheet.cell(PrLix, 2).value != "Process Group List":
        PrLix += 1

    PrL_Number = []
    PrL_Name = []
    PrL_Comment = []
    PrL_Type = []
    PrLix += 2  # start on first data row

    while True:
        if Model_Configsheet.cell(PrLix, 3).value is None:
            break
        PrL_Number.append(int(Model_Configsheet.cell(PrLix, 3).value))
        PrL_Name.append(Model_Configsheet.cell(PrLix, 4).value)
        PrL_Type.append(Model_Configsheet.cell(PrLix, 5).value)
        PrL_Comment.append(Model_Configsheet.cell(PrLix, 6).value)
        PrLix += 1

    # while Model_Configsheet.cell(PrLix,3).value is not None:
    #     print(Model_Configsheet.cell(PrLix,3).value)
    #     PrL_Number.append(int(Model_Configsheet.cell(PrLix,3).value))
    #     PrL_Name.append(Model_Configsheet.cell(PrLix,4).value)
    #     PrL_Type.append(Model_Configsheet.cell(PrLix,5).value)
    #     PrL_Comment.append(Model_Configsheet.cell(PrLix,6).value)
    #     PrLix += 1

    Mylog.info("Read model run control from model config sheet.")
    PrLix = 0

    # search for model flow control entry
    while True:
        if Model_Configsheet.cell(PrLix + 1, 2).value == "Model flow control":
            break
        else:
            PrLix += 1

    # start on first data row
    PrLix += 2
    while True:
        if Model_Configsheet.cell(PrLix + 1, 3).value is not None:
            try:
                ScriptConfig[Model_Configsheet.cell(PrLix + 1, 3).value] = (
                    Model_Configsheet.cell(PrLix + 1, 4).value
                )
            except:
                None
            PrLix += 1
        else:
            break

    Mylog.info("Read model output control from model config sheet.")
    PrLix = 0

    # search for model flow control entry
    while True:
        if Model_Configsheet.cell(PrLix + 1, 2).value == "Model output control":
            break
        else:
            PrLix += 1

    # start on first data row
    PrLix += 2
    while True:
        if Model_Configsheet.cell(PrLix + 1, 3).value is not None:
            try:
                ScriptConfig[Model_Configsheet.cell(PrLix + 1, 3).value] = (
                    Model_Configsheet.cell(PrLix + 1, 4).value
                )
            except:
                None
            PrLix += 1
        else:
            break

    return (
        IT_Aspects,
        IT_Description,
        IT_Dimension,
        IT_Classification,
        IT_Selector,
        IT_IndexLetter,
        PL_Names,
        PL_Description,
        PL_Version,
        PL_IndexStructure,
        PL_IndexMatch,
        PL_IndexLayer,
        PL_SubFolder,
        PL_ProxyCode,
        PL_ProcMethod,
        PL_UpdateOverwrite,
        PrL_Number,
        PrL_Name,
        PrL_Comment,
        PrL_Type,
        ScriptConfig,
    )
