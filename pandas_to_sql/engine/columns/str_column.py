from pandas_to_sql.engine.columns.column import Column
from pandas_to_sql.engine.columns.common import add_comparison_operators_to_class, value_to_sql_string, create_column_from_operation


class StrColumn(Column):
    def __init__(self, sql_string):
        super().__init__(dtype='VARCHAR', sql_string=sql_string)
        
    def __add__(self, r):
        return create_column_from_operation(self, r, StrColumn, '||')

    def __radd__(self, l):
        return create_column_from_operation(self, StrColumn, l, '||')


add_comparison_operators_to_class(StrColumn)
