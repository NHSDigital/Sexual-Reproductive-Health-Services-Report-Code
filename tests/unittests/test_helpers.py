import pandas as pd
import numpy as np
from datetime import datetime
import srh_code.utilities.helpers as helpers


def test_create_year_list():
    """Tests the create_year_list function, which creates a list of years
    contained within the year field of a dataframe and orders the list by
    oldest year first.
    """
    input_df = pd.DataFrame(
        {
            "CollectionYearRange": ["2020-21", "2018-19", "2020-21", "2017-18",
                                    "2016-17"],
            "Parent_Org_Code": ["A", "A", "D", "H", "D"],
            "Row_Def": ["50", "51-52", "60", "50", "51-52"],
            "Total": [10, 50, 50, 100, 10],
            }
        )

    expected = ["2016-17", "2017-18", "2018-19", "2020-21"]

    actual = helpers.create_year_list(
        input_df,
        year_field="CollectionYearRange",
        )

    assert actual == expected


def test_replace_col_value():
    """Tests the replace_col_value function, create replaces all values within a
    column with another value
    """

    input_df = pd.DataFrame(
        {
            "Screened": [100, 200, 100, 500, 800],
            "Non-op_diag_rate_invasive": [0, 1000, 5000, 250, 2000],
            "Non-op_diag_rate_non-invasive": [0, 2000, 2000, 500, 8000],
            "Assement_rate": [98.8, 67.8, 56.8, 100.0, 87.6]
            }
        )

    expected = pd.DataFrame(
        {
            "Screened": [100, 200, 100, 500, 800],
            "Non-op_diag_rate_invasive": [":", ":", ":", ":", ":"],
            "Non-op_diag_rate_non-invasive": [":", ":", ":", ":", ":"],
            "Assement_rate": [98.8, 67.8, 56.8, 100.0, 87.6]
            }
        )

    actual = helpers.replace_col_value(
        input_df,
        col_names=["Non-op_diag_rate_invasive", "Non-op_diag_rate_non-invasive"],
        replace_value=":",
        )

    pd.testing.assert_frame_equal(actual, expected)


def test_remove_rows():
    """Tests the remove rows function, which removes rows from dataframe where
    any column contains a specified value(s)
    """
    input_df = pd.DataFrame(
        {
            "BreakdownA": ["Total", "Group1", "Group2", "Group1", "Group2", "Group2"],
            "BreakdownB": ["Total", "Total", "Total", "Group1", "Group1", "Group2"],
            "MeasureA": [200, 100, 200, 100, 50, 100],
            "MeasureB": [450, 500, 300, 10, 20, 100],
            }
        )

    expected = pd.DataFrame(
        {
            "BreakdownA": ["Group2"],
            "BreakdownB": ["Group2"],
            "MeasureA": [100],
            "MeasureB": [100],
            }
        )

    actual = helpers.remove_rows(
        input_df,
        remove_values=["Total", "Group1"]
        )

    pd.testing.assert_frame_equal(actual.reset_index(drop=True),
                                  expected.reset_index(drop=True))


def test_excel_cell_to_col_num():
    """
   Tests that the excel_cell_to_col_num function works as expected

    """

    cells = ["A1", "D8", "AA1"]

    actual = []
    for cell in cells:
        a = helpers.excel_cell_to_col_num(cell)
        actual.append(a)

    expected = [1, 4, 27]

    assert actual == expected, f"When checking excel_cell_to_col_num expected to find {expected} but found {actual}"


def test_excel_col_to_df_col():
    """
   Tests that the excel_col_to_df_col function works as expected

    """
    write_cell = "B10"
    cols = ["C", "E", "AA"]

    actual = []
    for col in cols:
        a = helpers.excel_col_to_df_col(col, write_cell)
        actual.append(a)

    expected = [1, 3, 25]

    assert actual == expected, f"When checking excel_col_to_df_col expected to find {expected} but found {actual}"


def test_add_percent_or_rate():
    """
    Tests the add_percent_or_rate function, which adds a calculated percentage
    or rate to the dataframe based on defined inputs.
    """

    input_df = pd.DataFrame(
        {
            "Numerator_Col": [50, 100, 25, 0],
            "Denominator_Col": [100, 800, 100, 0]
            }
        )

    expected = pd.DataFrame(
        {
            "Numerator_Col": [50, 100, 25, 0],
            "Denominator_Col": [100, 800, 100, 0],
            "New_Col_Name": [50, 12.5, 25, np.nan]}
        )

    actual = helpers.add_percent_or_rate(
        input_df,
        new_column_name="New_Col_Name",
        numerator="Numerator_Col",
        denominator="Denominator_Col",
        multiplier=100)

    pd.testing.assert_frame_equal(actual, expected)


