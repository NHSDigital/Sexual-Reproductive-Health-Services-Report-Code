import pandas as pd
import numpy as np
from srh_code.utilities import field_definitions


def test_contraceptive_care_flags():
    """
    Tests the contraceptive_care_flags function, which creates new fields with
    flags to indicate contraceptive care activity.
    """
    input_df = pd.DataFrame({"ContraceptiveMethodStatus": [1, 3, 2, 3, 4, 1,
                                                           np.nan]})
    expected_df = pd.DataFrame({"ContraceptiveMethodStatus": [1, 3, 2, 3, 4, 1,
                                                              np.nan],
                                "MainMethodNewFlag": [1, np.nan, np.nan,
                                                      np.nan, np.nan, 1,
                                                      np.nan],
                                "MainMethodChangeFlag": [np.nan, np.nan, 1,
                                                         np.nan, np.nan,
                                                         np.nan, np.nan],
                                "MainMethodMaintFlag": [np.nan, 1, np.nan, 1,
                                                        np.nan, np.nan,
                                                        np.nan],
                                "MainMethodAdviceFlag": [np.nan, np.nan,
                                                         np.nan, np.nan, 1,
                                                         np.nan, np.nan],
                                "ContraceptiveCareFlag": [1, 1, 1, 1, 1, 1,
                                                          np.nan]})

    actual_df = field_definitions.contraceptive_care_flags(input_df)

    pd.testing.assert_frame_equal(actual_df.reset_index(drop=True),
                                  expected_df.reset_index(drop=True))


