from srh_code.utilities.processing.processing_publication import create_output_crosstab
from srh_code.utilities.processing.processing_publication import create_output_multi_field

"""
This module contains all the user defined inputs for each chart output (data).

See the tables.py file for details of each argument.

"""


def get_charts_srhad():
    """
    Establishes the functions (contents) required for each chart output
    that use SRHAD data, and the arguments needed for the write process.

    Parameters:
        None

    """
    all_outputs = [
        {"name": "All_contacts_year",
         "write_type": "excel_static",
         "write_cell": "L4",
         "include_row_labels": False,
         "year_check_cell": "L3",
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_chart_contacts_year,
                      create_chart_contacts_contraception_year]
         },
        {"name": "Consult_medium",
         "write_type": "excel_static",
         "write_cell": "L4",
         "include_row_labels": False,
         "year_check_cell": "L3",
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_chart_consult_medium_year]
         },
        {"name": "Likelihood_contact_contr",
         "write_type": "excel_static",
         "write_cell": "A4",
         "include_row_labels": False,
         "year_check_cell": None,
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_chart_contraception_gender]
         },
        {"name": "Likelihood_contact_contr",
         "write_type": "excel_static",
         "write_cell": "D4",
         "include_row_labels": False,
         "year_check_cell": None,
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_chart_contraception_female_age]
         },
        {"name": "Contact_reason",
         "write_type": "excel_static",
         "write_cell": "A4",
         "include_row_labels": False,
         "year_check_cell": None,
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_chart_contact_reason]
         },
        {"name": "Main_method_year",
         "write_type": "excel_static",
         "write_cell": "M6",
         "include_row_labels": False,
         "year_check_cell": "M3",
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_chart_main_method_year]
         },
        {"name": "Main_method_age",
         "write_type": "excel_static",
         "write_cell": "B5",
         "include_row_labels": False,
         "year_check_cell": None,
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_chart_main_method_age]
         },
        {"name": "EC_year",
         "write_type": "excel_static",
         "write_cell": "L4",
         "include_row_labels": False,
         "year_check_cell": "L3",
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_chart_ec_srhs_year]
         },
        {"name": "EC_u16_year",
         "write_type": "excel_static",
         "write_cell": "B13",
         "include_row_labels": False,
         "year_check_cell": "A13",
         "years_as_rows": True,
         "empty_cols": None,
         "contents_counts": [create_chart_ec_u16_year],
         "contents_percents": [create_chart_ec_u16_year_percent]
         },
        {"name": "EC_age",
         "write_type": "excel_static",
         "write_cell": "C4",
         "include_row_labels": False,
         "year_check_cell": None,
         "years_as_rows": True,
         "empty_cols": None,
         "contents": [create_chart_ec_age],
         }]

    return all_outputs


def get_charts_ahas():
    """
    Establishes the functions (contents) required for each chart that uses
    AHAS (HES) data, and the arguments needed for the write process.

    Parameters
    ----------
    None

    Returns
    -------
    list[dict]: list of dictionaries
        Containing the write information for each output
    """
    all_outputs = [
        {"name": "Vasec_steril_year",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "L4",
         "year_check_cell": "L3",
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_chart_vasec_steril_year],
         }
        ]

    return all_outputs


def get_charts_prescribing():
    """
    Establishes the functions (contents) required for each chart that uses
    prescribing data, and the arguments needed for the write process.

    Parameters
    ----------
    None

    Returns
    -------
    list[dict]: list of dictionaries
        Containing the write information for each output
    """
    all_outputs = [
        {"name": "EC_year",
         "write_type": "excel_static",
         "write_cell": "AC4",
         "include_row_labels": False,
         "year_check_cell": "AC3",
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_chart_ec_prescriptions_year]
         },
        {"name": "Prescriptions_year",
         "write_type": "excel_static",
         "write_cell": "L4",
         "include_row_labels": False,
         "year_check_cell": "L3",
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_chart_prescriptions_year]
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


def create_chart_contacts_year(df):

    filter_type = None
    filter_condition = None
    rows = ["ReportingYear"]
    columns = "Age_group"
    sort_on = None
    row_order = None
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.000001
    output_type = "counts"
    percent_across_columns = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns)


def create_chart_contacts_contraception_year(df):

    filter_type = "contacts_contraception"
    filter_condition = None
    rows = ["ReportingYear"]
    columns = "Age_group"
    sort_on = None
    row_order = None
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.000001
    output_type = "counts"
    percent_across_columns = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns)


def create_chart_consult_medium_year(df):

    filter_type = None
    filter_condition = None
    rows = ["ConsultationMedium"]
    columns = "ReportingYear"
    sort_on = None
    row_order = ["1", "Other"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = {"ConsultationMedium": {"Other": ["2", "3", "4", "5", "6", "98"]}}
    column_subgroup = None
    include_row_total = False
    multiplier = None
    output_type = "percents"
    percent_across_columns = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns)


def create_chart_contraception_gender(df):
    filter_type = "persons_contraception"
    filter_condition = "Gender.isin(['1', '2'])"
    rows = ["Age_group_alt"]
    columns = "Gender"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["1", "2"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 100
    output_type = "rates"
    percent_across_columns = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns)


def create_chart_contraception_female_age(df):
    filter_type = "persons_contraception"
    filter_condition = "(Gender == '2')"
    rows = ["Gender"]
    columns = "Age_group_alt"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["45-54", "35-44", "25-34", "20-24", "18-19", "16-17", "15",
                    "13-14"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 100
    output_type = "rates"
    percent_across_columns = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns)