def test_add_percent_or_rate_no_multiplier():
    """
    Tests the add_percent_or_rate function, which adds a calculated percentage
    or rate to the dataframe based on defined inputs. This version tests the
    function when no multiplier is supplied.
    """

    input_df = pd.DataFrame(
        {
            "Numerator_Col": [50, 100, 25, 0],
            "Denominator_Col": [100, 800, 100, 0]
            }
        )

    expected = pd.DataFrame(
        {
            "Numerator_Col": [50, 100, 25, 0],
            "Denominator_Col": [100, 800, 100, 0],
            "New_Col_Name": [0.5, 0.125, 0.25, np.nan]}
        )

    actual = helpers.add_percent_or_rate(
        input_df,
        new_column_name="New_Col_Name",
        numerator="Numerator_Col",
        denominator="Denominator_Col")

    pd.testing.assert_frame_equal(actual, expected)


def test_add_subgroup_rows():
    """Tests add_subgroup_rows, which adds extra subgroup rows
    based on the subgroup input. This tests the function using age groups.
    """
    input_df = pd.DataFrame(
        {
            "Parent_Code": ["ENG", "ENG", "ENG", "ENG", "ENG", "ENG"],
            "Row_Def": ["50", "51-52", "60", "65-69", "70", "71-73"],
            "Total": [10, 10, 10, 20, 30, 10]
        }
    )

    expected = pd.DataFrame(
        {
            "Parent_Code": ["ENG", "ENG", "ENG", "ENG", "ENG", "ENG", "ENG", "ENG"],
            "Row_Def": ["50", "51-52", "60", "65-69", "70", "71-73", "50-52", "65-70"],
            "Total": [10, 10, 10, 20, 30, 10, 20, 50]
        }
    )

    actual = helpers.add_subgroup_rows(
        input_df,
        breakdown=["Parent_Code", "Row_Def"],
        subgroup={"Row_Def": {"50-52": ["50", "51-52"],
                              "65-70": ["65-69", "70"]}},
    )

    pd.testing.assert_frame_equal(actual.reset_index(drop=True),
                                  expected.reset_index(drop=True))


def test_add_subgroup_columns():
    """Tests add_subgroup_columns function, which combines groups of columns
    into a single summed column. This tests the function using Table Code
    """
    input_df = pd.DataFrame(
        {
           "A": [0, 10, 10, 20],
           "B": [0, 20, 10, 0],
           "C1": [0, 15, 5, 10],
           "C2": [0, 5, 50, 100],
           "D": [0, 10, 10, 0],
           }
        )

    expected = pd.DataFrame(
        {
            "A": [0, 10, 10, 20],
            "B": [0, 20, 10, 0],
            "C1": [0, 15, 5, 10],
            "C2": [0, 5, 50, 100],
            "D": [0, 10, 10, 0],
            "A and C1": [0, 25, 15, 30],
            "A to C2": [0, 50, 75, 130],
            }
        )

    actual = helpers.add_subgroup_columns(
        input_df,
        subgroup={'A and C1': ['A', 'C1'],
                  'A to C2': ['A', 'B', 'C1', 'C2']
                  }
        )

    pd.testing.assert_frame_equal(actual.reset_index(drop=True),
                                  expected.reset_index(drop=True))


def test_order_by_list():
    """Tests the order_by_list function, which orders a dataframe by a customer
    list based on a specified column within the dataframe.  Tested using region
    codes.
    """
    input_df = pd.DataFrame(
        {
            "Parent_Org_Code": ["A", "B", "D", "E", "F", "G", "H", "J", "K"],
            "Total": [10, 10, 20, 20, 30, 10, 50, 100, 50],
            }
        )

    expected = pd.DataFrame(
        {
            "Parent_Org_Code": ["A", "D", "B", "E", "F", "H", "G", "K", "J"],
            "Total": [10, 20, 10, 20, 30, 50, 10, 50, 100],
            }
        )

    actual = helpers.order_by_list(
        input_df,
        column="Parent_Org_Code",
        order=["A", "D", "B", "E", "F", "H", "G", "K", "J"],
       )

    pd.testing.assert_frame_equal(actual, expected)


def test_group_numeric_values():
    """Tests the group_numeric_value function, which creates a new column in
    the dataframe and add a new value based on the source field.
    """

    age_groups = {"<16": {1: 15},
                  "16-24": {16: 24},
                  "25-34": {25: 34},
                  "35-44": {35: 44},
                  "45-54": {45: 54},
                  "55-64": {55: 64},
                  "65-74": {65: 74},
                  "75+": {75: 120}
                  }

    input_df = pd.DataFrame(
            {
                "STARTAGE": [15, 16, 25, 35, 45, 55, 65, 75, 150],
                }
            )

    expected = pd.DataFrame(
        {
            "STARTAGE": [15, 16, 25, 35, 45, 55, 65, 75, 150],
            "Age_groups": ["<16", "16-24", "25-34", "35-44", "45-54",
                           "55-64", "65-74", "75+", 'unknown'],
            }
        )

    source_field = 'STARTAGE'
    group_name = 'Age_groups'
    default_value = 'unknown'
    group_info = age_groups

    actual = helpers.group_numeric_values(input_df,
                                          source_field,
                                          group_name,
                                          group_info,
                                          default_value)

    pd.testing.assert_frame_equal(actual, expected)


