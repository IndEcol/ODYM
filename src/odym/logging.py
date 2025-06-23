import os
import logging
import numpy as np
import xlrd
import openpyxl
import pypandoc
from scipy.interpolate import make_interp_spline
from scipy.interpolate import interp1d
import odym.classes as msc


def function_logger(log_filename, log_pathname, file_level=logging.DEBUG, console_level=logging.WARNING):
    """
    This is the logging routine of the model. It returns alogger that can be used by other functions to write to the
    log(file).

    :param file_level: Verbosity level for the logger's output file. This can be log.WARNING (default),
        log.INFO, log.DEBUG
    :param log_filename: The filename for the logfile.
    :param log_pathname: The pathname for the logfile.
    :param console_level: Verbosity level for the logger's output file.
    out
    :param logfile_type: Type of file to write. Markdown syntax is the default.
        TODO: If other outputs types are desired, they can be converted via pandoc.
    :return: A logger that can be used by other files to write to the log(file)
    """

    log_file = os.path.join(log_pathname, log_filename)
    # logging.basicConfig(format='%(levelname)s (%(filename)s <%(funcName)s>): %(message)s',
    #                     filename=log_file,
    #                     level=logging.INFO)
    logger = logging.getLogger()
    logger.handlers = []  # required if you don't want to exit the shell
    logger.setLevel(file_level)

    # The logger for console output
    console_log = logging.StreamHandler() #StreamHandler logs to console
    console_log.setLevel(console_level)
    # console_log_format = logging.Formatter('%(message)s')
    console_log_format = logging.Formatter('%(levelname)s (%(filename)s <%(funcName)s>): %(message)s')
    console_log.setFormatter(console_log_format)
    logger.addHandler(console_log)

    # The logger for log file output
    file_log = logging.FileHandler(log_file, mode='w', encoding=None, delay=False)
    file_log.setLevel(file_level)
    file_log_format = logging.Formatter('%(message)s\n')
    file_log.setFormatter(file_log_format)
    logger.addHandler(file_log)

    return logger,  console_log, file_log


def convert_log(file: str, file_format: str='html') -> None:
    """
    Converts the log file to a given file format

    :param file: The filename and path
    :param file_format: The desired format
    """
    output_filename = os.path.splitext(file)[0] + '.' + file_format
    output = pypandoc.convert_file(file, file_format, outputfile=output_filename)
    assert output == ""
