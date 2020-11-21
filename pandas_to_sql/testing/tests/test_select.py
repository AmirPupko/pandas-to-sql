import pytest
from pandas_to_sql.testing.utils.asserters import assert_


def test_select_inline():
    assert_(pytest.df1[['random_int', 'random_float']])


def test_select_not_inline():
    df = pytest.df1[['random_int', 'random_float']]
    assert_(df)


def test_select_multiple_times():
    df = pytest.df1[['random_int', 'random_datetime','random_bool']]
    df = df[['random_datetime']]
    assert_(df)
