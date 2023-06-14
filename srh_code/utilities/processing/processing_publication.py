import pandas as pd
import numpy as np
import logging
from srh_code.utilities import filter_definitions, helpers
import srh_code.parameters as param

logger = logging.getLogger(__name__)


def select_population_data(columns, filter_condition):
    """
    Extracts the population data for calculating rates.

    Parameters
    ----------
    columns : list[str]
        List of non-count column names that are needed for the output.
        Function will use the information to extract the required organisation
        details (column names) from the population data.
    filter_condition : str
        Non-standard, optional dataframe filter as a string needed for some
        outputs.

    Returns
    -------
    df: pandas.DataFrame
        Containing only the organisation reference data for the required level

    """
    logging.info("Extracting the required population data")

    # Read in the population reference data from the cached folder.
    df = pd.read_feather('cached_dataframes/df_pop.ft')

    # Check the required organisation type from the columns argument, and
    # rename columns in population data as per the organisation type
    if "LA_code" in columns:
        org_type = "LA"
        df = df.rename(columns={"Org_code": "LA_code",
                                "Org_name": "LA_name",
                                "Parent_code": "LA_parent_code",
                                "Parent_name": "LA_parent_name"})
    elif "LA_parent_code" in columns:
        org_type = "LA_parent"
        df = df.rename(columns={"Org_code": "LA_parent_code",
                                "Org_name": "LA_parent_name"})
    elif "IMD_decile" in columns:
        org_type = "LSOA"
    else:
        org_type = "National"

    # Add the available columns in the population data to a list
    pop_columns = df.columns.tolist()

    # Check each value in columns to ensure it is available in the population data
    for value in columns:
        if value not in pop_columns:
            raise ValueError(f"The process is attempting to extract {value} from \
                             the population data but it does not exist. Only \
                            {pop_columns} are available. Please review the output \
                            specification")

    # Filter population df to required organisation level.
    df = df[df["Org_type"] == org_type]

    # Apply the optional general filter
    if filter_condition is not None:
        df = df.query(filter_condition)

    # Group and sum population data by the required column groupings.
    df_agg = (df.groupby(columns, as_index=False)
              ["Count"].sum())

    return df_agg


def select_org_ref_data(org_type, columns):
    """
    Extracts the valid sub regional (local) level organisation reference
    data based on the org_type argument.

    Parameters
    ----------
    org_type: str
        Level of organisation required. Valid options in this pipeline are
        only "LA".
    columns : list[str]
        List of column names that are needed for the output. Function will use
        the information to extract the required organisation details (column names)
        from the org ref data.

    Returns
    -------
    df: pandas.DataFrame
        Containing only the organisation reference data for the required level

    """
    logging.info("Extracting the required type of organisation data")

    # Read in the organisation reference data from the cached folder.
    df = pd.read_feather('cached_dataframes/df_la_ref.ft')

    # Check that a valid org_type has been used - exists in the organisation
    # reference data as added in pre_processing by helpers.add_organisation_type
    org_type_valid = df[df["Org_level"] == "Local"]
    org_type_valid = org_type_valid["Org_type"].unique().tolist()
    helpers.validate_value_with_list("Org_type",
                                     org_type,
                                     org_type_valid)

    # Extract the required organisation types
    df_org_type = df[df["Org_type"] == org_type]

    # For LA outputs, retain the lower or upper tier LA's only, as determined by
    # the level of LA being reported.
    if ("LA_code_lower" in columns) or ("Clinic_LA_code_lower" in columns):
        df_org_type = df_org_type[df_org_type["Entity_code"] != "E10"]
    elif ("LA_code" in columns) or ("Clinic_LA_code_upper" in columns):
        df_org_type = df_org_type[df_org_type["Entity_code"] != "E07"]

    # For LA of residence tables, drop the small LA's that are combined with
    # larger neighbours for reporting.
    if ("LA_code" in columns) or ("LA_code_lower" in columns):
        # Creates a list from the LA update dictionary in parameters that contains
        # details of the small LAs being combined and drops these from the dataframe
        df_la_update = pd.DataFrame(data=param.LA_UPDATE)
        small_las = df_la_update["From_code"].tolist()
        df_org_type = df_org_type[~df_org_type["Org_code"].isin(small_las)]

    # Set organisation column names that will be applied based on the org type
    # These follow the project naming convention e.g. LA_code, LA_parent_name
    org_code = org_type + "_code"
    org_name = org_type + "_name"
    parent_code = org_type + "_parent_code"
    parent_name = org_type + "_parent_name"

    # Where LA of clinic is being used in the output, then different org codes
    # and names need to be applied to match the source data.
    for clinic_column in ["Clinic_LA_code_lower", "Clinic_LA_code_upper"]:
        if clinic_column in columns:
            org_code = clinic_column
            org_name = org_code.replace("code", "name")

    # Now apply rename of the columns to the organisation data ready for joining
    # with SRHAD data.
    df_orgs = df_org_type.rename(columns={"Org_code": org_code,
                                          "Org_name": org_name,
                                          "Parent_code": parent_code,
                                          "Parent_name": parent_name})

    # Check for any item in columns that do appear in the org ref data and
    # drop these from the org ref extract requirement
    columns = [item for item in columns if item in df_orgs.columns]

    # Extract the details (column names) needed for the output
    df_orgs = df_orgs[columns]

    return df_orgs


