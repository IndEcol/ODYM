## ODYM   -   Open Dynamic Material Systems Model

The ODYM model framework is a software library for dynamic material flow analysis (MFA). It can best be described as a framework for modeling biophysical stock-flow relations in socioeconomic metabolism. 

The novel features of ODYM include:\
•	System variables (stocks and flows) can have any number of aspects (time, age-cohort, region, product, component, material, element, …)\
•	The software automatically matches the different dimensions during computations. No manual re-indexing of tables and arrays is necessary. \
•	The user only specifies those aspects that are relevant for the model. The software handles the data storage and matching of the indices used.\
•	The software checks whether a consistent classification is used all across the model.\
•	Flexibility regarding different data formats (table and list) and subsets of classifications used (only certain years or chemical elements, for example).\
•	Representation of system variables and parameters as objects, general data structures serve as interfaces to a wide spectrum of modules for stock-driven modelling, waste cascade optimisation, etc.

__More information is available:__\
•	Wiki pages in this repository.\
•	Tutorials (Jupyther notebooks) in the docs folder.\
•	Documentation of the ODYM classes: http://htmlpreview.github.com/?https://github.com/IndEcol/ODYM/blob/master/docs/ODYM_Classes.html \
•	Documentation of the ODYM functions: http://htmlpreview.github.com/?https://github.com/IndEcol/ODYM/blob/master/docs/ODYM_Functions.html \
•	Documentation of the dynamic stock model class: http://htmlpreview.github.com/?https://github.com/IndEcol/ODYM/blob/master/docs/dynamic_stock_model.html \
•	A journal paper (in preparation).

## Background

ODYM was developed to handle the typical types of model equations and approaches in a dynamic MFA model in a systematic manner. 
These approaches include:

__a)	Regression models:__ Socioeconomic parameters, such as in-use stocks or final consumption are required to determine the basic material balance or material flows. They are often determined from regression models fed by exogenous parameters such as GDP. A typical example for a regression model is the Gompertz function, where $a(p,r)$ and $b(p,r)$ are product-and region-dependent scaling parameters. Regression models can also be used to determine future scenarios.
	   
	$$ i(p,r,t) = i_{Sat}\cdot exp^{-b(p,r)\cdot exp^{-a(p,r)\cdot t}} $$
     
__b)	Dynamic stock model:__ The material stock S and outflow o can be estimated from inflow data i, using a product lifetime distribution $\lambda(t,c)$, which describes the probability of a product of age-cohort c being discarded at time t 

	$$ \begin{eqnarray} o(t)=\sum_{t'\leq t}i(t')\cdot \lambda(t,c = t') \\ S(t)=\sum_{t'\leq t}(i(t')-o(t')) \end{eqnarray} $$

__c)	Parameter equation with transfer coefficients:__ The distribution of a material flow to different processes is determined by the transfer coefficient. Consider a flow of different end-of-life products p, $F_p$, with chemical element composition $\mu$. The products are sent to waste treatment by different technologies w, and each technology has its own element-specific yield factor $\Gamma$, which assigns the incoming elements to different scrap groups s and which varies depending on when the technology was installed (age-cohort dependency): $\Gamma = \Gamma(w,e,s,c)$. The flow of chemical elements in the different scrap groups $F_s$ is then

	$$ F_s(t,s,e) = \sum_{w,p,c}\Gamma(w,e,s,c)\cdot C(w,t,c)\cdot F_p(t,p)\cdot \mu(p,e)$$

Where $C(w,t,c)$ is the capacity of the different waste treatment technologies w of age-cohort c in a year t.

__d)	Optimisation:__ For a system with a 1:1 correspondence of industries and markets, which is the basis of input-output models, the application of linear optimisation to select between competing technological alternatives is common. This optimisation approach can also be used to determine waste treatment cascades so that non-functional recycling, costs, or GHG emissions are minimized. A waste cascade optimisation problem has the typical form (Kondo and Nakamura 2005)
	
	$$ \begin{eqnarray} min C = c^t\cdot x\\ s.t.\\ w = G\cdot x+y\\ x = S\cdot w \\ x \geq 0 $$
	
In the above equation, x is the output vector of the different waste treatment plants, c is a cost vector, y is the final demand for waste treatment, G is the waste generation of waste treatment, and S is the allocation of waste to treatment processes.
	
## Development of ODYM
The methods and algorithms of MFA have significantly improved over the last years, but a flexible platform that integrates recent modeling advances such as simultaneous consideration of the product, component, material, and chemical element levels, lifetime models, and uncertainty treatment is not available. There is also no versatile data format for exchanging data between projects. This lack of research infrastructure hampers the uptake of new MFA methods by other scholars and ultimately, it slows down scientific progress. 

To fill that gap we developed ODYM (Open Dynamic Material Systems Model), an open source framework for material systems modelling programmed in Python. The description of systems, processes, stocks, flows, and parameters is object-based, which facilitates the development of modular software and testing routines for individual model blocks. 

ODYM MFA models can handle any depth of flow and stock specification: products, components, sub-components, materials, alloys, waste, and chemical elements can be traced simultaneously. ODYM features a new data structure for material flow analysis; all input and output data are stored in a standardized file format and can thus be exchanged across projects. It comes with an extended library for dynamic stock modelling. 

## Folder structure of the ODYM repo
The folder structure of the ODYM repository is shown in the figure below. It shows the main module files, the tutorials with related material, and the unit tests. 

![ODYM directory tree](https://github.com/IndEcol/ODYM/blob/master/docs/Images/ODYM_DirectoryTree.png "ODYM directory tree")
