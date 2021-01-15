import pandas as pd
from pandas_to_sql.utils.pandas_dataframe_intercepter import PandasDataFrameIntercepter
from copy import copy

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
