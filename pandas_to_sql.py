from copy import copy
from lib.table import Table
from lib.utils.helpers import  create_schema_from_df
from lib.utils.pandas_dataframe_intercepter import PandasDataFrameIntercepter
from lib.utils.pandas_interceptor import PandasIntercepter


def wrap_df(df, table_name):
    t = Table(table_name, column_dtype_map=create_schema_from_df(df))
    return PandasDataFrameIntercepter(copy(df), copy(t))

def wrap_pd(pd):
    return PandasIntercepter(pd)