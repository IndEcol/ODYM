# Getting Started

The ODYM model run is designed as simple procedural program, meaning that the actual model run contains of a list of instructions bundled into a script, which are executed by the Python working environment. This procedural approach provides very high flexibility, which means that modelers can move forward quickly with their analysis of material cycles. An ODYM model run consists of the following steps:

•	**Initialization:** The model script reads the config file and stores all relevant config parameters into a dictionary. It loads all ODYM modules, creates the result folder (each model run has its own result folder and is identified by a UUID), creates a copy of itself and the config file in the result folder, and initializes the logger, which keeps track of the model output during the model run.

•	**Read classifications and data:** The model script reads the master classification and the index table, the process list, and the parameter list from the config file. It builds the index table as Pandas dataframe and creates the model classifications as instances of the ODYM Classification class. All parameters are read from the ODYM database and formatted as instances of the ODYM parameter class.

•	**Initialize MFA system:** The model script creates and MFA system as an instance of the ODYM MFA System class, moves the index table, the process list, and the parameter dictionary into this system. All flows and stocks (the system variables) that were defined by the modeler are initialized. 

•	**Model calculations:** The values of the system variables are determined according to the model solution programmed, e.g., as single parameter equations or by using other modules such as the dynamic stock module. Examples can be found on the ODYM GitHub page.

•	**Model result check:** The validity of the model results, e.g., the mass balance for all processes and chemical elements, is checked using the methods provided by the ODYM MFA System class.

•	**Visualization:** The model results are evaluated and visualized according to the specification made in the config file.

•	**Result export:** The model results are exported according to the specification made in the config file.

•	**Model wrap-up:** The logger is shut down and the script terminates.

During each model run, ODYM creates a result folder, containing a copy of the main model script, a copy of the config file, and a markdown log file where all information is stored that is needed to re-run the model with the exact same setup. This feature greatly enhances reproducibility; it is also necessary because the size of the model output will make it impractical in many cases to store all results. Examples of model scripts are supplied as Jupyter notebooks on the GitHub repo.

