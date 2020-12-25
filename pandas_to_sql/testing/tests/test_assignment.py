from datetime import datetime
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

def test_assignment_int():
    df = pytest.df1
    df['new_value2'] = 4
    assert_(df)

def test_assignment_float():
    df = pytest.df1
    df['new_value2'] = 23.132
    assert_(df)

def test_assignment_bool():
    df = pytest.df1
    df['new_value2'] = True
    assert_(df)

def test_assignment_str():
    df = pytest.df1
    df['new_value2'] = 'some_str'
    assert_(df)

def test_assignment_datetime():
    df = pytest.df1
    df['new_value'] = datetime(1970, 1, 1)
    assert_(df)
