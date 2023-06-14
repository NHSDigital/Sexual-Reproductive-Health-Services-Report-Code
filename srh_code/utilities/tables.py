from srh_code.utilities.processing.processing_publication import create_output_crosstab
from srh_code.utilities.processing.processing_publication import create_output_multi_field

"""
This module contains all the user defined inputs for each table.
The write arguments in get_tables are defined as:

name : str
    Excel worksheet where data is to be written.
write_type: str
    Determines the method of writing the output. Valid options for Excel are:
    excel_static: Writes data to Excel where the length of the data is
    static (write_cell must be populated).
    excel_variable: Writes data to Excel where the length of the data is
    variable (write_cell must be populated).
header_cell: str
    identifies the cell location in the Excel worksheet where the header
    values will be pasted (leftmost position of header row).
    Only required for write_type = excel_with_headers.
write_cell: str
    identifies the cell location in the Excel worksheet where the data
    will be pasted (top left of data)
include_row_labels: bool
    Determines if the row labels will be written.
year_check_cell: str
    If the output is a time series table, this identifies the cell
    location in the Excel worksheet that contains the latest year value.
    Used to determine if the time series needs moving back a year before the
    new data is added.
years_as_rows: bool
    Set to true if years in a time series table are arranged in rows
    (vertical).
empty_cols: list[str]
    A list of letters representing any empty (section seperator) excel
    columns in the worksheet. Empty columns will be inserted into the
    dataframe in these positions. Default is None.
contents: list[str]
    The name of the function that creates the output.
    If more than one function is included, the outputs will be appended.
    Note that multiple contents keys can be added to the dictionary with
    different suffixes (e.g. contents_1), as long as the outputs are of the
    same length and order e.g.same organisation type. The outputs of each
    contents_key will be joined before writing, retaining only the first
    version of the row labels.

"""


def get_tables_srhad():
    """
    Establishes the functions (contents) required for each table that uses
    SRHAD data, and the arguments needed for the write process.

    Parameters
    ----------
    None

    Returns
    -------
    list[dict]: list of dictionaries
        Containing the write information for each output
    """
    all_outputs = [
      {"name": "Table 1",
       "write_type": "excel_static",
       "write_cell": "M10",
       "include_row_labels": False,
       "year_check_cell": "M5",
       "years_as_rows": False,
       "empty_cols": None,
       "contents": [create_table_contacts_year,
                    create_table_persons_year]
       },
      {"name": "Table 1",
       "write_type": "excel_static",
       "write_cell": "M13",
       "include_row_labels": False,
       "year_check_cell": "M5",
       "years_as_rows": False,
       "empty_cols": None,
       "contents": [create_table_females_year,
                    create_table_females_year_percent]
       },
      {"name": "Table 1",
       "write_type": "excel_static",
       "write_cell": "M16",
       "include_row_labels": False,
       "year_check_cell": "M5",
       "years_as_rows": False,
       "empty_cols": None,
       "contents": [create_table_males_year,
                    create_table_males_year_percent]
       },
      {"name": "Table 1",
       "write_type": "excel_static",
       "write_cell": "M20",
       "include_row_labels": False,
       "year_check_cell": "M5",
       "years_as_rows": False,
       "empty_cols": None,
       "contents": [create_table_contraception_contacts_year,
                    create_table_females_contraception_year,
                    create_table_females_contraception_method_year,
                    create_table_females_contraception_method_year_percent]
       },
      {"name": "Table 1",
       "write_type": "excel_static",
       "write_cell": "M25",
       "include_row_labels": False,
       "year_check_cell": "M5",
       "years_as_rows": False,
       "empty_cols": None,
       "contents": [create_table_method_u16_year],
       },
      {"name": "Table 1",
       "write_type": "excel_static",
       "write_cell": "M26",
       "include_row_labels": False,
       "year_check_cell": "M5",
       "years_as_rows": False,
       "empty_cols": None,
       "contents": [create_table_contraception_ec_srh_year],
       },
      {"name": "Table 2a",
       "write_type": "excel_static",
       "write_cell": "C11",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["D"],
       "contents": [create_table_contraception_gender_age],
       },
      {"name": "Table 2a",
       "write_type": "excel_static",
       "write_cell": "C16",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["D"],
       "contents": [create_table_contraception_gender_age_percent],
       },
      {"name": "Table 2a",
       "write_type": "excel_static",
       "write_cell": "C21",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": None,
       "contents": [create_table_contraception_gender_rate],
       },
      {"name": "Table 2a",
       "write_type": "excel_static",
       "write_cell": "F21",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": None,
       "contents": [create_table_contraception_gender_age_rate],
       },
      {"name": "Table 2b",
       "write_type": "excel_static",
       "write_cell": "A22",
       "include_row_labels": True,
       "year_check_cell": "A22",
       "years_as_rows": True,
       "empty_cols": ["B", "D", "N"],
       "contents_females": [create_table_contraception_female_age_year],
       "contents_males": [create_table_contraception_male_age_year]
       },
      {"name": "Table 3a",
       "write_type": "excel_static",
       "write_cell": "A18",
       "include_row_labels": True,
       "year_check_cell": "A18",
       "years_as_rows": True,
       "empty_cols": ["B", "D", "I"],
       "contents_counts": [create_table_location],
       "contents_percents": [create_table_location_percent]
       },
      {"name": "Table 3b",
       "write_type": "excel_static",
       "write_cell": "A18",
       "include_row_labels": True,
       "year_check_cell": "A18",
       "years_as_rows": True,
       "empty_cols": ["B", "D", "G"],
       "contents_counts": [create_table_consultation_medium_year],
       "contents_percents": [create_table_consultation_medium_year_percent]
       },
      {"name": "Table 4",
       "write_type": "excel_static",
       "write_cell": "C9",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["D", "I"],
       "contents": [create_table_age_reason_total]
       },
      {"name": "Table 4",
       "write_type": "excel_static",
       "write_cell": "C11",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["D", "I"],
       "contents": [create_table_age_reason_female]
       },
      {"name": "Table 4",
       "write_type": "excel_static",
       "write_cell": "C20",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["D", "I"],
       "contents": [create_table_reason_male]
       },
      {"name": "Table 4",
       "write_type": "excel_static",
       "write_cell": "C23",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["D", "I"],
       "contents": [create_table_age_reason_total_percent]
       },
      {"name": "Table 4",
       "write_type": "excel_static",
       "write_cell": "C26",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["D", "I"],
       "contents": [create_table_age_reason_female_percent]
       },
      {"name": "Table 4",
       "write_type": "excel_static",
       "write_cell": "C37",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["D", "I"],
       "contents": [create_table_reason_male_percent]
       },
      {"name": "Table 5",
       "write_type": "excel_static",
       "write_cell": "C10",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["D"],
       "contents": [create_table_contact_age,
                    create_table_activity_age]
       },
      {"name": "Table 5",
       "write_type": "excel_static",
       "write_cell": "C31",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["D"],
       "contents": [create_table_activity_age_percent]
       },
      {"name": "Table 6",
       "write_type": "excel_static",
       "write_cell": "M6",
       "include_row_labels": False,
       "year_check_cell": "M4",
       "years_as_rows": False,
       "empty_cols": None,
       "contents": [create_table_method_year,
                    create_table_method_year_percent]
       },
      {"name": "Table 7",
       "write_type": "excel_static",
       "write_cell": "C7",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": None,
       "empty_cols": None,
       "contents": [create_table_method_age,
                    create_table_method_age_percent]
       },
      {"name": "Table 8",
       "write_type": "excel_static",
       "write_cell": "C12",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["D"],
       "contents": [create_table_status_method_female]
       },
      {"name": "Table 8",
       "write_type": "excel_static",
       "write_cell": "C37",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["D"],
       "contents": [create_table_status_method_female_percent]
       },
      {"name": "Table 8",
       "write_type": "excel_static",
       "write_cell": "C27",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["D"],
       "contents": [create_table_status_method_male]
       },
      {"name": "Table 8",
       "write_type": "excel_static",
       "write_cell": "C51",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["D"],
       "contents": [create_table_status_method_male_percent]
       },
      {"name": "Table 9a",
       "write_type": "excel_static",
       "write_cell": "A18",
       "include_row_labels": True,
       "year_check_cell": "A18",
       "years_as_rows": True,
       "empty_cols": ["B"],
       "contents": [create_table_ec_year]
       },
      {"name": "Table 9a",
       "write_type": "excel_static",
       "write_cell": "G18",
       "include_row_labels": False,
       "year_check_cell": "A18",
       "years_as_rows": True,
       "empty_cols": None,
       "contents_counts": [create_table_ec_under16_year],
       "contents_percents": [create_table_ec_under16_year_percent]
       },
      {"name": "Table 9b",
       "write_type": "excel_static",
       "write_cell": "C8",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["F"],
       "contents_counts": [create_table_ec_age],
       "contents_percents": [create_table_ec_age_percent]
       },
      {"name": "Table 9c",
       "write_type": "excel_static",
       "write_cell": "C7",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": None,
       "contents_counts": [create_table_ec_female_age],
       "contents_rates": [create_table_ec_female_age_population]
       },
      {"name": "Table 10",
       "write_type": "excel_static",
       "write_cell": "A18",
       "include_row_labels": True,
       "year_check_cell": "A18",
       "years_as_rows": True,
       "empty_cols": ["B", "D"],
       "contents_counts": [create_table_male_year],
       "contents_condoms": [create_table_male_condoms_year]
       },
      {"name": "Table 11",
       "write_type": "excel_static",
       "write_cell": "D9",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["F", "H"],
       "contents_method": [create_table_method_imd_percent],
       "contents_ec_1315": [create_table_ec_13_15_imd],
       "contents_females_1554": [create_table_females_13_54_imd],
       },
      {"name": "Table 14",
       "write_type": "excel_static",
       "write_cell": "C11",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["D"],
       "contents_nat": [create_table_females_age_region_national],
       "contents_reg": [create_table_females_age_region],
       },
      {"name": "Table 14",
       "write_type": "excel_static",
       "write_cell": "C22",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["D"],
       "contents_nat": [create_table_females_method_region_national],
       "contents_reg": [create_table_females_method_region],
       },
      {"name": "Table 14",
       "write_type": "excel_static",
       "write_cell": "C24",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["D"],
       "contents": [create_table_females_method_region_percent],
       },
      {"name": "Table 15a",
       "write_type": "excel_static",
       "write_cell": "E8",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["F", "K", "N"],
       "contents_location": [create_table_location_national],
       "contents_medium": [create_table_consultation_medium_national],
       "contents_reasons": [create_table_contacts_contraception_national]
       },
      {"name": "Table 15a",
       "write_type": "excel_static",
       "write_cell": "E9",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["F", "K", "N"],
       "contents_location": [create_table_location_la_parent],
       "contents_medium": [create_table_consultation_medium_la_parent],
       "contents_reasons": [create_table_contacts_contraception_la_parent]
       },
      {"name": "Table 15a",
       "write_type": "excel_variable",
       "write_cell": "A19",
       "include_row_labels": True,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["B", "F", "K", "N"],
       "contents_location": [create_table_location_la],
       "contents_medium": [create_table_consultation_medium_la],
       "contents_reasons": [create_table_contacts_contraception_la]
       },
      {"name": "Table 15b",
       "write_type": "excel_static",
       "write_cell": "D8",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["E", "J", "M"],
       "contents_location": [create_table_location_national],
       "contents_medium": [create_table_consultation_medium_national],
       "contents_reasons": [create_table_contacts_contraception_national]
       },
      {"name": "Table 15b",
       "write_type": "excel_variable",
       "write_cell": "A10",
       "include_row_labels": True,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["B", "E", "J", "M"],
       "contents_location": [create_table_location_provider],
       "contents_medium": [create_table_consultation_medium_provider],
       "contents_reasons": [create_table_contacts_contraception_provider]
       },
      {"name": "Table 16a",
       "write_type": "excel_static",
       "write_cell": "E9",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["M", "V", "Y", "AH", "AQ"],
       "contents_counts_f": [create_table_females_age_national,
                             create_table_females_age_la_parent],
       "contents_rates_f": [create_table_females_age_national_rate,
                            create_table_females_age_la_parent_rate],
       "contents_counts_m": [create_table_males_age_national,
                             create_table_males_age_la_parent],
       "contents_rates_m": [create_table_males_age_national_rate,
                            create_table_males_age_la_parent_rate],
       "contents_counts_f_roc": [create_table_females_contraception_age_national,
                                 create_table_females_contraception_age_la_parent],
       "contents_rates_f_roc": [create_table_females_contraception_age_national_rate,
                                create_table_females_contraception_age_la_parent_rate],
       "contents_counts_m_roc": [create_table_males_contraception_age_national,
                                 create_table_males_contraception_age_la_parent],
       "contents_rates_m_roc": [create_table_males_contraception_age_national_rate,
                                create_table_males_contraception_age_la_parent_rate]
       },
      {"name": "Table 16a",
       "write_type": "excel_variable",
       "write_cell": "A20",
       "include_row_labels": True,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["B", "M", "V", "Y", "AH", "AQ"],
       "contents_counts_f": [create_table_females_age_la],
       "contents_rates_f": [create_table_females_age_la_rate],
       "contents_counts_m": [create_table_males_age_la],
       "contents_rates_m": [create_table_males_age_la_rate],
       "contents_counts_f_roc": [create_table_females_contraception_age_la],
       "contents_rates_f_roc": [create_table_females_contraception_age_la_rate],
       "contents_counts_m_roc": [create_table_males_contraception_age_la],
       "contents_rates_m_roc": [create_table_males_contraception_age_la_rate]
       },
      {"name": "Table 16b",
       "write_type": "excel_static",
       "write_cell": "D8",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["L", "N", "W"],
       "contents_counts_f": [create_table_females_age_national],
       "contents_counts_m": [create_table_males_age_national],
       "contents_counts_f_roc": [create_table_females_contraception_age_national],
       "contents_counts_m_roc": [create_table_males_contraception_age_national]
       },
      {"name": "Table 16b",
       "write_type": "excel_variable",
       "write_cell": "A10",
       "include_row_labels": True,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["B", "L", "N", "W"],
       "contents_counts_f": [create_table_females_age_provider],
       "contents_counts_m": [create_table_males_age_provider],
       "contents_counts_f_roc": [create_table_females_contraception_age_provider],
       "contents_counts_m_roc": [create_table_males_contraception_age_provider]
       },
      {"name": "Table 17a",
       "write_type": "excel_static",
       "write_cell": "E9",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["F", "L", "R", "X"],
       "contents_counts": [create_table_females_method_national,
                           create_table_females_method_la_parent],
       "contents_percents": [create_table_females_method_national_percent,
                             create_table_females_method_la_parent_percent],
       },
      {"name": "Table 17a",
       "write_type": "excel_variable",
       "write_cell": "A20",
       "include_row_labels": True,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["B", "F", "L", "R", "X"],
       "contents_counts": [create_table_females_method_la],
       "contents_percents": [create_table_females_method_la_percent],
       },
      {"name": "Table 17b",
       "write_type": "excel_static",
       "write_cell": "D9",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["E", "K", "Q", "W"],
       "contents_counts": [create_table_females_method_national],
       "contents_percents": [create_table_females_method_national_percent],
       },
      {"name": "Table 17b",
       "write_type": "excel_variable",
       "write_cell": "A11",
       "include_row_labels": True,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["B", "E", "K", "Q", "W"],
       "contents_counts": [create_table_females_method_provider],
       "contents_percents": [create_table_females_method_provider_percent],
       },
      {"name": "Table 18a",
       "write_type": "excel_static",
       "write_cell": "E8",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["H"],
       "contents_counts": [create_table_ec_age_national,
                           create_table_ec_age_la_parent],
       "contents_rates": [create_table_ec_age_national_rate,
                          create_table_ec_age_la_parent_rate]
       },
      {"name": "Table 18a",
       "write_type": "excel_static",
       "write_cell": "A19",
       "include_row_labels": True,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["B", "H"],
       "contents_counts": [create_table_ec_age_la],
       "contents_rates": [create_table_ec_age_la_rate],
       },
      {"name": "Table 18b",
       "write_type": "excel_static",
       "write_cell": "D8",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": None,
       "contents_counts": [create_table_ec_age_national],
       },
      {"name": "Table 18b",
       "write_type": "excel_variable",
       "write_cell": "A10",
       "include_row_labels": True,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["B"],
       "contents_counts": [create_table_ec_age_provider],
       },
      {"name": "Table 19a",
       "write_type": "excel_static",
       "write_cell": "E8",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["F"],
       "contents_counts": [create_table_all_activity_national,
                           create_table_all_activity_la_parent],
       },
      {"name": "Table 19a",
       "write_type": "excel_variable",
       "write_cell": "A19",
       "include_row_labels": True,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["B", "F"],
       "contents_counts": [create_table_all_activity_la],
       },
      {"name": "Table 19b",
       "write_type": "excel_static",
       "write_cell": "D8",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["E"],
       "contents_counts": [create_table_all_activity_national],
       },
      {"name": "Table 19b",
       "write_type": "excel_variable",
       "write_cell": "A10",
       "include_row_labels": True,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["B", "E"],
       "contents_counts": [create_table_all_activity_provider],
       },
      {"name": "Table 20a",
       "write_type": "excel_variable",
       "write_cell": "A9",
       "include_row_labels": True,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["B", "G"],
       "contents_counts": [create_table_laclinic_cross_boundary_upper],
       "contents_percents": [create_table_laclinic_cross_boundary_upper_percent],
       },
      {"name": "Table 20a",
       "write_type": "excel_with_headers",
       "header_cell": "K7",
       "write_cell": "K9",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": None,
       "contents": [create_table_laclinic_lares_upper]
       },
      {"name": "Table 20b",
       "write_type": "excel_variable",
       "write_cell": "A9",
       "include_row_labels": True,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["B", "G"],
       "contents_counts": [create_table_laclinic_cross_boundary_lower],
       "contents_percents": [create_table_laclinic_cross_boundary_lower_percent],
       },
      {"name": "Table 20b",
       "write_type": "excel_with_headers",
       "header_cell": "K7",
       "write_cell": "K9",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": None,
       "contents": [create_table_laclinic_lares_lower]
       },
      {"name": "Table 20c",
       "write_type": "excel_variable",
       "write_cell": "A9",
       "include_row_labels": True,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["B"],
       "contents": [create_table_laclinic_clinic_total]
       },
      {"name": "Table 20c",
       "write_type": "excel_with_headers",
       "header_cell": "H7",
       "write_cell": "H9",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": None,
       "contents": [create_table_laclinic_clinic_lares_upper]
       },
      {"name": "Table 21",
       "write_type": "excel_static",
       "write_cell": "E17",
       "include_row_labels": False,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["F"],
       "contents_contacts": [create_table_contacts_year],
       "contents_dq": [create_table_dq_national]
       },
      {"name": "Table 21",
       "write_type": "excel_variable",
       "write_cell": "A19",
       "include_row_labels": True,
       "year_check_cell": None,
       "years_as_rows": False,
       "empty_cols": ["B", "D", "F"],
       "contents_contacts": [create_table_dq_contacts_provider],
       "contents_dq": [create_table_dq_provider]
       }
      ]
    return all_outputs


