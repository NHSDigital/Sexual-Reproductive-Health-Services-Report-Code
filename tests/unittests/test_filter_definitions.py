import pandas as pd
import numpy as np
from srh_code.utilities import filter_definitions


def test_filter_vasectomies():
    """
    Tests the filter_vasectomies function, which filters the dataframe to male
    contacts where SRH sctivity code 15 has been applied.
    """
    input_df = pd.DataFrame({"Gender": ["1", "1", "1", "1", "2", "2", "99"],
                             "SRHCareActivity1": [15, 1, 1, 1, 15, 3, 2],
                             "SRHCareActivity2": [1, 15, 3, 3, 10, 8, 1],
                             "SRHCareActivity3": [np.nan, np.nan, np.nan,
                                                  12, 15, 18, 3],
                             "SRHCareActivity4": [np.nan, np.nan, np.nan,
                                                  15, np.nan, 7,
                                                  1],
                             "SRHCareActivity5": [np.nan, np.nan, np.nan,
                                                  np.nan, np.nan, np.nan,
                                                  15],
                             "SRHCareActivity6": [np.nan, np.nan, np.nan,
                                                  np.nan, np.nan, np.nan,
                                                  np.nan]
                             })

    expected_df = pd.DataFrame({"Gender": ["1", "1", "1"],
                                "SRHCareActivity1": [15, 1, 1],
                                "SRHCareActivity2": [1, 15, 3],
                                "SRHCareActivity3": [np.nan, np.nan, 12],
                                "SRHCareActivity4": [np.nan, np.nan, 15],
                                "SRHCareActivity5": [np.nan, np.nan, np.nan],
                                "SRHCareActivity6": [np.nan, np.nan, np.nan]
                                })

    actual_df = filter_definitions.filter_vasectomies(input_df)

    pd.testing.assert_frame_equal(actual_df.reset_index(drop=True),
                                  expected_df.reset_index(drop=True))
