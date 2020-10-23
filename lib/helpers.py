from lib.Table import Table
from lib.Column import Column
from lib.GroupedTable import GroupedTable

def flatten_grouped_dataframe(df):
    if isinstance(df, Table) or isinstance(df, GroupedTable) or isinstance(df, Column):
        return df
    df_c = df.copy()
    df_c.columns = df_c.columns.map('_'.join)
    return df_c.reset_index()
