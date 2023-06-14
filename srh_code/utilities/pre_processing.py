"""
Purpose of script: contains the core business logic
"""
import pandas as pd
import logging
from srh_code.utilities import helpers
from srh_code.utilities import field_definitions
from srh_code.utilities import filter_definitions
import srh_code.parameters as param
from srh_code.utilities import load

logger = logging.getLogger(__name__)


def update_non_uk_las(df):
    """
    Updates Channel Islands and Isle of Man LA codes to the general outside UK
    LA code (X99999998). Also renames the general outside UK name and parent
    code.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df : pandas.DataFrame
        with the LA codes and names updated to country level
    """
    logging.info("Updating non UK LA information")

    # Set Channel Island, Isle of Man LA codes and the outside UK code
    la_codes = ["M99999999", "L99999999", "X99999998"]
    # Set the default outside England code and name
    default_code = "X99999998"
    default_name = "Outside the United Kingdom"
    # Update the lower and upper LA codes and names to the defaults
    for la_code in la_codes:
        df.loc[df["LA_code_lower"] == la_code,
               ["LA_code", "LA_name",
                "LA_code_lower", "LA_name_lower",
                "LA_parent_code"]] = [default_code, default_name,
                                      default_code, default_name,
                                      default_code]

    return df


def update_non_english_las(df):
    """
    Updates non-English UK LA codes and names to country level (e.g. Aberdeen to
    Scotland) for reporting purposes.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df : pandas.DataFrame
        with the LA codes and names updated to country level
    """
    logging.info("Updating non-English UK LA information")

    # Update Scottish, Welsh and Northern Ireland LA details to the default
    # country codes and names
    update_info = {"S": "Scotland",
                   "W": "Wales",
                   "N": "Northern Ireland"}

    for country_prefix, country_name in update_info.items():
        country_code = country_prefix + "99999999"
        df.loc[df["LA_code_lower"].str.startswith((country_prefix)),
               ["LA_code", "LA_name",
                "LA_code_lower", "LA_name_lower",
                "LA_parent_code"]] = [country_code, country_name,
                                      country_code, country_name,
                                      country_code]

    return df


def update_small_las(df, column_code, column_name,
                     lookup=param.LA_UPDATE):
    """
    Updates small LA details to neighbouring LA details for non-
    disclosive purposes, using a dictionary of old to new org codes and names
    from the paramaters file.
    As they sit in the same region, the parent details do not require updating.

    Parameters
    ----------
    df : pandas.DataFrame that includes an org code as a variable
    column_code : str
        Column name that holds the LA codes to be updated.
        Can be set to none if only the name requires updating.
    column_name : str
        Column name that holds the LA names to be updated.
        Can be set to none if only the code required updating.
    lookup: dict(str, list)
        Dictionary containing the original org codes and names.
        and corresponding replacement values.

    Returns
    -------
    df : pandas.DataFrame
        with the codes and names updated as per the values in the
        input dictionary.
    """
    logging.info("Updating small LA information")

    # Create a dataframe from the reference data input
    df_la_update = pd.DataFrame(data=lookup)

    # Create seperate dictionaries for the org code and org name lookups
    df_code_update = dict(zip(df_la_update["From_code"],
                              df_la_update["To_code"]))
    df_name_update = dict(zip(df_la_update["From_name"],
                              df_la_update["To_name"]))

    # use the dictionaries to update the codes and names in the input dataframe
    if column_code is not None:
        df.replace({column_code: df_code_update}, inplace=True)
    if column_name is not None:
        df.replace({column_name: df_name_update}, inplace=True)

    return df


