# %%
import odym
import odym.functions
import openpyxl


odym.functions.ParseClassificationFile_Main(
    Classsheet=openpyxl.load_workbook('/Users/michaelweinold/github/ODYM/docs/_files/ODYM_Classifications_Master_Tutorial.xlsx'),
    Mylog=None,    
)