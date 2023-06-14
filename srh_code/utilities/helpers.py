from pathlib import Path
import pandas as pd
import numpy as np
import math
import os
import shutil
import datetime
from itertools import chain, combinations
from decimal import Decimal, ROUND_HALF_UP, getcontext
import multiprocessing as mp
from multiprocessing import Pool


def create_folder(directory):
    """
    Creates a empty folder where it doesn't already exist
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def remove_folder(directory):
    """
    Removes the specified folder and all it's contents
    """
    if os.path.exists(directory):
        shutil.rmtree(directory)
    else:
        pass


def get_project_root() -> Path:
    """
    Return the project root path from any file in the project.

    Example:
        from shmi_improvement.utilities.helpers import get_project_root
        root_path = get_project_root()
    """
    return Path(__file__).parent.parent.parent


def get_year_range_fy(end_year: str, year_span: int):
    """
    Create list of financial year strings, given an end year and a number
    of years to go back

    Example:
        get_year_range('2020-21',2)
        returns -> ['2020-21','2019-20']

    Parameters
    ----------
    end_year: str
        end of year range in format yyyy-yy
    year_span: int
        number of years in range

    Returns
    -------
    list[str] : list of years

    """
    year_range = []

    for n_year in range(year_span):
        year = (str(int(end_year[0:4])-(n_year))
                + "-"
                + str(int(end_year[5:7])-(n_year)))
        year_range.append(year)
        n_year += 1

    # List oldest year first
    return year_range[::-1]


def get_year_range_calendar(end_year: int, year_span: int):
    """
    Create list of year integers, given an end year and a number of years to go
    back

    Example:
        get_year_range(2020,2)
        returns -> [2020,2019]
    """
    year_range = []

    for n_year in range(year_span):
        year = end_year - n_year
        year_range.append(year)
        n_year += 1

    # List oldest year first
    return year_range[::-1]


def create_year_list(df, year_field):
    """
    Creates a list of years contained in a dataframe. This list can be used
    within loops in functions used to create time series tables.

    Parameters
    ----------
    df : pandas.DataFrame
    year_field : list[str]
        Variable name that holds year data

    Returns
    -------
    years : list
        Returns a list of years, order by oldest first

    """
    # Set a list of years in the dataframe to loop through, oldest year first
    years = set(df[year_field].values)
    years = list(years)
    years.sort()

    return years


def lookup_column(df, from_column, lookup, new_column):
    """
    Add a new dataframe column by looking up values in a dictionary

    Parameters
    ----------
    df : pandas.DataFrame
    from_column: str
        name of the column containing the original values
    lookup: dict
        contains the lookup from and to values
    new_column: str
        name of the new column containing the values to added

    Returns
    -------
    df : pandas.DataFrame
        with added column
    """
    # create the lookup dataframe from the lookup input
    df_lookup = pd.DataFrame(list(lookup.items()))
    df_lookup.columns = [from_column, new_column]

    # add the new column based on the lookup df
    df = df.merge(df_lookup, how='left',
                  on=[from_column])

    return df


def replace_col_value(df, col_names, replace_value):
    """
    Will replace all values in a column(s) with a specified default value
    (is currently used for Table 14 to replace invalid regional invasive
    and non-invasive non-operative diagnosis rates)

    Parameters
    ----------
    df : pandas.DataFrame
    col_names : list[str]
        Names of columns where rate values to be replaced
    replace_value : str
        Value to replace existing rate values (e.g ":")

    Returns
    -------
    df : pandas.DataFrame
        With updated values for specified columns
    """

    for col in col_names:
        df[col] = replace_value

    return df


def remove_rows(df, remove_values):
    """
    Will remove rows from dataframe that contain the specified values

    Parameters
    ----------
    df : pandas.DataFrame
    remove_values : list[str]
        list of values based on which the rows will be removed if found
        in any df columns.

    Returns
    -------
    df : pandas.DataFrame
        With rows removed
    """
    for condition in remove_values:
        df = df[~df.eq(condition).any(axis=1)]

    return df


def excel_cell_to_col_num(cell):
    '''
    Convert Excel cell reference to Excel numeric column position for use in
    xlwings (e.g. A1 = 1, C23 = 2).

    Parameters
    ----------
    cell: str
        Excel cell reference (e.g. "A1")
    Returns
    -------
    int
        Number indicating the equivalent Excel column number
    '''
    # Convert the cell reference to column letter(s)
    col = ''.join(filter(str.isalpha, cell))

    # return the excel column number
    col_num = 0
    for c in col:
        col_num = col_num * 26 + (ord(c.upper()) - ord('A')) + 1

    return col_num


def excel_cell_to_row_num(cell):
    '''
    Convert Excel cell reference to Excel row number for use in
    xlwings (e.g. A1 = 1, C23 = 23).

    Parameters
    ----------
    cell: str
        Excel cell reference (e.g. "A1")
    Returns
    -------
    int
        Number indicating the equivalent Excel row number
    '''
    # Convert the cell reference to row number
    row_num = int(''.join(filter(str.isdigit, cell)))

    return row_num


def excel_col_letter_to_col_num(col):
    '''
    Converts an Excel column letter into the Excel column number e.g. if the
    column letter is D, then the output will be 4.

    Parameters
    ----------
    col: str
        Excel column letter

    Returns
    -------
    order of letter value: int
        Excel column number
    '''
    column_number = ord(col[0])-ord('A') + 1
    if len(col) == 1:
        column_number
    if len(col) == 2:
        column_number = (int(math.pow(26, len(col)-1) * column_number
                             + excel_col_letter_to_col_num(col[1:])))

    return column_number


def excel_col_to_df_col(col, write_cell):
    '''
    Converts an Excel column letter into a dataframe column position based on
    an a starting cell (write_cell) in Excel e.g. if the column letter is
    D, and the write_cell is B10, then the output will be 2 (3rd column in df)

    Parameters
    ----------
    col: str
        Excel column letter
    write_cell: str
        cell that identifies start of where df will be written

    Returns
    -------
    order of letter value: int
        number indicating which position to insert new column into dataframe
    '''
    if len(col) == 1:
        return (ord(col[0])) - (ord(write_cell[0]))
    if len(col) == 2:
        return (int(math.pow(26, len(col)-1)*(ord(col[0]) - ord('A') + 1)
                    + excel_col_to_df_col(col[1:], write_cell)))


def validate_value_with_list(check_name, value, valid_values):
    """
    Checks a string against a list of strings and aborts the process if it is
    not found in the list.

    Parameters
    ----------
    check_name: str
        Name of the item being checked that will be returned in the system
        exit message.
    value: str
        Value to be checked.
    valid_values: list[str]
        Contains the valid values to check against.
    """
    if value not in valid_values:
        raise ValueError(f'An invalid value has been entered in the\
                         {check_name} input. Only {valid_values} are valid values')


def add_percent_or_rate(df, new_column_name, numerator,
                        denominator, multiplier=1):
    """
    Adds a percent or rate to a dataframe based on specified column inputs.

    Parameters
    ----------
    df : pandas.DataFrame
    new_column_name: str
        Name of the new calculated column.
    numerator: str
        Name of dataframe column that contains the numerator values
    denominator: str
        Name of dataframe column that contains the denominator values
    multiplier: int
        Value by which the calculated field will be multiplied by e.g. set to
        100 for percents. If no multiplier is needed then the parameter should
        be excluded or set to 1.

    Returns
    -------
    pandas.DataFrame
    """
    if numerator not in df:
        raise ValueError(f"The column {numerator} is needed to create\
                         {new_column_name} but is not in the dataframe")
    if denominator not in df:
        raise ValueError(f"The column {denominator} is needed to create\
                         {new_column_name} but is not in the dataframe")

    df[new_column_name] = ((df[numerator]/df[denominator] * multiplier))

    return df


def add_column_difference(df,
                          new_column_name="Difference"):
    """
    Adds a difference column to a dataframe based on the last 2 columns.

    Parameters
    ----------
    df : pandas.DataFrame
    new_column_name: str
        Name of the new calculated column. Set by default to 'Difference'

    Returns
    -------
    pandas.DataFrame
    """
    # Select the last 2 columns in the dataframe
    df_columns = df.iloc[:, -2:]
    from_column = df_columns.iloc[:, 0]
    to_column = df_columns.iloc[:, 1]
    # Extract the column names of the 2 columns on which the calculation will
    # be performed
    from_column_name = from_column.name
    to_column_name = to_column.name

    # Check for numeric values in the 2 columns
    if from_column.dtypes not in ["integer", "float"]:
        raise ValueError(f"A difference calculation is being performed on column\
                         ({from_column_name}) that contains non-numeric values")
    if to_column.dtypes not in ["integer", "float"]:
        raise ValueError(f"A difference calculation is being performed on column\
                         ({to_column_name}) that contains non-numeric values")

    # Add a new column with the calculated difference
    df[new_column_name] = (to_column - from_column)

    return df


def add_subtotals(df, columns,
                  total_name="Grand_Total"):
    """
    Add row totals and sub-totals to a dataframe for all specified dataframe
    column combinations.

    Parameters
    ----------
    df : pandas.DataFrame
    columns: list[str]
        Columns to use in the breakdowns (e.g. age, sex, etc)
    total_name: str
        Default value to be assigned where totals are added.

    Returns
    -------
    pandas.DataFrame

    """

    # List to store the different sub-groups
    total_dfs = []

    # Combinations of columns to be replaced with total_name
    # Firstly don't replace any, then replace a single column, then 2 colss, etc
    # E.g. [[], ["sex"], ["age"], ["sex", "age"], ...]
    n_replacements = len(columns) + 1
    replace_combinations = [combinations(columns, n)
                            for n in range(n_replacements)]
    replace_combinations = chain.from_iterable(replace_combinations)

    for columns_to_replace in replace_combinations:
        # Make a copy of df with default values for non-grouped columns
        # inserted (e.g. replace values in 'sex' with total_name)
        default_df = df.copy()

        for col in columns_to_replace:
            default_df[col] = total_name

        # Aggregate the column values / counts
        default_df = default_df.groupby(columns).sum().reset_index()

        # Add each of the subgroup datafranes just created to the total
        # dataframe list
        total_dfs.append(default_df)

    # Add each dataframe from the list of dataframes together
    return pd.concat(total_dfs, axis=0).reset_index(drop=True)


def add_subgroup_rows(df, breakdown, subgroup):
    """
    Combines groups of values in specified dataframe column into a subgroup
    and adds new rows to the datatframe with the grouped value.

    Parameters
    ----------
    df : pandas.DataFrame
        Data with breakdowns and counts
    breakdown: list[str]
        The column(s) present in the dataframe on which the data is aggregated
        i.e. the non count/measure columns
        This can include the column to which the subgroup function is being
        applied.
    subgroup: dict(dict(str, list))
        Contain the target column name, and for each target column another
        nested dictionary with new subgroup code that will be assigned to the
        new grouping(s), and the original subgroup values that will form the
        group e.g. {"AgeBand": {'53<64': ['53-54', '55-59', '60-64']}}

    Returns
    -------
    pandas.DataFrame with subgroup added to target column

    """
    # Extract the target column, and the subgroup info (a 2nd dictionary nested
    # within the subgroup dictionary)
    for subgroup_column, subgroup_info in subgroup.items():
        # For each set of items in subgroup info
        for subgroup_code, subgroup_values in subgroup_info.items():
            # Then add new rows for the subgroup
            df_subgroup = df[df[subgroup_column].isin(subgroup_values)].copy()
            df_subgroup[subgroup_column] = subgroup_code
            df_subgroup = (
                df_subgroup.groupby([*breakdown])
                .sum()
                .reset_index()
                )
            # Add the new subgroups to the original dataframe
            df = pd.concat([df, df_subgroup], ignore_index=True)

    return df


def add_subgroup_columns(df, subgroup):
    """
    Combines groups of specified columns into a single summed column

    Parameters
    ----------
    df : pandas.DataFrame
        Data with a breakdown
    subgroup: dict(str, list)
        Contains new column name that will be assigned to the grouping,
        and the columns that will form the group.

    Returns
    -------
    pandas.DataFrame with subgroup column(s) added

    """
    for subgroup_name, subgroup_cols in subgroup.items():
        df[subgroup_name] = df[subgroup_cols].sum(axis=1)

    return df


def order_by_list(df, column, order):
    """
    Orders the dataframe based on a custom list applied to a specified column

    Parameters
    ----------
    df : pandas.DataFrame
        Data with a breakdown
    columm: str
        Column name to be ordered on.
    order: list[str]
        List that contains the custom order for the specified column
    Returns
    -------
    pandas.DataFrame with subgroup column(s) added

    """
    # Create a dummy df with the required list and the column name to sort on
    dummy = pd.Series(order, name=column).to_frame()

    # Use left merge on the dummy to return a sorted df
    ordered_df = pd.merge(dummy, df, on=column, how='left')

    return ordered_df


def group_numeric_values(df, source_field, group_name,
                         group_info, default_value):
    '''
    Creates a new column in the dataframe based on an existing one by grouping
    numeric values in the existing column

    Parameters
    ----------
    df : pandas.DataFrame
    source_field : str
        Name of the dataframe variable that contains the value on which the new
        column is based on
    group_name : str
        Name of the new column
    group_info : dict(dict)
        Dictionary containing the labels and ranges for each group
    default_value : str
        String of the initial default value upon column creation. Can be set to
        None if not required.

    Returns
    -------
        pandas.Dataframe with new column added or modified
    '''
    if default_value is not None:
        df[group_name] = default_value

    for range_label, range_info in group_info.items():
        for range_start, range_end in range_info.items():
            df.loc[df[source_field].between(range_start, range_end),
                   group_name] = range_label

    return df


def add_organisation_type(df, org_code_column, missing_value="None"):
    """
    Adds a new organisation type and level columns to a dataframe
    based on the entity codes in the organisation reference data.

    Parameters
    ----------
    df : pandas.DataFrame
    org_code_column: str
        Name of the column that will contains the organisation codes
    missing_value: str
        Value that will be returned if no organisation type can be assigned.

    Returns
    -------
    df_population : pandas.DataFrame

    """
    # Set the new columns as the default missing value
    df['Org_type'] = missing_value
    df['Org_level'] = missing_value

    # Set the Org Type
    df.loc[df[org_code_column].str.startswith(("E01")),
           ["Org_type", "Org_level"]] = ["LSOA", "LSOA"]
    df.loc[df[org_code_column].str.startswith(("E06", "E07", "E08", "E09", "E10")),
           ["Org_type", "Org_level"]] = ["LA", "Local"]
    df.loc[df[org_code_column].str.startswith(("E12")),
           ["Org_type", "Org_level"]] = ["LA_parent", "Regional"]
    df.loc[df[org_code_column].str.startswith(("E38")),
           ["Org_type", "Org_level"]] = ["CCG", "Local"]
    df.loc[df[org_code_column].str.startswith(("E54")),
           ["Org_type", "Org_level"]] = ["ICB", "Local"]
    df.loc[df[org_code_column].str.startswith(("E40")),
           ["Org_type", "Org_level"]] = ["ICB_parent", "Regional"]
    df.loc[df[org_code_column].str.startswith(("E92")),
           ["Org_type", "Org_level"]] = ["National", "National"]

    return df


def hes_year_to_fyear(df, year_field="ReportingYear"):
    '''
    Reformats the year style stored in the HES dataframe ("YYYY") to standard
    financial year format ("YYYY-YY"). e.g. 1920 to 2019-20.

    Parameters
    ----------
    df : pandas.DataFrame
    year_field : str
        Name of the dataframe variable that contains the year value

    Returns
    -------
        reformatted year
    '''
    # Reformat HES year into the required style
    df[year_field] = ("20"
                      + df[year_field].str[:2]
                      + "-"
                      + df[year_field].str[-2:])

    return df


def calendar_year_to_fyear(df, year_field="ReportingYear"):
    '''
    Reformats the calendar year style (numeric YYYY) to
    standard financial year string ("YYYY-YY)". e.g. 2021 to 2021-22.

    Parameters
    ----------
    df : pandas.DataFrame
    year_field : str
        Name of the dataframe variable that contains the year value

    Returns
    -------
        reformatted year string
    '''
    # Reformat SRHAD year into the required style
    df[year_field] = (df[year_field].astype(str).str[:4]
                      + "-"
                      + (df[year_field]+1).astype(int).astype(str).str[-2:])

    return df


def fyear_to_year_start_end(fyear):
    '''
    From a standard financial year (YYYY-YY) creates year start and year end
    outputs in date format (yyyy-mm-dd)

    Parameters
    ----------
    fyear : str
        Financial year in format YYYY-YY

    Returns
    -------
        tuple
    '''
    # Create fy start and end dates from the financial year input
    fy_start = datetime.date(int(fyear[:4]), 4, 1)
    fy_end = datetime.date(int(fyear[:4]) + 1, 3, 31)

    return (fy_start, fy_end)


def add_group_to_df(df, group_on, group_value, count_column):
    '''
    Groups a dataframe on a single column and appends it back to the original
    dataframe with a user defined value.

    group_on : str
        Name of the dataframe variable that contains the data to be grouped.
    group_value : float
        Value that will be assigned to the grouped data. e.g. if grouping
        "males" and "females" then this might be "All". Data type should be
        the same as the that in the group_on column.
    count_column : str
        Name of the dataframe variable containing the data counts.

    Returns
    -------
        pandas.Dataframe with grouped data appended.

    '''
    # Identify the position of the group on column in the dataframe. Used for
    # inserting a new group_on column into the grouped dataframe later
    insert_position = df.columns.get_loc(group_on)

    # Create a list of dataframe columns and exclude the group on and count
    # columns
    all_fields = df.columns.values.tolist()
    fields_to_remove = [group_on, count_column]
    grouped_fields = list(set(all_fields) - set(fields_to_remove))

    # created a new dataframe grouped on the required column
    df_grouped = df.groupby(grouped_fields,
                            as_index=False)[count_column].sum()
    # Insert a new column to represent the grouped data and apply the user
    # defined value
    df_grouped.insert(insert_position, group_on, group_value)

    # Append the grouped data to the original dataframe
    return pd.concat([df, df_grouped], ignore_index=True)


def suppress_column(column_to_suppress,
                    lower=1, upper=7, base=5):
    """Follows HES disclosure control guidance.
    https://digital.nhs.uk/data-and-information/data-tools-and-services/data-services/hospital-episode-statistics/change-to-disclosure-control-methodology-for-hes-and-ecds-from-september-2018
    For sub-national counts, suppress the values of a count column
    based on upper and lower bounds, and round the values above the upper bound
    to the nearest base.

    If not national level, then apply suppression and rounding as per below logic.
    If more than or equal to lower bound and less than or equal to upper bound,
    then replace the values with nulls.
    If more than upper value, then round to the nearest 5.

    Parameters
    ----------
    col_to_suppress: pd.Series
        A numeric series that should be suppressed
    lower: int
        Lower bound - default is 1
        Used to filter for values more than or equal to 1 (>=1).
    upper: int
        Upper bound - default is 7
        Used to filter for values less than or equal to 7 (<=7).
    base: int - default is 5
        Round to the nearest base.
        E.g. a value of 21 or 22 would round to 20,
        while value of 23 or 24 would round to 25.

    Returns
    -------
    pd.Series

    """
    # Copy of the column to suppress
    suppression = column_to_suppress.copy(deep=True)

    # Filter data between lower and upper bound that should be suppressed
    # for sub-national level
    should_suppress = (column_to_suppress.between(lower, upper, inclusive="both"))
    # Filter data above upper limit to be rounded for sub-national level
    should_round = (column_to_suppress > upper)

    # Suppression and rounding logic for relevant data defined by above filters
    # if data should be suppressed, replace with nulls (will be updated later)
    suppression.loc[should_suppress] = np.nan

    # If data should be rounded, round to the nearest base
    suppression.loc[should_round] = (
        suppression[should_round]
        .apply(
            lambda p: base * round(p/base)
            )
        )

    return suppression


def round_half_up(n, decimals=0):
    """
    Round a given number, n, to a given number of decimal places, rounding up
    on >=5, and down on <5. Eg. (1.5, 0) = 2, (2.4, 0) = 2

    Parameters
    ----------
    n : float
        Number to be rounded
    decimals : integer, optional
        Number of decimal places to round to. The default is 0.

    Returns
    -------
    float

    """

    # Set the context for rounding, the precision, and the method of rounding
    context = getcontext().copy()
    context.prec = decimals + 10
    context.rounding = ROUND_HALF_UP

    # Creates a Decimal object from the given number n, with the given
    # number of decimal places. The quantize method rounds to the nearest
    # integer, using the 'ROUND_HALF_UP' method
    return float(context.create_decimal(str(n)).quantize(
            Decimal('0.' + '0'*decimals), context=context))


def parallelize(data, func):
    """
    Applies parallel multi-processing to a function based on the available
    number of cores. Useful for improving speed of processes with lots of
    iterations.

    Parameters
    ----------
    data : pd.series
        Data to which the function will be applied.
    func :
        Function to be applied.

    Returns
    -------
    pd.series
    """
    # Determine the number of available cores
    num_processes = mp.cpu_count()
    # Split the data by the number of available cores
    data_split = np.array_split(data, num_processes)
    pool = Pool(num_processes)
    # Apply the function and merge processed parts
    data = pd.concat(pool.map(func, data_split))
    pool.close()
    pool.join()

    return data
