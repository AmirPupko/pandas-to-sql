import pytest
from pandas_to_sql.testing.utils.asserters import assert_


def test_assign():
    df = pytest.df1
    df['new_value'] = df.random_float + 10
    assert_(df)


def test_assign2():
    df = pytest.df1
    df['new_value'] = df.random_bool
    assert_(df)

def test_assign3():
    df = pytest.df1
    df['new_value'] = df.random_bool
    df2 = df[['new_value','random_float']]
    assert_(df2)
