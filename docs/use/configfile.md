# Config File

[Tutorial 4](../tutorials/tutorial_4.ipynb) shows a simple example of the formatting and use of the ODYM config file.

On the first sheet `Config` of the config file, cell `D4`, the desired configuration sheet with the model configuration is selected. The information in the configuration sheet is split into different groups:

1)	General info: 
Contains the name of the current model setting, the script to be used, and a description. The ODYM configuration sheet points to the model script to be used, which then will import all other modules needed.

2)	Software version selection:
Here the modeller specifies which master classification file is to be used. All parameters loaded for this model run must then be given in the same classification. The version numbers of the different ODYM modules that are used are specified as well.

3)	Index table:
Here the modeller defines the index table as described above. The entries in the `classification` column must match the classification names in the classification master file, and the index letters in the rightmost column must be unique.

4)	Process group list:
Here all process groups as displayed in the system definition are listed and alphanumeric indices are assigned to them. The different process groups can have one or more subdivisions, depending on the dimensions in the index table. For example, the use phase process group can be divided into the use phases of the different products considered.

5)	Model parameters:
The configuration sheet lists all parameters used, which are then read from the ODYM database by the model script. For each model parameter the version (identical to the filename) of the parameter is selected, as well as its index structure (year x good x element gives `tGe`, region x year x material gives `rta`, etc.), the aspect order match (tells ODYM which dimension in the parameter file fits to which model aspect), and the layer selection (next to the actual parameter values, there will be an option to include alternative scenarios or uncertainty ranges).
If the parameters are formatted correctly and their values are given in the same classifications as used for the model run, ODYM is able to parse all data just using the info in the index table, the ODYM process table, and the parameter list.

6)	Model flow control:
Here a number of config parameters to control the model flow can be defined and then used by the script. One example is the verbosity level of the logging function, and many other possibilities exist.

7)	Model output control:
Here a number of config parameters can be defined to control how, where, and which results are to be stored. 