def get_tables_prescribing():
    """
    Establishes the functions (contents) required for each table that uses
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
        {"name": "Table 1",
         "write_type": "excel_static",
         "write_cell": "M42",
         "include_row_labels": False,
         "year_check_cell": "M39",
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_table_prescriptions_year],
         },
        {"name": "Table 13",
         "write_type": "excel_static",
         "write_cell": "M6",
         "include_row_labels": False,
         "year_check_cell": "M4",
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_table_prescriptions_type_year]
         },
        ]

    return all_outputs


def get_tables_ahas():
    """
    Establishes the functions (contents) required for each table that uses
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
        {"name": "Table 1",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "M29",
         "year_check_cell": "M5",
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_table_vasec_steril_year]
         },
        {"name": "Table 1",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "M32",
         "year_check_cell": "M5",
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_table_vasectomies_year]
         },
        {"name": "Table 1",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "M37",
         "year_check_cell": "M5",
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_table_vasectomies_reversal_year]
         },
        {"name": "Table 12",
         "write_type": "excel_static",
         "include_row_labels": False,
         "write_cell": "D8",
         "year_check_cell": None,
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_table_sterilisation_age]
         },
        {"name": "Table 12",
         "write_type": "excel_static",
         "write_cell": "E9",
         "include_row_labels": False,
         "year_check_cell": None,
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_table_sterilisation_age_percent]
         },
        {"name": "Table 12",
         "write_type": "excel_static",
         "write_cell": "G8",
         "include_row_labels": False,
         "year_check_cell": None,
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_table_vasectomies_age]
         },
        {"name": "Table 12",
         "write_type": "excel_static",
         "write_cell": "H9",
         "include_row_labels": False,
         "year_check_cell": None,
         "years_as_rows": False,
         "empty_cols": None,
         "contents": [create_table_vasectomies_age_percent]
         },
        ]

    return all_outputs