def merge_org_ref_data(df, join_on, org_type, columns):
    """
    For local level outputs, joins the processed data for the output with the
    valid organisation details for the reporting period. All valid organisations
    will be outputted, even where no data exists for them.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the processed local level output data.
    join_on: str
        Column containing the local level organisation codes that will be
        used to join to the organisation ref data.
    org_type: str
        Level of organisation required for the output. Valid options are
        currently "LA".
    columns : list[str]
        List of column names that are needed for the output. Function will use
        the information to extract the required organisation details (column names)
        from the org ref data.

    Returns
    -------
    df: pandas.DataFrame

    """
    logging.info("Joining with organisation reference data")

    # For the required org type, extract the valid organisatons with the
    # details needed
    df_valid_orgs = select_org_ref_data(org_type, columns)
    # Where any organisation details (apart from the org code to be joined on)
    # are present in the source data, drop these. They will be replaced with
    # organisation details from the reference data.
    cols_to_keep = df.columns.difference(df_valid_orgs.columns).tolist()
    cols_to_keep = [join_on] + cols_to_keep
    # Merge the organisation details with the data.
    # Where no data exists for an org, replace the nulls with 0.
    df = (pd.merge(df_valid_orgs, df[cols_to_keep],
                   how="left", on=join_on)
          .fillna(0))

    return df


def filter_dataframe(df, filter_type, filter_condition, output_type):
    """
    Filters a dataframe with optional filters required.

    Parameters
    ----------
    df : pandas.DataFrame
    filter_type : str
        Determines which of the pre-defined filters are to be applied to the
        dataframe
    filter_condition : str
        Ton-standard, optional dataframe filter as a string needed for some
        outputs.
    output_type : str
        Checks which of the pre-defined output types are being created
        (counts, percents, rates) for application of default filters relating
        to these.

    Returns
    -------
    df_filtered : pandas.DataFrame
        Filtered to the conditions set for the function.

    """

    if filter_type is not None:
        # Call the list of valid filter types from parameters
        valid_filter_types = param.FILTER_TYPES
        # Check for invalid fiter_type argument against the input value
        helpers.validate_value_with_list("filter_type", filter_type,
                                         valid_filter_types)

    # Apply pre-set filters from filter_definitions.py
    if filter_type == "persons_first_contact":
        df = filter_definitions.filter_persons_first_contact(df)
    if filter_type == "persons_main_contact":
        df = filter_definitions.filter_persons_main_contact(df)
    if filter_type == "contacts_main_method":
        df = filter_definitions.filter_contacts_main_method(df)
    if filter_type == "persons_main_method":
        df = filter_definitions.filter_persons_main_method(df)
    if filter_type == "contacts_contraception":
        df = filter_definitions.filter_contacts_contraception(df)
    if filter_type == "persons_contraception":
        df = filter_definitions.filter_persons_contraception(df)
    if filter_type == "females_emergency_contraception":
        df = filter_definitions.filter_females_emergency_contraception(df)
    if filter_type == "females_emergency_contraception_imd":
        df = filter_definitions.filter_females_emergency_contraception_imd(df)

    # Apply the optional general filter
    if filter_condition is not None:
        df = df.query(filter_condition)

    # Apply the standard filter for population outputs - England residents only
    # with ages 13 to 54
    if output_type == "rates":
        df = df.query("(Outside_england == 'N')")
        df = df.query("(Age_group_alt not in['<13', '55+', 'unrecorded'])")

    return df


