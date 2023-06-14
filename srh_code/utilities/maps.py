from srh_code.utilities.processing.processing_publication import create_output_crosstab

"""
This module contains all the user defined inputs for each map output (data).

See the tables.py file for details of each argument.

"""


def get_maps_srhad():
    """
    Establishes the functions (contents) required for each map output
    that use SRHAD data, and the arguments needed for the write process.

    Parameters:
        None

    """
    all_outputs = [
        {"name": "map_users",
         "write_type": "excel_variable",
         "write_cell": "A2",
         "include_row_labels": True,
         "year_check_cell": None,
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_map_females_contraception]
         },
        {"name": "map_method",
         "write_type": "excel_variable",
         "write_cell": "A2",
         "include_row_labels": True,
         "year_check_cell": None,
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_map_method_larc]
         },
         ]

    return all_outputs


"""
    The following functions contain the user defined inputs that determine the
    dataframe content for each output.

    See the tables.py file for details of each argument.

Returns:
-------
    Each function returns a dataframe with the output.

"""


def create_map_females_contraception(df):
    filter_type = "persons_contraception"
    filter_condition = "(Gender == '2')"
    rows = ["LA_code"]
    columns = "Gender"
    sort_on = ["LA_code"]
    row_order = None
    column_order = ["2"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 100
    output_type = "rates"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_map_method_larc(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["LA_code"]
    columns = "ContraceptiveMainMethod"
    sort_on = ["LA_code"]
    row_order = None
    column_order = ["LARC"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"LARC": [1, 2, 3, 4]}
    include_row_total = True
    multiplier = 0.001
    output_type = "percents"
    percent_across_columns = True
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)