"""
    The following functions contain the user defined inputs that determine the
    dataframe content for each output. The arguments are defined as:

    filter_type : str
        Determines which of the pre-defined filters are to be applied to the
        dataframe.
    filter_condition : str
        This is a non-standard, optional dataframe filter as a string
        needed for some tables. It may consist of one or more filters of the
        dataframe variables.
        Note that any rates outputs are filtered to ages 13 to 54 by default.
        However, any further  filters required for rates tables must be included
        here to ensure that the population data is filtered correctly e.g.
        Gender = '2' for females.
    rows : list[str]
        Variable name(s) that holds the output row content (mutliple variables
        can be selected).
        Applies to create_output_crosstab function only.
    columns : str
        Variable name that holds the output column content (single variable)
        If set to None then output will be in a list format (based on rows
        content) without counts.
        Applies to create_output_crosstab function only.
    breakdown : list[str]
        Variable name(s) that holds the breakdown labels (e.g. regions) that
        are to be included in the output.
        Applies to the create_output_multi_field function only.
    sort_on : list[str]
        Optional list of column names to sort on (ascending).
        Can include columns that will not be displayed in the output.
        If row_order / breakdown_order is not None then this argument will not
        be used.
    row_order/breakdown_order: list[str]
        Optional list of row/breakdown content that determines the order data
        will be presented in the output. Allows for full control of ordering.
    column_order: list[str]
        Optional list of content from the "columns" variable that determines
        what is included and the order they will be presented in the output.
        This can include derived variables as long as they have been added to
        field_definitions.py.
        If set to None then only the grand total of columns will be included.
        Applies to create_output_crosstab function only.
    breakdown_order: list[str]
        list of breakdown content that determines the order data will be
        presented in the output. Allows for full control of row ordering
        (can only include row values that exist in the collection).
        Applies to the create_output_multi_field function only.
    measure_type: str
        Defines which measures will be extracted as per the MEASURES_GROUP
        dictionary in parameters.py.
        Applies to the create_output_multi_field function only.
    measure_order: list[str]
        list of column names that determines the order they will be
        presented in the output.
        If set to None then order from the measures parameter will be applied,
        including the total.
        Applies to create_output_multi_field function only.
    column_rename : dict
        Optional dictionary for renaming of columns from the data source
        version to output requirement. Any column set within the "rows" or
        "column order" parameters can be renamed.
    row/breakdown_subgroup: dict(dict(str, list))
        Optional input where a grouped option is reported, requiring a new
        subgroup based on row/breakdown content.
        Contain the target column name, and for each target column another
        nested dictionary with new subgroup code that will be assigned to the
        new grouping(s), and the original subgroup values that will form the.
        group e.g. {"Age": {"53<64": ["53-54", "55-59", "60-64"]}}
    column_subgroup / measure_subroup: dict(str, list)
        Optional input where a grouped option is reported, requiring a new
        subgroup based on column content.
        Contains the new value(s) that will be assigned to the
        new grouping(s), and the values (from the "columns" variable) that
        will form the group.
        Applies to create_output_crosstab function only.
    include_row_total: bool
        Determines if the grand total row will be included in the output. Only
        applicable if row_order has not been defined.
    multiplier: num
        All counts will be multiplied by this value in the output e.g. for
        thousands set to 0.001. Rates will be multiplied by this value, e.g.
        for rate per 1000 population, set to 1000. Set to None if no multiplier
        is needed.
    output_type: str
        Set the type of output required. Valid options are "counts", "percents"
        and "rates" ("rates" for create_output_crosstab function only).
        Note that the rates output uses the processesed population data, and
        so only columns avaiable in the population data can be used as row/
        column inputs and filters (ReportingYear, LA_code, LA_parent_code,
                                   Gender, Age_group_alt and IMD_decile)
    percent_across_columns: bool
        If true then percentages will be calculated across columns
        If false then percentages will be calculated down rows
        Only applicable if output_type is "percents".
    measure_as_rows: bool
        If True, then transpose the output to show measures as rows.
        If False, then keep measures as columns.
        Applies to the create_output_multi_field function only.
    disclosure_control: bool
        flag set to True if disclosure control for suppressing and rounding
        should be applied
    count_column: str
        This is the column on which the count of records will be made (all non
        null values) during aggregation. It is set by default as the
        'PatientID'. Can be overridden to sum, rather than count, a column by
        providing a sum_column input (see below)
    sum_column: str
        Column name containing counts that are to be summed.
        By default the data is aggregated as a count of records. However, this
        input can be added in order to select a column that already contains
        counts, which will then be instead summed during aggregation.

Returns:
-------
    Each function returns a dataframe with the output.

"""


