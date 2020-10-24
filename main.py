from copy import copy
import pandas_to_sql
from lib.testing.utils.fake_data_creation import create_fake_dataset

df, _, random_table_name = create_fake_dataset()
df_ = pandas_to_sql.wrap_df(df, random_table_name)
df2 = df_.groupby('random_int').agg({'random_float':['mean','sum','count'], 'random_str':', '.join})
print(df2.new_obj.get_sql_string())
