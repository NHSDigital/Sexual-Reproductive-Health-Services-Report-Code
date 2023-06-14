import pandas as pd
import numpy as np
from srh_code.utilities import pre_processing


def test_update_non_english_las():
    """
    Tests the update_non_english_las function, which updates non-English UK
    LA codes to country level (e.g. Aberdeen to Scotland) for reporting purposes.
    """
    input_df = pd.DataFrame(
        {"LA_code_lower": ["E09000001", "E07000028", "S12000033", "W06000022",
                           "N09000009", "X99999999"],
         "LA_name_lower": ["City of London", "Carlisle", "Aberdeen City",
                           "Newport", "Mid Ulster", "Unknown"],
         "LA_code": ["E09000001", "E10000006", "S12000033", "W06000022",
                     "N09000009", "X99999999"],
         "LA_name": ["City of London", "Cumbria", "Aberdeen City", "Newport",
                     "Mid Ulster", "Unknown"],
         "LA_parent_code": ["E12000006", "E12000006", "S12000002", "W12000002",
                            "N12000009", "X99999999"]}
        )

    expected = pd.DataFrame(
        {"LA_code_lower": ["E09000001", "E07000028", "S99999999", "W99999999",
                           "N99999999", "X99999999"],
         "LA_name_lower": ["City of London", "Carlisle", "Scotland",
                           "Wales", "Northern Ireland", "Unknown"],
         "LA_code": ["E09000001", "E10000006", "S99999999", "W99999999",
                     "N99999999", "X99999999"],
         "LA_name": ["City of London", "Cumbria", "Scotland", "Wales",
                     "Northern Ireland", "Unknown"],
         "LA_parent_code": ["E12000006", "E12000006", "S99999999", "W99999999",
                            "N99999999", "X99999999"]}
        )

    actual = pre_processing.update_non_english_las(input_df)

    pd.testing.assert_frame_equal(actual, expected)


def test_update_non_uk_las():
    """
    Tests the update_non_uk_las function, which updates non UK LA codes and
    names to the defaults for reporting purposes.
    """
    input_df = pd.DataFrame(
        {"LA_code_lower": ["E07000028", "M99999999", "L99999999", "X99999998",
                           "X99999999"],
         "LA_name_lower": ["Carlisle", "Isle of Man", "Channel Islands",
                           "Not applicable (outside United Kingdom)", "Not known"],
         "LA_code": ["E10000006", "M99999999", "L99999999", "X99999998",
                     "X99999999"],
         "LA_name": ["Cumbria", "Isle of Man", "Channel Islands",
                     "Not applicable (outside United Kingdom)", "Not known"],
         "LA_parent_code": ["E12000006", "M99999999", "L99999999", "X99999998",
                            "X99999999"]}
        )

    expected = pd.DataFrame(
        {"LA_code_lower": ["E07000028", "X99999998", "X99999998", "X99999998",
                           "X99999999"],
         "LA_name_lower": ["Carlisle", "Outside the United Kingdom",
                           "Outside the United Kingdom",
                           "Outside the United Kingdom", "Not known"],
         "LA_code": ["E10000006", "X99999998", "X99999998", "X99999998",
                     "X99999999"],
         "LA_name": ["Cumbria", "Outside the United Kingdom",
                     "Outside the United Kingdom",
                     "Outside the United Kingdom", "Not known"],
         "LA_parent_code": ["E12000006", "X99999998", "X99999998", "X99999998",
                            "X99999999"]}
        )

    actual = pre_processing.update_non_uk_las(input_df)

    pd.testing.assert_frame_equal(actual, expected)


def test_update_small_las():
    """
    Tests the update_small_las function, which updates small LA details to
    neighbouring LA details for non-disclosure purposes (currently City of
     London and Isles of Scilly)
    """
    Org_updates = {"From_code": ["E09000001",
                                 "E06000053"],
                   "To_code": ["E09000012",
                               "E06000052"],
                   "From_name": ["City of London",
                                 "Isles of Scilly"],
                   "To_name": ["Hackney",
                               "Cornwall"]
                   }

    input_df = pd.DataFrame(
        {"Org_code": ["E09000001", "E09000012", "E06000053",
                      "E06000052", "E06000047", "E10000006"],
         "Org_name": ["City of London", "Hackney", "Isles of Scilly",
                      "Cornwall", "County Durham", "Cumbria"]}
        )

    expected = pd.DataFrame(
        {"Org_code": ["E09000012", "E09000012", "E06000052", "E06000052",
                      "E06000047", "E10000006"],
         "Org_name": ["Hackney", "Hackney", "Cornwall", "Cornwall",
                      "County Durham", "Cumbria"]}
        )

    actual = pre_processing.update_small_las(input_df,
                                             "Org_code",
                                             "Org_name",
                                             Org_updates)

    pd.testing.assert_frame_equal(actual, expected)


