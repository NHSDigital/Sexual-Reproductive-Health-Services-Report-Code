"""
Purpose of script: define commonly used filters for the pipeline
"""


def filter_persons_first_contact(df):
    """
    Filters a dataframe to persons based on first contact only

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df_filtered : pandas.DataFrame
        Filtered to first contacts only.

    """

    df = df[df["FirstContact"] == "Y"]

    return df


def filter_persons_main_contact(df):
    """
    Filters a dataframe to persons based on main contact in the year only

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df_filtered : pandas.DataFrame
        Filtered to persons based on main contact only.

    """
    df = df[df["MainContact"] == "Y"]

    return df


def filter_persons_main_method(df):
    """
    Filters a dataframe to persons with a contraception main method only, based
    on the main contact during the year.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df_filtered : pandas.DataFrame
        Filtered to main contacts with a main method only

    """

    df = df[(df["ContraceptiveMainMethod"] != 99) &
            (df["MainContact"] == "Y")]

    return df


def filter_contacts_main_method(df):
    """
    Filters a dataframe to contacts with a contraception main method only

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df_filtered : pandas.DataFrame
        Filtered to contacts with a main method only

    """

    df = df[df["ContraceptiveMainMethod"] != 99]

    return df


def filter_contacts_contraception(df):
    """
    Filters a dataframe to total contacts for contraception reasons

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df_filtered : pandas.DataFrame
        Filtered to total contacts for contraception reasons

    """

    df = df[(df["ContraceptiveMethodStatus"].notnull()) |
            (df["ContraceptiveMethodPostCoital1"].notnull())]

    return df


def filter_persons_contraception(df):
    """
    Filters a dataframe to persons contacting for reasons of contraception
    only. A person will only be counted once during the year.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df_filtered : pandas.DataFrame
        Filtered to persons contacting for reasons of contraception

    """

    df = df[(df["MainContact"] == "Y") &
            ((df["ContraceptiveMethodStatus"].notnull()) |
            df["ContraceptiveMethodPostCoital1"].notnull())]

    return df


def filter_females_emergency_contraception(df):
    """
    Filters a dataframe to females contacting for reasons of emergency
    contraception. A female will only be counted once during the year, with
    age at youngest contact retained. Any patients from the same organisation
    with the same patient ID are considered matching patients. LA parent is
    include to prioritise records where the LA of residence is recorded.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df_filtered : pandas.DataFrame
        Filtered to females contacting for reasons of emergency contraception

    """
    # Filter to all female records with emergency contraception
    df = df[(df["EmergencyContraceptionFlag"] == 1) & (df["Gender"] == "2")]
    # Sort so that where the same patient appears more than once, the most
    # recent version is last in the dataset. Note that patients are matched
    # based on the undedited organiation code (see apply_clinic_as_org in
    # pre-processing)
    df = df.sort_values(by=["Org_code_unedited", "PatientID", "LA_parent_code",
                            "Age", "RowNum"], ascending=False)
    # Drop all but the most recent record for each patient.
    df = df.drop_duplicates(subset=["Org_code_unedited", "PatientID"], keep="last")

    return df


def filter_vasectomies(df):
    """
    Filters a dataframe to vasectomy contacts only
    (males with srh activity code 15 applied)

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df_filtered : pandas.DataFrame
        Filtered to vasectomy contacts only.

    """
    # Set the columns to check for the relevent srh activity code
    input_columns = ["SRHCareActivity1",
                     "SRHCareActivity2",
                     "SRHCareActivity3",
                     "SRHCareActivity4",
                     "SRHCareActivity5",
                     "SRHCareActivity6"]

    # Create a filter for any records where the gender is male and the srh code
    # is present
    df = df.loc[(df[input_columns].eq(15).any(axis=1))
                & (df["Gender"] == "1")]

    return df
