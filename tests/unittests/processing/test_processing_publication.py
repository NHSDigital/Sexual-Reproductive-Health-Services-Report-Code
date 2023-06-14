import pandas as pd
import numpy as np
import srh_code.utilities.processing.processing_publication as processing
from srh_code.utilities import helpers


def test_check_for_sort_on():
    """Tests the check_for_sort_on function.
    """

    expected_rows = ["LA_code", "LA_name", "LA_parent_code"]
    expected_cols_to_remove = ["LA_parent_code"]

    actual_rows, actual_cols_to_remove = processing.check_for_sort_on(
                                        sort_on=["LA_parent_code", "LA_name"],
                                        rows=["LA_code", "LA_name"],
                                        )

    assert actual_rows == expected_rows
    assert actual_cols_to_remove == expected_cols_to_remove


def test_sort_for_output_defined():
    """
    Tests the sort for output_defined function, which sorts a dataframe
    by the order required for Excel tables.
    """
    input_df = pd.DataFrame(
        {
            "RowDef": ["<45", "45-49", "50-52", "53-54", "55-59", "60-64", "65-69",
                       "70", "71-74", "50-74", "65-70", "53<71"],
            "A": [200, 100, 200, 50, 100, 500, 300, 200, 150, 2350, 500, 1150],
            "B": [450, 500, 300, 100, 50, 250, 600, 100, 60, 1460, 700, 1100],
            }
        )

    expected = pd.DataFrame(
        {
            "RowDef": ["50-74", "65-70", "53<71", "45-49", "50-52", "53-54",
                       "55-59", "60-64", "65-69", "70", "71-74"],
            "A": [2350, 500, 1150, 100, 200, 50, 100, 500, 300, 200, 150],
            "B": [1460, 700, 1100, 500, 300, 100, 50, 250, 600, 100, 60],
            }
        )

    actual = processing.sort_for_output_defined(
        input_df,
        rows=["RowDef"],
        row_order=["50-74", "65-70", "53<71", "45-49", "50-52", "53-54",
                   "55-59", "60-64", "65-69", "70", "71-74"],
        )

    pd.testing.assert_frame_equal(actual.reset_index(drop=True),
                                  expected.reset_index(drop=True))


def test_sort_for_output():
    """
    Tests the sort for output function
    """

    input_df = pd.DataFrame(
        {
            "Org_Name": ["Bolton", "Bradford", "Camden", "Cumbria", "Gateshead",
                         "Hartlepool", "Islington", "Leeds", "Liverpool",
                         "Rotherham", "Tameside", "Westminster"],
            "Parent_OrgONSCode": ["E12000002", "E12000003", "E12000007",
                                  "E12000001", "E12000001", "E12000001",
                                  "E12000007", "E12000003", "E12000002",
                                  "E12000003", "E12000002", "E12000007"],
            "A": [150, 300, 500, 800, 50, 100, 700, 350, 960, 10, 200, 750],
            }
        )

    expected = pd.DataFrame(
        {
            "Org_Name": ["Cumbria", "Gateshead", "Hartlepool", "Bolton",
                         "Liverpool", "Tameside", "Bradford", "Leeds",
                         "Rotherham", "Camden", "Islington", "Westminster"],
            "A": [800, 50, 100, 150, 960, 200, 300, 350, 10, 500, 700, 750],
            }
        )

    actual = processing.sort_for_output(
        input_df,
        sort_on=["Parent_OrgONSCode", "Org_Name"],
        cols_to_remove=['Parent_OrgONSCode'],
        )

    pd.testing.assert_frame_equal(actual.reset_index(drop=True),
                                  expected.reset_index(drop=True))


def test_df_counts_to_percents_rows():
    """
    Tests the df_counts_to_percents function
    """

    input_df = pd.DataFrame(
        {
            "Method": ["LARC", "User_dependent", "Other", "Grand_total"],
            "16-17": [20, 30, 100, 150],
            "18-19": [10, 90, 300, 400],
            "Grand_total": [30, 120, 400, 550],
            }
        )

    expected = pd.DataFrame(
        {
            "Method": ["LARC", "User_dependent", "Other", "Grand_total"],
            "16-17": ["#", "#", "#", "#"],
            "18-19": [2.5, 22.5, 75.0, 100.0],
            "Grand_total": [5.5, 21.8, 72.7, 100.0],
            }
        )

    actual = processing.df_counts_to_percents(
        input_df,
        rows=["Method"],
        percent_across_columns=False,
        disclosure_control=False,
        denominator="Grand_total",
        )

    pd.testing.assert_frame_equal(actual, expected, check_dtype=False,
                                  check_exact=False, rtol=1e-1)


