ODYM   -   Open Dynamic Material Systems Model

__Please note that ODYM is still in its inception phase. Documentation on this repo and a scientific publication are in preparation.__

The ODYM model framework is a software library for dynamic material flow analysis (MFA). It can best be described as a framework for modeling biophysical stock-flow relations in socioeconomic metabolism. 

The novel features of ODYM include:\
•	System variables (stocks and flows) can have any number of aspects (time, age-cohort, region, product, component, material, element, …)\
•	The software automatically matches the different dimensions during computations. No manual re-indexing of tables and arrays is necessary. \
•	The user only specifies those aspects that are relevant for the model. The software handles the data storage and matching of the indices used.\
•	The software checks whether a consistent classification is used all across the model.\
•	Flexibility regarding different data formats (table and list) and subsets of classifications used (only certain years or chemical elements, for example).\
•	Representation of system variables and parameters as objects, general data structures serve as interfaces to a wide spectrum of modules for stock-driven modelling, waste cascade optimisation, etc.

More information is available:\
•	Wiki pages in this repository.\
•	Tutorials (Jupyther notebooks) in the docs folder.\
•	A journal paper (in preparation).
