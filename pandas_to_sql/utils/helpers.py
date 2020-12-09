import pandas as pd
from pandas_to_sql.engine.table import Table
from pandas_to_sql.engine.grouped_table import GroupedTable
from pandas_to_sql.utils.pandas_dataframe_intercepter import PandasDataFrameIntercepter
from copy import copy

## Conventions
def flatten_grouped_dataframe(df):
    if not isinstance(df, PandasDataFrameIntercepter):
        raise Exception(f"can only get type {str(type(PandasDataFrameIntercepter))}")
    
    df_c = copy(df.df_pandas)
    if isinstance(df_c, pd.core.series.Series):
        series_name = df_c.name
        new_col_name = list(filter(lambda k: k.startswith(series_name), df.df_sql_convert_table.columns.keys()))[0]
        df_c = df_c.reset_index().rename(columns={series_name: new_col_name})
    else:
        df_c.columns = df_c.columns.map('_'.join)
        df_c = df_c.reset_index()
    return PandasDataFrameIntercepter(df_c, copy(df.df_sql_convert_table))


## Types
def convert_df_type(col_type):
    if pd.api.types.is_bool_dtype(col_type): return 'BOOL'
    elif pd.api.types.is_integer_dtype(col_type): return 'INT'
    elif pd.api.types.is_numeric_dtype(col_type): return 'FLOAT'
    elif pd.api.types.is_string_dtype(col_type): return 'VARCHAR'
    elif pd.api.types.is_datetime64_any_dtype(col_type): return 'TIMESTAMP'
    else: raise Exception(f"could not convert column type. got: {str(col_type)}")


def create_schema_from_df(df):        
    schema = {}
    for col_name, col_type in df.dtypes.items():
        schema[col_name] = convert_df_type(col_type)
    return schema