def create_table_contacts_year(df):
    filter_type = None
    filter_condition = None
    rows = ["ReportingYear"]
    columns = None
    sort_on = None
    row_order = None
    column_order = None
    # Note that the total column is renamed here so that it can be easily
    # identified for use in the output_specific_updates function when adding
    # average contacts
    column_rename = {"Grand_total": "Activity summary"}
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_persons_year(df):
    filter_type = 'persons_first_contact'
    filter_condition = None
    rows = ["ReportingYear"]
    columns = None
    sort_on = None
    row_order = None
    column_order = None
    # Note that the total column is renamed here so that it can be easily
    # identified for use in the output_specific_updates function when adding
    # average contacts
    column_rename = {"Grand_total": "Activity summary"}
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_year(df):
    filter_type = 'persons_first_contact'
    filter_condition = "(Gender == '2')"
    rows = ["Age_group_alt"]
    columns = 'ReportingYear'
    sort_on = None
    row_order = ["Grand_total", "<16"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = {"Age_group_alt": {"<16": ["<13", "13-14", "15"]}}
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_year_percent(df):
    filter_type = 'persons_first_contact'
    filter_condition = "(Gender == '2')"
    rows = ["Age_group_alt"]
    columns = 'ReportingYear'
    sort_on = None
    row_order = ["<16"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = {"Age_group_alt": {"<16": ["<13", "13-14", "15"]}}
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "percents"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_males_year(df):
    filter_type = 'persons_first_contact'
    filter_condition = None
    rows = ["Gender"]
    columns = 'ReportingYear'
    sort_on = None
    row_order = ["1"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_males_year_percent(df):
    filter_type = 'persons_first_contact'
    filter_condition = None
    rows = ["Gender"]
    columns = 'ReportingYear'
    sort_on = None
    row_order = ["1"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "percents"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_contraception_contacts_year(df):
    filter_type = "contacts_contraception"
    filter_condition = None
    rows = ["ContraceptiveMainMethod"]
    columns = "ReportingYear"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_contraception_year(df):
    filter_type = "persons_contraception"
    filter_condition = "(Gender == '2')"
    rows = ["ContraceptiveMainMethod"]
    columns = "ReportingYear"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_contraception_method_year(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["ContraceptiveMainMethod"]
    columns = "ReportingYear"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_contraception_method_year_percent(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["ContraceptiveMainMethod"]
    columns = "ReportingYear"
    sort_on = None
    row_order = ["LARC", "User"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = {"ContraceptiveMainMethod": {"LARC": [1, 2, 3, 4],
                                                "User": [5, 6, 7, 8, 9, 10, 11,
                                                         12, 13]}}
    column_subgroup = None
    include_row_total = False
    multiplier = None
    output_type = "percents"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_method_u16_year(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["ContraceptiveMainMethod"]
    columns = "Age_group"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["<16"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = True
    multiplier = None
    output_type = "percents"
    percent_across_columns = True
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_contraception_ec_srh_year(df):
    filter_type = None
    filter_condition = None
    breakdown = ["ReportingYear"]
    sort_on = None
    breakdown_order = None
    measure_type = "EC"
    measure_order = ["Grand_total"]
    breakdown_subgroup = None
    include_breakdown_total = False
    multiplier = 0.001
    output_type = "counts"
    measures_as_rows = False
    disclosure_control = False

    return create_output_multi_field(df, filter_type, filter_condition,
                                     breakdown, sort_on, breakdown_order,
                                     measure_type, measure_order,
                                     breakdown_subgroup,
                                     include_breakdown_total, multiplier,
                                     output_type, measures_as_rows,
                                     disclosure_control)


def create_table_vasec_steril_year(df):
    filter_type = None
    filter_condition = None
    rows = ["ProcType"]
    columns = "ReportingYear"
    sort_on = None
    row_order = ["Sterilisations", "Sterilisation reversals",
                 "Vasectomies"]
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


def create_table_vasectomies_year(df):
    filter_type = None
    filter_condition = "(ProcType == 'Vasectomies')"
    rows = ["PatientType"]
    columns = "ReportingYear"
    sort_on = None
    row_order = ["Inpatients", "Day cases", "Outpatients", "SRH services"]
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


def create_table_vasectomies_reversal_year(df):
    filter_type = None
    filter_condition = None
    rows = ["ProcType"]
    columns = "ReportingYear"
    sort_on = None
    row_order = ["Vasectomy_reversals"]
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


def create_table_prescriptions_year(df):
    filter_type = None
    filter_condition = None
    rows = ["Group"]
    columns = "Year"
    sort_on = None
    row_order = ["Grand_total", "Emergency"]
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
    sum_column = "Number Items"

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns, disclosure_control,
                                  count_column, sum_column)


def create_table_contraception_gender_age(df):
    filter_type = "persons_contraception"
    filter_condition = None
    rows = ["Gender"]
    columns = "Age_group_alt"
    sort_on = None
    row_order = ["2", "1"]
    column_order = ["Grand_total", "<13", "13-14", "15", "<16", "16-17",
                    "18-19", "20-24", "25-34", "35-44", "45-54", "55+"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"<16": ["<13", "13-14", "15"]}
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_contraception_gender_age_percent(df):
    filter_type = "persons_contraception"
    filter_condition = "(Age_group_alt != 'unrecorded')"
    rows = ["Gender"]
    columns = "Age_group_alt"
    sort_on = None
    row_order = ["2", "1"]
    column_order = ["Grand_total", "<13", "13-14", "15", "<16", "16-17",
                    "18-19", "20-24", "25-34", "35-44", "45-54", "55+"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"<16": ["<13", "13-14", "15"]}
    include_row_total = False
    multiplier = None
    output_type = "percents"
    percent_across_columns = True
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_contraception_gender_rate(df):
    filter_type = "persons_contraception"
    filter_condition = None
    rows = ["Gender"]
    columns = None
    sort_on = None
    row_order = ["2", "1"]
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 100
    output_type = "rates"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_contraception_gender_age_rate(df):
    filter_type = "persons_contraception"
    filter_condition = None
    rows = ["Gender"]
    columns = "Age_group_alt"
    sort_on = None
    row_order = ["2", "1"]
    column_order = ["13-14", "15", "13-15", "16-17", "18-19", "20-24", "25-34",
                    "35-44", "45-54"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"13-15": ["13-14", "15"]}
    include_row_total = False
    multiplier = 100
    output_type = "rates"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_contraception_female_age_year(df):
    filter_type = "persons_contraception"
    filter_condition = "(Gender == '2')"
    rows = ["ReportingYear"]
    columns = "Age_group_alt"
    sort_on = None
    row_order = None
    column_order = ["Grand_total", "13-14", "15", "13-15", "16-17", "18-19",
                    "20-24", "25-34", "35-44", "45-54"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"13-15": ["13-14", "15"]}
    include_row_total = False
    multiplier = 100
    output_type = "rates"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_contraception_male_age_year(df):
    filter_type = "persons_contraception"
    filter_condition = "(Gender == '1')"
    rows = ["ReportingYear"]
    columns = "Age_group_alt"
    sort_on = None
    row_order = None
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 100
    output_type = "rates"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_method_year(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["ContraceptiveMainMethod"]
    columns = "ReportingYear"
    sort_on = None
    row_order = ["Grand_total", "LARC", 3, 4, 2, 1, "User", "Oral", 12, 6, 11,
                 "Other"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = {"ContraceptiveMainMethod": {"LARC": [1, 2, 3, 4],
                                                "User": [5, 6, 7, 8, 9, 10, 11,
                                                         12, 13],
                                                "Oral": [7, 8],
                                                "Other": [5, 9, 10, 13]}}
    column_subgroup = None
    include_row_total = True
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_method_year_percent(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["ContraceptiveMainMethod"]
    columns = "ReportingYear"
    sort_on = None
    row_order = ["Grand_total", "LARC", 3, 4, 2, 1, "User", "Oral", 12, 6, 11,
                 "Other"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = {"ContraceptiveMainMethod": {"LARC": [1, 2, 3, 4],
                                                "User": [5, 6, 7, 8, 9, 10, 11,
                                                         12, 13],
                                                "Oral": [7, 8],
                                                "Other": [5, 9, 10, 13]}}
    column_subgroup = None
    include_row_total = True
    multiplier = None
    output_type = "percents"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_location(df):
    filter_type = None
    filter_condition = None
    rows = ["ReportingYear"]
    columns = "LocationType"
    sort_on = None
    row_order = None
    column_order = ["Grand_total", "B01", "L99", "A01", "Other"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"Other": ["M01", "N01", "X01"]}
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_location_percent(df):
    filter_type = None
    filter_condition = None
    rows = ["ReportingYear"]
    columns = "LocationType"
    sort_on = None
    row_order = None
    column_order = ["B01", "L99", "A01", "Other"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"Other": ["M01", "N01", "X01"]}
    include_row_total = False
    multiplier = None
    output_type = "percents"
    percent_across_columns = True
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_method_age(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["ContraceptiveMainMethod"]
    columns = "Age_group"
    sort_on = None
    row_order = ["Grand_total", "LARC", 3, 4, 2, 1, "User", "Oral", 12, 6, 11,
                 "Other"]
    column_order = ["Grand_total", "<16", "16-17", "18-19", "20-24", "25-34",
                    "35-44", "45+"]
    column_rename = None
    row_subgroup = {"ContraceptiveMainMethod": {"LARC": [1, 2, 3, 4],
                                                "User": [5, 6, 7, 8, 9, 10, 11,
                                                         12, 13],
                                                "Oral": [7, 8],
                                                "Other": [5, 9, 10, 13]}}
    column_subgroup = None
    include_row_total = True
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_method_age_percent(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["ContraceptiveMainMethod"]
    columns = "Age_group"
    sort_on = None
    row_order = ["Grand_total", "LARC", 3, 4, 2, 1, "User", "Oral", 12, 6, 11,
                 "Other"]
    column_order = ["Grand_total", "<16", "16-17", "18-19", "20-24", "25-34",
                    "35-44", "45+"]
    column_rename = None
    row_subgroup = {"ContraceptiveMainMethod": {"LARC": [1, 2, 3, 4],
                                                "User": [5, 6, 7, 8, 9, 10, 11,
                                                         12, 13],
                                                "Oral": [7, 8],
                                                "Other": [5, 9, 10, 13]}}
    column_subgroup = None
    include_row_total = True
    multiplier = None
    output_type = "percents"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_consultation_medium_year(df):
    filter_type = None
    filter_condition = None
    rows = ["ReportingYear"]
    columns = "ConsultationMedium"
    sort_on = None
    row_order = None
    column_order = ["Grand_total", "1", "Other"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"Other": ["2", "3", "4", "5", "6", "98"]}
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_consultation_medium_year_percent(df):
    filter_type = None
    filter_condition = None
    rows = ["ReportingYear"]
    columns = "ConsultationMedium"
    sort_on = None
    row_order = None
    column_order = ["1", "Other"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"Other": ["2", "3", "4", "5", "6", "98"]}
    include_row_total = False
    multiplier = None
    output_type = "percents"
    percent_across_columns = True
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_age_reason_total(df):
    filter_type = None
    filter_condition = None
    breakdown = ["Age_group"]
    sort_on = None
    breakdown_order = ["Grand_total"]
    measure_type = "Contacts"
    measure_order = None
    breakdown_subgroup = None
    include_breakdown_total = True
    multiplier = 0.001
    output_type = "counts"
    measures_as_rows = False
    disclosure_control = False

    return create_output_multi_field(df, filter_type, filter_condition,
                                     breakdown, sort_on, breakdown_order,
                                     measure_type, measure_order,
                                     breakdown_subgroup,
                                     include_breakdown_total, multiplier,
                                     output_type, measures_as_rows,
                                     disclosure_control)


def create_table_age_reason_female(df):
    filter_type = None
    filter_condition = "(Gender == '2')"
    breakdown = ["Age_group"]
    sort_on = None
    breakdown_order = ["Grand_total", "<16", "16-17", "18-19", "20-24",
                       "25-34", "35-44", "45+"]
    measure_type = "Contacts"
    measure_order = None
    breakdown_subgroup = None
    include_breakdown_total = True
    multiplier = 0.001
    output_type = "counts"
    measures_as_rows = False
    disclosure_control = False

    return create_output_multi_field(df, filter_type, filter_condition,
                                     breakdown, sort_on, breakdown_order,
                                     measure_type, measure_order,
                                     breakdown_subgroup,
                                     include_breakdown_total, multiplier,
                                     output_type, measures_as_rows,
                                     disclosure_control)


def create_table_reason_male(df):
    filter_type = None
    filter_condition = "(Gender == '1')"
    breakdown = ["Age_group"]
    sort_on = None
    breakdown_order = ["Grand_total"]
    measure_type = "Contacts"
    measure_order = None
    breakdown_subgroup = None
    include_breakdown_total = True
    multiplier = 0.001
    output_type = "counts"
    measures_as_rows = False
    disclosure_control = False

    return create_output_multi_field(df, filter_type, filter_condition,
                                     breakdown, sort_on, breakdown_order,
                                     measure_type, measure_order,
                                     breakdown_subgroup,
                                     include_breakdown_total, multiplier,
                                     output_type, measures_as_rows,
                                     disclosure_control)


def create_table_age_reason_total_percent(df):
    filter_type = None
    filter_condition = None
    breakdown = ["Age_group"]
    sort_on = None
    breakdown_order = ["Grand_total"]
    measure_type = "Contacts"
    measure_order = None
    breakdown_subgroup = None
    include_breakdown_total = True
    multiplier = None
    output_type = "percents"
    measures_as_rows = False
    disclosure_control = False

    return create_output_multi_field(df, filter_type, filter_condition,
                                     breakdown, sort_on, breakdown_order,
                                     measure_type, measure_order,
                                     breakdown_subgroup,
                                     include_breakdown_total, multiplier,
                                     output_type, measures_as_rows,
                                     disclosure_control)


def create_table_age_reason_female_percent(df):
    filter_type = None
    filter_condition = "(Gender == '2')"
    breakdown = ["Age_group"]
    sort_on = None
    breakdown_order = ["Grand_total", "<16", "16-17", "18-19", "20-24",
                       "25-34", "35-44", "45+"]
    measure_type = "Contacts"
    measure_order = None
    breakdown_subgroup = None
    include_breakdown_total = True
    multiplier = None
    output_type = "percents"
    measures_as_rows = False
    disclosure_control = False

    return create_output_multi_field(df, filter_type, filter_condition,
                                     breakdown, sort_on, breakdown_order,
                                     measure_type, measure_order,
                                     breakdown_subgroup,
                                     include_breakdown_total, multiplier,
                                     output_type, measures_as_rows,
                                     disclosure_control)


def create_table_reason_male_percent(df):
    filter_type = None
    filter_condition = "(Gender == '1')"
    breakdown = ["Age_group"]
    sort_on = None
    breakdown_order = ["Grand_total"]
    measure_type = "Contacts"
    measure_order = None
    breakdown_subgroup = None
    include_breakdown_total = True
    multiplier = None
    output_type = "percents"
    measures_as_rows = False
    disclosure_control = False

    return create_output_multi_field(df, filter_type, filter_condition,
                                     breakdown, sort_on, breakdown_order,
                                     measure_type, measure_order,
                                     breakdown_subgroup,
                                     include_breakdown_total, multiplier,
                                     output_type, measures_as_rows,
                                     disclosure_control)


def create_table_ec_year(df):
    filter_type = None
    filter_condition = None
    breakdown = ["ReportingYear"]
    sort_on = None
    breakdown_order = None
    measure_type = "EC"
    measure_order = None
    breakdown_subgroup = None
    include_breakdown_total = False
    multiplier = 0.001
    output_type = "counts"
    measures_as_rows = False
    disclosure_control = False

    return create_output_multi_field(df, filter_type, filter_condition,
                                     breakdown, sort_on, breakdown_order,
                                     measure_type, measure_order,
                                     breakdown_subgroup,
                                     include_breakdown_total, multiplier,
                                     output_type, measures_as_rows,
                                     disclosure_control)


def create_table_ec_under16_year(df):
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
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control,
                                  count_column, sum_column)


def create_table_ec_under16_year_percent(df):
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
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control,
                                  count_column, sum_column)


def create_table_ec_age(df):
    filter_type = None
    filter_condition = None
    breakdown = ["Age_group_alt"]
    sort_on = None
    breakdown_order = ["Grand_total", "<16", "<15", "15", "16-17", "18-19",
                       "20-24", "25-34", "35-44", "45+"]
    measure_type = "EC"
    measure_order = None
    breakdown_subgroup = {"Age_group_alt": {"<16": ["<13", "13-14", "15"],
                                            "<15": ["<13", "13-14"],
                                            "45+": ["45-54", "55+"]}}
    include_breakdown_total = True
    multiplier = 0.001
    output_type = "counts"
    measures_as_rows = False
    disclosure_control = False

    return create_output_multi_field(df, filter_type, filter_condition,
                                     breakdown, sort_on, breakdown_order,
                                     measure_type, measure_order,
                                     breakdown_subgroup,
                                     include_breakdown_total, multiplier,
                                     output_type, measures_as_rows,
                                     disclosure_control)


def create_table_ec_age_percent(df):
    filter_type = None
    filter_condition = None
    breakdown = ["Age_group_alt"]
    sort_on = None
    breakdown_order = ["Grand_total", "<16", "<15", "15", "16-17", "18-19",
                       "20-24", "25-34", "35-44", "45+"]
    measure_type = "EC"
    measure_order = ["ECIUDFlag"]
    breakdown_subgroup = {"Age_group_alt": {"<16": ["<13", "13-14", "15"],
                                            "<15": ["<13", "13-14"],
                                            "45+": ["45-54", "55+"]}}
    include_breakdown_total = True
    multiplier = None
    output_type = "percents"
    measures_as_rows = False
    disclosure_control = False

    return create_output_multi_field(df, filter_type, filter_condition,
                                     breakdown, sort_on, breakdown_order,
                                     measure_type, measure_order,
                                     breakdown_subgroup,
                                     include_breakdown_total, multiplier,
                                     output_type, measures_as_rows,
                                     disclosure_control)


def create_table_contact_age(df):
    filter_type = None
    filter_condition = None
    rows = ["ReportingYear"]
    columns = "Age_group"
    sort_on = None
    row_order = None
    column_order = ["Grand_total", "<16", "16-17", "18-19", "20-24",
                    "25-34", "35-44", "45+"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_activity_age(df):
    filter_type = None
    filter_condition = None
    breakdown = ["Age_group"]
    sort_on = None
    breakdown_order = ["Grand_total", "<16", "16-17", "18-19", "20-24",
                       "25-34", "35-44", "45+"]
    measure_type = "Activity"
    measure_order = None
    breakdown_subgroup = None
    include_breakdown_total = True
    multiplier = 0.001
    output_type = "counts"
    measures_as_rows = True
    disclosure_control = False

    return create_output_multi_field(df, filter_type, filter_condition,
                                     breakdown, sort_on, breakdown_order,
                                     measure_type, measure_order,
                                     breakdown_subgroup,
                                     include_breakdown_total, multiplier,
                                     output_type, measures_as_rows,
                                     disclosure_control)


def create_table_activity_age_percent(df):
    filter_type = None
    filter_condition = None
    breakdown = ["Age_group"]
    sort_on = None
    breakdown_order = ["Grand_total", "<16", "16-17", "18-19", "20-24",
                       "25-34", "35-44", "45+"]
    measure_type = "Activity"
    measure_order = None
    breakdown_subgroup = None
    include_breakdown_total = True
    multiplier = None
    output_type = "percents"
    measures_as_rows = True
    disclosure_control = False

    return create_output_multi_field(df, filter_type, filter_condition,
                                     breakdown, sort_on, breakdown_order,
                                     measure_type, measure_order,
                                     breakdown_subgroup,
                                     include_breakdown_total, multiplier,
                                     output_type, measures_as_rows,
                                     disclosure_control)


def create_table_status_method_female(df):
    filter_type = "contacts_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["ContraceptiveMainMethod"]
    columns = "ContraceptiveMethodStatus"
    sort_on = None
    row_order = ["Grand_total", "LARC", 3, 4, 2, 1, "User", "Oral", 12, 6, 11,
                 "Other"]
    column_order = ["Grand_total", 1, 2, 3]
    column_rename = None
    row_subgroup = {"ContraceptiveMainMethod": {"LARC": [1, 2, 3, 4],
                                                "User": [5, 6, 7, 8, 9, 10, 11,
                                                         12, 13],
                                                "Oral": [7, 8],
                                                "Other": [5, 9, 10, 13]}}
    column_subgroup = None
    include_row_total = True
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_status_method_female_percent(df):
    filter_type = "contacts_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["ContraceptiveMainMethod"]
    columns = "ContraceptiveMethodStatus"
    sort_on = None
    row_order = ["LARC", 3, 4, 2, 1, "User", "Oral", 12, 6, 11, "Other"]
    column_order = ["Grand_total", 1, 2, 3]
    column_rename = None
    row_subgroup = {"ContraceptiveMainMethod": {"LARC": [1, 2, 3, 4],
                                                "User": [5, 6, 7, 8, 9, 10, 11,
                                                         12, 13],
                                                "Oral": [7, 8],
                                                "Other": [5, 9, 10, 13]}}

    column_subgroup = None
    include_row_total = False
    multiplier = None
    output_type = "percents"
    percent_across_columns = True
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_status_method_male(df):
    filter_type = "contacts_main_method"
    filter_condition = "(Gender == '1')"
    rows = ["ContraceptiveMainMethod"]
    columns = "ContraceptiveMethodStatus"
    sort_on = None
    row_order = ["Grand_total", 12, "Other"]
    column_order = ["Grand_total", 1, 2, 3]
    column_rename = None
    row_subgroup = {"ContraceptiveMainMethod": {"Other": [10, 11]}}
    column_subgroup = None
    include_row_total = True
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_status_method_male_percent(df):
    filter_type = "contacts_main_method"
    filter_condition = "(Gender == '1')"
    rows = ["ContraceptiveMainMethod"]
    columns = "ContraceptiveMethodStatus"
    sort_on = None
    row_order = ["Grand_total", 12, "Other"]
    column_order = ["Grand_total", 1, 2, 3]
    column_rename = None
    row_subgroup = {"ContraceptiveMainMethod": {"Other": [10, 11]}}
    column_subgroup = None
    include_row_total = True
    multiplier = None
    output_type = "percents"
    percent_across_columns = True
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_ec_female_age(df):
    filter_type = "females_emergency_contraception"
    filter_condition = None
    rows = ["Age_group_alt"]
    columns = None
    sort_on = None
    row_order = ["Grand_total", "13-15", "13-14", "15", "16-17", "18-19",
                 "20-24", "25-34", "35-44", "45-54"]
    column_order = None
    column_rename = None
    row_subgroup = {"Age_group_alt": {"13-15": ["13-14", "15"]}}
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_ec_female_age_population(df):
    filter_type = "females_emergency_contraception"
    filter_condition = "(Gender == '2')"
    rows = ["Age_group_alt"]
    columns = None
    sort_on = None
    row_order = ["Grand_total", "13-15", "13-14", "15", "16-17", "18-19",
                 "20-24", "25-34", "35-44", "45-54"]
    column_order = None
    column_rename = None
    row_subgroup = {"Age_group_alt": {"13-15": ["13-14", "15"]}}
    column_subgroup = None
    include_row_total = False
    multiplier = 1000
    output_type = "rates"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_male_year(df):
    filter_type = "persons_first_contact"
    filter_condition = "(Gender == '1')"
    rows = ["ReportingYear"]
    columns = "Gender"
    sort_on = None
    row_order = None
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    count_multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  count_multiplier, output_type,
                                  percent_across_columns,
                                  disclosure_control)


def create_table_male_condoms_year(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '1')"
    rows = ["ReportingYear"]
    columns = "ContraceptiveMainMethod"
    sort_on = None
    row_order = None
    column_order = [12]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    count_multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  count_multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_method_imd_percent(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["IMD_decile"]
    columns = "ContraceptiveMainMethod"
    sort_on = None
    row_order = None
    column_order = ["LARC", "User"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"LARC": [1, 2, 3, 4],
                       "User": [5, 6, 7, 8, 9, 10, 11, 12, 13]}
    include_row_total = False
    multiplier = None
    output_type = "percents"
    percent_across_columns = True
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_ec_13_15_imd(df):
    filter_type = "females_emergency_contraception"
    filter_condition = "(Age_group_alt in['13-14', '15']) & (Gender == '2')"
    rows = ["IMD_decile"]
    columns = "Age_group_alt"
    sort_on = None
    row_order = None
    column_order = ["13-15"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"13-15": ["13-14", "15"]}
    include_row_total = False
    multiplier = 1000
    output_type = "rates"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_13_54_imd(df):
    filter_type = "persons_first_contact"
    filter_condition = "(Gender == '2')"
    rows = ["IMD_decile"]
    columns = "Age_group_alt"
    sort_on = None
    row_order = None
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 100
    output_type = "rates"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_prescriptions_type_year(df):
    filter_type = None
    filter_condition = None
    rows = ["Subgroup"]
    columns = "Year"
    sort_on = None
    row_order = ["Grand_total", "LARC", "01_iud", "02_ius", "04_implant",
                 "03_injectable", "User_dependent", "Oral_total", "05_combined",
                 "06_progestrogen", "07_patch", "08_cap", "09_vaginal ring",
                 "10_spermicides", "11_emergency"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = {"Subgroup": {"LARC": ["01_iud", "02_ius", "03_injectable",
                                          "04_implant"],
                                 "User_dependent": ["05_combined",
                                                    "06_progestrogen",
                                                    "07_patch",
                                                    "08_cap",
                                                    "09_vaginal ring",
                                                    "10_spermicides"],
                                 "Oral_total": ["05_combined",
                                                "06_progestrogen"]
                                 }}
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


def create_table_sterilisation_age(df):
    filter_type = None
    filter_condition = "(ProcType == 'Sterilisations')"
    rows = ["Age_group"]
    columns = "ProcType"
    sort_on = None
    row_order = ["Grand_total", "<20", "20-24", "25-29",
                 "30-34", "35-39", "40-44", "45+"]
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


def create_table_sterilisation_age_percent(df):
    filter_type = None
    filter_condition = "(ProcType == 'Sterilisations') & (Age_group != 'unrecorded')"
    rows = ["Age_group"]
    columns = "ProcType"
    sort_on = None
    row_order = ["<20", "20-24", "25-29",
                 "30-34", "35-39", "40-44", "45+"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = None
    output_type = "percents"
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


def create_table_vasectomies_age(df):
    filter_type = None
    filter_condition = "(ProcType == 'Vasectomies')"
    rows = ["Age_group"]
    columns = "ProcType"
    sort_on = None
    row_order = ["Grand_total", "<20", "20-24", "25-29",
                 "30-34", "35-39", "40-44", "45+"]
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


def create_table_vasectomies_age_percent(df):
    filter_type = None
    filter_condition = "(ProcType == 'Vasectomies') & (Age_group != 'unrecorded')"
    rows = ["Age_group"]
    columns = "ProcType"
    sort_on = None
    row_order = ["<20", "20-24", "25-29",
                 "30-34", "35-39", "40-44", "45+"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = None
    output_type = "percents"
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


def create_table_females_age_region_national(df):
    filter_type = "persons_contraception"
    filter_condition = "(Gender == '2')"
    rows = ["Age_group_alt"]
    columns = None
    sort_on = None
    row_order = ["Grand_total", "13-15", "16-17", "18-19", "20-24", "25-34",
                 "35-44", "45-54"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = {"Age_group_alt": {"13-15": ["13-14", "15"]}}
    column_subgroup = None
    include_row_total = False
    multiplier = 100
    output_type = "rates"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_age_region(df):
    filter_type = "persons_contraception"
    filter_condition = "(Gender == '2') & (LA_parent_code != 'X99999999')"
    rows = ["Age_group_alt"]
    columns = "LA_parent_code"
    sort_on = None
    row_order = ["Grand_total", "13-15", "16-17", "18-19", "20-24", "25-34",
                 "35-44", "45-54"]
    column_order = ["E12000001", "E12000002", "E12000003",	"E12000004",
                    "E12000005", "E12000006", "E12000007",	"E12000008",
                    "E12000009"]
    column_rename = None
    row_subgroup = {"Age_group_alt": {"13-15": ["13-14", "15"]}}
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


def create_table_females_method_region_national(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["Age_group_alt"]
    columns = "LA_parent_code"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = True
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_method_region(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["Age_group_alt"]
    columns = "LA_parent_code"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["E12000001", "E12000002", "E12000003", "E12000004",
                    "E12000005", "E12000006", "E12000007", "E12000008",
                    "E12000009"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = True
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_method_region_percent(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["ContraceptiveMainMethod"]
    columns = "LA_parent_code"
    sort_on = None
    row_order = ["LARC", 3, 4, 2, 1, "User", "Oral", 12, 6, 11,
                 "Other"]
    column_order = ["Grand_total", "E12000001", "E12000002", "E12000003",
                    "E12000004", "E12000005", "E12000006", "E12000007",
                    "E12000008", "E12000009"]
    column_rename = None
    row_subgroup = {"ContraceptiveMainMethod": {"LARC": [1, 2, 3, 4],
                                                "User": [5, 6, 7, 8, 9, 10, 11,
                                                         12, 13],
                                                "Oral": [7, 8],
                                                "Other": [5, 9, 10, 13]}}
    column_subgroup = None
    include_row_total = True
    multiplier = None
    output_type = "percents"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_age_national(df):
    filter_type = "persons_first_contact"
    filter_condition = "(Gender == '2')"
    rows = ["LA_parent_code"]
    columns = "Age_group"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["Grand_total", "<16", "16-17", "18-19", "20-24", "25-34",
                    "35-44", "45+"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_age_national_rate(df):
    filter_type = "persons_first_contact"
    filter_condition = "(Gender == '2')"
    rows = ["LA_parent_code"]
    columns = "Age_group_alt"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["Grand_total", "13-15", "16-17", "18-19", "20-24", "25-34",
                    "35-44", "45-54"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"13-15": ["13-14", "15"]}
    include_row_total = False
    multiplier = 100
    output_type = "rates"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_age_la_parent(df):
    filter_type = "persons_first_contact"
    filter_condition = "(Gender == '2') & (LA_parent_code.str.startswith('E12'))"
    rows = ["LA_parent_code", "LA_parent_name"]
    columns = "Age_group"
    sort_on = ["LA_parent_code"]
    row_order = None
    column_order = ["Grand_total", "<16", "16-17", "18-19", "20-24", "25-34",
                    "35-44", "45+"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_age_la_parent_rate(df):
    filter_type = "persons_first_contact"
    filter_condition = "(Gender == '2') & (LA_parent_code.str.startswith('E12'))"
    rows = ["LA_parent_code", "LA_parent_name"]
    columns = "Age_group_alt"
    sort_on = ["LA_parent_code"]
    row_order = None
    column_order = ["Grand_total", "13-15", "16-17", "18-19", "20-24", "25-34",
                    "35-44", "45-54"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"13-15": ["13-14", "15"]}
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


def create_table_females_age_la(df):
    filter_type = "persons_first_contact"
    filter_condition = "(Gender == '2')"
    rows = ["LA_code", "LA_name", "LA_parent_name"]
    columns = "Age_group"
    sort_on = ["LA_parent_code", "LA_name"]
    row_order = None
    column_order = ["Grand_total", "<16", "16-17", "18-19", "20-24", "25-34",
                    "35-44", "45+"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_age_la_rate(df):
    filter_type = "persons_first_contact"
    filter_condition = "(Gender == '2')"
    rows = ["LA_code", "LA_name", "LA_parent_name"]
    columns = "Age_group_alt"
    sort_on = ["LA_parent_code", "LA_name"]
    row_order = None
    column_order = ["Grand_total", "13-15", "16-17", "18-19", "20-24", "25-34",
                    "35-44", "45-54"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"13-15": ["13-14", "15"]}
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


def create_table_males_age_national(df):
    filter_type = "persons_first_contact"
    filter_condition = "(Gender == '1')"
    rows = ["LA_parent_code"]
    columns = "Age_group"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_males_age_national_rate(df):
    filter_type = "persons_first_contact"
    filter_condition = "(Gender == '1')"
    rows = ["LA_parent_code"]
    columns = "Age_group_alt"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"13-15": ["13-14", "15"]}
    include_row_total = False
    multiplier = 100
    output_type = "rates"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_males_age_la_parent(df):
    filter_type = "persons_first_contact"
    filter_condition = "(Gender == '1') & (LA_parent_code.str.startswith('E12'))"
    rows = ["LA_parent_code", "LA_parent_name"]
    columns = "Age_group"
    sort_on = ["LA_parent_code"]
    row_order = None
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_males_age_la_parent_rate(df):
    filter_type = "persons_first_contact"
    filter_condition = "(Gender == '1') & (LA_parent_code.str.startswith('E12'))"
    rows = ["LA_parent_code", "LA_parent_name"]
    columns = "Age_group_alt"
    sort_on = ["LA_parent_code"]
    row_order = None
    column_order = ["Grand_total"]
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


def create_table_males_age_la(df):
    filter_type = "persons_first_contact"
    filter_condition = "(Gender == '1')"
    rows = ["LA_code", "LA_name", "LA_parent_name"]
    columns = "Age_group"
    sort_on = ["LA_parent_code", "LA_name"]
    row_order = None
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_males_age_la_rate(df):
    filter_type = "persons_first_contact"
    filter_condition = "(Gender == '1')"
    rows = ["LA_code", "LA_name", "LA_parent_name"]
    columns = "Age_group_alt"
    sort_on = ["LA_parent_code", "LA_name"]
    row_order = None
    column_order = ["Grand_total"]
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


def create_table_females_contraception_age_national(df):
    filter_type = "persons_contraception"
    filter_condition = "(Gender == '2')"
    rows = ["LA_parent_code"]
    columns = "Age_group"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["Grand_total", "<16", "16-17", "18-19", "20-24", "25-34",
                    "35-44", "45+"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_contraception_age_national_rate(df):
    filter_type = "persons_contraception"
    filter_condition = "(Gender == '2')"
    rows = ["LA_parent_code"]
    columns = "Age_group_alt"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["Grand_total", "13-15", "16-17", "18-19", "20-24", "25-34",
                    "35-44", "45-54"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"13-15": ["13-14", "15"]}
    include_row_total = False
    multiplier = 100
    output_type = "rates"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_contraception_age_la_parent(df):
    filter_type = "persons_contraception"
    filter_condition = "(Gender == '2') & (LA_parent_code.str.startswith('E12'))"
    rows = ["LA_parent_code", "LA_parent_name"]
    columns = "Age_group"
    sort_on = ["LA_parent_code"]
    row_order = None
    column_order = ["Grand_total", "<16", "16-17", "18-19", "20-24", "25-34",
                    "35-44", "45+"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_contraception_age_la_parent_rate(df):
    filter_type = "persons_contraception"
    filter_condition = "(Gender == '2') & (LA_parent_code.str.startswith('E12'))"
    rows = ["LA_parent_code", "LA_parent_name"]
    columns = "Age_group_alt"
    sort_on = ["LA_parent_code"]
    row_order = None
    column_order = ["Grand_total", "13-15", "16-17", "18-19", "20-24", "25-34",
                    "35-44", "45-54"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"13-15": ["13-14", "15"]}
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


def create_table_females_contraception_age_la(df):
    filter_type = "persons_contraception"
    filter_condition = "(Gender == '2')"
    rows = ["LA_code", "LA_name", "LA_parent_name"]
    columns = "Age_group"
    sort_on = ["LA_parent_code", "LA_name"]
    row_order = None
    column_order = ["Grand_total", "<16", "16-17", "18-19", "20-24", "25-34",
                    "35-44", "45+"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_contraception_age_la_rate(df):
    filter_type = "persons_contraception"
    filter_condition = "(Gender == '2')"
    rows = ["LA_code", "LA_name", "LA_parent_name"]
    columns = "Age_group_alt"
    sort_on = ["LA_parent_code", "LA_name"]
    row_order = None
    column_order = ["Grand_total", "13-15", "16-17", "18-19", "20-24", "25-34",
                    "35-44", "45-54"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"13-15": ["13-14", "15"]}
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


def create_table_males_contraception_age_national(df):
    filter_type = "persons_contraception"
    filter_condition = "(Gender == '1')"
    rows = ["LA_parent_code"]
    columns = "Age_group"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_males_contraception_age_national_rate(df):
    filter_type = "persons_contraception"
    filter_condition = "(Gender == '1')"
    rows = ["LA_parent_code"]
    columns = "Age_group_alt"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"13-15": ["13-14", "15"]}
    include_row_total = False
    multiplier = 100
    output_type = "rates"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_males_contraception_age_la_parent(df):
    filter_type = "persons_contraception"
    filter_condition = "(Gender == '1') & (LA_parent_code.str.startswith('E12'))"
    rows = ["LA_parent_code", "LA_parent_name"]
    columns = "Age_group"
    sort_on = ["LA_parent_code"]
    row_order = None
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_males_contraception_age_la_parent_rate(df):
    filter_type = "persons_contraception"
    filter_condition = "(Gender == '1') & (LA_parent_code.str.startswith('E12'))"
    rows = ["LA_parent_code", "LA_parent_name"]
    columns = "Age_group_alt"
    sort_on = ["LA_parent_code"]
    row_order = None
    column_order = ["Grand_total"]
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


def create_table_males_contraception_age_la(df):
    filter_type = "persons_contraception"
    filter_condition = "(Gender == '1')"
    rows = ["LA_code", "LA_name", "LA_parent_name"]
    columns = "Age_group"
    sort_on = ["LA_parent_code", "LA_name"]
    row_order = None
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_males_contraception_age_la_rate(df):
    filter_type = "persons_contraception"
    filter_condition = "(Gender == '1')"
    rows = ["LA_code", "LA_name", "LA_parent_name"]
    columns = "Age_group_alt"
    sort_on = ["LA_parent_code", "LA_name"]
    row_order = None
    column_order = ["Grand_total"]
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


def create_table_females_age_provider(df):
    filter_type = "persons_first_contact"
    filter_condition = "(Gender == '2')"
    rows = ["Org_code", "Org_name"]
    columns = "Age_group"
    sort_on = ["Org_name"]
    row_order = None
    column_order = ["Grand_total", "<16", "16-17", "18-19", "20-24", "25-34",
                    "35-44", "45+"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_males_age_provider(df):
    filter_type = "persons_first_contact"
    filter_condition = "(Gender == '1')"
    rows = ["Org_code", "Org_name"]
    columns = "Age_group"
    sort_on = ["Org_name"]
    row_order = None
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_contraception_age_provider(df):
    filter_type = "persons_contraception"
    filter_condition = "(Gender == '2')"
    rows = ["Org_code", "Org_name"]
    columns = "Age_group"
    sort_on = ["Org_name"]
    row_order = None
    column_order = ["Grand_total", "<16", "16-17", "18-19", "20-24", "25-34",
                    "35-44", "45+"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_males_contraception_age_provider(df):
    filter_type = "persons_contraception"
    filter_condition = "(Gender == '1')"
    rows = ["Org_code", "Org_name"]
    columns = "Age_group"
    sort_on = ["Org_name"]
    row_order = None
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_location_national(df):
    filter_type = None
    filter_condition = None
    rows = ["LA_name"]
    columns = "LocationType"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["Grand_total", "B01", "L99", "A01", "Other"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"Other": ["M01", "N01", "X01"]}
    include_row_total = True
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_consultation_medium_national(df):
    filter_type = None
    filter_condition = None
    rows = ["LA_name"]
    columns = "ConsultationMedium"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["1", "Non_face"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"Non_face": ["2", "3", "4", "5", "6", "98"]}
    include_row_total = True
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_contacts_contraception_national(df):
    filter_type = "contacts_contraception"
    filter_condition = None
    rows = ["LA_name"]
    columns = None
    sort_on = None
    row_order = ["Grand_total"]
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = True
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_location_la_parent(df):
    filter_type = None
    filter_condition = "(LA_parent_code.str.startswith('E12'))"
    rows = ["LA_parent_code"]
    columns = "LocationType"
    sort_on = ["LA_parent_code"]
    row_order = None
    column_order = ["Grand_total", "B01", "L99", "A01", "Other"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"Other": ["M01", "N01", "X01"]}
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_consultation_medium_la_parent(df):
    filter_type = None
    filter_condition = "(LA_parent_code.str.startswith('E12'))"
    rows = ["LA_parent_code"]
    columns = "ConsultationMedium"
    sort_on = ["LA_parent_code"]
    row_order = None
    column_order = ["1", "Non_face"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"Non_face": ["2", "3", "4", "5", "6", "98"]}
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_contacts_contraception_la_parent(df):
    filter_type = "contacts_contraception"
    filter_condition = "(LA_parent_code.str.startswith('E12'))"
    rows = ["LA_parent_code"]
    columns = None
    sort_on = ["LA_parent_code"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_location_la(df):
    filter_type = None
    filter_condition = None
    rows = ["LA_code", "LA_name", "LA_parent_name"]
    columns = "LocationType"
    sort_on = ["LA_parent_code", "LA_name"]
    row_order = None
    column_order = ["Grand_total", "B01", "L99", "A01", "Other"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"Other": ["M01", "N01", "X01"]}
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_consultation_medium_la(df):
    filter_type = None
    filter_condition = None
    rows = ["LA_code", "LA_name", "LA_parent_name"]
    columns = "ConsultationMedium"
    sort_on = ["LA_parent_code", "LA_name"]
    row_order = None
    column_order = ["1", "Non_face"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"Non_face": ["2", "3", "4", "5", "6", "98"]}
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_contacts_contraception_la(df):
    filter_type = "contacts_contraception"
    filter_condition = None
    rows = ["LA_code", "LA_name", "LA_parent_name"]
    columns = None
    sort_on = ["LA_parent_code", "LA_name"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_location_provider(df):
    filter_type = None
    filter_condition = None
    rows = ["Org_code", "Org_name"]
    columns = "LocationType"
    sort_on = ["Org_name"]
    row_order = None
    column_order = ["Grand_total", "B01", "L99", "A01", "Other"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"Other": ["M01", "N01", "X01"]}
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_consultation_medium_provider(df):
    filter_type = None
    filter_condition = None
    rows = ["Org_code", "Org_name"]
    columns = "ConsultationMedium"
    sort_on = ["Org_name"]
    row_order = None
    column_order = ["1", "Non_face"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"Non_face": ["2", "3", "4", "5", "6", "98"]}
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_contacts_contraception_provider(df):
    filter_type = "contacts_contraception"
    filter_condition = None
    rows = ["Org_code", "Org_name"]
    columns = None
    sort_on = ["Org_name"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_method_national(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["LA_parent_code"]
    columns = "ContraceptiveMainMethod"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["Grand_total", "LARC", 3, 4, 2, 1, "User", "Oral", 12, 6,
                    "Other"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"LARC": [1, 2, 3, 4],
                       "User": [5, 6, 7, 8, 9, 10, 11, 12, 13],
                       "Oral": [7, 8],
                       "Other": [5, 9, 10, 11, 13]}
    include_row_total = True
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_method_la_parent(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2') & (LA_parent_code.str.startswith('E12'))"
    rows = ["LA_parent_code"]
    columns = "ContraceptiveMainMethod"
    sort_on = ["LA_parent_code"]
    row_order = None
    column_order = ["Grand_total", "LARC", 3, 4, 2, 1, "User", "Oral", 12, 6,
                    "Other"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"LARC": [1, 2, 3, 4],
                       "User": [5, 6, 7, 8, 9, 10, 11, 12, 13],
                       "Oral": [7, 8],
                       "Other": [5, 9, 10, 11, 13]}
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_method_la(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["LA_code", "LA_name", "LA_parent_name"]
    columns = "ContraceptiveMainMethod"
    sort_on = ["LA_parent_code", "LA_name"]
    row_order = None
    column_order = ["Grand_total", "LARC", 3, 4, 2, 1, "User", "Oral", 12, 6,
                    "Other"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"LARC": [1, 2, 3, 4],
                       "User": [5, 6, 7, 8, 9, 10, 11, 12, 13],
                       "Oral": [7, 8],
                       "Other": [5, 9, 10, 11, 13]}
    include_row_total = True
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_method_national_percent(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["LA_parent_code"]
    columns = "ContraceptiveMainMethod"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["LARC", 3, 4, 2, 1, "User", "Oral", 12, 6,
                    "Other"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"LARC": [1, 2, 3, 4],
                       "User": [5, 6, 7, 8, 9, 10, 11, 12, 13],
                       "Oral": [7, 8],
                       "Other": [5, 9, 10, 11, 13]}
    include_row_total = True
    multiplier = 0.001
    output_type = "percents"
    percent_across_columns = True
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_method_la_parent_percent(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2') & (LA_parent_code.str.startswith('E12'))"
    rows = ["LA_parent_code"]
    columns = "ContraceptiveMainMethod"
    sort_on = ["LA_parent_code"]
    row_order = None
    column_order = ["LARC", 3, 4, 2, 1, "User", "Oral", 12, 6,
                    "Other"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"LARC": [1, 2, 3, 4],
                       "User": [5, 6, 7, 8, 9, 10, 11, 12, 13],
                       "Oral": [7, 8],
                       "Other": [5, 9, 10, 11, 13]}
    include_row_total = False
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


def create_table_females_method_la_percent(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["LA_code", "LA_name", "LA_parent_name"]
    columns = "ContraceptiveMainMethod"
    sort_on = ["LA_parent_code", "LA_name"]
    row_order = None
    column_order = ["LARC", 3, 4, 2, 1, "User", "Oral", 12, 6,
                    "Other"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"LARC": [1, 2, 3, 4],
                       "User": [5, 6, 7, 8, 9, 10, 11, 12, 13],
                       "Oral": [7, 8],
                       "Other": [5, 9, 10, 11, 13]}
    include_row_total = True
    multiplier = 0.001
    output_type = "percents"
    percent_across_columns = True
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_method_provider(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["Org_code", "Org_name"]
    columns = "ContraceptiveMainMethod"
    sort_on = ["Org_name"]
    row_order = None
    column_order = ["Grand_total", "LARC", 3, 4, 2, 1, "User", "Oral", 12, 6,
                    "Other"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"LARC": [1, 2, 3, 4],
                       "User": [5, 6, 7, 8, 9, 10, 11, 12, 13],
                       "Oral": [7, 8],
                       "Other": [5, 9, 10, 11, 13]}
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_females_method_provider_percent(df):
    filter_type = "persons_main_method"
    filter_condition = "(Gender == '2')"
    rows = ["Org_code", "Org_name"]
    columns = "ContraceptiveMainMethod"
    sort_on = ["Org_name"]
    row_order = None
    column_order = ["LARC", 3, 4, 2, 1, "User", "Oral", 12, 6,
                    "Other"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"LARC": [1, 2, 3, 4],
                       "User": [5, 6, 7, 8, 9, 10, 11, 12, 13],
                       "Oral": [7, 8],
                       "Other": [5, 9, 10, 11, 13]}
    include_row_total = False
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


def create_table_ec_age_national(df):
    filter_type = None
    filter_condition = "(Number_EC_items != 0)"
    rows = ["LA_parent_code"]
    columns = "Age_group"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["Grand_total", "<16", "16+"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"16+": ["16-17", "18-19", "20-24", "25-34", "35-44", "45+"]}
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
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control,
                                  count_column, sum_column)


def create_table_ec_age_la_parent(df):
    filter_type = None
    filter_condition = "(Number_EC_items != 0) & (LA_parent_code.str.startswith('E12'))"
    rows = ["LA_parent_code"]
    columns = "Age_group"
    sort_on = ["LA_parent_code"]
    row_order = None
    column_order = ["Grand_total", "<16", "16+"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"16+": ["16-17", "18-19", "20-24", "25-34", "35-44", "45+"]}
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True
    count_column = None
    sum_column = "Number_EC_items"

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control,
                                  count_column, sum_column)


def create_table_ec_age_la(df):
    filter_type = None
    filter_condition = "(Number_EC_items != 0)"
    rows = ["LA_code", "LA_name", "LA_parent_name"]
    columns = "Age_group"
    sort_on = ["LA_parent_code", "LA_name"]
    row_order = None
    column_order = ["Grand_total", "<16", "16+"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"16+": ["16-17", "18-19", "20-24", "25-34", "35-44", "45+"]}
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True
    count_column = None
    sum_column = "Number_EC_items"

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control,
                                  count_column, sum_column)


def create_table_ec_age_national_rate(df):
    filter_type = "females_emergency_contraception"
    filter_condition = "(Gender == '2')"
    rows = ["LA_parent_code"]
    columns = "Age_group_alt"
    sort_on = None
    row_order = ["Grand_total"]
    column_order = ["Grand_total", "13-15", "16-54"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"13-15": ["13-14", "15"],
                       "16-54": ["16-17", "18-19", "20-24", "25-34", "35-44", "45-54"]}
    include_row_total = False
    multiplier = 1000
    output_type = "rates"
    percent_across_columns = False
    disclosure_control = False

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_ec_age_la_parent_rate(df):
    filter_type = "females_emergency_contraception"
    filter_condition = "(Gender == '2') & (LA_parent_code.str.startswith('E12'))"
    rows = ["LA_parent_code"]
    columns = "Age_group_alt"
    sort_on = ["LA_parent_code"]
    row_order = None
    column_order = ["Grand_total", "13-15", "16-54"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"13-15": ["13-14", "15"],
                       "16-54": ["16-17", "18-19", "20-24", "25-34", "35-44", "45-54"]}
    include_row_total = False
    multiplier = 1000
    output_type = "rates"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_ec_age_la_rate(df):
    filter_type = "females_emergency_contraception"
    filter_condition = "(Gender == '2')"
    rows = ["LA_code", "LA_name", "LA_parent_name"]
    columns = "Age_group_alt"
    sort_on = ["LA_parent_code", "LA_name"]
    row_order = None
    column_order = ["Grand_total", "13-15", "16-54"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"13-15": ["13-14", "15"],
                       "16-54": ["16-17", "18-19", "20-24", "25-34", "35-44", "45-54"]}
    include_row_total = False
    multiplier = 1000
    output_type = "rates"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_ec_age_provider(df):
    filter_type = None
    filter_condition = None
    rows = ["Org_code", "Org_name"]
    columns = "Age_group"
    sort_on = ["Org_name"]
    row_order = None
    column_order = ["Grand_total", "<16", "16+"]
    column_rename = None
    row_subgroup = None
    column_subgroup = {"16+": ["16-17", "18-19", "20-24", "25-34", "35-44", "45+"]}
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True
    count_column = None
    sum_column = "Number_EC_items"

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control,
                                  count_column, sum_column)


def create_table_all_activity_national(df):
    filter_type = None
    filter_condition = None
    breakdown = ["Org_code", "Org_name"]
    sort_on = None
    breakdown_order = ["Grand_total"]
    measure_type = "Activity"
    measure_order = None
    breakdown_subgroup = None
    include_breakdown_total = True
    multiplier = 0.001
    output_type = "counts"
    measures_as_rows = False
    disclosure_control = False

    return create_output_multi_field(df, filter_type, filter_condition,
                                     breakdown, sort_on, breakdown_order,
                                     measure_type, measure_order,
                                     breakdown_subgroup,
                                     include_breakdown_total, multiplier,
                                     output_type, measures_as_rows,
                                     disclosure_control)


def create_table_all_activity_la_parent(df):
    filter_type = None
    filter_condition = "(LA_parent_code.str.startswith('E12'))"
    breakdown = ["LA_parent_code"]
    sort_on = ["LA_parent_code"]
    breakdown_order = None
    measure_type = "Activity"
    measure_order = None
    breakdown_subgroup = None
    include_breakdown_total = False
    multiplier = 0.001
    output_type = "counts"
    measures_as_rows = False
    disclosure_control = True

    return create_output_multi_field(df, filter_type, filter_condition,
                                     breakdown, sort_on, breakdown_order,
                                     measure_type, measure_order,
                                     breakdown_subgroup,
                                     include_breakdown_total, multiplier,
                                     output_type, measures_as_rows,
                                     disclosure_control)


def create_table_all_activity_la(df):
    filter_type = None
    filter_condition = None
    breakdown = ["LA_code", "LA_name", "LA_parent_name"]
    sort_on = ["LA_parent_code", "LA_name"]
    breakdown_order = None
    measure_type = "Activity"
    measure_order = None
    breakdown_subgroup = None
    include_breakdown_total = False
    multiplier = 0.001
    output_type = "counts"
    measures_as_rows = False
    disclosure_control = True

    return create_output_multi_field(df, filter_type, filter_condition,
                                     breakdown, sort_on, breakdown_order,
                                     measure_type, measure_order,
                                     breakdown_subgroup,
                                     include_breakdown_total, multiplier,
                                     output_type, measures_as_rows,
                                     disclosure_control)


def create_table_all_activity_provider(df):
    filter_type = None
    filter_condition = None
    breakdown = ["Org_code", "Org_name"]
    sort_on = ["Org_name"]
    breakdown_order = None
    measure_type = "Activity"
    measure_order = None
    breakdown_subgroup = None
    include_breakdown_total = False
    multiplier = 0.001
    output_type = "counts"
    measures_as_rows = False
    disclosure_control = True

    return create_output_multi_field(df, filter_type, filter_condition,
                                     breakdown, sort_on, breakdown_order,
                                     measure_type, measure_order,
                                     breakdown_subgroup,
                                     include_breakdown_total, multiplier,
                                     output_type, measures_as_rows,
                                     disclosure_control)


def create_table_laclinic_cross_boundary_upper(df):
    filter_type = None
    filter_condition = None
    rows = ["Clinic_LA_code_upper", "Clinic_LA_name_upper"]
    columns = "Cross_boundary_upper"
    sort_on = ["Clinic_LA_name_upper"]
    row_order = None
    column_order = ["Grand_total", "Inside", "Outside"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_laclinic_cross_boundary_upper_percent(df):
    filter_type = None
    filter_condition = "(Cross_boundary_upper != 'Unknown')"
    rows = ["Clinic_LA_code_upper", "Clinic_LA_name_upper"]
    columns = "Cross_boundary_upper"
    sort_on = ["Clinic_LA_name_upper"]
    row_order = None
    column_order = ["Inside", "Outside"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = None
    output_type = "percents"
    percent_across_columns = True
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_laclinic_lares_upper(df):
    filter_type = None
    filter_condition = None
    rows = ["Clinic_LA_code_upper", "Clinic_LA_name_upper"]
    columns = "LA_name_inc_small"
    sort_on = ["Clinic_LA_name_upper"]
    row_order = None
    column_order = None
    # Note that the total column is renamed here so that it can be easily
    # identified for removal in the output_specific_updates function
    column_rename = {"Grand_total": "All_LAs"}
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_laclinic_cross_boundary_lower(df):
    filter_type = None
    filter_condition = None
    rows = ["Clinic_LA_code_lower", "Clinic_LA_name_lower"]
    columns = "Cross_boundary_lower"
    sort_on = ["Clinic_LA_name_lower"]
    row_order = None
    column_order = ["Grand_total", "Inside", "Outside"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_laclinic_cross_boundary_lower_percent(df):
    filter_type = None
    filter_condition = "(Cross_boundary_lower != 'Unknown')"
    rows = ["Clinic_LA_code_lower", "Clinic_LA_name_lower"]
    columns = "Cross_boundary_lower"
    sort_on = ["Clinic_LA_name_lower"]
    row_order = None
    column_order = ["Inside", "Outside"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = None
    output_type = "percents"
    percent_across_columns = True
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_laclinic_lares_lower(df):
    filter_type = None
    filter_condition = None
    rows = ["Clinic_LA_code_lower", "Clinic_LA_name_lower"]
    columns = "LA_name_lower"
    sort_on = ["Clinic_LA_name_lower"]
    row_order = None
    column_order = None
    # Note that the total column is renamed here so that it can be easily
    # identified for removal in the output_specific_updates function
    column_rename = {"Grand_total": "All_LAs"}
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_laclinic_clinic_total(df):
    filter_type = None
    filter_condition = None
    rows = ["Clinic_LA_code_upper", "Clinic_LA_name_upper", "Clinic_code",
            "Clinic_name"]
    columns = None
    sort_on = ["Clinic_LA_name_upper", "Clinic_code"]
    row_order = None
    column_order = ["Grand_total"]
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_laclinic_clinic_lares_upper(df):
    filter_type = None
    filter_condition = None
    rows = ["Clinic_LA_code_upper", "Clinic_LA_name_upper", "Clinic_code",
            "Clinic_name"]
    columns = "LA_name_inc_small"
    sort_on = ["Clinic_LA_name_upper", "Clinic_code"]
    row_order = None
    column_order = None
    # Note that the total column is renamed here so that it can be easily
    # identified for removal in the output_specific_updates function
    column_rename = {"Grand_total": "All_LAs"}
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total, multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_dq_contacts_provider(df):
    filter_type = None
    filter_condition = None
    rows = ["Org_code", "Org_name"]
    columns = None
    sort_on = ["Org_name"]
    row_order = None
    column_order = None
    column_rename = None
    row_subgroup = None
    column_subgroup = None
    include_row_total = False
    multiplier = 0.001
    output_type = "counts"
    percent_across_columns = False
    disclosure_control = True

    return create_output_crosstab(df, filter_type, filter_condition, rows,
                                  columns, sort_on, row_order, column_order,
                                  column_rename, row_subgroup, column_subgroup,
                                  include_row_total,
                                  multiplier, output_type,
                                  percent_across_columns, disclosure_control)


def create_table_dq_national(df):
    filter_type = None
    filter_condition = None
    breakdown = ["ReportingYear"]
    sort_on = None
    breakdown_order = None
    measure_type = "DQ"
    measure_order = ["Duplicate", "Unknown_LSOA_code", "Unknown_LA_code",
                     "Unknown_GP_code", "Unknown_Ethnicity", "Extreme_age", ]
    breakdown_subgroup = None
    include_breakdown_total = False
    multiplier = None
    output_type = "percents"
    measures_as_rows = False
    disclosure_control = False

    return create_output_multi_field(df, filter_type, filter_condition,
                                     breakdown, sort_on, breakdown_order,
                                     measure_type, measure_order,
                                     breakdown_subgroup,
                                     include_breakdown_total, multiplier,
                                     output_type, measures_as_rows,
                                     disclosure_control)


def create_table_dq_provider(df):
    filter_type = None
    filter_condition = None
    breakdown = ["Org_code", "Org_name"]
    sort_on = ["Org_name"]
    breakdown_order = None
    measure_type = "DQ"
    measure_order = ["Duplicate", "Unknown_LSOA_code", "Unknown_LA_code",
                     "Unknown_GP_code", "Unknown_Ethnicity", "Extreme_age", ]
    breakdown_subgroup = None
    include_breakdown_total = False
    multiplier = None
    output_type = "percents"
    measures_as_rows = False
    disclosure_control = True

    return create_output_multi_field(df, filter_type, filter_condition,
                                     breakdown, sort_on, breakdown_order,
                                     measure_type, measure_order,
                                     breakdown_subgroup,
                                     include_breakdown_total, multiplier,
                                     output_type, measures_as_rows,
                                     disclosure_control)