def check_for_sort_on(sort_on, rows):
    """
    Check if the sort_on option has been used, and if so re-defines the row/breakdown
    content required for processing, in order that columns only needed for
    sorting are included, but then dropped later (cols_to_remove).

    Parameters
    ----------
    sort_on : list[str]
        list of columns names to sort on (ascending).
    rows : list[str]
        Column name(s) that holds the row/breakdown labels to be included
        in the output
    Returns
    -------
    df : pandas.DataFrame
    """

    if sort_on is not None:
        # Combine the rows and sort_on lists to ensure all are included for
        # processing (created as a set to remove fields appearing in both
        # lists)
        rows_all = set(rows + sort_on)
        # Identify any columns that are only used to sort on (will not be
        # included in the final output)
        cols_to_remove = list(set(rows_all) - set(rows))
        # Now redefine rows to also include the column(s) used for sorting only
        rows = rows + cols_to_remove
    # Else set the cols_to_remove list as empty
    else:
        cols_to_remove = []

    return (rows, cols_to_remove)


def sort_for_output_defined(df, rows, row_order):
    """
    Sorts the dataframe in the user defined order required for the output.
    If there are multiple columns in the rows list, the ordering will be
    applied on the first row in the list.

    Parameters
    ----------
    df : pandas.DataFrame
    rows : list[str]
        Variable name(s) that holds the row labels to be included
        in the output
    row_order: list[str]
        List of row content that determines the inclusions and sorting.
    Returns
    -------
    df : pandas.DataFrame
    """

    # Select the rows to include in table and apply the row order
    row = rows[0]
    df = df[(df[row].isin(row_order))]
    df = helpers.order_by_list(df, row, row_order)

    return df


def sort_for_output(df, sort_on, cols_to_remove, include_row_total=True,
                    total_name="Grand_total"):
    """
    Sorts the dataframe on specified columns required for the output.
    Drops columns only used for sorting.

    Parameters
    ----------
    df : pandas.DataFrame
    sort_on: list[str]
        Columns that will be sorted on (ascending).
    cols_to_remove : list[str]
        List containing the names of any columns to be removed (i.e. those only
        used for sorting).
    include_row_total: bool
        Determines if the grand total row will be included in the output.
        Set to True by default.
    total_name: str
        Name that was assigned to the total row that will be removed if not
        required.

    Returns
    -------
    df : pandas.DataFrame
    """
    # If total is not required then drop rows that contain the total name
    if include_row_total is False:
        df = helpers.remove_rows(df, [total_name])

    # Sort the dataframe based on columns defined by sort_on input
    df = df.sort_values(by=sort_on, ascending=True)

    # Move the total to the top of the dataframe (if present)
    if include_row_total:
        df = pd.concat([df[df.eq(total_name).any(axis=1)],
                        df[~df.eq(total_name).any(axis=1)]])

    # Drop any columns only used for sorting and not output to table
    if len(cols_to_remove) > 0:
        df.drop(columns=cols_to_remove, inplace=True)

    return df


