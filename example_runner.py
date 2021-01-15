from copy import copy
import sqlite3
import pandas as pd
import pandas_to_sql
from pandas_to_sql.testing.utils.fake_data_creation import create_fake_dataset
from pandas_to_sql.conventions import flatten_grouped_dataframe

# table_name = 'random_data'
# df, _ = create_fake_dataset()
# df_ = pandas_to_sql.wrap_df(df, table_name)
# df2 = df_.groupby('random_int').agg({'random_float':['mean','sum','count'], 'random_str':', '.join})
# df2 = flatten_grouped_dataframe(df2)
# print(df2.get_sql_string())

iris = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')
table_name = 'iris'
sql_connection = sqlite3.connect('./iris.db') #create db
iris.to_sql(table_name, sql_connection, if_exists='replace', index=False)

df = pandas_to_sql.wrap_df(iris, table_name)
pd_wrapped = pandas_to_sql.wrap_pd(pd)

df_ = copy(df)
df_['sepal_width_rounded'] = df_.sepal_width.round()
df_1 = df_[df_.species=='setosa'].reset_index(drop=True)
df_2 = df_[df_.species=='versicolor'].reset_index(drop=True)

some_df = pd_wrapped.concat([df_1, df_2]).reset_index(drop=True)

sql_string = some_df.get_sql_string()

df_from_sql_database = pd.read_sql_query(sql_string, sql_connection)
df_pandas = some_df.df_pandas

from pandas_to_sql.testing.utils.asserters import assert_dataframes_equals
assert_dataframes_equals(df_pandas, df_from_sql_database)
