
from copy import copy
import pandas as pd
import pytest
import sqlite3
from lib.Table import Table
from lib.utils.helpers import flatten_grouped_dataframe
from lib.testing.utils import fake_data_creation, dataframes_compare
import pandas_to_sql


df, df_random_columns, random_table_name = fake_data_creation.create_fake_dataset()
conn = sqlite3.connect('./example.db') #create db
df.to_sql(random_table_name, conn, if_exists='replace', index=False, dtype=df_random_columns)

def assert_for(df):
    actual_query_string = df.new_obj.get_sql_string()
    try:
        df_from_sql = pd.read_sql_query(actual_query_string, conn, parse_dates=['random_datetime'])
        dataframes_compare.assert_dataframes_equals(df.obj_to_intercept, df_from_sql)
    except Exception as e:
        print(actual_query_string)
        raise e

def test_groupby():
    df_wrapped = pandas_to_sql.wrap_df(copy(df), random_table_name)
    df2 = df_wrapped \
        .groupby('random_int') \
        .agg({'random_float':['mean','sum','count'], 'random_str':', '.join})
    df3 = flatten_grouped_dataframe(df2)
    assert_for(df3)

def test_select():
    df_wrapped = pandas_to_sql.wrap_df(copy(df), random_table_name)
    df2 = df_wrapped[['random_int', 'random_float']]
    assert_for(df2)

