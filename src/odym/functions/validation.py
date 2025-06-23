import os


def check_dataset(path, PL_Names, PL_Version, PL_SubFolder, Mylog):
    """
    Checks that every parameter in Pl_Names with the corrsponding version PL_Versions is in the folder given by path, or subfolder given by PL_SubFolder

    :param path: Dataset folder
    :param PL_Names: List of parameters names
    :param PL_versions: List of parameters versions
    :param PL_SubFolder: List of data subfolder names
    :param Mylog: log file

    """
    for m in range(len(PL_Names)):
        if PL_Names[m] + "_" + PL_Version[m] + ".xlsx" not in os.listdir(path):
            if PL_Names[m] + "_" + PL_Version[m] + ".xlsx" not in os.listdir(
                os.path.join(path, PL_SubFolder[m])
            ):
                Mylog.error(
                    PL_Names[m] + "_" + PL_Version[m] + ".xlsx not in the dataset."
                )
