import pytest
from lib.testing.utils.asserters import assert_
from lib.utils.helpers import flatten_grouped_dataframe
from copy import copy
import pandas as pd
import pandas_to_sql 

def test_concat_simple():
    df = pytest.df1

    pd_wrapped = pandas_to_sql.wrap_pd(pd)

    df2 = pd_wrapped.concat([df, df, df])

    assert_(df2)


def test_concat_simple_with_copy():
    df = pytest.df1

    pd_wrapped = pandas_to_sql.wrap_pd(pd)

    df2 = pd_wrapped.concat([df, copy(df), copy(df)])

    assert_(df2)

