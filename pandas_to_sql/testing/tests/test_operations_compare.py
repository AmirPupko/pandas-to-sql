import pandas as pd
import pytest
from pandas_to_sql import wrap_df
from pandas_to_sql.testing.utils.asserters import assert_


def test_gt1():
    df = pytest.df1
    df['new_value'] = df.random_float > 10
    assert_(df)

def test_gt2():
    df = pytest.df1
    df['new_value'] = df.random_int > 3
    assert_(df)

def test_abs_float():
    df = pytest.df1
    df['new_value'] = abs(df.random_float)
    assert_(df)

def test_abs_int():
    df = pytest.df1
    df['new_value'] = abs(df.random_int)
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

def test_tilde():
    df = pytest.df1
    df['new_value'] = ~df.random_bool
    assert_(df)

def test_neg_bool():
    df = pytest.df1
    df['new_value'] = -df.random_bool
    assert_(df)

def test_neg_numeric():
    df = pytest.df1
    df['new_value'] = -df.random_int
    assert_(df)


def test_two_conds_and():
    df = pytest.df1
    df['new_value'] = (df.random_float > 1) & (df.random_float <=2)
    assert_(df)

def test_two_conds_or():
    df = pytest.df1
    df['new_value'] = (df.random_float > 1) or True
    assert_(df)

def test_fillna():
    df = pd.DataFrame({'col':[1,None,.3,-20,None]})
    table_name = 'some_fillna_table_name'
    df.to_sql(table_name, pytest.sql_connection, if_exists='replace', index=False)
    df_ = wrap_df(df, table_name)

    df_['new_value'] = df_.col.fillna(2)
    
    assert_(df_)

def test_fillna2():
    df = pd.DataFrame({'col':[1,None,.3,-20,None]})
    table_name = 'some_fillna_table_name'
    df.to_sql(table_name, pytest.sql_connection, if_exists='replace', index=False)
    df_ = wrap_df(df, table_name)

    df_['new_value'] = df_.col.fillna('f')
    
    assert_(df_)

def test_astype():
    df = pytest.df1
    df['new_value'] = df.random_float.astype(int)
    assert_(df)

