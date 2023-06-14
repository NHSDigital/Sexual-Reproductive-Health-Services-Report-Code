Warning - this repository is a snapshot of a repository internal to NHS England. This means that links to videos and some URLs may not work.***

Repository owner: Analytical Services: Population Health, Clinical Audit and Specialist Care

Email: lifestyles@nhs.net

To contact us raise an issue on Github or via email and we will respond promptly.

# Background

This project produces the required publication outputs for the Sexual and
Reproductive Health Services (Contraception) publication: Data tables, charts,
and map data.

Data is sourced from the Sexual and Reproductive Health Activity Dataset (SRHAD),
NHS hospital admissions data, NHS Business Services Authority (NHSBA)
prescription cost analysis data, and the NHS corporate reference datasets.

# Initial package set up

Set up is done using the requirements.txt file

Run the following command in Terminal to set up the package
Note that before running the below, it is advised to delete the folder with currently
stored user packages: C:\Users\YOUR_SHORTCODE\AppData\Roaming\Python\Python39
This will reset your packages to the default install versions before updating
for this project.
```
pip install --user --no-warn-script-location -r requirements.txt
```


# Directory structure:
```
srh-services-rap
│   README.md
│   requirements.txt                      - Used to install the python dependencies
│
├───srh_code                              - This is the main code directory for this project
│   │   create_publication.py             - This script runs the entire publication
│   │   parameters.py                     - Contains parameters that define the how the publication will run
│   │
│   └───sql_code                          - This folder contains all the SQL queries used in the import data stage
│           │   query_ahas.sql
│           │   query_asset_reporting.sql
│           │   query_asset.sql
│           │   query_imd_decile.sql
│           │   query_imd_lsoa.sql
│           │   query_la_ref.sql
│           │   query_lsoa_ref.sql
│           │   query_org_daily.sql
│           │   query_org_sites.sql
│           │   query_population.sql
│           │
│       utilities                          - This folder contains all the main modules used to create the publication
│           │   charts.py                  - Defines the arguments needed to create and export chart outputs
│           │   data_connections.py        - Defines the df_from_sql function, used when importing SQL data
│           │   field_definitions.py       - Defines any derived fields added during processing.
│           │   filter_definitions.py      - Defines pe-set pipeline filters.
│           │   helpers.py                 - Contains generalised functions used within the project
│           │   load.py                    - Contains functions for reading in the required data
│           │   logger_config.py           - The configuration functions for the publication logger
│           │   pre-processing.py          - Contains the core pre-processing functions
│           │   publication_files.py       - Contains functions used to create publication ready outputs and save in relevant folders
│           │   tables.py                  - Defines the arguments needed to create and export Excel table outputs
│           │   
│           └───processing
│                 │   processing_publication.py    - Contains the core functions used to produce publication outputs
│                write                     - This folder contains all the main modules used to write the outputs to external files
│                     write_data.py        - Contains functions for writing in the data to external files
│                     write_format.py      - Contains functions for formatting the external files
└───tests
    └────unittests                         - Unit tests for Python functions
            │   test_field_definitions.py
            │   test_filter_definitions.py            
            │   test_helpers.py
            │   test_pre_processing.py        
            │   test_processing_publication.py
 
```
# Running the pipeline:

There are two main files that users running the process will need to interact with:

    * The `parameters.py` 
    * The `create_publication.py`

The file parameters.py contains all of the things that we expect to change from one publication
to the next. Indeed, if the methodology has not changed, then this should be the only file you need
to modify. A few elements require updating each year (e.g. the reporting year), but most
are likely to only require occassional updates (e.g. file paths, default codes).
It also allows the user to control which parts of the publication they want the pipeline to produce.

The publication process is run using the top-level script, create_publication.py.
This script imports and runs all the required functions from the sub-modules.

# Link to publication
https://digital.nhs.uk/data-and-information/publications/statistical/sexual-and-reproductive-health-services

# Licence
The NHS England Sexual and Reproductive Health Services (Contraception) National Statistics publication codebase is released under the MIT License.

Copyright © 2023, NHS England

You may re-use this document/publication (not including logos) free of charge in any format or medium, under the terms of the Open Government Licence v3.0. Information Policy Team, The National Archives, Kew, Richmond, Surrey, TW9 4DU; email: psi@nationalarchives.gsi.gov.uk
