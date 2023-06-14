# Set the parameters for the project
import pathlib

# Sets the file paths for the project
BASE_DIR = pathlib.Path(r"projectfilepath")
INPUT_DIR = BASE_DIR / "Inputs"
OUTPUT_DIR = BASE_DIR / "Outputs"
TEMPLATE_DIR = OUTPUT_DIR / "Templates"
PUB_DIR = OUTPUT_DIR / "PublicationFiles"
TAB_DIR = PUB_DIR / "DataTables"
CHART_DIR = PUB_DIR / "Charts"
LOG_DIR = OUTPUT_DIR / "Logs"
VALID_DIR = OUTPUT_DIR / "Validations"
EXTRACT_DIR = OUTPUT_DIR / "Extract"

# Set the locations/filenames of the template files
TABLE_TEMPLATE = TEMPLATE_DIR / "sexual_reproductive_health_services_datatables.xlsx"
CHART_TEMPLATE = TEMPLATE_DIR / "sexual_reproductive_health_services_charts.xlsx"
MAP_TEMPLATE = TEMPLATE_DIR / "sexual_reproductive_health_services_mapdata.xlsx"

# Set the file paths of the prescribing data and reference data
PRESCRIBING_PATH = INPUT_DIR / "srh_prescribing_source.xlsx"
PRESCRIBING_REF_PATH = INPUT_DIR / "srh_prescribing_reference.xlsx"

# Set the data asset sql database properties
SERVER = "server"
DATABASE = "database"
TABLE_REP = "table"

# Set the names of the corporate reference data tables that contain the site
# (clinic) details for NHS and independent organisations (used for adding clinic
# details to the OHID extract).
TABLE_SITES_NHS = "table"
TABLE_SITES_IND = "table"

# Set the current reporting financial year
FYEAR = "2021-22"  # format str(YYYY-YY)
# Year of population data to be used for rates
POPULATION_YEAR = 2020   # format YYYY
# LSOA estimates have a seperate input as they are published later than the
# other estimates
POPULATION_YEAR_LSOA = 2020  # format YYYY

# Set the start and end dates for the OHID extract (run using create_extract.py)
EXTRACT_START = "01APR2021"  # format str(DDMMMYYYY) e.g. "01APR2021"
EXTRACT_END = "30APR2021"  # format str(DDMMMYYYY)

# Year of IMD data and name of LSOA field to be used from reference table
# "ENGLISH_INDICES_OF_DEP_V02"
IMD_YEAR = 2019
IMD_LSOA_FIELD = "LSOA_CODE_2011"
# Year of LSOA data that corresponds to the above IMD year
# (should be most recent census year for which data has been published)
LSOA_YEAR = 2011

# Set server/database/table names for import of AHAS (HES) data
AHAS_SERVER = "server"
AHAS_DATABASE = "database"
AHAS_APC_TABLE = "apc table"
AHAS_OP_TABLE = "op table"

# Sets which outputs should be run as part of the create_publication process
# (True or False)
RUN_TABLES_SRHAD = True  # Table outputs that use SRHAD data
RUN_TABLES_PRESCRIBING = True  # Table outputs that use prescribing data
RUN_TABLES_AHAS = True  # Table outputs that use AHAS (HES) data
RUN_CHARTS_SRHAD = True  # Chart outputs that use SRHAD data
RUN_CHARTS_PRESCRIBING = True  # Chart outputs that use prescribing data
RUN_CHARTS_AHAS = True  # Chart outputs that use AHAS (HES) data
RUN_MAPS_SRHAD = True  # Map outputs that use SRHAD data

# Set whether the final publication outputs should be written as part of the
# pipeline
RUN_PUBLICATION_OUTPUTS = True
# Worksheets to be removed from final publication file
TABLES_REMOVE = ["Crosschecks"]

# Set the symbols to be used for not applicable (null) and not shown (low
# denominator) values in the outputs
NOT_APPLICABLE = "z"
NOT_SHOWN = "#"

# List of valid filter type names to be checked. These should all have been
# set as filter options in processing.filter_dataframe.py
FILTER_TYPES = ["persons_first_contact", "persons_main_contact",
                "persons_main_method", "contacts_main_method",
                "contacts_contraception", "persons_contraception",
                "females_emergency_contraception",
                "females_emergency_contraception_imd"]

