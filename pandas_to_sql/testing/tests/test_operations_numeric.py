import pytest
from pandas_to_sql.testing.utils.asserters import assert_


def test_add():
    df = pytest.df1
    df['new_value'] = df.random_float + 10
    assert_(df)

def test_radd():
    df = pytest.df1
    df['new_value'] = 10 + df.random_float
    assert_(df)

def test_add_str():
    df = pytest.df1
    df['new_value'] = df.random_str + '_some_other_str'
    assert_(df)

def test_add_str_to_str():
    df = pytest.df1
    df['new_value'] = df.random_str + '_' + df.random_str
    assert_(df)


def test_sub():
    df = pytest.df1
    df['new_value'] = df.random_float - 10
    assert_(df)

def test_rsub():
    df = pytest.df1
    df['new_value'] = 10 - df.random_float
    assert_(df)


def test_mul():
    df = pytest.df1
    df['new_value'] = df.random_float * 2
    assert_(df)

def test_rmul():
    df = pytest.df1
    df['new_value'] = 2.5 * df.random_int
    assert_(df)

def test_truediv():
    df = pytest.df1
    df['new_value'] = df.random_int / 2.0
    assert_(df)

def test_truediv2():
    df = pytest.df1
    df['new_value'] = df.random_float / 2
    assert_(df)

def test_truediv_int_int():
    df = pytest.df1
    df['new_value'] = df.random_int / 2
    assert_(df)

def test_rtruediv():
    df = pytest.df1
    df['new_value'] = 2 / df.random_float
    assert_(df)

def test_floordiv():
    df = pytest.df1
    df['new_value'] = df.random_float // 2.0
    assert_(df)

def test_rfloordiv():
    df = pytest.df1
    df['new_value'] = 1 // df.random_float
    assert_(df)