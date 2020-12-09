from pandas_to_sql.engine.columns.column import Column
from pandas_to_sql.engine.columns.common import value_to_sql_string, add_comparison_operators_to_class


class BoolColumn(Column):
    def __init__(self, sql_string):
        super().__init__(dtype='BOOL', sql_string=sql_string)
    
    def __neg__(self):
        return BoolColumn(sql_string=f'(NOT({value_to_sql_string(self)}))')

    def __invert__(self):
        return BoolColumn(sql_string=f'(NOT({value_to_sql_string(self)}))')


add_comparison_operators_to_class(BoolColumn)