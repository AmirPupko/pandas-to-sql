import pytest
from pandas_to_sql.testing.utils.asserters import assert_
from pandas_to_sql.utils.helpers import flatten_grouped_dataframe



def test_groupby_mean():
    df2 = pytest.df1.groupby('random_int').random_float.mean()
    assert_(flatten_grouped_dataframe(df2))

def test_groupby_sum():
    df2 = pytest.df1.groupby('random_int').random_float.sum()
    assert_(flatten_grouped_dataframe(df2))

def test_groupby_count():
    df2 = pytest.df1.groupby('random_int').random_float.count()
    assert_(flatten_grouped_dataframe(df2))


def test_groupby_agg_1():
    df2 = pytest.df1 \
        .groupby('random_int') \
        .agg({'random_float':['mean','sum','count'], 'random_str':', '.join})
    assert_(flatten_grouped_dataframe(df2))

def test_groupby_agg_2():
    df2 = pytest.df1 \
        .groupby('random_bool') \
        .agg({'random_int':['mean','sum','count'], 'random_str':[', '.join]})
    assert_(flatten_grouped_dataframe(df2))


def test_groupby_multiple_on():
    df2 = pytest.df1 \
        .groupby(['random_bool', 'random_int']).random_float.mean()
    assert_(flatten_grouped_dataframe(df2))

def test_groupby_multiple_on_agg():
    df2 = pytest.df1 \
        .groupby(['random_bool', 'random_int']) \
        .agg({'random_float': ['count','sum']})
    assert_(flatten_grouped_dataframe(df2))