
from copy import copy
import pandas as pd
import pytest
import sqlite3
from lib.Table import Table
from lib.helpers import flatten_grouped_dataframe
from lib.testing.utils import fake_data_creation, dataframes_compare
import pandas_to_sql


df, df_random_columns, random_table_name = fake_data_creation.create_fake_dataset()
conn = sqlite3.connect('./example.db') #create db
df.to_sql(random_table_name, conn, if_exists='replace', index=False, dtype=df_random_columns)

table = {'table_name': 'random_data', 
        'schema': df_random_columns}

def assert_for(df_manipulation_func):
    expected = df_manipulation_func(copy(df))
    actual_query_string = pandas_to_sql.get([table], df_manipulation_func)
    try:
        actual = pd.read_sql_query(
            actual_query_string, 
            conn,
            parse_dates=['random_datetime'])
        dataframes_compare.assert_dataframes_equals(expected, actual)
    except Exception as e:
        print(actual_query_string)
        raise e

def test_groupby():
    def __test(df):
        df2 = df.groupby('random_int').agg({'random_float':['mean','sum','count'], 'random_str':', '.join})
        return df
    assert_for(__test)

def test_select():
    def __test(df):
        return df[['random_int', 'random_float']]
    assert_for(__test)