def df_counts_to_percents(df, rows, percent_across_columns=True,
                          disclosure_control=False, measure_type=None,
                          denominator="Grand_total", round_to_dp=0, cut_off=400):
    """
    Converts a datafame containing counts, to a dataframe containing percentages
    of column or row totals.
    Includes rounding for disclosure control and check for low denomindators
    (where percents are not shown).

    Parameters
    ----------
    df : pandas.DataFrame
    rows : list[str]
        Column name(s) that holds the row labels of the output (non numeric
        columns).
    percent_across_columns: bool
        If true then percentages will be calculated across columns
        If false then percentages will be calculated down rows
    disclosure_control: bool
        Determines if the percentages will be rounded (if set to true).
        Set to False by default.
    measure_type : str
        Identifies which group of measures have been be extracted (if applicable).
        Nneeded for checking if the percent not shown rule should be ignored.
        Set to None by default as not present for non-measure outputs.
    denominator: str
        Name of the total row/column that will be used as the denominator
    round_to_dp: int
        Rounds to this number of decimal places if disclosure
        control is being applied
    cut_off: int
        If the denominator is below this level (and above zero), then the
        percent will not be calculated due to uncertain level of accuracy.
        Set to 400 by default.
    Returns
    -------
    df : pandas.DataFrame
        With percentages replacing counts
    """

    # Set the columns that don't contain counts as the index.
    df.set_index(rows, inplace=True)
    # Determine if percents are calculated based on the row or column content
    # If based on row content then the rows are temporarily transposed to
    # columns whilst percents are added.
    if not percent_across_columns:
        df = df.transpose()

    # For the data quality outputs, the rule for not showing percents based on
    # low denominators is not applied. This section checks for the DQ columns
    # in the output, and if present skips that element of processing.
    if measure_type == "DQ":
        # all records are placed in the dataframe to which percents will be applied
        df_shown = df
        # dummy dataframes with same structure are created for the not shown and
        # zero denominator checks
        df_not_shown = df.drop(df.index)
        df_zero = df_not_shown

    # For all non data quality outputs, process all rules.
    else:
        # Select rows with zero denominator (percent will not be applied)
        df_zero = df[df[denominator] == 0].copy()
        # Select rows with denominator above 0 but below cutoff (percent will
        # not be shown)
        df_not_shown = df[(df[denominator] > 0) & (df[denominator] < cut_off)].copy()
        # Select all other rows (percent will be shown)
        df_shown = df[df[denominator] >= cut_off].copy()

        # For the zero denominator and not shown data, update all cells to the
        # default values.
        df_zero = df_zero.replace({0: param.NOT_APPLICABLE})
        for column in df_not_shown.columns:
            df_not_shown[column] = param.NOT_SHOWN

    # For all other rows, the percent is now applied (rounded if disclosure
    # control is true
    df_shown = df_shown.apply(lambda a: (a/df_shown[denominator]) * 100)
    if disclosure_control:
        df_shown = df_shown.applymap(lambda a: np.inf if a == np.inf else
                                     helpers.round_half_up(a, round_to_dp))

    # Join the datasets back together
    df = pd.concat([df_zero, df_not_shown, df_shown])

    # If df was transposed before percents were added, then transpose back
    if not percent_across_columns:
        df = df.transpose()

    return df.reset_index()


def df_apply_rates(df_denom, df_num, rows, multiplier,
                   disclosure_control=False, round_to_dp=0):
    """
    Creates a dataframe with rates calculations based on 2 input dataframes
    that hold the numerator and denominator information in the
    same structure.
    Includes rounding for disclosure control.

    Parameters
    ----------
    df_num : pandas.DataFrame
        Holds the numerator counts
    df_denom : pandas.DataFrame
        Holds the denominator counts
    rows : list[str]
        Variable name(s) that holds the row information to be included
        in the output.
    multiplier : int
        Value by which the measure will be multiplied
    disclosure_control: bool
        Determines if the rates will be rounded (if set to true).
        Set to False by default.
    round_to_dp: int
        Rounds to this number of decimal places if disclosure
        control is being applied

    Returns
    -------
    df : pandas.DataFrame
        Containing only percentages
    """
    # Set the index on the row variables
    df_denom.set_index([*rows], inplace=True)
    df_num.set_index([*rows], inplace=True)

    # Apply rates to entire dataframe
    df_rates = np.divide(*df_num.align(df_denom, axis=0))
    df_rates = df_rates * multiplier

    # Round rates if disclosure control is being applied
    if disclosure_control:
        df_rates = df_rates.applymap(lambda a: np.inf if a == np.inf else
                                     helpers.round_half_up(a, round_to_dp))

    # Replace any infinity values (where denominator was 0) with the default
    # not applicable value
    df_rates.replace(np.inf, param.NOT_APPLICABLE, inplace=True)

    return df_rates.reset_index()


