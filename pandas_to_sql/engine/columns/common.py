
import numbers
import operator
from pandas_to_sql.engine.columns.column import Column


def get_column_class_from_type(col_type):
    from pandas_to_sql.engine.columns.bool_column import BoolColumn
    from pandas_to_sql.engine.columns.numeric_columns import IntColumn, FloatColumn
    from pandas_to_sql.engine.columns.str_column import StrColumn
    from pandas_to_sql.engine.columns.timestamp_column import TimestampColumn
    if col_type == 'BOOL': return BoolColumn
    elif col_type == 'INT': return IntColumn
    elif col_type == 'FLOAT': return FloatColumn
    elif col_type == 'VARCHAR': return StrColumn
    elif col_type == 'TIMESTAMP': return TimestampColumn
    else: raise Exception(f"could not convert column type. got: {str(col_type)}")


def value_to_sql_string(value):
    if isinstance(value, numbers.Number):
        return str(value)
    elif isinstance(value, str):
        return "'" + value + "'"
    elif isinstance(value, Column):
        return value.sql_string
    raise Exception(f"Value not supported. supporting: premitives and {str(Column)}. got {str(type(value))}")


def create_column_from_operation(l, r, dtype, op):
    return dtype(sql_string=f'({value_to_sql_string(l)} {op} {value_to_sql_string(r)})')  


def add_comparison_operators_to_class(class_type):
    from pandas_to_sql.engine.columns.bool_column import BoolColumn

    def __lt__(self,other):
        return create_column_from_operation(self, other, BoolColumn, '<')

    def __le__(self,other):
        return create_column_from_operation(self, other, BoolColumn, '<=')

    def __gt__(self,other):
        return create_column_from_operation(self, other, BoolColumn, '>')

    def __ge__(self,other):
        return create_column_from_operation(self, other, BoolColumn, '>=')

    def __eq__(self,other):
        return create_column_from_operation(self, other, BoolColumn, '=')

    def __ne__(self,other):
        return create_column_from_operation(self, other, BoolColumn, '<>')

    class_type.__lt__ = __lt__
    class_type.__gt__ = __gt__
    class_type.__le__ = __le__
    class_type.__ge__ = __ge__
    class_type.__eq__ = __eq__
    class_type.__ne__ = __ne__
