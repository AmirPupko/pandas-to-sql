import pytest
from lib.testing.utils.asserters import assert_
from copy import copy

def test_copy():
    df = pytest.df1
    df2 = copy(df)
    df['new_value'] = df.random_float > 10  # some unrelated operation
    assert_(df2)