def create_la_ref_data(fyear=param.FYEAR):
    """
    Imports and makes updates to the LA and regions organisation reference
    data needed for processing. Map the parent org codes in the corporate
    reference data to parent names. Adds organisation type.

    Parameters
    ----------
    year: str
        Financial year of extract
    Returns
    -------
    df: pandas.DataFrame
        Dataframe containing LA organisation reference data with LA parent name
        and organisation type added.

    """
    logging.info("Creating the LA and regions organisation reference data")

    # Import from the corporate reference data
    df_org_ref = load.import_la_ref_data(fyear)

    # Extract the org code and org name from the reference data as a new dataframe
    df_orgs = df_org_ref[["Org_code", "Org_name"]].copy()
    # Rename org code column to parent org code
    df_orgs = df_orgs.rename(columns={"Org_code": "Parent_code",
                                      "Org_name": "Parent_name"})

    # Add parent names to parent codes in the original dataframe
    df_org_ref = pd.merge(df_org_ref, df_orgs, how="left", on="Parent_code")

    # Add organisation type and level
    df_org_ref = helpers.add_organisation_type(df_org_ref, "Org_code")

    # Default index values are reset here to support saving to feather
    return df_org_ref.reset_index(drop=True)


def map_org_code_to_name(df, df_org_ref, col_ref):
    """
    Function to map user specified org codes to its name in the
    corporate referance dataframe.

    Parameters
    ----------
    df: pandas.DataFrame
    df_org_ref: pandas.DataFrame
        corporate reference dataframe with the organisation codes and names
        (expects Org_code and Org_name in columns).
    col_ref: list(str)
        list of org code columns we want to find the organisation name for.
        Expects format to be 'orgtype'_code. e.g. LA_code, LA_parent_code

    Returns
    -------
    df : pandas.DataFrame
    """
    logging.info("Mapping organisations codes to names")

    # Filtering ref data for code and name cols
    df_org_ref = df_org_ref[["Org_code", "Org_name"]]

    # For each column in the list specified in param
    for i in col_ref:
        # Rename reference columns based on the column to be updated
        df_i = df_org_ref.rename(columns={"Org_code": i})
        i_name = i.replace("code", "")
        df_i = df_i.rename(columns={"Org_name": i_name+"name"})

        # Merge dataframe with ref data on the ref column name
        df = pd.merge(df, df_i, how="left", on=i)

    return df


def update_old_to_new_lsoa(df, df_lsoa_ref,
                           update_col="LSOA_code",
                           right_old_col="LSOA_code_old",
                           right_new_col="LSOA_code_new"):
    """
    Updates old LSOA codes to their new equivalents based on old to new LSOA
    lookup dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the LA codes to be updated
    df_lsoa_ref : pandas.DataFrame
        Dataframe containing the lookup of old to new LSOA codes
    update_col : str
        Column name in the main df that holds the LSOA data
    right_old_col : str
        Column name in the reference data that holds the old LSOA codes
    right_new_col : str
        Column name in the reference data that holds the new LSOA codes

    Returns
    -------
    df : pandas.DataFrame
        With updated codes

    """
    logging.info("Updating old to new LSOA codes")
    # Join to the old to new LSOA lookup dataframe
    df = df.merge(df_lsoa_ref, how='left',
                  left_on=[update_col], right_on=[right_old_col])

    # Update LSOA codes to the new verions where applicable
    df.loc[(df[right_new_col].notnull()),
           update_col] = df[right_new_col]

    # Drop the look up columns added during the merge
    df.drop([right_old_col, right_new_col], axis=1, inplace=True)

    return df


def create_imdref_data():
    """
    Imports the 2 required elements of the IMD reference data, and adds the IMD
    decile to a dataframe containing IMD ranked LSOA data

    Parameters
    ----------
    None

    Returns
    -------
    df_imd_ref : pandas.DataFrame

    """
    logging.info("Creating IMD reference data")

    # Import the imd coroprate reference data
    df_imd_lsoa = load.import_imd_lsoa()
    df_imd_decile = load.import_imd_decile()

    # Join to the 2 dataframes
    df_imd_ref = pd.merge(df_imd_lsoa, df_imd_decile,
                          on="IMD_rank", how="left")
    # Drop the IMD rank
    df_imd_ref.drop(["IMD_rank"], axis=1, inplace=True)

    return df_imd_ref