def test_add_organisation_type():
    """
    Tests the add_organisation_type function
    """

    input_df = pd.DataFrame(
        {
            "Org_code": ["E92000001", "E06000001", "E07000001", "E08000001",
                         "E09000001", "E10000001", "E12000001", "E38000001",
                         "E40000001", "E54000001", "E99999999"],
            }
        )

    expected = pd.DataFrame(
        {
            "Org_code": ["E92000001", "E06000001", "E07000001", "E08000001",
                         "E09000001", "E10000001", "E12000001", "E38000001",
                         "E40000001", "E54000001", "E99999999"],
            "Org_type": ["National", "LA", "LA", "LA",
                         "LA", "LA", "LA_parent", "CCG",
                         "ICB_parent", "ICB", "None"],
            "Org_level": ["National", "Local", "Local", "Local",
                          "Local", "Local", "Regional", "Local",
                          "Regional", "Local", "None"],
            }
        )

    actual = helpers.add_organisation_type(
        input_df,
        org_code_column="Org_code",
        )

    pd.testing.assert_frame_equal(actual, expected)


def test_hes_year_to_fyear():
    """
   Tests that the hes_year_to_fyear function works as expected
    """

    input_df = pd.DataFrame(
        {
            "ReportingYear": ["0001", "2021"],
            "Count": [200, 100],
        }
    )

    expected = pd.DataFrame(
        {
            "ReportingYear": ["2000-01", "2020-21"],
            "Count": [200, 100],
        }
    )

    actual = helpers.hes_year_to_fyear(input_df)

    pd.testing.assert_frame_equal(actual, expected)


def test_calendar_year_to_fyear():
    """
   Tests that the calendar_year_to_fyear function works as expected
    """

    input_df = pd.DataFrame(
        {
            "ReportingYear": [2000, 2021],
            "Count": [200, 100],
        }
    )

    expected = pd.DataFrame(
        {
            "ReportingYear": ["2000-01", "2021-22"],
            "Count": [200, 100],
        }
    )

    actual = helpers.calendar_year_to_fyear(input_df)

    pd.testing.assert_frame_equal(actual, expected)


def test_fyear_to_year_start_end():
    """
   Tests that the fyear_to_year_start_end function works as expected

    """
    input_value = "2019-20"

    actual_start, actual_end = helpers.fyear_to_year_start_end(input_value)

    expected_start = datetime.strptime("2019-04-01", '%Y-%m-%d').date()
    expected_end = datetime.strptime("2020-03-31", '%Y-%m-%d').date()

    assert actual_start == expected_start, f"When checking fyear_to_year_start_end\
        expected to find {expected_start} but found {actual_start}"
    assert actual_end == expected_end, f"When checking fyear_to_year_start_end\
        expected to find {expected_end} but found {actual_end}"


def test_add_group_to_df():
    """
    Tests the add_group_to_df function, which groups a dataframe on a single
    column and appends it back to the original dataframe
    """

    input_df = pd.DataFrame(
            {
                "Sex": [1, 1, 1, 2, 2, 2],
                "Age": [20, 22, 19, 20, 19, 82],
                "Count": [20, 10, 10, 5, 2, 1],
            }
        ).sort_values(by=["Sex", "Age", "Count"])

    expected = pd.DataFrame(
            {
                "Sex": [1, 1, 1, 2, 2, 2, 3, 3, 3, 3],
                "Age": [20, 22, 19, 20, 19, 82, 20, 22, 19, 82],
                "Count": [20, 10, 10, 5, 2, 1, 25, 10, 12, 1],
            }
        ).sort_values(by=["Sex", "Age", "Count"])

    group_on = "Sex"
    group_value = 3
    count_column = "Count"

    actual = helpers.add_group_to_df(input_df,
                                     group_on,
                                     group_value,
                                     count_column)

    pd.testing.assert_frame_equal(actual.reset_index(drop=True),
                                  expected.reset_index(drop=True))


def test_suppress_column():
    """
    Tests the suppress_column function
    """
    input_column = pd.Series([0, 1, 4, 7, 8, 12, 16, 21, 101], name="to_suppress")

    actual = helpers.suppress_column(input_column)

    expected = pd.Series([0, np.nan, np.nan, np.nan, 10, 10, 15, 20, 100],
                         name="to_suppress")

    pd.testing.assert_series_equal(actual, expected)


def test_round_half_up():
    """
    Tests the round_half_up function, using various example of postive and
    negative numbers, with various decimal precision

    """

    assert helpers.round_half_up(1.234, 2) == 1.23
    assert helpers.round_half_up(-1.234, 2) == -1.23
    assert helpers.round_half_up(2.675, 2) == 2.68
    assert helpers.round_half_up(-2.675, 2) == -2.68
    assert helpers.round_half_up(3.14159, 3) == 3.142
    assert helpers.round_half_up(-3.14159, 3) == -3.142
    assert helpers.round_half_up(0.5, 0) == 1
    assert helpers.round_half_up(-0.5, 0) == -1
    assert helpers.round_half_up(0, 2) == 0
    assert helpers.round_half_up(2.5, 0) == 3
    assert helpers.round_half_up(3.5, 0) == 4
    assert helpers.round_half_up(0.5, 1) == 0.5
