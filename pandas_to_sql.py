from lib.table import create_table_from_schema
from lib.utils.helpers import  create_schema_from_df
from lib.utils.pandas_dataframe_intercepter import PandasDataFrameIntercepter
from lib.utils.pandas_interceptor import PandasIntercepter


def wrap_df(df, table_name):
    t = create_table_from_schema(table_name=table_name, schema=create_schema_from_df(df))
    return PandasDataFrameIntercepter(df, t)


def wrap_pd(pd):
    return PandasIntercepter(pd)