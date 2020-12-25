import pandas as pd
from pandas.testing import assert_frame_equal
import pytest


def assert_dataframes_equals(expected, actual):
    assert expected.shape==actual.shape
    assert set(expected.columns) == set(actual.columns)
    columns_order = list(expected.columns)
    a = actual[columns_order].sort_values(by=list(actual.columns)).reset_index(drop=True)
    e = expected[columns_order].sort_values(by=list(actual.columns)).reset_index(drop=True)
    assert_frame_equal(e, a, check_dtype=False)

def assert_(df):
    actual_query_string = df.df_sql_convert_table.get_sql_string()
    actual_columns = df.df_sql_convert_table.columns
    timestamp_columns = [c for c in actual_columns.keys() if actual_columns[c].dtype == 'TIMESTAMP']
    try:
        df_actual = pd.read_sql_query(actual_query_string, pytest.sql_connection, parse_dates=timestamp_columns)
        df_expected = df.df_pandas
        assert_dataframes_equals(df_expected, df_actual)
    except Exception as e:
        # print(actual_query_string)
        raise e