# Tutorials

The ODYM Tutorials use Jupyter notebooks that can be found under the docs folder. Here a quick overview is provided.

## ODYM Example no. 1. System with two processes, two parameters, one material.

A simple MFA system with one material (represented by the indicator element carbon 'C'), a time horizon of 30 years [1980-2010], two processes, and a time-dependent parameter is analysed.

## ODYM Example no. 2. Alloying elements in recycling.

A recycling system with two end-of-life (EoL) products, two scrap types, one secondary material, and several types of losses are studied. Three chemical elements are considered: iron, copper, and manganese. A time horizon of 30 years [1980-2010], five processes, and time-dependent parameters are analysed. The processes have element-specific yield factors, meaning that the loss rates depend on the chemical element considered.

## ODYM Example no. 3. Dynamic stock modelling.

ODYM includes the Python class dynamic_stock_modelling for handling the inflow-driven and stock driven model of in-use stocks (http://www.teaching.industrialecology.uni-freiburg.de/ Methods section 3). Here it is shown how the dynamic stock model is used in the ODYM framework. Other methods of the dynamic_stock_modelling class can be used in a similar way.


## ODYM Example no. 4. ODYM classification and database

This tutorial shows how to use the ODYM data structure, including the classification file, the configuration file, and formatted parameter datasets.

## ODYM Example no. 5. Estimating the material content of the global vehicle fleet

ODYM was designed to handle extensive MFA systems by covering multiple aspects (time, age-cohort, region, material, chemical elements, processes, goods, components, ...) in a systematic manner. Its data format is used to structure and store input data, its software structure determines how the information is organised in the computer, and its application scripts provide a working environment for conducting reproducible dynamic MFA research with comprehensive and multi-aspect systems.

This example shows a fully-fledged application of ODYM to estimate the material composition of the global passenger vehicle fleet in 2017, covering 130 countries, 25 age-cohorts, and 25 materials. The application is controlled by a config file, reads the model parameters in standard format, performs the model computations and a Monte-Carlo simulation of the uncertainties stemming from vehicle lifetime and material composition, performs automatic mass balance checks, and stores the model procedures in a log file.

The research questions asked are: **How big is the material stock currently embodied in the global passenger vehicle fleet, and when will this material become available for recycling?**

The research questions asked are: How big is the material stock currently embodied in the global passenger vehicle fleet, and when will this material become available for recycling?

To answer these questions a dynamic material flow analysis of the global passenger vehicle fleet and the waste management industries is performed.

The dynamic MFA model has the following indices:

*     t: time (1990-2017)
*     c: age-cohort (1990-2017)
*     r: region (130 countries accounting for most of the global vehicle fleet)
*     g: good (passenger vehicle)
*     p: process (vehicle markets, use phase, waste management industries, scrap markets)
*     m: engineering materials (25)
*     e: chemical elements (all)
*     w: waste types (steel, Al, Cu scrap, plastics, glass, and other waste)

The system definition of the model is given in the figure below. The data availability limits the temporal scope to 2017. The figure also shows the aspects of the different system variables. The total registration of vehicles, for example, is broken down into individual materials, whereas the flow of deregistered vehicles is broken down into regions, age-cohorts, and materials.

![System Definition](https://github.com/IndEcol/ODYM/blob/master/docs/Images/ODYM_Tutorial5_SysDef.png)

**The following plots are created:**

![EoL outflow vehicles](https://github.com/IndEcol/ODYM/blob/master/docs/Images/ScrapFlows_2017.png)

![EoL vehicles outflow by region](https://github.com/IndEcol/ODYM/blob/master/docs/Images/ScrapFlows_2017_Top10Regions.png)

One can see that the pre-2020 outflows will decline sharply by about 25%, before they reach a plateau between ca. 2021 and 2029. This plateau is probably the consequence of two peaks overlapping, one pre-2017 peak (from 2002 +/- 5 years cars) and one ca. 2027 (from 2012 +/- 5 years cars). To find out which countries are causing this behaviour, let's zoom into the region-specific results! The value for electronic waste is very low because due to data limitations, it was assumed that all copper goes into the copper wire scrap fraction and all plastic to the shredder light fraction. The total outflow from the 2017 stock is indeed the consequence of two overlapping peaks, one resulting from the constantly high car sales in the richest countries, and the later one resulting from the recent sharp increase of vehicle registration in China.

**Performing a Monte-Carlo-Simulation**

ODYM has no built-in MC tool yet, as practices still need to evolve and the different application cases vary a lot. Re-sampling an entire parameter from the Uncertainty information is easy to implement but often very inefficient, as, like in this case, few actually known parameter values are replicated to span all countries and age-cohorts.

Here, we therefore sample the 25 original material content array only, and replicate the sampled values to cover all regions and age-cohorts. Of course, this can be changed when more data is available. We sample the material content per vehicle NMC times from its defined distribution and re-calculate the stock and outflow variables.

The result can be visualized in box plots, for example, as shown below.


![Box plot results](https://github.com/IndEcol/ODYM/blob/master/docs/Images/BoxPlot_OtherMaterials_2017_Sel.png)

As the material content array comes with min/max uncertainty/variability ranges, from which uniformly distributed samples were drawn, the box plot shows no outliers and the 1./3. quartiles span exactly half the space between min and max values. It does show how the variability of the different material content estimates impacts the variation of the material stock estimate. While the estimates for materials 20-22 (rubber, glass, and ceramics) are rather certain, the one for material 11 (Aluminium) varies substantially, which reflects the high variability of the Al content of passenger vehicles.

If the data are well structured and the model is set up accordingly, performing an uncertainty analysis can be quickly done, as the brevity of the Monte-Carlo-code above shows.

