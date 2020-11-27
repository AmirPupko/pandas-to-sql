from copy import copy
import operator
from pandas_to_sql.utils.pandas_dataframe_intercepter import PandasDataFrameIntercepter
from pandas_to_sql.engine.table import create_table, Table

class PandasIntercepter:
    def __init__(self, pandas):
        self.pandas = pandas
    
    def concat(self, objs, axis=0):
        objs_pandas = list(map(lambda x: x.df_pandas, objs))
        a = self.pandas.concat(objs_pandas, axis=axis)
        objs_sql_convert = list(map(lambda x: x.df_sql_convert_table, objs))
        b = concat(objs_sql_convert, axis=axis)
        return PandasDataFrameIntercepter(a,b)


def concat(objs, axis=0):
    if axis != 0:
        raise Exception(f"supporting only axis==0")
    for df in objs:
        if not isinstance(df, Table):
            raise Exception(f'expected Table. got: {str(type(df))}')
    
    first = None
    for columns in list(map(lambda t: set(t.columns.keys()), objs)):
        if not first:
            first = columns
        else:
            if columns != first:
                raise Exception(f"expected all dataframes to have same columns")
    
    all_tables_sql_string = list(map(lambda x: x.get_sql_string(), objs))
    new_table_sql_string = ' UNION ALL '.join(all_tables_sql_string)
    return create_table(table_name='Temp',
                        columns=copy(objs[0]).columns,
                        from_sql_string=new_table_sql_string)


