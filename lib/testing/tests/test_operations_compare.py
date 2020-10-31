import pytest
from lib.testing.utils.asserters import assert_


def test_gt1():
    df = pytest.df1
    df['new_value'] = df.random_float > 10
    assert_(df)

def test_gt2():
    df = pytest.df1
    df['new_value'] = df.random_int > 3
    assert_(df)

def test_abs():
    df = pytest.df1
    df['new_value'] = abs(df.random_float)
    assert_(df)

def test_ge():
    df = pytest.df1
    df['new_value'] = df.random_int >= 3
    assert_(df)

def test_ge():
    df = pytest.df1
    df['new_value'] = df.random_float >= 0
    assert_(df)

def test_ge2():
    df = pytest.df1
    df['new_value'] = df.random_int >= 3
    assert_(df)

def test_lt():
    df = pytest.df1
    df['new_value'] = df.random_int < 3
    assert_(df)

def test_le():
    df = pytest.df1
    df['new_value'] = df.random_int <= 3
    assert_(df)

def test_eq():
    df = pytest.df1
    df['new_value'] = df.random_int == 3
    assert_(df)

def test_ne():
    df = pytest.df1
    df['new_value'] = df.random_int != 3
    assert_(df)