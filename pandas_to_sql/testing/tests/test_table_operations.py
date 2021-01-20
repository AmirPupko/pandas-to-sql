from datetime import datetime
import pytest
from pandas_to_sql.testing.utils.asserters import assert_


def test_rename():
    df = pytest.df1
    df = df.rename(columns={'random_int': 'random_int_2',
                            'random_str': 'random_str_2'})
    assert_(df)

def test_drop():
    df = pytest.df1
    df = df.drop(columns=['random_int', 'random_str'])
    assert_(df)
