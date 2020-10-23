
from copy import copy
import pandas as pd
import pytest
import sqlite3
from lib.Table import Table
from lib.helpers import flatten_grouped_dataframe
from lib.testing.utils import fake_data_creation, dataframes_compare


def get(tables, datamrames_manipulation_func):
    args = []
    for table in tables:
        args.append(Table(table['table_name'], column_dtype_map=table['schema']))
    return datamrames_manipulation_func(*args).get_sql_string()
