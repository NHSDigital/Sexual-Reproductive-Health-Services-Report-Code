import logging
import pandas as pd
import srh_code.parameters as param
import srh_code.utilities.helpers as helpers
import srh_code.utilities.data_connections as dbc

logger = logging.getLogger(__name__)


def import_reporting_table_data():
    """
    This function will import data filtered by a given year from
    the reporting table SQL database.
    Uses the df_from_sql function

    Parameters
    ----------
    None

    Returns
    -------
    pandas.DataFrame

    """
    logging.info("Importing SRHAD data from the SQL reporting table")

    # Load our parameters
    server = param.SERVER
    database = param.DATABASE
    table = param.TABLE_REP

    sql_folder = r"srh_code\sql_code"

    with open(sql_folder + "\query_asset_reporting.sql", "r") as sql_file:
        data = sql_file.read()

    # The parameters in the sql query file are replaced with our user
    # defined parameters
    data = data.replace("<Database>", database)
    data = data.replace("<Table>", table)

    # Get SQL data
    df = dbc.df_from_sql(data, server, database)

    return df


def import_ahas_vas_ster_data():
    """
    This function will imports vasectomy and sterilisation procedure data from
    the AHAS APC and OP SQL databases. Uses the df_from_sql function.
    Includes inputs for procedure codes to filter on which are set in the
    parameters file.

    Parameters
    ----------
    None

    Returns
    -------
    pandas.DataFrame

    """
    # Load the parameters that identify the sql table name and location
    server = param.AHAS_SERVER
    database = param.AHAS_DATABASE
    table_apc = param.AHAS_APC_TABLE
    table_op = param.AHAS_OP_TABLE

    # Get the parameters list of procedure codes for each procedure type
    proc_list_vas = param.HES_PROCEDURE_CODES["Vasectomies"]
    proc_list_vas_rev = param.HES_PROCEDURE_CODES["Vasectomy reversals"]
    proc_list_ster = param.HES_PROCEDURE_CODES["Sterilisations"]
    proc_list_ster_rev = param.HES_PROCEDURE_CODES["Sterilisation reversals"]

    # Set the general sql query folder and open the HES query
    query_name = r"\query_ahas.sql"
    sql_folder = r"srh_code\sql_code"

    with open(sql_folder + r"/" + query_name, "r") as sql_file:
        data = sql_file.read()

    # The parameters in the sql query file are replaced with our user
    # defined parameters
    data = data.replace("<Database>", database)
    data = data.replace("<TableAPC>", table_apc)
    data = data.replace("<TableOP>", table_op)
    data = data.replace("<ProcListVas>", "','".join(proc_list_vas))
    data = data.replace("<ProcListVasRev>", "','".join(proc_list_vas_rev))
    data = data.replace("<ProcListSter>", "','".join(proc_list_ster))
    data = data.replace("<ProcListSterRev>", "','".join(proc_list_ster_rev))

    # Get SQL data
    df = dbc.df_from_sql(data, server, database)

    return df


def import_la_ref_data(financial_year):
    """
    Import data from the corporate reference SQL database containing upper
    and lower tier LAs and their regions that exist in the current reporting
    year). Uses the df_from_sql function

    Parameters
    ----------
    financial_year: str
        financial year for reporting (YYYY-YY)

    Returns
    -------
    pandas.DataFrame

    """
    logging.info("Importing organisation reference data from the SQL database")

    # Set server/database/table
    server = "server"
    database = "database"
    table = "table"

    # Extract required query parameters from financial year
    fy_start, fy_end = helpers.fyear_to_year_start_end(financial_year)

    sql_folder = r"srh_code\sql_code"
    query_name = r"\query_la_ref.sql"

    with open(sql_folder + r"/" + query_name, "r") as sql_file:
        data = sql_file.read()

    # The parameters in the sql query file
    # are replaced with our user defined parameters
    data = data.replace("<Database>", database)
    data = data.replace("<Table>", table)
    data = data.replace("<FYStart>", str(fy_start))
    data = data.replace("<FYEnd>", str(fy_end))

    # Get SQL data
    df = dbc.df_from_sql(data, server, database)

    # Remove any duplicate orgs keeping most recent version where duplicated
    df = df.sort_values(by=["Org_code", "Open_date"], ascending=True)
    df = df.drop_duplicates(subset=["Org_code"], keep="last")

    return df