def update_srhad_source_data(df, df_org_ref, df_lsoa_ref, df_imd_ref, fyear):
    """
    Makes general updates to the shrad source data needed for processing
    of outputs.

    Parameters
    ----------
    df: pandas.Dataframe
        Dataframe containing the imported srhad data
    df_org_ref: pandas.Dataframe
        Dataframe containing the organisation reference data containing org_code
        and org_name fields for each organisation type and level used in outputs.
    df_lsoa_ref: pandas.Dataframe
        Dataframe containing a lookup of old to new LSOA codes
    df_imd_ref: pandas.Dataframe
        Dataframe containing the index of multiple deprivation reference data
    fyear : str
        User defined reporting financial year

    Returns
    -------
    df: pandas.DataFrame

    """
    logging.info("Applying pre-processing updates to shrad source data")

    # Apply the year re-formatting and extract the value for validation check
    df = helpers.calendar_year_to_fyear(df)
    srhad_year = df["ReportingYear"].values[0]

    # Check that the SRHAD financial year matches the expected reporting
    # financial year
    if srhad_year != fyear:
        raise ValueError(f'The reporting year in the parameters file ({fyear})\
                         does not match the financial year extacted from the \
                         SRHAD data ({srhad_year}). Please review')

    # Add the data quality check flags
    df = field_definitions.dq_duplicate_flag(df)
    df = field_definitions.dq_extreme_age_flag(df)
    df = field_definitions.dq_unknown_code_flags(df)

    # Create new field which indicates if person was resident inside or outside
    # the LA of clinic location (adds fields for lower and upper tier LA check).
    # NOTE that this is applied before small LA's are combined for other
    # table outputs in next step.
    df = field_definitions.cross_boundary_check(df,
                                                "Clinic_LA_code_lower",
                                                "LA_code_lower",
                                                "Cross_boundary_lower")
    df = field_definitions.cross_boundary_check(df,
                                                "Clinic_LA_code_upper",
                                                "LA_code",
                                                "Cross_boundary_upper")

    # Add LA parent names to LA codes using org reference data
    df = map_org_code_to_name(df,
                              df_org_ref,
                              ["LA_parent_code"])

    # Copies the unedited lower and upper LA fields as these are required
    # for the record level extract
    la_columns = ["LA_code", "LA_name", "LA_code_lower", "LA_name_lower"]
    for column in la_columns:
        unedited_column = column + "_unedited"
        df[unedited_column] = df[column]

    # Update Scottish, Welsh and Northern Ireland LA details to the default
    # country codes and names
    df = update_non_english_las(df)

    # Update Channel Island and Isle of Man LA details to the default
    # non UK LA code and name
    df = update_non_uk_las(df)

    # Makes further copies of the upper tier LA fields as versions of these
    # with small LAs still present are required for the cross boundary outputs
    la_columns = ["LA_code", "LA_name"]
    for column in la_columns:
        unedited_column = column + "_inc_small"
        df[unedited_column] = df[column]

    # Update small upper tier LA codes and names to match the LA's that their
    # data will be combined with in the LA tables / maps
    df = update_small_las(df, "LA_code", "LA_name")

    # Update old to new LSOA codes
    df = update_old_to_new_lsoa(df, df_lsoa_ref)

    # Add imd deciles by linking on LSOA code
    df_imd_ref = df_imd_ref.rename(columns={"Org_code": "LSOA_code"})
    df = pd.merge(df, df_imd_ref, on="LSOA_code", how="left")

    # Update the org code and names with the clinic codes and names
    # for those with an org code of NQ5 (Brook clinics)
    df = apply_clinic_as_org(df, "NQ5")

    # Ensure all org names are upper string
    df["Org_name"] = df["Org_name"].str.upper()

    # Create column with the standard age groups used in the outputs
    df = field_definitions.create_age_groups(df, "Age")

    # Create column with the alternate age groups used in the outputs
    df = field_definitions.create_age_groups_alt(df, "Age")

    # Update nulls in the main method field to 99 to signify no main method
    df["ContraceptiveMainMethod"] = df["ContraceptiveMainMethod"].fillna(99)

    # Create new fields with flags to indicate contraceptive care activity
    df = field_definitions.contraceptive_care_flags(df)

    # Create new fields with flags to indicate SRH code activity
    df = field_definitions.srh_activity_flags(df)

    # Create new fields with flags to indicate emergency oral contraception
    # activity and emergency IUD contraception activity
    df = field_definitions.ec_oral_iud_flags(df)

    # Create new field with count of emergency contraception items
    df = field_definitions.number_ec_items(df)

    # Create new field which indicates if person was resident outside of England
    df = field_definitions.outside_england_flag(df)

    return df