def test_map_org_code_to_name():
    """
    Tests the map_org_code_to_name function, which adds organisation names to
    a dataframe based on specfied organisation code column(s),
    by using a reference data file.
    """
    input_df = pd.DataFrame({
        "LA_code": ["E00000001", "E00000002", "E00000009"],
        "Region_code": ["E12000001", "E12000005", "E12000007"],
        })

    input_df_ref = pd.DataFrame({
        "Org_code": ["E00000001", "E00000002", "E00000003",
                     "E00000004", "E00000005", "E00000006",
                     "E00000007", "E00000008", "E00000009",
                     "E12000001", "E12000002", "E12000003",
                     "E12000004", "E12000005", "E12000006"],
        "Org_name": ["Darlington", "Coventry", "York",
                     "Oxford", "Bath", "Bristol",
                     "Warrington", "Luton", "Blackpool",
                     "North East", "North West", "Yorkshire & Humber",
                     "East Midlands", "West Midlands", "London"]
        })

    col_ref = ["LA_code", "Region_code"]

    actual_df = pre_processing.map_org_code_to_name(input_df, input_df_ref,
                                                    col_ref)

    expected_df = pd.DataFrame({
        "LA_code": ["E00000001", "E00000002", "E00000009"],
        "Region_code": ["E12000001", "E12000005", "E12000007"],
        "LA_name": ["Darlington", "Coventry", "Blackpool"],
        "Region_name": ["North East", "West Midlands", np.nan]
        }
        )

    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_update_prescribing_data():
    """
    Tests the update_prescribing_data function, which adds the contraceptve
    group and subgroup columns to the source data, by linking with reference
    data.
    """
    input_df_source = pd.DataFrame(
        {
            "Year": ["2021", "2021", "2021"],
            "Drug Name": ["Drug A", "Drug B", "Drug C"],
            "Number Items": [20, 50, 100]
            }
        )

    input_df_ref = pd.DataFrame(
        {
            "Drug Name": ["Drug A", "Drug B", "Drug c"],
            "Group": ["LARC", "User_dependent", "Emergency"],
            "Subgroup": ["01_iud", "05_combined", "11_emergency"]
            }
        )

    expected_df = pd.DataFrame(
        {
            "Year": ["2021", "2021", "2021"],
            "Drug Name": ["drug a", "drug b", "drug c"],
            "Number Items": [20, 50, 100],
            "Group": ["LARC", "User_dependent", "Emergency"],
            "Subgroup": ["01_iud", "05_combined", "11_emergency"]
            }
        )

    actual_df = pre_processing.update_prescribing_data(
        input_df_source,
        input_df_ref,
        cyear="2021"
        )

    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_apply_clinic_as_org():
    """
    Tests the apply_clinic_as_org function

    """

    input_df = pd.DataFrame({
        "Org_code": ["NQ5", "A1B", "C3D"],
        "Org_name": ["Org Name 1", "Org Name 2", "Org Name 3"],
        "Clinic_code": ["C1", "C2", "C3"],
        "Clinic_name": ["Clinic Name 1", "Clinic Name 2", "Clinic Name 3"]
    })

    expected_df = pd.DataFrame({
        "Org_code": ["C1", "A1B", "C3D"],
        "Org_name": ["Clinic Name 1", "Org Name 2", "Org Name 3"],
        "Clinic_code": ["C1", "C2", "C3"],
        "Clinic_name": ["Clinic Name 1", "Clinic Name 2", "Clinic Name 3"],
        "Org_code_unedited": ["NQ5", "A1B", "C3D"]
    })

    actual_df = pre_processing.apply_clinic_as_org(input_df, "NQ5")

    pd.testing.assert_frame_equal(actual_df, expected_df)