def import_population_data(year=param.POPULATION_YEAR,
                           year_lsoa=param.POPULATION_YEAR_LSOA):
    """
    This function will import ONS population data from the corporate reference
    SQL database for organsations that exist in the population year (LSOAs,
    Upper tier LA's, regions, and national level)
    Uses the df_from_sql function

    Parameters
    ----------
    year: int
        year of population data to be extracted
    year_lsoa: int
        year of population data to be extracted for LSOA data (this is usually
        a year behind higher level organisations.
    Returns
    -------
    pandas.DataFrame

    """
    logging.info("Importing population data from the SQL database")

    # Set server/database/table
    server = "server"
    database = "database"
    table = "table"

    sql_folder = r"srh_code\sql_code"
    query_name = r"\query_population.sql"

    with open(sql_folder + r"/" + query_name, "r") as sql_file:
        data = sql_file.read()

    # The parameters in the sql query file
    # are replaced with our user defined parameters
    data = data.replace("<Database>", database)
    data = data.replace("<Table>", table)
    data = data.replace("<YearOfCount>", str(year))
    data = data.replace("<YearOfCountLSOA>", str(year_lsoa))

    # Get SQL data
    df = dbc.df_from_sql(data, server, database)

    # Remove duplicate estimates where multiple releases have been loaded.
    # Most recent release is retained
    df = df.sort_values(by=["Org_code", "Release_date"], ascending=True)
    df = df.drop_duplicates(subset=["Org_code", "Gender", "Age_group_alt"],
                            keep="last")

    return df


def import_from_excel(file_path, sheet_name, expected_cols=None):
    """
    This function will import data from a single worksheet of an external excel
    file to a pandas dataframe, checking that all columns are as expected.

    Parameters
    ----------
    file_path: path
        Filepath of the Excel file that the data will be imported from.
    sheet_name : str
        Name of the source Excel worksheet.
    expected_cols: list[str]
        Optional list of columns names for validation against the actual column
        names.
        Default is None
    Returns
    -------
    pandas.DataFrame

    """
    logging.info(f"Importing data from {file_path}")

    # Read the excel data to a dataframe
    df = pd.read_excel(file_path, sheet_name)

    # If an expected columns list has been provided, then check against actual
    if expected_cols is not None:
        # Sort the expected column list
        expected_cols = sorted(expected_cols)

        # Add the actual column names to a list
        actual_cols = sorted(df.columns.tolist())

        # Check that the columns are as expected, raise an error if not.
        if expected_cols != actual_cols:
            raise ValueError(f"The data imported from {sheet_name} does not\
                             contain the expected column names: {expected_cols}.\
                             Please review the content")

    return df


def import_from_csv(file_path, expected_cols=None, drop_cols=None):
    """
    This function will import data from an external csv file to a pandas
    dataframe, checking that all columns are as expected.

    Parameters
    ----------
    file_path: path
        Filepath of the Excel file that the data will be imported from.
    expected_cols: list[str]
        Optional list of columns names for validation against the actual column
        names.
        Default is None
    drop_cols: list[str]
        Optional list of columns names to drop after import
        Default is None
    Returns
    -------
    pandas.DataFrame

    """
    logging.info(f"Importing data from {file_path}")

    # Read the excel data to a dataframe
    df = pd.read_csv(file_path)

    # If an expected columns list has been provided, then check against actual
    if expected_cols is not None:
        # Sort the expected column list
        expected_cols = sorted(expected_cols)

        # Add the actual column names to a list
        actual_cols = sorted(df.columns.tolist())

        # Check that the columns are as expected, raise an error if not.
        if expected_cols != actual_cols:
            raise ValueError(f"The data imported from {file_path} does not\
                             contain the expected column names: {expected_cols}.\
                             Please review the content")

    if drop_cols is not None:
        df.drop(drop_cols, axis=1, inplace=True)

    return df


def import_imd_lsoa():
    """
    This function will import data from the corporate reference SQL database
    containing a lookup of LSOA codes to IMD rank for the specified year.
    Uses the df_from_sql function

    Parameters
    ----------
    None

    Returns
    -------
    pandas.DataFrame

    """
    # Set server/database/table
    server = "server"
    database = "database"
    table = "table"
    # Set the IMD year to extract
    year = param.IMD_YEAR
    # Set the name of the LSOA field to extract
    lsoa_field = param.IMD_LSOA_FIELD

    sql_folder = r"srh_code\sql_code"
    query_name = r"\query_imd_lsoa.sql"

    with open(sql_folder + r'/' + query_name, 'r') as sql_file:
        data = sql_file.read()

    # The parameters in the sql query file are replaced with our user
    # defined parameters
    data = data.replace("<Database>", database)
    data = data.replace("<Table>", table)
    data = data.replace("<Year>", str(year))
    data = data.replace("<LSOAField>", lsoa_field)

    # Get SQL data
    df = dbc.df_from_sql(data, server, database)

    return df


