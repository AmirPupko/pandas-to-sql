import pytest
from pandas_to_sql.testing.utils.asserters import assert_
from pandas_to_sql.utils.helpers import flatten_grouped_dataframe
from copy import copy
import pandas as pd
import pandas_to_sql 


# def test_add_hours():
#     df = pytest.df1
#     df['new_value'] = df.random_datetime + pd.DateOffset(hours=16)
#     assert_(df)