def test_df_counts_to_percents_columns():
    """
    Tests the df_counts_to_percents function with percent_across_columns set to False
    """

    input_df = pd.DataFrame(
        {
            "Age_group": ["16-17", "18-19", "20-24", "Grand_total"],
            "LARC": [20, 200, 1000, 1500],
            "User_dependent": [10, 200, 200, 3000],
            "Grand_total": [30, 400, 1200, 4500],
            }
        )

    expected = pd.DataFrame(
        {
            "Age_group": ["16-17", "18-19", "20-24", "Grand_total"],
            "LARC": ["#", 50, 83, 33],
            "User_dependent": ["#", 50, 17, 67],
            "Grand_total": ["#", 100, 100, 100],
            }
        )

    actual = processing.df_counts_to_percents(
        input_df,
        rows=["Age_group"],
        percent_across_columns=True,
        disclosure_control=True,
        denominator="Grand_total",
        )

    pd.testing.assert_frame_equal(actual, expected, check_dtype=False,
                                  check_exact=False, rtol=1e-1)


def test_select_org_ref_data():
    """
    Tests the select_org_ref_data function, which selects content from the
    organisation reference data based on user defined org type and column content
    """

    input_df = pd.DataFrame(
        {
            "Org_code": ["E06000001", "E10000001", "E07000001", "E54000001",
                         "E54000002", "E12000001", "E40000001"],
            "Org_name": ["LA1", "LA2", "LA3", "ICB1", "ICB2", "REG1", "CREG1"],
            "Parent_code": ["E12000001", "E12000002", "E12000002",
                            "E40000001", "E400000002", "E92000001",
                            "E92000001"],
            "Parent_name": ["REG1", "REG2", "REG2", "CREG1", "CREG2",
                            "ENG", "ENG"],
            "Entity_code": ["E06", "E10", "E07", "E54", "E54", "E12", "E40"],
            "Org_type": ["LA", "LA", "LA", "ICB", "ICB", "LA_parent",
                         "ICB_parent"],
            "Org_level": ["Local", "Local", "Local", "Local", "Local",
                          "Regional", "Regional"],
            }
        )

    helpers.create_folder("cached_dataframes/")
    input_df.to_feather('cached_dataframes/df_la_ref.ft')

    expected = pd.DataFrame(
        {
            "LA_code": ["E06000001", "E10000001"],
            "LA_name": ["LA1", "LA2"],
            "LA_parent_name": ["REG1", "REG2"]
            }
        )

    actual = processing.select_org_ref_data(org_type="LA",
                                            columns=["LA_code",
                                                     "LA_name",
                                                     "LA_parent_name"])

    helpers.remove_folder("cached_dataframes/")

    pd.testing.assert_frame_equal(actual.reset_index(drop=True),
                                  expected.reset_index(drop=True))


def test_df_apply_rates():
    """Tests the df_apply_rates function, which creates a new dataframe containing
    calculations from 2 dataframes holding the numerator and denominator counts
    """
    input_df_denom = pd.DataFrame(
        {
            "Org_code": ["R1", "R2", "R3", "R4"],
            "A": [100, 500, 1000, 2500],
            "B": [0, 20, 50, 100],
            "C": [1000, 2000, 500, 1000],
            }
        )

    input_df_num = pd.DataFrame(
        {
            "Org_code": ["R1", "R2", "R3", "R4"],
            "A": [0, 250, 800, 250],
            "B": [0, 5, 38, 72],
            "C": [100, 250, 100, 100],
            }
        )

    expected = pd.DataFrame(
        {
            "Org_code": ["R1", "R2", "R3", "R4"],
            "A": [0.0, 500.0, 800.0, 100.0],
            "B": [np.nan, 250.0, 760.0, 720.0],
            "C": [100.0, 125.0, 200.0, 100.0],
            }
        )

    actual = processing.df_apply_rates(
        input_df_denom,
        input_df_num,
        rows=["Org_code"],
        multiplier=1000
        )

    pd.testing.assert_frame_equal(actual, expected)
