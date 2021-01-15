from datetime import timedelta, datetime
import pytest
from pandas_to_sql.testing.utils.asserters import assert_, get_expected_and_actual
from copy import copy
import pandas as pd
import pandas_to_sql 


def test_replace():
    df = pytest.df1
    df['new_value'] = df.random_str.str.replace('m','v').str.replace('z','_3')
    assert_(df)

def test_lower():
    df = pytest.df1
    df['new_value'] = df.random_str.str.lower()
    assert_(df)

def test_upper():
    df = pytest.df1
    df['new_value'] = df.random_str.str.upper()
    assert_(df)

def test_slice1():
    df = pytest.df1
    df['new_value'] = df.random_str.str.slice(1,3)
    assert_(df)

def test_slice2():
    df = pytest.df1
    df['new_value'] = df.random_str.str.slice(2)
    assert_(df)

def test_slice3():
    df = pytest.df1
    df['new_value'] = df.random_str.str.slice(stop=4)
    assert_(df)

def test_slice4():
    df = pytest.df1
    df['new_value'] = df.random_str.str.slice(-1,-3)
    assert_(df)

def test_strip():
    df = pytest.df1
    df['new_value'] = df.random_str.str.strip('ABCKSLFjadkj')
    assert_(df)

def test_strip_none_chars():
    df = pytest.df1
    df['new_value1'] = df.random_str + ' '
    df['new_value2'] = df.random_str.str.strip()
    assert_(df)

def test_lstrip():
    df = pytest.df1
    df['new_value'] = df.random_str.str.lstrip('ABCKSLFjadkj')
    assert_(df)


def test_rstrip():
    df = pytest.df1
    df['new_value'] = df.random_str.str.rstrip('ABCKSLFjadkj')
    assert_(df)

def test_len():
    df = pytest.df1
    df['new_value'] = df.random_str.str.len()
    assert_(df)

def test_contains():
    df = pytest.df1
    df['new_value1'] = df.random_str.str.contains('a')
    df['new_value2'] = df.random_str.str.contains('B')
    assert_(df)

def test_contains_case_false():
    df = pytest.df1
    df['new_value1'] = df.random_str.str.contains('a', case=False)
    df['new_value2'] = df.random_str.str.contains('B', case=False)
    assert_(df)