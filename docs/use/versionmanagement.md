# Version Management

ODYM runs as local copy on individual machines. A project-wide config file ODYM_Config.xlsx points to a specific model and database version for each model run. The results are stored at a unique location created by the model. Local improvements of ODYM can be pushed to the GitHub repository. Each modification or extension of ODYM by individual project members should be internally reviewed and unit-tested before it is added to the ODYM library and pushed to the public repository. Testing can also be automated for future releases. 

The projects based on ODYM are subject to different stringency levels of version management (Table below). Strict version management with Git is applied to the core software routines, including the ODYM classes and respective methods, like mass balance checks and export routines, and the ODYM functions like data parsers. These parts of the module contain computer code that is used for every model run, which is why it is subject to testing and version management. 

| ODYM version management:                    | Project-wide version management, e.g., via | Individual version management (local machine) |
| :------------------------------------------ | :----------------------------------------- | :-------------------------------------------- |
| Git, public repository                      | git, file names, cloud                     | Results                                       |
| https://github.com/indecol/odym             | Config files                               | Local data                                    |
| Model core: classes, methods, functions     | Main model scripts                         |                                               |
| Model classification and metadata structure | Project-wide data                          |                                               |
| Tutorials                                   | Documentation                              |                                               |

Individual scenarios are constructed using local copies/images of the centrally stored files plus local files. The scenario configurations and results are stored locally.

Files that are used for specific projects also need to be version-managed, and the stringency project-specific version management is at the discretion of the project teams. Next to using Git or other version management software typical procedures can include the creation of file names with different version numbers included and their storage on the cloud. Project teams are responsible for keeping track of all relevant changes, and to make backup copies of all relevant files. This type of version management applies to the project’s main model scripts, the model config files, the data files, the model documentation, and the tutorials. 
Finally, the version management of results and local data is under the responsibility of the individual team members.

