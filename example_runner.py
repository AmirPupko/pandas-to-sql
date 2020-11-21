from copy import copy
import pandas_to_sql
from pandas_to_sql.testing.utils.fake_data_creation import create_fake_dataset
from pandas_to_sql.utils.helpers import flatten_grouped_dataframe

table_name = 'random_data'
df, _ = create_fake_dataset()
df_ = pandas_to_sql.wrap_df(df, table_name)
df2 = df_.groupby('random_int').agg({'random_float':['mean','sum','count'], 'random_str':', '.join})
df2 = flatten_grouped_dataframe(df2)
print(df2.get_sql_string())
