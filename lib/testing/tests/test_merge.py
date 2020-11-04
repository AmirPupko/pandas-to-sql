import pytest
from lib.testing.utils.asserters import assert_
from lib.utils.helpers import flatten_grouped_dataframe
from copy import copy


def test_merge_simple():
    df = pytest.df1
    df2 = copy(df)
    df2['random_int_plus_3'] = df2.random_int + 3
    df2 = df2[['random_int_plus_3','random_str']]
    df3 = df.merge(df2, on='random_str', how='inner')
    assert_(df3)