def create_output_crosstab(df, filter_type, filter_condition, rows, columns,
                           sort_on, row_order, column_order, column_rename,
                           row_subgroup, column_subgroup, include_row_total,
                           multiplier, output_type, percent_across_columns,
                           disclosure_control=False,
                           count_column="PatientID", sum_column=None):
    """
    Will create a crosstab output based on the user defined inputs, with
    either counts, percentages of the total, or rates per head of population.

    Parameters
    ----------
    df : pandas.DataFrame
    filter_type : str
        Determines which of the pre-defined filters are to be applied to the
        dataframe.
    filter_condition : str
        This is a non-standard, optional dataframe filter as a string
        needed for some tables. It may consist of one or more filters of the
        dataframe variables.
    rows : list[str]
        Variable name(s) that holds the row labels (e.g. regions) that are
        to be included in the output.
    columns : str
        Single variable name that holds the information to be displayed in the
        output column headers (i.e. the measure(s))
    sort_on: list[str]
        list of columns names to sort on (ascending).
        Can include columns that will not be displayed in the output.
        If row_order is not None then this argument will not be used.
    row_order: list[str]
        list of row content that determines the order data will be presented
        in the output. Allows for full control of row ordering (can only
        include row values that exist in the collection).
    column_order: list[str]
        list of column names that determines the order they will be
        presented in the output.
        If set to None then only the total will be applied.
    column_rename : dict
        Optional dictionary for renaming of columns from the data source
        version to output requirement.
    row_subgroup: dict(dict(str, list))
        Optional input where a grouped option is reported, requiring a new
        subgroup based on row content.
        Contain the target column name, and for each target column another
        nested dictionary with new subgroup code that will be assigned to the
        new grouping(s), and the original subgroup values that will form the
        group.
    column_subgroup: dict(str, list)
        Optional input where a grouped option is reported, requiring a new
        subgroup based on column content.
        Contains the new value(s) that will be assigned to the
        new grouping(s), and the values (from the 'columns' variable) that
        will form the group.
    include_row_total: bool
        Determines if the grand total row will be included in the output. Only
        applicable if row_order has not been defined.
    multiplier: num
        All counts will be multiplied by this value in the output e.g. for
        thousands set to 0.001. Rates will be multiplied by this value, e.g.
        for rate per 1000 population, set to 1000.
        Only applicable if produce_percentages is False.
    output_type: str
        Set the type of output required. Valid options are "counts", "percents"
        and "rates".
    percent_across_columns: bool
        If true then percentages will be calculated across columns
        If false then percentages will be calculated down rows
        Only applicable if output_type is "percents".
    disclosure_control: bool
        Flag set to True if disclosure control for suppressing and rounding
        should be applied.
    count_column: str
        This is the column on which the count of records will be made (all non
        null values) during aggregation. It is set by default as the
        'PatientID'. Can be overridden to sum, rather than count, a column by
        providing a sum_column input (see below).
    sum_column: str
        Column name containing counts that are to be summed.
        By default the data is aggregated as a count of records. However, this
        input can be added in order to select a column that already contains
        counts, which will then be instead summed during aggregation.

    Returns
    -------
    df : pandas.DataFrame
        in the form of a crosstab
    """

    # Set list of valid output_types that can be processed by this function
    valid_output_types = ["counts", "percents", "rates"]

    # Check for invalid output_type argument against input value
    helpers.validate_value_with_list("output_type", output_type,
                                     valid_output_types)

    # Filter data as per filter type and condition
    df_filtered = filter_dataframe(df, filter_type, filter_condition,
                                   output_type)

    # If sort_on is used, need to account for columns only used for sorting
    rows, cols_to_remove = check_for_sort_on(sort_on, rows)

    # Create a combined rows and columns list to represent all the variables
    # that will be grouped on.
    if columns is None:
        all_variables = rows
    else:
        all_variables = rows + [columns]

    # Aggregate the data and create count column. If sum_column is present then
    # this will use the sum values in that column. Else will add a count of the
    # count_column
    if sum_column is not None:
        df_agg = (df_filtered.groupby(all_variables)[sum_column]
                  .sum()
                  .reset_index(name='Count'))
    else:
        df_agg = (df_filtered.groupby(all_variables)[count_column]
                  .count()
                  .reset_index(name='Count'))

    # Create a dataframe list which will be looped through for the next steps
    # This is because for rates outputs, the same processing is applied to both the
    # counts and population data
    dfs_to_process = [df_agg]

    # If population rates are required, then select the required data and add it
    # to the df list
    if output_type == "rates":
        df_pop_agg = select_population_data(all_variables, filter_condition)
        dfs_to_process.append(df_pop_agg)

    # Create an empty list that the dfs will be added to once the following common
    # processing steps are complete.
    total_dfs = []
    # For each df run the common processing steps
    for df in dfs_to_process:

        # Pivot the data into crosstab format
        df_pivot = pd.pivot_table(df,
                                  values="Count",
                                  index=rows,
                                  columns=columns,
                                  aggfunc="sum",
                                  margins=True,
                                  margins_name="Grand_total").reset_index()

        # If no grand_total column was created (no columns content) then rename
        # the Count column to Grand_total
        if "Count" in df_pivot.columns:
            df_pivot.rename(columns={"Count": "Grand_total"}, inplace=True)

        # Replace null values created during pivoting with count of 0
        df_pivot = df_pivot.fillna(0)

        # Add any required row or column subgroups to data
        if row_subgroup is not None:
            df_pivot = helpers.add_subgroup_rows(df_pivot, rows, row_subgroup)

        if column_subgroup is not None:
            df_pivot = helpers.add_subgroup_columns(df_pivot, column_subgroup)

        # Check the rows content for the presence of one of the sub regional org
        # types defined for the project in parameters.py
        # If present then join to the valid organisation reference data.
        # This ensures all (and only) current valid organisations are included,
        # even those with no data.
        for local_col_name, local_type in param.LOCAL_LEVEL_ORGS.items():
            if local_col_name in rows:
                df_pivot = merge_org_ref_data(df_pivot,
                                              local_col_name, local_type, rows)

        # This section ensures column_order it is not empty when called in next step.
        # If no columns were defined then set it as the total count created by
        # the earlier pivot function
        if columns is None:
            column_order = ["Grand_total"]
        # Else if just no column_order was defined then set it as everything
        # present in the columns field (will be sorted ascending by default).
        elif column_order is None:
            column_order = df_pivot.set_index(rows).columns.tolist()

        # Apply count suppression and rounding. Suppressed values will be nulls
        # at this point in order that the counts remain numeric.
        # Grand total is included even if not in the output columns, as where
        # percents are calculated, they are based on rounded totals.
        if disclosure_control:
            df_pivot["Grand_total"] = helpers.suppress_column(df_pivot["Grand_total"])
            for column in column_order:
                df_pivot[column] = helpers.suppress_column(df_pivot[column])

        # Apply the count multiplier if applicable
        if (multiplier is not None) & (output_type == "counts"):
            df_pivot = (df_pivot.set_index(rows)) * multiplier
            df_pivot.reset_index(inplace=True)

        # Add the dataframe to the list of processed dataframes
        total_dfs.append(df_pivot)

    # If percents are required then replace counts with percents
    # They are calculated as a percent of the grand_total of rows or columns
    # Suppressed counts (null numerator or denominator) will remain nulls.
    if output_type == "percents":
        df_pivot = df_counts_to_percents(df_pivot, rows,
                                         percent_across_columns,
                                         disclosure_control)

    # If rates are required, then calculate these now from the processed population
    # and srhad data (in this case there will be 2 dataframes in total_dfs).
    # Suppressed counts (null numerator or denominator) will remain nulls.
    if output_type == "rates":
        df_pop = total_dfs[1]
        df_counts = total_dfs[0]
        df_pivot = df_apply_rates(df_pop, df_counts, rows, multiplier,
                                  disclosure_control)

    # Replace the suppressed null values with the standard suppression value
    df_pivot = df_pivot.fillna("*")

    if output_type == "rates":
        # Where a total rate was not applicable (zero denominator) ensure that
        # this is applied to all rates (on occasions can be otherwise overridden
        # by the suppression rule (and so shown as *).
        for column in column_order:
            df_pivot[column] = np.where(df_pivot["Grand_total"] == "z",
                                        "z",
                                        df_pivot[column])

    # Set final df column content and order (for now including any column that
    # is only used for sorting).
    df_order = df_pivot[rows + column_order]

    # Apply selected row ordering option, removing any columns only used for sorting
    if row_order is not None:
        df_order = sort_for_output_defined(df_order, rows, row_order)
    elif sort_on is not None:
        df_order = sort_for_output(df_order, sort_on, cols_to_remove,
                                   include_row_total)
    else:
        # If no ordering was done, drop the total row if not required
        if include_row_total is False:
            df_order = helpers.remove_rows(df_order, ["Grand_total"])

    # Remove any variables from rows that were only used for
    # sorting (as have now been dropped from df)
    rows = [item for item in rows if item not in cols_to_remove]

    # Rename the user selected columns as defined in column_rename dictionary
    if column_rename is not None:
        df_order = df_order.rename(columns=column_rename)

    # Restore the row labels as the index
    df_order.set_index(rows, inplace=True)

    return df_order