def create_chart_contact_reason(df):
    filter_type = None
    filter_condition = "(Gender == '2')"
    breakdown = ["ReportingYear"]
    sort_on = None
    breakdown_order = None
    measure_type = "Contacts"
    measure_order = ["Grand_total", "SRHCareActivityFLag", "EmergencyContraceptionFlag",
                     "MainMethodAdviceFlag", "MainMethodMaintFlag",
                     "MainMethodChangeFlag", "MainMethodNewFlag"]
    breakdown_subgroup = None
    include_breakdown_total = False
    multiplier = None
    output_type = "percents"
    measures_as_rows = False

    return create_output_multi_field(df, filter_type, filter_condition,
                                     breakdown, sort_on, breakdown_order,
                                     measure_type, measure_order,
                                     breakdown_subgroup,
                                     include_breakdown_total, multiplier,
                                     output_type, measures_as_rows)


def create_chart_main_method_year(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["ContraceptiveMainMethod"]
    columns = "ReportingYear"
    sort_on = None
    row_order = ["User", "LARC", 3, 4, 2, 1, "Oral", 12, "Other"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = {"ContraceptiveMainMethod": {"LARC": [1, 2, 3, 4],
                                                "User": [5, 6, 7, 8, 9, 10, 11,
                                                         12, 13],
                                                "Oral": [7, 8],
                                                "Other": [5, 9, 10, 13, 6, 11]}}
    column_subgroup = None
    include_row_total = True
    multiplier = None
    output_type = "percents"
    percent_across_columns = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns)


def create_chart_main_method_age(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["ContraceptiveMainMethod"]
    columns = "Age_group"
    sort_on = None
    row_order = ["User", "LARC"]
    column_order = ["Grand_total", "45+", "35-44", "25-34", "20-24", "18-19",
                    "16-17", "<16"]
    column_rename = None
    row_subgroup = {"ContraceptiveMainMethod": {"LARC": [1, 2, 3, 4],
                                                "User": [5, 6, 7, 8, 9, 10, 11,
                                                         12, 13]}}
    column_subgroup = None
    include_row_total = False
    multiplier = None
    output_type = "percents"
    percent_across_columns = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns)


def create_chart_ec_u16_year(df):
    filter_type = None
    filter_condition = "(Number_EC_items != 0)"
    rows = ["ReportingYear"]
    columns = "Age_group"
    sort_on = None
    row_order = None
    column_order = ["<16"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False
    count_column = None
    sum_column = "Number_EC_items"

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns, disclosure_control,
                                  count_column, sum_column)


def create_chart_ec_u16_year_percent(df):
    filter_type = None
    filter_condition = "(Number_EC_items != 0)"
    rows = ["ReportingYear"]
    columns = "Age_group"
    sort_on = None
    row_order = None
    column_order = ["<16"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = None
    output_type = "percents"
    percent_across_columns = True
    disclosure_control = False
    count_column = None
    sum_column = "Number_EC_items"

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns, disclosure_control,
                                  count_column, sum_column)


def create_chart_vasec_steril_year(df):
    filter_type = None
    filter_condition = None
    rows = ["ProcType"]
    columns = "ReportingYear"
    sort_on = None
    row_order = ["Vasectomies", "Sterilisations"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False
    count_column = None
    sum_column = "Count"

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns, disclosure_control,
                                  count_column, sum_column)


def create_chart_ec_srhs_year(df):
    filter_type = None
    filter_condition = "(Number_EC_items != 0)"
    rows = ["Number_EC_items"]
    columns = "ReportingYear"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = True
    count_multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False
    count_column = None
    sum_column = "Number_EC_items"

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, count_multiplier, output_type,
                                  percent_across_columns, disclosure_control,
                                  count_column, sum_column)


def create_chart_ec_prescriptions_year(df):
    filter_type = None
    filter_condition = "(Group == 'Emergency')"
    rows = ["Group"]
    columns = "Year"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = True
    count_multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False
    count_column = None
    sum_column = "Number Items"

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, count_multiplier,
                                  output_type, percent_across_columns,
                                  disclosure_control, count_column, sum_column)


def create_chart_prescriptions_year(df):
    filter_type = None
    filter_condition = None
    rows = ["Group"]
    columns = "Year"
    sort_on = None
    row_order = ["LARC", "User_dependent"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = True
    count_multiplier = 0.000001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False
    count_column = None
    sum_column = "Number Items"

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, count_multiplier,
                                  output_type, percent_across_columns,
                                  disclosure_control, count_column, sum_column)


def create_chart_ec_age(df):
    filter_type = "females_emergency_contraception"
    filter_condition = "(Gender == '2')"
    rows = ["Age_group_alt"]
    columns = None
    sort_on = None
    row_order = ["Grand_total", "45-54", "35-44", "25-34", "20-24", "18-19",
                 "16-17", "13-15", "15", "13-14"]
    column_order = None
    column_rename = None
    row_subgroup = {"Age_group_alt": {"13-15": ["13-14", "15"]}}
    column_subgroup = None
    include_row_total = False
    multiplier = 1000
    output_type = "rates"
    percent_across_columns = True
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier,
                                  output_type, percent_across_columns,
                                  disclosure_control)
