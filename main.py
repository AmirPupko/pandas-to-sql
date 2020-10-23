import sqlite3
import os
import numpy as np
import pandas as pd
from copy import copy
from lib.Table import Table
import pandas_to_sql

df_random_columns = {
    'random_int': 'INT',
    'random_float': 'FLOAT',
    'random_bool': 'BOOL',
    'random_datetime': 'TIMESTAMP',
    'random_str': 'VARCHAR',
}

def foo(df1, df2):
    return df1[['random_int', 'random_float']].merge(
        df2[['random_int','random_str']],
        on='random_int',
        how='inner')

table = {'table_name': 'random_table_name', 
        'schema': df_random_columns}
print(pandas_to_sql.get([table, table], foo))
