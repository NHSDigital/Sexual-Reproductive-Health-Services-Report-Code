"""
Purpose of script: define commonly used calculated/added fields for the pipeline
"""

from srh_code.utilities import helpers
import srh_code.parameters as param
import numpy as np


def create_age_groups(df, source_field,
                      group_name="Age_group", default_value="unrecorded"):
    """
    Uses group_numerical_values helper function to add the standard srh services
    age groups column to the dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
    source_field: str
        name of the column containing the single year of age values
    group_name: str
        name of the new age group column
    default_value: str
        value that will be applied to any age values that can't be assigned
        to an age group

    Returns
    -------
    df : pandas.DataFrame
        Dataframe with age group column added

    """

    age_groups = {"<16": {0: 15},
                  "16-17": {16: 17},
                  "18-19": {18: 19},
                  "20-24": {20: 24},
                  "25-34": {25: 34},
                  "35-44": {35: 44},
                  "45+": {45: 998},
                  }

    df = helpers.group_numeric_values(df, source_field, group_name,
                                      age_groups, default_value)

    return df


def create_age_groups_alt(df, source_field,
                          group_name="Age_group_alt",
                          default_value="unrecorded"):
    """
    Uses group_numerical_values helper function to add the alternate srh services
    age groups to the dataframe - includes more granular breakdown of under 16's.

    Parameters
    ----------
    df : pandas.DataFrame
    source_field: str
        name of the column containing the single year of age values
    group_name: str
        name of the new age group column
    default_value: str
        value that will be applied to any age values that can't be assigned
        to an age group

    Returns
    -------
    df : pandas.DataFrame
        Dataframe with alternate age group column added

    """

    age_groups = {"<13": {0: 12},
                  "13-14": {13: 14},
                  "15": {15: 15},
                  "16-17": {16: 17},
                  "18-19": {18: 19},
                  "20-24": {20: 24},
                  "25-34": {25: 34},
                  "35-44": {35: 44},
                  "45-54": {45: 54},
                  "55+": {55: 998},
                  }

    df = helpers.group_numeric_values(df, source_field, group_name,
                                      age_groups, default_value)

    return df


def create_age_groups_ster_vas(df, source_field,
                               group_name='Age_group',
                               default_value='unrecorded'):
    """
    Uses group_numerical_values helper function to add the sterilisation and
    vasectomy age group column to the dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
    source_field: str
        name of the column containing the single year of age values
    group_name: str
        name of the new age group column
    default_value: str
        value that will be applied to any age values that can't be assigned
        to an age group

    Returns
    -------
    df : pandas.DataFrame
        Dataframe with sterlisation and vasectomy age group column added

    """

    age_groups = {"<20": {1: 20},
                  "20-24": {20: 24},
                  "25-29": {25: 29},
                  "30-34": {30: 34},
                  "35-39": {35: 39},
                  "40-44": {40: 44},
                  "45+": {45: 998},
                  }

    df = helpers.group_numeric_values(df, source_field, group_name,
                                      age_groups, default_value)

    return df


def contraceptive_care_flags(df):
    """
    Creates new fields with flags to indicate contraceptive care activity

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df : pandas.DataFrame
        Dataframe with contraceptive care activity flags added

    """
    input_column = "ContraceptiveMethodStatus"

    df.loc[df[input_column] == 1, "MainMethodNewFlag"] = 1
    df.loc[df[input_column] == 2, "MainMethodChangeFlag"] = 1
    df.loc[df[input_column] == 3, "MainMethodMaintFlag"] = 1
    df.loc[df[input_column] == 4, "MainMethodAdviceFlag"] = 1
    df.loc[df[input_column].isin([1, 2, 3, 4]), "ContraceptiveCareFlag"] = 1

    return df


def srh_activity_flags(df):
    """
    Creates new fields with flags to indicate SRH code activity

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df : pandas.DataFrame
        Dataframe with SRH code activity flags added

    """
    input_columns = ["SRHCareActivity1",
                     "SRHCareActivity2",
                     "SRHCareActivity3",
                     "SRHCareActivity4",
                     "SRHCareActivity5",
                     "SRHCareActivity6"]

    srh_groups = param.SRH_ACTIVITY_REF

    for col_label, srh_codes in srh_groups.items():
        df[col_label] = 0
        for input_column in input_columns:
            df.loc[df[input_column].isin(srh_codes),
                   col_label] = df[col_label] + 1

    return df


