# About

## Development of ODYM

The methods and algorithms of MFA have significantly improved over the last years, but a flexible platform that integrates recent modeling advances such as simultaneous consideration of the product, component, material, and chemical element levels, lifetime models, and uncertainty treatment is not available. There is also no versatile data format for exchanging data between projects. This lack of research infrastructure hampers the uptake of new MFA methods by other scholars and ultimately, it slows down scientific progress. 

To fill that gap we developed ODYM (Open Dynamic Material Systems Model), an open source framework for material systems modelling programmed in Python. The description of systems, processes, stocks, flows, and parameters is object-based, which facilitates the development of modular software and testing routines for individual model blocks. 

ODYM MFA models can handle any depth of flow and stock specification: products, components, sub-components, materials, alloys, waste, and chemical elements can be traced simultaneously. ODYM features a new data structure for material flow analysis; all input and output data are stored in a standardized file format and can thus be exchanged across projects. It comes with an extended library for dynamic stock modelling. 

## License

```plaintext
--8<-- "LICENSE.txt"
```