def create_output_multi_field(df, filter_type, filter_condition, breakdown,
                              sort_on, breakdown_order, measure_type,
                              measure_order, breakdown_subgroup,
                              include_breakdown_total,
                              multiplier, output_type,
                              measures_as_rows, disclosure_control=False):
    """
    Will create a custom output using the sum of counts for multiple
    fields based on the user defined inputs, with eiher counts, or percentages
    of the total.

    Parameters
    ----------
    df : pandas.DataFrame
    filter_type : str
        Determines which of the pre-defined filters are to be applied to the
        dataframe.
    filter_condition : str
        This is a non-standard, optional dataframe filter as a string
        needed for some tables. It may consist of one or more filters of the
        dataframe variables.
    breakdown : list[str]
        Variable name(s) that holds the breakdown labels (e.g. regions) that
        are to be included in the output.
    sort_on: list[str]
        list of columns names to sort on (ascending).
        Can include columns that will not be displayed in the output.
        If breakdown_order is not None then this argument will not be used.
    breakdown_order: list[str]
        list of breakdown content that determines the order data will be
        presented in the output. Allows for full control of row ordering
    measure_type: str
        Defines which measures will be extracted as per the MEASURES_GROUP
        dictionary in parameters.py.
    measure_order: list[str]
        list of column names that determines the order they will be
        presented in the output.
        If set to None then order from the measures parameter will be applied,
        including the total.
    breakdown_subgroup: dict(dict(str, list))
        Optional input where a grouped option is reported, requiring a new
        subgroup based on breakdown content.
        Contain the target column name, and for each target column another
        nested dictionary with new subgroup code that will be assigned to the
        new grouping(s), and the original subgroup values that will form the
        group.
    include_breakdown_total: bool
        Determines if the grand total will be included in the output. Only
        applicable if row_order has not been defined.
    multiplier: num
        All counts will be multiplied by this value in the output e.g. for
        thousands set to 0.001. Set to None if no multiplier is needed.
        Only applicable if output_type is 'counts'.
    output_type: str
        Set the type of output required. Valid options are "counts" and "percents"
    measure_as_rows: bool
        If True, then transpose the output to show measures as rows.
        If False, then keep measures as columns.
    disclosure_control: bool
        Flag set to True if disclosure control for suppressing and rounding
        should be applied.

    Returns
    -------
    df : pandas.DataFrame
        in the form of a crosstab, with aggregated counts
    """

    # Set list of valid output_types that can be processed by this function
    valid_output_types = ["counts", "percents"]

    # Check for invalid filter_type argument against input value
    helpers.validate_value_with_list("output_type", output_type,
                                     valid_output_types)

    # Filter data as per filter type and condition
    df_filtered = filter_dataframe(df, filter_type, filter_condition,
                                   output_type)

    # If sort_on is used, need to account for columns only used for sorting
    breakdown, cols_to_remove = check_for_sort_on(sort_on, breakdown)

    # Check for invalid measure_type argument against list in MEASURES_GROUP
    valid_measure_type = param.MEASURES_GROUP.keys()
    helpers.validate_value_with_list("measure_type",
                                     measure_type,
                                     valid_measure_type)

    # Get the measures group needed based on defined measure_type
    measures = param.MEASURES_GROUP[measure_type]

    # Group the data on the breakdown columns, summing up all measure columns
    df_group = (df_filtered.fillna(0).groupby(breakdown)[measures].sum())

    # Depending on the measure_base being Activity or Contacts or EC define
    # how we calculate the total of columns
    if measure_type in ["Activity", "EC"]:
        # Activity or EC total is a sum across the row
        df_group["Grand_total"] = df_group.sum(axis=1)
    elif measure_type in ["Contacts", "DQ"]:
        # Contacts total is the count of all PatientIDs
        df_count = (df_filtered.groupby(by=breakdown)
                    .agg(Grand_total=("PatientID", "count")))

        df_group = df_group.merge(df_count, how="left", on=breakdown)

    # Calculate the total of rows for each measure column (ignores index)
    df_group.loc["Grand_total", :] = df_group.sum().values
    df_group.reset_index(inplace=True)

    # Add any required breakdown subgroups to data
    if breakdown_subgroup is not None:
        df_group = helpers.add_subgroup_rows(df_group, breakdown, breakdown_subgroup)

    # Check the rows content for the presence of one of the sub regional org
    # types defined for the project in parameters.py
    # If present then join to the valid organisation reference data.
    # This ensures all (and only) current valid organisations are included,
    # even those with no data.
    for local_col_name, local_type in param.LOCAL_LEVEL_ORGS.items():
        if local_col_name in breakdown:
            df_group = merge_org_ref_data(df_group,
                                          local_col_name, local_type, breakdown)

    # Apply count suppression and rounding. Suppressed values will be nulls
    # at this point in order that the counts remain numeric.
    if disclosure_control:
        df_group["Grand_total"] = helpers.suppress_column(df_group["Grand_total"])
        for column in measures:
            df_group[column] = helpers.suppress_column(df_group[column])

    # Apply the count multiplier if applicable
    if (multiplier is not None) & (output_type == "counts"):
        df_group["Grand_total"] = df_group["Grand_total"] * multiplier
        for column in measures:
            df_group[column] = df_group[column] * multiplier

    # If percents are required then replace counts with percents. For this function
    # they are awlways calculated as a percent of the grand_total of columns
    # Suppressed counts (null numerator or denominator) will remain nulls.
    if output_type == "percents":
        percent_across_columns = True
        df_group = df_counts_to_percents(df_group, breakdown,
                                         percent_across_columns,
                                         disclosure_control, measure_type)

    # If measure_order not defined, set as per parameter order plus total
    if measure_order is None:
        measure_order = ["Grand_total"] + measures

    # Set final df column content and order (for now including any column that
    # is only used for sorting).
    df_order = df_group[breakdown + measure_order]

    # Apply selected row ordering option
    if breakdown_order is not None:
        df_order = sort_for_output_defined(df_order, breakdown, breakdown_order)
    elif sort_on is not None:
        df_order = sort_for_output(df_order, sort_on, cols_to_remove,
                                   include_breakdown_total)
        # Remove any variables from breakdown that were
        # only used for sorting (have now been dropped from df)
        breakdown = [item for item in breakdown if item not in cols_to_remove]
    else:
        # If total is not required then drop rows that contain the total name
        if include_breakdown_total is False:
            df_order = helpers.remove_rows(df_order, ["Grand_total"])

    # Replace the suppressed null values with the standard suppression value
    df_order = df_order.fillna("*")

    # Restore the breakdown labels as the index
    df_order.set_index(breakdown, inplace=True)

    # If measure_as_rows is true, transpose the dataframe
    if measures_as_rows:
        df_order = df_order.transpose()

    return df_order


