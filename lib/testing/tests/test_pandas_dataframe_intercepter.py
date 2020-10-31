import pytest
from lib.testing.conftest import TABLE_NAME_1

def test_columns_attribute():
    expected = pytest.df1.df_pandas.columns
    actual = pytest.df1.columns
    assert type(expected) == type(actual)
    assert set(expected) == set(actual)


def test_get_sql_string_attribute():
    expected = '''SELECT (random_int) AS 'random_int', (random_float) AS 'random_float', (random_bool) AS 'random_bool', (random_datetime) AS 'random_datetime', (random_str) AS 'random_str' FROM random_data_1'''
    assert expected == pytest.df1.get_sql_string()