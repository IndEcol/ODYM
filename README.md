## ODYM   -   Open Dynamic Material Systems Model

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

## Background

ODYM was developed to handle the typical types of model equations and approaches in a dynamic MFA model in a systematic manner. 
These approaches include:\

a)	Regression models: Socioeconomic parameters, such as in-use stocks or final consumption are required to determine the basic material balance or material flows. They are often determined from regression models fed by exogenous parameters such as GDP. A typical example for a regression model is the Gompertz function, where $a(p,r)$ and $b(p,r)$ are product-and region-dependent scaling parameters. Regression models can also be used to determine future scenarios.
	   
	$$ i(p,r,t) = i_{Sat}\cdot exp^{-b(p,r)\cdot exp^{-a(p,r)\cdot t}} $$
     
b)	Dynamic stock model: The material stock S and outflow o can be estimated from inflow data i, using a product lifetime distribution lambda, which describes the probability of a product of age-cohort c being discarded at time t 

c)	Parameter equation with transfer coefficient: The distribution of a material flow to different processes is determined by the transfer coefficient. Consider a flow of different end-of-life products p, Fp, with chemical element composition mu. The products are sent to waste treatment by different technologies w, and each technology has its own element-specific yield factor Gamma, which assigns the incoming elements to different scrap groups s and which varies depending on when the technology was installed (age-cohort dependency): Gamma = Gamma(w,e,s,c). The flow of chemical elements in the different scrap groups Fs is then

	$$ F_s(t,s,e) = \sum_{w,p,c}\Gamma(w,e,s,c)\cdot C(w,t,c)\cdot F_p(t,p)\cdot \mu(p,e)$$


Where C(w,t,c) is the capacity of the different waste treatment technologies w of age-cohort c in a year t.

d)	Optimisation: For a system with a 1:1 correspondence of industries and markets, which is the basis of input-output models, the application of linear optimisation to select between competing technological alternatives is common. This optimisation approach can also be used to determine waste treatment cascades so that non-functional recycling, costs, or GHG emissions are minimized.
