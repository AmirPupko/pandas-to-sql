
from copy import copy
import sqlite3
import pytest
from pandas_to_sql import wrap_df
from pandas_to_sql.testing.utils import fake_data_creation

sql_connection = sqlite3.connect('./example.db') #create db

TABLE_NAME_1 = 'random_data_1'
DF1, SCHEMA_1 = fake_data_creation.create_fake_dataset()
DF1.to_sql(TABLE_NAME_1, sql_connection, if_exists='replace', index=False, dtype=SCHEMA_1)

TABLE_NAME_2 = 'random_data_2'
DF2, SCHEMA_2 = fake_data_creation.create_fake_dataset()
DF2.columns = DF2.columns.map(lambda c: c + '_2')
DF2.to_sql(TABLE_NAME_2, sql_connection, if_exists='replace', index=False, dtype=SCHEMA_2)

def pytest_configure():
    pytest.df1 = None
    pytest.df2 = None
    pytest.sql_connection = sql_connection

@pytest.fixture(scope="function", autouse=True)
def run_around_tests():
    # print('\nhere\n')
    pytest.df1 = wrap_df(copy(DF1), TABLE_NAME_1)
    pytest.df2 = wrap_df(copy(DF2), TABLE_NAME_2)
    yield
    # run after function