def import_imd_decile():
    """
    This function will import data from the corporate reference SQL database
    containing a lookup of LSOA IMD rankings to Index of Multiple Deprivation
    deciles. Uses the df_from_sql function

    Parameters
    ----------
    None

    Returns
    -------
    pandas.DataFrame

    """
    # Set server/database/table
    server = "server"
    database = "database"
    table = "table"
    # Set the IMD year to extract
    year = param.LSOA_YEAR

    sql_folder = r"srh_code\sql_code"
    query_name = r"\query_imd_decile.sql"

    with open(sql_folder + r'/' + query_name, 'r') as sql_file:
        data = sql_file.read()

    # The parameters in the sql query file are replaced with our user
    # defined parameters
    data = data.replace("<Database>", database)
    data = data.replace("<Table>", table)
    data = data.replace("<Year>", str(year))

    # Get SQL data
    df = dbc.df_from_sql(data, server, database)

    return df


def import_lsoa_ref():
    """
    This function will import data from the corporate reference SQL database
    containing a lookup of old to new LSOA codes. Currently set to lookup from
    2001 to 2011.

    Parameters
    ----------
    None

    Returns
    -------
    pandas.DataFrame

    """
    # Set server/database/table
    server = "server"
    database = "database"
    table = "table"

    sql_folder = r"srh_code\sql_code"
    query_name = r"\query_lsoa_ref.sql"

    with open(sql_folder + r'/' + query_name, 'r') as sql_file:
        data = sql_file.read()

    # The parameters in the sql query file are replaced with our user
    # defined parameters
    data = data.replace("<Database>", database)
    data = data.replace("<Table>", table)

    # Get SQL data
    df = dbc.df_from_sql(data, server, database)

    # Where an old LSOA split into more then one new LSOA, it is assigned to
    # the first of thesw
    df = df.sort_values(by=["LSOA_code_new", "SYSTEM_CREATED_DATE"], ascending=True)
    df = df.drop_duplicates(subset=["LSOA_code_old"], keep="first")
    df = df[["LSOA_code_old", "LSOA_code_new"]]

    return df


def import_org_daily():
    """
    This function will import data from the corporate reference SQL database
    containing NHS organisation codes and names

    Parameters
    ----------
    None

    Returns
    -------
    pandas.DataFrame

    """
    logging.info("Importing org daily reference data from the SQL database")

    # Set server/database/table
    server = "server"
    database = "database"
    table = "table"

    sql_folder = r"srh_code\sql_code"
    query_name = r"\query_org_daily.sql"

    with open(sql_folder + r"/" + query_name, "r") as sql_file:
        data = sql_file.read()

    # The parameters in the sql query file
    # are replaced with our user defined parameters
    data = data.replace("<Database>", database)
    data = data.replace("<Table>", table)

    # Get SQL data
    df = dbc.df_from_sql(data, server, database)

    # Remove any duplicate orgs keeping most recent version where duplicated
    df = df.sort_values(by=["OrganisationID", "Open_date"], ascending=True)
    df = df.drop_duplicates(subset=["OrganisationID"], keep="last")

    # Drop the open date column no longer needed
    df.drop(["Open_date"], axis=1, inplace=True)

    return df


def import_org_sites(table):
    """
    This function will import data from the corporate reference SQL databases
    containing site (clinic) codes, names and postcodes.

    Parameters
    ----------
    table: str
        The name of the reference data table to extract data from.

    Returns
    -------
    pandas.DataFrame

    """
    logging.info("Importing NHS org sites reference data from the SQL database")

    # Set server/database/table
    server = "server"
    database = "database"

    sql_folder = r"srh_code\sql_code"
    query_name = r"\query_org_sites.sql"

    with open(sql_folder + r"/" + query_name, "r") as sql_file:
        data = sql_file.read()

    # The parameters in the sql query file
    # are replaced with our user defined parameters
    data = data.replace("<Database>", database)
    data = data.replace("<Table>", table)

    # Get SQL data
    df = dbc.df_from_sql(data, server, database)

    # Remove any duplicate orgs keeping most recent version where duplicated
    df = df.sort_values(by=["ClinicID", "Open_date"], ascending=True)
    df = df.drop_duplicates(subset=["ClinicID"], keep="last")

    # Drop the open date column no longer needed
    df.drop(["Open_date"], axis=1, inplace=True)

    return df