def ec_oral_iud_flags(df):
    """
    Creates new fields with flags to indicate emergency oral contraception
    activity and emergency IUD contraception activity.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df : pandas.DataFrame
        Dataframe with emergency oral and emergency IUD contraception activity
        flags added.

    """
    input_columns = ["ContraceptiveMethodPostCoital1",
                     "ContraceptiveMethodPostCoital2"]

    df.loc[df[input_columns].eq(1).any(axis=1), "ECOralFlag"] = 1
    df.loc[df[input_columns].eq(2).any(axis=1), "ECIUDFlag"] = 1

    return df


def number_ec_items(df):
    """
    Creates new field with count of emergency contraception items.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df : pandas.DataFrame
        Dataframe with count of emergency contraception items added

    """
    input_columns = ["ContraceptiveMethodPostCoital1",
                     "ContraceptiveMethodPostCoital2"]

    df["Number_EC_items"] = 0
    # Adds a count of the number of the emergency contraception items
    # recorded across the input columns.
    df.loc[df[input_columns].isin([1, 2]).any(axis=1),
           "Number_EC_items"] = df[input_columns].count(axis=1)

    return df


def outside_england_flag(df):
    """
    Adds a Y (Yes) or N (No) flag to indicate if the person is resident outside
    of England to assist with filtering

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df : pandas.DataFrame

    """
    # Set to N as default
    df["Outside_england"] = "N"
    # Update to Y where applicable
    df.loc[~((df["LA_parent_code"] == "X99999999") |
           (df["LA_parent_code"].str.startswith("E12"))),
           "Outside_england"] = "Y"

    return df


def cross_boundary_check(df, clinic_la, residence_la, new_column_name):
    """
    Adds a dataframe column that identifies if the patient was resident inside
    or outside the Local Authority (LA) of the clinic location. Used to check
    at both the lower and upper tier LA level

    Parameters
    ----------
    df : pandas.DataFrame
    clinic_la: str
        Name of column that holds the LA of clinic location to be checked
    residence_la: str
        Name of column that holds the LA of patient residence to be checked
    new_column_name: str
        Name of the column that holds the added cross boundary information

    Returns
    -------
    df : pandas.DataFrame

    """

    # Assign the value by checking LA of clinic location against LA of residence
    df.loc[(df[clinic_la] == df[residence_la]),
           new_column_name] = "Inside"
    df.loc[(df[clinic_la] != df[residence_la]),
           new_column_name] = "Outside"
    # Replace with unknown where LA of residence was the not known default code
    df.loc[(df[residence_la] == "X99999999"),
           new_column_name] = "Unknown"

    return df


def dq_duplicate_flag(df):
    """
    Adds a 1 (Yes) or 0 (No) flag as a new column to indicate duplicate
    records (excluding row number, first contact, and main contact fields,
     which are all added in processing).

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df : pandas.DataFrame

    """
    # Add the dataframe column names to a list.
    all_columns = df.columns.tolist()
    # Create a list of columns to remmove from the duplicate check.
    remove_columns = ["RowNum", "FirstContact", "MainContact"]
    # Remove the columns from the all columns list to create a list of columns
    # for the duplicate check
    check_columns = [item for item in all_columns if item not in remove_columns]

    # Create a boolean flag that identifies duplicates (will not mark the first
    # version as a duplicate, only subsequent versions)
    df["Duplicate"] = df.duplicated(subset=check_columns)

    # Covert the boolean flag to a string
    df["Duplicate"] = np.where(df["Duplicate"] == True, 1, 0)

    return df


def dq_extreme_age_flag(df):
    """
    Adds a 1 (Yes) or 0 (No) flag as a new column to indicate if the patient
    age is within a ranges defined as extreme (1 to 10, or over 70) - few
    patients are expected in these age ranges.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df : pandas.DataFrame

    """
    # Set to N as default
    df["Extreme_age"] = 0
    # Update to Y where age is in extreme range (1 to 10, or over 70)
    df.loc[((df["Age"].between(1, 10)) | (df["Age"] > 70)),
           "Extreme_age"] = 1

    return df


def dq_unknown_code_flags(df):
    """
    Adds a 1 (Yes) or 0 (No) flag as a new column for each of the unknown code
    DQ checks (where the default unknown code has been applied to the record)

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df : pandas.DataFrame

    """
    # Set the columns to be checked and the unknown code value for each check
    # (as a dictionary)
    unknown_checks = {"LSOA_code": "X99999999",
                      "LA_code": "X99999999",
                      "GP_code": "V81999",
                      "Ethnicity": "99"}

    for column, code in unknown_checks.items():
        # Create the column name for the DQ check
        dq_column = "Unknown_" + column
        # Create and set DQ check column to N
        df[dq_column] = 0
        # Update to Y where the default unknown code has been used
        df.loc[df[column] == code, dq_column] = 1

    return df
