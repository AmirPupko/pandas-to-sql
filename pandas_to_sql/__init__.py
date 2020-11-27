from pandas_to_sql.engine.table import create_table_from_schema
from pandas_to_sql.utils.helpers import  create_schema_from_df
from pandas_to_sql.utils.pandas_dataframe_intercepter import PandasDataFrameIntercepter
from pandas_to_sql.utils.pandas_interceptor import PandasIntercepter


def wrap_df(df, table_name):
    t = create_table_from_schema(table_name=table_name, schema=create_schema_from_df(df))
    return PandasDataFrameIntercepter(df, t)


def wrap_pd(pd):
    return PandasIntercepter(pd)