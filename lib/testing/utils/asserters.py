import pandas as pd
import pytest
from lib.testing.utils import dataframes_compare


def assert_(df):
    actual_query_string = df.df_sql_convert_table.get_sql_string()
    try:
        df_actual = pd.read_sql_query(actual_query_string, pytest.sql_connection, parse_dates=['random_datetime'])
        df_expected = df.df_pandas
        dataframes_compare.assert_dataframes_equals(df_expected, df_actual)
    except Exception as e:
        print(actual_query_string)
        raise e