def output_specific_updates(df, name):
    """
    This checks the output name and applies any transformations/updates that
    are specific to a particular output(s), that not covered by the general
    functions.

    Parameters
    ----------
    df : pandas.DataFrame
    name: str
        Name of output. This will be the worksheet name for Excel outputs and
        the filename for csv outputs.

    Returns
    -------
    df : pandas.DataFrame
    """

    if name == "map_users":
        # Filter out not applicable and not shown values for map data
        df = df[~df["2"].isin(["z", "#", "*"])]
        df.insert(0, "Measure", "Perc_pop_cont")

    if name == "map_method":
        # Filter out not applicable and not shown values for map data
        df = df[~df["LARC"].isin(["z", "#", "*"])]
        df.insert(0, "Measure", "Perc_LARC")

    if name == "Table 10":
        # Adds the percent of males attending for condom calculation. Required
        # here as the numerator and denominator use different filters.
        df["Percent_condom"] = (df[12] / df["Grand_total"]) * 100

    if name == "Table 1" and "Activity summary" in df.columns:
        avg_contacts = (df.iloc[0, 0] / df.iloc[1, 0])
        avg_df = pd.DataFrame({'Activity summary': avg_contacts},
                              index=[param.FYEAR])
        df = pd.concat([df, avg_df])

    if name in ["Table 20a", "Table 20b", "Table 20c"]:
        # Where present in df, moves the non English and unknown LA columns to
        # the end of the output.
        cols_to_move = ["Northern Ireland", "Scotland", "Wales",
                        "Outside the United Kingdom", "Not Known"]
        for col in cols_to_move:
            if col in df.columns:
                df = df.reindex(columns=[item for item in df.columns if item != col]
                                + [col])
        # Drop the All_LAs column (Grand total was renamed to this in the
        # LA column output to distinguish from the other outputs for table 20a.
        if "All_LAs" in df.columns:
            df.drop(["All_LAs"], axis=1, inplace=True)

        # For table 20c, drop any rows where there is an LA with no clinic
        # (clinic_code = 0)
        if name == "Table 20c":
            df = df.query("Clinic_code != 0")

    return df