def update_population_data(df, df_org_ref, df_imd_ref):
    """
    Makes updates to the population data needed for processing of rates.

    Parameters
    ----------
    df: pandas.Dataframe
        Dataframe containing the corporate reference population data
    df_imd_ref: pandas.Dataframe
        Dataframe containing the index of multiple deprivation reference data
    Returns
    -------
    df: pandas.DataFrame

    """
    logging.info("Applying pre-processing updates to population data")

    # Create a default year field to match the SRHAD data. This is just to allow
    # linking when year has been included in outputs.
    df["ReportingYear"] = param.FYEAR

    # Replace M/F sex with 1/2 - to match admissions data.
    df["Gender"].replace(["M", "F"], ["1", "2"], inplace=True)

    # Update small LA codes to match the LA's that their data will be
    # combined with
    df = update_small_las(df, "Org_code", None)

    # Add org type to the population data to assist filtering
    df = helpers.add_organisation_type(df, "Org_code")

    # Add the parent org code from the org reference data
    df = pd.merge(df, df_org_ref[["Org_code", "Parent_code"]],
                  how="left", on="Org_code")

    # Add LA names and parent names using org reference data
    df = map_org_code_to_name(df,
                              df_org_ref,
                              ["Org_code", "Parent_code"])

    # Add imd deciles to org codes (applies to LSOA codes only)
    df = pd.merge(df, df_imd_ref, on="Org_code", how="left")

    return df


def update_prescribing_data(df, df_pres_ref, cyear):
    """
    Makes updates to the prescribing source data needed for processing
    of outputs. Checks for any new items in the data that have not yet
    been included in the reference file and advises the user.

    Parameters
    ----------
    df: pandas.Dataframe
        Dataframe containing the updated prescribing data
    df_pres_ref: pandas.Dataframe
        Dataframe containing the prescribing reference data that is used to
        allocate items in the source data to contraceptive groups.
    cyear : str
        latest reporting calendar year (should be last complete year) as derived
        from the user defined reporting financial year.
    Returns
    -------
    df: pandas.DataFrame

    """
    logging.info("Applying pre-processing updates to prescribing source data")

    # Extract the year value from the prescribing source file for validation check
    pres_year = df["Year"].values[0]

    # Check that the prescribing year matches the expected reporting calendar
    # year
    if pres_year != cyear:
        raise ValueError(f'The last complete calendar year derived from the \
                         FYEAR parameter ({cyear}) does not match the calendar \
                         year extacted from the prescribing data ({pres_year}).\
                         Please review')

    # Set the drug names in the source and ref data to lower case for non-case
    # sensitive joining
    df["Drug Name"] = df["Drug Name"].str.lower()
    df_pres_ref["Drug Name"] = df_pres_ref["Drug Name"].str.lower()

    # Join the reference data to the source data on the drug name, adding the
    # contraceptive subgroup and group from the ref data file (these are used
    # for reporting)
    df = pd.merge(df, df_pres_ref[["Drug Name", "Group", "Subgroup"]],
                  how="left", on="Drug Name")

    # Check for any new items that are not present in the reference data file.
    df_new_items = df[df["Group"].isnull()]

    # If there are items not present in the reference data file then output
    # the details to an external file and abort the process. Processing will
    # only continue once all new items have been added to the reference file.
    if len(df_new_items) > 0:
        output_path = param.VALID_DIR / "srh_prescribing_new_items.csv"
        df_new_items.to_csv(output_path, index=False)
        raise ValueError("There are new contraceptive items in the \
                         'srh_prescribing_source.csv' file that have not yet \
                         been added to the 'srh_prescribing_reference.csv' file.\
                         The list of new items have been exported to the \
                         'srh_prescribing_new_items.csv' file in the validations \
                         output folder. Please add them to the reference file \
                         before continuing")

    return df


