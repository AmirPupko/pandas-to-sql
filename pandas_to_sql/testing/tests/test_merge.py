import pytest
from pandas_to_sql.testing.utils.asserters import assert_
from pandas_to_sql.conventions import flatten_grouped_dataframe
from copy import copy


def test_merge_inner():
    df = pytest.df1
    df2 = copy(df)
    df2['random_int_plus_3'] = df2.random_int + 3
    df2 = df2[df2.random_int < 3]
    df2 = df2[['random_int_plus_3','random_str']]
    df3 = df.merge(df2, on='random_str', how='inner')
    assert_(df3)


def test_merge_left():
    df = pytest.df1
    df2 = copy(df)
    df2['random_int_plus_3'] = df2.random_int + 3
    df2 = df2[df2.random_int < 3]
    df2 = df2[['random_int_plus_3','random_str']]
    df3 = df.merge(df2, on='random_str', how='left')
    assert_(df3)


def test_merge_left_on_right_on_how_inner():
    df = pytest.df1
    df2 = copy(df)
    df2['random_int_plus_3'] = df2.random_int + 3
    df2['random_str_2'] = df2.random_str
    df2 = df2[df2.random_int < 3]
    df2 = df2[['random_int_plus_3','random_str_2']]
    df3 = df.merge(df2, left_on='random_str', right_on='random_str_2', how='inner')
    assert_(df3)


def test_merge_left_on_right_on_how_left():
    df = pytest.df1
    df2 = copy(df)
    df2['random_int_plus_3'] = df2.random_int + 3
    df2['random_str_2'] = df2.random_str
    df2 = df2[df2.random_int < 3]
    df2 = df2[['random_int_plus_3','random_str_2']]
    df3 = df.merge(df2, left_on='random_str', right_on='random_str_2', how='left')
    assert_(df3)