# SRH Care Activity groupings dictionary
SRH_ACTIVITY_REF = {"SRH_advice": [1],
                    "Pregnancy": [2, 3],
                    "Abortion": [4, 5, 6, 7, 8, 9, 10],
                    "Cervical_screening": [11],
                    "Psychosexual": [12, 13],
                    "Implant_removal": [19],
                    "IUS_removal": [20],
                    "IUD_removal": [21],
                    "Ultrasound": [27],
                    "PMS_menopause": [18, 22, 23, 24],
                    "Alcohol": [30],
                    "STI_care": [34],
                    "Other": [14, 15, 16, 17, 25, 26, 26, 28, 29, 31, 32, 33,
                              35, 36, 37, 38, 39, 40, 41]}

# Define the group of measures that will be returned under each measure type
MEASURES_GROUP = {"Contacts": ["MainMethodNewFlag",
                               "MainMethodChangeFlag",
                               "MainMethodMaintFlag",
                               "MainMethodAdviceFlag",
                               "EmergencyContraceptionFlag",
                               "SRHCareActivityFLag"],
                  "Activity": ["ContraceptiveCareFlag",
                               "Number_EC_items",
                               "STI_care",
                               "SRH_advice",
                               "Pregnancy",
                               "Ultrasound",
                               "Abortion",
                               "Cervical_screening",
                               "Psychosexual",
                               "Implant_removal",
                               "IUS_removal",
                               "IUD_removal",
                               "PMS_menopause",
                               "Alcohol",
                               "Other"],
                  "EC":       ["ECOralFlag",
                               "ECIUDFlag"],
                  "DQ": ["Duplicate",
                         "Unknown_LSOA_code",
                         "Unknown_LA_code",
                         "Unknown_GP_code",
                         "Unknown_Ethnicity",
                         "Extreme_age"]}

# Define the types of local level organisations that are included in the outputs
# Used to select organisation reference data for sub-regional (local) tables.
# Should contain the name of the org_code column and corresponding org_type.
# The org type must exist in df_org_ref (as extracted by query_orgref.sql)
LOCAL_LEVEL_ORGS = {"LA_code": "LA",
                    "Clinic_LA_code_upper": "LA",
                    "Clinic_LA_code_lower": "LA"}

# Small LAs to combine with larger LAs for outputs
# Reassigns City of London E09000001 to Hackney E09000012
# Reassigns Isles of Scilly E06000053 to Cornwall E06000052
# Reassigns Rutland E06000017 to Leicestershire E10000018
LA_UPDATE = {"From_code": ["E09000001",
                           "E06000053",
                           "E06000017"],
             "To_code": ["E09000012",
                         "E06000052",
                         "E10000018"],
             "From_name": ["City of London",
                           "Isles of Scilly",
                           "Rutland"],
             "To_name": ["Hackney",
                         "Cornwall",
                         "Leicestershire"]}

# Define the expected column names for the prescribing source and reference data files.
PRESCRIBING_SOURCE_COLS = ["Year", "Drug Name", "BNF Chemical Name",
                           "BNF Chapter", "BNF Section Name", "Number Items"]

PRESCRIBING_REF_COLS = ["Drug Name", "BNF Chemical Name", "BNF Chapter",
                        "Group", "Subgroup"]

# Define the OPCS procedure codes for the HES vasectomy and sterilisation data
HES_PROCEDURE_CODES = {"Vasectomies": ["N171", "N172", "N178", "N179"],
                       "Vasectomy reversals": ["N181", "N182", "N188", "N189"],
                       "Sterilisations": ["Q271", "Q272", "Q278", "Q279",
                                          "Q281", "Q282", "Q283", "Q284",
                                          "Q288", "Q289", "Q351", "Q352",
                                          "Q353", "Q354", "Q358", "Q359",
                                          "Q361", "Q362", "Q368", "Q369"],
                       "Sterilisation reversals": ["Q291", "Q292", "Q298",
                                                   "Q299", "Q371", "Q378",
                                                   "Q379"]}
