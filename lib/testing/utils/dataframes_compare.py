from pandas.testing import assert_frame_equal

def assert_dataframes_equals(expected, actual):
    assert expected.shape==actual.shape
    assert set(expected.columns) == set(actual.columns)
    columns_order = list(expected.columns)
    a = actual[columns_order].sort_values(by=list(actual.columns)).reset_index(drop=True)
    b = expected[columns_order].sort_values(by=list(actual.columns)).reset_index(drop=True)
    assert_frame_equal(a, b, check_dtype=False)