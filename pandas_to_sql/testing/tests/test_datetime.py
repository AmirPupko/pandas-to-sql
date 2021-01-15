from datetime import timedelta, datetime
import pytest
from pandas_to_sql.testing.utils.asserters import assert_, get_expected_and_actual
from pandas_to_sql.utils.helpers import flatten_grouped_dataframe
from copy import copy
import pandas as pd
import pandas_to_sql 


def test_add_days():
    df = pytest.df1
    df['new_value'] = df.random_datetime + timedelta(days=20)
    assert_(df)

def test_radd_days():
    df = pytest.df1
    df['new_value'] = timedelta(days=40) + df.random_datetime
    assert_(df)

def test_sub_days():
    df = pytest.df1
    df['new_value'] = df.random_datetime - timedelta(days=40)
    assert_(df)


def test_add_zero_time_dateoffset():
    df = pytest.df1
    df['new_value'] = df.random_datetime + pd.offsets.DateOffset(minutes=0, years=0)
    assert_(df)


def test_dt_second():
    df = pytest.df1
    df['seconds'] = df.random_datetime.dt.second
    assert_(df)

def test_dt_month():
    df = pytest.df1
    df['month'] = df.random_datetime.dt.month
    assert_(df)

def test_dt_day():
    df = pytest.df1
    df['day'] = df.random_datetime.dt.day
    assert_(df)

def test_dt_hour():
    df = pytest.df1
    df['hour'] = df.random_datetime.dt.hour
    assert_(df)

def test_dt_year():
    df = pytest.df1
    df['y'] = df.random_datetime.dt.year
    assert_(df)

def test_dt_dayofweek():
    df = pytest.df1
    df['dayofweek'] = df.random_datetime.dt.dayofweek
    assert_(df)

def test_dt_week():
    df = pytest.df1
    df['week'] = df.random_datetime.dt.week
    df_expected, df_actual = get_expected_and_actual(df)

    week_diff = (df_expected.week - df_actual.week).value_counts()

    # asserting week error <= 2. 52,53 is modulo
    assert (df_expected.week - df_actual.week).isin([0,1,2,52,53]).all()
