import pytest
from lib.testing.utils.asserters import assert_


def test_add():
    df = pytest.df1
    df['new_value'] = df.random_float + 10
    assert_(df)


def test_radd():
    df = pytest.df1
    df['new_value'] = 10 + df.random_float
    assert_(df)

def test_sub():
    df = pytest.df1
    df['new_value'] = df.random_float - 10
    assert_(df)