def test_srh_activity_flags():
    """
    Tests the srh_activity_flags function, creates new fields with flags to
    indicate SRH code activity.
    """
    input_df = pd.DataFrame({"SRHCareActivity1": [2, 23, 5, 12, 15, 22, 23, 33,
                                                  34, 41],
                             "SRHCareActivity2": [1, 3, 8, 13, 21, 24, 25, 32,
                                                  35, np.nan],
                             "SRHCareActivity3": [6, 4, 9, 14, 20, 26, 31, 36,
                                                  37, np.nan],
                             "SRHCareActivity4": [11, 7, 10, 16, 19, 27, 28,
                                                  38, np.nan, np.nan],
                             "SRHCareActivity5": [13, 11, 17, 18, 29, 30, 39,
                                                  40, np.nan, np.nan],
                             "SRHCareActivity6": [np.nan, np.nan, np.nan,
                                                  np.nan, np.nan, np.nan,
                                                  np.nan, np.nan, np.nan,
                                                  np.nan]})

    expected_df = pd.DataFrame({"SRHCareActivity1": [2, 23, 5, 12, 15, 22, 23,
                                                     33, 34, 41],
                                "SRHCareActivity2": [1, 3, 8, 13, 21, 24, 25,
                                                     32, 35, np.nan],
                                "SRHCareActivity3": [6, 4, 9, 14, 20, 26, 31,
                                                     36, 37, np.nan],
                                "SRHCareActivity4": [11, 7, 10, 16, 19, 27, 28,
                                                     38, np.nan, np.nan],
                                "SRHCareActivity5": [13, 11, 17, 18, 29, 30,
                                                     39, 40, np.nan, np.nan],
                                "SRHCareActivity6": [np.nan, np.nan, np.nan,
                                                     np.nan, np.nan, np.nan,
                                                     np.nan, np.nan, np.nan,
                                                     np.nan],
                                "SRH_advice": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                "Pregnancy": [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                                "Abortion": [1, 2, 4, 0, 0, 0, 0, 0, 0, 0],
                                "Cervical_screening": [1, 1, 0, 0, 0, 0, 0, 0,
                                                       0, 0],
                                "Psychosexual": [1, 0, 0, 2, 0, 0, 0, 0, 0, 0],
                                "Implant_removal": [0, 0, 0, 0, 1, 0, 0, 0, 0,
                                                    0],
                                "IUS_removal": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                "IUD_removal": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                "Ultrasound": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                                "PMS_menopause": [0, 1, 0, 1, 0, 2, 1, 0, 0,
                                                  0],
                                "Alcohol": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                                "STI_care": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                                "Other": [0, 0, 1, 2, 2, 1, 4, 5, 2, 1]
                                })

    actual_df = field_definitions.srh_activity_flags(input_df)

    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_ec_oral_iud_flags():
    """
    Tests the ec_oral_IUD_flags function, which creates new fields with flags
    to indicate emergency oral contraception activity and emergency IUD
    contraception activity.
    """
    input_df = pd.DataFrame({"ContraceptiveMethodPostCoital1": [1, 2, 1, 2,
                                                                np.nan, 1, 2],
                             "ContraceptiveMethodPostCoital2": [2, 1, np.nan,
                                                                np.nan, np.nan,
                                                                1, 2]})

    expected_df = pd.DataFrame({"ContraceptiveMethodPostCoital1": [1, 2, 1, 2,
                                                                   np.nan, 1,
                                                                   2],
                                "ContraceptiveMethodPostCoital2": [2, 1,
                                                                   np.nan,
                                                                   np.nan,
                                                                   np.nan, 1,
                                                                   2],
                                "ECOralFlag": [1, 1, 1, np.nan, np.nan, 1,
                                               np.nan],
                                "ECIUDFlag": [1, 1, np.nan, 1, np.nan, np.nan,
                                              1]})

    actual_df = field_definitions.ec_oral_iud_flags(input_df)

    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_number_ec_items():
    """
    Tests the number_ec_items function, which creates new field with count of
    emergency contraception items.
    """
    input_df = pd.DataFrame({"ContraceptiveMethodPostCoital1": [1, 2, 1, 2,
                                                                np.nan, 1, 2],
                             "ContraceptiveMethodPostCoital2": [2, 1, np.nan,
                                                                np.nan, np.nan,
                                                                1, 2]})

    expected_df = pd.DataFrame({"ContraceptiveMethodPostCoital1": [1, 2, 1, 2,
                                                                   np.nan, 1,
                                                                   2],
                                "ContraceptiveMethodPostCoital2": [2, 1,
                                                                   np.nan,
                                                                   np.nan,
                                                                   np.nan, 1,
                                                                   2],
                                "Number_EC_items": [2, 2, 1, 1, 0, 2, 2]})

    actual_df = field_definitions.number_ec_items(input_df)

    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_outside_england_flag():
    """
    Tests the outside_england_flag function
    """
    input_df = pd.DataFrame({"LA_parent_code": ["E12000001", "X99999999",
                                                "S99999999", "X99999998"]}
                            )
    expected_df = pd.DataFrame({"LA_parent_code": ["E12000001", "X99999999",
                                                   "S99999999", "X99999998"],
                               "Outside_england": ["N", "N", "Y", "Y"]})

    actual_df = field_definitions.outside_england_flag(input_df)

    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_cross_boundary_check():
    """
    Tests the cross_boundary_check function which identifies if the patient was
    resident inside or outside the Local Authority (LA) of the clinic location
    and adds a column with the new information.
    """
    input_df = pd.DataFrame({"Clinic_LA_code_upper": ["E09000001", "E09000001",
                                                      "E09000001", "E09000001"],
                             "LA_code": ["E09000001", "E08000001",
                                         "S99999999", "X99999999"]}
                            )
    expected_df = pd.DataFrame({"Clinic_LA_code_upper": ["E09000001", "E09000001",
                                                         "E09000001", "E09000001"],
                                "LA_code": ["E09000001", "E08000001",
                                            "S99999999", "X99999999"],
                                "Cross_boundary_upper": ["Inside", "Outside",
                                                         "Outside", "Unknown"]}
                               )

    actual_df = field_definitions.cross_boundary_check(input_df,
                                                       "Clinic_LA_code_upper",
                                                       "LA_code",
                                                       "Cross_boundary_upper")

    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_dq_duplicate_flag():
    """
    Tests the dq_duplicate_flag function, which flags duplicate records
    """
    input_df = pd.DataFrame({"RowNum": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                             "Org_code": ["E00000001", "E00000001", "E00000003",
                                          "E00000003", "E00000003", "E00000006",
                                          "E00000006", "E00000008", "E00000009",
                                          "E12000001"],
                             "FirstContact": ["N", "Y", "Y", "N", "N", "Y",
                                              "Y", "N", "Y", "Y"],
                             "MainContact": ["Y", "N", "Y", "N", "N", "Y",
                                             "Y", "N", "N", "Y"],
                             "ContraceptiveMethodStatus": [1, 1, 2, 2, 2, 1, 1,
                                                           np.nan, 3, 4],
                             "SRHCareActivity1": [2, 2, 5, 5, 5, 3, 4, 33,
                                                  34, 41],
                             "SRHCareActivity2": [1, 1, np.nan, np.nan, np.nan,
                                                  1, 1, 32, 35, np.nan],
                             "SRHCareActivity3": [4, 4, np.nan, np.nan, np.nan,
                                                  3, 3, 36, 37, np.nan]
                             })

    expected_df = pd.DataFrame({"RowNum": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                "Org_code": ["E00000001", "E00000001", "E00000003",
                                             "E00000003", "E00000003", "E00000006",
                                             "E00000006", "E00000008", "E00000009",
                                             "E12000001"],
                                "FirstContact": ["N", "Y", "Y", "N", "N", "Y",
                                                 "Y", "N", "Y", "Y"],
                                "MainContact": ["Y", "N", "Y", "N", "N", "Y",
                                                "Y", "N", "N", "Y"],
                                "ContraceptiveMethodStatus": [1, 1, 2, 2, 2, 1, 1,
                                                              np.nan, 3, 4],
                                "SRHCareActivity1": [2, 2, 5, 5, 5, 3, 4, 33,
                                                     34, 41],
                                "SRHCareActivity2": [1, 1, np.nan, np.nan, np.nan,
                                                     1, 1, 32, 35, np.nan],
                                "SRHCareActivity3": [4, 4, np.nan, np.nan, np.nan,
                                                     3, 3, 36, 37, np.nan],
                                "Duplicate": [0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
                                })

    actual_df = field_definitions.dq_duplicate_flag(input_df)

    pd.testing.assert_frame_equal(actual_df, expected_df, check_dtype=False)


def test_dq_extreme_age_flag():
    """
    Tests the dq_extreme_age_flag function, which flags duplicate records
    """
    input_df = pd.DataFrame({"PatientID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                             "Age": [1, 3, 5, 10, 11, 21, 69, 70, 71, 100]
                             })

    expected_df = pd.DataFrame({"PatientID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                "Age": [1, 3, 5, 10, 11, 21, 69, 70, 71, 100],
                                "Extreme_age": [1, 1, 1, 1, 0, 0, 0, 0, 1, 1]
                                })

    actual_df = field_definitions.dq_extreme_age_flag(input_df)

    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_dq_unknown_code_flags():
    """
    Tests the dq_unknown_code_flags function, which flags use of default unknown
    codes in specified fields.
    """
    input_df = pd.DataFrame({"PatientID": [1, 2, 3, 4, 5, 6],
                             "LSOA_code": ["E01000001", "E01000002", "X99999999",
                                           "E01000187", "E01000033", "X99999999"],
                             "LA_code": ["E06000001", "X99999999", "E10000003",
                                         "E10000003", "E09000003", "X99999999"],
                             "GP_code": ["L85034", "M86002", "E81057",
                                         "V81999", "P84673", "V81999"],
                             "Ethnicity": ["A", "C", "M", "Z", "99", "99"]
                             })

    expected_df = pd.DataFrame({"PatientID": [1, 2, 3, 4, 5, 6],
                                "LSOA_code": ["E01000001", "E01000002", "X99999999",
                                              "E01000187", "E01000033", "X99999999"],
                                "LA_code": ["E06000001", "X99999999", "E10000003",
                                            "E10000003", "E09000003", "X99999999"],
                                "GP_code": ["L85034", "M86002", "E81057",
                                            "V81999", "P84673", "V81999"],
                                "Ethnicity": ["A", "C", "M", "Z", "99", "99"],
                                "Unknown_LSOA_code": [0, 0, 1, 0, 0, 1],
                                "Unknown_LA_code": [0, 1, 0, 0, 0, 1],
                                "Unknown_GP_code": [0, 0, 0, 1, 0, 1],
                                "Unknown_Ethnicity": [0, 0, 0, 0, 1, 1]
                                })

    actual_df = field_definitions.dq_unknown_code_flags(input_df)

    pd.testing.assert_frame_equal(actual_df, expected_df)