def update_ahas_ster_vas_data(df):
    """
    Makes pre-processing updates to the ahas sterlisation and vasectomy source
    data in order that it can be combined with the equivalent SRH services data.

    Parameters
    ----------
    df: pandas.Dataframe
        Dataframe containing the imported ahas data (aggregated counts)
    Returns
    -------
    df: pandas.DataFrame

    """
    logging.info("Applying pre-processing updates to AHAS source data")

    # Apply the year re-formatting
    df = helpers.hes_year_to_fyear(df)

    # Create column with the standard age groups used in the outputs
    df = field_definitions.create_age_groups_ster_vas(df, "Age")
    # Re-aggregate the counts on the added age groups
    columns = ["ReportingYear", "PatientType", "ProcType", "Age_group"]
    df = df.groupby(columns)["Count"].sum().reset_index()

    return df


def update_srh_vas_data(df):
    """
    Extracts and applies pre-processing updates to the srh services
    vasectomy source data in order that it can be combined with the
    eqivalent AHAS data.

    Parameters
    ----------
    df: pandas.Dataframe
        Dataframe containing the pre-processed record level source SRH services
        data (output of function update_srhad_source_data)
    Returns
    -------
    df: pandas.DataFrame

    """
    logging.info("Applying pre-processing updates to SRHAD vasectomy source data")

    # Filter the record level data to vasectomy contacts
    df = filter_definitions.filter_vasectomies(df).copy()

    # Create column with the age groups needed for sterlisation and vasectomy outputs
    df = field_definitions.create_age_groups_ster_vas(df, "Age")

    # Add the patient type and procedure type identifier fields that will be
    # used to distinguish the data from ahas procedures.
    df.insert(0, "PatientType", "SRH services")
    df.insert(1, "ProcType", "Vasectomies")

    # Aggregate the data on the required fields
    columns = ["ReportingYear", "PatientType", "ProcType", "Age_group"]
    df = df.groupby(columns)["PatientID"].count().reset_index(name='Count')

    return df


def create_ster_vas_data(df_srhad, df_ahas):
    """
    Makes updates to the sterilisation and vasectomy source data needed for
    processing of outputs. Checks for any new items in the data that have not
    yet been included in the reference file and advises the user.

    Parameters
    ----------
    df: pandas.Dataframe
        Dataframe containing the imported SRH services source data
    df_ahas: pandas.Dataframe
        Dataframe containing the imported AHAS sterlisation and vasectomy
        source data
    Returns
    -------
    df: pandas.DataFrame

    """
    logging.info("Creating SRHAD and AHAS sterilisation and vasectomy source data")

    # Perform pre-processing updates on the SRHAD vasectomy data
    df_srhad = update_srh_vas_data(df_srhad)
    # Extract the financial year value for validation check
    srhad_year = df_srhad["ReportingYear"].values[0]

    # Extract and perform pre-processing updates on the AHAS data
    df_ahas = update_ahas_ster_vas_data(df_ahas)
    # Extract the financial year value for validation check
    ahas_year = df_ahas["ReportingYear"].values[0]

    # Create the combined dataset
    df = pd.concat([df_srhad, df_ahas], ignore_index=True)

    # Check that the SRHAD and AHAS financial years are the same
    if srhad_year != ahas_year:
        raise ValueError(f'The financial year extracted from the AHAS data \
                         ({ahas_year}) does not match the financial year extacted \
                         from the SRHAD data ({srhad_year}). Please review')

    return df


def apply_clinic_as_org(df, org_code):
    """
    Updates the Org_code and Org_name with the Clinic_code and Clinic_name
    for a subset of the dataframe with a given Org_code. This is because some
    independent organisations use a shared organisation code but each site is
    submitted and reported seperately.
    The old version is retained as checks for repeat patients require the
    higher level organistion code.

    Parameters
    ----------
    df : pandas DataFrame
    org_code : str
        The org code which should be updated with the clinic code.

    Returns
    -------
    df : pandas DataFrame

    """
    # Create a copy of the original organisation code as this is needed for
    # the record level extract
    df["Org_code_unedited"] = df["Org_code"]

    # Create the org code filter
    mask = df["Org_code"] == org_code

    # Where the org_code is found in the Org_code column, update the Org_code
    # column with the Clinic_code and the Org_name with the Clinic_name
    df.loc[mask, "Org_code"] = df.loc[mask, "Clinic_code"]
    df.loc[mask, "Org_name"] = df.loc[mask, "Clinic_name"]

    return df
